exec('import json\nimport time\nimport numpy as np\nimport pandas as pd\nimport json\nimport time\nimport numpy as np\nimport pandas as pd\npolicy = {\'units\': \'seconds\', \'ddof\': 0, \'declared_percentile\': 99, \'percentile_method\': \'linear\', \'probe\': {\'t0\': 0.0, \'window\': \'[0, 300)\', \'attempt_count\': 300, \'rate_per_second\': 1, \'deadline_seconds\': 2.0, \'earliest_summary_time_seconds\': 301.0, \'error_classification\': \'Every attempt not HTTP 200 with a valid prediction received within two seconds\'}, \'load\': {\'offered_rates\': [5, 10, 15], \'measurement_seconds\': 10.0, \'warmup_seconds\': 2.0, \'arrival_profile\': \'fixed evenly spaced starts\', \'payload_mix\': \'valid first-three-order matrix only; intentional malformed fixtures run separately\', \'max_in_flight\': 30, \'timeout_seconds\': 2.0, \'minimum_success_probability\': 0.9, \'maximum_failed_fraction\': 0.1, \'maximum_p99_seconds\': 1.0, \'minimum_successful_throughput_per_second\': 5.0, \'backlog_rule\': \'No increase between sampled unfinished-work observations; end unfinished work zero\'}, \'batching\': {\'settings\': [\'limit_1\', \'limit_2\'], \'maximum_p99_seconds\': 0.5, \'population\': \'Matched successful decoded responses only; exclude failure and unmatched response\'}, \'scaling\': {\'offered_rate\': 10.0, \'measurement_seconds\': 10.0, \'settings\': [\'replicas_2\', \'replicas_3\'], \'minimum_success_probability\': 0.95, \'maximum_p99_seconds\': 1.0, \'minimum_successful_throughput_per_second\': 9.0}, \'late_response_policy\': \'Responses received after the two-second deadline are failed attempts, not successful completions; late response observations do not contribute to successful throughput.\', \'unfinished_requests_definition\': \'Client attempts still awaiting a terminal outcome: request_start_seconds < elapsed_seconds < terminal_outcome_seconds. Immediate connection refusal terminates at request start; timeout terminates at start plus two seconds. Queued-only backlog, if needed, is a separate measure.\'}\nattempts = pd.read_csv("serving_attempts.csv").to_dict("records")\nFEATURE_NAMES = ("feature_1", "feature_2")\nclass FrozenPreprocessor:\n    def transform(self, values):\n        return [[float(x) for x in row] for row in values]\nclass FrozenModel:\n    def predict(self, values):\n        return [row[0] + 2.0 * row[1] for row in values]\npreprocessing_pipeline = FrozenPreprocessor()\nmodel = FrozenModel()\nprobe = [r for r in attempts if r[\'experiment\'] == \'probe\' and r[\'setting\'] == \'baseline\' and policy[\'probe\'][\'t0\'] <= r[\'request_start_seconds\'] < policy[\'probe\'][\'t0\'] + policy[\'probe\'][\'attempt_count\']]\nhandler_events = []\ndef supplied_predict(payload):\n    if current_row[\'handler_status\'] != 200:\n        raise ValueError(\'handled error\')\n    return {\'predictions\': model.predict(preprocessing_pipeline.transform(payload[\'features\']))}\ndef supplied_error_status():\n    return int(current_row[\'handler_status\'])\ndef supplied_missing(value):\n    return pd.isna(value)\ndef supplied_status_counts(events):\n    return {str(status):sum(e[\'status\']==status for e in events) for status in sorted(set(e[\'status\'] for e in events))}\n\n\n\n')

def handle_prediction(body):
    start = time.perf_counter()
    try:
        payload = json.loads(body)
        result = supplied_predict(payload)
        encoded = json.dumps(result)
        status = 200
    except ValueError:
        encoded = json.dumps({'error': 'ValueError'})
        status = supplied_error_status()
    end = time.perf_counter()
    handler_events.append({'timestamp': start, 'duration': end-start, 'status': status, 'body': json.loads(encoded)})
    return {'status': status, 'body': encoded}

def summarize_probe(probe, handler_events):
    successful = []
    external_failures = []
    absent = []
    durations = []
    for row in probe:
        if row['http_status'] == 200 and row['valid_prediction'] and not supplied_missing(row['response_complete_seconds']) and row['response_complete_seconds'] - row['request_start_seconds'] <= policy['probe']['deadline_seconds']:
            successful.append(row)
        else:
            external_failures.append(row['request_id'])
        recorded = False
        for event in handler_events:
            if event['timestamp'] == row['handler_start_seconds']:
                recorded = True
        if not recorded:
            absent.append(row['request_id'])
    for event in handler_events:
        durations.append(event['duration'])
    return {'window':policy['probe']['window'], 'units':policy['units'], 'rate_per_second':policy['probe']['rate_per_second'], 'earliest_summary_time_seconds':policy['probe']['earliest_summary_time_seconds'], 'deadline_seconds':policy['probe']['deadline_seconds'], 'attempt_count':len(probe), 'successful_deadline_count':len(successful), 'availability':len(successful)/len(probe), 'error_fraction':len(external_failures)/len(probe), 'error_classification':policy['probe']['error_classification'], 'handler_count':len(handler_events), 'handler_status_counts':supplied_status_counts(handler_events), 'handler_mean':np.mean(durations), 'handler_std':np.std(durations, ddof=0), 'ddof':policy['ddof'], 'absent_handler_request_ids':absent, 'external_failure_request_ids':external_failures, 'handler_events':handler_events}

exec("\ndef latency_mean(numeric_values):\n    return np.mean(numeric_values)\n\ndef latency_std(numeric_values):\n    return np.std(numeric_values, ddof=0)\n\noriginal_clock = time.perf_counter\nfor current_row in probe:\n    if not pd.isna(current_row['handler_start_seconds']):\n        times = iter([current_row['handler_start_seconds'], current_row['handler_complete_seconds']])\n        time.perf_counter = lambda: next(times)\n        handle_prediction(json.dumps({'features': [[1.0, 2.0]]}))\ntime.perf_counter = original_clock\n\ndurations = [event['duration'] for event in handler_events]\n\n\n\nreport = summarize_probe(probe, handler_events)\n")
