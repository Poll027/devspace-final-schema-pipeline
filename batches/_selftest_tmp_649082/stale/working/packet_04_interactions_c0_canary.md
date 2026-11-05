# EVALUATOR PACKET — Matching and Simplifying Charts for an Audience (tile_stakeholder_chart_matching_simplifying)
Tile summary: Learn to choose the right chart type for the specific point you are making to a stakeholder audience, then simplify that chart by removing visual clutter so the operations manager can focus on the finding, not on reading the graph.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = stakeholder.chart_type_to_point_matching — Matching chart type to the specific point being made (trend vs. comparison vs. distribution vs. part-to-whole)
B = stakeholder.simplifying_charts_for_audience — Simplifying a technical chart for a non-technical audience (removing gridlines, axis clutter, unneeded precision)

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: tile_stakeholder_chart_matching_simplifying.s01: prose block without lineage.fact_ids

## SOURCE FACTS — A (stakeholder.chart_type_to_point_matching)   objective: Match a chart type to the specific point being communicated to a stakeholder audience (trend, comparison, distribution, or part-to-whole), distinct from choosing a chart type for one's own exploration.
A.f1: A bar chart is used for graphing categorical data and comparing values across categories.   [sources: swd_what_is_a_bar_chart]
A.f2: Line graphs are best when you want to show how the value of something changes over time, or compare how several things change over time relative to each other.   [sources: swd_what_is_a_line_graph]
A.f3: Boxplots offer a condensed display for comparing the distributions of multiple datasets side by side.   [sources: swd_what_is_a_boxplot]
A.f4: A pie chart expresses a part-to-whole relationship in the data, and is best used either for a general sense of how parts relate to the whole, or to highlight that one segment is notably larger or smaller than the others; the pie must depict a meaningful whole (values that sum to 100%).   [sources: swd_what_is_a_pie_chart]
A.f5: A boxplot may be unfamiliar to many people and could introduce a learning curve; choosing a different display altogether may avoid confusion for audiences who do not know this chart type or how to read it.   [sources: swd_what_is_a_boxplot#When should you not use a boxplot?]
A.f6: A scatterplot is often used to understand data rather than to communicate with it, though it can still be designed to convey findings to an audience.   [sources: swd_what_is_a_scatterplot]
A.m1 (misconception): It is just as easy to precisely compare the sizes of pie slices as it is to compare bar lengths.   [sources: swd_what_is_a_pie_chart]
note: TOC conflict: f4 requires teaching what a pie chart is and when it fits, but no viz concept in this path teaches matplotlib pie-chart creation syntax. Teach the pie chart as a communication-design concept only (what it shows, when it fits, its part-to-whole requirement) -- no plt.pie() code is given here, since no earlier concept taught it.
PRACTICE ANCHOR (matching): Given the stakeholder point 'this category dominates the total', choose one chart type from the set {bar chart, line graph, boxplot, pie chart, scatterplot} and write one sentence justifying why it best communicates that specific point to a non-technical audience.  SUCCESS: The learner selects the pie chart (or provides a well-reasoned case for a bar chart showing share), correctly invokes the part-to-whole requirement (values sum to 100%), and explains why the chosen type makes the dominance of one segment immediately visible to a non-technical reader.
ASSESSMENT ANCHOR: select_chart_type_for_stakeholder_point facts=['f1', 'f2', 'f3', 'f4', 'f5', 'f6']
ASSESSMENT ANCHOR: distinguish_part_to_whole_from_comparison_framing facts=['f4', 'm1']
ASSESSMENT ANCHOR: evaluate_audience_readiness_for_boxplot facts=['f3', 'f5']
ASSESSMENT ANCHOR: classify_scatterplot_as_exploratory_vs_communicative facts=['f6']

## SOURCE FACTS — B (stakeholder.simplifying_charts_for_audience)   objective: Simplify a technical-looking chart for a non-technical audience by removing gridlines, chart borders, and unneeded label precision, without changing the underlying data.
B.f1: Gridlines can be deleted from a chart; if precise values matter to the audience, label the data point(s) directly instead of relying on gridlines.   [sources: swd_declutter_question_defaults]
B.f2: A chart's border can be removed, since it is not adding informative value; white space can differentiate parts of a visual better than a border.   [sources: swd_declutter_question_defaults]
B.f3: Data labels should be used sparingly, only where the exact values are important to the audience; otherwise they should be removed and the axis used instead.   [sources: swd_declutter_question_defaults]
B.f4: Reducing clutter lets the audience use their attention to decide what actions might be warranted, rather than working out how to read the graph.   [sources: swd_declutter_question_defaults]
B.f5: Unnecessary trailing zeroes can be dropped from axis labels.   [sources: swd_declutter_question_defaults]
B.f6: Diagonally rotated axis text is slower to read; labels can be abbreviated so they render horizontally instead.   [sources: swd_declutter_question_defaults]
note: No specific matplotlib method names are given by the facts for removing gridlines/borders (e.g. no ax.grid(False) is stated), so the example stays at the conceptual/design level rather than inventing exact syntax.
PRACTICE ANCHOR (UI_edit): Given a bar chart that has a visible border, gridlines, trailing-zero axis labels (e.g. '22.00'), diagonally rotated city-name tick labels, and data labels on every bar, simplify it for a non-technical operations manager: remove the border and gridlines, drop the trailing zeros from axis labels, abbreviate and horizontalise the city-name tick labels, and remove the data labels (keeping the axis for approximate reading).  SUCCESS: The revised chart has no border, no gridlines, axis labels without trailing zeros, horizontal (non-rotated) city-name tick labels, and no per-bar data labels — while the underlying delivery-time values are unchanged.
ASSESSMENT ANCHOR: identify_clutter_elements_to_remove facts=['f1', 'f2', 'f3', 'f5', 'f6']
ASSESSMENT ANCHOR: choose_between_data_labels_and_axis_for_precision facts=['f1', 'f3']
ASSESSMENT ANCHOR: explain_cognitive_benefit_of_reducing_chart_clutter facts=['f4']
ASSESSMENT ANCHOR: simplify_axis_labels_for_readability facts=['f5', 'f6']
ASSESSMENT ANCHOR: justify_border_removal_using_white_space facts=['f2']

## DATA ASSETS USED
asset_city_deliveries: City Delivery Summary — columns: city(categorical), avg_delivery_minutes(numerical), order_count(numerical)
   ["Lagos",34.0,720]
   ["Abuja",22.0,300]
   ["Kano",19.0,180]
   variant city_deliveries_messy: 1 ops; planted: issue_impossible_delivery_time(impossible_value)
asset_lagos_weekly_deliveries: Lagos Weekly Delivery Trend — columns: week_number(identifier,digits-as-label), week_label(categorical), avg_delivery_minutes(numerical), order_count(numerical)
   [1,"Wk 1",28.0,85]
   [2,"Wk 2",29.5,88]
   [3,"Wk 3",30.0,91]
   [4,"Wk 4",31.5,90]
   [5,"Wk 5",33.0,94]
   [6,"Wk 6",34.0,96]
   [7,"Wk 7",36.5,99]
   [8,"Wk 8",38.0,102]
   variant lagos_weekly_messy: 1 ops; planted: issue_missing_delivery_time_wk6(impossible_value)

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Applying descriptive statistics to capstone findings; Basic presentation structure (opening, body, call to action); Building a data model for the capstone dataset; Building a polished matplotlib/seaborn visualization set for the capstone; Defining a capstone business question/problem statement; Documenting and presenting the finished capstone deliverable; Independent, unassisted execution across multiple tool families; Integrating Python/pandas cleaning and analysis into an end-to-end project; Integrating SQL querying into an end-to-end project; Integrating spreadsheet analysis into an end-to-end project; Producing a stakeholder-facing narrated summary of the capstone; Selecting an appropriate data retrieval method (SQL and/or spreadsheet); Simplifying a technical chart for a non-technical audience (removing gridlines, axis clutter, unneeded precision); Structuring an end-to-end workflow (retrieval, cleaning, modeling, analysis, visualization, communication); Writing an executive summary

## LESSON, in learner order

### s01 · explainer · The chart must match the point, not just the data  [reward 5]
Chart Type to Point Matching — You have the delivery data. The question is: which chart makes your specific point land for the operations manager?
(intro) During your own exploration you might have built a bar chart, a line plot, and a boxplot of the delivery data. Presenting to the operations manager, the question changes: which one actually makes the Lagos point, for this audience? The same dataset can support several chart types — the right choice depends on the specific point you are communicating, not on the data alone. ⟦A:tb1⟧
(mechanism) A bar chart is used for graphing categorical data and comparing values across categories — showing average delivery time side by side across Lagos, Abuja, and Kano. A line graph is best when you want to show how the value of something changes over time — showing Lagos delivery time rising week over week. Boxplots offer a condensed display for comparing distributions side by side, but a boxplot may be unfamiliar to many people and could introduce a learning curve; for a manager who hasn't seen one before, a bar chart or line plot can often make the point more directly. ⟦A.f1 A.f2 A.f3 A.f5 A:tb2⟧
[SIDE_BY_SIDE] The same delivery data supports both charts — the bar chart makes a comparison point (which city is slowest?), the line graph makes a trend point (is Lagos getting slower?). Choose the chart that matches the point you are making. left_label: Bar chart — compare values across cities | right_label: Line graph — show Lagos trend over weeks
  left:
[CHART bar: Average Delivery Time by City] data=asset_city_deliveries x=city y=avg_delivery_minutes color=None annotations=[] alt: Bar chart showing average delivery time in minutes for Lagos (34), Abuja (22), and Kano (19), illustrating a city-vs-city comparison.
  right:
[CHART line: Lagos Average Delivery Time — Week over Week] data=asset_lagos_weekly_deliveries x=week_label y=avg_delivery_minutes color=None annotations=[] alt: Line graph showing Lagos average delivery time rising from 28 min in Wk 1 to 38 min in Wk 8, illustrating a week-over-week trend.

### s02 · video · Why the chart type must match the point you are making  [reward 5]
Chart Type to Point Matching — Watch how the same data looks different depending on chart type, and notice when a chart makes comparison easy versus hard.
[VIDEO Why the chart type must match the point you are making] bridge-before: Watch how the same data looks different depending on chart type, and notice when a chart makes comparison easy versus hard. The first clip argues strongly for bars over pies; Devspace's text also covers when a pie is the right choice. | bridge-after: The first clip demonstrates f1 and counters the pie-slice comparison misconception; the second covers f3 and f5. Neither clip addresses part-to-whole framing (f4) or scatterplots (f6) — the text covers both.
  - RiEZ_hEf96A 0-101s facts=['f1'] label: Bar chart vs. pie chart: comparing values across categories | summary: The same time-use data (sleep, work, eat, rest) is shown first as a pie chart, then as a bar chart. The pie makes it hard to judge which slice is larger when two slices are close in size. The bar chart, with its common baseline, makes the one-hour difference between working and sleeping immediately readable. A second example pits two pie charts against a grouped bar chart to answer 'does Earl work more than Herman, and by how much?' — a question the pies struggle to answer and the bar chart resolves at a glance.
  - Z77c53eYtHc 149-201s facts=['f3', 'f5'] label: Boxplots: strong for distributions, but risky with unfamiliar audiences | summary: A boxplot is considered as a candidate for showing distributions across multiple groups. Two practical problems emerge: sparse data on some days would produce boxes with no box body, and — more broadly — boxplots are not a widely recognised chart type, so an audience unfamiliar with them faces a steeper learning curve. The presenter notes that a specialist audience (researchers and physicians) may be the exception, but still sets the boxplot aside in favour of continuing to explore other options.

### s03 · explainer · Pie charts, scatterplots, and the comparison trap  [reward 5]
Chart Type to Point Matching — Two more chart types complete the toolkit — and one common misconception about pie charts is worth clearing up.
(practical_context) A pie chart expresses a part-to-whole relationship in the data. It is best used either for a general sense of how parts relate to the whole, or to highlight that one segment is notably larger or smaller than the others. The pie must depict a meaningful whole — values that sum to 100%. If the point is 'Lagos accounts for most of our total delivery volume,' a pie chart of each city's share of total orders fits that part-to-whole framing in a way a bar chart of averages would not. ⟦A.f4 A:tb3⟧
(practical_context) A scatterplot is often used to understand data rather than to communicate with it, though it can still be designed to convey findings to an audience. Keep this in mind if the distance/delivery-time relationship ever needs to go in front of the manager directly, rather than staying an exploratory chart. ⟦A.f6 A:tb4⟧
(misconception) It can look like comparing pie slices is just as easy as comparing bar lengths, since both show a value at a glance — but it is not. A bar chart's aligned, common baseline makes length differences easy to judge; two pie slices of similar size are harder to rank correctly by eye. ⟦A.m1 A:tb5⟧

### s04 · check · Scatterplot: exploratory or communicative?  [reward 10]
Quick Check — Test your understanding of when a scatterplot is the right choice for a stakeholder audience.
QUESTION [choice, core, grading=client] A data analyst plots distance_km against delivery_minutes for all orders across Lagos, Abuja, and Kano. Which statement best describes how a scatterplot is typically used?
  ✔ opt_a: A scatterplot is primarily used to understand data during exploration, though it can be designed to communicate findings to an audience.
      why: Correct. A scatterplot is often used to understand data rather than to communicate with it, but it can still be designed to convey findings to an audience.
  ✘ opt_b: A scatterplot is the clearest chart for communicating findings to a non-technical audience because it shows every individual data point.
      why: Incorrect. Showing every individual data point makes a scatterplot harder, not easier, for a non-technical audience to read without extra design work such as a clear title, colour coding, and a trend line.
  ✘ opt_c: A scatterplot cannot be used to communicate findings to an audience under any circumstances.
      why: Incorrect. A scatterplot can be designed to communicate findings to an audience — it just requires deliberate choices such as a clear title and colour coding. The default is exploratory, not the only use.
  ✘ opt_d: A scatterplot is best used to show how a value changes over time.
      why: Incorrect. Showing change over time is the strength of a line graph, not a scatterplot. A scatterplot shows the relationship between two numerical variables.
  feedback✔: Right. Scatterplots are exploratory by default — they reveal relationships in your own analysis. With deliberate design choices they can communicate findings to an audience, but that extra work is required.  feedback✘: A scatterplot is often used to understand data rather than to communicate with it, though it can still be designed to convey findings to an audience.  hints: ['Think about who typically reads a scatterplot — the analyst building it, or the manager receiving the report?', "The fact says 'often used to understand data' — does that mean it can never communicate?"]  remediation→r01
  MEASURES: A:classify_scatterplot_as_exploratory_vs_communicative(f6)   anchors=['assessment:classify_scatterplot_as_exploratory_vs_communicative']
  taught-before-tested: A.f6←s03

### s05 · hands_on · Match the chart to the stakeholder point  [reward 15]
Practice — Given a stakeholder point about the delivery data, choose the chart type that best communicates it and explain why.
QUESTION [classify, stretch, grading=client] The operations manager needs three separate charts for three different points. Drag each stakeholder point into the bucket for the chart type that best communicates it.
  '"Lagos has the longest average delivery time compared with Abuja and Kano."' -> Bar chart
      feedback: A bar chart is used for graphing categorical data and comparing values across categories — perfect for a side-by-side city comparison.
  '"Lagos average delivery time has been rising week over week for the past eight weeks."' -> Line graph
      feedback: Line graphs are best when you want to show how the value of something changes over time, making the week-over-week rise in Lagos immediately visible.
  '"Lagos accounts for most of our total delivery volume across all three cities."' -> Pie chart
      feedback: A pie chart expresses a part-to-whole relationship — Lagos's share of total orders sums to 100% with the other cities, making this the right framing.
  '"The spread of individual delivery times differs across cities — some cities have much more variation than others."' -> Boxplot — avoid with this audience
      feedback: Boxplots offer a condensed display for comparing distributions side by side, but may be unfamiliar to many people and could introduce a learning curve — flag this for a non-technical audience.
  '"There may be a relationship between distance from the depot and delivery time."' -> Scatterplot — exploratory, needs design work
      feedback: A scatterplot is often used to understand data rather than to communicate with it. It can convey the distance/delivery-time relationship, but requires deliberate design choices for a non-technical audience.
  feedback✔: Well done. Each chart type matches the specific point: bar for comparison, line for trend, pie for part-to-whole, boxplot for distribution (with an audience caveat), and scatterplot for relationships (exploratory by default).  feedback✘: The chart type must match the specific point being made. Bar = comparison across categories; line = change over time; pie = part-to-whole (must sum to 100%); boxplot = distributions (risky with non-technical audiences); scatterplot = relationships (exploratory by default).  hints: ['Ask yourself: is the point about comparing categories, showing change over time, or showing how parts add up to a whole?', 'For the distribution item, think about whether the operations manager has seen a boxplot before.']  remediation→r02
  MEASURES: A:select_chart_type_for_stakeholder_point(f1,f2,f3,f4,f5,f6); A:distinguish_part_to_whole_from_comparison_framing(f4,m1); A:evaluate_audience_readiness_for_boxplot(f3,f5)   anchors=['practice', 'assessment:select_chart_type_for_stakeholder_point', 'assessment:distinguish_part_to_whole_from_comparison_framing', 'assessment:evaluate_audience_readiness_for_boxplot']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01; A.f4←s03; A.f5←s01; A.f6←s03; A.f4←s03; A.m1←s03; A.f3←s01; A.f5←s01

### s06 · explainer · Remove the clutter — not the data  [reward 5]
Simplifying Charts for an Audience — A chart built for your own exploration carries elements the operations manager doesn't need. Each removal reduces reading effort without changing the numbers.
(intro) A bar chart of city delivery times built during your own exploration can carry gridlines, a border, and precise decimal labels that help you double-check the numbers. The operations manager probably doesn't need any of that to get the point. Gridlines can be deleted from a chart; if precise values matter to the audience, label the data point directly instead of relying on gridlines. ⟦B.f1 B:tb1 B:tb2⟧
(mechanism) A chart's border can be removed, since it is not adding informative value; white space can differentiate parts of a visual better than a border. Data labels should be used sparingly, only where the exact values are important to the audience; otherwise remove them and use the axis instead. Unnecessary trailing zeroes can be dropped from axis labels — '22.00 minutes' can become '22 min'. Diagonally rotated axis text is slower to read; city-name tick labels like Lagos, Abuja, and Kano don't need to be rotated at all. ⟦B.f2 B.f3 B.f5 B.f6 B:tb2 B:tb3⟧
[BEFORE_AFTER] Border removed — white space does the job of separation. Gridlines removed — the axis scale is sufficient. Trailing zeros dropped from axis labels (34.00 → 34). City-name tick labels un-rotated — short names read fine horizontally. Per-bar data labels removed — the axis gives approximate values. None of these changes alter the underlying delivery-time numbers.
  before:
[DIAGRAM: Before: cluttered bar chart] nodes=['Chart border (box around entire chart)', 'Horizontal gridlines behind bars', 'Y-axis labels with trailing zeros (e.g., 0.00, 10.00, 20.00, 30.00, 40.00)', 'X-axis city names rotated 45°', 'Data label on every bar (34.00, 22.00, 19.00)', 'Bars: Lagos 34 min, Abuja 22 min, Kano 19 min'] edges=[] alt: Diagram representing a cluttered bar chart with a border, gridlines, decimal axis labels, rotated city-name tick labels, and data labels on every bar.
  after:
[DIAGRAM: After: simplified bar chart] nodes=['Bars: Lagos 34 min, Abuja 22 min, Kano 19 min', 'Y-axis: 0, 10, 20, 30, 40 (no trailing zeros)', 'X-axis: Lagos, Abuja, Kano (horizontal, no rotation)', 'White space separates chart from surrounding content'] edges=[] alt: Diagram representing a simplified bar chart with no border, no gridlines, clean axis labels without trailing zeros, horizontal city-name tick labels, and no per-bar data labels.

### s07 · video · Decluttering a chart for a non-technical audience  [reward 5]
Simplifying Charts for an Audience — Watch how each removal reduces reading effort. The same design principles apply in any charting tool.
[VIDEO Decluttering a chart for a non-technical audience] bridge-before: Watch how each removal reduces reading effort. Note: the presenter uses Excel; the same design principles apply in any charting tool. The clip does not demonstrate labelling a data point directly when precision matters (f1). | bridge-after: The clip shows f2–f6 applied in sequence. Devspace's text also covers f1: when precise values are essential, label the data point directly rather than restoring gridlines.
  - XgY1-BsZSzM 51-393s facts=['f2', 'f3', 'f4', 'f5', 'f6'] label: Removing chart clutter: border, gridlines, trailing zeros, diagonal labels, and excess data labels | summary: The presenter opens by explaining that every chart element adds cognitive burden, and that overwhelming an audience risks losing them entirely — establishing why decluttering matters. Working on a bar chart in Excel, they remove the chart border (noting white space does the job of separation better), delete the gridlines and shaded background, then reformat the y-axis to drop trailing zeros by switching to thousands units with a 'k' suffix. They then abbreviate the diagonal month labels on the x-axis to horizontal text, citing research that diagonal text takes fifty percent longer to read. Finally, they weigh whether exact values are needed: deciding they are not, they delete all data labels and keep the y-axis instead, leaving a much cleaner chart.

### s08 · check · Which elements reduce clutter?  [reward 10]
Quick Check — Identify the chart elements that should be removed to simplify a chart for a non-technical audience.
QUESTION [choice, core, grading=client] An analyst has a bar chart with a visible border, gridlines, decimal axis labels (e.g. '34.00'), diagonally rotated city-name tick labels, and a data label on every bar. The operations manager does not need exact values. Which set of changes best simplifies this chart?
  ✔ opt_a: Remove the border, gridlines, and data labels; drop trailing zeros from axis labels; display city-name tick labels horizontally.
      why: Correct. Removing the border, gridlines, trailing zeros, diagonal labels, and unnecessary data labels reduces the visual effort the audience must spend before they can act on the finding.
  ✘ opt_b: Remove only the gridlines, because they are the main source of visual noise; keep the border, decimal labels, and data labels to maintain precision.
      why: Incorrect. Gridlines are one source of clutter, but the border, decimal trailing zeros, and diagonal tick labels also add visual effort without adding informative value. Data labels should be removed when exact values are not critical.
  ✘ opt_c: Keep all elements — removing any of them risks losing information the audience needs to understand the chart.
      why: Incorrect. None of these removals change the underlying data. The border adds no informative value; white space differentiates the chart better. Trailing zeros and diagonal labels slow reading.
  ✘ opt_d: Remove the data labels and replace them with a table below the chart so the audience can look up exact values.
      why: Incorrect. Adding a separate table increases the total visual effort. Since the manager does not need exact values, removing data labels and keeping the axis is the simpler solution.
  feedback✔: Exactly right. Each removal — border, gridlines, trailing zeros, diagonal labels, excess data labels — reduces the visual effort the audience must spend before they can act on the finding.  feedback✘: Focus on what each element adds for the audience. The border adds no informative value; white space does the job better. Trailing zeros and diagonal labels slow reading. Data labels are only needed when exact values are critical.  hints: ['Which elements encode data, and which are just visual decoration?', 'If the manager does not need exact values, do data labels help or add clutter?']  remediation→r03
  MEASURES: B:identify_clutter_elements_to_remove(f1,f2,f3,f5,f6); B:explain_cognitive_benefit_of_reducing_chart_clutter(f1,f2,f3)   anchors=['assessment:identify_clutter_elements_to_remove', 'assessment:explain_cognitive_benefit_of_reducing_chart_clutter']
  taught-before-tested: B.f1←s06; B.f2←s06; B.f3←s06; B.f5←s06; B.f6←s06; B.f1←s06; B.f2←s06; B.f3←s06

### s09 · check · Why remove the border?  [reward 10]
Quick Check — Explain why removing a chart border improves readability for a non-technical audience.
QUESTION [choice, core, grading=client] Why can a chart's border be removed without losing anything important?
  ✔ opt_a: White space can differentiate parts of a visual better than a border, and the border is not adding informative value.
      why: Correct. A chart's border is not adding informative value; white space can differentiate parts of a visual better than a border.
  ✘ opt_b: The border should only be removed if the chart has no gridlines, because one of the two is needed to frame the chart.
      why: Incorrect. Neither a border nor gridlines are required to frame a chart. White space alone differentiates the chart from surrounding content.
  ✘ opt_c: Borders are only decorative in pie charts; bar charts need a border to separate the bars from the background.
      why: Incorrect. The principle applies to all chart types: a border is not adding informative value regardless of chart type, and white space does the job of separation better.
  ✘ opt_d: Removing the border makes the chart smaller, which saves space on the slide.
      why: Incorrect. Removing a border does not change the chart's dimensions. The reason to remove it is that it adds no informative value, not that it saves space.
  feedback✔: Right. The border encodes no data and adds no informative value. White space around the chart separates it from surrounding content just as effectively.  feedback✘: A chart's border can be removed because it is not adding informative value; white space can differentiate parts of a visual better than a border.  hints: ['Does the border tell the audience anything about the delivery data?', 'What does white space do that a border also does?']  remediation→r04
  MEASURES: B:justify_border_removal_using_white_space(f2)   anchors=['assessment:justify_border_removal_using_white_space']
  taught-before-tested: B.f2←s06

### s10 · hands_on · Simplify a chart for the operations manager  [reward 15]
Practice — Given a bar chart with a border, gridlines, trailing-zero axis labels, rotated city-name tick labels, and data labels on every bar — simplify it for a non-technical operations manager.
QUESTION [classify, stretch, grading=client] The operations manager's bar chart currently has these elements. Classify each one: should it be kept as-is, removed, or changed? (The manager does not need exact delivery-time values.)
  'Gridlines across the chart area' -> Remove
      feedback: Gridlines can be deleted from a chart. If precise values matter, label the data point directly instead — but here the manager does not need exact values, so the axis alone is sufficient.
  'Data labels showing '34.00 min', '22.00 min', '19.00 min' on every bar' -> Remove
      feedback: Data labels should be used sparingly, only where exact values are important to the audience. Since the manager does not need exact values, remove the data labels and rely on the axis.
  'Y-axis labels showing '10.00', '20.00', '30.00', '40.00'' -> Change (abbreviate / simplify)
      feedback: Unnecessary trailing zeros can be dropped — '10.00' becomes '10' or '10 min'. This reduces visual noise without changing the data.
  'City-name tick labels 'Lagos', 'Abuja', 'Kano' displayed diagonally at 45°' -> Change (abbreviate / simplify)
      feedback: Diagonally rotated axis text is slower to read. Labels can be abbreviated so they render horizontally — 'Lagos', 'Abuja', and 'Kano' are short enough to display horizontally without overlap.
  'The bars themselves (the encoded delivery-time data)' -> Keep as-is
      feedback: The bars encode the delivery-time data — they are the point of the chart and must be kept.
  feedback✔: Correct. Remove gridlines and unnecessary data labels; drop trailing zeros from axis labels; display city-name tick labels horizontally. The bars stay — they are the data.  feedback✘: Focus on what each element adds for the audience. Gridlines and excess data labels add visual effort without adding value. Trailing zeros and diagonal labels slow reading. The bars are the data and must stay.  hints: ['Which elements encode the delivery-time data, and which are just formatting?', 'If the manager does not need exact values, do data labels help or add clutter?']  remediation→r03
  MEASURES: B:choose_between_data_labels_and_axis_for_precision(f1,f3); B:simplify_axis_labels_for_readability(f5,f6)   anchors=['practice', 'assessment:choose_between_data_labels_and_axis_for_precision', 'assessment:simplify_axis_labels_for_readability']
  taught-before-tested: B.f1←s06; B.f3←s06; B.f5←s06; B.f6←s06

### s11 · recap · What you've learned  [reward 5]
Recap — Two skills that work together: matching the chart to the point, then clearing the noise.
(takeaway) Reducing clutter lets the audience use their attention to decide what actions might be warranted, rather than working out how to read the graph. None of these changes alter the underlying delivery-time numbers — only how much visual effort it takes to read them. Match the chart to the point; then strip everything that doesn't serve that point. ⟦B.f4 B:tb4⟧
[UP NEXT] Up next: Structuring a Stakeholder Presentation: Now that your charts are matched to their points and stripped of clutter, the next tile covers how to structure the full presentation — opening with the finding, not the method.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Scatterplots: exploratory by default, communicative by design — A scatterplot is a powerful tool for your own analysis — but it needs extra design work to communicate findings to an audience.
(practical_context) A scatterplot is often used to understand data rather than to communicate with it. When you plot distance_km against delivery_minutes for orders across Lagos, Abuja, and Kano, you are exploring a relationship — that is the scatterplot's strength. It can still be designed to convey findings to an audience, but that requires deliberate choices: a clear title stating the finding, colour coding by city, and a trend line if the relationship is the point. Without those additions, a scatterplot of 15 order records is harder for the operations manager to read than a bar chart or line graph. ⟦A.f6 A:tb4⟧
### r02 · Matching chart type to the point: a quick contrast — The same delivery data can be shown as a bar chart, line graph, pie chart, or scatterplot — the right choice depends entirely on the point you are making.
(mechanism) Bar chart: comparing values across categories — which city has the longest average delivery time? Use it when the point is a side-by-side comparison (Lagos 34 min, Abuja 22 min, Kano 19 min). Line graph: showing change over time — is Lagos delivery time rising week over week? Pie chart: part-to-whole — does Lagos account for most of total orders? The pie must sum to 100%. Boxplot: comparing distributions side by side — but may be unfamiliar to a non-technical audience, so a bar chart or line plot often makes the point more directly. Scatterplot: exploring a relationship — distance vs. delivery time — but needs extra design work to communicate findings clearly. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A:tb2 A:tb3 A:tb4⟧
(misconception) It can look like comparing pie slices is just as easy as comparing bar lengths — but it is not. A bar chart's aligned, common baseline makes length differences easy to judge; two pie slices of similar size are harder to rank correctly by eye. Use a pie chart only when the part-to-whole relationship is the point, not when precise comparison between categories is needed. ⟦A.m1 A:tb5⟧
### r03 · What counts as clutter — and why removing it helps — Each element you remove from a chart reduces the cognitive effort the audience spends reading it.
(mechanism) Gridlines can be deleted; if precise values matter, label the data point directly instead. A chart's border can be removed — white space differentiates parts of a visual better than a border. Data labels should be used sparingly, only where exact values are important; otherwise use the axis. Unnecessary trailing zeroes can be dropped from axis labels. Diagonally rotated axis text is slower to read — abbreviate labels so they render horizontally. ⟦B.f1 B.f2 B.f3 B.f5 B.f6 B:tb2 B:tb3⟧
(takeaway) Reducing clutter lets the audience use their attention to decide what actions might be warranted, rather than working out how to read the graph. None of these removals change the underlying delivery-time numbers. ⟦B.f4 B:tb4⟧
### r04 · Border vs. white space: why the border can go — A chart border feels like it organises the visual — but white space does that job better.
(mechanism) A chart's border is not adding informative value — it does not encode any data and does not help the audience read the bars. White space around the chart differentiates it from surrounding content just as effectively, without adding a visual element the eye has to process. Removing the border is one of the quickest single changes that reduces clutter on a chart built for a non-technical audience like the operations manager. ⟦B.f2 B:tb2⟧

## OTHER CONTENT (fields without a dedicated renderer)
· y.title: Avg Delivery Time (min)
· y.title: Avg Delivery Time (min)