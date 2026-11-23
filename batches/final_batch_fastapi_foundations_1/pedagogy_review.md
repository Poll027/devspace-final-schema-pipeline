# Stage 08 — Independent pedagogy review

VERDICT: PASS

## Scope and method

Reviewed all 12 tiles as a conservative canary review: tile_000, tile_003, tile_005, tile_007, tile_008, tile_009, tile_010, tile_011, tile_012, tile_014, tile_015 and tile_017. Read the assembled lessons, including their learner-facing workspaces, questions, answer-specific feedback and remediation. Independently consulted the input glossary's required facts, teaching material and media summaries, and the scenario registry's examples and datasets. Applied EVALUATOR.md and Playbook principles 2.5–2.6 and the lesson contract in §5. Did not read generator reasoning or prior reviews, run deterministic validation, execute graders, or modify lesson artifacts.

No screenshots were present in the batch. Visual review therefore covers authored diagrams, tables, code walkthroughs and media bridges, not rendered layout. Video review is limited to the supplied segment summaries and bridges; it is not a claim to have watched external footage. Stated lesson durations are estimates, not measured learner completion times.

## Assessment

No BLOCKING pedagogy defects identified. Text explanations precede their checks and practices. Required distinctions are available without relying on video: origin versus endpoint access; safety versus idempotency; annotations versus runtime validation; omission versus nullable values; cleanup versus suppression; immediate versus pending awaits; definition-time decoration versus later calls; interpreter versus package inspection; server versus application responsibility; password storage versus verification; mapping versus database writes; preflight permission versus actual execution; status meanings; model conversion versus original input types; declaration capture versus reconstruction; package identity versus execution name; and independent database constraint roles.

Questions and requested learner edits can be answered from the preceding text and supplied examples. Code harness internals are explicitly designated scaffolding rather than required learner knowledge. Feedback and linked remediation provide the pertinent rule; some hints and examples could be substantially more focused. Registered origin cases, status outcomes and independent proposed-order cases support the visible examples. No contradictory authored visual was found.

Six single-concept lessons fall below the stage's 8–14-step / approximately 6–12-minute target. This is a pacing advisory, not a missing-fact or structural-integrity finding. Do not pad them with duplicate prose or change timing metadata without changing the learner journey.

## Findings

ADVISORY tile_007/s01–s05: Five steps and a 3.5-minute estimate make this core, HIGH-video-need tile shorter than the target → Expand to eight purposeful steps: separate definition-time binding and later wrapper execution into two explainers, add a definition-time trace check, and add a later-call ordering exercise using the existing decorate/function example. Re-estimate duration from the expanded lesson; keep existing taught facts and avoid unrelated decorator features.

ADVISORY tile_008/s01–s06: Six steps and a 3.9-minute estimate undershoot the target, while s01 packs environment identity and both operating systems' commands into one screen → Move the Unix and Windows walkthroughs into their own steps after the environment explanation, each clearly labelled by shell/platform; retain path-inspection checks and estimate actual completion time rather than adding redundant prose.

ADVISORY tile_009/s01–s06: Six steps and a 4.0-minute estimate undershoot the target for the ASGI lifecycle → Add a scope-versus-event matching step after s02 and an explicit response-start/body trace check after s03, using only the supplied request and response events. Re-estimate duration without requiring networking implementation or status selection.

ADVISORY tile_010/s01–s05: Five steps and a 4.2-minute estimate undershoot the target, and s01 contains storage, salt/work-factor roles and the full verification pattern together → Separate storage choice, salt/work-factor roles and pwdlib argument order into three explainers, and add one verification-order check before the existing excerpt practice. Keep all sample passwords synthetic and re-estimate duration.

ADVISORY tile_011/s01–s06: Six steps and a 3.7-minute estimate undershoot the target; s02 and s03 largely repeat the declarations already shown → Use one repeat screen for an annotated missing-primary-key contrast, then add a Base/table-name/attribute-role matching step and a repaired-declaration inspection step. Keep the practice limited to mapping, not persistence, and re-estimate duration.

ADVISORY tile_017/s01–s06: Six steps and a 4.4-minute estimate undershoot the target while s01 introduces all five constraint roles and three tables together → Separate identity/reference constraints from value/null/uniqueness constraints, then add a proposed-row rejection classification using the registered independent candidates before the SQL editing practice. Preserve the independent-against-baseline interpretation and default distinct-null UNIQUE policy; re-estimate duration.

ADVISORY tile_012/s09: The prompt duplicates ten outcome mappings already visible in the table and combines ten assignments, five class labels and editor instructions in one long reading block → Use a short lead-in, “Replace each zero with the status for its named outcome. Then label the five STATUS_CLASS patterns using the taught class names. Edit only the assignments and STATUS_CLASS comments; keep the supplied checker unchanged.” Show the outcome mappings as a compact reference alongside the editor rather than repeating them in the paragraph. Retain the comment-source editor explanation in a separate instruction callout.

ADVISORY tile_014/s01: The worked model uses note: str | None = None, but s06–s07 switch to note: str = '' without explicitly signalling the variation; each case is valid, but learners must track the change unnecessarily → Use note: str = '' in the introductory worked model too and change its expected accepted outcomes to quantity=3 and note=''. Alternatively, explicitly label the later model as a changed declaration and explain that its omitted-note default is now the empty string.

ADVISORY tile_015/s06–s07: Absolute and leading-dot imports are described verbally but lack a concrete paired syntax example → Add a small labelled comparison: “Inside service/orders.py, from service import helpers is package-qualified; from . import helpers is relative to the current package, service.” Show service/helpers.py and service/__init__.py in the example and retain python -m service.orders from the parent directory. Do not make helper behavior a new assessment requirement.

ADVISORY tile_003/s06: The container diagram links each fresh instance collection to the alternative shared class collection, making the contrast visually harder to parse despite its correct labels → Render two separately labelled panels: “Fresh per-instance state” with draft_a and draft_b pointing to separate lists, and “Shared mutable class state” with both pointing to one Draft.items list. Remove cross-panel edges and give each panel its own alt-text description.

ADVISORY tile_007/s04: The hint only says to edit learner-owned lines rather than helping with the wrapper's most likely error → Replace the hint with “Inside inner_function, return function() calls the original. Outside that inner definition, return inner_function returns the wrapper without running it.” Preserve the existing remediation rule about definition-time binding.

ADVISORY tile_012/r03: The remediation rule correctly distinguishes 500 from 503, but its worked contrast switches to 200 versus 201, an unrelated mistake → Replace the contrast sentence with “An unexpected server condition maps to 500. Temporary inability during maintenance maps to 503; temporary inability is not the same outcome as an unexpected failure.”

## Disposition

Advisory-only: PASS. The suggested expansions are pacing improvements, not an assertion that required facts are absent. No mandatory blocker replacements are needed. Rendered readability and measured completion time remain unverified.
