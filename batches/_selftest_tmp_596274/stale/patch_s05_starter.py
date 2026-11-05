import json

path = "batches/final_batch_012_da_viz/interactions.part.c0_canary.json"

with open(path) as f:
    data = json.load(f)

for tile in data["tiles"]:
    for item in tile["interactions"]:
        iid = item["interaction"].get("interaction_id")
        if iid == "ix.tile_viz_figures_layout_plotting.s05":
            pub = item["interaction"]["public"]
            # Update the starter to include fig, ax = plt.subplots() as actual code
            # so learner_part strips it and the judged code is only ax.plot(...)
            new_starter = (
                "import matplotlib.pyplot as plt\n"
                "\n"
                "# Data (these values will be changed by the grader to test your code)\n"
                "day_1 = 1\n"
                "days = [day_1, 2, 3, 4, 5]\n"
                "dt_1 = 21\n"
                "delivery_times = [dt_1, 23, 19, 25, 20]\n"
                "\n"
                "fig, ax = plt.subplots()\n"
                "\n"
                "# Draw delivery_times against days on the Axes\n"
                "# ax.plot(..., ...)\n"
            )
            pub["workspace"]["files"][0]["content"] = new_starter

            # Update the solution to match (fig, ax = plt.subplots() is now in starter)
            new_solution = (
                "import matplotlib.pyplot as plt\n"
                "\n"
                "# Data (these values will be changed by the grader to test your code)\n"
                "day_1 = 1\n"
                "days = [day_1, 2, 3, 4, 5]\n"
                "dt_1 = 21\n"
                "delivery_times = [dt_1, 23, 19, 25, 20]\n"
                "\n"
                "fig, ax = plt.subplots()\n"
                "\n"
                "ax.plot(days, delivery_times)\n"
            )
            item["interaction"]["grading"]["solution_files"][0]["content"] = new_solution

            # Update the prompt to reflect that plt.subplots() is already provided
            pub["prompt"] = (
                "Two lists are already defined: `days = [1, 2, 3, 4, 5]` and "
                "`delivery_times = [21, 23, 19, 25, 20]`. "
                "A Figure and Axes have already been created with `fig, ax = plt.subplots()`.\n\n"
                "Call `ax.plot(days, delivery_times)` to draw the data onto the Axes.\n\n"
                "The figure should contain exactly one Axes with one line whose x-values are "
                "`days` and y-values are `delivery_times`."
            )

            print(f"Patched {iid}: starter and solution updated")

with open(path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("Done.")
