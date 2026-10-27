#!/usr/bin/env python3
"""Run a Final Schema batch unattended on AWS Bedrock: the orchestrator loop from START_HERE.md as a program. ROLE-AGNOSTIC.

    python3 run_pipeline.py batches/<batch_id> --max-usd 25 [--plan] [--selftest-batch batches/<passing batch>]

Walks pipeline_manifest.json. A stage already gated PASS on disk (ledger hash matches) is skipped, so a rerun resumes.
  script             the RUN.md command (00_preflight builds its command from batches/<id>/run_config.json)
  generate_evaluate  generator -> deterministic gate (failures go back to the generator, no evaluator spend) -> fresh evaluator
                     -> up to 3 repair rounds (scoped re-evaluation) -> advisories get one reword-only repair, no re-evaluation
  evaluator_only     one fresh evaluator writes the stage artifact; a BLOCKING finding stops the run for a human
Stages whose manifest status starts with "planned" are skipped (05 stops the run if the tile plans need sandbox types).
Stops (exit 2, writes working/DRIVER_STOPPED.md, SNS if SNS_TOPIC_ARN is set) on: 3 failed rounds, the same blockers coming back
unchanged, a failed script, or the spend cap (exit 3). Fix the cause and rerun the same command.

run_config.json: {"path_id","glossary_bundle","glossary_batch_id","toc_workspace","tiles":[...]?,"player_version"?}
Env: GEN_MODEL_ID / EVAL_MODEL_ID (pin one model) or GEN_LADDER / EVAL_LADDER, MAX_USD, CALL_CAP_USD (per agent call and tile, default 8),
     CHUNK_WORKERS (default 2), SNS_TOPIC_ARN, AWS_REGION.
# ponytail: the driver never commits or pushes; chunks need >12 tiles to fan out; a blocking 08/09/11 result stops for a human
# instead of auto-routing the fix to the stage it names.
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import update_ledger as UL  # noqa: E402
from bedrock_agent import Budget, BudgetExceeded, run_agent  # noqa: E402
from bedrock_llm import load_env, sns  # noqa: E402
from finlib import CORE, ROOT, load, save  # noqa: E402

SCRIPTS = CORE / "scripts"
TEMPLATE = ROOT / "01_FINAL_PACK_TEMPLATE"
MAX_ROUNDS = 3
MAX_TILES_PER_CHUNK = 12
SANDBOX_TYPES = {"code_exercise", "formula_entry", "spreadsheet_grid"}  # need a verified runtime (registry/runtimes.json)
VERDICT = re.compile(r"VERDICT:\s*(PASS_WITH_NONBLOCKING_CHANGES|PASS|FAIL)")
SEVERITY = re.compile(r"^\s*[-*]?\s*(BLOCKING|ADVISORY)\b")


class Stuck(Exception):
    pass


class Ctx:
    def __init__(self, B, args):
        self.B, self.args = B, args
        self.id = B.name
        self.gen_pin, self.ev_pin = os.environ.get("GEN_MODEL_ID"), os.environ.get("EVAL_MODEL_ID")
        (B / "working").mkdir(exist_ok=True)
        self.budget = Budget(args.max_usd, B / "working" / "cost_log.jsonl")
        self.call_cap = float(os.environ.get("CALL_CAP_USD", 8))
        self.manifest = load(CORE / "pipeline_manifest.json")
        self.stage = {s["id"]: s for s in self.manifest["stages"]}
        self.env = {**os.environ, "PATH": f"{Path(sys.executable).parent}:{os.environ['PATH']}"}
        self.t0 = ""  # UTC start of the stage being run

    def window_models(self, evaluator):
        """Models that really made generator (or evaluator) calls since this driver run started the stage (the ladder may have
        fallen back), from the cost log. Labels end ':eval' for evaluator calls. ponytail: a resumed stage only sees this run's calls."""
        ms = set()
        try:
            for ln in open(self.B / "working" / "cost_log.jsonl"):
                r = json.loads(ln)
                if r["t"][:19] >= self.t0 and r["label"].endswith(":eval") == evaluator:
                    ms.add(r["model"])
        except FileNotFoundError:
            pass
        return ",".join(sorted(ms)) or "none"

    gen = property(lambda s: s.gen_pin or s.window_models(False))
    ev = property(lambda s: s.ev_pin or s.window_models(True))

    def log(self, msg):
        line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}"
        print(line, flush=True)
        with open(self.B / "working" / "driver.log", "a") as f:
            f.write(line + "\n")

    def artifact(self, sid):
        return self.stage[sid]["outputs"][0]

    def part(self, sid, chunk):
        a = self.artifact(sid)
        return self.B / (a if chunk == "all" else a.replace(".json", f".part.{chunk}.json"))

    def rel(self, p):
        return Path(p).resolve().relative_to(ROOT)

    def sh(self, cmd, check=True, cwd=ROOT):
        r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, env=self.env)
        self.budget.check()
        if check and r.returncode:
            raise Stuck(f"command failed ({r.returncode}): {cmd}\n{(r.stdout + r.stderr)[-2500:]}")
        return r

    def py(self, script, *a):
        return f"'{sys.executable}' '{SCRIPTS / script}' " + " ".join(f"'{x}'" for x in a)

    def protected(self):
        """Files an agent's write_file must refuse: every gated artifact, the ledger and the staged inputs. (Bash can still write; the ledger's
        hash check is the backstop that caught the batch-004 edit.)"""
        out = [self.B / UL.LEDGER, self.B / "inputs", self.B / "run_config.json", self.B / "chunks.json"]
        if (self.B / UL.LEDGER).exists():
            for g in UL.load_ledger(str(self.B))["gates"]:
                out += list(self.B.glob(g["artifact"]))
        return out

    def agent(self, role, task, label, tiles=1):
        t = (ROOT / ".claude" / "agents" / ("final-generator.md" if role == "GEN" else "final-evaluator.md")).read_text()
        system = (t.split("---", 2)[2].strip() + "\n\nYou have three tools: read_file, write_file (only under the batch folder), bash "
                  "(run from the pack root; `python3` has jsonschema; no web access). The pack root is the working directory. "
                  "Finish by replying with the requested summary.")
        model = (self.gen_pin if role == "GEN" else self.ev_pin) or role
        return run_agent(model, system, task, self.budget, role=role, write_roots=[self.B, ROOT / "scratch"], label=label,
                         call_cap_usd=self.call_cap * max(tiles, 1), protected=self.protected())  # the ceiling is per tile: a 3-tile chunk call may cost 3x


# ---------- chunks ----------
def tile_chunks(c):
    """{chunk: [tile_id]}: whole tiles, split at region boundaries, <=12 tiles; the first chunk is the canary and runs alone."""
    p = c.B / "chunks.json"
    if p.exists():
        return load(p)["chunks"]
    tiles = load(c.B / "tile_plans.json")["tiles"]
    if len(tiles) <= MAX_TILES_PER_CHUNK:
        chunks = {"all": [t["tile_id"] for t in tiles]}
    else:
        chunks, cur, reg = {}, [], None
        for t in tiles:
            if cur and (len(cur) >= MAX_TILES_PER_CHUNK or (t["region_id"] != reg and len(cur) >= 8)):
                chunks[f"c{len(chunks)}"] = cur
                cur = []
            cur.append(t["tile_id"])
            reg = t["region_id"]
        chunks[f"c{len(chunks)}"] = cur
        first = next(iter(chunks))
        chunks = {("c0_canary" if k == first else k): v for k, v in chunks.items()}
    save(p, {"path_id": load(c.B / "tile_plans.json")["path_id"], "chunks": chunks})
    return chunks


def scope_text(chunk, ids):
    if ids is None:
        return "Cover the whole batch."
    if chunk == "all":
        return f"Cover every tile of this batch: {json.dumps(ids)}."
    return f"Fan-out chunk `{chunk}`: cover ONLY these tile ids: {json.dumps(ids)}."


# ---------- deterministic gates ----------
def sandbox_dir(c, sid, chunk, ids):
    """A copy of the batch holding only this chunk's tiles, so assemble/validate can judge a chunk before the others exist."""
    d = c.B / "working" / f"gate_{sid}_{chunk}"
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)
    ctx = load(c.B / "batch_run_context.json")
    ctx["tile_ids"] = ids
    save(d / "batch_run_context.json", ctx)
    (d / "inputs").symlink_to((c.B / "inputs").resolve())
    own = c.artifact(sid)
    for name in c.stage[sid]["depends_on"] + [own]:
        if not name.endswith(".json"):
            continue
        src = c.part(sid, chunk) if name == own else c.B / name
        doc = load(src)
        if isinstance(doc.get("tiles"), list):
            doc["tiles"] = [t for t in doc["tiles"] if t["tile_id"] in ids]
        save(d / name, doc)
    return d


def gate_cmd(c, cmd, B):
    """'script.py {B} --flag' -> shell command; {B} is substituted after splitting so paths with spaces survive."""
    return c.py(*[str(B) if t == "{B}" else t for t in cmd.split()])


def part_gate(c, sid, chunk, ids):
    """Everything a script can check about one part, before any evaluator. Returns (ok, message for the generator)."""
    g, part = c.stage[sid].get("gate", {}), c.part(sid, chunk)
    if not part.exists():
        return False, f"{c.rel(part)} was not written"
    out = []
    if g.get("part_schema"):
        r = c.sh(c.py("schema_check.py", g["part_schema"], part), check=False)
        if r.returncode:
            out.append("schema_check:\n" + (r.stdout + r.stderr)[-1500:])
    doc = load(part)
    if ids is not None and isinstance(doc.get("tiles"), list):
        got = [t["tile_id"] for t in doc["tiles"]]
        if sorted(got) != sorted(ids):
            out.append(f"tile coverage: part has {got}, scope is {ids}")
    for cmd in g.get("cmds", []):
        r = c.sh(gate_cmd(c, cmd, c.B), check=False)
        if r.returncode:
            out.append(f"{cmd}:\n" + (r.stdout + r.stderr)[-2500:])
    if g.get("sandbox") and not out:
        d = sandbox_dir(c, sid, chunk, ids)
        for cmd in g["sandbox"]:
            r = c.sh(gate_cmd(c, cmd, d), check=False)
            if r.returncode:
                out.append(f"{cmd}:\n" + (r.stdout + r.stderr)[-2500:])
                break
    return not out, "\n\n".join(out)


# ---------- agent tasks ----------
def generator_task(c, sid, chunk, ids, repair=None, gate_msg=None):
    part = c.rel(c.part(sid, chunk))
    if repair or gate_msg:
        what = gate_msg or repair
        head = (f"REPAIR ROUND for stage `{sid}`, artifact `{part}`, batch folder `{c.rel(c.B)}/`. Read `01_FINAL_PACK_TEMPLATE/{sid}/GENERATOR.md` for the rules. "
                + ("A deterministic gate failed; fix exactly what it reports" if gate_msg else
                   "Evaluator findings follow. Change ONLY what the findings name; advisory fixes may only reword, delete, move or cite, never add a claim or change an answer key")
                + f". Patch the existing file with a small script (do not rewrite it from scratch), then re-run the gate.\n\n{what}")
        return head
    return (f"Stage `{sid}`, batch folder `{c.rel(c.B)}/`. Read `01_FINAL_PACK_TEMPLATE/{sid}/GENERATOR.md` and follow it exactly, plus the playbook sections it cites. "
            f"{scope_text(chunk, ids)} Run your own 'mistakes to avoid' checklist before finishing. Write `{part}`. "
            f"Build large files with a script, not by hand. Run the stage gate named in GENERATOR.md before finishing.")


def evaluator_task(c, sid, chunk, ids, prior=None):
    part = c.rel(c.part(sid, chunk))
    sb = c.stage[sid].get("gate", {}).get("sandbox")
    t = (f"Evaluate stage `{sid}`, batch folder `{c.rel(c.B)}/`. Read `01_FINAL_PACK_TEMPLATE/{sid}/EVALUATOR.md` and follow it. "
         f"Artifact under evaluation: `{part}`. {scope_text(chunk, ids)} The deterministic gates already passed; do not rerun them. "
         + (f"The assembled lessons for this scope are in `{c.rel(c.B)}/working/gate_{sid}_{chunk}/tile_lessons/`. " if sb else "")
         + "Label every defect BLOCKING or ADVISORY. End with `VERDICT: PASS` or `VERDICT: FAIL`, then one line per defect: "
           "`BLOCKING|ADVISORY <tile or asset>/<step or field>: what is wrong -> exact fix`. Do not edit any artifact.")
    if prior:
        t += ("\n\nThis is a SCOPED re-evaluation after a repair. Check only what the repair changed against its sources and confirm nothing else changed. "
              f"Findings that were sent for repair:\n{prior}")
    return t


def parse_eval(text):
    m = VERDICT.findall(text)
    if not m:
        return None, []
    defects = [ln.strip() for ln in text.splitlines() if SEVERITY.match(ln)]
    if m[-1] == "FAIL" and not any(SEVERITY.match(d).group(1) == "BLOCKING" for d in defects):
        defects.append("BLOCKING (unparsed): " + text[-1200:])
    return m[-1], defects


def is_blocking(d):
    return SEVERITY.match(d).group(1) == "BLOCKING"


# ---------- generate / evaluate / repair ----------
def ensure_gate(c, sid, chunk, ids):
    """Run the part gate; on failure send the errors to the generator (no evaluator call). Up to MAX_ROUNDS attempts."""
    for i in range(MAX_ROUNDS + 1):
        ok, msg = part_gate(c, sid, chunk, ids)
        if ok:
            return
        if i == MAX_ROUNDS:
            raise Stuck(f"{sid}:{chunk} still failing its deterministic gate after {MAX_ROUNDS} generator repairs:\n{msg[-2000:]}")
        c.log(f"{sid}:{chunk} gate failed, generator repair {i + 1}")
        c.agent("GEN", generator_task(c, sid, chunk, ids, gate_msg=msg), f"{sid}:{chunk}:gatefix", tiles=len(ids or []))


def chunk_gen_eval(c, sid, chunk, ids):
    """Generate (or reuse), then evaluate/repair up to 3 rounds. Returns the number of unresolved advisories."""
    done = c.B / "working" / f"state_{sid}_{chunk}.json"
    if done.exists() and load(done).get("passed"):
        return load(done)["advisories"]
    if not c.part(sid, chunk).exists() or not part_gate(c, sid, chunk, ids)[0]:
        if not c.part(sid, chunk).exists():
            c.log(f"{sid}:{chunk} generating")
            c.agent("GEN", generator_task(c, sid, chunk, ids), f"{sid}:{chunk}:gen", tiles=len(ids or []))
        ensure_gate(c, sid, chunk, ids)
    prior, prev_keys = None, None
    for rnd in range(1, MAX_ROUNDS + 1):
        c.log(f"{sid}:{chunk} evaluating (round {rnd})")
        verdict, defects = None, []
        for _ in range(2):
            verdict, defects = parse_eval(c.agent("EVAL", evaluator_task(c, sid, chunk, ids, prior), f"{sid}:{chunk}:eval", tiles=len(ids or [])))
            if verdict:
                break
        (c.B / "working" / f"eval_{sid}_{chunk}_r{rnd}.txt").write_text(f"{verdict}\n" + "\n".join(defects))
        if not verdict:
            raise Stuck(f"{sid}:{chunk} evaluator never produced a VERDICT line")
        blocking = [d for d in defects if is_blocking(d)]
        if not blocking:
            if defects:  # one reword-only repair, script gate, no re-evaluation (START_HERE)
                c.log(f"{sid}:{chunk} PASS with {len(defects)} advisories; one repair, no re-evaluation")
                c.agent("GEN", generator_task(c, sid, chunk, ids, repair="\n".join(defects)), f"{sid}:{chunk}:repair", tiles=len(ids or []))
                ensure_gate(c, sid, chunk, ids)
            done.write_text(json.dumps({"passed": True, "advisories": 0, "rounds": rnd}))
            return 0
        c.log(f"{sid}:{chunk} FAIL round {rnd}: {len(blocking)} blocking")
        keys = {re.sub(r"^\W*BLOCKING\s+", "", d).split(":")[0].strip() for d in blocking}
        if rnd > 1 and keys == prev_keys:
            raise Stuck(f"{sid}:{chunk} the same blocking defects came back unchanged after a repair (check whether the finding is a false positive):\n" + "\n".join(blocking[:15]))
        prev_keys = keys
        if rnd == MAX_ROUNDS:
            raise Stuck(f"{sid}:{chunk} still failing after {MAX_ROUNDS} rounds:\n" + "\n".join(blocking[:15]))
        c.agent("GEN", generator_task(c, sid, chunk, ids, repair="\n".join(defects)), f"{sid}:{chunk}:repair", tiles=len(ids or []))
        ensure_gate(c, sid, chunk, ids)
        prior = "\n".join(defects)


def fan_out(chunks, fn):
    names = list(chunks)
    results = {names[0]: fn(names[0], chunks[names[0]])}  # canary alone
    rest = names[1:]
    if rest:
        errs = []
        with cf.ThreadPoolExecutor(int(os.environ.get("CHUNK_WORKERS", 2))) as ex:
            futs = {ex.submit(fn, n, chunks[n]): n for n in rest}
            for f in cf.as_completed(futs):
                try:
                    results[futs[f]] = f.result()
                except (Stuck, BudgetExceeded) as e:
                    errs.append(e)
        if errs:
            raise next((e for e in errs if isinstance(e, BudgetExceeded)), errs[0])
    return results


def merge(c, sid, chunks):
    """Concatenate the chunk parts' `tiles` into the stage artifact (header from the first part), in plan order."""
    docs = [load(c.part(sid, ch)) for ch in chunks]
    out = dict(docs[0])
    out["tiles"] = [t for d in docs for t in d["tiles"]]
    save(c.B / c.artifact(sid), out)


def gate(c, sid, verdict="PASS", gen=None, ev=None, unresolved=0):
    UL.record(str(c.B), sid, c.artifact(sid), verdict, generator=gen or "none", evaluator=ev or "none", unresolved=unresolved)
    c.log(f"GATE {sid} {verdict}")


# ---------- stage runners ----------
def run_gen_eval(c, sid):
    st = c.stage[sid]
    chunks = tile_chunks(c) if st.get("chunk_by") == "tile" else {"all": None}
    n = fan_out(chunks, lambda ch, ids: chunk_gen_eval(c, sid, ch, ids))
    if list(chunks) != ["all"]:
        merge(c, sid, chunks)
        if st["gate"].get("part_schema"):
            r = c.sh(c.py("schema_check.py", st["gate"]["part_schema"], c.B / c.artifact(sid)), check=False)
            if r.returncode:
                raise Stuck(f"{sid} merged artifact invalid:\n{(r.stdout + r.stderr)[-1500:]}")
    gate(c, sid, gen=c.gen, ev=c.ev, unresolved=sum(n.values()))


def blocking_in(path, reply):
    """BLOCKING/BLOCKER findings in an evaluator-only artifact (json or text) or its reply."""
    hits = [ln.strip() for ln in reply.splitlines() if re.match(r"\s*[-*]?\s*(BLOCKING|BLOCKER)\b", ln)]
    if path.suffix == ".json":
        def walk(o):
            if isinstance(o, dict):
                if str(o.get("severity", "")).upper() in ("BLOCKING", "BLOCKER"):
                    hits.append(json.dumps(o)[:300])
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(load(path))
    else:
        hits += [ln.strip() for ln in path.read_text().splitlines() if re.match(r"\s*[-*]?\s*(BLOCKING|BLOCKER)\b", ln)]
    return hits


def run_evaluator_only(c, sid):
    art = c.B / c.artifact(sid)
    instr = "INDEPENDENT_AUDIT.md" if sid.endswith("final_audit") else "EVALUATOR.md"
    task = (f"Run stage `{sid}`, batch folder `{c.rel(c.B)}/`. Read `01_FINAL_PACK_TEMPLATE/{sid}/{instr}` and follow it. "
            f"Write the stage artifact `{c.rel(art)}` yourself. Label defects BLOCKING or ADVISORY (audit: BLOCKER/HIGH/MEDIUM/LOW). "
            f"End your reply with `VERDICT: PASS`, `VERDICT: PASS_WITH_NONBLOCKING_CHANGES` or `VERDICT: FAIL`.")
    text = ""
    for _ in range(2):
        text = c.agent("EVAL", task, f"{sid}:eval", tiles=len(load(c.B / "tile_plans.json")["tiles"]))  # whole-batch review: ceiling scales with tiles
        if art.exists() and VERDICT.findall(text):
            break
    else:
        raise Stuck(f"{sid} evaluator did not write {c.artifact(sid)} with a VERDICT line")
    hits = blocking_in(art, text)
    if hits or VERDICT.findall(text)[-1] == "FAIL":
        raise Stuck(f"{sid} reported blocking findings; decide which earlier stage to reopen, then rerun. See {c.artifact(sid)}.\n" + "\n".join(hits[:15]))
    gate(c, sid, ev=c.ev)


def run_script_stage(c, sid):
    if sid == "00_preflight":
        cfg = load(c.B / "run_config.json")
        cmd = c.py("preflight.py", c.B, "--path-id", cfg["path_id"], "--glossary-bundle", cfg["glossary_bundle"],
                   "--glossary-batch-id", cfg["glossary_batch_id"], "--toc-workspace", cfg["toc_workspace"],
                   "--player-version", cfg.get("player_version", "0.1.0"))
        if cfg.get("tiles"):
            cmd += f" --tiles {','.join(cfg['tiles'])}"
        lines = [cmd]
    else:
        txt = (TEMPLATE / sid / "RUN.md").read_text()
        block = re.search(r"```bash\n(.*?)```", txt, re.S).group(1).replace("\\\n", " ").replace("<batch_id>", c.id)
        lines = [x.strip().replace("[--strict]", "--strict") for x in block.splitlines() if x.strip() and "update_ledger.py" not in x or " verify" in x]
    for line in lines:
        c.log(f"{sid}: {line[:140]}")
        c.sh(line.replace("python3 ", f"'{sys.executable}' ", 1))
    if sid == "02_tile_plan":
        check_plan_gaps(c)
    if c.artifact(sid) != UL.LEDGER:  # the ledger can't gate itself
        gate(c, sid)


def verified_runtimes():
    return {k for k, v in load(CORE / "registry" / "runtimes.json")["runtimes"].items() if v["status"] == "verified"}


def check_plan_gaps(c):
    """Stop BEFORE any generator spend if a planned tile can't be authored or verified: a type gap ('NO interaction type registered' /
    no block mapping), or code/formula/spreadsheet content whose runtime has no verified runner (registry/runtimes.json)."""
    ok_rt, gaps = verified_runtimes(), {}
    for t in load(c.B / "tile_plans.json")["tiles"]:
        g = [w for w in t["warnings"] if "NO " in w and "registered" in w or "no block mapping" in w.lower()]
        needs = set(t["needs"]["interaction_types"]) | set(t["needs"]["block_types"])
        if needs & SANDBOX_TYPES and (not t["needs"]["runtimes"] or not set(t["needs"]["runtimes"]) <= ok_rt):
            g.append(f"needs runtime(s) {t['needs']['runtimes'] or ['<none inferred>']} with no verified runner (verified: {sorted(ok_rt)})")
        if g:
            gaps[t["tile_id"]] = g
    if gaps:
        raise Stuck("tile plans have gaps (NEW_ROLE_RUNBOOK step 4 / build the runner): fix them or remove these tiles from run_config.json/chunks.json, then rerun.\n"
                    + json.dumps(gaps, indent=1))


def check_planned(c, sid):
    c.log(f"{sid}: planned stage, not run" + (" (code exercises are authored in stage 04 and executed by its gate)" if sid == "05_code_exercises" else ""))


def is_done(c, sid):
    if c.artifact(sid) == UL.LEDGER or not (c.B / UL.LEDGER).exists():
        return False
    g = next((g for g in UL.load_ledger(str(c.B))["gates"] if g["stage_id"] == sid), None)
    try:
        return bool(g and g["verdict"] == "PASS" and UL.artifact_hash(str(c.B), g["artifact"]) == g["artifact_hash"])
    except FileNotFoundError:
        return False


def notify(c, subject, body):
    c.log(f"NOTIFY {subject}")
    (c.B / "working" / ("DRIVER_STOPPED.md" if "STOPPED" in subject else "DRIVER_DONE.md")).write_text(f"# {subject}\n\n{body}\n")
    if not ("STOPPED" in subject and os.environ.get("SUPERVISED")):  # the supervisor sends the triaged stop email
        sns(subject, body)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("batch_dir")
    ap.add_argument("--max-usd", type=float, default=float(os.environ["MAX_USD"]) if "MAX_USD" in os.environ else None, required="MAX_USD" not in os.environ,
                    help="hard spend cap in USD (required: no default, so a run can't start uncapped)")
    ap.add_argument("--plan", action="store_true", help="walk the manifest and print what would run; no model calls, no spend")
    ap.add_argument("--selftest-batch", help="a PASSing batch to run selftest.py on first (must report 0 missed)")
    a = ap.parse_args()
    load_env()
    B = Path(a.batch_dir)
    B = B if B.is_absolute() else ROOT / B
    B.mkdir(parents=True, exist_ok=True)
    c = Ctx(B, a)
    if not a.plan:
        (B / "working" / "DRIVER_STOPPED.md").unlink(missing_ok=True)
    c.log(f"start {c.id}; cap ${a.max_usd}; spent so far ${c.budget.spent():.2f}")
    try:
        if a.selftest_batch and not a.plan:
            r = c.sh(c.py("selftest.py", a.selftest_batch), check=False)
            if r.returncode or not re.search(r"\b0 missed\b", r.stdout):
                raise Stuck("selftest.py did not report 0 missed:\n" + (r.stdout + r.stderr)[-1500:])
            c.log("selftest: 0 missed")
        for st in c.manifest["stages"]:
            sid, kind = st["id"], st["kind"]
            if st["status"].startswith("planned"):
                if a.plan:
                    c.log(f"{sid}: planned, would skip")
                else:
                    check_planned(c, sid)
                continue
            if is_done(c, sid):
                c.log(f"{sid}: gated PASS on disk, skipping")
                continue
            if a.plan:
                c.log(f"{sid}: WOULD RUN ({kind})")
                continue
            c.t0 = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
            c.log(f"=== {sid} ({kind}) spent ${c.budget.spent():.2f}")
            {"script": run_script_stage, "generate_evaluate": run_gen_eval, "evaluator_only": run_evaluator_only}[kind](c, sid)
        if not a.plan:
            notify(c, f"DONE {c.id}", f"All implemented stages gated. Spend ${c.budget.spent():.2f}. 05 and 12 are planned stages and were not run.")
    except (Stuck, BudgetExceeded) as e:
        notify(c, f"STOPPED {c.id}", f"{e}\n\nSpend so far ${c.budget.spent():.2f}. Fix the cause, then rerun the same command (finished stages are skipped).")
        sys.exit(3 if isinstance(e, BudgetExceeded) else 2)
    except Exception as e:  # an unexpected crash must still leave a stop file (and the SNS/supervisor path), not just a traceback
        import traceback
        notify(c, f"STOPPED {c.id}", f"unexpected {type(e).__name__}: {e}\n\n{traceback.format_exc()[-2500:]}\nSpend so far ${c.budget.spent():.2f}. Rerun the same command (finished stages are skipped).")
        sys.exit(2)


if __name__ == "__main__":
    main()
