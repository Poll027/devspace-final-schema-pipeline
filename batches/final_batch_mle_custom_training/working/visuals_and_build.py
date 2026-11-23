exec((B/'working/build_screens.py').read_text()) if False else None
# This file is appended to the authoring script at build time.
K={
'pytorch_input_tensors':'''import torch
def convert(features, targets, feature_dtype, target_dtype, feature_shape, target_shape):
    features = torch.from_numpy(features).to(dtype=feature_dtype)
    targets = torch.from_numpy(targets).to(dtype=target_dtype)
    assert features.shape == feature_shape
    assert targets.shape == target_shape
    assert features.shape[0] == targets.shape[0]
    assert features.dtype == feature_dtype
    assert targets.dtype == target_dtype
    return features, targets
# The supplied fixtures establish row correspondence.
# Inspect accepted and boundary pairs; assert rejection of the misaligned fixture.''',
'dataset_minibatch_loader':'''from torch.utils.data import Dataset, DataLoader
class OrderItems(Dataset):
    def __init__(self, features, targets):
        self.features, self.targets = features, targets
    def __len__(self):
        return len(self.features)
    def __getitem__(self, index):
        return self.features[index], self.targets[index]
items = OrderItems(features, targets)
loader = DataLoader(items, batch_size=declared_size,
                    shuffle=declared_order_policy, drop_last=declared_drop_policy)
for features, targets in loader:
    assert features.shape[0] == targets.shape[0]
    assert supplied_pairing_check(features, targets)
    observed_batch_sizes.append(features.shape[0])
# Compare item identities and batch boundaries with the declared fixture.''',
'autograd_gradients':'''# X and D are the supplied fixture; D already includes reduction.
# W and b are trainable leaves. Clear any previous .grad first.
W.grad = None
b.grad = None
Z = X @ W + b
loss = (Z * D).sum()
loss.backward()
weight_reference = X.T @ D
bias_reference = D.sum(dim=0)
assert W.grad.shape == weight_reference.shape
assert b.grad.shape == bias_reference.shape
assert torch.allclose(W.grad, weight_reference, rtol=rtol, atol=atol)
assert torch.allclose(b.grad, bias_reference, rtol=rtol, atol=atol)
# Inspect both gradients before clearing; test a supplied mismatched reference too.''',
'task_loss_selection':'''import torch
from torch import nn
# Supplied same-shaped MSE fixture; mean reduction is explicit.
outputs = supplied_outputs.requires_grad_()
targets = supplied_targets
assert outputs.shape == targets.shape
loss = nn.MSELoss(reduction="mean")(outputs, targets)
loss.backward()
reference = 2 * (outputs.detach() - targets) / outputs.numel()
assert torch.allclose(outputs.grad, reference, rtol=rtol, atol=atol)
# Inspect loss.item(), shapes, outputs.grad and reference together.''',
'minibatch_training_loop':'''for epoch in range(declared_epochs):
    losses_and_counts = []
    for features, targets in loader:
        predictions = model(features)
        loss = loss_fn(predictions, targets)
        optimizer.zero_grad()
        before = selected_parameter.detach().clone()
        loss.backward()
        current_gradient = selected_parameter.grad.detach().clone()
        optimizer.step()
        losses_and_counts.append((loss.item(), features.shape[0]))
        # Only for the declared plain-SGD fixture:
        reference_change = -learning_rate * current_gradient
        observed_change = selected_parameter.detach() - before
        assert torch.allclose(observed_change, reference_change, rtol=rtol, atol=atol)''',
'validation_early_stopping':'''# Quantity, direction, min_delta, patience and maximum epochs are predeclared.
while epoch < maximum_epochs:
    current = supplied_validation_quantity(epoch)
    if current < best - min_delta:
        best = current
        counter = 0
        save_checkpoint(model.state_dict())  # save a snapshot, not a live reference
    else:
        counter += 1
        if counter >= patience:
            break
    epoch += 1
# Retain the most recent accepted snapshot; never select with protected test data.'''
}
# Structural views compare the evidence needed, not fabricated run outcomes.
PAIR={
'optimizer_configuration':(
 'Before step',['Parameter before update','Current gradient from backward','Declared learning rate; plain SGD only'],
 'After step',['Parameter after optimizer.step()','Observed change versus −learning_rate × gradient','Tolerance assertion; include rejected fixture']),
 'training_evaluation_modes':(
 'Training layer mode',['model.train(): dropout masking/scaling','Graph recording unless no_grad is active','Training under no_grad still uses training dropout'],
 'Validation',['model.eval(): dropout returns x unchanged','no_grad: graph recording disabled','Forward-only; no optimizer step; restore train']),
 'weight_persistence':(
 'Original',['Compatible architecture; model.eval()','Original state_dict entries','Fixed-fixture prediction reference; binary save'],
 'Restored',['Binary load with weights_only=True','Corresponding state entries; tolerance checks','Same-fixture eval predictions; tolerance checks']),
 'training_failure_diagnosis':(
 'Reproduced failure',['Loss and output/target contract','Expected derivative sign versus measured magnitude','.grad after backward, before clearing; update record'],
 'One supported correction',['Same task and bounded fixture','Only the hypothesized factor changed','Compare corrected loss, gradient and assertion evidence']),
 'device_placement':(
 'Incomplete placement',['Chosen device from actual availability','Model and features moved','Targets on another device: contract not met'],
 'Compatible placement',['model.to(device)','Features and targets both .to(device)','Inspect all devices; bounded forward/backward check']),
 'training_memory_diagnosis':(
 'Failure evidence',['Failure point; allocated versus reserved peaks','Parameter, gradient, activation and batch allocations','Unnecessary retained graph-connected diagnostics?'],
 'One-factor rerun',['Smaller batch OR remove unneeded graph reference','Same task: completion and measured peak','empty_cache cannot release live tensor storage']),
 'training_bottleneck_profiling':(
 'Attribute work',['Warm-up; labelled loading / transfer / model work','Profiler trace and operator attribution','Same-window CPU, memory and process evidence'],
 'Compare one change',['Same bounded workload; one supported factor','Unprofiled final timing after warm-up','Synchronize CUDA timing boundaries']),
 'training_hardware_selection':(
 'CPU option',['Model and minibatches on CPU','Same workload, quality and memory limits','Execution and lifecycle durations; supplied rate'],
 'Accelerator option',['Availability; model and minibatches on selected device','Same workload, quality and memory limits','Execution and lifecycle durations; supplied rate']),
 'task_specific_pretrained_weight_fine_tuning':(
 'Frozen pretrained reference',['Original label map; matching checkpoint processor','Same validation cohort; protected test excluded','Confusion counts: actual negatives / positives'],
 'Adapted task model',['Task map; logits (N, C); long targets (N,)','Head gradient versus chain-rule reference','Changed head / unchanged backbone; matched cost rule'])
}

def visual(ps,lin):
 cid=ps['concept_ids'][0]; key=cid.split('.')[-1]; vl=copy.deepcopy(lin);vl['anchors']=[cid+'#visual']
 typ=ps['planned_visual_block_type']
 if key=='neural_model_definition':
  purpose=C[cid]['visual_anchor']['purpose']
  chain=re.search(r'chain visible: (.*?)\. Annotate',purpose).group(1).split(' → ')
  d=diagram(chain,vl,'Preserve the leading minibatch dimension')
  d['diagram_kind']='layers';d['edges']=[{'from':f'n{i}','to':f'n{i+1}','directed':True} for i in range(len(chain)-1)]
  return [d]
 if key=='training_batch_sizing':
  # No registered dataset exists. Do not invent an asset, rows or measured peaks.
  return [diagram(['Candidate batch size; actual dimensions','Feature + target byte estimate versus measured allocated peak','Budget quantity; completed examples / elapsed time','Eligibility first; compare eligible throughput'],vl,'Controlled batch-size evidence')]
 if key in K:
  blocks=[code(K[key],vl)]
  if key=='validation_early_stopping':
   a=next(a for a in R['assets'] if a['asset_kind']=='image')
   blocks.append({'type':'annotated_image','asset_id':a['asset_id'],'alt_text':a['alt_text'],'lineage':vl})
  return blocks
 left,ll,right,rl=PAIR[key]
 if key=='optimizer_configuration':
  before=code('''optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
optimizer.zero_grad()
before = selected_parameter.detach().clone()
loss.backward()
gradient = selected_parameter.grad.detach().clone()''',vl)
  after=code('''optimizer.step()
after = selected_parameter.detach().clone()
reference = before - learning_rate * gradient
assert torch.allclose(after, reference, rtol=rtol, atol=atol)
# Plain SGD: no momentum, weight decay or other modifications.''',vl)
  return [{'type':'before_after','before':before,'after':after,'change_summary':'Backward produces the gradient; step applies it. Compare the observed update with the conditional plain-SGD rule.','lineage':vl}]
 d1=diagram(ll,vl,left);d2=diagram(rl,vl,right)
 if typ=='before_after':return [{'type':'before_after','before':d1,'after':d2,'change_summary':'Move targets as well as model and features; verify actual placement.','lineage':vl}]
 return [{'type':'side_by_side','left':d1,'right':d2,'left_label':left,'right_label':right,'takeaway':{
 'training_evaluation_modes':'Layer mode and graph recording are independent.',
 'weight_persistence':'Check parameter state and fixed-input evaluation predictions.',
 'training_failure_diagnosis':'One change on the same fixture tests one root-cause hypothesis.',
 'training_memory_diagnosis':'Compare completion and peak, not only cached storage.',
 'training_bottleneck_profiling':'Attribution and final elapsed-time comparison answer different questions.',
 'training_hardware_selection':'Compare scoped cost and eligibility; stop and verify both authorized VMs.',
 'task_specific_pretrained_weight_fine_tuning':'Use conditional error rates and supplied deployment costs on matched validation.'}[key],'lineage':vl}]

SHORT={
'pytorch_input_tensors':'Check feature and target contracts separately before returning an aligned tuple.',
'dataset_minibatch_loader':'Pair by index, then apply declared batching, ordering and partial-batch policies.',
'neural_model_definition':'Match adjacent widths and the final task contract while preserving batch length.',
'autograd_gradients':'Compare fresh gradients with shaped chain-rule references under explicit tolerances.',
'task_loss_selection':'Match logits, targets and reduction to the selected loss.',
'optimizer_configuration':'Verify a current-gradient step against the conditional plain-SGD rule.',
'minibatch_training_loop':'Repeat the current-gradient sequence and retain losses with batch counts.',
 'training_evaluation_modes':'Separate layer mode from graph recording; validation never steps the optimizer.',
 'weight_persistence':'Restore compatible state and compare entries plus fixed-fixture evaluation predictions.',
 'validation_early_stopping':'Preserve the checkpoint accepted by min_delta, not simply the last or lowest epoch.',
 'training_failure_diagnosis':'Inspect gradients at the right time and test one supported correction.',
 'device_placement':'Verify compatible model, feature and target placement, then stop the authorized VM.',
 'training_batch_sizing':'Choose eligible throughput using the budget’s measured-memory quantity.',
 'training_memory_diagnosis':'Count simultaneously live allocations and verify one-factor corrections.',
 'training_bottleneck_profiling':'Separate profiling attribution from matched unprofiled timing.',
 'training_hardware_selection':'Compare task eligibility and scoped costs; verify both authorized VMs stopped.',
 'task_specific_pretrained_weight_fine_tuning':'Verify the adapted head and compare matched validation costs without protected test leakage.'}
OUT={k:P[k] for k in ['schema_version','path_id','batch_id']};OUT['kind']='screens_part';OUT['tiles']=[]
for ti,tp in enumerate(P['tiles']):
 tile={'tile_id':tp['tile_id'],'title':' / '.join(C[c]['context']['concept_name'] for c in tp['concept_ids']),'steps':[],'remediation_steps':[]}
 for ps in tp['steps']:
  lin=lineage(ps['concept_ids'],ps['teaching_block_ids'],ps['fact_ids'],ps['anchors']);lin['segment_ids']=ps['segment_ids']
  s={k:ps[k] for k in ['step_id','type','concept_ids']};s['lineage']=lin
  cid=ps['concept_ids'][0];c=C[cid]; key=cid.split('.')[-1]
  if ps['type'] in ('check','hands_on'):
   s['title']=('Check: ' if ps['type']=='check' else 'Review evidence: ')+c['context']['concept_name']
   s['eyebrow']='Contract check' if ps['type']=='check' else 'Bounded evidence review'
  elif ps['type']=='video':
   s['title']='Layer modes and gradient recording';s['blocks']=[{'type':'media_group','segment_ids':ps['segment_ids']}]
  elif ps['type']=='recap':
   s['title']='Keep these distinctions';s['blocks']=[]
   for rc in ps['concept_ids']:
    facts=[rc+'#'+f['id'] for f in C[rc]['coverage']['required_facts']]
    # Recap fact lineage points only to facts already taught in this tile.
    tbs=[rc+'#'+tb['id'] for tb in C[rc]['teaching_blocks'] if tb['fact_ids']]
    s['blocks'].append(prose(SHORT[rc.split('.')[-1]],lineage([rc],tbs,facts)))
   nxt=tp['next_tile_id']; nt=next((x for x in P['tiles'] if x['tile_id']==nxt),None)
   if nt:idea=C[nt['concept_ids'][0]]['context']['concept_name']
   else:
    # The frozen bundle supplies the next tile's name without reading another stage.
    order=G.get('tile_order',[])
    idea=G['names']['mle.ml_training_script']
   s['blocks'].append({'type':'up_next','title':'Up next: '+idea,'text':nxt or 'Continue to the next training idea.'})
  else:
   tbs=[next(t for t in C[q.split('#')[0]]['teaching_blocks'] if t['id']==q.split('#')[1]) for q in ps['teaching_block_ids']]
   s['title']=c['context']['concept_name'] if len(tbs)>1 else {'example':'Review the bounded fixture','misconception':'Keep the distinction','mechanism':'Apply and verify'}.get(tbs[0]['purpose'],tbs[0]['title'])
   s['blocks']=[]
   for q,tb in zip(ps['teaching_block_ids'],tbs):
    bl=lineage([cid],[q],[cid+'#'+f for f in tb['fact_ids']])
    txt=V[key].get(tb['id'],example(tb))
    # Ensure the explicitly supplied dropout probability remains taught.
    if key=='training_evaluation_modes' and tb['id']=='tb3':
     probability=re.search(r'with (p=[0-9.]+)',tb['content']).group(1).rstrip('.')
     txt=txt.replace('supplied dropout fixture.','supplied dropout fixture ('+probability+').')
    s['blocks']+=split_prose(txt,bl)
   if ps['planned_visual_block_type']:s['blocks']+=visual(ps,lin)
  tile['steps'].append(s)
 # Remediation for each distinct measured fact set in the first check and hands-on.
 seen=set()
 for ps in tp['steps']:
  if ps['type'] not in ('check','hands_on'):continue
  cid=ps['concept_ids'][0]; fs=tuple(ps['fact_ids']); signature=(cid,fs)
  if signature in seen:continue
  seen.add(signature);key=cid.split('.')[-1];c=C[cid]
  wanted={f.split('#')[1] for f in fs};chosen=[];covered=set()
  # Prefer mechanism blocks: avoid repeating long fixture narratives.
  for tb in c['teaching_blocks']:
   if tb['purpose']=='mechanism' and (set(tb['fact_ids']) & (wanted-covered)):
    chosen.append(tb);covered.update(tb['fact_ids'])
  for tb in c['teaching_blocks']:
   if wanted-covered and set(tb['fact_ids']) & (wanted-covered):chosen.append(tb);covered.update(tb['fact_ids'])
  rl=lineage([cid],[cid+'#'+tb['id'] for tb in chosen],list(fs))
  r={'step_id':tp['tile_id']+'.r%02d'%(len(tile['remediation_steps'])+1),'type':'remediation','required':False,'concept_ids':[cid],'title':'Retry: '+c['context']['concept_name'],'lineage':rl,'blocks':[]}
  ex=next(tb for tb in c['teaching_blocks'] if tb['purpose']=='example')
  fixture_sentence=re.split(r'(?<=[.!?])\s+(?=[A-Z])',ex['content'].split('\n\n')[0])[0]
  r['blocks']+=split_prose(fixture_sentence,lineage([cid],[cid+'#'+ex['id']],[cid+'#'+f for f in ex['fact_ids']]))
  for tb in chosen:
   txt=V[key].get(tb['id'],example(tb))
   bl=lineage([cid],[cid+'#'+tb['id']],[cid+'#'+f for f in tb['fact_ids']])
   r['blocks']+=split_prose(txt,bl)
  # One explicit contrast stays in the same fictional order-training / image task.
  mis=next(tb for tb in reversed(c['teaching_blocks']) if tb['purpose']=='misconception')
  contrast=V[key].get(mis['id'],mis['content'])
  r['blocks']+=split_prose(contrast,lineage([cid],[cid+'#'+mis['id']],[cid+'#'+f for f in mis['fact_ids']]))
  r['lede']='Revisit the same bounded '+('image-adaptation' if key=='task_specific_pretrained_weight_fine_tuning' else 'order-training')+' evidence.'
  tile['remediation_steps'].append(r)
 OUT['tiles'].append(tile)
(B/'screens.json').write_text(json.dumps(OUT,indent=2,ensure_ascii=False)+'\n')
print('tiles',len(OUT['tiles']),'planned steps',sum(len(t['steps']) for t in OUT['tiles']),'remediation',sum(len(t['remediation_steps']) for t in OUT['tiles']))
