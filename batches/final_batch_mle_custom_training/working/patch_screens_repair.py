import json
from pathlib import Path
p=Path('batches/final_batch_mle.region.custom_training/screens.json')
d=json.loads(p.read_text()); before=json.loads(p.read_text())
steps={s['step_id']:s for t in d['tiles'] for s in t['steps']}
def step(s):return steps['mle.tile.'+s]
def diagram(b, text):
    labels=text.split('\n')
    b['nodes']=[{'id':f'n{i}','label':v} for i,v in enumerate(labels)]
    b['edges']=[]
    b['alt_text']=' '.join(labels)
def panels(s,left,right):
    b=next(b for b in step(s)['blocks'] if b['type'] in ('side_by_side','before_after'))
    keys=('left','right') if b['type']=='side_by_side' else ('before','after')
    diagram(b[keys[0]],left);diagram(b[keys[1]],right)
panels('041_043.s06',
'''Illustrative fixture: x=[1,1], requires_grad=True, Dropout(p=0.5).
Training: permitted output=[0,2]; layer.training=True; output.requires_grad=True; masking/scaling assertion passes.
Training under no_grad: permitted output=[2,0]; layer.training=True; output.requires_grad=False; masking/scaling assertion passes.''',
'''Evaluation under no_grad: output=[1,1]; layer.training=False; output.requires_grad=False; identity assertion passes.
These training outputs are possible outcomes, not guaranteed masks; [2,2] is also permitted.
Restore training mode afterward.''')
panels('041_043.s13',
'''Illustrative original: Linear(2,1), weight=[[1,2]], bias=[0.5], eval mode;
input=[[1,1]]; prediction=[[3.5]]; save state_dict through open(path,'wb').''',
'''Illustrative restored: construct the same Linear(2,1); load through open(path,'rb') with weights_only=True; apply load_state_dict;
weight=[[1,2]], bias=[0.5], eval mode; same-input prediction=[[3.5]].
Corresponding-entry and prediction checks pass with rtol=1e-5, atol=1e-8.
A supplied differing-entry fixture must fail its state assertion.''')
panels('044_045.s07',
'''Illustrative reproduced failure: scalar prediction w=2, target=3, mean MSE=1, learning_rate=0.1; expected dL/dw=-2.
Backward produces -2, but premature zero_grad before step removes it; parameter remains 2, observed change=0; intended-update assertion fails.''',
'''Single correction: remove premature gradient clearing between backward and step.
Same fixture: loss=1; .grad after backward and before clearing=-2; parameter after plain-SGD step=2.2; observed change=+0.2=-0.1×(-2); update assertion passes.
Same-fixture post-update loss=0.64.''')
panels('046_048.s01',
'''Illustrative mismatch: CUDA available=True; selected device=cuda:0; model parameter device=cuda:0; feature device=cuda:0; target device=cpu;
placement assertion fails; bounded loss/backward cannot complete with this mismatch.''',
'''Repair: assign targets=targets.to(device).
Model, features and targets are now on cuda:0; placement assertion and bounded forward/backward pass.
Separate authorized lifecycle record: INSTANCE/ZONE identity verified; initial TERMINATED → start completed, RUNNING → authorized SSH workload → stop completed, TERMINATED.
CPU boundary: CUDA unavailable, select cpu and place all three on cpu.''')
b=next(b for b in step('046_048.s07')['blocks'] if b['type']=='diagram')
b['title']='Illustrative fixture; allocated-tensor-peak budget=1,000 bytes.'
diagram(b,'''Five observations, two float32 features and one float32 target per observation.
batch_size | actual batch rows | feature+target estimate | recorded peak allocated bytes | completed examples | elapsed seconds | examples/second | eligible
1 | 1,1,1,1,1 | 12 bytes per batch | 400 | 5 | 5 | 1.0 | yes
2 | 2,2,1 | 24,24,12 bytes | 800 | 5 | 2.5 | 2.0 | yes
5 | 5 | 60 bytes | 1,200 | 5 | 2 | 2.5 | no
Select batch_size=2: highest throughput among completed eligible trials.
Peaks are recorded illustrative evidence after resetting CUDA peak statistics; input estimates are not total training memory or total GPU usage.''')
shared='Shared simultaneously live allocations, float32: parameters (256,256)=256 KiB; parameter gradients (256,256)=256 KiB; current activations (128,512)=256 KiB; input batch (128,512)=256 KiB; total=1,024 KiB.'
panels('046_048.s12',
'''Illustrative allocation fixture.
'''+shared+'''
Failure while allocating the next activation block; unnecessary graph-connected diagnostic tensors retain another (128,512)=256 KiB;
current/peak allocated=1,280/1,280 KiB; current/peak reserved=1,536/1,536 KiB; declared allocated-memory requirement=1,100 KiB; workload does not complete.''',
'''Single correction: retain scalar diagnostics instead of graph-connected tensors.
Shared task and batch unchanged; current/peak allocated=1,024/1,024 KiB; current/peak reserved=1,536/1,536 KiB; workload completes within the declared requirement.
Reserved memory can remain high; empty_cache cannot free live tensor storage.''')
panels('049_050.s01',
'''Illustrative attribution after warm-up: labelled loading=8 s, transfer=1 s, model computation=1 s;
same-window CPU=50%, memory=256 MiB, authorized workload process running, corroborated by docker stats/docker top.
Loading dominates this fixture.''',
'''Single change: reuse the same prepared inputs instead of repeating identical loading work.
Same bounded workload and quality contract; matched unprofiled completed-work times after warm-up: baseline=10 s, changed=6 s.
For both CUDA timings, synchronize immediately before starting and before stopping the CPU clock.
Profiler attribution is diagnostic evidence; the unprofiled comparison establishes the measured improvement.''')
panels('049_050.s06',
'''Illustrative matched benchmark.
Fixed requirements: same workload and quality check; memory≤4,096 MiB; execution time≤90 s; lifecycle compute cost≤1.50 currency units.
CPU: model/features/targets on cpu; completes; quality check passes; observed memory=2,048 MiB; execution=60 s; lifecycle=100 s; rate=0.01/s; execution cost=0.60; lifecycle compute cost=1.00; final verified state=TERMINATED.''',
'''GPU: availability verified; model/features/targets on cuda:0; completes; same quality check passes; observed memory=3,072 MiB; execution=20 s; lifecycle=30 s; rate=0.04/s; execution cost=0.80; lifecycle compute cost=1.20; final verified state=TERMINATED.
Both meet the stated limits; CPU has lower lifecycle compute cost in this fixture.
Both lifecycle records include authorized identity inspection, completed start and stop operations, and final describe verification.
Disk or other charges may continue.''')
panels('051_051.s01',
'''Frozen reference: retained original id2label={0:'negative',1:'positive'} and corresponding inverse map; matching checkpoint processor; same validation cohort;
TN=8, FP=2, FN=1, TP=9; FPR=0.2, FNR=0.1.''',
'''Adapted model: task id2label={0:'negative',1:'positive'} and inverse map recorded separately;
logits shape=(1,2), target shape=(1,), dtype=long, target=[1]; task-map width and target-range assertions pass.
For a supplied head-input value 1 and equal logits, selected class-1 weight gradient: computed=-0.5, chain-rule reference=-0.5; tolerance check passes.
Selected head weight changes 2→2.05 under plain SGD with lr=0.1; corresponding frozen backbone entries remain equal.
Same validation cohort: TN=9, FP=1, FN=1, TP=9; FPR=0.1, FNR=0.1.
With P(Y=0)=P(Y=1)=0.5, cost_FP=1, cost_FN=2 and zero correct-prediction cost: reference cost=0.20, adapted cost=0.15.
Decision: adapted model has lower expected error cost in this illustrative comparison; protected test data are excluded.
Empty conditioning groups yield undefined rates.''')
b=next(b for b in step('051_051.s01')['blocks'] if b['type']=='side_by_side')
b['left']['title']='Illustrative frozen pretrained reference';b['right']['title']='Illustrative adapted task model'
b=step('035_037.s12')['blocks'][0]
b['text']=b['text'].replace('In this fixture, a fixture has four observations with two features','This fixture has four observations with two features')
b=next(b for b in step('035_037.s11')['blocks'] if b['type']=='diagram')
node=next(n for n in b['nodes'] if n['label']=='Linear(3, 1)')
node['label']+=' — Final Linear output is unconstrained; no final activation'
b['alt_text']='; '.join(n['label'] for n in b['nodes'])
b=step('046_048.s03')['blocks'][0]
old='On the supplied VM, inspect its identity and state, start it under the approved scope and connect for the bounded workload. Inspect authorized VM identity/status, start it, wait and connect only within approved scope.'
assert old in b['text']
b['text']=b['text'].replace(old,'Inspect the supplied authorized VM’s identity and initial state, start it within approved scope, wait for completion, verify its running state and connect.')
allowed={'mle.tile.'+s for s in ['041_043.s06','041_043.s13','044_045.s07','046_048.s01','046_048.s07','046_048.s12','049_050.s01','049_050.s06','051_051.s01','035_037.s12','035_037.s11','046_048.s03']}
changed=[]
for a,t in zip(before['tiles'],d['tiles']):
 for a,s in zip(a['steps'],t['steps']):
  if a!=s:assert s['step_id'] in allowed;changed.append(s['step_id'])
assert set(changed)==allowed
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Patched',len(changed),'named steps')
print('Tiles',len(d['tiles']),'steps',sum(len(t['steps']) for t in d['tiles']),'remediation',sum(len(t.get('remediation_steps',[])) for t in d['tiles']))
