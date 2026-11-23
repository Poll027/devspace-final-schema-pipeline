# Supplied trace loading and declared settings/conventions only.
exec('import json\nimport numpy as np\nimport csv\nwith open("batching_trace.csv") as handle:\n    raw_rows = list(csv.DictReader(handle))\ntrace = [{"request_id": r["request_id"], "batching_setting": r["batching_setting"], "request_start_seconds": float(r["request_start_seconds"]) if r["request_start_seconds"] else None, "response_complete_seconds": float(r["response_complete_seconds"]) if r["response_complete_seconds"] else None, "success": r["success"].lower() == "true", "response_json": r["response_json"]} for r in raw_rows]\nsettings = [\'limit_1\', \'limit_2\']\ndeclared_percentile = 99\npercentile_method = \'linear\'\nlatency_objective = 0.5\nunits = \'seconds\'\ndivisor = 0\n\n')
# TODO: write JSON and NumPy imports.
# TODO: encode/decode trace, decode response_json, filter matched successful records,
# compute end-to-end durations and required statistics, and select eligible settings.
report = {}
selected = []
