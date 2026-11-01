"""
Patch interactions.part.c0_canary.json for REPAIR ROUND:
BLOCKING: s06 – add Accuracy check category + accuracy follow-up task to instructions/feedback
ADVISORY s05: clarify hypothetical scenario
ADVISORY s15: revise opt_s15_c feedback
ADVISORY s17: strengthen feedback to address limitation/re-identification
"""
import json, copy

SRC = "batches/final_batch_007_da_nocode/interactions.part.c0_canary.json"

with open(SRC) as f:
    data = json.load(f)

tile = data["tiles"][0]
interactions = tile["interactions"]

def find_ix(step_id):
    return next(i for i in interactions if i["step_id"] == step_id)

# ── BLOCKING: s06 ──────────────────────────────────────────────────────────────
s06 = find_ix("tile_data_quality_and_workflow.s06")
ix06 = s06["interaction"]

# 1. Add Accuracy check category
ix06["public"]["categories"].append({
    "category_id": "cat_accuracy",
    "label": "Accuracy check"
})

# 2. Update instructions to include accuracy reflection task
ix06["public"]["instructions"] = (
    "The delivery-orders table has three quality problems. "
    "Click each problem cell or row and assign it to the check it fails. "
    "Find all three to complete the exercise. "
    "Then, for the Accuracy check: consider the remaining records — "
    "state what real-world information (for example, GPS logs or customer confirmation) "
    "would be needed to verify that the city and delivery-time values are accurate."
)

# 3. Update completion_message to address accuracy
ix06["grading"]["completion_message"] = (
    "You found all three quality problems: a missing value (completeness), "
    "a duplicate row (uniqueness), and an impossible value (validity). "
    "For accuracy: to confirm that city and delivery-time values are correct, "
    "you would need real-world evidence such as GPS delivery logs or "
    "customer confirmation — accuracy cannot be verified from the data alone."
)

# 4. Update feedback to address accuracy
ix06["feedback"]["correct"]["message"] = (
    "Well done. You identified all three quality problems: the missing delivery time "
    "(completeness), the duplicate order row (uniqueness), and the negative delivery time "
    "(validity). For accuracy: to confirm that recorded cities and times match reality, "
    "you would need external evidence such as GPS logs or customer confirmation — "
    "accuracy cannot be checked from the data alone."
)
ix06["feedback"]["incorrect"]["message"] = (
    "Keep looking — there are three problems in total. Check for a missing value, "
    "a repeated row, and a value that is outside the valid range. "
    "Once you find them, also think about what real-world information would be needed "
    "to verify accuracy of the remaining records."
)
ix06["feedback"]["hints"].append(
    "For the Accuracy check: what external source (GPS logs, customer confirmation) "
    "would tell you whether the city and delivery-time values are correct?"
)

# ── ADVISORY: s05 – clarify hypothetical scenario ─────────────────────────────
s05 = find_ix("tile_data_quality_and_workflow.s05")
ix05 = s05["interaction"]
# Update prompt to clarify this is a hypothetical scenario
ix05["public"]["prompt"] = (
    "Order 1006 has delivery_minutes = −5. "
    "In a hypothetical scenario, Order 1007 is logged as delivered to Lagos, "
    "but the driver's GPS shows the delivery was actually in Port Harcourt. "
    "Which row has a validity failure, which has an accuracy failure, "
    "and what does this mean for fitness for purpose?"
)

# ── ADVISORY: s15 – revise opt_s15_c feedback ─────────────────────────────────
s15 = find_ix("tile_data_quality_and_workflow.s15")
ix15 = s15["interaction"]
ix15["grading"]["option_feedback"]["opt_s15_c"]["message"] = (
    "driver_id is a numeric code, not personally identifying information about customers. "
    "The columns to remove are those that identify individual customers and are not needed "
    "for the stated purpose."
)

# ── ADVISORY: s17 – strengthen feedback on limitation and re-identification ────
s17 = find_ix("tile_data_quality_and_workflow.s17")
ix17 = s17["interaction"]
ix17["feedback"]["correct"]["message"] = (
    "Correct. customer_name and customer_phone are personally identifiable information "
    "not needed to calculate average delivery times per city — they must be removed before sharing. "
    "Note that removing these columns does not fully eliminate re-identification risk: "
    "the remaining data combined with other sources could still identify individuals. "
    "Also note the one-week data coverage as a limitation to state in your report."
)

with open(SRC, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Patch applied successfully.")
