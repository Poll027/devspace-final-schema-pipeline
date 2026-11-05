# EVALUATOR PACKET — Bar Charts and Histograms (tile_viz_bar_histograms)
Tile summary: Learn to compare categories with plt.bar() and reveal distributions with plt.hist(), understanding the zero-baseline rule and the bins parameter.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = viz.bar_charts — Bar charts
B = viz.histograms — Histograms

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (viz.bar_charts)   objective: Create a bar chart with matplotlib to compare a numeric value across discrete categories, aligning bars to a common baseline.
A.f1: plt.bar(x, height) (or ax.bar(x, height)) makes a bar plot with bars positioned at the given x coordinates and given heights, with the baseline defaulting to 0.   [sources: matplotlib_official_docs#matplotlib.pyplot.bar]
A.f2: A bar chart is a common chart type for graphing categorical data or data sorted into groups.   [sources: swd_what_is_a_bar_chart]
A.f3: Bar charts are easy to interpret because the eye is good at comparing lengths when the objects being compared are aligned to a common baseline.   [sources: swd_what_is_a_bar_chart]
A.f4: Categorical variables such as names can be passed directly as the x argument to plt.bar() (for example plt.bar(names, values)), rather than only numeric x-positions.   [sources: matplotlib_pyplot_tutorial#Plotting with categorical variables]
A.m1 (misconception): A bar's baseline can start at any value without distorting the comparison.   [sources: swd_what_is_a_bar_chart]
note: Build on pandas.groupby_aggregation's own orders/city/delivery_time_minutes example so the dataset is familiar.
PRACTICE ANCHOR (live_code): Given a grouped summary of average delivery time by city, plot a bar chart comparing the three city averages.  SUCCESS: A bar chart appears with city names on the x-axis, average delivery times as bar heights, and a baseline of 0.
ASSESSMENT ANCHOR: identify_bar_chart_as_categorical_comparison_tool facts=['f2']
ASSESSMENT ANCHOR: construct_bar_chart_with_plt_bar_using_categorical_x facts=['f1', 'f4']
ASSESSMENT ANCHOR: explain_why_zero_baseline_is_required_for_valid_length_comparison facts=['f3', 'm1']

## SOURCE FACTS — B (viz.histograms)   objective: Create a histogram with matplotlib to visualize a numeric variable's distribution, and adjust the bins parameter to change how the data is binned.
B.f1: plt.hist(x, bins=...) uses numpy.histogram to bin the data in x, count the number of values in each bin, and draw the result as bars.   [sources: matplotlib_official_docs#matplotlib.pyplot.hist]
B.f2: The bins parameter defaults to rcParams['hist.bins'], which defaults to 10; passing an integer sets that many equal-width bins, passing a sequence sets explicit bin edges, and passing a string such as 'auto' selects a binning strategy.   [sources: matplotlib_official_docs#matplotlib.pyplot.hist]
PRACTICE ANCHOR (live_code): Plot a histogram of the delivery_time_minutes column and adjust the bin count to better reveal its distribution shape.  SUCCESS: A histogram of delivery_time_minutes is displayed with a non-default bin count (or explicit bin edges) that makes the distribution shape clearer than the default 10-bin view.
ASSESSMENT ANCHOR: call_plt_hist_and_explain_binning_mechanism facts=['f1']
ASSESSMENT ANCHOR: configure_bins_parameter_with_integer_sequence_or_string facts=['f2']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Basic A/B test structure (control vs treatment group); Box plots; Conceptual effect of sample size on confidence; Conceptual interpretation of statistical significance/confidence level; Converting a vague business question into a specific, measurable analytical question; Custom styling/theming (advanced/optional); Drawing a business conclusion from an experiment-result summary; Framing an actionable recommendation that is distinct from the finding itself; Histograms; Identifying stakeholder needs/requirements before analysis; Identifying the business decision a stakeholder needs the analysis to inform; Interpreting lift/percentage change between groups; Labeling axes, titles, and legends; Line plots; Making a data-driven recommendation; Matching chart type to the analytical question; Multi-panel figures/subplots (advanced/optional); Plotting directly from pandas DataFrames with seaborn; Prioritizing findings by relevance to the stakeholder's specific decision, not by analytical interestingness; Scatter plots; Stating a finding precisely and quantitatively (the specific number or comparison, not a vague claim); Tailoring level of detail to audience technical background; Translating 

## LESSON, in learner order

### s01 · explainer · Comparing Cities with a Bar Chart  [reward 5]
bar charts — When you want to compare a number across discrete categories, a bar chart aligns every bar to a shared baseline so the eye can judge lengths at a glance.
(intro) Suppose you want to compare average delivery time across Lagos, Abuja, and Kano. A bar chart is a common chart type for graphing categorical data or data sorted into groups — which fits this comparison exactly. ⟦A.f2 A:tb1⟧
(syntax) `plt.bar(x, height)` (or `ax.bar(x, height)`) makes a bar plot with bars positioned at the given x coordinates and given heights, with the baseline defaulting to 0. Categorical names can be passed directly as the x argument: `plt.bar(city_avg.index, city_avg)` plots the three city names as bar positions and each city's average delivery time as the bar height. ⟦A.f1 A.f4 A:tb2⟧
[BEFORE_AFTER] Adding groupby + plt.bar turns a flat list into a per-city comparison chart.
  before:
[CODE python]
# Delivery times as a raw list — hard to compare cities
print(orders['delivery_time_minutes'].tolist())
  annotations: ['A flat list gives no per-city comparison']
  after:
[CODE python]
city_avg = orders.groupby('city')['delivery_time_minutes'].mean()
plt.bar(city_avg.index, city_avg)
  annotations: ['groupby + mean produces one average per city', 'plt.bar(city_avg.index, city_avg) passes city names as x and averages as heights']

### s02 · video · Bar Charts: Live Code and the Zero-Baseline Rule  [reward 5]
watch — 
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · explainer · Why the Baseline Must Start at Zero  [reward 5]
bar charts — The bar chart's power comes from comparing lengths — and that only works when every bar starts at the same point.
(mental_model) Bar charts are easy to interpret because the eye is good at comparing lengths when the objects being compared are aligned to a common baseline. Every bar starts at 0, so a taller bar genuinely represents a larger value — Kano's bar looks taller than Lagos's because its average delivery time is higher. ⟦A.f3 A:tb3⟧
(misconception) Starting bars at a value other than 0 — say 20 minutes — distorts the comparison. If Kano averages 30 minutes and Lagos 25, bars starting at 20 are 10 and 5 units tall: Kano's bar looks twice as long even though its average is only 5 minutes higher. Keep the baseline at 0. ⟦A.f3 A.m1 A:tb4⟧

### s04 · check · When to Use a Bar Chart  [reward 10]
quick check — Which kind of data is a bar chart designed to compare?

### s05 · check · The Zero-Baseline Rule  [reward 10]
quick check — Why must a bar chart's baseline start at zero?

### s06 · hands_on · Plot City Averages with plt.bar()  [reward 15]
hands-on — Use groupby to compute per-city averages, then pass the city names and averages to plt.bar().

### s07 · explainer · Seeing the Distribution with a Histogram  [reward 5]
histograms — A histogram bins a numeric variable and draws one bar per bin — revealing the shape of the distribution rather than individual values.
(intro) A bar chart compares categories, but delivery times are a numeric variable. You might instead want to see how those times are distributed — how many deliveries were fast, how many were slow, and whether most cluster in the middle. A histogram answers that question. ⟦B.f1 B:tb1⟧
(mechanism) `plt.hist(x, bins=...)` uses `numpy.histogram` to bin the data in x, count the number of values in each bin, and draw the result as bars. `plt.hist(orders['delivery_time_minutes'])` bins every delivery time and shows how many orders fall into each time range. ⟦B.f1 B:tb2⟧
(syntax) The `bins` parameter defaults to `rcParams['hist.bins']`, which defaults to 10. Passing an integer sets that many equal-width bins; passing a sequence sets explicit bin edges; passing a string such as `'auto'` selects a binning strategy automatically. ⟦B.f2 B:tb3⟧
[BEFORE_AFTER] plt.hist() replaces a sorted list with a binned bar chart that reveals the distribution shape.
  before:
[CODE python]
# Delivery times as a sorted list — shape is not visible
print(sorted(orders['delivery_time_minutes'].tolist()))
  annotations: ['A sorted list shows individual values but not the distribution shape']
  after:
[CODE python]
plt.hist(orders['delivery_time_minutes'], bins=10)
  annotations: ['plt.hist bins the values and draws one bar per bin, revealing the distribution shape']

### s08 · video · Histograms: Binning and Distribution Shape  [reward 5]
watch — 
[VIDEO ] bridge-before:  | bridge-after: 

### s09 · check · How plt.hist() Works  [reward 10]
quick check — What does plt.hist() do with the values you pass it?

### s10 · check · Controlling Bin Count  [reward 10]
quick check — What does passing an integer to the bins parameter do?

### s11 · hands_on · Plot a Delivery-Time Histogram  [reward 15]
hands-on — Call plt.hist() on the delivery_time_minutes column and experiment with the bins parameter.

### s12 · recap · Bar Charts and Histograms: What You Learned  [reward 10]
recap — Two chart types, two different questions — categories versus distribution.
(takeaway) Use `plt.bar(x, height)` to compare a numeric value across discrete categories, keeping the baseline at 0 so bar lengths stay honest. Use `plt.hist(x, bins=...)` to reveal how a numeric variable is distributed — it bins the values and draws one bar per bin.
[UP NEXT] Up next: Line Plots, Scatter Plots, and Box Plots: Next you'll plot trends over time with plt.plot(), relationships between two numeric variables with plt.scatter(), and per-city spread with plt.boxplot().

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Bar Charts Are for Categories — A bar chart compares a numeric value across discrete groups — not distributions or trends.
(definition) A bar chart is a common chart type for graphing categorical data or data sorted into groups. The three cities Lagos, Abuja, and Kano are discrete categories, so a bar chart comparing their average delivery times is the right fit. A histogram would show the spread of times, not a city-by-city comparison. ⟦A.f2 A:tb1⟧
### r02 · The Baseline Must Be Zero — Shifting the baseline away from zero makes bars misleading because the eye compares lengths.
(misconception) Bar charts are easy to interpret because the eye compares lengths from a common baseline. If Kano averages 30 minutes and Lagos 25, bars starting at 20 are 10 and 5 units tall — Kano's bar looks twice as long even though its average is only 5 minutes higher. Keep the baseline at 0 so lengths stay proportional to values. ⟦A.f3 A.m1 A:tb3 A:tb4⟧
### r03 · How plt.hist() Bins Your Data — plt.hist() doesn't just count values — it groups them into bins first.
(mechanism) `plt.hist(x, bins=...)` uses `numpy.histogram` to bin the data in x, count the number of values in each bin, and draw the result as bars. Each bar represents a range of values, not a single value — that's what makes a histogram different from a bar chart. ⟦B.f1 B:tb2⟧
### r04 · Controlling Bins in plt.hist() — The bins parameter accepts an integer, a sequence, or a strategy string.
(syntax) The `bins` parameter defaults to `rcParams['hist.bins']`, which defaults to 10. Passing an integer sets that many equal-width bins. Passing a sequence sets explicit bin edges. Passing a string such as `'auto'` selects a binning strategy automatically. ⟦B.f2 B:tb3⟧

=========

# EVALUATOR PACKET — Line Plots, Scatter Plots, and Box Plots (tile_viz_line_scatter_box)
Tile summary: Plot trends over time with plt.plot(), relationships between two numeric variables with plt.scatter(), and per-group distributions with plt.boxplot().
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = viz.line_plots — Line plots
B = viz.scatter_plots — Scatter plots
C = viz.box_plots — Box plots

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (viz.line_plots)   objective: Create a line plot with matplotlib to visualize a trend in a numeric value over an ordered sequence such as time.
A.f1: Line graphs are best when you want to show how the value of something changes over time, or compare how several things change over time relative to each other.   [sources: swd_what_is_a_line_graph]
A.f2: plt.plot(x, y) plots the y-values against the given x-values.   [sources: matplotlib_pyplot_tutorial#Introduction to pyplot]
A.f3: A line graph plots the measured points and then draws a line that connects those points, making it easier to see how the values rose, fell, or stayed the same over time.   [sources: swd_what_is_a_line_graph]
PRACTICE ANCHOR (live_code): Given two Python lists — one holding day labels (or integers representing days) and one holding a numeric value for each day — call plt.plot() to produce a line chart that shows how the value changes across the days.  SUCCESS: Running the cell produces a line chart with the day values on the x-axis and the numeric values on the y-axis, connected by a line that makes the day-to-day rise and fall visible.
ASSESSMENT ANCHOR: identify_line_plot_appropriate_use_case facts=['f1']
ASSESSMENT ANCHOR: call_plt_plot_with_x_and_y_arguments facts=['f2']
ASSESSMENT ANCHOR: explain_how_connecting_line_reveals_trend facts=['f3']
ASSESSMENT ANCHOR: build_line_plot_for_time_ordered_numeric_data facts=['f1', 'f2', 'f3']

## SOURCE FACTS — B (viz.scatter_plots)   objective: Create a scatter plot with matplotlib to visualize the relationship between two numeric variables.
B.f1: plt.scatter(x, y) (or ax.scatter(x, y)) makes a scatter plot of the y-values against the x-values, one point per (x, y) pair.   [sources: matplotlib_official_docs#matplotlib.pyplot.scatter]
B.f2: A scatterplot shows the relationship between two numerical variables plotted simultaneously along the horizontal and vertical axis, and is useful for focusing on the relationship between two series.   [sources: swd_what_is_a_scatterplot]
PRACTICE ANCHOR (live_code): Given the orders DataFrame with columns distance_km and delivery_time_minutes, produce a scatter plot and describe the apparent relationship between the two variables.  SUCCESS: A scatter plot appears with one point per row of orders; the learner states whether the points suggest a positive, negative, or no relationship between distance and delivery time.
ASSESSMENT ANCHOR: build_scatter_plot_from_two_numeric_columns facts=['f1', 'f2']

## SOURCE FACTS — C (viz.box_plots)   objective: Create a box plot with matplotlib to visualize a numeric variable's quartiles, median, and outliers, optionally comparing several groups.
C.f1: plt.boxplot(x) (or ax.boxplot(x)) draws a box plot from the data in x; it accepts array-like data and can draw one or more boxes.   [sources: matplotlib_official_docs#matplotlib.pyplot.boxplot]
C.f2: The box extends from the first quartile (Q1) to the third quartile (Q3) of the data, with a line at the median. The whiskers extend from the box to the farthest data point lying within 1.5x the interquartile range (IQR) from the box; points past the end of the whiskers are flier points (outliers).   [sources: matplotlib_official_docs#matplotlib.pyplot.boxplot]
C.f3: Boxplots offer a condensed display for comparing the distributions of multiple datasets side by side.   [sources: swd_what_is_a_boxplot]
C.f4: Passing a sequence of 1D arrays as x draws one box for each array in the sequence; tick_labels=[...] labels each boxplot's tick accordingly instead of leaving it as a numeric value.   [sources: matplotlib_official_docs#matplotlib.pyplot.boxplot]
PRACTICE ANCHOR (live_code): Given a DataFrame with a numeric column and a categorical column, extract one 1D array per category and pass them as a sequence to plt.boxplot(), using tick_labels to name each box.  SUCCESS: A figure appears showing one labeled box per category, each correctly reflecting that category's distribution with a visible median line, box, whiskers, and any flier points.
ASSESSMENT ANCHOR: call_boxplot_function_with_array_like_data facts=['f1']
ASSESSMENT ANCHOR: identify_box_whisker_and_flier_anatomy facts=['f2']
ASSESSMENT ANCHOR: apply_iqr_rule_to_determine_whisker_extent_and_outliers facts=['f2']
ASSESSMENT ANCHOR: explain_box_plot_value_for_comparing_multiple_distributions facts=['f3']
ASSESSMENT ANCHOR: draw_grouped_box_plot_with_labeled_ticks_from_sequence_of_arrays facts=['f4']

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
img.boxplot_anatomy: MISSING

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Anticipating stakeholder questions and objections; Basic A/B test structure (control vs treatment group); Box plots; Conceptual effect of sample size on confidence; Conceptual interpretation of statistical significance/confidence level; Converting a vague business question into a specific, measurable analytical question; Custom styling/theming (advanced/optional); Drawing a business conclusion from an experiment-result summary; Framing an actionable recommendation that is distinct from the finding itself; Identifying stakeholder needs/requirements before analysis; Identifying the business decision a stakeholder needs the analysis to inform; Interpreting lift/percentage change between groups; Labeling axes, titles, and legends; Making a data-driven recommendation; Matching chart type to the analytical question; Matching chart type to the specific point being made (trend vs. comparison vs. distribution vs. part-to-whole); Multi-panel figures/subplots (advanced/optional); Plotting directly from pandas DataFrames with seaborn; Prioritizing findings by relevance to the stakeholder's specific decision, not by analytical interestingness; Scatter plots; Simplifying a technical chart for a 

## LESSON, in learner order

### s01 · explainer · Tracking Trends Over Time with a Line Plot  [reward 5]
line plots — A line plot connects measured points in order — making rises and falls in the data immediately visible.
(intro) Suppose you have this week's average Lagos delivery time for each of 5 days and want to see whether it is getting better or worse. Line graphs are best when you want to show how the value of something changes over time, or compare how several things change over time relative to each other. ⟦A.f1 A:tb1⟧
(mechanism) A line graph plots the measured points and then draws a line that connects those points, making it easier to see how the values rose, fell, or stayed the same over time. ⟦A.f3 A:tb2⟧
(syntax) `plt.plot(x, y)` plots the y-values against the given x-values. `plt.plot([1, 2, 3, 4, 5], [21, 23, 19, 25, 20])` plots 5 days of average Lagos delivery times, with the connecting line making the day-to-day rise and fall immediately readable. ⟦A.f2 A:tb3⟧
[CHART line: Average Lagos Delivery Time — Days 1–5] data=ds.daily_averages x=day y=lagos_avg color=None annotations=[] alt: A line chart of 5 days of Lagos average delivery times (21, 23, 19, 25, 20 minutes). The connected line makes the day-to-day rise and fall immediately readable.

### s02 · video · Line Plots: Connecting Points to Reveal Trends  [reward 5]
watch — 
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · What the Connecting Line Adds  [reward 10]
quick check — Why does a line graph draw a line through the measured points?

### s04 · hands_on · Plot Lagos Delivery Trends with plt.plot()  [reward 15]
hands-on — Call plt.plot() with a list of days and a list of average delivery times to draw a line chart.

### s05 · explainer · Exploring Relationships with a Scatter Plot  [reward 5]
scatter plots — A scatter plot places one point per (x, y) pair — making the relationship between two numeric variables visible at a glance.
(intro) Suppose you want to see whether delivery distance and delivery time move together across your orders. A scatterplot shows the relationship between two numerical variables plotted simultaneously along the horizontal and vertical axis, and is useful for focusing on the relationship between two series. ⟦B.f2 B:tb1⟧
(syntax) `plt.scatter(x, y)` (or `ax.scatter(x, y)`) makes a scatter plot of the y-values against the x-values, one point per (x, y) pair. `plt.scatter(orders['distance_km'], orders['delivery_time_minutes'])` plots one point per order, with distance on the x-axis and delivery time on the y-axis. ⟦B.f1 B:tb2⟧
[CHART scatter: Distance vs Delivery Time — QuickDeliver Orders] data=ds.orders x=distance_km y=delivery_time_minutes color=None annotations=[] alt: A scatter plot of distance_km on the x-axis versus delivery_time_minutes on the y-axis, one point per order. Points trend upward, showing that longer distances tend to take more time.

### s06 · video · Scatter Plots: One Point per Pair  [reward 5]
watch — 
[VIDEO ] bridge-before:  | bridge-after: 

### s07 · check · Scatter Plot Basics  [reward 10]
quick check — What does each point in a scatter plot represent?

### s08 · hands_on · Plot Distance vs Delivery Time  [reward 15]
hands-on — Use plt.scatter() to plot distance_km against delivery_time_minutes from the orders dataset.

### s09 · explainer · Reading a Box Plot  [reward 5]
box plots — Every part of a box plot has a name — learn to read the box, whiskers, and flier points.
(intro) Boxplots offer a condensed display for comparing the distributions of multiple datasets side by side — showing spread, median, and outliers in a single compact shape. ⟦C.f3 C:tb1⟧
[ANNOTATED_IMAGE — unrendered type, raw] {"type":"annotated_image","block_id":"tile_viz_line_scatter_box.s09.b02","asset_id":"img.boxplot_anatomy","alt_text":"A box plot with labelled parts: Q1 at the bottom of the box, median as a line inside the box, Q3 at the top of the box, IQR as the box height, upper and lower whiskers extending to the farthest in-range points, and a flier point above the upper whisker.","hotspots":[{"x":0.5,"y":0.25,"w":0.15,"h":0.05,"label":"Q1 (first quartile)","detail":"Bottom edge of the box"},{"x":0.5,"y":0.5,"w":0.15,"h":0.05,"label":"Median","detail":"Line inside the box"},{"x":0.5,"y":0.75,"w":0.15,"h":0.05,"label":"Q3 (third quartile)","detail":"Top edge of the box"},{"x":0.5,"y":0.12,"w":0.12,"h":0.04,"label":"Lower whisker","detail":"Farthest point within 1.5×IQR below Q1"},{"x":0.5,"y":0.88,"w":0.12,"h":0.04,"label":"Upper whisker","detail":"Farthest point within 1.5×IQR above Q3"},{"x":0.5,"y":0.97,"w":0.08,"h":0.03,"label":"Flier point (outlier)","detail":"Point beyond the whisker end"}],"lineage":{"concept_ids":["viz.box_plots"],"teaching_block_ids":["viz.box_plots#tb1"],"fact_ids":["viz.box_plots#f3"],"anchors":["viz.box_plots#visual"]}}

### s10 · explainer · The Box, Whiskers, and Flier Points  [reward 5]
box plots — The box spans Q1 to Q3; whiskers reach 1.5×IQR beyond the box; anything further is a flier.
(mechanism) `plt.boxplot(x)` (or `ax.boxplot(x)`) draws a box plot from the data in x; it accepts array-like data and can draw one or more boxes. The box extends from Q1 to Q3, with a line at the median. The whiskers extend to the farthest data point lying within 1.5× the IQR from the box; points past the whisker ends are flier points (outliers). ⟦C.f1 C.f2 C:tb2⟧
(example) If Lagos's box runs from Q1 = 20 to Q3 = 30 minutes, the IQR is 10 minutes. The whiskers can reach at most 1.5 × 10 = 15 minutes beyond the box — no lower than 5 minutes and no higher than 45 minutes — so a 50-minute Lagos delivery would be drawn as a separate flier point. ⟦C.f2 C:tb2⟧

### s11 · video · Box Plots: Distribution and Outliers  [reward 5]
watch — 
[VIDEO ] bridge-before:  | bridge-after: 

### s12 · explainer · Comparing Multiple Cities Side by Side  [reward 5]
box plots — Pass a sequence of arrays to draw one box per group, and use tick_labels to name each box.
(syntax) Passing a sequence of 1D arrays as x draws one box for each array in the sequence; `tick_labels=[...]` labels each boxplot's tick accordingly instead of leaving it as a numeric value. `plt.boxplot([lagos_times, abuja_times, kano_times], tick_labels=['Lagos', 'Abuja', 'Kano'])` draws three boxes side by side, each labeled with its city name. ⟦C.f4 C:tb3⟧

### s13 · check · Box Plot Anatomy  [reward 10]
quick check — What do the edges of the box represent?

### s14 · check · When to Use a Box Plot  [reward 10]
quick check — What is a box plot's main advantage over a bar chart for delivery-time data?

### s15 · hands_on · Compare City Delivery Spreads with plt.boxplot()  [reward 15]
hands-on — Filter the orders dataset by city, then pass the three arrays to plt.boxplot() with tick_labels.

### s16 · recap · Line, Scatter, and Box Plots: What You Learned  [reward 10]
recap — Three chart types for three different questions about numeric data.
(takeaway) Use `plt.plot(x, y)` to show how a value changes over time. Use `plt.scatter(x, y)` to explore the relationship between two numeric variables. Use `plt.boxplot(x)` to compare the full spread — median, quartiles, and outliers — across multiple groups.
[UP NEXT] Up next: Labeling Charts and Choosing Chart Types: Next you'll add titles, axis labels, and legends to make charts self-explanatory, then learn a decision framework for choosing the right chart type for any question.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · The Connecting Line Reveals the Trend — Without the line, you see points; with it, you see the direction of change.
(mechanism) A line graph plots the measured points and then draws a line that connects those points, making it easier to see how the values rose, fell, or stayed the same over time. The line between day 2 (23 min) and day 3 (19 min) slopes downward — showing improvement — in a way that a list of numbers does not. ⟦A.f3 A:tb2⟧
### r02 · Scatter Plots Show Relationships Between Two Variables — Each point encodes one (x, y) pair — the pattern of points reveals whether the two variables move together.
(definition) A scatterplot shows the relationship between two numerical variables plotted simultaneously along the horizontal and vertical axis. `plt.scatter(orders['distance_km'], orders['delivery_time_minutes'])` places one point per order — if longer distances consistently produce longer times, the points will trend upward from left to right. ⟦B.f1 B.f2 B:tb1 B:tb2⟧
### r03 · The Box Spans Q1 to Q3 — The box edges mark the first and third quartiles; the line inside marks the median.
(mechanism) The box extends from the first quartile (Q1) to the third quartile (Q3) of the data, with a line at the median. The whiskers extend to the farthest data point lying within 1.5× the IQR from the box; points past the whisker ends are flier points (outliers). ⟦C.f2 C:tb2⟧
### r04 · Box Plots Compare Distributions, Not Just Averages — A box plot shows spread, median, and outliers — a bar chart shows only a single summary value per group.
(definition) Boxplots offer a condensed display for comparing the distributions of multiple datasets side by side. Unlike a bar chart that shows only the average per city, a box plot shows how spread out the delivery times are, where the middle half falls, and whether any deliveries are unusually slow. ⟦C.f3 C:tb1⟧

## OTHER CONTENT (fields without a dedicated renderer)
· y.title: Avg delivery time (min)

=========

# EVALUATOR PACKET — Labeling Charts and Selecting Chart Types (tile_viz_labeling_chart_selection)
Tile summary: Add titles, axis labels, and legends with ax.set_xlabel/ylabel/title and ax.legend(), then choose the right chart type by matching it to the analytical question.
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
ds.chart_selection_mini: QuickDeliver chart-selection mini dataset — columns: distance_km(numerical), delivery_minutes(numerical)
   [1.2,14]
   [2.5,21]
   [3.8,28]
   [4.1,31]
   [5.6,38]
   [6.3,44]
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

### s01 · explainer · Titles, Axis Labels, and Legends  [reward 5]
chart labeling — A chart without labels forces the reader to guess — three method calls make it self-explanatory.
(intro) Titles, axis labels, and legends are the text that tells a reader what a plot shows. Matplotlib gives two parallel ways to add them, depending on whether you are working with an Axes object or the pyplot interface directly. ⟦A:tb1⟧
(syntax) `ax.set_xlabel('...')` and `ax.set_ylabel('...')` set the x-axis and y-axis labels, and `ax.set_title('...')` sets the Axes title. `ax.set_xlabel('Day')`, `ax.set_ylabel('Average delivery time (minutes)')`, and `ax.set_title('Average delivery time by day')` label the Lagos trend line. ⟦A.f1 A:tb2⟧
(syntax) Passing `label='...'` to a plotting call and then calling `ax.legend()` displays a legend identifying each labeled series. `ax.plot(days, lagos_avg, label='Lagos')` followed by `ax.legend()` shows a legend identifying the Lagos line — which matters once a second city's line is added. ⟦A.f2 A:tb3⟧
[BEFORE_AFTER] Adding set_xlabel, set_ylabel, set_title, and legend turns an unlabeled plot into a self-explanatory chart.
  before:
[CODE python]
fig, ax = plt.subplots()
ax.plot(days, lagos_avg)
  annotations: ['No labels — the reader cannot tell what the axes or line represent']
  after:
[CODE python]
fig, ax = plt.subplots()
ax.plot(days, lagos_avg, label='Lagos')
ax.set_xlabel('Day')
ax.set_ylabel('Average delivery time (minutes)')
ax.set_title('Average delivery time by day')
ax.legend()
  annotations: ["label='Lagos' names this series for the legend", 'ax.set_xlabel() labels the x-axis', 'ax.set_ylabel() labels the y-axis', 'ax.set_title() sets the Axes title', 'ax.legend() displays the legend for all labeled series']

### s02 · explainer · The pyplot Shorthand  [reward 5]
chart labeling — plt.xlabel(), plt.ylabel(), and plt.title() do the same job as the Axes methods.
(syntax) In the pyplot interface, `plt.xlabel()`, `plt.ylabel()`, and `plt.title()` set the same label/title elements on the current Axes — the pyplot equivalents of `ax.set_xlabel()`, `ax.set_ylabel()`, and `ax.set_title()`. ⟦A.f3 A:tb4⟧

### s03 · check · Axes Labeling Methods  [reward 10]
quick check — Which three method calls add a title and both axis labels to an Axes object?

### s04 · check · pyplot vs Axes Interface  [reward 10]
quick check — What is the pyplot equivalent of ax.set_title()?

### s05 · hands_on · Label a Two-Series Line Chart  [reward 15]
hands-on — Add a title, both axis labels, and a legend that distinguishes the Lagos and Abuja lines.

### s06 · explainer · Choosing the Right Chart for Your Question  [reward 5]
chart selection — The chart type follows from the analytical question — name what you're asking before you plot.
(definition) Use a bar chart to compare a numeric value across discrete categories. Use a histogram to see how a numeric variable is distributed. Use a line graph to show how a value changes over time. Use a scatter plot to explore the relationship between two numeric variables. ⟦B.f1 B.f2 B.f3 B.f4 B:tb1⟧
(definition) Use a box plot to compare the full spread — median, quartiles, and outliers — of a numeric variable across several groups side by side. ⟦B.f5 B:tb2⟧
[SIDE_BY_SIDE] The same delivery dataset rendered two ways — the question you ask determines which chart fits. left_label: Scatter: relationship between two numeric variables | right_label: Bar: numeric value compared across categories
  left:
[CHART scatter: Scatter: distance vs delivery time] data=ds.chart_selection_mini x=distance_km y=delivery_minutes color=None annotations=[] alt: A scatter plot of distance_km vs delivery_minutes showing a positive relationship between the two variables.
  right:
[CHART bar: Bar: average delivery time by city] data=ds.orders x=city y=delivery_time_minutes color=None annotations=[] alt: A bar chart showing average delivery_time_minutes for Lagos, Abuja, and Kano side by side.

### s07 · video · Chart Selection: Boxplot Fitness and Histogram Construction  [reward 5]
watch — 
[VIDEO ] bridge-before:  | bridge-after: 

### s08 · check · Match the Question to the Chart  [reward 10]
quick check — For each analytical question, choose the chart type that fits best.

### s09 · check · Line Graph or Box Plot?  [reward 10]
quick check — Which chart type shows how a value changes over time, and which compares spread across groups?

### s10 · hands_on · Choose and Build the Right Chart  [reward 15]
hands-on — Given a question about whether longer distances lead to longer delivery times, choose the right chart type and build it.

### s11 · recap · Labeling and Chart Selection: What You Learned  [reward 10]
recap — Labels make charts readable; the right chart type makes the answer visible.
(takeaway) Add `ax.set_xlabel()`, `ax.set_ylabel()`, and `ax.set_title()` to label every chart. Use `label='...'` plus `ax.legend()` when a chart has more than one series. Choose the chart type by naming the question: category comparison → bar; distribution → histogram; trend over time → line; relationship between two variables → scatter; spread across groups → box plot. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb3⟧
[UP NEXT] Up next: Seaborn — DataFrame Plotting, Stats, and Themes: Next you'll use seaborn's dataframe-aware plotting functions, add automatic statistical estimates with sns.regplot(), and apply themes and palettes with sns.set_theme().

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Three Calls to Label an Axes — ax.set_xlabel(), ax.set_ylabel(), and ax.set_title() are the three Axes labeling methods.
(syntax) `ax.set_xlabel('...')` and `ax.set_ylabel('...')` set the x-axis and y-axis labels, and `ax.set_title('...')` sets the Axes title. All three take a string argument — for example `ax.set_xlabel('Day')` labels the x-axis with the word 'Day'. ⟦A.f1 A:tb2⟧
### r02 · pyplot Labeling Functions — plt.xlabel(), plt.ylabel(), and plt.title() are the pyplot equivalents of the Axes methods.
(syntax) In the pyplot interface, `plt.xlabel()`, `plt.ylabel()`, and `plt.title()` set the same label/title elements on the current Axes — the pyplot equivalents of `ax.set_xlabel()`, `ax.set_ylabel()`, and `ax.set_title()`. ⟦A.f3 A:tb4⟧
### r03 · Five Chart Types, Five Questions — Each chart type answers a different analytical question — match the question to the chart.
(definition) Bar chart: compare a numeric value across discrete categories. Histogram: see how a numeric variable is distributed. Line graph: show how a value changes over time. Scatter plot: explore the relationship between two numeric variables. Box plot: compare the full spread across several groups. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb1 B:tb2⟧
### r04 · Line Graph vs Box Plot — A line graph tracks change over time; a box plot compares spread across groups.
(definition) A line graph is best when you want to show how the value of something changes over time. A box plot offers a condensed display for comparing the distributions of multiple datasets side by side — showing spread, median, and outliers per group, not a trend over time. ⟦B.f3 B.f5 B:tb1⟧

## OTHER CONTENT (fields without a dedicated renderer)
· y.title: Avg delivery time (min)

=========

# EVALUATOR PACKET — Seaborn: DataFrame Plotting, Statistical Functions, and Themes (tile_viz_seaborn_stats_themes)
Tile summary: Use seaborn's dataframe-aware plotting functions, add automatic statistical estimates with sns.regplot(), and apply themes and palettes with sns.set_theme().
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

### s01 · explainer · Plotting Directly from a DataFrame with Seaborn  [reward 5]
seaborn — Seaborn's functions take column names instead of extracted arrays — less code, same chart.
(intro) Most matplotlib calls so far have needed you to pull a column out of `orders` yourself before plotting it. Seaborn's plotting functions operate on dataframes and arrays containing whole datasets, taking only the names of the variables and their roles in the plot (for example `data=`, `x=`, `y=`) rather than requiring the caller to extract each array. ⟦A.f1 A:tb1⟧
(syntax) `seaborn.barplot(data=..., x=..., y=...)` visualizes an aggregate statistical estimate for each category as a bar; its default estimator is the mean, and it draws an error bar (uncertainty indicator) around each bar by default. `sns.barplot(data=orders, x='city', y='delivery_time_minutes')` produces a per-city mean bar chart without a groupby call. ⟦A.f2 A:tb2⟧
[CHART bar: Average Delivery Time by City — seaborn barplot] data=ds.orders x=city y=delivery_time_minutes color=None annotations=[] alt: A seaborn barplot showing the mean delivery_time_minutes for Lagos, Abuja, and Kano, with error bars indicating uncertainty around each mean.

### s02 · check · Seaborn's DataFrame Interface  [reward 10]
quick check — How does sns.barplot() differ from plt.bar() in how it receives data?

### s03 · hands_on · Build a Seaborn Bar Chart from a DataFrame  [reward 15]
hands-on — Call sns.barplot() with data=orders and column names for x and y — no groupby needed.

### s04 · explainer · Automatic Statistical Estimates with Seaborn  [reward 5]
seaborn — Many seaborn functions compute a statistical estimate for you — sns.regplot() adds a fitted regression line to a scatter plot.
(definition) Many seaborn functions will automatically perform the statistical estimation necessary to answer questions such as the average value of one variable as a function of other variables. `sns.barplot()` already does this — it computes the mean per category without a groupby call. ⟦B.f1 B:tb1⟧
(syntax) `seaborn.regplot(data=..., x=..., y=...)` plots a scatterplot of the observations together with a fitted linear regression line. `sns.regplot(data=orders, x='distance_km', y='delivery_time_minutes')` draws each order as a point and overlays the best-fit line through those points. ⟦B.f2 B:tb2⟧
[BEFORE_AFTER] sns.regplot() adds a fitted regression line to the scatter plot, making the statistical relationship visible.
  before:
[CHART scatter: Scatter: distance vs delivery time (no trend line)] data=ds.orders x=distance_km y=delivery_time_minutes color=None annotations=[] alt: A plain scatter plot of distance_km vs delivery_time_minutes with no regression line.
  after:
[CHART scatter: regplot: scatter + fitted regression line] data=ds.orders x=distance_km y=delivery_time_minutes color=None annotations=[] alt: The same scatter plot of distance_km vs delivery_time_minutes with a fitted linear regression line added by sns.regplot().

### s05 · check · Seaborn's Automatic Estimation  [reward 10]
quick check — What does seaborn do automatically that you would otherwise have to compute yourself?

### s06 · check · Choosing the Right Seaborn Function  [reward 10]
quick check — Which seaborn function adds a fitted regression line to a scatter plot?

### s07 · hands_on · Add a Regression Line with sns.regplot()  [reward 15]
hands-on — Call sns.regplot() with data=orders and column names to produce a scatter plot with a fitted trend line.

### s08 · explainer · Applying Themes and Palettes with sns.set_theme()  [reward 5]
seaborn themes — One call before your plot changes the background, gridlines, and colors for every chart that follows.
(syntax) `seaborn.set_theme()` accepts a `style` parameter (default `'darkgrid'`) and a `palette` parameter (default `'deep'`) among its arguments, which set the plot's background/gridline style and its color palette respectively. `sns.set_theme(style='whitegrid', palette='deep')` switches to a white background with gridlines. ⟦C.f2 C:tb1⟧
(mechanism) `sns.set_theme(style=..., palette=...)` changes the global defaults for all plots using the matplotlib rcParams system, so it affects matplotlib plots too, even ones not made with seaborn. Calling `sns.set_theme()` changes how plots drawn after that call look — it does not restyle a figure you already drew and displayed. ⟦C.f1 C:tb2⟧
[BEFORE_AFTER] sns.set_theme(style='whitegrid', palette='deep') changes the background, gridlines, and colors for all subsequent plots.
  before:
[CHART bar: Default matplotlib styling] data=ds.theming_demo x=category y=value color=None annotations=[] alt: A seaborn barplot of category vs value rendered with default matplotlib styling — grey background, no gridlines.
  after:
[CHART bar: After sns.set_theme(style='whitegrid', palette='deep')] data=ds.theming_demo x=category y=value color=None annotations=[] alt: The same seaborn barplot after calling sns.set_theme(style='whitegrid', palette='deep') — white background with gridlines and the 'deep' color palette.

### s09 · check · Global Effect of sns.set_theme()  [reward 10]
quick check — Why does sns.set_theme() affect matplotlib plots that were not made with seaborn?

### s10 · hands_on · Apply a Theme and Palette with sns.set_theme()  [reward 15]
hands-on — Call sns.set_theme() with a named style and palette before drawing a seaborn plot.

### s11 · recap · Seaborn: What You Learned  [reward 10]
recap — Seaborn plots from DataFrames, computes statistics automatically, and applies themes globally.
(takeaway) Use `sns.barplot(data=..., x=..., y=...)` to plot directly from a DataFrame without extracting columns. Use `sns.regplot(data=..., x=..., y=...)` to add a fitted regression line to a scatter plot. Call `sns.set_theme(style=..., palette=...)` before plotting to apply a consistent visual style to all subsequent charts.
[UP NEXT] Up next: Custom Styling and Multi-Panel Figures: Next you'll apply matplotlib style sheets and rcParams for custom branding, and use plt.subplots(nrows, ncols) to arrange multiple charts in a single figure.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Seaborn Takes Column Names, Not Arrays — Pass the DataFrame and column names — seaborn extracts the data for you.
(definition) Seaborn's plotting functions operate on dataframes and arrays containing whole datasets, taking only the names of the variables and their roles in the plot (`data=`, `x=`, `y=`) rather than requiring the caller to extract each array. `sns.barplot(data=orders, x='city', y='delivery_time_minutes')` produces a per-city mean bar chart without a groupby call. ⟦A.f1 A.f2 A:tb1 A:tb2⟧
### r02 · Seaborn Computes Statistics Automatically — You don't need to compute the mean or fit a regression line yourself — seaborn does it.
(definition) Many seaborn functions will automatically perform the statistical estimation necessary to answer questions such as the average value of one variable as a function of other variables. `sns.barplot()` computes the mean per category; `sns.regplot()` fits a linear regression line through the scatter points — both without any manual calculation. ⟦B.f1 B:tb1⟧
### r03 · sns.set_theme() Changes Global rcParams — It works by changing matplotlib's global defaults — so it affects every plot drawn after the call.
(mechanism) `sns.set_theme(style=..., palette=...)` changes the global defaults for all plots using the matplotlib rcParams system, so it affects matplotlib plots too, even ones not made with seaborn. Because it works by changing global defaults, calling `sns.set_theme()` changes how plots drawn after that call look — it does not go back and restyle a figure you already drew and displayed earlier. ⟦C.f1 C:tb2⟧

## OTHER CONTENT (fields without a dedicated renderer)
· y.title: Avg delivery time (min)
· y.title: Avg delivery time (min)
· y.title: Avg delivery time (min)

=========

# EVALUATOR PACKET — Custom Styling and Multi-Panel Figures (tile_viz_custom_multi_panel)
Tile summary: Apply matplotlib style sheets and rcParams for custom branding, use sns.set_palette() for color schemes, and arrange multiple charts with plt.subplots(nrows, ncols).
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

### s01 · explainer · Style Sheets, rcParams, and Seaborn Palettes  [reward 5]
custom styling — Three tools let you control the visual appearance of every chart: style sheets, rcParams, and seaborn palettes.
(syntax) `plt.style.use('style-name')` applies one of matplotlib's predefined style sheets — for example `'ggplot'` or `'dark_background'`. The available styles can be listed with `plt.style.available`. ⟦A.f1 A:tb1⟧
(mechanism) A custom style file can set specific properties such as `'axes.titlesize'`, `'lines.linewidth'`, or tick label sizes, and rcParams can be set directly to change defaults globally. After `import matplotlib as mpl`, `mpl.rcParams['lines.linewidth'] = 2` sets the default line width for every plot drawn after that call. ⟦A.f2 A:tb2⟧
(syntax) `seaborn.set_palette(palette, ...)` sets the matplotlib color cycle from a seaborn palette, applying that color scheme to subsequent plots. `sns.set_palette('pastel')` switches later plots to seaborn's pastel color scheme. ⟦A.f3 A:tb3⟧
[BEFORE_AFTER] plt.style.use('ggplot') and mpl.rcParams['lines.linewidth'] = 2 change the chart's appearance globally.
  before:
[CODE python]
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot(days, lagos_avg)
  annotations: ['Default matplotlib style — grey background, thin lines']
  after:
[CODE python]
import matplotlib.pyplot as plt
import matplotlib as mpl
plt.style.use('ggplot')
mpl.rcParams['lines.linewidth'] = 2
fig, ax = plt.subplots()
ax.plot(days, lagos_avg)
  annotations: ["plt.style.use('ggplot') applies the ggplot style sheet", "mpl.rcParams['lines.linewidth'] = 2 sets the default line width globally"]

### s02 · check · Applying a Style Sheet  [reward 10]
quick check — Which call applies a predefined matplotlib style sheet?

### s03 · check · Three Ways to Style a Chart  [reward 10]
quick check — Match each styling tool to what it controls.

### s04 · hands_on · Apply rcParams and a Seaborn Palette  [reward 15]
hands-on — Set a line width with mpl.rcParams and apply a seaborn palette with sns.set_palette().

### s05 · explainer · Arranging Multiple Charts in One Figure  [reward 5]
multi-panel figures — plt.subplots(nrows, ncols) creates a grid of Axes — each panel is independent.
(intro) Suppose you want to show the delivery-time histogram and the distance/delivery-time scatter plot together, side by side, instead of as two separate figures. ⟦B:tb1⟧
(syntax) `fig, axs = plt.subplots(nrows, ncols)` creates a Figure containing a grid of Axes with the given number of rows and columns. `fig, axs = plt.subplots(2, 2)` creates one Figure holding four Axes arranged in two rows and two columns. ⟦B.f1 B:tb2⟧
(mechanism) Each Axes in the returned grid is indexed separately (for example `axs[0, 0]`) and plotting/labeling calls made on one Axes only affect that panel. `axs[0, 0].hist(orders['delivery_time_minutes'])` draws the histogram into the top-left panel, and `axs[0, 1].scatter(orders['distance_km'], orders['delivery_time_minutes'])` draws the scatter into the top-right panel without disturbing the first. ⟦B.f2 B:tb3⟧
[DIAGRAM: plt.subplots(2, 2) — four independent Axes in one Figure] nodes=['Figure', 'axs[0,0]\nhistogram', 'axs[0,1]\nscatter', 'axs[1,0]\nbar chart', 'axs[1,1]\nbox plot'] edges=[('fig_node', 'ax00', 'contains'), ('fig_node', 'ax01', 'contains'), ('fig_node', 'ax10', 'contains'), ('fig_node', 'ax11', 'contains')] alt: A 2×2 grid of panels inside one Figure. Each panel is labelled with its Axes index (axs[0,0] through axs[1,1]) and a chart type. Plotting on one panel does not affect the others.

### s06 · video · Multi-Panel Figures: Indexing and Independent Axes  [reward 5]
watch — 
[VIDEO ] bridge-before:  | bridge-after: 

### s07 · check · Indexing into the Axes Grid  [reward 10]
quick check — How do you plot on the top-right panel of a 2×2 subplot grid?

### s08 · hands_on · Build a Two-Panel Figure  [reward 15]
hands-on — Use plt.subplots(1, 2) to create two side-by-side panels, then plot a histogram and a scatter plot.

### s09 · recap · Custom Styling and Multi-Panel Figures: What You Learned  [reward 10]
recap — Style sheets and rcParams control appearance; plt.subplots(nrows, ncols) arranges multiple charts.
(takeaway) Use `plt.style.use('style-name')` to apply a predefined style sheet, `mpl.rcParams['property'] = value` to set individual defaults globally, and `sns.set_palette('palette-name')` to change the color cycle. Use `fig, axs = plt.subplots(nrows, ncols)` to create a grid of independent panels and index each one with `axs[row, col]`.
[UP NEXT] Up next: A/B Tests and Statistical Significance: Next you'll learn how to structure an A/B test, interpret lift, and decide whether an observed difference is statistically significant.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · plt.style.use() Applies a Style Sheet — Pass a style name as a string — the style is applied to all plots drawn after the call.
(syntax) `plt.style.use('style-name')` applies one of matplotlib's predefined style sheets — for example `'ggplot'` or `'dark_background'`. The available styles can be listed with `plt.style.available`. ⟦A.f1 A:tb1⟧
### r02 · Three Styling Tools and What They Control — Style sheets set a bundle of defaults; rcParams set individual properties; set_palette sets colors.
(definition) `plt.style.use('style-name')` applies a predefined bundle of style settings. `mpl.rcParams['lines.linewidth'] = 2` sets a single default property globally. `sns.set_palette('pastel')` sets the matplotlib color cycle from a seaborn palette, applying that color scheme to subsequent plots. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3⟧
### r03 · Each Panel Has Its Own Index — axs[row, col] selects one panel — calls on that Axes only affect that panel.
(mechanism) Each Axes in the returned grid is indexed separately (for example `axs[0, 0]`) and plotting/labeling calls made on one Axes only affect that panel. `axs[0, 1].scatter(orders['distance_km'], orders['delivery_time_minutes'])` draws the scatter into the top-right panel without disturbing the histogram in `axs[0, 0]`. ⟦B.f2 B:tb3⟧