# EVALUATOR PACKET — Labeling and Chart Selection (tile_viz_labeling_chart_selection)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = viz.labeling_annotation — Labeling axes, titles, and legends
B = viz.chart_type_selection — Matching chart type to the analytical question

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s04 · check · Check your understanding  [reward 5]
Labeling axes, titles, and legends — 

### s05 · hands_on · Practice  [reward 5]
Labeling axes, titles, and legends — Add a title, axis labels, and a legend to an unlabeled plot.

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
[VIDEO ] bridge-before:  | bridge-after: 

### s08 · check · Check your understanding  [reward 5]
Matching chart type to the analytical question — 

### s09 · check · Check your understanding  [reward 5]
Matching chart type to the analytical question — 

### s10 · hands_on · Practice  [reward 5]
Matching chart type to the analytical question — Choose the right chart type for each analytical question.

### s11 · recap · What you learned  [reward 5]
Recap — 
(takeaway) ax.set_xlabel(), ax.set_ylabel(), and ax.set_title() add axis labels and a title to an Axes object. Passing label= to a plot call and then calling ax.legend() adds a legend. In the pyplot interface, plt.xlabel(), plt.ylabel(), and plt.title() do the same. ⟦A.f1 A.f2 A.f3⟧
(takeaway) Chart type follows the question: bar for category comparison, histogram for distribution, line for trends over time, scatter for relationships between two numeric variables, and boxplot for spread comparison across groups. ⟦B.f1 B.f2 B.f3 B.f4 B.f5⟧
[UP NEXT] Up next: Viz Seaborn Stats Themes: Next: seaborn's DataFrame interface and statistical plotting functions

### r01 · remediation · Let's review  [reward 5]
Labeling axes, titles, and legends — Here's another way to think about Axes labeling methods.
(practical_context) Think of the three set_* methods as captions for each part of the chart. ax.set_xlabel('Day') labels the x-axis. ax.set_ylabel('Average delivery time (minutes)') labels the y-axis. ax.set_title('Average delivery time by day') gives the whole chart a headline. Without these, the reader has to guess what the numbers mean. ⟦A.f1⟧

### r02 · remediation · Let's review  [reward 5]
Matching chart type to the analytical question — Here's another way to think about chart selection.
(practical_context) Ask yourself: What question am I answering? Comparing cities (which is fastest?) → bar chart. Showing how delivery times are spread out → histogram. Tracking change over days → line chart. Checking whether distance and time move together → scatter. Comparing the full spread across cities → boxplot. ⟦B.f1 B.f2 B.f3 B.f4 B.f5⟧

=========

# EVALUATOR PACKET — Multi-Panel Figures and Custom Styling (tile_viz_custom_multi_panel)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = viz.custom_styling_theming — Custom styling/theming (advanced/optional)
B = viz.multi_panel_figures — Multi-panel figures/subplots (advanced/optional)

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · check · Check your understanding  [reward 5]
Customizing plot appearance with rcParams and styles — 

### s04 · hands_on · Practice  [reward 5]
Customizing plot appearance with rcParams and styles — Set rcParams globally and apply a seaborn palette.

### s05 · explainer · A grid of Axes in one Figure  [reward 5]
Creating multi-panel figures with subplots — plt.subplots(nrows, ncols) creates a Figure containing a grid of Axes.
(intro) Suppose you want to show the delivery-time histogram and the distance/delivery-time scatter plot together, side by side, instead of as two separate figures. fig, axs = plt.subplots(nrows, ncols) creates a Figure containing a grid of Axes with the given number of rows and columns. plt.subplots(2, 2) creates a 2×2 grid of four Axes inside one Figure. ⟦B.f1 B:tb1 B:tb2⟧
(mechanism) Each Axes in the returned grid is indexed separately—for example axs[0, 0] for the top-left panel. Plotting and labeling calls made on one Axes only affect that panel. axs[0, 0].hist(orders['delivery_time_minutes']) draws the histogram into the top-left panel; axs[0, 1].scatter(orders['distance_km'], orders['delivery_time_minutes']) draws the scatter into the top-right panel without disturbing the first. ⟦B.f2 B:tb3⟧
[DIAGRAM] nodes=['Figure', 'axs[0,0]\nTop-left', 'axs[0,1]\nTop-right', 'axs[1,0]\nBottom-left', 'axs[1,1]\nBottom-right'] edges=[] alt: A 2×2 grid of empty Axes boxes inside a single Figure boundary. Each box is labelled with its index: axs[0,0] top-left, axs[0,1] top-right, axs[1,0] bottom-left, axs[1,1] bottom-right.

### s06 · video · Video walkthrough  [reward 5]
Creating multi-panel figures with subplots — 
[VIDEO ] bridge-before:  | bridge-after: 

### s07 · check · Check your understanding  [reward 5]
Creating multi-panel figures with subplots — 

### s08 · hands_on · Practice  [reward 5]
Creating multi-panel figures with subplots — Create a subplot grid and plot on each Axes independently.

### s09 · recap · What you learned  [reward 5]
Recap — 
(takeaway) plt.style.use('style-name') applies a predefined style sheet. mpl.rcParams['lines.linewidth'] = 2 sets a specific default globally. sns.set_palette('pastel') sets the color cycle from a seaborn palette. ⟦A.f1 A.f2 A.f3⟧
(takeaway) fig, axs = plt.subplots(nrows, ncols) creates a Figure with a grid of Axes. Each Axes is indexed separately (axs[0, 0]) and plotting calls on one panel don't affect the others. ⟦B.f1 B.f2⟧
[UP NEXT] Up next: Stats Ab Test Lift: Next: seaborn's DataFrame interface and statistical plotting functions

### r01 · remediation · Let's review  [reward 5]
Customizing plot appearance with rcParams and styles — Here's another way to think about style sheets.
(practical_context) plt.style.use('ggplot') changes the look of all plots drawn after that call—background color, grid lines, font sizes, and more. You can see all available style names by printing plt.style.available. Call it once at the top of your notebook to set a consistent look. ⟦A.f1⟧

### r02 · remediation · Let's review  [reward 5]
Creating multi-panel figures with subplots — Here's another way to think about subplot indexing.
(practical_context) When plt.subplots(2, 2) returns axs, think of it as a 2D grid. axs[0, 0] is the top-left panel, axs[0, 1] is top-right, axs[1, 0] is bottom-left, axs[1, 1] is bottom-right. Plotting on axs[0, 0] only affects that one panel—the others stay empty until you plot on them. ⟦B.f2⟧

## OTHER CONTENT (fields without a dedicated renderer)
· nodes.label: axs[1,0]
Bottom-left
· nodes.label: axs[1,1]
Bottom-right

=========

# EVALUATOR PACKET — seaborn for Statistical Visualization (tile_viz_seaborn_stats_themes)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = viz.seaborn_dataframe_plotting — Plotting directly from pandas DataFrames with seaborn
B = viz.seaborn_statistical_functions — seaborn statistical plotting functions
C = viz.seaborn_themes_palettes — seaborn built-in themes and color palettes

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
[BEFORE_AFTER] seaborn's data= and column-name arguments replace manual groupby and array extraction.
  before:
[CODE python]
import matplotlib.pyplot as plt
# matplotlib: extract columns first
fig, ax = plt.subplots()
city_avg = orders.groupby('city')['delivery_time_minutes'].mean()
ax.bar(city_avg.index, city_avg)
plt.show()
  annotations: ['Must groupby and extract before plotting']
  after:
[CODE python]
import seaborn as sns
import matplotlib.pyplot as plt
# seaborn: pass DataFrame and column names
sns.barplot(data=orders, x='city', y='delivery_time_minutes')
plt.show()
  annotations: ['data= takes the DataFrame; x= and y= take column names']

### s02 · check · Check your understanding  [reward 5]
Plotting directly from pandas DataFrames with seaborn — 

### s03 · hands_on · Practice  [reward 5]
Plotting directly from pandas DataFrames with seaborn — Build a seaborn barplot from the orders DataFrame using column names.

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

### s06 · check · Check your understanding  [reward 5]
seaborn statistical plotting functions — 

### s07 · hands_on · Practice  [reward 5]
seaborn statistical plotting functions — Use sns.regplot() to visualize the relationship between distance and delivery time.

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

### s10 · hands_on · Practice  [reward 5]
seaborn built-in themes and color palettes — Apply a seaborn theme and palette to produce a polished plot.

### s11 · recap · What you learned  [reward 5]
Recap — 
(takeaway) Seaborn's plotting functions take data=, x=, and y= arguments, so you pass the DataFrame and column names directly—no array extraction needed. sns.barplot() computes the mean per category and draws error bars automatically. ⟦A.f1 A.f2⟧
(takeaway) Many seaborn functions perform statistical estimation automatically. sns.regplot(data=orders, x='distance_km', y='delivery_time_minutes') plots a scatterplot together with a fitted linear regression line in one call. ⟦B.f1 B.f2⟧
(takeaway) sns.set_theme(style='whitegrid', palette='deep') changes the global defaults for all subsequent plots via matplotlib's rcParams—including plots not made with seaborn. ⟦C.f1 C.f2⟧
[UP NEXT] You've completed this section!: You've completed the visualization section!

### r01 · remediation · Let's review  [reward 5]
Plotting directly from pandas DataFrames with seaborn — Here's another way to think about seaborn's DataFrame interface.
(practical_context) With matplotlib you write ax.bar(orders['city'], orders['delivery_time_minutes']). With seaborn you write sns.barplot(data=orders, x='city', y='delivery_time_minutes'). The difference: seaborn takes the whole DataFrame and column names as strings, so you never extract a column manually. ⟦A.f1 A.f2⟧

### r02 · remediation · Let's review  [reward 5]
seaborn statistical plotting functions — Here's another way to think about seaborn's automatic estimation.
(practical_context) When you call sns.barplot(data=orders, x='city', y='delivery_time_minutes'), seaborn computes the mean delivery time for each city automatically—you don't need a .groupby().mean() step first. This automatic statistical estimation is what makes seaborn different from matplotlib's raw plotting functions. ⟦B.f1⟧

### r03 · remediation · Let's review  [reward 5]
seaborn built-in themes and color palettes — Here's another way to think about sns.set_theme().
(practical_context) sns.set_theme() works by changing matplotlib's rcParams—the global settings that control how all plots look. Because it changes global defaults, every plot drawn after the call uses the new style, whether it's a seaborn plot or a plain matplotlib plot. ⟦C.f1⟧