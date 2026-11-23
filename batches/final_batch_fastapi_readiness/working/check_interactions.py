import ast, collections, json, pathlib, re, subprocess
B=pathlib.Path('batches/final_batch_readiness')
x=json.loads((B/'interactions.json').read_text()); plans=json.loads((B/'tile_plans.json').read_text()); screens=json.loads((B/'screens.json').read_text()); g=json.loads((B/'inputs/path_glossary_bundle.json').read_text()); gm={b['context']['concept_id']:b for b in g['bundles']}; sm={t['tile_id']:t for t in screens['tiles']}
assert [t['tile_id'] for t in x['tiles']]==[t['tile_id'] for t in plans['tiles']]
counts=collections.Counter(); first=set(); pending=[]
for t,p in zip(x['tiles'],plans['tiles']):
 expected=[s for s in p['steps'] if s['type'] in ['check','hands_on']]
 assert [r['step_id'] for r in t['interactions']]==[s['step_id'] for s in expected]
 difficulty=[]
 for r,s in zip(t['interactions'],expected):
  ix=r['interaction'];counts[ix['type']]+=1
  assert ix['type']==s['planned_interaction_type']
  assert ix['anchors']==s['anchors']
  assert ix['standalone'] and 'the table above' not in ix['public']['prompt'].lower()
  assert ix['grading_mode']=='client'
  difficulty.append(['intro','core','stretch'].index(ix['difficulty']))
  for m in ix['measures']:
   a=next(a for a in gm[m['concept_id']]['assessment_anchors'] if a['capability']==m['capability'])
   assert m['fact_ids']==a['fact_ids'] and all('#' not in f for f in m['fact_ids'])
  cid=s['concept_ids'][0]
  if cid not in first:
   remediation=[a for a in sm[t['tile_id']]['remediation_steps'] if cid in a.get('concept_ids',[])]
   if remediation: assert ix['feedback']['remediation_step_id']==remediation[0]['step_id']
   first.add(cid)
  assert 1<=len(ix['feedback']['hints'])<=2
  if ix['type']=='choice':
   assert len(ix['grading']['correct_option_ids'])==1
   ids={o['option_id'] for o in ix['public']['options']}
   assert set(ix['grading']['correct_option_ids'])<=ids
   assert ids==set(ix['grading']['option_feedback'])
  else:
   assert 'hidden_checks' not in ix['grading'] and 'execution_provenance' not in ix['grading']
   live=gm[cid]['practice_anchor']['live_code']
   assert ix['public']['constraints']=={k:live[k] for k in ['allowed_syntax','blocked_syntax']}
   fs={f['path']:f for f in ix['public']['workspace']['files']}
   assert len([f for f in fs.values() if f['role']=='editable'])==1
   path=ix['public']['workspace']['entry'];solution=ix['grading']['solution_files'][0]
   assert solution['path']==path and solution['content']!=fs[path]['content']
   assert ix['grading']['tests']
   if ix['public']['runtime']['kind']=='bash':
    pending.append(r['step_id'])
    result=subprocess.run(['bash','-n'],input=solution['content'],text=True,capture_output=True)
    assert result.returncode==0,result.stderr
    for target,delimiter,content in re.findall(r"cat > '([^']+)' <<'([^']+)'\n(.*?)\n\2\n",solution['content'],re.S):
     if target.endswith('.py'):ast.parse(content)
   else:ast.parse(solution['content'])
 assert difficulty==sorted(difficulty)
report={'artifact':str(B/'interactions.json'),'tile_count':len(x['tiles']),'interaction_counts':dict(counts),'total_interactions':sum(counts.values()),'structural_checklist':'passed','manual_review':['Single defensible choice alternatives and misconception feedback reviewed against glossary facts.','Earlier-text-before-test checked by deterministic tile gate.','Practice success checks mapped to supplied fixtures; native commands retain real verification/storage boundaries rather than inventing proxies.','No data keys, hidden checks or execution provenance authored in interactions.json.','Expected values for pinned exercises computed from executed solution/native probe code or supplied fixture contracts; native commands remain unverified.','No standalone references to earlier screens; required files are included.','Starters differ from solutions; all Python syntax and shell syntax parse.','Release selection uses readonly phase scaffolding; timestamp task uses precomputed receiver-minus-delivery age to limit learner edits to the allowed comparison syntax.'],'limitations':{'native_runner_unavailable_steps':pending,'native_checks_executed_by_pack_gate':False}}
(B/'working/interactions_checklist.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
