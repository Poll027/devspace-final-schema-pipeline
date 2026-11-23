# Stage 08 — Independent pedagogy review

Batch: `final_batch_verification_1`

## Scope and method

Reviewed all 12 tiles (15 concepts), rather than taking a later-rollout sample: the dispatch does not identify a sampling phase, and the batch includes core concepts, HIGH video need and multi-concept tiles. Read the full assembled lesson journeys, public exercise workspaces, checks, feedback and remediation. Re-derived the taught boundaries from `inputs/path_glossary_bundle.json` and the fictional scenario/fixtures in `scenario_asset_registry.json`. Applied `08_pedagogy_review/EVALUATOR.md` and Playbook §§2, 5 and 7. Did not inspect generator reasoning or prior evaluator reports, alter generator artifacts, or rerun deterministic gates.

This is a source-level pedagogy review. No rendered screenshots were supplied; video judgments use the glossary's segment summaries and bridges, not direct playback. Native shutdown execution and player rendering were not performed.

## Journey assessment

| Tile | Main steps | Authored minutes | Assessment |
|---|---:|---:|---|
| tile_039 | 6 | 3.9 | Source declarations and model conversion precede the check and signature edit; the extra walkthrough largely repeats the source map. |
| tile_040 | 5 | 3.5 | Acquisition, cleanup, scope and failure visibility are explicitly taught before the combined check. The practice clearly identifies its supplied scope model. |
| tile_041 | 5 | 3.6 | Event attributes, reserved names and formatter preservation are taught before checking or configuring logging; full duplicated scaffolding burdens the visual. |
| tile_042 | 6 | 4.3 | Allowlisting, public addresses, connected-address validation and redirects precede checks; the coding task correctly limits its claim to destination selection. |
| tile_043 | 5 | 3.9 | Multipart declarations, total versus parser limits, validation and cleanup are explicit, but concentrated heavily in the first screen. |
| tile_044 | 5 | 3.5 | Defaults, explicit credential permissions and the separate endpoint-access boundary precede practice. |
| tile_045 | 12 | 9.8 | Request-local reuse is applied before the separate endpoint-testing concept is introduced. Tests have prior text support. The video adds a concrete payload-change/failing-test demonstration. |
| tile_047 | 11 | 7.6 | Presence versus null is taught and applied before OpenAPI navigation begins. Both component references and component definitions are explained. |
| tile_049 | 4 | 3.1 | Host policies and redirects precede the check; the comparison matches the authored host fixture. Very compressed. |
| tile_050 | 4 | 3.2 | Main-message and supplemental-context inspection precede verification; the masking fixture retains its event field. Visual code duplication dominates the short journey. |
| tile_051 | 7 | 7.7 | Factory versus mutable-session ownership is taught before context/yield practice. The video supplies concrete setup syntax and distinguishes factory naming; text independently covers concurrency and exceptional cleanup. |
| tile_052 | 8 | 6.9 | Shutdown verification precedes the distinct probe contract; YAML nesting is taught before editing. In-process cleanup is explicitly distinguished from required native termination evidence, but external setup is not budgeted clearly. |

No reviewed check required an untaught boundary. The supplied runtime adapters and no-I/O fixtures are infrastructure the learner need not understand to complete the declared edits; they were not treated as future-concept blockers. Multiple facts on a screen are generally explicit facets of one boundary, not hidden second ideas. Remediation addresses the tested distinctions, even where generic inline hints are weak. No blocking visual contradiction or registry disagreement was identified in this review.

The short step counts and minute estimates below are pedagogical pacing advisories, not renewed schema-gate findings. Do not pad journeys with repeated prose or count conditional remediation as main-path teaching time.

## Findings

ADVISORY tile_039/s02–s03: The main journey has six steps and a 3.9-minute estimate; both walkthrough paragraphs repeat the source map without tracing an actual request → Replace s03's repeated paragraph with a worked POST `/customers/42/orders?option=standard` and JSON `{"quantity":"2"}` trace, showing path `customer_id=42`, query `option='standard'` and model `body.quantity=2`; distribute declaration, source mapping and conversion into eight purposeful main-path steps and re-estimate toward 6–12 minutes.

ADVISORY tile_040/s01–s04: Five steps and 3.5 minutes compress resource ownership, exception visibility and two cleanup timings into one first-screen explanation followed by a combined check → Split the existing explanation into acquisition/yield, finally plus unhandled-exception visibility, and a request/function timing comparison; add a guided success/failure trace before the current check to reach at least eight purposeful steps, then re-estimate learner time.

ADVISORY tile_041/s01–s04: Five steps and 3.6 minutes provide little guided practice between the formatter example and the editing task → Separate event-field selection, attachment with extra, and formatter preservation; add a guided field-to-placeholder match and emitted-record inspection to reach eight purposeful steps, then re-estimate toward 6–12 minutes.

ADVISORY tile_041/s01: The before/after visual repeats almost all logger setup code, making the meaningful formatter/extra changes hard to locate → Show only the changed formatter and logger.error lines in the comparison; retain complete setup in the supplied workspace and add the resulting six-field emitted line directly below the comparison.

ADVISORY tile_042/s01–s05: Six steps and 4.3 minutes compress three trust boundaries and redirect enforcement into an initial list; two checks then precede a comparatively easy dictionary edit → Add a guided approved-provider/public-address trace and a guided forbidden redirect or IPv6 loopback trace, retaining the explicit 'destination selection only' practice boundary; aim for eight main-path steps and re-estimate toward 6–12 minutes.

ADVISORY tile_043/s01–s04: Five steps and 3.9 minutes place five controls and two code walkthroughs on the first screen, then jump to an endpoint with several edits → Distribute the existing material across declaration/spooled-file, total-byte budget, parser limits, and validation/cleanup screens; add a worked 415/422/413 rejection comparison before practice so the journey reaches eight purposeful steps, then re-estimate its duration.

ADVISORY tile_044/s01–s04: Five steps and 3.5 minutes leave only a repeated paragraph between the initial configuration and a combined defaults/access-boundary check → Add a defaults-versus-shop-client comparison, an explicit-list/wildcard correction example and a browser-permission-versus-endpoint-check scenario, keeping endpoint access checks separate; use eight purposeful steps and re-estimate toward 6–12 minutes.

ADVISORY tile_045/s11: A six-line endpoint test task is embedded in a 138-line editable file with adapter and verification internals; the lengthy prompt foregrounds implementation caveats over the test being learned → Move unchanged adapter and verifier internals to supplied read-only support files, leave the fixture and a clearly marked test_get_order TODO in the editable file, and put the WASM/native explanation in a separate infrastructure note. Retain the HTTP request, lifespan and independent status/JSON requirements.

ADVISORY tile_047/s05: The editable test workspace begins with roughly 40 lines of threadless-client infrastructure before the note declarations and test TODO, interrupting the presence/nullability exercise → Move unchanged client adapter and verification functions into supplied read-only support files; begin the editable file with the two model/route fixtures and clearly marked test_required_note and test_default_note TODOs. Keep all three request bodies and their separate status/payload expectations.

ADVISORY tile_049/s01–s03: Four steps and 3.1 minutes jump directly from the entire policy table to checking and configuring middleware → Add a worked exact-domain versus subdomain-wildcard comparison, an all-host-wildcard counterexample, a redirect-versus-rejection trace and a guided policy edit, reaching eight purposeful steps; re-estimate toward 6–12 minutes without inventing an unspecified redirect status.

ADVISORY tile_050/s01–s03: Four steps and 3.2 minutes provide no guided record inspection between the complete formatter implementation and writing verification assertions → Add separate policy, message/context inspection, preserved-event and guided assertion screens using the supplied synthetic values; reach eight purposeful steps and re-estimate toward 6–12 minutes.

ADVISORY tile_050/s01: The before/after visual duplicates the whole formatter/harness implementation and does not directly display the emitted-record contrast → Keep unchanged scaffolding in the supplied workspace, highlight only the masking change, and display the unsafe synthetic record beside `synthetic failure token=[REDACTED] context=connection=[REDACTED] token=[REDACTED] event=order_failure`. Label both as outputs of this fictional fixture, not a general proof of production redaction.

ADVISORY tile_051/s02–s03: The seven-step journey has suitable overall time but two adjacent paragraphs repeat factory/session ownership before the video → Replace s03's repeated walkthrough with an annotated code example `session_factory = async_sessionmaker(engine)` and `async def get_session():` containing `async with session_factory() as session:` then `yield session`; add a separate normal-versus-exceptional ownership trace to reach eight purposeful steps while retaining concurrency text independently of video.

ADVISORY tile_052/s03: The 6.9-minute tile estimate does not distinguish in-player edits from saving files, preparing a native environment and running the required SIGTERM harness → Add a preflight note listing a native Python environment with FastAPI, Uvicorn and httpx installed, require exercise.py and termination_harness.py in the same directory, and give the command `python termination_harness.py`; display separate in-player and native-lab time estimates measured with the prepared environment. Keep the requirement for actual active-request termination evidence unchanged.

## Verdict

Blocking defects: 0. Advisory findings: 14.

VERDICT: PASS
