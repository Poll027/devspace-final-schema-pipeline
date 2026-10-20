"""Core-pack checkers: role-agnostic blocks and interactions. Signature for every checker: fn(C, step, obj, rep).
C = finlib.Ctx (registry, bundles, plans, profile); rep.e() = blocking error, rep.w() = advisory warning."""


def media_group(C, step, b, rep):
    here = f"{step['step_id']}/media_group"
    cids = step["concept_ids"]
    known = {sid for c in cids for sid in C.bundles.segments(c)}
    for sid in b["segment_ids"]:
        if sid not in known:
            rep.e(f"{here}: segment {sid} is not an approved segment of {cids}")
    if not b.get("segments"):
        rep.e(f"{here}: segments not inlined (run assemble_tiles.py)")
    for s in b.get("segments", []):
        src = next((C.bundles.segments(c)[s["segment_id"]] for c in cids if s["segment_id"] in C.bundles.segments(c)), None)
        if src and any(s.get(k) != src.get(k) for k in src if k in s):
            rep.e(f"{here}: segment {s['segment_id']} differs from the glossary bundle (media is copied verbatim, never edited)")


def _graph(C, step, b, rep):
    ids = {n["id"] for n in b["nodes"]}
    if len(ids) != len(b["nodes"]):
        rep.e(f"{step['step_id']}/{b['type']}: duplicate node ids")
    for ed in b["edges"]:
        if ed["from"] not in ids or ed["to"] not in ids:
            rep.e(f"{step['step_id']}/{b['type']}: edge {ed['from']}->{ed['to']} references an unknown node")


def process_flow(C, step, b, rep):
    _graph(C, step, b, rep)
    kinds = {n.get("kind") for n in b["nodes"]}
    if "decision" in kinds and not any(e.get("kind") in ("yes", "no", "branch") or e.get("label") for e in b["edges"]):
        rep.w(f"{step['step_id']}/process_flow: a decision node but no labelled/yes/no edge")


def code_walkthrough(C, step, b, rep):
    here = f"{step['step_id']}/code_walkthrough"
    n = len(b["code"].splitlines())
    for a in b.get("annotations", []):
        if a["end_line"] > n or a["start_line"] > a["end_line"]:
            rep.e(f"{here}: annotation lines {a['start_line']}-{a['end_line']} outside code ({n} lines)")
    if "output" in b and "execution_provenance" not in b:
        rep.w(f"{here}: output without execution_provenance — outputs must be computed, not typed")


def annotated_image(C, step, b, rep):
    from .dataset import asset_by_id
    a = asset_by_id(C.registry, b["asset_id"])
    if not a or a["asset_kind"] != "image":
        rep.e(f"{step['step_id']}/annotated_image: asset {b['asset_id']} is not a registered image")


def diagram(C, step, b, rep):
    _graph(C, step, b, rep)


# ---------------------------------------------------------------- interactions
def choice(C, step, ix, rep):
    here, pub, gr = f"{step['step_id']}/{ix['interaction_id']}", ix["public"], ix["grading"]
    opts = {o["option_id"] for o in pub["options"]}
    corr = set(gr["correct_option_ids"])
    if not corr <= opts:
        rep.e(f"{here}: correct_option_ids {sorted(corr - opts)} not among the options")
    if pub["selection"] == "single" and len(corr) != 1:
        rep.e(f"{here}: single-select needs exactly 1 correct option, has {len(corr)}")
    fb = gr.get("option_feedback", {})
    for k in fb:
        if k not in opts:
            rep.e(f"{here}: option_feedback for unknown option {k}")
    for o in sorted(opts - corr):
        if o not in fb:
            rep.w(f"{here}: wrong option {o} has no option_feedback (each distractor should explain WHY it is wrong)")
    if len({o["text"].strip().lower() for o in pub["options"]}) != len(pub["options"]):
        rep.e(f"{here}: duplicate option text")


def ordering(C, step, ix, rep):
    here, pub, gr = f"{step['step_id']}/{ix['interaction_id']}", ix["public"], ix["grading"]
    ids = [i["item_id"] for i in pub["items"]]
    if sorted(gr["correct_order"]) != sorted(ids):
        rep.e(f"{here}: correct_order is not a permutation of the items")
    for alt in gr.get("accepted_alternatives", []):
        if sorted(alt) != sorted(ids):
            rep.e(f"{here}: an accepted_alternative is not a permutation of the items")
    fu = pub.get("follow_up")
    if bool(fu) != bool(gr.get("follow_up_correct_option_ids")):
        rep.e(f"{here}: follow_up and follow_up_correct_option_ids must appear together")
    if fu and not set(gr["follow_up_correct_option_ids"]) <= {o["option_id"] for o in fu["options"]}:
        rep.e(f"{here}: follow_up_correct_option_ids not among the follow-up options")


def match_pairs(C, step, ix, rep):
    here, pub, gr = f"{step['step_id']}/{ix['interaction_id']}", ix["public"], ix["grading"]
    L, R = {i["id"] for i in pub["left"]}, {i["id"] for i in pub["right"]}
    for p in gr["pairs"]:
        if p["left"] not in L or p["right"] not in R:
            rep.e(f"{here}: pair {p} references an unknown id")
    if sorted(p["left"] for p in gr["pairs"]) != sorted(L):
        rep.e(f"{here}: every left item needs exactly one pair")


def field_selection(C, step, ix, rep):
    here, pub, gr = f"{step['step_id']}/{ix['interaction_id']}", ix["public"], ix["grading"]
    fields = {f["field_id"] for f in pub["fields"]}
    rules = {r["field_id"]: r["role"] for r in gr["rules"]}
    if set(rules) != fields:
        rep.e(f"{here}: rules must cover exactly the fields (missing {sorted(fields - set(rules))}, extra {sorted(set(rules) - fields)})")
    if "required" not in rules.values():
        rep.e(f"{here}: at least one field must be required")
    if set(rules.values()) == {"required"}:
        rep.w(f"{here}: every field is required — selection is trivial (add forbidden/unneeded/acceptable fields)")


def short_answer(C, step, ix, rep):
    here, gr = f"{step['step_id']}/{ix['interaction_id']}", ix["grading"]
    if ix["public"]["input_kind"] == "number" and "numeric" not in gr:
        rep.e(f"{here}: a number answer needs grading.numeric")
    if ix["public"]["input_kind"] == "text" and not gr.get("accepted_answers"):
        rep.e(f"{here}: a text answer needs grading.accepted_answers")


def external_proof(C, step, ix, rep):
    gr = ix["grading"]
    if gr["mode"] == "rubric_ai" and not gr.get("rubric"):
        rep.e(f"{step['step_id']}/{ix['interaction_id']}: rubric_ai grading needs a rubric")


def diagram_label(C, step, ix, rep):
    here, pub, gr = f"{step['step_id']}/{ix['interaction_id']}", ix["public"], ix["grading"]
    nodes = {n["id"] for n in pub["diagram"]["nodes"]}
    labels = {l["label_id"] for l in pub["labels"]}
    if set(gr["placements"]) != labels:
        rep.e(f"{here}: placements must cover exactly the labels")
    for lab, node in gr["placements"].items():
        if node not in nodes:
            rep.e(f"{here}: label {lab} placed on unknown node {node}")


BLOCK = {"media_group": media_group, "process_flow": process_flow, "code_walkthrough": code_walkthrough, "annotated_image": annotated_image, "diagram": diagram}
# block types with no external references: nothing to execute or resolve (their schema is their check)
NO_CHECK_NEEDED = {"prose", "heading", "callout", "concept_chips", "up_next", "comparison", "before_after", "side_by_side"}
INTERACTION = {"choice": choice, "ordering": ordering, "match_pairs": match_pairs, "field_selection": field_selection,
               "short_answer": short_answer, "external_proof": external_proof, "diagram_label": diagram_label}
ASSET = {}
