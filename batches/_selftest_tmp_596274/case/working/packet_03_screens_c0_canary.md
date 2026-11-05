# EVALUATOR PACKET — Figures, Layout, and Basic Plotting (tile_viz_figures_layout_plotting)
Tile summary: Learn matplotlib's Figure/Axes object model, how to set figure size and call tight_layout, and how to use plt.plot() in both its one-argument and two-argument forms.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = viz.matplotlib_figure_axes — matplotlib figure and axes object model
B = viz.figure_size_layout — Adjusting figure size and layout
C = viz.pyplot_basic_plotting — Basic plot creation with the pyplot interface

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · explainer · Plotting onto the Axes  [reward 5]
matplotlib basics — All drawing goes through ax — not fig.
(example) Plotting calls such as `ax.plot(x, y)` draw onto that Axes object. After `fig, ax = plt.subplots()`, `ax.plot([1, 2, 3, 4, 5], [18, 22, 26, 19, 30])` draws the delivery times as a line onto `ax`. The Figure never receives plotted data — it just holds the Axes. ⟦A.f2 A.f3 A:tb4⟧

### s04 · check · Figure or Axes?  [reward 10]
quick check — Choose the right object for each plotting task.

### s05 · hands_on · Create a Figure and Plot on Its Axes  [reward 15]
hands-on — Use `plt.subplots()` to get a Figure and an Axes, then draw delivery times onto the Axes.

### s06 · explainer · Setting Figure Size and Fitting the Layout  [reward 5]
figure layout — Two settings on the Figure object control how big it is and whether its contents fit without clipping.
(definition) `plt.subplots(figsize=(width, height))` sets the figure's dimensions. `figsize` is a (width, height) tuple measured in inches; its default is [6.4, 4.8]. Passing `figsize=(8, 4)` makes a wider-than-default figure, 8 inches by 4 inches. ⟦B.f1 B:tb1⟧
(mechanism) `tight_layout()` automatically adjusts subplot parameters so the subplot(s) fit into the figure area; it checks the extents of tick labels, axis labels, and titles. Call it as `plt.tight_layout()` or `fig.tight_layout()`. ⟦B.f2 B.f3 B:tb2⟧
[CODE python]
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(8, 4))
fig.tight_layout()
  annotations: ['figsize=(8, 4) sets the canvas to 8 inches wide by 4 inches tall', 'fig.tight_layout() adjusts spacing so labels and titles fit without clipping']

### s07 · check · Fitting the Layout  [reward 10]
quick check — Which call adjusts subplot spacing so labels don't get clipped?

### s08 · hands_on · Custom Figure Size and Tight Layout  [reward 15]
hands-on — Create a figure with a custom `figsize` and call `tight_layout` on it.

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
[VIDEO ] bridge-before:  | bridge-after: 

### s11 · check · One Argument or Two?  [reward 10]
quick check — Identify which plt.plot() form produces which x-axis.

### s12 · hands_on · Plot Delivery Times with plt.plot()  [reward 15]
hands-on — Call `plt.plot()` in both its one-argument and two-argument forms using the QuickDeliver delivery times.

### s13 · recap · What You've Learned  [reward 10]
recap — Three concepts, one workflow: create a Figure, size it, and plot onto its Axes.
(takeaway) With `plt.subplots()` you get a Figure and an Axes first, then call a plotting method on the Axes, not the Figure. Figure is the canvas; Axes is where data goes. Set `figsize` to control canvas dimensions and call `tight_layout()` to prevent labels from clipping. ⟦A.f1 A.f2 A.f3 B.f1 B.f2 B.f3 A:tb5⟧
(takeaway) Both `plt.plot(y)` and `plt.plot(x, y)` call the same function; the only difference is whether you supply x-values or let pyplot number them from 0. ⟦C.f1 C.f2 C:tb4⟧
[UP NEXT] Up next: Bar Charts and Histograms: In the next tile you will use `plt.bar()` to compare average delivery times across Lagos, Abuja, and Kano — building directly on the Figure/Axes model you just learned.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Figure vs. Axes — Which Object Does What? — A quick contrast to clarify which object is the canvas and which one receives your data.
(definition) The Figure is the outer canvas — the whole window. The Axes is the inner plotting area where data is drawn. `fig, ax = plt.subplots()` creates both at once: `fig` is the canvas, `ax` is the plotting area. Plotting calls like `ax.plot(x, y)` go on `ax`, never on `fig`. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4⟧
### r02 · tight_layout() — What It Does and How to Call It — A clear contrast between calling tight_layout and not calling it.
(mechanism) `tight_layout()` automatically adjusts subplot parameters so the subplot(s) fit into the figure area; it checks the extents of tick labels, axis labels, and titles. Without it, labels can be clipped or overlap. Call it as `plt.tight_layout()` or `fig.tight_layout()` — both work. ⟦B.f2 B.f3 B:tb2⟧
### r03 · plt.plot() — One Argument vs. Two — The x-axis is the only thing that changes between the two forms.
(syntax) `plt.plot([18, 22, 26, 19, 30])` uses one argument: the list is treated as y-values and x-positions are filled in automatically starting at 0 (so 0, 1, 2, 3, 4). `plt.plot([1, 2, 3, 4, 5], [18, 22, 26, 19, 30])` uses two arguments: the first list sets the x-axis to 1–5, the second sets the y-axis. Both calls produce a line; only the x-axis differs. ⟦C.f1 C.f2 C:tb2 C:tb3⟧