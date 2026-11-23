# EVALUATOR PACKET — Tensors, Minibatches and Model Outputs (mle.tile.035_037)
Tile summary: Review separate tensor contracts, same-index minibatches and task-compatible layer dimensions.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.pytorch_input_tensors — Construct PyTorch input tensors with compatible shapes and dtypes
B = mle.dataset_minibatch_loader — Build a dataset and minibatch loader
C = mle.neural_model_definition — Define a neural network with task-compatible layers and activations

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (mle.pytorch_input_tensors)   objective: Convert aligned feature/target arrays into tensors with explicitly checked shape and dtype.
A.f1: Use import torch and torch.from_numpy(array) to construct tensors from the supplied NumPy feature and target arrays.   [sources: pytorch_learn_basics#tensorqs_tutorial.html — Initializing a Tensor; Attributes of a Tensor; Operations on Tensors]
A.f2: Convert the feature and target tensors explicitly with tensor.to(dtype=declared_dtype), inspect tensor.shape and tensor.dtype, and verify row correspondence rather than relying on inferred types or deriving target representation from feature dtype.   [sources: pytorch_learn_basics#tensorqs_tutorial.html — Initializing a Tensor; Attributes of a Tensor; Operations on Tensors]
A.f4: Assert the declared feature and target axis lengths and their common batch length, and return the aligned tensors as a tuple.   [sources: pytorch_learn_basics#tensorqs_tutorial.html — Initializing a Tensor; Attributes of a Tensor; Operations on Tensors]
A.f5: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Tensors, Minibatches and Model Outputs.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.numpy_shape_dtype, mle.numpy_dtype_selection, mle.label_integrity. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write the required imports and a Python function that converts supplied NumPy features and targets into PyTorch tensors, explicitly applies their separately declared dtypes, asserts the declared shapes, common batch length and row correspondence, and returns the pair as a tuple. Verify the function using supplied valid, boundary and failure fixtures.  SUCCESS: The valid (4, 2) feature and (4,) target fixture and supplied boundary fixture produce aligned tensor tuples with the declared shapes and separate dtypes. Learner-authored assertions verify each accepted result. The three-target fixture and supplied incompatible-contract fixtures are rejected by assertions during ordinary non-optimized execution.
ASSESSMENT ANCHOR: construct_tensors_with_declared_dtypes facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_tensor_shapes_and_row_alignment facts=['f2', 'f4']
ASSESSMENT ANCHOR: assert_input_contract_and_return_aligned_tuple facts=['f4', 'f5']

## SOURCE FACTS — B (mle.dataset_minibatch_loader)   objective: Implement a dataset/loader that preserves sample identity and minibatch alignment.
B.f1: A map-style Dataset implements __len__ for sample count and __getitem__(index) for the corresponding feature/target item.   [sources: pytorch_learn_basics#data_tutorial.html — Creating a Custom Dataset for your files; Preparing your data for training with DataLoaders]
B.f2: For list-based observations, retrieve the feature and target from the same observation index and return them as a tuple.   [sources: pytorch_learn_basics#data_tutorial.html — Creating a Custom Dataset for your files; Preparing your data for training with DataLoaders]
B.f3: Construct DataLoader(dataset, batch_size=declared_size, shuffle=declared_order_policy) and iterate for features, targets in loader.   [sources: pytorch_learn_basics#data_tutorial.html — Creating a Custom Dataset for your files; Preparing your data for training with DataLoaders]
B.f4: The loader groups observation items into minibatches while preserving the feature/target relationship within each item.   [sources: pytorch_learn_basics#data_tutorial.html — Creating a Custom Dataset for your files; Preparing your data for training with DataLoaders]
B.f5: Set DataLoader(..., drop_last=True) to discard the last incomplete batch, or drop_last=False (the default) to retain it with fewer samples than batch_size; test the observed batch boundaries against that explicit choice.   [sources: pytorch_learn_basics#https://docs.pytorch.org/docs/2.9/data.html — torch.utils.data.DataLoader — drop_last]
B.f6: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Tensors, Minibatches and Model Outputs.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.pytorch_input_tensors, mle.label_integrity. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write the required imports and a learner-defined Python function that builds a map-style Dataset and DataLoader from five list-based feature/target observations within supplied infrastructure scaffolding. Implement indexed feature/target tuple retrieval, iterate the loader, and write shape, row-alignment and batch-boundary assertions for batch_size=2 under explicit shuffle and drop_last policies.  SUCCESS: The dataset reports five items and returns each feature with its corresponding target. With shuffle=False, assertions verify source-order pairings and batch sizes [2, 2, 1] for drop_last=False and [2, 2] for drop_last=True. With shuffle=True, checks verify pairings without assuming source order. A deliberately mismatched feature/target pair fails an alignment assertion with AssertionError during ordinary non-optimized execution.
ASSESSMENT ANCHOR: implement_index_aligned_dataset_items facts=['f1', 'f2']
ASSESSMENT ANCHOR: yield_aligned_minibatches_under_declared_order_policy facts=['f3', 'f4']
ASSESSMENT ANCHOR: assert_expected_batch_boundaries_and_alignment facts=['f5', 'f6']

## SOURCE FACTS — C (mle.neural_model_definition)   objective: Build a minimal module whose layer widths, nonlinearity and output shape satisfy the task.
C.f1: Import torch.nn as nn and define an nn.Module subclass with super().__init__(), registered layer attributes and a forward(self, x) method.   [sources: pytorch_learn_basics#buildmodel_tutorial.html — Define the Class; Model Layers]
C.f2: nn.Linear(in_features, out_features) maps each input feature vector to out_features outputs using learned weights and bias, preserving the leading minibatch dimension.   [sources: pytorch_learn_basics#buildmodel_tutorial.html — Define the Class; Model Layers]
C.f3: nn.ReLU applies max(0, x) elementwise and introduces a nonlinearity between linear layers.   [sources: pytorch_learn_basics#buildmodel_tutorial.html — Define the Class; Model Layers]
C.f4: nn.Sequential composes its modules in declared order; match each layer’s output width to the next layer’s input width.   [sources: pytorch_learn_basics#buildmodel_tutorial.html — Define the Class; Model Layers]
C.f5: Set the final layer width and activation to the supplied output task contract and verify the resulting output shape with a fixture batch.   [sources: pytorch_learn_basics#buildmodel_tutorial.html — Define the Class; Model Layers]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Tensors, Minibatches and Model Outputs.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.pytorch_input_tensors, mle.prediction_task_definition. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a Python function that imports torch.nn as nn, defines and returns a small nn.Module subclass for the supplied two-feature input and single unconstrained numerical output contract. Register a 2 → 3 → 1 layer sequence with ReLU between the linear layers, implement forward(self, x), and check the returned model's output shape using the supplied four-observation fixture.  SUCCESS: The learner-defined function returns an nn.Module with correctly registered layers and an implemented forward method. Its intermediate widths match, ReLU appears between the linear layers, the final linear output remains unconstrained, and the fixture produces shape (4, 1).
ASSESSMENT ANCHOR: verify_module_definition_and_layer_registration facts=['f1']
ASSESSMENT ANCHOR: verify_layer_widths_and_intermediate_activation facts=['f2', 'f3', 'f4']
ASSESSMENT ANCHOR: verify_task_compatible_output_width_activation_and_shape facts=['f5']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjust training batch size to fit available memory; Apply correct neural-network training and evaluation modes; Build a dataset and minibatch loader; Choose CPU or GPU capacity for a bounded training workload; Choose a task-compatible training loss; Compute neural-network gradients with automatic differentiation; Configure a baseline optimizer and learning rate; Convert an ML notebook prototype into a repeatable executable training script with an explicit entry point; Define a neural network with task-compatible layers and activations; Diagnose training failures from loss and gradient behavior; Diagnose training memory exhaustion; Evaluate the frozen selected model and threshold against the baseline on the protected test set; Execute a bounded managed custom-model training job on an existing platform; Freeze and identify a traceable dataset snapshot for reproducible training; Implement batch inference over a bounded dataset; Implement online prediction using the fitted preprocessing and model; Implement the minibatch forward, backward and optimizer-step loop; Package a versioned model with fitted preprocessing and inference dependencies; Place models and tensors on the correct comp

## LESSON, in learner order

### s01 · explainer · Construct PyTorch input tensors with compatible shapes and dtypes
Understand — 
(intro) For the numerical order arrays, feature and target representations have separate contracts. A shared feature dtype is not enough. ⟦A:tb1⟧
(mechanism) Import torch and construct each tensor with torch.from_numpy(array). Apply tensor.to(dtype=declared_dtype) separately to features and targets. Inspect shape and dtype, and verify corresponding observation order. Assert the declared axes and common batch length before returning the aligned tensors as a tuple. ⟦A.f1 A.f2 A.f4 A:tb2⟧
(mechanism) Check the valid, boundary and failure fixtures with assert predicates. A false predicate raises AssertionError in ordinary, non-optimized execution. ⟦A.f5 A:tb3⟧
[CODE python]
import torch

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

import numpy as np
feature_dtype = torch.float32
target_dtype = torch.long

def inspect_pair(pair, feature_shape, target_shape):
    features, targets = pair
    inspected = (features.shape, features.dtype, targets.shape, targets.dtype)
    shape_ok = features.shape == feature_shape and targets.shape == target_shape
    dtype_ok = features.dtype == feature_dtype and targets.dtype == target_dtype
    alignment_ok = features.shape[0] == targets.shape[0]
    return inspected, shape_ok, dtype_ok, alignment_ok

# Accepted fixture: four same-index observations.
features_array = np.arange(8).reshape(4, 2)
targets_array = np.arange(4)
accepted = aligned_pair(features_array, targets_array, feature_dtype,
                        target_dtype, (4, 2), (4,))
accepted_inspection, shape_ok, dtype_ok, alignment_ok = inspect_pair(
    accepted, (4, 2), (4,))
assert shape_ok and dtype_ok and alignment_ok

# Declared illustrative boundary: one observation, two feature columns.
boundary_shapes = ((1, 2), (1,))
boundary = aligned_pair(features_array[:1], targets_array[:1], feature_dtype,
                        target_dtype, *boundary_shapes)
boundary_inspection, shape_ok, dtype_ok, alignment_ok = inspect_pair(
    boundary, *boundary_shapes)
assert shape_ok and dtype_ok and alignment_ok

# Three-target failure: conversion succeeds; contract predicates fail.
short_targets_array = targets_array[:3]
converted_short = (torch.from_numpy(features_array).to(dtype=feature_dtype),
                   torch.from_numpy(short_targets_array).to(dtype=target_dtype))
short_inspection, shape_ok, dtype_ok, alignment_ok = inspect_pair(
    converted_short, (4, 2), (4,))
assert dtype_ok and not shape_ok and not alignment_ok
try:
    aligned_pair(features_array, short_targets_array, feature_dtype,
                 target_dtype, (4, 2), (4,))
except AssertionError:
    rejected = True
else:
    rejected = False
assert rejected
  annotations: ['Inspect these fixture checks: conversion can succeed while the declared shape or alignment predicate fails.']

### s02 · explainer · Separate casts: accepted and shorter-target pairs
Understand — 
(example) In the supplied order-array pair, inspect feature and target axes separately. A target array with too few rows may convert successfully but still fail alignment. A wrong target representation is a separate defect: do not derive its dtype from the features. Return the tuple only after both contracts and row correspondence pass. Check the accepted pair, supplied boundary and incompatible fixtures, rather than treating conversion success as acceptance. ⟦A.f1 A.f2 A.f4 A.f5 A:tb4⟧

### s03 · explainer · A distinction to keep
Understand — 
(misconception) Conversion alone is not acceptance. Use the declared target dtype, and check batch correspondence even when individual values look valid. ⟦A.f2 A.f4 A:tb5⟧

### s04 · check · Judge pytorch input tensors
Check your judgement — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s05 · hands_on · Review pytorch input tensors
Review the evidence — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s06 · explainer · Build a dataset and minibatch loader
Understand — 
(intro) The dataset defines a paired observation; the loader groups observations using a declared size and ordering policy. ⟦B:tb1⟧
(mechanism) In a map-style Dataset, __len__ supplies the sample count and __getitem__(index) supplies an item. For list observations, fetch features and targets at the same index and return a tuple. Configure DataLoader(dataset, batch_size=declared_size, shuffle=declared_order_policy), then iterate for features, targets in loader. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Batching preserves each item’s feature/target relationship. drop_last=True discards an incomplete final batch; drop_last=False, the default, retains it with fewer samples. Test boundaries against that policy. Use assert for valid, boundary and failure fixtures; false predicates raise AssertionError during ordinary non-optimized execution. ⟦B.f4 B.f5 B.f6 B:tb3⟧
[CODE python]
from torch.utils.data import Dataset, DataLoader

class PairedItems(Dataset):
    def __init__(self, features, targets):
        self.features, self.targets = features, targets
        assert len(features) == len(targets)
    def __len__(self):
        return len(self.features)
    def __getitem__(self, index):
        return self.features[index], self.targets[index]

features = list(range(5))
targets = list(range(5))
dataset = PairedItems(features, targets)
assert len(dataset) == 5
for index in range(5):
    assert dataset[index] == (features[index], targets[index])

# Retain the incomplete batch
retained_loader = DataLoader(dataset, batch_size=2, shuffle=False, drop_last=False)
retained = list(retained_loader)
assert [len(x) for x, y in retained] == [2, 2, 1]
for x, y in retained:
    assert x.tolist() == y.tolist()
assert [i for x, y in retained for i in x.tolist()] == features

# Discard the incomplete batch
dropped_loader = DataLoader(dataset, batch_size=2, shuffle=False, drop_last=True)
dropped = list(dropped_loader)
assert [len(x) for x, y in dropped] == [2, 2]
for x, y in dropped:
    assert x.tolist() == y.tolist()
assert [i for x, y in dropped for i in x.tolist()] == features[:4]
  annotations: ['Retain the incomplete batch', 'Discard the incomplete batch']

### s07 · explainer · Five observations: retain or drop the last batch
Understand — 
(example) In the supplied indexed-observation fixture, retaining the incomplete batch produces a smaller final batch; dropping it removes that batch. Neither policy creates observations. Verify __len__, item identities and batch boundaries. Same-index retrieval establishes pairing before collation: well-shaped batches can still contain mismatched items. Shuffle changes ordering, not the feature/target relationship, so do not assume the first loader item is the first source row. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B:tb4⟧

### s08 · explainer · A distinction to keep
Understand — 
(misconception) A loader cannot fill a partial batch by assumption. Declare drop_last explicitly; establish alignment in each dataset item. ⟦B.f2 B.f4 B.f5 B:tb5⟧

### s09 · check · Judge dataset minibatch loader
Check your judgement — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s10 · hands_on · Review dataset minibatch loader
Review the evidence — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s11 · explainer · Define a neural network with task-compatible layers and activations
Understand — 
(intro) Match layer widths and final outputs to the supplied task contract. ⟦C:tb1⟧
(mechanism) Import torch.nn as nn. An nn.Module subclass calls super().__init__(), registers layers as attributes and defines forward(self, x). nn.Linear(in_features, out_features) uses learned weights and bias to map feature vectors to outputs while preserving the leading minibatch dimension. nn.ReLU applies max(0, x) elementwise, introducing nonlinearity between linear layers. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) nn.Sequential applies modules in declared order. Match each output width to the following input width. Choose final width and activation from the task contract, then verify output shape with a fixture batch. ⟦C.f4 C.f5 C:tb3⟧
[DIAGRAM: Task-bounded layer chain] nodes=['Input (4, 2)', 'Linear(2, 3): output (4, 3)', 'ReLU: output (4, 3)', 'Linear(3, 1): output (4, 1)', 'Task output: unconstrained; batch length 4 preserved'] edges=[('node0', 'node1', None), ('node1', 'node2', None), ('node2', 'node3', None), ('node3', 'node4', None)] alt: Four observations pass through widths 2 → 3 → 1; ReLU preserves shape, and the task’s final output is unconstrained.

### s12 · explainer · Four observations through widths 2 → 3 → 1
Understand — 
(example) Follow the supplied dimension chain for one observation, then restore the leading batch axis. Linear layers change per-observation width; ReLU changes values elementwise without changing that width. Register layer attributes and define forward, or inspect the declared Sequential composition. Check the final activation against the task. A mismatched intermediate width is not repaired by changing batch size. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C:tb4⟧

### s13 · explainer · A distinction to keep
Understand — 
(misconception) Layer widths are per-observation dimensions, not sample counts. Let the supplied task determine final width and activation. ⟦C.f2 C.f4 C.f5 C:tb5⟧

### s14 · check · Judge neural model definition
Check your judgement — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s15 · hands_on · Review neural model definition
Review the evidence — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s16 · recap · Take the contract with you
Keep the essentials — 
(takeaway) Check separate dtypes, axes and aligned rows before returning tensors. ⟦A.f2 A.f4 A:tb2 A:tb4 A:tb5⟧
(takeaway) Pair items by index and declare incomplete-batch policy. ⟦B.f2 B.f5 B:tb2 B:tb3 B:tb4 B:tb5⟧
(takeaway) Match layer widths and final task output. ⟦C.f4 C.f5 C:tb3 C:tb4 C:tb5⟧
[UP NEXT] Compute neural-network gradients with automatic differentiation: Next: Compute neural-network gradients with automatic differentiation.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the evidence from the assumption
(mechanism) Assert the declared feature and target axis lengths and their common batch length, and return the aligned tensors as a tuple. ⟦A.f4 A:tb2⟧
(mechanism) Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution. ⟦A.f5 A:tb3⟧
(misconception) For the same supplied task: A converted target can still be misaligned; conversion is not acceptance. ⟦A.f4 A.f5 A:tb2 A:tb3⟧
### r02 · Separate the evidence from the assumption
(mechanism) Use import torch and torch.from_numpy(array) to construct tensors from the supplied NumPy feature and target arrays. ⟦A.f1 A:tb2⟧
(mechanism) Convert the feature and target tensors explicitly with tensor.to(dtype=declared_dtype), inspect tensor.shape and tensor.dtype, and verify row correspondence rather than relying on inferred types or deriving target representation from feature dtype. ⟦A.f2 A:tb2⟧
(mechanism) Assert the declared feature and target axis lengths and their common batch length, and return the aligned tensors as a tuple. ⟦A.f4 A:tb2⟧
(mechanism) Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution. ⟦A.f5 A:tb3⟧
(misconception) For the same supplied task: A converted target can still be misaligned; conversion is not acceptance. ⟦A.f1 A.f2 A.f4 A.f5 A:tb2 A:tb3⟧
### r03 · Separate the evidence from the assumption
(mechanism) Construct DataLoader(dataset, batch_size=declared_size, shuffle=declared_order_policy) and iterate for features, targets in loader. ⟦B.f3 B:tb2⟧
(mechanism) The loader groups observation items into minibatches while preserving the feature/target relationship within each item. ⟦B.f4 B:tb3⟧
(misconception) For the same supplied task: Well-shaped batches can contain mismatched items; pairing begins at the same index. ⟦B.f3 B.f4 B:tb2 B:tb3⟧
### r04 · Separate the evidence from the assumption
(mechanism) A map-style Dataset implements __len__ for sample count and __getitem__(index) for the corresponding feature/target item. ⟦B.f1 B:tb2⟧
(mechanism) For list-based observations, retrieve the feature and target from the same observation index and return them as a tuple. ⟦B.f2 B:tb2⟧
(mechanism) Set DataLoader(..., drop_last=True) to discard the last incomplete batch, or drop_last=False (the default) to retain it with fewer samples than batch_size; test the observed batch boundaries against that explicit choice. ⟦B.f5 B:tb3⟧
(mechanism) Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution. ⟦B.f6 B:tb3⟧
(misconception) For the same supplied task: Well-shaped batches can contain mismatched items; pairing begins at the same index. ⟦B.f1 B.f2 B.f5 B.f6 B:tb2 B:tb3⟧
### r05 · Separate the evidence from the assumption
(mechanism) Set the final layer width and activation to the supplied output task contract and verify the resulting output shape with a fixture batch. ⟦C.f5 C:tb3⟧
(misconception) For the same supplied task: Changing sample count cannot fix incompatible per-observation widths. ⟦C.f5 C:tb3⟧
### r06 · Separate the evidence from the assumption
(mechanism) Import torch.nn as nn and define an nn.Module subclass with super().__init__(), registered layer attributes and a forward(self, x) method. ⟦C.f1 C:tb2⟧
(mechanism) nn.Linear(in_features, out_features) maps each input feature vector to out_features outputs using learned weights and bias, preserving the leading minibatch dimension. ⟦C.f2 C:tb2⟧
(mechanism) nn.ReLU applies max(0, x) elementwise and introduces a nonlinearity between linear layers. ⟦C.f3 C:tb2⟧
(mechanism) nn.Sequential composes its modules in declared order; match each layer’s output width to the next layer’s input width. ⟦C.f4 C:tb3⟧
(mechanism) Set the final layer width and activation to the supplied output task contract and verify the resulting output shape with a fixture batch. ⟦C.f5 C:tb3⟧
(misconception) For the same supplied task: Changing sample count cannot fix incompatible per-observation widths. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C:tb2 C:tb3⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again

=========

# EVALUATOR PACKET — Gradients, Loss and Optimizer (mle.tile.038_040)
Tile summary: Review fresh leaf gradients, task-loss references and plain-SGD parameter changes.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.autograd_gradients — Compute neural-network gradients with automatic differentiation
B = mle.task_loss_selection — Choose a task-compatible training loss
C = mle.optimizer_configuration — Configure a baseline optimizer and learning rate

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (mle.autograd_gradients)   objective: Verify parameter gradients against the corresponding matrix-shaped derivative reference.
A.f1: Autograd records tensor operations as a computation graph and differentiates the scalar output through that graph using the chain rule.   [sources: pytorch_learn_basics#autogradqs_tutorial.html — Tensors, Functions and Computational graph; Computing Gradients]
A.f2: Set requires_grad=True on trainable leaf tensors, form the supplied scalar loss, call loss.backward(), and inspect each leaf parameter’s .grad.   [sources: pytorch_learn_basics#autogradqs_tutorial.html — Tensors, Functions and Computational graph; Computing Gradients]
A.f3: Backward accumulates into .grad, so clear old gradients before comparing a fresh computation with the reference.   [sources: pytorch_learn_basics#autogradqs_tutorial.html — Tensors, Functions and Computational graph; Computing Gradients]
A.f4: For a linear batch Z = XW + b with scalar-loss derivative D = ∂L/∂Z, the chain rule yields ∂L/∂W = X.T @ D and ∂L/∂b = D.sum(axis=0), with any loss reduction already included in D.   [sources: pytorch_learn_basics#autogradqs_tutorial.html — Tensors, Functions and Computational graph; Computing Gradients]
A.f5: Compare the computed gradients to the matrix-shaped chain-rule reference with explicit relative and absolute tolerances.   [sources: numpy_user_guide#reference/generated/numpy.testing.assert_allclose.html]
A.f6: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Gradients, Loss and Optimizer.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.pytorch_input_tensors. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write the required PyTorch import and a learner-defined Python function within supplied scaffolding. For the linear computation Z = X @ W + b, enable gradient tracking on leaf parameters W and b, clear any existing gradients, form the supplied scalar loss, and compute its gradients. Author assertions comparing gradient shapes and values with X.T @ D and D.sum(dim=0), using explicit relative and absolute tolerances. Cover the declared valid matrix fixture, a supplied single-row boundary fixture, and a deliberately mismatched reference.  SUCCESS: The function computes fresh W.grad and b.grad, matches both matrix-shaped chain-rule references within declared tolerances, preserves the supplied reduction convention in D, and uses assertions to accept valid and boundary cases and reject a deliberately mismatched reference.
ASSESSMENT ANCHOR: verify_scalar_loss_gradient_tracking facts=['f1', 'f2']
ASSESSMENT ANCHOR: ensure_fresh_parameter_gradients facts=['f3']
ASSESSMENT ANCHOR: derive_matrix_shaped_parameter_gradients facts=['f4']
ASSESSMENT ANCHOR: assert_gradient_agreement_with_explicit_tolerances facts=['f5', 'f6']

## SOURCE FACTS — B (mle.task_loss_selection)   objective: Choose a task-compatible loss and verify its output, target and gradient contracts.
B.f1: A loss compares model outputs with the corresponding target representation; choose its input contract before computing the scalar objective.   [sources: pytorch_learn_basics#optimization_tutorial.html — Hyperparameters; Loss Function; Optimizer; Full Implementation]
B.f2: CrossEntropyLoss expects unnormalized class logits; for class-index targets, logits have shape (N, C), targets have shape (N,) with dtype long and values in [0, C).   [sources: pytorch_learn_basics#https://docs.pytorch.org/docs/2.15/generated/torch.nn.CrossEntropyLoss.html — Shape; Parameters; Examples]
B.f3: MSELoss takes input and target tensors of the same shape and, under mean reduction, averages their squared elementwise differences.   [sources: pytorch_learn_basics#https://docs.pytorch.org/docs/2.15/generated/torch.nn.MSELoss.html — Formula; Shape]
B.f4: BCEWithLogitsLoss combines sigmoid and binary cross-entropy for logits and same-shaped targets in [0, 1], rather than expecting already-sigmoid-transformed inputs.   [sources: pytorch_learn_basics#https://docs.pytorch.org/docs/2.15/generated/torch.nn.BCEWithLogitsLoss.html — Formula; Shape]
B.f5: For mean squared error over M output elements, the loss derivative with respect to an output is 2 × (output−target)/M, so its sign points toward increasing loss as the output moves away from the target.   [sources: pytorch_learn_basics#https://docs.pytorch.org/docs/2.15/generated/torch.nn.MSELoss.html — Formula; Shape]
B.f6: For unweighted mean binary cross-entropy with logits over M elements, the logit derivative is (sigmoid(logit)−target)/M; this distinguishes the probability representation from the raw logit.   [sources: pytorch_learn_basics#https://docs.pytorch.org/docs/2.15/generated/torch.nn.BCEWithLogitsLoss.html — Formula; Shape]
B.f7: For mean class-index cross-entropy without weighting, the derivative per sample logit is (softmax probability−one-hot target)/N, so output width, target identity and reduction affect the gradient reference.   [sources: pytorch_learn_basics#https://docs.pytorch.org/docs/2.15/generated/torch.nn.CrossEntropyLoss.html — Shape; Parameters; Examples]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Gradients, Loss and Optimizer.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.pytorch_input_tensors, mle.autograd_gradients, mle.prediction_task_definition, mle.neural_model_definition. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a Python function with learner-written PyTorch imports that selects and verifies a loss for the supplied numerical-target fixture: outputs [2, 4] and targets [1, 2]. Check tensor shape compatibility, compute the unweighted mean loss, and compare automatic differentiation with the taught output-derivative reference.  SUCCESS: The function verifies equal output and target shapes, selects MSELoss with mean reduction, obtains loss 2.5, and confirms output derivatives [1, 2]. It verifies that both positive derivatives indicate increasing loss when the corresponding output increases farther above its target.
ASSESSMENT ANCHOR: select_cross_entropy_for_class_index_targets_and_logits facts=['f1', 'f2']
ASSESSMENT ANCHOR: select_mean_squared_error_for_same_shaped_numerical_targets facts=['f1', 'f3']
ASSESSMENT ANCHOR: select_binary_cross_entropy_with_logits_for_binary_targets facts=['f1', 'f4']
ASSESSMENT ANCHOR: verify_loss_gradient_against_output_representation_and_mean_reduction facts=['f5', 'f6', 'f7']

## SOURCE FACTS — C (mle.optimizer_configuration)   objective: Implement and test one plain-SGD update from the current gradients.
C.f1: Initialize torch.optim.SGD(model.parameters(), lr=declared_learning_rate) so the optimizer receives the trainable model parameters.   [sources: pytorch_learn_basics#optimization_tutorial.html — Hyperparameters; Loss Function; Optimizer; Full Implementation]
C.f2: For plain SGD without momentum, weight decay or other modifications, the parameter update is parameter_new = parameter_old − learning_rate × gradient.   [sources: pytorch_learn_basics#https://docs.pytorch.org/docs/2.15/generated/torch.optim.SGD.html — Algorithm; Parameters]
C.f3: Clear old parameter gradients with optimizer.zero_grad(), compute loss.backward(), then call optimizer.step() to apply the current update.   [sources: pytorch_learn_basics#optimization_tutorial.html — Hyperparameters; Loss Function; Optimizer; Full Implementation]
C.f4: Check one deterministic fixture update against the declared plain-SGD equation, rather than assuming every optimizer uses that update rule.   [sources: pytorch_learn_basics#https://docs.pytorch.org/docs/2.15/generated/torch.optim.SGD.html — Algorithm; Parameters]
C.f5: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Gradients, Loss and Optimizer.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.autograd_gradients. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a Python function with learner-written imports that configures plain SGD on the supplied small model and performs one deterministic update. Bind model.parameters(), use the declared learning rate, clear old gradients, compute the supplied loss, run backward, and step. Check the observed update against the declared equation with assert predicates.  SUCCESS: For the supplied parameter value 2, gradient 3 and learning rate 0.1, the function verifies an updated value of 1.7 and a change of −0.3 within supplied tolerances. A separate zero-learning-rate boundary fixture leaves the parameter at 2. A deliberately incorrect expected update fails an assert predicate and raises AssertionError during ordinary non-optimized execution.
ASSESSMENT ANCHOR: bind_baseline_optimizer_to_model_parameters facts=['f1']
ASSESSMENT ANCHOR: verify_declared_plain_sgd_update facts=['f2', 'f4']
ASSESSMENT ANCHOR: apply_current_gradients_in_correct_order facts=['f3']
ASSESSMENT ANCHOR: assert_valid_boundary_and_failure_cases facts=['f5']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjust training batch size to fit available memory; Apply correct neural-network training and evaluation modes; Choose CPU or GPU capacity for a bounded training workload; Choose a task-compatible training loss; Configure a baseline optimizer and learning rate; Convert an ML notebook prototype into a repeatable executable training script with an explicit entry point; Diagnose training failures from loss and gradient behavior; Diagnose training memory exhaustion; Evaluate the frozen selected model and threshold against the baseline on the protected test set; Execute a bounded managed custom-model training job on an existing platform; Expose model readiness checks before admitting prediction traffic; Freeze and identify a traceable dataset snapshot for reproducible training; Implement batch inference over a bounded dataset; Implement online prediction using the fitted preprocessing and model; Implement the minibatch forward, backward and optimizer-step loop; Package a versioned model with fitted preprocessing and inference dependencies; Place models and tensors on the correct compute device; Profile training compute and data-loading bottlenecks; Record the code revision and pinned tr

## LESSON, in learner order

### s01 · explainer · Compute neural-network gradients with automatic differentiation
Understand — 
(intro) Trace the scalar loss back to its parameters. A matrix-shaped reference makes the learning signal inspectable. ⟦A:tb1⟧
(mechanism) Autograd records tensor operations in a graph and differentiates the scalar output by the chain rule. Mark trainable leaf tensors requires_grad=True, form the scalar loss, call loss.backward() and inspect each leaf’s .grad. Backward accumulates gradients: clear old values before a fresh comparison. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) For Z = XW + b and D = ∂L/∂Z, the references are ∂L/∂W = X.T @ D and ∂L/∂b = D.sum(axis=0). D already includes loss reduction. Compare gradient shapes and values using explicit relative and absolute tolerances. Assert valid, boundary and failure predicates; false predicates raise AssertionError during ordinary non-optimized execution. ⟦A.f4 A.f5 A.f6 A:tb3⟧
[CODE python]
import torch
X = torch.tensor([[1., 2.], [3., 4.]])
D = torch.tensor([[0.1], [0.2]])
W = torch.tensor([[1.], [1.]], requires_grad=True)
b = torch.tensor([0.], requires_grad=True)
assert W.is_leaf and b.is_leaf and W.requires_grad and b.requires_grad
rtol, atol = 1e-5, 1e-6
W.grad = None
b.grad = None
Z = X @ W + b
loss = (Z * D).sum()
assert loss.shape == torch.Size([])
loss.backward()
weight_reference = X.T @ D
bias_reference = D.sum(dim=0)
weight_shape_ok = W.grad.shape == weight_reference.shape
bias_shape_ok = b.grad.shape == bias_reference.shape
weight_values_ok = torch.allclose(W.grad, weight_reference, rtol=rtol, atol=atol)
bias_values_ok = torch.allclose(b.grad, bias_reference, rtol=rtol, atol=atol)
assert weight_shape_ok and bias_shape_ok and weight_values_ok and bias_values_ok
differing_reference = weight_reference + 1
assert not torch.allclose(W.grad, differing_reference, rtol=rtol, atol=atol)
  annotations: ['D already includes reduction; compare fresh leaf gradients without dividing again.']

### s02 · explainer · Fresh gradients: the X and D matrix reference
Understand — 
(example) Use the supplied X and D once in the matrix reference. Each weight combines its feature column with D; the bias combines derivatives across rows. Do not divide again for a reduction already included in D. Compare .grad after backward and before clearing, using the declared shapes and tolerances. A transpose error or stale accumulation can invalidate a plausible-looking value. Include the differing-gradient failure fixture as well as an accepted computation. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A:tb4⟧

### s03 · video · A supporting walkthrough
Optional support — 
[VIDEO ] bridge-before:  | bridge-after: 

### s04 · explainer · A distinction to keep
Understand — 
(misconception) Backward accumulates; it does not automatically replace old gradients. Correct shapes and the supplied reduction convention matter as much as plausible numbers. ⟦A.f3 A.f4 A.f5 A:tb5⟧

### s05 · check · Judge autograd gradients
Check your judgement — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s06 · hands_on · Review autograd gradients
Review the evidence — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s07 · explainer · Choose a task-compatible training loss
Understand — 
(intro) Choose the output/target contract before computing loss. A scalar value alone cannot verify the representation. ⟦B:tb1⟧
(mechanism) A loss compares outputs with corresponding targets. For class-index CrossEntropyLoss, use unnormalized logits shaped (N, C) and long targets shaped (N,) with indices in [0, C). MSELoss requires input and target tensors of the same shape; mean reduction averages squared elementwise differences. ⟦B.f1 B.f2 B.f3 B:tb2⟧
[CODE python]
import torch
from torch import nn
outputs = torch.tensor([2., 4.], requires_grad=True)
targets = torch.tensor([1., 2.])
rtol, atol = 1e-5, 1e-6
criterion = nn.MSELoss(reduction="mean")
loss = criterion(outputs, targets)
assert loss.shape == torch.Size([])
loss.backward()
reference = 2 * (outputs.detach() - targets) / outputs.numel()
assert torch.allclose(loss.detach(), torch.tensor(2.5), rtol=rtol, atol=atol)
assert outputs.grad.shape == reference.shape
assert torch.allclose(outputs.grad, reference, rtol=rtol, atol=atol)
assert torch.allclose(outputs.grad, torch.tensor([1., 2.]), rtol=rtol, atol=atol)
  annotations: ['Two output elements: mean reduction divides the squared-error sum and derivative reference by two.']

### s08 · explainer · Choose a task-compatible training loss
Understand — 
(mechanism) BCEWithLogitsLoss combines sigmoid with binary cross-entropy: supply logits and same-shaped targets in [0, 1], not already-sigmoid inputs. For mean MSE over M elements, the output derivative is 2 × (output−target)/M. Its sign identifies the direction of increasing loss as outputs move away from targets. For unweighted mean binary-logit loss over M elements, it is (sigmoid(logit)−target)/M. These distinguish raw logits, probabilities and numerical outputs. ⟦B.f4 B.f5 B.f6 B:tb3⟧
(mechanism) For unweighted mean class-index cross-entropy, each sample’s logit derivative is (softmax probability−one-hot target)/N. The target identity, output width and sample-count reduction belong in the reference. ⟦B.f7 B:tb4⟧

### s09 · explainer · Mean MSE: value and gradient
Understand — 
(example) Compare the supplied MSE, binary-logit and class-index fixtures under their distinct contracts. Keep the mean-reduction denominator visible and inspect derivative direction as well as scalar loss. Binary-logit loss compares the sigmoid probability with its target, but receives raw logits. Class-index loss requires the declared class width and long target indices. Verify axes and dtype before applying the reference; a positive scalar does not establish the correct representation. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B:tb5⟧

### s10 · explainer · A distinction to keep
Understand — 
(misconception) CrossEntropyLoss and BCEWithLogitsLoss receive logits. Check MSE’s same-shape contract instead of relying on accidental broadcasting. ⟦B.f2 B.f3 B.f4 B:tb6⟧

### s11 · check · Judge task loss selection
Check your judgement — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s12 · check · Judge task loss selection
Check your judgement — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s13 · hands_on · Review task loss selection
Review the evidence — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s14 · explainer · Configure a baseline optimizer and learning rate
Understand — 
(intro) A deterministic single step distinguishes a current gradient from the parameter change it should produce. ⟦C:tb1⟧
(mechanism) Bind the trainable parameters with torch.optim.SGD(model.parameters(), lr=declared_learning_rate). Only for plain SGD without momentum, weight decay or other modifications, parameter_new = parameter_old − learning_rate × gradient. Clear old gradients with optimizer.zero_grad(), compute loss.backward(), then use optimizer.step() for the current update. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) Compare one deterministic update with that conditional plain-SGD equation; it is not every optimizer’s rule. Assert valid, boundary and failure predicates. False predicates raise AssertionError during ordinary non-optimized execution. ⟦C.f4 C.f5 C:tb3⟧
[BEFORE_AFTER] Backward supplies gradient 3; plain SGD step applies the reference change −0.3.
  before:
[CODE python]
import torch
from torch import nn
model = nn.Module()
model.register_parameter("value", nn.Parameter(torch.tensor(2.)))
parameter = model.value
learning_rate = 0.1
rtol, atol = 1e-5, 1e-6
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate,
                            momentum=0, weight_decay=0)
parameter_before = parameter.detach().clone()
optimizer.zero_grad()
loss = 3 * parameter
loss.backward()
current_gradient = parameter.grad.detach().clone()
assert torch.allclose(current_gradient, torch.tensor(3.), rtol=rtol, atol=atol)
  annotations: []
  after:
[CODE python]
optimizer.step()
parameter_after = parameter.detach().clone()
reference_after = parameter_before - 0.1 * current_gradient
assert torch.allclose(parameter_after, reference_after, rtol=rtol, atol=atol)
assert torch.allclose(parameter_after, torch.tensor(1.7), rtol=rtol, atol=atol)
  annotations: []

### s15 · explainer · Plain SGD: gradient 3 and parameter change −0.3
Understand — 
(example) In the supplied one-step fixture, retain the parameter before and after step and the current gradient separately. Compare the observed difference with the plain-SGD reference under declared tolerances. Backward without step can produce a gradient without updating the parameter. Bind model.parameters(), clear old gradients before a fresh backward, and retain the restrictions on momentum, weight decay and other modifications. Do not extend the equation to a different optimizer. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C:tb4⟧

### s16 · explainer · A distinction to keep
Understand — 
(misconception) A learning rate does not update parameters by itself. Backward must reach step; the plain-SGD equation retains its stated restrictions. ⟦C.f1 C.f2 C.f3 C:tb5⟧

### s17 · check · Judge optimizer configuration
Check your judgement — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s18 · hands_on · Review optimizer configuration
Review the evidence — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s19 · recap · Take the contract with you
Keep the essentials — 
(takeaway) Compare fresh gradients with the matrix reference and tolerances. ⟦A.f3 A.f4 A.f5 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Match logits or numerical outputs to the target contract and reduction. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧
(takeaway) Verify the current-gradient step under plain-SGD restrictions. ⟦C.f2 C.f3 C.f4 C:tb2 C:tb3 C:tb4 C:tb5⟧
[UP NEXT] Implement the minibatch forward, backward and optimizer-step loop: Next: Implement the minibatch forward, backward and optimizer-step loop.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the evidence from the assumption
(mechanism) Compare the computed gradients to the matrix-shaped chain-rule reference with explicit relative and absolute tolerances. ⟦A.f5 A:tb3⟧
(mechanism) Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution. ⟦A.f6 A:tb3⟧
(misconception) For the same supplied task: A fresh reference is not an accumulated gradient; inspect before clearing. ⟦A.f5 A.f6 A:tb3⟧
### r02 · Separate the evidence from the assumption
(mechanism) Autograd records tensor operations as a computation graph and differentiates the scalar output through that graph using the chain rule. ⟦A.f1 A:tb2⟧
(mechanism) Set requires_grad=True on trainable leaf tensors, form the supplied scalar loss, call loss.backward(), and inspect each leaf parameter’s .grad. ⟦A.f2 A:tb2⟧
(mechanism) Backward accumulates into .grad, so clear old gradients before comparing a fresh computation with the reference. ⟦A.f3 A:tb2⟧
(mechanism) For a linear batch Z = XW + b with scalar-loss derivative D = ∂L/∂Z, the chain rule yields ∂L/∂W = X.T @ D and ∂L/∂b = D.sum(axis=0), with any loss reduction already included in D. ⟦A.f4 A:tb3⟧
(mechanism) Compare the computed gradients to the matrix-shaped chain-rule reference with explicit relative and absolute tolerances. ⟦A.f5 A:tb3⟧
(mechanism) Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution. ⟦A.f6 A:tb3⟧
(misconception) For the same supplied task: A fresh reference is not an accumulated gradient; inspect before clearing. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A:tb2 A:tb3⟧
### r03 · Separate the evidence from the assumption
(mechanism) A loss compares model outputs with the corresponding target representation; choose its input contract before computing the scalar objective. ⟦B.f1 B:tb2⟧
(mechanism) CrossEntropyLoss expects unnormalized class logits; for class-index targets, logits have shape (N, C), targets have shape (N,) with dtype long and values in [0, C). ⟦B.f2 B:tb2⟧
(misconception) For the same supplied task: A scalar loss can exist with the wrong representation; check the contract first. ⟦B.f1 B.f2 B:tb2⟧
### r04 · Separate the evidence from the assumption
(mechanism) A loss compares model outputs with the corresponding target representation; choose its input contract before computing the scalar objective. ⟦B.f1 B:tb2⟧
(mechanism) BCEWithLogitsLoss combines sigmoid and binary cross-entropy for logits and same-shaped targets in [0, 1], rather than expecting already-sigmoid-transformed inputs. ⟦B.f4 B:tb3⟧
(misconception) For the same supplied task: A scalar loss can exist with the wrong representation; check the contract first. ⟦B.f1 B.f4 B:tb2 B:tb3⟧
### r05 · Separate the evidence from the assumption
(mechanism) A loss compares model outputs with the corresponding target representation; choose its input contract before computing the scalar objective. ⟦B.f1 B:tb2⟧
(mechanism) MSELoss takes input and target tensors of the same shape and, under mean reduction, averages their squared elementwise differences. ⟦B.f3 B:tb2⟧
(mechanism) For mean squared error over M output elements, the loss derivative with respect to an output is 2 × (output−target)/M, so its sign points toward increasing loss as the output moves away from the target. ⟦B.f5 B:tb3⟧
(mechanism) For unweighted mean binary cross-entropy with logits over M elements, the logit derivative is (sigmoid(logit)−target)/M; this distinguishes the probability representation from the raw logit. ⟦B.f6 B:tb3⟧
(mechanism) For mean class-index cross-entropy without weighting, the derivative per sample logit is (softmax probability−one-hot target)/N, so output width, target identity and reduction affect the gradient reference. ⟦B.f7 B:tb4⟧
(misconception) For the same supplied task: A scalar loss can exist with the wrong representation; check the contract first. ⟦B.f1 B.f3 B.f5 B.f6 B.f7 B:tb2 B:tb3 B:tb4⟧
### r06 · Separate the evidence from the assumption
(mechanism) Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution. ⟦C.f5 C:tb3⟧
(misconception) For the same supplied task: Backward produces gradients; step applies the parameter update. ⟦C.f5 C:tb3⟧
### r07 · Separate the evidence from the assumption
(mechanism) Initialize torch.optim.SGD(model.parameters(), lr=declared_learning_rate) so the optimizer receives the trainable model parameters. ⟦C.f1 C:tb2⟧
(mechanism) For plain SGD without momentum, weight decay or other modifications, the parameter update is parameter_new = parameter_old − learning_rate × gradient. ⟦C.f2 C:tb2⟧
(mechanism) Clear old parameter gradients with optimizer.zero_grad(), compute loss.backward(), then call optimizer.step() to apply the current update. ⟦C.f3 C:tb2⟧
(mechanism) Check one deterministic fixture update against the declared plain-SGD equation, rather than assuming every optimizer uses that update rule. ⟦C.f4 C:tb3⟧
(mechanism) Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution. ⟦C.f5 C:tb3⟧
(misconception) For the same supplied task: Backward produces gradients; step applies the parameter update. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C:tb2 C:tb3⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again

=========

# EVALUATOR PACKET — Train, Evaluate and Persist Weights (mle.tile.041_043)
Tile summary: Review minibatch updates, dropout modes and restored-state prediction checks.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.minibatch_training_loop — Implement the minibatch forward, backward and optimizer-step loop
B = mle.training_evaluation_modes — Apply correct neural-network training and evaluation modes
C = mle.weight_persistence — Save and reload neural-network weights for prediction

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (mle.minibatch_training_loop)   objective: Execute a parameterized minibatch training loop and verify its gradient/update wiring.
A.f1: Iterate for features, targets in loader inside each declared epoch, compute predictions with model(features), then loss_fn(predictions, targets).   [sources: pytorch_learn_basics#optimization_tutorial.html — Hyperparameters; Loss Function; Optimizer; Full Implementation]
A.f2: Within each minibatch, call optimizer.zero_grad(), loss.backward() and optimizer.step() so each step uses the intended current gradient.   [sources: pytorch_learn_basics#optimization_tutorial.html — Hyperparameters; Loss Function; Optimizer; Full Implementation]
A.f3: Use loss.item() to collect scalar loss evidence, and retain batch counts when forming an epoch summary so an incomplete batch is not silently misinterpreted.   [sources: pytorch_learn_basics#optimization_tutorial.html — Hyperparameters; Loss Function; Optimizer; Full Implementation]
A.f4: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
A.f5: For a plain-SGD fixture, retain parameter values before the step and assert parameter_after − parameter_before agrees with −learning_rate × current_gradient under tolerance.   [sources: pytorch_learn_basics#https://docs.pytorch.org/docs/2.15/generated/torch.optim.SGD.html — Algorithm; Parameters]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Train, Evaluate and Persist Weights.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.neural_model_definition, mle.dataset_minibatch_loader, mle.autograd_gradients, mle.task_loss_selection, mle.optimizer_configuration. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write the required PyTorch import and a learner-defined Python function that trains the supplied model within each declared epoch. Iterate features and targets from loader, perform zero-gradient, forward, loss, backward and step operations in order, and retain scalar losses with batch counts. In the supplied deterministic plain-SGD fixture, use scalar loss arithmetic and the supplied derivative-chain expectation to verify the current gradient and parameter-update direction. Write assertions for the declared valid, boundary and failure cases.  SUCCESS: Each minibatch receives exactly one update based on its current loss gradient. The five-observation fixture retains batch counts of 2, 2 and 1 alongside loss.item() values. Assertions confirm that parameter_after minus parameter_before agrees with minus learning_rate times current_gradient under the declared tolerance, including the expected direction. Valid and boundary cases pass; the declared false predicate raises AssertionError in ordinary non-optimized execution.
ASSESSMENT ANCHOR: execute_current_minibatch_update_in_correct_order facts=['f1', 'f2']
ASSESSMENT ANCHOR: retain_scalar_losses_and_batch_counts facts=['f3']
ASSESSMENT ANCHOR: assert_loss_dependent_plain_sgd_parameter_changes facts=['f4', 'f5']

## SOURCE FACTS — B (mle.training_evaluation_modes)   objective: Separate training behavior from forward-only validation behavior in a tested loop.
B.f1: Use model.train() during parameter training and model.eval() during validation; the mode changes behavior of layers such as dropout and batch normalization.   [sources: pytorch_learn_basics#optimization_tutorial.html — Hyperparameters; Loss Function; Optimizer; Full Implementation]
B.f2: Wrap validation prediction in with torch.no_grad(): to disable graph recording and avoid building gradients for validation.   [sources: pytorch_learn_basics#autogradqs_tutorial.html — Tensors, Functions and Computational graph; Computing Gradients]
B.f3: Evaluation mode and no_grad serve different purposes: eval changes relevant layer behavior, while no_grad controls gradient recording.   [sources: pytorch_learn_basics#optimization_tutorial.html — Hyperparameters; Loss Function; Optimizer; Full Implementation]
B.f4: Keep validation as a forward-only pass without optimizer.step(), then restore model.train() before the next training pass.   [sources: pytorch_learn_basics#optimization_tutorial.html — Hyperparameters; Loss Function; Optimizer; Full Implementation]
B.f5: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
B.f6: For a mode-sensitive fixture use import torch; from torch import nn; layer = nn.Dropout(p=0.5): in training each input element is randomly zeroed with probability p and retained values are scaled by 1/(1-p), whereas in evaluation layer(x) is the identity x; assert evaluation output equals the input and training output satisfies the masking/scaling rule, without assuming every random call masks an element. torch.no_grad() disables gradient recording but does not switch dropout into evaluation mode.   [sources: pytorch_learn_basics#https://docs.pytorch.org/docs/2.9/generated/torch.nn.Dropout.html — Dropout — behavior; Parameters; Examples, pytorch_learn_basics#autogradqs_tutorial.html — Disabling Gradient Tracking]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Train, Evaluate and Persist Weights.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.neural_model_definition. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a learner-defined Python function with learner-written torch and nn imports. Run one nn.Dropout(p=0.5) fixture in training and evaluation modes using supplied x. Author assertions for evaluation identity and the training masking/scaling rule, including the permitted all-retained boundary outcome and a supplied rule-violating failure case. Verify that no_grad alone does not change training mode, and restore training mode after forward-only evaluation.  SUCCESS: Evaluation output equals x. Every training output element is either zero or twice its corresponding input, without requiring any element to be masked. The all-retained boundary outcome passes the rule check, the supplied invalid outcome triggers AssertionError in ordinary non-optimized execution, validation records no gradient graph and performs no optimizer step, and the fixture finishes in training mode.
ASSESSMENT ANCHOR: select_layer_mode_for_training_and_evaluation facts=['f1', 'f3']
ASSESSMENT ANCHOR: apply_forward_only_validation_and_restore_training_mode facts=['f2', 'f3', 'f4']
ASSESSMENT ANCHOR: distinguish_dropout_mode_from_gradient_recording facts=['f3', 'f6']
ASSESSMENT ANCHOR: assert_valid_dropout_identity_and_masking_outcomes facts=['f5', 'f6']

## SOURCE FACTS — C (mle.weight_persistence)   objective: Save and reload model state through file handles and verify state and prediction agreement.
C.f1: Save learned parameters with torch.save(model.state_dict(), path), then construct the same compatible architecture before reloading.   [sources: pytorch_learn_basics#saveloadrun_tutorial.html — Saving and Loading Model Weights]
C.f2: Load the saved parameter mapping with torch.load(path, weights_only=True), and apply model.load_state_dict(mapping) to the compatible model.   [sources: pytorch_learn_basics#saveloadrun_tutorial.html — Saving and Loading Model Weights]
C.f3: Call model.eval() before prediction with the restored weights.   [sources: pytorch_learn_basics#saveloadrun_tutorial.html — Saving and Loading Model Weights]
C.f4: Compare reloaded-model predictions with the original evaluation-mode predictions on the same fixture under explicit numerical tolerances.   [sources: numpy_user_guide#reference/generated/numpy.testing.assert_allclose.html]
C.f5: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
C.f6: Open the checkpoint with a binary file handle (with open(path, "wb") for saving and "rb" for loading), and pass that handle to torch.save or torch.load.   [sources: python_tutorial#inputoutput.html — Reading and Writing Files]
C.f7: Compare corresponding original and reloaded state_dict entries in addition to fixed-input predictions to verify the parameter state was preserved.   [sources: pytorch_learn_basics#saveloadrun_tutorial.html — Saving and Loading Model Weights]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Train, Evaluate and Persist Weights.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.neural_model_definition, mle.training_evaluation_modes. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write the required library imports and a learner-defined Python function that saves the supplied network's state_dict through a binary write handle, constructs the same compatible architecture, and restores the mapping through a binary read handle using weights_only=True. Compare corresponding parameter entries and original versus restored evaluation-mode predictions on the fixed order fixture. Author assertions for the supplied valid, boundary and failure cases, and verify the deliverable with the supplied unit-test fixtures.  SUCCESS: The function preserves corresponding state_dict entries and reproduces the original evaluation-mode predictions on the same fixture within explicit supplied tolerances. It uses binary file handles for both operations. Valid and boundary fixtures satisfy the declared assertions; failure fixtures do not receive a successful reload verdict. Supplied unit-test fixtures confirm the same deliverable.
ASSESSMENT ANCHOR: restore_saved_parameters_into_compatible_architecture facts=['f1', 'f2', 'f6']
ASSESSMENT ANCHOR: verify_fixed_input_prediction_equivalence_in_evaluation_mode facts=['f3', 'f4']
ASSESSMENT ANCHOR: verify_corresponding_parameter_state facts=['f7']
ASSESSMENT ANCHOR: assert_declared_persistence_acceptance_conditions facts=['f5']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjust training batch size to fit available memory; Apply correct neural-network training and evaluation modes; Choose CPU or GPU capacity for a bounded training workload; Convert an ML notebook prototype into a repeatable executable training script with an explicit entry point; Diagnose training failures from loss and gradient behavior; Diagnose training memory exhaustion; Enforce prediction-service authentication on an existing platform; Evaluate the frozen selected model and threshold against the baseline on the protected test set; Execute a bounded managed custom-model training job on an existing platform; Expose model readiness checks before admitting prediction traffic; Freeze and identify a traceable dataset snapshot for reproducible training; Implement batch inference over a bounded dataset; Implement online prediction using the fitted preprocessing and model; Instrument prediction-service availability, errors and latency; Load-test a prediction endpoint against tail-latency and sustainable-throughput objectives; Package a versioned model with fitted preprocessing and inference dependencies; Place models and tensors on the correct compute device; Profile training compute an

## LESSON, in learner order

### s01 · explainer · Implement the minibatch forward, backward and optimizer-step loop
Understand — 
(intro) Every minibatch in each declared epoch needs the intended current-gradient update and enough loss evidence to interpret partial batches. ⟦A:tb1⟧
(mechanism) Inside each epoch, iterate for features, targets in loader. Compute model(features) and loss_fn(predictions, targets). For each minibatch, call optimizer.zero_grad(), loss.backward() and optimizer.step(). Collect scalar loss.item() evidence with batch counts so an incomplete batch is represented correctly in the epoch summary. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Assert the valid, boundary and failure predicates; a false predicate raises AssertionError during ordinary non-optimized execution. In a plain-SGD fixture, retain pre-step parameters and check parameter_after − parameter_before against −learning_rate × current_gradient under tolerance. ⟦A.f4 A.f5 A:tb3⟧
[CODE python]
import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader
features = torch.arange(5, dtype=torch.float32).reshape(5, 1)
targets = features.clone()
loader = DataLoader(TensorDataset(features, targets), batch_size=2,
                    shuffle=False, drop_last=False)
model = nn.Linear(1, 1, bias=False)
with torch.no_grad():
    model.weight.fill_(2.)
learning_rate = 0.1
rtol, atol = 1e-5, 1e-6
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate,
                            momentum=0, weight_decay=0)
criterion = nn.MSELoss(reduction="mean")
epoch_records = []
step_checks = []
for epoch in range(1):
    loss_count_pairs = []
    for batch_features, batch_targets in loader:
        batch_count = len(batch_features)
        assert batch_count == len(batch_targets)
        assert torch.equal(batch_features, batch_targets)
        parameter_before = model.weight.detach().clone()
        optimizer.zero_grad()
        outputs = model(batch_features)
        loss = criterion(outputs, batch_targets)
        loss.backward()
        current_gradient = model.weight.grad.detach().clone()
        optimizer.step()
        parameter_after = model.weight.detach().clone()
        change_ok = torch.allclose(parameter_after - parameter_before,
                                   -learning_rate * current_gradient,
                                   rtol=rtol, atol=atol)
        assert change_ok
        step_checks.append((parameter_before, current_gradient, parameter_after, change_ok))
        loss_count_pairs.append((loss.item(), batch_count))
    assert [count for scalar_loss, count in loss_count_pairs] == [2, 2, 1]
    epoch_records.append(loss_count_pairs)
  annotations: ['Each minibatch gets its own current-gradient update; the final loss is paired with count 1, not the configured maximum 2.']

### s02 · explainer · Three minibatches: current gradients and actual counts
Understand — 
(example) The retained final minibatch in the supplied order fixture is smaller than the configured maximum. Record its actual count with its scalar loss before applying the declared epoch-summary rule. Keep the full zero/backward/step sequence inside each minibatch of each epoch. Retain one pre-step parameter and verify its change at that same minibatch under the plain-SGD reference. A differently positioned step or an old gradient contribution describes a different procedure. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb4⟧

### s03 · explainer · A distinction to keep
Understand — 
(misconception) An epoch is more than a step count. Preserve actual batch counts for loss summaries, and clear old gradients before the next minibatch’s update. ⟦A.f2 A.f3 A:tb5⟧

### s04 · check · Judge minibatch training loop
Check your judgement — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s05 · hands_on · Review minibatch training loop
Review the evidence — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s06 · explainer · Apply correct neural-network training and evaluation modes
Understand — 
(intro) Validation needs two controls: layer behavior and gradient recording. Neither control replaces the other. ⟦B:tb1⟧
(mechanism) model.train() selects training behavior; model.eval() selects validation behavior for relevant layers such as dropout and batch normalization. Use with torch.no_grad(): around validation prediction to disable gradient-graph recording. eval changes layer behavior, while no_grad changes recording. ⟦B.f1 B.f2 B.f3 B:tb2⟧
[SIDE_BY_SIDE] Training under no_grad still applies dropout; evaluation changes layer behavior independently of gradient recording. left_label: Training, with and without gradient recording | right_label: Evaluation: the same dropout layer
  left:
[CODE python]
import torch
from torch import nn
layer = nn.Dropout(p=0.5)
inputs = torch.tensor([1., 2., 3., 4.], requires_grad=True)
layer.train()
training_output = layer(inputs)
with torch.no_grad():
    training_no_grad_output = layer(inputs)
for output in (training_output, training_no_grad_output):
    assert torch.all((output == 0) | (output == 2 * inputs))
assert not training_no_grad_output.requires_grad
# Neither call is required to drop at least one element.
  annotations: []
  right:
[CODE python]
layer.eval()
evaluation_output = layer(inputs)
assert torch.equal(evaluation_output, inputs)
# This is the same layer; mode and gradient recording are independent.
layer.train()
  annotations: []

### s07 · explainer · Apply and verify
Understand — 
(mechanism) Validation is forward-only: omit optimizer.step() and restore model.train() before the next training pass. Test valid, boundary and failure predicates with assert; false predicates raise AssertionError in ordinary non-optimized execution. Import torch and nn from torch for the supplied nn.Dropout(p=0.5) fixture. Training randomly zeros each element with probability p and scales retained values by 1/(1-p). Evaluation returns x unchanged. Check identity and permitted masking/scaling without requiring every random call to mask an element. no_grad does not select evaluation behavior. ⟦B.f4 B.f5 B.f6 B:tb3⟧

### s08 · explainer · Dropout: mode versus gradient recording
Understand — 
(example) In the supplied dropout fixture, inspect mode and recording context independently. Evaluation behaves as an identity even when recording is enabled. Training can still mask and scale values inside no_grad. Compare the permitted stochastic outcomes rather than demanding a particular random mask. Validation also excludes updates; disabling the graph alone does not describe the whole pass. Restore training mode afterward. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B:tb4⟧

### s09 · explainer · A distinction to keep
Understand — 
(misconception) eval does not disable recording; no_grad does not switch dropout behavior. Validation must also exclude parameter updates. ⟦B.f1 B.f2 B.f3 B.f4 B.f6 B:tb5⟧

### s10 · video · A supporting walkthrough
Optional support — 
[VIDEO ] bridge-before:  | bridge-after: 

### s11 · check · Judge training evaluation modes
Check your judgement — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s12 · hands_on · Review training evaluation modes
Review the evidence — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s13 · explainer · Save and reload neural-network weights for prediction
Understand — 
(intro) Restoring learned state requires a compatible architecture and checks of both parameters and fixed-fixture predictions. ⟦C:tb1⟧
(mechanism) torch.save(model.state_dict(), path) saves learned parameters. Reconstruct the same compatible architecture, read the mapping with torch.load(path, weights_only=True), and apply model.load_state_dict(mapping). Select model.eval() before restored prediction. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) Compare original and restored evaluation predictions on the same fixture with explicit numerical tolerances. Assert valid, boundary and failure predicates; false predicates raise AssertionError during ordinary non-optimized execution. For the specified handle-based path, open with open(path, "wb") to save and open(path, "rb") to load, passing the binary handle to torch.save or torch.load. ⟦C.f4 C.f5 C.f6 C:tb3⟧
(mechanism) Also compare corresponding original and restored state_dict entries to verify preserved parameter state. ⟦C.f7 C:tb4⟧
[SIDE_BY_SIDE] Check corresponding parameter entries separately from same-input evaluation predictions. left_label: Preserve state | right_label: Restore and verify
  left:
[CODE python]
import torch
from torch import nn
from tempfile import TemporaryDirectory
from pathlib import Path

def compatible_architecture():
    return nn.Linear(2, 1)

model = compatible_architecture()
fixed_input = torch.tensor([[1., 2.], [3., 4.]])
rtol, atol = 1e-5, 1e-6
original_entries = {name: value.detach().clone()
                    for name, value in model.state_dict().items()}
model.eval()
with torch.no_grad():
    original_predictions = model(fixed_input).detach().clone()
temporary = TemporaryDirectory()
path = Path(temporary.name) / "weights.pt"
with open(path, "wb") as handle:
    torch.save(model.state_dict(), handle)
  annotations: []
  right:
[CODE python]
restored = compatible_architecture()
with open(path, "rb") as handle:
    mapping = torch.load(handle, weights_only=True)
restored.load_state_dict(mapping)
restored_entries = restored.state_dict()
assert original_entries.keys() == restored_entries.keys()
entry_equal = {name: torch.equal(value, restored_entries[name])
               for name, value in original_entries.items()}
assert all(entry_equal.values())
name = next(iter(original_entries))
differing_entry = original_entries[name] + 1
assert not torch.equal(differing_entry, restored_entries[name])
restored.eval()
with torch.no_grad():
    restored_predictions = restored(fixed_input)
predictions_match = torch.allclose(original_predictions, restored_predictions,
                                   rtol=rtol, atol=atol)
assert predictions_match
temporary.cleanup()
  annotations: []

### s14 · explainer · Restored entries and same-input predictions
Understand — 
(example) Keep the original evaluation predictions as the reference, rather than generating both references with the restored object. Save and load through binary handles, reconstruct the compatible architecture and apply the parameter mapping. Compare corresponding entries separately from the same-fixture prediction check. One matching output does not replace state verification. Distinguish an incompatible architecture or differing entry from successful restoration. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C.f7 C:tb5⟧

### s15 · explainer · A distinction to keep
Understand — 
(misconception) Weight loading does not choose an architecture. Use compatible structure, matching evaluation fixtures and parameter-entry checks. ⟦C.f1 C.f3 C.f4 C.f7 C:tb6⟧

### s16 · check · Judge weight persistence
Check your judgement — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s17 · hands_on · Review weight persistence
Review the evidence — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s18 · recap · Take the contract with you
Keep the essentials — 
(takeaway) Repeat zero/backward/step per batch; retain actual counts with losses. ⟦A.f2 A.f3 A:tb2 A:tb4 A:tb5⟧
(takeaway) Validation needs evaluation behavior, no_grad and no updates. ⟦B.f1 B.f2 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧
(takeaway) Restore compatible state and check entries plus fixed-fixture predictions. ⟦C.f2 C.f4 C.f7 C:tb2 C:tb3 C:tb4 C:tb5 C:tb6⟧
[UP NEXT] Stop training using validation behavior without consulting the protected test: Next: Stop training using validation behavior without consulting the protected test.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the evidence from the assumption
(mechanism) Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution. ⟦A.f4 A:tb3⟧
(mechanism) For a plain-SGD fixture, retain parameter values before the step and assert parameter_after − parameter_before agrees with −learning_rate × current_gradient under tolerance. ⟦A.f5 A:tb3⟧
(misconception) For the same supplied task: A configured batch maximum is not the actual final-batch count. ⟦A.f4 A.f5 A:tb3⟧
### r02 · Separate the evidence from the assumption
(mechanism) Iterate for features, targets in loader inside each declared epoch, compute predictions with model(features), then loss_fn(predictions, targets). ⟦A.f1 A:tb2⟧
(mechanism) Within each minibatch, call optimizer.zero_grad(), loss.backward() and optimizer.step() so each step uses the intended current gradient. ⟦A.f2 A:tb2⟧
(mechanism) Use loss.item() to collect scalar loss evidence, and retain batch counts when forming an epoch summary so an incomplete batch is not silently misinterpreted. ⟦A.f3 A:tb2⟧
(mechanism) Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution. ⟦A.f4 A:tb3⟧
(mechanism) For a plain-SGD fixture, retain parameter values before the step and assert parameter_after − parameter_before agrees with −learning_rate × current_gradient under tolerance. ⟦A.f5 A:tb3⟧
(misconception) For the same supplied task: A configured batch maximum is not the actual final-batch count. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3⟧
### r03 · Separate the evidence from the assumption
(mechanism) Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution. ⟦B.f5 B:tb3⟧
(mechanism) For a mode-sensitive fixture use import torch; from torch import nn; layer = nn.Dropout(p=0.5): in training each input element is randomly zeroed with probability p and retained values are scaled by 1/(1-p), whereas in evaluation layer(x) is the identity x; assert evaluation output equals the input and training output satisfies the masking/scaling rule, without assuming every random call masks an element. torch.no_grad() disables gradient recording but does not switch dropout into evaluation mode. ⟦B.f6 B:tb3⟧
(misconception) For the same supplied task: no_grad changes recording, not dropout’s layer mode. ⟦B.f5 B.f6 B:tb3⟧
### r04 · Separate the evidence from the assumption
(mechanism) Use model.train() during parameter training and model.eval() during validation; the mode changes behavior of layers such as dropout and batch normalization. ⟦B.f1 B:tb2⟧
(mechanism) Wrap validation prediction in with torch.no_grad(): to disable graph recording and avoid building gradients for validation. ⟦B.f2 B:tb2⟧
(mechanism) Evaluation mode and no_grad serve different purposes: eval changes relevant layer behavior, while no_grad controls gradient recording. ⟦B.f3 B:tb2⟧
(mechanism) Keep validation as a forward-only pass without optimizer.step(), then restore model.train() before the next training pass. ⟦B.f4 B:tb3⟧
(mechanism) Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution. ⟦B.f5 B:tb3⟧
(mechanism) For a mode-sensitive fixture use import torch; from torch import nn; layer = nn.Dropout(p=0.5): in training each input element is randomly zeroed with probability p and retained values are scaled by 1/(1-p), whereas in evaluation layer(x) is the identity x; assert evaluation output equals the input and training output satisfies the masking/scaling rule, without assuming every random call masks an element. torch.no_grad() disables gradient recording but does not switch dropout into evaluation mode. ⟦B.f6 B:tb3⟧
(misconception) For the same supplied task: no_grad changes recording, not dropout’s layer mode. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B:tb2 B:tb3⟧
### r05 · Separate the evidence from the assumption
(mechanism) Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution. ⟦C.f5 C:tb3⟧
(misconception) For the same supplied task: One matching prediction is not a substitute for corresponding state-entry checks. ⟦C.f5 C:tb3⟧
### r06 · Separate the evidence from the assumption
(mechanism) Save learned parameters with torch.save(model.state_dict(), path), then construct the same compatible architecture before reloading. ⟦C.f1 C:tb2⟧
(mechanism) Load the saved parameter mapping with torch.load(path, weights_only=True), and apply model.load_state_dict(mapping) to the compatible model. ⟦C.f2 C:tb2⟧
(mechanism) Call model.eval() before prediction with the restored weights. ⟦C.f3 C:tb2⟧
(mechanism) Compare reloaded-model predictions with the original evaluation-mode predictions on the same fixture under explicit numerical tolerances. ⟦C.f4 C:tb3⟧
(mechanism) Open the checkpoint with a binary file handle (with open(path, "wb") for saving and "rb" for loading), and pass that handle to torch.save or torch.load. ⟦C.f6 C:tb3⟧
(mechanism) Compare corresponding original and reloaded state_dict entries in addition to fixed-input predictions to verify the parameter state was preserved. ⟦C.f7 C:tb4⟧
(misconception) For the same supplied task: One matching prediction is not a substitute for corresponding state-entry checks. ⟦C.f1 C.f2 C.f3 C.f4 C.f6 C.f7 C:tb2 C:tb3 C:tb4⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again

=========

# EVALUATOR PACKET — Stop and Debug Training (mle.tile.044_045)
Tile summary: Review validation stopping decisions and same-fixture training-failure diagnosis.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.validation_early_stopping — Stop training using validation behavior without consulting the protected test
B = mle.training_failure_diagnosis — Diagnose training failures from loss and gradient behavior

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (mle.validation_early_stopping)   objective: Implement a validation-patience controller that returns the best retained model state.
A.f1: Predeclare the validation quantity, improvement direction, minimum improvement and patience; patience counts consecutive epochs without sufficient improvement.   [sources: tensorflow_tutorials#https://www.tensorflow.org/api_docs/python/tf/keras/callbacks/EarlyStopping — Args]
A.f2: For a minimized validation quantity, reset the non-improvement counter only when current < best − min_delta; otherwise increment it and stop when the declared patience is exhausted.   [sources: tensorflow_tutorials#https://www.tensorflow.org/api_docs/python/tf/keras/callbacks/EarlyStopping — Args]
A.f3: Retain the model weights associated with the best monitored validation value rather than automatically using the last epoch’s weights.   [sources: tensorflow_tutorials#https://www.tensorflow.org/api_docs/python/tf/keras/callbacks/EarlyStopping — Args]
A.f4: A state_dict refers to live parameter values, so preserve a best-epoch state with a deep copy or a saved state file before later updates alter the model.   [sources: pytorch_learn_basics#saveloadrun_tutorial.html — Saving and Loading Model Weights]
A.f5: Do not use protected test observations to fit preprocessing, choose a model or tune its settings; doing so leaks information into the chosen system.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.2 Data leakage]
A.f6: Implement the controller as a while loop bounded by maximum epochs and the non-improvement rule; update best loss/checkpoint inside the improvement branch and use break when patience is exhausted.   [sources: python_tutorial#controlflow.html — Defining Functions; Default Argument Values; Keyword Arguments]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Stop and Debug Training.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.minibatch_training_loop, mle.weight_persistence, mle.deployment_matched_splits, mle.training_evaluation_modes. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a learner-defined Python training-controller function with learner-written imports. Predeclare minimized validation loss, min_delta, patience and maximum epochs. Use an explicit while loop, compare current < best - min_delta, update the best loss and independently preserved checkpoint only on sufficient improvement, and break when patience is exhausted. Restore and report the accepted checkpoint without accessing protected test data or using a framework early-stopping callback.  SUCCESS: For validation losses 0.50, 0.44, 0.43 and 0.45, min_delta 0.02, patience 2 and a maximum of 10 epochs, the controller records counters 0, 0, 1 and 2, stops after epoch 4, and restores the checkpoint accepted at epoch 2 with loss 0.44. It reports that epoch and loss, preserves weights independently of later model updates, respects the epoch bound, and never accesses protected test data.
ASSESSMENT ANCHOR: choose_stopping_point_by_declared_validation_rule facts=['f1', 'f2', 'f6']
ASSESSMENT ANCHOR: preserve_and_restore_accepted_best_checkpoint facts=['f3', 'f4']
ASSESSMENT ANCHOR: keep_protected_test_out_of_training_decisions facts=['f5']

## SOURCE FACTS — B (mle.training_failure_diagnosis)   objective: Localize and correct one evidence-supported neural training failure.
B.f1: Inspect trainable parameter .grad values after backward and before clearing gradients to determine whether expected parameters receive a learning signal.   [sources: pytorch_learn_basics#autogradqs_tutorial.html — Tensors, Functions and Computational graph; Computing Gradients]
B.f2: Check the observed losses, output/target compatibility and learning rate against the declared training computation before changing the training configuration.   [sources: pytorch_learn_basics#optimization_tutorial.html — Hyperparameters; Loss Function; Optimizer; Full Implementation]
B.f3: Choose one evidence-supported correction, rerun the same bounded fixture and compare its loss/gradient record with the failing reference.   [sources: pytorch_learn_basics#optimization_tutorial.html — Hyperparameters; Loss Function; Optimizer; Full Implementation]
B.f4: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
B.f5: Follow the derivative chain from loss to outputs to parameters, compare expected signs and measured gradient magnitudes, and test a single root-cause hypothesis on the reproduced failure.   [sources: pytorch_learn_basics#autogradqs_tutorial.html — Tensors, Functions and Computational graph; Computing Gradients]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Stop and Debug Training.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.minibatch_training_loop, mle.autograd_gradients, mle.task_loss_selection. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Implement a learner-defined Python function with learner-written imports for the required dependencies. Within supplied infrastructure scaffolding, reproduce one failing bounded training fixture, inspect the derivative chain and parameter gradients, check the declared loss, output/target and learning-rate contract, and test one evidence-supported correction. Write assertion predicates for the supplied valid, boundary and failure cases.  SUCCESS: The function preserves the supplied fixture and failing reference, records gradients after backward and before clearing them, identifies one supported root-cause hypothesis, and changes only its supported factor. The corrected rerun meets the declared loss, gradient and update expectations. Assertions distinguish the valid, boundary and reproduced failure cases; a deliberately false predicate raises AssertionError in ordinary non-optimized execution.
ASSESSMENT ANCHOR: localize_failure_from_derivative_and_parameter_gradient_evidence facts=['f1', 'f5']
ASSESSMENT ANCHOR: check_loss_target_and_learning_rate_contract facts=['f2', 'f5']
ASSESSMENT ANCHOR: evaluate_one_correction_against_failing_loss_gradient_and_update_records facts=['f3', 'f5']
ASSESSMENT ANCHOR: define_assertion_predicates_for_valid_boundary_and_failure_cases facts=['f4']

## DATA ASSETS USED
ds.early_stopping_trace: Validation patience trace — columns: epoch(numerical), validation_loss(numerical), min_delta(numerical), patience(numerical), maximum_epochs(numerical), sufficient_improvement(categorical), accepted_best_loss(numerical), non_improvement_counter(numerical), checkpoint_epoch(numerical), stop(categorical)
   [1,0.5,0.02,2,10,true,0.5,0,1,false]
   [2,0.44,0.02,2,10,true,0.44,0,2,false]
   [3,0.43,0.02,2,10,false,0.44,1,2,false]
   [4,0.45,0.02,2,10,false,0.44,2,2,true]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjust training batch size to fit available memory; Choose CPU or GPU capacity for a bounded training workload; Choose inference batching under latency constraints; Configure bounded prediction-worker concurrency on an existing runtime; Convert an ML notebook prototype into a repeatable executable training script with an explicit entry point; Diagnose training failures from loss and gradient behavior; Diagnose training memory exhaustion; Enforce prediction-service authentication on an existing platform; Evaluate the frozen selected model and threshold against the baseline on the protected test set; Execute a bounded managed custom-model training job on an existing platform; Expose model readiness checks before admitting prediction traffic; Freeze and identify a traceable dataset snapshot for reproducible training; Implement batch inference over a bounded dataset; Implement online prediction using the fitted preprocessing and model; Instrument prediction-service availability, errors and latency; Load-test a prediction endpoint against tail-latency and sustainable-throughput objectives; Package a versioned model with fitted preprocessing and inference dependencies; Place models and t

## LESSON, in learner order

### s01 · explainer · Stop training using validation behavior without consulting the protected test
Understand — 
(intro) Early stopping follows predeclared improvement and patience rules. Preserve the accepted checkpoint, not automatically the last epoch. ⟦A:tb1⟧
(mechanism) Declare the validation quantity, direction, min_delta and patience. For minimization, reset the consecutive non-improvement count only if current < best − min_delta; otherwise increment and stop when patience is exhausted. best is the most recently accepted checkpoint’s value, not necessarily the lowest observation. Retain that checkpoint’s weights. ⟦A.f1 A.f2 A.f3 A:tb2⟧
[CODE python]
# Minimized validation quantity; best belongs to an accepted checkpoint.
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
# Retain the accepted snapshot, not automatically the last live weights.
  annotations: []

### s02 · explainer · Apply and verify
Understand — 
(mechanism) A state_dict references live values: deep-copy the accepted state or save it before further updates. Keep protected-test observations out of preprocessing fit, model selection and tuning to avoid leakage. Bound the controller’s while loop by maximum epochs and the non-improvement rule. Update best loss and checkpoint within the improvement branch; break when patience is exhausted. ⟦A.f4 A.f5 A.f6 A:tb3⟧

### s03 · explainer · Validation patience: accepted checkpoint versus lowest loss
Understand — 
(example) Trace the registered validation sequence using its strict min_delta comparison. A smaller observed loss can still be insufficient improvement, leaving the previously accepted checkpoint unchanged. Reset or increment the counter at every epoch, and honor both patience and the maximum-epoch bound. Deep-copy or save weights when improvement is accepted, then restore that snapshot instead of the last live weights. Protected-test observations do not choose patience or the checkpoint. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A:tb4⟧
[TABLE ds.early_stopping_trace cols=['epoch', 'validation_loss', 'min_delta', 'patience', 'maximum_epochs', 'sufficient_improvement', 'accepted_best_loss', 'non_improvement_counter', 'checkpoint_epoch', 'stop'] ] caption: Validation patience trace

### s04 · explainer · A distinction to keep
Understand — 
(misconception) A live state_dict is not a frozen snapshot. A small loss decrease need not pass min_delta; preserve the accepted state before later updates. ⟦A.f2 A.f4 A:tb5⟧

### s05 · check · Judge validation early stopping
Check your judgement — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s06 · hands_on · Review validation early stopping
Review the evidence — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s07 · explainer · Diagnose training failures from loss and gradient behavior
Understand — 
(intro) Reproduce the failure; inspect loss, representation and gradients before changing settings. ⟦B:tb1⟧
(mechanism) Inspect expected trainable parameters’ .grad after backward and before clearing. Compare losses, output/target compatibility and learning rate with the declared computation. Choose one evidence-supported correction and rerun the identical bounded fixture, comparing loss and gradient records with the failing reference. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Assert valid, boundary and failure predicates; false predicates raise AssertionError in ordinary non-optimized execution. Follow the derivative chain from loss through outputs to parameters, checking expected signs and measured magnitudes. Test one root-cause hypothesis on the reproduced failure. ⟦B.f4 B.f5 B:tb3⟧
[SIDE_BY_SIDE] No corrected observation is claimed: compare loss and gradient evidence on the same fixture. left_label: Illustrative failing evidence | right_label: One hypothesis; conditional acceptance
  left:
[DIAGRAM: Illustrative reproduced failure] nodes=['Expected selected gradient: negative', 'Measured failing gradient: zero', 'Inspect after backward, before clearing', 'Failing loss: supplied record; selected gradient fails derivative-reference sign', 'Preserve fixture, target representation, learning rate and derivative reference'] edges=[('node0', 'node1', None), ('node1', 'node2', None), ('node2', 'node3', None), ('node3', 'node4', None)] alt: Illustrative reproduced failure: Expected selected gradient: negative; Measured failing gradient: zero; Inspect after backward, before clearing; Failing loss: supplied record; selected gradient fails derivative-reference sign; Preserve fixture, target representation, learning rate and derivative reference
  right:
[DIAGRAM: Illustrative correction checks — no corrected observation supplied] nodes=['Supported hypothesis to test: a missing gradient path to the selected parameter', 'Single correction: restore that path; rerun the identical bounded fixture', 'Loss predicate: compare corrected_loss with same_fixture_loss_reference under declared tolerance', 'Gradient sign predicate: corrected_gradient < 0', 'Gradient magnitude predicate: allclose(corrected_gradient, declared_derivative_reference, rtol, atol)', 'Accept only when the corrected sign and magnitude satisfy the declared derivative reference.'] edges=[('node0', 'node1', None), ('node1', 'node2', None), ('node2', 'node3', None), ('node3', 'node4', None), ('node4', 'node5', None)] alt: Illustrative correction checks — no corrected observation supplied: Supported hypothesis to test: a missing gradient path to the selected parameter; Single correction: restore that path; rerun the identical bounded fixture; Loss predicate: compare corrected_loss with same_fixture_loss_reference under declared tolerance; Gradient sign predicate: corrected_gradient < 0; Gradient magnitude predicate: allclose(corrected_gradient, declared_derivative_reference, rtol, atol); Accept only when the corrected sign and magnitude satisfy the declared derivative reference.

### s08 · explainer · Negative reference, zero gradient: isolate one cause
Understand — 
(example) For the supplied missing-gradient failure, compare the expected sign with the measured gradient at the same point after backward. Follow the derivative chain, checking target representation and declared learning rate alongside loss. Preserve the failing reference while testing one supported correction on the identical fixture. Compare corrected signs, magnitudes and losses. Several simultaneous changes or a different task would not isolate that hypothesis; disappearance of an exception alone is insufficient. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb4⟧

### s09 · explainer · A distinction to keep
Understand — 
(misconception) A stalled loss is not permission for arbitrary changes. Inspect gradients before zeroing them, then test one evidence-supported correction. ⟦B.f1 B.f2 B.f3 B.f5 B:tb5⟧

### s10 · check · Judge training failure diagnosis
Check your judgement — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s11 · hands_on · Review training failure diagnosis
Review the evidence — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s12 · recap · Take the contract with you
Keep the essentials — 
(takeaway) Preserve the checkpoint accepted by the declared improvement rule. ⟦A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Inspect gradients before clearing; test one supported correction. ⟦B.f1 B.f3 B:tb2 B:tb4 B:tb5⟧
[UP NEXT] Place models and tensors on the correct compute device: Next: Place models and tensors on the correct compute device.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the evidence from the assumption
(mechanism) Do not use protected test observations to fit preprocessing, choose a model or tune its settings; doing so leaks information into the chosen system. ⟦A.f5 A:tb3⟧
(misconception) For the same supplied task: A lower observation is not necessarily an accepted improvement under min_delta. ⟦A.f5 A:tb3⟧
### r02 · Separate the evidence from the assumption
(mechanism) Predeclare the validation quantity, improvement direction, minimum improvement and patience; patience counts consecutive epochs without sufficient improvement. ⟦A.f1 A:tb2⟧
(mechanism) For a minimized validation quantity, reset the non-improvement counter only when current < best − min_delta; otherwise increment it and stop when the declared patience is exhausted. ⟦A.f2 A:tb2⟧
(mechanism) Retain the checkpoint weights accepted under min_delta, rather than automatically using the last epoch’s weights. ⟦A.f3 A:tb2⟧
(mechanism) A state_dict refers to live parameter values, so preserve a best-epoch state with a deep copy or a saved state file before later updates alter the model. ⟦A.f4 A:tb3⟧
(mechanism) Do not use protected test observations to fit preprocessing, choose a model or tune its settings; doing so leaks information into the chosen system. ⟦A.f5 A:tb3⟧
(mechanism) Implement the controller as a while loop bounded by maximum epochs and the non-improvement rule; update best loss/checkpoint inside the improvement branch and use break when patience is exhausted. ⟦A.f6 A:tb3⟧
(misconception) For the same supplied task: A lower observation is not necessarily an accepted improvement under min_delta. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A:tb2 A:tb3⟧
### r03 · Separate the evidence from the assumption
(mechanism) Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution. ⟦B.f4 B:tb3⟧
(misconception) For the same supplied task: Inspecting after zeroing can hide the gradient; compare after backward. ⟦B.f4 B:tb3⟧
### r04 · Separate the evidence from the assumption
(mechanism) Inspect trainable parameter .grad values after backward and before clearing gradients to determine whether expected parameters receive a learning signal. ⟦B.f1 B:tb2⟧
(mechanism) Check the observed losses, output/target compatibility and learning rate against the declared training computation before changing the training configuration. ⟦B.f2 B:tb2⟧
(mechanism) Choose one evidence-supported correction, rerun the same bounded fixture and compare its loss/gradient record with the failing reference. ⟦B.f3 B:tb2⟧
(mechanism) Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution. ⟦B.f4 B:tb3⟧
(mechanism) Follow the derivative chain from loss to outputs to parameters, compare expected signs and measured gradient magnitudes, and test a single root-cause hypothesis on the reproduced failure. ⟦B.f5 B:tb3⟧
(misconception) For the same supplied task: Inspecting after zeroing can hide the gradient; compare after backward. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2 B:tb3⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again

=========

# EVALUATOR PACKET — Device Placement and Memory Limits (mle.tile.046_048)
Tile summary: Review device placement, batch-size limits and live-allocation memory evidence.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.device_placement — Place models and tensors on the correct compute device
B = mle.training_batch_sizing — Adjust training batch size to fit available memory
C = mle.training_memory_diagnosis — Diagnose training memory exhaustion

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (mle.device_placement)   objective: Verify consistent tensor/model placement on an authorized instance and restore its stopped state.
A.f1: Check torch.cuda.is_available() before choosing torch.device("cuda"); otherwise select the supported CPU device.   [sources: pytorch_learn_basics#tensorqs_tutorial.html — Initializing a Tensor; Attributes of a Tensor; Operations on Tensors]
A.f2: Move the model with model.to(device) and every input and target tensor with tensor.to(device) so operations use compatible device placement.   [sources: pytorch_learn_basics#tensorqs_tutorial.html — Initializing a Tensor; Attributes of a Tensor; Operations on Tensors]
A.f3: Inspect the model parameters’ device and both minibatch tensor devices, and run a bounded forward/backward fixture to check the declared placement.   [sources: pytorch_learn_basics#tensorqs_tutorial.html — Initializing a Tensor; Attributes of a Tensor; Operations on Tensors]
A.f4: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
A.f5: For an authorized supplied Compute Engine VM, gcloud compute instances start INSTANCE --zone=ZONE and gcloud compute instances stop INSTANCE --zone=ZONE change its lifecycle state; wait for the operation and inspect the resulting state.   [sources: google_mlops_pipelines#https://cloud.google.com/compute/docs/instances/stop-start-instance — Stop an instance; Start an instance]
A.f6: Connect to the running authorized VM with gcloud compute ssh INSTANCE --zone=ZONE to execute the workload.   [sources: google_mlops_pipelines#https://cloud.google.com/compute/docs/connect/standard-ssh — Connect to VMs]
A.f7: Use gcloud compute instances describe INSTANCE --zone=ZONE to inspect the instance status and identity before and after the authorized lifecycle action.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/sdk/gcloud/reference/compute/instances/describe — DESCRIPTION; EXAMPLES]
A.f8: Stop the authorized instance after the bounded workload with gcloud compute instances stop INSTANCE --zone=ZONE, wait for completion and verify its stopped state.   [sources: google_mlops_pipelines#https://cloud.google.com/compute/docs/instances/stop-start-instance — Stop an instance; Start an instance]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Device Placement and Memory Limits.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.pytorch_input_tensors, mle.neural_model_definition. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Inspect the supplied stopped Compute Engine VM's identity and status, start it within the authorized scope, wait for completion, verify its running state and connect. Write the required imports and a Python function that selects CUDA only when available, otherwise selects the supported CPU device, and aligns the supplied model, matrix-shaped features and targets. Diagnose and repair the supplied device mismatch, verify bounded forward/backward and prediction execution, then stop the authorized instance and verify its stopped state.  SUCCESS: The lifecycle record identifies the authorized instance and confirms its initial, running and final stopped states. The learner-written function records the actual selected device, places model state, features and targets compatibly without repeated transfers during the bounded fixture, and completes forward/backward and prediction execution. Assertions cover the declared valid, boundary and failure cases; a deliberately false placement predicate raises AssertionError in ordinary non-optimized execution.
ASSESSMENT ANCHOR: select_device_from_measured_availability facts=['f1']
ASSESSMENT ANCHOR: detect_and_fix_model_input_target_device_mismatches facts=['f2', 'f3']
ASSESSMENT ANCHOR: verify_compatible_placement_without_unnecessary_transfers facts=['f2', 'f3']
ASSESSMENT ANCHOR: validate_placement_with_bounded_execution_and_assertions facts=['f3', 'f4']
ASSESSMENT ANCHOR: execute_bounded_workload_on_authorized_instance_and_verify_shutdown facts=['f5', 'f6', 'f7', 'f8']

## SOURCE FACTS — B (mle.training_batch_sizing)   objective: Choose a minibatch size using matrix-memory estimates, observed peak memory and completed-work evidence.
B.f1: Training memory includes live tensors and other allocations; larger minibatches ordinarily require more activation storage, so input element bytes alone do not define peak training memory.   [sources: pytorch_learn_basics#https://docs.pytorch.org/docs/2.15/notes/cuda.html — Memory management; Asynchronous execution]
B.f2: Vary only the declared batch_size of the DataLoader for the comparison, preserving observation alignment and the supplied training task.   [sources: pytorch_learn_basics#data_tutorial.html — Creating a Custom Dataset for your files; Preparing your data for training with DataLoaders]
B.f3: For a CUDA trial, reset_peak_memory_stats() before the measured workload and inspect torch.cuda.max_memory_allocated() afterward to obtain peak allocated tensor bytes.   [sources: pytorch_learn_basics#https://docs.pytorch.org/docs/2.15/notes/cuda.html — Memory management; Asynchronous execution]
B.f4: A reported allocated-tensor peak does not include every component of GPU usage; compare the supplied budget with the memory quantity it actually governs.   [sources: pytorch_learn_basics#https://docs.pytorch.org/docs/2.15/notes/cuda.html — Memory management; Asynchronous execution]
B.f5: Compare completed work per elapsed time for the eligible batch sizes and choose a size within the measured memory bound.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/framework/operational-excellence/manage-and-optimize-cloud-resources — Manage and optimize cloud resources]
B.f6: Estimate the matrix-shaped minibatch allocation as batch_rows × feature_columns × bytes_per_feature_element, add the target allocation under its dtype, and compare this estimate with the actual observed peak.   [sources: numpy_user_guide#reference/generated/numpy.ndarray.nbytes.html]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Device Placement and Memory Limits.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.minibatch_training_loop, mle.device_placement, mle.numpy_dtype_selection, mle.dataset_minibatch_loader. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a Python function with learner-written imports that compares supplied candidate DataLoader batch sizes for the existing training task. Calculate feature and target allocation estimates from actual batch dimensions and dtype widths, measure each bounded CUDA trial's peak allocated tensor bytes and completed examples per elapsed time, and select an eligible batch size using the supplied budget interpretation.  SUCCESS: The function changes only DataLoader batch_size across otherwise equivalent trials, preserves observation alignment, reports feature-plus-target byte estimates alongside measured peaks, counts actual completed examples including the final incomplete batch, and selects a successfully completed setting that meets the supplied memory and performance requirements.
ASSESSMENT ANCHOR: distinguish_batch_allocation_estimates_from_measured_training_memory facts=['f1', 'f4', 'f6']
ASSESSMENT ANCHOR: measure_peak_allocated_tensor_memory_for_controlled_batch_size_trials facts=['f2', 'f3']
ASSESSMENT ANCHOR: choose_batch_size_within_the_declared_measured_memory_bound facts=['f4', 'f5']

## SOURCE FACTS — C (mle.training_memory_diagnosis)   objective: Diagnose a reproduced out-of-memory failure from simultaneous allocations and runtime measurements.
C.f1: CUDA memory_allocated reports tensor-occupied memory, while memory_reserved includes storage held by the caching allocator; distinguish them when locating exhaustion.   [sources: pytorch_learn_basics#https://docs.pytorch.org/docs/2.15/notes/cuda.html — Memory management; Asynchronous execution]
C.f2: Inspect the workload’s peak allocated and reserved memory and the point of failure before attributing the failure to the input batch alone.   [sources: pytorch_learn_basics#https://docs.pytorch.org/docs/2.15/notes/cuda.html — Memory management; Asynchronous execution]
C.f3: Retaining tensors attached to computation graphs can retain graph memory; use detached/scalar diagnostic values when gradients through those saved values are not needed.   [sources: pytorch_learn_basics#autogradqs_tutorial.html — Tensors, Functions and Computational graph; Computing Gradients]
C.f4: empty_cache releases unused cached memory for other uses but cannot free storage occupied by live tensors.   [sources: pytorch_learn_basics#https://docs.pytorch.org/docs/2.15/notes/cuda.html — Memory management; Asynchronous execution]
C.f5: Change one supported factor, such as reducing minibatch size or removing an unnecessary retained graph reference, and verify completion and the measured peak on the same bounded workload.   [sources: pytorch_learn_basics#https://docs.pytorch.org/docs/2.15/notes/cuda.html — Memory management; Asynchronous execution]
C.f6: Account for each parameter, gradient, activation and batch matrix as element_count × element_width, then sum simultaneously live allocations rather than only the input matrix.   [sources: numpy_user_guide#reference/generated/numpy.ndarray.nbytes.html]
C.f7: For a linear layer with input width F and output width H, the weight matrix has F × H elements and its bias has H, supporting the parameter-allocation reference.   [sources: pytorch_learn_basics#buildmodel_tutorial.html — Define the Class; Model Layers]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Device Placement and Memory Limits.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.minibatch_training_loop, mle.training_batch_sizing, mle.numpy_dtype_selection, mle.device_placement. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a learner-defined Python function with learner-written imports that diagnoses one supplied CUDA out-of-memory case within existing infrastructure scaffolding. Reproduce the failure, record its location and allocated/reserved peaks, account for simultaneously live parameter, gradient, activation and batch allocations using matrix dimensions and element widths, then change one supported factor and rerun the same bounded workload.  SUCCESS: The function returns failed-run evidence, an allocation reference, a justified diagnosis, the single correction applied, and corrected-run evidence. The corrected run completes the same bounded task within the supplied memory requirement; its measured allocated and reserved peaks are retained for comparison.
ASSESSMENT ANCHOR: distinguish_live_tensor_allocations_from_reserved_memory facts=['f1', 'f2', 'f4']
ASSESSMENT ANCHOR: identify_graph_connected_diagnostic_retention facts=['f3']
ASSESSMENT ANCHOR: attribute_memory_exhaustion_using_simultaneously_live_allocation_sizes facts=['f6', 'f7']
ASSESSMENT ANCHOR: verify_a_single_memory_correction_against_failure_evidence facts=['f2', 'f5']

## DATA ASSETS USED
ds.batch_size_trials: Controlled batch-size comparison — columns: batch_size(numerical), actual_feature_shape(text), actual_target_shape(text), final_batch_rows(numerical), feature_columns(numerical), bytes_per_feature_element(numerical), bytes_per_target_element(numerical), feature_bytes(numerical), target_bytes(numerical), input_estimate_bytes(numerical), peak_allocated_tensor_bytes(numerical), budget_bytes(numerical), budget_interpretation(text), completed_examples(numerical), elapsed_seconds(numerical), throughput_examples_per_second(numerical), minimum_throughput(numerical), completed(categorical), eligible(categorical), selected(categorical), peak_reset_before_trial(categorical), measurement_boundary(text)
   [50,"full (50, 20); final (5, 20)","full (50,); final (5,)",5,20,4,4,4000,200,4200,18000,30000,"peak allocated tensor bytes, not total GPU usage",1005,2.0,502.5,400,true,true,false,true,"reset before bounded CUDA trial; inspect peak after completion; same task and synchronized elapsed-time boundarie
   [100,"full (100, 20); final (5, 20)","full (100,); final (5,)",5,20,4,4,8000,400,8400,26000,30000,"peak allocated tensor bytes, not total GPU usage",1005,1.25,804.0,400,true,true,true,true,"reset before bounded CUDA trial; inspect peak after completion; same task and synchronized elapsed-time bounda
   [200,"full (200, 20); final (5, 20)","full (200,); final (5,)",5,20,4,4,16000,800,16800,46000,30000,"peak allocated tensor bytes, not total GPU usage",1005,1.0,1005.0,400,true,false,false,true,"reset before bounded CUDA trial; inspect peak after completion; same task and synchronized elapsed-time bo

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjust training batch size to fit available memory; Choose CPU or GPU capacity for a bounded training workload; Choose inference batching under latency constraints; Configure bounded prediction-worker concurrency on an existing runtime; Configure replica scaling to right-size serving capacity under a service objective; Convert an ML notebook prototype into a repeatable executable training script with an explicit entry point; Diagnose training memory exhaustion; Enforce prediction-service authentication on an existing platform; Evaluate the frozen selected model and threshold against the baseline on the protected test set; Execute a bounded managed custom-model training job on an existing platform; Expose model readiness checks before admitting prediction traffic; Freeze and identify a traceable dataset snapshot for reproducible training; Gate pipeline execution on dataset-quality tests; Implement batch inference over a bounded dataset; Implement online prediction using the fitted preprocessing and model; Instrument prediction-service availability, errors and latency; Load-test a prediction endpoint against tail-latency and sustainable-throughput objectives; Package a versioned mode

## LESSON, in learner order

### s01 · explainer · Place models and tensors on the correct compute device
Understand — 
(intro) An accelerator label does not establish placement. Verify availability and the devices of the model, features and targets. ⟦A:tb1⟧
(mechanism) Check torch.cuda.is_available() before selecting torch.device("cuda"); otherwise use the supported CPU device. Move the model with model.to(device) and each feature and target tensor with tensor.to(device). Inspect parameter and minibatch devices, then check the declared placement with a bounded forward/backward fixture. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Assert valid, boundary and failure predicates; false predicates raise AssertionError in ordinary non-optimized execution. Only for the authorized supplied VM, gcloud compute instances start INSTANCE --zone=ZONE and gcloud compute instances stop INSTANCE --zone=ZONE change lifecycle state. Wait and inspect the result. gcloud compute ssh INSTANCE --zone=ZONE connects to the running authorized VM for the workload. ⟦A.f4 A.f5 A.f6 A:tb3⟧
[BEFORE_AFTER] Lifecycle status and tensor placement are separate checks. Required sequence (not an observed run): Initial stopped state → running state after authorized start → verified stopped state after workload
  before:
[CODE python]
import torch
from torch import nn
model = nn.Linear(2, 1)
features = torch.tensor([[1., 2.], [3., 4.]])
targets = torch.tensor([[1.], [2.]])
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
features = features.to(device)  # Model and targets have not yet been moved.
before_devices = ([p.device for p in model.parameters()], features.device, targets.device)
before_same_device = all(p.device == features.device == targets.device
                         for p in model.parameters())
# CPU fallback may already align them; inspect rather than assume a mismatch.
  annotations: []
  after:
[CODE python]
model = model.to(device)
features = features.to(device)
targets = targets.to(device)
after_devices = ([p.device for p in model.parameters()], features.device, targets.device)
same_device = (all(p.device == features.device == targets.device for p in model.parameters()) and features.device.type == device.type)
assert same_device
model.zero_grad()
outputs = model(features)
loss = nn.MSELoss()(outputs, targets)
loss.backward()
bounded_execution_ok = (outputs.shape == targets.shape
                        and loss.shape == torch.Size([])
                        and bool(torch.isfinite(loss))
                        and all(p.grad is not None and bool(torch.isfinite(p.grad).all())
                                for p in model.parameters()))
assert bounded_execution_ok
  annotations: []

### s02 · explainer · Apply and verify
Understand — 
(mechanism) gcloud compute instances describe INSTANCE --zone=ZONE checks identity and status before and after the authorized action. After the bounded workload, stop that instance, wait for completion and verify its stopped state. ⟦A.f7 A.f8 A:tb4⟧

### s03 · explainer · Tensor placement and authorized lifecycle checks
Understand — 
(example) The authorized lifecycle procedure and tensor placement are separate checks. Inspect instance identity and state before acting. Select CUDA only after checking availability, otherwise record the supported CPU path. Move and inspect the model, features and targets together; moving only features is insufficient. Check the bounded forward/backward fixture. After the workload, stop the authorized instance, wait and verify its state. Record actual placement rather than copying the intended hardware label. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A:tb5⟧

### s04 · explainer · A distinction to keep
Understand — 
(misconception) A running VM does not prove tensor placement. Verify availability, compatible devices and the bounded fixture; stop and verify the authorized VM afterward. ⟦A.f1 A.f2 A.f3 A.f8 A:tb6⟧

### s05 · check · Judge device placement
Check your judgement — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s06 · hands_on · Review device placement
Review the evidence — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s07 · explainer · Adjust training batch size to fit available memory
Understand — 
(intro) A larger batch may improve throughput but must satisfy the declared memory bound. Input bytes are only an estimate. ⟦B:tb1⟧
(mechanism) Training memory includes other live allocations; larger batches ordinarily require more activation storage. Change only DataLoader batch_size, keeping alignment and the task fixed. For each CUDA trial, reset_peak_memory_stats() before the workload and inspect torch.cuda.max_memory_allocated() afterward for peak allocated tensor bytes. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) That peak does not cover every component of GPU usage: use the quantity governed by the supplied budget. Compare completed work per elapsed time among eligible sizes. Estimate features as batch_rows × feature_columns × bytes_per_feature_element, add targets under their own dtype, and compare the estimate with the measured peak. ⟦B.f4 B.f5 B.f6 B:tb3⟧
[TABLE ds.batch_size_trials cols=['batch_size', 'actual_feature_shape', 'actual_target_shape', 'final_batch_rows', 'feature_columns', 'bytes_per_feature_element', 'bytes_per_target_element', 'feature_bytes', 'target_bytes', 'input_estimate_bytes', 'peak_allocated_tensor_bytes', 'budget_bytes', 'budget_interpretation', 'completed_examples', 'elapsed_seconds', 'throughput_examples_per_second', 'minimum_throughput', 'completed', 'eligible', 'selected', 'peak_reset_before_trial', 'measurement_boundary'] ] caption: Controlled batch-size comparison

### s08 · explainer · Batch-size trials against the declared memory bound
Understand — 
(example) Inspect the registered batch-size trials rather than equating feature-plus-target bytes with total training memory. Keep the task, alignment and measurement protocol fixed. Reset each CUDA trial’s peak before measuring; otherwise an earlier peak can contaminate the comparison. Record actual batch shapes, including the partial final batch, with completed examples and elapsed time. Higher throughput does not rescue a setting outside the declared memory bound. Select only among settings meeting the supplied requirements. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B:tb4⟧

### s09 · explainer · A distinction to keep
Understand — 
(misconception) Allocated-tensor peak is not total GPU usage. Input-byte estimates omit other live allocations; eligibility must follow the declared measured-memory scope. ⟦B.f1 B.f4 B.f6 B:tb5⟧

### s10 · check · Judge training batch sizing
Check your judgement — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s11 · hands_on · Review training batch sizing
Review the evidence — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s12 · explainer · Diagnose training memory exhaustion
Understand — 
(intro) Locate the failure: distinguish occupied tensors, reserved storage and retained graphs. ⟦C:tb1⟧
(mechanism) CUDA memory_allocated measures tensor-occupied memory; memory_reserved includes caching-allocator storage. Inspect peak allocated and reserved memory and the failure point. Graph-connected saved tensors can retain graph memory; use detached or scalar diagnostics when gradients through saved values are unnecessary. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) empty_cache releases unused cache, not storage occupied by live tensors. Test one supported change, such as smaller batches or removing an unnecessary graph reference, on the same bounded workload; verify completion and peak. Count each parameter, gradient, activation and batch matrix as element_count × element_width, summing simultaneously live allocations rather than inputs alone. ⟦C.f4 C.f5 C.f6 C:tb3⟧
[SIDE_BY_SIDE] A correction is supported only by same-workload completion and the measured peak comparison; input bytes alone are insufficient. left_label: Illustrative failed accounting | right_label: Illustrative one-factor correction
  left:
[DIAGRAM: Illustrative failed allocation record — measurements not supplied] nodes=['Failure location: supplied failing operation', 'Current allocated / peak allocated: measurement fields; tensor-occupied memory', 'Current reserved / peak reserved: measurement fields; allocator storage', 'Simultaneously live parameters: Linear(20, 10): weights 200 elements; bias 10 elements; parameter reference (200+10)×4=840 bytes', 'Simultaneously live gradients: separate element_count × element_width field', 'Simultaneously live activations: separate element_count × element_width field', 'Simultaneously live batch allocations: separate feature and target fields', 'One changed factor: baseline retained graph-connected diagnostics', 'Completion / declared bound: retain failing baseline record'] edges=[('node0', 'node1', None), ('node1', 'node2', None), ('node2', 'node3', None), ('node3', 'node4', None), ('node4', 'node5', None), ('node5', 'node6', None), ('node6', 'node7', None), ('node7', 'node8', None)] alt: Illustrative failed allocation record — measurements not supplied: Failure location: supplied failing operation; Current allocated / peak allocated: measurement fields; tensor-occupied memory; Current reserved / peak reserved: measurement fields; allocator storage; Simultaneously live parameters: Linear(20, 10): weights 200 elements; bias 10 elements; parameter reference (200+10)×4=840 bytes; Simultaneously live gradients: separate element_count × element_width field; Simultaneously live activations: separate element_count × element_width field; Simultaneously live batch allocations: separate feature and target fields; One changed factor: baseline retained graph-connected diagnostics; Completion / declared bound: retain failing baseline record
  right:
[DIAGRAM: Illustrative corrected allocation record — measurements not supplied] nodes=['Failure location on identical rerun: record whether workload completes', 'Current allocated / peak allocated: measurement fields; tensor-occupied memory', 'Current reserved / peak reserved: measurement fields; allocator storage', 'Simultaneously live parameters: Linear(20, 10): weights 200 elements; bias 10 elements; parameter reference (200+10)×4=840 bytes', 'Simultaneously live gradients: separate element_count × element_width field', 'Simultaneously live activations: separate element_count × element_width field', 'Simultaneously live batch allocations: separate feature and target fields', 'One changed factor: scalar or detached diagnostics where gradient connection is unnecessary', 'Completion predicate: same_workload_completed and measured_peak_allocated <= declared_bound; compare corrected and failed measured peaks'] edges=[('node0', 'node1', None), ('node1', 'node2', None), ('node2', 'node3', None), ('node3', 'node4', None), ('node4', 'node5', None), ('node5', 'node6', None), ('node6', 'node7', None), ('node7', 'node8', None)] alt: Illustrative corrected allocation record — measurements not supplied: Failure location on identical rerun: record whether workload completes; Current allocated / peak allocated: measurement fields; tensor-occupied memory; Current reserved / peak reserved: measurement fields; allocator storage; Simultaneously live parameters: Linear(20, 10): weights 200 elements; bias 10 elements; parameter reference (200+10)×4=840 bytes; Simultaneously live gradients: separate element_count × element_width field; Simultaneously live activations: separate element_count × element_width field; Simultaneously live batch allocations: separate feature and target fields; One changed factor: scalar or detached diagnostics where gradient connection is unnecessary; Completion predicate: same_workload_completed and measured_peak_allocated <= declared_bound; compare corrected and failed measured peaks

### s13 · explainer · Apply and verify
Understand — 
(mechanism) For a linear layer with widths F and H, weights contain F × H elements and bias contains H. These counts support the parameter-allocation reference. ⟦C.f7 C:tb4⟧

### s14 · explainer · Live allocations: parameters are not total memory
Understand — 
(example) Use the supplied linear-layer widths to count weight and bias elements separately. Apply each allocation’s element width, then include simultaneously live gradients, activations and batch matrices. At the reproduced failure, inspect allocated/reserved evidence and saved graph-connected diagnostics. Test one supported correction on the same bounded workload and compare completion and measured peak with the failed reference. Do not sum every tensor ever created or treat a smaller successful task as the same comparison. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C.f7 C:tb5⟧

### s15 · explainer · A distinction to keep
Understand — 
(misconception) empty_cache cannot release live tensor storage. Reserved differs from allocated, and the input matrix alone does not explain training memory. ⟦C.f1 C.f4 C.f6 C:tb6⟧

### s16 · check · Judge training memory diagnosis
Check your judgement — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s17 · hands_on · Review training memory diagnosis
Review the evidence — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s18 · recap · Take the contract with you
Keep the essentials — 
(takeaway) Verify availability, all devices and authorized lifecycle completion. ⟦A.f1 A.f2 A.f3 A.f8 A:tb2 A:tb4 A:tb5 A:tb6⟧
(takeaway) Choose eligible throughput using the budget’s measured-memory scope. ⟦B.f4 B.f5 B:tb3 B:tb4 B:tb5⟧
(takeaway) Simultaneously live allocations and verify one correction. ⟦C.f5 C.f6 C:tb3 C:tb5 C:tb6⟧
[UP NEXT] Profile training compute and data-loading bottlenecks: Next: Profile training compute and data-loading bottlenecks.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the evidence from the assumption
(mechanism) Check torch.cuda.is_available() before choosing torch.device("cuda"); otherwise select the supported CPU device. ⟦A.f1 A:tb2⟧
(misconception) For the same supplied task: A running accelerator does not prove that targets moved with features. ⟦A.f1 A:tb2⟧
### r02 · Separate the evidence from the assumption
(mechanism) Move the model with model.to(device) and every input and target tensor with tensor.to(device) so operations use compatible device placement. ⟦A.f2 A:tb2⟧
(mechanism) Inspect the model parameters’ device and both minibatch tensor devices, and run a bounded forward/backward fixture to check the declared placement. ⟦A.f3 A:tb2⟧
(mechanism) Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution. ⟦A.f4 A:tb3⟧
(mechanism) For an authorized supplied Compute Engine VM, gcloud compute instances start INSTANCE --zone=ZONE and gcloud compute instances stop INSTANCE --zone=ZONE change its lifecycle state; wait for the operation and inspect the resulting state. ⟦A.f5 A:tb3⟧
(mechanism) Connect to the running authorized VM with gcloud compute ssh INSTANCE --zone=ZONE to execute the workload. ⟦A.f6 A:tb3⟧
(mechanism) Use gcloud compute instances describe INSTANCE --zone=ZONE to inspect the instance status and identity before and after the authorized lifecycle action. ⟦A.f7 A:tb4⟧
(mechanism) Stop the authorized instance after the bounded workload with gcloud compute instances stop INSTANCE --zone=ZONE, wait for completion and verify its stopped state. ⟦A.f8 A:tb4⟧
(misconception) For the same supplied task: A running accelerator does not prove that targets moved with features. ⟦A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A:tb2 A:tb3 A:tb4⟧
### r03 · Separate the evidence from the assumption
(mechanism) A reported allocated-tensor peak does not include every component of GPU usage; compare the supplied budget with the memory quantity it actually governs. ⟦B.f4 B:tb3⟧
(mechanism) Compare completed work per elapsed time for the eligible batch sizes and choose a size within the measured memory bound. ⟦B.f5 B:tb3⟧
(misconception) For the same supplied task: Higher throughput cannot rescue an ineligible measured peak. ⟦B.f4 B.f5 B:tb3⟧
### r04 · Separate the evidence from the assumption
(mechanism) Training memory includes live tensors and other allocations; larger minibatches ordinarily require more activation storage, so input element bytes alone do not define peak training memory. ⟦B.f1 B:tb2⟧
(mechanism) Vary only the declared batch_size of the DataLoader for the comparison, preserving observation alignment and the supplied training task. ⟦B.f2 B:tb2⟧
(mechanism) For a CUDA trial, reset_peak_memory_stats() before the measured workload and inspect torch.cuda.max_memory_allocated() afterward to obtain peak allocated tensor bytes. ⟦B.f3 B:tb2⟧
(mechanism) A reported allocated-tensor peak does not include every component of GPU usage; compare the supplied budget with the memory quantity it actually governs. ⟦B.f4 B:tb3⟧
(mechanism) Compare completed work per elapsed time for the eligible batch sizes and choose a size within the measured memory bound. ⟦B.f5 B:tb3⟧
(mechanism) Estimate the matrix-shaped minibatch allocation as batch_rows × feature_columns × bytes_per_feature_element, add the target allocation under its dtype, and compare this estimate with the actual observed peak. ⟦B.f6 B:tb3⟧
(misconception) For the same supplied task: Higher throughput cannot rescue an ineligible measured peak. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B:tb2 B:tb3⟧
### r05 · Separate the evidence from the assumption
(mechanism) Retaining tensors attached to computation graphs can retain graph memory; use detached/scalar diagnostic values when gradients through those saved values are not needed. ⟦C.f3 C:tb2⟧
(misconception) For the same supplied task: Unused cache can be released; live tensor storage cannot be freed by empty_cache. ⟦C.f3 C:tb2⟧
### r06 · Separate the evidence from the assumption
(mechanism) CUDA memory_allocated reports tensor-occupied memory, while memory_reserved includes storage held by the caching allocator; distinguish them when locating exhaustion. ⟦C.f1 C:tb2⟧
(mechanism) Inspect the workload’s peak allocated and reserved memory and the point of failure before attributing the failure to the input batch alone. ⟦C.f2 C:tb2⟧
(mechanism) empty_cache releases unused cached memory for other uses but cannot free storage occupied by live tensors. ⟦C.f4 C:tb3⟧
(mechanism) Change one supported factor, such as reducing minibatch size or removing an unnecessary retained graph reference, and verify completion and the measured peak on the same bounded workload. ⟦C.f5 C:tb3⟧
(mechanism) Account for each parameter, gradient, activation and batch matrix as element_count × element_width, then sum simultaneously live allocations rather than only the input matrix. ⟦C.f6 C:tb3⟧
(mechanism) For a linear layer with input width F and output width H, the weight matrix has F × H elements and its bias has H, supporting the parameter-allocation reference. ⟦C.f7 C:tb4⟧
(misconception) For the same supplied task: Unused cache can be released; live tensor storage cannot be freed by empty_cache. ⟦C.f1 C.f2 C.f4 C.f5 C.f6 C.f7 C:tb2 C:tb3 C:tb4⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again

=========

# EVALUATOR PACKET — Profile and Choose Training Hardware (mle.tile.049_050)
Tile summary: Review bottleneck attribution, matched timing and hardware cost evidence.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.training_bottleneck_profiling — Profile training compute and data-loading bottlenecks
B = mle.training_hardware_selection — Choose CPU or GPU capacity for a bounded training workload

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (mle.training_bottleneck_profiling)   objective: Profile a bounded training workload and verify one bottleneck-oriented improvement.
A.f1: Wrap the measured computation in the PyTorch profiler context and mark data-loading and model-computation regions with record_function labels.   [sources: pytorch_learn_basics#../profiler.html — Profiling your PyTorch Module]
A.f2: Inspect key_averages().table(...) or the trace to attribute elapsed operator and labeled-region work to the observed bottleneck.   [sources: pytorch_learn_basics#../profiler.html — Profiling your PyTorch Module]
A.f3: Warm up the workload before comparing steady-state execution and remove profiler overhead when making the final unprofiled timing comparison.   [sources: pytorch_learn_basics#../profiler.html — Profiling your PyTorch Module]
A.f4: CUDA work is asynchronous, so CPU clock timings require synchronization at the measurement boundaries to include completed accelerator work.   [sources: pytorch_learn_basics#https://docs.pytorch.org/docs/2.15/notes/cuda.html — Memory management; Asynchronous execution]
A.f5: Change one supported bottleneck factor and compare the same bounded workload again rather than inferring improvement only from a code change.   [sources: pytorch_learn_basics#../profiler.html — Profiling your PyTorch Module]
A.f6: Inspect CPU and memory measurements and running process state during the profiled interval, using docker stats and docker top for a containerized run, to distinguish resource limits from stage timing evidence.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/stats/ — Description; Examples]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Profile and Choose Training Hardware.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.minibatch_training_loop, mle.dataset_minibatch_loader, mle.device_placement. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Implement a learner-defined Python function, with learner-written imports, that profiles a short bounded order-training run within the supplied runtime scaffolding. Warm up the workload, label loading and model-computation regions, inspect stage and operator timings alongside same-window CPU, memory and process evidence, isolate the suspected limiting stage, and test one supported change using a matched unprofiled timing comparison.  SUCCESS: Identify loading, transfer or model computation as the dominant limiting stage using profiler attribution and supporting process evidence. Reproduce the suspected limitation and report whether one isolated, supported change improves the same bounded workload, with warm-up, profiler overhead and CUDA completion handled correctly.
ASSESSMENT ANCHOR: localize_loading_compute_or_transfer_bottleneck facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_steady_state_timing_from_measurement_artifacts facts=['f3', 'f4']
ASSESSMENT ANCHOR: corroborate_stage_attribution_with_process_resource_evidence facts=['f6']
ASSESSMENT ANCHOR: verify_dominant_stage_diagnosis_with_one_factor_comparison facts=['f5']

## SOURCE FACTS — B (mle.training_hardware_selection)   objective: Choose between authorized CPU/GPU instances using matched runtime, memory and billing evidence.
B.f1: CPU and accelerator execution require the model and minibatches to be placed on the selected device, with accelerator availability checked first.   [sources: pytorch_learn_basics#tensorqs_tutorial.html — Initializing a Tensor; Attributes of a Tensor; Operations on Tensors]
B.f2: Benchmark the same bounded workload and task quality requirements on the compared devices, including relevant data movement and warm-up in the declared measurement interpretation.   [sources: pytorch_learn_basics#../profiler.html — Profiling your PyTorch Module]
B.f3: A running VM is billed for compute usage; stopping it ends compute billing but can leave persistent disk and other charges.   [sources: google_mlops_pipelines#https://cloud.google.com/compute/docs/instances/instance-lifecycle — Instance states; Billing]
B.f4: Estimate compute execution cost from the measured runtime and the applicable supplied rate, retaining the billing scope rather than assuming utilization alone is cost.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/billing/docs/how-to/reports — View your billing reports and cost trends]
B.f5: For an authorized supplied Compute Engine VM, gcloud compute instances start INSTANCE --zone=ZONE and gcloud compute instances stop INSTANCE --zone=ZONE change its lifecycle state; wait for the operation and inspect the resulting state.   [sources: google_mlops_pipelines#https://cloud.google.com/compute/docs/instances/stop-start-instance — Stop an instance; Start an instance]
B.f6: Connect to the running authorized VM with gcloud compute ssh INSTANCE --zone=ZONE to execute the workload.   [sources: google_mlops_pipelines#https://cloud.google.com/compute/docs/connect/standard-ssh — Connect to VMs]
B.f7: Stop the authorized supplied VM when the bounded training measurement finishes, then verify it is stopped and retain the measured runtime/cost record.   [sources: google_mlops_pipelines#https://cloud.google.com/compute/docs/instances/stop-start-instance — Stop an instance; Start an instance]
B.f8: Use gcloud compute instances describe INSTANCE --zone=ZONE to inspect the instance status and identity before and after the authorized lifecycle action.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/sdk/gcloud/reference/compute/instances/describe — DESCRIPTION; EXAMPLES]
B.f9: Record observed memory and whether each CPU/GPU instance option completes the same bounded matrix workload within its fixed limits.   [sources: numpy_user_guide#reference/generated/numpy.ndarray.nbytes.html]
B.f10: After benchmarking both authorized options, stop both and verify their resulting lifecycle states; use measured lifecycle durations in the billing calculation.   [sources: google_mlops_pipelines#https://cloud.google.com/compute/docs/instances/stop-start-instance — Stop an instance; Start an instance]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Profile and Choose Training Hardware.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.numpy_dtype_selection. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Inspect, start and connect to the two supplied authorized CPU/GPU instances. Benchmark the same bounded matrix-shaped training workload on each, recording device availability and placement, observed memory, completion, task quality and runtime under the declared data-movement and warm-up interpretation. Stop both instances, verify their states, and choose feasible capacity using the fixed memory, time and cost limits and supplied billing scope.  SUCCESS: Both options have comparable workload records and verified stopped states. The capacity decision checks completion, task quality, observed memory and time against the fixed limits, distinguishes execution cost from lifecycle-billed compute cost, and acknowledges any continuing disk or other charges.
ASSESSMENT ANCHOR: establish_a_matched_device_benchmark facts=['f1', 'f2']
ASSESSMENT ANCHOR: choose_feasible_capacity_under_memory_time_and_cost_limits facts=['f2', 'f4', 'f9', 'f10']
ASSESSMENT ANCHOR: start_inspect_and_connect_to_authorized_instances facts=['f5', 'f6', 'f8']
ASSESSMENT ANCHOR: verify_both_instances_stopped_and_retain_billing_evidence facts=['f3', 'f7', 'f8', 'f10']

## DATA ASSETS USED
ds.hardware_comparison: CPU and accelerator cost comparison — columns: option(categorical), model_device(categorical), feature_device(categorical), target_device(categorical), completed(categorical), task_quality_requirement_met(categorical), observed_memory_bytes(numerical), memory_limit_bytes(numerical), execution_seconds(numerical), lifecycle_seconds(numerical), rate_per_second(numerical), execution_compute_cost(numerical), lifecycle_compute_cost(numerical), billing_scope(text), stopped_state_verified(categorical), final_instance_state(categorical), remaining_charge_note(text)
   ["CPU","cpu","cpu","cpu",true,true,24000,30000,60.0,90,0.01,0.6,0.9,"currency units per second; simplified compute-only rate",true,"TERMINATED","persistent disk and other charges may remain"]
   ["accelerator","cuda","cuda","cuda",true,true,28000,30000,20.0,50,0.04,0.8,2.0,"currency units per second; simplified compute-only rate",true,"TERMINATED","persistent disk and other charges may remain"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Block release promotion when model acceptance gates fail; Choose CPU or GPU capacity for a bounded training workload; Choose inference batching under latency constraints; Configure bounded prediction-worker concurrency on an existing runtime; Configure replica scaling to right-size serving capacity under a service objective; Convert an ML notebook prototype into a repeatable executable training script with an explicit entry point; Enforce prediction-service authentication on an existing platform; Evaluate the frozen selected model and threshold against the baseline on the protected test set; Execute a bounded managed custom-model training job on an existing platform; Expose model readiness checks before admitting prediction traffic; Freeze and identify a traceable dataset snapshot for reproducible training; Gate pipeline execution on dataset-quality tests; Implement batch inference over a bounded dataset; Implement online prediction using the fitted preprocessing and model; Instrument prediction-service availability, errors and latency; Load-test a prediction endpoint against tail-latency and sustainable-throughput objectives; Package a versioned model with fitted preprocessing and

## LESSON, in learner order

### s01 · explainer · Profile training compute and data-loading bottlenecks
Understand — 
(intro) Duration shows slowness, not attribution. Separate loading and computation before choosing a supported bottleneck change. ⟦A:tb1⟧
(mechanism) Use the PyTorch profiler context and record_function labels around loading and model computation. Inspect key_averages().table(...) or the trace for operator and labeled-region attribution. Warm up before steady-state comparison; exclude profiler overhead from the final unprofiled timing. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) CUDA is asynchronous: synchronize CPU-clock measurement boundaries to include completed accelerator work. Change one supported factor and compare the same bounded workload again. Inspect CPU, memory and process state in that interval; docker stats and docker top support a containerized run’s resource evidence, distinct from stage timing. ⟦A.f4 A.f5 A.f6 A:tb3⟧
[SIDE_BY_SIDE] If loading dominates the trace, test one supported loading factor; accept improvement only from the matched unprofiled timing comparison. left_label: Illustrative baseline attribution and timing | right_label: Illustrative single-change comparison
  left:
[DIAGRAM: Illustrative baseline evidence fields — no observations supplied] nodes=['Warm-up completed', 'Profile attribution fields: loading; transfer; model computation (distinct labeled regions)', 'Same-window resource fields: CPU utilization; memory; process state (docker stats / docker top)', 'Baseline unprofiled elapsed time: measurement field', 'No profiler in final timing', 'CUDA synchronized before and after the timed workload', 'Timing comparison fields: baseline window and elapsed time; changed window and elapsed time; same bounded work', 'Acceptance predicate: changed unprofiled elapsed time < baseline unprofiled elapsed time under matched boundaries'] edges=[('node0', 'node1', None), ('node1', 'node2', None), ('node2', 'node3', None), ('node3', 'node4', None), ('node4', 'node5', None), ('node5', 'node6', None), ('node6', 'node7', None)] alt: Illustrative baseline evidence fields — no observations supplied: Warm-up completed; Profile attribution fields: loading; transfer; model computation (distinct labeled regions); Same-window resource fields: CPU utilization; memory; process state (docker stats / docker top); Baseline unprofiled elapsed time: measurement field; No profiler in final timing; CUDA synchronized before and after the timed workload; Timing comparison fields: baseline window and elapsed time; changed window and elapsed time; same bounded work; Acceptance predicate: changed unprofiled elapsed time < baseline unprofiled elapsed time under matched boundaries
  right:
[DIAGRAM: Illustrative one-factor-change evidence fields — no observations supplied] nodes=['Warm-up completed', 'Profile attribution fields: loading; transfer; model computation (distinct labeled regions)', 'Same-window resource fields: CPU utilization; memory; process state (docker stats / docker top)', 'One supported loading-factor change: name the single factor; matched workload held fixed', 'No profiler in final timing', 'CUDA synchronized before and after the timed workload', 'Timing comparison fields: baseline window and elapsed time; changed window and elapsed time; same bounded work', 'Acceptance predicate: changed unprofiled elapsed time < baseline unprofiled elapsed time under matched boundaries'] edges=[('node0', 'node1', None), ('node1', 'node2', None), ('node2', 'node3', None), ('node3', 'node4', None), ('node4', 'node5', None), ('node5', 'node6', None), ('node6', 'node7', None)] alt: Illustrative one-factor-change evidence fields — no observations supplied: Warm-up completed; Profile attribution fields: loading; transfer; model computation (distinct labeled regions); Same-window resource fields: CPU utilization; memory; process state (docker stats / docker top); One supported loading-factor change: name the single factor; matched workload held fixed; No profiler in final timing; CUDA synchronized before and after the timed workload; Timing comparison fields: baseline window and elapsed time; changed window and elapsed time; same bounded work; Acceptance predicate: changed unprofiled elapsed time < baseline unprofiled elapsed time under matched boundaries

### s02 · explainer · Loading attribution versus unprofiled improvement
Understand — 
(example) Keep attribution and final timing separate. If the labeled trace implicates loading, test one supported loading factor rather than changing model computation by assumption. Inspect CPU, memory and process state in the same window. Compare the identical bounded workload after warm-up without profiler overhead for the final elapsed-time comparison. Synchronize accelerator boundaries. Labels must enclose their intended work, not blend loading, computation and setup into an uninterpretable interval. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A:tb4⟧

### s03 · explainer · A distinction to keep
Understand — 
(misconception) A code change is not measured improvement. Control asynchronous completion, warm-up, profiler overhead and timing boundaries in the matched comparison. ⟦A.f3 A.f4 A.f5 A:tb5⟧

### s04 · check · Judge training bottleneck profiling
Check your judgement — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s05 · hands_on · Review training bottleneck profiling
Review the evidence — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s06 · explainer · Choose CPU or GPU capacity for a bounded training workload
Understand — 
(intro) Compare CPU and accelerator options on matched work, quality, memory and billing scope, not utilization alone. ⟦B:tb1⟧
(mechanism) Check accelerator availability and place the model and minibatches on the selected device. Benchmark the same bounded workload and quality requirements, retaining the declared treatment of data movement and warm-up. Running VMs incur compute billing; stopping compute can leave persistent-disk and other charges. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Estimate compute execution cost using measured runtime and the supplied rate, with its billing scope. For authorized supplied VMs only, use gcloud compute instances start INSTANCE --zone=ZONE or stop INSTANCE --zone=ZONE; wait and inspect the resulting state. Connect to a running authorized VM with gcloud compute ssh INSTANCE --zone=ZONE. ⟦B.f4 B.f5 B.f6 B:tb3⟧
[SIDE_BY_SIDE] Execution cost and lifecycle billing differ. left_label: Matched option records | right_label: Lifecycle and billing scope
  left:
[TABLE ds.hardware_comparison cols=['option', 'model_device', 'feature_device', 'target_device', 'completed', 'task_quality_requirement_met', 'observed_memory_bytes', 'memory_limit_bytes', 'execution_seconds', 'lifecycle_seconds', 'rate_per_second', 'execution_compute_cost', 'lifecycle_compute_cost', 'billing_scope', 'stopped_state_verified', 'final_instance_state', 'remaining_charge_note'] ] caption: CPU and accelerator cost comparison
  right:
[DIAGRAM: Authorized lifecycle] nodes=['Authorized identity and initial status', 'Start; wait; inspect; connect', 'Same bounded task, placement, quality and memory', 'Retain execution and lifecycle durations', 'Stop both; wait; verify both states'] edges=[('node0', 'node1', None), ('node1', 'node2', None), ('node2', 'node3', None), ('node3', 'node4', None)] alt: Authorized lifecycle: Authorized identity and initial status leads to Stop both; wait; verify both states

### s07 · explainer · Choose CPU or GPU capacity for a bounded training workload
Understand — 
(mechanism) After the measurement, stop the authorized VM, verify its stopped state and retain runtime/cost evidence. gcloud compute instances describe INSTANCE --zone=ZONE checks identity and status before and after actions. Record memory and completion of the same bounded matrix workload against each option’s fixed limits. ⟦B.f7 B.f8 B.f9 B:tb4⟧
(mechanism) After both authorized benchmarks, stop both instances and verify their states. Use measured lifecycle durations for billing. ⟦B.f10 B:tb5⟧

### s08 · explainer · CPU versus accelerator: runtime and lifecycle cost
Understand — 
(example) Compare the registered CPU and accelerator records under the same workload, quality and memory limits. Execution cost uses the supplied rate and bounded execution duration; billing interpretation also needs lifecycle duration. Retain the declared movement and warm-up scope. Start, connect to and inspect only authorized instances; stop both after measurement and verify the result. A faster option can still cost more, and persistent-disk or other charges can remain after compute stops. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B.f8 B.f9 B.f10 B:tb6⟧
(misconception) Faster is not automatically cheaper or eligible. Stopping compute does not end every charge; preserve billing scope. ⟦B.f2 B.f3 B.f4 B:tb7⟧

### s09 · check · Judge training hardware selection
Check your judgement — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s10 · hands_on · Review training hardware selection
Review the evidence — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s11 · recap · Take the contract with you
Keep the essentials — 
(takeaway) Separate attribution from synchronized, unprofiled matched timing. ⟦A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Compare matched quality, memory, runtime and scoped cost. ⟦B.f2 B.f4 B.f9 B:tb2 B:tb3 B:tb4 B:tb6 B:tb7⟧
[UP NEXT] Task specific pretrained weight fine tuning: Next: Task specific pretrained weight fine tuning.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the evidence from the assumption
(mechanism) Warm up the workload before comparing steady-state execution and remove profiler overhead when making the final unprofiled timing comparison. ⟦A.f3 A:tb2⟧
(mechanism) CUDA work is asynchronous, so CPU clock timings require synchronization at the measurement boundaries to include completed accelerator work. ⟦A.f4 A:tb3⟧
(misconception) For the same supplied task: A trace attributes work; final unprofiled timing tests improvement. ⟦A.f3 A.f4 A:tb2 A:tb3⟧
### r02 · Separate the evidence from the assumption
(mechanism) Wrap the measured computation in the PyTorch profiler context and mark data-loading and model-computation regions with record_function labels. ⟦A.f1 A:tb2⟧
(mechanism) Inspect key_averages().table(...) or the trace to attribute elapsed operator and labeled-region work to the observed bottleneck. ⟦A.f2 A:tb2⟧
(mechanism) Change one supported bottleneck factor and compare the same bounded workload again rather than inferring improvement only from a code change. ⟦A.f5 A:tb3⟧
(mechanism) Inspect CPU and memory measurements and running process state during the profiled interval, using docker stats and docker top for a containerized run, to distinguish resource limits from stage timing evidence. ⟦A.f6 A:tb3⟧
(misconception) For the same supplied task: A trace attributes work; final unprofiled timing tests improvement. ⟦A.f1 A.f2 A.f5 A.f6 A:tb2 A:tb3⟧
### r03 · Separate the evidence from the assumption
(mechanism) A running VM is billed for compute usage; stopping it ends compute billing but can leave persistent disk and other charges. ⟦B.f3 B:tb2⟧
(mechanism) Stop the authorized supplied VM when the bounded training measurement finishes, then verify it is stopped and retain the measured runtime/cost record. ⟦B.f7 B:tb4⟧
(mechanism) Use gcloud compute instances describe INSTANCE --zone=ZONE to inspect the instance status and identity before and after the authorized lifecycle action. ⟦B.f8 B:tb4⟧
(mechanism) After benchmarking both authorized options, stop both and verify their resulting lifecycle states; use measured lifecycle durations in the billing calculation. ⟦B.f10 B:tb5⟧
(misconception) For the same supplied task: Faster completion can cost more; compute stopping need not end disk charges. ⟦B.f10 B.f3 B.f7 B.f8 B:tb2 B:tb4 B:tb5⟧
### r04 · Separate the evidence from the assumption
(mechanism) CPU and accelerator execution require the model and minibatches to be placed on the selected device, with accelerator availability checked first. ⟦B.f1 B:tb2⟧
(mechanism) Benchmark the same bounded workload and task quality requirements on the compared devices, including relevant data movement and warm-up in the declared measurement interpretation. ⟦B.f2 B:tb2⟧
(mechanism) A running VM is billed for compute usage; stopping it ends compute billing but can leave persistent disk and other charges. ⟦B.f3 B:tb2⟧
(mechanism) Estimate compute execution cost from the measured runtime and the applicable supplied rate, retaining the billing scope rather than assuming utilization alone is cost. ⟦B.f4 B:tb3⟧
(mechanism) For an authorized supplied Compute Engine VM, gcloud compute instances start INSTANCE --zone=ZONE and gcloud compute instances stop INSTANCE --zone=ZONE change its lifecycle state; wait for the operation and inspect the resulting state. ⟦B.f5 B:tb3⟧
(mechanism) Connect to the running authorized VM with gcloud compute ssh INSTANCE --zone=ZONE to execute the workload. ⟦B.f6 B:tb3⟧
(mechanism) Stop the authorized supplied VM when the bounded training measurement finishes, then verify it is stopped and retain the measured runtime/cost record. ⟦B.f7 B:tb4⟧
(mechanism) Use gcloud compute instances describe INSTANCE --zone=ZONE to inspect the instance status and identity before and after the authorized lifecycle action. ⟦B.f8 B:tb4⟧
(mechanism) Record observed memory and whether each CPU/GPU instance option completes the same bounded matrix workload within its fixed limits. ⟦B.f9 B:tb4⟧
(mechanism) After benchmarking both authorized options, stop both and verify their resulting lifecycle states; use measured lifecycle durations in the billing calculation. ⟦B.f10 B:tb5⟧
(misconception) For the same supplied task: Faster completion can cost more; compute stopping need not end disk charges. ⟦B.f1 B.f10 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B.f8 B.f9 B:tb2 B:tb3 B:tb4 B:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again

=========

# EVALUATOR PACKET — Fine-Tune Task-Specific Weights (mle.tile.051_051)
Tile summary: Review classifier-only adaptation and matched-validation error-cost comparisons.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = ml.task_specific_pretrained_weight_fine_tuning — Task specific pretrained weight fine tuning

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (ml.task_specific_pretrained_weight_fine_tuning)   objective: Adapt a pretrained supervised task head and verify its contract, learning signal and validation result.
A.f1: For the bounded ViT image-classification adaptation, import torch; from torch import nn; from transformers import AutoImageProcessor, ViTForImageClassification, TrainingArguments, Trainer; load model = ViTForImageClassification.from_pretrained(checkpoint) from the supplied compatible pretrained ViT checkpoint, retaining its original label mapping for the pretrained baseline before replacing the task head.   [sources: huggingface_transformers_docs#https://huggingface.co/docs/transformers/model_doc/vit — ViTForImageClassification — Examples; ViTImageProcessor.preprocess, huggingface_transformers_docs#https://raw.githubusercontent.com/huggingface/transformers/main/src/transformers/models/vit/modeling_vit.py — ViTForImageClassification.__init__ — vit and classifier]
A.f2: Load processor = AutoImageProcessor.from_pretrained(checkpoint); inputs = processor(images, return_tensors="pt") produces pixel_values for the model, whose logits are obtained with model(**inputs).logits; preprocess the training and validation images with that same checkpoint processor rather than substituting an unrelated representation.   [sources: huggingface_transformers_docs#https://huggingface.co/docs/transformers/tasks/image_classification — Preprocess; Train; Inference, huggingface_transformers_docs#https://huggingface.co/docs/transformers/model_doc/vit — ViTForImageClassification — Examples; ViTImageProcessor.preprocess]
A.f3: With the supplied preprocessed training/validation datasets and image collator, construct args = TrainingArguments(output_dir=output_dir, num_train_epochs=epochs, per_device_train_batch_size=batch_size, learning_rate=learning_rate, eval_strategy="epoch", remove_unused_columns=False); trainer = Trainer(model=model, args=args, train_dataset=train_dataset, eval_dataset=validation_dataset, data_collator=data_collator, processing_class=processor); trainer.train() executes the bounded supervised adaptation.   [sources: huggingface_transformers_docs#https://huggingface.co/docs/transformers/tasks/image_classification — Preprocess; Train; Inference]
A.f4: For classifier-only supervised adaptation, freeze the existing parameters and construct the task head:
for parameter in model.parameters():
    parameter.requires_grad = False
model.classifier = nn.Linear(model.config.hidden_size, num_labels)
model.num_labels = model.config.num_labels = num_labels
model.config.id2label = id2label
model.config.label2id = label2id
Newly constructed head parameters are trainable by default; verify head weights change and frozen backbone parameter values do not.   [sources: huggingface_transformers_docs#https://raw.githubusercontent.com/huggingface/transformers/main/src/transformers/models/vit/modeling_vit.py — ViTForImageClassification.__init__ — vit and classifier, pytorch_learn_basics#https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html — ConvNet as fixed feature extractor, huggingface_transformers_docs#https://huggingface.co/docs/transformers/tasks/image_classification — Preprocess; Train; Inference]
A.f5: Evaluate the fine-tuned task predictions on the same validation cohort as the frozen pretrained output reference, without constructing an application or using protected test data.   [sources: huggingface_transformers_docs#https://huggingface.co/docs/transformers/tasks/image_classification — Preprocess; Train; Inference]
A.f6: For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
A.f7: With zero cost for correct predictions and supplied deployment class probabilities, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
A.f8: Do not use protected test observations to fit preprocessing, choose a model or tune its settings; doing so leaks information into the chosen system.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.2 Data leakage]
A.f9: For a class-index task head, verify logits shape (N, C) and target shape (N,) with long indices in [0, C), where C matches the task label mapping.   [sources: pytorch_learn_basics#https://docs.pytorch.org/docs/2.15/generated/torch.nn.CrossEntropyLoss.html — Shape; Parameters; Examples]
A.f10: Within the adaptation run, compute the task loss, backpropagate it and compare a selected head gradient with the chain-rule reference before claiming the task head receives the intended supervised update.   [sources: pytorch_learn_basics#autogradqs_tutorial.html — Tensors, Functions and Computational graph; Computing Gradients]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Fine-Tune Task-Specific Weights.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.minibatch_training_loop, mle.weight_persistence, mle.training_evaluation_modes, mle.task_metric_selection, mle.neural_model_definition, mle.task_loss_selection. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Implement a learner-defined Python function with learner-written imports that adapts the classifier of one supplied small pretrained ViT model. Preserve the original label mapping and frozen pretrained validation reference, reuse the checkpoint processor, verify task-head shapes and a selected loss gradient against the chain rule, and compare conditional error rates and expected error cost on the same validation cohort.  SUCCESS: The function completes the bounded supervised run using the supplied scaffolding. It demonstrates changed head weights and unchanged frozen backbone values, valid task-label shapes and indices, and agreement between a selected head gradient and its chain-rule reference. Its returned comparison reports FPR, FNR and expected error cost for both models, handles undefined conditional rates explicitly, and justifies improvement or non-improvement without accessing protected test observations.
ASSESSMENT ANCHOR: establish_matched_pretrained_validation_reference facts=['f1', 'f2', 'f5', 'f8']
ASSESSMENT ANCHOR: verify_classifier_only_supervised_adaptation facts=['f3', 'f4']
ASSESSMENT ANCHOR: verify_task_head_shapes_and_chain_rule_gradient facts=['f9', 'f10']
ASSESSMENT ANCHOR: compute_conditional_validation_error_and_expected_cost facts=['f6', 'f7']
ASSESSMENT ANCHOR: justify_adapted_model_improvement_or_non_improvement facts=['f5', 'f6', 'f7', 'f8']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Block release promotion when model acceptance gates fail; Choose inference batching under latency constraints; Configure bounded prediction-worker concurrency on an existing runtime; Configure replica scaling to right-size serving capacity under a service objective; Convert an ML notebook prototype into a repeatable executable training script with an explicit entry point; Define artifact dependencies between ML pipeline stages; Enforce prediction-service authentication on an existing platform; Evaluate the frozen selected model and threshold against the baseline on the protected test set; Execute a bounded managed custom-model training job on an existing platform; Expose model readiness checks before admitting prediction traffic; Freeze and identify a traceable dataset snapshot for reproducible training; Gate pipeline execution on dataset-quality tests; Implement batch inference over a bounded dataset; Implement online prediction using the fitted preprocessing and model; Instrument prediction-service availability, errors and latency; Load-test a prediction endpoint against tail-latency and sustainable-throughput objectives; Package a versioned model with fitted preprocessing and in

## LESSON, in learner order

### s01 · explainer · Task specific pretrained weight fine tuning
Understand — 
(intro) Adapt the supplied ViT image classifier in a bounded supervised task. Keep original pretrained and task label mappings distinct. ⟦A:tb1⟧
(mechanism) Import torch, nn from torch, and AutoImageProcessor, ViTForImageClassification, TrainingArguments and Trainer from transformers. Load the compatible checkpoint with ViTForImageClassification.from_pretrained(checkpoint); retain its original label mapping for the baseline. Load AutoImageProcessor.from_pretrained(checkpoint). Processing images with return_tensors="pt" gives pixel_values; model(**inputs).logits gives logits. Use this processor for both training and validation. With supplied preprocessed datasets and collator, configure TrainingArguments with output_dir, num_train_epochs, per_device_train_batch_size and learning_rate as declared, eval_strategy="epoch" and remove_unused_columns=False. Configure Trainer with model, args, train_dataset, eval_dataset=validation_dataset, data_collator and processing_class=processor. Trainer.train() performs the bounded adaptation. ⟦A.f1 A.f2 A.f3 A:tb2⟧
[SIDE_BY_SIDE] Illustrative comparison checks: accept only under the declared cost-based rule on matched validation evidence, not head change alone. left_label: Frozen pretrained reference | right_label: Adapted task model
  left:
[DIAGRAM: Illustrative frozen pretrained comparison checks] nodes=['Original id2label / label2id: retain supplied checkpoint mappings', 'Frozen pretrained validation outputs: retain original mapping; same checkpoint processor and fixed validation cohort', 'Task label comparison: original mapping versus supplied two-class task id2label / label2id', 'Matched-validation baseline fields: FP, TN, FN, TP; no protected test observations', 'FPR = FP/(FP+TN); FNR = FN/(FN+TP)', 'Empty conditioning group: rate undefined', 'Expected cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN; correct-prediction cost zero'] edges=[('node0', 'node1', None), ('node1', 'node2', None), ('node2', 'node3', None), ('node3', 'node4', None), ('node4', 'node5', None), ('node5', 'node6', None)] alt: Illustrative frozen pretrained comparison checks: Original id2label / label2id: retain supplied checkpoint mappings; Frozen pretrained validation outputs: retain original mapping; same checkpoint processor and fixed validation cohort; Task label comparison: original mapping versus supplied two-class task id2label / label2id; Matched-validation baseline fields: FP, TN, FN, TP; no protected test observations; FPR = FP/(FP+TN); FNR = FN/(FN+TP); Empty conditioning group: rate undefined; Expected cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN; correct-prediction cost zero
  right:
[DIAGRAM: Illustrative adapted task comparison checks — not observed results] nodes=['Task label maps: two labels; indices 0 and 1; distinct from original mapping', 'Task logits (N, 2); long targets (N,) in [0, 2); N is common batch length', 'Selected head gradient: computed after fresh loss.backward(); reference from same-loss chain rule', 'Gradient predicate: shape matches and allclose(computed_selected_head_gradient, reference_selected_head_gradient, declared_rtol, declared_atol)', 'Changed-head predicate: at least one head entry differs from cloned pre-adaptation value', 'Unchanged-backbone predicate: every frozen backbone entry equals its cloned pre-adaptation value', 'Matched-validation adapted fields: FP, TN, FN, TP → FPR, FNR → expected cost using the same supplied probabilities and error costs', 'Empty conditioning group: rate undefined', 'Declared cost-based acceptance predicate: defined rates and supplied_acceptance_rule(adapted_expected_cost, frozen_expected_cost); report improvement or non-improvement'] edges=[('node0', 'node1', None), ('node1', 'node2', None), ('node2', 'node3', None), ('node3', 'node4', None), ('node4', 'node5', None), ('node5', 'node6', None), ('node6', 'node7', None), ('node7', 'node8', None)] alt: Illustrative adapted task comparison checks — not observed results: Task label maps: two labels; indices 0 and 1; distinct from original mapping; Task logits (N, 2); long targets (N,) in [0, 2); N is common batch length; Selected head gradient: computed after fresh loss.backward(); reference from same-loss chain rule; Gradient predicate: shape matches and allclose(computed_selected_head_gradient, reference_selected_head_gradient, declared_rtol, declared_atol); Changed-head predicate: at least one head entry differs from cloned pre-adaptation value; Unchanged-backbone predicate: every frozen backbone entry equals its cloned pre-adaptation value; Matched-validation adapted fields: FP, TN, FN, TP → FPR, FNR → expected cost using the same supplied probabilities and error costs; Empty conditioning group: rate undefined; Declared cost-based acceptance predicate: defined rates and supplied_acceptance_rule(adapted_expected_cost, frozen_expected_cost); report improvement or non-improvement

### s02 · explainer · Apply and verify
Understand — 
(mechanism) For classifier-only adaptation, set existing parameters’ requires_grad=False, then replace model.classifier with nn.Linear(model.config.hidden_size, num_labels). Update model.num_labels, config.num_labels, config.id2label and config.label2id to the task mapping. New head parameters are trainable by default. Verify changed head weights and unchanged frozen backbone. Compare task predictions with the frozen pretrained reference on the same validation cohort, without an application or protected-test data. Binary FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) conditions on actual positives. Empty conditioning groups give undefined rates. ⟦A.f4 A.f5 A.f6 A:tb3⟧

### s03 · explainer · Task specific pretrained weight fine tuning
Understand — 
(mechanism) With zero cost for correct predictions, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN, using supplied deployment probabilities. Keep protected tests out of preprocessing fit, model choice and tuning to prevent leakage. For a class-index head, verify logits (N, C), targets (N,) and long indices in [0, C), with C matching the task map. ⟦A.f7 A.f8 A.f9 A:tb4⟧
(mechanism) Compute task loss, backpropagate and compare a selected head gradient with the chain-rule reference inside adaptation before claiming the intended supervised update. ⟦A.f10 A:tb5⟧

### s04 · explainer · Classifier-only adaptation: gradients and validation cost
Understand — 
(example) For the supplied task images, retain the original baseline mapping and checkpoint processor. Freeze existing parameters before replacing the head; update both label maps and class-count settings. Verify class-index shapes and dtype, a selected head gradient, changed head weights and unchanged backbone. Compare against the frozen reference on the same validation cohort under fixed cost and acceptance rules. Keep protected tests outside adaptation and selection. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A.f9 A.f10 A:tb6⟧
(misconception) Freezing existing parameters does not freeze a new head. Changed weights alone do not verify target mapping or matched validation. ⟦A.f4 A.f5 A.f9 A:tb7⟧

### s05 · check · Judge task specific pretrained weight fine tuning
Check your judgement — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s06 · hands_on · Review task specific pretrained weight fine tuning
Review the evidence — Read the supplied excerpts in this step and decide which satisfy the declared task contract and which are defective or unsafe.

### s07 · recap · Take the contract with you
Keep the essentials — 
(takeaway) Verify task mapping, supervised head updates and matched validation. ⟦A.f4 A.f5 A.f9 A.f10 A:tb3 A:tb4 A:tb5 A:tb6 A:tb7⟧
[UP NEXT] Convert an ML notebook prototype into a repeatable executable training script with an explicit entry point: Next: Convert an ML notebook prototype into a repeatable executable training script with an explicit entry point.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Separate the evidence from the assumption
(mechanism) Evaluate the fine-tuned task predictions on the same validation cohort as the frozen pretrained output reference, without constructing an application or using protected test data. ⟦A.f5 A:tb3⟧
(mechanism) For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate. ⟦A.f6 A:tb3⟧
(mechanism) With zero cost for correct predictions and supplied deployment class probabilities, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. ⟦A.f7 A:tb4⟧
(mechanism) Do not use protected test observations to fit preprocessing, choose a model or tune its settings; doing so leaks information into the chosen system. ⟦A.f8 A:tb4⟧
(misconception) For the same supplied task: Frozen existing parameters do not freeze the newly constructed task head. ⟦A.f5 A.f6 A.f7 A.f8 A:tb3 A:tb4⟧
### r02 · Separate the evidence from the assumption
(mechanism) For the bounded ViT image-classification adaptation, import torch; from torch import nn; from transformers import AutoImageProcessor, ViTForImageClassification, TrainingArguments, Trainer; load model = ViTForImageClassification.from_pretrained(checkpoint) from the supplied compatible pretrained ViT checkpoint, retaining its original label mapping for the pretrained baseline before replacing the task head. ⟦A.f1 A:tb2⟧
(mechanism) Load processor = AutoImageProcessor.from_pretrained(checkpoint); inputs = processor(images, return_tensors="pt") produces pixel_values for the model, whose logits are obtained with model(**inputs).logits; preprocess the training and validation images with that same checkpoint processor rather than substituting an unrelated representation. ⟦A.f2 A:tb2⟧
(mechanism) With the supplied preprocessed training/validation datasets and image collator, construct args = TrainingArguments(output_dir=output_dir, num_train_epochs=epochs, per_device_train_batch_size=batch_size, learning_rate=learning_rate, eval_strategy="epoch", remove_unused_columns=False); trainer = Trainer(model=model, args=args, train_dataset=train_dataset, eval_dataset=validation_dataset, data_collator=data_collator, processing_class=processor); trainer.train() executes the bounded supervised adaptation. ⟦A.f3 A:tb2⟧
(mechanism) For classifier-only supervised adaptation, freeze the existing parameters and construct the task head:
for parameter in model.parameters():
    parameter.requires_grad = False
model.classifier = nn.Linear(model.config.hidden_size, num_labels)
model.num_labels = model.config.num_labels = num_labels
model.config.id2label = id2label
model.config.label2id = label2id
Newly constructed head parameters are trainable by default; verify head weights change and frozen backbone parameter values do not. ⟦A.f4 A:tb3⟧
(mechanism) Evaluate the fine-tuned task predictions on the same validation cohort as the frozen pretrained output reference, without constructing an application or using protected test data. ⟦A.f5 A:tb3⟧
(mechanism) For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate. ⟦A.f6 A:tb3⟧
(mechanism) With zero cost for correct predictions and supplied deployment class probabilities, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. ⟦A.f7 A:tb4⟧
(mechanism) Do not use protected test observations to fit preprocessing, choose a model or tune its settings; doing so leaks information into the chosen system. ⟦A.f8 A:tb4⟧
(mechanism) For a class-index task head, verify logits shape (N, C) and target shape (N,) with long indices in [0, C), where C matches the task label mapping. ⟦A.f9 A:tb4⟧
(mechanism) Within the adaptation run, compute the task loss, backpropagate it and compare a selected head gradient with the chain-rule reference before claiming the task head receives the intended supervised update. ⟦A.f10 A:tb5⟧
(misconception) For the same supplied task: Frozen existing parameters do not freeze the newly constructed task head. ⟦A.f1 A.f10 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A.f9 A:tb2 A:tb3 A:tb4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Try the distinction again
· remediation_steps.eyebrow: Try the distinction again