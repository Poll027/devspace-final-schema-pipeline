import copy,json
from pathlib import Path
p=Path('batches/final_batch_aws_devops.region.06_2/screens.json')
d=json.loads(p.read_text()); before=copy.deepcopy(d)
t=next(t for t in d['tiles'] if t['tile_id']=='aws_devops.tile.125')
parts=[
'Spreadsheet syntax for this worksheet: start a formula with =. C2 means column C, row 2. Subtract times with -, multiply with *, and use parentheses to group operations. Times are fractions of a day, so =ROUND((D2-C2)*1440,0) returns whole restoration minutes; =ROUND((C2-F2)*1440,0) returns whole data-gap minutes. ROUND(value,0) rounds to a whole number.',
'IF(test,"pass","fail") returns pass when the test is true and fail otherwise; <= means less than or equal to. Compare restoration minutes with H2 and data-gap minutes with K2 separately. For example, =IF(ROUND((D2-C2)*1440,0)<=H2,"pass","fail") returns the RTO conclusion.',
'Put literal text in double quotes and join text, cell values and calculated values with &: =A2&": RTO="&ROUND((D2-C2)*1440,0)&" minutes "&IF(ROUND((D2-C2)*1440,0)<=H2,"pass","fail"). Extend this row summary with "; RPO=" and the separately calculated gap and RPO conclusion. Build the second summary by changing row references from 2 to 3, then join the summaries with &" | "&. Keep the measurements calculated from timestamps, not copied from result columns.'
]
troubleshooting='If your result is rejected, check the leading =, quoted literal text, & joins, parentheses and commas. Then check that RTO uses D minus C and H, RPO uses C minus F and K, and the second summary uses row 3. Match the requested spaces, punctuation and separator.'
s=next(s for s in t['steps'] if s['step_id'].endswith('.s02'))
r=next(s for s in t['remediation_steps'] if s['step_id'].endswith('.r02'))
for step in (s,r):
 lineage=copy.deepcopy(step['blocks'][0]['lineage'])
 for text in parts+([troubleshooting] if step is r else []):
  assert len(text.split())<=90
  step['blocks'].append({'type':'prose','text':text,'role':'example','lineage':copy.deepcopy(lineage)})
# Only the two named steps may differ.
check=copy.deepcopy(d)
ct=next(t for t in check['tiles'] if t['tile_id']=='aws_devops.tile.125')
for seq,suffix,n in [('steps','.s02',len(parts)),('remediation_steps','.r02',len(parts)+1)]:
 step=next(s for s in ct[seq] if s['step_id'].endswith(suffix)); del step['blocks'][-n:]
assert check==before
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print('tiles',len(d['tiles']),'steps',sum(len(t['steps']) for t in d['tiles']),'remediation',sum(len(t.get('remediation_steps',[])) for t in d['tiles']))
print('Appended prose blocks:',2*len(parts)+1)
