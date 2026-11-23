import json
from pathlib import Path
p=Path('batches/final_batch_mle.region.data_readiness/interactions.json');d=json.loads(p.read_text())
hints={
'000_000':['Identify what is available when the order is accepted; separate the target from the permitted inputs.'],
'001_003':['Check rank before indexing shape[1].','Compare scalar differences and element bytes separately.','Compare the transform with an independently computed reference and check its shape.'],
'004_006':['Distinguish writing the local record from assigning or displaying its text.','Account for every feature in a row when deriving the chunk limit.','Identify what each matrix axis represents before summarizing columns.'],
'007_008':['Check columns before dtypes and value bounds; keep runtime rejections separate from fixture checks.','Track accepted keys and compare retained and rejected IDs with the declared policy.'],
'009_011':['Use the sample total for sample shares, the target total for target shares, and each category’s target count for its inclusion rate.','Align labels by ID, not row position; compare the audit verdict with the expected fixture outcome.','Check group intersections and the inequalities at the time cutoff separately.'],
'012_015':['Save the fitted replacement statistic before transforming held-out data and compare it afterward.','Save mean_ and scale_ before transform and compare both afterward.','Use the stored category order to align expected output columns.','Check state reuse separately from normal, missing-value, and malformed-input outcomes.'],
'016_017':['Compare fitted inputs with permitted training fields, not with whichever inputs were selected.','Compare information availability with the recorded prediction boundary, including equality.'],
'018_018':['Keep credentials inside the authorized interface and check dictionary membership before retaining sample fields.']}
for t in d['tiles']:
 tile=t['tile_id'].replace('mle.tile.','')
 for x in t['interactions']:
  s=int(x['step_id'].split('.s')[1]);i=x['interaction']
  j=0
  if tile=='001_003':j=0 if s<9 else 1 if s<15 else 2
  if tile=='004_006':j=0 if s<10 else 1 if s<15 else 2
  if tile=='007_008':j=int(s>=9)
  if tile=='009_011':j=0 if s<10 else 1 if s<15 else 2
  if tile=='012_015':j=0 if s<10 else 1 if s<15 else 2 if s<20 else 3
  if tile=='016_017':j=int(s>=10)
  i['feedback']['hints']=[hints[tile][j]]
  if tile=='000_000' and s==6:
   old=i['public']['prompt']; record=old.split('Preserve the exact labels and text: ')[1]
   fields=record.split(' | ')
   scaffold='\n'.join('- '+f for f in fields)
   i['public']['prompt']='Complete the task fields and population-labeled calculations in one formula in E2. Choose each field’s value from the scaffold alternatives below, then join the completed fields with " | ". Use B2/C2 for all orders and B3/C3 for the specified zone, not typed proportions.\n\nTask-field choices (select the value that matches order-acceptance prediction):\n- prediction_unit: one order at acceptance / one zone\n- eligible_population: all 100 supplied accepted orders / specified-zone orders only\n- target_event: arrival more than 30 minutes after acceptance / distance\n- prediction_time: acceptance / eventual arrival\n- horizon: 30 minutes / unspecified\n- allowed_inputs: distance; promised delivery zone / eventual arrival time\n- excluded_input: eventual arrival time / distance\n\nReadable output scaffold (keep these field labels and exact selected text):\n'+scaffold
p.write_text(json.dumps(d,indent=2)+'\n')
