# EVALUATOR PACKET — Data Quality and the Analysis Workflow (tile_data_quality_and_workflow)
Tile summary: Learn to check whether a dataset is fit for purpose using four quality checks (completeness, uniqueness, validity, accuracy), follow a six-stage repeatable analysis workflow, and apply basic data-ethics and privacy principles when handling and sharing data.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = data.data_quality_basics — Basic data-quality checks
B = data.analysis_workflow — Ask, inspect, clean, analyze, visualize, communicate
C = data.ethics_privacy_basics — Data ethics, privacy, and responsible handling basics

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (data.data_quality_basics)   objective: Apply basic data-quality checks (completeness, uniqueness, validity, accuracy) to decide whether a simple dataset is fit for a stated purpose.
A.f1: Data quality means whether a dataset is fit for the purpose it will be used for.   [sources: uk_gov_data_quality_framework#Why do we need a data quality framework?]
A.f2: Completeness checks whether the records and values that should be present in the dataset actually are, rather than missing.   [sources: uk_gov_data_quality_framework#Completeness]
A.f3: Uniqueness checks whether a record that should appear once (one entity, one row) is duplicated in the dataset.   [sources: uk_gov_data_quality_framework#Uniqueness]
A.f4: Validity checks whether a column's values are in the range and format expected for that column.   [sources: uk_gov_data_quality_framework#Validity]
A.f5: Accuracy checks whether the data correctly matches the real-world thing it describes.   [sources: uk_gov_data_quality_framework#Accuracy]
A.m1 (misconception): Good-quality data does not have to be perfect.   [sources: uk_gov_data_quality_framework#User needs and trade-offs]
note: The four required checks (completeness, uniqueness, validity, accuracy) are the core; consistency and timeliness are optional enrichment facts and can be skipped or touched only briefly.
note: Keep each check's example tight -- one line each, same delivery-orders table throughout.
PRACTICE ANCHOR (field_selection): Given a small delivery-orders table with planted problems, flag each problem and name the check it fails.  SUCCESS: The learner flags the row with no delivery time as a completeness failure, the repeated order number as a uniqueness failure, the negative delivery time as a validity failure, and states what real-world information would be needed to confirm accuracy.
ASSESSMENT ANCHOR: judge_fitness_for_purpose facts=['f1']
ASSESSMENT ANCHOR: spot_missing_or_duplicate_records facts=['f2', 'f3']
ASSESSMENT ANCHOR: distinguish_invalid_from_inaccurate_values facts=['f4', 'f5']
ASSESSMENT ANCHOR: recognize_good_enough_data facts=['m1']

## SOURCE FACTS — B (data.analysis_workflow)   objective: Describe the repeatable analysis workflow (clarify the question, inspect and clean the data, analyze it, visualize findings, then communicate them) and use it to structure a small analysis task.
B.f1: A repeatable analysis process typically begins by clarifying the question or purpose, so both the analyst and whoever needs the answer share an understanding of what is being analyzed and why.   [sources: uk_gov_aqua_book#5.2.1]
B.f2: Before analysis, the data should be inspected and checked for quality, so quality problems are addressed as early as possible.   [sources: uk_gov_data_quality_framework#3.1 Assess data quality at all stages of the lifecycle]
B.f3: Cleaning the data helps reduce quality problems such as duplication and inconsistent values.   [sources: uk_gov_data_quality_framework#Prepare, store and maintain]
B.f4: Analyzing means examining the prepared data to answer the question; exploratory data analysis, for example, looks at the data to uncover its underlying structure and spot anomalies (unusual values).   [sources: nist_eda_handbook#1.1.1, uk_gov_aqua_book#5.2.2, uk_gov_aqua_book#5.2.3]
B.f5: Visualizing means turning data into plots or other graphics; exploratory data analysis relies mostly on such graphical techniques to gain insight into a dataset and reveal its structure.   [sources: nist_eda_handbook#1.1.1]
B.f6: The final stage of an analysis is communicating the findings, and how far they can be trusted, to the people who will use them, not merely producing the analysis itself.   [sources: uk_gov_aqua_book#5.2.4]
B.f7: This process is commonly iterative rather than strictly linear: earlier stages, such as inspecting or cleaning, may be revisited as later stages reveal new issues.   [sources: uk_gov_aqua_book#5.2, uk_gov_data_quality_framework#What is a data lifecycle?]
note: Keep 'analyze' and 'visualize' as clearly distinct steps -- don't let visualize collapse into analyze; this path splits them explicitly.
note: The iterative note (going back to inspect/clean) should stay a short closing point, not a new sub-workflow.
PRACTICE ANCHOR (ordering): Put the steps of a small delivery-data analysis in order (clarify the question, inspect, clean, analyze, visualize, communicate), then say where the process loops back when the analysis turns up a suspicious value.  SUCCESS: Steps are in the correct order with analyze and visualize kept distinct, and the learner points back to inspecting or cleaning as the step to revisit.
ASSESSMENT ANCHOR: order_workflow_steps facts=['f1', 'f2', 'f3', 'f4', 'f5', 'f6']
ASSESSMENT ANCHOR: separate_analyze_from_visualize facts=['f4', 'f5']
ASSESSMENT ANCHOR: recognize_iterative_loop_back facts=['f7']

## SOURCE FACTS — C (data.ethics_privacy_basics)   objective: Apply basic data-ethics and privacy principles (respecting privacy, minimizing collection, honest reporting of limitations) when handling and presenting data in a small analysis task.
C.f1: Data users should respect the privacy and confidentiality of the individuals a dataset describes.   [sources: federal_data_ethics_framework#Tenet 3]
C.f2: Responsible data handling includes minimizing data collection to what is needed and being accountable for how the data is used.   [sources: federal_data_ethics_framework#Tenet 5]
C.f3: Data work should consider its potential impact on the people and communities it affects.   [sources: federal_data_ethics_framework#Tenet 2]
C.f4: When sharing data and findings, data users should honestly report data limitations and known biases rather than overstating certainty.   [sources: federal_data_ethics_framework#Tenet 4]
C.f5: Identifying information that isn't needed for the purpose should be left out or removed, especially before data is shared; findings can describe a group without identifying individuals.   [sources: federal_data_ethics_framework#Tenet 3, federal_data_ethics_framework#Data Ethics Tenets in Action, federal_data_ethics_framework#Figure 2 Statistical Data Uses]
C.m1 (misconception): Removing identifying information does not by itself remove the risk of re-identification; the data combined with other available data can still identify people.   [sources: federal_data_ethics_framework#Tenet 3, federal_data_ethics_framework#Data Ethics Tenets in Action]
note: Keep ethics principles grounded in the same delivery-orders example, not abstract.
note: The de-identification misconception (m1) is easy to skip -- make sure it's stated explicitly, not implied.
PRACTICE ANCHOR (field_selection): Given a delivery table and a stated purpose, choose which columns to keep and which to leave out before sharing, and note one limitation to report.  SUCCESS: Columns not needed for the purpose, such as customer phone numbers and names, are left out; the learner also notes that removing them does not fully rule out re-identification, and names one data limitation to state in the findings.
ASSESSMENT ANCHOR: identify_unneeded_identifying_data facts=['f1', 'f5']
ASSESSMENT ANCHOR: apply_minimal_collection_and_impact_thinking facts=['f2', 'f3']
ASSESSMENT ANCHOR: report_limitations_honestly facts=['f4']
ASSESSMENT ANCHOR: recognize_reidentification_risk facts=['m1']

## DATA ASSETS USED
ds_delivery_orders: Kwik Courier — Delivery Orders — columns: order_id(identifier,digits-as-label), order_date(datetime), city(categorical), delivery_minutes(numerical), driver_id(identifier,digits-as-label), customer_name(pii), customer_phone(pii)
   [1001,"2024-03-01","Lagos",28,201,"Amara Okafor","+2348012345678"]
   [1002,"2024-03-01","Abuja",20,202,"Emeka Nwosu","+2348023456789"]
   [1003,"2024-03-02","Lagos",32,201,"Fatima Bello","+2348034567890"]
   [1004,"2024-03-02","Port Harcourt",25,203,"Chidi Eze","+2348045678901"]
   [1005,"2024-03-03","Abuja",22,202,"Ngozi Adeyemi","+2348056789012"]
   [1006,"2024-03-03","Lagos",30,204,"Tunde Afolabi","+2348067890123"]
   [1007,"2024-03-04","Port Harcourt",24,203,"Kemi Obi","+2348078901234"]
   [1008,"2024-03-04","Abuja",21,205,"Yusuf Musa","+2348089012345"]
   variant ds_delivery_orders_messy: 3 ops; planted: issue_dq_001(missing_value); issue_dq_002(duplicate_row); issue_dq_003(impossible_value)

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Arithmetic operators; Ask, inspect, clean, analyze, visualize, communicate; Basic error handling (try/except); Basic file I/O (reading/writing text and CSV files); Comparison operators; Control flow: if/elif/else; Core data structure: dictionaries; Core data structure: lists; Core data structure: sets; Core data structure: tuples; Core data types (int, float, str, bool); Data ethics, privacy, and responsible handling basics; Default and keyword arguments; Defining calling functions; For loops; Iterating over data structures; List and dict comprehensions; Logical operators; Loop control statements (break, continue); Modules and imports; Parameters arguments; Return values; String basics and f-string formatting; Type conversion/casting; Variable scope (local vs global); Variables and assignment; While loops

## LESSON, in learner order

### s01 · explainer · Is the data any good?  [reward 0]
Data Quality — Before drawing conclusions from the delivery-orders table, you need to ask one question first: is this data fit for the purpose?
(intro) Data quality means whether a dataset is fit for the purpose it will be used for — not whether it looks tidy, but whether it can actually support the question you're asking. Before trusting any conclusion drawn from the Kwik Courier delivery-orders table, you need to check whether the data itself is reliable enough to answer that question. ⟦A.f1 A:tb1⟧
(mechanism) Two checks look at what is missing or repeated. Completeness checks whether the records and values that should be present actually are — for example, an order row with no delivery time recorded at all. Uniqueness checks whether a record that should appear only once is duplicated — for example, the same order number showing up as two separate rows. ⟦A.f2 A.f3 A:tb2⟧
[TABLE ds_delivery_orders cols=['order_id', 'order_date', 'city', 'delivery_minutes', 'driver_id'] variant=ds_delivery_orders_messy highlights=[["cell","delivery_minutes","Completeness failure: delivery time missing"],["row",null,"Uniqueness failure: duplicate order row"],["cell","delivery_minutes","Validity failure: −5 minutes is not a valid delivery time"]]] caption: Kwik Courier delivery orders — three quality problems highlighted

### s02 · video · Data-quality dimensions in action  [reward 0]
Data Quality — Watch how each check is tied to one concrete problem: a missing detail, a repeated entry, a badly formatted value.
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · explainer · Validity, accuracy, and good enough  [reward 0]
Data Quality — Two more checks look at whether the values themselves are trustworthy — and data doesn't have to be perfect to be useful.
(mechanism) Validity checks whether a column's values are in the range and format expected — a delivery time of −5 minutes fails validity because negative time is not a valid delivery time. Accuracy checks whether the data correctly matches the real-world thing it describes — an order logged as delivered to Lagos when the driver actually delivered it to Abuja is complete, unique and validly formatted, but still inaccurate. ⟦A.f4 A.f5 A:tb3⟧
(misconception) Good-quality data does not have to be perfect. The goal of these checks is not a flawless dataset; it is a dataset good enough to answer the question you actually have, using completeness, uniqueness, validity and accuracy as the specific things to look for. ⟦A.m1 A:tb4⟧

### s04 · check · Fitness for purpose and missing or duplicate records  [reward 5]
Quick Check — Apply what you've learned about completeness and uniqueness.

### s05 · check · Invalid vs inaccurate values, and good-enough data  [reward 5]
Quick Check — Distinguish validity failures from accuracy failures, and recognise when data is good enough.

### s06 · hands_on · Flag the quality problems  [reward 10]
Hands On — The delivery-orders table below has three planted problems. Flag each one and name the check it fails.

### s07 · explainer · A repeatable order for analysis  [reward 0]
Analysis Workflow — Knowing what to check is only half the job — you also need to know what order to do things in.
(intro) A repeatable analysis process typically begins by clarifying the question or purpose — for the Kwik Courier data, that might be 'which cities have unusually slow deliveries?' Clarifying this first means both you and whoever asked for the analysis share an understanding of what is being analyzed and why, before any work starts. ⟦B.f1 B:tb1⟧
(workflow) Next comes inspecting and cleaning. Before analysis, the data should be inspected and checked for quality so problems are addressed early — this is where the completeness, uniqueness, validity and accuracy checks come in. Cleaning then helps reduce quality problems such as duplication and inconsistent values, for example removing the duplicate order row found during inspection. ⟦B.f2 B.f3 B:tb2⟧
[PROCESS_FLOW: The six-stage analysis workflow] nodes=['Clarify the question — Agree on what is being analyzed and why', 'Inspect — Check completeness, uniqueness, validity, accuracy', 'Clean — Remove duplicates, fix inconsistent values', 'Analyze — Examine prepared data; spot anomalies', 'Visualize — Turn data into plots or graphics', 'Communicate — Share findings and their limitations'] edges=[('n_clarify', 'n_inspect', None), ('n_inspect', 'n_clean', None), ('n_clean', 'n_analyze', None), ('n_analyze', 'n_visualize', None), ('n_visualize', 'n_communicate', None), ('n_analyze', 'n_inspect', 'new issue found'), ('n_visualize', 'n_inspect', 'new issue found')] alt: Six boxes in a row: Clarify the question → Inspect → Clean → Analyze → Visualize → Communicate. Two loop-back arrows point from Analyze and Visualize back to Inspect, labelled 'new issue found'.

### s08 · video · One analysis walked through in order  [reward 0]
Analysis Workflow — Watch how ask, prepare, clean, analyze and share play out in a real example.
[VIDEO ] bridge-before:  | bridge-after: 

### s09 · explainer · Analyzing and visualizing are different steps  [reward 0]
Analysis Workflow — Examining the data and turning it into a graphic are two distinct jobs — keeping them separate matters.
(workflow) Analyzing means examining the prepared data to answer the question. Exploratory data analysis looks at the data to uncover its underlying structure and spot anomalies — unusual values, like one delivery that took far longer than every other in the batch. For the Kwik Courier data, analyzing might mean looking closely at the cleaned rows to see which cities' deliveries stand out. ⟦B.f4 B:tb3⟧
(workflow) Visualizing is its own step: turning data into plots or other graphics. Exploratory data analysis relies mostly on such graphical techniques to gain insight and reveal structure, but making the graphic is a different job from examining the data. For the delivery data, visualizing might mean turning those delivery times into a graphic so the pattern is easy to see at a glance. ⟦B.f5 B:tb4⟧

### s10 · explainer · Communicating findings is part of the workflow  [reward 0]
Analysis Workflow — The analysis isn't done when the numbers are ready — sharing what they mean, and how far they can be trusted, is the final stage.
(workflow) The final stage is communicating the findings, and how far they can be trusted, to the people who will use them — not merely producing the analysis itself. Telling a manager that Lagos deliveries are running slow but the sample is small is part of the workflow. ⟦B.f6 B:tb5⟧

### s11 · check · The workflow loops back  [reward 5]
Quick Check — Recognise when and why the process revisits earlier stages.

### s12 · hands_on · Put the workflow in order  [reward 10]
Hands On — Arrange the six analysis stages in the correct order, then identify where the process loops back when a suspicious value turns up.

### s13 · explainer · The people behind the data  [reward 0]
Data Ethics — The delivery-orders table contains information about real people — that changes how you should handle it.
(intro) The Kwik Courier delivery-orders table almost certainly contains information about real people — customers' addresses, drivers' names. Data users should respect the privacy and confidentiality of the individuals a dataset describes, which means treating that table as more than just numbers to analyze. ⟦C.f1 C:tb1⟧
(practical_context) Responsible data handling includes minimizing data collection to what is needed and being accountable for how the data is used — if the analysis only needs delivery times and cities, there is no reason to keep customers phone numbers. Data work should also consider its potential impact on the people and communities it affects: a finding like slow deliveries in one neighborhood could affect real customers and drivers, not just look interesting in a report. ⟦C.f2 C.f3 C:tb2⟧

### s14 · explainer · Honest reporting and the limits of removing names  [reward 0]
Data Ethics — Sharing findings responsibly means stating what the data can and cannot claim — and knowing that removing a name column is not enough.
(practical_context) When sharing data and findings, data users should honestly report data limitations and known biases rather than overstating certainty — if the delivery data only covers one week, or one driver logged times inconsistently, that limitation belongs in the report. Identifying information that is not needed for the purpose should be left out or removed, especially before data is shared; findings can describe a group without identifying individuals — reporting 'the eastern delivery zone runs slow' rather than naming individual customers. ⟦C.f4 C.f5 C:tb3⟧
(misconception) Removing identifying information does not by itself remove the risk of re-identification: the data, combined with other available data, can still identify people, so removing a name column alone is not automatically enough. ⟦C.m1 C:tb4⟧

### s15 · check · Privacy, minimal collection, and impact  [reward 5]
Quick Check — Apply the principles of privacy, minimal collection and impact thinking to the delivery-orders scenario.

### s16 · check · Honest reporting and re-identification risk  [reward 5]
Quick Check — Recognise when a finding overstates certainty, and why removing names is not always enough.

### s17 · hands_on · Which columns should you keep?  [reward 10]
Hands On — Given the delivery-orders table and a stated analysis purpose, select the columns to keep before sharing — and note one limitation to report.

### s18 · recap · What you've learned  [reward 5]
Recap — Three ideas that will shape every analysis you run.
(takeaway) Running completeness, uniqueness, validity and accuracy checks on the delivery-orders table before analyzing it is what tells you whether you can trust what the numbers say. The analysis workflow — clarify, inspect, clean, analyze, visualize, communicate — is commonly iterative: earlier stages may be revisited as later stages reveal new issues. Treating the people behind the data with care, and being honest about what the analysis can and cannot claim, is as much a part of the job as getting the numbers right. ⟦A.f1 B.f7 C.f1 C.f4 A:tb5 B:tb6 C:tb5⟧
[UP NEXT] Up next: Variables and assignment: In the next tile you will learn how Python stores values in variables — the foundation for writing code that processes the delivery-orders data.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Fitness for purpose, completeness and uniqueness — a closer look — Here is a clear contrast to help you see the difference.
(definition) Data quality means whether a dataset is fit for the purpose it will be used for. A completeness failure means a value that should be present is missing — order 1009 in the Kwik Courier table has no delivery time recorded at all. A uniqueness failure means a record that should appear once is duplicated — order 1003 appears as two identical rows. Neither problem means the data is useless; it means you know what to fix before analyzing. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2⟧
[TABLE ds_delivery_orders cols=['order_id', 'order_date', 'city', 'delivery_minutes'] variant=ds_delivery_orders_messy highlights=[["cell","delivery_minutes","Completeness: delivery time missing"],["row",null,"Uniqueness: duplicate row"]]] caption: Completeness failure (order 1009) and uniqueness failure (order 1003 duplicated)
### r02 · Validity vs accuracy — the key contrast — These two checks are easy to confuse. Here is the clearest way to tell them apart.
(definition) Validity checks whether a value is in the expected range or format — order 1006 has delivery_minutes = −5, which is not a valid delivery time. Accuracy checks whether the value correctly matches the real world — an order logged as delivered to Lagos when the driver actually delivered it to Abuja passes validity (the city name is a real city) but fails accuracy. Good-quality data does not have to be perfect; it only has to be good enough to answer the question you actually have. ⟦A.f4 A.f5 A.m1 A:tb3 A:tb4⟧
### r03 · Why the workflow loops back — The analysis process is not a straight line — here is why earlier stages get revisited.
(mechanism) This process is commonly iterative rather than strictly linear: earlier stages, such as inspecting or cleaning, may be revisited as later stages reveal new issues. If analyzing the Kwik Courier delivery data turns up a value that looks wrong, you go back and inspect or clean it before continuing, rather than treating each stage as done for good. ⟦B.f7 B:tb6⟧
### r04 · Privacy, minimal collection and impact — a concrete contrast — Here is the clearest way to apply these principles to the delivery-orders table.
(practical_context) Data users should respect the privacy and confidentiality of the individuals a dataset describes. Responsible data handling means minimizing collection to what is needed — if the analysis only needs delivery times and cities, customer phone numbers should not be collected or kept. Data work should consider its potential impact on the people it affects: a finding about slow deliveries in one area affects real customers and drivers. Identifying information that is not needed for the purpose should be left out or removed before data is shared; findings can describe a group without identifying individuals. ⟦C.f1 C.f2 C.f3 C.f5 C:tb1 C:tb2 C:tb3⟧
### r05 · Honest reporting and re-identification — why removing names is not enough — Two principles that are easy to underestimate.
(practical_context) When sharing findings, data users should honestly report data limitations and known biases rather than overstating certainty — if the delivery data only covers one week, that limitation belongs in the report. Removing identifying information does not by itself remove the risk of re-identification: the data, combined with other available data, can still identify people, so removing a name column alone is not automatically enough. ⟦C.f4 C.m1 C:tb3 C:tb4⟧