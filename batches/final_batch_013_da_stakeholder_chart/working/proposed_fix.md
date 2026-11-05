# Proposed Fix

## Issue
The ledger verification failed because `screens.json` was modified after stage 03_screens was gated. This happened when stage 04_interactions discovered untaught facts and sent them back to the screens generator for repair.

## Root Cause
This is a **code** issue in the pipeline logic. When 04_interactions triggers a screens repair (line 22-23 in driver.log: "2 fact(s) not taught by text; sending them to the screens generator"), it modifies screens.json but does NOT:
1. Re-run the 03_screens gate/evaluator to verify the patched screens
2. Update the ledger entry for 03_screens with the new hash and timestamp

## Fix Required
The pipeline code needs to be modified so that when 04_interactions triggers a screens repair:

1. After the screens generator patches screens.json, the 03_screens evaluator must be re-invoked
2. The 03_screens gate must pass again with the updated artifact
3. The ledger entry for 03_screens must be updated with the new hash and gated_at timestamp

**Location**: The fix should be in the 04_interactions stage handler, specifically in the logic that handles "generator repair" when facts are not taught by text.

**Specific change**: After calling the screens generator to patch in the missing facts (around line 23 of driver.log), the code should:
- Re-evaluate screens.json using the 03_screens evaluator
- Update the gate status for 03_screens
- Update the ledger entry for 03_screens before proceeding

This ensures the ledger remains consistent and all gated artifacts reflect their current state.
