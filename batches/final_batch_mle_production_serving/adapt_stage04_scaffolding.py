# Stage-owned builder insertion: supply infrastructure/configuration glue as readonly scaffolding;
# keep glossary syntax constraints verbatim and editable work in the supported descriptor subset.
import pathlib
p=pathlib.Path(__file__).with_name('build_interactions_stage04.py')
s=p.read_text()
insert=r"""
# Descriptor conflicts: scaffold unsupported glue, keep learner edits in allowed calls/assignments.
for ix, old_solution, mounts, exprs in code_jobs:
    cid=ix['measures'][0]['concept_id']
    k=cid.split('.')[-1]
    if k == 'bounded_batch_inference':
        helper=old_solution[:old_solution.index('def validate_records')]
        helper += '''
def validate_keyed_records(records, expected_records):
    assert len(records) == len(expected_records)
    assert len({r["order_id"] for r in records}) == len(records)
    assert {r["order_id"] for r in records} == {r["order_id"] for r in expected_records}
    expected = {r["order_id"]: r for r in expected_records}
    for record in records:
        assert set(record) == set(result_keys)
        assert record == expected[record["order_id"]]
    return True
def no_validation(records, expected_records):
    return True
def discard_identity(key, prediction):
    return {"prediction": prediction, "version": version}
def keyed_record(key, prediction):
    return {"order_id": key, "prediction": prediction, "version": version}
def run_pipeline(reader, size, make_record, validate_records):
    decoded = []
    expected = []
    chunk_lengths = []
    events = []
    with open(input_path) as inp, open(output_path, "w") as out:
        for chunk in reader(inp, chunksize=size):
            events.append("read")
            chunk_lengths.append(len(chunk))
            predictions = fitted_package.predict(chunk[feature_names])
            for key, prediction in zip(chunk["order_id"], predictions):
                expected.append(keyed_record(key, prediction))
                out.write(json.dumps(make_record(key, prediction)) + "\\n")
            events.append("write")
    with open(output_path) as inp:
        for line in inp:
            decoded.append(json.loads(line))
    fixtures = [decoded[::-1], decoded[:-1], decoded + decoded[:1], [{**r, "order_id": "unknown"} if i == 0 else r for i, r in enumerate(decoded)], [{"order_id": r["order_id"]} for r in decoded], [{**r, "prediction": r["prediction"] + 1} if i == 0 else r for i, r in enumerate(decoded)]]
    checks = []
    for fixture in fixtures:
        try:
            checks.append(validate_records(fixture, expected))
        except AssertionError:
            checks.append(False)
    return {"records": decoded, "chunk_lengths": chunk_lengths, "events": events, "validation_results": checks}
'''
        prefix='import pandas as pd\nfrom scaffold import declared_rows, run_pipeline, keyed_record, discard_identity, validate_keyed_records, no_validation\n'
        prefix+='full_fixture_rows = '+repr(len(A['ds.orders']['rows']))+'\n'
        starter=prefix+'# Complete the callback/size wiring; inspect the readonly pipeline and validators.\nreader = pd.read_csv\nchunk_rows = full_fixture_rows\nmake_record = keyed_record\nvalidate_records = no_validation\nbatch_report = run_pipeline(reader, chunk_rows, make_record, validate_records)\n'
        solution=prefix+'reader = pd.read_csv\nchunk_rows = declared_rows\nmake_record = keyed_record\nvalidate_records = validate_keyed_records\nbatch_report = run_pipeline(reader, chunk_rows, make_record, validate_records)\n'
        prompt='Inspect scaffold.py, then correct the callback/size wiring in learner.py. Keep the supplied run_pipeline call and readonly frozen package unchanged. reader must be pandas.read_csv, chunk_rows must be the supplied declared_rows, make_record must preserve order_id with prediction and version, and validate_records must verify exact schema, unique complete keys and keyed predictions independent of order. Choose among the supplied validator callbacks; no_validation intentionally checks nothing. The pipeline writes each chunk before reading the next, then decodes JSON lines and runs reordered-valid, missing, duplicate, mismatched-key, malformed-schema and wrong-prediction fixtures in that order. batch_report must contain records, chunk_lengths, alternating read/write events, and validation_results. The five orders must form chunks of two, two and one with no refitting. Do not change scaffold.py. This is a bounded wiring exercise: transport/iteration/assertion glue is supplied because its syntax descriptors are not executable by this gate.'
    elif k == 'inference_batching_decision':
        prefix_end=old_solution.index('encoded_trace =')
        helper=old_solution[:prefix_end]
        helper+='''
def keep_success(candidate):
    return candidate["success"]
def keep_matched_success(candidate):
    return candidate["success"] and candidate["request_start_seconds"] is not None and candidate["response_complete_seconds"] is not None and candidate["decoded_response"]["request_id"] == candidate["request_id"] and candidate["decoded_response"]["batching_setting"] == candidate["batching_setting"]
def report_from_trace(decode, encode, eligible, mean_stat, std_stat, tail_stat):
    decoded_trace = decode(encode(trace))
    report = {}
    selected = []
    for setting in settings:
        latencies = []
        for row in decoded_trace:
            if row["batching_setting"] == setting:
                row["decoded_response"] = decode(row["response_json"]) if row["response_json"] else {}
                if eligible(row):
                    latencies.append(row["response_complete_seconds"] - row["request_start_seconds"])
        values = np.array(latencies)
        tail = tail_stat(values)
        report[setting] = {"count": len(latencies), "mean": mean_stat(values), "std": std_stat(values), "p99": tail, "units": units, "ddof": divisor, "percentile_method": percentile_method}
        if tail <= latency_objective:
            selected.append(setting)
    return report, selected
'''
        prefix='import numpy as np\nfrom json import loads, dumps\nfrom scaffold import report_from_trace, keep_success, keep_matched_success, declared_percentile, percentile_method\n'
        functions='''def mean_stat(numeric_values):
    return np.mean(numeric_values)
def std_stat(numeric_values):
    return np.std(numeric_values, ddof=0)
def tail_stat(latencies):
    return np.percentile(latencies, declared_percentile, method=percentile_method)
'''
        starter=prefix+'''# TODO: replace the empty statistics with the taught NumPy calls.
def mean_stat(numeric_values):
    return None
def std_stat(numeric_values):
    return None
def tail_stat(latencies):
    return None
# Choose the callback that matches response identity/setting and excludes missing request traces.
decode = loads
encode = dumps
eligible = keep_success
report, selected = report_from_trace(decode, encode, eligible, mean_stat, std_stat, tail_stat)
'''
        solution=prefix+functions+'decode = loads\nencode = dumps\neligible = keep_matched_success\nreport, selected = report_from_trace(decode, encode, eligible, mean_stat, std_stat, tail_stat)\n'
        prompt='Inspect the supplied trace matching/report scaffold, then complete mean_stat, std_stat and tail_stat using np.mean, np.std(..., ddof=0) and np.percentile(..., declared_percentile, method=percentile_method). Keep supplied imports and final report_from_trace call unchanged. Wire decode to loads and encode to dumps, and select the eligible callback that excludes failures and responses lacking a request-start trace and matches decoded response identity and setting (keep_success does not perform those checks). The supplied pipeline uses response completion minus request start, including waiting, in seconds. report contains each supplied setting in settings order with count, mean, std, p99, units, ddof, percentile_method; selected lists settings with p99 <= latency_objective, or [] if none qualify. Do not change scaffold.py. The scaffold supplies matching/iteration glue; the learner completes the supported eligibility wiring and numerical functions.'
    else:
        prefix_end=old_solution.index('def instrumented_handler')
        helper=old_solution[:prefix_end]
        helper=helper.replace('return {"predictions": [sum(row) for row in payload["features"]], "version": "A"}', 'return {"predictions": model.predict(preprocessing_pipeline.transform(payload["features"])), "version": version}')
        helper+='\n'+file('ws.service_telemetry','frozen_package.py')+'\nversion = '+repr(C['version'])+'\n'
        handler=old_solution[prefix_end:old_solution.index('external = run_supplied_probe')]
        helper+=handler
        summary=old_solution[old_solution.index('external = run_supplied_probe'):]
        summary=summary.replace('np.mean(numeric_values)','mean_stat(numeric_values)').replace('np.std(numeric_values, ddof=0)','std_stat(numeric_values)')
        # Two eligible policies make the denominator/negative-case distinction learner-controlled.
        summary=summary.replace('if attempt["http_status"] == 200 and attempt["valid_prediction"] and attempt["response_complete_seconds"] is not None and attempt["response_complete_seconds"] - attempt["request_start_seconds"] <= deadline_seconds:', 'if available(attempt):')
        summary=summary.replace('successes / window_seconds', 'successes / denominator').replace('(len(external) - successes) / window_seconds', '(len(external) - successes) / denominator')
        helper+='''
def accept_http_only(attempt):
    return attempt["http_status"] == 200
def accept_valid_deadline(attempt):
    return attempt["http_status"] == 200 and attempt["valid_prediction"] and attempt["response_complete_seconds"] is not None and attempt["response_complete_seconds"] - attempt["request_start_seconds"] <= deadline_seconds
handler_denominator = sum(a["handler_start_seconds"] is not None for a in attempts)
def report_probe(mean_stat, std_stat, available, denominator):
'''
        helper+='\n'.join('    '+line for line in summary.splitlines())+'\n    return report\n'
        prefix='import numpy as np\nfrom scaffold import report_probe, accept_http_only, accept_valid_deadline, window_seconds, handler_denominator\n'
        functions='''def mean_stat(numeric_values):
    return np.mean(numeric_values)
def std_stat(numeric_values):
    return np.std(numeric_values, ddof=0)
'''
        starter=prefix+'''# Inspect the supplied instrumented handler, external outcomes and deadline policies.
def mean_stat(numeric_values):
    return None
def std_stat(numeric_values):
    return None
available = accept_http_only
denominator = handler_denominator
report = report_probe(mean_stat, std_stat, available, denominator)
'''
        solution=prefix+functions+'available = accept_valid_deadline\ndenominator = window_seconds\nreport = report_probe(mean_stat, std_stat, available, denominator)\n'
        prompt='Inspect scaffold.py: its deterministic external probe preserves one valid request per second in the half-open [window_start, window_start+window_seconds) window and summary_time allows the final two-second deadline. Its instrumented handler brackets JSON decode, frozen prediction and JSON encode with timestamp(); finally records success and handled ValueError duration/status. Complete mean_stat with np.mean and std_stat with np.std(..., ddof=0) over all handler durations, including errors. Wire available to the supplied policy requiring HTTP 200, valid prediction and timely completion, not HTTP status alone; wire denominator to prescribed window_seconds (300), never handler_denominator. Keep report_probe call and readonly scaffold unchanged. report must contain window endpoints, summary_time, attempted, successful, availability, error_fraction (non-success/300), explicit error_classification, handler_status_counts, handler_errors, handler_mean, handler_std, handler_count, units, external_failures by outcome, absent_handler_records (request_id/outcome dictionaries) and timestamped telemetry. Missing handler records remain external attempts. The handler/transport/report assembly are supplied glue; supported learner work is statistical function completion and availability/denominator wiring.'
    ix['public']['prompt']=prompt
    ix['public']['workspace']['files']=[{'path':'learner.py','role':'editable','language':'python','content':starter},{'path':'scaffold.py','role':'readonly','language':'python','content':helper}]
    ix['grading']['solution_files']=[{'path':'learner.py','content':solution},{'path':'scaffold.py','content':helper}]
    for j,(jix,_,jm,je) in enumerate(code_jobs):
        if jix is ix:
            code_jobs[j]=(ix,solution,mounts,exprs)
            break
"""
s=s.replace('# Expected answers are obtained by a real execution in the pinned player engine.',insert+'\n# Expected answers are obtained by a real execution in the pinned player engine.')
s=s.replace("'files':[{'path':'learner.py','content':solution}],'mounts':", "'files':ix['grading']['solution_files'],'mounts':")
p.write_text(s)
