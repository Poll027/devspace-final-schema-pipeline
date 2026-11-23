# Supplied trace loading and declared settings/conventions only.
exec('import json\nimport numpy as np\nimport csv\nwith open("batching_trace.csv") as handle:\n    raw_rows = list(csv.DictReader(handle))\ntrace = [{"request_id": r["request_id"], "batching_setting": r["batching_setting"], "request_start_seconds": float(r["request_start_seconds"]) if r["request_start_seconds"] else None, "response_complete_seconds": float(r["response_complete_seconds"]) if r["response_complete_seconds"] else None, "success": r["success"].lower() == "true", "response_json": r["response_json"]} for r in raw_rows]\nsettings = [\'limit_1\', \'limit_2\']\ndeclared_percentile = 99\npercentile_method = \'linear\'\nlatency_objective = 0.5\nunits = \'seconds\'\ndivisor = 0\n\n')
import json
import numpy as np

decoded_trace = json.loads(json.dumps(trace))
report = {}
selected = []
for setting in settings:
    latencies = []
    for row in decoded_trace:
        if row["batching_setting"] == setting:
            if row["success"]:
                if row["request_start_seconds"] is not None:
                    if row["response_complete_seconds"] is not None:
                        if row["response_json"]:
                            response = json.loads(row["response_json"])
                            if response["request_id"] == row["request_id"]:
                                if response["batching_setting"] == setting:
                                    latencies.append(row["response_complete_seconds"] - row["request_start_seconds"])
    values = np.array(latencies)
    tail = np.percentile(values, declared_percentile, method=percentile_method)
    report[setting] = {"count": len(latencies), "mean": np.mean(values), "std": np.std(values, ddof=divisor), "p99": tail, "units": units, "ddof": divisor, "percentile_method": percentile_method}
    if tail <= latency_objective:
        selected.append(setting)
