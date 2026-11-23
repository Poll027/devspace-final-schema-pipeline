"""Supplied fitted package, including preprocessing through its inference path."""
import numpy as np
from prediction_reference import predict_records, InputContractError
class FittedPackage:
    def __init__(self, regression=None):
        self.regression = regression
    def predict(self, records):
        result = predict_records(records)
        ids = result["sample_ids"]
        values = np.array(result["values"], dtype=float).reshape((-1,1))
        if self.regression == "reverse_rows":
            ids, values = ids[::-1], values[::-1]
        elif self.regression == "wrong_shape":
            values = values.ravel()
        elif self.regression == "wrong_values":
            values = values + 0.1
        elif self.regression == "drops_row":
            ids, values = ids[:-1], values[:-1]
        return {"sample_ids": ids, "values": values}
predict = FittedPackage().predict
