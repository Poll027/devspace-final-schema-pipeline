"""
Repair round 3 patch for interactions.part.c3.json.

Fixes:
1. tile_python_errors_imports.s06:
   - Hard-coded answer: add top-level x=144 starter var so hidden checks can mutate it
   - import:math not in allowed syntax: add 'import math' descriptor
   - attr:sqrt not in allowed syntax: add 'math.sqrt()' descriptor
   - Update solution to use x instead of literal 144
   - Update test expected (still 12.0 when x=144)

2. tile_python_file_io.s06:
   - import:csv not in allowed syntax: add 'import csv' descriptor

3. tile_python_pep8_style.s03:
   - Hard-coded answer (t1_stdout): add top-level minutes=30, rate=2 vars
     so hidden checks can mutate them; solution prints calc_fee(minutes, rate)
   - Update t1_stdout expected to '60' (unchanged, but now depends on vars)
"""
import json, copy

PATH = "batches/final_batch_008_da_python_core/interactions.part.c3.json"

with open(PATH) as f:
    data = json.load(f)

for tile in data["tiles"]:
    tid = tile["tile_id"]

    # ── tile_python_errors_imports ──────────────────────────────────────────
    if tid == "tile_python_errors_imports":
        for ix_entry in tile["interactions"]:
            if ix_entry["step_id"] != "tile_python_errors_imports.s06":
                continue
            ix = ix_entry["interaction"]
            pub = ix["public"]

            # 1. Add 'import math' and 'math.sqrt()' to allowed_syntax
            allowed = pub["constraints"]["allowed_syntax"]
            if "import math" not in allowed:
                allowed.append("import math")
            if "math.sqrt()" not in allowed:
                allowed.append("math.sqrt()")

            # 2. Update solution: use top-level x = 144 so mutation changes result
            new_solution = (
                "import math\n"
                "\n"
                "x = 144\n"
                "result = math.sqrt(x)\n"
                "print(result)\n"
            )
            ix["grading"]["solution_files"][0]["content"] = new_solution

            # 3. Update starter to include x = 144 so learner sees the variable
            pub["workspace"]["files"][0]["content"] = (
                "# Import the math module and use math.sqrt() on x.\n"
                "# Store the result in a variable called result and print it.\n"
                "\n"
                "x = 144\n"
            )

            # 4. Update prompt to mention x
            pub["prompt"] = (
                "A starter variable `x = 144` is already defined.\n\n"
                "Import the `math` standard module, call `math.sqrt(x)`, "
                "store the result in a variable called `result`, and print it.\n\n"
                "Expected output: `12.0`"
            )

            # 5. Tests: value_equals and stdout_equals — expected stays 12.0
            #    (the hidden check will mutate x and verify result changes)
            for t in ix["grading"]["tests"]:
                if t["test_id"] == "t1_result":
                    t["spec"]["expected"] = 12.0
                if t["test_id"] == "t2_stdout":
                    t["spec"]["expected"] = "12.0"

    # ── tile_python_file_io ─────────────────────────────────────────────────
    if tid == "tile_python_file_io":
        for ix_entry in tile["interactions"]:
            if ix_entry["step_id"] != "tile_python_file_io.s06":
                continue
            ix = ix_entry["interaction"]
            pub = ix["public"]

            # Add 'import csv' to allowed_syntax
            allowed = pub["constraints"]["allowed_syntax"]
            if "import csv" not in allowed:
                allowed.append("import csv")

    # ── tile_python_pep8_style ──────────────────────────────────────────────
    if tid == "tile_python_pep8_style":
        for ix_entry in tile["interactions"]:
            if ix_entry["step_id"] != "tile_python_pep8_style.s03":
                continue
            ix = ix_entry["interaction"]
            pub = ix["public"]

            # Update solution: use top-level minutes=30, rate=2 so mutation works
            new_solution = (
                "minutes = 30\n"
                "rate = 2\n"
                "\n"
                "def calc_fee(minutes, rate):\n"
                "    fee = minutes * rate\n"
                "    return fee\n"
                "\n"
                "print(calc_fee(minutes, rate))\n"
            )
            ix["grading"]["solution_files"][0]["content"] = new_solution

            # Update starter to include the variables
            pub["workspace"]["files"][0]["content"] = (
                "minutes = 30\n"
                "rate = 2\n"
                "\n"
                "# Rewrite the function below to follow PEP 8 style.\n"
                "# Use 4-space indentation, lowercase_with_underscores names,\n"
                "# and tidy whitespace. Do not change what the function does.\n"
                "\n"
                "def CalcFee(Minutes,Rate):\n"
                "  Fee=Minutes*Rate\n"
                "  return Fee\n"
                "\n"
                "print(CalcFee(minutes, rate))\n"
            )

            # Update t1_stdout expected — still 60 when minutes=30, rate=2
            for t in ix["grading"]["tests"]:
                if t["test_id"] == "t1_stdout":
                    t["spec"]["expected"] = "60"

with open(PATH, "w") as f:
    json.dump(data, f, indent=2)

print("Patch applied.")
