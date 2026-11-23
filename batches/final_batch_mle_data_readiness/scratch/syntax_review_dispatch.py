import json
from pathlib import Path
b=Path('batches/final_batch_mle.region.data_readiness');p=b/'interactions.json';d=json.loads(p.read_text())
def scaffold(ix,text):
 starter=ix['public']['workspace']['files'][0];starter['content']=starter['content'].replace('# TODO:',text+'\n# TODO:')
 sol=ix['grading']['solution_files'][0];pos=sol['content'].index('\n\n');sol['content']=sol['content'][:pos]+'\n'+text+sol['content'][pos:]
for tile in d['tiles']:
 for item in tile['interactions']:
  ix=item['interaction']
  if ix['type']!='code_exercise':continue
  short=ix['anchors'][0].split('#')[0].split('.',1)[1];sol=ix['grading']['solution_files'][0];c=sol['content']
  if short=='numpy_dtype_selection':
   # Numerical reference dimensions are supplied scaffolding; the learner casts and compares scalars.
   scaffold(ix,'row_count = reference.shape[0]\ncolumn_count = reference.shape[1]\nboundary_count = boundaries.shape[1]')
   c=sol['content'].replace('range(reference.shape[0])','range(row_count)').replace('range(reference.shape[1])','range(column_count)').replace('range(boundaries.shape[1])','range(boundary_count)')
  if short=='training_fitted_imputation':
   c=c.replace('before = imputer.statistics_.copy()','before = imputer.statistics_[0]')
   c=c.replace('assert np.array_equal(before, imputer.statistics_)','assert before == imputer.statistics_[0]')
   c=c.replace('assert np.allclose(boundary_result[0], mean)','assert boundary_result[0][0] == mean[0]')
   c=c.replace('assert np.allclose(result[2][1],result[0])','assert result[2][1][0] == result[0][0]')
   c=c.replace("assert not np.allclose(result[2][1],FIXTURES['incorrect_replacement'])","assert result[2][1][0] != FIXTURES['incorrect_replacement'][0][0]")
  if short=='training_fitted_scaling':
   c=c.replace('scaler.mean_.copy()','np.array(scaler.mean_)').replace('scaler.scale_.copy()','np.array(scaler.scale_)')
   c=c.replace('np.allclose(scaler.mean_,before_mean)','np.array_equal(scaler.mean_,before_mean)').replace('np.allclose(scaler.scale_,before_scale)','np.array_equal(scaler.scale_,before_scale)')
   c=c.replace('assert np.allclose(validation[0][0],(X_validation[0][0]-mean[0])/std[0])','assert validation[0][0] == (X_validation[0][0]-mean[0])/std[0]')
   c=c.replace("np.allclose(result[2],FIXTURES['incorrect_transformed_fixture'])","np.array_equal(result[2],FIXTURES['incorrect_transformed_fixture'])")
  if short=='categorical_encoding':
   c=c.replace('assert np.all(unseen == 0)','assert unseen[0][0] == 0 and unseen[0][1] == 0').replace('assert np.all(missing == 0)','assert missing[0][0] == 0 and missing[0][1] == 0')
  if short=='dataset_cleaning_policy':
   c=c.replace("assert len(result['cleaned']) == 3","assert result['cleaned'][2]['observation_id'] == records[4]['observation_id']")
   c=c.replace("assert len(result['report']) == 3","assert result['report'][2]['observation_id'] == records[3]['observation_id']")
  if short=='label_integrity':
   c=c.replace('len(repeated_obs) == 0 and len(repeated_labels) == 0 and len(missing) == 0 and len(orphaned) == 0 and len(bad) == 0','not repeated_obs and not repeated_labels and not missing and not orphaned and not bad')
  if short=='deployment_matched_splits':
   # All split and proportion computations are learner-authored loops/comprehensions in the allowed grammar.
   c=c.replace("train_groups = {row['customer_group'] for row in train}\n    val_groups = {row['customer_group'] for row in validation}\n    assert not (train_groups & val_groups)","for row in train:\n        assert row['customer_group'] not in [v['customer_group'] for v in validation]")
   c=c.replace("train_share = sum([row['target'] for row in train]) / len(train)\n    val_share = sum([row['target'] for row in validation]) / len(validation)","train_count = 0\n    train_positive = 0\n    for row in train:\n        train_count += 1\n        train_positive += row['target']\n    val_count = 0\n    val_positive = 0\n    for row in validation:\n        val_count += 1\n        val_positive += row['target']\n    train_share = train_positive / train_count\n    val_share = val_positive / val_count")
   c=c.replace("assert max([row['observation_timestamp'] for row in train]) < cutoff\n    assert min([row['observation_timestamp'] for row in validation]) >= cutoff", "for row in train:\n        assert row['observation_timestamp'] < cutoff\n    for row in validation:\n        assert cutoff <= row['observation_timestamp'] and row['observation_timestamp'] < end\n    train_count = 0\n    train_positive = 0\n    for row in train:\n        train_count += 1\n        train_positive += row['target']\n    val_count = 0\n    val_positive = 0\n    for row in validation:\n        val_count += 1\n        val_positive += row['target']")
   c=c.replace("sum([row['target'] for row in train])/len(train)",'train_positive/train_count').replace("sum([row['target'] for row in validation])/len(validation)",'val_positive/val_count')
  sol['content']=c
p.write_text(json.dumps(d,indent=2)+'\n')
