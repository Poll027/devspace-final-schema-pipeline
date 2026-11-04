#!/usr/bin/env python3
"""
Patch interactions.json to fix tile_python_errors_imports.s06:
- Remove 'math.sqrt()' from allowed_syntax (not in glossary)
- Change solution from math.sqrt(x) to x ** 0.5
- Update prompt and feedback accordingly
"""
import json
from pathlib import Path

B = Path('batches/final_batch_008_da_python_core')
src = B / 'interactions.json'

with open(src) as f:
    data = json.load(f)

patched = False
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_python_errors_imports':
        for entry in tile['interactions']:
            if entry['step_id'] == 'tile_python_errors_imports.s06':
                ix = entry['interaction']
                pub = ix['public']
                grading = ix['grading']

                # Remove 'math.sqrt()' from allowed_syntax if present
                allowed = pub['constraints']['allowed_syntax']
                if 'math.sqrt()' in allowed:
                    allowed.remove('math.sqrt()')
                    print("Removed 'math.sqrt()' from allowed_syntax")

                # Update prompt
                pub['prompt'] = (
                    "A starter variable `x = 144` is already defined.\n\n"
                    "1. Write `import math` at the top of the file.\n"
                    "2. Compute the square root of `x` using the expression `x ** 0.5` "
                    "and store the result in a variable called `result`.\n"
                    "3. Print `result`.\n\n"
                    "Expected output: `12.0`"
                )

                # Update solution
                grading['solution_files'] = [
                    {
                        "path": "solution.py",
                        "content": "import math\n\nx = 144\nresult = x ** 0.5\nprint(result)\n"
                    }
                ]

                # Update feedback
                ix['feedback']['correct']['message'] = (
                    "Well done \u2014 `import math` adds the module to the namespace, "
                    "and `x ** 0.5` computes the square root using the power operator."
                )
                ix['feedback']['incorrect']['message'] = (
                    "Write `import math` at the top, then `result = x ** 0.5`, then `print(result)`."
                )
                ix['feedback']['hints'] = [
                    "The import statement goes at the top: `import math`.",
                    "Compute the square root with the power operator: `result = x ** 0.5`."
                ]

                # Update test messages
                for test in grading['tests']:
                    if test['test_id'] == 't1_result':
                        test['message_on_fail'] = (
                            "`result` should hold `12.0` (144 ** 0.5). "
                            "Make sure you write `result = x ** 0.5`."
                        )
                    elif test['test_id'] == 't2_stdout':
                        test['message_on_fail'] = (
                            "The program should print `12.0`. "
                            "Check that you call `print(result)` after the assignment."
                        )

                # Remove stale execution_provenance and hidden_checks (will be recomputed by assemble)
                grading.pop('execution_provenance', None)
                grading.pop('hidden_checks', None)

                print("Patched tile_python_errors_imports.s06 in interactions.json")
                patched = True
                break
        if patched:
            break

with open(src, 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')

print("Done. Saved to", src)
