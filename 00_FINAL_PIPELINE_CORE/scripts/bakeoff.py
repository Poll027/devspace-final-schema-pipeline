#!/usr/bin/env python3
"""Model bake-off for the Final Schema pipeline: measure candidate models on finished Data Analyst content before trusting them with new paths.

  bakeoff.py eval-test MODEL[:flex] ...     Evaluator quality (about $1-3 in total). Seeds 11 known defects into copies of 3 gated tiles (plus one
                                            untouched control tile), renders the same evaluator packets the driver uses, asks each model to judge
                                            them, and reports which seeded defects it flagged BLOCKING and what it flagged on the clean control.
  bakeoff.py setup NAME --bundle F --toc D  Generator cost/quality. Creates batches/tmp_bakeoff_NAME with 5 finished tiles (SQL, Python, spreadsheet,
                                            chart, no-code) to regenerate from scratch. Then run the normal driver on it, e.g.
                                              GEN_LADDER=DeepSeek-V4.1-Flash EVAL_LADDER=gpt-6.1-sol LLM_SERVICE_TIER=flex \\
                                              python3 run_pipeline.py batches/tmp_bakeoff_NAME --max-usd 15
  bakeoff.py report NAME ...                Per batch: how far it got, evaluator rounds, calls, tokens and cost per tile.

A seeded defect counts as caught when a BLOCKING line of the model's reply names its step. That match is approximate: read the saved replies
(batches/tmp_bakeoff_eval/replies/) before deciding anything on a close result.
# ponytail: the seeded defects are hand-written for three tiles of final_batch_003; if those tiles are regenerated the seeds must be re-aimed.
"""
import argparse
import collections
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bedrock_llm as BL  # noqa: E402
import evaluator_packet as EP  # noqa: E402
from finlib import ROOT, load, save  # noqa: E402

GOLD = ROOT / "batches" / "final_batch_003_da_chunk"
T1, T2, T3, CONTROL = "tile_datamodel_foreign_keys_one_to_many", "tile_stats_correlation", "tile_stakeholder_tailoring_anticipating", "tile_datamodel_entities_keys"
GEN_TILES = ["tile_sql_case_expressions", "tile_python_file_io", "tile_spreadsheet_grid_references", "tile_viz_custom_multi_panel", "tile_datamodel_entities_keys"]
EXP = ROOT / "batches" / "tmp_bakeoff_eval"  # batches/tmp_* is gitignored


# ---------- seeded defects (evaluator-only: every one still passes the deterministic gates)
def seed_defects(lessons_dir):
    truth = []

    def step(L, suffix, remediation=False):
        return next(s for s in (L["remediation_steps"] if remediation else L["steps"]) if s["step_id"].endswith(suffix))

    def sub_text(L, suffix, old, new, remediation=False):
        hits = [b for b in step(L, suffix, remediation).get("blocks", []) if b["type"] in ("prose", "callout") and old in b["text"]]
        assert len(hits) == 1, (suffix, old, len(hits))
        hits[0]["text"] = hits[0]["text"].replace(old, new, 1)

    def seed(tile, did, klass, where, desc):
        truth.append({"id": did, "tile": tile, "step": where, "class": klass, "what_was_done": desc})

    L = load(lessons_dir / f"{T1}.json")
    sub_text(L, ".s01", "referenced table. orders.customer_id", "referenced table, and the database always rejects any change that would break the match. orders.customer_id")
    seed(T1, "D1", "overstated claim", "s01", "FK definition now says the database always rejects any change that would break the match")
    ix = step(L, ".s03")["interaction"]
    for o in ix["public"]["options"]:
        if o["option_id"] == "opt_duplicate":
            o["text"] = "A dangling foreign key row — it violates referential integrity because the value 99 has no matching primary key in customers"
    ix["grading"]["option_feedback"]["opt_duplicate"]["message"] = "Not quite. The correct label is orphan record."
    seed(T1, "D2", "second defensible answer", "s03", "wrong option opt_duplicate rewritten into a paraphrase of the correct answer")
    step(L, ".s07")["interaction"]["grading"]["option_feedback"]["opt_both"]["message"] = \
        "Not quite. Placing it in both tables would break the database engine, which cannot store the same column name in two different tables."
    seed(T1, "D3", "false wrong-option feedback", "s07", "opt_both feedback states a false reason")
    for tk in step(L, ".s08")["interaction"]["public"]["tasks"]:
        if tk["task_id"] == "task_many_side_evidence":
            tk["prompt"] = "Select a row that an INNER JOIN of orders to customers would pair with the same customer as order 101 — evidence that orders is the many side of the relationship."
    seed(T1, "D4", "needs a later concept (leakage)", "s08", "task prompt now relies on INNER JOIN, a blocked future concept")
    save(lessons_dir / f"{T1}.json", L)

    L = load(lessons_dir / f"{T2}.json")
    sub_text(L, ".s07", "slightly stronger", "far stronger")
    seed(T2, "D5", "overstated claim (numeric)", "s07", "'slightly stronger' -> 'far stronger' for |-0.41| vs |-0.38|")
    for tk in step(L, ".s06")["interaction"]["public"]["tasks"]:
        if tk["task_id"] == "task_weakest_pair":
            tk["prompt"] = "Select the cell showing the most negative correlation between any two different variables (excluding the diagonal)."
    seed(T2, "D6", "answer key wrong for the question asked", "s06", "task asks for the MOST NEGATIVE value but the key is still -0.38 (the most negative is -0.41)")
    step(L, ".s05")["interaction"]["grading"]["option_feedback"]["opt_weak"]["message"] = \
        "Not quite. A correlation near 0 always means the relationship is weak, but the scatter plot shows a clear pattern, so recheck the data."
    seed(T2, "D7", "false wrong-option feedback", "s05", "feedback asserts 'near 0 always means weak', contradicting the taught linear-only limit")
    save(lessons_dir / f"{T2}.json", L)

    L = load(lessons_dir / f"{T3}.json")
    sub_text(L, ".s02", "An executive audience might only want the high-level arc:", "An executive audience only ever wants the high-level arc and will disengage at the first technical detail:")
    seed(T3, "D8", "overstated claim (hedge upgraded)", "s02", "'might only want' -> 'only ever wants ... will disengage at the first technical detail'")
    ix = step(L, ".s06")["interaction"]
    assert "operations manager" in ix["public"]["prompt"]
    ix["public"]["prompt"] = ix["public"]["prompt"].replace("operations manager", "executive team")
    seed(T3, "D9", "answer key wrong for the stated audience", "s06", "question now asks about the EXECUTIVE team; key and feedback are written for an operations manager")
    sub_text(L, ".r01", "delivery times rose from 22 to 30 min", "delivery times rose from 22 to 38 min", remediation=True)
    seed(T3, "D10", "example contradicts the dataset (remediation)", "r01", "'22 to 30 min' -> '22 to 38 min'; the dataset says 22.0 -> 30.0")
    step(L, ".s07")["interaction"]["grading"]["option_feedback"]["opt_avoids_questions"]["message"] = \
        "Not quite. Providing all the details upfront never avoids questions; audiences always ask more when given more detail."
    seed(T3, "D11", "false wrong-option feedback (contradicts a source fact)", "s07", "feedback now contradicts fact B.f2")
    save(lessons_dir / f"{T3}.json", L)
    return truth


def prepare():
    """Mutated copies of the four tiles, their packets and the hidden truth. No model call."""
    shutil.rmtree(EXP, ignore_errors=True)
    (EXP / "tile_lessons").mkdir(parents=True)
    (EXP / "replies").mkdir()
    for t in (T1, T2, T3, CONTROL):
        shutil.copy(GOLD / "tile_lessons" / f"{t}.json", EXP / "tile_lessons" / f"{t}.json")
    truth = seed_defects(EXP / "tile_lessons")
    save(EXP / "_truth.json", {"seeded": truth, "control_tile_unmodified": CONTROL})
    env, packets = EP.Env(GOLD), {}
    for t in (T1, T2, T3, CONTROL):
        L = load(EXP / "tile_lessons" / f"{t}.json")
        text = EP.render(L, env)
        n, miss = EP.completeness(L, text)
        assert not miss, (t, miss[:3])
        packets[t] = text
        (EXP / f"{t}.packet.md").write_text(text)
    for d in truth:  # the seeded text must really be in what the evaluator reads
        marker = {"D1": "always rejects any change", "D2": "dangling foreign key row", "D3": "cannot store the same column name", "D4": "INNER JOIN of orders",
                  "D5": "far stronger", "D6": "most negative correlation", "D7": "always means the relationship is weak", "D8": "only ever wants",
                  "D9": "executive team", "D10": "22 to 38 min", "D11": "never avoids questions"}[d["id"]]
        assert marker in packets[d["tile"]], (d["id"], "seed not visible in the packet")
    return truth, packets


def blocking_lines(reply):
    return [ln.strip() for ln in reply.splitlines() if re.match(r"^\s*[-*`]*\s*\**BLOCKING\b", ln)]


def eval_test(specs):
    import run_pipeline as rp
    from bedrock_agent import transient
    truth, packets = prepare()
    persona = (ROOT / ".claude" / "agents" / "final-evaluator.md").read_text().split("---", 2)[2].strip()
    sid = "04_interactions"
    system = f"{persona}\n\n--- STAGE INSTRUCTIONS: {sid} ---\n{(rp.TEMPLATE / sid / 'EVALUATOR.md').read_text().strip()}\n\n{rp.PACKET_RULES}"
    os.environ["COST_LOG"] = str(EXP / "cost_log.jsonl")
    BL.load_env()
    client, rows = BL.make_client(), []
    for spec in specs:
        model, _, tier = spec.partition(":")
        os.environ.pop("LLM_SERVICE_TIER", None)
        if tier:
            os.environ["LLM_SERVICE_TIER"] = tier
        caught, extra, control_fp, usd, secs, verdicts = [], 0, 0, 0.0, 0.0, {}
        for t, pk in packets.items():
            task = (f"Evaluate stage `{sid}`. Cover ONLY these tile ids: {json.dumps([t])}. The packet above is the artifact under evaluation. The deterministic gates "
                    "already passed. Label every defect BLOCKING or ADVISORY. End with `VERDICT: PASS` or `VERDICT: FAIL`, then one line per defect: "
                    "`BLOCKING|ADVISORY <tile or asset>/<step or field>: what is wrong -> exact fix`.")
            t0 = time.time()
            for attempt in range(5):
                try:
                    r = client.converse(modelId=model, system=[{"text": system}], messages=[{"role": "user", "content": [{"text": pk}, {"text": task}]}],
                                        inferenceConfig={"maxTokens": 16000})
                    break
                except Exception as e:
                    if attempt == 4 or not transient(e):
                        raise
                    time.sleep(10 * 2 ** attempt)
            secs += time.time() - t0
            usd += BL.log_usage(model, r["usage"], f"evaltest:{spec}:{t}")
            reply = "".join(b.get("text", "") for b in r["output"]["message"]["content"])
            (EXP / "replies" / f"{spec.replace(':', '_')}__{t}.md").write_text(reply)
            m = rp.VERDICT.search(reply)
            verdicts[t] = m.group(1) if m else "NONE"
            bl = blocking_lines(reply)
            mine = [d for d in truth if d["tile"] == t]
            hit = lambda d, ln: re.search(rf"(?<![a-z0-9]){d['step']}(?![0-9])", ln)
            caught += [d["id"] for d in mine if any(hit(d, ln) for ln in bl)]
            if t == CONTROL:
                control_fp += len(bl)
            else:
                extra += sum(1 for ln in bl if not any(hit(d, ln) for d in mine))
        rows.append((spec, caught, extra, control_fp, verdicts, usd, secs))
        print(f"{spec}: caught {len(caught)}/{len(truth)}  missed {sorted({d['id'] for d in truth} - set(caught), key=lambda x: int(x[1:]))}  "
              f"other BLOCKING on seeded tiles {extra}  BLOCKING on clean control {control_fp} (verdict {verdicts[CONTROL]})  ${usd:.3f}  {secs:.0f}s", flush=True)
    save(EXP / "result.json", [{"model": r[0], "caught": r[1], "other_blocking": r[2], "control_blocking": r[3], "verdicts": r[4], "usd": round(r[5], 4), "seconds": round(r[6])} for r in rows])
    print(f"\nreplies: {EXP / 'replies'}   (earlier baseline on Claude Opus through the same packets: 11/11)")


def setup(name, bundle, toc, tiles=None):
    B = ROOT / "batches" / f"tmp_bakeoff_{name}"
    if B.exists():
        sys.exit(f"{B} already exists; remove it first if you want a fresh run")
    for p in (bundle, toc):
        if not Path(p).exists():
            sys.exit(f"not found: {p}")
    B.mkdir(parents=True)
    save(B / "run_config.json", {"path_id": "data_analyst", "glossary_bundle": str(Path(bundle).resolve()), "glossary_batch_id": "glossary_batch_001_data_analyst_pilot",
                                 "toc_workspace": str(Path(toc).resolve()), "tiles": tiles or GEN_TILES, "player_version": "0.1.0"})
    print(f"created {B.relative_to(ROOT)} with {len(tiles or GEN_TILES)} tiles")


def report(names):
    print(f"{'batch':22} {'state':16} {'tiles':>5} {'gates':>5} {'calls':>6} {'in M':>6} {'cached M':>8} {'out M':>6} {'gen $':>7} {'repair $':>8} {'eval $':>7} {'total $':>8} {'$/tile':>7}  eval rounds 03/04")
    for n in names:
        B = ROOT / "batches" / (n if n.startswith(("tmp_", "final_")) else f"tmp_bakeoff_{n}")
        w = B / "working"
        rows = [json.loads(ln) for ln in open(w / "cost_log.jsonl") if ln.strip()] if (w / "cost_log.jsonl").exists() else []
        kind = lambda lab: "eval" if (":eval" in lab or lab.split(":")[0] in ("08_pedagogy_review", "09_leakage_check", "11_final_audit")) else "repair" if ("repair" in lab or "gatefix" in lab) else "gen"
        usd, tok = collections.Counter(), collections.Counter()
        for r in rows:
            usd[kind(r.get("label", ""))] += r["usd"]
            tok["in"] += r.get("in", 0) + r.get("cache_write", 0)
            tok["cached"] += r.get("cache_read", 0)
            tok["out"] += r.get("out", 0)
        labels = [r.get("label", "") for r in rows]
        log = (w / "driver.log").read_text() if (w / "driver.log").exists() else ""
        rounds = "/".join(str(len(set(re.findall(rf"{s}\S* round (\d+)", log))) or len(re.findall(rf"EVAL {s}", log)) or "-") for s in ("03_screens", "04_interactions"))
        state = "DONE" if (w / "DRIVER_DONE.md").exists() else "STOPPED" if (w / "DRIVER_STOPPED.md").exists() else "running/not run"
        gates = len(load(B / "final_stage_gate_ledger.json")["gates"]) if (B / "final_stage_gate_ledger.json").exists() else 0
        tiles = len(list((B / "tile_lessons").glob("*.json"))) if (B / "tile_lessons").exists() else 0
        total = sum(usd.values())
        print(f"{n[:22]:22} {state:16} {tiles:5} {gates:5} {len(rows):6} {tok['in'] / 1e6:6.2f} {tok['cached'] / 1e6:8.2f} {tok['out'] / 1e6:6.2f} {usd['gen']:7.2f} {usd['repair']:8.2f} "
              f"{usd['eval']:7.2f} {total:8.2f} {total / max(tiles, len(GEN_TILES) if not tiles else tiles):7.2f}  {rounds}  models: {sorted({r['model'] for r in rows})}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("eval-test")
    e.add_argument("models", nargs="*", help="deployment names, optionally with :flex; none = prepare and check the packets only (no model call)")
    s = sub.add_parser("setup")
    s.add_argument("name")
    s.add_argument("--bundle", required=True, help="path_glossary_bundle.data_analyst.json")
    s.add_argument("--toc", required=True, help="the frozen Data Analyst TOC workspace folder")
    s.add_argument("--tiles", help="comma-separated tile ids (default: the 5 mixed-topic tiles). Prefer tiles of ONE topic: a batch shares one scenario/asset registry")
    r = sub.add_parser("report")
    r.add_argument("names", nargs="+")
    a = ap.parse_args()
    if a.cmd == "eval-test":
        if not a.models:
            truth, packets = prepare()
            print(f"prepared {len(truth)} seeded defects in 3 tiles + 1 control; packets: " + ", ".join(f"{t.split('_', 1)[1][:24]}={len(p):,} chars" for t, p in packets.items()))
        else:
            eval_test(a.models)
    elif a.cmd == "setup":
        setup(a.name, a.bundle, a.toc, a.tiles.split(",") if a.tiles else None)
    else:
        report(a.names)


if __name__ == "__main__":
    main()
