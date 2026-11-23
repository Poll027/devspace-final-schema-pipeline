# Stage 08 — Independent pedagogy review

VERDICT: PASS

## Scope and method

Reviewed all nine tiles (the conservative canary scope), including all main steps, answer choices, grading feedback and conditional remediation. Re-derived the instructional requirements from `inputs/path_glossary_bundle.json`, checked the two table examples against `scenario_asset_registry.json`, and read the assembled `tile_lessons` as learner journeys. Applied the stage evaluator instructions and the playbook's text-before-assessment principle. Did not consult generator reasoning or prior evaluator reports and did not rerun deterministic gates.

No player screenshots were present; visual judgements concern authored diagrams, code schematics and tables, not rendered layout. All glossary media entries are null and there are no video steps, so video-added-value review is not applicable. HIGH video need alone is not an unsupported-content defect. Inspect-and-judge practice is assessed as read-only practice, not as an execution lab.

## Journey assessment

| Tile | Assessment |
|---|---|
| aws_devops.tile.089 | Limits and observations are explained before recovery identification and whole-record classification. Specific feedback distinguishes configuration, notification and recovery. The bounded, honestly recorded unsuccessful experiment is defensibly acceptable under the practice objective; the generic bucket label could obscure that distinction. |
| aws_devops.tile.090 | Three separate explain → check → apply sequences cover Lambda, EKS and EC2 blue/green. Commands and verification requirements precede their checks. The revision, alias and traffic distinctions remain separate. The 13-step, 10.5-minute estimate fits the intended pacing range. Remediation addresses the selected evidence errors. |
| aws_devops.tile.093 | The text and schematic teach exception-path placement and identity-based cleanup before assessment. The independent postcheck is explicitly separate from normal control flow after an unhandled exception. Wrong-item feedback distinguishes skipped cleanup from overbroad deletion. |
| aws_devops.tile.094 | Approved intent and reconciliation are taught before the checks; refresh-only planning, persistence on apply and unchanged remote infrastructure are accurately distinguished. The symbolic example supports the text. |
| aws_devops.tile.095 | The interface schematic and prose precede interface/verification judgements. The invented interface names and mismatched live settings have explicit evidence and defensible keys. The one explainer is compact but does not hide a tested requirement. |
| aws_devops.tile.096 | Requirements and multi-period comparisons precede table selection. The current option satisfies the registered bounds; the smaller candidate fails latency at peak (260 > 200 ms) and changing demand (230 > 200 ms). Equality is explicitly allowed in the practice introduction. Remediation supplies the relevant rule and table, though the default incorrect message is poorly tailored. |
| aws_devops.tile.097 | Context, evidence preservation and mapped routing precede checks and handoff-field selection. Every selected value agrees with the registered finding. The practice is relatively easy because each field is directly named; this is a difficulty preference, not an ambiguous key. |
| aws_devops.tile.098 | Pattern selection, approved-only targets, parameters, permissions and actual positive/negative target evidence are taught before judgement. The illustrative SNS sequence supports the verification distinction. |
| aws_devops.tile.099 | Desired-count reconciliation and the running/pending sequence precede checks. Wrong-item feedback separately addresses incomplete restoration and the wrong supplied cluster. The illustrative timing is not presented as guaranteed. |

No BLOCKING defects found. Tested ideas are available in preceding text, wrong-option/item feedback is supported, remediation is relevant, and visuals do not contradict the lessons or registry. There is no needs-to-understand dependence on a blocked future concept. The short tiles compress explanation, checking and application into four or five steps and roughly 3.4–3.6 minutes; this is a pacing advisory, not a recommendation to override the fixed tile plan.

## Findings

ADVISORY aws_devops.tile.089/s02: The five-step journey is estimated at 3.4 minutes, leaving little worked-example time before whole-record classification → Within the existing s02, add an annotated illustrative record showing a missed notification and explaining why recording that result honestly differs from claiming full alarm-path success; retain the fixed step types and count and re-estimate actual reading time.

ADVISORY aws_devops.tile.093/s02: The five-step journey is estimated at 3.4 minutes and moves quickly from schematic cleanup to code classification → Add a short worked contrast within s02: cleanup after the failing task in try is skipped, while scoped cleanup in finally runs; show the separate CREATED-absent/PREEXISTING-present postcheck. Retain the fixed skeleton and re-estimate reading time.

ADVISORY aws_devops.tile.094/s02: The five-step journey is estimated at 3.6 minutes, with the restore/accept/refresh-only distinction densely compressed → Add a worked approved-acceptance record within s02: live B, approved intent B, declaration changed to B, reviewed workflow completed, final live B; contrast that with refresh-only leaving the declaration unchanged. Retain the fixed skeleton and re-estimate reading time.

ADVISORY aws_devops.tile.095/s01: The four-step, 3.4-minute journey has only one compact explainer before both assessments → Add an annotated illustrative supplied interface and input → planned setting → created-instance/output comparison inside s01, explicitly marking placeholders as schematic. Retain the fixed skeleton and re-estimate reading time rather than inflating the estimate alone.

ADVISORY aws_devops.tile.096/s02: The five-step journey is estimated at 3.5 minutes and states the sizing conclusion without walking through a numeric comparison → Add the worked comparisons “Current peak: 200 ms ≤ 200 ms; smaller peak: 260 ms > 200 ms; smaller changing demand: 230 ms > 200 ms. Normal spare capacity does not override either failure.” Keep the existing steps and re-estimate reading time.

ADVISORY aws_devops.tile.097/s01: The four-step, 3.4-minute journey moves directly from a short explanation to field selection → Add a worked handoff paragraph using the registered finding ID, resource, high severity, reported suspicious activity, prompt-review urgency, mapped owner and conditional escalation. Annotate the evidence-preservation and routing decisions within the existing step; retain the fixed skeleton and re-estimate reading time.

ADVISORY aws_devops.tile.098/s01: The four-step journey is estimated at 3.4 minutes and compresses setup and target verification into one explanation → Add a worked contrast within s01 between a pattern-only pass and an approved-target notification result, preserving matching and nonmatching observations separately. Keep the fixed skeleton and re-estimate reading time.

ADVISORY aws_devops.tile.099/s01: The four-step journey is estimated at 3.4 minutes and offers little guided interpretation of the task-count sequence → Annotate the existing sequence with “running=2/pending=1 is replacement progress, not completed restoration; running=3/pending=0 restores desiredCount=3.” Retain the fixed skeleton and re-estimate reading time.

ADVISORY aws_devops.tile.089/s04: The bucket “Meets the stated verification criteria” can sound like full alarm/notification success even though i1 correctly preserves an absent notification → Rename the buckets to “Bounded experiment with honestly recorded outcomes” and “Unsafe experiment or unsupported outcome claim”; retain i1 as acceptable and the existing item-specific explanation.

ADVISORY aws_devops.tile.096/s04: The shared incorrect message refers to approved scope and missing observations rather than the sizing mistake → Replace it with “Compare each size option across all three demand periods. Both bounds must hold in every period; equality is allowed. Then select the smaller candidate’s peak and changing-demand latency cells that exceed 200 ms.”

ADVISORY aws_devops.tile.097/s03: The shared incorrect message discusses whether an outcome occurred instead of accurate handoff-field selection → Replace it with “Select the requested field from the supplied finding record. Preserve its reported value, use the accountable-owner mapping, and use the established escalation path if that owner is unavailable.”

ADVISORY aws_devops.tile.097/s01: “Suspicious activity is not an unsupported conclusion that the resource is compromised” is an awkward negation that blurs the intended contrast → Replace that sentence with “A report of suspicious activity does not by itself establish that the resource is compromised.”
