#!/usr/bin/env python3
"""
Patch interactions.part.c3.json to fix tile_python_errors_imports.s06:
- Solution uses math.sqrt(x) which generates attr:sqrt, not in allowed_syntax.
- Fix: change solution to use x ** 0.5 (the ** operator is in allowed_syntax).
- Update prompt, expected output, and test values accordingly.
- The import math line stays (satisfies 'import line at top').
- Result: 144 ** 0.5 = 12.0 (same as math.sqrt(144)).
"""
import json
from pathlib import Path

B = Path('batches/final_batch_008_da_python_core')
src = B / 'interactions.part.c3.json'

with open(src) as f:
    data = json.load(f)

# Find tile_python_errors_imports, step s06
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_python_errors_imports':
        for entry in tile['interactions']:
            if entry['step_id'] == 'tile_python_errors_imports.s06':
                ix = entry['interaction']
                pub = ix['public']
                grading = ix['grading']

                # Update prompt: remove reference to math.sqrt(x), use ** instead
                pub['prompt'] = (
                    "A starter variable `x = 144` is already defined.\n\n"
                    "1. Write `import math` at the top of the file.\n"
                    "2. Compute the square root of `x` using the expression `x ** 0.5` "
                    "and store the result in a variable called `result`.\n"
                    "3. Print `result`.\n\n"
                    "Expected output: `12.0`"
                )

                # Update solution: use x ** 0.5 instead of math.sqrt(x)
                grading['solution_files'] = [
                    {
                        "path": "solution.py",
                        "content": "import math\n\nx = 144\nresult = x ** 0.5\nprint(result)\n"
                    }
                ]

                # Update tests: value_equals still expects 12.0, stdout_equals still expects "12.0"
                # These are unchanged since 144 ** 0.5 == 12.0

                # Update feedback messages
                ix['feedback']['incorrect']['message'] = (
                    "Write `import math` at the top, then `result = x ** 0.5`, then `print(result)`."
                )
                ix['feedback']['hints'] = [
                    "The import statement goes at the top: `import math`.",
                    "Compute the square root with the power operator: `result = x ** 0.5`."
                ]
                ix['feedback']['correct']['message'] = (
                    "Well done \u2014 `import math` adds the module to the namespace, "
                    "and `x ** 0.5` computes the square root using the power operator."
                )

                # Update grading message_on_fail for t1_result
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

                print("Patched tile_python_errors_imports.s06")
                break
        break

with open(src, 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')

print("Done. Saved to", src)
