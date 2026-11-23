import json,re,copy
from pathlib import Path
B=Path('batches/final_batch_mle.region.custom_training')
p=json.loads((B/'tile_plans.json').read_text());g=json.loads((B/'inputs/path_glossary_bundle.json').read_text());r=json.loads((B/'scenario_asset_registry.json').read_text())
cs={c['context']['concept_id']:c for c in g['bundles']}
tbs={cid:{t['id']:t for t in c['teaching_blocks']} for cid,c in cs.items()}
assets={a['asset_id']:a for a in r['assets']}
# Screen voices are bounded reframings of the authored glossary teaching blocks.
intros=[
'Keep the order features and targets aligned, with a separate representation contract for each.',
'The dataset defines a paired observation; the loader groups those pairs under your declared policy.',
'Build from the input width to the task output contract, checking every layer boundary.',
'Use the chain-rule reference to check autograd, not just the existence of a gradient.',
'Choose the output and target contract before choosing the scalar objective.',
'Give plain SGD the trainable parameters and verify one current-gradient update.',
'Each minibatch needs its own forward pass, fresh gradient and parameter update.',
'Validation needs both the right layer behavior and disabled gradient recording.',
'Preserving weights means checking the restored state and fixed-input predictions.',
'Declare the validation stopping rule before training, and preserve the accepted best weights.',
'Reproduce the failure and inspect its loss-to-parameter derivative chain before changing anything.',
'Check availability, then verify placement for the model, features and targets together.',
'Compare measured training peaks and completed work, not just input bytes.',
'Locate the failure among simultaneous live allocations before choosing one correction.',
'Locate the slow region, then verify any change with matched, unprofiled timing.',
'Compare the same workload on authorized options using quality, memory, timing and billing scope.',
'Keep the pretrained baseline mapping separate from the new task head mapping.'
]
misconceptions=[
'Conversion alone is not a contract check. Use the declared target dtype; matching-looking values cannot fix different batch lengths.',
'Shuffling must not separate a feature from its target. The last batch size depends on the declared drop_last policy.',
'A valid layer call is not enough: adjacent widths and the final output contract must match.',
'A populated .grad is not proof of correctness. Clear accumulated gradients and compare the matrix-shaped reference under declared tolerances.',
'Loss names do not repair incompatible shapes or representations. Logits, class indices and same-shaped numerical targets have different contracts.',
'An optimizer needs the model parameters and a fresh gradient. The plain-SGD equation is not a rule for every optimizer.',
'One update per epoch is not the minibatch loop. Clear and apply each current gradient; keep batch counts when summarizing loss.',
'eval() changes layer behavior; no_grad() changes graph recording. Neither replaces the other, and validation must not update parameters.',
'A file existing is not proof of restoration. Verify the compatible state and evaluation predictions under explicit tolerances.',
'A small decrease may not satisfy min_delta. A live state_dict reference may change after later training updates.',
'A changed setting is not a diagnosis. Check the gradient chain and rerun one evidence-supported correction on the same fixture.',
'An available accelerator does not place tensors automatically. Check all devices, and verify the authorized VM is stopped after the workload.',
'Input bytes are only an estimate, not the training peak. The allocated-tensor budget does not describe all GPU usage.',
'Unused cache and live tensors are different. empty_cache cannot release storage still occupied by live tensors.',
'A code edit is not a speed result. Synchronize accelerator timing boundaries and exclude profiler overhead from the final comparison.',
'Faster need not mean cheaper or eligible. Stopping compute can leave disk and other charges; keep the billing scope.',
'A new head remains trainable by default after freezing old parameters. Verify its target mapping and a matched validation comparison.'
]
voice={}
for i,(cid,c) in enumerate(cs.items()):
 for tb in c['teaching_blocks']:
  text=tb['content']
  if tb['purpose']=='intro': text=intros[i]
  elif tb['purpose']=='misconception': text=misconceptions[i]
  elif tb['purpose']=='example':
   # The first paragraph contains the bounded fixture; later paragraphs repeat it.
   text=text.split('\n\n')[0]
   text=re.sub(r'^Suppose ', 'In the supplied fixture, ',text)
   text=re.sub(r'^Imagine ', 'Use ',text)
  else:
   # Preserve technical contracts and qualifiers while moving to direct screen voice.
   text=text.replace('Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.', 'Test valid, boundary and failure fixtures with assert predicates. A false predicate raises AssertionError in ordinary non-optimized execution.')
   text=text.replace('rather than relying on inferred types or deriving target representation from feature dtype','not inferred types or a target representation borrowed from the feature dtype')
   text=text.replace('rather than assuming every optimizer uses that update rule','without extending that rule to every optimizer')
   text=text.replace('rather than automatically using the last epoch’s weights','not automatically the last epoch’s weights')
   text=text.replace('rather than inferring improvement only from a code change','not a code edit alone')
  voice[(cid,tb['id'])]=text
# Direct screen voice keeps API names, formula terms, qualifiers and fixture values intact.
rephrasings = {
"Use import torch and torch.from_numpy(array) to construct tensors from the supplied NumPy feature and target arrays.": "Import torch, then construct each supplied NumPy array's tensor with torch.from_numpy(array).",
"Convert the feature and target tensors explicitly with tensor.to(dtype=declared_dtype), inspect tensor.shape and tensor.dtype, and verify row correspondence not inferred types or a target representation borrowed from the feature dtype.": "For each tensor, explicitly apply tensor.to(dtype=declared_dtype) and inspect tensor.shape and tensor.dtype. Check row correspondence; do not infer the target representation from the feature dtype.",
"Assert the declared feature and target axis lengths and their common batch length, and return the aligned tensors as a tuple.": "Before returning the aligned tuple, assert each declared axis length and the shared batch length.",
"A map-style Dataset implements __len__ for sample count and __getitem__(index) for the corresponding feature/target item.": "Implement a map-style Dataset with __len__ reporting sample count and __getitem__(index) retrieving its paired feature/target item.",
"For list-based observations, retrieve the feature and target from the same observation index and return them as a tuple.": "When observations are lists, use the same index for features and targets and return that pair as a tuple.",
"The loader groups observation items into minibatches while preserving the feature/target relationship within each item.": "Minibatches group observation items; each item's feature/target relationship stays intact.",
"Import torch.nn as nn and define an nn.Module subclass with super().__init__(), registered layer attributes and a forward(self, x) method.": "After importing torch.nn as nn, subclass nn.Module. Call super().__init__(), register layers as attributes and define forward(self, x).",
"nn.Sequential composes its modules in declared order; match each layer’s output width to the next layer’s input width.": "In nn.Sequential, modules run in the declared order. Each output width must match the next input width.",
"Autograd records tensor operations as a computation graph and differentiates the scalar output through that graph using the chain rule.": "Autograd builds a computation graph from tensor operations, then applies the chain rule to differentiate its scalar output.",
"Set requires_grad=True on trainable leaf tensors, form the supplied scalar loss, call loss.backward(), and inspect each leaf parameter’s .grad.": "Mark trainable leaves with requires_grad=True. Form the supplied scalar loss and call loss.backward(); inspect .grad on each leaf parameter.",
"Backward accumulates into .grad, so clear old gradients before comparing a fresh computation with the reference.": "Clear old gradients before a fresh reference comparison: backward accumulates into .grad.",
"A loss compares model outputs with the corresponding target representation; choose its input contract before computing the scalar objective.": "The scalar objective compares outputs with their corresponding targets. First establish the loss's input contract.",
"MSELoss takes input and target tensors of the same shape and, under mean reduction, averages their squared elementwise differences.": "For MSELoss, inputs and targets must share a shape. Mean reduction averages the squared elementwise differences.",
"Initialize torch.optim.SGD(model.parameters(), lr=declared_learning_rate) so the optimizer receives the trainable model parameters.": "Pass the model's trainable parameters to torch.optim.SGD(model.parameters(), lr=declared_learning_rate).",
"Clear old parameter gradients with optimizer.zero_grad(), compute loss.backward(), then call optimizer.step() to apply the current update.": "Apply the current update in order: optimizer.zero_grad() clears old gradients, loss.backward() computes gradients, and optimizer.step() updates parameters.",
"Within each minibatch, call optimizer.zero_grad(), loss.backward() and optimizer.step() so each step uses the intended current gradient.": "For every minibatch, use optimizer.zero_grad(), loss.backward() and optimizer.step() in order; the update must use that minibatch's current gradient.",
"Use loss.item() to collect scalar loss evidence, and retain batch counts when forming an epoch summary so an incomplete batch is not silently misinterpreted.": "Collect scalar evidence with loss.item(). Keep batch counts in the epoch summary, including an incomplete batch rather than silently treating it as full.",
"Evaluation mode and no_grad serve different purposes: eval changes relevant layer behavior, while no_grad controls gradient recording.": "Separate the two controls: eval changes relevant layer behavior; no_grad controls gradient recording.",
"Keep validation as a forward-only pass without optimizer.step(), then restore model.train() before the next training pass.": "Do not call optimizer.step() in validation: use a forward-only pass. Restore model.train() before training again.",
"Save learned parameters with torch.save(model.state_dict(), path), then construct the same compatible architecture before reloading.": "Use torch.save(model.state_dict(), path) to save learned parameters. Reconstruct the same compatible architecture before loading them.",
"Call model.eval() before prediction with the restored weights.": "Before predicting with restored weights, switch the model to eval().",
"Compare corresponding original and reloaded state_dict entries in addition to fixed-input predictions to verify the parameter state was preserved.": "Verify preservation in two ways: compare corresponding state_dict entries and compare predictions on fixed inputs.",
"Predeclare the validation quantity, improvement direction, minimum improvement and patience; patience counts consecutive epochs without sufficient improvement.": "Before training, declare the validation quantity, direction, minimum improvement and patience. Patience counts consecutive epochs lacking sufficient improvement.",
"Retain the model weights associated with the best monitored validation value not automatically the last epoch’s weights.": "Keep the weights for the best monitored validation value; the final epoch is not automatically the retained model.",
"Inspect trainable parameter .grad values after backward and before clearing gradients to determine whether expected parameters receive a learning signal.": "After backward, inspect trainable parameters' .grad before clearing it. Check whether the expected parameters received a learning signal.",
"Choose one evidence-supported correction, rerun the same bounded fixture and compare its loss/gradient record with the failing reference.": "Test one correction supported by the evidence. Rerun the same bounded fixture and compare its loss/gradient record with the failure.",
"Check torch.cuda.is_available() before choosing torch.device(\"cuda\"); otherwise select the supported CPU device.": "Choose torch.device(\"cuda\") only after checking torch.cuda.is_available(); otherwise use the supported CPU device.",
"Move the model with model.to(device) and every input and target tensor with tensor.to(device) so operations use compatible device placement.": "Place all participants compatibly: model.to(device) for the model and tensor.to(device) for every input and target tensor.",
"Training memory includes live tensors and other allocations; larger minibatches ordinarily require more activation storage, so input element bytes alone do not define peak training memory.": "Input bytes alone are not peak training memory. Live tensors and other allocations also count, and larger minibatches ordinarily need more activation storage.",
"Vary only the declared batch_size of the DataLoader for the comparison, preserving observation alignment and the supplied training task.": "Change only DataLoader batch_size in the comparison. Keep observation alignment and the supplied training task unchanged.",
"Compare completed work per elapsed time for the eligible batch sizes and choose a size within the measured memory bound.": "Among eligible batch sizes, compare completed work per elapsed time. Choose within the measured memory bound.",
"CUDA memory_allocated reports tensor-occupied memory, while memory_reserved includes storage held by the caching allocator; distinguish them when locating exhaustion.": "Distinguish the CUDA readings: memory_allocated measures tensor-occupied memory, while memory_reserved includes caching-allocator storage.",
"empty_cache releases unused cached memory for other uses but cannot free storage occupied by live tensors.": "empty_cache releases unused cache for other uses, not storage still occupied by live tensors.",
"Wrap the measured computation in the PyTorch profiler context and mark data-loading and model-computation regions with record_function labels.": "Use a PyTorch profiler context around the measured computation. Label data-loading and model-computation regions with record_function.",
"Warm up the workload before comparing steady-state execution and remove profiler overhead when making the final unprofiled timing comparison.": "Warm up before comparing steady-state execution. For the final timing comparison, run unprofiled to remove profiler overhead.",
"Change one supported bottleneck factor and compare the same bounded workload again not a code edit alone.": "Change one supported bottleneck factor and remeasure the same bounded workload. A code edit alone does not demonstrate improvement.",
"A running VM is billed for compute usage; stopping it ends compute billing but can leave persistent disk and other charges.": "Compute billing continues while a VM runs. Stopping ends compute billing, but persistent disk and other charges can remain.",
"After benchmarking both authorized options, stop both and verify their resulting lifecycle states; use measured lifecycle durations in the billing calculation.": "After both benchmarks, stop both authorized options and verify their lifecycle states. Base billing calculations on measured lifecycle durations.",
"Within the adaptation run, compute the task loss, backpropagate it and compare a selected head gradient with the chain-rule reference before claiming the task head receives the intended supervised update.": "Check the supervised update within adaptation: compute task loss, backpropagate, and compare a selected head gradient against the chain-rule reference before claiming the intended signal reaches the head."
}
for key,text in voice.items():
 for original,revoiced in rephrasings.items(): text=text.replace(original,revoiced)
 voice[key]=text

# Separate ideas at sentence boundaries, never split a contract in the middle.
def chunks(text,cap=90):
 sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z])',text)
 out=[];cur=''
 for sentence in sentences:
  if cur and len((cur+' '+sentence).split())>cap:out.append(cur);cur=''
  if len(sentence.split())>cap:
   # Long source blocks are split at complete semicolon clauses only.
   clauses=re.split(r'(?<=;)\s+',sentence)
   for clause in clauses:
    if cur and len((cur+' '+clause).split())>cap:out.append(cur);cur=''
    cur=(cur+' '+clause).strip()
  else:cur=(cur+' '+sentence).strip()
 if cur:out.append(cur)
 return out

def lin(cid,tbids=(),fids=(),anchors=()):
 return {'concept_ids':[cid],'teaching_block_ids':[cid+'#'+x for x in tbids], 'fact_ids':[cid+'#'+x for x in fids], 'anchors':list(anchors)}
def prose(text,lineage,role='mechanism'):
 return {'type':'prose','text':text,'role':role,'lineage':copy.deepcopy(lineage)}
def code(text,lineage):
 return {'type':'code_walkthrough','language':'python','code':text.strip(),'reveal':'all','lineage':copy.deepcopy(lineage)}
def table(aid,lineage,columns=None):
 a=assets[aid]
 return {'type':'data_table','asset_ref':{'asset_id':a['asset_id'],'columns':columns or [c['name'] for c in a['columns']]},'caption':a['title'],'lineage':copy.deepcopy(lineage)}
# Display code is a contract walkthrough using supplied fixture variables. Outputs
# are intentionally absent: execution and output provenance belong to stage 05.
walks={
'mle.pytorch_input_tensors':'''import torch

def prepare(features_array, targets_array, feature_dtype, target_dtype,
            feature_shape, target_shape):
    features = torch.from_numpy(features_array).to(dtype=feature_dtype)
    targets = torch.from_numpy(targets_array).to(dtype=target_dtype)
    assert features.shape == feature_shape
    assert targets.shape == target_shape
    assert features.shape[0] == targets.shape[0]
    assert features.dtype == feature_dtype
    assert targets.dtype == target_dtype
    return features, targets

# Fixtures supply corresponding observation order and separate declared dtypes.
# Run accepted and boundary pairs; the mismatched-target fixture must fail.
for fixture in accepted_and_boundary_fixtures:
    features, targets = prepare(**fixture)
try:
    prepare(**three_target_failure_fixture)
except AssertionError:
    pass
else:
    raise AssertionError("Expected the alignment check to reject this fixture")''',
'mle.dataset_minibatch_loader':'''from torch.utils.data import Dataset, DataLoader

class PairedOrders(Dataset):
    def __init__(self, features, targets):
        self.features, self.targets = features, targets
        assert len(features) == len(targets)
    def __len__(self):
        return len(self.features)
    def __getitem__(self, index):
        return self.features[index], self.targets[index]

dataset = PairedOrders(feature_observations, target_observations)
for drop_policy in (False, True):
    loader = DataLoader(dataset, batch_size=declared_size,
                        shuffle=declared_order_policy, drop_last=drop_policy)
    observed_sizes = []
    for features, targets in loader:
        assert features.shape[0] == targets.shape[0]
        observed_sizes.append(features.shape[0])
    assert observed_sizes == declared_boundary_sizes[drop_policy]''',
'mle.neural_model_definition':'''import torch.nn as nn

class OrderModel(nn.Module):
    def __init__(self, input_width, hidden_width, output_width):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_width, hidden_width),
            nn.ReLU(),
            nn.Linear(hidden_width, output_width))
    def forward(self, x):
        return self.layers(x)

# This fixture declares a raw-output task contract.
model = OrderModel(input_width, hidden_width, declared_output_width)
outputs = model(features)
assert outputs.shape == (features.shape[0], declared_output_width)''',
'mle.autograd_gradients':'''import torch

W = supplied_W.clone().requires_grad_(True)
b = supplied_b.clone().requires_grad_(True)
W.grad = None
b.grad = None
Z = X @ W + b
loss = supplied_scalar_loss(Z, targets)
loss.backward()
# D is the supplied scalar-loss derivative, including its reduction.
reference_W = X.T @ D
reference_b = D.sum(dim=0)
assert torch.allclose(W.grad, reference_W, rtol=rtol, atol=atol)
assert torch.allclose(b.grad, reference_b, rtol=rtol, atol=atol)''',
'mle.task_loss_selection':'''from torch import nn

# Class indices: raw logits (N, C), long targets (N,), indices in [0, C).
class_loss = nn.CrossEntropyLoss()(class_logits, class_indices)
# Numerical targets: same shape as outputs.
regression_loss = nn.MSELoss(reduction="mean")(outputs, numeric_targets)
# Binary targets: same shape, values in [0, 1], raw logits as inputs.
binary_loss = nn.BCEWithLogitsLoss(reduction="mean")(binary_logits, binary_targets)

mse_D = 2 * (outputs - numeric_targets) / outputs.numel()
binary_D = (binary_logits.sigmoid() - binary_targets) / binary_logits.numel()
class_D = (class_logits.softmax(dim=1) - one_hot_targets) / class_logits.shape[0]''',
'mle.minibatch_training_loop':'''import torch

for epoch in range(declared_epochs):
    batch_records = []
    for features, targets in loader:
        optimizer.zero_grad()
        predictions = model(features)
        loss = loss_fn(predictions, targets)
        loss.backward()
        before = [p.detach().clone() for p in model.parameters()]
        gradients = [p.grad.detach().clone() for p in model.parameters()]
        optimizer.step()
        # This fixture uses plain SGD only.
        for p, old, gradient in zip(model.parameters(), before, gradients):
            assert torch.allclose(p.detach() - old, -learning_rate * gradient,
                                  rtol=rtol, atol=atol)
        batch_records.append((loss.item(), features.shape[0]))''',
'mle.validation_early_stopping':'''from copy import deepcopy

best = float("inf")
non_improvements = 0
epoch = 0
best_state = None
while epoch < maximum_epochs:
    train_one_epoch()
    current = validation_loss_forward_only()
    epoch += 1
    if current < best - min_delta:
        best = current
        non_improvements = 0
        best_state = deepcopy(model.state_dict())
    else:
        non_improvements += 1
        if non_improvements >= patience:
            break
model.load_state_dict(best_state)
# No protected-test observations enter this controller.'''
}
pairs={
'mle.optimizer_configuration':('''import torch
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
optimizer.zero_grad()
loss = loss_fn(model(features), targets)
loss.backward()
before = [p.detach().clone() for p in model.parameters()]
gradients = [p.grad.detach().clone() for p in model.parameters()]''','''optimizer.step()
for p, old, gradient in zip(model.parameters(), before, gradients):
    expected = old - learning_rate * gradient
    assert torch.allclose(p.detach(), expected, rtol=rtol, atol=atol)''','Before the plain-SGD step','After the plain-SGD step','Verify the current-gradient update.'),
'mle.training_evaluation_modes':('''import torch
from torch import nn
layer = nn.Dropout(p=declared_dropout_probability)
layer.train()
with torch.no_grad():
    training_output = layer(x)
# no_grad does not switch dropout behavior.
assert torch.all((training_output == 0) |
                 (training_output == x / (1 - layer.p)))''','''layer.eval()
with torch.no_grad():
    evaluation_output = layer(x)
assert torch.equal(evaluation_output, x)
model.eval()
with torch.no_grad():
    validation_predictions = model(validation_features)
# Forward only: no optimizer.step().
model.train()''','Training layer behavior','Evaluation and validation','Layer mode and graph recording are separate.'),
'mle.weight_persistence':('''import torch
model.eval()
with torch.no_grad():
    original_predictions = model(fixture_inputs)
with open(path, "wb") as handle:
    torch.save(model.state_dict(), handle)''','''restored = compatible_architecture()
with open(path, "rb") as handle:
    mapping = torch.load(handle, weights_only=True)
restored.load_state_dict(mapping)
restored.eval()
for key, value in model.state_dict().items():
    assert torch.allclose(value, restored.state_dict()[key], rtol=rtol, atol=atol)
with torch.no_grad():
    restored_predictions = restored(fixture_inputs)
assert torch.allclose(original_predictions, restored_predictions,
                      rtol=rtol, atol=atol)''','Save the evaluation reference','Reload and compare','Verify state entries and fixed-input predictions.'),
'mle.training_failure_diagnosis':('''optimizer.zero_grad()
outputs = model(features)
loss = loss_fn(outputs, targets)
loss.backward()
# Inspect before clearing gradients.
for name, parameter in model.named_parameters():
    inspect_gradient(name, parameter.grad)
compare_loss_to_output_derivative(outputs, targets, loss)''','''# Apply exactly one correction supported by the reproduced evidence.
apply_supported_correction()
corrected_record = rerun_same_bounded_fixture()
compare_loss_and_gradient_records(failing_record, corrected_record)
assert derivative_chain_matches_reference(corrected_record)''','Reproduced failing computation','Single-hypothesis rerun','Follow loss → outputs → parameters.'),
'mle.device_placement':('''import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# A device choice alone does not move the model or tensors.
inspect_devices(model, features, targets)''','''model = model.to(device)
features = features.to(device)
targets = targets.to(device)
assert all(p.device == features.device for p in model.parameters())
assert targets.device == features.device
loss = loss_fn(model(features), targets)
loss.backward()''','Device selection only','Verified compatible placement','Move and check all three participants.'),
'mle.training_memory_diagnosis':('''import torch
allocated = torch.cuda.memory_allocated()
reserved = torch.cuda.memory_reserved()
peak_allocated = torch.cuda.max_memory_allocated()
peak_reserved = torch.cuda.max_memory_reserved()
# Retaining loss can retain its computation graph.
diagnostic_history.append(loss)
# empty_cache cannot free live tensor storage.''','''# Contrast: retain scalar evidence when its gradient is not needed.
diagnostic_history.append(loss.item())
# For the rerun, remove the unnecessary retained graph reference.
# Change only that supported factor and remeasure the same workload.
parameter_elements = F * H + H
parameter_bytes = parameter_elements * parameter_element_width
live_bytes = sum(element_count * element_width
                 for element_count, element_width in simultaneous_allocations)
verify_completion_and_peak_on_same_workload()''','Inspect allocated and reserved storage','Avoid unnecessary graph retention','Sum simultaneously live allocations, not only the input matrix.'),
'mle.training_bottleneck_profiling':('''import torch
from torch.profiler import profile, record_function
warm_up_workload()
with profile(activities=declared_activities) as prof:
    with record_function("data_loading"):
        features, targets = next(iterator)
    with record_function("model_computation"):
        run_bounded_model_computation(features, targets)
inspect_profile(prof.key_averages().table())
# During a containerized interval, inspect docker stats and docker top.''','''# Final comparison: same workload, no profiler overhead.
apply_one_supported_bottleneck_change()
warm_up_workload()
if using_cuda:
    torch.cuda.synchronize()
start = clock()
run_same_bounded_workload()
if using_cuda:
    torch.cuda.synchronize()
elapsed = clock() - start
compare_with_matched_reference(elapsed)''','Attribute observed work','Verify unprofiled completion time','Synchronize accelerator timing boundaries.'),
'ml.task_specific_pretrained_weight_fine_tuning':('''import torch
from torch import nn
from transformers import AutoImageProcessor, ViTForImageClassification
from transformers import TrainingArguments, Trainer
model = ViTForImageClassification.from_pretrained(checkpoint)
processor = AutoImageProcessor.from_pretrained(checkpoint)
original_id2label = dict(model.config.id2label)
original_label2id = dict(model.config.label2id)
inputs = processor(images, return_tensors="pt")
frozen_baseline_logits = model(**inputs).logits
# Retain baseline outputs on the same validation cohort.''','''for parameter in model.parameters():
    parameter.requires_grad = False
model.classifier = nn.Linear(model.config.hidden_size, num_labels)
model.num_labels = model.config.num_labels = num_labels
model.config.id2label = id2label
model.config.label2id = label2id
args = TrainingArguments(output_dir=output_dir, num_train_epochs=epochs,
    per_device_train_batch_size=batch_size, learning_rate=learning_rate,
    eval_strategy="epoch", remove_unused_columns=False)
trainer = Trainer(model=model, args=args, train_dataset=train_dataset,
    eval_dataset=validation_dataset, data_collator=data_collator,
    processing_class=processor)
trainer.train()
# Verify head changes, frozen backbone, and selected head gradient.
# Compare same-cohort validation under fixed cost/acceptance rules.''','Pretrained mapping and processor','Task head and bounded adaptation','Keep baseline and task mappings distinct.')
}
# Short recaps use glossary objectives, not invented outcomes.
recaps=[
'Check separate tensor shapes and dtypes, preserve paired observations through minibatches, and match layer widths and outputs to the task contract.',
'Compare autograd with the chain rule, select a compatible loss representation, and verify the fresh-gradient plain-SGD update.',
'Update per minibatch, keep validation forward-only with the right mode, and verify saved/restored state and predictions.',
'Use predeclared validation improvement and patience, preserve a snapshot of accepted best weights, and test one evidence-supported failure correction.',
'Verify compatible devices, choose batch size from measured eligible work, and distinguish live allocations from cached storage when diagnosing exhaustion.',
'Attribute observed bottlenecks, verify matched unprofiled timing, and compare hardware using task quality, memory and scoped billing evidence.',
'Keep pretrained and task label maps distinct. Verify head gradients and updates with a frozen backbone, then compare matched validation under fixed cost rules; exclude protected-test data.'
]
result={k:p[k] for k in ('schema_version','path_id','batch_id')};result['kind']='screens_part';result['tiles']=[]
for ti,tp in enumerate(p['tiles']):
 tile={'tile_id':tp['tile_id'],'title': ' / '.join(cs[c]['context']['concept_name'] for c in tp['concept_ids']), 'steps':[], 'remediation_steps':[]}
 for sp in tp['steps']:
  cid=sp['concept_ids'][0]
  lineage={'concept_ids':sp['concept_ids'],'teaching_block_ids':sp['teaching_block_ids'],'fact_ids':sp['fact_ids'],'segment_ids':sp['segment_ids'],'anchors':sp['anchors']}
  s={'step_id':sp['step_id'],'type':sp['type'],'concept_ids':sp['concept_ids'],'title':cs[cid]['context']['concept_name'],'eyebrow':{'explainer':'Learn','video':'Demonstration','check':'Check','hands_on':'Apply','recap':'Takeaways'}[sp['type']],'lineage':copy.deepcopy(lineage)}
  if sp['type'] in ('check','hands_on'):
   s['title']=('Check: ' if sp['type']=='check' else 'Apply: ')+cs[cid]['coverage']['learning_objective']
  elif sp['type']=='video':
   s['title']='A worked demonstration';s['blocks']=[{'type':'media_group','segment_ids':sp['segment_ids']}]
  elif sp['type']=='recap':
   s['title']='Keep these contracts together'
   facts=[c+'#'+f['id'] for c in tp['concept_ids'] for f in cs[c]['coverage']['required_facts']]
   blocks=[prose(recaps[ti],{'concept_ids':tp['concept_ids'],'fact_ids':facts,'teaching_block_ids':[c+'#'+t['id'] for c in tp['concept_ids'] for t in cs[c]['teaching_blocks'] if t['purpose']=='mechanism']},'takeaway')]
   next_id=tp['next_tile_id'];next_plan=next((t for t in p['tiles'] if t['tile_id']==next_id),None)
   next_name=cs[next_plan['concept_ids'][0]]['context']['concept_name'] if next_plan else g['names']['mle.ml_training_script']
   blocks.append({'type':'up_next','title':next_name,'text':'Next: '+next_id})
   s['blocks']=blocks
  else:
   s['blocks']=[]
   for qid in sp['teaching_block_ids']:
    tcid,tid=qid.split('#');tb=tbs[tcid][tid]
    # Intro framing has its TB lineage, while fact teaching occurs in the mechanisms.
    pl=lin(tcid,[tid],tb['fact_ids'])
    for text in chunks(voice[(tcid,tid)]):s['blocks'].append(prose(text,pl,tb['purpose']))
   vt=sp['planned_visual_block_type']
   vl=copy.deepcopy(lineage);vl['anchors']=[cid+'#visual']
   if vt=='code_walkthrough':s['blocks'].append(code(walks[cid],vl))
   elif vt in ('side_by_side','before_after'):
    if cid=='mle.training_hardware_selection':
     a='ds.hardware_comparison';left=table(a,vl,['option','model_device','feature_device','target_device','completed','task_quality_requirement_met','observed_memory_bytes','memory_limit_bytes','execution_seconds']);right=table(a,vl,['option','rate_per_second','execution_compute_cost','lifecycle_seconds','lifecycle_compute_cost','billing_scope','stopped_state_verified','final_instance_state','remaining_charge_note'])
     labels=('Matched workload eligibility','Measured billing scope');takeaway='Compare eligible completion with scoped compute cost.'
    else:
     a,b,ll,rl,takeaway=pairs[cid];left=code(a,vl);right=code(b,vl);labels=(ll,rl)
    if vt=='side_by_side':v={'type':vt,'left':left,'right':right,'left_label':labels[0],'right_label':labels[1],'takeaway':takeaway,'lineage':vl}
    else:v={'type':vt,'before':left,'after':right,'change_summary':takeaway,'lineage':vl}
    s['blocks'].append(v)
   elif vt=='diagram':
    chain=re.search(r'visible: (.*?)\. Annotate',sp['visual_purpose']).group(1).split(' → ')
    nodes=[{'id':f'layer_{i}', 'label':label} for i,label in enumerate(chain)]
    nodes[0]['fields']=['Leading minibatch dimension is preserved']
    nodes[-1]['fields']=["The supplied contract has an unconstrained final output"]
    s['blocks'].append({'type':'diagram','diagram_kind':'layers','title':'Fixture dimension chain',
      'nodes':nodes,'edges':[{'from':nodes[i]['id'],'to':nodes[i+1]['id'],'directed':True} for i in range(len(nodes)-1)],
      'layout':'auto','alt_text':sp['visual_purpose'],'lineage':vl})
   elif vt=='data_table':s['blocks'].append(table('ds.batch_size_trials',vl))
  tile['steps'].append(s)
 # Primary remediation per concept comes first. A second measured fact set gets
 # a separate target, allowing different checks to route to their own facts.
 signatures=[]
 for cid in tp['concept_ids']:
  assessed=[sp for sp in tp['steps'] if sp['type'] in ('check','hands_on') and cid in sp['concept_ids']]
  seen=set()
  for sp in assessed:
   sig=tuple(sp['fact_ids'])
   if sig not in seen:seen.add(sig);signatures.append((cid,sp,sig))
 primaries=[];extras=[];seen_c=set()
 for item in signatures:
  if item[0] in seen_c:extras.append(item)
  else:primaries.append(item);seen_c.add(item[0])
 for ri,(cid,sp,sig) in enumerate(primaries+extras,1):
  # Use the smallest glossary teaching-block set that explicitly covers facts.
  fids=[q.split('#')[1] for q in sig]
  needed=[]
  for tb in cs[cid]['teaching_blocks']:
   if tb['purpose']=='mechanism' and set(tb['fact_ids'])&set(fids):needed.append(tb['id'])
  rl=lin(cid,needed,fids)
  blocks=[]
  for fid in fids:
   fact=next(f for f in cs[cid]['coverage']['required_facts'] if f['id']==fid)
   text=fact['statement'].replace('Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.', 'Use assert predicates on valid, boundary and failure fixtures. A false predicate raises AssertionError during ordinary non-optimized execution.')
   fl=lin(cid,[tid for tid in needed if fid in tbs[cid][tid]['fact_ids']],[fid])
   for chunk in chunks(text):blocks.append(prose(chunk,fl))
  misconception=next(tb for tb in cs[cid]['teaching_blocks'] if tb['purpose']=='misconception')
  blocks.append(prose(voice[(cid,misconception['id'])],lin(cid,[misconception['id']],misconception['fact_ids']),'misconception'))
  # The bounded example refers to exactly the same fixture as the main teaching.
  example=next(tb for tb in cs[cid]['teaching_blocks'] if tb['purpose']=='example')
  # One short concrete contrast, sourced from the first complete example sentence.
  contrast=re.split(r'(?<=[.!?])\s+(?=[A-Z])',voice[(cid,example['id'])])[0]
  blocks.append(prose(contrast,lin(cid,[example['id']],example['fact_ids']),'example'))
  tile['remediation_steps'].append({'step_id':tp['tile_id']+f'.r{ri:02d}','type':'remediation','concept_ids':[cid],'title':'Recheck: '+cs[cid]['coverage']['learning_objective'],'eyebrow':'One clear contrast','blocks':blocks,'lineage':rl})
 result['tiles'].append(tile)
(B/'screens.json').write_text(json.dumps(result,indent=2)+'\n')
print('Tiles:',len(result['tiles']),'Steps:',sum(len(t['steps']) for t in result['tiles']),'Remediation:',sum(len(t['remediation_steps']) for t in result['tiles']))
