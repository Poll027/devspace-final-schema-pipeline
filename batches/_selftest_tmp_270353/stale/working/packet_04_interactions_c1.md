# EVALUATOR PACKET — Aggregation and Logical Functions (tile_spreadsheet_aggregation_logical)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = spreadsheet.aggregation_functions — Common aggregation functions (SUM, AVERAGE, COUNT, COUNTA)
B = spreadsheet.logical_functions — Logical functions (IF, nested IF, AND, OR)

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=4
  warn: remediation step tile_spreadsheet_aggregation_logical.r03 is never referenced
  warn: plan: tile_spreadsheet_aggregation_logical.s05 was planned to measure spreadsheet.aggregation_functions#assessment:apply_sum_to_a_range but its interaction does not
  warn: plan: tile_spreadsheet_aggregation_logical.s05 was planned to measure spreadsheet.aggregation_functions#assessment:apply_average_and_identify_ignored_values but its interaction does not
  warn: plan: tile_spreadsheet_aggregation_logical.s05 was planned to measure spreadsheet.aggregation_functions#assessment:apply_count_and_identify_what_is_excluded but its interaction does not

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
(syntax) With a full column of delivery amounts or times, you often want one summary number. SUM adds every value in a range: =SUM(D2:D21) totals all order amounts on your Orders sheet. AVERAGE returns the arithmetic mean: =AVERAGE(C2:C21) gives the average delivery time, skipping blank cells and text but including any cell that contains zero (Pending or Cancelled orders with no recorded time are blank, not zero, so they are excluded). ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3⟧
[SIDE_BY_SIDE] COUNT returns a smaller number than COUNTA when the column contains blanks or text, because COUNT skips non-numeric cells while COUNTA counts everything that is not empty. left_label: COUNT (numbers only) | right_label: COUNTA (any non-blank)
  left:
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_spreadsheet_aggregation_logical.s01.b2.left","asset_ref":{"asset_id":"asset_orders_clean"},"range":"C1:C6","sheet_name":"Orders","show_formula_bar":true,"cells":[{"ref":"C22","formula":"=COUNT(C2:C21)","note":"Counts numeric cells only"}],"annotations":[{"target":"C22","text":"=COUNT — numbers only"}],"computed_values":{"C22":13}}
  right:
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_spreadsheet_aggregation_logical.s01.b2.right","asset_ref":{"asset_id":"asset_orders_clean"},"range":"C1:C6","sheet_name":"Orders","show_formula_bar":true,"cells":[{"ref":"C23","formula":"=COUNTA(C2:C21)","note":"Counts all non-blank cells"}],"annotations":[{"target":"C23","text":"=COUNTA — any non-blank"}],"computed_values":{"C23":13}}

### s02 · video · Aggregation Functions in Action
Aggregation Functions — 
[VIDEO SUM, AVERAGE, and COUNT demonstrated on a number column] bridge-before: Watch how SUM, AVERAGE, and COUNT are entered and what each returns. Note: COUNTA is not shown here — the text covers it. | bridge-after: The clip confirms COUNT ignores blank cells. The text adds the full rule: COUNT also skips text and logical values, and introduces COUNTA for counting anything non-blank.
  - BzwAZ1k3WEY 24-161s facts=['f1', 'f2', 'f3'] label: SUM, AVERAGE, and COUNT applied to a range of numbers | summary: The presenter enters =SUM over a column of ten numbers and gets 5,220, then builds =AVERAGE over the same range, pausing to show it is equivalent to dividing the SUM by the COUNT of that range. Finally, =COUNT is applied to the same column, returning 10; deleting one value drops the result to 9, confirming that COUNT only registers cells holding numbers.

### s03 · explainer · COUNT vs COUNTA: What Gets Counted  [reward 5]
Aggregation Functions — The difference matters whenever a column mixes numbers, blanks, or text.
(mechanism) COUNT counts only cells that contain numbers; empty cells, text, and error values are skipped. On your Orders sheet, =COUNT(C2:C21) counts only the rows where delivery_minutes is recorded (Delivered orders) — Pending and Cancelled rows with NULL times are excluded. ⟦A.f3 A:tb4⟧
(mechanism) COUNTA counts every cell that is not empty, regardless of type — numbers, text, or error values all count. =COUNTA(C2:C21) on the same column returns a larger number than COUNT because it includes any row that has any value at all. Use COUNTA when you need to count rows, not just numeric entries. ⟦A.f4 A:tb4⟧

### s04 · check · Choosing the Right Aggregation Function  [reward 5]
Quick Check — Which function should you use for each summarisation requirement?
QUESTION [choice, core, grading=client] The Orders sheet has 20 rows. Column A holds order IDs (text like "LG-2001"), column C holds delivery_minutes (numbers for delivered orders, blank for pending/cancelled), and column D holds order amounts (all numbers).

A manager asks: "How many orders have a recorded delivery time?" Which function should you use, and why?
  ✔ opt_a: COUNT(C2:C21) — because COUNT counts only numeric cells and delivery_minutes is blank for undelivered orders.
  ✘ opt_b: COUNTA(C2:C21) — because COUNTA counts all non-empty cells, including text.
      why: COUNTA counts any non-empty cell, including text. For delivery_minutes, all non-blank cells are numbers, so COUNTA and COUNT give the same result here. But COUNT is the precise choice: it counts only numeric cells, which is exactly what 'has a recorded delivery time' means.
  ✘ opt_c: SUM(C2:C21) — because SUM adds up all the delivery times to give a total count.
      why: SUM adds the values together and returns a total number of minutes, not a count of rows. To count how many rows have a value, use COUNT or COUNTA.
  ✘ opt_d: AVERAGE(C2:C21) — because AVERAGE returns the number of values in the range.
      why: AVERAGE returns the arithmetic mean of the values, not the number of values. To count how many cells contain a number, use COUNT.
  feedback✔: Correct! COUNT(C2:C21) counts only the numeric cells in the delivery_minutes column. Blank cells (for pending/cancelled orders) are skipped, so the result equals the number of orders with a recorded delivery time.  feedback✘: COUNT counts only numeric cells and ignores blanks, text, and logical values. Because delivery_minutes is blank for undelivered orders, COUNT(C2:C21) returns exactly the number of orders that have a recorded delivery time.  hints: ['COUNT counts only numbers. COUNTA counts anything that is not empty. SUM adds values. AVERAGE computes a mean.', 'Blank cells in delivery_minutes represent orders with no recorded time — COUNT skips them automatically.']  remediation→r01
  MEASURES: A:select_correct_aggregation_function_for_a_summarization_requirement(f1,f2,f3,f4); A:apply_sum_to_a_range(f1); A:apply_average_and_identify_ignored_values(f2); A:apply_count_and_identify_what_is_excluded(f3)   anchors=['assessment:select_correct_aggregation_function_for_a_summarization_requirement', 'assessment:apply_sum_to_a_range', 'assessment:apply_average_and_identify_ignored_values', 'assessment:apply_count_and_identify_what_is_excluded']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s03; A.f4←s03; A.f1←s01; A.f2←s01; A.f3←s03

### s05 · hands_on · Summarise the Orders Sheet  [reward 10]
Practice — Write SUM, AVERAGE, COUNT, and COUNTA formulas on the QuickDeliver data.
QUESTION [formula_entry, core, grading=client] The Orders sheet has 20 rows of data (rows 2–21). Column A holds order IDs — text values like "LG-2001". Column D holds order amounts — all numeric.

In cell H1, write a formula using **COUNTA** that counts how many non-empty cells are in the order_id column (A2:A21). Because order IDs are text, COUNT would return 0 — COUNTA is the right choice here.

The expected result is **20**.
  [unrendered interaction type formula_entry] public={"prompt":"The Orders sheet has 20 rows of data (rows 2–21). Column A holds order IDs — text values like \"LG-2001\". Column D holds order amounts — all numeric.\n\nIn cell H1, write a formula using **COUNTA** that counts how many non-empty cells are in the order_id column (A2:A21). Because order IDs are text, COUNT would return 0 — COUNTA is the right choice here.\n\nThe expected result is **20**.","asset_ref":{"asset_id":"asset_orders_clean","variant_id":null},"target_cell":"H1","allowed_functions":["COUNTA"],"sheet_name":"orders"} grading={"expected_value":20,"reference_formula":"=COUNTA(A2:A21)","must_use_functions":["COUNTA"],"forbid_hardcoded_values":true}
  feedback✔: Correct! =COUNTA(A2:A21) returns 20 because all 20 order-ID cells are non-empty. COUNTA counts any non-empty cell — numbers, text, or errors — while COUNT counts only numeric cells. Since order IDs are text, COUNT(A2:A21) would return 0.  feedback✘: Use =COUNTA(A2:A21). COUNTA counts every non-empty cell regardless of type, so it correctly counts the 20 text order IDs. COUNT would return 0 here because it only counts numeric cells.  hints: ['COUNTA counts cells that contain any value — numbers, text, or errors. COUNT counts only numbers.', 'The range A2:A21 covers all 20 data rows in column A (order_id).']  remediation→r01
  MEASURES: A:apply_counta_and_distinguish_from_count(f3,f4); A:choose_count_vs_counta_for_a_given_summarization_requirement(f3,f4)   anchors=['assessment:apply_counta_and_distinguish_from_count', 'assessment:choose_count_vs_counta_for_a_given_summarization_requirement']
  taught-before-tested: A.f3←s03; A.f4←s03; A.f3←s03; A.f4←s03

### s06 · explainer · IF, Nested IF, AND, and OR  [reward 5]
Logical Functions — Label, flag, or categorise rows based on conditions — without changing the data.
(syntax) IF tests a condition and returns one value when it is TRUE and another when it is FALSE. Its syntax is IF(logical_test, value_if_true, value_if_false). Text results go in quotes: =IF(C2>60,"Late","On Time") placed in a helper column (H) labels each order row based on its delivery_minutes value without overwriting the amount column. ⟦B.f1 B.f5 B:tb1 B:tb2⟧
(mechanism) Multiple IF functions can be nested to handle more than two outcomes. =IF(H2>89,"A",IF(H2>79,"B",IF(H2>69,"C",IF(H2>59,"D","F")))) converts a numeric score to a letter grade. The same structure could sort orders into delivery-time bands in a helper column instead of a single Late/On-Time split. ⟦B.f2 B.f6 B:tb3⟧
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_spreadsheet_aggregation_logical.s06.b3","asset_ref":{"asset_id":"asset_orders_clean"},"range":"C1:H5","sheet_name":"Orders","show_formula_bar":true,"cells":[{"ref":"H2","formula":"=IF(C2>60,\"Late\",\"On Time\")","note":"Logical test on delivery_minutes"},{"ref":"H3","formula":"=IF(C3>60,\"Late\",\"On Time\")"},{"ref":"H4","formula":"=IF(C4>60,\"Late\",\"On Time\")"}],"annotations":[{"target":"H2","text":"IF formula in formula bar"},{"target":"H1","text":"Status label column shows result"}],"lineage":{"concept_ids":["spreadsheet.logical_functions"],"fact_ids":["spreadsheet.logical_functions#f1","spreadsheet.logical_functions#f2","spreadsheet.logical_functions#f5","spreadsheet.logical_functions#f6"],"teaching_block_ids":["spreadsheet.logical_functions#tb2","spreadsheet.logical_functions#tb3"],"anchors":["spreadsheet.logical_functions#visual"]},"computed_values":{"H2":"On Time","H3":"On Time","H4":"Late"}}

### s07 · video · Logical Functions in Action
Logical Functions — 
[VIDEO Building IF, AND, and OR formulas step by step in a spreadsheet] bridge-before: Watch how each formula is built argument by argument. Notice where AND and OR sit inside IF, and how a second IF slots into the false branch. Neither clip covers the letter-grade nested-IF pattern from the teaching text. | bridge-after: The clips show the evaluation order clearly: Excel stops at the first TRUE branch. The teaching text covers the letter-grade nested-IF example (f6) that neither clip demonstrates.
  - 5vHT16cEOPc 0-224s facts=['f1', 'f3', 'f4', 'f5'] label: IF with AND and OR: classifying rows by one or two conditions | summary: Using a travel-claims dataset, the presenter builds an IF formula that labels claims as 'high value' or 'standard' based on a single amount threshold, demonstrating that text results must be wrapped in double quotes. AND is then introduced in isolation to show it returns TRUE only when every condition is met, before being placed inside IF's logical-test argument to auto-approve claims that satisfy two criteria at once. OR is introduced next: it returns TRUE when at least one condition is met and FALSE only when all conditions are FALSE, and is used inside IF to calculate a settlement offer for claims meeting either of two criteria. A formula result (a calculation) is shown without quotes, contrasting with quoted text.
  - KkTaQ5OjAGc 55-557s facts=['f1', 'f2', 'f3', 'f4', 'f5'] label: Nested IF with AND and OR: layering multiple conditions on a revenue list | summary: Working through a list of apps and their revenues, the presenter builds an IF formula argument by argument, noting that text values in formulas require quotation marks and that an empty string ('""') returns nothing. AND is then placed inside IF's logical-test position to check two revenue boundaries simultaneously. A nested IF is constructed by placing a second IF inside the value-if-false argument of the first, producing three outcome bands; the presenter notes that Excel exits the formula as soon as it finds a TRUE condition, so order matters. Finally, OR is used inside IF's logical-test to flag rows that meet either of two threshold conditions.

### s08 · explainer · AND and OR: Testing Multiple Conditions  [reward 5]
Logical Functions — Combine conditions inside IF to test more than one thing at once.
(syntax) AND returns TRUE only when all of its arguments are TRUE; if any one is FALSE, AND returns FALSE. Its syntax is AND(logical1, logical2, ...). Use AND as the logical_test of IF to require every condition to hold: =IF(AND(C2>30,E2="Delivered"),"Fast Delivery","Other") flags only orders that are both fast and delivered. ⟦B.f3 B:tb4⟧
(syntax) OR returns TRUE when any of its arguments is TRUE; it returns FALSE only when all arguments are FALSE. Its syntax is OR(logical1, logical2, ...). =IF(OR(E2="Pending",E2="Cancelled"),"Not Delivered","Delivered") flags any order that has not yet completed. ⟦B.f4 B:tb4⟧

### s09 · check · Reading an IF Formula  [reward 5]
Quick Check — Which formula correctly labels an order as "Late" when delivery_minutes exceeds 60?
QUESTION [choice, intro, grading=client] Cell C2 holds a delivery time in minutes. You want a formula in F2 that displays "Late" if the delivery took more than 60 minutes, or "On Time" otherwise.

Which formula is correct?
  ✔ opt_a: =IF(C2>60,"Late","On Time")
  ✘ opt_b: =IF(C2>60,Late,On Time)
      why: Text results in an IF formula must be enclosed in double quotation marks. Without quotes, Excel tries to interpret Late and On Time as cell names or named ranges and returns a #NAME? error.
  ✘ opt_c: =IF("C2>60","Late","On Time")
      why: The logical_test (C2>60) must not be in quotes. Putting it in quotes makes Excel treat it as a text string rather than evaluating it as a comparison, so the condition is never tested.
  ✘ opt_d: =IF(C2>60,"On Time","Late")
      why: The arguments are in the wrong order. IF(logical_test, value_if_true, value_if_false): the second argument is returned when the condition is TRUE (C2>60), so "Late" must come second, not "On Time".
  feedback✔: Correct! =IF(C2>60,"Late","On Time") tests whether C2 is greater than 60. If TRUE it returns the text "Late"; if FALSE it returns "On Time". Text values in formulas must always be wrapped in double quotation marks.  feedback✘: The IF syntax is IF(logical_test, value_if_true, value_if_false). Text results must be in double quotes: "Late" and "On Time". The logical test (C2>60) must not be in quotes — it is a comparison, not text.  hints: ['Text in a formula always goes inside double quotation marks, like "Late".', 'The second argument of IF is what is returned when the condition is TRUE.']  remediation→r02
  MEASURES: B:write_basic_if_formula_with_quoted_text(f1,f5)   anchors=['assessment:write_basic_if_formula_with_quoted_text']
  taught-before-tested: B.f1←s06; B.f5←s06

### s10 · hands_on · AND vs OR  [reward 5]
Practice — Write nested IF formulas with AND and OR to classify delivery times.
QUESTION [code_exercise, stretch, grading=client] The **orders** sheet has delivery times in column C (rows 2–5). You need to classify each delivery into one of three bands:

- **"Late"** if delivery_minutes > 60
- **"On Time"** if delivery_minutes is between 30 and 60 (inclusive on both ends)
- **"Fast"** if delivery_minutes < 30

**Task 1 — nested IF with AND:** In cell F2, write a nested IF formula that classifies the delivery time in C2. Use **AND** as the logical_test of the inner IF to enforce both the lower bound (>=30) and the upper bound (<=60) of the "On Time" band. Then write the same formula in F3 and F4.

Expected results:
- F2: **"Fast"** (C2 = 28)
- F3: **"Fast"** (C3 = 25)
- F4: **"On Time"** (C4 = 56)

**Task 2 — OR flag:** In cell F5, write an IF formula that returns **"Extreme"** if C5 is less than 20 **OR** greater than 70, and **"Normal"** otherwise. Use **OR** as the logical_test.

Expected result:
- F5: **"Extreme"** (C5 = 19)
  runtime={'kind': 'spreadsheet', 'version': '3.4.0'} constraints.allowed=['IF(logical_test, value_if_true, value_if_false)', 'AND(condition1, condition2)', 'OR(condition1, condition2)', 'comparison operators', 'text in quotes', 'numbers', 'relative cell references'] blocked=3 items
  file book.sheet [editable]:
// The orders sheet has delivery_minutes in column C.
// Input cells (typed constants - the gate will mutate these):
orders!C2: 28
orders!C3: 25
orders!C4: 56
orders!C5: 19

// Task 1: In F2, write a nested IF formula that classifies C2 as:
//   'Late'    if C2 > 60
//   'On Time' if C2 >= 30 AND C2 <= 60  (use AND for both bounds)
//   'Fast'    if C2 < 30
// Then write the same pattern in F3 and F4.

// Task 2: In F5, write an IF formula that returns 'Extreme' if
//   C5 < 20 OR C5 > 70, and 'Normal' otherwise. Use OR.

  SOLUTION book.sheet:
// Input cells (typed constants):
orders!C2: 28
orders!C3: 25
orders!C4: 56
orders!C5: 19

// Formula cells:
F2: =IF(C2>60,"Late",IF(AND(C2>=30,C2<=60),"On Time","Fast"))
F3: =IF(C3>60,"Late",IF(AND(C3>=30,C3<=60),"On Time","Fast"))
F4: =IF(C4>60,"Late",IF(AND(C4>=30,C4<=60),"On Time","Fast"))
F5: =IF(OR(C5<20,C5>70),"Extreme","Normal")

  test test_f2_fast (cell_equals, visible=True): {"cell":"F2","expected":"Fast"} | on-fail: F2 should be "Fast" because C2=28 is less than 30. Check the order of your IF conditions: test >60 first, then AND(>=30,<=60), then the else is Fast.
  test test_f3_fast (cell_equals, visible=True): {"cell":"F3","expected":"Fast"} | on-fail: F3 should be "Fast" because C3=25 is less than 30. Check the order of your IF conditions: test >60 first, then AND(>=30,<=60), then the else is Fast.
  test test_f4_on_time (cell_equals, visible=True): {"cell":"F4","expected":"On Time"} | on-fail: F4 should be "On Time" because C4=56 is between 30 and 60. Use AND(C4>=30,C4<=60) as the logical_test of the inner IF.
  test test_f2_uses_if_and (formula_uses, visible=True): {"cell":"F2","functions":["IF","AND"]} | on-fail: F2 must use both IF and AND. Use AND(C2>=30,C2<=60) as the logical_test of the inner IF to enforce both bounds of the 'On Time' band.
  test test_f5_extreme (cell_equals, visible=True): {"cell":"F5","expected":"Extreme"} | on-fail: F5 should be "Extreme" because C5=19 is less than 20. Use =IF(OR(C5<20,C5>70),"Extreme","Normal"). OR returns TRUE when any condition is met.
  test test_f5_uses_or (formula_uses, visible=True): {"cell":"F5","functions":["IF","OR"]} | on-fail: F5 must use both IF and OR. Use OR(C5<20,C5>70) as the logical_test: OR returns TRUE when any one of its conditions is TRUE.
  provenance: {"runtime":"hyperformula","runtime_version":"3.4.0","solution_sha256":"cc956c65595c48ba85b924789c089efc2422155b0035bf84d05febdb1d045359","tests_passed":6}
  feedback✔: Well done! Your nested IF correctly classifies all three delivery times using AND for the On Time band. AND returns TRUE only when BOTH conditions are met. Your OR formula in F5 correctly flags C5=19 as Extreme because OR returns TRUE when ANY condition is met (19 < 20 is TRUE).  feedback✘: For F2–F4: use =IF(C2>60,"Late",IF(AND(C2>=30,C2<=60),"On Time","Fast")). AND requires BOTH bounds to be true. For F5: use =IF(OR(C5<20,C5>70),"Extreme","Normal"). OR returns TRUE when ANY condition is true.  hints: ['Start with the outer IF: =IF(C2>60,"Late", ...). Then nest another IF for the middle band.', 'AND(C2>=30,C2<=60) returns TRUE only when C2 is at least 30 AND at most 60.']  remediation→r02
  MEASURES: B:construct_nested_if_for_multi_band_classification(f1,f2,f6); B:use_and_as_if_logical_test_for_multiple_conditions(f3); B:select_and_combine_if_and_or_for_given_decision_logic(f1,f3,f4,f5); B:use_or_as_if_logical_test_for_any_condition(f4)   anchors=['practice', 'assessment:construct_nested_if_for_multi_band_classification', 'assessment:use_and_as_if_logical_test_for_multiple_conditions', 'assessment:use_or_as_if_logical_test_for_any_condition', 'assessment:select_and_combine_if_and_or_for_given_decision_logic']
  taught-before-tested: B.f1←s06; B.f2←s06; B.f6←s06; B.f3←s08; B.f1←s06; B.f3←s08; B.f4←s08; B.f5←s06; B.f4←s08

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

# EVALUATOR PACKET — Writing Formulas and Reference Types (tile_spreadsheet_formula_syntax_refs)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = spreadsheet.formula_syntax — Basic formula syntax and arithmetic operators
B = spreadsheet.relative_absolute_references — Relative vs absolute references ($ notation)

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: tile_spreadsheet_formula_syntax_refs.s05: remediation tile_spreadsheet_formula_syntax_refs.r01 re-teaches ['spreadsheet.formula_syntax#f1'] but the check measures ['spreadsheet.formula_syntax#f3'] — a learner who fails it is sent to an unrelated fact
  warn: remediation step tile_spreadsheet_formula_syntax_refs.r02 is never referenced

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
(syntax) Built-in functions follow the same = prefix but add a name and parentheses: =SUM(D2:D21) totals every amount in that range of your Orders sheet. Type =, the function name, an opening parenthesis, select the range, close the parenthesis, then press Enter. The cell shows the computed result. ⟦A.f3 A:tb4⟧
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_spreadsheet_formula_syntax_refs.s01.b4","asset_ref":{"asset_id":"asset_orders_clean"},"range":"A1:E4","sheet_name":"Orders","show_formula_bar":true,"cells":[{"ref":"F2","formula":"=D3-D2","note":"Difference between two amounts"},{"ref":"F3","formula":"=SUM(D2:D21)","note":"Total of all amounts"}],"annotations":[{"target":"F2","text":"= prefix + cell refs + operator"},{"target":"F3","text":"= prefix + function name + range"}],"lineage":{"concept_ids":["spreadsheet.formula_syntax"],"fact_ids":["spreadsheet.formula_syntax#f1","spreadsheet.formula_syntax#f2","spreadsheet.formula_syntax#f3","spreadsheet.formula_syntax#f4"],"teaching_block_ids":["spreadsheet.formula_syntax#tb2","spreadsheet.formula_syntax#tb3","spreadsheet.formula_syntax#tb4"],"anchors":["spreadsheet.formula_syntax#visual"]},"computed_values":{"F2":2700,"F3":99100}}

### s02 · video · Formulas in Action
Formula Syntax — 
[VIDEO Entering formulas: the equal sign, arithmetic operators, and function calls] bridge-before: Watch how = signals a formula and how each operator or function name follows it directly. The first clip uses plain numbers; the second shows a range argument inside parentheses. | bridge-after: These clips cover f1–f3 but leave out cell-to-cell formulas (f4) and operator precedence (f5); the teaching text covers both fully.
  - gvhsKtjAmgc 311-418s facts=['f1', 'f2'] label: Formulas always start with =, and the four core arithmetic operators | summary: The presenter distinguishes a formula (any expression starting with =) from a function (a built-in tool that can appear inside a formula). Omitting the = sign causes Excel to treat the entry as text rather than a calculation. The arithmetic operators are then demonstrated one by one: + for addition, - for subtraction, * for multiplication, and / for division, each with a concrete numeric example that shows the result Excel returns.
  - XRPyj7cKVsQ 151-220s facts=['f1', 'f3'] label: Starting a formula with = and calling a built-in function over a selected range | summary: The presenter types = in a cell to begin a formula, then types a function name (MAX), presses Tab to accept it, and drags to select a range of cells as the argument. The closing parenthesis is added and Enter is pressed to confirm. The same steps are repeated with MIN on the same range, showing how the function-call pattern — equal sign, name, opening parenthesis, range, closing parenthesis, Enter — applies to any built-in function.

### s03 · explainer · Operator Precedence and Parentheses  [reward 3]
Formula Syntax — Multiplication runs before addition — unless you use parentheses.
(mechanism) Excel evaluates multiplication and division before addition and subtraction. =5+2*3 gives 11, not 21. Wrap the addition in parentheses — =(5+2)*3 — to get 21. Whenever a formula mixes operators, check the order or add parentheses to be explicit. ⟦A.f5 A:tb5⟧

### s04 · check · The Required Formula Prefix  [reward 5]
Quick Check — Which character must every Excel formula begin with?
QUESTION [choice, intro, grading=client] You type the following into cell D4 of the Orders sheet: D2+D3

What happens when you press Enter?
  ✔ opt_a: Excel treats it as text and displays the string "D2+D3" in the cell.
  ✘ opt_b: Excel adds the values in D2 and D3 and shows the numeric result.
      why: Without a leading = Excel does not evaluate the entry as a formula. It stores the literal text "D2+D3" instead of computing a sum.
  ✘ opt_c: Excel shows a #NAME? error because the cell addresses are invalid.
      why: #NAME? appears when Excel cannot recognise a name inside a formula. Here there is no formula at all — the entry has no = prefix, so Excel stores it as plain text.
  ✘ opt_d: Excel shows a #VALUE! error because + requires numbers.
      why: #VALUE! occurs when a formula receives the wrong type of argument. But without a leading = there is no formula to evaluate, so no error is raised — the entry is stored as text.
  feedback✔: Correct! Without the = prefix Excel treats the entry as plain text and displays "D2+D3" literally. Every formula must start with = to tell Excel to compute a value.  feedback✘: Formulas in Excel always begin with the equal sign (=). Without it, Excel treats the entry as plain text and displays it as-is, not as a computed result.  hints: ['Think about what tells Excel that an entry is a formula rather than a label.', "Try typing just the letter A in a cell — Excel shows 'A', not an error."]  remediation→r01
  MEASURES: A:identify_required_equal_sign_prefix(f1)   anchors=['assessment:identify_required_equal_sign_prefix']
  taught-before-tested: A.f1←s01

### s05 · check · Writing a Function Formula  [reward 5]
Quick Check — Which formula correctly sums the range C2:C21 on the Orders sheet?
QUESTION [choice, core, grading=client] Which formula correctly sums the range D2:D21 on the Orders sheet?

The Orders sheet has 20 rows of data in rows 2–21. You want to add up all the values in the amount column (D2:D21) using the SUM function. Which formula is correctly structured?
  ✔ opt_a: =SUM(D2:D21)
  ✘ opt_b: SUM(D2:D21)
      why: This is missing the = prefix. Without it, Excel stores the entry as text rather than evaluating the SUM function.
  ✘ opt_c: =SUM D2:D21
      why: The parentheses are required. The correct syntax is =SUM(range) — the opening parenthesis immediately follows the function name, and the range goes inside.
  ✘ opt_d: =SUM(D2,D21)
      why: =SUM(D2,D21) adds only two individual cells: D2 and D21. To sum a continuous range of cells, use the colon notation: D2:D21.
  feedback✔: Correct! =SUM(D2:D21) follows the required structure: = prefix, function name, opening parenthesis, the range D2:D21, closing parenthesis. This sums all 20 amount values.  feedback✘: A function formula needs: = prefix, the function name, an opening parenthesis, the range argument, and a closing parenthesis — for example =SUM(D2:D21).  hints: ['Every formula starts with =. Then comes the function name, then the range inside parentheses.', "D2:D21 uses a colon to mean 'from D2 to D21'. A comma would list only two separate cells."]  remediation→r01
  MEASURES: A:construct_function_call_formula_with_range(f3)   anchors=['assessment:construct_function_call_formula_with_range']
  taught-before-tested: A.f3←s01

### s06 · hands_on · Write Formulas on the Orders Sheet  [reward 10]
Practice — Apply arithmetic operators, cell references, and a function call to the QuickDeliver data.
QUESTION [code_exercise, core, grading=client] The **orders** sheet has order amounts in column D (rows 2–21). Row 2 (LG-2001) has amount **4500** and row 3 (LG-2002) has amount **7200**.

**Task 1 — subtraction:** In cell E1, write a formula that subtracts the amount in D2 from the amount in D3 (D3 minus D2). The result should be **2700**.

**Task 2 — operator precedence:** In cell E2, write a formula that first adds D2 and D3, then multiplies the sum by 2. Use parentheses to force the addition before the multiplication. The result should be **23400**.
  runtime={'kind': 'spreadsheet', 'version': '3.4.0'} constraints.allowed=['+ - * /', 'parentheses', 'relative cell references', 'numbers'] blocked=3 items
  file book.sheet [editable]:
// The orders sheet has order amounts in column D.
// D2 = 4500 (LG-2001), D3 = 7200 (LG-2002)

// Task 1: In E1, write a formula that computes D3 minus D2.
// Expected result: 2700

// Task 2: In E2, write a formula that adds D2 and D3, then multiplies by 2.
// Use parentheses so the addition happens before the multiplication.
// Expected result: 23400

  SOLUTION book.sheet:
E1: =D3-D2
E2: =(D2+D3)*2

  test test_subtraction_result (cell_equals, visible=True): {"cell":"E1","expected":2700.0} | on-fail: E1 should equal 2700 (D3 minus D2 = 7200 - 4500). Make sure your formula starts with = and uses the - operator between D3 and D2.
  test test_precedence_result (cell_equals, visible=True): {"cell":"E2","expected":23400.0} | on-fail: E2 should equal 23400 ((D2+D3)*2 = (4500+7200)*2 = 11700*2). Without parentheses, =D2+D3*2 gives 18600 because * is evaluated before +. Wrap the addition in parentheses: =(D2+D3)*2.
  provenance: {"runtime":"hyperformula","runtime_version":"3.4.0","solution_sha256":"f1fec9a91f28bf81d25414f8bb8f0fede0213b7abba1f7007441fc47e250d276","tests_passed":2}
  feedback✔: Well done! E1 uses = and the - operator to subtract D2 from D3, returning 2700. E2 uses parentheses to force the addition (D2+D3) before the multiplication by 2, returning 23400. Without parentheses, =D2+D3*2 would give 18600 because * has higher precedence than +.  feedback✘: Check both cells. E1 needs =D3-D2 (the = prefix, then D3, then -, then D2). E2 needs parentheses around the addition: =(D2+D3)*2. Without parentheses, multiplication happens before addition and the result is wrong.  hints: ['Every formula must start with =. Without it, Excel stores the entry as text.', 'Parentheses change the order of operations: =(D2+D3)*2 adds first, then multiplies.']  remediation→r01
  MEASURES: A:apply_arithmetic_operators_in_formula(f2); A:build_cell_reference_formula_with_operator(f4); A:apply_operator_precedence_and_parentheses(f5); A:write_syntactically_correct_formula_for_given_computation(f1,f2,f3,f4,f5)   anchors=['practice', 'assessment:apply_arithmetic_operators_in_formula', 'assessment:build_cell_reference_formula_with_operator', 'assessment:apply_operator_precedence_and_parentheses', 'assessment:write_syntactically_correct_formula_for_given_computation']
  taught-before-tested: A.f2←s01; A.f4←s01; A.f5←s03; A.f1←s01; A.f2←s01; A.f3←s01; A.f4←s01; A.f5←s03

### s07 · explainer · Relative and Absolute References  [reward 5]
Reference Types — Copy a formula down a column and watch which parts shift — and which stay fixed.
(definition) A relative reference such as D2 is position-based: copy the formula one row down and D2 becomes D3 automatically. By default, every new formula uses relative references. This is what you want when each row should calculate against its own data. ⟦B.f1 B:tb1 B:tb2⟧
(mechanism) An absolute reference such as $H$1 always points to the same cell, no matter where you copy the formula. Dollar signs lock both the column letter and the row number. If a delivery fee rate lives in H1, =D2*$H$1 copied down every order row keeps pointing to H1 for the rate while D2 shifts to D3, D4, and so on. ⟦B.f2 B:tb3⟧
[BEFORE_AFTER] After copying H2 down to H3 and H4, the relative part (D2→D3→D4) adjusts while the absolute part ($H$1) stays fixed.
  before:
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_spreadsheet_formula_syntax_refs.s07.b3.before","asset_ref":{"asset_id":"asset_orders_clean"},"range":"D2:H5","sheet_name":"Orders","show_formula_bar":true,"cells":[{"ref":"H2","formula":"=D2*$H$1","note":"Original formula in row 2"}],"annotations":[{"target":"H2","text":"=D2*$H$1 — D2 is relative, $H$1 is absolute"}],"computed_values":{"H2":0}}
  after:
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_spreadsheet_formula_syntax_refs.s07.b3.after","asset_ref":{"asset_id":"asset_orders_clean"},"range":"D2:H5","sheet_name":"Orders","show_formula_bar":true,"cells":[{"ref":"H2","formula":"=D2*$H$1"},{"ref":"H3","formula":"=D3*$H$1"},{"ref":"H4","formula":"=D4*$H$1"}],"annotations":[{"target":"H3","text":"D3 shifted; $H$1 unchanged"}],"computed_values":{"H2":0,"H3":0,"H4":0}}

### s08 · video · Watching References Shift (or Stay Fixed)
Reference Types — 
[VIDEO Reference lock in action: watching a cell address shift — or stay fixed — as a formula is copied] bridge-before: Watch how the address in the formula bar changes — or doesn't — each time the formula is pasted to a new cell. The clip uses 'lock' as a synonym for absolute reference. | bridge-after: The clip covers all three reference types. Devspace's text adds the tax-rate column example and clarifies that relative referencing is the spreadsheet default.
  - 4MVNjzsGokc 31-338s facts=['f1', 'f2', 'f3'] label: Relative, absolute, and mixed references demonstrated by copying formulas across a sheet | summary: The instructor starts with a simple formula that multiplies a value by 2, then copies it to show how the cell address shifts automatically to match the new position — this is relative referencing. Next, dollar signs are added before both the column letter and row number to lock the address completely, so the formula always points to the same cell no matter where it is pasted — absolute referencing. A clinic appointment tracker then reinforces relative references by copying a set of formulas across a full week of data with no manual edits. Finally, a sales-bonus grid introduces mixed referencing: the column is locked with a dollar sign so the formula always reads from the sales-amount column, while the row is locked separately so it always reads from the chosen bonus-rate row, letting a single formula fill every combination in the grid correctly.

### s09 · explainer · Mixed References: Lock One Dimension  [reward 3]
Reference Types — Lock just the column or just the row — not both.
(mechanism) A mixed reference locks only one dimension. $A1 locks the column (A stays, row shifts); A$1 locks the row (1 stays, column shifts). Use a mixed reference when copying a formula across both rows and columns and only one axis should stay fixed. ⟦B.f3 B:tb4⟧

### s10 · check · Constructing a Mixed Reference  [reward 5]
Quick Check — Which reference locks the column but lets the row shift when copied down?
QUESTION [choice, core, grading=client] You are building a multiplication table. Row 1 holds the column multipliers (B1, C1, D1, …) and column A holds the row multipliers (A2, A3, A4, …). You want to enter one formula in B2 and copy it across the entire table so that it always multiplies the correct row multiplier by the correct column multiplier.

Which formula should you enter in B2?
  ✔ opt_a: =$A2*B$1
  ✘ opt_b: =$A$2*$B$1
      why: $A$2 locks both the column and the row of the row multiplier. When you copy the formula down, the row part ($2) never changes, so every row in the table uses A2 instead of A3, A4, etc.
  ✘ opt_c: =A2*B1
      why: =A2*B1 uses fully relative references. When copied across columns, A2 shifts to B2, C2, etc., so the formula no longer reads from column A. When copied down, B1 shifts to B2, B3, etc., losing the header row.
  ✘ opt_d: =$A$2*B1
      why: $A$2 locks both dimensions of the row multiplier, so copying down always reads A2 instead of A3, A4, etc. You need $A2 (lock column A, let the row adjust) to keep the row multiplier in column A while allowing the row to change.
  feedback✔: Correct! =$A2*B$1 uses two mixed references. $A2 locks column A so the row multiplier always comes from column A, while the row number adjusts as you copy down. B$1 locks row 1 so the column multiplier always comes from row 1, while the column letter adjusts as you copy across.  feedback✘: A mixed reference locks one dimension and lets the other adjust. $A2 locks the column (A stays fixed) but lets the row change when copied down. B$1 locks the row (1 stays fixed) but lets the column change when copied across. Together, =$A2*B$1 fills the entire multiplication table correctly from one formula.  hints: ['The $ sign locks the part that follows it: $A locks the column, $1 locks the row.', 'Ask yourself: when I copy this formula down, which part must NOT change? When I copy across, which part must NOT change?']  remediation→r03
  MEASURES: B:construct_mixed_reference_locking_one_dimension(f3)   anchors=['assessment:construct_mixed_reference_locking_one_dimension']
  taught-before-tested: B.f3←s09

### s11 · hands_on · Apply Reference Types to the Orders Sheet  [reward 10]
Practice — Choose the right reference type for each copy scenario.
QUESTION [code_exercise, stretch, grading=client] The **orders** sheet has order amounts in column D (rows 2–4). Cell H1 holds the tax rate **0.075** (7.5%).

**Task:** In cells E2, E3, and E4, write a formula that multiplies each row's amount (D2, D3, D4) by the shared tax rate in H1. Use an **absolute reference** for H1 so the tax-rate address does not change when the formula is copied down. Use a **relative reference** for the amount cell so it adjusts to the correct row.

- E2 should equal **337.5** (4500 × 0.075)
- E3 should equal **540** (7200 × 0.075)
- E4 should equal **232.5** (3100 × 0.075)
  runtime={'kind': 'spreadsheet', 'version': '3.4.0'} constraints.allowed=['+ - * /', 'relative cell references', 'absolute references ($A$1)'] blocked=3 items
  file book.sheet [editable]:
// H1 holds the shared tax rate.
H1: 0.075

// Task: In E2, write a formula that multiplies D2 by the tax rate in H1.
// Use $H$1 (absolute) for the tax rate so it does not shift when copied.
// Use D2 (relative) for the amount so it adjusts to D3, D4 when copied down.
// Then write the same pattern in E3 and E4.

  SOLUTION book.sheet:
H1: 0.075
E2: =D2*$H$1
E3: =D3*$H$1
E4: =D4*$H$1

  test test_e2_tax (cell_equals, visible=True): {"cell":"E2","expected":337.5,"tolerance":0.01} | on-fail: E2 should equal 337.5 (D2 × H1 = 4500 × 0.075). Use =D2*$H$1 — the $ signs lock H1 so it does not shift when copied.
  test test_e3_tax (cell_equals, visible=True): {"cell":"E3","expected":540.0,"tolerance":0.01} | on-fail: E3 should equal 540 (D3 × H1 = 7200 × 0.075). If you copied =D2*$H$1 down, D2 should have adjusted to D3 while $H$1 stayed fixed.
  test test_e4_tax (cell_equals, visible=True): {"cell":"E4","expected":232.5,"tolerance":0.01} | on-fail: E4 should equal 232.5 (D4 × H1 = 3100 × 0.075). Check that E4 uses D4 (relative, adjusts per row) and $H$1 (absolute, stays fixed).
  provenance: {"runtime":"hyperformula","runtime_version":"3.4.0","solution_sha256":"3c35c42eeaa6090ba5d5380f71c67267c797e06c02ee4f44fafaa223c0d8588a","tests_passed":3}
  feedback✔: Excellent! =D2*$H$1 uses a relative reference for D2 (it adjusts to D3, D4 as you copy down) and an absolute reference for $H$1 (the $ signs lock both the column H and row 1, so the tax-rate cell never shifts). This is the key pattern for applying a shared rate to a column of values.  feedback✘: Use =D2*$H$1 in E2. The $ signs in $H$1 lock the tax-rate cell so it does not shift when the formula is copied. D2 has no $ signs, so it adjusts to D3 in E3 and D4 in E4. If you used =D2*H1 (no $), H1 would shift to H2, H3, etc. when copied down.  hints: ['Add $ before both the column letter and the row number of H1 to lock it: $H$1.', 'Leave D2 without $ signs so it automatically becomes D3 when you copy the formula to E3.']  remediation→r03
  MEASURES: B:identify_relative_reference_adjustment_on_copy(f1); B:apply_absolute_reference_to_fix_cell_on_copy(f2); B:select_correct_reference_type_for_copy_scenario(f1,f2,f3)   anchors=['practice', 'assessment:identify_relative_reference_adjustment_on_copy', 'assessment:apply_absolute_reference_to_fix_cell_on_copy', 'assessment:select_correct_reference_type_for_copy_scenario']
  taught-before-tested: B.f1←s07; B.f2←s07; B.f1←s07; B.f2←s07; B.f3←s09

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

# EVALUATOR PACKET — Text, Date, and Conditional Aggregation (tile_spreadsheet_text_date_conditional_agg)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = spreadsheet.text_combining — Text combining
B = spreadsheet.text_extraction — Text extraction
C = spreadsheet.date_functions — Date functions and date arithmetic (TODAY, DATEDIF)
D = spreadsheet.conditional_aggregation — Conditional aggregation (COUNTIF/COUNTIFS, SUMIF/SUMIFS)

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: plan: tile_spreadsheet_text_date_conditional_agg.s05 was planned to measure spreadsheet.text_extraction#assessment:apply_trim_to_remove_extraneous_whitespace but its interaction does not
  warn: plan: tile_spreadsheet_text_date_conditional_agg.s07 was planned to measure spreadsheet.text_extraction#assessment:apply_right_to_extract_trailing_characters but its interaction does not

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
(syntax) CONCATENATE joins two or more text strings into one: CONCATENATE(text1, text2, ...). Microsoft recommends using the newer CONCAT function instead, as CONCATENATE may not be available in future versions of Excel. CONCATENATE does not add a separator automatically — include it as a literal argument. TEXTJOIN uses its delimiter argument to insert one for you. ⟦A.f3 A:tb2⟧
[BEFORE_AFTER] TEXTJOIN(", ", TRUE, B2, E2) combines the city and status columns with a comma-space delimiter; setting ignore_empty to TRUE means a blank status cell produces no trailing comma.
  before:
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_spreadsheet_text_date_conditional_agg.s01.b3.before","asset_ref":{"asset_id":"asset_orders_clean"},"range":"B1:E4","sheet_name":"Orders","show_formula_bar":true,"annotations":[{"target":"B1","text":"city — separate column"},{"target":"E1","text":"status — separate column"}]}
  after:
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_spreadsheet_text_date_conditional_agg.s01.b3.after","asset_ref":{"asset_id":"asset_orders_clean"},"range":"B1:G4","sheet_name":"Orders","show_formula_bar":true,"cells":[{"ref":"G2","formula":"=TEXTJOIN(\", \",TRUE,B2,E2)","note":"Combines city and status with delimiter"},{"ref":"G3","formula":"=TEXTJOIN(\", \",TRUE,B3,E3)"}],"annotations":[{"target":"G1","text":"Full_Name — combined with TEXTJOIN"},{"target":"G2","text":"=TEXTJOIN(\", \",TRUE,B2,E2)"}],"computed_values":{"G2":"#NAME?","G3":"#NAME?"}}

### s02 · check · CONCATENATE Syntax and Deprecation  [reward 5]
Quick Check — What is the syntax of CONCATENATE, and why does Microsoft recommend using CONCAT instead?
QUESTION [choice, intro, grading=client] A colleague shares a workbook that uses =CONCATENATE(A2," ",B2) to join a first name and a last name. Which statement about CONCATENATE is accurate?
  ✔ opt_a: CONCATENATE works but Microsoft recommends using CONCAT instead, as CONCATENATE may not be available in future versions of Excel.
  ✘ opt_b: CONCATENATE is the current recommended function and CONCAT is the deprecated one.
      why: This is reversed. Microsoft recommends the newer CONCAT function and notes that CONCATENATE may not be available in future versions of Excel.
  ✘ opt_c: CONCATENATE automatically skips empty cells, so no ignore_empty argument is needed.
      why: CONCATENATE does not skip empty cells — it joins them as blank values, which can produce unwanted extra spaces. TEXTJOIN with ignore_empty=TRUE is the function that skips empty cells.
  ✘ opt_d: CONCATENATE can only join two text strings at a time.
      why: CONCATENATE accepts multiple text arguments: CONCATENATE(text1, [text2], ...). It can join more than two strings in a single formula.
  feedback✔: Correct! CONCATENATE joins text strings and its syntax is CONCATENATE(text1, [text2], ...). However, Microsoft recommends using the newer CONCAT function instead, since CONCATENATE may not be available in future versions of Excel.  feedback✘: CONCATENATE joins two or more text strings. Microsoft recommends using CONCAT instead, as CONCATENATE may not be available in future versions of Excel. Neither function automatically skips empty cells — use TEXTJOIN with ignore_empty=TRUE for that.  hints: ['Think about which function Microsoft says is the newer, recommended replacement.', 'TEXTJOIN is the function with the ignore_empty argument, not CONCATENATE.']
  MEASURES: A:identify_concatenate_syntax_and_deprecation_caveat(f3)   anchors=['assessment:identify_concatenate_syntax_and_deprecation_caveat']
  taught-before-tested: A.f3←s01

### s03 · hands_on · Combine Text Columns on the Orders Sheet  [reward 10]
Practice — Use TEXTJOIN to merge city and status into a single label.
QUESTION [formula_entry, core, grading=client] The Orders sheet has the delivery city in column B and the order status in column E. Row 2 has city **"Lagos"** and status **"Delivered"**.

In cell H2, write a TEXTJOIN formula that combines the city (B2) and status (E2) with the delimiter **" | "** (space-pipe-space) and sets ignore_empty to **TRUE**.

The expected result is **"Lagos | Delivered"**.
  [unrendered interaction type formula_entry] public={"prompt":"The Orders sheet has the delivery city in column B and the order status in column E. Row 2 has city **\"Lagos\"** and status **\"Delivered\"**.\n\nIn cell H2, write a TEXTJOIN formula that combines the city (B2) and status (E2) with the delimiter **\" | \"** (space-pipe-space) and sets ignore_empty to **TRUE**.\n\nThe expected result is **\"Lagos | Delivered\"**.","asset_ref":{"asset_id":"asset_orders_clean","variant_id":null},"target_cell":"H2","allowed_functions":["TEXTJOIN"],"sheet_name":"orders"} grading={"expected_value":"Lagos | Delivered","reference_formula":"=TEXTJOIN(\" | \",1,B2,E2)","must_use_functions":["TEXTJOIN"],"forbid_hardcoded_values":true}
  feedback✔: Correct! =TEXTJOIN(" | ",1 (or TRUE()),B2,E2) joins B2 ("Lagos") and E2 ("Delivered") with the delimiter " | ", returning "Lagos | Delivered". Setting ignore_empty to 1 (or TRUE()) means any blank cells in the argument list are skipped rather than producing an extra delimiter.  feedback✘: Use =TEXTJOIN(" | ",1 (or TRUE()),B2,E2). The first argument is the delimiter (" | "), the second is ignore_empty (1 (or TRUE())), and the remaining arguments are the cells to join (B2 and E2). Make sure the delimiter is in double quotes.  hints: ['TEXTJOIN syntax: TEXTJOIN(delimiter, ignore_empty, text1, [text2], ...)', 'The delimiter " | " includes spaces on both sides of the pipe character.']  remediation→r01
  MEASURES: A:build_combined_string_from_cells_with_delimiter(f1); A:apply_textjoin_with_ignore_empty(f1,f2)   anchors=['practice', 'assessment:build_combined_string_from_cells_with_delimiter', 'assessment:apply_textjoin_with_ignore_empty']
  taught-before-tested: A.f1←s01; A.f1←s01; A.f2←s01

### s04 · explainer · Extracting Text with LEFT, RIGHT, MID, and TRIM  [reward 5]
Text Functions — Pull specific characters out of a string — or strip unwanted spaces.
(syntax) LEFT returns the first N characters of a string: LEFT(text, num_chars). RIGHT returns the last N characters: RIGHT(text, num_chars). On order IDs like "LG-2001", =LEFT(A2,2) returns "LG" and =RIGHT(A2,4) returns "2001". ⟦B.f1 B.f2 B:tb1⟧
(syntax) MID returns characters from any position: MID(text, start_num, num_chars). =MID(A2,4,4) on "LG-2001" starts at position 4 and takes 4 characters, returning "2001". TRIM removes all extra spaces — leading, trailing, and multiple spaces between words — leaving only single spaces between words: TRIM(text). If a city was imported as " Lagos ", =TRIM(B2) returns "Lagos". ⟦B.f3 B.f4 B:tb2 B:tb3⟧
[BEFORE_AFTER] LEFT extracts the two-character prefix from the order ID; TRIM removes the stray spaces from the city name.
  before:
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_spreadsheet_text_date_conditional_agg.s04.b3.before","asset_ref":{"asset_id":"asset_orders_clean"},"range":"A1:B4","sheet_name":"Orders","show_formula_bar":true,"cells":[{"ref":"A2","note":"LG-2001 — raw order ID"},{"ref":"B2","note":" Lagos  — imported with spaces"}],"annotations":[{"target":"A2","text":"Raw: LG-2001"},{"target":"B2","text":"Raw: \" Lagos \""}]}
  after:
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_spreadsheet_text_date_conditional_agg.s04.b3.after","asset_ref":{"asset_id":"asset_orders_clean"},"range":"A1:D4","sheet_name":"Orders","show_formula_bar":true,"cells":[{"ref":"C2","formula":"=LEFT(A2,2)","note":"Returns LG"},{"ref":"D2","formula":"=TRIM(B2)","note":"Returns Lagos"}],"annotations":[{"target":"C2","text":"=LEFT(A2,2) → \"LG\""},{"target":"D2","text":"=TRIM(B2) → \"Lagos\""}],"computed_values":{"C2":"LG","D2":"Lagos"}}

### s05 · check · MID and TRIM  [reward 5]
Quick Check — Which formula extracts 4 characters starting at position 4 from cell A2?
QUESTION [choice, core, grading=client] Cell A2 contains the order ID **"LG-2001"**. You want to extract the 4-digit number starting at position 4 (the "2001" part).

Which formula correctly extracts exactly 4 characters starting at position 4?
  ✔ opt_a: =MID(A2,4,4)
  ✘ opt_b: =MID(A2,4,3)
      why: =MID(A2,4,3) starts at position 4 but extracts only 3 characters, returning "200" instead of "2001". The third argument of MID is the number of characters to extract.
  ✘ opt_c: =LEFT(A2,4)
      why: =LEFT(A2,4) extracts the first 4 characters from the left, returning "LG-2" instead of "2001". LEFT always starts from the beginning of the string.
  ✘ opt_d: =MID(A2,3,4)
      why: =MID(A2,3,4) starts at position 3, which is the "-" character in "LG-2001". This returns "-200" instead of "2001". The start position must be 4 to begin at the "2" character.
  feedback✔: Correct! =MID(A2,4,4) starts at position 4 (the "2" in "2001") and extracts 4 characters, returning "2001". MID syntax: MID(text, start_num, num_chars).  feedback✘: MID(text, start_num, num_chars) extracts num_chars characters starting at start_num. In "LG-2001": position 1=L, 2=G, 3=-, 4=2, 5=0, 6=0, 7=1. To get "2001", start at position 4 and extract 4 characters: =MID(A2,4,4).  hints: ['Count the characters in "LG-2001": L=1, G=2, -=3, 2=4, 0=5, 0=6, 1=7.', "MID's third argument is how many characters to return, not the end position."]  remediation→r02
  MEASURES: B:apply_mid_to_extract_characters_by_position(f3)   anchors=['assessment:apply_mid_to_extract_characters_by_position']
  taught-before-tested: B.f3←s04

### s06 · check · Choosing the Right Extraction Function  [reward 5]
Quick Check — Which function should you use for each text extraction task?
QUESTION [choice, core, grading=client] A city name imported from an external system is stored in cell B2 as **"  Lagos  "** (with two leading spaces and two trailing spaces). You want to clean it so it reads **"Lagos"** with no extra spaces.

Which function should you use?
  ✔ opt_a: =TRIM(B2)
  ✘ opt_b: =LEFT(B2,5)
      why: =LEFT(B2,5) extracts the first 5 characters from the left. Because the string starts with two spaces, LEFT(B2,5) returns "  Lag" — the spaces are included and the full city name is cut off.
  ✘ opt_c: =MID(B2,3,5)
      why: =MID(B2,3,5) starts at position 3 (the first non-space character) and extracts 5 characters, returning "Lagos". This works for this specific string, but it relies on knowing exactly how many leading spaces there are. TRIM is the robust solution because it removes all leading and trailing spaces regardless of count.
  ✘ opt_d: =RIGHT(B2,5)
      why: =RIGHT(B2,5) extracts the last 5 characters. Because the string ends with two spaces, RIGHT(B2,5) returns "gos  " — the trailing spaces are included.
  feedback✔: Correct! =TRIM(B2) removes all leading and trailing spaces from the text, returning "Lagos". TRIM also collapses multiple spaces between words to a single space, making it the standard tool for cleaning imported text.  feedback✘: TRIM removes all spaces from a text value except for single spaces between words. It is the right tool when you need to clean leading or trailing spaces from imported data. LEFT, RIGHT, and MID extract characters by position — they do not remove spaces.  hints: ['TRIM is designed specifically to remove leading and trailing spaces from text.', 'LEFT and RIGHT extract characters from the start or end — they include any spaces that are there.']  remediation→r02
  MEASURES: B:select_correct_extraction_function_for_given_text_task(f1,f2,f3,f4); B:apply_trim_to_remove_extraneous_whitespace(f4); B:apply_right_to_extract_trailing_characters(f2)   anchors=['assessment:select_correct_extraction_function_for_given_text_task', 'assessment:apply_trim_to_remove_extraneous_whitespace', 'assessment:apply_right_to_extract_trailing_characters']
  taught-before-tested: B.f1←s04; B.f2←s04; B.f3←s04; B.f4←s04; B.f4←s04; B.f2←s04

### s07 · hands_on · Extract Characters from Order IDs  [reward 10]
Practice — Use LEFT and RIGHT to pull the prefix and numeric suffix from the order_id column.
QUESTION [formula_entry, core, grading=client] The Orders sheet has order IDs in column A (e.g., **"LG-2001"**). Each order ID has a 2-letter prefix ("LG") followed by a hyphen and a 4-digit number.

In cell G2, write a formula using **LEFT** that extracts the first 2 characters of the order ID in A2 — the 2-letter prefix.

The expected result is **"LG"**.
  [unrendered interaction type formula_entry] public={"prompt":"The Orders sheet has order IDs in column A (e.g., **\"LG-2001\"**). Each order ID has a 2-letter prefix (\"LG\") followed by a hyphen and a 4-digit number.\n\nIn cell G2, write a formula using **LEFT** that extracts the first 2 characters of the order ID in A2 — the 2-letter prefix.\n\nThe expected result is **\"LG\"**.","asset_ref":{"asset_id":"asset_orders_clean","variant_id":null},"target_cell":"G2","allowed_functions":["LEFT"],"sheet_name":"orders"} grading={"expected_value":"LG","reference_formula":"=LEFT(A2,2)","must_use_functions":["LEFT"],"forbid_hardcoded_values":true}
  feedback✔: Correct! =LEFT(A2,2) extracts the first 2 characters of "LG-2001", returning "LG". LEFT(text, num_chars) always counts from the beginning of the string.  feedback✘: Use =LEFT(A2,2). LEFT(text, num_chars) returns the first num_chars characters. "LG-2001" starts with "LG" — the first 2 characters.  hints: ['LEFT(text, num_chars) extracts characters from the left end of the string.', '"LG-2001" has 7 characters. The first 2 characters are "LG".']
  MEASURES: B:apply_left_to_extract_leading_characters(f1)   anchors=['practice', 'assessment:apply_left_to_extract_leading_characters']
  taught-before-tested: B.f1←s04

### s08 · explainer · TODAY, DATEDIF, and the Date Serial Number  [reward 5]
Date Functions — Excel stores dates as numbers — which makes date arithmetic straightforward.
(mechanism) Excel stores every date as a sequential serial number: January 1, 1900 is 1, and each subsequent day adds 1. That is why date functions can do arithmetic on dates the same way ordinary functions do on numbers — a date cell is just a number displayed in a date format. ⟦C.f4 C:tb1⟧
(syntax) TODAY() returns the serial number of the current date and takes no arguments. DATEDIF(start_date, end_date, unit) returns the difference between two dates in the unit you specify: "Y" for complete years, "D" for days. DATEDIF is useful for age calculations: DATEDIF(birthdate, TODAY(), "Y") returns the number of complete years between the birthdate and today. ⟦C.f1 C.f2 C.f3 C.f5 C:tb2 C:tb3⟧
(example) On your Orders sheet, with an order date in G2, =DATEDIF(G2,TODAY(),"D") tells you how many days have passed since that order was placed. TODAY() supplies the end date automatically, so the result updates each day the workbook is opened. ⟦C.f1 C.f2 C:tb4⟧
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_spreadsheet_text_date_conditional_agg.s08.b4","asset_ref":{"asset_id":"asset_orders_clean"},"range":"G1:H4","sheet_name":"Orders","show_formula_bar":true,"cells":[{"ref":"H2","formula":"=DATEDIF(G2,TODAY(),\"D\")","note":"Days since order placed"},{"ref":"H3","formula":"=DATEDIF(G3,TODAY(),\"D\")"}],"annotations":[{"target":"H2","text":"DATEDIF formula in formula bar"},{"target":"G2","text":"order_date (serial number)"}],"lineage":{"concept_ids":["spreadsheet.date_functions"],"fact_ids":["spreadsheet.date_functions#f1","spreadsheet.date_functions#f2","spreadsheet.date_functions#f3","spreadsheet.date_functions#f4","spreadsheet.date_functions#f5"],"teaching_block_ids":["spreadsheet.date_functions#tb1","spreadsheet.date_functions#tb2","spreadsheet.date_functions#tb3","spreadsheet.date_functions#tb4"],"anchors":["spreadsheet.date_functions#visual"]},"computed_values":{"H2":"#VALUE!","H3":"#VALUE!"}}

### s09 · check · Choosing the Right Date Function  [reward 5]
Quick Check — Which function returns the number of days between two dates?
QUESTION [choice, core, grading=client] Cell G2 holds an order date. You want a formula that calculates how many **days** have elapsed between the order date in G2 and today's date.

Which formula uses **DATEDIF** to calculate how many days have elapsed between the order date in G2 and today's date?
  ✔ opt_a: =DATEDIF(G2,TODAY(),"D")
  ✘ opt_b: =DATEDIF(TODAY(),G2,"D")
      why: DATEDIF(start_date, end_date, unit): the start_date must come before the end_date. Putting TODAY() as the start_date and G2 as the end_date reverses the order — if G2 is in the past, this returns a negative number or an error.
  ✘ opt_c: =DATEDIF(G2,TODAY(),"Y")
      why: The unit "Y" returns the number of complete years, not days. To count days, use the unit "D".
  ✘ opt_d: =TODAY()-G2
      why: =TODAY()-G2 does return the number of days as a serial-number difference, and it works. However, the question asks for DATEDIF, which is the explicit function for date-difference calculations and makes the intent clearer. =DATEDIF(G2,TODAY(),"D") is the correct DATEDIF form.
  feedback✔: Correct! =DATEDIF(G2,TODAY(),"D") computes the number of complete days between the order date (G2) and today. DATEDIF syntax: DATEDIF(start_date, end_date, unit). The unit "D" returns days; "Y" would return complete years.  feedback✘: DATEDIF(start_date, end_date, unit) requires the earlier date as start_date and the later date as end_date. TODAY() supplies today's date as the end_date. The unit "D" returns the number of days in the period.  hints: ['DATEDIF argument order: start_date first, end_date second. The order date (G2) is the start.', 'The unit controls what is counted: "D" = days, "Y" = complete years.']  remediation→r03
  MEASURES: C:select_correct_date_function_for_given_calculation_requirement(f1,f2,f5)   anchors=['assessment:select_correct_date_function_for_given_calculation_requirement']
  taught-before-tested: C.f1←s08; C.f2←s08; C.f5←s08

### s10 · hands_on · Calculate Days Since Each Order Was Placed  [reward 10]
Practice — Write a DATEDIF formula using TODAY() to find how many days have passed since each order date.
QUESTION [code_exercise, core, grading=client] The **orders** sheet has order dates in column G (rows 2–21). The starter file provides the order-date serial numbers for rows 2 and 3 in cells G2 and G3 (both are **45355**, representing 2024-03-04), and a fixed reference date in H1 (**45361**, representing 2024-03-10).

**Task 1 — days elapsed (fixed date):** In cell I2, write a DATEDIF formula that calculates the number of **days** (unit "D") between the order date in G2 and the reference date in H1. The result should be **6**.

**Task 2 — days for row 3:** In cell I3, write the same DATEDIF formula for G3. The result should also be **6**.

**Task 3 — age in years (TODAY):** In cell J2, write a formula using **DATEDIF** and **TODAY()** that calculates the number of complete **years** (unit "Y") between the order date in G2 and today's date. Use TODAY() as the end_date argument. Syntax: =DATEDIF(G2,TODAY(),"Y").
  runtime={'kind': 'spreadsheet', 'version': '3.4.0'} constraints.allowed=['DATEDIF(start_date, end_date, unit)', 'TODAY()', 'relative cell references', 'text in quotes'] blocked=2 items
  file book.sheet [editable]:
// H1 holds the reference date as a serial number (45361 = 2024-03-10).
H1: 45361
// G2 and G3 hold order-date serial numbers (45355 = 2024-03-04).
G2: 45355
G3: 45355

// Task 1: In I2, write a DATEDIF formula that returns the number of days
// between the order date in G2 and the reference date in H1.
// DATEDIF syntax: DATEDIF(start_date, end_date, unit)
// Use unit "D" for days. Expected result: 6

// Task 2: In I3, write the same DATEDIF formula for G3.
// Expected result: 6

  SOLUTION book.sheet:
H1: 45361
G2: 45355
G3: 45355
I2: =DATEDIF(G2,H1,"D")
I3: =DATEDIF(G3,H1,"D")
J2: =DATEDIF(G2,TODAY(),"Y")

  test test_i2_days (cell_equals, visible=True): {"cell":"I2","expected":6} | on-fail: I2 should equal 6 (days from 2024-03-04 to 2024-03-10). Use =DATEDIF(G2,H1,"D") — G2 is the start_date, H1 is the end_date, "D" counts days.
  test test_i3_days (cell_equals, visible=True): {"cell":"I3","expected":6} | on-fail: I3 should equal 6 (days from 2024-03-04 to 2024-03-10). Use =DATEDIF(G3,H1,"D") — same pattern as I2 but referencing G3.
  test test_i2_uses_datedif (formula_uses, visible=True): {"cell":"I2","functions":["DATEDIF"]} | on-fail: I2 must contain a DATEDIF formula.
  test test_j2_uses_today_datedif (formula_uses, visible=True): {"cell":"J2","functions":["DATEDIF","TODAY"]} | on-fail: J2 must contain a formula using both DATEDIF and TODAY(). Use =DATEDIF(G2,TODAY(),"Y") — TODAY() supplies the current date as the end_date, and "Y" returns complete years.
  provenance: {"runtime":"hyperformula","runtime_version":"3.4.0","solution_sha256":"824c67dac4fb4a0d61b8be1435fba94cc4dbc7891ba81fc718a33f84d4507585","tests_passed":4}
  feedback✔: Well done! =DATEDIF(G2,H1,"D") correctly places the earlier date (G2) as start_date and the later date (H1) as end_date, with unit "D" for days. =DATEDIF(G2,TODAY(),"Y") uses TODAY() as the end_date to compute the age in complete years — TODAY() returns today's date as a serial number, and "Y" counts complete years. Excel stores dates as serial numbers, so DATEDIF can subtract them to count days or years.  feedback✘: For Tasks 1 and 2: Use =DATEDIF(G2,H1,"D") and =DATEDIF(G3,H1,"D"). The argument order is: start_date (earlier date), end_date (later date), unit ("D" for days). For Task 3: Use =DATEDIF(G2,TODAY(),"Y") — TODAY() supplies today's date as the end_date, and "Y" returns the number of complete years.  hints: ['DATEDIF(start_date, end_date, unit): the earlier date goes first.', 'The unit "D" counts days. Use "Y" for complete years, "M" for complete months.']  remediation→r03
  MEASURES: C:write_datedif_with_correct_arguments_and_unit(f2); C:construct_age_calculation_formula_using_datedif_and_today(f2,f3); C:explain_date_serial_number_model(f4); C:select_correct_date_function_for_given_calculation_requirement(f1,f2,f5); C:write_today_function_with_correct_syntax(f1)   anchors=['practice', 'assessment:write_datedif_with_correct_arguments_and_unit', 'assessment:construct_age_calculation_formula_using_datedif_and_today', 'assessment:explain_date_serial_number_model', 'assessment:select_correct_date_function_for_given_calculation_requirement', 'assessment:write_today_function_with_correct_syntax']
  taught-before-tested: C.f2←s08; C.f2←s08; C.f3←s08; C.f4←s08; C.f1←s08; C.f2←s08; C.f5←s08; C.f1←s08

### s11 · explainer · COUNTIF and SUMIF: One Condition  [reward 5]
Conditional Aggregation — Count or sum only the rows that match a single criterion.
(intro) SUM, AVERAGE, COUNT, and COUNTA take every value in their range. When you only want rows that meet a condition — orders from Lagos, say — use COUNTIF or SUMIF instead. ⟦D.f1 D.f3 D:tb1⟧
(syntax) COUNTIF(range, criteria) counts the cells in range that match criteria. =COUNTIF(B2:B21,"Lagos") counts how many orders in the city column are from Lagos. SUMIF(range, criteria, sum_range) sums the values in sum_range for rows where range matches criteria. =SUMIF(B2:B21,"Lagos",D2:D21) totals the amounts for Lagos orders only. ⟦D.f1 D.f3 D:tb2⟧
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_spreadsheet_text_date_conditional_agg.s11.b3","asset_ref":{"asset_id":"asset_orders_clean"},"range":"A1:E6","sheet_name":"Orders","show_formula_bar":true,"cells":[{"ref":"G2","formula":"=COUNTIF(B2:B21,\"Lagos\")","note":"Count of Lagos orders"},{"ref":"G3","formula":"=SUMIF(B2:B21,\"Lagos\",D2:D21)","note":"Total amount for Lagos"}],"annotations":[{"target":"G2","text":"COUNTIF — criteria range + criterion"},{"target":"G3","text":"SUMIF — criteria range + criterion + sum range"}],"lineage":{"concept_ids":["spreadsheet.conditional_aggregation"],"fact_ids":["spreadsheet.conditional_aggregation#f1","spreadsheet.conditional_aggregation#f3"],"teaching_block_ids":["spreadsheet.conditional_aggregation#tb1","spreadsheet.conditional_aggregation#tb2"],"anchors":["spreadsheet.conditional_aggregation#visual"]},"computed_values":{"G2":8,"G3":28000}}

### s12 · explainer · COUNTIFS and SUMIFS: Multiple Conditions  [reward 5]
Conditional Aggregation — Add a second (or third) condition by extending the argument list.
(syntax) COUNTIFS(criteria_range1, criteria1, criteria_range2, criteria2, ...) counts rows where all criteria are met together. Each additional range must have the same number of rows and columns as the first. =COUNTIFS(B2:B21,"Lagos",E2:E21,"Delivered") counts only Lagos orders that are Delivered. ⟦D.f2 D:tb3⟧
(syntax) SUMIFS(sum_range, criteria_range1, criteria1, criteria_range2, criteria2, ...) sums sum_range for rows where all criteria hold. Note the argument order: sum_range comes first, then each criteria_range/criteria pair. =SUMIFS(D2:D21,B2:B21,"Lagos",E2:E21,"Delivered") totals amounts for Lagos Delivered orders. ⟦D.f4 D:tb3⟧

### s13 · video · Building Conditional Aggregation Formulas
Conditional Aggregation — 
[VIDEO Building conditional aggregation formulas argument by argument] bridge-before: Watch how each argument slot is filled in order. The first clip uses text criteria only; the second clip uses both text and cell-reference criteria — no comparison operators like ">32" appear in either. | bridge-after: The clips do not show criteria with comparison operators, the quoting rule for expressions, or the same-range-twice trick for between-value counts — the teaching text covers all three.
  - AZuBNWMh7VM 118-366s facts=['f3', 'f4'] label: SUMIF and SUMIFS: summing revenue for one condition, then two, then three | summary: A dataset of months, products, countries, and sales revenue is used to build SUMIF for a single criterion (February revenue): the criteria range comes first, then the criterion, then the sum range at the end. SUMIFS is then built for two criteria (February and shirt white), with the sum range moved to the front and criteria_range1/criteria1/criteria_range2/criteria2 following in pairs. A third criterion (USA) is added by appending one more range–criteria pair, and each result is verified against the visible data.
  - X-xZ3eKvkzo 43-341s facts=['f1', 'f2', 'f5'] label: COUNTIF and COUNTIFS: counting rows that match one or two conditions | summary: A spreadsheet table of builders and regions is used to build COUNTIF step by step: the criteria range is selected first, then the criterion is entered as a quoted text string, then as a cell reference copied down the column. The formula correctly returns one instance of Doug, two of Dave, two of Brian, and one of Larry. COUNTIFS is then introduced to add a second condition — builder name paired with region — showing how criteria_range1/criteria1 and criteria_range2/criteria2 are entered in sequence; the result correctly returns zero for Doug (who is in the Central region), one for Brian, and one for Larry in the South.

### s14 · explainer · Criteria Syntax and the Between Pattern  [reward 5]
Conditional Aggregation — Criteria with comparison symbols or text must be in quotes — and you can use the same range twice.
(mechanism) Criteria can be a number, an expression, a cell reference, or text. Criteria that contain comparison symbols or text must be enclosed in quotation marks: use ">32" not >32, and "Lagos" not Lagos. A bare number like 32 or a cell reference like B4 does not need quotes. ⟦D.f5 D:tb4⟧
(mechanism) The same range can appear in more than one criteria pair to test a between condition. =COUNTIFS(C2:C21,">30",C2:C21,"<60") counts orders where delivery_minutes is between 30 and 60 — both criteria apply to the same column. ⟦D.f6 D:tb4⟧

### s15 · check · Single vs Multi-Condition Aggregation  [reward 5]
Quick Check — Which function counts rows that meet two conditions at once?
QUESTION [choice, core, grading=client] The Orders sheet has city in column B (B2:B21), status in column E (E2:E21), and amount in column D (D2:D21).

You want the total amount for orders that are **both** from Lagos **and** have status Delivered. Which formula is correct?
  ✔ opt_a: =SUMIFS(D2:D21,B2:B21,"Lagos",E2:E21,"Delivered")
  ✘ opt_b: =SUMIF(D2:D21,"Lagos",E2:E21,"Delivered")
      why: SUMIF handles only one condition. Its syntax is SUMIF(range, criteria, [sum_range]) — it takes one criteria range and one criterion. To apply two conditions at once, use SUMIFS.
  ✘ opt_c: =SUMIFS(B2:B21,"Lagos",E2:E21,"Delivered",D2:D21)
      why: SUMIFS syntax is SUMIFS(sum_range, criteria_range1, criteria1, ...). The sum_range (D2:D21) must come first. This formula puts the criteria ranges first and the sum_range last, which is the SUMIF order, not SUMIFS.
  ✘ opt_d: =SUMIF(B2:B21,"Lagos",D2:D21)+SUMIF(E2:E21,"Delivered",D2:D21)
      why: Adding two SUMIF results double-counts orders that are both from Lagos AND Delivered. An order that meets both conditions is included in both SUMIF results, so the total is inflated. SUMIFS applies both conditions simultaneously to avoid double-counting.
  feedback✔: Correct! =SUMIFS(D2:D21,B2:B21,"Lagos",E2:E21,"Delivered") sums the amounts in D2:D21 where the city is Lagos AND the status is Delivered. SUMIFS syntax: SUMIFS(sum_range, criteria_range1, criteria1, [criteria_range2, criteria2], ...).  feedback✘: SUMIFS(sum_range, criteria_range1, criteria1, criteria_range2, criteria2, ...) applies multiple conditions simultaneously. The sum_range (D2:D21) comes first, then each criteria_range/criteria pair. SUMIF handles only one condition.  hints: ['SUMIFS (plural) handles multiple conditions; SUMIF (singular) handles one.', 'In SUMIFS, the sum_range is the first argument, followed by criteria_range/criteria pairs.']  remediation→r04
  MEASURES: D:write_single_condition_countif_sumif(f1,f3); D:write_multi_condition_countifs_sumifs(f2,f4)   anchors=['assessment:write_single_condition_countif_sumif', 'assessment:write_multi_condition_countifs_sumifs']
  taught-before-tested: D.f1←s11; D.f3←s11; D.f2←s12; D.f4←s12

### s16 · check · The Between Pattern  [reward 5]
Quick Check — How do you count values in C2:C21 that are greater than 30 AND less than 60?
QUESTION [choice, stretch, grading=client] The Orders sheet has delivery times in column C (C2:C21). You want to count how many deliveries took between 30 and 60 minutes (inclusive).

Which formula correctly counts deliveries where delivery_minutes >= 30 AND <= 60?
  ✔ opt_a: =COUNTIFS(C2:C21,">=30",C2:C21,"<=60")
  ✘ opt_b: =COUNTIF(C2:C21,">=30 AND <=60")
      why: COUNTIF does not support compound criteria like ">=30 AND <=60" in a single criterion string. Each condition must be a separate criteria_range/criteria pair in COUNTIFS.
  ✘ opt_c: =COUNTIFS(C2:C21,">=30 AND <=60")
      why: COUNTIFS does not support compound criteria in a single string. ">=30 AND <=60" is not valid syntax. Use two separate criteria pairs: COUNTIFS(C2:C21,">=30",C2:C21,"<=60").
  ✘ opt_d: =COUNTIF(C2:C21,">=30")+COUNTIF(C2:C21,"<=60")
      why: This formula adds the count of deliveries >= 30 to the count of deliveries <= 60. Every delivery between 30 and 60 minutes is counted twice (once in each COUNTIF), so the result is inflated. COUNTIFS with two criteria counts each matching row exactly once.
  feedback✔: Correct! =COUNTIFS(C2:C21,">=30",C2:C21,"<=60") uses the same range (C2:C21) twice — once with the lower bound (">=30") and once with the upper bound ("<=60"). COUNTIFS counts only rows where both conditions are met simultaneously.  feedback✘: To test a range condition (between two values), list the same range twice in COUNTIFS: COUNTIFS(C2:C21,">=30",C2:C21,"<=60"). Each criteria_range/criteria pair adds another condition that must be met. COUNTIF cannot handle two conditions at once.  hints: ['COUNTIFS allows you to use the same range more than once — once for each bound of the between condition.', 'Criteria containing comparison operators like >= and <= must be in quotation marks.']  remediation→r05
  MEASURES: D:use_same_range_twice_for_between_condition(f6)   anchors=['assessment:use_same_range_twice_for_between_condition']
  taught-before-tested: D.f6←s14

### s17 · hands_on · Write Conditional Aggregation Formulas  [reward 10]
Practice — Apply correct criteria quoting to COUNTIF and SUMIFS on the Orders sheet.
QUESTION [formula_entry, core, grading=client] The Orders sheet has city in column B (B2:B21) and order amount in column D (D2:D21).

In cell H1, write a SUMIF formula that totals the amounts for orders from **Lagos**. The city criterion is a text value, so it must be enclosed in double quotation marks.

The expected result is **28000**.
  [unrendered interaction type formula_entry] public={"prompt":"The Orders sheet has city in column B (B2:B21) and order amount in column D (D2:D21).\n\nIn cell H1, write a SUMIF formula that totals the amounts for orders from **Lagos**. The city criterion is a text value, so it must be enclosed in double quotation marks.\n\nThe expected result is **28000**.","asset_ref":{"asset_id":"asset_orders_clean","variant_id":null},"target_cell":"H1","allowed_functions":["SUMIF"],"sheet_name":"orders"} grading={"expected_value":28000.0,"reference_formula":"=SUMIF(B2:B21,\"Lagos\",D2:D21)","must_use_functions":["SUMIF"],"forbid_hardcoded_values":true}
  feedback✔: Correct! =SUMIF(B2:B21,"Lagos",D2:D21) sums the amounts in D2:D21 where the corresponding city in B2:B21 equals "Lagos". The text criterion "Lagos" is enclosed in double quotation marks, as required for text and expression criteria.  feedback✘: Use =SUMIF(B2:B21,"Lagos",D2:D21). SUMIF syntax: SUMIF(range, criteria, [sum_range]). The criteria "Lagos" is a text value and must be in double quotation marks. Without quotes, Excel returns a #NAME? or #VALUE! error.  hints: ['SUMIF syntax: SUMIF(range, criteria, sum_range). The range is where you check the condition.', 'Text criteria must be in double quotes: "Lagos". Number criteria do not need quotes.']
  MEASURES: D:apply_correct_criteria_syntax_quoting(f5)   anchors=['practice', 'assessment:apply_correct_criteria_syntax_quoting']
  taught-before-tested: D.f5←s14

### s18 · recap · Text, Date, and Conditional Aggregation — Key Takeaways  [reward 5]
Recap — 
(takeaway) TEXTJOIN combines text with a delimiter; CONCATENATE (or CONCAT) joins without one. LEFT, RIGHT, and MID extract characters by position; TRIM removes stray spaces. Excel stores dates as serial numbers starting from January 1, 1900; TODAY() returns today's serial number and DATEDIF computes the difference in years or days. COUNTIF and SUMIF apply one condition; COUNTIFS and SUMIFS apply multiple — criteria with text or comparison symbols must be in quotes. ⟦A.f1 A.f2 A.f3 B.f1 B.f2 B.f3 B.f4 C.f1 C.f2 C.f4 D.f1 D.f2 D.f3 D.f4 D.f5⟧
[UP NEXT] Up Next: VLOOKUP, XLOOKUP, and INDEX/MATCH: In the next tile you'll look up a driver name from the Drivers sheet using VLOOKUP, then see how XLOOKUP and INDEX/MATCH handle cases VLOOKUP cannot.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · TEXTJOIN's ignore_empty Argument
(syntax) TEXTJOIN(delimiter, ignore_empty, text1, text2, ...) has three required parts. The delimiter is the separator inserted between each value. ignore_empty controls blank cells: TRUE skips them so no extra delimiter appears; FALSE includes them as empty strings. TEXTJOIN(", ", TRUE, B2, E2) on a row where E2 is blank returns just the city, not "Lagos, ". ⟦A.f1 A.f2 A:tb1⟧
### r02 · MID and TRIM Syntax
(syntax) MID(text, start_num, num_chars) needs three arguments: the text, where to start (1-based), and how many characters to take. =MID(A2,4,4) on "LG-2001" starts at position 4 (the '2') and takes 4 characters, returning "2001". TRIM(text) takes one argument and removes all leading and trailing spaces, leaving only single spaces between words. ⟦B.f3 B.f4 B:tb2 B:tb3⟧
### r03 · TODAY vs DATEDIF
(syntax) TODAY() returns the current date as a serial number and takes no arguments — it is always =TODAY() with empty parentheses. DATEDIF(start_date, end_date, unit) computes the difference between two dates. Use "D" as the unit for days and "Y" for complete years. To find days since an order was placed: =DATEDIF(G2,TODAY(),"D"). ⟦C.f1 C.f2 C.f5 C:tb2 C:tb3⟧
### r04 · COUNTIF/SUMIF vs COUNTIFS/SUMIFS
(mechanism) COUNTIF and SUMIF each accept exactly one criteria range and one criterion. COUNTIFS and SUMIFS accept any number of criteria_range/criteria pairs — all conditions must be met for a row to be counted or summed. For two conditions (city = Lagos AND status = Delivered), use COUNTIFS or SUMIFS, not COUNTIF or SUMIF. ⟦D.f1 D.f2 D.f3 D.f4 D:tb2 D:tb3⟧
### r05 · Using the Same Range Twice for a Between Condition
(mechanism) COUNTIFS allows the same range to appear in more than one criteria pair. To count values between 30 and 60 in C2:C21, write: =COUNTIFS(C2:C21,">30",C2:C21,"<60"). The first pair filters rows where delivery_minutes > 30; the second pair further filters to delivery_minutes < 60. Both criteria must be in quotes because they contain comparison symbols. ⟦D.f6 D:tb4⟧

## OTHER CONTENT (fields without a dedicated renderer)
· cells.formula: =TEXTJOIN(", ",TRUE,B2,E2)
· cells.formula: =TEXTJOIN(", ",TRUE,B3,E3)
· annotations.text: =TEXTJOIN(", ",TRUE,B2,E2)
· grading.reference_formula: =TEXTJOIN(" | ",1,B2,E2)
· cells.formula: =DATEDIF(G3,TODAY(),"D")