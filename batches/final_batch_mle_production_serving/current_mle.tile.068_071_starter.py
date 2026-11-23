import json
import numpy as np
import pandas as pd
policy = {'units': 'seconds', 'ddof': 0, 'declared_percentile': 99, 'percentile_method': 'linear', 'probe': {'t0': 0.0, 'window': '[0, 300)', 'attempt_count': 300, 'rate_per_second': 1, 'deadline_seconds': 2.0, 'earliest_summary_time_seconds': 301.0, 'error_classification': 'Every attempt not HTTP 200 with a valid prediction received within two seconds'}, 'load': {'offered_rates': [5, 10, 15], 'measurement_seconds': 10.0, 'warmup_seconds': 2.0, 'arrival_profile': 'fixed evenly spaced starts', 'payload_mix': 'valid first-three-order matrix only; intentional malformed fixtures run separately', 'max_in_flight': 30, 'timeout_seconds': 2.0, 'minimum_success_probability': 0.9, 'maximum_failed_fraction': 0.1, 'maximum_p99_seconds': 1.0, 'minimum_successful_throughput_per_second': 5.0, 'backlog_rule': 'No increase between sampled unfinished-work observations; end unfinished work zero'}, 'batching': {'settings': ['limit_1', 'limit_2'], 'maximum_p99_seconds': 0.5, 'population': 'Matched successful decoded responses only; exclude failure and unmatched response'}, 'scaling': {'offered_rate': 10.0, 'measurement_seconds': 10.0, 'settings': ['replicas_2', 'replicas_3'], 'minimum_success_probability': 0.95, 'maximum_p99_seconds': 1.0, 'minimum_successful_throughput_per_second': 9.0}, 'late_response_policy': 'Responses received after the two-second deadline are failed attempts, not successful completions; late response observations do not contribute to successful throughput.', 'unfinished_requests_definition': 'Client attempts still awaiting a terminal outcome: request_start_seconds < elapsed_seconds < terminal_outcome_seconds. Immediate connection refusal terminates at request start; timeout terminates at start plus two seconds. Queued-only backlog, if needed, is a separate measure.'}
trace = pd.read_csv("batching_trace.csv").to_dict("records")
# Supply encoder and decoder, then complete statistics on the matched durations.
encode = None
decode = None
# Supplied identity/setting matcher; failed and unmatched rows are excluded.
durations = {setting:[] for setting in policy['batching']['settings']}
for row in trace:
    if row['success'] and not pd.isna(row['request_start_seconds']) and not pd.isna(row['response_complete_seconds']):
        decoded = decode(encode(decode(row['response_json'])))
        if decoded['request_id'] == row['request_id'] and decoded['batching_setting'] == row['batching_setting']:
            durations[row['batching_setting']].append(row['response_complete_seconds'] - row['request_start_seconds'])
latencies_1 = durations[policy['batching']['settings'][0]]
latencies_2 = durations[policy['batching']['settings'][1]]
declared_percentile = policy['declared_percentile']
percentile_method = policy['percentile_method']
count_1 = None
count_2 = None
mean_1 = None
mean_2 = None
std_1 = None
std_2 = None
tail_1 = None
tail_2 = None
# Supplied comparison/report structure: report all feasible limits, selecting neither if none qualifies.
chosen_settings = [setting for setting,tail in zip(policy['batching']['settings'],[tail_1,tail_2]) if tail <= policy['batching']['maximum_p99_seconds']]
batching_report = {'settings':policy['batching']['settings'], 'successful_counts':[count_1,count_2], 'means':[mean_1,mean_2], 'standard_deviations':[std_1,std_2], 'tails':[tail_1,tail_2], 'percentile':declared_percentile, 'percentile_method':percentile_method, 'ddof':policy['ddof'], 'units':policy['units'], 'maximum_tail':policy['batching']['maximum_p99_seconds'], 'chosen_settings':chosen_settings, 'durations':[latencies_1,latencies_2]}
