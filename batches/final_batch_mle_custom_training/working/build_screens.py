import json,re,copy,html
from pathlib import Path
B=Path('batches/final_batch_mle.region.custom_training')
P=json.load(open(B/'tile_plans.json')); G=json.load(open(B/'inputs/path_glossary_bundle.json')); R=json.load(open(B/'scenario_asset_registry.json'))
C={x['context']['concept_id']:x for x in G['bundles']}
# Short authored voices, keyed to the source block, not an inferred fact list.
V={
'pytorch_input_tensors':{
'tb1':'Treat features and targets as separate contracts. The numerical order arrays need aligned PyTorch representations, not one shared convenience dtype.',
'tb2':'Import torch and build each tensor with torch.from_numpy(array). Use tensor.to(dtype=declared_dtype) separately for features and targets. Inspect shape and dtype, and check observation order. Assert each declared axis length and the common batch length before returning features, targets as a tuple.',
'tb3':'Assert the accepted, boundary and failure predicates. In ordinary non-optimized execution, a false assertion raises AssertionError.',
'tb5':'Conversion is not contract verification. Use the declared target dtype; equal-looking values cannot repair different batch lengths.'},
'dataset_minibatch_loader':{
'tb1':'The dataset defines a paired item; the loader groups those items. Keep correspondence separate from the batch-size and ordering policies.',
'tb2':'A map-style Dataset supplies __len__ for sample count and __getitem__(index) for an item. With lists, retrieve features and targets at the same index and return a tuple. Build DataLoader(dataset, batch_size=declared_size, shuffle=declared_order_policy), then iterate for features, targets in loader.',
'tb3':'Batching preserves each item’s feature/target relationship. drop_last=True discards the last incomplete batch; drop_last=False, the default, keeps it smaller. Assert observed boundaries and pairings for accepted, boundary and failure fixtures. False predicates raise AssertionError in ordinary non-optimized execution.',
'tb5':'A loader cannot fill an incomplete batch. Decide whether to keep or drop it, and establish alignment in the dataset item first.'},
'neural_model_definition':{
'tb1':'Check the dimension chain, not just the layer names. Each output width must fit the next input, and the final output must match the supplied task.',
'tb2':'Import torch.nn as nn. An nn.Module subclass calls super().__init__(), registers layers as attributes and implements forward(self, x). nn.Linear(in_features, out_features) uses learned weights and bias to map each observation to out_features outputs, preserving the leading batch dimension. nn.ReLU applies max(0, x) elementwise, adding nonlinearity between linear layers.',
'tb3':'nn.Sequential runs modules in their declared order. Match adjacent widths. Choose the final width and activation from the task contract, then verify output shape on a fixture batch.',
'tb5':'Layer widths describe features and outputs per observation, not observation count. Let the supplied task determine the final width and activation.'},
'autograd_gradients':{
'tb1':'Inspect whether the scalar loss sends the intended signal to the linear parameters. A matrix-shaped chain-rule reference gives backward something concrete to agree with.',
'tb2':'Autograd records tensor operations in a computation graph and differentiates a scalar through it by the chain rule. Trainable leaf tensors need requires_grad=True. Form the loss, call loss.backward() and inspect leaf .grad values. Backward accumulates gradients: clear old values before a fresh comparison.',
'tb3':'For Z = XW + b and D = ∂L/∂Z, use X.T @ D for the weight derivative and D.sum(axis=0) for the bias derivative. D already includes loss reduction. Check gradient shapes and values with explicit relative and absolute tolerances. Assert accepted, boundary and failure predicates; false assertions raise AssertionError during ordinary non-optimized execution.',
'tb5':'Backward accumulates rather than replacing .grad. Compare with a fresh reference, and do not divide again when D already includes the loss reduction.'},
'task_loss_selection':{
'tb1':'Choose the loss contract before interpreting its scalar. Logits, probabilities, class indices and same-shaped numerical targets are not interchangeable.',
'tb2':'A loss compares outputs with the corresponding target representation. CrossEntropyLoss takes unnormalized logits. For class-index targets, require logits (N, C), long targets (N,) and indices in [0, C). MSELoss requires input and target tensors of the same shape; mean reduction averages squared elementwise differences.',
'tb3':'BCEWithLogitsLoss combines sigmoid with binary cross-entropy: supply raw logits and same-shaped targets in [0, 1], not already-sigmoid inputs. For mean MSE over M elements, the output derivative is 2 × (output−target)/M; its sign follows increasing loss away from the target. For unweighted mean binary-logit loss, use (sigmoid(logit)−target)/M. Raw logit and probability play different roles.',
'tb4':'For unweighted mean class-index cross-entropy, each sample-logit derivative is (softmax probability−one-hot target)/N. Check width, class identity and reduction when building the reference.',
'tb6':'Both class-index CrossEntropyLoss and BCEWithLogitsLoss take logits. For MSE, assert matching shapes rather than depending on accidental broadcasting.'},
'optimizer_configuration':{
'tb1':'A deterministic step exposes whether the optimizer receives the intended trainable parameters and current gradient. A learning-rate setting alone is not an update.',
'tb2':'Construct torch.optim.SGD(model.parameters(), lr=declared_learning_rate). For plain SGD without momentum, weight decay or other modifications, parameter_new = parameter_old − learning_rate × gradient. Clear old gradients with optimizer.zero_grad(), backpropagate the loss, then call optimizer.step().',
'tb3':'Check the deterministic update against that conditional SGD rule, not a rule for every optimizer. Assert accepted, boundary and failure cases; false predicates raise AssertionError in ordinary non-optimized execution.',
'tb5':'The current backward result must reach step. The plain-SGD equation applies only without momentum, weight decay or other modifications.'},
'minibatch_training_loop':{
'tb1':'Repeat the intended update for each minibatch in each declared epoch. Keep batch counts beside loss evidence so a partial final batch stays visible.',
'tb2':'Within each epoch, iterate for features, targets in loader. Compute model(features), then loss_fn(predictions, targets). Each minibatch needs optimizer.zero_grad(), loss.backward() and optimizer.step() for its current gradient. Collect scalar loss.item() values and batch counts when summarizing an epoch.',
'tb3':'Assert accepted, boundary and failure predicates; false assertions raise AssertionError in ordinary non-optimized execution. For plain SGD, retain pre-step values and check parameter_after − parameter_before against −learning_rate × current_gradient under tolerance.',
'tb5':'Step counts alone do not describe an epoch. Interpret loss with batch sizes, and do not mix leftover gradients into the next intended minibatch update.'},
 'training_evaluation_modes':{
'tb1':'Validation needs evaluation layer behavior and no parameter updates. Layer mode and graph recording are independent controls.',
'tb2':'Use model.train() for training and model.eval() for validation. Mode changes relevant layers, including dropout and batch normalization. Put validation prediction inside with torch.no_grad(): to disable graph recording. eval changes layer behavior; no_grad controls whether a gradient graph is recorded.',
'tb3':'Keep validation forward-only, with no optimizer.step(), and restore model.train() afterward. Import torch and nn from torch for the supplied dropout fixture. Training randomly zeroes elements with probability p and scales retained values by 1/(1-p); evaluation returns x unchanged. Assert evaluation identity and permitted masking/scaling, not a particular random mask. no_grad alone leaves dropout mode unchanged. Test accepted, boundary and failure predicates; false assertions raise AssertionError in ordinary non-optimized execution.',
'tb5':'eval does not turn graph recording off. no_grad does not set dropout to evaluation mode. Neither makes a validation parameter update acceptable.'},
'weight_persistence':{
'tb1':'Restore learned state into a compatible architecture and check bounded predictions. A saved mapping does not select an arbitrary new architecture.',
'tb2':'Save model.state_dict() with torch.save. Construct the same compatible architecture, load the mapping with torch.load(..., weights_only=True), and apply model.load_state_dict(mapping). Set the restored model to eval before prediction.',
'tb3':'Use binary handles: open(path, "wb") for torch.save and open(path, "rb") for torch.load. Compare restored and original evaluation predictions on the same fixture with explicit numerical tolerances. Assert accepted, boundary and failure predicates; false assertions raise AssertionError in ordinary non-optimized execution.',
'tb4':'Also compare corresponding original and restored state_dict entries. Prediction agreement alone is not the full parameter-state check.',
'tb6':'Reloading does not choose an architecture. Verify saved entries as well as predictions on the same evaluation-mode fixture.'},
'validation_early_stopping':{
'tb1':'Early stopping follows a declared controller, not the last epoch that ran. Retain weights from the checkpoint accepted by the minimum-improvement rule.',
'tb2':'Declare the validation quantity, direction, min_delta and patience first. For minimization, accept only current < best − min_delta and reset the counter; otherwise increment it and stop at exhausted patience. Patience counts consecutive insufficient improvements. best means the last accepted checkpoint value, not necessarily the lowest observation. Retain those accepted weights instead of the final epoch’s.',
'tb3':'A state_dict refers to live parameter values. Deep-copy or save the accepted state before further updates. Bound a while loop by maximum epochs and the non-improvement rule; update best and checkpoint in the improvement branch and break at exhausted patience. Keep protected test observations out of preprocessing fitting, model choice and tuning: those uses leak information.',
'tb5':'A state_dict reference need not be a frozen snapshot. Later updates can alter it, and a small decrease is insufficient if it fails min_delta.'},
 'training_failure_diagnosis':{
'tb1':'Reproduce the bounded failure, then inspect losses, the output/target contract and gradients. Test one evidence-supported correction on that same fixture.',
'tb2':'Read trainable parameter .grad after backward and before clearing it. Check loss evidence, output/target compatibility and learning rate against the declared computation. Choose one supported correction, rerun the same bounded fixture and compare its loss/gradient record with the failing reference.',
'tb3':'Follow loss → outputs → parameters. Compare derivative signs and measured gradient magnitudes, then test a single root-cause hypothesis on the reproduced failure. Assert accepted, boundary and failure cases; false predicates raise AssertionError in ordinary non-optimized execution.',
'tb5':'A stalled loss is not permission for arbitrary changes. Read gradients before zeroing; otherwise the record can hide the learning signal.'},
'device_placement':{
'tb1':'An available accelerator is not proof of placement. Verify that the model, features and targets actually use compatible devices.',
'tb2':'Check torch.cuda.is_available() before selecting torch.device("cuda"); otherwise use the supported CPU path. Move the model with model.to(device) and both inputs and targets with tensor.to(device). Inspect parameter and minibatch devices, then test placement with a bounded forward/backward fixture.',
'tb3':'Assert accepted, boundary and failure predicates; false assertions raise AssertionError in ordinary non-optimized execution. For the authorized supplied VM, gcloud compute instances start INSTANCE --zone=ZONE and stop INSTANCE --zone=ZONE change lifecycle state. Wait and inspect the result. Connect to the running authorized VM with gcloud compute ssh INSTANCE --zone=ZONE for the workload.',
'tb4':'Inspect identity and status before and after the authorized action with gcloud compute instances describe INSTANCE --zone=ZONE. Stop the supplied instance after the bounded workload, wait for completion and verify it is stopped.',
'tb6':'A running accelerator VM proves neither availability nor compatible tensor placement. Verify the bounded fixture and stop the authorized VM afterward.'},
 'training_batch_sizing':{
'tb1':'Throughput matters only within the declared memory budget. Input bytes estimate one allocation, not the whole live training peak.',
'tb2':'Training memory includes live tensors and other allocations. Larger batches ordinarily need more activation storage. Change only DataLoader batch_size, preserving alignment and task. For CUDA, reset_peak_memory_stats() before the workload and read torch.cuda.max_memory_allocated() afterward for peak allocated tensor bytes.',
'tb3':'That allocated-tensor peak does not cover all GPU usage. Match the budget to the quantity it governs, then compare completed work per elapsed time among eligible sizes. Estimate feature bytes as batch_rows × feature_columns × bytes_per_feature_element, add target bytes using their dtype, and compare with the observed peak.',
'tb5':'Allocated-tensor peak is not all GPU usage. Input-matrix estimates omit other live allocations; use the declared measured-memory quantity for eligibility.'},
 'training_memory_diagnosis':{
'tb1':'Locate exhaustion before blaming the input batch. Tensor-occupied storage, allocator reservations and retained graphs are different evidence.',
'tb2':'memory_allocated reports tensor-occupied CUDA memory; memory_reserved includes caching-allocator storage. Inspect both peaks and the failure point. Saved graph-connected tensors can keep graph memory live; use detached or scalar diagnostics when gradients through saved values are unnecessary.',
'tb3':'empty_cache releases unused cached storage, not storage held by live tensors. Change one supported factor—such as batch size or an unnecessary retained graph reference—and verify completion and peak on the same bounded task. Count each parameter, gradient, activation and batch matrix as element_count × element_width, summing simultaneously live allocations.',
'tb4':'For input width F and output width H, a linear layer has F × H weight elements and H bias elements. Use those counts in the parameter-allocation reference.',
'tb6':'empty_cache cannot free live tensor storage. Keep reserved and allocated memory distinct, and count more than the input matrix.'},
 'training_bottleneck_profiling':{
'tb1':'Duration alone does not locate a bottleneck. Label loading and computation regions and inspect profiler evidence before selecting one change.',
'tb2':'Wrap computation in the PyTorch profiler and mark loading and model regions with record_function. Use key_averages().table(...) or the trace to attribute operator and labeled-region work. Warm up before comparing steady-state execution, and make the final timing comparison without profiler overhead.',
'tb3':'CUDA work is asynchronous: synchronize CPU-clock measurement boundaries to include completed accelerator work. Change one supported factor and compare the same bounded workload. Inspect CPU, memory and running processes during the interval; docker stats and docker top support a containerized run. Separate resource limits from stage timing evidence.',
'tb5':'Changed code is not measured improvement. Control asynchronous timing boundaries and exclude profiler overhead from the final comparison.'},
 'training_hardware_selection':{
'tb1':'Compare completed work, quality, memory and billing scope. Accelerator utilization alone is neither a cost result nor proof of eligibility.',
'tb2':'Check accelerator availability, then place model and minibatches on the chosen device. Compare the same bounded workload and quality requirements, interpreting relevant data movement and warm-up as declared. Running VM compute is billed; stopping ends compute billing but may leave disk and other charges.',
'tb3':'Estimate compute execution cost from measured runtime and the supplied rate, keeping billing scope explicit. On the authorized supplied VM, gcloud compute instances start INSTANCE --zone=ZONE and stop INSTANCE --zone=ZONE change lifecycle state; wait and inspect. Use gcloud compute ssh INSTANCE --zone=ZONE to execute the workload on the running VM.',
'tb4':'After the bounded measurement, stop the authorized VM and verify its state. Use gcloud compute instances describe INSTANCE --zone=ZONE to inspect identity and status before and after lifecycle actions. Retain runtime/cost evidence, observed memory and whether each CPU/GPU option completes the same matrix workload within fixed limits.',
'tb5':'After both authorized benchmarks, stop both options and verify their states. Base billing calculations on measured lifecycle durations.',
'tb7':'Faster need not mean cheaper or eligible. Stopped compute does not establish that every resource charge ended.'},
 'task_specific_pretrained_weight_fine_tuning':{
'tb1':'Adapt the compatible pretrained ViT within the supplied supervised scope. Keep the pretrained label mapping distinct from the task-head mapping.',
'tb2':'Import torch, nn from torch, and AutoImageProcessor, ViTForImageClassification, TrainingArguments and Trainer from transformers. Load model and matching processor with from_pretrained(checkpoint); retain the original label map first. The processor’s return_tensors="pt" yields pixel_values; model(**inputs).logits gives logits. Use that processor for training and validation. Set declared output_dir, num_train_epochs, per_device_train_batch_size and learning_rate in TrainingArguments, plus eval_strategy="epoch" and remove_unused_columns=False. Build Trainer with model, args, train_dataset, eval_dataset=validation_dataset, data_collator and processing_class=processor. trainer.train() runs the bounded adaptation.',
'tb3':'Freeze existing parameters with requires_grad=False, then replace model.classifier with nn.Linear(model.config.hidden_size, num_labels). Update model.num_labels, model.config.num_labels, id2label and label2id. The new head is trainable by default: verify changed head weights and unchanged backbone. Compare adapted predictions with the frozen reference on the same validation cohort, without an application or protected test data. FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) on actual positives. Empty conditioning groups have undefined rates.',
'tb4':'With zero cost for correct predictions, use supplied deployment probabilities: expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected test observations must not fit preprocessing, select models or tune settings; that leaks information. For the class-index head, require logits (N, C), long targets (N,) in [0, C), and C matching the task map.',
'tb5':'Compute and backpropagate task loss within adaptation. Compare a selected head gradient with its chain-rule reference before claiming the intended supervised update reached the head.',
'tb7':'Freezing existing parameters does not freeze a new head by default. Changed head weights still need a verified target mapping and matched validation comparison.'}
}
# Examples remain grounded in source fixture values; no value or output is retyped.
def example(tb):
 text=tb['content'].split('\n\n')[0]
 text=re.sub(r'^(Suppose|Imagine|Take|For) ',lambda m:{'Suppose':'In this review,','Imagine':'Review','Take':'Inspect','For':'In'}[m[1]]+' ',text)
 text=text.replace('The expected output shape is','The task requires output shape').replace('Keep these','Separate these').replace('This makes it clear','This separates')
 return text

def lineage(cids,tbs,facts,anchors=None):
 d={'concept_ids':cids,'teaching_block_ids':tbs,'fact_ids':facts}
 if anchors:d['anchors']=anchors
 return d

def prose(text,lin):return {'type':'prose','text':text,'lineage':copy.deepcopy(lin)}
def split_prose(text,lin,maxwords=85):
 sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z])',text); parts=[]; cur=''
 for sent in sentences:
  if cur and len((cur+' '+sent).split())>maxwords:parts.append(prose(cur,lin));cur=''
  cur=(cur+' '+sent).strip()
 if cur:parts.append(prose(cur,lin))
 return parts

def code(txt,lin):return {'type':'code_walkthrough','language':'python','code':txt,'lineage':copy.deepcopy(lin)}
def diagram(labels,lin,title='Evidence to inspect'):
 nodes=[{'id':f'n{i}','label':s} for i,s in enumerate(labels)]
 # A labelled SVG makes this a concrete rendered schematic as well as a graph.
 svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 %d">'% (len(labels)*65+35)
 for i,s in enumerate(labels):svg+=f'<rect x="10" y="{i*65+10}" width="740" height="55" rx="8" fill="#eef2ff" stroke="#444"/><text x="25" y="{i*65+42}" font-size="13">{html.escape(s)}</text>'
 svg+='</svg>'
 return {'type':'diagram','diagram_kind':'mapping','title':title,'nodes':nodes,'edges':[],'alt_text':'; '.join(labels),'lineage':copy.deepcopy(lin)}
