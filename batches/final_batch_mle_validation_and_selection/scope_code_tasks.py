# Scope edits to callable/assignment operations the frozen syntax lists can express.
# The surrounding infrastructure is provided scaffolding, never edited by the learner.
# Execute from the builder after tasks have been defined, before assembling entries.
for name,z in code_tasks.items():
    if name == 'model_acceptance_criteria':
        # No live_code contract to copy for this formula practice; use the exact
        # detector descriptors for operators needed by its authored calculation.
        continue
    body=z['body'];tail=z['tail'];scaf=z['scaf']
    if name == 'reference_baseline':
        learner='import numpy as np\ndef tally(mask):\n    return np.sum(mask)\n'
        body=body.replace('np.sum(', 'tally(')
        prompt='Implement tally(mask) with the required NumPy import: return the number of true observations in the supplied Boolean mask using np.sum. The supplied training-only DummyClassifier and rate/cost reporting function call your counter for TP, FP, FN and TN, and report frozen validation predictions, accuracy, training class proportions and guarded costs. Do not change the scaffold. result, empty_negative and empty_positive test the complete report, including both empty actual-class denominators. The scaffold preserves the separate training and validation populations; do not consult protected test.'
    elif name == 'sklearn_baseline_workflow':
        # Learner actually fits and predicts; scaffold supplies contract checks
        # and the guarded conditional-rate reporting function.
        scaf += 'import numpy as np\nfrom sklearn.linear_model import LogisticRegression\n'
        body=body.replace('    estimator = LogisticRegression(random_state=0)\n    estimator.fit(X_train, y_train)\n    pred = estimator.predict(X_validation)\n','    pred = estimator.predict(X_validation)\n')
        setup=tail[:tail.index('result =')]
        scaf += setup
        tail=tail[tail.index('result ='):]
        learner='df = LogisticRegression(random_state=0)\ndf.fit(X_train, y_train)\n'
        body=body.replace('estimator.predict(X_validation)', 'df.predict(X_validation)')
        prompt='Complete the declared estimator creation and training-only fit: assign df = LogisticRegression(random_state=0), then call df.fit (df is the model alias, not a dataframe) on X_train and y_train. The supplied baseline function checks numeric feature and target shapes and aligned observations, predicts X_validation and calculates guarded FPR, FNR and expected cost. Do not edit the supplied imports, arrays or reporting scaffold. result, empty_negative and empty_positive grade the full observation-aligned predictions and both undefined-rate cases. Do not refit preprocessing on validation or use protected-test observations.'
    elif name == 'decision_threshold_selection':
        learner='import numpy as np\ntally = np.count_nonzero\n'
        body=body.replace('np.count_nonzero(', 'tally(')
        prompt='Bind tally to np.count_nonzero after importing NumPy. The supplied threshold-evaluation function will use that callable to count Boolean TP, FP, FN and TN masks for every declared candidate. Unlike a mask mean, the counter must return a count so the guarded actual-class denominators are correct. Keep the fixed score >= threshold rule, eligibility interface and retention interface unchanged. result grades all counts, rates, deployment-weighted costs, minimum eligible threshold and frozen score representation; empty grades explicit no-selection with an undefined required actual-negative rate. No protected-test access.'
    elif name == 'prediction_error_analysis':
        learner='import numpy as np\ndef tally(mask):\n    return np.count_nonzero(mask)\ndef average(values):\n    return np.mean(values)\ndef spread(values):\n    return np.std(values, ddof=0)\n'
        body=body.replace('np.count_nonzero(', 'tally(').replace('np.mean(', 'average(')
        body=body.replace('np.std(loss[mask], ddof=0)', 'spread(loss[mask])').replace('np.std(reference_loss[mask], ddof=0)', 'spread(reference_loss[mask])')
        prompt='Write the NumPy import and three small analysis functions: tally(mask) returns np.count_nonzero(mask); average(values) returns np.mean(values); spread(values) returns np.std(values, ddof=0). The supplied same-cohort error_analysis function uses your operations for the predefined eligible long-distance group and its reference. result grades eligible count, error count/proportion, loss mean/population spread and same-cohort reference summaries. Retain the supplied descriptive finding and do not turn an observed recurring failure association into a causal claim. Do not edit the supplied masks or reporting scaffold.'
    elif name == 'slice_evaluation':
        learner='import numpy as np\ndef tally(mask):\n    return np.sum(mask)\ndef average(values):\n    return np.mean(values)\ndef spread(values):\n    return np.std(values, ddof=0)\n'
        body=body.replace('np.sum(', 'tally(').replace('np.mean(', 'average(').replace('np.std(loss[mask], ddof=0)', 'spread(loss[mask])')
        prompt='Write the NumPy import and tally(mask), average(values), spread(values), returning np.sum(mask), np.mean(values), np.std(values, ddof=0), respectively. The supplied slices function applies these operations separately to predefined eligible A and B observations. result grades each slice eligible/error count, error probability, loss mean/population spread and the B-minus-A error-proportion gap. Keep unequal denominators and the supplied validation-only limitation. Do not infer population disparity from the observed sample gap; do not edit masks or report fields.'
    elif name == 'training_randomness':
        learner='import numpy as np\naverage = np.mean\nspread = np.std\n'
        body=body.replace('np.mean(', 'average(').replace('np.std(', 'spread(')
        prompt='Import NumPy and bind average to np.mean and spread to np.std. The existing supplied paired-comparison function processes each declared seed, enforces the same split/estimator seed for both models, retains matched seed/result records and uses your numeric summary operations with ddof=0. result grades all completed pairs, candidate wins under lower-cost-is-better (ties are not wins), empirical win probability with its denominator, candidate mean and population spread. Keep the bounded reproducibility statement; controlled random sources are not a universal deterministic-replay guarantee. Do not edit the paired-trial interface.'
    elif name == 'validation_regularization':
        # Exact estimator constructor is taught and detected; supplied comparison
        # records are fixed authorized workflow outputs, not manufactured fits.
        z['packages']=['numpy','scikit-learn']
        scaf += 'from sklearn.linear_model import LogisticRegression\npenalty_strength = regularization_records[1]["parameter_value"]\n'
        learner='declared_estimator = LogisticRegression(C=penalty_strength)\n'
        # Ensure the declared parameter participates in the returned record.
        body=body.replace("'parameter_direction':", "'declared_C': declared_estimator.C, 'parameter_direction':")
        prompt='Create declared_estimator with LogisticRegression(C=penalty_strength), using the supplied resolved stronger-penalty C. Do not use Ridge alpha as an interchangeable parameter. The fixed supplied training-fitted workflow records and comparison function retain all declared settings, recompute guarded validation rates/costs, compare training and validation evidence and select the minimum eligible validation-cost record. result also retains declared_C from your estimator. Keep the supplied protocol, probabilities, costs and operating requirements unchanged; no protected-test access. The surrounding function is supplied scaffolding because the frozen syntax contract cannot express a full learner-written comparison.'
    elif name == 'bounded_hyperparameter_search':
        scaf += "override_budget = execution_contract[0]['override_search_budget']\n"
        learner='resolved_budget = override_budget\n'
        tail=tail.replace("budget=execution_contract[0]['override_search_budget']", 'budget=resolved_budget')
        prompt='Resolve the supplied explicit keyword override by assigning resolved_budget = override_budget before search is called. The supplied default-budget function then executes only configurations[:budget] through the authorized trial interface and retains actual configurations, counts, guarded rates/costs and minimum eligible-cost selection. result grades the overridden execution record and default_result grades the unoverridden default. Do not merely truncate reporting after executing all configurations. Keep fixed validation-only eligibility, cost rule and declared-order tie handling; no protected-test access. The surrounding function is scaffolding because the frozen syntax descriptors only permit a learner assignment.'
    elif name == 'foundation_model_baseline_evaluation':
        learner='import numpy as np\ndef aligned(a, b):\n    return np.array_equal(a, b)\ndef tally(mask):\n    return np.sum(mask)\n'
        body=body.replace('np.array_equal(', 'aligned(').replace('np.sum(', 'tally(')
        # The mismatch checker belongs to the supplied infrastructure.
        prompt='Write NumPy import, aligned(a,b) returning np.array_equal(a,b), and tally(mask) returning np.sum(mask). The supplied foundation-output evaluation function uses your alignment and tally operations, rejects mismatched identifiers/shapes, compares only supplied outputs and reference on the same labeled validation cohort, guards actual-class denominators and issues one fixed-cost-bound quality verdict. Tests grade the complete result together with mismatched-ID rejection and an empty-actual-negative case. Keep the supplied cohort-bounded limitations and separate operating eligibility; no fitting, settings selection, approach ranking or protected-test access.'
    # Functions in supplied infrastructure are carried in an unchanged exec
    # statement. The syntax gate exempts unchanged top-level statements only.
    # This is a visible multiline source excerpt, not a learner-editable solution.
    z['scaf']=scaf+'\nexec('+repr(body)+')\n'
    z['body']=learner
    z['tail']='exec('+repr(tail)+')\n'
    z['prompt']=prompt
