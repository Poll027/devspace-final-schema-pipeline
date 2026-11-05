# EVALUATOR PACKET — Figures, Layout, and Basic Plotting (tile_viz_figures_layout_plotting)
Tile summary: Learn matplotlib's Figure/Axes object model, how to set figure size and call tight_layout, and how to use plt.plot() in both its one-argument and two-argument forms.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = viz.matplotlib_figure_axes — matplotlib figure and axes object model
B = viz.figure_size_layout — Adjusting figure size and layout
C = viz.pyplot_basic_plotting — Basic plot creation with the pyplot interface

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (viz.matplotlib_figure_axes)   objective: Recognize matplotlib's Figure/Axes object model: identify which calls create the Figure vs. the Axes, and create a Figure with one Axes to plot on.
A.f1: Matplotlib graphs data on Figures, and each Figure can contain one or more Axes, which is the area where data is actually plotted.   [sources: matplotlib_quickstart_guide#Parts of a Figure]
A.f2: fig, ax = plt.subplots() creates a Figure and one Axes together, giving explicit variables for both objects.   [sources: matplotlib_quickstart_guide#Coding styles]
A.f3: Plotting calls such as ax.plot(x, y) draw onto that specific Axes object.   [sources: matplotlib_quickstart_guide#Coding styles]
note: Establish the Figure/Axes container relationship clearly before any other viz concept -- everything in this tile builds on fig, ax = plt.subplots().
note: Don't introduce figsize or tight_layout here -- that's viz.figure_size_layout next.
PRACTICE ANCHOR (live_code): Create a Figure and one Axes explicitly using plt.subplots(), then draw a simple line on that Axes object using the delivery-times data.  SUCCESS: The learner's code assigns fig and ax from plt.subplots() and calls ax.plot() with two lists of equal length; fig and ax are used as separate named variables.
ASSESSMENT ANCHOR: identify_figure_vs_axes_roles facts=['f1']
ASSESSMENT ANCHOR: recognise_subplots_creates_figure_and_axes facts=['f2']
ASSESSMENT ANCHOR: identify_axes_as_target_of_plot_calls facts=['f3']
ASSESSMENT ANCHOR: map_plotting_task_to_correct_object facts=['f1', 'f2', 'f3']

## SOURCE FACTS — B (viz.figure_size_layout)   objective: Adjust a matplotlib figure's size using figsize and its subplot spacing using tight_layout so a plot renders clearly without overlapping labels.
B.f1: plt.subplots(figsize=(width, height)) sets the figure's dimensions; figsize is a (width, height) tuple which is interpreted as (width, height, 'in'), and its default is rcParams['figure.figsize'], which defaults to [6.4, 4.8].   [sources: matplotlib_official_docs#matplotlib.pyplot.figure]
B.f2: tight_layout() automatically adjusts subplot parameters so that the subplot(s) fit into the figure area; it works by checking the extents of tick labels, axis labels, and titles.   [sources: matplotlib_official_docs#Tight layout guide]
B.f3: tight_layout() can be called as plt.tight_layout() or fig.tight_layout().   [sources: matplotlib_official_docs#Tight layout guide]
note: This tile sits before any plotting concept, so there is no labeled or cramped plot yet to show tight_layout fixing -- teach figsize and tight_layout as general figure-level settings rather than as a fix for overlapping axis labels specifically (that payoff comes later, once viz.labeling_annotation adds labels that can overlap). TOC conflict noted, not resolved here.
note: Optional enrichment (layout='constrained') is skipped -- not required.
note: TOC practice_objective says 'fix overlapping axis labels', but axis labels are introduced in viz.labeling_annotation (blocked). The practice task has been adapted to the achievable subset: creating a custom-sized figure and calling tight_layout, without requiring any labels to overlap or be fixed.
PRACTICE ANCHOR (live_code): Create a figure with a custom figsize and call tight_layout on it.  SUCCESS: A figure object is created via plt.subplots with a figsize tuple that differs from the default [6.4, 4.8], and tight_layout is called on it without error using either plt.tight_layout() or fig.tight_layout().
ASSESSMENT ANCHOR: set_figure_size_with_figsize facts=['f1']
ASSESSMENT ANCHOR: apply_tight_layout_to_fit_subplots facts=['f2', 'f3']

## SOURCE FACTS — C (viz.pyplot_basic_plotting)   objective: Create a basic plot from data using matplotlib's pyplot interface, with the correct plt.plot() argument form.
C.f1: plt.plot(y) called with a single array argument treats it as the y-values and automatically generates the x-values starting from 0.   [sources: matplotlib_pyplot_tutorial#Introduction to pyplot]
C.f2: plt.plot(x, y) called with two array arguments plots the y-values against the given x-values.   [sources: matplotlib_pyplot_tutorial#Introduction to pyplot]
note: TOC conflict: this concept's practice_objective asks for a 'line chart', but line charts as a concept (trend over time, connecting points) belong to the later viz.line_plots. Here, teach plt.plot()'s two argument forms generically, without the 'trend' framing -- that framing is introduced next.
note: TOC conflict (practice): the practice_objective names a 'line chart', but viz.line_plots (trend framing) is blocked. The practice_anchor is scoped to the two plt.plot() argument forms only, with no trend or time-series framing, and the starter data uses the concept's own delivery_times/days running example rather than any time-series narrative.
PRACTICE ANCHOR (live_code): Plot a simple line of one numeric series using plt.plot(), first with a single list argument and then with explicit x and y lists.  SUCCESS: Two plt.plot() calls execute without error: one using only a y-values list (x-axis starts at 0), and one using both an x-values list and a y-values list (x-axis shows the supplied values).
ASSESSMENT ANCHOR: identify_single_arg_plot_auto_x_behavior facts=['f1']
ASSESSMENT ANCHOR: produce_two_arg_plot_with_explicit_x_values facts=['f2']
ASSESSMENT ANCHOR: distinguish_one_arg_from_two_arg_pyplot_call facts=['f1', 'f2']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjusting figure size and layout; Bar charts; Basic A/B test structure (control vs treatment group); Basic plot creation with the pyplot interface; Box plots; Conceptual effect of sample size on confidence; Conceptual interpretation of statistical significance/confidence level; Converting a vague business question into a specific, measurable analytical question; Custom styling/theming (advanced/optional); Drawing a business conclusion from an experiment-result summary; Framing an actionable recommendation that is distinct from the finding itself; Histograms; Identifying stakeholder needs/requirements before analysis; Identifying the business decision a stakeholder needs the analysis to inform; Interpreting lift/percentage change between groups; Labeling axes, titles, and legends; Line plots; Making a data-driven recommendation; Matching chart type to the analytical question; Multi-panel figures/subplots (advanced/optional); Plotting directly from pandas DataFrames with seaborn; Prioritizing findings by relevance to the stakeholder's specific decision, not by analytical interestingness; Scatter plots; Stating a finding precisely and quantitatively (the specific number or comparison,

## LESSON, in learner order

### s01 · explainer · The Figure and the Axes  [reward 5]
matplotlib basics — Every matplotlib graph lives inside two nested objects — learn which is which before writing code.
(intro) Imagine this week's QuickDeliver delivery times — 18, 22, 26, 19, 30 minutes — as a graph instead of a list. Matplotlib draws that graph onto two different kinds of object. Matplotlib graphs data on Figures, and each Figure can contain one or more Axes, which is the area where data is actually plotted. ⟦A.f1 A:tb1⟧
(definition) The Figure is the overall canvas — the whole window or image you display or save. An Axes is one plotting area inside that Figure: the rectangle with its own x- and y-axis where lines, bars, or points are drawn. A single Figure can hold more than one Axes. ⟦A.f1 A:tb2⟧
(syntax) After `import matplotlib.pyplot as plt`, `fig, ax = plt.subplots()` creates a Figure and one Axes together: `fig` refers to the whole canvas, `ax` refers to the plotting area inside it. ⟦A.f2 A:tb3⟧
[DIAGRAM: Figure contains Axes] nodes=['Figure (canvas)', 'Axes (plotting area)', 'line drawn on Axes'] edges=[('figure_node', 'axes_node', 'contains'), ('axes_node', 'line_node', 'renders')] alt: A box-within-a-box diagram: the outer rectangle is labelled 'Figure (canvas)'; inside it sits a smaller rectangle labelled 'Axes (plotting area)'; inside the Axes a simple line represents plotted data.

### s02 · video · Figure and Axes: the container relationship in code  [reward 5]
watch — 
[VIDEO Figure and Axes: the container relationship in code] bridge-before: The first clip names the Figure/Axes/axis hierarchy; note the presenter's canvas analogy matches Devspace's. The second clip shows plt.subplots() being written; watch how fig and ax are assigned together. | bridge-after: Neither clip shows ax.plot() being called — the teaching text covers that, along with the rule that plotted data attaches to the Axes, not the Figure.
  - 7Lc2AxiM17o 303-361s facts=['f1'] label: Figure as canvas, Axes as plotting area — the architecture explained | summary: The presenter defines the three-level hierarchy: a Figure is the top-level container — the entire window or page — while an Axes (spelled with an 'e') is the actual plot area where a specific piece of data is drawn, and a single Figure can hold multiple Axes. The axis (no 'e') is the familiar x- or y-axis that lives inside one Axes. The segment closes by restating the canvas framing: Figure is the canvas, each Axes is one painting on it.
  - XFZRVnP-MTU 274-402s facts=['f1', 'f2'] label: Creating a Figure and one Axes explicitly with plt.subplots() | summary: The presenter recaps that the Figure is the container holding all plots — the whole window — and that Axes are the actual plots inside it, with a Figure able to hold more than one. They then introduce the object-oriented approach: writing fig, ax = plt.subplots() instantiates both a Figure and an Axes at once. Because no row or column count is passed, subplots defaults to a one-by-one grid, producing exactly one Axes assigned to ax.

### s03 · explainer · Plotting onto the Axes  [reward 5]
matplotlib basics — All drawing goes through ax — not fig.
(example) Plotting calls such as `ax.plot(x, y)` draw onto that Axes object. After `fig, ax = plt.subplots()`, `ax.plot([1, 2, 3, 4, 5], [18, 22, 26, 19, 30])` draws the delivery times as a line onto `ax`. The Figure never receives plotted data — it just holds the Axes. ⟦A.f2 A.f3 A:tb4⟧

### s04 · check · Figure or Axes?  [reward 10]
quick check — Choose the right object for each plotting task.
QUESTION [choice, intro, grading=client] After running `fig, ax = plt.subplots()`, you want to draw a line of QuickDeliver delivery times. Which object do you call `.plot()` on?
  ✔ opt_ax: `ax` — the Axes object
      why: Correct. Plotting calls such as `ax.plot(x, y)` draw onto the Axes object — the rectangle with its own x- and y-axis where data is actually rendered.
  ✘ opt_fig: `fig` — the Figure object
      why: Not quite. The Figure is the overall canvas — it holds the Axes but never receives plotted data directly. Plotting calls go on `ax`, not `fig`.
  ✘ opt_plt: `plt` — the pyplot module directly
      why: Not quite. `plt.plot()` is a different function from `ax.plot()`. When you have an explicit `ax` variable from `plt.subplots()`, you call `ax.plot()` to draw onto that specific Axes.
  ✘ opt_either: Either `fig` or `ax` — they both hold the same data
      why: Not quite. Only the Axes (`ax`) receives plotted data. The Figure (`fig`) is the canvas that contains the Axes — it does not hold data itself.
  feedback✔: Exactly right. The Axes is the plotting area — all drawing calls go on `ax`.  feedback✘: Remember: `fig, ax = plt.subplots()` gives you two objects. The Figure (`fig`) is the canvas; the Axes (`ax`) is where data is drawn. Plotting calls go on `ax`.  hints: ["Think about which object is described as 'the rectangle with its own x- and y-axis where data is drawn'.", '`plt.subplots()` returns two values — the first is the canvas, the second is the plotting area.']  remediation→r01
  MEASURES: A:map_plotting_task_to_correct_object(f1,f2,f3)   anchors=['assessment:map_plotting_task_to_correct_object']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s03

### s05 · hands_on · Create a Figure and Plot on Its Axes  [reward 15]
hands-on — Use `plt.subplots()` to get a Figure and an Axes, then draw delivery times onto the Axes.
QUESTION [code_exercise, intro, grading=client] Two lists are already defined: `days = [1, 2, 3, 4, 5]` and `delivery_times = [21, 23, 19, 25, 20]`. A Figure and Axes have already been created with `fig, ax = plt.subplots()`.

Call `ax.plot(days, delivery_times)` to draw the data onto the Axes.

The figure should contain exactly one Axes with one line whose x-values are `days` and y-values are `delivery_times`.
  runtime={'kind': 'chart_renderer', 'version': '0.29.5', 'packages': ['matplotlib', 'pandas']} constraints.allowed=['import matplotlib.pyplot as plt', 'fig, ax = plt.subplots()', 'ax.plot(x, y)'] blocked=15 items
  file solution.py [editable]:
import matplotlib.pyplot as plt

# Data (these values will be changed by the grader to test your code)
day_1 = 1
days = [day_1, 2, 3, 4, 5]
dt_1 = 21
delivery_times = [dt_1, 23, 19, 25, 20]

fig, ax = plt.subplots()

# Draw delivery_times against days on the Axes
# ax.plot(..., ...)

  SOLUTION solution.py:
import matplotlib.pyplot as plt

# Data (these values will be changed by the grader to test your code)
day_1 = 1
days = [day_1, 2, 3, 4, 5]
dt_1 = 21
delivery_times = [dt_1, 23, 19, 25, 20]

fig, ax = plt.subplots()

ax.plot(days, delivery_times)

  test ix.tile_viz_figures_layout_plotting.s05.t01 (figure_equals, visible=True): {"expected":{"n_axes":1,"chart_types":[["line"]]}} | on-fail: Your figure should contain exactly one Axes with one line. Make sure you called `fig, ax = plt.subplots()` and then `ax.plot(days, delivery_times)`.
  test ix.tile_viz_figures_layout_plotting.s05.t02 (plotted_data_equals, visible=True): {"chart":"line","field":"x","expected":[1,2,3,4,5],"series":0,"axes":0} | on-fail: The x-values of the line should be the `days` list. Pass `days` as the first argument to `ax.plot()`.
  test ix.tile_viz_figures_layout_plotting.s05.t03 (plotted_data_equals, visible=True): {"chart":"line","field":"y","expected":[21,23,19,25,20],"series":0,"axes":0} | on-fail: The y-values of the line should be the `delivery_times` list. Pass `delivery_times` as the second argument to `ax.plot()`.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"e61e2bc41c8b26678669e09dbe4aa17e8618bf9b6bf0c42fe9c91f3c7648e2fe","tests_passed":3}
  feedback✔: Well done! You created a Figure and an Axes with `plt.subplots()` and drew the delivery times onto the Axes with `ax.plot(days, delivery_times)`.  feedback✘: Check that you called `fig, ax = plt.subplots()` first, then `ax.plot(days, delivery_times)`. The data must be drawn on `ax`, not on `fig`.  hints: ['`plt.subplots()` returns two values — assign them as `fig, ax = plt.subplots()`.', 'Once you have `ax`, call `ax.plot(days, delivery_times)` — the first argument is x, the second is y.']
  MEASURES: A:identify_figure_vs_axes_roles(f1); A:recognise_subplots_creates_figure_and_axes(f2); A:identify_axes_as_target_of_plot_calls(f3)   anchors=['practice', 'assessment:identify_figure_vs_axes_roles', 'assessment:recognise_subplots_creates_figure_and_axes', 'assessment:identify_axes_as_target_of_plot_calls']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s03

### s06 · explainer · Setting Figure Size and Fitting the Layout  [reward 5]
figure layout — Two settings on the Figure object control how big it is and whether its contents fit without clipping.
(definition) `plt.subplots(figsize=(width, height))` sets the figure's dimensions. `figsize` is a (width, height) tuple measured in inches; its default is [6.4, 4.8]. Passing `figsize=(8, 4)` makes a wider-than-default figure, 8 inches by 4 inches. ⟦B.f1 B:tb1⟧
(mechanism) `tight_layout()` automatically adjusts subplot parameters so the subplot(s) fit into the figure area; it checks the extents of tick labels, axis labels, and titles. Call it as `plt.tight_layout()` or `fig.tight_layout()`. ⟦B.f2 B.f3 B:tb2⟧
[CODE python]
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(8, 4))
fig.tight_layout()
  annotations: ['figsize=(8, 4) sets the canvas to 8 inches wide by 4 inches tall', 'fig.tight_layout() adjusts spacing so subplot contents fit within the figure area']

### s07 · check · Fitting the Layout  [reward 10]
quick check — Which call adjusts subplot spacing so labels don't get clipped?
QUESTION [choice, core, grading=client] You have created a figure with `fig, ax = plt.subplots(figsize=(8, 4))`. Which of the following is true about calling `tight_layout`?
  ✘ opt_fig_tight: `fig.tight_layout()` is the only correct way to call `tight_layout`
      why: Not quite. `fig.tight_layout()` is a valid call, but it is not the only way. `plt.tight_layout()` also adjusts subplot spacing — both forms are correct.
  ✘ opt_plt_tight: `plt.tight_layout()` is the only correct way to call `tight_layout`
      why: Not quite. `plt.tight_layout()` is a valid call, but it is not the only way. `fig.tight_layout()` also adjusts subplot spacing — both forms are correct.
  ✔ opt_both: Both `fig.tight_layout()` and `plt.tight_layout()` are correct
      why: Correct. `tight_layout()` can be called as `plt.tight_layout()` or `fig.tight_layout()` — both automatically adjust subplot parameters so the subplot fits into the figure area.
  ✘ opt_ax_tight: `ax.tight_layout()`
      why: Incorrect. `tight_layout()` is a Figure-level method, not an Axes method. Call it as `fig.tight_layout()` or `plt.tight_layout()`, not on `ax`.
  feedback✔: Right! `tight_layout()` can be called on the figure object (`fig.tight_layout()`) or via pyplot (`plt.tight_layout()`) — both work.  feedback✘: `tight_layout()` is a Figure-level operation. It can be called as `fig.tight_layout()` or `plt.tight_layout()` — both adjust subplot spacing automatically.  hints: ['The fact says `tight_layout()` can be called in two ways — one uses the `fig` variable, the other uses `plt` directly.', '`tight_layout()` is not a method on the Axes (`ax`) — it operates on the Figure.']  remediation→r02
  MEASURES: B:apply_tight_layout_to_fit_subplots(f2,f3)   anchors=['assessment:apply_tight_layout_to_fit_subplots']
  taught-before-tested: B.f2←s06; B.f3←s06

### s08 · hands_on · Custom Figure Size and Tight Layout  [reward 15]
hands-on — Create a figure with a custom `figsize` and call `tight_layout` on it.
QUESTION [code_exercise, core, grading=client] Variables `target_width` and `target_height` are already defined (currently 10 and 5). Create a figure with those dimensions, then call `tight_layout` on it.

Steps:
1. Call `plt.subplots(figsize=(target_width, target_height))` and assign the result to `fig` and `ax`.
2. Call `fig.tight_layout()` to adjust the subplot spacing.

After running, `fig.get_size_inches()` should return `[target_width, target_height]`.
  runtime={'kind': 'chart_renderer', 'version': '0.29.5', 'packages': ['matplotlib']} constraints.allowed=['plt.subplots(figsize=(width, height))', 'fig.tight_layout()', 'plt.tight_layout()', 'tuple literals for figsize', 'variable assignment (fig, ax = ...)'] blocked=11 items
  file solution.py [editable]:
import matplotlib.pyplot as plt

# Target dimensions (these values will be changed by the grader)
target_width = 10
target_height = 5

# Step 1: create a figure with the target dimensions
# fig, ax = plt.subplots(figsize=(..., ...))

# Step 2: apply tight layout
# fig.tight_layout()

  SOLUTION solution.py:
import matplotlib.pyplot as plt

# Target dimensions (these values will be changed by the grader)
target_width = 10
target_height = 5

fig, ax = plt.subplots(figsize=(target_width, target_height))
fig.tight_layout()

  test ix.tile_viz_figures_layout_plotting.s08.t01 (figure_equals, visible=True): {"expected":{"n_axes":1}} | on-fail: Your figure should contain exactly one Axes. Make sure you called `plt.subplots(figsize=(target_width, target_height))`.
  test ix.tile_viz_figures_layout_plotting.s08.t02 (value_equals, visible=True): {"expr":"fig.get_size_inches()[0]","expected":10.0} | on-fail: The figure width should be `target_width`. Pass `figsize=(target_width, target_height)` to `plt.subplots()`.
  test ix.tile_viz_figures_layout_plotting.s08.t03 (value_equals, visible=True): {"expr":"fig.get_size_inches()[1]","expected":5.0} | on-fail: The figure height should be `target_height`. Pass `figsize=(target_width, target_height)` to `plt.subplots()`.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"3b3663215a2d224666428a24c171d49fbcdb67adbb7b46a743a5d0f070295148","tests_passed":3}
  feedback✔: Well done! You created a 10×5-inch figure with `plt.subplots(figsize=(10, 5))` and called `fig.tight_layout()` to fit the layout.  feedback✘: Make sure you pass `figsize=(10, 5)` to `plt.subplots()` and then call `fig.tight_layout()` (or `plt.tight_layout()`) on the result.  hints: ['`figsize` takes a (width, height) tuple in inches — `figsize=(10, 5)` means 10 inches wide, 5 inches tall.', 'After creating the figure, call `fig.tight_layout()` — this adjusts the subplot spacing automatically.']
  MEASURES: B:set_figure_size_with_figsize(f1); B:apply_tight_layout_to_fit_subplots(f2,f3)   anchors=['practice', 'assessment:set_figure_size_with_figsize', 'assessment:apply_tight_layout_to_fit_subplots']
  taught-before-tested: B.f1←s06; B.f2←s06; B.f3←s06

### s09 · explainer · Two Ways to Call plt.plot()  [reward 5]
pyplot interface — pyplot's `plot()` function accepts data in two forms — learn which x-axis you get from each.
(intro) You have already seen `ax.plot(x, y)` draw onto an Axes created with `plt.subplots()`. pyplot also has its own `plot()` function, called directly as `plt.plot()`, and it accepts data in two different forms. ⟦C.f1 C.f2 C:tb1⟧
(syntax) `plt.plot(y)` with a single argument treats it as y-values and automatically generates x-values starting from 0. `plt.plot([18, 22, 26, 19, 30])` plots those five delivery times against the automatic x-positions 0, 1, 2, 3, 4. ⟦C.f1 C:tb2⟧
(syntax) `plt.plot(x, y)` with two arguments plots y-values against the given x-values instead. `plt.plot([1, 2, 3, 4, 5], [18, 22, 26, 19, 30])` plots the same delivery times against day numbers 1 through 5, not the automatic 0-based positions. ⟦C.f2 C:tb3⟧
[SIDE_BY_SIDE] Both forms call the same function; the only difference is whether you supply x-values or let pyplot number them from 0. left_label: plt.plot(y) — automatic x-axis (0-based) | right_label: plt.plot(x, y) — supplied x-axis
  left:
[CODE python]
plt.plot([18, 22, 26, 19, 30])
# x-axis: 0, 1, 2, 3, 4 (auto)
  annotations: ['Single argument: y-values only; x starts at 0']
  right:
[CODE python]
plt.plot([1, 2, 3, 4, 5], [18, 22, 26, 19, 30])
# x-axis: 1, 2, 3, 4, 5 (supplied)
  annotations: ['Two arguments: x-values first, then y-values']

### s10 · video · Two ways to call plt.plot(): supplying x and y vs. y alone  [reward 5]
watch — 
[VIDEO Two ways to call plt.plot(): supplying x and y vs. y alone] bridge-before: Watch how the x-axis changes between the two calls — explicit years in the first, automatic 0-based positions in the second. The instructor uses plt.show(); Devspace's text focuses on the two argument forms. | bridge-after: Both forms call the same function; the only difference is whether you supply x-values or let pyplot number them from 0. The text covers both forms completely.
  - 2KY5AaFvWtE 179-367s facts=['f1', 'f2'] label: plt.plot(x, y) with explicit coordinates, then plt.plot(y) with automatic x-positions | summary: The instructor builds two Python lists — years as x-values and class sizes as y-values — then calls plt.plot(x, y), naming the first argument as x-axis points and the second as y-axis points, and calls plt.show() to display the result. The rendered plot maps each year to its class size. The instructor then demonstrates the single-argument form: passing only the y-values list, with the note that plt.plot() defaults to starting at zero and stepping by one for the x-positions, so the x-axis is filled in automatically.

### s11 · check · One Argument or Two?  [reward 10]
quick check — Identify which plt.plot() form produces which x-axis.
QUESTION [choice, core, grading=client] You call `plt.plot([18, 22, 26, 19, 30])` with a single list argument. What x-values does matplotlib use for the plot?
  ✔ opt_auto_0: Automatic positions starting from 0: 0, 1, 2, 3, 4
      why: Correct. `plt.plot(y)` with a single argument treats the list as y-values and automatically generates x-positions starting from 0 (0, 1, 2, 3, 4 for five values).
  ✘ opt_auto_1: Automatic positions starting from 1: 1, 2, 3, 4, 5
      why: Not quite. The automatic x-positions start from 0, not 1. For five y-values, matplotlib uses x = 0, 1, 2, 3, 4.
  ✘ opt_values: The y-values themselves: 18, 22, 26, 19, 30
      why: Not quite. The single argument is treated as y-values, not x-values. Matplotlib generates its own x-positions starting from 0.
  ✘ opt_none: No x-axis is drawn — a single argument produces a bar chart instead
      why: Not quite. `plt.plot()` always draws a line chart. With a single argument it uses the list as y-values and auto-generates x-positions from 0.
  feedback✔: Exactly right. `plt.plot(y)` auto-generates x-positions starting at 0 — so five values get x = 0, 1, 2, 3, 4.  feedback✘: `plt.plot(y)` treats its single argument as y-values and fills in x-positions automatically starting from 0. To supply your own x-values, use `plt.plot(x, y)` with two arguments.  hints: ["The fact says: `plt.plot(y)` 'automatically generates the x-values starting from 0'.", 'Think about what index position the first element of a Python list has.']  remediation→r03
  MEASURES: C:distinguish_one_arg_from_two_arg_pyplot_call(f1,f2)   anchors=['assessment:distinguish_one_arg_from_two_arg_pyplot_call']
  taught-before-tested: C.f1←s09; C.f2←s09

### s12 · hands_on · Plot Delivery Times with plt.plot()  [reward 15]
hands-on — Call `plt.plot()` in both its one-argument and two-argument forms using the QuickDeliver delivery times.
QUESTION [code_exercise, stretch, grading=client] Two lists are already defined: `days = [1, 2, 3, 4, 5]` and `delivery_times = [21, 23, 19, 25, 20]`. Make **two** `plt.plot()` calls in the order shown:

1. **One-argument form**: call `plt.plot(delivery_times)` — matplotlib will auto-generate x-positions 0, 1, 2, 3, 4.
2. **Two-argument form**: call `plt.plot(days, delivery_times)` — you provide both x and y explicitly.

The figure should contain two lines: the first with x-values [0, 1, 2, 3, 4] and the second with x-values from `days`.
  runtime={'kind': 'chart_renderer', 'version': '0.29.5', 'packages': ['matplotlib', 'pandas']} constraints.allowed=['import matplotlib.pyplot as plt', 'plt.plot(y_list)', 'plt.plot(x_list, y_list)'] blocked=11 items
  file solution.py [editable]:
import matplotlib.pyplot as plt

# Data (these values will be changed by the grader to test your code)
day_1 = 1
days = [day_1, 2, 3, 4, 5]
dt_1 = 21
delivery_times = [dt_1, 23, 19, 25, 20]

# Step 1: one-argument form (auto-generates x-positions 0, 1, 2, ...)
# plt.plot(...)

# Step 2: two-argument form (explicit x and y)
# plt.plot(..., ...)

  SOLUTION solution.py:
import matplotlib.pyplot as plt

# Data (these values will be changed by the grader to test your code)
day_1 = 1
days = [day_1, 2, 3, 4, 5]
dt_1 = 21
delivery_times = [dt_1, 23, 19, 25, 20]

plt.plot(delivery_times)
plt.plot(days, delivery_times)

  test ix.tile_viz_figures_layout_plotting.s12.t01 (figure_equals, visible=True): {"expected":{"n_axes":1,"chart_types":[["line"]]}} | on-fail: Your figure should contain exactly one Axes with two lines. Make sure you called `plt.plot()` twice.
  test ix.tile_viz_figures_layout_plotting.s12.t02 (plotted_data_equals, visible=True): {"chart":"line","field":"y","expected":[21,23,19,25,20],"series":0,"axes":0} | on-fail: The first line's y-values should be the `delivery_times` list. Call `plt.plot(delivery_times)`.
  test ix.tile_viz_figures_layout_plotting.s12.t04 (plotted_data_equals, visible=True): {"chart":"line","field":"x","expected":[1,2,3,4,5],"series":1,"axes":0} | on-fail: The second line's x-values should be the `days` list. Call `plt.plot(days, delivery_times)`.
  test ix.tile_viz_figures_layout_plotting.s12.t05 (plotted_data_equals, visible=True): {"chart":"line","field":"y","expected":[21,23,19,25,20],"series":1,"axes":0} | on-fail: The second line's y-values should be the `delivery_times` list. Call `plt.plot(days, delivery_times)`.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"38a54677afa92752822d713f028dfc00cb5def327250f7849203d81bb32153fe","tests_passed":4}
  feedback✔: Excellent! You used both forms: `plt.plot(delivery_times)` auto-numbered the x-axis from 0, and `plt.plot(days, delivery_times)` used your supplied day numbers.  feedback✘: Make sure you made exactly two `plt.plot()` calls: first `plt.plot(delivery_times)` (one argument, auto x from 0), then `plt.plot(days, delivery_times)` (two arguments, explicit x).  hints: ['The one-argument form is `plt.plot(delivery_times)` — pass only the y-values list.', 'The two-argument form is `plt.plot(days, delivery_times)` — x-values first, y-values second.']
  MEASURES: C:identify_single_arg_plot_auto_x_behavior(f1); C:produce_two_arg_plot_with_explicit_x_values(f2); C:distinguish_one_arg_from_two_arg_pyplot_call(f1,f2)   anchors=['practice', 'assessment:identify_single_arg_plot_auto_x_behavior', 'assessment:produce_two_arg_plot_with_explicit_x_values', 'assessment:distinguish_one_arg_from_two_arg_pyplot_call']
  taught-before-tested: C.f1←s09; C.f2←s09; C.f1←s09; C.f2←s09

### s13 · recap · What You've Learned  [reward 10]
recap — Three concepts, one workflow: create a Figure, size it, and plot onto its Axes.
(takeaway) With `plt.subplots()` you get a Figure and an Axes first, then call a plotting method on the Axes, not the Figure. Figure is the canvas; Axes is where data goes. Set `figsize` to control canvas dimensions and call `tight_layout()` to prevent labels from clipping. ⟦A.f1 A.f2 A.f3 B.f1 B.f2 B.f3 A:tb5 B:tb1 B:tb2⟧
(takeaway) Both `plt.plot(y)` and `plt.plot(x, y)` call the same function; the only difference is whether you supply x-values or let pyplot number them from 0. ⟦C.f1 C.f2 C:tb4⟧
[UP NEXT] Up next: Bar Charts and Histograms: In the next tile you will use `plt.bar()` to compare average delivery times across Lagos, Abuja, and Kano — building directly on the Figure/Axes model you just learned.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Figure vs. Axes — Which Object Does What? — A quick contrast to clarify which object is the canvas and which one receives your data.
(definition) The Figure is the outer canvas — the whole window. The Axes is the inner plotting area where data is drawn. `fig, ax = plt.subplots()` creates both at once: `fig` is the canvas, `ax` is the plotting area. Plotting calls like `ax.plot(x, y)` go on `ax`, never on `fig`. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4⟧
### r02 · tight_layout() — What It Does and How to Call It — A clear contrast between calling tight_layout and not calling it.
(mechanism) `tight_layout()` automatically adjusts subplot parameters so the subplot(s) fit into the figure area; it checks the extents of tick labels, axis labels, and titles. Without it, labels can be clipped or overlap. Call it as `plt.tight_layout()` or `fig.tight_layout()` — both work. ⟦B.f2 B.f3 B:tb2⟧
### r03 · plt.plot() — One Argument vs. Two — The x-axis is the only thing that changes between the two forms.
(syntax) `plt.plot([18, 22, 26, 19, 30])` uses one argument: the list is treated as y-values and x-positions are filled in automatically starting at 0 (so 0, 1, 2, 3, 4). `plt.plot([1, 2, 3, 4, 5], [18, 22, 26, 19, 30])` uses two arguments: the first list sets the x-axis to 1–5, the second sets the y-axis. Both calls produce a line; only the x-axis differs. ⟦C.f1 C.f2 C:tb2 C:tb3⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: plt.subplots(nrows, ncols) with more than one subplot