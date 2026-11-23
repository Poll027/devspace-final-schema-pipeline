"""Underlying fitted preprocessing and inference, shared by the supplied package."""
import math
class InputContractError(ValueError):
    pass
def predict_records(records):
    ids, values = [], []
    for row in records:
        if set(row) != {"sample_id", "feature"}:
            raise InputContractError("required input columns")
        x = row["feature"]
        if isinstance(x, bool) or not isinstance(x, (int,float)) or not math.isfinite(x) or not 0 <= x <= 5:
            raise InputContractError("feature must be finite in [0,5]")
        ids.append(row["sample_id"])
        values.append([float(x / 5.0 >= 0.4)])
    return {"sample_ids": ids, "values": values}
