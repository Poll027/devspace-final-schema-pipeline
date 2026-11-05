# EVALUATOR PACKET — Matching and Simplifying Charts for an Audience (tile_stakeholder_chart_matching_simplifying)
Tile summary: Learn to match chart type to the specific stakeholder point (bar for comparison, line for trend, pie for part-to-whole, boxplot with caution), then simplify the chosen chart by removing gridlines, borders, trailing zeros, rotated labels, and unnecessary data labels.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = stakeholder.chart_type_to_point_matching — Matching chart type to the specific point being made (trend vs. comparison vs. distribution vs. part-to-whole)
B = stakeholder.simplifying_charts_for_audience — Simplifying a technical chart for a non-technical audience (removing gridlines, axis clutter, unneeded precision)

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: tile_stakeholder_chart_matching_simplifying.s01: prose block without lineage.fact_ids
  warn: tile_stakeholder_chart_matching_simplifying.s06: prose block without lineage.fact_ids

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
ds_city_delivery_summary: City Delivery Summary — columns: city(categorical), avg_delivery_minutes(numerical), order_count(numerical), share_pct(numerical)
   ["Lagos",38.4,3120,57.1]
   ["Abuja",27.2,1560,28.6]
   ["Kano",22.0,780,14.3]
   variant ds_city_delivery_summary.messy: 4 ops; planted: issue_impossible_delivery_time(impossible_value); issue_city_casing(inconsistent_category); issue_missing_share_pct(missing_value)
ds_weekly_delivery_trend: Weekly Delivery Trend by City — columns: week_number(identifier,digits-as-label), city(categorical), avg_delivery_minutes(numerical), distance_km(numerical)
   [1,"Lagos",34.0,8.2]
   [1,"Abuja",27.0,6.1]
   [1,"Kano",22.0,4.8]
   [2,"Lagos",36.5,8.5]
   [2,"Abuja",27.3,6.0]
   [2,"Kano",21.8,4.9]
   [3,"Lagos",38.1,8.9]
   [3,"Abuja",27.1,6.2]
   variant ds_weekly_delivery_trend.messy: 2 ops; planted: issue_duplicate_lagos_week2(duplicate_row); issue_outlier_kano_week3(outlier_suspicious)

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Applying descriptive statistics to capstone findings; Basic presentation structure (opening, body, call to action); Building a data model for the capstone dataset; Building a polished matplotlib/seaborn visualization set for the capstone; Defining a capstone business question/problem statement; Documenting and presenting the finished capstone deliverable; Independent, unassisted execution across multiple tool families; Integrating Python/pandas cleaning and analysis into an end-to-end project; Integrating SQL querying into an end-to-end project; Integrating spreadsheet analysis into an end-to-end project; Producing a stakeholder-facing narrated summary of the capstone; Selecting an appropriate data retrieval method (SQL and/or spreadsheet); Simplifying a technical chart for a non-technical audience (removing gridlines, axis clutter, unneeded precision); Structuring an end-to-end workflow (retrieval, cleaning, modeling, analysis, visualization, communication); Writing an executive summary

## LESSON, in learner order

### s01 · explainer · The chart you pick should match the point you are making  [reward 5]
Chart Type Matching — The same delivery data can be shown as a bar chart, a pie chart, or a line plot — but only one will make your specific point land for the operations manager.
(intro) During your own exploration you might have built several charts of SwiftMove Nigeria's delivery data. Presenting to the operations manager, the question changes: which chart actually makes the point you need to make, for this audience? Chart choice is driven by the point, not by the data alone. ⟦A:tb1⟧
(mechanism) A bar chart is used for graphing categorical data and comparing values across categories — showing average delivery time side by side for Lagos, Abuja, and Kano. A line graph is best when you want to show how a value changes over time — for example, Lagos delivery time rising week over week. Boxplots offer a condensed display for comparing distributions side by side, but they may be unfamiliar to many audiences and could introduce a learning curve; a bar chart or line plot can often make the same point more directly. ⟦A.f1 A.f2 A.f3 A.f5 A:tb2⟧
[SIDE_BY_SIDE] The same delivery data, two different points — the chart type follows the point, not the other way around. left_label: Bar chart — compare cities | right_label: Line graph — Lagos trend over weeks
  left:
[CHART bar: Average Delivery Time by City] data=ds_city_delivery_summary x=city y=avg_delivery_minutes color=None annotations=['Point: Which city takes longest?'] alt: Bar chart showing average delivery minutes for Lagos (38.4), Abuja (27.2), and Kano (22.0). Point: compare values across cities.
  right:
[CHART line: Lagos Delivery Time — Weeks 1–3] data=ds_weekly_delivery_trend x=week_number y=avg_delivery_minutes color=city annotations=['Point: Is delivery time rising?'] alt: Line graph showing Lagos average delivery time rising from 34.0 min in week 1 to 38.1 min in week 3. Point: show a trend over time.

### s02 · video · Why the chart type must match the point you are making
Video — 
[VIDEO Why the chart type must match the point you are making] bridge-before: Watch how the same data looks different depending on chart type, and notice when a chart makes comparison easy versus hard. The first clip argues strongly for bars over pies; Devspace's text also covers when a pie is the right choice. | bridge-after: The first clip demonstrates f1 and counters the pie-slice comparison misconception; the second covers f3 and f5. Neither clip addresses part-to-whole framing (f4) or scatterplots (f6) — the text covers both.
  - RiEZ_hEf96A 0-101s facts=['f1'] label: Bar chart vs. pie chart: comparing values across categories | summary: The same time-use data (sleep, work, eat, rest) is shown first as a pie chart, then as a bar chart. The pie makes it hard to judge which slice is larger when two slices are close in size. The bar chart, with its common baseline, makes the one-hour difference between working and sleeping immediately readable. A second example pits two pie charts against a grouped bar chart to answer 'does Earl work more than Herman, and by how much?' — a question the pies struggle to answer and the bar chart resolves at a glance.
  - Z77c53eYtHc 149-201s facts=['f3', 'f5'] label: Boxplots: strong for distributions, but risky with unfamiliar audiences | summary: A boxplot is considered as a candidate for showing distributions across multiple groups. Two practical problems emerge: sparse data on some days would produce boxes with no box body, and — more broadly — boxplots are not a widely recognised chart type, so an audience unfamiliar with them faces a steeper learning curve. The presenter notes that a specialist audience (researchers and physicians) may be the exception, but still sets the boxplot aside in favour of continuing to explore other options.

### s03 · explainer · Pie charts, scatterplots, and a comparison trap  [reward 5]
Chart Type Matching — Part-to-whole framing calls for a pie chart — but comparing pie slices is harder than it looks.
(practical_context) A pie chart expresses a part-to-whole relationship in the data. It is best used for a general sense of how parts relate to the whole, or to highlight that one segment is notably larger or smaller than the others — and the pie must depict a meaningful whole (values that sum to 100%). If the point is 'Lagos accounts for most of our total delivery volume,' a pie chart of city order shares fits that framing in a way a bar chart of averages would not. ⟦A.f4 A:tb3⟧
(practical_context) A scatterplot is often used to understand data rather than to communicate with it, though it can still be designed to convey findings to an audience. It is not the default choice for a non-technical stakeholder presentation, but if the distance-versus-delivery-time relationship needs to go in front of the operations manager, a scatterplot can work. ⟦A.f6 A:tb4⟧
(misconception) It can look like comparing pie slices is just as easy as comparing bar lengths — but it is not. A bar chart's aligned, common baseline makes length differences easy to judge; two pie slices of similar size are harder to rank correctly by eye. When precise comparison between categories matters, a bar chart is the stronger choice. ⟦A.m1 A:tb5⟧

### s04 · check · Scatterplot: exploratory or communicative?  [reward 10]
Quick Check — A scatterplot of delivery distance versus delivery time sits on your screen. Is it ready for the operations manager, or is it still an exploratory tool?
QUESTION [choice, None, grading=client] You have built a scatterplot showing delivery distance vs. delivery time for all orders. The operations manager asks to see it in the presentation. What should you consider before including it?
  ✔ opt_a: Scatterplots are often used to understand data rather than to communicate with it; consider whether a simpler chart type would make the point more directly for this audience.
  ✘ opt_b: Scatterplots are the best choice for showing relationships between two variables, so include it without changes.
      why: Not quite. While scatterplots are useful for exploring relationships, they are often used to understand data rather than to communicate with it. For a non-technical audience, a simpler chart type may make the point more directly.
  ✘ opt_c: Scatterplots are too technical for any stakeholder presentation and should never be used.
      why: Not quite. Scatterplots can be designed to convey findings to an audience, though they are often used to understand data rather than to communicate with it. The key is to consider whether a simpler chart type would make the point more directly for this specific audience.
  ✘ opt_d: The scatterplot is fine as long as you add gridlines to help the manager read exact values.
      why: Not quite. Adding gridlines doesn't address the core issue: scatterplots are often used to understand data rather than to communicate with it. For a non-technical stakeholder, consider whether a simpler chart type would make the point more directly.
  feedback✔: Correct. A scatterplot is often used to understand data rather than to communicate with it, though it can still be designed to convey findings to an audience. For a non-technical stakeholder, consider whether a simpler chart type would make the point more directly.  feedback✘: Review the glossary's guidance on when scatterplots are typically used and consider the audience's familiarity with different chart types.  hints: ['Think about the difference between charts you build for your own exploration versus charts you show to stakeholders.', 'Consider what the glossary says about when scatterplots are typically used.']  remediation→r01
  MEASURES: A:classify_scatterplot_as_exploratory_vs_communicative(f6)   anchors=[]
  taught-before-tested: A.f6←s03

### s05 · hands_on · Match each stakeholder point to the right chart type  [reward 15]
Hands-On Practice — For each point the operations manager wants to make, choose the chart type that best communicates it — and explain why.
QUESTION [classify, None, grading=client] The operations manager needs charts for different stakeholder points. For each point below, classify which chart type best communicates it to a non-technical audience.
  'Which city has the longest average delivery time?' -> Bar chart
  'Lagos accounts for most of our total delivery volume.' -> Pie chart
  'Lagos delivery time is rising week over week.' -> Line graph
  'Compare the distribution of delivery times across all three cities.' -> Bar chart
  feedback✔: Excellent! You matched each stakeholder point to the chart type that best communicates it. Bar charts compare categories, pie charts show part-to-whole relationships, line graphs show trends over time, and for comparing distributions to a non-technical audience, a bar chart (or line graph) often makes the point more directly than a boxplot.  feedback✘: Review which chart types match which stakeholder points: bar charts for comparison, line graphs for trends, pie charts for part-to-whole, and consider audience familiarity with boxplots.  hints: ['Match the chart type to the specific point being made: comparison, trend, part-to-whole, or distribution.', 'Consider whether the audience is familiar with the chart type. Boxplots may introduce a learning curve for non-technical stakeholders.']  remediation→r02
  MEASURES: A:select_chart_type_for_stakeholder_point(f1,f2,f3,f4,f5,f6); A:distinguish_part_to_whole_from_comparison_framing(f4,m1); A:evaluate_audience_readiness_for_boxplot(f3,f5)   anchors=[]
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01; A.f4←s03; A.f5←s01; A.f6←s03; A.f4←s03; A.m1←s03; A.f3←s01; A.f5←s01

### s06 · explainer · Remove the clutter your audience doesn't need  [reward 5]
Simplifying Charts — A chart built for your own exploration can carry gridlines, a border, and precise decimal labels. The operations manager probably doesn't need any of that to get the point.
(intro) A bar chart of city delivery times built during your own exploration can carry gridlines, a border, and precise decimal labels that help you double-check the numbers. The operations manager probably doesn't need any of that to get the point. Each element you remove reduces the visual effort required to read the chart. ⟦B:tb1⟧
(mechanism) Gridlines can be deleted from a chart; if precise values matter to the audience, label the data point directly instead of relying on gridlines. A chart's border can be removed, since it is not adding informative value — white space can differentiate parts of a visual better than a border. ⟦B.f1 B.f2 B:tb2⟧
(mechanism) Data labels should be used sparingly, only where exact values are important; otherwise remove them and use the axis instead. Unnecessary trailing zeroes can be dropped — '22.00' becomes '22 min'. Diagonally rotated axis text is slower to read; city names like Lagos, Abuja, and Kano are short enough to render horizontally. ⟦B.f3 B.f5 B.f6 B:tb3⟧
[BEFORE_AFTER] Five removals — border, gridlines, trailing zeros, rotated labels, per-bar data labels — reduce visual effort without changing the underlying delivery-time values.
  before:
[DIAGRAM: Before: cluttered bar chart] nodes=['Border: visible frame around chart', 'Gridlines: horizontal lines behind bars', 'Axis labels: 0, 10, 20, 30, 40', 'Tick labels: rotated city names', 'Data labels: value on every bar'] edges=[('border', 'gridlines', None), ('gridlines', 'decimals', None), ('decimals', 'rotated', None), ('rotated', 'datalabels', None)] alt: Bar chart with visible border, gridlines, round-number axis labels (0, 10, 20, 30, 40), rotated city-name tick labels, and data labels on every bar — five clutter elements present.
  after:
[DIAGRAM: After: simplified bar chart] nodes=['Border removed — white space separates', 'Gridlines removed', 'Axis labels: 22, 27, 38 min', 'Tick labels: horizontal city names', 'No per-bar data labels — axis used instead'] edges=[('noborder', 'nogridlines', None), ('nogridlines', 'simplified', None), ('simplified', 'horizontal', None), ('horizontal', 'nodata', None)] alt: Bar chart with border removed, gridlines removed, axis labels simplified to 22, 27, 38 min, city-name tick labels horizontal, and no per-bar data labels — same data, less visual effort.

### s07 · video · Decluttering a chart for a non-technical audience
Video — 
[VIDEO Decluttering a chart for a non-technical audience] bridge-before: Watch how each removal reduces reading effort. Note: the presenter uses Excel; the same design principles apply in any charting tool. The clip does not demonstrate labelling a data point directly when precision matters (f1). | bridge-after: The clip shows f2–f6 applied in sequence. Devspace's text also covers f1: when precise values are essential, label the data point directly rather than restoring gridlines.
  - XgY1-BsZSzM 51-393s facts=['f2', 'f3', 'f4', 'f5', 'f6'] label: Removing chart clutter: border, gridlines, trailing zeros, diagonal labels, and excess data labels | summary: The presenter opens by explaining that every chart element adds cognitive burden, and that overwhelming an audience risks losing them entirely — establishing why decluttering matters. Working on a bar chart in Excel, they remove the chart border (noting white space does the job of separation better), delete the gridlines and shaded background, then reformat the y-axis to drop trailing zeros by switching to thousands units with a 'k' suffix. They then abbreviate the diagonal month labels on the x-axis to horizontal text, citing research that diagonal text takes fifty percent longer to read. Finally, they weigh whether exact values are needed: deciding they are not, they delete all data labels and keep the y-axis instead, leaving a much cleaner chart.
(tip) Reducing clutter lets the audience use their attention to decide what actions might be warranted, rather than working out how to read the graph. ⟦B.f4 B:tb4⟧

### s08 · check · Which elements should you remove to reduce chart clutter?  [reward 10]
Quick Check — The operations manager will see this bar chart in a slide deck. Identify which elements add visual effort without adding information.
QUESTION [choice, None, grading=client] A bar chart of city delivery times has a visible border, gridlines, trailing-zero axis labels (e.g. '22.00 minutes'), rotated city-name tick labels, and data labels on every bar. Which elements should you remove to reduce chart clutter for the operations manager?
  ✔ opt_a: Remove the border, gridlines, trailing zeros, rotated labels, and per-bar data labels — all add visual effort without adding information.
  ✘ opt_b: Keep the gridlines and border to help the manager read exact values; remove only the data labels.
      why: Not quite. Gridlines can be deleted; if precise values matter, label the data point directly instead. A chart border is not adding informative value — white space separates parts of a visual better than a border. Trailing zeros and rotated labels also add visual effort without adding information.
  ✘ opt_c: Remove only the border and gridlines; keep the trailing zeros and rotated labels for precision.
      why: Not quite. Trailing zeros can be dropped from axis labels (e.g. '22.00' becomes '22 min'), and diagonally rotated axis text is slower to read — labels can be abbreviated so they render horizontally instead. Both add visual effort without adding information.
  ✘ opt_d: Remove the gridlines but keep the border to separate the chart from the slide background.
      why: Not quite. A chart border is not adding informative value — white space can differentiate parts of a visual better than a border. Removing the border reduces one more element the audience must look past to reach the data.
  feedback✔: Correct. All five elements — border, gridlines, trailing zeros, rotated labels, and per-bar data labels — add visual effort without adding information. Removing them reduces clutter and lets the audience use their attention to decide what actions might be warranted, rather than working out how to read the graph.  feedback✘: Review which chart elements add visual effort without adding information, and consider the role of white space in separating visual elements.  hints: ['Consider which elements add visual effort without adding information.', 'Think about what the glossary says about gridlines, borders, trailing zeros, rotated labels, and data labels.']  remediation→r03
  MEASURES: B:identify_clutter_elements_to_remove(f1,f2,f3,f5,f6); B:explain_cognitive_benefit_of_reducing_chart_clutter(f4)   anchors=[]
  taught-before-tested: B.f1←s06; B.f2←s06; B.f3←s06; B.f5←s06; B.f6←s06; B.f4←s07

### s09 · check · Why remove the chart border?  [reward 10]
Quick Check — A colleague says the border helps separate the chart from the slide background. What is the better alternative, and why?
QUESTION [choice, None, grading=client] A colleague says the chart border helps separate the chart from the slide background. What is the better alternative, and why?
  ✔ opt_a: White space can differentiate parts of a visual better than a border; the border is not adding informative value, just one more element the eye must process.
  ✘ opt_b: The border is essential for separation; without it, the chart would blend into the slide.
      why: Not quite. A chart border is not adding informative value. White space around the chart already differentiates it from the surrounding content, and does so better than a border. Removing the border reduces one more element the audience must look past to reach the data.
  ✘ opt_c: Add a thicker border and a shadow effect to make the separation even clearer.
      why: Not quite. Adding more visual elements (thicker border, shadow) increases clutter rather than reducing it. White space can differentiate parts of a visual better than a border, and the border is not adding informative value.
  ✘ opt_d: Keep the border but make it a lighter color so it is less distracting.
      why: Not quite. Even a lighter border is still an element the eye must process. A chart border is not adding informative value — white space can differentiate parts of a visual better than a border. Removing the border entirely reduces one more element the audience must look past to reach the data.
  feedback✔: Correct. A chart border is not adding informative value — it is adding a line the eye must process. White space around the chart already differentiates it from the surrounding content. Removing the border reduces one more element the audience must look past to reach the data.  feedback✘: Review the role of white space in visual design and consider what the border is actually adding to the chart.  hints: ['Think about what the border is actually adding to the chart.', 'Consider what the glossary says about white space and borders.']  remediation→r04
  MEASURES: B:justify_border_removal_using_white_space(f2)   anchors=[]
  taught-before-tested: B.f2←s06

### s10 · hands_on · Simplify a chart for the operations manager  [reward 15]
Hands-On Practice — A bar chart of city delivery times has a border, gridlines, trailing-zero axis labels, rotated city-name tick labels, and data labels on every bar. Simplify it for a non-technical audience.
QUESTION [classify, None, grading=client] A bar chart of city delivery times has several clutter elements. For each element below, classify whether it should be removed or kept for the operations manager.
  'Chart border' -> Remove — adds visual effort without adding information
  'Gridlines' -> Remove — adds visual effort without adding information
  'Trailing zeros on axis labels (e.g. '22.00 minutes')' -> Remove — adds visual effort without adding information
  'Diagonally rotated city-name tick labels' -> Remove — adds visual effort without adding information
  'Data labels on every bar (when the axis shows approximate values)' -> Remove — adds visual effort without adding information
  feedback✔: Excellent! All five elements should be removed. The border is not adding informative value — white space separates better. Gridlines can be deleted; if precise values matter, label the data point directly. Trailing zeros can be dropped from axis labels. Diagonally rotated text is slower to read — abbreviate labels so they render horizontally. Data labels should be used sparingly, only where exact values are important; otherwise use the axis instead.  feedback✘: Review which chart elements add visual effort without adding information, and consider when data labels and gridlines are truly necessary.  hints: ['Consider which elements add visual effort without adding information.', 'Think about what the glossary says about each element: gridlines, borders, trailing zeros, rotated labels, and data labels.']  remediation→r03
  MEASURES: B:choose_between_data_labels_and_axis_for_precision(f1,f3); B:simplify_axis_labels_for_readability(f5,f6)   anchors=[]
  taught-before-tested: B.f1←s06; B.f3←s06; B.f5←s06; B.f6←s06

### s11 · recap · What you've learned: matching and simplifying charts  [reward 5]
Recap — 
(takeaway) Chart choice is driven by the point you are making, not the data alone. Bar charts compare categories; line graphs show trends; pie charts express part-to-whole relationships. Once the right chart is chosen, remove every element that adds visual effort without adding information — border, gridlines, trailing zeros, rotated labels, unnecessary data labels. Reducing clutter lets the audience use their attention to decide what actions are warranted, rather than working out how to read the graph. ⟦B.f4 B:tb4⟧
[UP NEXT] Up next: Presentation Structure: You will learn how to structure a stakeholder presentation — opening with the business question, building the body around your findings, and closing with a call to action.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Scatterplots: exploratory vs. communicative — a closer look
(mechanism) A scatterplot is often used to understand data rather than to communicate with it. When you plot delivery distance against delivery time for yourself, you are exploring a relationship. That same chart can be designed to convey a finding to an audience — but it is not the default choice for a non-technical stakeholder presentation, because the audience must first understand what a scatterplot shows before they can read the point. If the relationship needs to go in front of the operations manager, consider whether a simpler chart can make the same point. ⟦A.f6 A:tb4⟧
### r02 · Matching chart type to stakeholder point — a contrast
(mechanism) Bar charts compare values across categories — use one when the point is 'Lagos takes longer than Abuja.' Line graphs show how a value changes over time — use one when the point is 'Lagos delivery time has risen each week.' Pie charts express part-to-whole relationships — use one when the point is 'Lagos accounts for most of our total order volume' and the values sum to 100% (Lagos 57.1%, Abuja 28.6%, Kano 14.3%). Boxplots compare distributions but may be unfamiliar to non-technical audiences; a bar chart or line plot can often make the same point more directly. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3⟧
(misconception) Comparing pie slices looks easy, but it is not as easy as comparing bar lengths. A bar chart's common baseline makes differences immediately readable; two similar-sized pie slices are hard to rank correctly by eye. When precise comparison between categories matters, a bar chart is the stronger choice. ⟦A.m1 A:tb5⟧
### r03 · Clutter elements and why they slow your audience down
(mechanism) Every element in a chart that does not add information adds cognitive effort. Gridlines can be deleted; if precise values matter, label the data point directly instead. A chart border is not adding informative value — white space separates parts of a visual better than a border. Data labels should be used sparingly, only where exact values are important; otherwise use the axis. Trailing zeroes on axis labels ('22.00') can be dropped ('22 min'). Diagonally rotated axis text is slower to read; abbreviate labels so they render horizontally. ⟦B.f1 B.f2 B.f3 B.f5 B.f6 B:tb2 B:tb3⟧
(takeaway) Reducing clutter lets the audience use their attention to decide what actions might be warranted, rather than working out how to read the graph. None of these changes alter the underlying delivery-time values — only how much visual effort it takes to read them. ⟦B.f4 B:tb4⟧
### r04 · Border removal and white space — why it works
(mechanism) A chart border might seem to help by visually containing the chart on the slide. But the border is not adding informative value — it is adding a line the eye must process. White space around the chart already differentiates it from the surrounding content. Removing the border reduces one more element the audience must look past to reach the data. The same principle applies to gridlines: if the audience needs a precise value, label that data point directly rather than restoring the gridlines. ⟦B.f1 B.f2 B:tb2⟧

## OTHER CONTENT (fields without a dedicated renderer)
· buckets.label: Keep — essential for reading the chart