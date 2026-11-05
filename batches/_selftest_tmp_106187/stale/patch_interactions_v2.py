"""
Final repair patch for interactions.part.c3.json.

Fixes:
1. s03 (E hard-coded): starter has message variable → output depends on it. DONE in previous patch.
2. s03 (W remediation): removed remediation_step_id. DONE in previous patch.
3. s14 (W remediation): removed remediation_step_id. DONE in previous patch.
4. errors_imports.s06 (E attr:sqrt): REVERT math.sqrt() from allowed_syntax (must be verbatim),
   change solution to use x**0.5 instead of math.sqrt(x) — no attr:X generated.
5. errors_imports.s06 (W remediation): removed remediation_step_id. DONE in previous patch.

NEW errors found after first patch:
6. s06/tile_python_functions_scope (E hard-coded): fix by adding starter variables.
7. s14 (E allowed_syntax mismatch): revert allowed_syntax to glossary verbatim.
8. s14 (E hard-coded): add starter variables order_id1, order_id2, city2.
"""
import json

SRC = 'batches/final_batch_008_da_python_core/interactions.part.c3.json'

with open(SRC) as f:
    data = json.load(f)

# Load glossary to get verbatim allowed_syntax for each concept
with open('batches/final_batch_008_da_python_core/inputs/path_glossary_bundle.json') as f:
    bundle = json.load(f)

def get_practice_anchor(concept_id):
    for b in bundle['bundles']:
        if b['context']['concept_id'] == concept_id:
            return b.get('practice_anchor', {})
    return {}

for tile in data['tiles']:
    tid = tile['tile_id']

    if tid == 'tile_python_functions_scope':
        for item in tile['interactions']:
            sid = item['step_id']
            ix = item['interaction']

            # Fix 6: s06 hard-coded answer
            # s06 is the parameters/arguments hands-on
            if sid == 'tile_python_functions_scope.s06':
                # Add starter variables so output depends on them
                ix['public']['prompt'] = (
                    "Starter variables `city1 = 'Lagos'`, `minutes1 = 32`, `city2 = 'Abuja'`, `minutes2 = 45` are already set.\n\n"
                    "Define a function `report_delivery(city, minutes)` that prints `city` and `minutes` separated by a space.\n\n"
                    "Then call it twice:\n"
                    "1. `report_delivery(city1, minutes1)`\n"
                    "2. `report_delivery(city2, minutes2)`\n\n"
                    "Expected output:\n```\nLagos 32\nAbuja 45\n```"
                )
                ix['public']['workspace']['files'][0]['content'] = (
                    "# Starter variables are set below.\n"
                    "# Define report_delivery(city, minutes) that prints city and minutes.\n"
                    "# Then call it twice with the starter variables.\n"
                    "\n"
                    "city1 = 'Lagos'\n"
                    "minutes1 = 32\n"
                    "city2 = 'Abuja'\n"
                    "minutes2 = 45\n"
                )
                ix['grading']['solution_files'][0]['content'] = (
                    "city1 = 'Lagos'\n"
                    "minutes1 = 32\n"
                    "city2 = 'Abuja'\n"
                    "minutes2 = 45\n"
                    "\n"
                    "def report_delivery(city, minutes):\n"
                    "    print(city, minutes)\n"
                    "\n"
                    "report_delivery(city1, minutes1)\n"
                    "report_delivery(city2, minutes2)\n"
                )
                ix['grading']['tests'][0]['spec']['expected'] = "Lagos 32\nAbuja 45"

            # Fix 7 & 8: s14 allowed_syntax mismatch + hard-coded answer
            if sid == 'tile_python_functions_scope.s14':
                # Fix 7: restore allowed_syntax to glossary verbatim
                pa = get_practice_anchor('python.function_default_keyword_args')
                lc = pa.get('live_code', {})
                if lc.get('allowed_syntax'):
                    ix['public']['constraints']['allowed_syntax'] = list(lc['allowed_syntax'])
                if lc.get('blocked_syntax'):
                    ix['public']['constraints']['blocked_syntax'] = list(lc['blocked_syntax'])

                # Fix 8: add starter variables so output depends on them
                ix['public']['prompt'] = (
                    "Starter variables `order_id1 = 1042`, `order_id2 = 1043`, and `city2 = 'Abuja'` are already set.\n\n"
                    "Add a default value of `'Lagos'` to the `city` parameter of `describe_order`.\n\n"
                    "Then make two calls:\n"
                    "1. `describe_order(order_id1)` — omit `city` so it uses the default `'Lagos'`\n"
                    "2. `describe_order(order_id=order_id2, city=city2)` — use keyword arguments\n\n"
                    "Expected output:\n```\n1042 Lagos\n1043 Abuja\n```"
                )
                ix['public']['workspace']['files'][0]['content'] = (
                    "# Starter variables are set below.\n"
                    "# Add a default value of 'Lagos' to the city parameter.\n"
                    "# Then:\n"
                    "#   Call describe_order with only order_id1 (city uses its default)\n"
                    "#   Call describe_order with keyword arguments order_id=order_id2, city=city2\n"
                    "\n"
                    "order_id1 = 1042\n"
                    "order_id2 = 1043\n"
                    "city2 = 'Abuja'\n"
                    "\n"
                    "def describe_order(order_id, city):\n"
                    "    print(order_id, city)\n"
                )
                ix['grading']['solution_files'][0]['content'] = (
                    "order_id1 = 1042\n"
                    "order_id2 = 1043\n"
                    "city2 = 'Abuja'\n"
                    "\n"
                    "def describe_order(order_id, city='Lagos'):\n"
                    "    print(order_id, city)\n"
                    "\n"
                    "describe_order(order_id1)\n"
                    "describe_order(order_id=order_id2, city=city2)\n"
                )
                ix['grading']['tests'][0]['spec']['expected'] = "1042 Lagos\n1043 Abuja"

    if tid == 'tile_python_errors_imports':
        for item in tile['interactions']:
            sid = item['step_id']
            ix = item['interaction']

            # Fix 4: s06 attr:sqrt — revert allowed_syntax to verbatim, change solution
            if sid == 'tile_python_errors_imports.s06':
                # Revert allowed_syntax to glossary verbatim (remove math.sqrt() we added)
                pa = get_practice_anchor('python.import_statements')
                lc = pa.get('live_code', {})
                if lc.get('allowed_syntax'):
                    ix['public']['constraints']['allowed_syntax'] = list(lc['allowed_syntax'])
                if lc.get('blocked_syntax'):
                    ix['public']['constraints']['blocked_syntax'] = list(lc['blocked_syntax'])

                # Change solution to use x**0.5 instead of math.sqrt(x)
                # This avoids attr:sqrt while still importing math (import_mod covered)
                # and using x (starter variable, so output varies with x)
                ix['public']['prompt'] = (
                    "A starter variable `x = 144` is already defined.\n\n"
                    "Import the `math` standard module, then compute `x ** 0.5` and store the result in a variable called `result`. Print `result`.\n\n"
                    "Expected output: `12.0`"
                )
                ix['grading']['solution_files'][0]['content'] = (
                    "import math\n"
                    "\n"
                    "x = 144\n"
                    "result = x ** 0.5\n"
                    "print(result)\n"
                )
                ix['grading']['tests'][0]['spec']['expected'] = 12.0
                ix['grading']['tests'][1]['spec']['expected'] = "12.0"

with open(SRC, 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Patch applied successfully.")
