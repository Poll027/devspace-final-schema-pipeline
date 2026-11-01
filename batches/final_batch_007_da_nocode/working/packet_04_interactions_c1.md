# EVALUATOR PACKET — Identifying Decisions, Findings, and Requirements (tile_stakeholder_framing_requirements)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = stakeholder.identifying_decision_need — Identifying the business decision a stakeholder needs the analysis to inform
B = stakeholder.precise_finding_statement — Stating a finding precisely and quantitatively (the specific number or comparison, not a vague claim)
C = stakeholder.framing_analytical_question — Converting a vague business question into a specific, measurable analytical question
D = stakeholder.identifying_requirements — Identifying stakeholder needs/requirements before analysis

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (stakeholder.identifying_decision_need)   objective: Identify the business decision that a stakeholder's analysis request is meant to inform.
A.f1: Analysis is the collection, manipulation and interpretation of information and data for use in decision-making.   [sources: uk_gov_aqua_book#2 Definitions and concepts]
A.f2: The engagement and scoping stage of an analytical project should establish an understanding of how the analysis will inform decisions.   [sources: uk_gov_aqua_book#6.4 Treatment of uncertainty]
note: Opens the stakeholder-communication thread's running scenario: an operations manager's delivery-times request, carried through later concepts in this tile group.
PRACTICE ANCHOR (field_selection): Given a vague stakeholder request, state the specific decision it is meant to inform.  SUCCESS: The learner produces a single sentence naming the underlying decision (e.g. 'This analysis is meant to help decide whether to renegotiate with the courier partner'), not a restatement of the request or a list of metrics.
ASSESSMENT ANCHOR: identify_decision_behind_stakeholder_request facts=['f1', 'f2']

## SOURCE FACTS — B (stakeholder.precise_finding_statement)   objective: State an analysis finding as a specific, complete claim that accurately reflects what the data shows, rather than a vague summary.
B.f2: A communication's big idea must articulate a unique point of view, convey what's at stake, and be a complete sentence.   [sources: swd_whats_the_big_idea]
B.f3: A claim about the data should be checked against what the data actually shows, and narrowed if needed; one article's example revises the broader claim 'Price has declined for all products' to the more precise 'the average retail price of existing products declined' once the underlying data was examined more closely.   [sources: swd_story_you_want_to_tell]
B.f4: Writing about data should be specific about the point being made.   [sources: gov_uk_writing_about_data#Concentrate on the important points]
B.f5: Putting data into context includes making comparisons, for example: 'There were 787,000 suspensions in the 2022/23 academic year. This is an increase from the previous year, when 578,300 suspensions occurred...'   [sources: gov_uk_writing_about_data#Put the data into context]
note: Optional enrichment (quality assurance of communications, f1) is skipped -- not required for this concept's coverage.
PRACTICE ANCHOR (external_proof): Rewrite the vague finding 'sales went up' as a precise, quantified statement that names a specific number and a comparison to a prior period.  SUCCESS: The rewritten statement is a complete sentence, names at least one specific number, and includes a comparison (e.g., to a previous month or year), with no vague qualitative language remaining.
ASSESSMENT ANCHOR: identify_complete_sentence_big_idea facts=['f2']
ASSESSMENT ANCHOR: narrow_claim_to_match_data facts=['f3']
ASSESSMENT ANCHOR: state_finding_with_specific_number_and_comparison facts=['f4', 'f5']

## SOURCE FACTS — C (stakeholder.framing_analytical_question)   objective: Convert a vague business question into a specific analytical question with agreed boundaries and precision, that can actually be answered with data.
C.f1: In the engagement and scoping stage, the analyst should engage with the commissioner to identify the question, the context, and the boundaries of the analysis, as well as constraints such as deadlines and available resources.   [sources: uk_gov_aqua_book#6.1.2 The analyst's responsibilities]
C.f2: The engagement and scoping stage should lead to agreement between the analyst and commissioner about the outputs of the work, including acceptable levels of accuracy, precision and margins of error.   [sources: uk_gov_aqua_book#6.2 Assurance activities]
C.f3: A well-formed statistical question makes clear the variable(s) of interest, the group it focuses on, and its intent — describing the data, comparing a variable across two or more groups, or looking at an association between two variables — and can be answered with data collected or already in hand.   [sources: asa_gaise_ii#I. Formulate Statistical Investigative Questions]
PRACTICE ANCHOR (matching): Turn the vague question 'are we doing well?' into a specific, measurable analytical question by identifying the variable of interest, the group it focuses on, and the intent of the question.  SUCCESS: The learner produces a rewritten question that names at least one measurable variable, specifies the group or time period, and states a clear intent (description, comparison, or association) — and can explain what scoping conversation would be needed to arrive at it.
ASSESSMENT ANCHOR: restate_vague_question_as_measurable_analytical_question facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: identify_scoping_conversation_elements facts=['f1']
ASSESSMENT ANCHOR: identify_components_of_a_well_formed_statistical_question facts=['f3']
ASSESSMENT ANCHOR: describe_scoping_stage_agreement_on_outputs facts=['f2']

## SOURCE FACTS — D (stakeholder.identifying_requirements)   objective: Identify a stakeholder's requirements (scope, constraints, and expected output) before starting an analysis, and capture them in a specification.
D.f1: In the engagement and scoping stage, the commissioner should inform the analyst about the important aspects of the problem, its scope, and any constraints or issues.   [sources: uk_gov_aqua_book#6.1.1 The commissioner's responsibilities]
D.f2: The analyst should create a specification document that captures the commissioner's requirements, providing a definition of the scope and project constraints; the analyst should share this specification with the commissioner for sign-off.   [sources: uk_gov_aqua_book#6.1.2 The analyst's responsibilities]
D.f3: The commissioner should communicate to the analyst any relevant information about data sources and data quality.   [sources: uk_gov_aqua_book#6.2 Assurance activities]
D.f4: Constraints around resources and timelines should be clarified and agreed between the analyst and commissioner during engagement and scoping.   [sources: uk_gov_aqua_book#6.2 Assurance activities]
D.f5: The engagement and scoping stage should lead to agreement between the analyst and commissioner about the outputs of the work.   [sources: uk_gov_aqua_book#6.2 Assurance activities]
PRACTICE ANCHOR (field_selection): Given a short stakeholder request, list the four requirement categories (data needed, scope, deadline, output format) and write one concrete question the analyst should ask the commissioner to clarify each category before starting.  SUCCESS: The learner produces a list that names all four categories, assigns a realistic clarifying question to each, and does not begin any analytical work until all four are addressed.
ASSESSMENT ANCHOR: identify_commissioner_inputs_at_scoping facts=['f1', 'f3']
ASSESSMENT ANCHOR: describe_specification_document_and_sign_off facts=['f2']
ASSESSMENT ANCHOR: identify_resource_and_timeline_constraints facts=['f4']
ASSESSMENT ANCHOR: recognise_output_agreement_as_scoping_outcome facts=['f5']
ASSESSMENT ANCHOR: extract_data_scope_and_output_requirements_from_stakeholder_request facts=['f1', 'f2', 'f3', 'f4', 'f5']

## DATA ASSETS USED
ds_stakeholder_requests: Kwik Courier — Stakeholder Requests and Analytical Questions — columns: request_id(identifier,digits-as-label), request_text(text), decision(text), vague_question(text), measurable_question(text), variable_of_interest(categorical), group_or_period(categorical), intent(categorical)
   [1,"Can you look into our delivery times?","Decide whether to add more couriers on the Lagos route","Are our delivery times okay?","Is the average delivery time in Lagos this month higher than last month?","delivery time","Lagos, this month vs last month","comparison"]
   [2,"Can you check how our drivers are doing?","Decide whether to renegotiate the contract with the courier partner","Are our drivers performing well?","Is the average delivery time per driver in March 2024 above the 30-minute target?","delivery time per driver","all drivers, March 2024","description
   [3,"Look into whether Port Harcourt is a problem.","Decide whether to expand operations in Port Harcourt or reduce them","Is Port Harcourt a problem?","Is the average delivery time in Port Harcourt higher than in Lagos and Abuja over the same period?","delivery time","Port Harcourt vs Lagos and Abuj
   [4,"Find out if late deliveries are related to the time of day.","Decide whether to adjust dispatch scheduling to reduce late deliveries","Do late deliveries happen at certain times?","Is there an association between dispatch hour and delivery time across all orders in March 2024?","delivery time","
   [5,"Tell me about our order volumes.","Decide whether to hire additional operations staff for peak days","How many orders do we get?","What is the average number of orders per day in Lagos during March 2024?","order count per day","Lagos, March 2024","description"]
   [6,"Are customers happy with us?","Decide whether to invest in a customer-satisfaction improvement programme","Are customers satisfied?","What proportion of orders in March 2024 were delivered within the 30-minute target across all cities?","proportion of on-time deliveries","all cities, March 2024"

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Anticipating stakeholder questions and objections; Applying descriptive statistics to capstone findings; Basic presentation structure (opening, body, call to action); Building a data model for the capstone dataset; Building a polished matplotlib/seaborn visualization set for the capstone; Converting a vague business question into a specific, measurable analytical question; Defining a capstone business question/problem statement; Documenting and presenting the finished capstone deliverable; Framing an actionable recommendation that is distinct from the finding itself; Identifying stakeholder needs/requirements before analysis; Independent, unassisted execution across multiple tool families; Integrating Python/pandas cleaning and analysis into an end-to-end project; Integrating SQL querying into an end-to-end project; Integrating spreadsheet analysis into an end-to-end project; Making a data-driven recommendation; Matching chart type to the specific point being made (trend vs. comparison vs. distribution vs. part-to-whole); Prioritizing findings by relevance to the stakeholder's specific decision, not by analytical interestingness; Producing a stakeholder-facing narrated summary of t

## LESSON, in learner order

### s01 · explainer · What decision is this analysis for?  [reward 5]
Decision Need — Every analysis request hides a decision. Finding it first saves you from measuring the wrong thing.
(intro) An operations manager emails you: "Can you look into our delivery times?" Before opening a notebook, the first question worth asking is not what to measure — it is what decision this analysis is actually meant to inform. ⟦A.f1 A:tb1⟧
(definition) Analysis is the collection, manipulation and interpretation of information and data for use in decision-making. A request for analysis often exists because someone needs to decide something, even when the request itself does not say so directly. ⟦A.f1 A:tb2⟧
(mechanism) The engagement and scoping stage of an analytical project should establish an understanding of how the analysis will inform decisions. For the delivery-times request, that means asking the manager directly: is this about deciding whether to hire more couriers for the Lagos route, or whether to renegotiate with a courier partner? The answer changes what you would actually need to measure. ⟦A.f2 A:tb3⟧

### s02 · check · Spot the decision behind the request  [reward 5]
Quick Check — Apply what you've learned about identifying the decision a stakeholder needs.
QUESTION [choice, intro, grading=client] The operations manager sends you this message: "Can you look into our delivery times?"

What is the most useful first step before you start any analysis?
  ✔ opt_s02_a: Ask the manager what decision this analysis is meant to inform — for example, whether to add couriers on the Lagos route or renegotiate with a courier partner.
  ✘ opt_s02_b: Open the delivery-orders table and calculate the average delivery time straight away, because that is what the manager asked for.
      why: Starting the analysis immediately risks measuring the wrong thing. Analysis is for decision-making, and the engagement and scoping stage should establish how the analysis will inform a decision before any calculation begins.
  ✘ opt_s02_c: Ask the manager to send you a list of metrics they want, so you can measure each one.
      why: A list of metrics is not the same as a decision. The goal is to identify what the manager needs to decide — the metrics follow from that, not the other way around.
  ✘ opt_s02_d: Decide on your own which decision the analysis is for, so you can start without delay.
      why: Deciding on the manager's behalf skips the engagement and scoping stage. The scoping stage should establish an understanding of how the analysis will inform decisions by engaging with the commissioner, not by guessing.
  feedback✔: Correct. Analysis is for decision-making, and the engagement and scoping stage should establish how the analysis will inform a decision. Asking the manager what decision they face — add couriers? renegotiate a contract? — gives the analysis a clear target.  feedback✘: Think about why analysis exists: it is the collection, manipulation and interpretation of information for use in decision-making. Before measuring anything, the scoping stage should establish what decision the analysis is meant to inform.  hints: ['What does the engagement and scoping stage exist to establish?', "If the manager's decision turns out to be about renegotiating a contract, would 'average delivery time per city' be the right thing to measure?"]  remediation→r01
  MEASURES: A:identify_decision_behind_stakeholder_request(f1,f2)   anchors=['assessment:identify_decision_behind_stakeholder_request']
  taught-before-tested: A.f1←s01; A.f2←s01

### s03 · hands_on · Name the decision  [reward 10]
Hands On — Given a vague stakeholder request, identify the specific decision it is meant to inform.
QUESTION [table_select, core, grading=client] 
  intro shown to learner: The table below shows stakeholder requests and the decision each one is meant to inform. Read the request in row 2, then complete the task.
  task task_s03_t1 (cell): The manager says: "Can you check how our drivers are doing?" Click the cell in the table that names the specific decision this request is meant to inform.  KEY: row={'request_id': 2} column=decision expect=Decide whether to renegotiate the contract with the courier partner dataset-says=Decide whether to renegotiate the contract with the courier partner
      feedback: {'correct': 'Correct. The request is about driver performance, and the underlying decision is whether to renegotiate the courier partner contract.', 'incorrect': 'Look for the cell that names a specific decision — something the manager would act on — not a restatement of the request or a metric.'}
  feedback✔: Well done. The request 'Can you check how our drivers are doing?' hides the decision: whether to renegotiate the contract with the courier partner. Naming the decision before starting analysis keeps the work focused.  feedback✘: The decision is not the same as the request. Look for the cell that names what the manager would actually do with the analysis result — a concrete action or choice.  hints: ['The decision column names what the manager would do with the result, not what they asked you to measure.', "A decision is something you act on: 'renegotiate', 'hire', 'expand' — not 'look into' or 'check'."]
  MEASURES: A:identify_decision_behind_stakeholder_request(f1,f2)   anchors=['practice', 'assessment:identify_decision_behind_stakeholder_request']
  taught-before-tested: A.f1←s01; A.f2←s01

### s04 · explainer · From vague label to complete finding  [reward 5]
Precise Findings — A finding that names a number and a comparison is far more useful than one that only names a topic.
(intro) Once you have analyzed the delivery data, "delivery times went up" is a finding of sorts — but it does not say by how much, where, or compared to what. A communication's big idea must articulate a unique point of view, convey what is at stake, and be a complete sentence, not a fragment or a topic label. ⟦B.f2 B:tb1 B:tb2⟧
[BEFORE_AFTER] Adding a position and a statement of what is at stake turns a topic label into a complete finding sentence. (This is a first improvement — the next step adds the specific number and comparison.)
  before:
[DIAGRAM: Vague finding] nodes=['Lagos delivery times'] edges=[] alt: A box labelled 'Lagos delivery times' — a topic label with no claim, no number and no comparison.
  after:
[DIAGRAM: Precise finding] nodes=['Lagos delivery times have risen, so customers on that route are waiting longer for their orders.'] edges=[] alt: A box containing the sentence: 'Lagos delivery times have risen, so customers on that route are waiting longer for their orders.' Annotated as a complete sentence with a unique point of view and a statement of what is at stake.

### s05 · explainer · Narrow the claim and add the number  [reward 5]
Precise Findings — Check your claim against the data, narrow it if needed, then add the specific number and comparison.
(mechanism) A claim about the data should be checked against what the data actually shows, and narrowed if needed. One example revises the broader claim "Price has declined for all products" to the more precise "the average retail price of existing products declined" once the underlying data was examined more closely. The same check applies to the delivery claim: if only Lagos routes actually slowed down, the finding should narrow to Lagos, not describe every city. ⟦B.f3 B:tb3⟧
(example) Writing about data should be specific about the point being made, and putting data into context includes making comparisons. Following that pattern, a precise delivery finding names the number and the comparison: "the average Lagos delivery time rose to 30 minutes this month, up from 22 minutes last month" — rather than just "delivery times went up." ⟦B.f4 B.f5 B:tb4⟧

### s06 · check · Narrow the claim to match the data  [reward 5]
Quick Check — Apply what you've learned about checking a claim against what the data actually shows.
QUESTION [choice, intro, grading=client] An analyst writes this finding after reviewing the Kwik Courier data:

"Delivery times have declined for all cities."

The data shows: Lagos average rose from 22 to 30 minutes; Abuja average fell from 23 to 20 minutes; Port Harcourt average fell from 27 to 25 minutes.

What should the analyst do?
  ✔ opt_s06_a: Narrow the claim to match what the data actually shows — for example: 'Average delivery times fell in Abuja and Port Harcourt, but rose in Lagos.'
  ✘ opt_s06_b: Keep the claim as written, because two out of three cities did show a decline.
      why: A claim should be checked against what the data actually shows and narrowed if needed. Saying 'all cities' when Lagos shows the opposite is a claim the data does not support.
  ✘ opt_s06_c: Remove the finding entirely, because the data is contradictory.
      why: The data is not contradictory — it shows different trends in different cities. The right response is to narrow the claim to match what the data actually shows, not to remove it.
  ✘ opt_s06_d: Broaden the claim to 'delivery times have changed across all cities' so it is always true.
      why: Broadening the claim makes it vaguer, not more precise. A precise finding names the specific pattern the data shows, not a statement so general it is always true.
  feedback✔: Correct. A claim about the data should be checked against what the data actually shows and narrowed if needed. The original claim overstates the finding; the narrowed version accurately reflects the city-level pattern.  feedback✘: Check the data against the claim: does 'all cities' match what the numbers show? A precise finding is narrowed to match the data, not stretched to cover cases the data contradicts.  hints: ['Does the Lagos data support the claim that delivery times declined for all cities?', 'What would a claim look like that is true for Abuja and Port Harcourt but honest about Lagos?']  remediation→r02
  MEASURES: B:narrow_claim_to_match_data(f3)   anchors=['assessment:narrow_claim_to_match_data']
  taught-before-tested: B.f3←s05

### s07 · hands_on · Write a precise finding  [reward 10]
Hands On — Turn a vague delivery finding into a complete sentence with a specific number and comparison.
QUESTION [external_proof, core, grading=client] Rewrite the vague finding below as a precise, quantified statement.

Vague finding: "Sales went up."

Use the data and examples you have seen in this tile — for instance, the delivery-time figures from the earlier check question. Your rewritten statement must:
1. Be a complete sentence (subject + verb).
2. Name at least one specific number from the data.
3. Include a comparison — to a previous period, a target, or another group.

Write your statement in the text box, then check each criterion below before submitting.
  [unrendered interaction type external_proof] public={"instruction":"Rewrite the vague finding below as a precise, quantified statement.\n\nVague finding: \"Sales went up.\"\n\nUse the data and examples you have seen in this tile — for instance, the delivery-time figures from the earlier check question. Your rewritten statement must:\n1. Be a complete sentence (subject + verb).\n2. Name at least one specific number from the data.\n3. Include a comparison — to a previous period, a target, or another group.\n\nWrite your statement in the text box, then check each criterion below before submitting.","evidence_kinds":["text"],"checklist":["My statement is a complete sentence with a subject and a verb.","My statement names at least one specific number (e.g. a count, average, or percentage).","My statement includes a comparison (e.g. 'up from', 'compared with', 'above the target').","My statement contains no vague qualitative language such as 'w grading={"mode":"self_attest","rubric":[{"criterion":"The statement is a complete sentence with a subject and a verb.","weight":1},{"criterion":"The statement names at least one specific number from the examples in this tile.","weight":1},{"criterion":"The statement includes a comparison to a prior period, a target, or another group.","weight":1},{"criterion":"The statement contains no vague qualitative language.","weight":1}]}
  feedback✔: Well done. A precise finding is a complete sentence that names a specific number and puts it in context with a comparison — for example: 'The average Lagos delivery time rose to 30 minutes this month, up from 22 minutes last month — a 36% increase that suggests the Lagos route is slowing down.' That is the kind of statement a stakeholder can act on.  feedback✘: Review your statement against the checklist. A precise finding must be a complete sentence, name at least one specific number, and include a comparison. Vague language like 'went up' or 'improved' should be replaced with the actual figure.  hints: ['Look at the delivery-time figures from the earlier check question: what numbers were shown, and how could you compare them?', "A comparison could be 'the highest share of any city' or 'up from last month' — something that gives the number context."]  remediation→r03
  MEASURES: B:identify_complete_sentence_big_idea(f2); B:state_finding_with_specific_number_and_comparison(f4,f5)   anchors=['practice', 'assessment:identify_complete_sentence_big_idea', 'assessment:state_finding_with_specific_number_and_comparison']
  taught-before-tested: B.f2←s04; B.f4←s05; B.f5←s05

### s08 · explainer · From vague question to measurable question  [reward 5]
Analytical Question — A vague business question cannot be answered with data. A scoping conversation turns it into one that can.
(intro) "Are deliveries going well?" is the kind of question a stakeholder might actually ask — and it cannot be answered with data as written. In the engagement and scoping stage, the analyst should engage with the commissioner to identify the question, the context, and the boundaries of the analysis, as well as constraints such as deadlines and available resources. That kind of conversation can turn "are deliveries going well" into something answerable: which cities, which time period, compared against what. ⟦C.f1 C:tb1 C:tb2⟧
[BEFORE_AFTER] Naming the variable of interest, the group, and the intent turns an unanswerable question into a well-formed statistical question.
  before:
[DIAGRAM: Vague business question] nodes=['Are we doing well?'] edges=[] alt: A box containing the question 'Are we doing well?' with a note that it names no variable, no group, and no intent.
  after:
[DIAGRAM: Well-formed statistical question] nodes=['Variable of interest: average delivery time', 'Group: Lagos, this month vs. last month', 'Intent: comparison', 'Is average delivery time in Lagos this month higher than last month?'] edges=[('variable', 'question', None), ('group', 'question', None), ('intent', 'question', None)] alt: Three labelled components — variable of interest (average delivery time), group (Lagos, this month vs. last month), and intent (comparison) — combine to form the question: 'Is average delivery time in Lagos this month higher than last month?'
(definition) A well-formed statistical question makes clear the variable of interest, the group it focuses on, and its intent — whether that is describing the data, comparing a variable across two or more groups, or looking at an association between two variables — and can be answered with data collected or already in hand. ⟦C.f3 C:tb3⟧

### s09 · explainer · Agreeing on what a good answer looks like  [reward 5]
Analytical Question — Scoping ends with both sides agreeing on the outputs — not just the question.
(practical_context) The engagement and scoping stage should lead to agreement between the analyst and commissioner about the outputs of the work, including acceptable levels of accuracy, precision and margins of error, so both sides know in advance what kind of answer will count as sufficient. ⟦C.f2 C:tb4⟧

### s10 · check · Components of a well-formed statistical question  [reward 5]
Quick Check — Apply what you've learned about what makes a statistical question well-formed.
QUESTION [choice, intro, grading=client] Which of the following is a well-formed statistical question?
  ✔ opt_s10_a: Is the average delivery time in Lagos this month higher than last month? (variable: delivery time; group: Lagos, this month vs last month; intent: comparison)
  ✘ opt_s10_b: Are deliveries going well? (no variable, no group, no intent specified)
      why: This question cannot be answered with data as written. It names no measurable variable, no group, and no intent. A well-formed statistical question must make all three clear.
  ✘ opt_s10_c: What is happening with our drivers? (no measurable variable, no group, no intent)
      why: This question names no measurable variable (what about drivers?), no group (which drivers? when?), and no intent (description, comparison, or association?). It cannot be answered with data as written.
  ✘ opt_s10_d: Delivery times. (a topic label, not a question)
      why: This is a topic label, not a question. A well-formed statistical question must be a question that names a variable, a group, and an intent, and can be answered with data.
  feedback✔: Correct. A well-formed statistical question makes clear the variable of interest (delivery time), the group it focuses on (Lagos, this month vs last month), and its intent (comparison). It can be answered with data already in hand.  feedback✘: A well-formed statistical question must name three things: the variable of interest, the group it focuses on, and its intent — describing, comparing, or looking for an association. Which option does all three?  hints: ['Can you identify a measurable variable, a specific group, and a clear intent in each option?', "A question that can't be answered with data as written is not yet well-formed."]  remediation→r04
  MEASURES: C:identify_components_of_a_well_formed_statistical_question(f3)   anchors=['assessment:identify_components_of_a_well_formed_statistical_question']
  taught-before-tested: C.f3←s08

### s11 · check · Scoping stage agreement on outputs  [reward 5]
Quick Check — Apply what you've learned about what the scoping stage should produce.
QUESTION [choice, core, grading=client] At the end of the engagement and scoping stage for the Kwik Courier delivery-times project, the analyst and the operations manager should agree on which of the following?
  ✔ opt_s11_a: The outputs of the work, including acceptable levels of accuracy, precision and margins of error — for example, agreeing that a one-page summary with a bar chart of average delivery time per city is the deliverable.
  ✘ opt_s11_b: The exact SQL queries the analyst will use to extract the data, so the manager can review the code.
      why: The scoping stage is about agreeing on outputs and requirements, not on the technical implementation. The manager does not need to review SQL queries at this stage.
  ✘ opt_s11_c: The final conclusions of the analysis, so the manager knows the answer before the work begins.
      why: The conclusions cannot be agreed before the analysis is done — that would mean the analysis is not needed. The scoping stage agrees on the outputs (what will be delivered), not the findings.
  ✘ opt_s11_d: The list of all possible metrics that could be calculated from the delivery-orders table.
      why: Listing all possible metrics is not the goal of scoping. The scoping stage should lead to agreement on the specific outputs of this project, including what level of accuracy is acceptable.
  feedback✔: Correct. The engagement and scoping stage should lead to agreement between the analyst and commissioner about the outputs of the work, including acceptable levels of accuracy, precision and margins of error. For the delivery-times project, that means agreeing on the deliverable — for example, a one-page summary with a bar chart of average delivery time per city.  feedback✘: The scoping stage is about agreeing on what will be delivered and at what level of accuracy — not on the technical method, the final conclusions, or an exhaustive list of metrics.  hints: ['What does the scoping stage produce that both the analyst and commissioner sign off on?', "Think about what 'outputs of the work' means: what format, what level of detail, what accuracy?"]  remediation→r05
  MEASURES: C:describe_scoping_stage_agreement_on_outputs(f2)   anchors=['assessment:describe_scoping_stage_agreement_on_outputs']
  taught-before-tested: C.f2←s09

### s12 · hands_on · Rewrite the vague question  [reward 10]
Hands On — Classify each element of a scoping conversation and restate the vague question as a measurable analytical question.
QUESTION [classify, core, grading=client] The operations manager asks: "Can you look into our delivery times?"

After a scoping conversation, the analyst frames this as the measurable question: "Is the average delivery time in Lagos this month higher than last month?"

Classify each phrase below as the Variable of interest, the Group or time period, or the Intent of that well-formed question. One item does not belong to any component — drag it to 'Not a component'.
  'delivery time' -> Variable of interest  (column variable_of_interest, role=categorical)
      feedback: Correct. 'Delivery time' is the variable of interest — the measurable quantity the question is about.
  'Lagos, this month vs last month' -> Group or time period  (column group_or_period, role=categorical)
      feedback: Correct. 'Lagos, this month vs last month' specifies the group and time period the question focuses on.
  'comparison' -> Intent  (column intent, role=categorical)
      feedback: Correct. 'Comparison' is the intent — the question asks whether one value is higher than another.
  'Are our delivery times okay?' -> Not a component  (column vague_question, role=text)
      feedback: This is the vague question the analyst started with, not a component of the well-formed question. A well-formed statistical question is built from a variable, a group, and an intent — not from restating the original vague request.
  feedback✔: Well done. A well-formed statistical question names the variable of interest (delivery time), the group or time period (Lagos, this month vs last month), and the intent (comparison). The vague question 'Are our delivery times okay?' is what the scoping conversation starts from — not a component of the well-formed question.  feedback✘: A well-formed statistical question has three components: the variable of interest, the group or time period, and the intent. The vague question is what you start with — it is not one of those components.  hints: ['The variable of interest is the thing you would measure — what quantity does the question ask about?', 'The intent tells you whether the question is describing, comparing, or looking for an association.']
  MEASURES: C:restate_vague_question_as_measurable_analytical_question(f1,f3); C:identify_scoping_conversation_elements(f1)   anchors=['practice', 'assessment:restate_vague_question_as_measurable_analytical_question', 'assessment:identify_scoping_conversation_elements']
  taught-before-tested: C.f1←s08; C.f3←s08; C.f1←s08

### s13 · explainer · What the commissioner must tell you  [reward 5]
Requirements — Before analysis begins, the commissioner and analyst must exchange information about scope, data, and constraints.
(mechanism) Agreeing on the decision and the question still leaves open what you actually need from the operations manager before you can start: what data, by when, in what form. In the engagement and scoping stage, the commissioner should inform the analyst about the important aspects of the problem, its scope, and any constraints or issues, and should communicate any relevant information about data sources and data quality. ⟦D.f1 D.f3 D:tb1 D:tb2⟧
(mechanism) Constraints around resources and timelines should be clarified and agreed between the analyst and commissioner during engagement and scoping — for instance, whether the manager needs an answer this week or can wait for a fuller analysis next month. ⟦D.f4 D:tb3⟧
[PROCESS_FLOW: Engagement and scoping: the two-way exchange] nodes=['Commissioner provides: problem context, scope, constraints, data-quality information', 'Analyst drafts specification document', 'Commissioner signs off', 'Both parties agree on outputs before analysis begins'] edges=[('commissioner_input', 'analyst_draft', None), ('analyst_draft', 'commissioner_signoff', None), ('commissioner_signoff', 'agreed_outputs', None), ('commissioner_signoff', 'analyst_draft', 'Revise')] alt: A flow diagram showing the engagement-and-scoping exchange: the commissioner provides problem context, scope, constraints, and data-quality information; the analyst drafts a specification document; the commissioner signs off (or asks for revisions); both parties agree on outputs before analysis begins.

### s14 · explainer · The specification document and output agreement  [reward 5]
Requirements — The analyst captures requirements in a specification document and gets the commissioner's sign-off before starting.
(workflow) The analyst should create a specification document that captures the commissioner's requirements, providing a definition of the scope and project constraints; the analyst should share this specification with the commissioner for sign-off. For the delivery request, that means a short written specification of the routes, time period, data source, and deadline, which the manager signs off. The engagement and scoping stage should lead to agreement about the outputs of the work — for instance, agreeing the deliverable is a one-page summary with a bar chart of average delivery time per city. ⟦D.f2 D.f5 D:tb4⟧

### s15 · check · Commissioner inputs and the specification document  [reward 5]
Quick Check — Apply what you've learned about what the commissioner provides and what the analyst captures.
QUESTION [choice, intro, grading=client] During the engagement and scoping stage for the Kwik Courier delivery-times project, which of the following correctly describes what the commissioner provides and what the analyst produces?
  ✔ opt_s15_a: The commissioner informs the analyst about the problem, its scope, constraints, and relevant data sources and data quality; the analyst creates a specification document capturing these requirements and shares it with the commissioner for sign-off.
  ✘ opt_s15_b: The analyst decides the scope and constraints independently, then presents a finished report to the commissioner for approval.
      why: The analyst does not decide scope and constraints independently. In the engagement and scoping stage, the commissioner informs the analyst about the problem, scope, and constraints. The analyst then creates a specification document — not a finished report.
  ✘ opt_s15_c: The commissioner writes the specification document and the analyst signs it off before starting work.
      why: The roles are reversed. The analyst creates the specification document that captures the commissioner's requirements, and shares it with the commissioner for sign-off — not the other way around.
  ✘ opt_s15_d: The commissioner provides the final conclusions of the analysis; the analyst checks whether the data supports them.
      why: The commissioner does not provide conclusions. The commissioner provides information about the problem, scope, constraints, and data quality. The analyst then creates a specification document before any analysis begins.
  feedback✔: Correct. In the engagement and scoping stage, the commissioner informs the analyst about the problem, scope, constraints, and data sources and quality. The analyst captures these in a specification document and shares it with the commissioner for sign-off.  feedback✘: Think about who provides what: the commissioner brings knowledge of the problem, scope, constraints, and data quality; the analyst turns that into a specification document and asks the commissioner to sign it off.  hints: ['Who knows the most about the business problem and its constraints — the analyst or the commissioner?', 'What does the analyst produce at the end of the scoping stage, and who approves it?']  remediation→r06
  MEASURES: D:identify_commissioner_inputs_at_scoping(f1,f3); D:describe_specification_document_and_sign_off(f2)   anchors=['assessment:identify_commissioner_inputs_at_scoping', 'assessment:describe_specification_document_and_sign_off']
  taught-before-tested: D.f1←s13; D.f3←s13; D.f2←s14

### s16 · check · Resource constraints and output agreement  [reward 5]
Quick Check — Apply what you've learned about constraints and the output agreement that closes the scoping stage.
QUESTION [choice, core, grading=client] The operations manager says: "I need the delivery-times analysis by end of next week, and I want a one-page summary with a bar chart of average delivery time per city."

Which statement best describes what the analyst should do with this information during scoping?
  ✔ opt_s16_a: Clarify and agree the timeline constraint (end of next week) and record the agreed output (one-page summary with a bar chart) in the specification document, so both parties have agreed on the deliverable before analysis begins.
  ✘ opt_s16_b: Ignore the timeline for now and focus on the analysis; the deadline can be discussed later if needed.
      why: Constraints around resources and timelines should be clarified and agreed during engagement and scoping — not deferred. Leaving the deadline unaddressed risks delivering too late or misallocating effort.
  ✘ opt_s16_c: Treat the bar chart request as optional, because the analyst decides the output format independently.
      why: The engagement and scoping stage should lead to agreement between the analyst and commissioner about the outputs of the work. The output format is agreed jointly, not decided by the analyst alone.
  ✘ opt_s16_d: Ask the manager to provide a longer deadline, because resource and timeline constraints are the analyst's responsibility to set.
      why: Resource and timeline constraints are clarified and agreed between the analyst and commissioner — not set unilaterally by either party. The analyst should discuss whether the deadline is feasible, not simply reject it.
  feedback✔: Correct. Constraints around resources and timelines should be clarified and agreed during scoping. The engagement and scoping stage should lead to agreement about the outputs of the work — here, a one-page summary with a bar chart of average delivery time per city, delivered by end of next week.  feedback✘: Both the timeline and the output format are things to agree during scoping. Constraints around resources and timelines should be clarified and agreed; the scoping stage should lead to agreement about the outputs of the work.  hints: ['What should happen to resource and timeline constraints during the engagement and scoping stage?', 'Who agrees on the output format — the analyst alone, or both the analyst and the commissioner?']  remediation→r07
  MEASURES: D:identify_resource_and_timeline_constraints(f4); D:recognise_output_agreement_as_scoping_outcome(f5)   anchors=['assessment:identify_resource_and_timeline_constraints', 'assessment:recognise_output_agreement_as_scoping_outcome']
  taught-before-tested: D.f4←s13; D.f5←s14

### s17 · hands_on · Extract scope and output requirements  [reward 10]
Hands On — Given a stakeholder request, identify the data scope, constraints, and output requirements.
QUESTION [table_select, stretch, grading=client] 
  intro shown to learner: The table below shows stakeholder requests alongside the decision each is meant to inform and the measurable question the analyst should frame. Use row 3 to complete both tasks.
  task task_s17_t1 (cell): The manager says: "Look into whether Port Harcourt is a problem." Click the cell that names the specific decision this request is meant to inform — this is the scope the analyst must capture in the specification document.  KEY: row={'request_id': 3} column=decision expect=Decide whether to expand operations in Port Harcourt or reduce them dataset-says=Decide whether to expand operations in Port Harcourt or reduce them
      feedback: {'correct': 'Correct. The scope of the analysis is the decision it must inform: whether to expand or reduce operations in Port Harcourt.', 'incorrect': 'Look for the cell that names a concrete decision — something the manager would act on — not a restatement of the request.'}
  task task_s17_t2 (cell): Now click the cell that shows the measurable analytical question the analyst and commissioner should agree on during scoping.  KEY: row={'request_id': 3} column=measurable_question expect=Is the average delivery time in Port Harcourt higher than in Lagos and Abuja over the same period? dataset-says=Is the average delivery time in Port Harcourt higher than in Lagos and Abuja over the same period?
      feedback: {'correct': 'Correct. The measurable question names the variable (delivery time), the group (Port Harcourt vs Lagos and Abuja), and the intent (comparison) — this is what the analyst and commissioner should agree as the output requirement.', 'incorrect': 'The output requirement is the measurable analytical question — the one that names a variable, a group, and an intent, and can be answered with data.'}
  feedback✔: Well done. Before starting analysis, the analyst should capture the scope (the decision to inform) and the output requirement (the measurable question) in a specification document, and share it with the commissioner for sign-off.  feedback✘: The specification document captures two things: the scope (what decision the analysis informs) and the output requirement (the measurable question the analysis will answer). Both must be agreed with the commissioner before analysis begins.  hints: ['The scope is the decision the manager needs to make — what would they do with the result?', 'The output requirement is the measurable question: it names a variable, a group, and an intent.']
  MEASURES: D:extract_data_scope_and_output_requirements_from_stakeholder_request(f1,f2,f3,f4,f5)   anchors=['practice', 'assessment:extract_data_scope_and_output_requirements_from_stakeholder_request']
  taught-before-tested: D.f1←s13; D.f2←s14; D.f3←s13; D.f4←s13; D.f5←s14

### s18 · recap · What you've learned  [reward 5]
Recap — Four habits that shape every stakeholder conversation before analysis begins.
(takeaway) Every analysis request hides a decision — naming it up front gives the work a target. A precise finding names a number and a comparison, not just a topic. A well-formed statistical question names the variable, the group, and the intent. Before analysis begins, the commissioner and analyst agree on scope, constraints, data sources, and the expected output, captured in a specification document signed off by both sides. ⟦A.f1 A.f2 B.f2 B.f4 C.f3 C.f1 D.f1 D.f2 D.f3 D.f4 A:tb4 B:tb2 C:tb3 D:tb2 D:tb3⟧
[UP NEXT] Up next: Making a data-driven recommendation: In the next tile you will learn how to translate an analytical finding into a clear, actionable recommendation — the step that turns analysis into a decision.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Analysis serves a decision — a closer look — Here is a clear contrast to help you see the connection between a request and the decision behind it.
(definition) Analysis is the collection, manipulation and interpretation of information and data for use in decision-making. The engagement and scoping stage of an analytical project should establish an understanding of how the analysis will inform decisions. When the operations manager asks you to "look into delivery times," the decision could be whether to hire more Lagos couriers or whether to renegotiate with a courier partner — two very different analyses. Naming the decision first tells you what to measure. ⟦A.f1 A.f2 A:tb2 A:tb3⟧
### r02 · Narrowing a claim to match the data — Here is a clear contrast to help you see when a claim is too broad for the evidence.
(mechanism) A claim about the data should be checked against what the data actually shows, and narrowed if needed. If the delivery data shows only Lagos routes slowed down, the claim "delivery times went up" is too broad — it should narrow to "Lagos delivery times went up." One published example revised "Price has declined for all products" to "the average retail price of existing products declined" once the data was examined. Always match the scope of the claim to the scope of the evidence. ⟦B.f3 B:tb3⟧
### r03 · Complete sentence, specific number, comparison — Here is a clear contrast between a topic label and a precise finding sentence.
(example) A communication's big idea must be a complete sentence — not a fragment or a topic label. "Lagos delivery times" is only a topic label. Writing about data should be specific about the point being made, and putting data into context includes making comparisons. "The average Lagos delivery time rose to 30 minutes this month, up from 22 minutes last month" is a complete sentence that names the number (30 minutes) and the comparison (up from 22 minutes). That is the pattern: position + number + comparison. ⟦B.f2 B.f4 B.f5 B:tb2 B:tb4⟧
### r04 · The three components of a well-formed statistical question — Here is a clear contrast between a vague question and a well-formed one.
(definition) A well-formed statistical question makes clear the variable of interest, the group it focuses on, and its intent — describing the data, comparing a variable across two or more groups, or looking at an association between two variables — and can be answered with data collected or already in hand. "Is average delivery time in Lagos this month higher than last month?" names the variable (delivery time), the group (Lagos, this month vs. last), and the intent (a comparison). "Are we doing well?" names none of these. ⟦C.f3 C:tb3⟧
### r05 · Agreeing on outputs during scoping — Here is a clear contrast to help you see why output agreement matters.
(practical_context) The engagement and scoping stage should lead to agreement between the analyst and commissioner about the outputs of the work, including acceptable levels of accuracy, precision and margins of error, so both sides know in advance what kind of answer will count as sufficient. For the delivery request, that could mean agreeing that a one-page summary with a bar chart of average delivery time per city is sufficient — rather than discovering at the end that the manager expected a full statistical report. ⟦C.f2 C:tb4⟧
### r06 · Commissioner inputs and the specification document — a closer look — Here is a clear contrast to help you see what the commissioner provides and what the analyst captures.
(mechanism) In the engagement and scoping stage, the commissioner should inform the analyst about the important aspects of the problem, its scope, and any constraints or issues, and should communicate any relevant information about data sources and data quality — for the delivery request, that could mean telling you which system holds delivery timestamps and whether any routes are missing GPS data. The analyst should then create a specification document capturing these requirements and share it with the commissioner for sign-off. ⟦D.f1 D.f2 D.f3 D:tb2 D:tb4⟧
### r07 · Resource constraints and output agreement — a closer look — Here is a clear contrast to help you see what constraints and output agreement mean in practice.
(mechanism) Constraints around resources and timelines should be clarified and agreed between the analyst and commissioner during engagement and scoping — for instance, whether the manager needs an answer this week or can wait for a fuller analysis next month. The engagement and scoping stage should lead to agreement between the analyst and commissioner about the outputs of the work — for instance, agreeing the deliverable is a one-page summary with a bar chart of average delivery time per city. ⟦D.f4 D.f5 D:tb3 D:tb4⟧

## OTHER CONTENT (fields without a dedicated renderer)
· public.checklist: My statement contains no vague qualitative language such as 'went up', 'improved', or 'a lot'.