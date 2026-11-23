# Stage 08 — independent pedagogy review

VERDICT: PASS

No BLOCKING defects found. The findings below are ADVISORY; this is not a claim of measured completion time or rendered-player usability.

## Scope and method

Reviewed all 12 assembled lessons in `tile_lessons/`, including text, visual payloads, public interactions, keys and wrong-option/item feedback, code-workspace instructions, conditional remediation, recaps, and the two video segments and their bridges. Used the frozen `inputs/path_glossary_bundle.json` and `scenario_asset_registry.json` as independent teaching and example references. Applied EVALUATOR.md and Playbook §§2, 5 and 7. Did not inspect generator reasoning, repair scripts, previous evaluator claims, or re-run deterministic gates.

No screenshots were present in the batch. Visual judgments concern authored content and correspondence to text, not actual layout, clipping, or interaction rendering. Video judgments use the supplied segment summaries and bridges; footage was not independently played. The 6–12-minute target cannot be confirmed without learner timing.

## Learner journeys

| Tile | Journey assessment |
|---|---|
| tile_082 | Build/release/run, immutable records and rollback/schema boundary are explicitly taught before selection and procedure practice. Release example agrees with registered compatibility evidence. Compact journey; procedure practice largely supplies its own answer structure. |
| tile_083 | Separate documentation and safe-error cycles each explain before checking and reviewing candidate tests. Status/schema comparisons and public/internal evidence separation support the text. Wrong-option feedback distinguishes declaration from implementation and debug disclosure from internal diagnostics. |
| tile_085 | Transport/status distinction and explicit local mapping precede checks and implementation. The supplied 503/timeout mapping is identified as local policy, not universal forwarding. Second explainer is a reminder, not a worked example. |
| tile_086 | Raw bytes, supported verifier and processing gate precede check and candidate review. The independent valid/modified/absent cases make the processing boundary visible. Candidate review tests application of taught rules, although it is less demanding than writing a gate. |
| tile_087 | Operation-window signals and correlated timeline precede diagnosis. Registry data support unchanged rate, increased failure fraction/latency, completed database work and the outbound delay. Feedback and remediation direct investigation to evidence rather than the final endpoint error. |
| tile_088 | All independent resource budgets are explicit before checks and policy review. Early-rejection evidence supports the text. Reading load is concentrated in one large code block; the short second screen does little to relieve it. |
| tile_089 | N+1, selectinload, joinedload/unique and SQL/data comparison are taught before checks and executable practice. Captured baseline and illustrative revised pattern are clearly distinguished. Video adds a separate eight-movie, nine-to-two worked demonstration; its synchronous-execution bridge preserves the boundary. Large duplicated code panels and the 7:51 clip put timing at risk. |
| tile_090 | Yield lifecycle, outer transaction/savepoint session, provider override and cleanup are taught before checks and fixture review. Video adds a concrete lifecycle demonstration; bridge explicitly distinguishes table creation/drop from the taught transaction-isolation workflow. Remediation is relevant but could name outer rollback more directly. |
| tile_091 | Issuer acquisition/verification is taught and checked before the separate operation-permission cycle. Forward scope names in configuration are passing references, not an earlier scope-understanding requirement. Candidate feedback differentiates integration from overridden verification, and authenticated credentials from sufficiently scoped credentials. Diagram and review-packet configuration dumps are cumbersome. |
| tile_093 | Three explain/check/apply cycles keep idempotency, freshness and retries distinct. Registered event/timestamp examples support the text; inclusive freshness boundaries are shown before being tested. Practice instructions state commit/confirmed-duplicate handling and configuration-only retry simulation explicitly. Three hands-on tasks, including a large supplied transaction harness, likely need more time than a typical short tile. |
| tile_096 | Specific-object authorization and trusted-owner selection precede both checks and lookup implementation. Four retrieval combinations agree with registered owners. Retrieval-only practice does not contradict the wider taught prohibition on cross-owner changes. Compact journey with appropriate difficulty progression. |
| tile_097 | Deployed security declarations, public contract audit and security-test design each receive their own teaching cycle before application. Captured conflict-status drift, public examples and operation requirements provide relevant audit evidence. Denial matrix agrees with the registry and is explicitly a local contract. Repeated JSON and long review packets dominate reading time. |

Across the batch, checks can be answered from preceding text and visible examples without relying on video. Several screens cover multiple related rules, but the rules are explicit rather than hidden. No reviewed visual contradicts its accompanying text. Wrong-option/item feedback addresses the relevant misconception. Recap/up-next references do not require understanding later concepts to succeed.

## Findings

ADVISORY tile_082/s02: The nominal walkthrough merely restates a boundary, leaving the compact journey without a worked rollback decision → Replace its prose with: “release_prior_compatible records artifact_prior_compatible with config_prior_compatible and is compatible with schema_current. Select that recorded pair for rollback. Do not select release_prior_incompatible, and leave schema_current unchanged.” Keep s03 as the independent check.

ADVISORY tile_082/s04: The procedure prompt repeats the full answer structure after specifying each field, increasing reading without increasing application → Supply the dictionary skeleton once in the workspace, retain the no-mutation and compatible-prior-selection requirements in the prompt, and remove the second full dictionary from the prompt.

ADVISORY tile_085/s02: The second explainer is a reminder rather than the promised worked boundary → Walk through the fixture explicitly: “For the supplied upstream 503, raise_for_status() yields HTTPStatusError; inspect its response status and map it to the declared local 502 detail. For the supplied timeout, catch RequestError and use the declared local 504 detail. Neither outcome exposes the remote internals.”

ADVISORY tile_086/s02: The short reminder does not scaffold the transition from recognizing a signature failure to reviewing a full test packet → Add a compact worked sequence: unchanged signed bytes → verify → process once; changed bytes with original signature → reject → zero processing; absent signature → reject → zero processing. State that the recorder is cleared for each case.

ADVISORY tile_087/s02: The second screen repeats a rule instead of interpreting the adjacent evidence, making the diagnosis journey unusually compressed → Explain that both windows show 1 request/second, while failure fraction rises from 0 to 0.2 and latency from 25 to 2025 ms; then trace the outbound wait from offset 10 to 2010 ms. Keep the conclusion as a supported investigation boundary, not proven root cause.

ADVISORY tile_088/s01: Definitions, application setup, deployment policy and a full parametrized test appear in one lengthy code walkthrough → Separate the display into named body/batch enforcement, timeout/concurrency settings, and rejection-evidence panels. Show only the lines needed for each boundary, with the full scaffold available separately; reuse the existing short s02 for one concrete accepted-versus-rejected example.

ADVISORY tile_089/s01: Before/after panels repeat almost the entire schema and setup, while the 7:51 video leaves little of a 6–12-minute budget for checks and coding → Display shared setup once and compare only the listing function, changed options line, SQL pattern and returned collections. Make the video clearly optional/reinforcing and measure the text-plus-code route before assigning a completion estimate.

ADVISORY tile_090/r01: Remediation mentions lifecycle and cleanup but leaves the outer rollback implicit even though s04 explicitly asks what teardown lacks → Add: “Closing the Session is not the outer-transaction rollback. Teardown must close the test session, roll back outer_transaction, close connection, then clear and restore the saved dependency overrides.” Retain the fresh-test absence check.

ADVISORY tile_091/s01: A process-flow node contains the full issuer configuration JSON, making the acquisition path harder to scan than the text → Replace n0’s label with “Supplied registered client, issuer endpoints and redirect URI”; present the unchanged configuration in a separate labeled reference panel. Use short flow labels for acquisition, presentation and verification, leaving s02 to explain verification settings.

ADVISORY tile_093/s04: The first of three hands-on tasks exposes a large supplied transaction/concurrency harness immediately after a compact conceptual explanation, creating a steep reading and timing ramp → Put the editable handle_authenticated_event function first, add a short map of the supplied transaction facade and snapshot checks, and place unchanged harness code in a clearly labeled reference view. Explain that the learner edits only the handler. Measure this task separately when estimating total tile time; do not omit duplicate, concurrent, restart or failure cases.

ADVISORY tile_093/s09: The shared hint about inputs/decision/output does not help distinguish expired timestamps from excessive future offsets → Replace the hint with: “Compute age = receiver_now - int(signed_delivery_timestamp). Past deliveries have positive age; future deliveries have negative age. Check both inclusive bounds using the supplied acceptance_window and future_tolerance.”

ADVISORY tile_096/s01: The compact lesson has enough teaching to answer its checks, but no worked trusted-owner lookup before code completion → Add one short example after the matrix: “For caller_a requesting 202, select by id=202 and owner_id=caller_a together. Order 202 belongs to caller_b, so the lookup returns no permitted order. A caller-supplied owner_id must not replace the trusted principal.”

ADVISORY tile_097/s09: Five review items repeatedly inline large schemas, security configurations and HTTP packets, making the audit task primarily a rereading exercise → Show one shared labeled evidence packet and let each item cite its relevant section (input/output, duplicate status, security, examples). Preserve all concrete evidence and each independent proposed conclusion; remove only repeated copies. Likewise, let s13 reference the already displayed local denial matrix instead of serializing it again inside its good candidate.

## Disposition

Content verdict: PASS, advisory-only. No pinned blocking replacement is necessary. The pacing and presentation changes above should preserve all taught facts, policy boundaries and required evidence; they are not requests to change deterministic step plans or remove coverage.
