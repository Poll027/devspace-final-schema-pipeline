import json, re

path = "batches/final_batch_008_da_python_core/interactions.part.c3.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Locate tile_python_functions_scope / s14
tile = next(t for t in data["tiles"] if t["tile_id"] == "tile_python_functions_scope")
step = next(s for s in tile["interactions"] if s["step_id"] == "tile_python_functions_scope.s14")
ix = step["interaction"]

# ── 1. Prompt ──────────────────────────────────────────────────────────────
old_prompt = ix["public"]["prompt"]
new_prompt = old_prompt.replace(
    "2. `describe_order(**{'order_id': order_id2, 'city': city2})` \u2014 use `**dict` to pass keyword arguments by name",
    "2. `describe_order(order_id=order_id2, city=city2)` \u2014 use keyword arguments by name"
)
assert new_prompt != old_prompt, "Prompt replacement failed"
ix["public"]["prompt"] = new_prompt

# ── 2. Starter file comment ────────────────────────────────────────────────
starter = ix["public"]["workspace"]["files"][0]
old_content = starter["content"]
new_content = old_content.replace(
    "#   Call describe_order(**{'order_id': order_id2, 'city': city2})",
    "#   Call describe_order(order_id=order_id2, city=city2)"
)
assert new_content != old_content, "Starter comment replacement failed"
starter["content"] = new_content

# ── 3. Solution file ───────────────────────────────────────────────────────
sol = ix["grading"]["solution_files"][0]
old_sol = sol["content"]
new_sol = old_sol.replace(
    "describe_order(**{'order_id': order_id2, 'city': city2})\n",
    "describe_order(order_id=order_id2, city=city2)\n"
)
assert new_sol != old_sol, "Solution replacement failed"
sol["content"] = new_sol

# ── 4. message_on_fail ─────────────────────────────────────────────────────
test = ix["grading"]["tests"][0]
old_msg = test["message_on_fail"]
new_msg = old_msg.replace(
    "that you use **dict in the second call.",
    "that you use keyword arguments by name in the second call."
)
assert new_msg != old_msg, "message_on_fail replacement failed"
test["message_on_fail"] = new_msg

# ── 5. feedback.correct ────────────────────────────────────────────────────
old_correct = ix["feedback"]["correct"]["message"]
new_correct = old_correct.replace(
    "the second call passed keyword arguments by name using `**dict`.",
    "the second call passed keyword arguments by name."
)
assert new_correct != old_correct, "feedback.correct replacement failed"
ix["feedback"]["correct"]["message"] = new_correct

# ── 6. feedback.incorrect ──────────────────────────────────────────────────
old_incorrect = ix["feedback"]["incorrect"]["message"]
new_incorrect = old_incorrect.replace(
    "once with `describe_order(**{'order_id': order_id2, 'city': city2})`.",
    "once with `describe_order(order_id=order_id2, city=city2)`."
)
assert new_incorrect != old_incorrect, "feedback.incorrect replacement failed"
ix["feedback"]["incorrect"]["message"] = new_incorrect

# ── 7. hints[1] ────────────────────────────────────────────────────────────
old_hint = ix["feedback"]["hints"][1]
new_hint = old_hint.replace(
    "Use `describe_order(**{'order_id': order_id2, 'city': city2})` to pass keyword arguments by name via a dictionary.",
    "Use `describe_order(order_id=order_id2, city=city2)` to pass keyword arguments by name."
)
assert new_hint != old_hint, "hints[1] replacement failed"
ix["feedback"]["hints"][1] = new_hint

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("Patch applied successfully.")
