# Devspace Final Schema Pipeline

Turns a path's Glossary Learning Bundles into validated tile lessons (screens, visuals, interactions, answer keys, datasets) for the player. Role-agnostic: the same scripts run every path; per-role differences are data (registry/path_profiles, asset registry, packs).

To run or continue a batch follow `01_FINAL_PACK_TEMPLATE/START_HERE.md` exactly. New role: `01_FINAL_PACK_TEMPLATE/NEW_ROLE_RUNBOOK.md`. You are the orchestrator: dispatch stage work to the `final-generator` and `final-evaluator` subagents and run scripts; don't author content in your own context.

The spec is `00_FINAL_PIPELINE_CORE/PLAYBOOK.md`. Never edit frozen TOC workspaces or glossary bundles. Never hand-edit a ledger — `update_ledger.py` owns it. After any schema/checker change run `scripts/selftest.py` (must report 0 missed).
