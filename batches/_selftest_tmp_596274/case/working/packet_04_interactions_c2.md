# EVALUATOR PACKET — Multi-Panel Figures and Custom Styling (tile_viz_custom_multi_panel)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = viz.custom_styling_theming — Custom styling/theming (advanced/optional)
B = viz.multi_panel_figures — Multi-panel figures/subplots (advanced/optional)

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (viz.custom_styling_theming)   objective: Apply custom styling beyond seaborn's built-in themes, using a matplotlib style sheet or rcParams, and set a custom color palette with seaborn.
A.f1: plt.style.use('style-name') applies one of matplotlib's predefined style sheets (for example 'ggplot' or 'dark_background'); the available styles can be listed with plt.style.available.   [sources: matplotlib_official_docs#Customizing Matplotlib with style sheets and rcParams]
A.f2: A custom style file can set specific properties, such as 'axes.titlesize', 'lines.linewidth', or tick label sizes, and rcParams (for example mpl.rcParams['lines.linewidth'] = 2) can be set directly to change defaults globally.   [sources: matplotlib_official_docs#Customizing Matplotlib with style sheets and rcParams]
A.f3: seaborn.set_palette(palette, ...) sets the matplotlib color cycle from a seaborn palette, applying that color scheme to subsequent plots.   [sources: seaborn_official_docs#seaborn.set_palette]
PRACTICE ANCHOR (live_code): Apply a custom color palette via seaborn.set_palette and change a global rcParam (font size or line width) to a plot, going beyond seaborn's built-in themes.  SUCCESS: The plot reflects the specified custom palette on its elements and the rcParam change is visibly applied (e.g., larger title text or thicker lines), with no use of blocked syntax.
ASSESSMENT ANCHOR: apply_matplotlib_style_sheet facts=['f1']
ASSESSMENT ANCHOR: set_rcparams_globally facts=['f2']
ASSESSMENT ANCHOR: apply_seaborn_custom_palette facts=['f3']
ASSESSMENT ANCHOR: select_appropriate_styling_method_for_branding_requirement facts=['f1', 'f2', 'f3']

## SOURCE FACTS — B (viz.multi_panel_figures)   objective: Lay out multiple related plots in one figure using a grid of subplots.
B.f1: fig, axs = plt.subplots(nrows, ncols) creates a Figure containing a grid of Axes with the given number of rows and columns (for example plt.subplots(2, 2) creates a 2x2 grid).   [sources: matplotlib_quickstart_guide#Parts of a Figure]
B.f2: Each Axes in the returned grid is indexed separately (for example axs[0, 0]) and plotting/labeling calls made on one Axes only affect that panel.   [sources: matplotlib_quickstart_guide#Color mapped data]
PRACTICE ANCHOR (live_code): Create a 2×2 grid of subplots where each panel shows a histogram of a different numeric column from the orders DataFrame.  SUCCESS: Running the cell produces a single Figure containing four panels arranged in two rows and two columns, each displaying a histogram drawn from a distinct numeric column, with no panel affecting any other.
ASSESSMENT ANCHOR: create_subplot_grid_with_subplots facts=['f1']
ASSESSMENT ANCHOR: index_and_plot_on_individual_axes_independently facts=['f2']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Anticipating stakeholder questions and objections; Basic A/B test structure (control vs treatment group); Basic presentation structure (opening, body, call to action); Conceptual effect of sample size on confidence; Conceptual interpretation of statistical significance/confidence level; Converting a vague business question into a specific, measurable analytical question; Defining a capstone business question/problem statement; Drawing a business conclusion from an experiment-result summary; Framing an actionable recommendation that is distinct from the finding itself; Identifying stakeholder needs/requirements before analysis; Identifying the business decision a stakeholder needs the analysis to inform; Integrating SQL querying into an end-to-end project; Integrating spreadsheet analysis into an end-to-end project; Interpreting lift/percentage change between groups; Making a data-driven recommendation; Matching chart type to the specific point being made (trend vs. comparison vs. distribution vs. part-to-whole); Multi-panel figures/subplots (advanced/optional); Prioritizing findings by relevance to the stakeholder's specific decision, not by analytical interestingness; Selecting an

## LESSON, in learner order

### s01 · explainer · Style sheets, rcParams, and seaborn palettes  [reward 5]
Customizing plot appearance with rcParams and styles — matplotlib's default look is functional. Three tools let you change it.
(intro) plt.style.use('style-name') applies one of matplotlib's predefined style sheets—for example 'ggplot' or 'dark_background'. The available styles can be listed with plt.style.available. Calling it once changes the look of every plot drawn after that call. ⟦A.f1 A:tb1⟧
(mechanism) For finer control, rcParams can be set directly. After import matplotlib as mpl, mpl.rcParams['lines.linewidth'] = 2 sets the default line width for every plot drawn after that call. A custom style file can set properties such as 'axes.titlesize', 'lines.linewidth', or tick label sizes. ⟦A.f2 A:tb2⟧
(mechanism) sns.set_palette('pastel') sets the matplotlib color cycle from a seaborn palette, applying that color scheme to subsequent plots. This is separate from sns.set_theme() and affects only the color sequence. ⟦A.f3 A:tb3⟧
[BEFORE_AFTER] plt.style.use() and rcParams change the overall look; sns.set_palette() changes the color cycle.
  before:
[CODE python]
import matplotlib.pyplot as plt
# Default matplotlib style
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4, 5], [21, 23, 19, 25, 20])
ax.set_title('Delivery Times')
plt.show()
  annotations: ['Default: blue line, white background, no grid']
  after:
[CODE python]
import matplotlib as mpl
import matplotlib.pyplot as plt
plt.style.use('ggplot')
mpl.rcParams['lines.linewidth'] = 2
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4, 5], [21, 23, 19, 25, 20])
ax.set_title('Delivery Times')
plt.show()
  annotations: ['plt.style.use applies a predefined style sheet', 'rcParams sets a specific default globally']

### s02 · check · Check your understanding  [reward 5]
Customizing plot appearance with rcParams and styles — 
QUESTION [choice, intro, grading=client] Which call applies matplotlib's built-in `'ggplot'` style sheet to all subsequent plots?
  ✔ opt_correct: `plt.style.use('ggplot')`
      why: Correct. `plt.style.use('ggplot')` applies one of matplotlib's predefined style sheets; the available styles can be listed with `plt.style.available`.
  ✘ opt_sns: `sns.set_theme(style='ggplot')`
      why: `sns.set_theme()` applies seaborn's built-in themes, not matplotlib style sheets. To apply a matplotlib style sheet like `'ggplot'`, use `plt.style.use()`.
  ✘ opt_rcparams: `mpl.rcParams['style'] = 'ggplot'`
      why: `mpl.rcParams` sets individual style properties (like `'lines.linewidth'`), not a whole style sheet. To apply a named style sheet, use `plt.style.use('ggplot')`.
  ✘ opt_apply: `plt.style.apply('ggplot')`
      why: `plt.style.apply()` is not a valid function. The correct function is `plt.style.use('style-name')`.
  feedback✔: Right. `plt.style.use('style-name')` applies a predefined style sheet; you can see all available names with `plt.style.available`.  feedback✘: `plt.style.use('style-name')` is the function that applies a matplotlib style sheet. Pass the style name as a string, for example `plt.style.use('ggplot')`.  hints: ['The function lives in the `plt.style` namespace and is called `use`.', "Style names are strings — for example `'ggplot'` or `'dark_background'`."]  remediation→r01
  MEASURES: A:apply_matplotlib_style_sheet(f1)   anchors=['assessment:apply_matplotlib_style_sheet']
  taught-before-tested: A.f1←s01

### s03 · check · Check your understanding  [reward 5]
Customizing plot appearance with rcParams and styles — 
QUESTION [choice, core, grading=client] A team wants all their plots to use a specific brand color palette from seaborn. Which call sets **only** the matplotlib color cycle to that palette for all subsequent plots, without changing other style defaults?
  ✔ opt_set_palette: `sns.set_palette('pastel')`
      why: Correct. `sns.set_palette(palette, ...)` sets the matplotlib color cycle from a seaborn palette, applying that color scheme to subsequent plots.
  ✘ opt_style_use: `plt.style.use('pastel')`
      why: `plt.style.use()` applies a matplotlib style sheet by name. `'pastel'` is a seaborn palette name, not a matplotlib style sheet name — use `sns.set_palette('pastel')` instead.
  ✘ opt_rcparams: `mpl.rcParams['axes.prop_cycle'] = 'pastel'`
      why: While `mpl.rcParams` can set individual properties, assigning a palette name string directly to `'axes.prop_cycle'` is not the correct syntax. Use `sns.set_palette('pastel')` to set a seaborn palette.
  ✘ opt_set_theme: `sns.set_theme(palette='pastel')`
      why: `sns.set_theme(palette='pastel')` would also set the palette, but it also changes the background style. The question asks specifically about setting the color palette — `sns.set_palette()` is the dedicated function for that.
  feedback✔: Correct. `sns.set_palette()` is the dedicated function for setting the matplotlib color cycle from a seaborn palette.  feedback✘: `sns.set_palette('palette-name')` sets the matplotlib color cycle from a seaborn palette, applying that color scheme to all subsequent plots.  hints: ['The question asks about setting a color palette specifically — there is a dedicated seaborn function for this.', 'The function is `sns.set_palette()`, not `plt.style.use()` or `mpl.rcParams`.']
  MEASURES: A:select_appropriate_styling_method_for_branding_requirement(f1,f2,f3)   anchors=['assessment:select_appropriate_styling_method_for_branding_requirement']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s04 · hands_on · Practice  [reward 5]
Customizing plot appearance with rcParams and styles — Set rcParams globally and apply a seaborn palette.
QUESTION [code_exercise, core, grading=client] A DataFrame `df` with columns `city` and `delivery_time_minutes` is already loaded.

Apply custom styling and create a bar chart:
1. Set a custom seaborn palette using `sns.set_palette('pastel')`
2. Increase the title font size by setting `mpl.rcParams['axes.titlesize'] = 16`
3. Create a bar chart using `sns.barplot(data=df, x='city', y='delivery_time_minutes')`
4. Add a title `'Delivery Times by City'` using `plt.title()`

The styling changes will affect all subsequent plots.
  runtime={'kind': 'chart_renderer', 'version': '0.29.5', 'packages': ['matplotlib', 'pandas', 'seaborn']} constraints.allowed=['import matplotlib as mpl', 'import matplotlib.pyplot as plt', 'import seaborn as sns', 'sns.set_palette(palette_name)', "mpl.rcParams['axes.titlesize'] = value", "mpl.rcParams['lines.linewidth'] = value", "plt.style.use('style-name')", 'plt.style.available', 'sns.lineplot(data=df, x=col, y=col)', 'sns.barplot(data=df, x=col, y=col)', 'plt.title(str)', 'plt.xlabel(str)', 'plt.ylabel(str)', 'plt.show()'] blocked=5 items
  file solution.py [editable]:
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Data (these values will be changed by the grader to test your code)
lagos_time_1 = 18
df = pd.DataFrame({
    'city': ['Lagos', 'Lagos', 'Lagos', 'Lagos', 'Lagos', 'Lagos', 'Lagos', 'Lagos', 
             'Abuja', 'Abuja', 'Abuja', 'Abuja', 'Abuja', 'Abuja', 'Abuja', 'Abuja',
             'Kano', 'Kano', 'Kano', 'Kano', 'Kano', 'Kano', 'Kano', 'Kano'],
    'delivery_time_minutes': [lagos_time_1, 22, 19, 26, 30, 24, 28, 50,
                               25, 28, 23, 32, 35, 27, 31, 55,
                               27, 31, 26, 35, 38, 29, 34, 60]
})

# Styling values (these will be changed by the grader to test your code)
title_size = 16

# Apply custom styling and create a bar chart below

  SOLUTION solution.py:
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Data (already loaded)
lagos_time_1 = 18
df = pd.DataFrame({
    'city': ['Lagos', 'Lagos', 'Lagos', 'Lagos', 'Lagos', 'Lagos', 'Lagos', 'Lagos', 
             'Abuja', 'Abuja', 'Abuja', 'Abuja', 'Abuja', 'Abuja', 'Abuja', 'Abuja',
             'Kano', 'Kano', 'Kano', 'Kano', 'Kano', 'Kano', 'Kano', 'Kano'],
    'delivery_time_minutes': [lagos_time_1, 22, 19, 26, 30, 24, 28, 50,
                               25, 28, 23, 32, 35, 27, 31, 55,
                               27, 31, 26, 35, 38, 29, 34, 60]
})

# Styling values (these will be changed by the grader to test your code)
title_size = 16

# Apply custom styling and create a bar chart below
sns.set_palette('pastel')
mpl.rcParams['axes.titlesize'] = title_size
sns.barplot(data=df, x='city', y='delivery_time_minutes')
plt.title('Delivery Times by City')

  test ix.tile_viz_custom_multi_panel.s04.t01 (figure_equals, visible=True): {"expected":{"n_axes":1,"chart_types":[["bar","line"]]}} | on-fail: Your figure should contain one Axes with a bar chart. Call `sns.barplot(data=df, x='category', y='value')`.
  test ix.tile_viz_custom_multi_panel.s04.t04 (value_equals, visible=None): {"expr":"mpl.rcParams['axes.titlesize']","expected":16} | on-fail: Set `mpl.rcParams['axes.titlesize'] = title_size` before the plot call.
  test ix.tile_viz_custom_multi_panel.s04.t02 (axes_property, visible=True): {"property":"title","expected":"Delivery Times by City"} | on-fail: Add `plt.title('Delivery Times by City')` to set the chart title.
  test ix.tile_viz_custom_multi_panel.s04.t03 (plotted_data_equals, visible=True): {"chart":"bar","field":"heights","expected":[27.125,32.0,35.0],"series":0,"axes":0} | on-fail: The bar chart should show the mean delivery time for each city. Call `sns.barplot(data=df, x='city', y='delivery_time_minutes')`.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"f53426cc3ab9e8a1304dde491b3dd7ccb3635e17f4c76fcb1072cce715d49ecf","tests_passed":4}
  feedback✔: Well done! You set a custom seaborn palette with `sns.set_palette()` and changed a global rcParam with `mpl.rcParams['axes.titlesize']` — both affect all subsequent plots.  feedback✘: Make sure you called `sns.set_palette('pastel')`, set `mpl.rcParams['axes.titlesize'] = 16`, drew the bar chart with `sns.barplot(data=df, x='category', y='value')`, and added `plt.title('Delivery Times by City')`.  hints: ["Call `sns.set_palette('pastel')` and `mpl.rcParams['axes.titlesize'] = 16` before the plot call so they take effect.", "`mpl.rcParams` is a dictionary — set a key like `mpl.rcParams['axes.titlesize'] = 16`."]
  MEASURES: A:set_rcparams_globally(f2); A:apply_seaborn_custom_palette(f3)   anchors=['practice', 'assessment:set_rcparams_globally', 'assessment:apply_seaborn_custom_palette']
  taught-before-tested: A.f2←s01; A.f3←s01

### s05 · explainer · A grid of Axes in one Figure  [reward 5]
Creating multi-panel figures with subplots — plt.subplots(nrows, ncols) creates a Figure containing a grid of Axes.
(intro) Suppose you want to show the delivery-time histogram and the distance/delivery-time scatter plot together, side by side, instead of as two separate figures. fig, axs = plt.subplots(nrows, ncols) creates a Figure containing a grid of Axes with the given number of rows and columns. plt.subplots(2, 2) creates a 2×2 grid of four Axes inside one Figure. ⟦B.f1 B:tb1 B:tb2⟧
(mechanism) Each Axes in the returned grid is indexed separately—for example axs[0, 0] for the top-left panel. Plotting and labeling calls made on one Axes only affect that panel. axs[0, 0].hist(data) draws a histogram into the top-left panel; axs[0, 1].scatter(x_values, y_values) draws a scatter into the top-right panel without disturbing the first. ⟦B.f2 B:tb3⟧
[DIAGRAM] nodes=['Figure', 'axs[0,0]\nTop-left', 'axs[0,1]\nTop-right', 'axs[1,0]\nBottom-left', 'axs[1,1]\nBottom-right'] edges=[] alt: A 2×2 grid of empty Axes boxes inside a single Figure boundary. Each box is labelled with its index: axs[0,0] top-left, axs[0,1] top-right, axs[1,0] bottom-left, axs[1,1] bottom-right.

### s06 · video · Video walkthrough  [reward 5]
Creating multi-panel figures with subplots — 
[VIDEO Building a multi-panel figure: grid layout and independent axes] bridge-before: Watch how the nrows/ncols arguments change the shape of the returned collection, and how each panel receives its own plot call without affecting the other. Note: the clip unpacks axes into named variables (ax1, ax2) rather than using index notation like axs[0, 0]; both approaches are equivalent. | bridge-after: The key takeaway is that each Axes is independent — calls on one panel never touch another. The teaching text also covers 2×2 indexing (axs[0, 0]) which the clip omits.
  - XFZRVnP-MTU 503-804s facts=['f1', 'f2'] label: Creating a subplot grid and plotting independently on each Axes | summary: The instructor motivates splitting data across multiple panels rather than crowding one figure, then shows how the nrows and ncols arguments to plt.subplots control the shape of the returned Axes collection. Printing the result for a 1×1, 2×1, and 2×2 call reveals how the return value changes from a single Axes to a flat list to a nested list of lists. The instructor then simplifies to a 2×1 grid, unpacks the two Axes into separate variables, and assigns distinct plot calls, legends, titles, and axis labels to each — producing one figure with two fully independent panels.

### s07 · check · Check your understanding  [reward 5]
Creating multi-panel figures with subplots — 
QUESTION [choice, core, grading=client] After `fig, axs = plt.subplots(2, 2)`, you want to draw a histogram in the top-right panel only. Which call is correct?
  ✔ opt_correct: `axs[0, 1].hist(data)`
      why: Correct. `axs[0, 1]` selects row 0 (top), column 1 (right). Calling `.hist()` on that Axes draws only into that panel.
  ✘ opt_wrong_index: `axs[1, 0].hist(data)`
      why: `axs[1, 0]` selects row 1 (bottom), column 0 (left) — that is the bottom-left panel, not the top-right. The top-right is `axs[0, 1]`.
  ✘ opt_fig: `fig.hist(data, position=(0, 1))`
      why: The Figure object does not have a `hist()` method. Plotting calls go on individual Axes objects, indexed as `axs[row, col]`.
  ✘ opt_plt: `plt.hist(data)` — it automatically goes to the top-right panel
      why: `plt.hist()` draws on the current active Axes, not necessarily the top-right panel. To target a specific panel, use `axs[0, 1].hist(data)`.
  feedback✔: Right. In a 2×2 grid, `axs[0, 1]` is row 0 (top), column 1 (right). Calls on that Axes only affect that panel.  feedback✘: In a 2×2 grid, rows and columns are 0-indexed: `axs[0, 0]` is top-left, `axs[0, 1]` is top-right, `axs[1, 0]` is bottom-left, `axs[1, 1]` is bottom-right.  hints: ['The first index is the row (0 = top, 1 = bottom); the second is the column (0 = left, 1 = right).', 'Top-right means row 0, column 1 — so `axs[0, 1]`.']  remediation→r02
  MEASURES: B:index_and_plot_on_individual_axes_independently(f2)   anchors=['assessment:index_and_plot_on_individual_axes_independently']
  taught-before-tested: B.f2←s05

### s08 · hands_on · Practice  [reward 5]
Creating multi-panel figures with subplots — Create a subplot grid and plot on each Axes independently.
QUESTION [code_exercise, core, grading=client] A 2×2 subplot grid has already been created for you with `fig, axs = plt.subplots(2, 2)`. Four lists of data are also provided: `col_a`, `col_b`, `col_c`, and `col_d`.

Draw a histogram in each panel:
1. Top-left panel: `axs[0][0].hist(col_a)`
2. Top-right panel: `axs[0][1].hist(col_b)`
3. Bottom-left panel: `axs[1][0].hist(col_c)`
4. Bottom-right panel: `axs[1][1].hist(col_d)`

Each panel will show the distribution of one column.
  runtime={'kind': 'chart_renderer', 'version': '0.29.5', 'packages': ['matplotlib', 'pandas']} constraints.allowed=['plt.subplots(2, 2)', 'axs[0, 0].hist(...)', 'axs[0, 1].hist(...)', 'axs[1, 0].hist(...)', 'axs[1, 1].hist(...)', 'axs[row, col].set_title(...)', 'axs[row, col].set_xlabel(...)', 'axs[row, col].set_ylabel(...)', 'plt.tight_layout()', 'plt.show()'] blocked=0 items
  file solution.py [editable]:
import matplotlib.pyplot as plt

# Data (these values will be changed by the grader to test your code)
col_a_1 = 23
col_a = [col_a_1, 25, 22, 24, 26, 23, 25, 24]
col_b = [45, 47, 44, 46, 48, 45, 47, 46]
col_c = [56, 58, 55, 57, 59, 56, 58, 57]
col_d = [78, 80, 77, 79, 81, 78, 80, 79]

fig, axs = plt.subplots(2, 2)
# Draw a histogram in each panel below

  SOLUTION solution.py:
import matplotlib.pyplot as plt

# Data (these values will be changed by the grader to test your code)
col_a_1 = 23
col_a = [col_a_1, 25, 22, 24, 26, 23, 25, 24]
col_b = [45, 47, 44, 46, 48, 45, 47, 46]
col_c = [56, 58, 55, 57, 59, 56, 58, 57]
col_d = [78, 80, 77, 79, 81, 78, 80, 79]

fig, axs = plt.subplots(2, 2)
# Draw a histogram in each panel below
axs[0][0].hist(col_a)
axs[0][1].hist(col_b)
axs[1][0].hist(col_c)
axs[1][1].hist(col_d)

  test ix.tile_viz_custom_multi_panel.s08.t01 (figure_equals, visible=True): {"expected":{"n_axes":4,"chart_types":[["hist"],["hist"],["hist"],["hist"]]}} | on-fail: Your figure should contain 4 axes (2×2 grid), each with a histogram. Use `fig, axs = plt.subplots(2, 2)` and call `.hist()` on each `axs[row][col]`.
  test ix.tile_viz_custom_multi_panel.s08.t02 (value_equals, visible=True): {"expr":"col_a[0]","expected":23} | on-fail: The first element of col_a should be col_a_1.
  test ix.tile_viz_custom_multi_panel.s08.t03 (plotted_data_equals, visible=True): {"chart":"hist","field":"heights","axes":0,"expected":[1.0,0.0,2.0,0.0,0.0,2.0,0.0,2.0,0.0,1.0]} | on-fail: The histogram should be based on the data in col_a.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"f8c5791b2d61335e18f51fe371ede8b646478bdc0c2dc12721d23f5992bef891","tests_passed":3}
  feedback✔: Excellent! You created a 2×2 subplot grid and drew a distinct histogram in each panel — each Axes is independent.  feedback✘: Make sure you called `.hist()` on each of the four `axs[row][col]` objects with a different list: `axs[0][0].hist(col_a)`, `axs[0][1].hist(col_b)`, `axs[1][0].hist(col_c)`, `axs[1][1].hist(col_d)`.  hints: ['The grid is already created: `fig, axs = plt.subplots(2, 2)`. Add four `.hist()` calls, one per panel.', 'Each panel is addressed by `axs[row][col]` — for example `axs[0][0]` is top-left and `axs[1][1]` is bottom-right.']
  MEASURES: B:create_subplot_grid_with_subplots(f1)   anchors=['practice', 'assessment:create_subplot_grid_with_subplots']
  taught-before-tested: B.f1←s05

### s09 · recap · What you learned  [reward 5]
Recap — 
(takeaway) plt.style.use('style-name') applies a predefined style sheet. mpl.rcParams['lines.linewidth'] = 2 sets a specific default globally. sns.set_palette('pastel') sets the color cycle from a seaborn palette. ⟦A.f1 A.f2 A.f3⟧
(takeaway) fig, axs = plt.subplots(nrows, ncols) creates a Figure with a grid of Axes. Each Axes is indexed separately (axs[0, 0]) and plotting calls on one panel don't affect the others. ⟦B.f1 B.f2⟧
[UP NEXT] Up next: Viz Seaborn Stats Themes: Next: seaborn's DataFrame interface and statistical plotting functions

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Let's review — Here's another way to think about style sheets.
(practical_context) plt.style.use('ggplot') changes the look of all plots drawn after that call—background color, grid lines, font sizes, and more. You can see all available style names by printing plt.style.available. Call it once at the top of your notebook to set a consistent look. ⟦A.f1⟧
### r02 · Let's review — Here's another way to think about subplot indexing.
(practical_context) When plt.subplots(2, 2) returns axs, think of it as a 2D grid. axs[0, 0] is the top-left panel, axs[0, 1] is top-right, axs[1, 0] is bottom-left, axs[1, 1] is bottom-right. Plotting on axs[0, 0] only affects that one panel—the others stay empty until you plot on them. ⟦B.f2⟧

## OTHER CONTENT (fields without a dedicated renderer)
· nodes.label: axs[1,0]
Bottom-left
· nodes.label: axs[1,1]
Bottom-right

=========

# EVALUATOR PACKET — Labeling and Chart Selection (tile_viz_labeling_chart_selection)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = viz.labeling_annotation — Labeling axes, titles, and legends
B = viz.chart_type_selection — Matching chart type to the analytical question

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (viz.labeling_annotation)   objective: Add a title, axis labels, and a legend to a matplotlib plot so it is understandable on its own.
A.f1: ax.set_xlabel('...') and ax.set_ylabel('...') set the x-axis and y-axis labels, and ax.set_title('...') sets the Axes title.   [sources: matplotlib_quickstart_guide#Labelling plots]
A.f2: Passing label='...' to a plotting call (e.g. ax.plot(data, label='data1')) and then calling ax.legend() displays a legend identifying each labeled series.   [sources: matplotlib_quickstart_guide#Labelling plots]
A.f3: In the pyplot interface, plt.xlabel(), plt.ylabel(), and plt.title() set the same label/title elements on the current Axes.   [sources: matplotlib_pyplot_tutorial#Working with text]
PRACTICE ANCHOR (live_code): Starting from two pre-plotted series on a single Axes, add a title, both axis labels, and a legend that distinguishes the two series.  SUCCESS: The rendered figure shows a non-empty title, non-empty x-axis and y-axis labels, and a legend with two distinct entries, one per series.
ASSESSMENT ANCHOR: add_title_axis_labels_and_legend_to_unlabeled_plot facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: apply_axes_object_labeling_methods facts=['f1']
ASSESSMENT ANCHOR: attach_legend_via_label_kwarg_and_legend_call facts=['f2']
ASSESSMENT ANCHOR: apply_pyplot_interface_labeling_functions facts=['f3']

## SOURCE FACTS — B (viz.chart_type_selection)   objective: Match a chart type (bar, histogram, line, scatter, or box) to the analytical question being explored during one's own analysis.
B.f1: A bar chart is used for graphing categorical data and comparing values across categories.   [sources: swd_what_is_a_bar_chart]
B.f2: plt.hist() bins a numeric variable, counts values per bin, and draws the distribution as bars.   [sources: matplotlib_official_docs#matplotlib.pyplot.hist]
B.f3: Line graphs are best when you want to show how a value changes over time, or compare how several things change over time relative to each other.   [sources: swd_what_is_a_line_graph]
B.f4: A scatterplot shows the relationship between two numerical variables plotted along the horizontal and vertical axis.   [sources: swd_what_is_a_scatterplot]
B.f5: Boxplots offer a condensed display for comparing the distributions of multiple datasets side by side.   [sources: swd_what_is_a_boxplot]
note: This is a synthesis concept recapping facts already taught by the five chart-type concepts -- no new matplotlib syntax here.
PRACTICE ANCHOR (live_code): Given a small delivery dataset with columns 'distance_km' and 'delivery_minutes', produce a scatterplot of the two variables and write a one-line comment explaining why a scatterplot answers the question 'Do longer distances lead to longer delivery times?' better than a bar chart would.  SUCCESS: The code runs without error, displays a scatterplot with 'distance_km' on one axis and 'delivery_minutes' on the other, and the comment correctly names the relationship-between-two-numerical-variables purpose of a scatterplot versus the category-comparison purpose of a bar chart.
ASSESSMENT ANCHOR: select_chart_type_for_analytical_question facts=['f1', 'f2', 'f3', 'f4', 'f5']
ASSESSMENT ANCHOR: identify_bar_chart_use_case facts=['f1']
ASSESSMENT ANCHOR: identify_histogram_use_case facts=['f2']
ASSESSMENT ANCHOR: identify_line_graph_use_case facts=['f3']
ASSESSMENT ANCHOR: identify_scatter_plot_use_case facts=['f4']
ASSESSMENT ANCHOR: identify_boxplot_use_case facts=['f5']

## DATA ASSETS USED
ds.daily_averages: QuickDeliver daily average delivery times — columns: day(identifier,digits-as-label), lagos_avg(numerical), abuja_avg(numerical)
   [1,21.0,24.0]
   [2,23.0,26.0]
   [3,19.0,22.0]
   [4,25.0,28.0]
   [5,20.0,25.0]
ds.orders: QuickDeliver orders — clean — columns: order_id(identifier,digits-as-label), city(categorical), delivery_time_minutes(numerical), distance_km(numerical), order_value(numerical), num_items(numerical)
   [1001,"Lagos",18,2.1,1850.0,2]
   [1002,"Lagos",22,3.4,2200.0,3]
   [1003,"Lagos",19,2.8,1600.0,1]
   [1004,"Lagos",26,4.5,3100.0,4]
   [1005,"Lagos",30,5.2,2750.0,3]
   [1006,"Lagos",24,3.9,2400.0,2]
   [1007,"Lagos",28,4.8,3300.0,5]
   [1008,"Lagos",50,9.1,4800.0,6]
   variant ds.orders.messy: 5 ops; planted: iss.missing_delivery_time(missing_value); iss.negative_delivery_time(impossible_value); iss.city_casing(inconsistent_category); iss.duplicate_order_1007(duplicate_row); iss.implausible_distance(outlier_suspicious)

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Anticipating stakeholder questions and objections; Basic A/B test structure (control vs treatment group); Basic presentation structure (opening, body, call to action); Conceptual effect of sample size on confidence; Conceptual interpretation of statistical significance/confidence level; Converting a vague business question into a specific, measurable analytical question; Custom styling/theming (advanced/optional); Drawing a business conclusion from an experiment-result summary; Framing an actionable recommendation that is distinct from the finding itself; Identifying stakeholder needs/requirements before analysis; Identifying the business decision a stakeholder needs the analysis to inform; Interpreting lift/percentage change between groups; Making a data-driven recommendation; Matching chart type to the analytical question; Matching chart type to the specific point being made (trend vs. comparison vs. distribution vs. part-to-whole); Multi-panel figures/subplots (advanced/optional); Plotting directly from pandas DataFrames with seaborn; Prioritizing findings by relevance to the stakeholder's specific decision, not by analytical interestingness; Simplifying a technical chart for a 

## LESSON, in learner order

### s01 · explainer · Making charts readable with labels  [reward 5]
Labeling axes, titles, and legends — A chart without labels is just shapes. Three Axes methods and one legend call fix that.
(intro) Titles, axis labels, and legends are the text that tells a reader what a plot shows. Matplotlib gives two parallel ways to add them: the Axes object interface and the pyplot interface. On an Axes object, ax.set_xlabel('Day'), ax.set_ylabel('Average delivery time (minutes)'), and ax.set_title('Average delivery time by day') label the Lagos trend line. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) When you plot multiple series on the same Axes, a legend shows which line is which. Pass label='Lagos' to ax.plot(), then call ax.legend(). Once a second city's line is added to the same Axes, the legend identifies each series by its label. ⟦A.f2 A:tb3⟧
[BEFORE_AFTER] Adding set_xlabel, set_ylabel, set_title, and legend turns an unlabeled plot into a self-explanatory chart.
  before:
[CODE python]
fig, ax = plt.subplots()
days = [1, 2, 3, 4, 5]
lagos_avg = [21, 23, 19, 25, 20]
ax.plot(days, lagos_avg)
plt.show()
# No title, no axis labels, no legend
  annotations: ['Plot draws, but the reader has no context']
  after:
[CODE python]
fig, ax = plt.subplots()
days = [1, 2, 3, 4, 5]
lagos_avg = [21, 23, 19, 25, 20]
ax.plot(days, lagos_avg, label='Lagos')
ax.set_xlabel('Day')
ax.set_ylabel('Average delivery time (minutes)')
ax.set_title('Average delivery time by day')
ax.legend()
plt.show()
  annotations: ['label= kwarg names this series for the legend', 'set_xlabel, set_ylabel, set_title add axis labels and title', 'legend() renders the legend box']

### s02 · explainer · pyplot shortcut functions  [reward 5]
Labeling axes, titles, and legends — 
(mechanism) In the pyplot interface, plt.xlabel(), plt.ylabel(), and plt.title() set the same label and title elements on the current Axes—the pyplot equivalents of ax.set_xlabel(), ax.set_ylabel(), and ax.set_title(). ⟦A.f3 A:tb4⟧

### s03 · check · Check your understanding  [reward 5]
Labeling axes, titles, and legends — 
QUESTION [choice, intro, grading=client] You have an Axes object called `ax`. Which three method calls correctly add a title, an x-axis label, and a y-axis label to that Axes?
  ✔ opt_correct: `ax.set_title('...')`, `ax.set_xlabel('...')`, `ax.set_ylabel('...')`
      why: Correct. `ax.set_xlabel()`, `ax.set_ylabel()`, and `ax.set_title()` are the three Axes object methods for labeling.
  ✘ opt_plt: `plt.title('...')`, `plt.xlabel('...')`, `plt.ylabel('...')`
      why: Those are the pyplot interface functions (`plt.xlabel()`, etc.), not the Axes object methods. The Axes object uses `ax.set_xlabel()`, `ax.set_ylabel()`, and `ax.set_title()`.
  ✘ opt_fig: `fig.set_title('...')`, `fig.set_xlabel('...')`, `fig.set_ylabel('...')`
      why: The Figure object (`fig`) does not have `set_xlabel()`, `set_ylabel()`, or `set_title()` methods. Labeling calls go on the Axes object (`ax`), not the Figure.
  ✘ opt_mixed: `ax.title('...')`, `ax.xlabel('...')`, `ax.ylabel('...')`
      why: The Axes methods are `ax.set_xlabel()`, `ax.set_ylabel()`, and `ax.set_title()` — note the `set_` prefix. `ax.xlabel()` and `ax.ylabel()` are not valid method names.
  feedback✔: Right. The Axes object's labeling methods all start with `set_`: `ax.set_xlabel()`, `ax.set_ylabel()`, and `ax.set_title()`.  feedback✘: The Axes object uses `ax.set_xlabel('...')`, `ax.set_ylabel('...')`, and `ax.set_title('...')` — each takes a string argument.  hints: ['All three Axes labeling methods start with `set_`.', 'The methods belong to the `ax` object, not to `fig` or `plt`.']  remediation→r01
  MEASURES: A:apply_axes_object_labeling_methods(f1)   anchors=['assessment:apply_axes_object_labeling_methods']
  taught-before-tested: A.f1←s01

### s04 · check · Check your understanding  [reward 5]
Labeling axes, titles, and legends — 
QUESTION [choice, intro, grading=client] You are using the pyplot interface (no explicit `ax` variable). Which call sets the title of the current Axes?
  ✔ opt_plt_title: `plt.title('Delivery times by day')`
      why: Correct. In the pyplot interface, `plt.title()` sets the title of the current Axes — the pyplot equivalent of `ax.set_title()`.
  ✘ opt_ax_title: `ax.set_title('Delivery times by day')`
      why: `ax.set_title()` is the Axes object method, not the pyplot interface function. When using the pyplot interface without an explicit `ax`, use `plt.title()`.
  ✘ opt_fig_title: `fig.set_title('Delivery times by day')`
      why: The Figure object does not have a `set_title()` method for the Axes title. In the pyplot interface, use `plt.title()` to set the current Axes title.
  ✘ opt_plt_set: `plt.set_title('Delivery times by day')`
      why: `plt.set_title()` is not a valid pyplot function. The correct pyplot function is `plt.title()` (no `set_` prefix).
  feedback✔: Correct. `plt.title()`, `plt.xlabel()`, and `plt.ylabel()` are the pyplot interface equivalents of the Axes `set_` methods.  feedback✘: In the pyplot interface, the labeling functions are `plt.title()`, `plt.xlabel()`, and `plt.ylabel()` — they operate on the current Axes without needing an explicit `ax` variable.  hints: ['The pyplot interface functions mirror the Axes methods but are called on `plt` directly.', "Unlike the Axes methods, the pyplot functions do not have a `set_` prefix — it's `plt.title()`, not `plt.set_title()`."]
  MEASURES: A:apply_pyplot_interface_labeling_functions(f3)   anchors=['assessment:apply_pyplot_interface_labeling_functions']
  taught-before-tested: A.f3←s02

### s05 · hands_on · Practice  [reward 5]
Labeling axes, titles, and legends — Add a title, axis labels, and a legend to an unlabeled plot.
QUESTION [code_exercise, core, grading=client] Two series are already plotted on `ax`: Lagos daily averages and Abuja daily averages for days 1–5.

Complete the code to:
1. Set the Axes title to `'Average Delivery Time by Day'`
2. Set the x-axis label to `'Day'`
3. Set the y-axis label to `'Average delivery time (minutes)'`
4. Add a legend that shows two entries — one labelled `'Lagos'` and one labelled `'Abuja'`

Use `ax.set_title()`, `ax.set_xlabel()`, `ax.set_ylabel()`, and `ax.legend()`. Pass `label='Lagos'` and `label='Abuja'` to the two `ax.plot()` calls already in the starter.
  runtime={'kind': 'chart_renderer', 'version': '0.29.5', 'packages': ['matplotlib', 'pandas']} constraints.allowed=["ax.set_xlabel('...')", "ax.set_ylabel('...')", "ax.set_title('...')", "ax.plot(x, y, label='...')", 'ax.legend()', "plt.xlabel('...')", "plt.ylabel('...')", "plt.title('...')", 'import matplotlib.pyplot as plt', 'fig, ax = plt.subplots()', 'plt.show()'] blocked=8 items
  file solution.py [editable]:
import matplotlib.pyplot as plt
import pandas as pd

# Data (these values will be changed by the grader to test your code)
day_1 = 1
days = [day_1, 2, 3, 4, 5]
lagos_1 = 21
lagos_avg = [lagos_1, 23, 19, 25, 20]
abuja_1 = 24
abuja_avg = [abuja_1, 26, 22, 28, 25]

fig, ax = plt.subplots()
ax.plot(days, lagos_avg)  # add label='Lagos' here
ax.plot(days, abuja_avg)  # add label='Abuja' here

# Add title, axis labels, and legend below

  SOLUTION solution.py:
import matplotlib.pyplot as plt
import pandas as pd

# Data (these values will be changed by the grader to test your code)
day_1 = 1
days = [day_1, 2, 3, 4, 5]
lagos_1 = 21
lagos_avg = [lagos_1, 23, 19, 25, 20]
abuja_1 = 24
abuja_avg = [abuja_1, 26, 22, 28, 25]

fig, ax = plt.subplots()
ax.plot(days, lagos_avg, label='Lagos')
ax.plot(days, abuja_avg, label='Abuja')

ax.set_title('Average Delivery Time by Day')
ax.set_xlabel('Day')
ax.set_ylabel('Average delivery time (minutes)')
ax.legend()

  test ix.tile_viz_labeling_chart_selection.s05.t01 (axes_property, visible=True): {"property":"title","expected":"Average Delivery Time by Day"} | on-fail: Set the Axes title to 'Average Delivery Time by Day' using `ax.set_title('Average Delivery Time by Day')`.
  test ix.tile_viz_labeling_chart_selection.s05.t02 (axes_property, visible=True): {"property":"xlabel","expected":"Day"} | on-fail: Set the x-axis label to 'Day' using `ax.set_xlabel('Day')`.
  test ix.tile_viz_labeling_chart_selection.s05.t03 (axes_property, visible=True): {"property":"ylabel","expected":"Average delivery time (minutes)"} | on-fail: Set the y-axis label to 'Average delivery time (minutes)' using `ax.set_ylabel('Average delivery time (minutes)')`.
  test ix.tile_viz_labeling_chart_selection.s05.t04 (axes_property, visible=True): {"property":"legend","expected":["Lagos","Abuja"]} | on-fail: Add `label='Lagos'` and `label='Abuja'` to the two `ax.plot()` calls, then call `ax.legend()` to display the legend.
  test ix.tile_viz_labeling_chart_selection.s05.t05 (plotted_data_equals, visible=True): {"chart":"line","field":"y","expected":[21,23,19,25,20],"series":0,"axes":0} | on-fail: The first line should plot `lagos_avg` values [21, 23, 19, 25, 20]. Do not change the `ax.plot()` calls — only add the `label=` argument.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"dfae084a6c8553fbd8503258a3d607415ec8dadfb4a162615911f5b678126730","tests_passed":5}
  feedback✔: Well done! Your plot now has a title, axis labels, and a two-entry legend — everything a reader needs to understand the chart without extra context.  feedback✘: Check that you called `ax.set_title()`, `ax.set_xlabel()`, `ax.set_ylabel()`, and `ax.legend()`, and that you added `label='Lagos'` and `label='Abuja'` to the two `ax.plot()` calls.  hints: ["Add `label='Lagos'` inside the first `ax.plot()` call and `label='Abuja'` inside the second, then call `ax.legend()` at the end.", "The three labeling methods are `ax.set_title('...')`, `ax.set_xlabel('...')`, and `ax.set_ylabel('...')` — each takes a string."]
  MEASURES: A:add_title_axis_labels_and_legend_to_unlabeled_plot(f1,f2,f3); A:attach_legend_via_label_kwarg_and_legend_call(f2)   anchors=['practice', 'assessment:add_title_axis_labels_and_legend_to_unlabeled_plot', 'assessment:attach_legend_via_label_kwarg_and_legend_call']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s02; A.f2←s01

### s06 · explainer · Choosing the right chart for your question  [reward 5]
Matching chart type to the analytical question — Five chart types, five different questions. The chart you pick changes what the reader sees.
(intro) With five chart types available, the question during exploration is which one actually answers the question you're asking of the data. Picking a chart type comes down to naming what you're asking: a category comparison, a single variable's spread, a trend over time, a relationship between two variables, or a spread comparison across several groups. ⟦B.f1 B:tb1 B:tb3⟧
(mechanism) A bar chart compares values across categories—average delivery time per city. plt.hist() bins a numeric variable and draws its distribution—how delivery times are spread out. Line graphs show how a value changes over time—average delivery time across days of the week. A scatterplot shows the relationship between two numeric variables—whether distance and delivery time move together. Boxplots compare the distributions of multiple datasets side by side—the full spread of delivery times across several cities at once. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2⟧
[SIDE_BY_SIDE] The same delivery data can be visualized multiple ways. Pick the chart type that answers your specific question. left_label: Bar chart — Which city is slowest? | right_label: Line chart — How does time change by day?
  left:
[CHART bar: Average Delivery Time by City] data=ds.orders x=city y=delivery_time_minutes color=None annotations=[] alt: Bar chart of average delivery time per city (Lagos, Abuja, Kano). Each bar represents one city's mean delivery time in minutes.
  right:
[CHART line: Lagos Delivery Time — Days 1–5] data=ds.daily_averages x=day y=lagos_avg color=None annotations=[] alt: Line chart of Lagos average delivery times across 5 days: 21, 23, 19, 25, 20 minutes. The connected line shows day-to-day variation.

### s07 · video · Video walkthrough  [reward 5]
Matching chart type to the analytical question — 
[VIDEO Choosing between chart types: boxplot fitness check and histogram construction] bridge-before: The first clip shows a boxplot ruled out because of sparse data per group; watch for what makes a distribution display fail. The second clip demonstrates plt.hist() live — note the bins argument and how the output is read. | bridge-after: The clips cover f5 (boxplot fitness) and f2 (plt.hist()). Facts f1, f3, and f4 — bar charts, line graphs, and scatterplots — are not shown; the teaching text covers all five chart types and their decision rules.
  - Z77c53eYtHc 149-201s facts=['f5'] label: When a boxplot's distribution purpose doesn't fit the data at hand | summary: The presenter sketches a boxplot as a candidate for a dataset where most groups have only one observation per day. Because a boxplot needs enough values per group to form a box, the sketch collapses to single points for nearly every day — making the chart unreadable. The presenter also notes that boxplots carry a steeper learning curve for unfamiliar audiences, though domain experts such as researchers may handle them fine. The conclusion is that sketching the option was worthwhile precisely to rule it out.
  - ZyTO4SwhSeE 503-649s facts=['f2'] label: Building a histogram with plt.hist() to reveal an age-group distribution | summary: Starting from a list of ages, the presenter defines a set of numeric bins (0, 10, 20, … 130) and calls plt.hist() with the data list, the bins argument, histtype='bar', and rwidth=0.8. Running the code produces a bar-per-bin chart; the presenter reads the result aloud — the largest group falls between 40 and 50, no one appears in the 10–20 range — showing how the histogram surfaces the shape of the distribution rather than individual counts per label.

### s08 · check · Check your understanding  [reward 5]
Matching chart type to the analytical question — 
QUESTION [choice, core, grading=client] A QuickDeliver analyst wants to answer: 'What is the shape of the distribution of delivery times — are most deliveries fast, or is the spread wide?' Which chart type is best?
  ✔ opt_hist: Histogram
      why: Correct. `plt.hist()` bins a numeric variable, counts values per bin, and draws the distribution as bars — exactly what you need to see the shape of delivery times.
  ✘ opt_bar: Bar chart
      why: A bar chart compares a numeric value across discrete categories (e.g., average delivery time per city). It does not show the distribution shape of a single numeric variable.
  ✘ opt_line: Line graph
      why: A line graph shows how a value changes over time. It does not reveal the distribution shape of a numeric variable like delivery times.
  ✘ opt_scatter: Scatter plot
      why: A scatter plot shows the relationship between two numeric variables. To see the distribution of a single variable, use a histogram.
  feedback✔: Right. A histogram bins the data and shows how many values fall in each range — perfect for seeing the distribution shape.  feedback✘: To see how a numeric variable is distributed (its shape, spread, and concentration), use a histogram (`plt.hist()`). Each bar represents a count of values in a bin.  hints: ["The question asks about the 'shape of the distribution' of a single numeric variable.", 'Think about which chart type bins a numeric variable and counts values per bin.']  remediation→r02
  MEASURES: B:select_chart_type_for_analytical_question(f1,f2,f3,f4,f5); B:identify_histogram_use_case(f2)   anchors=['assessment:select_chart_type_for_analytical_question', 'assessment:identify_histogram_use_case']
  taught-before-tested: B.f1←s06; B.f2←s06; B.f3←s06; B.f4←s06; B.f5←s06; B.f2←s06

### s09 · check · Check your understanding  [reward 5]
Matching chart type to the analytical question — 
QUESTION [choice, core, grading=client] An analyst wants to compare the full spread of delivery times (median, quartiles, and outliers) across Lagos, Abuja, and Kano side by side. Which chart type is best?
  ✔ opt_box: Box plot
      why: Correct. Box plots offer a condensed display for comparing the distributions of multiple datasets side by side — showing median, quartiles, and outliers per group.
  ✘ opt_line: Line graph
      why: A line graph shows how a value changes over time. It does not show the spread (quartiles, outliers) of a distribution across groups.
  ✘ opt_hist: Histogram
      why: A histogram shows the distribution of a single numeric variable. To compare distributions across multiple groups side by side, a box plot is more compact and direct.
  ✘ opt_bar: Bar chart
      why: A bar chart compares a single aggregate value (like the mean) per category. It does not show the full spread — quartiles, median, and outliers — that a box plot provides.
  feedback✔: Exactly. A box plot condenses each group's distribution into a single visual — median, IQR, whiskers, and outliers — making side-by-side comparison easy.  feedback✘: When you need to compare the full spread (median, quartiles, outliers) across multiple groups, a box plot is the right choice. It shows all of that in a compact form per group.  hints: ["The question asks for 'full spread' across multiple groups — which chart type shows quartiles and outliers per group?", 'A line graph tracks change over time; a box plot compares distributions across groups.']
  MEASURES: B:identify_line_graph_use_case(f3); B:identify_boxplot_use_case(f5)   anchors=['assessment:identify_line_graph_use_case', 'assessment:identify_boxplot_use_case']
  taught-before-tested: B.f3←s06; B.f5←s06

### s10 · hands_on · Practice  [reward 5]
Matching chart type to the analytical question — Choose the right chart type for each analytical question.
QUESTION [code_exercise, core, grading=client] Two lists are provided: `distance_km` and `delivery_minutes`, each containing six delivery records.

Create a scatter plot showing the relationship between distance and delivery time:
1. Create a scatter plot with `distance_km` on the x-axis and `delivery_minutes` on the y-axis

Use `plt.scatter(distance_km, delivery_minutes)`.
3. Add a comment on its own line: `# A scatterplot shows the relationship between two numerical variables; a bar chart compares values across categories`
  runtime={'kind': 'chart_renderer', 'version': '0.29.5', 'packages': ['matplotlib', 'pandas']} constraints.allowed=['import matplotlib.pyplot as plt', 'plt.scatter(x, y)', 'plt.xlabel()', 'plt.ylabel()', 'plt.title()', 'plt.show()', 'Python list literals', 'variable assignment', 'single-line comments (#)'] blocked=8 items
  file solution.py [editable]:
import matplotlib.pyplot as plt

# Data (these values will be changed by the grader to test your code)
dist_1 = 2.1
distance_km = [dist_1, 3.4, 2.8, 4.5, 5.2, 3.9]
time_1 = 18
delivery_minutes = [time_1, 22, 19, 26, 30, 24]

# Create a scatter plot showing the relationship between distance and delivery time

  SOLUTION solution.py:
import matplotlib.pyplot as plt

# Data (these values will be changed by the grader to test your code)
dist_1 = 2.1
distance_km = [dist_1, 3.4, 2.8, 4.5, 5.2, 3.9]
time_1 = 18
delivery_minutes = [time_1, 22, 19, 26, 30, 24]

# Create a scatter plot showing the relationship between distance and delivery time
plt.scatter(distance_km, delivery_minutes)
# A scatterplot shows the relationship between two numerical variables; a bar chart compares values across categories

  test ix.tile_viz_labeling_chart_selection.s10.t01 (figure_equals, visible=True): {"expected":{"n_axes":1,"chart_types":[["scatter"]]}} | on-fail: Your figure should contain exactly one scatter plot. Call `plt.scatter(distance_km, delivery_minutes)`.
  test ix.tile_viz_labeling_chart_selection.s10.t02 (plotted_data_equals, visible=True): {"chart":"scatter","field":"x","series":0,"axes":0,"expected":[2.1,3.4,2.8,4.5,5.2,3.9]} | on-fail: The scatter plot's x-values should be the distance_km list. Call `plt.scatter(distance_km, delivery_minutes)`.
  test ix.tile_viz_labeling_chart_selection.s10.t03 (plotted_data_equals, visible=True): {"chart":"scatter","field":"y","series":0,"axes":0,"expected":[18,22,19,26,30,24]} | on-fail: The scatter plot's y-values should be the delivery_minutes list. Call `plt.scatter(distance_km, delivery_minutes)`.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"075fc7f754e3ffba7f5b170bf9f33366c9182436498e08ae2b64ecb3052f966b","tests_passed":3}
  feedback✔: Great work! Your scatter plot shows the relationship between distance and delivery time with properly labeled axes.  feedback✘: Make sure you called `plt.scatter(distance_km, delivery_minutes)`.  hints: ['A scatter plot is used when you want to see the relationship between two numerical variables.', 'Use `plt.scatter(x, y)` to create a scatter plot.']
  MEASURES: B:identify_bar_chart_use_case(f1); B:identify_scatter_plot_use_case(f4)   anchors=['practice', 'assessment:identify_bar_chart_use_case', 'assessment:identify_scatter_plot_use_case']
  taught-before-tested: B.f1←s06; B.f4←s06

### s11 · recap · What you learned  [reward 5]
Recap — 
(takeaway) ax.set_xlabel(), ax.set_ylabel(), and ax.set_title() add axis labels and a title to an Axes object. Passing label= to a plot call and then calling ax.legend() adds a legend. In the pyplot interface, plt.xlabel(), plt.ylabel(), and plt.title() do the same. ⟦A.f1 A.f2 A.f3 B:tb3⟧
(takeaway) Chart type follows the question: bar for category comparison, histogram for distribution, line for trends over time, scatter for relationships between two numeric variables, and boxplot for spread comparison across groups. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb3⟧
[UP NEXT] Up next: Viz Custom Multi Panel: Next: style sheets, rcParams, and multi-panel figures

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Let's review — Here's another way to think about Axes labeling methods.
(practical_context) Think of the three set_* methods as captions for each part of the chart. ax.set_xlabel('Day') labels the x-axis. ax.set_ylabel('Average delivery time (minutes)') labels the y-axis. ax.set_title('Average delivery time by day') gives the whole chart a headline. Without these, the reader has to guess what the numbers mean. ⟦A.f1⟧
### r02 · Let's review — Here's another way to think about chart selection.
(practical_context) Ask yourself: What question am I answering? Comparing cities (which is fastest?) → bar chart. Showing how delivery times are spread out → histogram. Tracking change over days → line chart. Checking whether distance and time move together → scatter. Comparing the full spread across cities → boxplot. ⟦B.f1 B.f2 B.f3 B.f4 B.f5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: plt.subplots_adjust()
· constraints.blocked_syntax: plt.subplots() with nrows/ncols > 1

=========

# EVALUATOR PACKET — seaborn for Statistical Visualization (tile_viz_seaborn_stats_themes)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = viz.seaborn_dataframe_plotting — Plotting directly from pandas DataFrames with seaborn
B = viz.seaborn_statistical_functions — seaborn statistical plotting functions
C = viz.seaborn_themes_palettes — seaborn built-in themes and color palettes

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (viz.seaborn_dataframe_plotting)   objective: Plot directly from a pandas DataFrame's columns with seaborn by passing the DataFrame via data= and the column names via x=/y=, instead of extracting arrays first.
A.f1: Seaborn's plotting functions operate on dataframes and arrays containing whole datasets, taking only the names of the variables and their roles in the plot (for example data=, x=, y=) rather than requiring the caller to extract each array.   [sources: seaborn_introduction_tutorial#An introduction to seaborn]
A.f2: seaborn.barplot(data=..., x=..., y=...) visualizes an aggregate statistical estimate for each category as a bar; its default estimator is the mean, and it draws an error bar (uncertainty indicator) around each bar by default.   [sources: seaborn_official_docs#seaborn.barplot]
PRACTICE ANCHOR (live_code): Plot a seaborn bar chart directly from a DataFrame using data= and x=/y= column names, without extracting arrays first.  SUCCESS: A seaborn bar chart appears showing a mean value per category, with error bars drawn automatically, produced by a single sns.barplot() call that passes the DataFrame to data= and column name strings to x= and y=.
ASSESSMENT ANCHOR: build_seaborn_barplot_from_dataframe_using_column_names facts=['f1', 'f2']

## SOURCE FACTS — B (viz.seaborn_statistical_functions)   objective: Use a seaborn statistical plotting function to visualize a statistical relationship, such as a fitted trend between two numeric variables, directly from the data.
B.f1: Many seaborn functions will automatically perform the statistical estimation necessary to answer questions such as the average value of one variable as a function of other variables.   [sources: seaborn_introduction_tutorial#Statistical estimation]
B.f2: seaborn.regplot(data=..., x=..., y=...) plots a scatterplot of the observations together with a fitted linear regression line.   [sources: seaborn_official_docs#seaborn.regplot]
PRACTICE ANCHOR (live_code): Use sns.regplot() to visualize the relationship between two numeric columns in a DataFrame, producing a scatterplot with a fitted linear regression line in a single function call.  SUCCESS: A plot appears showing individual data points and a fitted trend line, produced by a single sns.regplot() call with data=, x=, and y= arguments referencing two numeric columns.
ASSESSMENT ANCHOR: identify_seaborn_automatic_statistical_estimation facts=['f1']
ASSESSMENT ANCHOR: apply_regplot_to_visualize_relationship_with_fitted_trend facts=['f2']
ASSESSMENT ANCHOR: select_correct_seaborn_statistical_function_for_given_question facts=['f1', 'f2']

## SOURCE FACTS — C (viz.seaborn_themes_palettes)   objective: Apply one of seaborn's built-in themes and a color palette to a plot using sns.set_theme().
C.f1: sns.set_theme(style=..., palette=...) changes the global defaults for all plots using the matplotlib rcParams system, so it affects matplotlib plots too, even ones not made with seaborn.   [sources: seaborn_introduction_tutorial#Opinionated defaults and flexible customization]
C.f2: seaborn.set_theme() accepts a style parameter (default 'darkgrid') and a palette parameter (default 'deep') among its arguments, which set the plot's background/gridline style and its color palette respectively.   [sources: seaborn_official_docs#seaborn.set_theme]
note: TOC conflict: the practice_objective says 'apply a seaborn theme to an existing plot', but set_theme() only changes defaults for plots drawn after the call, not a plot already drawn. The practice_anchor was adapted so the learner calls set_theme() before the plot function, matching the taught mechanism; retroactive restyling is not required or implied.
PRACTICE ANCHOR (live_code): Call sns.set_theme() with a named style and a named categorical palette, then draw a seaborn plot to confirm the theme is applied.  SUCCESS: A seaborn plot is produced whose background/gridline style and colors match the style and palette arguments passed to sns.set_theme(), with set_theme() called before the plot function.
ASSESSMENT ANCHOR: apply_seaborn_theme_and_palette_to_produce_polished_plot facts=['f1', 'f2']
ASSESSMENT ANCHOR: explain_global_rcparams_effect_on_subsequent_plots facts=['f1']
ASSESSMENT ANCHOR: identify_style_and_palette_parameters_and_their_defaults facts=['f2']

## DATA ASSETS USED
ds.orders: QuickDeliver orders — clean — columns: order_id(identifier,digits-as-label), city(categorical), delivery_time_minutes(numerical), distance_km(numerical), order_value(numerical), num_items(numerical)
   [1001,"Lagos",18,2.1,1850.0,2]
   [1002,"Lagos",22,3.4,2200.0,3]
   [1003,"Lagos",19,2.8,1600.0,1]
   [1004,"Lagos",26,4.5,3100.0,4]
   [1005,"Lagos",30,5.2,2750.0,3]
   [1006,"Lagos",24,3.9,2400.0,2]
   [1007,"Lagos",28,4.8,3300.0,5]
   [1008,"Lagos",50,9.1,4800.0,6]
   variant ds.orders.messy: 5 ops; planted: iss.missing_delivery_time(missing_value); iss.negative_delivery_time(impossible_value); iss.city_casing(inconsistent_category); iss.duplicate_order_1007(duplicate_row); iss.implausible_distance(outlier_suspicious)
ds.theming_demo: QuickDeliver theming demo — category/value — columns: category(categorical), value(numerical)
   ["Lagos",24.0]
   ["Abuja",27.0]
   ["Kano",30.0]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Anticipating stakeholder questions and objections; Basic A/B test structure (control vs treatment group); Basic presentation structure (opening, body, call to action); Conceptual effect of sample size on confidence; Conceptual interpretation of statistical significance/confidence level; Converting a vague business question into a specific, measurable analytical question; Custom styling/theming (advanced/optional); Defining a capstone business question/problem statement; Drawing a business conclusion from an experiment-result summary; Framing an actionable recommendation that is distinct from the finding itself; Identifying stakeholder needs/requirements before analysis; Identifying the business decision a stakeholder needs the analysis to inform; Interpreting lift/percentage change between groups; Making a data-driven recommendation; Matching chart type to the specific point being made (trend vs. comparison vs. distribution vs. part-to-whole); Multi-panel figures/subplots (advanced/optional); Prioritizing findings by relevance to the stakeholder's specific decision, not by analytical interestingness; Selecting an appropriate data retrieval method (SQL and/or spreadsheet); Simplifyi

## LESSON, in learner order

### s01 · explainer · seaborn's DataFrame-first interface  [reward 5]
Plotting directly from pandas DataFrames with seaborn — seaborn functions take a DataFrame and column names—no array extraction needed.
(intro) Most matplotlib calls require you to extract a column from orders yourself before plotting it. Seaborn's plotting functions operate on DataFrames and arrays containing whole datasets, taking only the names of the variables and their roles in the plot—data=, x=, y=—rather than requiring the caller to extract each array. ⟦A.f1 A:tb1⟧
(mechanism) sns.barplot(data=orders, x='city', y='delivery_time_minutes') plots average delivery time per city directly from the orders DataFrame and its column names—no separate .groupby() call needed first. Its default estimator is the mean, and it draws an error bar (uncertainty indicator) around each bar automatically. ⟦A.f2 A:tb2⟧
[CHART bar: Average Delivery Time by City — seaborn barplot] data=ds.orders x=city y=delivery_time_minutes color=None annotations=[] alt: A seaborn barplot showing the mean delivery_time_minutes for Lagos, Abuja, and Kano, with error bars indicating uncertainty around each mean.

### s02 · check · Check your understanding  [reward 5]
Plotting directly from pandas DataFrames with seaborn — 
QUESTION [choice, intro, grading=client] You have a DataFrame `orders` with columns `'city'` and `'delivery_time_minutes'`. Which seaborn call produces a bar chart of mean delivery time per city, without a separate `.groupby()` call?
  ✔ opt_correct: `sns.barplot(data=orders, x='city', y='delivery_time_minutes')`
      why: Correct. Seaborn takes the DataFrame via `data=` and column names via `x=` and `y=`, then computes the mean per category automatically — no `.groupby()` needed.
  ✘ opt_groupby: `sns.barplot(orders.groupby('city')['delivery_time_minutes'].mean())`
      why: Seaborn does not need a `.groupby()` call first. Pass the full DataFrame to `data=` and the column names to `x=` and `y=` — seaborn computes the mean per category automatically.
  ✘ opt_arrays: `sns.barplot(x=orders['city'], y=orders['delivery_time_minutes'].mean())`
      why: Passing `orders['delivery_time_minutes'].mean()` gives a single scalar, not per-city means. Pass the full DataFrame to `data=` and the column name string to `y=` — seaborn handles the aggregation.
  ✘ opt_plt: `plt.bar(orders['city'], orders['delivery_time_minutes'])`
      why: `plt.bar()` is a matplotlib function that requires pre-aggregated data. Seaborn's `sns.barplot()` accepts the raw DataFrame and computes the mean per category automatically.
  feedback✔: Right. Seaborn's `data=`, `x=`, `y=` interface lets you pass the DataFrame and column names directly — it handles the aggregation for you.  feedback✘: Use `sns.barplot(data=orders, x='city', y='delivery_time_minutes')`. Seaborn takes the full DataFrame and column name strings, then computes the mean per category automatically.  hints: ["Seaborn's plotting functions take `data=` (the DataFrame) and `x=`/`y=` (column name strings), not extracted arrays.", 'No `.groupby()` is needed — seaborn computes the mean per category automatically.']  remediation→r01
  MEASURES: A:build_seaborn_barplot_from_dataframe_using_column_names(f1,f2)   anchors=['assessment:build_seaborn_barplot_from_dataframe_using_column_names']
  taught-before-tested: A.f1←s01; A.f2←s01

### s03 · hands_on · Practice  [reward 5]
Plotting directly from pandas DataFrames with seaborn — Build a seaborn barplot from the orders DataFrame using column names.
QUESTION [code_exercise, core, grading=client] The `orders` DataFrame is already loaded with columns `'city'` and `'delivery_time_minutes'`.

Call `sns.barplot(data=orders, x='city', y='delivery_time_minutes')` to produce a bar chart showing the mean delivery time per city.

The figure should show one bar per city (Abuja, Kano, Lagos), with error bars drawn automatically by seaborn.
  runtime={'kind': 'chart_renderer', 'version': '0.29.5', 'packages': ['matplotlib', 'pandas', 'seaborn']} constraints.allowed=['import seaborn as sns', 'sns.barplot(data=..., x=..., y=...)', 'import pandas as pd', 'pd.DataFrame(...)', 'import matplotlib.pyplot as plt', 'plt.show()'] blocked=13 items
  file solution.py [editable]:
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Data
lagos_time_1 = 45
orders = pd.DataFrame({
    'city': ['Lagos', 'Abuja', 'Kano', 'Lagos', 'Abuja', 'Kano'],
    'delivery_time_minutes': [lagos_time_1, 38, 42, 48, 35, 40]
})
x_col = 'city'
y_col = 'delivery_time_minutes'

# Create a bar chart showing mean delivery time per city

  SOLUTION solution.py:
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Data
lagos_time_1 = 45
orders = pd.DataFrame({
    'city': ['Lagos', 'Abuja', 'Kano', 'Lagos', 'Abuja', 'Kano'],
    'delivery_time_minutes': [lagos_time_1, 38, 42, 48, 35, 40]
})
x_col = 'city'
y_col = 'delivery_time_minutes'

# Create a bar chart showing mean delivery time per city
sns.barplot(data=orders, x=x_col, y=y_col)

  test ix.tile_viz_seaborn_stats_themes.s03.t01 (figure_equals, visible=True): {"expected":{"n_axes":1,"chart_types":[["bar","line"]]}} | on-fail: Your figure should contain one Axes with a bar chart. Call `sns.barplot(data=orders, x='city', y='delivery_time_minutes')`.
  test ix.tile_viz_seaborn_stats_themes.s03.t03 (plotted_data_equals, visible=None): {"chart":"bar","field":"heights","expected":[46.5,36.5,41.0],"series":0,"axes":0} | on-fail: The bar heights should represent the mean delivery time for each city. Ensure your data has the correct values.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"cee92e5a976f2629f538c920b5b72a47dfb9cdf1f442d6b83bff3124296365f4","tests_passed":2}
  feedback✔: Well done! `sns.barplot()` computed the mean per city and drew error bars automatically — no `.groupby()` needed.  feedback✘: Call `sns.barplot(data=orders, x='city', y='delivery_time_minutes')`. Pass the DataFrame to `data=` and the column name strings to `x=` and `y=`.  hints: ["The three keyword arguments are `data=orders`, `x='city'`, and `y='delivery_time_minutes'`.", 'Seaborn computes the mean per category automatically — you do not need to call `.groupby()` first.']
  MEASURES: A:build_seaborn_barplot_from_dataframe_using_column_names(f1,f2)   anchors=['practice', 'assessment:build_seaborn_barplot_from_dataframe_using_column_names']
  taught-before-tested: A.f1←s01; A.f2←s01

### s04 · explainer · Automatic statistical estimation  [reward 5]
seaborn statistical plotting functions — Some seaborn functions compute statistics—means, regression lines—automatically.
(intro) Many seaborn functions automatically perform the statistical estimation necessary to answer questions such as the average value of one variable as a function of other variables. The sns.barplot() call from before is one such example—it computed each city's mean delivery time automatically, without a separate .groupby() step. ⟦B.f1 B:tb1⟧
(mechanism) sns.regplot(data=orders, x='distance_km', y='delivery_time_minutes') plots a scatterplot of the observations together with a fitted linear regression line. It shows the distance/delivery-time scatter with a fitted trend line drawn through it in the same call—no separate fitting step required. ⟦B.f2 B:tb2⟧
[BEFORE_AFTER] sns.regplot() adds a fitted regression line to the scatter plot automatically.
  before:
[CHART scatter: Distance vs Delivery Time (scatter only)] data=ds.orders x=distance_km y=delivery_time_minutes color=None annotations=[] alt: Scatter plot of distance_km vs delivery_time_minutes from the orders dataset. Points show a positive relationship but no trend line is drawn.
  after:
[CODE python]
import seaborn as sns
import matplotlib.pyplot as plt
sns.regplot(data=orders, x='distance_km', y='delivery_time_minutes')
plt.show()
# Scatter + fitted regression line in one call
  annotations: ['regplot draws scatter points and fits a regression line automatically']

### s05 · check · Check your understanding  [reward 5]
seaborn statistical plotting functions — 
QUESTION [choice, intro, grading=client] Which statement best describes what seaborn does when you call `sns.barplot(data=orders, x='city', y='delivery_time_minutes')`?
  ✔ opt_correct: Seaborn automatically computes the mean delivery time per city and draws a bar for each, without a separate aggregation step.
      why: Correct. Many seaborn functions automatically perform the statistical estimation necessary to answer questions such as the average value of one variable as a function of other variables.
  ✘ opt_raw: Seaborn draws one bar per row in the DataFrame, using the raw `delivery_time_minutes` value as the bar height.
      why: Seaborn does not draw one bar per row. It aggregates the data — by default computing the mean per category — and draws one bar per category.
  ✘ opt_manual: Seaborn requires you to compute the mean per city with `.groupby()` before calling `sns.barplot()`.
      why: Seaborn does not require a `.groupby()` call. It performs the statistical estimation (mean per category) automatically when you pass the full DataFrame and column names.
  ✘ opt_sum: Seaborn automatically computes the sum of delivery times per city and draws a bar for each.
      why: Seaborn's default estimator is the mean, not the sum. It computes the mean delivery time per city and draws one bar per city.
  feedback✔: Right. Seaborn automatically performs statistical estimation — `sns.barplot()` computes the mean per category without any manual aggregation.  feedback✘: Seaborn automatically performs the statistical estimation (mean per category by default) when you pass the full DataFrame and column names — no `.groupby()` needed.  hints: ["Think about what 'automatic statistical estimation' means — seaborn does the aggregation for you.", 'The default estimator in `sns.barplot()` is the mean, not the sum or raw values.']  remediation→r02
  MEASURES: B:identify_seaborn_automatic_statistical_estimation(f1)   anchors=['assessment:identify_seaborn_automatic_statistical_estimation']
  taught-before-tested: B.f1←s04

### s06 · check · Check your understanding  [reward 5]
seaborn statistical plotting functions — 
QUESTION [choice, core, grading=client] An analyst wants to visualize whether longer delivery distances tend to produce longer delivery times, with a fitted trend line drawn through the scatter points. Which seaborn call is correct?
  ✔ opt_regplot: `sns.regplot(data=orders, x='distance_km', y='delivery_time_minutes')`
      why: Correct. `sns.regplot(data=..., x=..., y=...)` plots a scatterplot of the observations together with a fitted linear regression line — exactly what is needed to visualize the trend.
  ✘ opt_barplot: `sns.barplot(data=orders, x='distance_km', y='delivery_time_minutes')`
      why: `sns.barplot()` computes the mean per category and draws bars. `distance_km` is a continuous numeric variable, not a category — use `sns.regplot()` to show the scatter and fitted trend line.
  ✘ opt_scatter: `plt.scatter(orders['distance_km'], orders['delivery_time_minutes'])`
      why: `plt.scatter()` shows the data points but does not add a fitted trend line. To get both the scatter and the regression line in one call, use `sns.regplot()`.
  ✘ opt_lineplot: `sns.lineplot(data=orders, x='distance_km', y='delivery_time_minutes')`
      why: `sns.lineplot()` connects data points with a line in the order they appear. It does not fit a regression line. Use `sns.regplot()` to get a scatter plot with a fitted linear regression line.
  feedback✔: Right. `sns.regplot()` produces a scatterplot with a fitted linear regression line in a single call.  feedback✘: `sns.regplot(data=orders, x='distance_km', y='delivery_time_minutes')` plots the scatter points and fits a linear regression line through them automatically.  hints: ['The question asks for a scatter plot with a fitted trend line — which seaborn function adds both in one call?', "`sns.regplot()` stands for 'regression plot' — it adds the fitted line automatically."]
  MEASURES: B:select_correct_seaborn_statistical_function_for_given_question(f1,f2)   anchors=['assessment:select_correct_seaborn_statistical_function_for_given_question']
  taught-before-tested: B.f1←s04; B.f2←s04

### s07 · hands_on · Practice  [reward 5]
seaborn statistical plotting functions — Use sns.regplot() to visualize the relationship between distance and delivery time.
QUESTION [code_exercise, core, grading=client] The `orders` DataFrame is already loaded with columns `'distance_km'` and `'delivery_time_minutes'`.

Call `sns.regplot(data=orders, x='distance_km', y='delivery_time_minutes')` to produce a scatter plot of the observations with a fitted linear regression line drawn through them.

The figure should show individual data points and a fitted trend line, produced by a single `sns.regplot()` call.
  runtime={'kind': 'chart_renderer', 'version': '0.29.5', 'packages': ['matplotlib', 'pandas', 'seaborn']} constraints.allowed=['import seaborn as sns', 'sns.regplot(data=..., x=..., y=...)', 'import pandas as pd', 'pd.DataFrame(...)', 'sns.barplot(data=..., x=..., y=...)'] blocked=7 items
  file solution.py [editable]:
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Data
dist_1 = 2.1
orders = pd.DataFrame({
    'distance_km': [dist_1, 3.4, 2.8, 4.5, 5.2, 3.9],
    'delivery_time_minutes': [18, 22, 19, 26, 30, 24]
})
x_col = 'distance_km'
y_col = 'delivery_time_minutes'

# Create a scatter plot with regression line

  SOLUTION solution.py:
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Data
dist_1 = 2.1
orders = pd.DataFrame({
    'distance_km': [dist_1, 3.4, 2.8, 4.5, 5.2, 3.9],
    'delivery_time_minutes': [18, 22, 19, 26, 30, 24]
})
x_col = 'distance_km'
y_col = 'delivery_time_minutes'

# Create a scatter plot with regression line
sns.regplot(data=orders, x=x_col, y=y_col)

  test ix.tile_viz_seaborn_stats_themes.s07.t01 (figure_equals, visible=True): {"expected":{"n_axes":1,"chart_types":[["line","scatter","area"]]}} | on-fail: Your figure should contain one Axes with a scatter plot (plus a regression line). Call `sns.regplot(data=orders, x='distance_km', y='delivery_time_minutes')`.
  test ix.tile_viz_seaborn_stats_themes.s07.t03 (value_equals, visible=True): {"expr":"orders['distance_km'].iloc[0]","expected":2.1} | on-fail: The first distance value should be dist_1.
  test ix.tile_viz_seaborn_stats_themes.s07.t02 (plotted_data_equals, visible=True): {"chart":"scatter","field":"x","expected":[2.1,3.4,2.8,4.5,5.2,3.9],"series":0,"axes":0,"sorted":false} | on-fail: The scatter plot should use `distance_km` as the x-axis. Pass `x='distance_km'` to `sns.regplot()`.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"5cc05afd5fe0a692ac84ab8563803ab5e8fe8f16c33eaa265833dce6125009f1","tests_passed":3}
  feedback✔: Well done! `sns.regplot()` drew the scatter points and fitted the regression line automatically in a single call.  feedback✘: Call `sns.regplot(data=orders, x='distance_km', y='delivery_time_minutes')`. Pass the DataFrame to `data=` and the column name strings to `x=` and `y=`.  hints: ["The three keyword arguments are `data=orders`, `x='distance_km'`, and `y='delivery_time_minutes'`.", '`sns.regplot()` adds the fitted regression line automatically — you do not need a separate call.']
  MEASURES: B:apply_regplot_to_visualize_relationship_with_fitted_trend(f2)   anchors=['practice', 'assessment:apply_regplot_to_visualize_relationship_with_fitted_trend']
  taught-before-tested: B.f2←s04

### s08 · explainer · Polishing plots with sns.set_theme()  [reward 5]
seaborn built-in themes and color palettes — sns.set_theme() changes the global defaults for all plots—seaborn and matplotlib alike.
(intro) sns.set_theme(style='whitegrid', palette='deep') switches to a white background with gridlines and seaborn's 'deep' color palette. The style parameter (default 'darkgrid') controls the background and gridlines; the palette parameter (default 'deep') controls the color sequence. ⟦C.f2 C:tb1⟧
(mechanism) sns.set_theme() changes the global defaults for all plots using the matplotlib rcParams system, so it affects matplotlib plots too, even ones not made with seaborn. Because it works by changing global defaults, calling sns.set_theme() changes how plots drawn after that call look—it does not restyle a figure already displayed. ⟦C.f1 C:tb2⟧
[BEFORE_AFTER] sns.set_theme() changes the background, gridlines, and color palette for all subsequent plots.
  before:
[CHART bar: Default matplotlib style] data=ds.theming_demo x=category y=value color=None annotations=[] alt: Bar chart of category vs value using ds.theming_demo with matplotlib's default white background, blue bars, and no gridlines.
  after:
[CODE python]
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style='whitegrid', palette='deep')
sns.barplot(data=theming_demo, x='category', y='value')
plt.show()
# White background, gridlines, seaborn 'deep' palette
  annotations: ['set_theme applies style and palette globally via rcParams']

### s09 · check · Check your understanding  [reward 5]
seaborn built-in themes and color palettes — 
QUESTION [choice, core, grading=client] A notebook cell calls `sns.set_theme(style='whitegrid', palette='deep')` and then draws a seaborn bar chart. The next cell draws a plain matplotlib line chart without calling `sns.set_theme()` again. What will the matplotlib line chart look like?
  ✔ opt_correct: It will use the whitegrid style and deep palette, because `sns.set_theme()` changes global matplotlib rcParams that affect all subsequent plots.
      why: Correct. `sns.set_theme()` changes the global defaults for all plots using the matplotlib rcParams system, so it affects matplotlib plots too, even ones not made with seaborn.
  ✘ opt_default: It will use default matplotlib styling, because `sns.set_theme()` only affects seaborn plots.
      why: `sns.set_theme()` does not only affect seaborn plots. It changes the global matplotlib rcParams, so all subsequent plots — including plain matplotlib ones — use the new style.
  ✘ opt_error: It will raise an error, because `sns.set_theme()` must be called before every plot.
      why: `sns.set_theme()` does not need to be called before every plot. Once called, it changes the global rcParams, which persist for all subsequent plots in the session.
  ✘ opt_retroactive: The seaborn bar chart will be restyled to match the matplotlib defaults.
      why: `sns.set_theme()` changes defaults for plots drawn after the call — it does not go back and restyle a figure you already drew and displayed earlier.
  feedback✔: Right. `sns.set_theme()` works by changing matplotlib's global rcParams, so it affects every plot drawn after the call — seaborn or not.  feedback✘: `sns.set_theme()` changes the global matplotlib rcParams. Because it changes global defaults, all plots drawn after the call — including plain matplotlib plots — use the new style.  hints: ["Think about what 'global defaults' means — once changed, they apply to everything drawn afterward.", "`sns.set_theme()` works through matplotlib's rcParams system, not a seaborn-only mechanism."]  remediation→r03
  MEASURES: C:explain_global_rcparams_effect_on_subsequent_plots(f1)   anchors=['assessment:explain_global_rcparams_effect_on_subsequent_plots']
  taught-before-tested: C.f1←s08

### s10 · hands_on · Practice  [reward 5]
seaborn built-in themes and color palettes — Apply a seaborn theme and palette to produce a polished plot.
QUESTION [code_exercise, core, grading=client] A DataFrame `df` with columns `category` and `value` is already loaded.

Apply a seaborn theme and create a bar plot:
1. Call `sns.set_theme(style='whitegrid', palette='deep')` to set the theme
2. Call `sns.barplot(data=df, x='category', y='value')` to create the bar plot

The theme will change the background and colors of the plot.
  runtime={'kind': 'chart_renderer', 'version': '0.29.5', 'packages': ['matplotlib', 'pandas', 'seaborn']} constraints.allowed=['import seaborn as sns', 'import pandas as pd', 'sns.set_theme(style=..., palette=...)', 'sns.barplot(...)', 'sns.scatterplot(...)', 'sns.histplot(...)', 'pd.DataFrame(...)', 'variable assignment', 'string literals for style and palette names'] blocked=6 items
  file solution.py [editable]:
import seaborn as sns
import pandas as pd

# Data (these values will be changed by the grader to test your code)
val_a_1 = 23
df = pd.DataFrame({
    'category': ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C'],
    'value': [val_a_1, 25, 22, 45, 47, 44, 56, 58, 55]
})

# Set the theme and create the plot below


  SOLUTION solution.py:
import seaborn as sns
import pandas as pd

# Data (already loaded)
val_a_1 = 23
df = pd.DataFrame({
    'category': ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C'],
    'value': [val_a_1, 25, 22, 45, 47, 44, 56, 58, 55]
})

# Set the theme and create the plot
sns.set_theme(style='whitegrid', palette='deep')
sns.barplot(data=df, x='category', y='value')

  test ix.tile_viz_seaborn_stats_themes.s10.t01 (figure_equals, visible=True): {"expected":{"n_axes":1,"chart_types":[["bar","line"]]}} | on-fail: Your figure should contain one Axes with a bar chart. The starter already includes the barplot call.
  test ix.tile_viz_seaborn_stats_themes.s10.t03 (value_equals, visible=None): {"expr":"df['value'].tolist()","expected":[23,25,22,45,47,44,56,58,55]} | on-fail: The bar heights should represent the mean value for each category. Ensure your data has the correct values.
  test ix.tile_viz_seaborn_stats_themes.s10.t02 (plotted_data_equals, visible=True): {"chart":"bar","field":"heights","expected":[23.333333333333332,45.333333333333336,56.333333333333336],"series":0,"axes":0} | on-fail: The bar chart should show the mean value for each category. The starter already includes the correct barplot call.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"5c360c7b5e7018b2a4ff8e6d81580240f91eb9520285826d4b9c44c74b496e8e","tests_passed":3}
  feedback✔: Well done! You called `sns.set_theme(style='whitegrid', palette='deep')` before the plot, applying the whitegrid style and deep palette to the figure.  feedback✘: Make sure you called `sns.set_theme(style='whitegrid', palette='deep')` before the barplot.  hints: ["Call `sns.set_theme()` with two keyword arguments: `style='whitegrid'` and `palette='deep'`.", "The set_theme() call must come before the barplot call to affect the plot's appearance."]
  MEASURES: C:apply_seaborn_theme_and_palette_to_produce_polished_plot(f1,f2); C:identify_style_and_palette_parameters_and_their_defaults(f2)   anchors=['practice', 'assessment:apply_seaborn_theme_and_palette_to_produce_polished_plot', 'assessment:identify_style_and_palette_parameters_and_their_defaults']
  taught-before-tested: C.f1←s08; C.f2←s08; C.f2←s08

### s11 · recap · What you learned  [reward 5]
Recap — 
(takeaway) Seaborn's plotting functions take data=, x=, and y= arguments, so you pass the DataFrame and column names directly—no array extraction needed. sns.barplot() computes the mean per category and draws error bars automatically. ⟦A.f1 A.f2⟧
(takeaway) Many seaborn functions perform statistical estimation automatically. sns.regplot(data=orders, x='distance_km', y='delivery_time_minutes') plots a scatterplot together with a fitted linear regression line in one call. ⟦B.f1 B.f2⟧
(takeaway) sns.set_theme(style='whitegrid', palette='deep') changes the global defaults for all subsequent plots via matplotlib's rcParams—including plots not made with seaborn. ⟦C.f1 C.f2⟧
[UP NEXT] You've completed this section!: You've completed the visualization section!

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Let's review — Here's another way to think about seaborn's DataFrame interface.
(practical_context) With matplotlib you write city_avg = orders.groupby('city')['delivery_time_minutes'].mean() then ax.bar(city_avg.index, city_avg.values). With seaborn you write sns.barplot(data=orders, x='city', y='delivery_time_minutes'). The difference: seaborn takes the whole DataFrame and column names as strings, computing the mean automatically. ⟦A.f1 A.f2⟧
### r02 · Let's review — Here's another way to think about seaborn's automatic estimation.
(practical_context) When you call sns.barplot(data=orders, x='city', y='delivery_time_minutes'), seaborn computes the mean delivery time for each city automatically—you don't need a .groupby().mean() step first. This automatic statistical estimation is what makes seaborn different from matplotlib's raw plotting functions. ⟦B.f1⟧
### r03 · Let's review — Here's another way to think about sns.set_theme().
(practical_context) sns.set_theme() works by changing matplotlib's rcParams—the global settings that control how all plots look. Because it changes global defaults, every plot drawn after the call uses the new style, whether it's a seaborn plot or a plain matplotlib plot. ⟦C.f1⟧

## OTHER CONTENT (fields without a dedicated renderer)
· y.title: Avg delivery time (min)
· constraints.blocked_syntax: matplotlib.rcParams direct manipulation
· constraints.blocked_syntax: custom theme dictionaries
· constraints.blocked_syntax: subplots / multi-panel figures