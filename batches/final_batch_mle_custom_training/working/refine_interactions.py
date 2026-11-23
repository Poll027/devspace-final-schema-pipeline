from pathlib import Path
p=Path(__file__).with_name('build_interactions.py')
s=p.read_text()
addition=r'''
# Concrete recorded trials make the inspect-and-judge decisions applications,
# rather than classifications of generic procedure descriptions. Inputs are
# illustrative authored fixtures; every reported arithmetic result is computed.
trial_rows=[dict(size=2,peak=8000,seconds=5,complete=True),dict(size=4,peak=16000,seconds=3,complete=True),dict(size=8,peak=32000,seconds=2,complete=True)]
examples=5;memory_bound=20000;min_throughput=1
for r in trial_rows:
 r['counts']=[min(r['size'],examples-i) for i in range(0,examples,r['size'])]
 r['throughput']=examples/r['seconds']
 r['eligible']=r['complete'] and r['peak']<=memory_bound and r['throughput']>=min_throughput
chosen=max((r for r in trial_rows if r['eligible']),key=lambda r:r['throughput'])
trial_text='\n'.join(f"batch_size={r['size']}; actual counts={r['counts']}; completed={examples}; elapsed={r['seconds']} s; peak_allocated={r['peak']} bytes; completed/s={r['throughput']:.6f}; eligible={r['eligible']}" for r in trial_rows)
c='mle.training_batch_sizing'
context,items,hint=practices[c]
context+=f' Additional fixed trial limits: allocated-tensor peak <= {memory_bound} bytes and throughput >= {min_throughput} completed example/s. Each trial resets CUDA peak stats; alignment/task/other settings are unchanged. All five examples finish, including the last partial batch.'
items[0]=ok(f'# Recorded controlled comparison\n{trial_text}\n# Features have 20 four-byte columns; targets are four bytes each.\n# Report estimates from each actual batch row count separately from peaks.\n# Selection: batch_size={chosen["size"]}, highest throughput among eligible settings.\n# The larger, faster trial exceeds the allocated-tensor budget.', 'The actual partial-batch counts and completed-work rates support selecting the fastest eligible completed setting; the peak bound excludes the larger trial.')
practices[c]=(context,items,hint)
# A concrete allocation ledger and corrected peak record support attribution.
c='mle.training_memory_diagnosis';context,items,hint=practices[c]
ledger=dict(parameters=(20*10+10)*4,gradients=(20*10+10)*4,batch_features=100*20*4,batch_targets=100*4,activations=100*10*4,retained_graphs=20000)
live=sum(ledger.values()); corrected=live-ledger['retained_graphs'];memlimit=20000
context+=f' At the reproduced failure point, the supplied simultaneous-live ledger is {ledger} bytes; the allocator rejects a further required allocation under a {memlimit}-byte allocated-tensor bound. Failed allocated/reserved peaks and the point of failure are retained.'
items[0]=ok(f'# Sum the supplied simultaneous-live ledger: {live} bytes.\n# Parameter reference is (20*10+10)*4 = {ledger["parameters"]} bytes.\n# Failed peak allocated={live}; reserved={live+4000} bytes.\n# Graph-connected saved diagnostics require no future derivatives.\n# Single correction: store loss.item() instead of the graph-connected loss.\n# Same bounded task completes; corrected allocated peak={corrected},\n# corrected reserved peak={corrected+4000} bytes.\n# Retain both records; corrected allocated peak meets the {memlimit}-byte bound.', 'The ledger includes parameters, gradients, batch storage, activations and retained graphs at the same instant; removing only unnecessary diagnostic graph retention is supported by completion and the corrected allocated peak.')
practices[c]=(context,items,hint)
# Measured stage fractions and matched timings are computed from authored inputs.
c='mle.training_bottleneck_profiling';context,items,hint=practices[c]
stages=dict(loading=60,transfer=10,compute=20);before=100;after=80
items[0]=ok(f'# Warm-up complete; non-overlapping profiler labeled-region milliseconds:\n# {stages}. Loading region encloses only loading, compute only computation.\n# Loading share of attributed region time={stages["loading"]/sum(stages.values()):.6f}.\n# Same-window docker stats: loader process saturates its allotted CPU;\n# docker top confirms that process was running throughout the loading interval.\n# Reproduce the limitation; change only the supported loading factor.\n# Same bounded unprofiled CUDA work after warm-up on both runs, synchronized\n# at start/end: completed elapsed before={before} ms, after={after} ms.\n# Report loading as dominant; measured elapsed reduction={(before-after)/before:.6f}.', 'The loading-region attribution and contemporaneous loader CPU/process evidence agree. A one-factor matched unprofiled completion measurement supports the reported improvement.')
practices[c]=(context,items,hint)
# Concrete capacity choices: choose minimum lifecycle compute cost among eligible
# options, not minimum execution time. Costs are derived, never memorized.
c='mle.training_hardware_selection';context,items,hint=practices[c]
options=[dict(name='CPU',execution=60,lifecycle=100,rate=.01,memory=8000),dict(name='GPU',execution=20,lifecycle=40,rate=.04,memory=12000)]
limits=dict(memory=20000,execution_seconds=70,lifecycle_compute_cost=2)
for r in options:
 r['execution_cost']=round(r['execution']*r['rate'],10);r['lifecycle_cost']=round(r['lifecycle']*r['rate'],10)
 r['eligible']=r['memory']<=limits['memory'] and r['execution']<=limits['execution_seconds'] and r['lifecycle_cost']<=limits['lifecycle_compute_cost']
winner=min((r for r in options if r['eligible']),key=lambda r:r['lifecycle_cost'])
context+=f' The fixed limits are {limits}. Both complete the same quality-accepted workload. Select the eligible option with minimum lifecycle-billed compute cost under the supplied per-second rates; billable lifecycle durations are given below.'
records='\n'.join(f"# {r['name']}: execution={r['execution']} s, billable lifecycle={r['lifecycle']} s, rate={r['rate']} currency/s, observed memory={r['memory']} bytes, execution cost={r['execution_cost']}, lifecycle compute cost={r['lifecycle_cost']}, eligible={r['eligible']}" for r in options)
items[0]=ok(f'# Each supplied authorized identity/zone is confirmed by describe.\n# Both initially TERMINATED; start operations complete; describe RUNNING;\n# authorized gcloud compute ssh connects. Availability and compatible\n# model/input/target placement checked; matched task and quality criterion.\n# Warm-up and relevant movement included per fixed execution protocol.\n{records}\n# Choose {winner["name"]} by the declared lifecycle-cost rule.\n# Stop BOTH authorized VMs, wait for completion; describe confirms matching\n# identities in TERMINATED state. Retain lifecycle/cost records and continuing\n# disk/other charge scope separately.', 'Both options satisfy the fixed eligibility checks; the CPU has the lower lifecycle compute cost under the supplied durations and rates. Both authorized VM states are verified stopped without claiming all other charges ended.')
practices[c]=(context,items,hint)
# Actual conditional-rate/cost comparison plus an explicit undefined-group trap.
c='ml.task_specific_pretrained_weight_fine_tuning';context,items,hint=practices[c]
counts=dict(reference=dict(FP=2,TN=8,FN=3,TP=7),adapted=dict(FP=1,TN=9,FN=2,TP=8))
p0=.5;p1=.5;cfp=1;cfn=4
for r in counts.values():
 r['FPR']=r['FP']/(r['FP']+r['TN']);r['FNR']=r['FN']/(r['FN']+r['TP']);r['cost']=round(p0*r['FPR']*cfp+p1*r['FNR']*cfn,10)
context+=f' The comparison cohort has ten actual negatives and ten actual positives. Fixed deployment probabilities are P(Y=0)={p0}, P(Y=1)={p1}, error costs cost_FP={cfp}, cost_FN={cfn}, and correct predictions cost zero. The acceptance rule declares improvement only when all adaptation checks pass and expected error cost decreases.'
ct='\n'.join(f"# {name}: FP={r['FP']}, TN={r['TN']}, FN={r['FN']}, TP={r['TP']}; FPR={r['FPR']}, FNR={r['FNR']}, expected error cost={r['cost']}" for name,r in counts.items())
items[2]=ok(f'# Frozen pretrained and adapted predictions refer to exactly the same\n# validation observations, retained task mapping and checkpoint processor.\n{ct}\n# FPR denominator is actual negatives; FNR denominator is actual positives.\n# Both conditioning groups exist here. For supplied no-positive boundary,\n# FNR is explicitly undefined, not zero, and full cost is not claimed.\n# All head/backbone/shape/gradient checks passed as recorded. Expected error\n# cost decreases by {round(counts["reference"]["cost"]-counts["adapted"]["cost"],10)}; conclude improvement under the fixed rule.\n# Protected test observations never accessed.', 'Both models use matched validation evidence. The correctly conditioned rates and supplied deployment-cost calculation show a cost decrease; undefined boundary rates are explicitly handled rather than replaced with zero.')
practices[c]=(context,items,hint)
'''
s=s.replace('\nout={k:plans[k]',addition+'\nout={k:plans[k]')
# The screens provide one remediation entry per check/hands-on. Copy the
# corresponding concept entry by encounter position, including the mandatory first.
s=s.replace('seen=set(); check_index={}','seen=set(); check_index={}; remediation_index={}')
old="""  if cid not in seen:
   rem=next((r for r in sc.get('remediation_steps',[]) if cid in r['concept_ids']),None)
   if rem:ix['feedback']['remediation_step_id']=rem['step_id']
   seen.add(cid)
"""
new="""  rems=[r for r in sc.get('remediation_steps',[]) if cid in r['concept_ids']]
  ri=remediation_index.get(cid,0); remediation_index[cid]=ri+1
  if ri < len(rems): ix['feedback']['remediation_step_id']=rems[ri]['step_id']
  seen.add(cid)
"""
assert old in s
s=s.replace(old,new)
p.write_text(s)
print('Refined authored evidence and copied remediation references')
