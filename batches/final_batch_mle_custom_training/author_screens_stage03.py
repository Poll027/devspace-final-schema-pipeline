import json, re, copy
from pathlib import Path
B=Path('batches/final_batch_mle.region.custom_training')
P=json.loads((B/'tile_plans.json').read_text()); G=json.loads((B/'inputs/path_glossary_bundle.json').read_text()); R=json.loads((B/'scenario_asset_registry.json').read_text())
C={c['context']['concept_id']:c for c in G['bundles']}
A={a['asset_id']:a for a in R['assets']}
# Authored re-voicing, indexed in the glossary's teaching-block order.
TEXT={
'pytorch_input_tensors':[
'For the numerical order arrays, feature and target representations have separate contracts. A shared feature dtype is not enough.',
'Import torch and construct each tensor with torch.from_numpy(array). Apply tensor.to(dtype=declared_dtype) separately to features and targets. Inspect shape and dtype, and verify corresponding observation order. Assert the declared axes and common batch length before returning the aligned tensors as a tuple.',
'Check the valid, boundary and failure fixtures with assert predicates. A false predicate raises AssertionError in ordinary, non-optimized execution.',
'In the supplied order-array pair, inspect feature and target axes separately. A target array with too few rows may convert successfully but still fail alignment. A wrong target representation is a separate defect: do not derive its dtype from the features. Return the tuple only after both contracts and row correspondence pass. Check the accepted pair, supplied boundary and incompatible fixtures, rather than treating conversion success as acceptance.',
'Conversion alone is not acceptance. Use the declared target dtype, and check batch correspondence even when individual values look valid.'
],
'dataset_minibatch_loader':[
'The dataset defines a paired observation; the loader groups observations using a declared size and ordering policy.',
'In a map-style Dataset, __len__ supplies the sample count and __getitem__(index) supplies an item. For list observations, fetch features and targets at the same index and return a tuple. Configure DataLoader(dataset, batch_size=declared_size, shuffle=declared_order_policy), then iterate for features, targets in loader.',
'Batching preserves each item’s feature/target relationship. drop_last=True discards an incomplete final batch; drop_last=False, the default, retains it with fewer samples. Test boundaries against that policy. Use assert for valid, boundary and failure fixtures; false predicates raise AssertionError during ordinary non-optimized execution.',
'In the supplied indexed-observation fixture, retaining the incomplete batch produces a smaller final batch; dropping it removes that batch. Neither policy creates observations. Verify __len__, item identities and batch boundaries. Same-index retrieval establishes pairing before collation: well-shaped batches can still contain mismatched items. Shuffle changes ordering, not the feature/target relationship, so do not assume the first loader item is the first source row.',
'A loader cannot fill a partial batch by assumption. Declare drop_last explicitly; establish alignment in each dataset item.'
],
'neural_model_definition':[
'Match layer widths and final outputs to the supplied task contract.',
'Import torch.nn as nn. An nn.Module subclass calls super().__init__(), registers layers as attributes and defines forward(self, x). nn.Linear(in_features, out_features) uses learned weights and bias to map feature vectors to outputs while preserving the leading minibatch dimension. nn.ReLU applies max(0, x) elementwise, introducing nonlinearity between linear layers.',
'nn.Sequential applies modules in declared order. Match each output width to the following input width. Choose final width and activation from the task contract, then verify output shape with a fixture batch.',
'Follow the supplied dimension chain for one observation, then restore the leading batch axis. Linear layers change per-observation width; ReLU changes values elementwise without changing that width. Register layer attributes and define forward, or inspect the declared Sequential composition. Check the final activation against the task. A mismatched intermediate width is not repaired by changing batch size.',
'Layer widths are per-observation dimensions, not sample counts. Let the supplied task determine final width and activation.'
],
'autograd_gradients':[
'Trace the scalar loss back to its parameters. A matrix-shaped reference makes the learning signal inspectable.',
'Autograd records tensor operations in a graph and differentiates the scalar output by the chain rule. Mark trainable leaf tensors requires_grad=True, form the scalar loss, call loss.backward() and inspect each leaf’s .grad. Backward accumulates gradients: clear old values before a fresh comparison.',
'For Z = XW + b and D = ∂L/∂Z, the references are ∂L/∂W = X.T @ D and ∂L/∂b = D.sum(axis=0). D already includes loss reduction. Compare gradient shapes and values using explicit relative and absolute tolerances. Assert valid, boundary and failure predicates; false predicates raise AssertionError during ordinary non-optimized execution.',
'Use the supplied X and D once in the matrix reference. Each weight combines its feature column with D; the bias combines derivatives across rows. Do not divide again for a reduction already included in D. Compare .grad after backward and before clearing, using the declared shapes and tolerances. A transpose error or stale accumulation can invalidate a plausible-looking value. Include the differing-gradient failure fixture as well as an accepted computation.',
'Backward accumulates; it does not automatically replace old gradients. Correct shapes and the supplied reduction convention matter as much as plausible numbers.'
],
'task_loss_selection':[
'Choose the output/target contract before computing loss. A scalar value alone cannot verify the representation.',
'A loss compares outputs with corresponding targets. For class-index CrossEntropyLoss, use unnormalized logits shaped (N, C) and long targets shaped (N,) with indices in [0, C). MSELoss requires input and target tensors of the same shape; mean reduction averages squared elementwise differences.',
'BCEWithLogitsLoss combines sigmoid with binary cross-entropy: supply logits and same-shaped targets in [0, 1], not already-sigmoid inputs. For mean MSE over M elements, the output derivative is 2 × (output−target)/M. Its sign identifies the direction of increasing loss as outputs move away from targets. For unweighted mean binary-logit loss over M elements, it is (sigmoid(logit)−target)/M. These distinguish raw logits, probabilities and numerical outputs.',
'For unweighted mean class-index cross-entropy, each sample’s logit derivative is (softmax probability−one-hot target)/N. The target identity, output width and sample-count reduction belong in the reference.',
'Compare the supplied MSE, binary-logit and class-index fixtures under their distinct contracts. Keep the mean-reduction denominator visible and inspect derivative direction as well as scalar loss. Binary-logit loss compares the sigmoid probability with its target, but receives raw logits. Class-index loss requires the declared class width and long target indices. Verify axes and dtype before applying the reference; a positive scalar does not establish the correct representation.',
'CrossEntropyLoss and BCEWithLogitsLoss receive logits. Check MSE’s same-shape contract instead of relying on accidental broadcasting.'
],
'optimizer_configuration':[
'A deterministic single step distinguishes a current gradient from the parameter change it should produce.',
'Bind the trainable parameters with torch.optim.SGD(model.parameters(), lr=declared_learning_rate). Only for plain SGD without momentum, weight decay or other modifications, parameter_new = parameter_old − learning_rate × gradient. Clear old gradients with optimizer.zero_grad(), compute loss.backward(), then use optimizer.step() for the current update.',
'Compare one deterministic update with that conditional plain-SGD equation; it is not every optimizer’s rule. Assert valid, boundary and failure predicates. False predicates raise AssertionError during ordinary non-optimized execution.',
'In the supplied one-step fixture, retain the parameter before and after step and the current gradient separately. Compare the observed difference with the plain-SGD reference under declared tolerances. Backward without step can produce a gradient without updating the parameter. Bind model.parameters(), clear old gradients before a fresh backward, and retain the restrictions on momentum, weight decay and other modifications. Do not extend the equation to a different optimizer.',
'A learning rate does not update parameters by itself. Backward must reach step; the plain-SGD equation retains its stated restrictions.'
],
'minibatch_training_loop':[
'Every minibatch in each declared epoch needs the intended current-gradient update and enough loss evidence to interpret partial batches.',
'Inside each epoch, iterate for features, targets in loader. Compute model(features) and loss_fn(predictions, targets). For each minibatch, call optimizer.zero_grad(), loss.backward() and optimizer.step(). Collect scalar loss.item() evidence with batch counts so an incomplete batch is represented correctly in the epoch summary.',
'Assert the valid, boundary and failure predicates; a false predicate raises AssertionError during ordinary non-optimized execution. In a plain-SGD fixture, retain pre-step parameters and check parameter_after − parameter_before against −learning_rate × current_gradient under tolerance.',
'The retained final minibatch in the supplied order fixture is smaller than the configured maximum. Record its actual count with its scalar loss before applying the declared epoch-summary rule. Keep the full zero/backward/step sequence inside each minibatch of each epoch. Retain one pre-step parameter and verify its change at that same minibatch under the plain-SGD reference. A differently positioned step or an old gradient contribution describes a different procedure.',
'An epoch is more than a step count. Preserve actual batch counts for loss summaries, and clear old gradients before the next minibatch’s update.'
],
 'training_evaluation_modes':[
'Validation needs two controls: layer behavior and gradient recording. Neither control replaces the other.',
'model.train() selects training behavior; model.eval() selects validation behavior for relevant layers such as dropout and batch normalization. Use with torch.no_grad(): around validation prediction to disable gradient-graph recording. eval changes layer behavior, while no_grad changes recording.',
'Validation is forward-only: omit optimizer.step() and restore model.train() before the next training pass. Test valid, boundary and failure predicates with assert; false predicates raise AssertionError in ordinary non-optimized execution. Import torch and nn from torch for the supplied nn.Dropout fixture. Training randomly zeros each element with probability p and scales retained values by 1/(1-p). Evaluation returns x unchanged. Check identity and permitted masking/scaling without requiring every random call to mask an element. no_grad does not select evaluation behavior.',
'In the supplied dropout fixture, inspect mode and recording context independently. Evaluation behaves as an identity even when recording is enabled. Training can still mask and scale values inside no_grad. Compare the permitted stochastic outcomes rather than demanding a particular random mask. Validation also excludes updates; disabling the graph alone does not describe the whole pass. Restore training mode afterward.',
'eval does not disable recording; no_grad does not switch dropout behavior. Validation must also exclude parameter updates.'
],
'weight_persistence':[
'Restoring learned state requires a compatible architecture and checks of both parameters and fixed-fixture predictions.',
'torch.save(model.state_dict(), path) saves learned parameters. Reconstruct the same compatible architecture, read the mapping with torch.load(path, weights_only=True), and apply model.load_state_dict(mapping). Select model.eval() before restored prediction.',
'Compare original and restored evaluation predictions on the same fixture with explicit numerical tolerances. Assert valid, boundary and failure predicates; false predicates raise AssertionError during ordinary non-optimized execution. For the specified handle-based path, open with open(path, "wb") to save and open(path, "rb") to load, passing the binary handle to torch.save or torch.load.',
'Also compare corresponding original and restored state_dict entries to verify preserved parameter state.',
'Keep the original evaluation predictions as the reference, rather than generating both references with the restored object. Save and load through binary handles, reconstruct the compatible architecture and apply the parameter mapping. Compare corresponding entries separately from the same-fixture prediction check. One matching output does not replace state verification. Distinguish an incompatible architecture or differing entry from successful restoration.',
'Weight loading does not choose an architecture. Use compatible structure, matching evaluation fixtures and parameter-entry checks.'
],
'validation_early_stopping':[
'Early stopping follows predeclared improvement and patience rules. Preserve the accepted checkpoint, not automatically the last epoch.',
'Declare the validation quantity, direction, min_delta and patience. For minimization, reset the consecutive non-improvement count only if current < best − min_delta; otherwise increment and stop when patience is exhausted. best is the most recently accepted checkpoint’s value, not necessarily the lowest observation. Retain that checkpoint’s weights.',
'A state_dict references live values: deep-copy the accepted state or save it before further updates. Keep protected-test observations out of preprocessing fit, model selection and tuning to avoid leakage. Bound the controller’s while loop by maximum epochs and the non-improvement rule. Update best loss and checkpoint within the improvement branch; break when patience is exhausted.',
'Trace the registered validation sequence using its strict min_delta comparison. A smaller observed loss can still be insufficient improvement, leaving the previously accepted checkpoint unchanged. Reset or increment the counter at every epoch, and honor both patience and the maximum-epoch bound. Deep-copy or save weights when improvement is accepted, then restore that snapshot instead of the last live weights. Protected-test observations do not choose patience or the checkpoint.',
'A live state_dict is not a frozen snapshot. A small loss decrease need not pass min_delta; preserve the accepted state before later updates.'
],
 'training_failure_diagnosis':[
'Reproduce the failure; inspect loss, representation and gradients before changing settings.',
'Inspect expected trainable parameters’ .grad after backward and before clearing. Compare losses, output/target compatibility and learning rate with the declared computation. Choose one evidence-supported correction and rerun the identical bounded fixture, comparing loss and gradient records with the failing reference.',
'Assert valid, boundary and failure predicates; false predicates raise AssertionError in ordinary non-optimized execution. Follow the derivative chain from loss through outputs to parameters, checking expected signs and measured magnitudes. Test one root-cause hypothesis on the reproduced failure.',
'For the supplied missing-gradient failure, compare the expected sign with the measured gradient at the same point after backward. Follow the derivative chain, checking target representation and declared learning rate alongside loss. Preserve the failing reference while testing one supported correction on the identical fixture. Compare corrected signs, magnitudes and losses. Several simultaneous changes or a different task would not isolate that hypothesis; disappearance of an exception alone is insufficient.',
'A stalled loss is not permission for arbitrary changes. Inspect gradients before zeroing them, then test one evidence-supported correction.'
],
 'device_placement':[
'An accelerator label does not establish placement. Verify availability and the devices of the model, features and targets.',
'Check torch.cuda.is_available() before selecting torch.device("cuda"); otherwise use the supported CPU device. Move the model with model.to(device) and each feature and target tensor with tensor.to(device). Inspect parameter and minibatch devices, then check the declared placement with a bounded forward/backward fixture.',
'Assert valid, boundary and failure predicates; false predicates raise AssertionError in ordinary non-optimized execution. Only for the authorized supplied VM, gcloud compute instances start INSTANCE --zone=ZONE and gcloud compute instances stop INSTANCE --zone=ZONE change lifecycle state. Wait and inspect the result. gcloud compute ssh INSTANCE --zone=ZONE connects to the running authorized VM for the workload.',
'gcloud compute instances describe INSTANCE --zone=ZONE checks identity and status before and after the authorized action. After the bounded workload, stop that instance, wait for completion and verify its stopped state.',
'The authorized lifecycle procedure and tensor placement are separate checks. Inspect instance identity and state before acting. Select CUDA only after checking availability, otherwise record the supported CPU path. Move and inspect the model, features and targets together; moving only features is insufficient. Check the bounded forward/backward fixture. After the workload, stop the authorized instance, wait and verify its state. Record actual placement rather than copying the intended hardware label.',
'A running VM does not prove tensor placement. Verify availability, compatible devices and the bounded fixture; stop and verify the authorized VM afterward.'
],
 'training_batch_sizing':[
'A larger batch may improve throughput but must satisfy the declared memory bound. Input bytes are only an estimate.',
'Training memory includes other live allocations; larger batches ordinarily require more activation storage. Change only DataLoader batch_size, keeping alignment and the task fixed. For each CUDA trial, reset_peak_memory_stats() before the workload and inspect torch.cuda.max_memory_allocated() afterward for peak allocated tensor bytes.',
'That peak does not cover every component of GPU usage: use the quantity governed by the supplied budget. Compare completed work per elapsed time among eligible sizes. Estimate features as batch_rows × feature_columns × bytes_per_feature_element, add targets under their own dtype, and compare the estimate with the measured peak.',
'Inspect the registered batch-size trials rather than equating feature-plus-target bytes with total training memory. Keep the task, alignment and measurement protocol fixed. Reset each CUDA trial’s peak before measuring; otherwise an earlier peak can contaminate the comparison. Record actual batch shapes, including the partial final batch, with completed examples and elapsed time. Higher throughput does not rescue a setting outside the declared memory bound. Select only among settings meeting the supplied requirements.',
'Allocated-tensor peak is not total GPU usage. Input-byte estimates omit other live allocations; eligibility must follow the declared measured-memory scope.'
],
 'training_memory_diagnosis':[
'Locate the failure: distinguish occupied tensors, reserved storage and retained graphs.',
'CUDA memory_allocated measures tensor-occupied memory; memory_reserved includes caching-allocator storage. Inspect peak allocated and reserved memory and the failure point. Graph-connected saved tensors can retain graph memory; use detached or scalar diagnostics when gradients through saved values are unnecessary.',
'empty_cache releases unused cache, not storage occupied by live tensors. Test one supported change, such as smaller batches or removing an unnecessary graph reference, on the same bounded workload; verify completion and peak. Count each parameter, gradient, activation and batch matrix as element_count × element_width, summing simultaneously live allocations rather than inputs alone.',
'For a linear layer with widths F and H, weights contain F × H elements and bias contains H. These counts support the parameter-allocation reference.',
'Use the supplied linear-layer widths to count weight and bias elements separately. Apply each allocation’s element width, then include simultaneously live gradients, activations and batch matrices. At the reproduced failure, inspect allocated/reserved evidence and saved graph-connected diagnostics. Test one supported correction on the same bounded workload and compare completion and measured peak with the failed reference. Do not sum every tensor ever created or treat a smaller successful task as the same comparison.',
'empty_cache cannot release live tensor storage. Reserved differs from allocated, and the input matrix alone does not explain training memory.'
],
 'training_bottleneck_profiling':[
'Duration shows slowness, not attribution. Separate loading and computation before choosing a supported bottleneck change.',
'Use the PyTorch profiler context and record_function labels around loading and model computation. Inspect key_averages().table(...) or the trace for operator and labeled-region attribution. Warm up before steady-state comparison; exclude profiler overhead from the final unprofiled timing.',
'CUDA is asynchronous: synchronize CPU-clock measurement boundaries to include completed accelerator work. Change one supported factor and compare the same bounded workload again. Inspect CPU, memory and process state in that interval; docker stats and docker top support a containerized run’s resource evidence, distinct from stage timing.',
'Keep attribution and final timing separate. If the labeled trace implicates loading, test one supported loading factor rather than changing model computation by assumption. Inspect CPU, memory and process state in the same window. Compare the identical bounded workload after warm-up without profiler overhead for the final elapsed-time comparison. Synchronize accelerator boundaries. Labels must enclose their intended work, not blend loading, computation and setup into an uninterpretable interval.',
'A code change is not measured improvement. Control asynchronous completion, warm-up, profiler overhead and timing boundaries in the matched comparison.'
],
 'training_hardware_selection':[
'Compare CPU and accelerator options on matched work, quality, memory and billing scope, not utilization alone.',
'Check accelerator availability and place the model and minibatches on the selected device. Benchmark the same bounded workload and quality requirements, retaining the declared treatment of data movement and warm-up. Running VMs incur compute billing; stopping compute can leave persistent-disk and other charges.',
'Estimate compute execution cost using measured runtime and the supplied rate, with its billing scope. For authorized supplied VMs only, use gcloud compute instances start INSTANCE --zone=ZONE or stop INSTANCE --zone=ZONE; wait and inspect the resulting state. Connect to a running authorized VM with gcloud compute ssh INSTANCE --zone=ZONE.',
'After the measurement, stop the authorized VM, verify its stopped state and retain runtime/cost evidence. gcloud compute instances describe INSTANCE --zone=ZONE checks identity and status before and after actions. Record memory and completion of the same bounded matrix workload against each option’s fixed limits.',
'After both authorized benchmarks, stop both instances and verify their states. Use measured lifecycle durations for billing.',
'Compare the registered CPU and accelerator records under the same workload, quality and memory limits. Execution cost uses the supplied rate and bounded execution duration; billing interpretation also needs lifecycle duration. Retain the declared movement and warm-up scope. Start, connect to and inspect only authorized instances; stop both after measurement and verify the result. A faster option can still cost more, and persistent-disk or other charges can remain after compute stops.',
'Faster is not automatically cheaper or eligible. Stopping compute does not end every charge; preserve billing scope.'
],
 'task_specific_pretrained_weight_fine_tuning':[
'Adapt the supplied ViT image classifier in a bounded supervised task. Keep original pretrained and task label mappings distinct.',
'Import torch, nn from torch, and AutoImageProcessor, ViTForImageClassification, TrainingArguments and Trainer from transformers. Load the compatible checkpoint with ViTForImageClassification.from_pretrained(checkpoint); retain its original label mapping for the baseline. Load AutoImageProcessor.from_pretrained(checkpoint). Processing images with return_tensors="pt" gives pixel_values; model(**inputs).logits gives logits. Use this processor for both training and validation. With supplied preprocessed datasets and collator, configure TrainingArguments with output_dir, num_train_epochs, per_device_train_batch_size and learning_rate as declared, eval_strategy="epoch" and remove_unused_columns=False. Configure Trainer with model, args, train_dataset, eval_dataset=validation_dataset, data_collator and processing_class=processor. Trainer.train() performs the bounded adaptation.',
'For classifier-only adaptation, set existing parameters’ requires_grad=False, then replace model.classifier with nn.Linear(model.config.hidden_size, num_labels). Update model.num_labels, config.num_labels, config.id2label and config.label2id to the task mapping. New head parameters are trainable by default. Verify changed head weights and unchanged frozen backbone. Compare task predictions with the frozen pretrained reference on the same validation cohort, without an application or protected-test data. Binary FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) conditions on actual positives. Empty conditioning groups give undefined rates.',
'With zero cost for correct predictions, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN, using supplied deployment probabilities. Keep protected tests out of preprocessing fit, model choice and tuning to prevent leakage. For a class-index head, verify logits (N, C), targets (N,) and long indices in [0, C), with C matching the task map.',
'Compute task loss, backpropagate and compare a selected head gradient with the chain-rule reference inside adaptation before claiming the intended supervised update.',
'For the supplied task images, retain the original baseline mapping and checkpoint processor. Freeze existing parameters before replacing the head; update both label maps and class-count settings. Verify class-index shapes and dtype, a selected head gradient, changed head weights and unchanged backbone. Compare against the frozen reference on the same validation cohort under fixed cost and acceptance rules. Keep protected tests outside adaptation and selection.',
'Freezing existing parameters does not freeze a new head. Changed weights alone do not verify target mapping or matched validation.'
]}

def short(cid): return cid.split('.')[-1]
def lin(cid,tbs=(),facts=(),anchors=()):
 return {'concept_ids':[cid], 'teaching_block_ids':[x if '#' in x else cid+'#'+x for x in tbs], 'fact_ids':[x if '#' in x else cid+'#'+x for x in facts], 'anchors':list(anchors)}
def prose(text,lineage,role='mechanism'):
 # Split only at sentence boundaries, retaining one small idea per block.
 sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z])',text)
 out=[]; acc=''
 for sentence in sentences:
  if acc and len((acc+' '+sentence).split())>85:
   out.append({'type':'prose','text':acc,'role':role,'lineage':copy.deepcopy(lineage)}); acc=''
  acc=(acc+' '+sentence).strip()
 if acc: out.append({'type':'prose','text':acc,'role':role,'lineage':copy.deepcopy(lineage)})
 return out

def code(src,L):return {'type':'code_walkthrough','language':'python','code':src.strip(),'reveal':'all','lineage':copy.deepcopy(L)}
def diagram(labels,L,title):
 ids=['node'+str(i) for i in range(len(labels))]
 return {'type':'diagram','diagram_kind':'sequence','title':title,'nodes':[{'id':i,'label':s} for i,s in zip(ids,labels)],'edges':[{'from':ids[i],'to':ids[i+1],'directed':True} for i in range(len(ids)-1)],'alt_text':title+': '+labels[0]+' leads to '+labels[-1],'lineage':copy.deepcopy(L)}
def table(aid,L):return {'type':'data_table','asset_ref':{'asset_id':aid,'columns':[x['name'] for x in A[aid]['columns']]},'caption':A[aid]['title'],'lineage':copy.deepcopy(L)}

def visual(cid,kind,L):
 k=short(cid)
 if k=='pytorch_input_tensors':
  return code('''import torch

def aligned_pair(features_array, targets_array, feature_dtype, target_dtype,
                 feature_shape, target_shape):
    features = torch.from_numpy(features_array).to(dtype=feature_dtype)
    targets = torch.from_numpy(targets_array).to(dtype=target_dtype)
    assert features.shape == feature_shape
    assert targets.shape == target_shape
    assert features.dtype == feature_dtype
    assert targets.dtype == target_dtype
    assert features.shape[0] == targets.shape[0]
    return features, targets

# Inspect shape, dtype and correspondence separately.
# Apply the same predicates to accepted, boundary and failure cases.
# A shorter target array may convert but fails the common-batch assertion.''',L)
 if k=='dataset_minibatch_loader':
  return code('''from torch.utils.data import Dataset, DataLoader

class PairedItems(Dataset):
    def __init__(self, features, targets):
        self.features, self.targets = features, targets
        assert len(features) == len(targets)
    def __len__(self):
        return len(self.features)
    def __getitem__(self, index):
        return self.features[index], self.targets[index]

loader = DataLoader(dataset, batch_size=declared_size,
                    shuffle=declared_order_policy, drop_last=declared_drop_last)
for features, targets in loader:
    assert len(features) == len(targets)
# True drops an incomplete final batch; False retains the smaller batch.
# Check item identities as well as the declared batch boundaries.''',L)
 if k=='neural_model_definition':
  source=C[cid]['teaching_blocks'][3]['content']
  widths=re.search(r'widths ([0-9]+ → [0-9]+ → [0-9]+)',source).group(1).split(' → ')
  labels=['Input: '+widths[0]+' features per observation','Linear: '+widths[0]+' → '+widths[1],'ReLU: elementwise; width unchanged','Linear: '+widths[1]+' → '+widths[2],'Output: leading minibatch dimension preserved']
  return diagram(labels,L,'Task-bounded layer chain')
 if k=='autograd_gradients':return code('''# X and D are the supplied matrix-shaped references.
# D already contains the loss reduction.
weight_reference = X.T @ D
bias_reference = D.sum(axis=0)
# Trainable leaf tensors have requires_grad=True.
# Clear prior .grad before this fresh computation.
loss.backward()
weight_gradient = W.grad
bias_gradient = b.grad
# Compare shapes and values under explicit relative/absolute tolerances.
# Inspect here, before clearing; include a differing-gradient failure.''',L)
 if k=='task_loss_selection':return code('''from torch import nn

class_index_loss = nn.CrossEntropyLoss()
# Unnormalized logits: (N, C); long targets: (N,), indices in [0, C).
numerical_loss = nn.MSELoss(reduction="mean")
# Input and target shapes match; mean squared elementwise differences.
binary_logit_loss = nn.BCEWithLogitsLoss(reduction="mean")
# Raw logits and same-shaped targets in [0, 1], not sigmoid inputs.''',L)
 if k=='optimizer_configuration':
  return {'type':'before_after','before':code('''optimizer = torch.optim.SGD(model.parameters(), lr=declared_learning_rate)
# Plain SGD only: no momentum, weight decay or other modifications.
parameter_before = parameter.detach().clone()
optimizer.zero_grad()
loss.backward()
# .grad is now the current gradient; no step yet.''',L),'after':code('''optimizer.step()
# Compare parameter_after - parameter_before with:
# -declared_learning_rate * current_gradient
# Use declared tolerances; backward without step does not apply this update.''',L),'change_summary':'Step applies the current gradient.','lineage':L}
 if k=='minibatch_training_loop':return code('''for epoch in range(declared_epochs):
    batch_evidence = []
    for features, targets in loader:
        predictions = model(features)
        loss = loss_fn(predictions, targets)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        batch_evidence.append((loss.item(), len(features)))
    # Apply the declared summary rule with actual batch counts.
# Plain-SGD fixture: retain pre-step values and check the change
# against -learning_rate * current_gradient under tolerance.''',L)
 if k=='training_evaluation_modes':
  p=re.search(r'p=([0-9.]+)\.',C[cid]['teaching_blocks'][2]['content']).group(1)
  left=code('from torch import nn\ndropout = nn.Dropout(p='+p+')\nmodel.train()\n# Each element is masked with probability p.\n# Retained values are scaled by 1/(1-p).\n# A random call need not mask any element.',L)
  right=code('''model.eval()
with torch.no_grad():
    predictions = model(features)
# Evaluation dropout returns its input unchanged.
# No optimizer.step in validation.
model.train()  # restore before the next training pass''',L)
  return {'type':'side_by_side','left':left,'right':right,'left_label':'Training behavior','right_label':'Validation controls','takeaway':'Mode and recording are separate.','lineage':L}
 if k=='weight_persistence':
  return {'type':'side_by_side','left':code('''import torch
with open(path, "wb") as handle:
    torch.save(model.state_dict(), handle)
# Retain original evaluation predictions and parameter entries.''',L),'right':code('''restored = compatible_architecture()
with open(path, "rb") as handle:
    mapping = torch.load(handle, weights_only=True)
restored.load_state_dict(mapping)
restored.eval()
# Compare corresponding entries and same-fixture predictions.
# Use explicit numerical tolerances.''',L),'left_label':'Preserve state','right_label':'Restore and verify','takeaway':'State and prediction checks complement each other.','lineage':L}
 if k=='validation_early_stopping':
  return code('''# Minimized validation quantity; best belongs to an accepted checkpoint.
while epoch < maximum_epochs:
    current = validation_quantity()
    if current < best - min_delta:
        best = current
        counter = 0
        # Deep-copy state_dict or save a state file here.
    else:
        counter += 1
    if counter >= patience:
        break
    epoch += 1
# Retain the accepted snapshot, not automatically the last live weights.''',L)
 if k=='training_failure_diagnosis':
  return {'type':'side_by_side','left':diagram(['Reproduced bounded failure','Loss and output/target contract','After backward: gradient signs and magnitudes','Declared learning rate'],L,'Failure'),'right':diagram(['One supported hypothesis','One correction; identical fixture','Matched losses and gradients','Assert expectations'],L,'Correction'),'left_label':'Diagnose evidence','right_label':'Test one cause','takeaway':'Inspect before clearing gradients.','lineage':L}
 if k=='device_placement':
  return {'type':'before_after','before':code('''# A running accelerator VM does not prove tensor placement.
# Moving features alone leaves model and targets unchecked.
features = features.to(device)''',L),'after':code('''import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
features = features.to(device)
targets = targets.to(device)
# Inspect parameter, feature and target devices.
# Check the bounded forward/backward fixture.
# Authorized VM: inspect identity, wait for lifecycle actions,
# connect for the workload; afterward stop and verify stopped state.''',L),'change_summary':'Check availability and move all participants.','lineage':L}
 if k=='training_batch_sizing':return table('ds.batch_size_trials',L)
 if k=='training_memory_diagnosis':
  return {'type':'side_by_side','left':diagram(['Failure point','Peak allocated: tensor-occupied memory','Reserved: caching-allocator storage','Saved graph-connected diagnostics'],L,'Evidence'),'right':diagram(['Simultaneously live allocations','Parameters, gradients, activations and batches','element_count × element_width for each','One change; same-task completion and peak'],L,'Bounded correction'),'left_label':'Locate exhaustion','right_label':'Account and verify','takeaway':'empty_cache cannot free live tensors.','lineage':L}
 if k=='training_bottleneck_profiling':
  return {'type':'side_by_side','left':code('''# Warm up the bounded workload first.
with torch.profiler.profile() as prof:
    with torch.profiler.record_function("data_loading"):
        features, targets = next(batch_iterator)
    with torch.profiler.record_function("model_computation"):
        predictions = model(features)
# Inspect key_averages().table(...) or the trace.
# Container interval: docker stats and docker top support resource evidence.''',L),'right':diagram(['One trace-supported factor','Same bounded workload after warm-up','No profiler in final timing','Synchronize CUDA timing boundaries','Compare completed work and elapsed time'],L,'Matched timing'),'left_label':'Attribute work','right_label':'Measure improvement','takeaway':'Profiler attribution is not final unprofiled timing.','lineage':L}
 if k=='training_hardware_selection':
  return {'type':'side_by_side','left':table('ds.hardware_comparison',L),'right':diagram(['Authorized identity and initial status','Start; wait; inspect; connect','Same bounded task, placement, quality and memory','Retain execution and lifecycle durations','Stop both; wait; verify both states'],L,'Authorized lifecycle'),'left_label':'Matched option records','right_label':'Lifecycle and billing scope','takeaway':'Execution cost and lifecycle billing differ.','lineage':L}
 if k=='task_specific_pretrained_weight_fine_tuning':
  return {'type':'side_by_side','left':code('''from transformers import AutoImageProcessor, ViTForImageClassification
model = ViTForImageClassification.from_pretrained(checkpoint)
original_id2label = dict(model.config.id2label)
original_label2id = dict(model.config.label2id)
processor = AutoImageProcessor.from_pretrained(checkpoint)
inputs = processor(images, return_tensors="pt")
logits = model(**inputs).logits
# Keep the original mapping for the frozen baseline.
# Use the same checkpoint processor for training and validation.''',L),'right':code('''from transformers import TrainingArguments, Trainer
args = TrainingArguments(
    output_dir=declared_output_dir,
    num_train_epochs=declared_epochs,
    per_device_train_batch_size=declared_batch_size,
    learning_rate=declared_learning_rate,
    eval_strategy="epoch", remove_unused_columns=False)
trainer = Trainer(model=model, args=args, train_dataset=train_dataset,
                  eval_dataset=validation_dataset, data_collator=image_collator,
                  processing_class=processor)
# Trainer.train() is the bounded supervised adaptation.
# The task head and mapping are specified separately.''',L),'left_label':'Checkpoint representation and baseline','right_label':'Bounded supervised configuration','takeaway':'Keep baseline and task mappings distinct.','lineage':L}
 raise ValueError(k)

TAKEAWAYS={
'pytorch_input_tensors':'Check separate dtypes, axes and aligned rows before returning tensors.',
'dataset_minibatch_loader':'Pair items by index and declare incomplete-batch policy.',
'neural_model_definition':'Match layer widths and final task output.',
'autograd_gradients':'Compare fresh gradients with the matrix reference and tolerances.',
'task_loss_selection':'Match logits or numerical outputs to the target contract and reduction.',
'optimizer_configuration':'Verify the current-gradient step under plain-SGD restrictions.',
'minibatch_training_loop':'Repeat zero/backward/step per batch; retain actual counts with losses.',
'training_evaluation_modes':'Validation needs evaluation behavior, no_grad and no updates.',
'weight_persistence':'Restore compatible state and check entries plus fixed-fixture predictions.',
'validation_early_stopping':'Preserve the checkpoint accepted by the declared improvement rule.',
'training_failure_diagnosis':'Inspect gradients before clearing; test one supported correction.',
'device_placement':'Verify availability, all devices and authorized lifecycle completion.',
'training_batch_sizing':'Choose eligible throughput using the budget’s measured-memory scope.',
'training_memory_diagnosis':'Simultaneously live allocations and verify one correction.',
'training_bottleneck_profiling':'Separate attribution from synchronized, unprofiled matched timing.',
'training_hardware_selection':'Compare matched quality, memory, runtime and scoped cost.',
'task_specific_pretrained_weight_fine_tuning':'Verify task mapping, supervised head updates and matched validation.'}
CONTRAST={
'pytorch_input_tensors':'A converted target can still be misaligned; conversion is not acceptance.',
'dataset_minibatch_loader':'Well-shaped batches can contain mismatched items; pairing begins at the same index.',
'neural_model_definition':'Changing sample count cannot fix incompatible per-observation widths.',
'autograd_gradients':'A fresh reference is not an accumulated gradient; inspect before clearing.',
'task_loss_selection':'A scalar loss can exist with the wrong representation; check the contract first.',
'optimizer_configuration':'Backward produces gradients; step applies the parameter update.',
'minibatch_training_loop':'A configured batch maximum is not the actual final-batch count.',
'training_evaluation_modes':'no_grad changes recording, not dropout’s layer mode.',
'weight_persistence':'One matching prediction is not a substitute for corresponding state-entry checks.',
'validation_early_stopping':'A lower observation is not necessarily an accepted improvement under min_delta.',
'training_failure_diagnosis':'Inspecting after zeroing can hide the gradient; compare after backward.',
'device_placement':'A running accelerator does not prove that targets moved with features.',
'training_batch_sizing':'Higher throughput cannot rescue an ineligible measured peak.',
'training_memory_diagnosis':'Unused cache can be released; live tensor storage cannot be freed by empty_cache.',
'training_bottleneck_profiling':'A trace attributes work; final unprofiled timing tests improvement.',
'training_hardware_selection':'Faster completion can cost more; compute stopping need not end disk charges.',
'task_specific_pretrained_weight_fine_tuning':'Frozen existing parameters do not freeze the newly constructed task head.'}

dropout_c=C['mle.training_evaluation_modes']
dropout_p=re.search(r'p=([0-9.]+)\.',dropout_c['teaching_blocks'][2]['content']).group(1)
TEXT['training_evaluation_modes'][2]=TEXT['training_evaluation_modes'][2].replace('the supplied nn.Dropout fixture','the supplied nn.Dropout(p='+dropout_p+') fixture')

RECAP_FACTS={
'pytorch_input_tensors':['f2','f4'], 'dataset_minibatch_loader':['f2','f5'],
'neural_model_definition':['f4','f5'], 'autograd_gradients':['f3','f4','f5'],
'task_loss_selection':['f1','f2','f3','f4','f5','f6','f7'],
'optimizer_configuration':['f2','f3','f4'], 'minibatch_training_loop':['f2','f3'],
'training_evaluation_modes':['f1','f2','f3','f4'], 'weight_persistence':['f2','f4','f7'],
'validation_early_stopping':['f2','f3','f4'], 'training_failure_diagnosis':['f1','f3'],
'device_placement':['f1','f2','f3','f8'], 'training_batch_sizing':['f4','f5'],
'training_memory_diagnosis':['f5','f6'], 'training_bottleneck_profiling':['f2','f3','f4','f5'],
'training_hardware_selection':['f2','f4','f9'],
'task_specific_pretrained_weight_fine_tuning':['f4','f5','f9','f10']}

def step_lineage(s):return {key:copy.deepcopy(s[key]) for key in ['concept_ids','teaching_block_ids','fact_ids','segment_ids','anchors']}
O={'schema_version':P['schema_version'],'kind':'screens_part','path_id':P['path_id'],'batch_id':P['batch_id'],'tiles':[]}
for t in P['tiles']:
 tile={'tile_id':t['tile_id'],'title':' / '.join(C[c]['teaching_blocks'][0]['title'] for c in t['concept_ids']), 'summary':'Review bounded task contracts and their evidence.', 'steps':[], 'remediation_steps':[]}
 # Avoid repeated region titles while preserving source wording.
 tile['title']=' / '.join(dict.fromkeys(tile['title'].split(' / ')))
 for s in t['steps']:
  cid=s['concept_ids'][0]; c=C[cid]; k=short(cid)
  z={'step_id':s['step_id'],'type':s['type'],'concept_ids':s['concept_ids'],'eyebrow':{'explainer':'Understand','check':'Check your judgement','hands_on':'Review the evidence','video':'Optional support','recap':'Keep the essentials'}[s['type']], 'title':c['context']['concept_name'], 'lineage':step_lineage(s)}
  if s['type']=='explainer':
   z['blocks']=[]
   for qid in s['teaching_block_ids']:
    tb=next(x for x in c['teaching_blocks'] if cid+'#'+x['id']==qid)
    idx=c['teaching_blocks'].index(tb)
    z['blocks']+=prose(TEXT[k][idx],lin(cid,[tb['id']],tb['fact_ids']),tb['purpose'] if tb['purpose'] in ['intro','mechanism','misconception','example'] else 'example')
   z['title']=c['context']['concept_name'] if len(s['teaching_block_ids'])>1 else c['teaching_blocks'][idx]['title']
   if s['planned_visual_block_type']:
    L=step_lineage(s);L['anchors']=[cid+'#visual']
    z['blocks'].append(visual(cid,s['planned_visual_block_type'],L))
   # Registered trace is evidence, not typed output.
   if k=='validation_early_stopping' and any(q.endswith('#tb4') for q in s['teaching_block_ids']):z['blocks'].append(table('ds.early_stopping_trace',lin(cid,[q for q in s['teaching_block_ids']],s['fact_ids'])))
  elif s['type'] in ['check','hands_on']:
   z['title']=('Review ' if s['type']=='hands_on' else 'Judge ')+c['context']['learning_objective'] if 'learning_objective' in c['context'] else ('Review ' if s['type']=='hands_on' else 'Judge ')+k.replace('_',' ')
   z['lede']='Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.'
  elif s['type']=='video':
   z['title']='A supporting walkthrough';z['blocks']=[{'type':'media_group','segment_ids':copy.deepcopy(s['segment_ids'])}]
  else:
   z['title']='Take the contract with you';z['blocks']=[]
   for concept in t['concept_ids']:
    cc=C[concept]
    z['blocks']+=prose(TAKEAWAYS[short(concept)],lin(concept,[x['id'] for x in cc['teaching_blocks'] if set(x['fact_ids']).intersection(RECAP_FACTS[short(concept)])],RECAP_FACTS[short(concept)]),'takeaway')
   nxt=next((x for x in P['tiles'] if x['tile_id']==t['next_tile_id']),None)
   next_idea=C[nxt['concept_ids'][0]]['context']['concept_name'] if nxt else G['names']['mle.ml_training_script']
   z['blocks'].append({'type':'up_next','title':next_idea,'text':'Next: '+next_idea+'.'})
  tile['steps'].append(z)
 # One targeted remediation per distinct measured fact set in this concept.
 seen=set()
 for s in t['steps']:
  if s['type'] not in ['check','hands_on']:continue
  key=(tuple(s['concept_ids']),tuple(s['fact_ids']))
  if key in seen:continue
  seen.add(key);cid=s['concept_ids'][0];c=C[cid]
  factset=set(s['fact_ids']); blocks=[];tbids=[]
  # Teach only measured facts, preserving the source's exact conditions.
  for tb in c['teaching_blocks']:
   qfacts=[cid+'#'+f for f in tb['fact_ids']]
   if tb['purpose']=='mechanism' and factset.intersection(qfacts):
    tbids.append(cid+'#'+tb['id'])
  for f in c['coverage']['required_facts']:
   if cid+'#'+f['id'] in factset:
    related=[tb['id'] for tb in c['teaching_blocks'] if f['id'] in tb['fact_ids'] and tb['purpose']=='mechanism']
    fact_text=f['statement']
    if short(cid)=='validation_early_stopping' and f['id']=='f3':
     fact_text='Retain the checkpoint weights accepted under min_delta, rather than automatically using the last epoch’s weights.'
    blocks+=prose(fact_text,lin(cid,related,[f['id']]))
  blocks+=prose('For the same supplied task: '+CONTRAST[short(cid)],lin(cid,tbids,s['fact_ids']),'misconception')
  tile['remediation_steps'].append({'step_id':t['tile_id']+'.r'+str(len(tile['remediation_steps'])+1).zfill(2),'type':'remediation','concept_ids':[cid],'eyebrow':'Try the distinction again','title':'Separate the evidence from the assumption','blocks':blocks,'lineage':lin(cid,tbids,s['fact_ids'])})
 O['tiles'].append(tile)
(B/'screens.json').write_text(json.dumps(O,indent=2,ensure_ascii=False)+'\n')
print('Wrote',B/'screens.json')
