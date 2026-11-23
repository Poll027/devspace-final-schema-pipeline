import json,re
from pathlib import Path
B=Path('batches/final_batch_mle.region.custom_training')
g=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
profile=json.loads(Path('00_FINAL_PIPELINE_CORE/registry/path_profiles/'+g['path_id']+'.json').read_text())
assert all(b['context']['concept_id'] in profile['practice_type_by_concept'] for b in g['bundles'])
texts=[]
for b in g['bundles']:
 texts += [t['content'] for t in b['teaching_blocks']]
 texts += [json.dumps(b[k],ensure_ascii=False) for k in ('assessment_anchors','practice_anchor','visual_anchor')]
text='\n'.join(texts)
terms=['numerical order arrays','PyTorch','NumPy','features','targets','Dataset','DataLoader','batch_size','drop_last','shuffle','__len__','__getitem__','nn.Module','nn.Linear','ReLU','Sequential','X','D','W.grad','b.grad','MSELoss','CrossEntropyLoss','BCEWithLogitsLoss','SGD','learning_rate','optimizer.zero_grad()','loss.backward()','optimizer.step()','loss.item()','state_dict','weights_only=True','min_delta','patience','CUDA','CPU','GPU','torch.cuda.max_memory_allocated()','reset_peak_memory_stats()','memory_allocated','memory_reserved','empty_cache','docker stats','docker top','record_function','gcloud compute instances start INSTANCE --zone=ZONE','gcloud compute instances stop INSTANCE --zone=ZONE','gcloud compute instances describe INSTANCE --zone=ZONE','gcloud compute ssh INSTANCE --zone=ZONE','ViT','AutoImageProcessor','ViTForImageClassification','TrainingArguments','Trainer','pixel_values','id2label','label2id','FPR','FNR','protected test','training and validation images']
vocab=[s for s in terms if s in text]
# Mine literal numbers and dimension chains from the glossary, never supply them by hand.
examples='\n'.join(t['content'] for b in g['bundles'] for t in b['teaching_blocks'] if t['purpose']=='example')
vocab += sorted(set(re.findall(r'(?<![\w])(?:\d+(?:\.\d+)?)(?![\w])',examples)))
vocab += sorted(set(re.findall(r'\(\d+(?:,\s*\d+)*,?\)',examples)))
sid='scenario.custom_training'
r={'schema_version':'1.0','kind':'scenario_asset_registry','path_id':g['path_id'],'batch_id':g['batch_id'],'scenarios':[{'scenario_id':sid,'name':'Order-training review lab','summary':'A fictional ML team reviews a bounded numerical order-training task and a separate two-class image-classification adaptation fixture. All tables are authored, read-only training evidence, not observed production measurements. Learners inspect code and evidence; no PyTorch, GPU, container, checkpoint, VM or cloud service is provisioned.','domain':'custom model training','glossary_example_vocab':list(dict.fromkeys(vocab))}],'assets':[]}
def add(aid,title,desc,cols,rows):
 cs=[]
 for c in cols:
  name,typ,role,*extra=c
  cs.append({'name':name,'type':typ,'semantic_role':role,**(extra[0] if extra else {})})
 r['assets'].append({'asset_id':'ds.'+aid,'asset_kind':'dataset','scenario_id':sid,'title':title,'description':desc,'columns':cs,'rows':rows,'provenance':'authored'})
# Only the data_table anchor and numerical comparison/trace evidence are assets.
# Code, architecture and before/after excerpts are carried by later screens, not workspaces.
cols=[('batch_size','integer','numerical'),('actual_feature_shape','string','text'),('actual_target_shape','string','text'),('final_batch_rows','integer','numerical'),('feature_columns','integer','numerical'),('bytes_per_feature_element','integer','numerical'),('bytes_per_target_element','integer','numerical'),('feature_bytes','integer','numerical'),('target_bytes','integer','numerical'),('input_estimate_bytes','integer','numerical'),('peak_allocated_tensor_bytes','integer','numerical'),('budget_bytes','integer','numerical'),('budget_interpretation','string','text'),('completed_examples','integer','numerical'),('elapsed_seconds','number','numerical'),('throughput_examples_per_second','number','numerical'),('minimum_throughput','number','numerical'),('completed','boolean','categorical'),('eligible','boolean','categorical'),('selected','boolean','categorical'),('peak_reset_before_trial','boolean','categorical'),('measurement_boundary','string','text')]
rows=[]
# Fictional measured fields are authored; estimates, throughput and decisions are computed.
trials=[(50,18000,2.0),(100,26000,1.25),(200,46000,1.0)]
budget=30000;done=1005;minimum=400
eligible=[(n,done/sec) for n,peak,sec in trials if peak<=budget and done/sec>=minimum]
selected=max(eligible,key=lambda x:x[1])[0]
for n,peak,sec in trials:
 fb=n*20*4;tb=n*4;speed=done/sec;ok=peak<=budget and speed>=minimum
 rows.append([n,'full '+str((n,20))+'; final '+str((done%n,20)),'full '+str((n,))+'; final '+str((done%n,)),done%n,20,4,4,fb,tb,fb+tb,peak,budget,'peak allocated tensor bytes, not total GPU usage',done,sec,speed,minimum,True,ok,n==selected,True,'reset before bounded CUDA trial; inspect peak after completion; same task and synchronized elapsed-time boundaries'])
add('batch_size_trials','Controlled batch-size comparison','Authored read-only CUDA trial evidence. Only DataLoader batch_size changes; observation alignment, workload, model, dtypes and measurement protocol stay fixed. Fictional budget applies only to peak allocated tensor storage. Input estimates are not total training memory.',cols,rows)
# Extract the explicitly supplied early-stopping sequence and policy from its example.
b=next(b for b in g['bundles'] if b['context']['concept_id']=='mle.validation_early_stopping')
e=next(t['content'] for t in b['teaching_blocks'] if t['purpose']=='example')
seq=[float(x) for x in re.search(r'values are (.*?)[,],? with min_delta',e).group(1).replace(' and ', ', ').split(', ')]
delta=float(re.search(r'min_delta (\d+\.\d+)',e).group(1));patience=int(re.search(r'patience (\d+)',e).group(1))
best=None;counter=0;checkpoint=None;rows=[]
for epoch,value in enumerate(seq,1):
 improved=best is None or value<best-delta
 if improved:best=value;counter=0;checkpoint=epoch
 else:counter+=1
 rows.append([epoch,value,delta,patience,len(seq),improved,best,counter,checkpoint,counter>=patience])
add('early_stopping_trace','Validation patience trace','Read-only trace computed from the glossary sequence and strict min_delta rule. The retained checkpoint is a snapshot, not a live reference; protected-test observations play no role.', [('epoch','integer','numerical'),('validation_loss','number','numerical'),('min_delta','number','numerical'),('patience','integer','numerical'),('maximum_epochs','integer','numerical'),('sufficient_improvement','boolean','categorical'),('accepted_best_loss','number','numerical'),('non_improvement_counter','integer','numerical'),('checkpoint_epoch','integer','numerical'),('stop','boolean','categorical')],rows)
b=next(b for b in g['bundles'] if b['context']['concept_id']=='mle.training_hardware_selection');e=next(t['content'] for t in b['teaching_blocks'] if t['purpose']=='example')
m=re.search(r'CPU option.*?(\d+) seconds.*?(\d+\.\d+) currency.*?accelerator option taking (\d+) seconds at (\d+\.\d+)',e)
cpu_s,cpu_rate,gpu_s,gpu_rate=map(float,m.groups());rows=[]
for label,device,sec,rate,life,memory in [('CPU','cpu',cpu_s,cpu_rate,90,24000),('accelerator','cuda',gpu_s,gpu_rate,50,28000)]:
 rows.append([label,device,device,device,True,True,memory,30000,sec,life,rate,round(sec*rate,8),round(life*rate,8),'currency units per second; simplified compute-only rate',True,'TERMINATED','persistent disk and other charges may remain'])
add('hardware_comparison','CPU and accelerator cost comparison','Authored read-only records for the same bounded matrix workload. Execution durations and rates follow the glossary; other measurements and limits are fictional fixture values. Lifecycle billing scope is kept separate from bounded execution cost. No instances exist or are provisioned.', [('option','string','categorical'),('model_device','string','categorical'),('feature_device','string','categorical'),('target_device','string','categorical'),('completed','boolean','categorical'),('task_quality_requirement_met','boolean','categorical'),('observed_memory_bytes','integer','numerical'),('memory_limit_bytes','integer','numerical'),('execution_seconds','number','numerical'),('lifecycle_seconds','number','numerical'),('rate_per_second','number','numerical'),('execution_compute_cost','number','numerical'),('lifecycle_compute_cost','number','numerical'),('billing_scope','string','text'),('stopped_state_verified','boolean','categorical'),('final_instance_state','string','categorical'),('remaining_charge_note','string','text')],rows)
(B/'scenario_asset_registry.json').write_text(json.dumps(r,indent=2)+'\n')
# Mistakes-to-avoid audit: all widths/types/roles; no numeric-looking categorical labels;
# no variants means no ops, issue predicates or duplicate occurrence ambiguity.
for a in r['assets']:
 assert len(set(c['name'] for c in a['columns']))==len(a['columns'])
 for row in a['rows']:
  assert len(row)==len(a['columns'])
  for c,v in zip(a['columns'],row):
   assert {'integer':lambda v:type(v)==int,'number':lambda v:type(v) in (int,float),'boolean':lambda v:type(v)==bool,'string':lambda v:type(v)==str}[c['type']](v)
   if c['semantic_role']=='numerical':assert c['type'] in ('integer','number')
   if c['type']=='string' and str(v).isdigit():assert c.get('numeric_looking_label')
assert len(r['scenarios'])==1
assert all(s in text for s in vocab if not s.replace('.','').isdigit())
assert not any(a['asset_kind'] in ('image','code_workspace') for a in r['assets'])
assert sum(b['visual_anchor']['type']=='data_table' for b in g['bundles'])==1
print('Checklist PASS:',len(g['bundles']),'concepts;',len(r['assets']),'datasets;',sum(len(a['rows']) for a in r['assets']),'rows;',len(vocab),'vocabulary entries')
