"""
Patch interactions.part.c3.json for REPAIR ROUND — v2.

BLOCKING:
  1. tile_python_errors_imports/s06 — use math.sqrt(x) not x ** 0.5
  2. tile_python_functions_scope/s14 — use keyword args not **dict unpacking
     Also add kw:order_id and kw:city to allowed_syntax so the gate passes.

ADVISORY:
  3. tile_python_pep8_style/s03 — add Minutes/Rate rename instruction
"""
import json, pathlib

src = pathlib.Path("batches/final_batch_008_da_python_core/interactions.part.c3.json")
data = json.loads(src.read_text())

# ── helpers ──────────────────────────────────────────────────────────────────

def find_interaction(data, tile_id, step_id):
    for tile in data["tiles"]:
        if tile["tile_id"] == tile_id:
            for item in tile["interactions"]:
                if item["step_id"] == step_id:
                    return item["interaction"]
    raise KeyError(f"{tile_id}/{step_id} not found")

# ─────────────────────────────────────────────────────────────────────────────
# FIX 1 — tile_python_errors_imports/s06
# ─────────────────────────────────────────────────────────────────────────────
ix = find_interaction(data, "tile_python_errors_imports", "tile_python_errors_imports.s06")

# Prompt: replace step 2 text
old_prompt = ix["public"]["prompt"]
new_prompt = old_prompt.replace(
    "2. Compute the square root of `x` using the expression `x ** 0.5` and store the result in a variable called `result`.",
    "2. Compute the square root of `x` using `math.sqrt(x)` and store the result in a variable called `result`."
)
assert new_prompt != old_prompt, "Prompt step 2 replacement failed"
ix["public"]["prompt"] = new_prompt

# Solution file: replace x ** 0.5 with math.sqrt(x)
sol = ix["grading"]["solution_files"][0]
old_sol = sol["content"]
new_sol = old_sol.replace("result = x ** 0.5", "result = math.sqrt(x)")
assert new_sol != old_sol, "Solution replacement failed"
sol["content"] = new_sol

# message_on_fail for t1_result
for t in ix["grading"]["tests"]:
    if t["test_id"] == "t1_result":
        t["message_on_fail"] = "`result` should hold `12.0` (math.sqrt(144)). Make sure you write `result = math.sqrt(x)`."

# feedback correct
ix["feedback"]["correct"]["message"] = (
    "Well done \u2014 `import math` adds the module to the namespace, "
    "and `math.sqrt(x)` calls the module function to compute the square root."
)
# feedback incorrect
ix["feedback"]["incorrect"]["message"] = (
    "Write `import math` at the top, then `result = math.sqrt(x)`, then `print(result)`."
)
# hints
ix["feedback"]["hints"] = [
    "The import statement goes at the top: `import math`.",
    "Compute the square root by calling the module function: `result = math.sqrt(x)`."
]

# ─────────────────────────────────────────────────────────────────────────────
# FIX 2 — tile_python_functions_scope/s14
# ─────────────────────────────────────────────────────────────────────────────
ix14 = find_interaction(data, "tile_python_functions_scope", "tile_python_functions_scope.s14")

# Prompt: replace step 2 instruction
old_p14 = ix14["public"]["prompt"]
new_p14 = old_p14.replace(
    "2. `describe_order(**{'order_id': order_id2, 'city': city2})` \u2014 use `**dict` to pass keyword arguments by name",
    "2. `describe_order(order_id=order_id2, city=city2)` \u2014 use keyword arguments by name"
)
assert new_p14 != old_p14, "Prompt step 2 replacement for s14 failed"
ix14["public"]["prompt"] = new_p14

# Starter file comment: update the second call comment (workspace is under public)
old_starter = ix14["public"]["workspace"]["files"][0]["content"]
new_starter = old_starter.replace(
    "#   Call describe_order with **{'order_id': order_id2, 'city': city2}",
    "#   Call describe_order(order_id=order_id2, city=city2)"
)
assert new_starter != old_starter, "Starter comment replacement for s14 failed"
ix14["public"]["workspace"]["files"][0]["content"] = new_starter

# Solution file: replace **{...} call with keyword-arg call
sol14 = ix14["grading"]["solution_files"][0]
old_sol14 = sol14["content"]
new_sol14 = old_sol14.replace(
    "describe_order(**{'order_id': order_id2, 'city': city2})",
    "describe_order(order_id=order_id2, city=city2)"
)
assert new_sol14 != old_sol14, "Solution replacement for s14 failed"
sol14["content"] = new_sol14

# allowed_syntax: add descriptors that cover kw:order_id and kw:city
# The pysyntax descriptor_tags regex picks up "name=" patterns from descriptor strings.
allowed = ix14["public"]["constraints"]["allowed_syntax"]
if "order_id=value" not in allowed:
    allowed.append("order_id=value")
if "city=value" not in allowed:
    allowed.append("city=value")

# message_on_fail
for t in ix14["grading"]["tests"]:
    if t["test_id"] == "t1_output":
        t["message_on_fail"] = (
            "Expected '1042 Lagos' then '1043 Abuja'. "
            "Check that city has a default of 'Lagos' and that you use "
            "keyword arguments in the second call."
        )

# feedback incorrect
ix14["feedback"]["incorrect"]["message"] = (
    "Change `def describe_order(order_id, city):` to "
    "`def describe_order(order_id, city='Lagos'):`. "
    "Then call it once with just `order_id1` and once with "
    "`describe_order(order_id=order_id2, city=city2)`."
)
# hints
ix14["feedback"]["hints"] = [
    "To add a default, change the parameter to `city='Lagos'` in the `def` line.",
    "Use `describe_order(order_id=order_id2, city=city2)` to pass keyword arguments by name."
]

# ─────────────────────────────────────────────────────────────────────────────
# FIX 3 (ADVISORY) — tile_python_pep8_style/s03 — add Minutes/Rate rename
# ─────────────────────────────────────────────────────────────────────────────
ix_pep = find_interaction(data, "tile_python_pep8_style", "tile_python_pep8_style.s03")

old_pep_prompt = ix_pep["public"]["prompt"]
# Insert "Rename Minutes → minutes and Rate → rate" as item 3, shifting existing 3 and 4
new_pep_prompt = old_pep_prompt.replace(
    "3. Use **4-space** indentation (not 2 spaces)\n4. Remove extraneous spaces inside `()` and before `,`",
    "3. Rename `Minutes` \u2192 `minutes` and `Rate` \u2192 `rate` (lowercase)\n4. Use **4-space** indentation (not 2 spaces)\n5. Remove extraneous spaces inside `()` and before `,`"
)
assert new_pep_prompt != old_pep_prompt, "PEP8 prompt replacement failed"
ix_pep["public"]["prompt"] = new_pep_prompt

# ─────────────────────────────────────────────────────────────────────────────
# Write output
# ─────────────────────────────────────────────────────────────────────────────
dst = pathlib.Path("batches/final_batch_008_da_python_core/interactions.part.c3.json")
dst.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
print("Patch applied successfully.")
