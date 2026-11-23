# Supplied frozen package, paths, contract and fixture construction only.
exec('import pandas as pd\nimport json\nFEATURE_NAMES = ("feature_1", "feature_2")\nclass FrozenPreprocessor:\n    def transform(self, values):\n        return [[float(x) for x in row] for row in values]\nclass FrozenModel:\n    def predict(self, values):\n        return [row[0] + 2.0 * row[1] for row in values]\npreprocessing_pipeline = FrozenPreprocessor()\nmodel = FrozenModel()\n\nclass FittedPackage:\n    def predict(self, values):\n        return model.predict(preprocessing_pipeline.transform(values.values.tolist()))\nfitted_package = FittedPackage()\ninput_path = \'orders.csv\'\noutput_path = \'learner_results.jsonl\'\ndeclared_rows = 2\nfeature_names = [\'feature_1\', \'feature_2\']\nresult_keys = [\'order_id\', \'prediction\', \'version\']\nversion = \'A\'\n\ndef supplied_fixtures(decoded):\n    fixtures = [decoded[::-1], decoded[:-1], decoded + decoded[:1], [{**r, "order_id": "unknown"} if i == 0 else r for i, r in enumerate(decoded)], [{"order_id": r["order_id"]} for r in decoded], [{**r, "prediction": r["prediction"] + 1} if i == 0 else r for i, r in enumerate(decoded)]]\n    return fixtures\n')
import pandas as pd
import json

def validate_keyed_records(records, expected_records):
    assert len(records) == len(expected_records)
    keys = []
    expected_keys = []
    expected = {}
    for record in expected_records:
        expected_keys.append(record["order_id"])
        expected[record["order_id"]] = record
    for record in records:
        assert set(record) == set(result_keys)
        keys.append(record["order_id"])
    assert len(set(keys)) == len(keys)
    assert set(keys) == set(expected_keys)
    for record in records:
        assert record == expected[record["order_id"]]
    return True

def batch_predict():
    decoded = []
    expected = []
    chunk_lengths = []
    events = []
    with open(input_path) as inp, open(output_path, "w") as out:
        for chunk in pd.read_csv(inp, chunksize=declared_rows):
            events.append("read")
            chunk_lengths.append(len(chunk))
            predictions = fitted_package.predict(chunk[feature_names])
            for key, prediction in zip(chunk["order_id"], predictions):
                record = {"order_id": key, "prediction": prediction, "version": version}
                expected.append(record)
                out.write(json.dumps(record) + "\n")
            events.append("write")
    with open(output_path) as inp:
        for line in inp:
            decoded.append(json.loads(line))
    checks = []
    for fixture in supplied_fixtures(decoded):
        try:
            checks.append(validate_keyed_records(fixture, expected))
        except AssertionError:
            checks.append(False)
    return {"records": decoded, "chunk_lengths": chunk_lengths, "events": events, "validation_results": checks}

batch_report = batch_predict()
