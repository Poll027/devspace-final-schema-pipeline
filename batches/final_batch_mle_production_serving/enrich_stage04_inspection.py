import pathlib
p=pathlib.Path(__file__).with_name('build_interactions_stage04.py')
s=p.read_text()
helper='''
# Metric excerpts are computed from the registered attempts/backlog, never hand-entered.
def measured_evidence(experiment):
 import statistics, math
 policy=M['load' if experiment=='load' else 'scaling']
 duration=policy['measurement_seconds']
 attempts=rows('ds.serving_attempts'); backlog=rows('ds.backlog')
 settings=sorted({r['setting'] for r in attempts if r['experiment']==experiment})
 reports={}; qualifying=[]
 for setting in settings:
  subset=[r for r in attempts if r['experiment']==experiment and r['setting']==setting]
  successful=[r for r in subset if r['outcome']=='success' and r['http_status']==C['success_status'] and r['valid_prediction']]
  lat=sorted(r['response_complete_seconds']-r['request_start_seconds'] for r in successful)
  q=(len(lat)-1)*M['declared_percentile']/100
  lo=math.floor(q) if lat else None
  p99=lat[lo]+(q-lo)*(lat[min(lo+1,len(lat)-1)]-lat[lo]) if lat else None
  series=sorted([r for r in backlog if r['experiment']==experiment and r['setting']==setting],key=lambda r:r['elapsed_seconds'])
  increasing=all(b['unfinished_requests']>=a['unfinished_requests'] for a,b in zip(series,series[1:])) and series[-1]['unfinished_requests']>series[0]['unfinished_requests']
  record={'attempts':len(subset),'completed_successes':len(successful),'successful_throughput_per_second':len(successful)/duration,'success_probability':len(successful)/len(subset),'failed_fraction':1-len(successful)/len(subset),'mean_seconds':statistics.mean(lat) if lat else None,'std_seconds_ddof0':statistics.pstdev(lat) if lat else None,'p99_seconds':p99,'successful_latency_count':len(lat),'percentile_method':M['percentile_method'],'backlog_samples':[{'elapsed_seconds':r['elapsed_seconds'],'unfinished_requests':r['unfinished_requests']} for r in series],'increasing_backlog':increasing}
  if experiment=='load':
   record['offered_rate_per_second']=len(subset)/duration
   feasible=record['success_probability']>=policy['minimum_success_probability'] and record['failed_fraction']<=policy['maximum_failed_request_fraction'] and p99 is not None and p99<=policy['maximum_p99_seconds'] and record['successful_throughput_per_second']>=record['offered_rate_per_second']*policy['minimum_throughput_ratio'] and series[-1]['unfinished_requests']<=policy['maximum_end_unfinished_requests'] and not increasing
  else:
   record['offered_rate_per_second']=policy['offered_rate_per_second']
   feasible=record['success_probability']>=policy['minimum_success_probability'] and record['failed_fraction']<=policy['maximum_failed_request_fraction'] and p99 is not None and p99<=policy['maximum_p99_seconds'] and record['successful_throughput_per_second']>=policy['minimum_successful_throughput_per_second'] and series[-1]['unfinished_requests']<=policy['maximum_end_unfinished_requests']
  record['meets_all_declared_criteria']=feasible
  reports[setting]=record
  if feasible:qualifying.append(setting)
 if experiment=='load':selected=max(qualifying,key=lambda x:reports[x]['offered_rate_per_second']) if qualifying else None
 else:selected=qualifying
 return json.dumps({'measurement_seconds':duration,'latency_population':'completed successful responses (timeouts excluded)','failed_population':'every non-successful eligible attempt','requirements':policy,'measurements':reports,'selected':selected,'verdict':'bounded tested evidence only, no unmeasured setting claim'},indent=2)
'''
s=s.replace('def inspect(cid):',helper+'\ndef inspect(cid):')
s=s.replace(" return [('Meets declared practice',good),('Violates declared practice',bad)]", " if k=='prediction_load_test':good.append(('Computed capacity record',measured_evidence('load')))\n if k=='serving_replica_scaling':\n  good.append(('Computed same-load decision record',measured_evidence('scaling')))\n  bad[0]=('More-is-always-better trap','Choose the largest supplied replica count without regard to its measured timeout fraction, absent successful latency sample and unfinished-request evidence. More replicas alone prove it meets every objective.')\n if k=='prediction_schema_validation':bad.append(('Wrong-rank acceptance','Decoded features is a flat one-dimensional vector rather than the declared rank-two matrix. Validator accepts without checking rank.'))\n return [('Meets declared practice',good),('Violates declared practice',bad)]")
p.write_text(s)
