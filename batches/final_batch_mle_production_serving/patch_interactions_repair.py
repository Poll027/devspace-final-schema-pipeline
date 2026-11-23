import ast,json
from pathlib import Path
B=Path('batches/final_batch_mle.region.production_serving')
p=B/'interactions.json';d=json.loads(p.read_text())
for t in d['tiles']:
 for entry in t['interactions']:
  sid=entry['step_id'];ix=entry['interaction']
  if sid not in ['mle.tile.060_063.s16','mle.tile.066_067.s11']:continue
  old=ix['grading']['solution_files'][0]['content'];nodes=ast.parse(old).body
  prefix=ast.literal_eval(nodes[0].value.args[0]);implementation=ast.literal_eval(nodes[-2].value.args[0]);footer=ast.literal_eval(nodes[-1].value.args[0])
  if sid=='mle.tile.060_063.s16':
   ix['public']['prompt']='Implement predict_batch(contract, fitted_package): read through explicit handles in declared-size chunks, apply the frozen package without refitting, write each chunk before reading the next, reopen and decode JSON Lines, and author assertions for schema and unique key coverage. Return batch_report with records, chunk_sizes, writes_before_next_read and failures_detected.'
   ix['public']['prompt']+=' Implement assert_batch_output(records, expected, contract) as your editable validation helper: require the declared record keys, numeric predictions, declared version, no duplicate keys and exact order-independent eligible-key coverage. The supplied calls exercise valid, reversed-order, final-partial, missing, duplicate, mismatched-key and malformed-record fixtures; leave fixture setup, IO observation and fixture calls unchanged.'
   # Keep type checks and pandas conversion as infrastructural adapters, not validation or IO.
   prefix+='\ndef supplied_numeric_prediction(value):\n    return isinstance(value, (int, float))\ndef supplied_feature_values(chunk, names):\n    return chunk[names].values.tolist()\n'
   implementation=implementation.replace('require(', 'assert (').replace("isinstance(record['prediction'], (int, float))", "supplied_numeric_prediction(record['prediction'])")
   implementation=implementation.replace("keys = list(chunk[contract['batch_key']])", "keys = []\n                for key in chunk[contract['batch_key']]:\n                    keys.append(key)")
   implementation=implementation.replace("predict_chunk(chunk[contract['feature_names']].values.tolist())", "fitted_package.predict(supplied_feature_values(chunk, contract['feature_names']))")
   solution=implementation
   starter='''# Implement both helpers below; fixture data and IO observation above are supplied.
def assert_batch_output(records, expected, contract):
    # TODO: author schema, prediction-type, version, uniqueness and coverage assertions.
    return None

def predict_batch(contract, fitted_package):
    # TODO: bounded read -> frozen prediction -> keyed JSON Lines write for each chunk.
    # TODO: reopen and decode the file, validate it, and detect the failure fixtures.
    return None
'''
  else:
   ix['public']['prompt']='Implement handle_prediction(body), timing JSON decoding, prediction and JSON encoding on successful and handled-error paths and recording timestamp, duration and status. Implement summarize_probe(probe, handler_events), calculating the deadline-qualified numerator, full external denominator, availability, explicitly classified error fraction and reconciliation fields; calculate handler mean with np.mean and population standard deviation with np.std(..., ddof=0). Retain report with the declared fields.'
   # Preserve the field names and policy from the former supplied implementation.
   fields=ast.parse(implementation).body[-1].body[-1].value.keys
   ix['public']['prompt']+=' Report fields: '+', '.join(ast.literal_eval(k) for k in fields)+'. Keep deterministic timestamps, scheduling, prediction/error controls and fixture calls unchanged. Record each handler event as timestamp, duration, status and decoded body; return status and JSON-encoded body from handle_prediction.'
   solution=implementation.replace('latency_mean(durations)','np.mean(durations)').replace('latency_std(durations)','np.std(durations, ddof=0)')
   starter='''# Implement the handler instrumentation and full external-probe summary below.
def handle_prediction(body):
    # TODO: time decoding, prediction and encoding, including handled ValueError.
    # TODO: append timestamp, duration, status and decoded body to handler_events.
    return None

def summarize_probe(probe, handler_events):
    # TODO: classify every external attempt using status, validity and deadline.
    # TODO: retain the full denominator and reconcile absent handler events.
    # TODO: compute mean and population standard deviation and return all report fields.
    return None
'''
  ix['public']['workspace']['files'][0]['content']='exec('+repr(prefix)+')\n\n'+starter+'\n# Supplied fixture calls and observations; leave unchanged.\nexec('+repr(footer)+')\n'
  ix['grading']['solution_files'][0]['content']='exec('+repr(prefix)+')\n\n'+solution+'\n# Supplied fixture calls and observations; leave unchanged.\nexec('+repr(footer)+')\n'
  # Existing full-report test expectations must be derived by executing the modified solution.
  # Dataset mounts are read from the named registry input below.
  reg=json.loads((B/'scenario_asset_registry.json').read_text())
  assets={a['asset_id']:a for a in reg['assets']}
  import tempfile,os,csv
  # Run in a private batch workspace with asset CSVs generated from the registry.
  run=B/(sid+'.repair_run');run.mkdir(exist_ok=True)
  for mount in ix['public']['workspace']['asset_mounts']:
   a=assets[mount['asset_id']]
   print('mount',a.keys())
   # Details resolved below after inspecting the registry asset format.
  (B/(sid+'.new.solution.py')).write_text(ix['grading']['solution_files'][0]['content'])
p.write_text(json.dumps(d,indent=2)+'\n')
