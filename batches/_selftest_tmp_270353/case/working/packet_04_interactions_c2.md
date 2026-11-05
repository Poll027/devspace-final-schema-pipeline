# EVALUATOR PACKET — Removing Duplicates and Splitting Text (tile_spreadsheet_cleaning_cross_sheet)
Tile summary: Clean your Orders data by removing duplicate rows, split combined text into separate columns, and write formulas that reference cells on other sheets.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = spreadsheet.remove_duplicates_cleaning — Remove duplicates cleaning
B = spreadsheet.text_to_columns_split — Text to columns split
C = spreadsheet.cross_sheet_references — Cross-referencing cells across multiple sheets/workbooks

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=5
  warn: tile_spreadsheet_cleaning_cross_sheet.s04: remediation tile_spreadsheet_cleaning_cross_sheet.r01 re-teaches ['spreadsheet.remove_duplicates_cleaning#f1'] but the check measures ['spreadsheet.remove_duplicates_cleaning#f2'] — a learner who fails it is sent to an unrelated fact
  warn: tile_spreadsheet_cleaning_cross_sheet.s12: remediation tile_spreadsheet_cleaning_cross_sheet.r03 re-teaches ['spreadsheet.cross_sheet_references#f1', 'spreadsheet.cross_sheet_references#f3'] but the check measures ['spreadsheet.cross_sheet_references#f2'] — a learner who fails it is sent to an unrelated fact
  warn: remediation step tile_spreadsheet_cleaning_cross_sheet.r04 is never referenced
  warn: tile_spreadsheet_cleaning_cross_sheet.s01: prose block without lineage.fact_ids
  warn: tile_spreadsheet_cleaning_cross_sheet.s13: prose block without lineage.fact_ids

## SOURCE FACTS — A (spreadsheet.remove_duplicates_cleaning)   objective: Remove duplicate rows from a data range using the Remove Duplicates tool, choosing which columns define a duplicate.
A.f1: When you use the Remove Duplicates feature, the duplicate data is permanently deleted, so it's a good idea to copy the original data to another worksheet before removing duplicates.   [sources: excel_remove_duplicates_guide#Remove duplicate values]
A.f2: To remove duplicates, select the range of cells that has duplicate values, select Data > Remove Duplicates, and then check or uncheck the columns under Columns to choose which columns are used to identify a duplicate row.   [sources: excel_remove_duplicates_guide#Remove duplicate values]
PRACTICE ANCHOR (spreadsheet): Given a customer list worksheet containing duplicate rows, make a copy of the data on a second sheet, then use Data > Remove Duplicates on the copy to remove duplicate rows based on a chosen set of key columns (e.g., Customer ID and Email), and confirm the row count decreases as expected.  SUCCESS: The original data is preserved on one sheet; the cleaned sheet contains no duplicate rows for the chosen key columns; the learner can explain why they selected those specific columns in the Columns checklist.
ASSESSMENT ANCHOR: identify_permanent_deletion_and_copy_precaution facts=['f1']
ASSESSMENT ANCHOR: configure_and_run_remove_duplicates_with_column_selection facts=['f2']

## SOURCE FACTS — B (spreadsheet.text_to_columns_split)   objective: Split one column of delimited text into separate columns using the Convert Text to Columns Wizard.
B.f1: To split text into columns, select the cell or column that contains the text, select Data > Text to Columns, choose Delimited, select the delimiter(s) such as Comma or Space, choose the destination for the split data, and select Finish.   [sources: excel_text_to_columns_guide]
PRACTICE ANCHOR (spreadsheet): Given a spreadsheet with a single 'Full Name' column containing entries such as 'Amara Okafor', use Data > Text to Columns with Space as the delimiter to split it into separate First Name and Last Name columns.  SUCCESS: The original single column is replaced by (or accompanied by) two columns, one containing only first names and one containing only last names, with no merged values remaining.
ASSESSMENT ANCHOR: split_delimited_column_with_text_to_columns facts=['f1']

## SOURCE FACTS — C (spreadsheet.cross_sheet_references)   objective: Write a formula on one sheet that references a cell on a different sheet in the same workbook.
C.f1: A formula can refer to a cell on another sheet in the same workbook by writing the sheet name followed by an exclamation point (!) and then the cell or range reference, for example Marketing!B1.   [sources: excel_formulas_overview#Making a reference to a cell or a range of cells on another worksheet in the same workbook]
C.f2: If the referenced worksheet's name contains spaces or numbers, the name must be enclosed in single quotation marks in the reference, for example ='January Revenue'!A1.   [sources: excel_formulas_overview#Making a reference to a cell or a range of cells on another worksheet in the same workbook]
C.f3: A workbook link (previously called an external reference) to a cell range in another workbook, when the source workbook is open, includes the workbook name in square brackets, followed by the worksheet name, an exclamation point, and the cells the formula depends on, for example =SUM([Budget.xlsx]Annual!C10:C25).   [sources: excel_workbook_links_guide#What a workbook link to another workbook looks like]
PRACTICE ANCHOR (formula): Write a formula in cell B2 of a Summary sheet that pulls the value from cell B4 on a sheet named Q1 Sales.  SUCCESS: The learner writes ='Q1 Sales'!B4, correctly quoting the sheet name because it contains a space.
ASSESSMENT ANCHOR: write_same_workbook_cross_sheet_reference facts=['f1']
ASSESSMENT ANCHOR: quote_sheet_names_with_spaces_or_numbers facts=['f2']
ASSESSMENT ANCHOR: write_cross_workbook_link_with_square_bracket_syntax facts=['f3']
ASSESSMENT ANCHOR: select_correct_reference_syntax_given_formula_requirement facts=['f1', 'f2', 'f3']

## DATA ASSETS USED
asset_drivers_vlookup: Drivers — VLOOKUP layout (driver_id left, driver_name right) — columns: driver_id(identifier), driver_name(text)
   ["D01","Amara Okafor"]
   ["D02","Bello Musa"]
   ["D03","Chisom Eze"]
   ["D04","Damilola Adeyemi"]
   ["D05","Emeka Nwosu"]
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
asset_orders_location_combined: Orders — location column combined (Text to Columns exercise) — columns: order_id(identifier), location(text), delivery_minutes(numerical), amount(numerical), status(categorical), driver_id(identifier), order_date(datetime)
   ["LG-2001","Lagos,Nigeria",28,4500.0,"Delivered","D01","2024-03-04"]
   ["LG-2002","Abuja,Nigeria",45,7200.0,"Delivered","D02","2024-03-04"]
   ["LG-2003","Lagos,Nigeria",62,3100.0,"Delivered","D01","2024-03-05"]
   ["LG-2004","Kano,Nigeria",null,5800.0,"Pending","D03","2024-03-05"]
   ["LG-2005","Lagos,Nigeria",19,2200.0,"Delivered","D02","2024-03-05"]
   ["LG-2006","Port Harcourt,Nigeria",55,9100.0,"Delivered","D04","2024-03-06"]
   ["LG-2007","Lagos,Nigeria",null,1800.0,"Cancelled","D01","2024-03-06"]
   ["LG-2008","Abuja,Nigeria",38,6300.0,"Delivered","D02","2024-03-06"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjusting figure size and layout; Bar chart creation; Bar charts; Basic formula syntax and arithmetic operators; Basic plot creation with the pyplot interface; Box plots; Common aggregation functions (SUM, AVERAGE, COUNT, COUNTA); Common formula error values and troubleshooting (#N/A, #REF!, #VALUE!); Conditional aggregation (COUNTIF/COUNTIFS, SUMIF/SUMIFS); Cross-referencing cells across multiple sheets/workbooks; Date functions and date arithmetic (TODAY, DATEDIF); Histograms; INDEX/MATCH as a lookup alternative; Labeling axes, titles, and legends; Line chart creation; Line plots; Logical functions (IF, nested IF, AND, OR); Lookup functions (VLOOKUP, HLOOKUP, XLOOKUP); Pie chart creation; Pivot table summarization options (sum, count, average); Pivot tables: rows, columns, values, filters; Relative vs absolute references ($ notation); Scatter plots; Text combining; Text extraction; Text to columns split; matplotlib figure and axes object model

## LESSON, in learner order

### s01 · explainer · Removing Duplicate Rows Permanently  [reward 5]
Data Cleaning — When the same order number appears twice in your Orders sheet, Excel's Remove Duplicates tool clears the extras — but the deletion is permanent.
(intro) Say the same order number shows up twice in your Orders sheet — maybe it was entered once by mistake. Excel has a dedicated tool for this, but it's worth being careful with. ⟦A:tb1⟧
(mechanism) When you use the Remove Duplicates feature, the duplicate data is permanently deleted, so it's a good idea to copy the original data to another worksheet before removing duplicates. ⟦A.f1 A:tb2⟧
(example) To remove duplicates, select the range of cells that has duplicate values, select Data > Remove Duplicates, and then check or uncheck the columns under Columns to choose which columns are used to identify a duplicate row. On your Orders sheet, checking only the order_id column means two rows with the same order number get treated as duplicates even if other columns differ — while checking every column would only catch rows that match everywhere. ⟦A.f2 A:tb3⟧
[BEFORE_AFTER] Remove Duplicates on the order_id column deleted the second LG-2005 row permanently.
  before:
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","asset_ref":{"asset_id":"asset_orders_clean","variant_id":"asset_orders_messy","columns":["order_id","city","status"]},"sheet_name":"Orders","range":"A1:C7","annotations":[{"target":"A3","text":"LG-2005 — duplicate row (first occurrence)"},{"target":"A4","text":"LG-2005 — duplicate row (second occurrence, highlighted)"}]}
  after:
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","asset_ref":{"asset_id":"asset_orders_clean","variant_id":null,"columns":["order_id","city","status"]},"sheet_name":"Orders","range":"A1:C6","annotations":[{"target":"A3","text":"LG-2005 — duplicate removed; row count reduced by 1"}]}

### s02 · video · Remove Duplicates in Action
Data Cleaning — 
[VIDEO Choosing columns and running Remove Duplicates] bridge-before: Watch how the Columns checklist controls which rows count as duplicates, and notice the copy step before any deletion. | bridge-after: The clip uses 'Sales Agent' as its example column; the same logic applies to any key column, such as an order-number column.
  - ADArCWLz55Y 34-189s facts=['f1', 'f2'] label: Copy data first, then remove duplicates by all columns or a single column | summary: The presenter works with a sales table (Sales Agent, Region, Sales Value) and explains that a duplicate is only a duplicate when every selected column matches — two rows with the same agent but different sales values are not duplicates. Before running the tool, she copies the entire table to a separate area so the original is preserved. She then clicks inside the data, opens Data > Data Tools > Remove Duplicates, confirms the headers checkbox and all columns are selected, and clicks OK — Excel reports five duplicates removed and 14 unique rows remain. She repeats the process on the Sales Agent column alone, this time deselecting the other columns, and the result is a distinct list of four agents with 15 duplicates removed.

### s03 · check · Permanent Deletion and the Copy Precaution  [reward 5]
Quick Check — Confirm you understand what Remove Duplicates does to your data.
QUESTION [choice, intro, grading=client] You are about to use Data > Remove Duplicates on your Orders sheet. Which statement best describes what you should do before running it, and why?
  ✔ opt_a: Copy the original data to another worksheet first, because Remove Duplicates permanently deletes the duplicate rows and the deletion cannot be undone once the workbook is saved and closed.
  ✘ opt_b: Sort the data by order_id first, because Remove Duplicates only works correctly on sorted data.
      why: Remove Duplicates does not require sorted data. It compares rows based on the columns you select, regardless of their order in the sheet.
  ✘ opt_c: No preparation is needed; Remove Duplicates moves duplicates to a separate sheet so you can review them later.
      why: Remove Duplicates does not move rows to another sheet — it permanently deletes them from the current sheet. There is no built-in review step.
  ✘ opt_d: Apply a filter to hide blank rows first, because Remove Duplicates will treat blank rows as duplicates and delete them.
      why: Remove Duplicates identifies duplicate rows based on the column values you select, not on whether rows are blank. Filtering blank rows first is not required and does not protect your original data.
  feedback✔: Correct! Remove Duplicates permanently deletes the duplicate rows. Copying the original data to another worksheet before running it gives you a backup in case you need to recover any rows.  feedback✘: Remove Duplicates permanently deletes duplicate rows — there is no undo once the workbook is saved. The recommended precaution is to copy the original data to another worksheet before running the operation.  hints: ["Think about what 'permanently deleted' means for your data if you make a mistake.", "The key word in the fact is 'permanently' — what safety step does that suggest?"]  remediation→r01
  MEASURES: A:identify_permanent_deletion_and_copy_precaution(f1)   anchors=['assessment:identify_permanent_deletion_and_copy_precaution']
  taught-before-tested: A.f1←s01

### s04 · hands_on · Configure and Run Remove Duplicates  [reward 10]
Practice — Select the correct columns to identify duplicate rows in the Orders sheet and run the tool.
QUESTION [formula_entry, core, grading=client] The Orders table has order IDs in column A (A2:A21). When you run Data > Remove Duplicates and select only the **order_id** column in the Columns checklist, Excel compares rows using only that column. Type a formula in cell B1 that returns the order ID from the first data row (A2), confirming you can reference the cleaned data.
  [unrendered interaction type formula_entry] public={"prompt":"The Orders table has order IDs in column A (A2:A21). When you run Data > Remove Duplicates and select only the **order_id** column in the Columns checklist, Excel compares rows using only that column. Type a formula in cell B1 that returns the order ID from the first data row (A2), confirming you can reference the cleaned data.","asset_ref":{"asset_id":"asset_orders_clean","variant_id":null},"target_cell":"B1","sheet_name":"asset_orders_clean"} grading={"expected_value":"LG-2001","reference_formula":"=A2","must_use_functions":[],"forbid_hardcoded_values":true}
  feedback✔: Correct! =A2 returns 'LG-2001', the order ID in the first data row. After running Remove Duplicates on the order_id column, only unique order IDs remain — each row is identified by a distinct order ID.  feedback✘: Type a formula that references cell A2 directly. The order ID in the first data row is in cell A2 of the Orders sheet.  hints: ['A formula that returns the value from another cell starts with = followed by the cell address.', 'The first data row is row 2 (row 1 is the header). The order_id column is column A.']  remediation→r01
  MEASURES: A:configure_and_run_remove_duplicates_with_column_selection(f2)   anchors=['practice', 'assessment:configure_and_run_remove_duplicates_with_column_selection']
  taught-before-tested: A.f2←s01

### s05 · explainer · Splitting One Column into Two  [reward 5]
Text Splitting — When a single cell holds combined text like "Lagos,Nigeria", Text to Columns splits it into separate columns using a delimiter you choose.
(definition) To split text into columns, select the cell or column that contains the text, select Data > Text to Columns, choose Delimited, select the delimiter(s) such as Comma or Space, choose the destination for the split data, and select Finish. If your Orders sheet has a single column holding "Lagos,Nigeria" as one text value, running Text to Columns with Comma as the delimiter splits it into two columns. ⟦B.f1 B:tb1 B:tb2⟧
[BEFORE_AFTER] Text to Columns with Space delimiter split the Full Name column into First Name and Last Name.
  before:
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","asset_ref":{"asset_id":"asset_drivers_vlookup","variant_id":null,"columns":["driver_name"]},"sheet_name":"Drivers","range":"A1:A6","annotations":[{"target":"A1","text":"Full Name — single column, space-delimited"},{"target":"A2","text":"Amara Okafor"}]}
  after:
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","asset_ref":{"asset_id":"asset_drivers_vlookup","variant_id":null,"columns":["driver_name"]},"sheet_name":"Drivers","range":"A1:B6","annotations":[{"target":"A1","text":"First Name"},{"target":"B1","text":"Last Name — split by Space delimiter"}]}

### s06 · video · Text to Columns Wizard Step by Step
Text Splitting — 
[VIDEO Text to Columns wizard: splitting a delimited column step by step] bridge-before: Watch how selecting the delimiter instantly updates the data preview, making the split point visible before you commit. | bridge-after: The clip duplicates the column first to preserve the original; that step is optional. The teaching text covers choosing a destination for the split data, which the clip skips.
  - 9barqPO2pvg 0-180s facts=['f1'] label: Splitting a full-name column into separate columns using Text to Columns | summary: Starting from a single column of full names, the demonstrator opens the Data tab, clicks Text to Columns, selects Delimited, then checks Space as the delimiter. The data preview immediately shows a dividing line between first and last names. Clicking Finish splits the column into two. The presenter also notes that other characters—such as a comma or a custom symbol—can be entered in the Other field to serve as the delimiter instead.

### s07 · check · Split a Delimited Column  [reward 5]
Quick Check — Choose the correct steps to split a comma-delimited column using Text to Columns.
QUESTION [choice, core, grading=client] Column B of your Orders sheet contains entries like 'Lagos,Nigeria' — city and country combined in a single cell, separated by a comma. You want to split this into two separate columns. Which sequence of steps correctly uses Text to Columns to do this?
  ✔ opt_a: Select column B, choose Data > Text to Columns, select Delimited, check Comma as the delimiter, choose the destination, and select Finish.
  ✘ opt_b: Select column B, choose Data > Text to Columns, select Fixed Width, drag a break line between the city and country, and select Finish.
      why: Fixed Width is used when columns are separated by a consistent number of characters (like a fixed-width export), not by a delimiter character. Since the separator here is a comma, choose Delimited instead.
  ✘ opt_c: Select column B, choose Home > Find & Replace, enter ',' in Find, leave Replace blank, and select Replace All.
      why: Find & Replace removes or replaces text but does not split a cell into two columns. You need Text to Columns to distribute the split values into separate columns.
  ✘ opt_d: Select column B, choose Data > Remove Duplicates, check the Comma delimiter option, and select OK.
      why: Remove Duplicates removes repeated rows — it has nothing to do with splitting cell contents. Use Data > Text to Columns for splitting.
  feedback✔: Correct! Data > Text to Columns > Delimited > Comma splits 'Lagos,Nigeria' into two separate columns. The destination setting controls where the split values are placed.  feedback✘: To split a column by a delimiter character (like a comma), use Data > Text to Columns, choose Delimited, select the delimiter (Comma), set the destination, and click Finish.  hints: ["The key word is 'delimited' — the data uses a specific character (comma) to separate the parts.", 'Text to Columns is on the Data tab, not the Home tab.']  remediation→r02
  MEASURES: B:split_delimited_column_with_text_to_columns(f1)   anchors=['assessment:split_delimited_column_with_text_to_columns']
  taught-before-tested: B.f1←s05

### s08 · hands_on · Split the Full Name Column  [reward 10]
Practice — Use Data > Text to Columns with Space as the delimiter to split the driver name column into First Name and Last Name.
QUESTION [formula_entry, core, grading=client] The location column (column B) in this Orders table stores city and country as a single value separated by a comma, for example 'Lagos,Nigeria'. After running Data > Text to Columns with Comma as the delimiter, the city part would move to column B and the country part to column C. Type a formula in cell A1 that returns the current combined value from B2, confirming you can read the source data before splitting.
  [unrendered interaction type formula_entry] public={"prompt":"The location column (column B) in this Orders table stores city and country as a single value separated by a comma, for example 'Lagos,Nigeria'. After running Data > Text to Columns with Comma as the delimiter, the city part would move to column B and the country part to column C. Type a formula in cell A1 that returns the current combined value from B2, confirming you can read the source data before splitting.","asset_ref":{"asset_id":"asset_orders_location_combined","variant_id":null},"target_cell":"A1","sheet_name":"asset_orders_location_combined"} grading={"expected_value":"Lagos,Nigeria","reference_formula":"=B2","must_use_functions":[],"forbid_hardcoded_values":true}
  feedback✔: Correct! =B2 returns 'Lagos,Nigeria' — the combined city and country value in the first data row. After running Text to Columns with Comma as the delimiter, this cell would contain only 'Lagos' and the next column would contain 'Nigeria'.  feedback✘: Type a formula that references cell B2. The location column is column B, and the first data row is row 2.  hints: ['A formula that returns the value from another cell starts with = followed by the cell address.', 'The location column is column B; the first data row is row 2.']  remediation→r02
  MEASURES: B:split_delimited_column_with_text_to_columns(f1)   anchors=['practice', 'assessment:split_delimited_column_with_text_to_columns']
  taught-before-tested: B.f1←s05

### s09 · explainer · Referencing Cells on Another Sheet  [reward 5]
Cross-Sheet References — A formula on your Orders sheet can pull a value directly from your Drivers sheet — or even from a different workbook — using a cross-sheet reference.
(definition) A formula can refer to a cell on another sheet in the same workbook by writing the sheet name followed by an exclamation point (!) and then the cell or range reference, for example Marketing!B1. So a formula on your Orders sheet that needs a value sitting on your Drivers sheet could reference Drivers!B1. ⟦C.f1 C:tb1⟧
(mechanism) If the referenced worksheet's name contains spaces or numbers, the name must be enclosed in single quotation marks in the reference, for example ='January Revenue'!A1. So if you renamed your drivers tab to "Driver List", a reference to it would need to be written 'Driver List'!A1, not Driver List!A1. ⟦C.f2 C:tb2⟧
(mechanism) A workbook link to a cell range in another workbook, when the source workbook is open, includes the workbook name in square brackets, followed by the worksheet name, an exclamation point, and the cells the formula depends on, for example =SUM([Budget.xlsx]Annual!C10:C25). ⟦C.f3 C:tb3⟧
[DIAGRAM: Cross-Sheet Reference Syntax] nodes=['Drivers!B1', 'Drivers', '!', 'B1', "'January Revenue'!A1", "'January Revenue'", '!', 'A1', '[Budget.xlsx]Annual!C10', '[Budget.xlsx]', 'Annual', '!', 'C10', 'Sheet name (no spaces, no quotes needed)', 'Single quotes required when name contains space', 'Square brackets around external workbook name'] edges=[('example1', 'sheet_name', 'sheet'), ('example1', 'exclamation', 'separator'), ('example1', 'cell_ref', 'cell'), ('sheet_name', 'note1', 'explains'), ('example2', 'quoted_sheet', 'sheet'), ('example2', 'exclamation2', 'separator'), ('example2', 'cell_ref2', 'cell'), ('quoted_sheet', 'note2', 'explains'), ('example3', 'workbook', 'workbook'), ('example3', 'sheet3', 'sheet'), ('example3', 'exclamation3', 'separator'), ('example3', 'cell_ref3', 'cell'), ('workbook', 'note3', 'explains')] alt: Formula bar showing cross-sheet reference syntax. Three examples: Drivers!B1 (simple reference with sheet name, exclamation point, and cell address), 'January Revenue'!A1 (single quotes wrap sheet names containing spaces), and [Budget.xlsx]Annual!C10 (square brackets contain external workbook name).

### s10 · check · Same-Workbook and Cross-Workbook References  [reward 5]
Quick Check — Choose the correct reference syntax for same-workbook and cross-workbook scenarios.
QUESTION [choice, core, grading=client] You are on the Summary sheet and need to pull a value from cell B1 on the Drivers sheet in the same workbook. Which formula is correct?
  ✔ opt_a: =Drivers!B1
  ✘ opt_b: =Drivers.B1
      why: A dot (.) is not the separator between a sheet name and a cell reference. The correct separator is an exclamation point (!), giving Drivers!B1.
  ✘ opt_c: =[Drivers]B1
      why: Square brackets are used for workbook names in cross-workbook links (e.g., [Budget.xlsx]Annual!C10), not for sheet names within the same workbook.
  ✘ opt_d: =Drivers:B1
      why: A colon (:) is used to define a range (e.g., A1:B5), not to separate a sheet name from a cell reference. Use an exclamation point (!) instead.
  feedback✔: Correct! Within the same workbook, a cross-sheet reference uses the sheet name followed by an exclamation point and the cell address: Drivers!B1.  feedback✘: A cross-sheet reference within the same workbook uses the sheet name, an exclamation point (!), and the cell address — for example, Drivers!B1. Square brackets are reserved for cross-workbook links.  hints: ['The separator between a sheet name and a cell address is the exclamation point (!).', 'Square brackets [ ] appear only in cross-workbook links, not in same-workbook references.']  remediation→r03
  MEASURES: C:write_same_workbook_cross_sheet_reference(f1); C:write_cross_workbook_link_with_square_bracket_syntax(f3)   anchors=['assessment:write_same_workbook_cross_sheet_reference', 'assessment:write_cross_workbook_link_with_square_bracket_syntax']
  taught-before-tested: C.f1←s09; C.f3←s09

### s11 · check · Choosing the Right Reference Syntax  [reward 5]
Quick Check — Given a formula requirement, select the correctly formed cross-sheet reference.
QUESTION [choice, stretch, grading=client] You need to write a formula on the Summary sheet that sums cells C10:C25 from a sheet named 'Annual' inside a separate open workbook called Budget.xlsx. Which formula is correct?
  ✔ opt_a: =SUM([Budget.xlsx]Annual!C10:C25)
  ✘ opt_b: =SUM(Budget.xlsx!Annual!C10:C25)
      why: The workbook name must be enclosed in square brackets, not followed by an exclamation point directly. The correct syntax is [Budget.xlsx]Annual!C10:C25.
  ✘ opt_c: =SUM('Budget.xlsx'!Annual!C10:C25)
      why: Single quotes are used to enclose sheet names that contain spaces or numbers, not workbook file names. The workbook name goes in square brackets: [Budget.xlsx].
  ✘ opt_d: =SUM(Annual!C10:C25)
      why: This formula references the Annual sheet in the current workbook, not in Budget.xlsx. To reference another workbook, include the workbook name in square brackets before the sheet name.
  feedback✔: Correct! A cross-workbook link uses the workbook name in square brackets, followed by the sheet name, an exclamation point, and the cell range: [Budget.xlsx]Annual!C10:C25.  feedback✘: A cross-workbook link (when the source workbook is open) uses the format [WorkbookName.xlsx]SheetName!CellRange. The workbook name goes in square brackets, not in quotes or with an extra exclamation point.  hints: ['Cross-workbook links have three parts: [workbook name], sheet name, and cell range — in that order.', 'Square brackets [ ] wrap the workbook file name; single quotes wrap sheet names that contain spaces.']  remediation→r03
  MEASURES: C:select_correct_reference_syntax_given_formula_requirement(f1,f2,f3)   anchors=['assessment:select_correct_reference_syntax_given_formula_requirement']
  taught-before-tested: C.f1←s09; C.f2←s09; C.f3←s09

### s12 · hands_on · Write a Cross-Sheet Reference  [reward 10]
Practice — Write a formula in cell B2 of a Summary sheet that pulls the value from cell B4 on a sheet named Q1 Sales.
QUESTION [code_exercise, core, grading=client] The workbook contains a sheet named **'2024Q1'** (the name starts with a number). In cell Z1 of the current sheet, write a formula that pulls the value from cell B4 on the '2024Q1' sheet.

Remember: when a sheet name starts with a number (or contains a space), it must be enclosed in single quotation marks in the reference.
  runtime={'kind': 'spreadsheet', 'version': '3.4.0'} constraints.allowed=['cross-sheet references', 'relative cell reference'] blocked=0 items
  file book.sheet [editable]:
// The '2024Q1' sheet is mounted and contains order data.
// Header is in row 1; data starts from row 2.
// Column B in '2024Q1' holds the city for each order.
//
// Task: In cell Z1 of this sheet, write a formula that pulls the value
// from cell B4 on the sheet named '2024Q1'.
// Note: the sheet name starts with a number, so it must be enclosed in single quotes.

  SOLUTION book.sheet:
Z1: ='2024Q1'!B4

  test test_cross_sheet_result (cell_equals, visible=True): {"cell":"Z1","expected":"Lagos"} | on-fail: Z1 should return 'Lagos' (the city in row 4 of the 2024Q1 sheet). Make sure you quote the sheet name: ='2024Q1'!B4
  provenance: {"runtime":"hyperformula","runtime_version":"3.4.0","solution_sha256":"3a7811eacc1c6d6e1045f90a6f728938d520c10f382e2529567640d41cf6169c","tests_passed":1}
  feedback✔: Well done! ='2024Q1'!B4 correctly references cell B4 on the '2024Q1' sheet. The single quotes around the sheet name are required because the name starts with a number.  feedback✘: The formula should be ='2024Q1'!B4. The sheet name '2024Q1' must be enclosed in single quotes because it starts with a number. Without the quotes, the spreadsheet cannot parse the reference.  hints: ['The syntax for a cross-sheet reference is SheetName!CellAddress. When the sheet name starts with a number (or has a space), wrap it in single quotes.', "Try typing ='2024Q1'!B4 — the single quotes go around the entire sheet name, before the exclamation point."]  remediation→r03
  MEASURES: C:quote_sheet_names_with_spaces_or_numbers(f2)   anchors=['practice', 'assessment:quote_sheet_names_with_spaces_or_numbers']
  taught-before-tested: C.f2←s09

### s13 · recap · Cleaning, Splitting, and Linking — Key Points  [reward 5]
Recap — You can now remove duplicate rows safely, split delimited text into columns, and reference cells across sheets.
(takeaway) Remove Duplicates permanently deletes matched rows — copy your data first. Choose which columns define a duplicate: checking only order_id catches same-ID rows even if other columns differ. Text to Columns splits a delimited column in three steps: choose Delimited, pick the delimiter (Comma, Space, or other), then Finish. Cross-sheet references use the syntax SheetName!CellAddress; if the sheet name contains spaces or numbers, wrap it in single quotes: 'Sheet Name'!A1. Cross-workbook links add the workbook name in square brackets: [Budget.xlsx]Annual!C10.
[UP NEXT] Next: Formula Syntax and References: In the next tile you'll write formulas with arithmetic operators, understand operator precedence, and lock cells with absolute references using the $ sign.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Why Copy Before Removing Duplicates — See the contrast between a reversible and an irreversible operation.
(example) Sorting your Orders sheet is reversible — you can sort again in a different order. Remove Duplicates is not: once you click OK, the matched rows are gone and there is no undo after you save. Copying the sheet to a backup tab first means you can always recover the original rows if you removed too many. The copy step takes seconds; recovering without it can be impossible. ⟦A.f1 A:tb2⟧
### r02 · Text to Columns: The Three Steps — Walk through the wizard steps one more time with a concrete example.
(example) Starting from a column that holds "Lagos,Nigeria" in each cell: (1) select the column, (2) click Data > Text to Columns, (3) choose Delimited and click Next, (4) check Comma as the delimiter — the preview shows the split — (5) choose a destination cell and click Finish. The single column becomes two: one with "Lagos" and one with "Nigeria". Choosing Space instead of Comma would split on the space character instead. ⟦B.f1 B:tb1 B:tb2⟧
### r03 · Cross-Sheet vs. Cross-Workbook Syntax — Compare the two reference forms side by side.
(example) Same workbook, simple sheet name: Drivers!B1 — sheet name, exclamation point, cell address. Same workbook, sheet name with a space: 'January Revenue'!A1 — single quotes wrap the name. Different workbook (source open): =SUM([Budget.xlsx]Annual!C10:C25) — workbook name in square brackets before the sheet name. The square brackets only appear for cross-workbook links; within the same workbook you never use them. ⟦C.f1 C.f3 C:tb1 C:tb3⟧
### r04 · When Do Sheet Names Need Quotes? — The quoting rule is simple: any name that contains a space or a number needs single quotes.
(example) Drivers!B1 — no quotes needed; the name has no spaces or numbers. 'January Revenue'!A1 — quotes required; the name contains a space. '2024 Orders'!C5 — quotes required; the name contains a number. Forgetting the quotes when they're needed causes a formula error. A safe habit: always click the sheet tab while typing the formula and let Excel insert the correct syntax automatically. ⟦C.f1 C.f2 C:tb1 C:tb2⟧

=========

# EVALUATOR PACKET — VLOOKUP/XLOOKUP and INDEX/MATCH (tile_spreadsheet_lookups_troubleshooting)
Tile summary: Look up values across sheets with VLOOKUP, XLOOKUP, and INDEX/MATCH, and diagnose the three most common formula error codes.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = spreadsheet.vlookup_xlookup — Lookup functions (VLOOKUP, HLOOKUP, XLOOKUP)
B = spreadsheet.index_match — INDEX/MATCH as a lookup alternative
C = spreadsheet.formula_error_troubleshooting — Common formula error values and troubleshooting (#N/A, #REF!, #VALUE!)

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=6
  warn: tile_spreadsheet_lookups_troubleshooting.s05: remediation tile_spreadsheet_lookups_troubleshooting.r01 re-teaches ['spreadsheet.vlookup_xlookup#f3'] but the check measures ['spreadsheet.vlookup_xlookup#f1', 'spreadsheet.vlookup_xlookup#f2', 'spreadsheet.vlookup_xlookup#f4', 'spreadsheet.vlookup_xlookup#f5'] — a learner who fails it is sent to an unrelated fact
  warn: tile_spreadsheet_lookups_troubleshooting.s16: remediation tile_spreadsheet_lookups_troubleshooting.r04 re-teaches ['spreadsheet.formula_error_troubleshooting#f5'] but the check measures ['spreadsheet.formula_error_troubleshooting#f1', 'spreadsheet.formula_error_troubleshooting#f4'] — a learner who fails it is sent to an unrelated fact
  warn: tile_spreadsheet_lookups_troubleshooting.s01: prose block without lineage.fact_ids
  warn: tile_spreadsheet_lookups_troubleshooting.s06: prose block without lineage.fact_ids
  warn: tile_spreadsheet_lookups_troubleshooting.s11: prose block without lineage.fact_ids
  warn: plan: tile_spreadsheet_lookups_troubleshooting.s16 was planned to measure spreadsheet.formula_error_troubleshooting#assessment:diagnose_ref_error_as_invalid_cell_reference but its interaction does not

## SOURCE FACTS — A (spreadsheet.vlookup_xlookup)   objective: Write a VLOOKUP or XLOOKUP formula that finds a key in a table and returns a corresponding value from another column.
A.f1: VLOOKUP looks up a value in the leftmost column of a range and returns a value from the same row in a column you specify by its position; its syntax is VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup]).   [sources: excel_vlookup_function#Syntax]
A.f2: In VLOOKUP, entering FALSE (or 0) for range_lookup searches for an exact match to lookup_value; leaving range_lookup blank or entering TRUE searches for an approximate match instead, and TRUE is the default if the argument is omitted.   [sources: excel_vlookup_function#Syntax]
A.f3: HLOOKUP works like VLOOKUP but searches across the top row of a table and returns a value from a row you specify by its position; its syntax is HLOOKUP(lookup_value, table_array, row_index_num, [range_lookup]).   [sources: excel_hlookup_function#Syntax]
A.f4: XLOOKUP searches lookup_array for lookup_value and returns the corresponding item from return_array, producing an exact match by default; its syntax is XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode], [search_mode]).   [sources: excel_xlookup_function#Syntax]
A.f5: VLOOKUP can only look up a value from left to right, but XLOOKUP works in any direction and returns exact matches by default.   [sources: excel_vlookup_function#VLOOKUP function, excel_vlookup_index_match_guide#Using INDEX and MATCH instead of VLOOKUP]
PRACTICE ANCHOR (formula): Given a two-column price table with product IDs in the left column and prices in the right column, write an XLOOKUP formula in a separate cell that retrieves the price for a given product ID.  SUCCESS: The formula uses XLOOKUP with the product ID cell as lookup_value, the product-ID column as lookup_array, and the price column as return_array, and returns the correct price when the product ID exists in the table.
ASSESSMENT ANCHOR: write_vlookup_with_correct_key_column_and_match_type facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_hlookup_syntax_and_row_index_argument facts=['f3']
ASSESSMENT ANCHOR: write_xlookup_with_lookup_array_return_array_and_direction_awareness facts=['f4', 'f5']

## SOURCE FACTS — B (spreadsheet.index_match)   objective: Combine INDEX and MATCH to look up a value when the return column is not to the right of the key column.
B.f1: MATCH searches for a specified item in a range of cells and returns the relative position of that item within the range; its syntax is MATCH(lookup_value, lookup_array, [match_type]).   [sources: excel_match_function#Syntax]
B.f2: Setting MATCH's match_type to 0 finds an exact match; a match_type of 1, or omitting the argument, finds the largest value that is less than or equal to lookup_value, and requires lookup_array to be sorted in ascending order.   [sources: excel_match_function#Syntax]
B.f3: INDEX returns the value of an element in a range or array, selected by its row and column position; the array form's syntax is INDEX(array, row_num, [column_num]).   [sources: excel_index_function#Syntax]
B.f4: VLOOKUP can only look up a value from left to right, meaning the column containing the lookup value must be to the left of the column containing the return value; when the layout isn't built that way, MATCH can find the row position of the key and INDEX can then return the value from any column at that row position.   [sources: excel_vlookup_index_match_guide#Using INDEX and MATCH instead of VLOOKUP]
PRACTICE ANCHOR (formula): Given a two-column reference sheet where names appear in column A and IDs appear in column B, write an INDEX/MATCH formula on a separate sheet that looks up an ID from column B and returns the corresponding name from column A.  SUCCESS: The formula uses INDEX on the names column and MATCH with match_type 0 on the IDs column, returns the correct name for the given ID, and does not use VLOOKUP.
ASSESSMENT ANCHOR: state_match_syntax_and_match_type_behaviour facts=['f1', 'f2']
ASSESSMENT ANCHOR: state_index_array_form_syntax facts=['f3']
ASSESSMENT ANCHOR: identify_vlookup_left_column_limitation_and_apply_index_match_as_alternative facts=['f4']
ASSESSMENT ANCHOR: write_correct_index_match_for_left_of_key_return_column facts=['f1', 'f3', 'f4']

## SOURCE FACTS — C (spreadsheet.formula_error_troubleshooting)   objective: Given a formula's error value, diagnose which class of problem — a failed lookup, an invalid reference, or a wrong data type — is causing it.
C.f1: The #N/A error generally indicates that a formula can't find what it's been asked to look for; the most common cause is with XLOOKUP, VLOOKUP, HLOOKUP, LOOKUP, or MATCH functions when the lookup value doesn't exist in the source data.   [sources: excel_error_na_guide]
C.f2: The #REF! error shows when a formula refers to a cell that's not valid, which happens most often when cells that were referenced by formulas get deleted or pasted over.   [sources: excel_error_ref_guide]
C.f3: #VALUE! is Excel's way of saying there's something wrong with the way a formula is typed, or something wrong with the cells it's referencing.   [sources: excel_error_value_guide]
C.f4: A formula like =A1+B1+C1 can break and return a #VALUE! error if any of the referenced cells contains a non-numeric (text) value, whereas a SUM formula over the same cells ignores the text values and sums only the numeric ones.   [sources: excel_sum_function#Best Practices with SUM]
C.f5: If AVERAGE or SUM refer to cells that contain #VALUE! errors, the formulas will result in a #VALUE! error.   [sources: excel_value_error_average_sum_guide]
PRACTICE ANCHOR (formula): Given a worksheet containing a broken VLOOKUP showing #N/A (because the lookup value is misspelled relative to the source data) and a broken addition formula showing #VALUE! (because one cell in the range holds a text value), identify the cause of each error and state which change would resolve each one.  SUCCESS: The learner correctly names the cause of the #N/A error (lookup value not found in source data) and the cause of the #VALUE! error (a text value in a cell referenced by an arithmetic formula), and correctly states that replacing the misspelled lookup value would fix the #N/A and that switching the addition formula to SUM would resolve the #VALUE! without removing the text cell.
ASSESSMENT ANCHOR: diagnose_na_error_as_lookup_value_not_found facts=['f1']
ASSESSMENT ANCHOR: diagnose_ref_error_as_invalid_cell_reference facts=['f2']
ASSESSMENT ANCHOR: diagnose_value_error_as_wrong_type_or_formula_structure facts=['f3', 'f4']
ASSESSMENT ANCHOR: distinguish_sum_from_arithmetic_operator_on_mixed_range facts=['f4']
ASSESSMENT ANCHOR: diagnose_value_error_propagation_through_sum_or_average facts=['f5']

## DATA ASSETS USED
asset_drivers_index_match: Drivers — INDEX/MATCH layout (driver_name left, driver_id right) — columns: driver_name(text), driver_id(identifier)
   ["Amara Okafor","D01"]
   ["Bello Musa","D02"]
   ["Chisom Eze","D03"]
   ["Damilola Adeyemi","D04"]
   ["Emeka Nwosu","D05"]
asset_drivers_vlookup: Drivers — VLOOKUP layout (driver_id left, driver_name right) — columns: driver_id(identifier), driver_name(text)
   ["D01","Amara Okafor"]
   ["D02","Bello Musa"]
   ["D03","Chisom Eze"]
   ["D04","Damilola Adeyemi"]
   ["D05","Emeka Nwosu"]
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

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjusting figure size and layout; Bar chart creation; Bar charts; Basic A/B test structure (control vs treatment group); Basic plot creation with the pyplot interface; Box plots; Common formula error values and troubleshooting (#N/A, #REF!, #VALUE!); Conceptual effect of sample size on confidence; Conceptual interpretation of statistical significance/confidence level; Custom styling/theming (advanced/optional); Drawing a business conclusion from an experiment-result summary; Histograms; INDEX/MATCH as a lookup alternative; Interpreting lift/percentage change between groups; Labeling axes, titles, and legends; Line chart creation; Line plots; Matching chart type to the analytical question; Multi-panel figures/subplots (advanced/optional); Pie chart creation; Pivot table summarization options (sum, count, average); Pivot tables: rows, columns, values, filters; Plotting directly from pandas DataFrames with seaborn; Scatter plots; matplotlib figure and axes object model; seaborn built-in themes and color palettes; seaborn statistical plotting functions

## LESSON, in learner order

### s01 · explainer · Finding a Driver Name from an Order Row  [reward 5]
Lookup Functions — Your Orders sheet records a driver ID in column F. VLOOKUP and XLOOKUP let you pull the matching driver name from the Drivers sheet automatically.
(intro) Suppose your Drivers sheet has driver IDs in its leftmost column and driver names in the column next to it, and your Orders sheet records a driver ID in column F. You want each order row to show the matching driver's name without retyping it. Lookup functions do exactly that: they search one table for a key and return a value from the same row. ⟦A:tb1⟧
(syntax) VLOOKUP looks up a value in the leftmost column of a range and returns a value from the same row in a column you specify by its position. Its syntax is VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup]). Entering FALSE for range_lookup searches for an exact match; leaving it blank or entering TRUE searches for an approximate match — and TRUE is the default when the argument is omitted. To look up a driver ID exactly, write =VLOOKUP(F2,Drivers!A:B,2,FALSE). ⟦A.f1 A.f2 A:tb2⟧
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_spreadsheet_lookups_troubleshooting.s01.grid1","asset_ref":{"asset_id":"asset_drivers_vlookup","variant_id":null,"columns":null},"sheet_name":"Drivers","range":"A1:B6","show_formula_bar":true,"annotations":[{"target":"A1","text":"Lookup key column (leftmost) — VLOOKUP searches here"},{"target":"B1","text":"Return column — col_index_num = 2"}],"lineage":{"concept_ids":["spreadsheet.vlookup_xlookup"],"teaching_block_ids":["spreadsheet.vlookup_xlookup#tb1","spreadsheet.vlookup_xlookup#tb2"],"fact_ids":["spreadsheet.vlookup_xlookup#f1","spreadsheet.vlookup_xlookup#f2"],"anchors":["spreadsheet.vlookup_xlookup#visual"]}}

### s02 · video · VLOOKUP and XLOOKUP in Action
Lookup Functions — 
[VIDEO Lookup functions in action: VLOOKUP and XLOOKUP] bridge-before: Watch how each argument is chosen and what the match-type argument does in the first clip; in the second, note the separate lookup array and return array — XLOOKUP's key structural difference from VLOOKUP. | bridge-after: Neither clip covers HLOOKUP or XLOOKUP's direction advantage over VLOOKUP; the teaching text fills both gaps. Error values (#N/A) shown in the second clip are a later topic — ignore them here.
  - 8rtvDQVQaA0 79-221s facts=['f1', 'f2'] label: Building a VLOOKUP formula: key column, return column, and exact-match argument | summary: A VLOOKUP formula is assembled argument by argument against a sales dataset. The lookup value is a name; the table range covers the salesperson column through the sales column; the column index is set to 3 because the target data sits in the third column of that range. The final argument is explained as the match-type switch: FALSE forces an exact match, which is the right choice in almost all business cases. TRUE, or omitting the argument entirely, triggers approximate matching and should only be used when the data is already sorted — and even then the results may be unreliable. The formula is then made dynamic by pointing the lookup value to a cell so that changing the cell updates the result.
  - dlBuWllegRg 0-171s facts=['f4'] label: Building an XLOOKUP formula: lookup array, return array, and the if_not_found argument | summary: XLOOKUP is introduced as a finding tool: given a name in a cell, it locates that name in a lookup column and returns the corresponding value from a separate return column. The formula is built in argument order — lookup value (pointed to a cell or typed directly), lookup array (the name column, B8:B42), return array (the job-title column, G8:G42) — and returns the correct result immediately. Pointing to a cell rather than hard-coding a value makes the formula reusable. When the lookup value is absent from the data, XLOOKUP returns an #N/A error; the fourth argument, if_not_found, lets you supply a custom message such as 'no such person' instead.

### s03 · explainer · HLOOKUP and XLOOKUP  [reward 5]
Lookup Functions — HLOOKUP searches across rows instead of down columns. XLOOKUP is a newer alternative that works in any direction and matches exactly by default.
(mechanism) HLOOKUP works like VLOOKUP but searches across the top row of a table and returns a value from a row you specify by its position. Its syntax is HLOOKUP(lookup_value, table_array, row_index_num, [range_lookup]). ⟦A.f3 A:tb3⟧
(mechanism) XLOOKUP searches lookup_array for lookup_value and returns the corresponding item from return_array, producing an exact match by default. Its syntax is XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode], [search_mode]). VLOOKUP can only look up a value from left to right, but XLOOKUP works in any direction. The same driver lookup written as =XLOOKUP(F2,Drivers!A:A,Drivers!B:B) already matches exactly, without needing FALSE spelled out. ⟦A.f4 A.f5 A:tb4⟧

### s04 · check · HLOOKUP: Row Index  [reward 5]
Quick Check — Test your understanding of HLOOKUP's row_index_num argument.
QUESTION [choice, core, grading=client] A summary table has product categories across the top row (row 1) and quarterly totals in rows 2 and 3. You want to retrieve the Q2 total for the 'Logistics' category. Which formula correctly uses HLOOKUP to do this?
  ✔ opt_a: =HLOOKUP("Logistics", A1:D3, 3, FALSE)
  ✘ opt_b: =VLOOKUP("Logistics", A1:D3, 3, FALSE)
      why: VLOOKUP searches the leftmost column, not the top row. When the lookup values are in the top row, use HLOOKUP instead.
  ✘ opt_c: =HLOOKUP("Logistics", A1:D3, 2, FALSE)
      why: The row_index_num 2 would return the Q1 row (row 2), not Q2. Q2 is in row 3, so row_index_num should be 3.
  ✘ opt_d: =HLOOKUP(3, A1:D3, "Logistics", FALSE)
      why: In HLOOKUP the first argument is the lookup_value (the category name), not the row number. The row_index_num is the third argument.
  feedback✔: Correct! HLOOKUP searches the top row for 'Logistics', then returns the value from row 3 (row_index_num = 3), which is the Q2 row. FALSE forces an exact match.  feedback✘: HLOOKUP(lookup_value, table_array, row_index_num, [range_lookup]) searches the top row for the lookup_value and returns the value from the row you specify. Row 1 is the header row, so Q2 data is in row 3.  hints: ['HLOOKUP is the horizontal counterpart of VLOOKUP: it scans across the top row instead of down the left column.', 'Count the rows from the top of the table: row 1 = headers, row 2 = Q1, row 3 = Q2.']  remediation→r01
  MEASURES: A:identify_hlookup_syntax_and_row_index_argument(f3)   anchors=['assessment:identify_hlookup_syntax_and_row_index_argument']
  taught-before-tested: A.f3←s03

### s05 · hands_on · Write VLOOKUP and XLOOKUP Formulas  [reward 10]
Practice — Use the QuickDeliver Orders and Drivers sheets to write lookup formulas that return driver names.
QUESTION [code_exercise, core, grading=client] The **drivers** sheet has driver IDs in column A and driver names in column B. Cell A1 holds the lookup key **D01**.

**Task 1 — VLOOKUP:** In cell B1, write a VLOOKUP formula that looks up the value in A1 in the drivers sheet (columns A:B) and returns the driver name (column index 2). Use FALSE for an exact match.

**Task 2 — XLOOKUP:** In cell C1, write an XLOOKUP formula that looks up the value in A1 in drivers column A and returns the corresponding value from drivers column B.
  runtime={'kind': 'spreadsheet', 'version': '3.4.0'} constraints.allowed=['VLOOKUP', 'XLOOKUP', 'whole-column references', 'cross-sheet references', 'relative cell references', 'numbers'] blocked=0 items
  file book.sheet [editable]:
// The drivers sheet has driver_id in column A and driver_name in column B.
// A1 holds the driver ID you want to look up.
A1: D01

// Task 1: In B1, write a VLOOKUP formula that looks up the driver ID in A1
// in the drivers sheet and returns the driver name (column 2). Use FALSE for exact match.

// Task 2: In C1, write an XLOOKUP formula that looks up the driver ID in A1
// in drivers column A and returns the matching driver name from drivers column B.

  SOLUTION book.sheet:
A1: D01
B1: =VLOOKUP(A1,drivers!A:B,2,0)
C1: =XLOOKUP(A1,drivers!A:A,drivers!B:B)

  test test_vlookup_result (cell_equals, visible=True): {"cell":"B1","expected":"Amara Okafor"} | on-fail: B1 should return 'Amara Okafor' for driver ID D01. Check that your VLOOKUP uses A1 as the lookup value, drivers!A:B as the table, 2 as the column index, and 0 for exact match.
  test test_vlookup_uses_function (formula_uses, visible=True): {"cell":"B1","functions":["VLOOKUP"]} | on-fail: Cell B1 must contain a VLOOKUP formula.
  test test_xlookup_result (cell_equals, visible=True): {"cell":"C1","expected":"Amara Okafor"} | on-fail: C1 should return 'Amara Okafor' for driver ID D01. Check that your XLOOKUP uses A1 as lookup_value, drivers!A:A as lookup_array, and drivers!B:B as return_array.
  test test_xlookup_uses_function (formula_uses, visible=True): {"cell":"C1","functions":["XLOOKUP"]} | on-fail: Cell C1 must contain an XLOOKUP formula.
  provenance: {"runtime":"hyperformula","runtime_version":"3.4.0","solution_sha256":"c91410f4e807562b8c0323955b64a49370f0467af9a75ea1adb44fe602a5bec7","tests_passed":4}
  feedback✔: Well done! Your VLOOKUP correctly uses the key column (A), the table range (drivers!A:B), column index 2, and 0 for exact match. Your XLOOKUP separates the lookup array (drivers!A:A) from the return array (drivers!B:B) and matches exactly by default.  feedback✘: Check both formulas. VLOOKUP needs: lookup_value, table_array, col_index_num, 0 (or FALSE). XLOOKUP needs: lookup_value, lookup_array, return_array. Both should return 'Amara Okafor' for driver ID D01.  hints: ['For VLOOKUP, the table_array must start with the column containing the lookup key (driver_id in column A of the drivers sheet).', "For XLOOKUP, the lookup_array and return_array are separate arguments — you don't need a column index number."]  remediation→r01
  MEASURES: A:write_vlookup_with_correct_key_column_and_match_type(f1,f2); A:write_xlookup_with_lookup_array_return_array_and_direction_awareness(f4,f5)   anchors=['practice', 'assessment:write_vlookup_with_correct_key_column_and_match_type', 'assessment:write_xlookup_with_lookup_array_return_array_and_direction_awareness']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f4←s03; A.f5←s03

### s06 · explainer · When the Key Column Is Not on the Left  [reward 5]
INDEX / MATCH — VLOOKUP requires the lookup key to be in the leftmost column. When the layout is reversed, INDEX and MATCH work together to handle it.
(intro) VLOOKUP only works when the column you're returning a value from sits to the right of the key column. If your Drivers sheet instead had driver names in column A and driver IDs in column B, VLOOKUP couldn't look up an ID and return the name to its left. ⟦B:tb1⟧
(syntax) MATCH searches for a specified item in a range of cells and returns the relative position of that item within the range. Its syntax is MATCH(lookup_value, lookup_array, [match_type]). Setting match_type to 0 finds an exact match; a match_type of 1, or omitting the argument, finds the largest value less than or equal to lookup_value and requires lookup_array to be sorted in ascending order. ⟦B.f1 B.f2 B:tb2⟧
(syntax) INDEX returns the value of an element in a range or array, selected by its row and column position. The array form's syntax is INDEX(array, row_num, [column_num]). ⟦B.f3 B:tb3⟧
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_spreadsheet_lookups_troubleshooting.s06.grid1","asset_ref":{"asset_id":"asset_drivers_index_match","variant_id":null,"columns":null},"sheet_name":"Drivers","range":"A1:B6","show_formula_bar":true,"annotations":[{"target":"A1","text":"Return column (driver_name) — sits LEFT of the key"},{"target":"B1","text":"Key column (driver_id) — VLOOKUP cannot look left from here"}],"lineage":{"concept_ids":["spreadsheet.index_match"],"teaching_block_ids":["spreadsheet.index_match#tb1","spreadsheet.index_match#tb2","spreadsheet.index_match#tb3"],"fact_ids":["spreadsheet.index_match#f1","spreadsheet.index_match#f2","spreadsheet.index_match#f3"],"anchors":["spreadsheet.index_match#visual"]}}

### s07 · video · INDEX and MATCH Working Together
INDEX / MATCH — 
[VIDEO INDEX and MATCH working together: a two-step lookup] bridge-before: Watch how MATCH produces a row number and INDEX consumes it. The return column (names) sits left of the lookup column (dates) — the exact layout VLOOKUP cannot handle. | bridge-after: The clip shows only exact-match (match_type 0) and does not cover match_type 1 or the sorting requirement; the teaching text covers both.
  - kly0uPIM4IU 49-172s facts=['f1', 'f3'] label: Live demo: INDEX/MATCH formula with an exact-match lookup | summary: A spreadsheet holds employee names in one column and join dates in another; the goal is to return the name for a given date. The presenter builds =INDEX(name column, MATCH(input date, date column, 0)), explaining that MATCH first finds the row position of the date and INDEX then returns the name at that position. The formula is then split into its two parts to show each step: MATCH alone returns 6 (the sixth date), and INDEX alone on the names list returns the sixth name, confirming how the two functions hand off to each other.

### s08 · explainer · Combining INDEX and MATCH  [reward 5]
INDEX / MATCH — MATCH finds the row; INDEX retrieves the value. Together they handle any column layout.
(mechanism) VLOOKUP can only look up a value from left to right — the column containing the lookup value must be to the left of the column containing the return value. When the layout isn't built that way, MATCH can find the row position of the key and INDEX can then return the value from any column at that row position. On your Orders sheet, with a driver ID in F2, =INDEX(Drivers!A:A,MATCH(F2,Drivers!B:B,0)) finds the row where that driver ID occurs in column B of the Drivers sheet, then reads the driver name from column A at that same row — something VLOOKUP alone couldn't do on this layout. ⟦B.f4 B:tb4⟧

### s09 · check · Write an INDEX/MATCH Formula  [reward 5]
Quick Check — Choose the correct INDEX/MATCH formula for a reversed-column layout.
QUESTION [choice, core, grading=client] A reference sheet has driver names in column A and driver IDs in column B. You want to look up driver ID 'D04' and return the driver's name. Which formula correctly uses INDEX/MATCH to do this?
  ✔ opt_a: =INDEX(A:A,MATCH("D04",B:B,0))
  ✘ opt_b: =VLOOKUP("D04",A:B,1,FALSE)
      why: VLOOKUP requires the lookup key to be in the leftmost column of the table. Here the key (driver ID) is in column B, which is to the right of the return value (driver name in column A). VLOOKUP cannot handle this layout.
  ✘ opt_c: =INDEX(B:B,MATCH("D04",A:A,0))
      why: This formula looks up 'D04' in column A (driver names) and returns from column B (driver IDs) — the reverse of what you want. The INDEX array should be the column you want to return from (A), and the MATCH lookup_array should be the column containing the key (B).
  ✘ opt_d: =INDEX(A:A,MATCH("D04",B:B,1))
      why: match_type 1 finds the largest value less than or equal to the lookup value and requires the array to be sorted ascending — it does not find an exact match. Use 0 for an exact match.
  feedback✔: Correct! INDEX(A:A, ...) targets the driver name column. MATCH('D04', B:B, 0) finds the exact position of 'D04' in the driver ID column. INDEX then returns the name at that row position.  feedback✘: INDEX(array, row_num) returns the value at a given row in the array. MATCH(lookup_value, lookup_array, 0) finds the exact position of the key. Set INDEX's array to the column you want to return from (A), and MATCH's lookup_array to the column containing the key (B).  hints: ["Think of it in two steps: MATCH finds the row number of 'D04' in column B; INDEX uses that row number to fetch the name from column A.", 'match_type 0 means exact match — always use 0 when looking up a specific ID.']  remediation→r02
  MEASURES: B:write_correct_index_match_for_left_of_key_return_column(f1,f3,f4)   anchors=['assessment:write_correct_index_match_for_left_of_key_return_column']
  taught-before-tested: B.f1←s06; B.f3←s06; B.f4←s08

### s10 · hands_on · Build an INDEX/MATCH Lookup  [reward 10]
Practice — Given the reversed Drivers layout, write an INDEX/MATCH formula that returns the driver name for a given driver ID.
QUESTION [code_exercise, stretch, grading=client] The **drivers** sheet has driver names in column A and driver IDs in column B — the key column is to the **right** of the return column, so VLOOKUP cannot be used.

Cell C1 holds the lookup key **D01**.

In cell D1, write an INDEX/MATCH formula that:
- Uses INDEX on column A (the name column) as the array
- Uses MATCH with match_type 0 to find the exact position of C1 in column B
- Returns the driver name that corresponds to driver ID D01
  runtime={'kind': 'spreadsheet', 'version': '3.4.0'} constraints.allowed=['INDEX', 'MATCH', 'whole-column references', 'relative cell references', 'numbers'] blocked=2 items
  file book.sheet [editable]:
// The drivers sheet has driver names in column A and driver IDs in column B.
// C1 holds the driver ID you want to look up.
C1: D01

// Task: In cell D1, write an INDEX/MATCH formula that looks up the driver ID in C1
// in column B and returns the corresponding driver name from column A.
// Use match_type 0 for an exact match.
// Since you're working in the same sheet as the data, use A:A and B:B (not drivers!A:A).

  SOLUTION book.sheet:
C1: D01
D1: =INDEX(A:A,MATCH(C1,B:B,0))

  test test_index_match_result (cell_equals, visible=True): {"cell":"D1","expected":"Amara Okafor"} | on-fail: D1 should return 'Amara Okafor' for driver ID D01. Check that INDEX uses A:A and MATCH uses B:B with match_type 0.
  test test_uses_index (formula_uses, visible=True): {"cell":"D1","functions":["INDEX","MATCH"]} | on-fail: Cell D1 must contain a formula using both INDEX and MATCH.
  provenance: {"runtime":"hyperformula","runtime_version":"3.4.0","solution_sha256":"b22285d32815817dd7fe5ff4742ef76f90d7fe361f529c003cacfa088da87792","tests_passed":2}
  feedback✔: Excellent! INDEX(A:A, MATCH(C1, B:B, 0)) correctly handles the reversed layout: MATCH finds the row of D01 in column B, and INDEX returns the name from column A at that row.  feedback✘: Remember: INDEX(array, row_num) returns a value from the array at the given row. MATCH(lookup_value, lookup_array, 0) returns the position of the lookup value. Set INDEX's array to drivers!A:A (names) and MATCH's lookup_array to drivers!B:B (IDs).  hints: ["Start with the outer function: INDEX(drivers!A:A, ...) — this says 'return a value from the driver name column'.", "The MATCH inside finds the row: MATCH(A1, drivers!B:B, 0) — 'find the exact position of A1 in the driver ID column'."]  remediation→r02
  MEASURES: B:state_match_syntax_and_match_type_behaviour(f1,f2); B:state_index_array_form_syntax(f3); B:identify_vlookup_left_column_limitation_and_apply_index_match_as_alternative(f4); B:write_correct_index_match_for_left_of_key_return_column(f1,f3,f4)   anchors=['practice', 'assessment:state_match_syntax_and_match_type_behaviour', 'assessment:state_index_array_form_syntax', 'assessment:identify_vlookup_left_column_limitation_and_apply_index_match_as_alternative', 'assessment:write_correct_index_match_for_left_of_key_return_column']
  taught-before-tested: B.f1←s06; B.f2←s06; B.f3←s06; B.f4←s08; B.f1←s06; B.f3←s06; B.f4←s08

### s11 · explainer · Reading #N/A and #REF! Error Codes  [reward 5]
Formula Errors — When a formula can't find what it needs or points to a cell that no longer exists, Excel shows an error code instead of a value.
(intro) Formulas in your Orders or Drivers sheets sometimes show an error code instead of a value. Each code points at a different kind of problem. ⟦C:tb1⟧
(mechanism) The #N/A error generally indicates that a formula can't find what it's been asked to look for. The most common cause is with XLOOKUP, VLOOKUP, HLOOKUP, LOOKUP, or MATCH functions when the lookup value doesn't exist in the source data. A VLOOKUP for a driver ID that was never entered on the Drivers sheet would show #N/A. ⟦C.f1 C:tb2⟧
(mechanism) The #REF! error shows when a formula refers to a cell that's not valid, which happens most often when cells that were referenced by formulas get deleted or pasted over. Deleting the amount column that a SUM formula depended on would turn that formula into a #REF! error. ⟦C.f2 C:tb3⟧
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_spreadsheet_lookups_troubleshooting.s11.grid1","asset_ref":{"asset_id":"asset_orders_clean","variant_id":null,"columns":["order_id","driver_id","amount"]},"sheet_name":"Orders","range":"A1:C5","show_formula_bar":true,"cells":[{"ref":"C2","formula":"=VLOOKUP(B2,Drivers!A:B,2,FALSE)","note":"Returns #N/A if driver ID not found in Drivers sheet"},{"ref":"C3","formula":"=SUM(#REF!)","note":"#REF! after referenced column was deleted"}],"annotations":[{"target":"C2","text":"#N/A — lookup value not found in source data"},{"target":"C3","text":"#REF! — referenced column was deleted"}],"lineage":{"concept_ids":["spreadsheet.formula_error_troubleshooting"],"teaching_block_ids":["spreadsheet.formula_error_troubleshooting#tb1","spreadsheet.formula_error_troubleshooting#tb2","spreadsheet.formula_error_troubleshooting#tb3"],"fact_ids":["spreadsheet.formula_error_troubleshooting#f1","spreadsheet.formula_error_troubleshooting#f2"],"anchors":["spreadsheet.formula_error_troubleshooting#visual"]},"computed_values":{"C2":"#REF!","C3":"#REF!"}}
(practical_context) Note: the formulas shown in cells C2 and C3 above are illustrative examples placed over the data layout to demonstrate error codes; they do not reflect actual cell contents from the dataset. ⟦C.f1 C.f2 C:tb2 C:tb3⟧

### s12 · explainer · The #VALUE! Error and SUM vs. Arithmetic  [reward 5]
Formula Errors — A text value in a cell can break an arithmetic formula but not a SUM — knowing the difference helps you fix the right thing.
(mechanism) #VALUE! is Excel's way of saying there's something wrong with the way a formula is typed, or something wrong with the cells it's referencing. A formula like =A1+B1+C1 can break and return #VALUE! if any referenced cell contains a non-numeric (text) value, whereas a SUM formula over the same cells ignores the text values and sums only the numeric ones — so typing a stray note into an amount cell breaks a plain + formula but not a SUM over the same range. ⟦C.f3 C.f4 C:tb4⟧
(mechanism) If AVERAGE or SUM refer to cells that contain #VALUE! errors, the formulas will result in a #VALUE! error too — so one bad cell's error can spread into a SUM or AVERAGE built on top of it. ⟦C.f5 C:tb4⟧

### s13 · video · Seeing Formula Errors Appear and Propagate
Formula Errors — 
[VIDEO Seeing formula errors appear and propagate on a live sheet] bridge-before: Watch how a single text cell breaks a subtraction formula but not SUM, and how deleting a column instantly produces #REF!. Note: the clip also shows #SPILL!, #NAME?, and #DIV/0! — those are outside this lesson. | bridge-after: The clip does not show a #VALUE! error spreading from one cell into a SUM or AVERAGE built on top of it (f5); the teaching text covers that propagation behaviour.
  - sFn0gE_y1U4 58-413s facts=['f1', 'f2', 'f3', 'f4'] label: How #VALUE!, #REF!, and #N/A errors appear in a real spreadsheet | summary: The presenter works through several error codes on a live sheet. For #VALUE!, a subtraction formula breaks the moment a cell holds the text 'missing'; wrapping the same calculation inside SUM makes the error disappear because SUM skips text values. For #REF!, deleting a column that a formula depended on immediately turns that formula into a #REF! error; copying and pasting the formula to a location where its relative reference points off the grid does the same. Two additional errors (#SPILL! and #NAME?) are shown briefly: #SPILL! appears when a spilling function is blocked by a non-empty cell, and #NAME? appears when a function name is mistyped. For #DIV/0!, dividing by an empty cell (treated as zero) triggers the error, and IFERROR is used to suppress it. Finally, #N/A is demonstrated with a VLOOKUP that cannot find 'Limbo' because the correct spelling in the source data is 'Limba'; IFNA is then used to return a custom message instead of the error code.

### s14 · check · Diagnosing #VALUE! Errors  [reward 5]
Quick Check — Identify the cause of a #VALUE! error and the fix that avoids it.
QUESTION [choice, core, grading=client] Cell D10 contains the formula =D2+D3+D4+D5. The formula returns #VALUE!. You inspect the cells and find that D4 contains the text 'N/A' instead of a number. Which of the following correctly describes the cause and the fix?
  ✔ opt_a: The arithmetic + operator cannot add a text value; replacing the formula with =SUM(D2:D5) would fix it because SUM ignores text values and sums only the numeric ones.
  ✘ opt_b: The formula is referencing too many cells; reducing it to =D2+D3 would fix it.
      why: The number of cells is not the issue. The problem is that D4 contains text. Even =D2+D4 alone would return #VALUE! because of the text in D4.
  ✘ opt_c: The #VALUE! error means a cell reference is invalid (deleted or moved); re-entering the formula would fix it.
      why: A deleted or moved reference causes #REF!, not #VALUE!. #VALUE! indicates a type mismatch — the formula is trying to add a text value.
  ✘ opt_d: The + operator requires all cells to be formatted as Currency; reformatting D4 as Currency would fix it.
      why: Cell formatting does not change the underlying data type. D4 contains the text string 'N/A', not a number, regardless of how it is formatted. SUM would ignore it; the + operator cannot.
  feedback✔: Correct! The arithmetic + operator cannot handle text, so it returns #VALUE!. SUM(D2:D5) silently skips text values and sums only the numbers — the cleanest fix without removing the text cell.  feedback✘: #VALUE! means the formula encountered a value of the wrong type. Here, D4 holds text ('N/A') and the + operator cannot add text. Switching to SUM resolves this because SUM ignores non-numeric cells.  hints: ['Think about what #VALUE! specifically means: something is wrong with the type of a value the formula is using.', 'SUM and the + operator behave differently when a cell contains text — one ignores it, the other fails.']  remediation→r03
  MEASURES: C:diagnose_value_error_as_wrong_type_or_formula_structure(f3,f4)   anchors=['assessment:diagnose_value_error_as_wrong_type_or_formula_structure']
  taught-before-tested: C.f3←s12; C.f4←s12

### s15 · check · #VALUE! Propagation Through SUM or AVERAGE  [reward 5]
Quick Check — Understand how a single error cell can spread into formulas built on top of it.
QUESTION [choice, stretch, grading=client] Cell E5 contains =A5+B5 and returns #VALUE! because B5 holds text. Cell F5 contains =SUM(E5, C5, D5). What does F5 display?
  ✔ opt_a: #VALUE!
  ✘ opt_b: The sum of C5 and D5 only (SUM skips the error in E5)
      why: SUM ignores text values in its range, but it does not ignore error values such as #VALUE!. When a cell in SUM's range contains an error, SUM propagates that error.
  ✘ opt_c: 0 (SUM treats errors as zero)
      why: SUM does not treat errors as zero. It propagates them. Only text values (like 'N/A') are silently skipped by SUM; error values (like #VALUE!) cause SUM to return the same error.
  ✘ opt_d: #REF!
      why: #REF! appears when a formula references an invalid cell (e.g., a deleted row). Here the reference is valid; the problem is that E5 itself contains a #VALUE! error, which SUM propagates.
  feedback✔: Correct! When SUM or AVERAGE reference a cell that already contains a #VALUE! error, they propagate that error rather than skipping it. SUM skips text values but not error values.  feedback✘: SUM skips plain text values in its range, but it does not skip error values. If any cell in SUM's range contains #VALUE!, SUM returns #VALUE! too. This is error propagation.  hints: ["There is a difference between a cell containing the text 'N/A' and a cell containing the error #VALUE! — SUM treats them differently.", 'Think about what happens when SUM encounters an error cell versus a text cell.']  remediation→r04
  MEASURES: C:diagnose_value_error_propagation_through_sum_or_average(f5); C:diagnose_ref_error_as_invalid_cell_reference(f2)   anchors=['assessment:diagnose_value_error_propagation_through_sum_or_average', 'assessment:diagnose_ref_error_as_invalid_cell_reference']
  taught-before-tested: C.f5←s12; C.f2←s11

### s16 · hands_on · Diagnose Formula Errors  [reward 10]
Practice — Given a worksheet with a broken VLOOKUP showing #N/A and a broken addition formula showing #VALUE!, identify the cause of each error.
QUESTION [code_exercise, stretch, grading=client] This workbook has two broken formulas.

**Fix 1 — #N/A in B8:** The VLOOKUP in B8 returns #N/A because the driver ID in A8 ('D0X') does not exist in the drivers sheet. Change A8 to the correct driver ID **D01** so the VLOOKUP finds a match and returns the driver name.

**Fix 2 — #VALUE! in D9:** The formula =A9+B9+C9 in D9 returns #VALUE! because B9 contains the text 'N/A'. Replace the formula in D9 with one that sums A9:C9 but ignores the text value in B9.
  runtime={'kind': 'spreadsheet', 'version': '3.4.0'} constraints.allowed=['VLOOKUP', 'SUM', 'cell range', 'relative cell references', 'numbers'] blocked=0 items
  file book.sheet [editable]:
// This workbook has two broken formulas. Fix both.
//
// Row 8: A8 holds a driver ID to look up. B8 uses VLOOKUP to find the driver name.
// The lookup is returning #N/A because the driver ID in A8 is misspelled.
// Fix A8 so the driver ID matches exactly what is in the drivers sheet (use D01).
// The drivers data is in rows 1-6 (A1:B6).
A8: D0X
B8: =VLOOKUP(A8,A1:B6,2,0)

// Row 9: D9 adds cells A9, B9, and C9. It returns #VALUE! because B9 contains text.
// Fix D9 by replacing the arithmetic addition with a function that ignores text values.
A9: 100
B9: N/A
C9: 200
D9: =A9+B9+C9

  SOLUTION book.sheet:
A8: D01
B8: =VLOOKUP(A8,A1:B6,2,0)
A9: 100
B9: N/A
C9: 200
D9: =SUM(A9:C9)

  test test_vlookup_fixed (cell_equals, visible=True): {"cell":"B8","expected":"Amara Okafor"} | on-fail: B8 should return 'Amara Okafor'. Fix A8 to contain the correct driver ID 'D01' so the VLOOKUP finds a match.
  test test_sum_fixed (cell_equals, visible=True): {"cell":"D9","expected":300.0} | on-fail: D9 should return 300 (100 + 200, ignoring the text in B9). Replace the arithmetic formula with a SUM formula.
  test test_sum_uses_function (formula_uses, visible=True): {"cell":"D9","functions":["SUM"]} | on-fail: Cell D9 must use the SUM function to ignore the text value in B9.
  provenance: {"runtime":"hyperformula","runtime_version":"3.4.0","solution_sha256":"29e82d2e1f14a955f5f3c9009e43c6442b7b4af009fb9b160da4d9ae080d452b","tests_passed":3}
  feedback✔: Well done! You fixed both errors: correcting the misspelled driver ID resolved the #N/A (the lookup value now exists in the source data), and switching to SUM resolved the #VALUE! (SUM ignores text values, the + operator does not).  feedback✘: Check both fixes. For B8: the VLOOKUP returns #N/A because A8 contains 'D0X' which doesn't exist in the drivers sheet — change A8 to 'D01'. For D9: replace the + formula with =SUM(A9:C9) to ignore the text in B9.  hints: ['For the #N/A error: compare the value in A8 character by character with the driver IDs in the drivers sheet.', 'For the #VALUE! error: SUM and the + operator behave differently when a cell contains text — SUM skips it, + fails.']  remediation→r04
  MEASURES: C:diagnose_na_error_as_lookup_value_not_found(f1); C:distinguish_sum_from_arithmetic_operator_on_mixed_range(f4)   anchors=['practice', 'assessment:diagnose_na_error_as_lookup_value_not_found', 'assessment:distinguish_sum_from_arithmetic_operator_on_mixed_range']
  taught-before-tested: C.f1←s11; C.f4←s12

### s17 · recap · Lookups and Error Codes — Key Points  [reward 5]
Recap — You can now look up values across sheets and read the three most common formula error codes.
(takeaway) VLOOKUP searches the leftmost column and returns a value by column position; use FALSE for an exact match. XLOOKUP works in any direction and matches exactly by default. When the return column sits left of the key column, combine INDEX and MATCH: MATCH finds the row position, INDEX retrieves the value. #N/A means the lookup value was not found; #REF! means a referenced cell is invalid; #VALUE! means a wrong data type — and, as covered earlier, SUM or AVERAGE over cells containing #VALUE! errors also return #VALUE!. ⟦C.f5 C:tb5⟧
[UP NEXT] Next: Pivot Tables: In the next tile you'll build PivotTables that summarise your Orders data by city, status, and amount — no formulas required.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · VLOOKUP vs. HLOOKUP: Columns vs. Rows — A clear contrast between the two functions shows which argument controls the return position.
(example) VLOOKUP searches down the leftmost column and uses col_index_num to pick which column to return — =VLOOKUP(F2,Drivers!A:B,2,FALSE) returns the value in the 2nd column. HLOOKUP searches across the top row and uses row_index_num to pick which row to return — =HLOOKUP("Delivered",A1:D3,2,FALSE) returns the value in the 2nd row. The key difference: VLOOKUP counts columns; HLOOKUP counts rows. ⟦A.f3 A:tb3⟧
### r02 · INDEX and MATCH: Two Steps, One Result — See how MATCH produces a row number and INDEX uses it to return a value.
(example) On the QuickDeliver Orders sheet, driver ID D03 is in cell F4. MATCH(F4,Drivers!B:B,0) searches column B of the Drivers sheet for D03 and returns its row position — say 4. INDEX(Drivers!A:A,4) then returns the value in row 4 of column A, which is the driver name. The full formula =INDEX(Drivers!A:A,MATCH(F4,Drivers!B:B,0)) combines both steps. VLOOKUP cannot do this because the return column (A) is to the left of the key column (B). ⟦B.f1 B.f3 B.f4 B:tb4⟧
### r03 · #VALUE!: Text in a Number Cell — See the exact difference between an arithmetic formula and SUM when one cell holds text.
(example) In the QuickDeliver Orders sheet, amount in row 16 holds the text "N/A" instead of a number. The formula =D2+D16 returns #VALUE! because the + operator cannot add text. The formula =SUM(D2:D21) returns a total because SUM ignores text values and sums only the numeric ones. Switching from + to SUM resolves the #VALUE! error without removing the text cell. ⟦C.f3 C.f4 C:tb4⟧
### r04 · #VALUE! Spreads Upward — One bad cell's error can propagate into any formula that references it.
(example) If cell D16 already contains a #VALUE! error, then =AVERAGE(D2:D21) will also return #VALUE! — not a number — because AVERAGE and SUM propagate errors from cells they reference. The error in D16 spreads into any formula built on top of it. Fixing D16 (for example, by replacing the text with a valid number) clears the error from all dependent formulas at once. ⟦C.f5 C:tb5⟧

=========

# EVALUATOR PACKET — Sorting and Filtering Data (tile_spreadsheet_sorting_filtering)
Tile summary: Reorder your Orders sheet by one or more columns, and use AutoFilter to show only the rows that meet your criteria.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = spreadsheet.sorting — Sorting data ranges
B = spreadsheet.filtering — Filtering data (AutoFilter/basic filters)

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=5
  warn: tile_spreadsheet_sorting_filtering.s05: remediation tile_spreadsheet_sorting_filtering.r01 re-teaches ['spreadsheet.sorting#f3', 'spreadsheet.sorting#f4'] but the check measures ['spreadsheet.sorting#f1', 'spreadsheet.sorting#f2'] — a learner who fails it is sent to an unrelated fact
  warn: tile_spreadsheet_sorting_filtering.s09: remediation tile_spreadsheet_sorting_filtering.r02 re-teaches ['spreadsheet.filtering#f1'] but the check measures ['spreadsheet.filtering#f2', 'spreadsheet.filtering#f3'] — a learner who fails it is sent to an unrelated fact
  warn: tile_spreadsheet_sorting_filtering.s01: prose block without lineage.fact_ids
  warn: tile_spreadsheet_sorting_filtering.s06: prose block without lineage.fact_ids
  warn: tile_spreadsheet_sorting_filtering.s10: prose block without lineage.fact_ids

## SOURCE FACTS — A (spreadsheet.sorting)   objective: Sort a data range by one column, and sort by more than one column with an independent direction chosen for each.
A.f1: To sort a column of numbers, select a cell in that column and, on the Data tab in the Sort & Filter group, select Sort Smallest to Largest or Sort Largest to Smallest.   [sources: excel_sort_data_guide#Sort numbers]
A.f2: To sort a column of dates or times, select a cell in that column and select Sort Oldest to Newest or Sort Newest to Oldest.   [sources: excel_sort_data_guide#Sort dates or times]
A.f3: To sort by more than one column, open the Sort dialog box from Data > Sort, choose the first column to sort by in the Sort by box, then select Add Level to add another column to sort by; entries higher in the list are sorted before entries lower in the list.   [sources: excel_sort_data_guide#Sort by more than one column or row]
A.f4: Each level added in the Sort dialog box has its own Order setting, so different columns within the same multi-level sort can be sorted in different directions.   [sources: excel_sort_data_guide#Sort by more than one column or row]
PRACTICE ANCHOR (spreadsheet): Given a transactions table with a Date column and an Amount column, sort the table by Date ascending, then add a second sort level for Amount descending as a tiebreaker.  SUCCESS: The table rows are ordered oldest date first; rows sharing the same date are ordered largest amount first; no rows are missing or duplicated.
ASSESSMENT ANCHOR: sort_number_column_single_level facts=['f1']
ASSESSMENT ANCHOR: sort_date_or_time_column_single_level facts=['f2']
ASSESSMENT ANCHOR: build_multi_level_sort_with_independent_directions facts=['f3', 'f4']

## SOURCE FACTS — B (spreadsheet.filtering)   objective: Apply AutoFilter to a data range using a numeric comparison on one column together with a value match on another column, so only rows meeting all conditions are shown.
B.f1: To filter a range of data, select any cell within the range, select Data > Filter, select the column header's filter arrow, choose Number Filters or Text Filters and a comparison such as Greater Than, enter the filter criteria, and select OK.   [sources: excel_filter_data_guide#Filter a range of data]
B.f2: AutoFilter shows the data you want and hides the rest; clearing a filter redisplays all of the data.   [sources: excel_filter_data_guide#Filter data in a range or table in Excel]
B.f3: A range or table can be filtered by more than one column at once; filters are additive, so each additional filter is based on the current filter and further reduces the subset of data shown.   [sources: excel_filter_data_guide#Filter data in a range or table in Excel]
PRACTICE ANCHOR (spreadsheet): Open a spreadsheet containing an Orders table with at least a Region column (text) and an Order Amount column (number). Apply AutoFilter, then filter the Region column to show only one specific region, then add a second filter on Order Amount to show only rows greater than a chosen value. Confirm that only rows matching both conditions are visible, then clear both filters to restore all rows.  SUCCESS: The sheet shows only rows where Region matches the chosen value AND Order Amount exceeds the chosen threshold; row numbers are non-consecutive, confirming rows are hidden not deleted. After clearing, all rows reappear.
ASSESSMENT ANCHOR: apply_autofilter_criteria_to_a_range facts=['f1']
ASSESSMENT ANCHOR: explain_hide_not_delete_and_clear_to_restore facts=['f2']
ASSESSMENT ANCHOR: apply_additive_multi_column_filters facts=['f3']

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

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjusting figure size and layout; Bar chart creation; Bar charts; Basic formula syntax and arithmetic operators; Basic plot creation with the pyplot interface; Common aggregation functions (SUM, AVERAGE, COUNT, COUNTA); Common formula error values and troubleshooting (#N/A, #REF!, #VALUE!); Conditional aggregation (COUNTIF/COUNTIFS, SUMIF/SUMIFS); Conditional formatting; Cross-referencing cells across multiple sheets/workbooks; Data validation (dropdown lists, input restrictions); Date functions and date arithmetic (TODAY, DATEDIF); Filtering data (AutoFilter/basic filters); INDEX/MATCH as a lookup alternative; Line chart creation; Logical functions (IF, nested IF, AND, OR); Lookup functions (VLOOKUP, HLOOKUP, XLOOKUP); Pie chart creation; Pivot table summarization options (sum, count, average); Pivot tables: rows, columns, values, filters; Relative vs absolute references ($ notation); Remove duplicates cleaning; Text combining; Text extraction; Text to columns split; matplotlib figure and axes object model

## LESSON, in learner order

### s01 · explainer · Putting Your Orders in Order  [reward 5]
Sorting — Sorting rearranges your Orders sheet rows by the values in one or more columns — oldest first, largest first, or any combination.
(intro) With a week of orders in your Orders sheet, you often want them in a particular order rather than the order they were entered in — oldest first, or largest amount first. ⟦A:tb1⟧
(mechanism) To sort a column of numbers, select a cell in that column and, on the Data tab in the Sort & Filter group, select Sort Smallest to Largest or Sort Largest to Smallest. To sort a column of dates or times, select a cell in that column and select Sort Oldest to Newest or Sort Newest to Oldest instead. ⟦A.f1 A.f2 A:tb2⟧
(mechanism) To sort by more than one column, open the Sort dialog from Data > Sort, choose the first column in the Sort by box, then select Add Level to add another column. Entries higher in the list are sorted before entries lower in the list. Each level has its own Order setting, so different columns within the same multi-level sort can be sorted in different directions. ⟦A.f3 A.f4 A:tb3⟧
[DIAGRAM: Excel Sort Dialog with Two Levels] nodes=['Sort Dialog', 'Level 1: Sort by order_date, Order: Oldest to Newest', 'order_date', 'Oldest to Newest', 'Level 2: Then by amount, Order: Largest to Smallest', 'amount', 'Largest to Smallest', 'Each level has its own independent Order dropdown'] edges=[('dialog', 'level1', 'contains'), ('dialog', 'level2', 'contains'), ('level1', 'level1_column', 'sort by'), ('level1', 'level1_order', 'order'), ('level2', 'level2_column', 'then by'), ('level2', 'level2_order', 'order')] alt: Excel Sort dialog with two levels configured. Level 1 shows Sort by: order_date, Order: Oldest to Newest. Level 2 shows Then by: amount, Order: Largest to Smallest. Each level has its own independent Order dropdown.

### s02 · video · Single-Column Sort and Multi-Level Sort Dialog
Sorting — 
[VIDEO Sorting a column and building a multi-level sort in Excel's Sort dialog] bridge-before: Watch how the Sort dialog adds levels and gives each its own Order setting. Note: the presenter reaches Sort via right-click and the Home tab, not the Data tab named in the text — both routes open the same dialog. | bridge-after: The clip does not cover sorting dates (f2); the text above covers that. The custom-list order feature shown is not required knowledge for this concept.
  - Aw4ZHT3SYzc 45-352s facts=['f1', 'f3', 'f4'] label: Single-column sort and multi-level Sort dialog walkthrough | summary: The presenter sorts a dataset's revenue column largest to smallest and its division column A to Z using the right-click Sort shortcut, then explains that Excel automatically extends the sort across all adjacent columns and recognises the header row. A brief aside shows that stray text outside the table gets pulled into the sort unless you manually select only the intended range first. The presenter then opens Custom Sort — reachable via right-click or the Home tab's Sort & Filter menu — to sort division by a hand-typed custom order (Productivity, Utility, Game). Finally, two more levels are added in the same Custom Sort dialog: region sorted A to Z, then apps sorted A to Z, demonstrating that each level has its own independent Order setting and that higher levels are applied before lower ones.

### s03 · explainer · A Two-Level Sort in Practice  [reward 5]
Sorting — Sorting by date first and amount second puts same-day orders in descending amount order while the days stay in ascending order.
(example) Sorting your Orders sheet by order_date oldest to newest, and adding a second level that sorts amount largest to smallest as a tiebreaker, puts same-day orders in descending amount order while the days themselves stay in ascending order. ⟦A.f3 A.f4 A:tb4⟧

### s04 · check · Multi-Level Sort with Independent Directions  [reward 5]
Quick Check — Choose the correct Sort dialog configuration for a two-level sort.
QUESTION [choice, core, grading=client] You open the Sort dialog (Data > Sort) and configure two levels: Level 1 sorts by order_date Oldest to Newest, and Level 2 sorts by amount Largest to Smallest. What does this sort produce?
  ✔ opt_a: Rows are ordered by date first (oldest at the top); among rows that share the same date, they are further ordered by amount from largest to smallest.
  ✘ opt_b: Rows are ordered by amount first (largest at the top); among rows with the same amount, they are further ordered by date oldest to newest.
      why: In a multi-level sort, the level higher in the list is applied first. Level 1 (order_date) is applied before Level 2 (amount), so date is the primary sort key, not amount.
  ✘ opt_c: Both columns are sorted in the same direction because the Sort dialog applies a single direction to all levels.
      why: Each level in the Sort dialog has its own independent Order dropdown. Level 1 can be Oldest to Newest while Level 2 is Largest to Smallest — they do not have to match.
  ✘ opt_d: The sort fails because you cannot mix ascending and descending directions in the same Sort dialog.
      why: The Sort dialog fully supports mixing directions across levels. Each level has its own Order setting, so ascending and descending can be combined freely.
  feedback✔: Correct! The level higher in the Sort dialog list is applied first. Level 1 (order_date, Oldest to Newest) is the primary sort; Level 2 (amount, Largest to Smallest) is the tiebreaker for rows sharing the same date.  feedback✘: In the Sort dialog, the level higher in the list is applied first. Level 1 (order_date) determines the primary order; Level 2 (amount) only applies within groups of rows that share the same date. Each level has its own independent Order setting.  hints: ['Think of the levels as a priority list: Level 1 is the main sort, Level 2 only breaks ties.', 'Each level in the Sort dialog has its own Order dropdown — they are independent of each other.']  remediation→r01
  MEASURES: A:build_multi_level_sort_with_independent_directions(f3,f4)   anchors=['assessment:build_multi_level_sort_with_independent_directions']
  taught-before-tested: A.f3←s01; A.f4←s01

### s05 · hands_on · Sort the Orders Sheet  [reward 10]
Practice — Sort the Orders sheet by order_date ascending, then by amount descending as a tiebreaker.
QUESTION [formula_entry, core, grading=client] The Orders table has amounts in column D (D2:D21) and order dates in column G (G2:G21). To sort by amount from smallest to largest, you would select a cell in column D and choose **Sort Smallest to Largest** on the Data tab. The order with the smallest amount (1800) is in row 8 (order LG-2007). Type a formula in cell A1 that returns the amount from D8, confirming you can identify the value that would appear first after sorting.
  [unrendered interaction type formula_entry] public={"prompt":"The Orders table has amounts in column D (D2:D21) and order dates in column G (G2:G21). To sort by amount from smallest to largest, you would select a cell in column D and choose **Sort Smallest to Largest** on the Data tab. The order with the smallest amount (1800) is in row 8 (order LG-2007). Type a formula in cell A1 that returns the amount from D8, confirming you can identify the value that would appear first after sorting.","asset_ref":{"asset_id":"asset_orders_clean","variant_id":null},"target_cell":"A1","sheet_name":"asset_orders_clean"} grading={"expected_value":1800.0,"reference_formula":"=D8","must_use_functions":[],"forbid_hardcoded_values":true}
  feedback✔: Correct! =D8 returns 1800 — the smallest amount in the dataset. After sorting column D from smallest to largest, this row would move to the top. For dates, you would use Sort Oldest to Newest or Sort Newest to Oldest instead.  feedback✘: Type a formula that references cell D8. D8 holds the amount for order LG-2007, which has the smallest amount (1800) in the dataset.  hints: ['A formula that returns the value from another cell starts with = followed by the cell address.', 'The amount column is column D; row 8 holds order LG-2007 with amount 1800.']  remediation→r01
  MEASURES: A:sort_number_column_single_level(f1); A:sort_date_or_time_column_single_level(f2)   anchors=['practice', 'assessment:sort_number_column_single_level', 'assessment:sort_date_or_time_column_single_level']
  taught-before-tested: A.f1←s01; A.f2←s01

### s06 · explainer · Showing Only the Rows You Need  [reward 5]
Filtering — AutoFilter hides rows that don't match your criteria — the data is still there, just not visible. Clearing the filter brings it all back.
(intro) Sometimes you don't want to reorder your Orders sheet, you want to see only some of it — for example, only the orders above a certain amount. ⟦B:tb1⟧
(mechanism) To filter a range of data, select any cell within the range, select Data > Filter, select the column header's filter arrow, choose Number Filters or Text Filters and a comparison such as Greater Than, enter the filter criteria, and select OK. AutoFilter shows the data you want and hides the rest; clearing a filter redisplays all of the data. ⟦B.f1 B.f2 B:tb2⟧
(example) A range or table can be filtered by more than one column at once; filters are additive, so each additional filter further reduces the subset of data shown. Filtering your Orders sheet to amounts greater than 5000, then filtering the city column to Lagos, leaves only the Lagos orders above 5000 — both conditions apply together, not separately. ⟦B.f3 B:tb3⟧
[BEFORE_AFTER] After filtering amount > 5000 and city = Lagos, only row 14 (LG-2013, Lagos, 6800, Pending) is visible; rows 2–13 and 15–21 are hidden, showing non-consecutive row numbers.
  before:
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","asset_ref":{"asset_id":"asset_orders_clean","variant_id":null,"columns":["order_id","city","amount","status"]},"sheet_name":"Orders","range":"A1:D6","annotations":[{"target":"A1","text":"All 20 rows visible — no filter applied"}]}
  after:
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","asset_ref":{"asset_id":"asset_orders_clean","variant_id":null,"columns":["order_id","city","amount","status"]},"sheet_name":"Orders","range":"A1:D2","annotations":[{"target":"C1","text":"Filter icon changed — amount > 5000 filter active"},{"target":"B1","text":"Second filter on city = Lagos — rows further reduced"},{"target":"A2","text":"Row 14 (LG-2013) — only row matching Lagos AND amount > 5000"}]}

### s07 · video · AutoFilter: Hiding Rows, Stacking Filters, and Clearing
Filtering — 
[VIDEO AutoFilter in action: hiding rows, stacking filters, and clearing] bridge-before: Watch how the row numbers jump when rows are hidden, and notice the filter icon change on each column header when a second filter is added on top of the first. | bridge-after: The clip uses a salesperson name and a quantity column; the text’s example uses city and order amount — same additive logic. The clip demonstrates the value-checkbox method for text and Number Filters > Greater Than for numbers; the text generalizes to Text Filters as well.
  - cB5koQvGwsA 77-287s facts=['f1', 'f2', 'f3'] label: Applying AutoFilter: turning filters on, filtering by value, adding a number filter, and clearing | summary: The presenter starts with a data range that already has filter drop-down arrows in the header row, then shows how to turn AutoFilter on and off by selecting any cell inside the range and clicking Data > Filter (also noting the Ctrl+Shift+L shortcut). Filtering the salesperson column to show only 'Andrew' hides all other rows without deleting or resorting them — the row numbers confirm the rows are merely hidden. A second filter is then added on the quantity column using Number Filters > Greater Than 80, so both conditions apply at once and the visible set shrinks further. Finally, the quantity filter is cleared from its drop-down menu, restoring the salesperson-only view and returning the column's icon to its default state.

### s08 · check · Applying AutoFilter Criteria  [reward 5]
Quick Check — Choose the correct steps to apply a Number Filter to a range.
QUESTION [choice, intro, grading=client] You want to filter the Orders table to show only orders with an amount greater than 5000. Starting from a cell inside the table, what is the correct sequence of steps?
  ✔ opt_a: Select Data > Filter, click the filter arrow on the amount column header, choose Number Filters > Greater Than, enter 5000, and click OK.
  ✘ opt_b: Select Data > Sort, choose the amount column, set the order to Largest to Smallest, and click OK.
      why: Sorting reorders the rows but does not hide any rows. To show only rows meeting a condition, use Data > Filter, not Sort.
  ✘ opt_c: Select the amount column, choose Home > Conditional Formatting > Highlight Cells Rules > Greater Than, enter 5000, and click OK.
      why: Conditional Formatting highlights cells visually but does not hide rows. To show only rows where amount > 5000, use AutoFilter.
  ✘ opt_d: Select Data > Filter, click the filter arrow on the amount column header, choose Text Filters > Greater Than, enter 5000, and click OK.
      why: Amount is a numeric column, so you should choose Number Filters, not Text Filters. Text Filters are for columns containing text values.
  feedback✔: Correct! Data > Filter turns on AutoFilter. Clicking the column header arrow and choosing Number Filters > Greater Than lets you enter a numeric threshold. Only rows meeting the condition are shown.  feedback✘: To filter a range to rows meeting a condition: select Data > Filter, click the filter arrow on the column header, choose Number Filters (for numeric columns) or Text Filters (for text columns), select the comparison, enter the value, and click OK.  hints: ["Filtering hides rows that don't match — it's on the Data tab, not the Home tab.", 'Amount is a number, so use Number Filters, not Text Filters.']  remediation→r02
  MEASURES: B:apply_autofilter_criteria_to_a_range(f1)   anchors=['assessment:apply_autofilter_criteria_to_a_range']
  taught-before-tested: B.f1←s06

### s09 · hands_on · Filter the Orders Sheet  [reward 10]
Practice — Apply a filter to show only Delivered orders from Lagos, then clear the filter to restore all rows.
QUESTION [formula_entry, core, grading=client] The Orders table has amounts in column D (D2:D21) and cities in column B (B2:B21). AutoFilter hides rows that do not match the filter criteria — it does not delete them. Clearing the filter restores all rows. Filters are additive: filtering by city 'Lagos' and then by amount > 3000 shows only rows where BOTH conditions are true. Type a formula in cell A1 that returns the amount from the first data row (D2), confirming you can read the unfiltered data.
  [unrendered interaction type formula_entry] public={"prompt":"The Orders table has amounts in column D (D2:D21) and cities in column B (B2:B21). AutoFilter hides rows that do not match the filter criteria — it does not delete them. Clearing the filter restores all rows. Filters are additive: filtering by city 'Lagos' and then by amount > 3000 shows only rows where BOTH conditions are true. Type a formula in cell A1 that returns the amount from the first data row (D2), confirming you can read the unfiltered data.","asset_ref":{"asset_id":"asset_orders_clean","variant_id":null},"target_cell":"A1","sheet_name":"asset_orders_clean"} grading={"expected_value":4500.0,"reference_formula":"=D2","must_use_functions":[],"forbid_hardcoded_values":true}
  feedback✔: Correct! =D2 returns 4500 — the amount in the first data row. AutoFilter would hide rows that don't match your criteria, but D2 would still exist in the sheet. Clearing the filter would restore all rows, including any that were hidden.  feedback✘: Type a formula that references cell D2. The amount column is column D; the first data row is row 2.  hints: ['A formula that returns the value from another cell starts with = followed by the cell address.', 'The amount column is column D; the first data row is row 2.']  remediation→r02
  MEASURES: B:explain_hide_not_delete_and_clear_to_restore(f2); B:apply_additive_multi_column_filters(f3)   anchors=['practice', 'assessment:explain_hide_not_delete_and_clear_to_restore', 'assessment:apply_additive_multi_column_filters']
  taught-before-tested: B.f2←s06; B.f3←s06

### s10 · recap · Sorting and Filtering — Key Points  [reward 5]
Recap — You can now sort by one or more columns with independent directions, and filter to show only the rows that match your criteria.
(takeaway) To sort numbers, use Sort Smallest to Largest or Largest to Smallest from the Data tab. To sort dates, use Sort Oldest to Newest or Newest to Oldest. For multi-level sorts, open Data > Sort, add levels with Add Level, and set each level's Order independently — higher levels are applied first. AutoFilter hides rows that don't match; clearing the filter redisplays all data. Filters are additive: each additional column filter further reduces the visible subset.
[UP NEXT] Next: Conditional Formatting and Data Validation: In the next tile you'll highlight cells automatically based on their values and restrict what can be entered in a column using dropdown lists.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Multi-Level Sort: Each Level Has Its Own Direction — See the contrast between a single-level sort and a two-level sort with different directions.
(example) Single-level sort: sort the Orders sheet by amount Largest to Smallest — all rows reorder by amount alone. Two-level sort: Level 1 is order_date Oldest to Newest; Level 2 is amount Largest to Smallest. The result: rows are grouped by date in ascending order, and within each date the rows are ordered by amount descending. The key point is that Level 2's direction (Largest to Smallest) is completely independent of Level 1's direction (Oldest to Newest) — you set each in its own Order dropdown. ⟦A.f3 A.f4 A:tb3 A:tb4⟧
### r02 · AutoFilter: Hide vs. Delete — Filtering hides rows — it never removes them. Clearing the filter brings them back.
(example) After applying a Number Filter (Greater Than 5000) to the amount column of your Orders sheet, rows with amounts of 5000 or less disappear from view — but they are still in the sheet. The row numbers jump (e.g. 1, 3, 7 …) because the hidden rows are still there. Clicking Data > Filter again, or clicking Clear in the Sort & Filter group, removes the filter and all rows reappear. No data was deleted. ⟦B.f1 B:tb2⟧