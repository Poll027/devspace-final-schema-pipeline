# EVALUATOR PACKET — Identifying Decisions, Findings, and Requirements (tile_stakeholder_framing_requirements)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = stakeholder.identifying_decision_need — Identifying the business decision a stakeholder needs the analysis to inform
B = stakeholder.precise_finding_statement — Stating a finding precisely and quantitatively (the specific number or comparison, not a vague claim)
C = stakeholder.framing_analytical_question — Converting a vague business question into a specific, measurable analytical question
D = stakeholder.identifying_requirements — Identifying stakeholder needs/requirements before analysis

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Anticipating stakeholder questions and objections; Applying descriptive statistics to capstone findings; Basic presentation structure (opening, body, call to action); Building a data model for the capstone dataset; Building a polished matplotlib/seaborn visualization set for the capstone; Converting a vague business question into a specific, measurable analytical question; Defining a capstone business question/problem statement; Documenting and presenting the finished capstone deliverable; Framing an actionable recommendation that is distinct from the finding itself; Identifying stakeholder needs/requirements before analysis; Independent, unassisted execution across multiple tool families; Integrating Python/pandas cleaning and analysis into an end-to-end project; Integrating SQL querying into an end-to-end project; Integrating spreadsheet analysis into an end-to-end project; Making a data-driven recommendation; Matching chart type to the specific point being made (trend vs. comparison vs. distribution vs. part-to-whole); Prioritizing findings by relevance to the stakeholder's specific decision, not by analytical interestingness; Producing a stakeholder-facing narrated summary of t

## LESSON, in learner order

### s01 · explainer · What decision is this analysis for?  [reward 5]
Decision Need — Every analysis request hides a decision. Finding it first saves you from measuring the wrong thing.
(intro) An operations manager emails you: "Can you look into our delivery times?" Before opening a notebook, the first question worth asking is not what to measure — it is what decision this analysis is actually meant to inform. ⟦A:tb1⟧
(definition) Analysis is the collection, manipulation and interpretation of information and data for use in decision-making. A request for analysis often exists because someone needs to decide something, even when the request itself does not say so directly. ⟦A.f1 A:tb2⟧
(mechanism) The engagement and scoping stage of an analytical project should establish an understanding of how the analysis will inform decisions. For the delivery-times request, that means asking the manager directly: is this about deciding whether to hire more couriers for the Lagos route, or whether to renegotiate with a courier partner? The answer changes what you would actually need to measure. ⟦A.f2 A:tb3⟧

### s02 · check · Spot the decision behind the request  [reward 5]
Quick Check — Apply what you've learned about identifying the decision a stakeholder needs.

### s03 · hands_on · Name the decision  [reward 10]
Hands On — Given a vague stakeholder request, identify the specific decision it is meant to inform.

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

### s07 · hands_on · Write a precise finding  [reward 10]
Hands On — Turn a vague delivery finding into a complete sentence with a specific number and comparison.

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

### s11 · check · Scoping stage agreement on outputs  [reward 5]
Quick Check — Apply what you've learned about what the scoping stage should produce.

### s12 · hands_on · Rewrite the vague question  [reward 10]
Hands On — Classify each element of a scoping conversation and restate the vague question as a measurable analytical question.

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

### s16 · check · Resource constraints and output agreement  [reward 5]
Quick Check — Apply what you've learned about constraints and the output agreement that closes the scoping stage.

### s17 · hands_on · Extract scope and output requirements  [reward 10]
Hands On — Given a stakeholder request, identify the data scope, constraints, and output requirements.

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