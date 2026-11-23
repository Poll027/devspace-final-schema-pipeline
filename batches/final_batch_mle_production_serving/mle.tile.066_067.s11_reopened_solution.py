# Supplied transport, probe scheduling, clock, telemetry sink and frozen package only.
exec('import json\nimport time\nimport numpy as np\nimport csv\nwith open("serving_attempts.csv") as handle:\n    raw_rows = list(csv.DictReader(handle))\nattempts = [{"request_id": r["request_id"], "request_start_seconds": float(r["request_start_seconds"]) if r["request_start_seconds"] else None, "response_complete_seconds": float(r["response_complete_seconds"]) if r["response_complete_seconds"] else None, "http_status": int(r["http_status"]) if r["http_status"] else None, "valid_prediction": r["valid_prediction"].lower() == "true", "handler_start_seconds": float(r["handler_start_seconds"]) if r["handler_start_seconds"] else None, "handler_complete_seconds": float(r["handler_complete_seconds"]) if r["handler_complete_seconds"] else None, "handler_status": int(r["handler_status"]) if r["handler_status"] else None, "outcome": r["outcome"]} for r in raw_rows if r["experiment"] == "probe"]\ndeadline_seconds = 2.0\nwindow_start = 0.0\nwindow_seconds = 300\nsummary_time = 301.0\nerror_classification = \'Every attempt not HTTP 200 with a valid prediction received within two seconds\'\nunits = \'seconds\'\ntelemetry = []\ncurrent_attempt = None\nclock_phase = 0\ndef timestamp():\n    global clock_phase\n    result = current_attempt["handler_start_seconds"] if clock_phase == 0 else current_attempt["handler_complete_seconds"]\n    clock_phase += 1\n    return result\ndef supplied_predict(payload):\n    if current_attempt["handler_status"] != 200:\n        raise ValueError("supplied handled prediction error")\n    return {"predictions": model.predict(preprocessing_pipeline.transform(payload["features"])), "version": version}\ndef record_telemetry(start, finish, status):\n    telemetry.append({"request_id": current_attempt["request_id"], "timestamp": start, "duration": finish - start, "status": status})\ndef run_supplied_probe(handler):\n    global current_attempt, clock_phase\n    for attempt in attempts:\n        if attempt["handler_start_seconds"] is not None:\n            current_attempt = attempt\n            clock_phase = 0\n            handler(json.dumps({"features": [[1.0, 2.0]]}))\n    return attempts\n\nFEATURE_NAMES = ("feature_1", "feature_2")\nclass FrozenPreprocessor:\n    def transform(self, values):\n        return [[float(x) for x in row] for row in values]\nclass FrozenModel:\n    def predict(self, values):\n        return [row[0] + 2.0 * row[1] for row in values]\npreprocessing_pipeline = FrozenPreprocessor()\nmodel = FrozenModel()\n\nversion = \'A\'\n')
import time
import json
import numpy as np

def instrumented_handler(body):
    start = timestamp()
    status = 200
    try:
        payload = json.loads(body)
        response = supplied_predict(payload)
        encoded = json.dumps(response)
    except ValueError:
        status = 500
        encoded = json.dumps({"error": "prediction failure"})
    finally:
        finish = timestamp()
        record_telemetry(start, finish, status)
    return encoded

def accept_valid_deadline(attempt):
    return attempt["http_status"] == 200 and attempt["valid_prediction"] and attempt["response_complete_seconds"] is not None and attempt["response_complete_seconds"] - attempt["request_start_seconds"] <= deadline_seconds
def report_probe():
    external = run_supplied_probe(instrumented_handler)
    successes = 0
    absent = []
    external_failures = {}
    for attempt in external:
        if accept_valid_deadline(attempt):
            successes = successes + 1
        else:
            outcome = attempt["outcome"]
            if outcome not in external_failures:
                external_failures[outcome] = 0
            external_failures[outcome] = external_failures[outcome] + 1
        if attempt["handler_start_seconds"] is None:
            absent.append({"request_id": attempt["request_id"], "outcome": attempt["outcome"]})
    recorded_ids = []
    for record in telemetry:
        recorded_ids.append(record["request_id"])
    absent = []
    for attempt in external:
        if attempt["request_id"] not in recorded_ids:
            absent.append({"request_id": attempt["request_id"], "outcome": attempt["outcome"]})
    status_counts = {}
    handler_errors = 0
    numeric_values = []
    for record in telemetry:
        status = record["status"]
        if status not in status_counts:
            status_counts[status] = 0
        status_counts[status] = status_counts[status] + 1
        if status != 200:
            handler_errors = handler_errors + 1
        numeric_values.append(record["duration"])
    report = {"window": [window_start, window_start + window_seconds], "summary_time": summary_time, "attempted": len(external), "successful": successes, "availability": successes / window_seconds, "error_fraction": (len(external) - successes) / window_seconds, "error_classification": error_classification, "handler_status_counts": status_counts, "handler_errors": handler_errors, "handler_mean": np.mean(numeric_values), "handler_std": np.std(numeric_values, ddof=0), "handler_count": len(telemetry), "units": units, "external_failures": external_failures, "absent_handler_records": absent, "telemetry": telemetry}
    return report

report = report_probe()
