import ast, json, re, pathlib, textwrap, csv, io
B=pathlib.Path('batches/final_batch_mle.region.custom_training')
g=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
bundles={b['context']['concept_id']:b for b in g['bundles']}
def example(cid): return '\n'.join(t['content'] for t in bundles[cid]['teaching_blocks'] if t['purpose']=='example')
sid='scenario.custom_training_lab'
assets=[]
def col(name,typ='number',role='numerical',**kw): return dict(name=name,type=typ,semantic_role=role,**kw)
def dataset(id,title,columns,rows,variants=[]):
 a=dict(asset_id='ds.'+id,asset_kind='dataset',scenario_id=sid,title=title,description='Authored illustrative fixtures, not measured production evidence.',columns=columns,rows=rows,provenance='authored',variants=variants)
 assets.append(a); return a
def variant(id,asset,ops,issues=[]): return dict(variant_id=id,derived_from=asset,purpose=id.replace('_',' '),ops=ops,planted_issues=issues)
def drop(where): return dict(op='drop_rows',where=where)
def cell(where,column,value): return dict(op='set_cell',where=where,occurrence=0,column=column,value=value)
def issue(id,kind,where,column,description,rule=None):
 a=dict(issue_id=id,kind=kind,locations=[dict(where=where,occurrence=0,column=column)],description=description)
 if rule:a['rule']=rule
 return a
orders=dataset('orders','Five aligned order observations',[col('feature_1'),col('feature_2'),col('target','integer','categorical',numeric_looking_label=True,description='Class index, not a measured quantity; the numerical task converts it to a float column tensor explicitly.')],[[i,i+1,i%2] for i in range(1,6)])
orders['variants']=[variant('tensor_four','ds.orders',[drop({'feature_1':5})]),variant('tensor_three_targets','ds.orders',[drop({'feature_1':4}),drop({'feature_1':5})]),variant('single_observation','ds.orders',[drop({'feature_1':i}) for i in range(2,6)]),variant('invalid_class_index','ds.orders',[cell({'feature_1':1},'target',2)],[issue('invalid_target','impossible_value',{'feature_1':1},'target','Target falls outside the declared two-class index contract.',dict(column='target',op='ge',value=2))]),variant('target_wrong_type','ds.orders',[cell({'feature_1':1},'target','wrong')],[issue('wrong_target_type','wrong_type',{'feature_1':1},'target','An integer class-index field contains text.',dict(column='target',op='eq',value='wrong'))])]
s=example('mle.autograd_gradients')
X=ast.literal_eval(re.search(r'X=(\[\[.*?\]\])',s).group(1)); D=ast.literal_eval(re.search(r'D=(\[\[.*?\]\])',s).group(1))
grad=dataset('linear_derivative','Linear batch X and supplied derivative D',[col('X_1'),col('X_2'),col('D')],[x+d for x,d in zip(X,D)])
grad['variants']=[variant('single_row','ds.linear_derivative',[drop({'X_1':X[-1][0]})]),variant('mismatched_derivative','ds.linear_derivative',[cell({'X_1':X[0][0]},'D',D[0][0]+1)],[issue('derivative_mismatch','other',{'X_1':X[0][0]},'D','Derivative changed relative to the fixed valid chain-rule reference.',dict(column='D',op='ne',value=D[0][0]))])]
s=example('mle.task_loss_selection'); out=ast.literal_eval(re.search(r'outputs (\[.*?\])',s).group(1)); tar=ast.literal_eval(re.search(r'targets (\[.*?\])',s).group(1))
mse=dataset('mse','Same-shaped MSE outputs and targets',[col('outputs'),col('targets')],list(map(list,zip(out,tar))))
binary=dataset('binary_logits','Binary raw-logit fixture',[col('logit'),col('target','integer','categorical',numeric_looking_label=True)],[[0,1]])
classes=dataset('class_logits','Three-class logits and class-index targets',[col('logit_0'),col('logit_1'),col('logit_2'),col('target','integer','categorical',numeric_looking_label=True)],[[i/2,-i/3,i/4,i%3] for i in range(1,7)])
s=example('mle.validation_early_stopping'); seq=[float(v) for v in re.search(r'values are (.*?)[, ]+with min_delta',s).group(1).replace(' and ', ', ').split(', ') if v]
min_delta=float(re.search(r'min_delta ([\d.]+)',s).group(1)); patience=int(re.search(r'patience (\d+)',s).group(1)); maximum=int(re.search(r'maximum epochs to (\d+)',bundles['mle.validation_early_stopping']['practice_anchor']['live_code']['starter_state_intent']).group(1))
validation=dataset('validation_loss','Bounded validation-loss sequence',[col('epoch','integer','identifier'),col('validation_loss')],[[i+1,v] for i,v in enumerate(seq)])
validation['variants']=[variant('epoch_boundary','ds.validation_loss',[drop({'epoch':i}) for i in range(2,len(seq)+1)])]
s=example('mle.training_batch_sizing'); n=int(re.search(r'batch has (\d+) rows',s).group(1)); width=int(re.search(r'rows, (\d+) four-byte features',s).group(1))
batch=dataset('matrix_workload','Aligned 20-feature numerical task',[col('feature_'+str(i+1)) for i in range(width)]+[col('target')],[[((r+1)*(c+1)%17)/17 for c in range(width)]+[(r%7)/7] for r in range(n)])
s=example('mle.training_hardware_selection'); times=[int(v) for v in re.findall(r'(\d+) seconds',s)]; rates=[float(v) for v in re.findall(r'(0\.\d+) (?:currency units per second|per second)',s)]
hardware=dataset('hardware_example','Illustrative CPU and accelerator execution inputs',[col('option','string','categorical'),col('execution_seconds',unit='seconds'),col('rate_per_second',unit='fictional currency units per second')],[[k,t,r] for k,t,r in zip(['CPU','accelerator'],times,rates)])
manifest=dataset('image_cohort','Authored two-class image cohort manifest',[col('image_id','string','identifier'),col('split','string','categorical'),col('target','integer','categorical',numeric_looking_label=True)],[[f'{split}_{i:02}',split,i%2] for split,count in [('train',8),('validation',6)] for i in range(count)])
manifest['variants']=[variant('no_positive_validation','ds.image_cohort',[drop({'split':'validation','target':1})]),variant('no_negative_validation','ds.image_cohort',[drop({'split':'validation','target':0})])]
# Preserve named source vocabulary, numerical examples and API names mined from all teaching blocks and anchors.
source_text='\n'.join([t['content'] for b in g['bundles'] for t in b['teaching_blocks']]+[json.dumps(b[k],ensure_ascii=False) for b in g['bundles'] for k in ['visual_anchor','practice_anchor','assessment_anchors']])
vocab=sorted(set(re.findall(r'\b(?:[A-Za-z_]\w*\.[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*|[A-Za-z_]\w*_[A-Za-z_0-9]*|[A-Z][A-Za-z]*[A-Z][A-Za-z]*|PyTorch|NumPy|CUDA|CPU|GPU|ViT|SGD|ReLU|Dataset|DataLoader|Trainer|torch|nn|gcloud|docker|features|targets|outputs|logits|checkpoint|orders|X|D|W|Z|x|b|\d+(?:\.\d+)?)\b',source_text)))
registry=dict(schema_version='1.0',kind='scenario_asset_registry',path_id=g['path_id'],batch_id=g['batch_id'],scenarios=[dict(scenario_id=sid,name='Parcel Lab: bounded custom-training fixtures',summary='A fictional engineering lab tests an order predictor and a two-class image head using authored fixtures in an existing authorized runtime. Numerical examples are illustrative; accelerator observations and pretrained references must come from that runtime, not invented telemetry.',domain='bounded supervised training',glossary_example_vocab=vocab)],assets=assets)
# Common infrastructure is supplied, while every assessed implementation remains learner-authored.
common='''import csv
from pathlib import Path
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
ATOL = 1e-6
RTOL = 1e-5
ROOT = Path(__file__).parent

def table(name):
    with (ROOT / name).open(newline='') as stream:
        return list(csv.DictReader(stream))

def order_arrays():
    rows = table('orders.csv')
    return (np.array([[float(r['feature_1']), float(r['feature_2'])] for r in rows], dtype=np.float64),
            np.array([int(r['target']) for r in rows], dtype=np.int32))

def training_fixture():
    features, targets = order_arrays()
    features = torch.from_numpy(features).float()
    targets = torch.from_numpy(targets).float().reshape(-1, 1)
    torch.manual_seed(17)
    model = nn.Linear(2, 1)
    loss_fn = nn.MSELoss()
    learning_rate = 0.01
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
    loader = DataLoader(TensorDataset(features, targets), batch_size=2, shuffle=False, drop_last=False)
    return dict(model=model, features=features, targets=targets, loader=loader, loss_fn=loss_fn,
                optimizer=optimizer, learning_rate=learning_rate, epochs=2, atol=ATOL, rtol=RTOL)
'''
fixtures={}
fixtures['mle.pytorch_input_tensors']='''features, targets = order_arrays()
features, targets = features[:4], targets[:4]
feature_dtype, target_dtype = torch.float32, torch.long
feature_axes, target_axes = (4, 2), (4,)
valid = (features.copy(), targets.copy(), feature_dtype, target_dtype, feature_axes, target_axes)
boundary = (features[:1].copy(), targets[:1].copy(), feature_dtype, target_dtype, (1, 2), (1,))
three_targets = (features.copy(), targets[:3].copy(), feature_dtype, target_dtype, feature_axes, target_axes)
wrong_target_contract = (features.copy(), targets.copy(), feature_dtype, target_dtype, feature_axes, (4, 1))
wrong_feature_contract = (features.copy(), targets.copy(), feature_dtype, target_dtype, (4, 3), target_axes)
# Each fixture preserves source order; contract lengths must not be inferred from malformed inputs.
'''
fixtures['mle.dataset_minibatch_loader']='''f, t = order_arrays()
features, targets = f.tolist(), t.tolist()
observations = list(zip(features, targets))
batch_size, shuffle = 2, False
retained_batch_sizes = [min(batch_size, len(observations)-i) for i in range(0, len(observations), batch_size)]
dropped_batch_sizes = [batch_size] * (len(observations)//batch_size)
boundary_observations = observations[:1]
failure_targets = targets[1:] + targets[:1]
shuffle_policies = (False, True)
'''
fixtures['mle.neural_model_definition']='''f, _ = order_arrays()
x = torch.from_numpy(f[:4]).float()
input_width, hidden_width, output_width = 2, 3, 1
expected_output_shape = (x.shape[0], output_width)
final_output_contract = 'unconstrained numerical output'
boundary_x = x[:1]
incompatible_x = torch.cat([x, x[:, :1]], dim=1)
'''
fixtures['mle.autograd_gradients']='''rows = table('linear_derivative.csv')
X = torch.tensor([[float(r['X_1']), float(r['X_2'])] for r in rows])
D = torch.tensor([[float(r['D'])] for r in rows])
W, b = torch.zeros((X.shape[1], 1)), torch.zeros(1)
boundary_X, boundary_D = X[:1].clone(), D[:1].clone()
# Fixed scalar-loss contract: (Z * D).sum(), with Z = X @ W + b.
# D already contains reduction. Construct chain-rule references in learner code.
mismatched_reference = torch.full((X.shape[1], 1), -1.0)
'''
fixtures['mle.task_loss_selection']='''rows = table('mse.csv')
outputs = torch.tensor([float(r['outputs']) for r in rows])
targets = torch.tensor([float(r['targets']) for r in rows])
binary_rows = table('binary_logits.csv')
binary_logits = torch.tensor([float(r['logit']) for r in binary_rows])
binary_targets = torch.tensor([float(r['target']) for r in binary_rows])
class_rows = table('class_logits.csv')
class_logits = torch.tensor([[float(r['logit_'+str(i)]) for i in range(3)] for r in class_rows])
class_targets = torch.tensor([int(r['target']) for r in class_rows], dtype=torch.long)
# MSE is the practice task. Binary and class-index fixtures support bounded visual comparisons.
'''
fixtures['mle.optimizer_configuration']='''def optimizer_fixture(rate):
    model = nn.Linear(1, 1, bias=False)
    with torch.no_grad():
        model.weight.fill_(2)
    features = torch.tensor([[3.0]])
    targets = torch.zeros((1, 1))
    # Supplied scalar objective gives dL/d(weight)=3 at initial weight 2.
    def loss_fn(predictions, targets):
        return predictions.sum()
    return dict(model=model, features=features, targets=targets, loss_fn=loss_fn,
                learning_rate=rate, atol=ATOL, rtol=RTOL)
valid = optimizer_fixture(0.1)
boundary = optimizer_fixture(0.0)
failure = optimizer_fixture(0.1)
incorrect_expected_after = torch.tensor([[2.0]])
'''
fixtures['mle.minibatch_training_loop']='''valid = training_fixture()
boundary = training_fixture()
boundary['epochs'] = 0
failure = training_fixture()
failure['targets'] = failure['targets'][:-1]
# Failure fixture for correspondence, supplied independently from the valid loader.
failure['loader'] = [(failure['features'], failure['targets'])]
'''
fixtures['mle.training_evaluation_modes']='''f, _ = order_arrays()
x = torch.from_numpy(f[:4]).float().requires_grad_(True)
dropout_probability = 0.5
all_retained_boundary = x.detach() / (1-dropout_probability)
mask_scaling_violation = x.detach() * 3
'''
fixtures['mle.weight_persistence']='''state = training_fixture()
original_model = state['model']
x = state['features'][:4]
checkpoint_path = str(ROOT / 'weights.pt')
def compatible_architecture():
    return nn.Linear(2, 1)
def incompatible_architecture():
    return nn.Linear(3, 1)
boundary_x = x[:1]
# A differing-state fixture must be compared entry-by-entry, not just by predictions.
with torch.no_grad():
    differing_model = compatible_architecture()
    differing_model.load_state_dict(original_model.state_dict())
    differing_model.weight.add_(1)
'''
fixtures['mle.validation_early_stopping']=f'''state = training_fixture()
model = state['model']
validation_values = [float(r['validation_loss']) for r in table('validation_loss.csv')]
min_delta, patience, maximum_epochs = {min_delta!r}, {patience!r}, {maximum!r}
def train_epoch(epoch):
    # Independent deterministic infrastructure, not a completed controller.
    with torch.no_grad():
        model.weight.fill_(epoch)
def validate_epoch(epoch):
    return validation_values[epoch-1] if epoch <= len(validation_values) else validation_values[-1]
boundary_maximum_epochs = 1
invalid_patience = 0
'''
fixtures['mle.training_failure_diagnosis']='''def diagnosis_fixture(detached=False):
    model = nn.Linear(1, 1, bias=False)
    with torch.no_grad():
        model.weight.zero_()
    model.weight.grad = torch.zeros_like(model.weight)
    features, targets = torch.ones((1, 1)), torch.ones((1, 1))
    def loss_fn(outputs, targets):
        used = outputs.detach().requires_grad_(True) if detached else outputs
        return nn.MSELoss()(used, targets)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
    return dict(model=model, features=features, targets=targets, loss_fn=loss_fn,
                optimizer=optimizer, learning_rate=0.1, atol=ATOL, rtol=RTOL)
failing_fixture = diagnosis_fixture(detached=True)
corrected_fixture = diagnosis_fixture(detached=False)
# One permitted correction: remove output detachment. Measure failing record at runtime.
'''
runtime_contract='''# Authorized-runtime binding; no credentials, invented telemetry or lifecycle actions are supplied here.
# The host must provision this JSON before hardware exercises can execute.
import json

def load_runtime():
    path = ROOT / 'authorized_runtime.json'
    if not path.exists():
        raise RuntimeError('Authorized host must provide authorized_runtime.json; see RUNTIME_REQUIREMENTS.md')
    return json.loads(path.read_text())
'''
fixtures['mle.device_placement']='''state = training_fixture()
model, features, targets, loss_fn = [state[k] for k in ('model','features','targets','loss_fn')]
boundary_features, boundary_targets = features[:1], targets[:1]
# Host supplies an authorized VM and placement failure case if CUDA is available.
# Do not perform lifecycle actions merely by importing this fixture module.
'''
fixtures['mle.training_batch_sizing']='''rows = table('matrix_workload.csv')
features = torch.tensor([[float(r['feature_'+str(i+1)]) for i in range(20)] for r in rows], dtype=torch.float32)
targets = torch.tensor([[float(r['target'])] for r in rows], dtype=torch.float32)
feature_element_bytes, target_element_bytes = features.element_size(), targets.element_size()
candidate_batch_sizes = (1, 10, 25, 100)
def trial_state():
    torch.manual_seed(17)
    model = nn.Linear(features.shape[1], 1)
    return dict(model=model, loss_fn=nn.MSELoss(), optimizer=torch.optim.SGD(model.parameters(), lr=0.01))
# Host budget must explicitly govern peak allocated tensor bytes; measure, never substitute estimates.
'''
fixtures['mle.training_memory_diagnosis']=fixtures['mle.training_batch_sizing']+'''input_width, output_width = features.shape[1], 10
allocation_shapes = {'weights': (input_width, output_width), 'bias': (output_width,),
                     'weight_gradients': (input_width, output_width), 'bias_gradients': (output_width,),
                     'features': tuple(features.shape), 'targets': tuple(targets.shape),
                     'activation': (features.shape[0], output_width)}
# Host supplies reproducible OOM workload and diagnostic access, with one allowed correction.
# Inventory categories require lifetimes: do not sum arrays not simultaneously live.
'''
fixtures['mle.training_bottleneck_profiling']='''state = training_fixture()
model, loader, optimizer, loss_fn = [state[k] for k in ('model','loader','optimizer','loss_fn')]
workload_epochs, warmup_epochs = 2, 1
permitted_factor = 'loader num_workers'
def loader_for_workers(workers):
    return DataLoader(TensorDataset(state['features'], state['targets']), batch_size=2,
                      shuffle=False, drop_last=False, num_workers=workers)
# Host provides same-window authorized docker stats and docker top helpers, and device.
'''
fixtures['mle.training_hardware_selection']=fixtures['mle.training_batch_sizing']+'''illustrative_rates_and_times = table('hardware_example.csv')
# This table is the glossary arithmetic example, NOT benchmark evidence.
# Both authorized CPU/GPU identities, zones, actual rates, fixed limits, billing policy,
# memory observations, measured execution and lifecycle durations belong to the host binding.
'''
fixtures['ml.task_specific_pretrained_weight_fine_tuning']='''cohort = table('image_cohort.csv')
num_labels = 2
id2label = {0: 'class_0', 1: 'class_1'}
label2id = {label: index for index, label in id2label.items()}
# Two fictional task labels, not claims about a real checkpoint's original labels.
def authored_images(split):
    # Tiny deterministic RGB fixtures. These are inputs, not plot assets or real-world observations.
    from PIL import Image
    rows = [r for r in cohort if r['split'] == split]
    images = []
    for j, row in enumerate(rows):
        target = int(row['target'])
        pixels = np.zeros((32, 32, 3), dtype=np.uint8)
        pixels[:, :, target] = 96 + j*3
        pixels[j % 16:j % 16+8, :, 2] = 160
        images.append(Image.fromarray(pixels))
    return images, torch.tensor([int(r['target']) for r in rows], dtype=torch.long)
training_images, training_targets = authored_images('train')
validation_images, validation_targets = authored_images('validation')
output_dir, epochs, batch_size, learning_rate = str(ROOT / 'adaptation'), 1, 2, 0.001
# Host provisions a compatible LOCAL PRETRAINED ViT checkpoint + processor, original mapping,
# frozen reference outputs on this exact validation cohort, matched task-mapping rule,
# processor-prepared train_dataset and validation_dataset, data_collator, class probabilities,
# error costs and acceptance rules. Never generate fake pretrained logits or protected test data.
'''
requirements='''# Runtime requirements and evidence boundaries
The Python CPU fixtures require numpy and torch in ordinary, non-optimized execution.
No measured hardware telemetry, cloud identities, pretrained predictions, or acceptance policies
are invented by this registry. Those assets require the existing authorized runtime described
by the glossary. The host must bind the following before attempting the corresponding exercises:

* Device placement: authorized instance identifier, zone, connection instructions, approved scope;
  supported CPU boundary and (when available) CUDA placement-mismatch case. Verify lifecycle
  states with the host; importing fixtures must not start or stop a VM.
* Batch sizing: authorized CUDA device, peak-allocated-byte budget, eligible performance threshold,
  equivalent trial starting states and synchronized timing boundaries. Compare one batch-size factor.
* Memory diagnosis: authorized CUDA workload with a reproducible failure point, simultaneously-live
  allocation inventory with element widths, declared memory requirement, and one supported correction.
  No fabricated OOM record is included; measured allocated and reserved memory must be retained.
* Profiling: authorized container, fixed workload and num_workers adjustment, device,
  same-window docker stats/docker top helpers; warm-up and unprofiled synchronized final timings.
* Hardware comparison: existing authorized CPU and GPU identities and zones, actual supplied rates,
  billing scope, task-quality/time/memory/cost limits, and measurement policy including lifecycle time.
  The arithmetic CSV is illustrative only and must not be used as a measured benchmark.
* ViT: transformers, pillow, accelerate, a compatible local pretrained checkpoint and its processor,
  original label maps, frozen validation reference on image_cohort.csv observation order and an
  explicit original-to-task mapping. Host prepares datasets and collator from these exact images with
  that processor. Bind deployment class probabilities summing to one, FP/FN costs, acceptance rules,
  selected-gradient tolerances and bounded training controls. No protected-test observations exist here.
  Include no-positive and no-negative conditioning-group checks; undefined rates are not zero.

All input values authored here are fictional fixtures. Runtime bindings are not a license to access
other resources. Record actual observations at execution; do not treat intended settings as evidence.
'''
acceptance = """# Host acceptance primitives, not completed learner conversion/training/controller code.
import torch

def expect_assertion(callable_under_test, *args, **kwargs):
    try:
        callable_under_test(*args, **kwargs)
    except AssertionError:
        return
    raise AssertionError('Declared failure fixture was accepted')

def check_tensor_pair(result, feature_shape, target_shape, feature_dtype, target_dtype,
                      source_features, source_targets):
    assert isinstance(result, tuple) and len(result) == 2
    features, targets = result
    assert tuple(features.shape) == tuple(feature_shape)
    assert tuple(targets.shape) == tuple(target_shape)
    assert features.dtype == feature_dtype and targets.dtype == target_dtype
    assert features.shape[0] == targets.shape[0]
    assert torch.equal(features, torch.as_tensor(source_features, dtype=feature_dtype))
    assert torch.equal(targets, torch.as_tensor(source_targets, dtype=target_dtype))

def check_fresh_gradient(actual, reference, atol, rtol):
    assert actual is not None
    assert tuple(actual.shape) == tuple(reference.shape)
    assert torch.allclose(actual, reference, atol=atol, rtol=rtol)

def check_plain_sgd(before, after, current_gradient, learning_rate, atol, rtol):
    assert torch.allclose(after-before, -learning_rate*current_gradient, atol=atol, rtol=rtol)

def check_state_mapping(original, restored, atol, rtol):
    assert original.keys() == restored.keys()
    for name in original:
        assert original[name].shape == restored[name].shape
        assert torch.allclose(original[name], restored[name], atol=atol, rtol=rtol)

def check_dropout_output(x, training_output, evaluation_output, probability):
    assert torch.equal(x, evaluation_output)
    assert torch.all((training_output == 0) | (training_output == x/(1-probability)))
    # All-retained and all-masked samples are both permitted; no fixed random mask is asserted.
"""
for cid,b in bundles.items():
 files=[dict(path='README.md',content='# '+b['context']['concept_name']+'\n\n'+b['practice_anchor']['objective']+'\n\n## Acceptance contract\n'+b['practice_anchor']['success']+'\n\n## Starter intent\n'+b['practice_anchor']['live_code']['starter_state_intent']+'\n\n## Scope\nAllowed syntax:\n'+ '\n'.join(b['practice_anchor']['live_code']['allowed_syntax'])+'\n\nBlocked syntax:\n'+'\n'.join(b['practice_anchor']['live_code']['blocked_syntax'])+'\n\nFixtures are supplied infrastructure; learner.py deliberately contains no completed imports or assessed implementation.\n'),dict(path='acceptance.py',content=acceptance),dict(path='infrastructure.py',content=common),dict(path='fixtures.py',content='from infrastructure import *\n\n'+fixtures[cid]+ ('\n'+runtime_contract if cid in ['mle.device_placement','mle.training_batch_sizing','mle.training_memory_diagnosis','mle.training_bottleneck_profiling','mle.training_hardware_selection','ml.task_specific_pretrained_weight_fine_tuning'] else '')),dict(path='learner.py',content='# Write the required imports, function, and acceptance assertions here.\n'),dict(path='RUNTIME_REQUIREMENTS.md',content=requirements)]
 for a in assets[:]:
  if a['asset_kind']!='dataset':continue
  stream=io.StringIO(); w=csv.writer(stream); w.writerow([c['name'] for c in a['columns']]);w.writerows(a['rows'])
  files.append(dict(path=a['asset_id'][3:]+'.csv',content=stream.getvalue()))
 assets.append(dict(asset_id='ws.'+cid.split('.')[-1],asset_kind='code_workspace',scenario_id=sid,title=b['context']['concept_name'],runtime='python',files=files))
# All examples/anchors in this batch are code, diagrams, comparisons or tables; none requires a rendered plot.
(B/'scenario_asset_registry.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n')
print('Scenarios:',len(registry['scenarios']),'Assets:',len(assets),'Datasets:',sum(a['asset_kind']=='dataset' for a in assets),'Workspaces:',sum(a['asset_kind']=='code_workspace' for a in assets))
for a in assets: print(a['asset_id'])
# Independent author checklist: data width/role/label traps, uniqueness, scope coverage, code syntax, mounted CSV fidelity.
assert len(fixtures)==len(bundles)
assert len({a['asset_id'] for a in assets})==len(assets)
for a in assets:
 if a['asset_kind']=='dataset':
  assert all(len(row)==len(a['columns']) for row in a['rows'])
  assert all(c['semantic_role']!='numerical' or c['type'] in ('integer','number') for c in a['columns'])
  assert all(c.get('numeric_looking_label') for c in a['columns'] if c['semantic_role']=='categorical' and c['type']=='integer')
 else:
  for f in a['files']:
   if f['path'].endswith('.py'):compile(f['content'],f['path'],'exec')
print('Author checklist PASS; gate verifies planted issue predicates and duplicate occurrences.')
