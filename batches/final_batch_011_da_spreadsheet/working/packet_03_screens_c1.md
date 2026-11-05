# EVALUATOR PACKET — Writing Formulas and Reference Types (tile_spreadsheet_formula_syntax_refs)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = spreadsheet.formula_syntax — Basic formula syntax and arithmetic operators
B = spreadsheet.relative_absolute_references — Relative vs absolute references ($ notation)

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (spreadsheet.formula_syntax)   objective: Write a formula that begins with an equal sign and combines cell references and arithmetic operators, or a built-in function, into one computed value.
A.f1: Formulas in Excel always begin with the equal sign (=).   [sources: excel_formulas_overview#Create a formula that refers to values in other cells]
A.f2: Excel's arithmetic operators include + for addition, - for subtraction, * for multiplication, and / for division; for example =2+4, =4-2, =2*4, and =4/2 are all valid formulas.   [sources: excel_basic_tasks_guide#Create a simple formula]
A.f3: To enter a formula that contains a built-in function, type an equal sign and the function's name, an opening parenthesis, then select the range of cells the function should use, and a closing parenthesis, then press Enter.   [sources: excel_formulas_overview#Enter a formula that contains a built-in function]
A.f4: To create a formula that refers to values in other cells, select a cell, type an equal sign, select or type the first cell's address, enter an operator such as - for subtraction, select or type the next cell's address, and press Enter.   [sources: excel_formulas_overview#Create a formula that refers to values in other cells]
A.f5: Excel performs the operations in a formula in a specific precedence order (for example, multiplication and division before addition and subtraction); parentheses change that order — =5+2*3 gives 11, but =(5+2)*3 gives 21.   [sources: excel_calculation_precedence_guide]
note: The TOC's practice for this concept asks for a percentage-change formula, which overlaps with the later stats.lift_interpretation concept -- this text teaches only general arithmetic-operator and function-call syntax, not percentage change specifically.
note: The TOC practice objective asks for a percentage-change formula, which requires dividing a difference by a base value — a pattern that anticipates stats.lift_interpretation (blocked). The practice anchor has been adapted to a plain subtraction between two cell references, which exercises f1, f2, and f4 using only allowed knowledge.
PRACTICE ANCHOR (formula): Given two cells in the Orders sheet — one holding an earlier amount and one holding a later amount — write a formula that computes the arithmetic difference between them using a cell-reference formula with the subtraction operator.  SUCCESS: The formula begins with =, references two cell addresses from the Orders sheet separated by -, and returns the correct numeric difference when entered.
ASSESSMENT ANCHOR: identify_required_equal_sign_prefix facts=['f1']
ASSESSMENT ANCHOR: apply_arithmetic_operators_in_formula facts=['f2']
ASSESSMENT ANCHOR: construct_function_call_formula_with_range facts=['f3']
ASSESSMENT ANCHOR: build_cell_reference_formula_with_operator facts=['f4']
ASSESSMENT ANCHOR: apply_operator_precedence_and_parentheses facts=['f5']
ASSESSMENT ANCHOR: write_syntactically_correct_formula_for_given_computation facts=['f1', 'f2', 'f3', 'f4', 'f5']

## SOURCE FACTS — B (spreadsheet.relative_absolute_references)   objective: Distinguish a relative cell reference from an absolute cell reference, and use $ notation to keep a reference fixed when a formula is copied.
B.f1: A relative cell reference, such as A1, is based on the relative position of the cell containing the formula and the cell it refers to; if you copy or fill the formula across rows or down columns, the reference automatically adjusts, and by default new formulas use relative references.   [sources: excel_formulas_overview#The difference between absolute, relative, and mixed references]
B.f2: An absolute cell reference, such as $A$1, always refers to a cell in a specific location; if you copy or fill the formula across rows or down columns, the absolute reference does not adjust.   [sources: excel_formulas_overview#The difference between absolute, relative, and mixed references]
B.f3: A mixed reference has either an absolute column and relative row (for example $A1) or an absolute row and relative column (for example A$1); when the formula is copied, the relative part adjusts and the absolute part does not.   [sources: excel_formulas_overview#The difference between absolute, relative, and mixed references]
PRACTICE ANCHOR (formula): In a small orders table with a Price column and a fixed tax rate in a single cell, write a formula that multiplies a relative price reference by an absolute reference to the tax-rate cell, then copy it down the column and verify each row computes correctly.  SUCCESS: Every copied formula in the column shows the correct product of that row's price and the shared tax-rate cell; the tax-rate address remains unchanged in every formula while the price address increments by row.
ASSESSMENT ANCHOR: identify_relative_reference_adjustment_on_copy facts=['f1']
ASSESSMENT ANCHOR: apply_absolute_reference_to_fix_cell_on_copy facts=['f2']
ASSESSMENT ANCHOR: construct_mixed_reference_locking_one_dimension facts=['f3']
ASSESSMENT ANCHOR: select_correct_reference_type_for_copy_scenario facts=['f1', 'f2', 'f3']

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

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjusting figure size and layout; Bar chart creation; Bar charts; Basic plot creation with the pyplot interface; Box plots; Common aggregation functions (SUM, AVERAGE, COUNT, COUNTA); Common formula error values and troubleshooting (#N/A, #REF!, #VALUE!); Conditional aggregation (COUNTIF/COUNTIFS, SUMIF/SUMIFS); Date functions and date arithmetic (TODAY, DATEDIF); Histograms; INDEX/MATCH as a lookup alternative; Labeling axes, titles, and legends; Line chart creation; Line plots; Logical functions (IF, nested IF, AND, OR); Lookup functions (VLOOKUP, HLOOKUP, XLOOKUP); Matching chart type to the analytical question; Pie chart creation; Pivot table summarization options (sum, count, average); Pivot tables: rows, columns, values, filters; Plotting directly from pandas DataFrames with seaborn; Relative vs absolute references ($ notation); Scatter plots; Text combining; Text extraction; matplotlib figure and axes object model

## LESSON, in learner order

### s01 · explainer · Every Formula Starts with =  [reward 5]
Formula Syntax — A formula turns a cell into a calculator — here's the pattern every formula follows.
(intro) In your QuickDeliver Orders sheet, most cells hold plain values — an amount, a city, a date. A formula changes that: it tells Excel to compute a result instead. Every formula begins with the equal sign (=). Without it, Excel treats the entry as text. ⟦A.f1 A:tb1 A:tb2⟧
(definition) Excel's four arithmetic operators are + (addition), - (subtraction), * (multiplication), and / (division). You can combine them with literal numbers or cell addresses: =D3-D2 subtracts one order's amount from another; =D2*2 doubles it. To reference another cell, type its address after the = and operator. ⟦A.f2 A.f4 A:tb2 A:tb3⟧
(syntax) Built-in functions follow the same = prefix but add a name and parentheses: =SUM(D2:D51) totals every amount in that range of your Orders sheet. Type =, the function name, an opening parenthesis, select the range, close the parenthesis, then press Enter. The cell shows the computed result. ⟦A.f3 A:tb4⟧
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_spreadsheet_formula_syntax_refs.s01.b4","asset_ref":{"asset_id":"asset_orders_clean"},"range":"A1:E4","sheet_name":"Orders","show_formula_bar":true,"cells":[{"ref":"F2","formula":"=D3-D2","note":"Difference between two amounts"},{"ref":"F3","formula":"=SUM(D2:D21)","note":"Total of all amounts"}],"annotations":[{"target":"F2","text":"= prefix + cell refs + operator"},{"target":"F3","text":"= prefix + function name + range"}],"lineage":{"concept_ids":["spreadsheet.formula_syntax"],"fact_ids":["spreadsheet.formula_syntax#f1","spreadsheet.formula_syntax#f2","spreadsheet.formula_syntax#f3","spreadsheet.formula_syntax#f4"],"teaching_block_ids":["spreadsheet.formula_syntax#tb2","spreadsheet.formula_syntax#tb3","spreadsheet.formula_syntax#tb4"],"anchors":["spreadsheet.formula_syntax#visual"]}}

### s02 · video · Formulas in Action
Formula Syntax — 
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · explainer · Operator Precedence and Parentheses  [reward 3]
Formula Syntax — Multiplication runs before addition — unless you use parentheses.
(mechanism) Excel evaluates multiplication and division before addition and subtraction. =5+2*3 gives 11, not 21. Wrap the addition in parentheses — =(5+2)*3 — to get 21. Whenever a formula mixes operators, check the order or add parentheses to be explicit. ⟦A.f5 A:tb5⟧

### s04 · check · The Required Formula Prefix  [reward 5]
Quick Check — Which character must every Excel formula begin with?

### s05 · check · Writing a Function Formula  [reward 5]
Quick Check — Which formula correctly sums the range C2:C21 on the Orders sheet?

### s06 · hands_on · Write Formulas on the Orders Sheet  [reward 10]
Practice — Apply arithmetic operators, cell references, and a function call to the QuickDeliver data.

### s07 · explainer · Relative and Absolute References  [reward 5]
Reference Types — Copy a formula down a column and watch which parts shift — and which stay fixed.
(definition) A relative reference such as D2 is position-based: copy the formula one row down and D2 becomes D3 automatically. By default, every new formula uses relative references. This is what you want when each row should calculate against its own data. ⟦B.f1 B:tb1 B:tb2⟧
(mechanism) An absolute reference such as $H$1 always points to the same cell, no matter where you copy the formula. Dollar signs lock both the column letter and the row number. If a delivery fee rate lives in H1, =D2*$H$1 copied down every order row keeps pointing to H1 for the rate while D2 shifts to D3, D4, and so on. ⟦B.f2 B:tb3⟧
[BEFORE_AFTER] After copying H2 down to H3 and H4, the relative part (D2→D3→D4) adjusts while the absolute part ($H$1) stays fixed.
  before:
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_spreadsheet_formula_syntax_refs.s07.b3.before","asset_ref":{"asset_id":"asset_orders_clean"},"range":"D2:H5","sheet_name":"Orders","show_formula_bar":true,"cells":[{"ref":"H2","formula":"=D2*$H$1","note":"Original formula in row 2"}],"annotations":[{"target":"H2","text":"=D2*$H$1 — D2 is relative, $H$1 is absolute"}]}
  after:
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_spreadsheet_formula_syntax_refs.s07.b3.after","asset_ref":{"asset_id":"asset_orders_clean"},"range":"D2:H5","sheet_name":"Orders","show_formula_bar":true,"cells":[{"ref":"H2","formula":"=D2*$H$1"},{"ref":"H3","formula":"=D3*$H$1"},{"ref":"H4","formula":"=D4*$H$1"}],"annotations":[{"target":"H3","text":"D3 shifted; $H$1 unchanged"}]}

### s08 · video · Watching References Shift (or Stay Fixed)
Reference Types — 
[VIDEO ] bridge-before:  | bridge-after: 

### s09 · explainer · Mixed References: Lock One Dimension  [reward 3]
Reference Types — Lock just the column or just the row — not both.
(mechanism) A mixed reference locks only one dimension. $A1 locks the column (A stays, row shifts); A$1 locks the row (1 stays, column shifts). Use a mixed reference when copying a formula across both rows and columns and only one axis should stay fixed. ⟦B.f3 B:tb4⟧

### s10 · check · Constructing a Mixed Reference  [reward 5]
Quick Check — Which reference locks the column but lets the row shift when copied down?

### s11 · hands_on · Apply Reference Types to the Orders Sheet  [reward 10]
Practice — Choose the right reference type for each copy scenario.

### s12 · recap · Formulas and Reference Types — Key Takeaways  [reward 5]
Recap — 
(takeaway) Every formula starts with =, combines cell references and operators or a function call, and follows Excel's precedence rules unless parentheses override them. Relative references shift when copied; absolute references ($A$1) stay fixed; mixed references lock one dimension. That combination is the basis for every calculation you'll write in a spreadsheet. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb6⟧
[UP NEXT] Up Next: Aggregation Functions: In the next tile you'll use SUM, AVERAGE, COUNT, and COUNTA to summarise the entire Orders column in a single formula.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Why the = Sign Matters
(definition) Excel distinguishes a formula from plain text by the leading = sign. Type 5+2 and Excel stores the text '5+2'. Type =5+2 and Excel computes 7. Every formula — whether it uses arithmetic operators or a function like SUM — must start with =. ⟦A.f1 A:tb2⟧
### r02 · Function Call Syntax
(syntax) A function formula follows the pattern =NAME(range). =SUM(D2:D21) is correct: equal sign, function name, opening parenthesis, the range, closing parenthesis. Omitting the = or the parentheses produces an error or plain text, not a computed result. ⟦A.f3 A:tb4⟧
### r03 · Mixed References: One Dollar Sign
(mechanism) A mixed reference uses exactly one $ sign. $A1 locks the column letter A — copy the formula across columns and A never changes, but the row number shifts. A$1 locks the row number 1 — copy down rows and 1 never changes, but the column shifts. Two $ signs ($A$1) lock both and make the reference fully absolute. ⟦B.f3 B:tb4⟧

=========

# EVALUATOR PACKET — Aggregation and Logical Functions (tile_spreadsheet_aggregation_logical)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = spreadsheet.aggregation_functions — Common aggregation functions (SUM, AVERAGE, COUNT, COUNTA)
B = spreadsheet.logical_functions — Logical functions (IF, nested IF, AND, OR)

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (spreadsheet.aggregation_functions)   objective: Use SUM, AVERAGE, COUNT, and COUNTA to summarize a range of values into a single number.
A.f1: The SUM function adds values; its syntax is SUM(number1, [number2], ...), where each argument can be a number, a cell reference, or a range, for example =SUM(A2:A10).   [sources: excel_sum_function#Syntax]
A.f2: The AVERAGE function returns the average (arithmetic mean) of its arguments; its syntax is AVERAGE(number1, [number2], ...), and if a range or cell-reference argument contains text, logical values, or empty cells, those values are ignored, though cells with the value zero are included.   [sources: excel_average_function#Syntax, excel_average_function#Remarks]
A.f3: The COUNT function counts the number of cells that contain numbers; its syntax is COUNT(value1, [value2], ...), and only numbers in the array or reference are counted, while empty cells, logical values, text, and error values are not.   [sources: excel_count_function#Syntax]
A.f4: The COUNTA function counts the number of cells that are not empty in a range, counting cells with any type of information including text and error values, but not empty cells; its syntax is COUNTA(value1, [value2], ...).   [sources: excel_counta_function#Syntax]
PRACTICE ANCHOR (spreadsheet): Given a column of order amounts that includes some blank cells and one text entry, write formulas to compute the total of the amounts, the average of the amounts, the count of numeric entries, and the count of all non-blank entries, then compare the COUNT and COUNTA results to explain the difference.  SUCCESS: All four formulas return correct values: SUM totals only the numbers, AVERAGE ignores blanks and the text cell, COUNT equals the number of numeric cells, COUNTA is higher by the number of non-numeric non-blank cells, and the learner can state why COUNT and COUNTA differ.
ASSESSMENT ANCHOR: apply_sum_to_a_range facts=['f1']
ASSESSMENT ANCHOR: apply_average_and_identify_ignored_values facts=['f2']
ASSESSMENT ANCHOR: apply_count_and_identify_what_is_excluded facts=['f3']
ASSESSMENT ANCHOR: apply_counta_and_distinguish_from_count facts=['f4']
ASSESSMENT ANCHOR: choose_count_vs_counta_for_a_given_summarization_requirement facts=['f3', 'f4']
ASSESSMENT ANCHOR: select_correct_aggregation_function_for_a_summarization_requirement facts=['f1', 'f2', 'f3', 'f4']

## SOURCE FACTS — B (spreadsheet.logical_functions)   objective: Write an IF formula, including nested IFs, and combine conditions with AND or OR to build the logical test.
B.f1: The IF function tests a condition and returns one value if the condition is TRUE and another value if it's FALSE; its syntax is IF(logical_test, value_if_true, [value_if_false]).   [sources: excel_if_function#Syntax]
B.f2: Multiple IF functions can be nested inside each other in order to perform more than one comparison.   [sources: excel_if_function#Simple IF examples]
B.f3: The AND function returns TRUE if all of its arguments evaluate to TRUE, and returns FALSE if one or more arguments evaluate to FALSE; its syntax is AND(logical1, [logical2], ...), and it is commonly used as the logical_test argument of IF to test more than one condition at once.   [sources: excel_and_function#Syntax, excel_and_function#Technical Details]
B.f4: The OR function returns TRUE if any of its arguments evaluate to TRUE, and returns FALSE if all of its arguments evaluate to FALSE; its syntax is OR(logical1, [logical2], ...).   [sources: excel_or_function#Syntax, excel_or_function#Technical Details]
B.f5: Text in formulas goes in quotes; for example =IF(A2>B2,"Over Budget","OK") tests whether A2 is greater than B2 and returns one of the two quoted text results.   [sources: excel_if_function#Simple IF examples, excel_if_function#Syntax]
B.f6: A nested IF can convert a numeric score to a letter grade, for example =IF(D2>89,"A",IF(D2>79,"B",IF(D2>69,"C",IF(D2>59,"D","F")))).   [sources: excel_nested_if_guide]
PRACTICE ANCHOR (formula): Write a nested IF formula in a spreadsheet that assigns a letter-grade band (A, B, C, D, F) from a numeric score in column D, using AND to combine two boundary conditions in at least one branch so that branch fires only when the score falls within a specific range.  SUCCESS: The formula in the target cell returns the correct letter grade for every score in the sample column, including boundary values, and uses AND as the logical_test of at least one IF to enforce both a lower and upper bound on a grade band.
ASSESSMENT ANCHOR: write_basic_if_formula_with_quoted_text facts=['f1', 'f5']
ASSESSMENT ANCHOR: construct_nested_if_for_multi_band_classification facts=['f2', 'f6']
ASSESSMENT ANCHOR: use_and_as_if_logical_test_for_multiple_conditions facts=['f3']
ASSESSMENT ANCHOR: use_or_as_if_logical_test_for_any_condition facts=['f4']
ASSESSMENT ANCHOR: select_and_combine_if_and_or_for_given_decision_logic facts=['f1', 'f2', 'f3', 'f4', 'f5', 'f6']

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

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjusting figure size and layout; Bar chart creation; Bar charts; Basic plot creation with the pyplot interface; Box plots; Common formula error values and troubleshooting (#N/A, #REF!, #VALUE!); Conditional aggregation (COUNTIF/COUNTIFS, SUMIF/SUMIFS); Date functions and date arithmetic (TODAY, DATEDIF); Histograms; INDEX/MATCH as a lookup alternative; Labeling axes, titles, and legends; Line chart creation; Line plots; Logical functions (IF, nested IF, AND, OR); Lookup functions (VLOOKUP, HLOOKUP, XLOOKUP); Matching chart type to the analytical question; Pie chart creation; Pivot table summarization options (sum, count, average); Pivot tables: rows, columns, values, filters; Plotting directly from pandas DataFrames with seaborn; Scatter plots; Text combining; Text extraction; matplotlib figure and axes object model; seaborn built-in themes and color palettes; seaborn statistical plotting functions

## LESSON, in learner order

### s01 · explainer · SUM, AVERAGE, COUNT, and COUNTA  [reward 5]
Aggregation Functions — Four functions that reduce a whole column to one summary number.
(syntax) With a full column of delivery amounts or times, you often want one summary number. SUM adds every value in a range: =SUM(D2:D21) totals all order amounts on your Orders sheet. AVERAGE returns the arithmetic mean: =AVERAGE(C2:C21) gives the average delivery time, skipping any blank cells (Pending or Cancelled orders have no recorded time). ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3⟧
[SIDE_BY_SIDE] COUNT returns a smaller number than COUNTA when the column contains blanks or text, because COUNT skips non-numeric cells while COUNTA counts everything that is not empty. left_label: COUNT (numbers only) | right_label: COUNTA (any non-blank)
  left:
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_spreadsheet_aggregation_logical.s01.b2.left","asset_ref":{"asset_id":"asset_orders_clean"},"range":"C1:C6","sheet_name":"Orders","show_formula_bar":true,"cells":[{"ref":"C22","formula":"=COUNT(C2:C21)","note":"Counts numeric cells only"}],"annotations":[{"target":"C22","text":"=COUNT — numbers only"}]}
  right:
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_spreadsheet_aggregation_logical.s01.b2.right","asset_ref":{"asset_id":"asset_orders_clean"},"range":"C1:C6","sheet_name":"Orders","show_formula_bar":true,"cells":[{"ref":"C23","formula":"=COUNTA(C2:C21)","note":"Counts all non-blank cells"}],"annotations":[{"target":"C23","text":"=COUNTA — any non-blank"}]}

### s02 · video · Aggregation Functions in Action
Aggregation Functions — 
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · explainer · COUNT vs COUNTA: What Gets Counted  [reward 5]
Aggregation Functions — The difference matters whenever a column mixes numbers, blanks, or text.
(mechanism) COUNT counts only cells that contain numbers; empty cells, text, and error values are skipped. On your Orders sheet, =COUNT(C2:C21) counts only the rows where delivery_minutes is recorded (Delivered orders) — Pending and Cancelled rows with NULL times are excluded. ⟦A.f3 A:tb4⟧
(mechanism) COUNTA counts every cell that is not empty, regardless of type — numbers, text, or error values all count. =COUNTA(C2:C21) on the same column returns a larger number than COUNT because it includes any row that has any value at all. Use COUNTA when you need to count rows, not just numeric entries. ⟦A.f4 A:tb4⟧

### s04 · check · Choosing the Right Aggregation Function  [reward 5]
Quick Check — Which function should you use for each summarisation requirement?

### s05 · hands_on · Summarise the Orders Sheet  [reward 10]
Practice — Write SUM, AVERAGE, COUNT, and COUNTA formulas on the QuickDeliver data.

### s06 · explainer · IF, Nested IF, AND, and OR  [reward 5]
Logical Functions — Label, flag, or categorise rows based on conditions — without changing the data.
(syntax) IF tests a condition and returns one value when it is TRUE and another when it is FALSE. Its syntax is IF(logical_test, value_if_true, value_if_false). Text results go in quotes: =IF(C2>60,"Late","On Time") labels each order row on your Orders sheet based on its delivery_minutes value. ⟦B.f1 B.f5 B:tb1 B:tb2⟧
(mechanism) Multiple IF functions can be nested to handle more than two outcomes. =IF(D2>89,"A",IF(D2>79,"B",IF(D2>69,"C",IF(D2>59,"D","F")))) converts a numeric score to a letter grade. The same structure could sort orders into amount bands instead of a single Late/On-Time split. ⟦B.f2 B.f6 B:tb3⟧
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_spreadsheet_aggregation_logical.s06.b3","asset_ref":{"asset_id":"asset_orders_clean"},"range":"C1:D5","sheet_name":"Orders","show_formula_bar":true,"cells":[{"ref":"D2","formula":"=IF(C2>60,\"Late\",\"On Time\")","note":"Logical test on delivery_minutes"},{"ref":"D3","formula":"=IF(C3>60,\"Late\",\"On Time\")"},{"ref":"D4","formula":"=IF(C4>60,\"Late\",\"On Time\")"}],"annotations":[{"target":"D2","text":"IF formula in formula bar"},{"target":"D1","text":"Grade column shows result"}],"lineage":{"concept_ids":["spreadsheet.logical_functions"],"fact_ids":["spreadsheet.logical_functions#f1","spreadsheet.logical_functions#f2","spreadsheet.logical_functions#f5","spreadsheet.logical_functions#f6"],"teaching_block_ids":["spreadsheet.logical_functions#tb2","spreadsheet.logical_functions#tb3"],"anchors":["spreadsheet.logical_functions#visual"]}}

### s07 · video · Logical Functions in Action
Logical Functions — 
[VIDEO ] bridge-before:  | bridge-after: 

### s08 · explainer · AND and OR: Testing Multiple Conditions  [reward 5]
Logical Functions — Combine conditions inside IF to test more than one thing at once.
(syntax) AND returns TRUE only when all of its arguments are TRUE; if any one is FALSE, AND returns FALSE. Its syntax is AND(logical1, logical2, ...). Use AND as the logical_test of IF to require every condition to hold: =IF(AND(C2>30,E2="Delivered"),"Fast Delivery","Other") flags only orders that are both fast and delivered. ⟦B.f3 B:tb4⟧
(syntax) OR returns TRUE when any of its arguments is TRUE; it returns FALSE only when all arguments are FALSE. Its syntax is OR(logical1, logical2, ...). =IF(OR(E2="Pending",E2="Cancelled"),"Not Delivered","Delivered") flags any order that has not yet completed. ⟦B.f4 B:tb4⟧

### s09 · check · Reading an IF Formula  [reward 5]
Quick Check — Which formula correctly labels an order as "Late" when delivery_minutes exceeds 60?

### s10 · hands_on · AND vs OR  [reward 5]
Quick Check — Which function returns TRUE only when every condition is met?

### s11 · recap · Aggregation and Logical Functions — Key Takeaways  [reward 5]
Recap — What you've learned in this tile.
(takeaway) SUM, AVERAGE, COUNT, and COUNTA each reduce a range to one number; which one you reach for depends on whether you need a total, a mean, a count of numbers, or a count of anything non-blank. IF tests a condition and returns different values for TRUE and FALSE; nest IFs for multiple outcomes, and use AND or OR to combine conditions. ⟦A.f1 A.f2 A.f3 A.f4 B.f1 B.f2 B.f3 B.f4 B.f5 A:tb5⟧
[UP NEXT] Up Next: Text, Date, and Conditional Aggregation: In the next tile you'll combine and extract text with TEXTJOIN and LEFT/RIGHT/MID, calculate date differences with TODAY and DATEDIF, and count or sum only the rows that meet a condition with COUNTIF and SUMIFS.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Matching the Function to the Task
(mechanism) SUM totals numbers. AVERAGE finds the mean (blank cells are skipped, zero-value cells are included). COUNT counts only numeric cells — blank and text cells are excluded. COUNTA counts every non-blank cell regardless of type. On the Orders sheet: use SUM for total amount, AVERAGE for mean delivery time, COUNT for how many deliveries have a recorded time, COUNTA for how many rows have any entry. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧
### r02 · How IF Evaluates a Condition
(mechanism) IF(logical_test, value_if_true, value_if_false) evaluates the test first. If the test is TRUE, the formula returns value_if_true; if FALSE, value_if_false. =IF(C2>60,"Late","On Time"): when C2 is 45, the test 45>60 is FALSE, so the formula returns "On Time". Text values in IF must be wrapped in quotes. ⟦B.f1 B.f5 B:tb2⟧
### r03 · AND Requires All; OR Requires Any
(mechanism) AND(condition1, condition2) returns TRUE only when every condition is TRUE — one FALSE makes the whole AND FALSE. OR(condition1, condition2) returns TRUE when at least one condition is TRUE — it returns FALSE only when every condition is FALSE. Use AND when all criteria must hold; use OR when any one is enough. ⟦B.f3 B.f4 B:tb4⟧

## OTHER CONTENT (fields without a dedicated renderer)
· cells.formula: =IF(C3>60,"Late","On Time")
· cells.formula: =IF(C4>60,"Late","On Time")

=========

# EVALUATOR PACKET — Text, Date, and Conditional Aggregation (tile_spreadsheet_text_date_conditional_agg)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = spreadsheet.text_combining — Text combining
B = spreadsheet.text_extraction — Text extraction
C = spreadsheet.date_functions — Date functions and date arithmetic (TODAY, DATEDIF)
D = spreadsheet.conditional_aggregation — Conditional aggregation (COUNTIF/COUNTIFS, SUMIF/SUMIFS)

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (spreadsheet.text_combining)   objective: Combine several text values into one string using TEXTJOIN or CONCATENATE, inserting a delimiter between the joined values.
A.f1: TEXTJOIN combines text from multiple ranges or strings and inserts a delimiter you specify between each text value; its syntax is TEXTJOIN(delimiter, ignore_empty, text1, [text2], ...).   [sources: excel_textjoin_function#Syntax]
A.f2: In TEXTJOIN, setting the ignore_empty argument to TRUE skips empty cells among the arguments rather than joining them in as blank values.   [sources: excel_textjoin_function#Syntax]
A.f3: CONCATENATE joins two or more text strings into one string; its syntax is CONCATENATE(text1, [text2], ...), though Microsoft recommends using the newer CONCAT function instead, since CONCATENATE may not be available in future versions of Excel.   [sources: excel_concatenate_function#Syntax]
PRACTICE ANCHOR (spreadsheet): Given a spreadsheet with a First_Name column (A) and a Last_Name column (B), write a TEXTJOIN formula in column C that combines each row's first and last name into a single full-name string separated by a space, skipping any empty cells.  SUCCESS: Column C displays the correctly joined full name for each row (e.g., 'Jane Smith'), with no leading or trailing spaces caused by empty cells, using TEXTJOIN with a space delimiter and ignore_empty set to TRUE.
ASSESSMENT ANCHOR: build_combined_string_from_cells_with_delimiter facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: apply_textjoin_with_ignore_empty facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_concatenate_syntax_and_deprecation_caveat facts=['f3']

## SOURCE FACTS — B (spreadsheet.text_extraction)   objective: Extract a substring from fixed positions in a text value using LEFT, RIGHT, or MID, and remove extra spaces using TRIM.
B.f1: LEFT returns the first character or characters in a text string, based on the number of characters you specify; its syntax is LEFT(text, [num_chars]).   [sources: excel_left_function#Syntax]
B.f2: RIGHT returns the last character or characters in a text string, based on the number of characters you specify; its syntax is RIGHT(text, [num_chars]).   [sources: excel_right_function#Syntax]
B.f3: MID returns a specific number of characters from a text string, starting at the position you specify; its syntax is MID(text, start_num, num_chars).   [sources: excel_mid_function#Syntax]
B.f4: TRIM removes all spaces from a text value except for single spaces between words; its syntax is TRIM(text).   [sources: excel_trim_function#Syntax]
PRACTICE ANCHOR (spreadsheet): Given a column of phone numbers formatted as '(234) 801-0000' and a column of imported city names with leading or trailing spaces, write formulas to extract the three-digit area code from inside the parentheses and to remove the stray spaces from the city column.  SUCCESS: The area-code column shows only the three digits (e.g. '234') for every row, and the cleaned city column shows values with no leading or trailing spaces (e.g. 'Lagos' not ' Lagos ').
ASSESSMENT ANCHOR: apply_left_to_extract_leading_characters facts=['f1']
ASSESSMENT ANCHOR: apply_right_to_extract_trailing_characters facts=['f2']
ASSESSMENT ANCHOR: apply_mid_to_extract_characters_by_position facts=['f3']
ASSESSMENT ANCHOR: apply_trim_to_remove_extraneous_whitespace facts=['f4']
ASSESSMENT ANCHOR: select_correct_extraction_function_for_given_text_task facts=['f1', 'f2', 'f3', 'f4']

## SOURCE FACTS — C (spreadsheet.date_functions)   objective: Compute a date-based value, such as an age in years, using TODAY together with DATEDIF.
C.f1: The TODAY function returns the serial number of the current date and takes no arguments; its syntax is TODAY().   [sources: excel_today_function#Syntax]
C.f2: The DATEDIF function returns the difference between a start_date and an end_date in the unit you specify; its syntax is DATEDIF(start_date, end_date, unit), where a unit of "Y" returns the number of complete years in the period.   [sources: excel_datedif_function#Syntax]
C.f3: DATEDIF is useful in formulas where you need to calculate an age.   [sources: excel_datedif_function#Remarks]
C.f4: Excel stores dates as sequential serial numbers so they can be used in calculations; by default, January 1, 1900 is serial number 1.   [sources: excel_today_function#Syntax]
C.f5: DATEDIF's unit argument "D" returns the number of days in the period between start_date and end_date.   [sources: excel_datedif_function#Syntax]
PRACTICE ANCHOR (formula): Given a spreadsheet with a Birthdate column (column B, starting at B2), write a formula in column C that computes each person's age in complete years using TODAY and DATEDIF.  SUCCESS: The formula =DATEDIF(B2,TODAY(),"Y") (or equivalent using the correct argument order and unit) is entered in C2 and returns a whole-number age that updates to the current date; the learner can explain that TODAY() supplies the end date and "Y" returns complete years.
ASSESSMENT ANCHOR: write_today_function_with_correct_syntax facts=['f1']
ASSESSMENT ANCHOR: write_datedif_with_correct_arguments_and_unit facts=['f2', 'f5']
ASSESSMENT ANCHOR: construct_age_calculation_formula_using_datedif_and_today facts=['f3', 'f2', 'f1']
ASSESSMENT ANCHOR: explain_date_serial_number_model facts=['f4']
ASSESSMENT ANCHOR: select_correct_date_function_for_given_calculation_requirement facts=['f1', 'f2', 'f5']

## SOURCE FACTS — D (spreadsheet.conditional_aggregation)   objective: Aggregate only the rows that match one or more conditions using COUNTIF, COUNTIFS, SUMIF, or SUMIFS.
D.f1: COUNTIF counts the number of cells in a range that meet a single criterion; its syntax is COUNTIF(range, criteria).   [sources: excel_countif_function#Syntax]
D.f2: COUNTIFS applies criteria to cells across multiple ranges and counts the number of times all the criteria are met together; its syntax is COUNTIFS(criteria_range1, criteria1, [criteria_range2, criteria2], ...), and each additional range must have the same number of rows and columns as criteria_range1.   [sources: excel_countifs_function#Syntax]
D.f3: SUMIF sums the values in a range that meet criteria you specify, optionally applying the criteria to one range while summing the corresponding values in a different range; its syntax is SUMIF(range, criteria, [sum_range]).   [sources: excel_sumif_function#Syntax]
D.f4: SUMIFS adds the cells in a sum_range that meet multiple criteria at once, where each criteria_range/criteria pair is a separate condition that must all be met; its syntax is SUMIFS(sum_range, criteria_range1, criteria1, [criteria_range2, criteria2], ...).   [sources: excel_sumifs_function#Syntax]
D.f5: Criteria for these functions can be a number, expression, cell reference, or text, such as 32, ">32", B4, or "apples"; criteria containing comparison symbols or text must be enclosed in quotation marks.   [sources: excel_countif_function#Syntax, excel_sumif_function#Syntax]
D.f6: The same range can be used in more than one criteria pair to test a range condition, for example =COUNTIFS(A2:A7,"<6",A2:A7,">1") counts values between 1 and 6.   [sources: excel_countifs_function#Syntax]
PRACTICE ANCHOR (spreadsheet): Given a sales table with columns Region, Date, and Amount, write a SUMIFS formula that totals Amount only for rows where Region equals a specified value and Date falls within a given date range, using three criteria_range/criteria pairs (one for Region, two for the Date range boundaries).  SUCCESS: The formula returns the correct total that matches a manual filter of the table for the specified region and date range, with no #VALUE! or #NAME? errors.
ASSESSMENT ANCHOR: write_single_condition_countif_sumif facts=['f1', 'f3']
ASSESSMENT ANCHOR: write_multi_condition_countifs_sumifs facts=['f2', 'f4']
ASSESSMENT ANCHOR: apply_correct_criteria_syntax_quoting facts=['f5']
ASSESSMENT ANCHOR: use_same_range_twice_for_between_condition facts=['f6']

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

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjusting figure size and layout; Bar chart creation; Bar charts; Basic A/B test structure (control vs treatment group); Basic plot creation with the pyplot interface; Box plots; Common formula error values and troubleshooting (#N/A, #REF!, #VALUE!); Conditional aggregation (COUNTIF/COUNTIFS, SUMIF/SUMIFS); Custom styling/theming (advanced/optional); Date functions and date arithmetic (TODAY, DATEDIF); Histograms; INDEX/MATCH as a lookup alternative; Interpreting lift/percentage change between groups; Labeling axes, titles, and legends; Line chart creation; Line plots; Lookup functions (VLOOKUP, HLOOKUP, XLOOKUP); Matching chart type to the analytical question; Multi-panel figures/subplots (advanced/optional); Pie chart creation; Pivot table summarization options (sum, count, average); Pivot tables: rows, columns, values, filters; Plotting directly from pandas DataFrames with seaborn; Scatter plots; Text extraction; matplotlib figure and axes object model; seaborn built-in themes and color palettes; seaborn statistical plotting functions

## LESSON, in learner order

### s01 · explainer · Combining Text with TEXTJOIN and CONCATENATE  [reward 5]
Text Functions — Merge values from separate cells into one string — with or without a separator.
(syntax) TEXTJOIN combines text from multiple ranges or strings and inserts a delimiter between each value. Its syntax is TEXTJOIN(delimiter, ignore_empty, text1, text2, ...). Setting ignore_empty to TRUE skips blank cells rather than joining them as empty strings. On your Orders sheet, TEXTJOIN(", ", TRUE, B2, E2) would merge the city and status columns, skipping any blank status. ⟦A.f1 A.f2 A:tb1⟧
(syntax) CONCATENATE joins two or more text strings into one: CONCATENATE(text1, text2, ...). Microsoft recommends using the newer CONCAT function instead, as CONCATENATE may not be available in future versions of Excel. Neither function adds a separator automatically — include it as a literal argument if you need one. ⟦A.f3 A:tb2⟧
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_spreadsheet_text_date_conditional_agg.s01.b3","asset_ref":{"asset_id":"asset_orders_clean"},"range":"A1:F4","sheet_name":"Orders","show_formula_bar":true,"cells":[{"ref":"G2","formula":"=TEXTJOIN(\", \",TRUE,B2,E2)","note":"Combines city and status"},{"ref":"G3","formula":"=TEXTJOIN(\", \",TRUE,B3,E3)"}],"annotations":[{"target":"G2","text":"TEXTJOIN with \", \" delimiter"}],"lineage":{"concept_ids":["spreadsheet.text_combining"],"fact_ids":["spreadsheet.text_combining#f1","spreadsheet.text_combining#f2","spreadsheet.text_combining#f3"],"teaching_block_ids":["spreadsheet.text_combining#tb1","spreadsheet.text_combining#tb2"],"anchors":["spreadsheet.text_combining#visual"]}}

### s02 · check · CONCATENATE Syntax and Deprecation  [reward 5]
Quick Check — What is the syntax of CONCATENATE, and why does Microsoft recommend using CONCAT instead?

### s03 · hands_on · Combine Text Columns on the Orders Sheet  [reward 10]
Practice — Use TEXTJOIN to merge city and status into a single label.

### s04 · explainer · Extracting Text with LEFT, RIGHT, MID, and TRIM  [reward 5]
Text Functions — Pull specific characters out of a string — or strip unwanted spaces.
(syntax) LEFT returns the first N characters of a string: LEFT(text, num_chars). RIGHT returns the last N characters: RIGHT(text, num_chars). On order IDs like "LG-2045", =LEFT(A2,2) returns "LG" and =RIGHT(A2,4) returns "2045". ⟦B.f1 B.f2 B:tb1⟧
(syntax) MID returns characters from any position: MID(text, start_num, num_chars). =MID(A2,4,4) on "LG-2045" starts at position 4 and takes 4 characters, returning "2045". TRIM removes all leading and trailing spaces, keeping only single spaces between words: TRIM(text). If a city was imported as " Lagos ", =TRIM(B2) returns "Lagos". ⟦B.f3 B.f4 B:tb2 B:tb3⟧
[BEFORE_AFTER] LEFT extracts the two-character prefix from the order ID; TRIM removes the stray spaces from the city name.
  before:
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_spreadsheet_text_date_conditional_agg.s04.b3.before","asset_ref":{"asset_id":"asset_orders_clean"},"range":"A1:B4","sheet_name":"Orders","show_formula_bar":true,"cells":[{"ref":"A2","note":"LG-2045 — raw order ID"},{"ref":"B2","note":" Lagos  — imported with spaces"}],"annotations":[{"target":"A2","text":"Raw: LG-2045"},{"target":"B2","text":"Raw: \" Lagos \""}]}
  after:
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_spreadsheet_text_date_conditional_agg.s04.b3.after","asset_ref":{"asset_id":"asset_orders_clean"},"range":"A1:D4","sheet_name":"Orders","show_formula_bar":true,"cells":[{"ref":"C2","formula":"=LEFT(A2,2)","note":"Returns LG"},{"ref":"D2","formula":"=TRIM(B2)","note":"Returns Lagos"}],"annotations":[{"target":"C2","text":"=LEFT(A2,2) → \"LG\""},{"target":"D2","text":"=TRIM(B2) → \"Lagos\""}]}

### s05 · check · MID and TRIM  [reward 5]
Quick Check — Which formula extracts 4 characters starting at position 4 from cell A2?

### s06 · check · Choosing the Right Extraction Function  [reward 5]
Quick Check — Which function should you use for each text extraction task?

### s07 · hands_on · Extract Characters from Order IDs  [reward 10]
Practice — Use LEFT and RIGHT to pull the prefix and numeric suffix from the order_id column.

### s08 · explainer · TODAY, DATEDIF, and the Date Serial Number  [reward 5]
Date Functions — Excel stores dates as numbers — which makes date arithmetic straightforward.
(mechanism) Excel stores every date as a sequential serial number: January 1, 1900 is 1, and each subsequent day adds 1. That is why date functions can do arithmetic on dates the same way ordinary functions do on numbers — a date cell is just a number displayed in a date format. ⟦C.f4 C:tb1⟧
(syntax) TODAY() returns the serial number of the current date and takes no arguments. DATEDIF(start_date, end_date, unit) returns the difference between two dates in the unit you specify: "Y" for complete years, "D" for days. DATEDIF is useful for age calculations: DATEDIF(birthdate, TODAY(), "Y") returns the number of complete years between the birthdate and today. ⟦C.f1 C.f2 C.f3 C.f5 C:tb2 C:tb3⟧
(example) On your Orders sheet, with an order date in G2, =DATEDIF(G2,TODAY(),"D") tells you how many days have passed since that order was placed. TODAY() supplies the end date automatically, so the result updates each day the workbook is opened. ⟦C.f1 C.f2 C:tb4⟧
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_spreadsheet_text_date_conditional_agg.s08.b4","asset_ref":{"asset_id":"asset_orders_clean"},"range":"G1:H4","sheet_name":"Orders","show_formula_bar":true,"cells":[{"ref":"H2","formula":"=DATEDIF(G2,TODAY(),\"D\")","note":"Days since order placed"},{"ref":"H3","formula":"=DATEDIF(G3,TODAY(),\"D\")"}],"annotations":[{"target":"H2","text":"DATEDIF formula in formula bar"},{"target":"G2","text":"order_date (serial number)"}],"lineage":{"concept_ids":["spreadsheet.date_functions"],"fact_ids":["spreadsheet.date_functions#f1","spreadsheet.date_functions#f2","spreadsheet.date_functions#f3","spreadsheet.date_functions#f4","spreadsheet.date_functions#f5"],"teaching_block_ids":["spreadsheet.date_functions#tb1","spreadsheet.date_functions#tb2","spreadsheet.date_functions#tb3","spreadsheet.date_functions#tb4"],"anchors":["spreadsheet.date_functions#visual"]}}

### s09 · check · Choosing the Right Date Function  [reward 5]
Quick Check — Which function returns the number of days between two dates?

### s10 · hands_on · Calculate Days Since Each Order Was Placed  [reward 10]
Practice — Write a DATEDIF formula using TODAY() to find how many days have passed since each order date.

### s11 · explainer · COUNTIF and SUMIF: One Condition  [reward 5]
Conditional Aggregation — Count or sum only the rows that match a single criterion.
(intro) SUM, AVERAGE, COUNT, and COUNTA take every value in their range. When you only want rows that meet a condition — orders from Lagos, say — use COUNTIF or SUMIF instead. ⟦D.f1 D.f3 D:tb1⟧
(syntax) COUNTIF(range, criteria) counts the cells in range that match criteria. =COUNTIF(B2:B21,"Lagos") counts how many orders in the city column are from Lagos. SUMIF(range, criteria, sum_range) sums the values in sum_range for rows where range matches criteria. =SUMIF(B2:B21,"Lagos",D2:D21) totals the amounts for Lagos orders only. ⟦D.f1 D.f3 D:tb2⟧
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_spreadsheet_text_date_conditional_agg.s11.b3","asset_ref":{"asset_id":"asset_orders_clean"},"range":"A1:E6","sheet_name":"Orders","show_formula_bar":true,"cells":[{"ref":"G2","formula":"=COUNTIF(B2:B21,\"Lagos\")","note":"Count of Lagos orders"},{"ref":"G3","formula":"=SUMIF(B2:B21,\"Lagos\",D2:D21)","note":"Total amount for Lagos"}],"annotations":[{"target":"G2","text":"COUNTIF — criteria range + criterion"},{"target":"G3","text":"SUMIF — criteria range + criterion + sum range"}],"lineage":{"concept_ids":["spreadsheet.conditional_aggregation"],"fact_ids":["spreadsheet.conditional_aggregation#f1","spreadsheet.conditional_aggregation#f3"],"teaching_block_ids":["spreadsheet.conditional_aggregation#tb1","spreadsheet.conditional_aggregation#tb2"],"anchors":["spreadsheet.conditional_aggregation#visual"]}}

### s12 · explainer · COUNTIFS and SUMIFS: Multiple Conditions  [reward 5]
Conditional Aggregation — Add a second (or third) condition by extending the argument list.
(syntax) COUNTIFS(criteria_range1, criteria1, criteria_range2, criteria2, ...) counts rows where all criteria are met together. Each additional range must have the same number of rows and columns as the first. =COUNTIFS(B2:B21,"Lagos",E2:E21,"Delivered") counts only Lagos orders that are Delivered. ⟦D.f2 D:tb3⟧
(syntax) SUMIFS(sum_range, criteria_range1, criteria1, criteria_range2, criteria2, ...) sums sum_range for rows where all criteria hold. Note the argument order: sum_range comes first, then each criteria_range/criteria pair. =SUMIFS(D2:D21,B2:B21,"Lagos",E2:E21,"Delivered") totals amounts for Lagos Delivered orders. ⟦D.f4 D:tb3⟧

### s13 · video · Building Conditional Aggregation Formulas
Conditional Aggregation — 
[VIDEO ] bridge-before:  | bridge-after: 

### s14 · explainer · Criteria Syntax and the Between Pattern  [reward 5]
Conditional Aggregation — Criteria with comparison symbols or text must be in quotes — and you can use the same range twice.
(mechanism) Criteria can be a number, an expression, a cell reference, or text. Criteria that contain comparison symbols or text must be enclosed in quotation marks: use ">32" not >32, and "Lagos" not Lagos. A bare number like 32 or a cell reference like B4 does not need quotes. ⟦D.f5 D:tb4⟧
(mechanism) The same range can appear in more than one criteria pair to test a between condition. =COUNTIFS(C2:C21,">30",C2:C21,"<60") counts orders where delivery_minutes is between 30 and 60 — both criteria apply to the same column. ⟦D.f6 D:tb4⟧

### s15 · check · Single vs Multi-Condition Aggregation  [reward 5]
Quick Check — Which function counts rows that meet two conditions at once?

### s16 · check · The Between Pattern  [reward 5]
Quick Check — How do you count values in C2:C21 that are greater than 30 AND less than 60?

### s17 · hands_on · Write Conditional Aggregation Formulas  [reward 10]
Practice — Apply correct criteria quoting to COUNTIF and SUMIFS on the Orders sheet.

### s18 · recap · Text, Date, and Conditional Aggregation — Key Takeaways  [reward 5]
Recap — 
(takeaway) TEXTJOIN combines text with a delimiter; CONCATENATE (or CONCAT) joins without one. LEFT, RIGHT, and MID extract characters by position; TRIM removes stray spaces. Excel stores dates as serial numbers starting from January 1, 1900; TODAY() returns today's serial number and DATEDIF computes the difference in years or days. COUNTIF and SUMIF apply one condition; COUNTIFS and SUMIFS apply multiple — criteria with text or comparison symbols must be in quotes. ⟦A.f1 A.f2 A.f3 B.f1 B.f2 B.f3 B.f4 C.f1 C.f2 C.f4 D.f1 D.f2 D.f3 D.f4 D.f5⟧
[UP NEXT] Up Next: VLOOKUP, XLOOKUP, and INDEX/MATCH: In the next tile you'll look up a driver name from the Drivers sheet using VLOOKUP, then see how XLOOKUP and INDEX/MATCH handle cases VLOOKUP cannot.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · TEXTJOIN's ignore_empty Argument
(syntax) TEXTJOIN(delimiter, ignore_empty, text1, text2, ...) has three required parts. The delimiter is the separator inserted between each value. ignore_empty controls blank cells: TRUE skips them so no extra delimiter appears; FALSE includes them as empty strings. TEXTJOIN(", ", TRUE, B2, E2) on a row where E2 is blank returns just the city, not "Lagos, ". ⟦A.f1 A.f2 A:tb1⟧
### r02 · MID and TRIM Syntax
(syntax) MID(text, start_num, num_chars) needs three arguments: the text, where to start (1-based), and how many characters to take. =MID(A2,4,4) on "LG-2045" starts at position 4 (the '2') and takes 4 characters, returning "2045". TRIM(text) takes one argument and removes all leading and trailing spaces, leaving only single spaces between words. ⟦B.f3 B.f4 B:tb2 B:tb3⟧
### r03 · TODAY vs DATEDIF
(syntax) TODAY() returns the current date as a serial number and takes no arguments — it is always =TODAY() with empty parentheses. DATEDIF(start_date, end_date, unit) computes the difference between two dates. Use "D" as the unit for days and "Y" for complete years. To find days since an order was placed: =DATEDIF(G2,TODAY(),"D"). ⟦C.f1 C.f2 C.f5 C:tb2 C:tb3⟧
### r04 · COUNTIF/SUMIF vs COUNTIFS/SUMIFS
(mechanism) COUNTIF and SUMIF each accept exactly one criteria range and one criterion. COUNTIFS and SUMIFS accept any number of criteria_range/criteria pairs — all conditions must be met for a row to be counted or summed. For two conditions (city = Lagos AND status = Delivered), use COUNTIFS or SUMIFS, not COUNTIF or SUMIF. ⟦D.f1 D.f2 D.f3 D.f4 D:tb2 D:tb3⟧
### r05 · Using the Same Range Twice for a Between Condition
(mechanism) COUNTIFS allows the same range to appear in more than one criteria pair. To count values between 30 and 60 in C2:C21, write: =COUNTIFS(C2:C21,">30",C2:C21,"<60"). The first pair filters rows where delivery_minutes > 30; the second pair further filters to delivery_minutes < 60. Both criteria must be in quotes because they contain comparison symbols. ⟦D.f6 D:tb4⟧

## OTHER CONTENT (fields without a dedicated renderer)
· cells.formula: =TEXTJOIN(", ",TRUE,B2,E2)
· cells.formula: =TEXTJOIN(", ",TRUE,B3,E3)
· annotations.text: TEXTJOIN with ", " delimiter
· cells.formula: =DATEDIF(G3,TODAY(),"D")