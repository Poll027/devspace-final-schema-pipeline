# EVALUATOR PACKET — Chart Types (tile_spreadsheet_chart_types)
Tile summary: Build bar, line, and pie charts from Orders data to visualise comparisons, trends, and part-of-whole shares.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = spreadsheet.bar_chart_creation — Bar chart creation
B = spreadsheet.line_chart_creation — Line chart creation
C = spreadsheet.pie_chart_creation — Pie chart creation

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=4
  warn: tile_spreadsheet_chart_types.s09: remediation tile_spreadsheet_chart_types.r02 re-teaches ['spreadsheet.line_chart_creation#f1'] but the check measures ['spreadsheet.line_chart_creation#f2'] — a learner who fails it is sent to an unrelated fact
  warn: tile_spreadsheet_chart_types.s01: text contains the name of blocked future concept viz.bar_charts ('bar charts') — check it is not needed to understand
  warn: tile_spreadsheet_chart_types.s14: text contains the name of blocked future concept viz.bar_charts ('bar charts') — check it is not needed to understand
  warn: tile_spreadsheet_chart_types.s14: prose block without lineage.fact_ids

## SOURCE FACTS — A (spreadsheet.bar_chart_creation)   objective: Build a bar chart from a summary table, arranging category and value data in columns or rows before inserting the chart.
A.f1: Bar charts illustrate comparisons among individual items; in a bar chart, the categories are typically organized along one axis and the values along the other.   [sources: excel_chart_types_guide#Bar chart]
A.f2: To create a chart, select the data for the chart, select Insert > Recommended Charts, and select a chart on the Recommended Charts tab to preview it; if you don't see a bar chart you like, select the All Charts tab to see all chart types, select the chart, and select OK.   [sources: excel_create_chart_guide#Create a chart from start to finish]
PRACTICE ANCHOR (spreadsheet): Given a summary table with a Region column and a Total Sales column, build a bar chart that places regions on one axis and total sales values on the other, using Insert > Recommended Charts.  SUCCESS: A bar chart is present in the workbook with regions on the category axis and total sales values represented by bar lengths, created through the Insert > Recommended Charts workflow.
ASSESSMENT ANCHOR: identify_bar_chart_axis_encoding facts=['f1']
ASSESSMENT ANCHOR: create_bar_chart_via_insert_recommended_charts facts=['f2']
ASSESSMENT ANCHOR: build_correctly_encoded_bar_chart_from_categorical_summary_data facts=['f1', 'f2']

## SOURCE FACTS — B (spreadsheet.line_chart_creation)   objective: Build a line chart from time-ordered data to show a trend across the sequence.
B.f1: In a line chart, category data is distributed evenly along the horizontal axis and value data along the vertical axis; line charts can show continuous data over time on an evenly scaled axis, making them well suited to showing trends at equal intervals such as months, quarters, or fiscal years.   [sources: excel_chart_types_guide#Line chart]
B.f2: To create a chart, select the data for the chart, select Insert > Recommended Charts, and select a chart on the Recommended Charts tab to preview it; if you don't see a line chart you like, select the All Charts tab to see all chart types, select the chart, and select OK.   [sources: excel_create_chart_guide#Create a chart from start to finish]
PRACTICE ANCHOR (spreadsheet): Given a table of monthly revenue figures for a 12-month period, build a line chart that places months on the horizontal axis and revenue on the vertical axis using Insert > Recommended Charts.  SUCCESS: A line chart is present on the sheet with months distributed evenly along the horizontal axis and revenue values on the vertical axis, created through the Insert > Recommended Charts workflow.
ASSESSMENT ANCHOR: identify_axis_roles_and_interval_suitability facts=['f1']
ASSESSMENT ANCHOR: create_line_chart_via_insert_recommended_charts facts=['f2']
ASSESSMENT ANCHOR: build_correctly_encoded_line_chart_from_time_ordered_data facts=['f1', 'f2']

## SOURCE FACTS — C (spreadsheet.pie_chart_creation)   objective: Build a pie chart that shows each category's share of a single total.
C.f1: Pie charts show the size of items in one data series proportional to the sum of the items, and are appropriate when you have only one data series to plot, none of the values are negative, there are no more than seven categories, and the categories represent parts of the whole pie.   [sources: excel_chart_types_guide#Pie chart]
C.f2: To create a chart, select the data for the chart, select Insert > Recommended Charts, and select a chart on the Recommended Charts tab to preview it; if you don't see a pie chart you like, select the All Charts tab to see all chart types, select the chart, and select OK.   [sources: excel_create_chart_guide#Create a chart from start to finish]
PRACTICE ANCHOR (spreadsheet): Given a small table of product category names and their total revenue figures (values are positive, categories number seven or fewer, and they sum to a meaningful whole), build a pie chart that shows each category's share of total revenue using Insert > Recommended Charts.  SUCCESS: A pie chart is present in the workbook, each category appears as a correctly proportioned slice, all slices together represent 100% of total revenue, and the chart was produced via the Insert > Recommended Charts workflow.
ASSESSMENT ANCHOR: identify_pie_chart_eligibility_conditions facts=['f1']
ASSESSMENT ANCHOR: build_correctly_encoded_pie_chart_from_category_totals facts=['f1', 'f2']

## DATA ASSETS USED
asset_city_totals: City order totals — bar and pie chart source — columns: city(categorical), total_amount(numerical)
   ["Lagos",28200.0]
   ["Abuja",23000.0]
   ["Kano",12800.0]
   ["Port Harcourt",17900.0]
   ["Ibadan",9700.0]
   ["Enugu",7700.0]
asset_monthly_summary: Monthly order totals — line chart source — columns: month_label(categorical), total_amount(numerical)
   ["Jan-2024",312000.0]
   ["Feb-2024",287500.0]
   ["Mar-2024",341200.0]
   ["Apr-2024",298700.0]
   ["May-2024",375400.0]
   ["Jun-2024",362100.0]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjusting figure size and layout; Bar charts; Basic A/B test structure (control vs treatment group); Basic plot creation with the pyplot interface; Box plots; Conceptual effect of sample size on confidence; Conceptual interpretation of statistical significance/confidence level; Converting a vague business question into a specific, measurable analytical question; Custom styling/theming (advanced/optional); Drawing a business conclusion from an experiment-result summary; Histograms; Identifying stakeholder needs/requirements before analysis; Identifying the business decision a stakeholder needs the analysis to inform; Interpreting lift/percentage change between groups; Labeling axes, titles, and legends; Line chart creation; Line plots; Making a data-driven recommendation; Matching chart type to the analytical question; Multi-panel figures/subplots (advanced/optional); Pie chart creation; Plotting directly from pandas DataFrames with seaborn; Scatter plots; Stating a finding precisely and quantitatively (the specific number or comparison, not a vague claim); matplotlib figure and axes object model; seaborn built-in themes and color palettes; seaborn statistical plotting functions

## LESSON, in learner order

### s01 · explainer · Bar Charts: Comparing Categories  [reward 5]
Concept — A bar chart places categories on one axis and values on the other to show comparisons at a glance.
(definition) Bar charts illustrate comparisons among individual items; in a bar chart, the categories are typically organised along one axis and the values along the other. A summary table of total order amount by city is exactly the kind of category-versus-value data a bar chart compares. ⟦A.f1 A:tb1⟧
(mechanism) To create a chart, select the data, choose Insert > Recommended Charts, and select a chart on the Recommended Charts tab to preview it. If you don't see a bar chart you like, select the All Charts tab to see all chart types, select the chart, and click OK. ⟦A.f2 A:tb2⟧
[TABLE asset_city_totals cols=['city', 'total_amount'] tags=city:Category axis, total_amount:Bar height (NGN)] caption: City order totals — source data for a bar chart. Each city is a category; total_amount is the value.

### s02 · video · Building a Bar Chart in Excel  [reward 3]
Watch — See how to select data and insert a bar chart from the Charts group.
[VIDEO Building a bar chart in Excel: selecting data and reading the result] bridge-before: Watch how each clip selects data first, then uses the Insert tab to add a chart. Note: Excel labels these 'column' charts; Devspace calls them bar charts. Neither clip uses Insert > Recommended Charts — that path is in the text. | bridge-after: The first clip shows filtering out totals that skew the chart; the second shows fixing category order. The Recommended Charts and All Charts tab route — the full f2 path — is covered in the text above.
  - gMAHXrty6wI 136-359s facts=['f1'] label: Selecting data and inserting a column/bar chart from the Charts group | summary: The presenter highlights a monthly sales table, opens the Insert tab, and picks a 2-D column chart directly from the Charts gallery. After inserting, they explore chart style options and the Switch Row/Column toggle to flip which dimension appears on each axis. They then use the chart's filter to remove a totals row and a year-end total column that were distorting the scale, apply the change, and add a title. The finished chart shows months along the horizontal axis and bar heights representing product quantities, making it easy to see that paper is the top-selling product every month.
  - RY526I9h2SE 0-58s facts=['f2'] label: Insert > Column Chart button: selecting data and fixing category order | summary: Starting from a selected data range, the presenter goes to the Insert tab, clicks the Column Chart button, and chooses the bar chart option. They immediately notice that the category axis lists items in the reverse of the source data order. To fix this, they select the axis, press Ctrl+1 to open Format Axis, and check 'Categories in reverse order', restoring the original top-to-bottom sequence from the data.

### s03 · check · Building a Bar Chart from Category Data  [reward 5]
Quick Check — Test your understanding of bar chart axis encoding and the Insert > Recommended Charts workflow.
QUESTION [choice, intro, grading=client] You have a table with two columns: city and total_amount. You want to create a bar chart to compare total order amounts across cities. Which axis encoding is correct for a bar chart?
  ✔ opt_a: Cities on the category axis; total_amount values represented by bar lengths on the value axis.
  ✘ opt_b: total_amount values on the category axis; cities represented by bar lengths on the value axis.
      why: In a bar chart, categories (like city names) go on the category axis, and numeric values (like total_amount) are represented by bar lengths on the value axis — not the other way around.
  ✘ opt_c: Cities on both axes, with total_amount shown as a colour gradient.
      why: Bar charts do not use colour gradients to encode values. The category axis holds the category labels (cities) and the value axis holds the numeric values (total_amount), shown as bar lengths.
  ✘ opt_d: total_amount on both axes, with cities shown as data labels inside the bars.
      why: Both axes cannot hold the same type of data. The category axis holds category labels (cities) and the value axis holds numeric values (total_amount) represented by bar lengths.
  feedback✔: Correct! In a bar chart, categories (city names) are organised along the category axis and numeric values (total_amount) are represented by bar lengths along the value axis.  feedback✘: In a bar chart, categories go on the category axis and numeric values are shown as bar lengths on the value axis. Cities are the categories; total_amount is the value.  hints: ['A bar chart compares items: the items (categories) go on one axis, and their values (shown as bar lengths) go on the other.', 'Ask yourself: what am I comparing? Those are the categories. What am I measuring? That is the value axis.']  remediation→r01
  MEASURES: A:build_correctly_encoded_bar_chart_from_categorical_summary_data(f1,f2)   anchors=['assessment:build_correctly_encoded_bar_chart_from_categorical_summary_data']
  taught-before-tested: A.f1←s01; A.f2←s01

### s04 · hands_on · Build a Bar Chart from City Totals  [reward 10]
Practice — Select the city totals table and insert a bar chart using Insert > Recommended Charts.
QUESTION [formula_entry, core, grading=client] The city_totals sheet has city names in column A (A2:A7) and total order amounts in column B (B2:B7). A bar chart of this data would place cities on the category axis and total amounts as bar lengths on the value axis. In cell C1, write a formula that returns the sum of all total_amount values in B2:B7 — the grand total that would appear in the chart's data range.
  [unrendered interaction type formula_entry] public={"prompt":"The city_totals sheet has city names in column A (A2:A7) and total order amounts in column B (B2:B7). A bar chart of this data would place cities on the category axis and total amounts as bar lengths on the value axis. In cell C1, write a formula that returns the sum of all total_amount values in B2:B7 — the grand total that would appear in the chart's data range.","asset_ref":{"asset_id":"asset_city_totals","variant_id":null},"sheet_name":"city_totals","target_cell":"C1","allowed_functions":["SUM"]} grading={"expected_value":99300.0,"reference_formula":"=SUM(B2:B7)","must_use_functions":["SUM"],"forbid_hardcoded_values":true}
  feedback✔: Correct! =SUM(B2:B7) returns 99300 — the grand total of all city amounts. The bar chart would use B2:B7 as its value data, with each city's bar length proportional to its share of this total.  feedback✘: Use SUM with the total_amount range: =SUM(B2:B7). The city_totals sheet has 6 cities in rows 2 through 7.  hints: ['The total_amount values are in column B, rows 2 through 7 (one row per city).', '=SUM(B2:B7) adds up all six city totals.']  remediation→r01
  MEASURES: A:identify_bar_chart_axis_encoding(f1); A:create_bar_chart_via_insert_recommended_charts(f2)   anchors=['practice', 'assessment:identify_bar_chart_axis_encoding', 'assessment:create_bar_chart_via_insert_recommended_charts']
  taught-before-tested: A.f1←s01; A.f2←s01

### s05 · explainer · Line Charts: Showing Trends Over Time  [reward 5]
Concept — A line chart distributes evenly-spaced time intervals along the horizontal axis and values along the vertical axis.
(definition) In a line chart, category data is distributed evenly along the horizontal axis and value data along the vertical axis. Line charts can show continuous data over time on an evenly scaled axis, making them well suited to showing trends at equal intervals such as months, quarters, or fiscal years. A summary of total order amount by month is exactly this kind of evenly-spaced, time-ordered data. ⟦B.f1 B:tb1⟧
(mechanism) To create a line chart, select the data, choose Insert > Recommended Charts, and select a chart on the Recommended Charts tab to preview it. If you don't see a line chart you like, select the All Charts tab to see all chart types, select the chart, and click OK. ⟦B.f2 B:tb2⟧
[TABLE asset_monthly_summary cols=['month_label', 'total_amount'] tags=month_label:Horizontal axis (equal intervals), total_amount:Vertical axis (NGN)] caption: Monthly order totals — source data for a line chart. Each month is evenly spaced on the horizontal axis; total_amount maps to the vertical axis.

### s06 · video · Building a Line Chart from Monthly Sales Data  [reward 3]
Watch — See how to assign the data range and set the horizontal-axis labels.
[VIDEO Building a line chart from monthly sales data] bridge-before: Watch how the instructor assigns the data range after inserting the chart, and note which cells become the horizontal-axis labels versus the y-axis values. | bridge-after: The clip selects data after inserting; Devspace's text covers selecting data first. The clip does not state why equal intervals suit line charts — the teaching text covers that.
  - FnvE1SF1Wx0 82-360s facts=['f1', 'f2'] label: Inserting a line chart and assigning the data range | summary: The instructor starts with a single-row sales table spanning October through June, with monthly columns. From the Insert menu, Recommended Charts is opened and a 2D line chart with markers is chosen — noting that 3D variants should be avoided. Because no data was selected beforehand, a blank chart appears; right-clicking inside it and choosing Select Data lets the instructor drag cells A1 through J3 as the chart range. The series name and its y-axis values are confirmed, then the horizontal-axis label range is narrowed from B1:J2 down to B2:J2 to remove a two-level header and show only the month names. Clicking OK produces the finished chart.

### s07 · check · Axis Roles and Interval Suitability  [reward 5]
Quick Check — Test your understanding of which axis carries time intervals and when a line chart is appropriate.
QUESTION [choice, intro, grading=client] Which of the following datasets is best suited for a line chart, and why?
  ✔ opt_a: Monthly revenue totals for Jan through Jun 2024 — because the data is time-ordered at equal intervals, making a line chart ideal for showing the trend.
  ✘ opt_b: Total order amounts by city — because cities are categories and a line chart connects them with a line.
      why: Cities are unordered categories, not time-ordered intervals. A line connecting unordered categories implies a trend that does not exist. A bar chart is better for comparing city totals.
  ✘ opt_c: A single order's delivery time — because a line chart can show a single data point.
      why: A single data point cannot show a trend. Line charts are suited to continuous data over time at equal intervals — multiple points that form a meaningful sequence.
  ✘ opt_d: Driver names and their order counts — because a line chart works for any two-column dataset.
      why: Driver names are unordered categories, not time-ordered intervals. Connecting them with a line would imply a trend that does not exist. A bar chart is more appropriate.
  feedback✔: Correct! Monthly revenue at equal time intervals (Jan, Feb, Mar…) is exactly the kind of data a line chart is designed for — it shows the trend across evenly spaced time points.  feedback✘: Line charts are suited to continuous data over time at equal intervals (months, quarters, years). Unordered categories like cities or driver names should use a bar chart instead.  hints: ['Ask: is the horizontal axis a time sequence with equal spacing? If yes, a line chart works well.', 'A line connecting unordered categories (like cities) implies a trend that does not exist — that is a misuse of a line chart.']  remediation→r02
  MEASURES: B:identify_axis_roles_and_interval_suitability(f1)   anchors=['assessment:identify_axis_roles_and_interval_suitability']
  taught-before-tested: B.f1←s05

### s08 · check · Building a Line Chart from Time-Ordered Data  [reward 5]
Quick Check — Apply your knowledge of axis encoding and the Recommended Charts workflow.
QUESTION [choice, core, grading=client] You have monthly revenue data: month labels in column A (Jan-2024 through Jun-2024) and total amounts in column B. You create a line chart using Insert > Recommended Charts. Which statement correctly describes the resulting chart?
  ✔ opt_a: Month labels are distributed evenly along the horizontal axis; revenue values are plotted on the vertical axis, connected by a line showing the trend over time.
  ✘ opt_b: Revenue values are distributed along the horizontal axis; month labels appear on the vertical axis.
      why: In a line chart, category data (month labels) is distributed along the horizontal axis and value data (revenue) is plotted on the vertical axis — not the other way around.
  ✘ opt_c: Both axes show revenue values; month labels appear as data point labels on the line.
      why: The horizontal axis holds category data (month labels), not revenue values. Revenue values are plotted on the vertical axis.
  ✘ opt_d: The chart shows bars instead of a line because monthly data always produces a bar chart.
      why: Monthly data does not automatically produce a bar chart. When you select the data and use Insert > Recommended Charts, Excel recommends a line chart for evenly spaced time-series data.
  feedback✔: Correct! In a line chart, category data (month labels) is distributed evenly along the horizontal axis and value data (revenue) is plotted on the vertical axis, with points connected by a line.  feedback✘: In a line chart, the horizontal axis holds the category data (month labels) evenly spaced, and the vertical axis holds the value data (revenue). The line connects the data points to show the trend.  hints: ['Remember: horizontal axis = category data (months); vertical axis = value data (revenue).', 'The line connects the data points in order, showing how revenue changes from month to month.']  remediation→r02
  MEASURES: B:build_correctly_encoded_line_chart_from_time_ordered_data(f1,f2)   anchors=['assessment:build_correctly_encoded_line_chart_from_time_ordered_data']
  taught-before-tested: B.f1←s05; B.f2←s05

### s09 · hands_on · Build a Line Chart from Monthly Totals  [reward 10]
Practice — Select the monthly summary table and insert a line chart using Insert > Recommended Charts.
QUESTION [formula_entry, core, grading=client] The monthly_summary sheet has month labels in column A (A2:A7, Jan-2024 through Jun-2024) and total order amounts in column B (B2:B7). A line chart of this data would place months evenly along the horizontal axis and revenue values on the vertical axis. In cell C1, write a formula that returns the sum of all monthly totals in B2:B7 — the grand total across all six months.
  [unrendered interaction type formula_entry] public={"prompt":"The monthly_summary sheet has month labels in column A (A2:A7, Jan-2024 through Jun-2024) and total order amounts in column B (B2:B7). A line chart of this data would place months evenly along the horizontal axis and revenue values on the vertical axis. In cell C1, write a formula that returns the sum of all monthly totals in B2:B7 — the grand total across all six months.","asset_ref":{"asset_id":"asset_monthly_summary","variant_id":null},"sheet_name":"monthly_summary","target_cell":"C1","allowed_functions":["SUM"]} grading={"expected_value":1976900.0,"reference_formula":"=SUM(B2:B7)","must_use_functions":["SUM"],"forbid_hardcoded_values":true}
  feedback✔: Correct! =SUM(B2:B7) returns 1976900 — the total revenue across all six months. The line chart would use B2:B7 as its value data, with each month's point plotted on the vertical axis.  feedback✘: Use SUM with the total_amount range: =SUM(B2:B7). The monthly_summary sheet has 6 months in rows 2 through 7. To create a line chart from this data, select A1:B7, then go to Insert → Recommended Charts and choose the Line chart option.  hints: ['The total_amount values are in column B, rows 2 through 7 (one row per month).', '=SUM(B2:B7) adds up all six monthly totals.']  remediation→r02
  MEASURES: B:create_line_chart_via_insert_recommended_charts(f2)   anchors=['practice', 'assessment:create_line_chart_via_insert_recommended_charts']
  taught-before-tested: B.f2←s05

### s10 · explainer · Pie Charts: Part-of-Whole Shares  [reward 5]
Concept — A pie chart shows each category's share of a total — but only when the data meets four conditions.
(definition) Pie charts show the size of items in one data series proportional to the sum of the items. They are appropriate when you have only one data series to plot, none of the values are negative, there are no more than seven categories, and the categories represent parts of the whole pie. A summary of total order amount by city, for no more than seven cities, fits that description as long as no amount is negative. ⟦C.f1 C:tb1⟧
(mechanism) To create a pie chart, select the data, choose Insert > Recommended Charts, and select a chart on the Recommended Charts tab to preview it. If you don't see a pie chart you like, select the All Charts tab to see all chart types, select the chart, and click OK. ⟦C.f2 C:tb2⟧
[CHART pie: Total Order Amount by City (NGN)] data=asset_city_totals x=city y=total_amount color=None annotations=[] alt: Pie chart showing six slices, one per city. Lagos is the largest slice, followed by Abuja, Port Harcourt, Kano, Ibadan, and Enugu. Each slice is labelled with the city name and its share of total order amount.

### s11 · video · When a Pie Chart Works: Proportional Slices  [reward 3]
Watch — See how even-split versus clear-winner data affects whether a pie chart communicates clearly.
[VIDEO When a pie chart works: proportional slices and the 'clear winner' pattern] bridge-before: Watch how the proportional-slice idea plays out in practice. Note: the clip does not cover the full eligibility checklist (one series, no negatives, up to seven categories) — the text covers those. | bridge-after: The clip shows when a pie chart communicates clearly. The text adds the complete eligibility rules and the step-by-step creation process the clip omits.
  - VgBxnayDXk0 38-198s facts=['f1'] label: Pie chart as part-of-whole: even-split versus clear-winner examples | summary: A pie chart displays each category's share of a total, where all slices together represent 100%. The presenter contrasts two scenarios: an 'even split' chart where slices are nearly equal and the story is hard to read, versus a 'clear winner' chart where grouping categories into two or three slices makes one dominant share immediately obvious. The even-split example is also shown remade as a bar chart to illustrate when ranking matters more than part-of-whole. The clear-winner examples show how reducing and grouping categories sharpens the message.

### s12 · check · Building a Pie Chart from Category Totals  [reward 5]
Quick Check — Test your understanding of pie chart eligibility conditions and the creation workflow.
QUESTION [choice, core, grading=client] You have city order totals for 6 cities, all amounts positive. You select the data and use Insert > Recommended Charts to create a pie chart. Which statement correctly describes the resulting chart?
  ✔ opt_a: Each city appears as a slice; each slice's size is proportional to that city's share of the total amount; all slices together represent 100% of total revenue.
  ✘ opt_b: Each city appears as a bar; bar lengths represent the city's total amount; the chart shows absolute values, not proportions.
      why: That describes a bar chart, not a pie chart. A pie chart shows proportions: each slice's size represents that category's share of the whole, and all slices together equal 100%.
  ✘ opt_c: Each city appears as a point on a line; the line shows how city totals change from city to city.
      why: That describes a line chart. A pie chart shows proportions as slices of a circle, not points on a line.
  ✘ opt_d: Each city appears as a slice, but slices are equal in size because pie charts do not encode values.
      why: Pie chart slices are not equal — they are sized proportionally to each category's value. A slice for Lagos (the largest city total) would be larger than a slice for Enugu (the smallest).
  feedback✔: Correct! In a pie chart, each category is a slice sized proportionally to its share of the total. All slices together represent 100% of the data series.  feedback✘: A pie chart shows proportions: each slice represents one category's share of the whole, sized proportionally to its value. All slices together equal 100%.  hints: ["The key word for pie charts is 'proportional' — each slice's size shows that category's fraction of the total.", "All slices together must equal 100% of the data series — that is what makes it a 'pie'."]  remediation→r03
  MEASURES: C:build_correctly_encoded_pie_chart_from_category_totals(f1,f2)   anchors=['assessment:build_correctly_encoded_pie_chart_from_category_totals']
  taught-before-tested: C.f1←s10; C.f2←s10

### s13 · hands_on · Build a Pie Chart from City Totals  [reward 10]
Practice — Select the city totals table and insert a pie chart using Insert > Recommended Charts.
QUESTION [formula_entry, stretch, grading=client] The city_totals sheet has city names in A2:A7 and total amounts in B2:B7. A pie chart is appropriate here because there is only one data series, all values are positive, and the number of categories does not exceed seven. In cell C1, write a formula that counts the number of city labels in A2:A7 — confirming that the category count is within the pie chart eligibility limit.
  [unrendered interaction type formula_entry] public={"prompt":"The city_totals sheet has city names in A2:A7 and total amounts in B2:B7. A pie chart is appropriate here because there is only one data series, all values are positive, and the number of categories does not exceed seven. In cell C1, write a formula that counts the number of city labels in A2:A7 — confirming that the category count is within the pie chart eligibility limit.","asset_ref":{"asset_id":"asset_city_totals","variant_id":null},"sheet_name":"city_totals","target_cell":"C1","allowed_functions":["COUNTA"]} grading={"expected_value":6,"reference_formula":"=COUNTA(A2:A7)","must_use_functions":["COUNTA"],"forbid_hardcoded_values":true}
  feedback✔: Correct! =COUNTA(A2:A7) returns 6 — there are 6 cities, which is within the seven-category limit for pie charts. With all positive values and a single data series, this dataset meets all pie chart eligibility conditions.  feedback✘: Use COUNTA to count the city labels in A2:A7: =COUNTA(A2:A7). COUNTA counts non-empty cells, including text labels.  hints: ['COUNTA counts all non-empty cells, including text. Use it to count the city names in A2:A7.', 'The pie chart eligibility rule says no more than seven categories. COUNTA(A2:A7) tells you how many categories there are.']  remediation→r03
  MEASURES: C:identify_pie_chart_eligibility_conditions(f1); C:build_correctly_encoded_pie_chart_from_category_totals(f1,f2)   anchors=['practice', 'assessment:identify_pie_chart_eligibility_conditions', 'assessment:build_correctly_encoded_pie_chart_from_category_totals']
  taught-before-tested: C.f1←s10; C.f1←s10; C.f2←s10

### s14 · recap · Chart Types — Key Points  [reward 5]
Recap — You can now build bar, line, and pie charts and choose the right type for your data.
(takeaway) Bar charts compare categories: the category axis holds labels and the value axis holds bar heights. Line charts show trends over equal time intervals: months, quarters, or fiscal years go on the horizontal axis and values on the vertical axis. Pie charts show part-of-whole shares and require one data series, no negative values, no more than seven categories, and categories that sum to a meaningful whole. For all three types, select the data and use Insert > Recommended Charts to preview and insert.
[UP NEXT] Next: Python Figures and Layouts: In the next tile you'll move from spreadsheet charts to Python's matplotlib, building figures with axes and controlling layout programmatically.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Bar Chart Axis Encoding and Creation Steps — A clear contrast shows which data goes on which axis and how to insert the chart.
(example) In a bar chart, categories go on one axis and values on the other. For the city totals table, city names go on the category axis and total_amount values determine bar height. To insert: select the city and total_amount columns, choose Insert > Recommended Charts, preview the bar chart, and click OK. If the bar chart is not on the Recommended tab, open All Charts, select Bar, and click OK. ⟦A.f1 A.f2 A:tb1 A:tb2⟧
### r02 · Line Chart Axis Roles and When to Use One — Equal time intervals on the horizontal axis make a line chart the right choice.
(example) In a line chart, category data — typically time labels such as Jan-2024, Feb-2024 — is distributed evenly along the horizontal axis, and value data goes on the vertical axis. Line charts are well suited to data measured at equal intervals: months, quarters, or fiscal years. The monthly summary table has six months at equal intervals, so a line chart shows the trend clearly. A table of city totals is not time-ordered, so a bar chart is more appropriate there. ⟦B.f1 B:tb1⟧
### r03 · Pie Chart Eligibility and Creation — Four conditions must hold before a pie chart is appropriate.
(example) A pie chart is appropriate when: (1) you have only one data series to plot, (2) none of the values are negative, (3) there are no more than seven categories, and (4) the categories represent parts of the whole. The city totals table has six cities (≤ 7), all positive amounts, one series, and the cities together represent all orders — so a pie chart is appropriate. To insert: select the city and total_amount columns, choose Insert > Recommended Charts, preview the pie chart, and click OK. ⟦C.f1 C.f2 C:tb1 C:tb2⟧

=========

# EVALUATOR PACKET — Conditional Formatting and Data Validation (tile_spreadsheet_formatting_validation)
Tile summary: Apply automatic cell formatting based on value rules, and restrict what users can enter into a cell.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = spreadsheet.conditional_formatting — Conditional formatting
B = spreadsheet.data_validation — Data validation (dropdown lists, input restrictions)

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: tile_spreadsheet_formatting_validation.s11: prose block without lineage.fact_ids

## SOURCE FACTS — A (spreadsheet.conditional_formatting)   objective: Apply a conditional formatting rule that automatically formats cells meeting a threshold condition.
A.f1: Conditional formatting applies a format to cells automatically based on rules you create that determine the format based on the cells' values.   [sources: excel_conditional_formatting_guide#Use conditional formatting to highlight information in Excel]
A.f2: To apply a quick conditional formatting rule, select the cells, then on the Home tab in the Style group select Conditional Formatting > Highlight Cells Rules, choose a comparison command such as Less Than, enter the comparison value, and select a format.   [sources: excel_conditional_formatting_guide#Format cells that contain text, number, or date or time values]
PRACTICE ANCHOR (spreadsheet): Given a small table of delivery times, apply a Highlight Cells Rules conditional formatting rule so that every cell whose value is below a specified threshold is filled in red.  SUCCESS: All cells containing values below the threshold display a red fill; cells at or above the threshold display no conditional fill; the rule was created through Home → Conditional Formatting → Highlight Cells Rules → Less Than.
ASSESSMENT ANCHOR: apply_conditional_formatting_rule_for_given_condition facts=['f1', 'f2']

## SOURCE FACTS — B (spreadsheet.data_validation)   objective: Restrict a cell or range to only accept values from a fixed list by adding a dropdown-list data validation rule.
B.f1: Data validation restricts the type of data or the values users can enter into a cell, such as a dropdown list, and can display a customized error message when a user enters invalid data.   [sources: excel_data_validation_guide#Apply data validation to cells]
B.f2: To add a dropdown-list data validation rule, select the cells, select Data > Data Validation, on the Settings tab set Allow to List, then in the Source box type the list values separated by commas, making sure the In-cell dropdown check box is selected.   [sources: excel_data_validation_guide#Add data validation to a cell or a range]
B.f3: Data validation can also restrict entry to a whole number, decimal, date, time, or text length within limits: under Allow choose the type (for example Whole Number), under Data choose a condition (for example between), and then enter the minimum, maximum, or specific value to allow.   [sources: excel_data_validation_guide#Adding other types of data validation]
PRACTICE ANCHOR (spreadsheet): Open a spreadsheet containing an Orders table with a 'Status' column. Add a dropdown-list data validation rule to the Status column that restricts entry to exactly three values: Pending, Delivered, and Cancelled. Confirm the In-cell dropdown is enabled.  SUCCESS: Each cell in the Status column shows a dropdown arrow; selecting a listed value is accepted; typing a value not in the list triggers the default Excel/Sheets restriction notice; no formula or function is used.
ASSESSMENT ANCHOR: identify_data_validation_purpose_and_error_message_behaviour facts=['f1']
ASSESSMENT ANCHOR: configure_dropdown_list_validation_with_source_values facts=['f2']
ASSESSMENT ANCHOR: configure_numeric_date_or_text_length_validation_with_condition_and_limits facts=['f3']
ASSESSMENT ANCHOR: select_correct_validation_type_for_a_given_input_restriction_requirement facts=['f1', 'f2', 'f3']

## DATA ASSETS USED
asset_orders_clean: Orders — clean baseline (20 rows) — columns: order_id(identifier), city(categorical), delivery_minutes(numerical), amount(numerical), status(categorical), driver_id(identifier), order_date(datetime)
   ["LG-2001","Lagos",28,4500.0,"Delivered","D01","2024-03-04"]
   ["LG-2002","Abuja",45,7200.0,"Delivered","D02","2024-03-04"]
   ["LG-2003","Lagos",62,3100.0,"Delivered","D01","2024-03-05"]
   ["LG-2004","Kano",null,5800.0,"Pending","D03","2024-03-05"]
   ["LG-2005","Lagos",19,2200.0,"Delivered","D02","2024-03-05"]
   ["LG-2006","Port Harcourt",55,9100.0,"Delivered","D04","2024-03-06"]
   ["LG-2007","Lagos",null,1800.0,"Cancelled","D01","2024-03-06"]
   ["LG-2008","Abuja",38,6300.0,"Delivered","D02","2024-03-06"]
   variant asset_orders_messy: 4 ops; planted: issue_dup_LG2005(duplicate_row); issue_case_status_LG2009(inconsistent_category); issue_neg_delivery_LG2011(impossible_value); issue_wrong_type_amount_LG2016(wrong_type)

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjusting figure size and layout; Bar chart creation; Bar charts; Basic formula syntax and arithmetic operators; Basic plot creation with the pyplot interface; Common aggregation functions (SUM, AVERAGE, COUNT, COUNTA); Common formula error values and troubleshooting (#N/A, #REF!, #VALUE!); Conditional aggregation (COUNTIF/COUNTIFS, SUMIF/SUMIFS); Cross-referencing cells across multiple sheets/workbooks; Data validation (dropdown lists, input restrictions); Date functions and date arithmetic (TODAY, DATEDIF); Histograms; INDEX/MATCH as a lookup alternative; Line chart creation; Line plots; Logical functions (IF, nested IF, AND, OR); Lookup functions (VLOOKUP, HLOOKUP, XLOOKUP); Pie chart creation; Pivot table summarization options (sum, count, average); Pivot tables: rows, columns, values, filters; Relative vs absolute references ($ notation); Remove duplicates cleaning; Text combining; Text extraction; Text to columns split; matplotlib figure and axes object model

## LESSON, in learner order

### s01 · explainer · Highlighting Cells Automatically by Value  [reward 5]
Concept — Conditional formatting applies a format to cells based on rules you create — no manual colouring needed.
(definition) Conditional formatting applies a format to cells automatically based on rules you create that determine the format based on the cells' values — rather than you manually colouring cells one at a time. ⟦A.f1 A:tb1⟧
(mechanism) To apply a quick conditional formatting rule, select the cells, then on the Home tab in the Style group select Conditional Formatting > Highlight Cells Rules, choose a comparison command such as Less Than, enter the comparison value, and select a format. Selecting the delivery-time column and applying Highlight Cells Rules > Less Than with a value of 15 and a green fill automatically colours every delivery under 15 minutes. ⟦A.f2 A:tb2⟧
[BEFORE_AFTER] Home > Conditional Formatting > Highlight Cells Rules > Less Than, value 15, green fill — cells below 15 are automatically coloured; cells at or above 15 remain unformatted.
  before:
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","asset_ref":{"asset_id":"asset_orders_clean","variant_id":null,"columns":["order_id","delivery_minutes"]},"range":"A1:B12","sheet_name":"Orders","annotations":[{"target":"B1:B8","text":"delivery_minutes — no formatting applied"}]}
  after:
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","asset_ref":{"asset_id":"asset_orders_clean","variant_id":null,"columns":["order_id","delivery_minutes"]},"range":"A1:B12","sheet_name":"Orders","annotations":[{"target":"B2","text":"28 — no fill (≥ 15)"},{"target":"B6","text":"19 — no fill (≥ 15)"},{"target":"B12","text":"14 — green fill (< 15)"}]}

### s02 · video · Applying a Conditional Formatting Rule via Highlight Cells Rules  [reward 3]
Watch — See the menu path and how the rule re-evaluates automatically when cell values change.
[VIDEO Applying a conditional formatting rule via Highlight Cells Rules] bridge-before: Watch the menu path: Home tab → Conditional Formatting → Highlight Cells Rules. The clip uses Duplicate Values; Devspace's example uses Less Than — the same route, different command. | bridge-after: The clip shows the rule triggering automatically from cell values (f1, f2), but never demonstrates a numeric threshold like Less Than. The teaching text covers that step.
  - _eZRkmRfVTM 467-520s facts=['f1', 'f2'] label: Navigating to Highlight Cells Rules and applying a rule to a column | summary: The presenter selects a date column, opens Conditional Formatting > Highlight Cells Rules > Duplicate Values, and the spreadsheet immediately highlights the duplicate entry. Switching the rule to Unique then highlights the non-duplicate cells instead, showing how the rule re-evaluates automatically based on cell values.

### s03 · check · Applying a Conditional Formatting Rule  [reward 5]
Quick Check — Test your understanding of how to set up a Highlight Cells Rules rule.
QUESTION [choice, intro, grading=client] You want to highlight all cells in the delivery_minutes column (C2:C21) that contain values below 30, using a red fill. Which sequence of steps achieves this?
  ✔ opt_a: Select C2:C21 → Home → Conditional Formatting → Highlight Cells Rules → Less Than → enter 30 → choose a red fill format.
  ✘ opt_b: Select C2:C21 → Insert → Conditional Formatting → Less Than → enter 30 → choose a red fill format.
      why: Conditional Formatting is not on the Insert tab. It is on the Home tab, in the Styles group. The correct path is Home → Conditional Formatting → Highlight Cells Rules → Less Than.
  ✘ opt_c: Select C2:C21 → Home → Format Cells → Conditional → Less Than → enter 30 → choose a red fill format.
      why: There is no Conditional option inside Format Cells. Conditional Formatting is a separate command on the Home tab: Home → Conditional Formatting → Highlight Cells Rules → Less Than.
  ✘ opt_d: Select C2:C21 → Data → Conditional Formatting → Highlight Cells Rules → Less Than → enter 30 → choose a red fill format.
      why: Conditional Formatting is not on the Data tab. It is on the Home tab, in the Styles group. The correct path is Home → Conditional Formatting → Highlight Cells Rules → Less Than.
  feedback✔: Correct! The path is Home → Conditional Formatting → Highlight Cells Rules → Less Than → enter 30 → choose the red fill format. The rule then applies the format automatically to any cell below 30.  feedback✘: Conditional Formatting is on the Home tab (not Insert or Data). The path is: Home → Conditional Formatting → Highlight Cells Rules → Less Than → enter the threshold → choose the format.  hints: ['Conditional Formatting lives on the Home tab, in the Styles group — not on Insert or Data.', 'The Highlight Cells Rules submenu contains comparison commands like Less Than, Greater Than, and Equal To.']  remediation→r01
  MEASURES: A:apply_conditional_formatting_rule_for_given_condition(f1,f2)   anchors=['assessment:apply_conditional_formatting_rule_for_given_condition']
  taught-before-tested: A.f1←s01; A.f2←s01

### s04 · hands_on · Apply a Less Than Rule to Delivery Times  [reward 10]
Practice — Use Highlight Cells Rules to colour delivery times below a threshold in red.
QUESTION [formula_entry, core, grading=client] A conditional formatting rule highlights cells in C2:C21 where delivery_minutes is less than 30 with a red fill. In cell F1, write a formula that counts how many cells in C2:C21 satisfy that condition — that is, how many cells would be highlighted red. Use COUNTIF with the range C2:C21 and the criterion "<30". (Note: COUNTIF is previewed here to reinforce the conditional formatting concept; it will be covered fully in a later lesson on conditional aggregation.)
  [unrendered interaction type formula_entry] public={"prompt":"A conditional formatting rule highlights cells in C2:C21 where delivery_minutes is less than 30 with a red fill. In cell F1, write a formula that counts how many cells in C2:C21 satisfy that condition — that is, how many cells would be highlighted red. Use COUNTIF with the range C2:C21 and the criterion \"<30\". (Note: COUNTIF is previewed here to reinforce the conditional formatting concept; it will be covered fully in a later lesson on conditional aggregation.)","asset_ref":{"asset_id":"asset_orders_clean","variant_id":null},"sheet_name":"Orders","target_cell":"F1","allowed_functions":["COUNTIF"]} grading={"expected_value":4,"reference_formula":"=COUNTIF(C2:C21,\"<30\")","must_use_functions":["COUNTIF"],"forbid_hardcoded_values":true}
  feedback✔: Correct! =COUNTIF(C2:C21,"<30") returns 4 — there are 4 orders with delivery times below 30 minutes (28, 19, 14, and 29). Those 4 cells would be highlighted red by the conditional formatting rule.  feedback✘: Use COUNTIF with the delivery_minutes range and the criterion "<30": =COUNTIF(C2:C21,"<30"). The criterion must be in double quotes.  hints: ['COUNTIF takes two arguments: the range and the criterion. The criterion for \'less than 30\' is "<30" (in double quotes).', 'The formula is =COUNTIF(C2:C21,"<30"). Make sure the criterion is a text string with the comparison operator inside the quotes.']  remediation→r01
  MEASURES: A:apply_conditional_formatting_rule_for_given_condition(f1,f2)   anchors=['practice', 'assessment:apply_conditional_formatting_rule_for_given_condition']
  taught-before-tested: A.f1←s01; A.f2←s01

### s05 · explainer · Restricting What Users Can Enter  [reward 5]
Concept — Data validation restricts the type of data or values users can enter into a cell, and can display a custom error message.
(definition) Data validation restricts the type of data or the values users can enter into a cell, such as a dropdown list, and can display a customised error message when a user enters invalid data. ⟦B.f1 B:tb1⟧
(example) To add a dropdown-list validation rule, select the cells, choose Data > Data Validation, on the Settings tab set Allow to List, then in the Source box type the list values separated by commas, making sure the In-cell dropdown check box is selected. Restricting the Orders sheet's status column with Source set to Pending,Delivered,Cancelled gives each cell a dropdown of those three words. ⟦B.f2 B:tb2⟧
[DIAGRAM: Data Validation dialog — Settings tab for a List restriction] nodes=['Data Validation dialog — Settings tab', 'Allow: List', 'Source: Pending,Delivered,Cancelled', 'In-cell dropdown: checked', 'Status cell — dropdown arrow visible', 'Set Allow to List to create a dropdown restriction.', 'Type the allowed values separated by commas. These become the dropdown options.', 'The cell now shows a dropdown arrow; only the three listed values are accepted.'] edges=[('allow_field', 'callout_allow', None), ('source_field', 'callout_source', None), ('cell_dropdown', 'callout_cell', None)] alt: Diagram of the Data Validation dialog open on the Settings tab with Allow set to List and the Source box containing 'Pending,Delivered,Cancelled'. A callout points to a Status column cell showing a dropdown arrow. Labels explain each dialog field.

### s06 · explainer · Numeric, Date, and Text-Length Validation  [reward 3]
Concept — Data validation can also restrict entry to a number, date, or text of a specific length.
(example) Data validation can restrict entry to a whole number, decimal, date, time, or text length within limits: under Allow choose the type (for example Whole Number), under Data choose a condition (for example between), and then enter the minimum, maximum, or specific value to allow. On the delivery-time column, choosing Whole Number, between 0 and 300, blocks anyone from typing a negative or unreasonably large delivery time. ⟦B.f3 B:tb3⟧

### s07 · video · Restricting Cell Input: Error Alerts and Numeric Rules  [reward 3]
Watch — See how the Allow menu switches between types and how error alerts work.
[VIDEO Restricting cell input: error alerts, date, whole-number, and text-length rules] bridge-before: Watch how the dialog's Allow menu switches between Date, Whole Number, and Text Length, and how the Data and minimum/maximum fields change with each type. Note: the TODAY function appears but is not required knowledge here. | bridge-after: The clip does not show building a dropdown list from scratch (f2); the text above covers that full step-by-step procedure.
  - FRiFfKb_B_A 494-849s facts=['f1', 'f3'] label: Input messages, error alerts, and numeric/date/text-length validation rules | summary: The instructor selects a cell that already has a dropdown rule and opens Data Validation to add an input message ('Please make a selection from the list') and a custom error alert, showing that without a custom message Excel displays a default restriction notice, and with one it shows the custom text instead. The instructor then opens Data Validation for a date column, chooses the Date type with a 'greater than today' condition using the TODAY function, adds an input message and a custom alert, and demonstrates that a past date is rejected while a future date is accepted. Next, a project-number column is restricted to Whole Number, between 1,000 and 2,000, with the error alert noting the allowed range. A company-code column is then restricted using Text Length equal to 5, confirming that a five-character entry passes and a six-character entry fails. Finally, a project-description column is restricted to Text Length greater than 20, so a short phrase is rejected and a longer one is accepted. A brief aside notes that a Custom formula option exists for pattern-based rules but is deferred as an advanced topic.

### s08 · check · Data Validation Purpose and Numeric Rules  [reward 5]
Quick Check — Test your understanding of what data validation does and how to configure a numeric rule.
QUESTION [choice, intro, grading=client] You want to restrict the delivery_minutes column so that only whole numbers between 1 and 300 can be entered. In the Data Validation dialog, which settings achieve this?
  ✔ opt_a: Allow: Whole Number; Data: between; Minimum: 1; Maximum: 300.
  ✘ opt_b: Allow: Decimal; Data: between; Minimum: 1; Maximum: 300.
      why: Decimal allows fractional numbers (e.g., 45.5). To restrict to whole numbers only, choose Whole Number, not Decimal.
  ✘ opt_c: Allow: List; Source: 1,300.
      why: List creates a dropdown with specific values. To allow any whole number in a range, choose Whole Number with a between condition and set the minimum and maximum.
  ✘ opt_d: Allow: Text Length; Data: between; Minimum: 1; Maximum: 300.
      why: Text Length restricts the number of characters in a text entry, not the numeric value. To restrict to whole numbers between 1 and 300, choose Whole Number with a between condition.
  feedback✔: Correct! Allow: Whole Number; Data: between; Minimum: 1; Maximum: 300 restricts the cell to whole numbers in that range. Any entry outside the range triggers the error message.  feedback✘: To allow only whole numbers between 1 and 300, set Allow to Whole Number, Data to between, Minimum to 1, and Maximum to 300.  hints: ['The Allow dropdown determines the type of data permitted. For whole numbers, choose Whole Number (not Decimal or Text Length).', 'The Data dropdown sets the condition (between, greater than, less than, etc.). For a range, choose between and set the minimum and maximum.']  remediation→r02
  MEASURES: B:identify_data_validation_purpose_and_error_message_behaviour(f1); B:configure_numeric_date_or_text_length_validation_with_condition_and_limits(f3)   anchors=['assessment:identify_data_validation_purpose_and_error_message_behaviour', 'assessment:configure_numeric_date_or_text_length_validation_with_condition_and_limits']
  taught-before-tested: B.f1←s05; B.f3←s06

### s09 · check · Choosing the Right Validation Type  [reward 5]
Quick Check — Given an input restriction requirement, identify the correct validation type to use.
QUESTION [choice, core, grading=client] A colleague wants to restrict the status column so that users can only enter one of three values: Delivered, Pending, or Cancelled. Which validation type should they choose?
  ✔ opt_a: List — because it creates a dropdown with the exact allowed values, preventing any other entry.
  ✘ opt_b: Whole Number — because the status values can be coded as numbers (1, 2, 3).
      why: Whole Number restricts entries to numeric values within a range. It cannot enforce specific text values like 'Delivered'. Use List to restrict entries to a fixed set of text options.
  ✘ opt_c: Text Length — because each status value has a specific character count.
      why: Text Length restricts the number of characters, not the specific text. 'Delivered' (9 chars) and 'Cancelled' (9 chars) have the same length, so Text Length cannot distinguish between them. Use List instead.
  ✘ opt_d: Decimal — because status values can be represented as decimal codes.
      why: Decimal restricts entries to numeric values. It cannot enforce specific text values like 'Pending'. Use List to create a dropdown with the allowed text values.
  feedback✔: Correct! List validation creates a dropdown showing the allowed values (Delivered, Pending, Cancelled) and prevents any other entry. It is the right choice when you need to restrict input to a fixed set of text options.  feedback✘: When you need to restrict input to a fixed set of text values, use List validation. It creates a dropdown with the allowed options and blocks any other entry.  hints: ['List validation is designed for exactly this scenario: a fixed set of allowed values shown as a dropdown.', 'Whole Number and Decimal are for numeric ranges; Text Length is for character counts. None of those can enforce specific text values.']  remediation→r02
  MEASURES: B:select_correct_validation_type_for_a_given_input_restriction_requirement(f1,f2,f3)   anchors=['assessment:select_correct_validation_type_for_a_given_input_restriction_requirement']
  taught-before-tested: B.f1←s05; B.f2←s05; B.f3←s06

### s10 · hands_on · Add a Dropdown Validation Rule to the Status Column  [reward 10]
Practice — Restrict the Status column to Pending, Delivered, and Cancelled using Data > Data Validation.
QUESTION [formula_entry, core, grading=client] The status column (E2:E21) has a dropdown list validation rule that allows only Delivered, Pending, or Cancelled. Every cell in E2:E21 currently contains one of those three values. In cell F1, write a formula that counts how many non-empty cells are in E2:E21 — confirming that all 20 rows have a valid status entry. Use COUNTA with the range E2:E21.
  [unrendered interaction type formula_entry] public={"prompt":"The status column (E2:E21) has a dropdown list validation rule that allows only Delivered, Pending, or Cancelled. Every cell in E2:E21 currently contains one of those three values. In cell F1, write a formula that counts how many non-empty cells are in E2:E21 — confirming that all 20 rows have a valid status entry. Use COUNTA with the range E2:E21.","asset_ref":{"asset_id":"asset_orders_clean","variant_id":null},"sheet_name":"Orders","target_cell":"F1","allowed_functions":["COUNTA"]} grading={"expected_value":20,"reference_formula":"=COUNTA(E2:E21)","must_use_functions":["COUNTA"],"forbid_hardcoded_values":true}
  feedback✔: Correct! =COUNTA(E2:E21) returns 20 — all 20 rows have a status value. With dropdown list validation applied to E2:E21, each of those values must be one of the three allowed options: Delivered, Pending, or Cancelled.  feedback✘: Use COUNTA to count non-empty cells in the status range: =COUNTA(E2:E21). COUNTA counts all non-empty cells, including text values.  hints: ['COUNTA counts all non-empty cells, including text. Use it to count the status values in E2:E21.', 'The status column is column E, rows 2 through 21 (20 orders).']  remediation→r03
  MEASURES: B:configure_dropdown_list_validation_with_source_values(f2)   anchors=['practice', 'assessment:configure_dropdown_list_validation_with_source_values']
  taught-before-tested: B.f2←s05

### s11 · recap · Conditional Formatting and Data Validation — Key Points  [reward 5]
Recap — You can now apply automatic cell formatting rules and restrict what users can enter.
(takeaway) Conditional formatting applies a format to cells automatically based on rules you create from cell values. Use Home > Conditional Formatting > Highlight Cells Rules, choose a comparison such as Less Than, enter the threshold, and pick a format. Data validation restricts what users can enter: choose Data > Data Validation, set Allow to List and type comma-separated values for a dropdown, or choose Whole Number, Date, or Text Length with a condition and limits for numeric restrictions. A customised error message can be shown when invalid data is entered.
[UP NEXT] Next: Cleaning and Cross-Sheet References: In the next tile you'll remove duplicates, split combined text into columns, and reference data across sheets in the same workbook.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Setting Up a Highlight Cells Rule — Walk through the exact menu path and see the rule trigger automatically.
(example) Conditional formatting applies a format automatically based on cell values — you do not colour cells manually. To apply a Less Than rule to the delivery-time column: select the column cells, go to Home > Conditional Formatting > Highlight Cells Rules > Less Than, type 15 in the value box, choose a red fill, and click OK. Every cell whose value is below 15 is immediately coloured red; cells at or above 15 remain unformatted. The rule re-evaluates whenever a cell value changes. ⟦A.f1 A.f2 A:tb1 A:tb2⟧
### r02 · What Data Validation Does and How to Set Numeric Limits — Data validation blocks invalid input before it reaches the cell.
(example) Data validation restricts the type of data or the values users can enter into a cell, and can display a customised error message when a user enters invalid data. For a numeric restriction on the delivery-time column: select the column, choose Data > Data Validation, set Allow to Whole Number, set Data to between, enter 0 as the minimum and 300 as the maximum, and click OK. Typing a negative number or a value above 300 triggers the restriction notice. ⟦B.f1 B.f3 B:tb1 B:tb3⟧
### r03 · Choosing the Right Validation Type — Match the input restriction requirement to the correct Allow setting.
(example) Use List when you want to restrict entry to a fixed set of text values — for example, Pending, Delivered, Cancelled in the status column. Use Whole Number or Decimal when you want to restrict entry to a number within a range — for example, delivery times between 0 and 300. Use Date or Time for date or time restrictions. Use Text Length when you want to restrict how many characters can be entered. All types are set through Data > Data Validation > Settings > Allow. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3⟧

## OTHER CONTENT (fields without a dedicated renderer)
· feedback.hints: COUNTIF takes two arguments: the range and the criterion. The criterion for 'less than 30' is "<30" (in double quotes).

=========

# EVALUATOR PACKET — Pivot Tables (tile_spreadsheet_pivot_tables)
Tile summary: Build a PivotTable to summarise Orders data by city and status, then change the value-field summary function.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = spreadsheet.pivot_tables — Pivot tables: rows, columns, values, filters
B = spreadsheet.pivot_summarization — Pivot table summarization options (sum, count, average)

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=4
  warn: tile_spreadsheet_pivot_tables.s10: remediation tile_spreadsheet_pivot_tables.r03 re-teaches ['spreadsheet.pivot_summarization#f1'] but the check measures ['spreadsheet.pivot_summarization#f2'] — a learner who fails it is sent to an unrelated fact
  warn: remediation step tile_spreadsheet_pivot_tables.r02 is never referenced
  warn: tile_spreadsheet_pivot_tables.s01: 174 words vs budget 119
  warn: tile_spreadsheet_pivot_tables.s11: prose block without lineage.fact_ids

## SOURCE FACTS — A (spreadsheet.pivot_tables)   objective: Build a PivotTable that places one field in Rows, another in Columns, and a numeric field in Values.
A.f1: A PivotTable is a tool to calculate, summarize, and analyze data that lets you see comparisons, patterns, and trends in your data.   [sources: excel_pivottable_guide#Create a PivotTable to analyze worksheet data]
A.f2: To create a PivotTable, select the data cells, select Insert > PivotTable, choose where to place the PivotTable report, and select OK.   [sources: excel_pivottable_guide#Create a PivotTable in Excel for Windows]
A.f3: To add a field to the PivotTable, select its checkbox in the PivotTable Fields pane; selected fields are added to their default areas, with non-numeric fields added to Rows and numeric fields added to Values, and a field can be moved to a different area by dragging it there.   [sources: excel_pivottable_guide#Building out your PivotTable]
A.f4: Filters area fields are shown as top-level report filters above the PivotTable; Columns area fields are shown as Column Labels at the top of the PivotTable; Rows area fields are shown as Row Labels on the left side of the PivotTable; Values area fields are shown as summarized numeric values in the PivotTable.   [sources: excel_pivottable_field_list_guide]
PRACTICE ANCHOR (spreadsheet): Given an Orders dataset with Region, Product Category, and Sales Amount columns, build a PivotTable that shows total Sales Amount broken down by Region (rows) and Product Category (columns).  SUCCESS: The completed PivotTable has Region in the Rows area, Product Category in the Columns area, and Sales Amount in the Values area, producing a grid of totals for every Region/Product Category combination.
ASSESSMENT ANCHOR: define_pivot_table_purpose facts=['f1']
ASSESSMENT ANCHOR: execute_pivot_table_creation_steps facts=['f2']
ASSESSMENT ANCHOR: add_and_reposition_fields_in_pivot_areas facts=['f3']
ASSESSMENT ANCHOR: identify_visual_output_of_each_pivot_area facts=['f4']
ASSESSMENT ANCHOR: build_pivot_table_to_answer_summarization_requirement facts=['f2', 'f3', 'f4']

## SOURCE FACTS — B (spreadsheet.pivot_summarization)   objective: Change a PivotTable value field's summary function, recognizing that Sum is the default for numeric fields.
B.f1: Data in a PivotTable's Values area summarizes the underlying source data by default using the SUM function for numeric values and the COUNT function for text values.   [sources: excel_pivottable_summary_guide#Change the summary function or custom calculation for a field in a PivotTable]
B.f2: To change a value field's summary function, select the field in the Values area, on the PivotTable Analyze tab select Active Field > Field Settings (or right-click the value and choose Value Field Settings), select the Summarize Values By tab, and choose the summary function you want, such as Average.   [sources: excel_pivottable_summary_guide#Change the summary function]
PRACTICE ANCHOR (spreadsheet): Open an existing PivotTable that shows total order amounts per city (Sum), navigate to Value Field Settings, switch the summary function to Average, and explain in one sentence how the displayed numbers changed and what they now represent.  SUCCESS: The Values area header updates to 'Average of Amount', each city row shows a per-order average rather than a total, and the learner's written sentence correctly contrasts total revenue with average order value.
ASSESSMENT ANCHOR: identify_default_summarization_by_data_type facts=['f1']
ASSESSMENT ANCHOR: select_correct_value_field_summarization_setting facts=['f2']

## DATA ASSETS USED
asset_orders_clean: Orders — clean baseline (20 rows) — columns: order_id(identifier), city(categorical), delivery_minutes(numerical), amount(numerical), status(categorical), driver_id(identifier), order_date(datetime)
   ["LG-2001","Lagos",28,4500.0,"Delivered","D01","2024-03-04"]
   ["LG-2002","Abuja",45,7200.0,"Delivered","D02","2024-03-04"]
   ["LG-2003","Lagos",62,3100.0,"Delivered","D01","2024-03-05"]
   ["LG-2004","Kano",null,5800.0,"Pending","D03","2024-03-05"]
   ["LG-2005","Lagos",19,2200.0,"Delivered","D02","2024-03-05"]
   ["LG-2006","Port Harcourt",55,9100.0,"Delivered","D04","2024-03-06"]
   ["LG-2007","Lagos",null,1800.0,"Cancelled","D01","2024-03-06"]
   ["LG-2008","Abuja",38,6300.0,"Delivered","D02","2024-03-06"]
   variant asset_orders_messy: 4 ops; planted: issue_dup_LG2005(duplicate_row); issue_case_status_LG2009(inconsistent_category); issue_neg_delivery_LG2011(impossible_value); issue_wrong_type_amount_LG2016(wrong_type)

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjusting figure size and layout; Bar chart creation; Bar charts; Basic A/B test structure (control vs treatment group); Basic plot creation with the pyplot interface; Box plots; Conceptual effect of sample size on confidence; Conceptual interpretation of statistical significance/confidence level; Custom styling/theming (advanced/optional); Drawing a business conclusion from an experiment-result summary; Histograms; Identifying the business decision a stakeholder needs the analysis to inform; Interpreting lift/percentage change between groups; Labeling axes, titles, and legends; Line chart creation; Line plots; Matching chart type to the analytical question; Multi-panel figures/subplots (advanced/optional); Pie chart creation; Pivot table summarization options (sum, count, average); Plotting directly from pandas DataFrames with seaborn; Scatter plots; Stating a finding precisely and quantitatively (the specific number or comparison, not a vague claim); matplotlib figure and axes object model; seaborn built-in themes and color palettes; seaborn statistical plotting functions

## LESSON, in learner order

### s01 · explainer · What a PivotTable Does and How to Build One  [reward 5]
Concept — A PivotTable summarises your Orders data by city, status, or any other field — no formulas required.
(intro) Reading down a long Orders sheet to compare total amounts by city and status by hand would take forever. A PivotTable is a tool to calculate, summarize, and analyze data that lets you see comparisons, patterns, and trends in your data. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) To create a PivotTable, select the data cells, select Insert > PivotTable, choose where to place the PivotTable report, and select OK. To add a field, select its checkbox in the PivotTable Fields pane; non-numeric fields go to Rows and numeric fields go to Values by default. A field can be moved to a different area by dragging it there. ⟦A.f2 A.f3 A:tb3⟧
(example) Filters area fields appear as top-level report filters above the PivotTable. Columns area fields appear as Column Labels at the top. Rows area fields appear as Row Labels on the left. Values area fields appear as summarised numeric values in the body. Building a PivotTable from your Orders data with City in Rows, Status in Columns, and Amount in Values gives a grid of summarised order amounts for every city/status combination. ⟦A.f4 A:tb4⟧
[DIAGRAM: PivotTable Fields pane — four drop zones] nodes=['Filters area', 'Columns area — Status', 'Rows area — City', 'Values area — Sum of Amount', 'Fields here appear as top-level report filters above the PivotTable.', 'Fields here appear as Column Labels at the top of the PivotTable. Status is placed here.', 'Fields here appear as Row Labels on the left side. City is placed here.', 'Fields here appear as summarised numeric values in the body. Amount is placed here.'] edges=[('filters_zone', 'callout_filters', None), ('columns_zone', 'callout_columns', None), ('rows_zone', 'callout_rows', None), ('values_zone', 'callout_values', None)] alt: Diagram of the PivotTable Fields pane showing four drop zones: Filters (top), Columns (top-right), Rows (bottom-left), and Values (bottom-right), with City in Rows, Status in Columns, and Amount in Values. Callouts describe what each area controls.

### s02 · video · Building a PivotTable: Fields, Areas, and Layout  [reward 3]
Watch — Watch how each field snaps into its area and the summary grid rearranges instantly.
[VIDEO Building a PivotTable: fields, areas, and layout] bridge-before: Watch how each field snaps into its area and the grid rearranges instantly. The instructor mentions 'sum or count' briefly — summarization options are covered separately. | bridge-after: The clip shows all four areas in action. Note that the checkbox default-placement rule (non-numeric → Rows, numeric → Values) is stated in the text but not narrated in the clip.
  - aofsdpjvK7w 84-302s facts=['f1', 'f2', 'f3', 'f4'] label: Create a PivotTable and place fields in Rows, Columns, Values, and Filters | summary: The instructor selects all data, converts it to a named table, then launches the PivotTable dialog. On the right-hand side, four drop zones appear: Filters, Columns, Rows, and Values. Salesperson is dragged to Rows and Amount to Values, producing a total-sales-per-salesperson summary. A second PivotTable adds Geography first to Rows (creating a two-level layout), then moves Geography to Columns to produce a matrix view. A third PivotTable places Geography in Filters, which adds a top-level filter control above the table so results can be narrowed to a single geography such as New Zealand.

### s03 · explainer · What Each PivotTable Area Displays  [reward 3]
Concept — Each of the four drop zones produces a distinct visual output in the PivotTable.
(definition) Filters area fields are shown as top-level report filters above the PivotTable. Columns area fields are shown as Column Labels at the top of the PivotTable. Rows area fields are shown as Row Labels on the left side of the PivotTable. Values area fields are shown as summarised numeric values in the body of the PivotTable. ⟦A.f4 A:tb4⟧

### s04 · check · Creating a PivotTable and Reading Its Areas  [reward 5]
Quick Check — Test your understanding of the creation steps and what each area displays.
QUESTION [choice, intro, grading=client] You drag the city field into the Rows area of a PivotTable. Where does city appear in the finished PivotTable?
  ✔ opt_a: As Row Labels on the left side of the PivotTable, with one row per city.
  ✘ opt_b: As Column Labels across the top of the PivotTable, with one column per city.
      why: Column Labels appear when a field is placed in the Columns area, not the Rows area. A field in the Rows area appears as Row Labels on the left side.
  ✘ opt_c: As a top-level report filter above the PivotTable.
      why: A top-level report filter appears when a field is placed in the Filters area. A field in the Rows area appears as Row Labels on the left side of the PivotTable.
  ✘ opt_d: As summarized numeric values in the body of the PivotTable.
      why: Summarized numeric values appear in the Values area. A field in the Rows area appears as Row Labels — one row per unique value of that field.
  feedback✔: Correct! A field placed in the Rows area appears as Row Labels on the left side of the PivotTable — one row for each unique value of that field (e.g., one row per city).  feedback✘: The Rows area produces Row Labels on the left side of the PivotTable. Each unique value of the field (e.g., each city name) gets its own row.  hints: ['Think about the four areas: Filters (top), Columns (top header), Rows (left side), Values (body numbers).', 'The Rows area places field values down the left side of the PivotTable as row labels.']  remediation→r01
  MEASURES: A:execute_pivot_table_creation_steps(f2); A:identify_visual_output_of_each_pivot_area(f4)   anchors=['assessment:execute_pivot_table_creation_steps', 'assessment:identify_visual_output_of_each_pivot_area']
  taught-before-tested: A.f2←s01; A.f4←s01

### s05 · check · Building a PivotTable to Answer a Question  [reward 5]
Quick Check — Apply your knowledge of fields, areas, and creation steps to a summarisation task.
QUESTION [choice, core, grading=client] You want a PivotTable that shows the total order amount for each city, with cities listed down the left and a single column of totals. Which field placement achieves this?
  ✔ opt_a: city in Rows area; amount in Values area.
  ✘ opt_b: city in Columns area; amount in Values area.
      why: Placing city in the Columns area would spread city names across the top as column headers, not down the left as row labels. To list cities down the left, place city in the Rows area.
  ✘ opt_c: city in Values area; amount in Rows area.
      why: The Values area holds numeric summaries, not category labels. city is a text field and should go in the Rows area; amount is numeric and should go in the Values area.
  ✘ opt_d: city in Filters area; amount in Rows area.
      why: The Filters area creates a top-level report filter, not row labels. To list cities down the left side, place city in the Rows area.
  feedback✔: Correct! city in the Rows area creates one row per city on the left side; amount in the Values area fills in the total for each city. That gives you the city-by-total layout you need.  feedback✘: To list cities down the left with totals beside them, place city in the Rows area and amount in the Values area. Rows area → left-side labels; Values area → numeric summaries.  hints: ['Rows area = left-side labels (one row per unique value). Values area = numeric summaries in the body.', 'Match the field type to the area: text/category fields go in Rows or Columns; numeric fields go in Values.']  remediation→r01
  MEASURES: A:build_pivot_table_to_answer_summarization_requirement(f2,f3,f4)   anchors=['assessment:build_pivot_table_to_answer_summarization_requirement']
  taught-before-tested: A.f2←s01; A.f3←s01; A.f4←s01

### s06 · hands_on · Build a PivotTable from the Orders Data  [reward 10]
Practice — Create a PivotTable and place fields in the Rows, Columns, and Values areas.
QUESTION [formula_entry, core, grading=client] A PivotTable with city in the Rows area and amount in the Values area would show the total amount for each city. In cell F1, write a formula that returns the total amount for Lagos orders — the value that would appear in the Lagos row of that PivotTable. Use SUMIF with the city range B2:B21, the criterion "Lagos", and the amount range D2:D21. (Note: SUMIF is previewed here to connect the PivotTable concept to a formula equivalent; it will be covered fully in a later lesson on conditional aggregation.)
  [unrendered interaction type formula_entry] public={"prompt":"A PivotTable with city in the Rows area and amount in the Values area would show the total amount for each city. In cell F1, write a formula that returns the total amount for Lagos orders — the value that would appear in the Lagos row of that PivotTable. Use SUMIF with the city range B2:B21, the criterion \"Lagos\", and the amount range D2:D21. (Note: SUMIF is previewed here to connect the PivotTable concept to a formula equivalent; it will be covered fully in a later lesson on conditional aggregation.)","asset_ref":{"asset_id":"asset_orders_clean","variant_id":null},"sheet_name":"Orders","target_cell":"F1","allowed_functions":["SUMIF"]} grading={"expected_value":28000.0,"reference_formula":"=SUMIF(B2:B21,\"Lagos\",D2:D21)","must_use_functions":["SUMIF"],"forbid_hardcoded_values":true}
  feedback✔: Correct! =SUMIF(B2:B21,"Lagos",D2:D21) returns 28000 — the total amount for Lagos orders. In a PivotTable with city in Rows and amount in Values, this is exactly the value that would appear in the Lagos row.  feedback✘: Use SUMIF with three arguments: the city range (B2:B21), the criterion ("Lagos"), and the amount range (D2:D21). The formula is =SUMIF(B2:B21,"Lagos",D2:D21).  hints: ['SUMIF takes three arguments: =SUMIF(range, criteria, sum_range). The range is the city column, the criteria is "Lagos", and the sum_range is the amount column.', 'Make sure to put Lagos in double quotes inside the formula: =SUMIF(B2:B21,"Lagos",D2:D21).']  remediation→r01
  MEASURES: A:define_pivot_table_purpose(f1); A:add_and_reposition_fields_in_pivot_areas(f3)   anchors=['practice', 'assessment:define_pivot_table_purpose', 'assessment:add_and_reposition_fields_in_pivot_areas']
  taught-before-tested: A.f1←s01; A.f3←s01

### s07 · explainer · Changing How Values Are Summarised  [reward 5]
Concept — The Values area defaults to Sum for numbers and Count for text — and you can change it.
(definition) Data in a PivotTable's Values area summarises the underlying source data by default using the SUM function for numeric values and the COUNT function for text values. Placing Amount in Values on your Orders PivotTable defaults to a total of every matching order's amount, not an average. ⟦B.f1 B:tb1⟧
(mechanism) To change a value field's summary function, select the field in the Values area, then on the PivotTable Analyze tab select Active Field > Field Settings (or right-click the value and choose Value Field Settings), select the Summarize Values By tab, and choose the function you want, such as Average. Switching Amount from Sum to Average turns the same PivotTable from showing total revenue per city into showing average order value per city. ⟦B.f2 B:tb2⟧
[BEFORE_AFTER] Value Field Settings > Summarize Values By > Average changes the Values area from Sum to Average — the same row/column layout, different numbers.
  before:
[TABLE asset_orders_clean cols=['city', 'amount'] tags=amount:Sum of Amount] caption: PivotTable: Sum of Amount by City
  after:
[TABLE asset_orders_clean cols=['city', 'amount'] tags=amount:Average of Amount] caption: PivotTable: Average of Amount by City

### s08 · video · Changing a PivotTable's Value-Field Summary Function  [reward 3]
Watch — See how to open Value Field Settings and switch between Sum and Average.
[VIDEO Changing a PivotTable's value-field summary function] bridge-before: The first clip shows both routes into Value Field Settings to switch to Average (f2); the second explains the Count-vs-Sum default rule (f1). Watch for the two entry points: the dropdown and the right-click menu. | bridge-after: Neither clip covers the full step-by-step path on the PivotTable Analyze tab (Active Field > Field Settings); the teaching text fills that gap and remains the complete reference.
  - UsdedFoTA68 239-280s facts=['f2'] label: Opening Value Field Settings to switch a summary function from Sum to Average | summary: Starting from a PivotTable that already has a numeric field in the Values area, the presenter opens Value Field Settings two ways: first by clicking the field's dropdown arrow in the Values area and selecting Value Field Settings, then by right-clicking the value cell in the PivotTable itself. In both cases the same dialog appears; selecting Average and clicking OK immediately updates the displayed numbers, and the process is reversed by returning to the dialog and selecting Sum.
  - RpCZ_kb1Gfs 0-132s facts=['f1'] label: Why a PivotTable value field defaults to Count for text and Sum for numbers | summary: A PivotTable's Values area automatically chooses its calculation type based on the data type of the field: text fields default to Count because text cannot be summed, while numeric fields default to Sum. A numeric column that contains blank cells is treated as mixed and also defaults to Count; the same applies to columns containing error values such as #REF! or #N/A.

### s09 · check · Default Summarisation by Data Type  [reward 5]
Quick Check — Test your understanding of when a PivotTable defaults to Sum versus Count.
QUESTION [choice, intro, grading=client] You add the status field (which contains text values: Delivered, Pending, Cancelled) to the Values area of a PivotTable. What summary function does Excel apply by default?
  ✔ opt_a: COUNT — because the field contains text values, not numbers.
  ✘ opt_b: SUM — because SUM is always the default for any field in the Values area.
      why: SUM is the default only for numeric fields. When the field contains text values, Excel defaults to COUNT instead, because you cannot add text values together.
  ✘ opt_c: AVERAGE — because Excel averages all values by default.
      why: AVERAGE is not the default for any field type. Excel defaults to SUM for numeric fields and COUNT for text fields.
  ✘ opt_d: MAX — because Excel picks the largest value by default.
      why: MAX is not the default. Excel defaults to SUM for numeric fields and COUNT for text fields.
  feedback✔: Correct! Excel defaults to COUNT for text fields in the Values area, because text values cannot be summed. For numeric fields it defaults to SUM.  feedback✘: Excel uses COUNT as the default for text fields in the Values area (you cannot sum text), and SUM as the default for numeric fields.  hints: ["Ask yourself: can you add text values like 'Delivered' and 'Pending' together? If not, what would Excel do instead?", 'The rule is: numeric field → SUM by default; text field → COUNT by default.']  remediation→r03
  MEASURES: B:identify_default_summarization_by_data_type(f1)   anchors=['assessment:identify_default_summarization_by_data_type']
  taught-before-tested: B.f1←s07

### s10 · hands_on · Switch the Summary Function to Average  [reward 10]
Practice — Change the Values area from Sum to Average using Value Field Settings.
QUESTION [formula_entry, core, grading=client] A PivotTable currently shows the Sum of amount for each city. You want to change the Values area to show the Average of amount instead. In cell F1, write a formula that returns the average order amount across all 20 orders — the overall average that the PivotTable grand total row would show after switching to Average. Use AVERAGE with the range D2:D21.
  [unrendered interaction type formula_entry] public={"prompt":"A PivotTable currently shows the Sum of amount for each city. You want to change the Values area to show the Average of amount instead. In cell F1, write a formula that returns the average order amount across all 20 orders — the overall average that the PivotTable grand total row would show after switching to Average. Use AVERAGE with the range D2:D21.","asset_ref":{"asset_id":"asset_orders_clean","variant_id":null},"sheet_name":"Orders","target_cell":"F1","allowed_functions":["AVERAGE"]} grading={"expected_value":4955.0,"reference_formula":"=AVERAGE(D2:D21)","must_use_functions":["AVERAGE"],"forbid_hardcoded_values":true}
  feedback✔: Correct! =AVERAGE(D2:D21) returns 4955 — the average order amount. After changing the PivotTable's Values field setting from Sum to Average, the grand total row would show this value.  feedback✘: Use AVERAGE with the amount range: =AVERAGE(D2:D21). This returns the average order amount across all 20 orders.  hints: ['The AVERAGE function takes a range as its argument: =AVERAGE(D2:D21).', 'The amount column is column D, rows 2 through 21 (20 orders).']  remediation→r03
  MEASURES: B:select_correct_value_field_summarization_setting(f2)   anchors=['practice', 'assessment:select_correct_value_field_summarization_setting']
  taught-before-tested: B.f2←s07

### s11 · recap · Pivot Tables — Key Points  [reward 5]
Recap — You can now build a PivotTable, place fields in the four areas, and change the summary function.
(takeaway) A PivotTable lets you calculate, summarise, and analyse data to see comparisons, patterns, and trends. Select the data, choose Insert > PivotTable, and drag fields into Rows, Columns, Values, or Filters. Non-numeric fields default to Rows; numeric fields default to Values. The Values area defaults to Sum for numbers and Count for text. To change the summary function, open Value Field Settings and choose from the Summarize Values By tab.
[UP NEXT] Next: Chart Types: In the next tile you'll build bar, line, and pie charts from your Orders data to visualise comparisons, trends, and part-of-whole relationships.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Creating a PivotTable Step by Step — Walk through the creation steps and see what each area produces.
(example) To create a PivotTable: select the data cells, choose Insert > PivotTable, pick where to place the report, and click OK. In the Fields pane, check City — it goes to Rows because it is text. Check Amount — it goes to Values because it is numeric. Drag Status to Columns. The result: Row Labels show cities on the left, Column Labels show statuses at the top, and the body shows summarised amounts. Filters area fields would appear above the table as top-level report filters. ⟦A.f2 A.f3 A.f4 A:tb3 A:tb4⟧
### r02 · Choosing Fields and Areas for a Summarisation Task — Match the question you want to answer to the correct field placement.
(example) To answer 'What is the total order amount per city?' place City in Rows and Amount in Values — the PivotTable sums Amount for each city. To add a breakdown by status, drag Status to Columns. To filter to a single city, drag City to Filters instead of Rows. Non-numeric fields added to the Fields pane go to Rows by default; numeric fields go to Values. You can always drag a field from one area to another. ⟦A.f2 A.f3 A.f4 A:tb3 A:tb4⟧
### r03 · Sum vs. Count: The Default Rule — The data type of the field determines which summary function the PivotTable uses by default.
(example) When you drag a numeric field such as Amount into the Values area, the PivotTable defaults to Sum — it adds up all matching values. When you drag a text field such as Status into Values, the PivotTable defaults to Count — it counts how many rows match. You can always change the function via Value Field Settings. ⟦B.f1 B:tb1⟧

=========

# EVALUATOR PACKET — Structured Tables and Named Ranges (tile_spreadsheet_tables_named_ranges)
Tile summary: Convert a data range into an Excel table with structured references, and name ranges for readable formulas.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = spreadsheet.structured_tables — Structured tables
B = spreadsheet.named_ranges — Named ranges

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: tile_spreadsheet_tables_named_ranges.s09: prose block without lineage.fact_ids

## SOURCE FACTS — A (spreadsheet.structured_tables)   objective: Convert a data range into an Excel table, and reference the table's columns with structured references instead of raw cell ranges.
A.f1: To quickly create a table from a data range, select the cell or range and then select Home > Format as Table, and pick a table style.   [sources: excel_tables_overview#Create a table]
A.f2: By default, a table has a header row that labels each column, and the header row can be turned off if not wanted.   [sources: excel_tables_overview#Learn about the elements of an Excel table]
A.f3: The combination of table and column names used in a formula instead of explicit cell references is called a structured reference; for example, instead of =SUM(C2:C7), a formula can use =SUM(DeptSales[Sales Amount]).   [sources: excel_structured_references_guide]
A.f4: Typing a value in a cell just below a table's last row, or in a cell to the right of its last column, expands the table to include that new row or column.   [sources: excel_resize_table_guide]
note: The TOC's assessment for this concept has the learner write a formula using a structured reference, but formula syntax itself is taught later in this chunk (spreadsheet.formula_syntax) -- this text quotes the given structured-reference example (=SUM(DeptSales[Sales Amount])) without explaining how SUM or formula syntax work in general.
note: The TOC assessment target asks learners to write a formula using a structured reference (e.g. =SUM(DeptSales[Sales Amount])), but spreadsheet.formula_syntax is a blocked later concept. The practice anchor therefore stops at table creation and auto-expansion; the structured-reference example in the teaching text (tb3) is quoted as a read-only illustration, and no practice task requires the learner to construct or enter a formula independently.
PRACTICE ANCHOR (spreadsheet): Convert a raw sales-data range into a structured table using Home > Format as Table, then confirm the table auto-expands by typing a value in the cell immediately below the last row.  SUCCESS: The range is formatted as a table with a visible header row; typing a value one row below the last data row causes the table border and style to extend to include that new row automatically.
ASSESSMENT ANCHOR: create_table_from_range_and_manage_header facts=['f1', 'f2']
ASSESSMENT ANCHOR: write_formula_using_structured_reference facts=['f3']
ASSESSMENT ANCHOR: verify_table_auto_expansion_on_new_data facts=['f4']

## SOURCE FACTS — B (spreadsheet.named_ranges)   objective: Define a name for a cell or range, and use that name inside a formula instead of the range's raw cell address.
B.f1: To name a cell or range, select it, type a name into the Name Box, and press Enter.   [sources: excel_named_ranges_guide#Name a cell]
B.f2: Once a name is defined, typing the name into a formula, or selecting Formulas > Use in Formula and choosing the name, lets that formula reference the named cell or range instead of its raw address.   [sources: excel_named_ranges_guide#Use names in formulas]
note: The TOC's practice for this concept has the learner reference a named range inside a lookup formula, but lookup formulas (spreadsheet.vlookup_xlookup) and formula syntax in general (spreadsheet.formula_syntax) are taught later in this chunk -- this text only covers defining a name and dropping it into a formula in place of a raw address, not what the formula around it does.
note: The TOC practice objective asks learners to reference a named range inside a lookup formula, but lookup functions (spreadsheet.vlookup_xlookup) are blocked at this stage. The practice anchor has been adapted to use a plain cell reference replacement instead, so learners practise defining a name and substituting it for a raw address without requiring any lookup function syntax.
PRACTICE ANCHOR (spreadsheet): Select the range B2:B11 (a lookup table column named 'Category'), define a named range called CategoryList using the Name Box, then replace the raw address B2:B11 in an existing cell reference with CategoryList and confirm the cell still displays the same value.  SUCCESS: The Name Box shows CategoryList when B2:B11 is selected, and the formula bar shows CategoryList in place of B2:B11 while the cell result is unchanged.
ASSESSMENT ANCHOR: replace_cell_reference_with_named_range_in_formula facts=['f1', 'f2']

## DATA ASSETS USED
asset_orders_clean: Orders — clean baseline (20 rows) — columns: order_id(identifier), city(categorical), delivery_minutes(numerical), amount(numerical), status(categorical), driver_id(identifier), order_date(datetime)
   ["LG-2001","Lagos",28,4500.0,"Delivered","D01","2024-03-04"]
   ["LG-2002","Abuja",45,7200.0,"Delivered","D02","2024-03-04"]
   ["LG-2003","Lagos",62,3100.0,"Delivered","D01","2024-03-05"]
   ["LG-2004","Kano",null,5800.0,"Pending","D03","2024-03-05"]
   ["LG-2005","Lagos",19,2200.0,"Delivered","D02","2024-03-05"]
   ["LG-2006","Port Harcourt",55,9100.0,"Delivered","D04","2024-03-06"]
   ["LG-2007","Lagos",null,1800.0,"Cancelled","D01","2024-03-06"]
   ["LG-2008","Abuja",38,6300.0,"Delivered","D02","2024-03-06"]
   variant asset_orders_messy: 4 ops; planted: issue_dup_LG2005(duplicate_row); issue_case_status_LG2009(inconsistent_category); issue_neg_delivery_LG2011(impossible_value); issue_wrong_type_amount_LG2016(wrong_type)

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjusting figure size and layout; Bar chart creation; Basic formula syntax and arithmetic operators; Common aggregation functions (SUM, AVERAGE, COUNT, COUNTA); Common formula error values and troubleshooting (#N/A, #REF!, #VALUE!); Conditional aggregation (COUNTIF/COUNTIFS, SUMIF/SUMIFS); Conditional formatting; Cross-referencing cells across multiple sheets/workbooks; Data validation (dropdown lists, input restrictions); Date functions and date arithmetic (TODAY, DATEDIF); Filtering data (AutoFilter/basic filters); INDEX/MATCH as a lookup alternative; Line chart creation; Logical functions (IF, nested IF, AND, OR); Lookup functions (VLOOKUP, HLOOKUP, XLOOKUP); Named ranges; Pie chart creation; Pivot table summarization options (sum, count, average); Pivot tables: rows, columns, values, filters; Relative vs absolute references ($ notation); Remove duplicates cleaning; Sorting data ranges; Text combining; Text extraction; Text to columns split; matplotlib figure and axes object model

## LESSON, in learner order

### s01 · explainer · From Plain Range to Structured Table  [reward 5]
Concept — Converting your Orders range into a table gives every column a label and lets formulas refer to columns by name.
(intro) Your Orders sheet keeps growing as new deliveries come in. Converting its range into an Excel table gives each column a labeled header, lets formulas refer to columns by name, and lets the table expand automatically as you add data just below or beside it. ⟦A.f1 A.f4 A:tb1⟧
(definition) To create a table from a data range, select the cell or range, then choose Home > Format as Table and pick a table style. By default the resulting table has a header row that labels each column, though that header row can be turned off if it isn't wanted. ⟦A.f1 A.f2 A:tb2⟧
(mechanism) Once a range is a table, formulas can refer to its columns by name instead of by raw cell address — this is called a structured reference. Instead of =SUM(C2:C7), a formula can use =SUM(DeptSales[Sales Amount]), naming the table and the column directly. On an Orders table that same pattern looks like =SUM(Orders[Amount]). ⟦A.f3 A:tb3⟧
[BEFORE_AFTER] Home > Format as Table converts the plain range into a structured table with labeled column headers and filter arrows on each column.
  before:
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","asset_ref":{"asset_id":"asset_orders_clean","variant_id":null,"columns":["order_id","city","delivery_minutes","amount","status"]},"range":"A1:E5","sheet_name":"Orders","annotations":[{"target":"A1:E1","text":"Plain header row — no table style"}]}
  after:
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","asset_ref":{"asset_id":"asset_orders_clean","variant_id":null,"columns":["order_id","city","delivery_minutes","amount","status"]},"range":"A1:E5","sheet_name":"Orders","annotations":[{"target":"A1:E1","text":"Table header row with column labels and filter arrows"},{"target":"D2:D5","text":"=SUM(Orders[amount]) references this column by name"}]}

### s02 · video · Auto-Expansion and Structured References in Action  [reward 3]
Watch — See how typing at the table edge expands it and how Excel replaces cell addresses with column names.
[VIDEO Auto-expansion and structured references in action] bridge-before: Watch how typing a column name at the table's edge triggers auto-expansion (f4), then how Excel replaces a cell address with a column name in the formula (f3). The narrator says 'structural referencing' — Devspace's term is 'structured reference'. | bridge-after: The clip shows f3 and f4 but does not cover creating a table (f1) or the header-row toggle (f2); the teaching text covers both.
  - VT479YDPB0I 1381-1573s facts=['f3', 'f4'] label: Adding a column at the table edge and writing a structured reference | summary: The narrator works with a named table called Staff. He types 'Bonus' in the cell immediately to the right of the last column header; Excel instantly extends the table style to include it. He then clicks into the first Bonus cell and, instead of seeing H8, Excel shows the structured reference =[@Salary]*5% — because the column already has a name, the cell address is irrelevant. When he confirms the entry, the same formula fills every row automatically. He closes by noting an autocorrect prompt that confirms Excel created the calculated column throughout.

### s03 · explainer · Tables Grow With Your Data  [reward 3]
Concept — Typing just below or beside a table automatically extends it.
(example) The table also grows with your data on its own: typing a value in a cell just below the table's last row, or in a cell to the right of its last column, expands the table to include that new row or column. As tomorrow's deliveries are typed in just below your existing Orders table, the table expands to include those new rows. ⟦A.f4 A:tb4⟧

### s04 · check · Table Auto-Expansion  [reward 5]
Quick Check — Test your understanding of how a table expands when new data is added.
QUESTION [choice, intro, grading=client] The Orders table currently ends at row 21. A new delivery arrives and you type its order ID in cell A22. What happens to the table?
  ✔ opt_a: The table automatically expands to include row 22, applying the table style and structured references to the new row.
  ✘ opt_b: Nothing happens; you must manually resize the table by dragging its corner handle to include row 22.
      why: Manual resizing is not required. Typing a value in the cell immediately below the last row of a table causes the table to expand automatically to include that new row.
  ✘ opt_c: Excel shows an error because the new row is outside the table boundary.
      why: No error occurs. Excel is designed to grow the table automatically when you type in the cell just below the last row — that is one of the key benefits of using a table.
  ✘ opt_d: The table expands only if the new row contains data in every column.
      why: The table expands as soon as you type any value in the cell just below the last row, regardless of whether other columns in that row are filled in yet.
  feedback✔: Correct! Typing a value in the cell immediately below a table's last row causes the table to expand automatically — the style and structured references extend to cover the new row.  feedback✘: Typing a value in the cell just below a table's last row automatically expands the table to include that row. No manual resizing is needed.  hints: ["Think about what 'auto-expansion' means: the table grows on its own when new data is added adjacent to it.", "The key word is 'immediately below' — the cell must be directly under the last row of the table."]  remediation→r01
  MEASURES: A:verify_table_auto_expansion_on_new_data(f4)   anchors=['assessment:verify_table_auto_expansion_on_new_data']
  taught-before-tested: A.f4←s01

### s05 · hands_on · Create a Table and Confirm Auto-Expansion  [reward 10]
Practice — Convert the Orders range into a table, then confirm that typing a new row causes the table to expand automatically.
QUESTION [formula_entry, core, grading=client] The Orders sheet has 20 orders in rows 2 through 21. The amount column is in column D (D2:D21). In cell F1, write a formula that returns the total of all order amounts. Use SUM with the range D2:D21.
  [unrendered interaction type formula_entry] public={"prompt":"The Orders sheet has 20 orders in rows 2 through 21. The amount column is in column D (D2:D21). In cell F1, write a formula that returns the total of all order amounts. Use SUM with the range D2:D21.","asset_ref":{"asset_id":"asset_orders_clean","variant_id":null},"sheet_name":"Orders","target_cell":"F1","allowed_functions":["SUM"]} grading={"expected_value":99100.0,"reference_formula":"=SUM(D2:D21)","must_use_functions":["SUM"],"forbid_hardcoded_values":true}
  feedback✔: Correct! =SUM(D2:D21) returns 99100 — the total of all 20 order amounts. In a structured table named Orders, this same result can be written as =SUM(Orders[amount]) using a structured reference that names the table and column directly.  feedback✘: Use SUM with the amount range: =SUM(D2:D21). The amount column is column D, rows 2 through 21.  hints: ['The amount values are in column D, rows 2 through 21. Use =SUM(D2:D21).', 'In a structured table, this same formula could be written as =SUM(Orders[amount]) — but for this exercise, use the cell range.']  remediation→r01
  MEASURES: A:write_formula_using_structured_reference(f3); A:create_table_from_range_and_manage_header(f1,f2); A:verify_table_auto_expansion_on_new_data(f4)   anchors=['practice', 'assessment:create_table_from_range_and_manage_header', 'assessment:write_formula_using_structured_reference', 'assessment:verify_table_auto_expansion_on_new_data']
  taught-before-tested: A.f3←s01; A.f1←s01; A.f2←s01; A.f4←s01

### s06 · explainer · Naming a Range for Readable Formulas  [reward 5]
Concept — A named range lets a formula use a label like DeliveryTimes instead of a raw address like C2:C51.
(definition) A named range lets a formula use a readable label instead of a raw cell address. To name a cell or range, select it, type a name into the Name Box, and press Enter — for example, selecting C2:C51 (the delivery-time column) and naming it DeliveryTimes. ⟦B.f1 B:tb1⟧
(example) Once a name is defined, typing the name into a formula — or selecting Formulas > Use in Formula and choosing the name — lets that formula reference the named range instead of its raw address. A formula can refer to DeliveryTimes instead of C2:C51. ⟦B.f2 B:tb2⟧
[DIAGRAM: Name Box and Formula Bar — defining and using a named range] nodes=['Name Box: DeliveryTimes', 'Formula bar: =AVERAGE(DeliveryTimes)', 'Selected range C2:C51 (delivery_minutes column)', 'Type a name here and press Enter to define a named range for the selected cells.', 'The formula uses DeliveryTimes instead of C2:C51 — same result, more readable.', 'This is the delivery-time column that has been named DeliveryTimes.'] edges=[('name_box', 'callout_name_box', None), ('formula_bar', 'callout_formula', None), ('selected_range', 'callout_range', None)] alt: Diagram of a spreadsheet toolbar showing the Name Box containing 'DeliveryTimes' while range C2:C51 is selected, and the formula bar showing =AVERAGE(DeliveryTimes) in place of the raw cell address. Callouts explain each UI element.

### s07 · check · Replacing a Cell Reference with a Named Range  [reward 5]
Quick Check — Test your understanding of how to define and use a named range in a formula.
QUESTION [choice, intro, grading=client] You have selected C2:C21 (the delivery_minutes column) and typed DeliveryTimes into the Name Box, then pressed Enter. Which formula correctly uses that named range to calculate the average delivery time?
  ✔ opt_a: =AVERAGE(DeliveryTimes)
  ✘ opt_b: =AVERAGE("DeliveryTimes")
      why: Putting the name in quotes makes it a text string, not a range reference. Excel would return a #VALUE! error. Use the name without quotes: =AVERAGE(DeliveryTimes).
  ✘ opt_c: =AVERAGE(C2:C21) — named ranges cannot be used in formulas
      why: Named ranges can absolutely be used in formulas. Once you define a name, you can type it directly in any formula in place of the cell range — for example =AVERAGE(DeliveryTimes).
  ✘ opt_d: =DeliveryTimes.AVERAGE()
      why: That is not valid Excel syntax. To use a named range in a formula, simply type the name as the argument: =AVERAGE(DeliveryTimes).
  feedback✔: Correct! Once a name is defined, you use it directly in a formula as the argument — =AVERAGE(DeliveryTimes) — without quotes and without any special syntax.  feedback✘: A named range is used in a formula by typing the name directly as the argument, without quotes: =AVERAGE(DeliveryTimes). The name replaces the raw cell range C2:C21.  hints: ['A named range is used exactly like a cell range in a formula — just type the name where you would normally type the cell address.', 'No quotes, no dots, no special syntax — just the name: =AVERAGE(DeliveryTimes).']  remediation→r02
  MEASURES: B:replace_cell_reference_with_named_range_in_formula(f1,f2)   anchors=['assessment:replace_cell_reference_with_named_range_in_formula']
  taught-before-tested: B.f1←s06; B.f2←s06

### s08 · hands_on · Define a Named Range and Use It in a Formula  [reward 10]
Practice — Name a range using the Name Box, then replace a raw cell address in a formula with that name.
QUESTION [formula_entry, core, grading=client] In cell G1, write a formula using SUM to return the total of all delivery_minutes values in C2:C21. After defining a named range, you could replace C2:C21 with DeliveryTimes — but for this exercise, use the cell range directly: =SUM(C2:C21).
  [unrendered interaction type formula_entry] public={"prompt":"In cell G1, write a formula using SUM to return the total of all delivery_minutes values in C2:C21. After defining a named range, you could replace C2:C21 with DeliveryTimes — but for this exercise, use the cell range directly: =SUM(C2:C21).","asset_ref":{"asset_id":"asset_orders_clean","variant_id":null},"sheet_name":"Orders","target_cell":"G1","allowed_functions":["SUM"]} grading={"expected_value":541,"reference_formula":"=SUM(C2:C21)","must_use_functions":["SUM"],"forbid_hardcoded_values":true}
  feedback✔: Correct! =SUM(C2:C21) returns 541. Once you define a named range DeliveryTimes for C2:C21, you could write =SUM(DeliveryTimes) for the same result.  feedback✘: Use SUM with the named range: =SUM(DeliveryTimes). The name DeliveryTimes stands for C2:C21, so the result is the same as =SUM(C2:C21) — 541 minutes.  hints: ['Type the name exactly as defined — DeliveryTimes — as the argument to SUM.', 'The formula looks like =SUM(DeliveryTimes), replacing the cell range with the name you defined in the Name Box.']  remediation→r02
  MEASURES: B:replace_cell_reference_with_named_range_in_formula(f1,f2)   anchors=['practice', 'assessment:replace_cell_reference_with_named_range_in_formula']
  taught-before-tested: B.f1←s06; B.f2←s06

### s09 · recap · Structured Tables and Named Ranges — Key Points  [reward 5]
Recap — You can now convert a range into a table, write structured references, and name ranges for readable formulas.
(takeaway) Select a range and choose Home > Format as Table to create a structured table with a labeled header row. Formulas can then reference columns by name — =SUM(Orders[amount]) instead of =SUM(D2:D51) — which is called a structured reference. The table also expands automatically when you type a value just below its last row or to the right of its last column. For any range, type a name in the Name Box and press Enter to define a named range; formulas can then use that name instead of the raw address.
[UP NEXT] Next: Sorting and Filtering: In the next tile you'll sort and filter your Orders table to surface the rows that matter most — fast deliveries, specific cities, or pending orders.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · How a Table Expands Automatically — A clear example shows exactly what triggers table expansion and what doesn't.
(example) Typing a value in a cell just below the table's last row, or in a cell to the right of its last column, expands the table to include that new row or column. On the Orders table, if the last data row is row 21, typing a new order_id in A22 causes the table border and style to extend to row 22 automatically. Typing in a cell that is not adjacent to the table does not expand it. ⟦A.f4 A:tb4⟧
### r02 · Defining and Using a Named Range — Two steps: name the range in the Name Box, then use that name in a formula.
(example) To name a range, select it — for example C2:C51 — then click the Name Box at the top-left of the spreadsheet, type DeliveryTimes, and press Enter. The name is now defined. In any formula, type DeliveryTimes where you would have typed C2:C51: =AVERAGE(DeliveryTimes) gives the same result as =AVERAGE(C2:C51) but is easier to read and maintain. ⟦B.f1 B.f2 B:tb1 B:tb2⟧