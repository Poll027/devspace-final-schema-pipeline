# EVALUATOR PACKET — The Spreadsheet Grid and Cell References (tile_spreadsheet_grid_references)
Tile summary: Introduces the spreadsheet grid model (cells, rows, columns, sheets) and A1 cell references and ranges, using the QuickDeliver orders workbook as context.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = spreadsheet.grid_model — Spreadsheet grid model (cells, rows, columns, sheets)
B = spreadsheet.cell_references_ranges — Cell references and ranges

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (spreadsheet.grid_model)   objective: Recognize that a spreadsheet is a grid of cells addressed by column letter and row number, and that a workbook can contain multiple named sheets.
A.f1: A spreadsheet's cells are grouped into rows and columns, forming a grid, and each cell can contain a number, text, or a formula.   [sources: excel_basic_tasks_guide#Basic tasks in Excel]
A.f2: Cells are referenced by their location in the row and column on the sheet, for example cell A1 is in the first row of column A; by default, Excel uses the A1 reference style, referring to columns with letters and rows with numbers, so a cell like B2 is at the intersection of column B and row 2.   [sources: excel_basic_tasks_guide#Enter your data, excel_formulas_overview#The A1 reference style]
A.f3: A workbook can contain multiple sheets, often called spreadsheets, and you can add as many sheets to a workbook as you want.   [sources: excel_basic_tasks_guide#Create a new workbook]
A.f4: By default, Excel names worksheets Sheet1, Sheet2, Sheet3 and so on; the name appears on the sheet tab and can be renamed.   [sources: excel_rename_worksheet_guide]
note: The TOC's assessment for this concept expects the learner to identify which sheet a reference points to, which really belongs to spreadsheet.cross_sheet_references (taught later in this chunk) -- this text only covers the grid, cell addressing, and that a workbook can hold multiple named sheets.
note: Don't introduce range references (A10:A20) here -- that's the next concept.
note: The TOC assessment target asks learners to identify which sheet a reference points to; because cross-sheet reference syntax is blocked (spreadsheet.cross_sheet_references), the assessment is scoped to recognising a sheet by its tab name only — no Sheet1!A1 notation is introduced or tested here.
PRACTICE ANCHOR (spreadsheet): Given a described sample workbook with two sheets (Orders and Drivers) and a small grid of delivery data, identify the correct cell address (column letter + row number) and sheet name for a specified piece of data.  SUCCESS: The learner names the correct cell address (e.g., B2) and the correct sheet tab name for each piece of data without confusing row and column orientation or mixing up sheet names.
ASSESSMENT ANCHOR: identify_cell_address_from_grid_position facts=['f2']
ASSESSMENT ANCHOR: identify_sheet_name_from_workbook_tab facts=['f3', 'f4']
ASSESSMENT ANCHOR: distinguish_cell_contents_and_address facts=['f1', 'f2']

## SOURCE FACTS — B (spreadsheet.cell_references_ranges)   objective: Write a single-cell reference and a range reference in A1 notation, including a whole-row or whole-column range.
B.f1: A reference identifies a cell or a range of cells on a worksheet, and tells Excel where to look for the values you want to use in a formula.   [sources: excel_formulas_overview#Using references in Excel formulas]
B.f2: In the A1 reference style, a cell is referred to by its column letter followed by its row number, for example B2.   [sources: excel_formulas_overview#The A1 reference style]
B.f3: A10:A20 refers to the range of cells in column A and rows 10 through 20; A10:E20 refers to the range in columns A through E and rows 10 through 20.   [sources: excel_formulas_overview#The A1 reference style]
B.f4: An entire row or column can be referenced with just its row number or column letter repeated on either side of a colon, for example 5:5 for all cells in row 5, or H:H for all cells in column H.   [sources: excel_formulas_overview#The A1 reference style]
note: The TOC practice objective asks the learner to write a formula that sums a range, but SUM and formula syntax are taught in later concepts (spreadsheet.formula_syntax, spreadsheet.aggregation_functions). The practice anchor has been adapted to focus solely on writing and identifying range references, which is the full scope of this concept.
PRACTICE ANCHOR (spreadsheet): Given a description of a data region (e.g., 'column C, rows 2 through 51' or 'all cells in column B'), write the correct range reference that covers exactly those cells.  SUCCESS: The learner produces the exact range notation (e.g., C2:C51, B:B, A10:E20) that matches the described region, with no extra or missing cells and correct colon syntax.
ASSESSMENT ANCHOR: write_correct_cell_or_range_reference_for_formula_requirement facts=['f1', 'f2', 'f3', 'f4']
ASSESSMENT ANCHOR: identify_single_cell_by_column_letter_and_row_number facts=['f2']
ASSESSMENT ANCHOR: write_rectangular_range_reference_using_colon_notation facts=['f3']
ASSESSMENT ANCHOR: write_whole_row_or_whole_column_reference facts=['f4']

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

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Bar chart creation; Basic formula syntax and arithmetic operators; Cell references and ranges; Common aggregation functions (SUM, AVERAGE, COUNT, COUNTA); Common formula error values and troubleshooting (#N/A, #REF!, #VALUE!); Conditional aggregation (COUNTIF/COUNTIFS, SUMIF/SUMIFS); Conditional formatting; Cross-referencing cells across multiple sheets/workbooks; Data validation (dropdown lists, input restrictions); Date functions and date arithmetic (TODAY, DATEDIF); Filtering data (AutoFilter/basic filters); INDEX/MATCH as a lookup alternative; Line chart creation; Logical functions (IF, nested IF, AND, OR); Lookup functions (VLOOKUP, HLOOKUP, XLOOKUP); Named ranges; Pie chart creation; Pivot table summarization options (sum, count, average); Pivot tables: rows, columns, values, filters; Relative vs absolute references ($ notation); Remove duplicates cleaning; Sorting data ranges; Structured tables; Text combining; Text extraction; Text to columns split

## LESSON, in learner order

### s01 · explainer · Every cell has an address  [reward 5]
The Spreadsheet Grid — A spreadsheet is a grid of cells, each one named by its column letter and row number.
(intro) Open a new workbook and you already have structure before you type anything. Cells are grouped into rows and columns, forming a grid, and each cell can hold a number, text, or a formula. Think of it like a table where every slot has its own name. ⟦A.f1 A:tb1⟧
(definition) Each cell's name is its address: the column letter followed by the row number. Excel uses the A1 reference style by default — columns are letters, rows are numbers. So the cell at the intersection of column B and row 2 is called B2. If you type a delivery city into the second row of the second column, you're typing into B2. ⟦A.f2 A:tb2⟧
[DIAGRAM: Spreadsheet grid: columns, rows, cells, and sheet tabs] nodes=['Column headers', 'A', 'B', 'C', 'Row 1', 'Row 2', 'Row 3', 'B2 — column B, row 2', 'Sheet1', 'Sheet2'] edges=[('col_b', 'cell_b2', 'column B'), ('row2', 'cell_b2', 'row 2')] alt: A small spreadsheet grid showing column letters A, B, C across the top and row numbers 1, 2, 3 down the side. Cell B2 is highlighted at the intersection of column B and row 2. Two sheet tabs at the bottom are labelled Sheet1 and Sheet2.

### s02 · explainer · One workbook, many sheets  [reward 5]
The Spreadsheet Grid — A workbook can hold multiple sheets, each with its own grid.
(mechanism) A workbook is not limited to one grid. It can contain multiple sheets — you can add as many as you need. By default Excel names them Sheet1, Sheet2, Sheet3 and so on; the name appears on the sheet tab at the bottom and can be renamed. A QuickDeliver workbook might start with Sheet1 for orders and Sheet2 for drivers, then you rename each tab to Orders and Drivers. ⟦A.f3 A.f4 A:tb3⟧

### s03 · check · Cell address vs. cell contents  [reward 5]
Quick Check — Test your understanding of what a cell address is and what a cell can contain.
QUESTION [choice, intro, grading=client] A cell in the Orders sheet displays the text "Lagos". Which of the following best describes the difference between the cell's address and its contents?
  ✔ opt_a: The address is the column-letter/row-number label (e.g., B2) that identifies where the cell sits in the grid; the contents are the value stored inside it (e.g., "Lagos").
  ✘ opt_b: The address is the value stored in the cell (e.g., "Lagos"); the column letter and row number are just display labels.
      why: That is reversed. The value "Lagos" is the cell's contents — what is stored inside it. The address is the column-letter/row-number label (like B2) that tells you where the cell lives in the grid.
  ✘ opt_c: The address and the contents are the same thing — both refer to the text "Lagos" shown in the cell.
      why: They are different things. The address (e.g., B2) is a fixed location label; the contents (e.g., "Lagos") are what you typed or calculated. You could change the contents without changing the address.
  ✘ opt_d: The address is the row number only (e.g., 2); the column letter is part of the contents.
      why: A cell address includes both the column letter and the row number together (e.g., B2). Neither part alone is the address, and neither is part of the contents.
  feedback✔: Exactly right. The address (B2) is the fixed grid location; the contents ("Lagos") are the value stored there. You can change the contents without changing the address.  feedback✘: The address is the column-letter/row-number label that locates the cell in the grid (e.g., B2). The contents are the value stored inside that cell (e.g., "Lagos"). They are two separate things.  hints: ['Think about what stays the same when you type something new into a cell — the location label or the value?', 'In Excel, the Name Box (top-left) shows the address; the cell itself shows the contents.']  remediation→r01
  MEASURES: A:distinguish_cell_contents_and_address(f1,f2)   anchors=['assessment:distinguish_cell_contents_and_address']
  taught-before-tested: A.f1←s01; A.f2←s01

### s04 · hands_on · Navigate the QuickDeliver workbook  [reward 10]
Practice — Identify cell addresses and sheet names in the Orders workbook.
QUESTION [formula_entry, core, grading=client] The QuickDeliver workbook has a sheet named Orders. In that sheet, column B holds the delivery city and row 2 holds the first order. Type a formula in cell A1 that returns the value stored at the intersection of column B and row 2.
  [unrendered interaction type formula_entry] public={"prompt":"The QuickDeliver workbook has a sheet named Orders. In that sheet, column B holds the delivery city and row 2 holds the first order. Type a formula in cell A1 that returns the value stored at the intersection of column B and row 2.","asset_ref":{"asset_id":"asset_orders_clean","variant_id":null},"sheet_name":"Orders","target_cell":"A1","allowed_functions":[]} grading={"expected_value":"Lagos","reference_formula":"=B2","must_use_functions":[],"forbid_hardcoded_values":true}
  feedback✔: Correct! =B2 points at column B, row 2 — the first order's city in the Orders sheet. The address B2 is the column letter followed by the row number, exactly as the A1 reference style works.  feedback✘: Remember: a cell address is the column letter followed by the row number. Column B, row 2 gives the address B2. Type =B2 to return the value stored there.  hints: ['The column letter comes first, then the row number — no space between them.', 'Start your formula with = so Excel knows it is a formula, not plain text.']  remediation→r02
  MEASURES: A:identify_cell_address_from_grid_position(f2); A:identify_sheet_name_from_workbook_tab(f3,f4); A:distinguish_cell_contents_and_address(f1,f2)   anchors=['practice', 'assessment:identify_cell_address_from_grid_position', 'assessment:identify_sheet_name_from_workbook_tab', 'assessment:distinguish_cell_contents_and_address']
  taught-before-tested: A.f2←s01; A.f3←s02; A.f4←s02; A.f1←s01; A.f2←s01

### s05 · explainer · Pointing at one cell or many  [reward 5]
Cell References and Ranges — A reference tells Excel exactly which cell or cells to use in a formula.
(intro) A reference identifies a cell or a range of cells on a worksheet and tells Excel where to look for the values a formula needs. Without a reference, a formula can only work with numbers you type directly — references let it reach into the grid. ⟦B.f1 B:tb1⟧
(definition) In the A1 reference style, a single cell is referred to by its column letter followed by its row number — for example B2. That is the same address you would use to describe one order's city in the Orders sheet. ⟦B.f2 B:tb2⟧
(mechanism) A reference can also point at a block of cells at once. A10:A20 refers to the range in column A, rows 10 through 20. A10:E20 refers to the range in columns A through E, rows 10 through 20. If delivery times sit in column C, rows 2 through 21, then C2:C21 covers every delivery time in that batch. ⟦B.f3 B:tb3⟧
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_spreadsheet_grid_references.s05.b4","asset_ref":{"asset_id":"asset_orders_clean"},"range":"A1:E21","selection":"A10:E20","annotations":[{"target":"A10:E20","text":"Rectangular range A10:E20 — rows 10 through 20, columns A through E"}],"lineage":{"concept_ids":["spreadsheet.cell_references_ranges"],"fact_ids":["spreadsheet.cell_references_ranges#f2","spreadsheet.cell_references_ranges#f3"],"teaching_block_ids":["spreadsheet.cell_references_ranges#tb2","spreadsheet.cell_references_ranges#tb3"],"anchors":["spreadsheet.cell_references_ranges#visual"]}}

### s06 · explainer · Referencing an entire row or column  [reward 5]
Cell References and Ranges — Use a repeated letter or number to select every cell in a column or row.
(mechanism) You can reference an entire row or column by repeating its letter or number on either side of a colon: 5:5 selects all cells in row 5, and H:H selects all cells in column H. If new orders keep being added to the Orders sheet and you want a reference that always covers the whole city column, B:B does that. ⟦B.f4 B:tb4⟧

### s07 · check · Whole-row and whole-column references  [reward 5]
Quick Check — Choose the correct reference notation for an entire row or column.
QUESTION [choice, core, grading=client] New delivery orders are added to the Orders sheet every day, so the city column keeps growing. Which reference covers every cell in column B, no matter how many rows are added?
  ✔ opt_a: B:B
  ✘ opt_b: B2:B51
      why: B2:B51 covers only rows 2 through 51. If a 52nd order is added, that row is outside the range. A whole-column reference like B:B always covers every row, past and future.
  ✘ opt_c: B1
      why: B1 is a single-cell reference — it points at just one cell, the header row. It does not cover the rest of column B.
  ✘ opt_d: B:2
      why: B:2 is not valid range notation. A whole-column reference repeats the column letter on both sides of the colon: B:B. A whole-row reference repeats the row number: 2:2.
  feedback✔: Correct! B:B selects every cell in column B by repeating the column letter on both sides of the colon. It automatically includes any new rows added later.  feedback✘: To reference an entire column, repeat the column letter on both sides of a colon: B:B. This covers every row in column B, including rows added in the future.  hints: ['A whole-column reference uses the same letter twice, separated by a colon.', 'Compare: 5:5 selects all of row 5; the same pattern with a letter selects all of a column.']  remediation→r03
  MEASURES: B:write_whole_row_or_whole_column_reference(f4)   anchors=['assessment:write_whole_row_or_whole_column_reference']
  taught-before-tested: B.f4←s06

### s08 · hands_on · Write range references for the Orders sheet  [reward 10]
Practice — Given a described data region, write the exact range reference that covers it.
QUESTION [formula_entry, stretch, grading=client] The Orders sheet has 20 orders in rows 2 through 21. The delivery_minutes values are in column C. COUNTA counts the number of non-empty cells in a range. In cell A1, type a formula using COUNTA that counts how many non-empty delivery_minutes values are in column C, rows 2 through 21. Use the range C2:C21.
  [unrendered interaction type formula_entry] public={"prompt":"The Orders sheet has 20 orders in rows 2 through 21. The delivery_minutes values are in column C. COUNTA counts the number of non-empty cells in a range. In cell A1, type a formula using COUNTA that counts how many non-empty delivery_minutes values are in column C, rows 2 through 21. Use the range C2:C21.","asset_ref":{"asset_id":"asset_orders_clean","variant_id":null},"sheet_name":"Orders","target_cell":"A1","allowed_functions":["COUNTA"]} grading={"expected_value":13,"reference_formula":"=COUNTA(C2:C21)","must_use_functions":["COUNTA"],"forbid_hardcoded_values":true}
  feedback✔: Correct! =COUNTA(C2:C21) uses the range C2:C21 — column C, rows 2 through 21 — to count the 13 non-empty delivery_minutes values. The colon separates the first cell from the last cell in the rectangular block.  feedback✘: The range covering column C, rows 2 through 21 is written C2:C21. The first cell reference (C2) and the last cell reference (C21) are separated by a colon. Type =COUNTA(C2:C21).  hints: ['A rectangular range is written as the top-left cell, a colon, then the bottom-right cell — for example A10:E20.', 'For a single-column range, both cell references share the same column letter: C2:C21 stays in column C.']  remediation→r04
  MEASURES: B:write_correct_cell_or_range_reference_for_formula_requirement(f1,f2,f3,f4); B:identify_single_cell_by_column_letter_and_row_number(f2); B:write_rectangular_range_reference_using_colon_notation(f3); B:write_whole_row_or_whole_column_reference(f4)   anchors=['practice', 'assessment:write_correct_cell_or_range_reference_for_formula_requirement', 'assessment:identify_single_cell_by_column_letter_and_row_number', 'assessment:write_rectangular_range_reference_using_colon_notation', 'assessment:write_whole_row_or_whole_column_reference']
  taught-before-tested: B.f1←s05; B.f2←s05; B.f3←s05; B.f4←s06; B.f2←s05; B.f3←s05; B.f4←s06

### s09 · recap · The grid, addresses, and ranges  [reward 5]
Recap — Everything in a spreadsheet starts from the cell address and the range.
(takeaway) A cell is found by its column-letter/row-number address, and a workbook can hold several grids as separate sheets. A reference points at one cell or a block of cells; a range like A10:E20 covers a rectangular block, while H:H covers an entire column. Every formula you write from here will use one of these reference forms. ⟦A.f1 A.f2 A.f3 A.f4 B.f1 B.f2 B.f3 B.f4 A:tb4 B:tb5⟧
[UP NEXT] Up next: Structured Tables: In the next tile you will convert the Orders range into an Excel table — giving each column a labelled header and letting formulas refer to columns by name.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Re-check: address vs. contents — A cell's address and its contents are two different things — here is the contrast.
(misconception) The address B2 is the cell's location — column B, row 2. The contents of B2 is whatever you have typed or calculated there: a number, a city name, or a formula. Changing the contents does not change the address; B2 is always B2 regardless of what is inside it. ⟦A.f1 A.f2 A:tb2⟧
### r02 · Re-check: grid structure and sheet names — Rows, columns, and sheet tabs — a quick contrast to clear up confusion.
(misconception) Columns run left to right and are labelled with letters (A, B, C…). Rows run top to bottom and are labelled with numbers (1, 2, 3…). A workbook can hold multiple sheets; by default they are named Sheet1, Sheet2 and so on, and each name appears on its tab at the bottom of the screen. ⟦A.f1 A.f2 A.f3 A.f4 A:tb3⟧
### r03 · Re-check: whole-row and whole-column notation — The colon syntax for selecting an entire row or column — a clear contrast.
(misconception) To reference all cells in row 5, write 5:5 — the row number on both sides of the colon. To reference all cells in column H, write H:H — the column letter on both sides. This is different from a rectangular range like A10:E20, which uses different start and end addresses. H:H always expands as new rows are added. ⟦B.f4 B:tb4⟧
### r04 · Re-check: single-cell and range references — Single cells, rectangular blocks, and whole-column references — the three forms side by side.
(mechanism) A single-cell reference uses column letter then row number: B2. A rectangular range uses a start address, a colon, and an end address: A10:E20 covers columns A through E, rows 10 through 20. A whole-column reference repeats the letter: B:B covers every cell in column B. A formula picks the form that matches how many cells it needs. ⟦B.f1 B.f2 B.f3 B.f4 B:tb1 B:tb2 B:tb3 B:tb4⟧