# EVALUATOR PACKET — Structured Tables and Named Ranges (tile_spreadsheet_tables_named_ranges)
Tile summary: Convert a data range into an Excel table with structured references, and name ranges for readable formulas.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = spreadsheet.structured_tables — Structured tables
B = spreadsheet.named_ranges — Named ranges

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
img_named_range_name_box: MISSING

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
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · explainer · Tables Grow With Your Data  [reward 3]
Concept — Typing just below or beside a table automatically extends it.
(example) The table also grows with your data on its own: typing a value in a cell just below the table's last row, or in a cell to the right of its last column, expands the table to include that new row or column. As tomorrow's deliveries are typed in just below your existing Orders table, the table expands to include those new rows. ⟦A.f4 A:tb4⟧

### s04 · check · Table Auto-Expansion  [reward 5]
Quick Check — Test your understanding of how a table expands when new data is added.

### s05 · hands_on · Create a Table and Confirm Auto-Expansion  [reward 10]
Practice — Convert the Orders range into a table, then confirm that typing a new row causes the table to expand automatically.

### s06 · explainer · Naming a Range for Readable Formulas  [reward 5]
Concept — A named range lets a formula use a label like DeliveryTimes instead of a raw address like C2:C51.
(definition) A named range lets a formula use a readable label instead of a raw cell address. To name a cell or range, select it, type a name into the Name Box, and press Enter — for example, selecting C2:C51 (the delivery-time column) and naming it DeliveryTimes. ⟦B.f1 B:tb1⟧
(example) Once a name is defined, typing the name into a formula — or selecting Formulas > Use in Formula and choosing the name — lets that formula reference the named range instead of its raw address. A formula can refer to DeliveryTimes instead of C2:C51. ⟦B.f2 B:tb2⟧
[ANNOTATED_IMAGE — unrendered type, raw] {"type":"annotated_image","block_id":"tile_spreadsheet_tables_named_ranges.s06.ai1","asset_id":"img_named_range_name_box","alt_text":"Spreadsheet screenshot showing the Name Box containing 'DeliveryTimes' while the range C2:C51 is selected, and the formula bar showing =AVERAGE(DeliveryTimes) in place of the raw cell address.","hotspots":[{"x":0.05,"y":0.04,"w":0.18,"h":0.06,"label":"Name Box","detail":"Type a name here and press Enter to define a named range for the selected cells."},{"x":0.25,"y":0.04,"w":0.4,"h":0.06,"label":"Formula bar","detail":"The formula uses DeliveryTimes instead of C2:C51 — same result, more readable."},{"x":0.05,"y":0.12,"w":0.08,"h":0.7,"label":"Selected range C2:C51","detail":"This is the delivery-time column that has been named DeliveryTimes."}],"lineage":{"concept_ids":["spreadsheet.named_ranges"],"teaching_block_ids":["spreadsheet.named_ranges#tb1","spreadsheet.named_ranges#tb2"],"fact_ids":["spreadsheet.named_ranges#f1","spreadsheet.named_ranges#f2"],"anchors":["spreadsheet.named_ranges#visual"]}}

### s07 · check · Replacing a Cell Reference with a Named Range  [reward 5]
Quick Check — Test your understanding of how to define and use a named range in a formula.

### s08 · hands_on · Define a Named Range and Use It in a Formula  [reward 10]
Practice — Name a range using the Name Box, then replace a raw cell address in a formula with that name.

### s09 · recap · Structured Tables and Named Ranges — Key Points  [reward 5]
Recap — You can now convert a range into a table, write structured references, and name ranges for readable formulas.
(takeaway) Select a range and choose Home > Format as Table to create a structured table with a labeled header row. Formulas can then reference columns by name — =SUM(Orders[amount]) instead of =SUM(D2:D51) — which is called a structured reference. The table also expands automatically when you type a value just below its last row or to the right of its last column. For any range, type a name in the Name Box and press Enter to define a named range; formulas can then use that name instead of the raw address.
[UP NEXT] Next: Sorting and Filtering: In the next tile you'll sort and filter your Orders table to surface the rows that matter most — fast deliveries, specific cities, or pending orders.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · How a Table Expands Automatically — A clear example shows exactly what triggers table expansion and what doesn't.
(example) Typing a value in a cell just below the table's last row, or in a cell to the right of its last column, expands the table to include that new row or column. On the Orders table, if the last data row is row 21, typing a new order_id in A22 causes the table border and style to extend to row 22 automatically. Typing in a cell that is not adjacent to the table does not expand it. ⟦A.f4 A:tb4⟧
### r02 · Defining and Using a Named Range — Two steps: name the range in the Name Box, then use that name in a formula.
(example) To name a range, select it — for example C2:C51 — then click the Name Box at the top-left of the spreadsheet, type DeliveryTimes, and press Enter. The name is now defined. In any formula, type DeliveryTimes where you would have typed C2:C51: =AVERAGE(DeliveryTimes) gives the same result as =AVERAGE(C2:C51) but is easier to read and maintain. ⟦B.f1 B.f2 B:tb1 B:tb2⟧

=========

# EVALUATOR PACKET — Pivot Tables (tile_spreadsheet_pivot_tables)
Tile summary: Build a PivotTable to summarise Orders data by city and status, then change the value-field summary function.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = spreadsheet.pivot_tables — Pivot tables: rows, columns, values, filters
B = spreadsheet.pivot_summarization — Pivot table summarization options (sum, count, average)

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
img_pivot_fields_pane: MISSING

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjusting figure size and layout; Bar chart creation; Bar charts; Basic A/B test structure (control vs treatment group); Basic plot creation with the pyplot interface; Box plots; Conceptual effect of sample size on confidence; Conceptual interpretation of statistical significance/confidence level; Custom styling/theming (advanced/optional); Drawing a business conclusion from an experiment-result summary; Histograms; Identifying the business decision a stakeholder needs the analysis to inform; Interpreting lift/percentage change between groups; Labeling axes, titles, and legends; Line chart creation; Line plots; Matching chart type to the analytical question; Multi-panel figures/subplots (advanced/optional); Pie chart creation; Pivot table summarization options (sum, count, average); Plotting directly from pandas DataFrames with seaborn; Scatter plots; Stating a finding precisely and quantitatively (the specific number or comparison, not a vague claim); matplotlib figure and axes object model; seaborn built-in themes and color palettes; seaborn statistical plotting functions

## LESSON, in learner order

### s01 · explainer · What a PivotTable Does and How to Build One  [reward 5]
Concept — A PivotTable summarises your Orders data by city, status, or any other field — no formulas required.
(intro) Reading down a long Orders sheet to compare total amounts by city and status by hand would take forever. A PivotTable is a tool to calculate, summarize, and analyze data that lets you see comparisons, patterns, and trends in your data. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) To create a PivotTable, select the data cells, select Insert > PivotTable, choose where to place the PivotTable report, and select OK. To add a field, select its checkbox in the PivotTable Fields pane; non-numeric fields go to Rows and numeric fields go to Values by default. A field can be moved to a different area by dragging it there. ⟦A.f2 A.f3 A:tb3⟧
(example) Filters area fields appear as top-level report filters above the PivotTable. Columns area fields appear as Column Labels at the top. Rows area fields appear as Row Labels on the left. Values area fields appear as summarised numeric values in the body. Building a PivotTable from your Orders data with City in Rows, Status in Columns, and Amount in Values gives a grid of summarised order amounts for every city/status combination. ⟦A.f4 A:tb4⟧
[ANNOTATED_IMAGE — unrendered type, raw] {"type":"annotated_image","block_id":"tile_spreadsheet_pivot_tables.s01.ai1","asset_id":"img_pivot_fields_pane","alt_text":"Screenshot of the PivotTable Fields pane showing four drop zones: Filters (top), Columns (top-right), Rows (bottom-left), and Values (bottom-right), with City in Rows, Status in Columns, and Amount in Values.","hotspots":[{"x":0.05,"y":0.05,"w":0.9,"h":0.12,"label":"Filters area","detail":"Fields here appear as top-level report filters above the PivotTable."},{"x":0.5,"y":0.55,"w":0.45,"h":0.2,"label":"Columns area","detail":"Fields here appear as Column Labels at the top of the PivotTable. Status is placed here."},{"x":0.05,"y":0.55,"w":0.4,"h":0.2,"label":"Rows area","detail":"Fields here appear as Row Labels on the left side. City is placed here."},{"x":0.5,"y":0.78,"w":0.45,"h":0.18,"label":"Values area","detail":"Fields here appear as summarised numeric values in the body. Amount is placed here."}],"lineage":{"concept_ids":["spreadsheet.pivot_tables"],"teaching_block_ids":["spreadsheet.pivot_tables#tb3","spreadsheet.pivot_tables#tb4"],"fact_ids":["spreadsheet.pivot_tables#f2","spreadsheet.pivot_tables#f3","spreadsheet.pivot_tables#f4"],"anchors":["spreadsheet.pivot_tables#visual"]}}

### s02 · video · Building a PivotTable: Fields, Areas, and Layout  [reward 3]
Watch — Watch how each field snaps into its area and the summary grid rearranges instantly.
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · explainer · What Each PivotTable Area Displays  [reward 3]
Concept — Each of the four drop zones produces a distinct visual output in the PivotTable.
(definition) Filters area fields are shown as top-level report filters above the PivotTable. Columns area fields are shown as Column Labels at the top of the PivotTable. Rows area fields are shown as Row Labels on the left side of the PivotTable. Values area fields are shown as summarised numeric values in the body of the PivotTable. ⟦A.f4 A:tb4⟧

### s04 · check · Creating a PivotTable and Reading Its Areas  [reward 5]
Quick Check — Test your understanding of the creation steps and what each area displays.

### s05 · check · Building a PivotTable to Answer a Question  [reward 5]
Quick Check — Apply your knowledge of fields, areas, and creation steps to a summarisation task.

### s06 · hands_on · Build a PivotTable from the Orders Data  [reward 10]
Practice — Create a PivotTable and place fields in the Rows, Columns, and Values areas.

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
[VIDEO ] bridge-before:  | bridge-after: 

### s09 · check · Default Summarisation by Data Type  [reward 5]
Quick Check — Test your understanding of when a PivotTable defaults to Sum versus Count.

### s10 · hands_on · Switch the Summary Function to Average  [reward 10]
Practice — Change the Values area from Sum to Average using Value Field Settings.

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

# EVALUATOR PACKET — Chart Types (tile_spreadsheet_chart_types)
Tile summary: Build bar, line, and pie charts from Orders data to visualise comparisons, trends, and part-of-whole shares.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = spreadsheet.bar_chart_creation — Bar chart creation
B = spreadsheet.line_chart_creation — Line chart creation
C = spreadsheet.pie_chart_creation — Pie chart creation

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Building a Bar Chart from Category Data  [reward 5]
Quick Check — Test your understanding of bar chart axis encoding and the Insert > Recommended Charts workflow.

### s04 · hands_on · Build a Bar Chart from City Totals  [reward 10]
Practice — Select the city totals table and insert a bar chart using Insert > Recommended Charts.

### s05 · explainer · Line Charts: Showing Trends Over Time  [reward 5]
Concept — A line chart distributes evenly-spaced time intervals along the horizontal axis and values along the vertical axis.
(definition) In a line chart, category data is distributed evenly along the horizontal axis and value data along the vertical axis. Line charts can show continuous data over time on an evenly scaled axis, making them well suited to showing trends at equal intervals such as months, quarters, or fiscal years. A summary of total order amount by month is exactly this kind of evenly-spaced, time-ordered data. ⟦B.f1 B:tb1⟧
(mechanism) To create a line chart, select the data, choose Insert > Recommended Charts, and select a chart on the Recommended Charts tab to preview it. If you don't see a line chart you like, select the All Charts tab to see all chart types, select the chart, and click OK. ⟦B.f2 B:tb2⟧
[TABLE asset_monthly_summary cols=['month_label', 'total_amount'] tags=month_label:Horizontal axis (equal intervals), total_amount:Vertical axis (NGN)] caption: Monthly order totals — source data for a line chart. Each month is evenly spaced on the horizontal axis; total_amount maps to the vertical axis.

### s06 · video · Building a Line Chart from Monthly Sales Data  [reward 3]
Watch — See how to assign the data range and set the horizontal-axis labels.
[VIDEO ] bridge-before:  | bridge-after: 

### s07 · check · Axis Roles and Interval Suitability  [reward 5]
Quick Check — Test your understanding of which axis carries time intervals and when a line chart is appropriate.

### s08 · check · Building a Line Chart from Time-Ordered Data  [reward 5]
Quick Check — Apply your knowledge of axis encoding and the Recommended Charts workflow.

### s09 · hands_on · Build a Line Chart from Monthly Totals  [reward 10]
Practice — Select the monthly summary table and insert a line chart using Insert > Recommended Charts.

### s10 · explainer · Pie Charts: Part-of-Whole Shares  [reward 5]
Concept — A pie chart shows each category's share of a total — but only when the data meets four conditions.
(definition) Pie charts show the size of items in one data series proportional to the sum of the items. They are appropriate when you have only one data series to plot, none of the values are negative, there are no more than seven categories, and the categories represent parts of the whole pie. A summary of total order amount by city, for no more than seven cities, fits that description as long as no amount is negative. ⟦C.f1 C:tb1⟧
(mechanism) To create a pie chart, select the data, choose Insert > Recommended Charts, and select a chart on the Recommended Charts tab to preview it. If you don't see a pie chart you like, select the All Charts tab to see all chart types, select the chart, and click OK. ⟦C.f2 C:tb2⟧
[CHART pie: Total Order Amount by City (NGN)] data=asset_city_totals x=city y=total_amount color=None annotations=[] alt: Pie chart showing six slices, one per city. Lagos is the largest slice, followed by Abuja, Port Harcourt, Kano, Ibadan, and Enugu. Each slice is labelled with the city name and its share of total order amount.

### s11 · video · When a Pie Chart Works: Proportional Slices  [reward 3]
Watch — See how even-split versus clear-winner data affects whether a pie chart communicates clearly.
[VIDEO ] bridge-before:  | bridge-after: 

### s12 · check · Building a Pie Chart from Category Totals  [reward 5]
Quick Check — Test your understanding of pie chart eligibility conditions and the creation workflow.

### s13 · hands_on · Build a Pie Chart from City Totals  [reward 10]
Practice — Select the city totals table and insert a pie chart using Insert > Recommended Charts.

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
img_data_validation_dialog: MISSING

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjusting figure size and layout; Bar chart creation; Bar charts; Basic formula syntax and arithmetic operators; Basic plot creation with the pyplot interface; Common aggregation functions (SUM, AVERAGE, COUNT, COUNTA); Common formula error values and troubleshooting (#N/A, #REF!, #VALUE!); Conditional aggregation (COUNTIF/COUNTIFS, SUMIF/SUMIFS); Cross-referencing cells across multiple sheets/workbooks; Data validation (dropdown lists, input restrictions); Date functions and date arithmetic (TODAY, DATEDIF); Histograms; INDEX/MATCH as a lookup alternative; Line chart creation; Line plots; Logical functions (IF, nested IF, AND, OR); Lookup functions (VLOOKUP, HLOOKUP, XLOOKUP); Pie chart creation; Pivot table summarization options (sum, count, average); Pivot tables: rows, columns, values, filters; Relative vs absolute references ($ notation); Remove duplicates cleaning; Text combining; Text extraction; Text to columns split; matplotlib figure and axes object model

## LESSON, in learner order

### s01 · explainer · Highlighting Cells Automatically by Value  [reward 5]
Concept — Conditional formatting applies a format to cells based on rules you create — no manual colouring needed.
(definition) Conditional formatting applies a format to cells automatically based on rules you create that determine the format based on the cells' values — rather than you manually colouring cells one at a time. ⟦A.f1 A:tb1⟧
(mechanism) To apply a quick conditional formatting rule, select the cells, then on the Home tab in the Style group select Conditional Formatting > Highlight Cells Rules, choose a comparison command such as Less Than, enter the comparison value, and select a format. Selecting the delivery-time column and applying Highlight Cells Rules > Less Than with a value of 15 and a green fill automatically colours every delivery under 15 minutes. ⟦A.f2 A:tb2⟧
[BEFORE_AFTER] Home > Conditional Formatting > Highlight Cells Rules > Less Than, value 15, green fill — cells below 15 are automatically coloured; cells at or above 15 remain unformatted.
  before:
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","asset_ref":{"asset_id":"asset_orders_clean","variant_id":null,"columns":["order_id","delivery_minutes"]},"range":"A1:B8","sheet_name":"Orders","annotations":[{"target":"B1:B8","text":"delivery_minutes — no formatting applied"}]}
  after:
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","asset_ref":{"asset_id":"asset_orders_clean","variant_id":null,"columns":["order_id","delivery_minutes"]},"range":"A1:B12","sheet_name":"Orders","annotations":[{"target":"B2","text":"28 — no fill (≥ 15)"},{"target":"B6","text":"19 — no fill (≥ 15)"},{"target":"B12","text":"14 — green fill (< 15)"}]}

### s02 · video · Applying a Conditional Formatting Rule via Highlight Cells Rules  [reward 3]
Watch — See the menu path and how the rule re-evaluates automatically when cell values change.
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Applying a Conditional Formatting Rule  [reward 5]
Quick Check — Test your understanding of how to set up a Highlight Cells Rules rule.

### s04 · hands_on · Apply a Less Than Rule to Delivery Times  [reward 10]
Practice — Use Highlight Cells Rules to colour delivery times below a threshold in red.

### s05 · explainer · Restricting What Users Can Enter  [reward 5]
Concept — Data validation restricts the type of data or values users can enter into a cell, and can display a custom error message.
(definition) Data validation restricts the type of data or the values users can enter into a cell, such as a dropdown list, and can display a customised error message when a user enters invalid data. ⟦B.f1 B:tb1⟧
(example) To add a dropdown-list validation rule, select the cells, choose Data > Data Validation, on the Settings tab set Allow to List, then in the Source box type the list values separated by commas, making sure the In-cell dropdown check box is selected. Restricting the Orders sheet's status column with Source set to Pending,Delivered,Cancelled gives each cell a dropdown of those three words. ⟦B.f2 B:tb2⟧
[ANNOTATED_IMAGE — unrendered type, raw] {"type":"annotated_image","block_id":"tile_spreadsheet_formatting_validation.s05.ai1","asset_id":"img_data_validation_dialog","alt_text":"Screenshot of the Data Validation dialog open on the Settings tab with Allow set to List and the Source box containing 'Pending,Delivered,Cancelled', alongside a Status column cell showing a dropdown arrow.","hotspots":[{"x":0.1,"y":0.2,"w":0.35,"h":0.08,"label":"Allow: List","detail":"Set Allow to List to create a dropdown restriction."},{"x":0.1,"y":0.45,"w":0.75,"h":0.08,"label":"Source: Pending,Delivered,Cancelled","detail":"Type the allowed values separated by commas. These become the dropdown options."},{"x":0.1,"y":0.6,"w":0.4,"h":0.06,"label":"In-cell dropdown checked","detail":"Ensures the dropdown arrow appears in the cell."},{"x":0.65,"y":0.3,"w":0.3,"h":0.12,"label":"Dropdown arrow in Status cell","detail":"The cell now shows a dropdown arrow; only the three listed values are accepted."}],"lineage":{"concept_ids":["spreadsheet.data_validation"],"teaching_block_ids":["spreadsheet.data_validation#tb1","spreadsheet.data_validation#tb2"],"fact_ids":["spreadsheet.data_validation#f1","spreadsheet.data_validation#f2"],"anchors":["spreadsheet.data_validation#visual"]}}

### s06 · explainer · Numeric, Date, and Text-Length Validation  [reward 3]
Concept — Data validation can also restrict entry to a number, date, or text of a specific length.
(example) Data validation can restrict entry to a whole number, decimal, date, time, or text length within limits: under Allow choose the type (for example Whole Number), under Data choose a condition (for example between), and then enter the minimum, maximum, or specific value to allow. On the delivery-time column, choosing Whole Number, between 0 and 300, blocks anyone from typing a negative or unreasonably large delivery time. ⟦B.f3 B:tb3⟧

### s07 · video · Restricting Cell Input: Error Alerts and Numeric Rules  [reward 3]
Watch — See how the Allow menu switches between types and how error alerts work.
[VIDEO ] bridge-before:  | bridge-after: 

### s08 · check · Data Validation Purpose and Numeric Rules  [reward 5]
Quick Check — Test your understanding of what data validation does and how to configure a numeric rule.

### s09 · check · Choosing the Right Validation Type  [reward 5]
Quick Check — Given an input restriction requirement, identify the correct validation type to use.

### s10 · hands_on · Add a Dropdown Validation Rule to the Status Column  [reward 10]
Practice — Restrict the Status column to Pending, Delivered, and Cancelled using Data > Data Validation.

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