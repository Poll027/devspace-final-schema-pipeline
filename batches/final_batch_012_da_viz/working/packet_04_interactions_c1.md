# EVALUATOR PACKET — Bar Charts and Histograms (tile_viz_bar_histograms)
Tile summary: Learn to compare categories with plt.bar() and reveal distributions with plt.hist(), understanding the zero-baseline rule and the bins parameter.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = viz.bar_charts — Bar charts
B = viz.histograms — Histograms

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: tile_viz_bar_histograms.s12: prose block without lineage.fact_ids

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
[VIDEO Building and reading bar charts: live code and the zero-baseline rule] bridge-before: The first clip shows plt.bar() with string category names as x; the second shows a real misleading chart — watch how the non-zero start distorts apparent differences between bars. | bridge-after: The first clip does not cover the zero-baseline rule or why bar lengths must be true to values; the teaching text fills both gaps.
  - k7UJg2E-TyU 0-144s facts=['f1', 'f2', 'f4'] label: Live demo: plotting categorical data with plt.bar() | summary: The instructor defines two parallel lists — food-group category names and daily-serving counts — then calls plt.bar(), passing the category names directly as the x argument and the counts as heights. The resulting chart appears with the category labels along the x-axis and bar heights reflecting each count, showing that string names work as x-positions without any numeric conversion.
  - dNVjFpHjbDs 70-134s facts=['f3'] label: Why a bar chart's baseline must be zero | summary: The instructor displays a bar chart whose y-axis starts at 350 rather than zero. Because readers judge bar charts by comparing bar heights from a shared baseline, the bars appear to show a three-to-four-times increase when the actual change is far smaller. Adding axis labels reveals the deception. The fix is stated plainly: always set the axis to zero.

### s03 · explainer · Why the Baseline Must Start at Zero  [reward 5]
bar charts — The bar chart's power comes from comparing lengths — and that only works when every bar starts at the same point.
(mental_model) Bar charts are easy to interpret because the eye is good at comparing lengths when the objects being compared are aligned to a common baseline. Every bar starts at 0, so a taller bar genuinely represents a larger value — Kano's bar looks taller than Lagos's because its average delivery time is higher. ⟦A.f3 A:tb3⟧
(misconception) Starting bars at a value other than 0 — say 20 minutes — distorts the comparison. If Kano averages 30 minutes and Lagos 25, bars starting at 20 are 10 and 5 units tall: Kano's bar looks twice as long even though its average is only 5 minutes higher. Keep the baseline at 0. ⟦A.f3 A.m1 A:tb4⟧

### s04 · check · When to Use a Bar Chart  [reward 10]
quick check — Which kind of data is a bar chart designed to compare?
QUESTION [choice, intro, grading=client] Which of the following datasets is a bar chart the right tool to visualise?
  ✔ opt_city: Average delivery time for each of three cities (Lagos, Abuja, Kano)
      why: Correct. A bar chart is a common chart type for graphing categorical data or data sorted into groups — here, the three cities are the categories and the bar heights show each city's average.
  ✘ opt_time: Daily average delivery time over five consecutive days
      why: Not quite. Daily averages over consecutive days form an ordered time series — a line plot is better suited to show how the value changes over time.
  ✘ opt_dist: The distribution of individual delivery times across all orders
      why: Not quite. Showing the distribution of a numeric variable across many values is what a histogram does — it bins the values and draws one bar per bin.
  ✘ opt_rel: The relationship between delivery distance and delivery time
      why: Not quite. Exploring the relationship between two numeric variables is what a scatter plot does — it places one point per (x, y) pair.
  feedback✔: Right. A bar chart is designed for categorical data — comparing a numeric value across discrete groups such as cities.  feedback✘: A bar chart is a common chart type for graphing categorical data or data sorted into groups. The three cities are categories, so a bar chart is the right choice for comparing their averages.  hints: ['Think about which dataset has discrete, named groups rather than a continuous numeric axis.', 'A bar chart compares a numeric value across categories — which option has categories?']  remediation→r01
  MEASURES: A:identify_bar_chart_as_categorical_comparison_tool(f2)   anchors=['assessment:identify_bar_chart_as_categorical_comparison_tool']
  taught-before-tested: A.f2←s01

### s05 · check · The Zero-Baseline Rule  [reward 10]
quick check — Why must a bar chart's baseline start at zero?
QUESTION [choice, core, grading=client] Kano averages 30 minutes and Lagos averages 25 minutes. A bar chart is drawn with the baseline starting at 20 minutes instead of 0. What is wrong with this chart?
  ✔ opt_distort: Kano's bar looks twice as long as Lagos's even though its average is only 5 minutes higher
      why: Correct. With a baseline at 20, Kano's bar is 10 units tall and Lagos's is 5 units tall — Kano looks twice as long even though its average is only 5 minutes higher. The eye compares bar lengths from the baseline, so the baseline must be 0.
  ✘ opt_fine: Nothing — starting at 20 makes the difference between cities easier to see
      why: Not quite. Starting at a non-zero baseline distorts the comparison. Bar charts are easy to read because the eye compares lengths from a common baseline — if that baseline is not 0, the lengths no longer truthfully represent the values.
  ✘ opt_missing: The chart is missing a title, which makes it unreadable
      why: Not quite. A missing title is a labeling issue, not a baseline issue. The real problem is that starting bars at 20 instead of 0 makes Kano's bar look twice as long as Lagos's, distorting the comparison.
  ✘ opt_wrong_type: Bar charts cannot display averages — only counts
      why: Not quite. Bar charts can display any numeric value per category, including averages. The problem here is the non-zero baseline, which distorts the visual comparison of bar lengths.
  feedback✔: Exactly. A non-zero baseline makes bar lengths misleading — Kano's bar looks twice as long as Lagos's even though the difference is only 5 minutes. Keep the baseline at 0.  feedback✘: Bar charts are easy to read because the eye compares lengths from a common baseline. If the baseline is not 0, the lengths distort the comparison. With a baseline at 20, Kano's bar (10 units) looks twice as long as Lagos's (5 units) even though the difference is only 5 minutes.  hints: ['Calculate the bar heights when the baseline is 20: Kano = 30 − 20 = ?, Lagos = 25 − 20 = ?', 'The eye compares bar *lengths* from the baseline — what happens to those lengths when the baseline shifts?']  remediation→r02
  MEASURES: A:explain_why_zero_baseline_is_required_for_valid_length_comparison(f3)   anchors=['assessment:explain_why_zero_baseline_is_required_for_valid_length_comparison']
  taught-before-tested: A.f3←s03

### s06 · hands_on · Plot City Averages with plt.bar()  [reward 15]
hands-on — Use groupby to compute per-city averages, then pass the city names and averages to plt.bar().
QUESTION [code_exercise, core, grading=client] The `orders` DataFrame is already loaded from `orders.csv`. It has columns `city` (Lagos, Abuja, Kano) and `delivery_time_minutes`.

Steps:
1. The mean delivery time per city is already computed: `df = orders.groupby('city')['delivery_time_minutes'].mean()`
2. Draw a bar chart: `plt.bar(df.index, df)`

The figure should show three bars — one per city — with city names on the x-axis and mean delivery times as bar heights, with the baseline at 0.
  runtime={'kind': 'chart_renderer', 'version': '0.29.5', 'packages': ['matplotlib', 'pandas']} constraints.allowed=['import matplotlib.pyplot as plt', "orders.groupby('city')['delivery_time_minutes'].mean()", 'plt.bar(city_avg.index, city_avg)', 'plt.show()', 'ax.bar(city_avg.index, city_avg)'] blocked=12 items
  file solution.py [editable]:
import matplotlib.pyplot as plt
import pandas as pd

orders = pd.read_csv('orders.csv')

# The mean delivery time per city is pre-computed for you
df = orders.groupby('city')['delivery_time_minutes'].mean()

# Call plt.bar() with city names as x and the averages as heights
# plt.bar(df.index, df)

  SOLUTION solution.py:
import matplotlib.pyplot as plt
import pandas as pd

orders = pd.read_csv('orders.csv')

# The mean delivery time per city is pre-computed for you
df = orders.groupby('city')['delivery_time_minutes'].mean()

plt.bar(df.index, df)

  test ix.tile_viz_bar_histograms.s06.t01 (figure_equals, visible=True): {"expected":{"n_axes":1,"chart_types":[["bar"]]}} | on-fail: Your figure should contain exactly one Axes with a bar chart. Call `plt.bar(df.index, df)`.
  test ix.tile_viz_bar_histograms.s06.t02 (axes_property, visible=True): {"property":"xticklabels","expected":["Abuja","Kano","Lagos"],"axes":0} | on-fail: The x-axis labels should be the city names ['Abuja', 'Kano', 'Lagos']. Pass `df.index` as the first argument to `plt.bar()`.
  test ix.tile_viz_bar_histograms.s06.t03 (plotted_data_equals, visible=True): {"chart":"bar","field":"heights","expected":[27.625,31.25,27.125],"series":0,"axes":0} | on-fail: The bar heights should be the per-city mean delivery times [27.625, 31.25, 27.125] for Abuja, Kano, and Lagos. Use `orders.groupby('city')['delivery_time_minutes'].mean()` to compute them.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"12635dd731c4bef135d71d0939f037d9c35b60c2df41dcdba37ce0e055c86802","tests_passed":3}
  feedback✔: Well done! `orders.groupby('city')['delivery_time_minutes'].mean()` computes the per-city averages, and `plt.bar(df.index, df)` draws a bar for each city with the correct height and a baseline at 0.  feedback✘: First compute the averages: `df = orders.groupby('city')['delivery_time_minutes'].mean()`. Then draw the chart: `plt.bar(df.index, df)`. Pass the city names (index) as x and the averages as heights.  hints: ["`orders.groupby('city')['delivery_time_minutes'].mean()` returns a Series with city names as the index.", 'Pass `df.index` as the first argument to `plt.bar()` and `df` as the second.']
  MEASURES: A:construct_bar_chart_with_plt_bar_using_categorical_x(f1,f4)   anchors=['practice', 'assessment:construct_bar_chart_with_plt_bar_using_categorical_x']
  taught-before-tested: A.f1←s01; A.f4←s01

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
plt.hist(orders['delivery_time_minutes'], bins=20)
  annotations: ['plt.hist bins the values and draws one bar per bin, revealing the distribution shape']

### s08 · video · Histograms: Binning and Distribution Shape  [reward 5]
watch — 
[VIDEO Binning data with plt.hist(): integer counts and explicit edges] bridge-before: Watch how the bar heights change when the bin count switches from an integer to an explicit edge list. The presenter calls the data 'ages'; Devspace's running example uses delivery_time_minutes. | bridge-after: The clip does not demonstrate the default of 10 bins or the 'auto' string strategy; the teaching text covers both. Key takeaway: bin choice directly controls what structure you see.
  - XDv6T4a0RNc 126-408s facts=['f1', 'f2'] label: plt.hist() with a bin count and with explicit bin edges | summary: Starting from the observation that plotting one bar per age would produce nearly a hundred columns, the presenter introduces histograms as a way to group values into bins. plt.hist() is called on a list of ages with bins=5, producing five equal-width bars whose heights show how many ages fall in each range. An edgecolor argument is added to make individual bins distinguishable. The presenter then replaces the integer with an explicit list [10, 20, 30, 40, 50, 60], showing that six edge values produce five bins with exact decade boundaries, and reads the per-bin counts aloud.

### s09 · check · How plt.hist() Works  [reward 10]
quick check — What does plt.hist() do with the values you pass it?
QUESTION [choice, core, grading=client] What does `plt.hist(orders['delivery_time_minutes'])` do internally before drawing the bars?
  ✔ opt_bin: Uses numpy.histogram to bin the values and count how many fall in each bin
      why: Correct. `plt.hist()` uses `numpy.histogram` to bin the data in x, count the number of values in each bin, and draw the result as bars — one bar per bin.
  ✘ opt_sort: Sorts the delivery times and draws one bar per unique value
      why: Not quite. `plt.hist()` groups values into bins (ranges), not one bar per unique value. Drawing one bar per unique value would produce too many bars for continuous data.
  ✘ opt_avg: Computes the average delivery time and draws a single bar
      why: Not quite. `plt.hist()` shows the distribution of all values, not a single summary. It bins the data and draws one bar per bin, showing how many values fall in each range.
  ✘ opt_scatter: Places one point per delivery time along the x-axis
      why: Not quite. Placing one point per value is what a scatter plot does. `plt.hist()` groups values into bins and draws one bar per bin, showing the count in each range.
  feedback✔: Right. `plt.hist()` uses `numpy.histogram` to bin the data and count values per bin, then draws one bar per bin — revealing the distribution shape.  feedback✘: `plt.hist(x, bins=...)` uses `numpy.histogram` to bin the data in x, count the number of values in each bin, and draw the result as bars.  hints: ['The fact says `plt.hist()` uses a specific numpy function — which one?', "Think about what 'binning' means: grouping values into ranges and counting how many fall in each."]  remediation→r03
  MEASURES: B:call_plt_hist_and_explain_binning_mechanism(f1)   anchors=['assessment:call_plt_hist_and_explain_binning_mechanism']
  taught-before-tested: B.f1←s07

### s10 · check · Controlling Bin Count  [reward 10]
quick check — What does passing an integer to the bins parameter do?
QUESTION [choice, core, grading=client] Which of the following is a valid way to call `plt.hist()` that sets explicit bin edges at 10, 20, 30, 40, and 50 minutes?
  ✔ opt_seq: `plt.hist(orders['delivery_time_minutes'], bins=[10, 20, 30, 40, 50])`
      why: Correct. Passing a sequence sets explicit bin edges — here the four bins are [10, 20), [20, 30), [30, 40), and [40, 50], exactly as specified.
  ✘ opt_int: `plt.hist(orders['delivery_time_minutes'], bins=4)`
      why: Not quite. Passing an integer sets that many *equal-width* bins — the edges are computed automatically from the data range, not set explicitly. To set explicit edges, pass a sequence.
  ✘ opt_auto: `plt.hist(orders['delivery_time_minutes'], bins='auto')`
      why: Not quite. Passing the string `'auto'` selects a binning strategy automatically — the edges are chosen by the algorithm, not set explicitly. To set explicit edges, pass a sequence.
  ✘ opt_default: `plt.hist(orders['delivery_time_minutes'])`
      why: Not quite. Calling `plt.hist()` without a `bins` argument uses the default of 10 equal-width bins. To set explicit bin edges, pass a sequence such as `[10, 20, 30, 40, 50]`.
  feedback✔: Exactly. Passing a sequence to `bins` sets explicit bin edges — the four bins are [10, 20), [20, 30), [30, 40), and [40, 50].  feedback✘: The `bins` parameter accepts three forms: an integer (equal-width bins), a sequence (explicit edges), or a string strategy such as `'auto'`. To set explicit edges at 10, 20, 30, 40, 50, pass a list.  hints: ['The question asks for *explicit* bin edges — which form of `bins` sets the edges directly?', 'An integer sets the *number* of bins; a sequence sets the *edges*.']  remediation→r04
  MEASURES: B:configure_bins_parameter_with_integer_sequence_or_string(f2)   anchors=['assessment:configure_bins_parameter_with_integer_sequence_or_string']
  taught-before-tested: B.f2←s07

### s11 · hands_on · Plot a Delivery-Time Histogram  [reward 15]
hands-on — Call plt.hist() on the delivery_time_minutes column and experiment with the bins parameter.
QUESTION [code_exercise, stretch, grading=client] The `orders` DataFrame is already loaded from `orders.csv`. It has a `delivery_time_minutes` column.

Call `plt.hist(orders['delivery_time_minutes'], bins=20)` to draw a histogram of delivery times with 20 equal-width bins.

The figure should show a histogram whose bar heights reflect the distribution of delivery times across all 24 orders.
  runtime={'kind': 'chart_renderer', 'version': '0.29.5', 'packages': ['matplotlib', 'pandas']} constraints.allowed=['plt.hist(series, bins=<int>)', 'plt.hist(series, bins=<list_of_edges>)', "plt.hist(series, bins='auto')", 'plt.hist(series)', 'plt.show()', 'orders["delivery_time_minutes"]'] blocked=9 items
  file solution.py [editable]:
import matplotlib.pyplot as plt
import pandas as pd

orders = pd.read_csv('orders.csv')

# Plot a histogram of delivery_time_minutes with a non-default bin count
# plt.hist(orders['delivery_time_minutes'], bins=...)

  SOLUTION solution.py:
import matplotlib.pyplot as plt
import pandas as pd

orders = pd.read_csv('orders.csv')

plt.hist(orders["delivery_time_minutes"], bins=20)

  test ix.tile_viz_bar_histograms.s11.t01 (figure_equals, visible=True): {"expected":{"n_axes":1,"chart_types":[["hist"]]}} | on-fail: Your figure should contain exactly one Axes with a histogram. Call `plt.hist(orders['delivery_time_minutes'], bins=<integer>)`.
  test ix.tile_viz_bar_histograms.s11.t02 (plotted_data_equals, visible=True): {"chart":"hist","field":"heights","expected":[2,0,1,2,1,4,5,2,3,1,1,1,0,0,0,0,0,0,0,1],"series":0,"axes":0} | on-fail: The bar heights should reflect the distribution of delivery_time_minutes with bins=20. Make sure you pass `orders['delivery_time_minutes']` to `plt.hist()` and set `bins=20`.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"2436980caf8503f5fa16a68e5495120058f17cea0963b16bf3e6dd5c8ce4be07","tests_passed":2}
  feedback✔: Well done! `plt.hist(orders['delivery_time_minutes'], bins=20)` bins the delivery times into 20 equal-width ranges and draws one bar per bin, revealing the distribution shape.  feedback✘: Call `plt.hist(orders['delivery_time_minutes'], bins=20)`. Pass the delivery_time_minutes column as the first argument and set `bins=20` to use 20 equal-width bins.  hints: ["`plt.hist()` takes the data column as the first argument: `orders['delivery_time_minutes']`.", 'Set `bins=20` to use 20 equal-width bins instead of the default 10.']
  MEASURES: B:call_plt_hist_and_explain_binning_mechanism(f1); B:configure_bins_parameter_with_integer_sequence_or_string(f2)   anchors=['practice', 'assessment:call_plt_hist_and_explain_binning_mechanism', 'assessment:configure_bins_parameter_with_integer_sequence_or_string']
  taught-before-tested: B.f1←s07; B.f2←s07

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

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: tile_viz_line_scatter_box.s16: prose block without lineage.fact_ids

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
[VIDEO Drawing a line plot: why the connecting line matters and how plt.plot() works] bridge-before: The first clip uses a bank loan example; the second uses age vs. salary. Watch how the connecting line — not just the dots — reveals the trend. Note: the second clip never calls this a 'line graph' by name. | bridge-after: The first clip does not show plt.plot() code (f2); the second clip does not state the line-graph definition (f1) or explain that points are connected to show rises and falls (f3). The teaching text covers all three facts.
  - Xhqj3gzn0gg 0-122s facts=['f1', 'f3'] label: Why a line graph is the right chart for showing how a value changes over time | summary: The presenter explains that line graphs are appropriate when the connecting lines between points make sense — most commonly for continuous data, and especially for time-based data such as days, months, quarters, or years. Using a bank's monthly loan origination volume as the example, the presenter builds the chart up period by period, narrating rises in Q1 driven by a mail campaign, a drop in Q2, a further dip in Q3 attributed to seasonal slowdown, and a forecast of recovery through year-end shown as a dotted line. The build-up illustrates how the connected line lets a viewer follow the story of what rose, fell, and why.
  - UO98lJQ3QGI 226-383s facts=['f2'] label: Coding plt.plot(x, y) to connect data points into a line | summary: The presenter creates two Python lists — dev_x holding age ranges from 25 to 35, and dev_y holding the corresponding median developer salaries — then calls plt.plot(dev_x, dev_y) followed by plt.show(). The resulting chart displays age on the x-axis and median salary on the y-axis, with a connected line that rises as age increases, showing that plt.plot() takes the x-values as the first argument and the y-values as the second.

### s03 · check · What the Connecting Line Adds  [reward 10]
quick check — Why does a line graph draw a line through the measured points?
QUESTION [choice, intro, grading=client] A line graph plots the measured points and then draws a line connecting them. What does the connecting line make easier to see?
  ✔ opt_trend: How the values rose, fell, or stayed the same over time
      why: Correct. The connecting line makes it easier to see how values rose, fell, or stayed the same over time — the slope between adjacent points shows the direction of change at a glance.
  ✘ opt_total: The total sum of all the measured values
      why: Not quite. The line connects measured points in order; it does not accumulate or sum them. A bar chart or a running total would show sums.
  ✘ opt_outlier: Which individual point is the highest outlier
      why: Not quite. The connecting line reveals the trend across all points, not just the highest one. Outliers are visible as individual points regardless of whether a line is drawn.
  ✘ opt_category: How many distinct categories the data contains
      why: Not quite. A line graph is for ordered numeric data over time, not for counting categories. A bar chart is the right tool for comparing discrete categories.
  feedback✔: Right. The line between adjacent points makes rises and falls immediately readable — that is the whole point of connecting them.  feedback✘: A line graph plots measured points and draws a line connecting them in order. That line makes it easier to see how values rose, fell, or stayed the same over time.  hints: ['Think about what you can read from the slope of the line between two adjacent points.', "The fact says the line makes it easier to see something 'over time' — what changes over time?"]  remediation→r01
  MEASURES: A:explain_how_connecting_line_reveals_trend(f3)   anchors=['assessment:explain_how_connecting_line_reveals_trend']
  taught-before-tested: A.f3←s01

### s04 · hands_on · Plot Lagos Delivery Trends with plt.plot()  [reward 15]
hands-on — Call plt.plot() with a list of days and a list of average delivery times to draw a line chart.
QUESTION [code_exercise, intro, grading=client] Two lists are already defined: `days = [1, 2, 3, 4, 5]` and `delivery_times = [21, 23, 19, 25, 20]` (Lagos average delivery times for days 1–5).

Call `plt.plot(days, delivery_times)` to draw a line chart that shows how the average delivery time changed across the five days.

The figure should contain one line with x-values from `days` and y-values from `delivery_times`.
  runtime={'kind': 'chart_renderer', 'version': '0.29.5', 'packages': ['matplotlib', 'pandas']} constraints.allowed=['plt.plot(x, y)', 'plt.show()', 'Python list literals', 'variable assignment', 'import matplotlib.pyplot as plt'] blocked=10 items
  file solution.py [editable]:
import matplotlib.pyplot as plt

# Data (these values will be changed by the grader to test your code)
day_1 = 1
days = [day_1, 2, 3, 4, 5]
dt_1 = 21
delivery_times = [dt_1, 23, 19, 25, 20]

# Call plt.plot(days, delivery_times) to draw a line chart of delivery times
# plt.plot(...)

  SOLUTION solution.py:
import matplotlib.pyplot as plt

# Data (these values will be changed by the grader to test your code)
day_1 = 1
days = [day_1, 2, 3, 4, 5]
dt_1 = 21
delivery_times = [dt_1, 23, 19, 25, 20]

plt.plot(days, delivery_times)

  test ix.tile_viz_line_scatter_box.s04.t01 (figure_equals, visible=True): {"expected":{"n_axes":1,"chart_types":[["line"]]}} | on-fail: Your figure should contain exactly one Axes with one line. Call `plt.plot(days, delivery_times)`.
  test ix.tile_viz_line_scatter_box.s04.t02 (plotted_data_equals, visible=True): {"chart":"line","field":"x","expected":[1,2,3,4,5],"series":0,"axes":0} | on-fail: The x-values of the line should be the `days` list [1, 2, 3, 4, 5]. Pass `days` as the first argument to `plt.plot()`.
  test ix.tile_viz_line_scatter_box.s04.t03 (plotted_data_equals, visible=True): {"chart":"line","field":"y","expected":[21,23,19,25,20],"series":0,"axes":0} | on-fail: The y-values of the line should be the `delivery_times` list. Pass `delivery_times` as the second argument to `plt.plot()`.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"2effb8e26519ac9ef637beeeeb3fc662cd6fed48a606543c01b811f14b6b7386","tests_passed":3}
  feedback✔: Well done! `plt.plot(days, delivery_times)` draws a line chart with the day numbers on the x-axis and the delivery times on the y-axis, making the day-to-day rise and fall immediately visible.  feedback✘: Call `plt.plot(days, delivery_times)` — pass `days` as the first argument (x-values) and `delivery_times` as the second argument (y-values).  hints: ['`plt.plot(x, y)` takes x-values first, then y-values. Pass `days` then `delivery_times`.', 'The starter already defines `days` and `delivery_times` — you just need to call `plt.plot()` with them.']
  MEASURES: A:identify_line_plot_appropriate_use_case(f1); A:call_plt_plot_with_x_and_y_arguments(f2); A:build_line_plot_for_time_ordered_numeric_data(f1,f2,f3)   anchors=['practice', 'assessment:identify_line_plot_appropriate_use_case', 'assessment:call_plt_plot_with_x_and_y_arguments', 'assessment:build_line_plot_for_time_ordered_numeric_data']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f1←s01; A.f2←s01; A.f3←s01

### s05 · explainer · Exploring Relationships with a Scatter Plot  [reward 5]
scatter plots — A scatter plot places one point per (x, y) pair — making the relationship between two numeric variables visible at a glance.
(intro) Suppose you want to see whether delivery distance and delivery time move together across your orders. A scatterplot shows the relationship between two numerical variables plotted simultaneously along the horizontal and vertical axis, and is useful for focusing on the relationship between two series. ⟦B.f2 B:tb1⟧
(syntax) `plt.scatter(x, y)` (or `ax.scatter(x, y)`) makes a scatter plot of the y-values against the x-values, one point per (x, y) pair. `plt.scatter(orders['distance_km'], orders['delivery_time_minutes'])` plots one point per order, with distance on the x-axis and delivery time on the y-axis. ⟦B.f1 B:tb2⟧
[CHART scatter: Distance vs Delivery Time — QuickDeliver Orders] data=ds.orders x=distance_km y=delivery_time_minutes color=None annotations=[] alt: A scatter plot of distance_km on the x-axis versus delivery_time_minutes on the y-axis, one point per order. Points trend upward, showing that longer distances tend to take more time.

### s06 · video · Scatter Plots: One Point per Pair  [reward 5]
watch — 
[VIDEO Scatter plots in action: one point per pair] bridge-before: Watch how a single plt.scatter(x, y) call places one point per pair. The data here is random; your running example uses meaningful columns. | bridge-after: The clip confirms the syntax and the 'one point per pair' mechanic. Devspace's text extends this to the delivery-distance/delivery-time example showing a real relationship.
  - zZZ_RCwp49g 120-180s facts=['f1', 'f2'] label: Building a scatter plot with plt.scatter(x, y) | summary: The instructor creates two lists of random values — one for each axis — then calls plt.scatter(x, y) to produce a scatter plot, with one point appearing per (x, y) pair. He notes that scatter plots are useful for spotting trends or outliers, and that this particular plot, because the data is random, shows no correlation between the two lists.

### s07 · check · Scatter Plot Basics  [reward 10]
quick check — What does each point in a scatter plot represent?
QUESTION [choice, core, grading=client] You have a DataFrame `orders` with columns `distance_km` and `delivery_time_minutes`. Which call produces a scatter plot with one point per order, distance on the x-axis, and delivery time on the y-axis?
  ✔ opt_scatter: `plt.scatter(orders['distance_km'], orders['delivery_time_minutes'])`
      why: Correct. `plt.scatter(x, y)` places one point per (x, y) pair, making the relationship between distance and delivery time visible across all orders.
  ✘ opt_plot: `plt.plot(orders['distance_km'], orders['delivery_time_minutes'])`
      why: Not quite. `plt.plot(x, y)` draws a line connecting the points in the order they appear — it is designed for ordered sequences such as time series, not for exploring the relationship between two unordered numeric variables.
  ✘ opt_bar: `plt.bar(orders['distance_km'], orders['delivery_time_minutes'])`
      why: Not quite. `plt.bar(x, height)` draws bars for categorical data. Here both columns are numeric and you want to see the relationship between them, so `plt.scatter()` is the right choice.
  ✘ opt_hist: `plt.hist(orders['distance_km'])`
      why: Not quite. `plt.hist()` bins a single numeric variable to show its distribution. To show the relationship between two numeric variables you need `plt.scatter(x, y)`.
  feedback✔: Exactly. `plt.scatter(x, y)` places one point per (x, y) pair — the right tool for exploring the relationship between two numeric variables.  feedback✘: To show the relationship between two numeric variables, use `plt.scatter(x, y)`. It places one point per (x, y) pair, so the pattern of points reveals whether the two variables move together.  hints: ['A scatter plot places one point per (x, y) pair — which function name matches that description?', '`plt.plot()` connects points with a line (for time series); `plt.scatter()` places independent points.']  remediation→r02
  MEASURES: B:build_scatter_plot_from_two_numeric_columns(f1,f2)   anchors=['assessment:build_scatter_plot_from_two_numeric_columns']
  taught-before-tested: B.f1←s05; B.f2←s05

### s08 · hands_on · Plot Distance vs Delivery Time  [reward 15]
hands-on — Use plt.scatter() to plot distance_km against delivery_time_minutes from the orders dataset.
QUESTION [code_exercise, core, grading=client] The `orders` DataFrame is already loaded from `orders.csv`. It has columns `distance_km` and `delivery_time_minutes`.

Call `plt.scatter(orders['distance_km'], orders['delivery_time_minutes'])` to produce a scatter plot with one point per order — distance on the x-axis and delivery time on the y-axis.

The figure should contain one scatter plot with 24 points.

After creating the plot, add a comment describing whether the points suggest a positive, negative, or no relationship between distance and delivery time.
  runtime={'kind': 'chart_renderer', 'version': '0.29.5', 'packages': ['matplotlib', 'pandas']} constraints.allowed=['plt.scatter(x, y)', 'ax.scatter(x, y)', 'plt.show()', 'fig, ax = plt.subplots()', 'import matplotlib.pyplot as plt', 'orders["distance_km"]', 'orders["delivery_time_minutes"]'] blocked=13 items
  file solution.py [editable]:
import matplotlib.pyplot as plt
import pandas as pd

orders = pd.read_csv('orders.csv')

# Call plt.scatter() with distance_km on the x-axis and delivery_time_minutes on the y-axis
# plt.scatter(...)

# Describe the relationship: positive, negative, or no relationship?
# Relationship: 

  SOLUTION solution.py:
import matplotlib.pyplot as plt
import pandas as pd

orders = pd.read_csv('orders.csv')

plt.scatter(orders["distance_km"], orders["delivery_time_minutes"])

# Relationship: positive

  test ix.tile_viz_line_scatter_box.s08.t01 (figure_equals, visible=True): {"expected":{"n_axes":1,"chart_types":[["scatter"]]}} | on-fail: Your figure should contain exactly one Axes with a scatter plot. Call `plt.scatter(orders['distance_km'], orders['delivery_time_minutes'])`.
  test ix.tile_viz_line_scatter_box.s08.t02 (plotted_data_equals, visible=True): {"chart":"scatter","field":"x","expected":[2.1,3.4,2.8,4.5,5.2,3.9,4.8,9.1,3.2,4.1,3.0,5.5,4.3,4.7,4.0,5.8,4.6,5.9,4.2,6.8,5.3,6.1,5.0,7.2],"series":0,"axes":0} | on-fail: The x-values should be `orders['distance_km']`. Pass that column as the first argument to `plt.scatter()`.
  test ix.tile_viz_line_scatter_box.s08.t03 (plotted_data_equals, visible=True): {"chart":"scatter","field":"y","expected":[18.0,22.0,19.0,26.0,30.0,24.0,28.0,50.0,25.0,28.0,23.0,31.0,27.0,29.0,26.0,32.0,28.0,32.0,27.0,35.0,30.0,33.0,29.0,36.0],"series":0,"axes":0} | on-fail: The y-values should be `orders['delivery_time_minutes']`. Pass that column as the second argument to `plt.scatter()`.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"396b46438a47185a32097d4d695f72daefe688ddb02aea65432e41983ba3a85f","tests_passed":3}
  feedback✔: Well done! `plt.scatter(orders['distance_km'], orders['delivery_time_minutes'])` places one point per order, making the relationship between distance and delivery time visible across all 24 orders.  feedback✘: Call `plt.scatter(orders['distance_km'], orders['delivery_time_minutes'])` — the first argument is the x-column (distance_km) and the second is the y-column (delivery_time_minutes).  hints: ['`plt.scatter(x, y)` takes two arguments: the x-column first, then the y-column.', "Access the columns with `orders['distance_km']` and `orders['delivery_time_minutes']`."]
  MEASURES: B:build_scatter_plot_from_two_numeric_columns(f1,f2)   anchors=['practice', 'assessment:build_scatter_plot_from_two_numeric_columns']
  taught-before-tested: B.f1←s05; B.f2←s05

### s09 · explainer · Reading a Box Plot  [reward 5]
box plots — Every part of a box plot has a name — learn to read the box, whiskers, and flier points.
(intro) Boxplots offer a condensed display for comparing the distributions of multiple datasets side by side — showing spread, median, and outliers in a single compact shape. ⟦C.f3 C:tb1⟧
[DIAGRAM: Box Plot Anatomy] nodes=['Flier point (outlier)', 'Upper whisker — farthest point within 1.5×IQR above Q3', 'Q3 (third quartile) — top edge of box', 'Median — line inside the box', 'Q1 (first quartile) — bottom edge of box', 'Lower whisker — farthest point within 1.5×IQR below Q1'] edges=[('flier_top', 'upper_whisker', None), ('upper_whisker', 'q3', None), ('q3', 'median', None), ('median', 'q1', None), ('q1', 'lower_whisker', None)] alt: A layered diagram of box plot anatomy from top to bottom: flier point (outlier) above the upper whisker; upper whisker reaching to the farthest in-range point above Q3; Q3 at the top of the box; median as a line inside the box; Q1 at the bottom of the box; lower whisker reaching to the farthest in-range point below Q1.

### s10 · explainer · The Box, Whiskers, and Flier Points  [reward 5]
box plots — The box spans Q1 to Q3; whiskers reach 1.5×IQR beyond the box; anything further is a flier.
(mechanism) `plt.boxplot(x)` (or `ax.boxplot(x)`) draws a box plot from the data in x; it accepts array-like data and can draw one or more boxes. The box extends from Q1 to Q3, with a line at the median. The whiskers extend to the farthest data point lying within 1.5× the IQR from the box; points past the whisker ends are flier points (outliers). ⟦C.f1 C.f2 C:tb2⟧
(example) If Lagos's box runs from Q1 = 20 to Q3 = 30 minutes, the IQR is 10 minutes. The whiskers can reach at most 1.5 × 10 = 15 minutes beyond the box — no lower than 5 minutes and no higher than 45 minutes — so a 50-minute Lagos delivery would be drawn as a separate flier point. ⟦C.f2 C:tb2⟧

### s11 · video · Box Plots: Distribution and Outliers  [reward 5]
watch — 
[VIDEO Box plot anatomy: reading the box, whiskers, and outlier dots] bridge-before: Watch how the diagram labels each part of the box. Note: the clip does not state the 1.5×IQR whisker rule or name Q1/Q3 explicitly — the teaching text covers both. | bridge-after: You saw the box span Q1 to Q3 and outlier dots beyond the whiskers. The teaching text adds the 1.5×IQR rule that sets exactly where whiskers end.
  - fHLhBnmwUM0 26-134s facts=['f2', 'f3'] label: Box plot structure: median, quartile box, whiskers, and flier points | summary: An annotated drawing introduces the box-and-whisker plot. The line inside the box marks the median, with half the data above and half below. The box itself contains the middle 50% of the data — 25% above the median and 25% below — corresponding to the Q1-to-Q3 range. Points that fall beyond the whiskers are drawn as individual dots. The segment then shows side-by-side boxes for different groups, contrasting that compact multi-distribution view with a traditional bar chart showing the same data.

### s12 · explainer · Comparing Multiple Cities Side by Side  [reward 5]
box plots — Pass a sequence of arrays to draw one box per group, and use tick_labels to name each box.
(syntax) Passing a sequence of 1D arrays as x draws one box for each array in the sequence; `tick_labels=[...]` labels each boxplot's tick accordingly instead of leaving it as a numeric value. `plt.boxplot([lagos_times, abuja_times, kano_times], tick_labels=['Lagos', 'Abuja', 'Kano'])` draws three boxes side by side, each labeled with its city name. ⟦C.f4 C:tb3⟧

### s13 · check · Box Plot Anatomy  [reward 10]
quick check — What do the edges of the box represent?
QUESTION [choice, core, grading=client] A box plot of Lagos delivery times has Q1 = 20 minutes and Q3 = 30 minutes. The IQR is 10 minutes. A delivery of 50 minutes is recorded. How will matplotlib draw that 50-minute delivery?
  ✔ opt_flier: As a flier point (outlier) beyond the upper whisker
      why: Correct. The upper whisker can reach at most Q3 + 1.5 × IQR = 30 + 15 = 45 minutes. A 50-minute delivery is beyond that limit, so it is drawn as a separate flier point.
  ✘ opt_whisker: At the tip of the upper whisker
      why: Not quite. The whisker tip is the farthest data point that still falls within 1.5 × IQR of the box (at most 45 minutes here). A 50-minute delivery exceeds that limit and is drawn as a flier point.
  ✘ opt_box: Inside the box, between Q1 and Q3
      why: Not quite. The box spans Q1 to Q3 (20 to 30 minutes). A 50-minute delivery is far above Q3 and would be drawn as a flier point beyond the upper whisker.
  ✘ opt_ignored: It is ignored and not drawn
      why: Not quite. Matplotlib draws all data points. Values beyond 1.5 × IQR from the box are shown as individual flier points — they are not ignored.
  feedback✔: Right. The upper whisker reaches at most Q3 + 1.5 × IQR = 45 minutes. The 50-minute delivery exceeds that, so it appears as a flier point.  feedback✘: The whiskers extend to the farthest point within 1.5 × IQR of the box. Here that is Q3 + 1.5 × 10 = 45 minutes. A 50-minute delivery is beyond that limit and is drawn as a separate flier point.  hints: ['Calculate the upper whisker limit: Q3 + 1.5 × IQR = 30 + 1.5 × 10 = ?', 'Any point beyond the whisker limit is drawn separately — what is that called?']  remediation→r03
  MEASURES: C:apply_iqr_rule_to_determine_whisker_extent_and_outliers(f2)   anchors=['assessment:apply_iqr_rule_to_determine_whisker_extent_and_outliers']
  taught-before-tested: C.f2←s10

### s14 · check · When to Use a Box Plot  [reward 10]
quick check — What is a box plot's main advantage over a bar chart for delivery-time data?
QUESTION [choice, core, grading=client] You want to compare the delivery-time distributions of Lagos, Abuja, and Kano side by side — not just their averages, but how spread out each city's times are. Which chart type is best suited for this?
  ✔ opt_box: A box plot, because it gives a condensed display of each distribution side by side
      why: Correct. Boxplots offer a condensed display for comparing the distributions of multiple datasets side by side — showing the median, spread, and outliers for each city in a single figure.
  ✘ opt_bar: A bar chart, because it shows the average for each city
      why: Not quite. A bar chart shows one value per category (such as the mean). It does not show the spread, quartiles, or outliers of each city's distribution — a box plot does.
  ✘ opt_line: A line plot, because it connects the values in order
      why: Not quite. A line plot is for showing how a value changes over an ordered sequence (such as time). It is not designed for comparing distributions across groups.
  ✘ opt_hist: A histogram, because it bins all delivery times into ranges
      why: Not quite. A histogram bins a single numeric variable to show its distribution shape. To compare distributions across multiple groups side by side, a box plot is the right choice.
  feedback✔: Exactly. A box plot gives a condensed display of each group's distribution — median, quartiles, whiskers, and outliers — all side by side.  feedback✘: When you want to compare the full distribution (not just the average) across multiple groups, use a box plot. It shows the median, spread, and outliers for each group in a condensed side-by-side display.  hints: ['The question asks about comparing *distributions* (spread, median, outliers) — not just averages.', "Which chart type is described as offering 'a condensed display for comparing the distributions of multiple datasets side by side'?"]  remediation→r04
  MEASURES: C:explain_box_plot_value_for_comparing_multiple_distributions(f3)   anchors=['assessment:explain_box_plot_value_for_comparing_multiple_distributions']
  taught-before-tested: C.f3←s09

### s15 · hands_on · Compare City Delivery Spreads with plt.boxplot()  [reward 15]
hands-on — Filter the orders dataset by city, then pass the three arrays to plt.boxplot() with tick_labels.
QUESTION [code_exercise, stretch, grading=client] Three arrays are already prepared for you: `lagos_times`, `abuja_times`, and `kano_times`. Each contains the delivery times for one city.

Call `plt.boxplot()` with all three arrays in a list as the first argument, and use the `tick_labels` parameter with a list `[city_1, city_2, city_3]` to label each box.

The figure should show three boxes, each reflecting the delivery time distribution for its city.
  runtime={'kind': 'chart_renderer', 'version': '0.29.5', 'packages': ['matplotlib', 'pandas']} constraints.allowed=['plt.boxplot(x)', 'ax.boxplot(x)', 'tick_labels=[...]', 'df.loc[df[col] == value, numeric_col]', 'import matplotlib.pyplot as plt', 'fig, ax = plt.subplots()', 'plt.show()', 'list literals and variable assignment'] blocked=9 items
  file solution.py [editable]:
import matplotlib.pyplot as plt
import pandas as pd

orders = pd.read_csv('orders.csv')

# City names
city_1 = 'Lagos'
city_2 = 'Abuja'
city_3 = 'Kano'

# Delivery times for each city (already filtered for you)
lagos_times = orders.loc[orders['city'] == city_1, 'delivery_time_minutes']
abuja_times = orders.loc[orders['city'] == city_2, 'delivery_time_minutes']
kano_times = orders.loc[orders['city'] == city_3, 'delivery_time_minutes']

# Call plt.boxplot() with all three arrays and tick_labels parameter
# plt.boxplot(...)

  SOLUTION solution.py:
import matplotlib.pyplot as plt
import pandas as pd

orders = pd.read_csv('orders.csv')

# City names
city_1 = 'Lagos'
city_2 = 'Abuja'
city_3 = 'Kano'

# Delivery times for each city (already filtered for you)
lagos_times = orders.loc[orders['city'] == city_1, 'delivery_time_minutes']
abuja_times = orders.loc[orders['city'] == city_2, 'delivery_time_minutes']
kano_times = orders.loc[orders['city'] == city_3, 'delivery_time_minutes']

# Call plt.boxplot() with all three arrays and labels parameter
plt.boxplot([lagos_times, abuja_times, kano_times], labels=[city_1, city_2, city_3])

  test ix.tile_viz_line_scatter_box.s15.t01 (figure_equals, visible=True): {"expected":{"n_axes":1,"chart_types":[["box"]]}} | on-fail: Your figure should contain exactly one Axes with a box plot. Call `plt.boxplot([lagos_times, abuja_times, kano_times], tick_labels=[city_1, city_2, city_3])`.
  test ix.tile_viz_line_scatter_box.s15.t02 (axes_property, visible=True): {"property":"xticklabels","expected":["Lagos","Abuja","Kano"],"axes":0} | on-fail: The tick labels should be ['Lagos', 'Abuja', 'Kano']. Make sure you pass `tick_labels=[city_1, city_2, city_3]` to `plt.boxplot()`.
  test ix.tile_viz_line_scatter_box.s15.t04 (plotted_data_equals, visible=True): {"chart":"box","field":"medians","expected":[25.0,27.5,31.0],"axes":0} | on-fail: The medians should be [25.0, 27.5, 31.0] for Lagos, Abuja, and Kano. Check that you are passing the three arrays in the correct order: `[lagos_times, abuja_times, kano_times]`.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"83e248ffa9bb1df2dfec59f71e450dd346eeb5fe0a10616d7a1915c022e71b1b","tests_passed":3}
  feedback✔: Excellent! You called `plt.boxplot([lagos_times, abuja_times, kano_times], tick_labels=[city_1, city_2, city_3])` to draw three side-by-side boxes, each labeled with its city name, showing the full distribution of delivery times for each city.  feedback✘: Call `plt.boxplot([lagos_times, abuja_times, kano_times], tick_labels=[city_1, city_2, city_3])` to draw three labeled boxes, one per city.  hints: ['Pass a list of three arrays to `plt.boxplot()`: `[lagos_times, abuja_times, kano_times]`.', 'Add `tick_labels=[city_1, city_2, city_3]` to label each box with its city name.']
  MEASURES: C:call_boxplot_function_with_array_like_data(f1); C:identify_box_whisker_and_flier_anatomy(f2); C:draw_grouped_box_plot_with_labeled_ticks_from_sequence_of_arrays(f4)   anchors=['practice', 'assessment:call_boxplot_function_with_array_like_data', 'assessment:identify_box_whisker_and_flier_anatomy', 'assessment:draw_grouped_box_plot_with_labeled_ticks_from_sequence_of_arrays']
  taught-before-tested: C.f1←s10; C.f2←s10; C.f4←s12

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
· constraints.blocked_syntax: plt.scatter(..., s=...)
· constraints.blocked_syntax: plt.scatter(..., c=...)
· constraints.blocked_syntax: plt.scatter(..., marker=...)
· constraints.blocked_syntax: plt.subplots() with nrows/ncols > 1