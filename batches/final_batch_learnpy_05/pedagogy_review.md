# Stage 08 — Independent pedagogy review

**Batch:** `final_batch_learn_python.region.05`  
**Verdict:** PASS  
**Defects:** 0 BLOCKING; 13 ADVISORY.

## Scope and method

Reviewed all ten assembled `tile_lessons` (69 main steps), including their text, visual specifications, media summaries/bridges, learner workspaces, questions, option/item feedback, hints and remediation. Re-derived the instructional requirements from `inputs/path_glossary_bundle.json` and the examples from `scenario_asset_registry.json`. Applied the stage evaluator and Playbook §§2, 3 and 5. Did not inspect generator reasoning or rerun deterministic validation/execution gates.

This is a source-content review, not a screenshot or live-player review: no rendered player was supplied. Runtime assertions below are not based on assumed filesystem persistence or unobserved player behavior. The classify exercises for runtime/environment/dependency concepts were assessed as read-and-judge practice, not as execution labs.

## Overall judgment

The text precedes the checks for each concept. The required distinctions are explicit, and learners can answer the questions from that text without watching video. Reviewed choices and classification excerpts have defensible keys, with option/item-specific feedback that explains the relevant error. Remediation generally revisits the appropriate distinction. The diagrams and code walkthroughs support their accompanying explanations; no contradictory visual was found. Video groups supply concrete demonstrations or alternate examples, with bridges identifying what remains the responsibility of the text.

The main weakness is the difficulty ramp: several live-code exercises leave only assignment/printing to the learner while the fixed scaffold performs the concept-specific work. This is a scaffolding and wording issue, not a finding that learners cannot succeed, and not a request for external labs. Keep the planned interaction types and step skeletons. In particular, retain the read-and-judge activities in the final two tiles.

### Pacing observations

| Tile suffix | Main steps | Authored estimate |
|---|---:|---:|
| 084_084 | 4 | 3.2 min |
| 085_086 | 9 | 13.5 min |
| 087_087 | 6 | 4.3 min |
| 088_089 | 9 | 11.6 min |
| 090_090 | 5 | 4.0 min |
| 091_091 | 5 | 4.0 min |
| 092_092 | 6 | 5.7 min |
| 093_093 | 5 | 3.5 min |
| 094_096 | 13 | 10.9 min |
| 097_098 | 7 | 6.5 min |

The short-tile departures from the approximate 8–14-step/6–12-minute review target are advisory planning/pacing observations, not structural blockers. They are included in the tile-specific findings below. Do not pad the lessons or alter the deterministic skeleton to hit a number; strengthen worked examples within existing steps and keep duration estimates honest.

## Findings

ADVISORY learn_python.tile.084_084/s01: Four steps and 3.2 estimated minutes compress parsing, format selection, timedelta and signed arithmetic into one explanation; the code has no displayed outcomes to anchor the sign discussion → Add the opening sentence “The order report needs the signed number of days between two supplied calendar dates.” Group the existing blocks under “Parse the dates” and “Compare the dates”, and add a worked-output prose block: “first is 2025-03-01 and second is 2025-03-04. (second - first).days is 3; reversing the subtraction gives -3.” Preserve the planned steps and recalibrate duration only after the actual additions.

ADVISORY learn_python.tile.085_086/s02: The two clips total 6 minutes 21 seconds, contributing to a 13.5-minute tile; the bridge recommends both before the learner reaches a first check → Replace the bridge's before text with “The first clip demonstrates creating a separate helper file and making module-qualified calls. The second offers an additional example and compares module-qualified calls with direct imports. The text already teaches both import forms; use the additional example if that distinction is still unclear.” Keep the registered segments unchanged.

ADVISORY learn_python.tile.085_086/s08: The lede asks the learner to group files and call through the package name, but the fixed scaffold creates the package, imports it and binds a direct cost name; the learner only calls that binding → Replace the lede with “Inspect the supplied orders package and its import, then call the imported cost helper.” In the prompt, identify “orders is the package; costs is its module; cost is the helper” before asking for result and its display. Do not claim that this learner edit creates the package layout.

ADVISORY learn_python.tile.087_087/s01: A six-step, 4.3-minute tile places logger identity, five levels, methods, thresholds and propagation in one explanation, while s02 repeats the propagation rule → Keep the existing rules but group them visibly as “Name the source”, “Choose a level”, and “Control output”. Replace s02's repeated prose with “An INFO event reaches the module logger's handler and then an ancestor handler when propagation is enabled. Those two handlers can display the same event twice. Keeping one suitable ancestor handler avoids that redundant route.” This earns the second explanation without changing its type or introducing handler-construction syntax.

ADVISORY learn_python.tile.087_087/s05: The lede promises replacement of diagnostic prints, but all event methods and application configuration are fixed; the edit is only logger = _module_logger, and the success feedback calls it a judgement → Replace the lede with “Connect the supplied module logger to the fixed report helper, then inspect which events the INFO configuration includes.” Replace success feedback with “The report uses the module logger. INFO includes completion once, excludes DEBUG detail, and no redundant module handler was added.” Keep adapter code fixed and make the hint explain the role of the module logger rather than merely repeating the assignment.

ADVISORY learn_python.tile.088_089/s08: The stretch-labelled practice prompt spells out all three assignments and then fixes declarations, parsing and printing; it functions as transcription rather than a difficulty increase → Replace the prompt's first two sentences with “Choose the supplied strings for the required positional argument's name, the optional flag's name, and the flag action. Complete positional_name, option_name and option_action so input_path is required and --verbose is selected by presence.” Retain the existing skeleton and case requirements, and move the explicit three assignments to the hint ladder rather than the initial prompt.

ADVISORY learn_python.tile.090_090/s04: The five-step, 4-minute tile's application immediately supplies the required repaired filename, so it is largely a rename task rather than evidence-led diagnosis → Replace the prompt opening with “Run the supplied diagnostic before editing the first line. Compare the search locations with json.__file__: does the imported file come from the project or the standard library? The first-line Workspace filename controls the local file created by the fixed adapter. For this exercise, rename the conflicting local module to report_data.py, retain the diagnostic imports and prints, and compare the imported location after the repaired run.” Keep the explicit required filename for the existing grading contract; do not require a new submission route.

ADVISORY learn_python.tile.091_091/s04: Five steps and 4 estimated minutes culminate in a supplied lookup and supplied absence check; the lede suggests the learner implements those operations, and generic feedback does little to consolidate the empty-string distinction → Replace the lede with “Use the supplied environment lookup, preserve its explicit absence check, and display the resulting value.” Replace success feedback with “A configured string is displayed unchanged. None triggers the missing-configuration message; a configured empty string does not.” Add a short explanation within the current step: “Why is None checked instead of truthiness? Empty text is configured text, not an absent key.”

ADVISORY learn_python.tile.092_092/s05: In this six-step, 5.7-minute tile the prompt explicitly supplies seed = initial_seed, while the scaffold performs all draws, reseeding and comparisons; the only remaining substantive edit is printing → Replace the assignment-giving sentence with “Use the supplied seed value for seed, then inspect the fixed skeleton: it draws twice, resets that same seed, and repeats the draws without intervening random calls.” Add a worked explanation after the requirement: “The reset replays the sequence; merely continuing to draw would advance it instead.” Retain the four requested output lines and the fixed scaffold, and describe the task as completing and inspecting a seeded demonstration rather than building a generator workflow.

ADVISORY learn_python.tile.093_093/s04: The five-step, 3.5-minute tile's two candidate variable names announce which pattern is correct, reducing practice to choosing the name nonempty_uppercase → Rename the supplied candidates neutrally to pattern_a and pattern_b throughout the learner-facing starter and prompt, retaining their values r'[A-Z][A-Z]*' and r'[A-Z]*'. Ask “Choose pattern_a or pattern_b so an uppercase label must contain at least one character.” Keep the fixed fullmatch loop and existing expected outcomes. Retain the explanation about the first required character in the hint, not in candidate names.

ADVISORY learn_python.tile.094_096/s05: s05 repeats s04's activation and inspection statements, and s09 similarly repeats s08's rerun rule; these second explainers add little to a 13-step journey → Replace s05 prose with “Case: .venv was created, but diagnostic.py is run with the base Python. Creating an environment does not make every subsequent command use it. Invoke the environment executable explicitly, check that its prefix comparison is True, and list packages through that same executable.” Replace s09 prose with “Case: the editor label now says .venv, but no new run has occurred. That label records a selection, not a runtime observation. Rerun the program and compare its executable path with the intended path, then check the prefix comparison.” Preserve step types and existing facts.

ADVISORY learn_python.tile.097_098/s03: The installation and recreation transcripts use literal-looking package_name, module_name and version tokens while describing successful installation; the glossary presents these as illustrative placeholders, which is not explicit in these practice prompts → Add to both s03 and s06 prompts: “These are schematic transcripts. package_name, module_name and version stand for verified project-specific distribution, import and version values; they are not literal names or a version string to install. Judge interpreter consistency and the supplied verification evidence.” Keep the read-and-judge format and keys; do not ask learners to run these schematic commands.

ADVISORY learn_python.tile.097_098/s06: The seven-step tile meets the approximate time target but has fewer steps than the stage's nominal range, and the stretch activity repeats the same-interpreter distinction already checked in s03 with only missing-check and wrong-interpreter failures → Within the existing classify step, add a fourth independent excerpt using the intended interpreter for all commands but showing that pip list reports a version different from the documented pin. Classify it as fails and add item feedback “The commands use the correct interpreter, but the listed version does not match the recorded pin.” Use explicitly schematic distinct version tokens with their relationship stated in the prompt, so the learner judges pin agreement without new package knowledge. Do not add a new planned step or an execution lab.

## Disposition

No BLOCKING defect was identified. The advisories improve chunking, honest task descriptions, practice discrimination and pacing. Fixed adapter internals and passing mentions of later topics were not treated as needs-to-understand leakage.

VERDICT: PASS
