# Stage 08 — Independent pedagogy review

## Scope and method
Reviewed all 12 assembled tile lessons (including all checks, hands-on judgements, feedback and remediation), rather than sampling. Independently used the input glossary's required facts and teaching blocks and the five datasets in `scenario_asset_registry.json` as the teaching/evidence baseline. Applied the learner-journey criteria in `08_pedagogy_review/EVALUATOR.md` and the playbook's text-before-assessment and adaptive-remediation principles. No generator reasoning or prior evaluator findings were used; deterministic gates were not rerun.

No screenshots were present in the batch. Visual judgements therefore concern authored blocks and their registered evidence, not verified player layout or video playback.

## Review outcome
No BLOCKING pedagogy defect found. Each assessed idea has preceding text instruction; the keys are defensible from the supplied evidence. Wrong-option/item feedback identifies the relevant mistaken inference, and linked remediation supplies the relevant principle. The hands-on steps are intentionally inspect-and-judge practice, not execution labs. Their lack of a live AWS/shell runtime is not a defect.

The main instructional weakness is compressed pacing and largely declarative worked reviews. Short tiles still have a coherent explain → check → apply → recap sequence. Their brevity is advisory, not evidence that learners cannot succeed. Visuals support the operational boundaries and do not contradict the text or registry. The two video steps add concrete supporting mechanisms (response filtering; baseline-driven scan/install) and explicitly bound/correct the clips' claims; assessments remain answerable without watching.

| Tile | Steps | Authored estimate (minutes) | Journey judgement |
|---|---:|---:|---|
| aws_devops.tile.074 | 12 | 10.2 | Three separately taught evidence boundaries; heavier authorization excerpt |
| aws_devops.tile.077 | 5 | 3.6 | Sound sequence; worked review repeats the rule more than demonstrating it |
| aws_devops.tile.078 | 9 | 7.0 | Scope preview and per-target outcomes are kept distinct |
| aws_devops.tile.080 | 5 | 3.6 | Renewal and retry-outcome branches are visible and taught |
| aws_devops.tile.081 | 4 | 3.2 | Role distinction precedes allowed/denied-operation judgement |
| aws_devops.tile.082 | 4 | 3.2 | Preventive/detective distinction precedes result interpretation |
| aws_devops.tile.083 | 6 | 4.3 | References, protection and refresh caveat precede their checks |
| aws_devops.tile.084 | 5 | 3.6 | Artifact continuity, service authority and failure path are explicit |
| aws_devops.tile.085 | 4 | 3.4 | Per-target verification is taught; record presentation is dense |
| aws_devops.tile.086 | 6 | 5.3 | Evidence-localization and bounded correction precede judgement |
| aws_devops.tile.087 | 5 | 5.5 | Approved task bounds and per-node evidence precede judgement |
| aws_devops.tile.088 | 4 | 3.3 | Selector/port/endpoints/client evidence precedes judgement |

## Findings
All findings below are ADVISORY. Preserve the deterministic plan's step types/order; do not replace read-and-judge practice with implementation or submission tasks. Pacing improvements should add useful worked observation within existing explainers, not pad prose or merely increase the estimate. The 8–14-step target is a future planning consideration, not permission to alter the fixed skeleton in this review round.

ADVISORY aws_devops.tile.074/s07: The successful authorization review embeds a long columns/rows JSON array inside one classification item, making identity/action/path/result comparison unnecessarily effortful → Present the same three registered records as three labelled, line-broken test records; retain policy scope and grants/denies evidence and all existing assignments.
ADVISORY aws_devops.tile.085/s03: Fifteen-column positional JSON forces learners to decode field positions before making the intended per-target judgement → Present the same four registry rows as labelled per-target records grouped into caller/profile/Region, stack/bucket verification, and absence-check evidence; retain every field and the explicit alternative-case label for e1.
ADVISORY aws_devops.tile.083/s01: The YAML reference example compresses both configuration and secret references into one long inline env array → Expand env into two multiline entries so each object name/key and valueFrom reference can be inspected separately; point each annotation at its own entry.
ADVISORY aws_devops.tile.077/s02: The worked review restates general instructions instead of demonstrating a saved-plan decision → Work through the already introduced retained-resource deletion: identify its resource/action, compare it with the retention criterion, and model the evidence-backed BLOCK record without applying the plan.
ADVISORY aws_devops.tile.078/s03: The hint is generic and does not direct attention to the easily misread DryRunOperation response → Replace the hint with “Separate permission-check evidence from a real operation result: was mutation enabled in this request?”
ADVISORY aws_devops.tile.077/s01: Five steps and 3.6 estimated minutes are below the requested journey range → Add guided observation of the existing four-action illustrative plan before its review annotations; retain the planned steps and reassess realistic reading/decision time after authoring.
ADVISORY aws_devops.tile.080/s02: Five steps and 3.6 estimated minutes leave little worked practice between instruction and assessment → Expand the existing completed/unresolved comparison into two short labelled outcome records and explain the different repeat decisions, within s02.
ADVISORY aws_devops.tile.081/s01: Four steps and 3.2 estimated minutes compress the role lesson into one explainer → Add a concrete two-field task-definition excerpt and walk through which role owns one startup result versus the application allowed/denied results, within s01.
ADVISORY aws_devops.tile.082/s01: Four steps and 3.2 estimated minutes provide only a brief baseline distinction → Add a guided reading of the existing fictional preventive and detective checkpoints, explicitly comparing what each result does and does not establish, within s01.
ADVISORY aws_devops.tile.083/s02: Six steps and 4.3 estimated minutes are short for the reference/protection/refresh journey → Add a worked nonsecret consumer-evidence comparison for the existing running-container refresh caveat, within s02; keep secret values hidden.
ADVISORY aws_devops.tile.084/s02: Five steps and 3.6 estimated minutes leave artifact continuity mostly abstract → Walk through a labelled SourceArtifact → CodeBuild → BuildArtifact → CodeDeploy record for revision-A and contrast one mismatched input, within s02.
ADVISORY aws_devops.tile.085/s01: Four steps and 3.4 estimated minutes are short for a multi-target evidence review → Guide the reading of one approved registry record and one unapproved record, then explain why each remaining target needs independent evidence, within s01.
ADVISORY aws_devops.tile.086/s02: Six steps and 5.3 estimated minutes fall below the approximate journey target → Expand the existing diagnosis into a short evidence-elimination walkthrough (DNS, used route, request permission, response denial) before the bounded correction/retest, within s02.
ADVISORY aws_devops.tile.087/s01: Five steps and 5.5 estimated minutes offer a compressed patch-result journey → Guide comparison of the existing fictional node A and node B execution/compliance records and explain why their shared task does not imply a shared outcome, within s01.
ADVISORY aws_devops.tile.088/s01: Four steps and 3.3 estimated minutes compress configuration and traffic verification → Add a concrete selector/port/targetPort excerpt using the later supplied sandbox-app, 80 and 8080 values, then walk through endpoint and client evidence, within s01.

VERDICT: PASS
