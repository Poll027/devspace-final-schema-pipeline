# Supplied frozen package, paths, contract and fixture construction only.
exec('import pandas as pd\nimport json\nFEATURE_NAMES = ("feature_1", "feature_2")\nclass FrozenPreprocessor:\n    def transform(self, values):\n        return [[float(x) for x in row] for row in values]\nclass FrozenModel:\n    def predict(self, values):\n        return [row[0] + 2.0 * row[1] for row in values]\npreprocessing_pipeline = FrozenPreprocessor()\nmodel = FrozenModel()\n\nclass FittedPackage:\n    def predict(self, values):\n        return model.predict(preprocessing_pipeline.transform(values.values.tolist()))\nfitted_package = FittedPackage()\ninput_path = \'orders.csv\'\noutput_path = \'learner_results.jsonl\'\ndeclared_rows = 2\nfeature_names = [\'feature_1\', \'feature_2\']\nresult_keys = [\'order_id\', \'prediction\', \'version\']\nversion = \'A\'\n\ndef supplied_fixtures(decoded):\n    fixtures = [decoded[::-1], decoded[:-1], decoded + decoded[:1], [{**r, "order_id": "unknown"} if i == 0 else r for i, r in enumerate(decoded)], [{"order_id": r["order_id"]} for r in decoded], [{**r, "prediction": r["prediction"] + 1} if i == 0 else r for i, r in enumerate(decoded)]]\n    return fixtures\n')
# TODO: write the pandas and JSON imports.
def validate_keyed_records(records, expected_records):
    # TODO: author count, exact schema, unique/complete key and keyed prediction assertions.
    return None

def batch_predict():
    # TODO: bounded explicit-handle reading, fitted prediction, keyed JSON Lines writing,
    # decoding and validation of supplied_fixtures(decoded).
    return None

batch_report = batch_predict()
