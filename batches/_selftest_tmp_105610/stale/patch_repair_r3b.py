"""
Apply the same fixes to interactions.json (the merged file read by assemble_tiles.py).
"""
import json, pathlib

PATH = pathlib.Path("batches/final_batch_008_da_python_core/interactions.json")
data = json.loads(PATH.read_text())

for tile in data["tiles"]:
    tid = tile["tile_id"]

    if tid == "tile_python_lists_dicts_tuples":
        for entry in tile["interactions"]:
            sid = entry["step_id"]
            ix = entry["interaction"]

            if sid == "tile_python_lists_dicts_tuples.s13":
                pub = ix["public"]
                grading = ix["grading"]
                pub["workspace"]["files"][0]["content"] = (
                    "min_val = 32\n"
                    "max_val = 45\n"
                    "order_stats = (min_val, max_val)\n"
                    "# Unpack order_stats into min_time and max_time, then print each\n"
                )
                pub["prompt"] = (
                    "QuickDeliver records the minimum and maximum delivery times as a fixed pair.\n\n"
                    "`min_val`, `max_val`, and `order_stats` are already assigned below.\n\n"
                    "Add lines that:\n"
                    "1. Unpack `order_stats` into two variables: `min_time` and `max_time`\n"
                    "2. Print `min_time` and `max_time` each on its own line\n\n"
                    "Expected output:\n"
                    "```\n"
                    "32\n"
                    "45\n"
                    "```"
                )
                grading["solution_files"][0]["content"] = (
                    "min_val = 32\n"
                    "max_val = 45\n"
                    "order_stats = (min_val, max_val)\n"
                    "min_time, max_time = order_stats\n"
                    "print(min_time)\n"
                    "print(max_time)\n"
                )
                # Remove stale execution_provenance and hidden_checks so assemble recomputes
                grading.pop("execution_provenance", None)
                grading.pop("hidden_checks", None)

    if tid == "tile_python_sets_strings":
        for entry in tile["interactions"]:
            sid = entry["step_id"]
            ix = entry["interaction"]

            if sid == "tile_python_sets_strings.s06":
                pub = ix["public"]
                grading = ix["grading"]
                pub["workspace"]["files"][0]["content"] = (
                    "city_a = 'Lagos'\n"
                    "city_b = 'Abuja'\n"
                    "city_c = 'Kano'\n"
                    "city_d = 'Ibadan'\n"
                    "cities_list = [city_a, city_b, city_c, city_a, city_d, city_b]\n"
                    "# Build unique_cities set, then print membership for 'Lagos' and 'Enugu'\n"
                )
                pub["prompt"] = (
                    "QuickDeliver wants to know which unique cities appear in a batch of orders.\n\n"
                    "`city_a`, `city_b`, `city_c`, `city_d`, and `cities_list` are assigned below "
                    "(the list contains duplicates).\n\n"
                    "Add lines that:\n"
                    "1. Assign `unique_cities` — a set built from `cities_list` using `set()`\n"
                    "2. Print whether `'Lagos'` is in `unique_cities`\n"
                    "3. Print whether `'Enugu'` is in `unique_cities`\n\n"
                    "Expected output:\n"
                    "```\n"
                    "True\n"
                    "False\n"
                    "```"
                )
                grading["solution_files"][0]["content"] = (
                    "city_a = 'Lagos'\n"
                    "city_b = 'Abuja'\n"
                    "city_c = 'Kano'\n"
                    "city_d = 'Ibadan'\n"
                    "cities_list = [city_a, city_b, city_c, city_a, city_d, city_b]\n"
                    "unique_cities = set(cities_list)\n"
                    "print('Lagos' in unique_cities)\n"
                    "print('Enugu' in unique_cities)\n"
                )
                for t in grading["tests"]:
                    if t["test_id"] == "t2_unique_cities_type":
                        t["test_id"] = "t2_unique_count"
                        t["kind"] = "value_equals"
                        t["spec"] = {"expr": "len(unique_cities)", "expected": 4}
                        t["message_on_fail"] = (
                            "`unique_cities` should have 4 unique cities. "
                            "Use `set(cities_list)` — sets remove duplicates automatically."
                        )
                        break
                grading.pop("execution_provenance", None)
                grading.pop("hidden_checks", None)

            if sid == "tile_python_sets_strings.s08":
                fb = ix.get("feedback", {})
                if fb.get("remediation_step_id") == "tile_python_sets_strings.r02":
                    fb["remediation_step_id"] = "tile_python_sets_strings.r03"

PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False))
print("interactions.json patched.")
