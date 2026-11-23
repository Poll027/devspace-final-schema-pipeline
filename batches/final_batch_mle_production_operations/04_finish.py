import ast,json,pathlib,sys,collections
B=pathlib.Path('batches/final_batch_mle.region.production_operations');sys.path.insert(0,'00_FINAL_PIPELINE_CORE/scripts');from checkers import sandbox,pysyntax
D=json.load(open(B/'interactions.json'));R=json.load(open(B/'scenario_asset_registry.json'));A={a['asset_id']:a for a in R['assets']}
def replace_infra(ix,edit):
 for f in [ix['public']['workspace']['files'][0],ix['grading']['solution_files'][0]]:
  text=f['content'];node=next(n for n in ast.parse(text).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_fixture_support' for t in n.targets));old=ast.get_source_segment(text,node);new='_fixture_support = '+repr(edit(node.value.value));f['content']=text.replace(old,new,1)
for t in D['tiles']:
 for i,e in enumerate(t['interactions']):
  ix=e['interaction'];ix['difficulty']='intro' if i==0 else 'core' if i < len(t['interactions'])//2 else 'stretch'
  if ix['type']!='code_exercise':continue
  c=ix['measures'][0]['concept_id']
  if c=='mle.retrained_candidate_validation':
   def edit(s):
    s=s.replace('for identity_match in [True,False]:',"for promotion_identity in [r['registry_artifact_id'],r['registry_artifact_id']+'.different']:\n                identity_match = promotion_identity == r['registry_artifact_id']")
    s=s.replace("'promotion_identity_matches':identity_match","'promotion_identity':promotion_identity,'promotion_identity_matches':identity_match")
    return s
   replace_infra(ix,edit)
  if c=='mle.ml_incident_runbook':
   def edit(s):
    s=s.replace("before=self.data[0]; after=self.data[-1]", "before=self.data[0]; after=self.data[-1]\n        for row in [before,after]:\n            assert row['INSTANCE']==self.policy['INSTANCE'] and row['ZONE']==self.policy['ZONE'] and row['authorized_identity']==self.policy['authorized_identity'] and row['credential_review_pass']\n        assert before['fault_evidence'] and before['hypothesis_result']\n        assert after['instance_state']=='RUNNING' and after['process_state']=='running' and after['readiness'] and after['prediction_contract_pass']")
    return s
   replace_infra(ix,edit)
  if c=='mle.retraining_run_idempotency':
   for a in ['ds.trigger_events','ds.pipeline_stages']:ix['public']['workspace']['asset_mounts'].append({'asset_id':a,'mount_path':a.split('.')[1]+'.csv'})
   def edit(s):
    node=next(n for n in ast.parse(s).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SCHEMAS' for t in n.targets));schema=ast.literal_eval(node.value)
    for a in ['ds.trigger_events','ds.pipeline_stages']:schema[a.split('.')[1]]={co['name']:co['type'] for co in A[a]['columns']}
    s=s.replace(ast.get_source_segment(s,node),'SCHEMAS = '+repr(schema),1)
    s=s.replace("self.phase=6", """self.trigger_results=[]
        inventory=load('pipeline_stages')
        for event in load('trigger_events'):
            accepted=event['authorized'] and event['investigated'] and event['entry_stage']=='entry'
            quality=accepted and event['data_quality_pass']
            self.trigger_results.append({'event':event['event_id'],'entry':'accepted' if accepted else 'rejected','resolved_input':event['dataset_ref'] if accepted else None,'data_quality':'pass' if quality else 'blocked','train':quality,'evaluate':quality,'promote':quality and event['promotion_approved'],'credential_reference':'runtime references only; no credential values'})
            if not accepted or not event['data_quality_pass']:
                assert not self.trigger_results[-1]['train']
        self.config['stage_inventory']=inventory
        self.config['trigger_policy']={'entry':'authorization, investigation and intended immutable snapshot','required_failure':'fatal','separate_promotion_approval':True,'credential_reference':'runtime references only; no credential values'}
        with open('build.yaml','w') as f:yaml.safe_dump(self.config,f)
        with open('build.yaml') as f:loaded=yaml.safe_load(f)
        assert loaded==self.config
        self.phase=6""")
    s=s.replace("'source_trace_count':len(self.events)","'source_traces':self.events,'trigger_results':self.trigger_results")
    return s
   replace_infra(ix,edit)
   ix['public']['prompt']+=' Replay the supplied trigger events against the existing stage inventory: record accepted/rejected entry, resolved snapshot, fatal data-quality blocking and separate promotion approval; round-trip those policy fields too.'
  if c=='mle.ml_resource_utilization':
   def edit(s):return s.replace("'memory_std':memory_std}","'memory_std':memory_std,'cpu_count':count,'memory_count':len(memory),'interpretation':'descriptive utilization for this matched workload interval only'}")
   replace_infra(ix,edit)
  tables,_=sandbox._tables(R,ix['public']['workspace']['asset_mounts'],{},[])
  result=sandbox.node_run(sandbox._py_job('python',ix['public']['runtime']['packages'],[sandbox._py_script('solution','main.py',ix['grading']['solution_files'][0]['content'],sandbox._py_mounts(tables),[{'id':'report','kind':'expr','expr':'report'}])]),sandbox.RUNTIMES['python']['runner'])['results']['solution']
  if not result['ok']:raise RuntimeError((c,result))
  expected=result['probes']['report']['value'];ix['grading']['tests'][0]['spec']['expected']=expected
  shape='a record with top-level fields '+', '.join(expected.keys()) if isinstance(expected,dict) else 'a list of records with fields '+', '.join(expected[0].keys())
  ix['public']['prompt']+=' The graded variable is report: '+shape+'. Retain the supplied nested record structure and declared ordering.'
# Deterministic own mistakes-to-avoid assertions.
P=json.load(open(B/'tile_plans.json'));S=json.load(open(B/'screens.json'));G=json.load(open(B/'inputs/path_glossary_bundle.json'));g={x['context']['concept_id']:x for x in G['bundles']};counter=collections.Counter()
for t,plan in zip(D['tiles'],P['tiles']):
 expected=[s for s in plan['steps'] if s['type'] in ['check','hands_on']];assert [e['step_id'] for e in t['interactions']]==[s['step_id'] for s in expected]
 seen=set();rem=next(s for s in S['tiles'] if s['tile_id']==t['tile_id'])['remediation_steps']
 for e,s in zip(t['interactions'],expected):
  ix=e['interaction'];counter[ix['type']]+=1;assert ix['type']==s['planned_interaction_type'];assert ix['anchors']==s['anchors'];assert ix['standalone'];assert 'the table above' not in ix['public']['prompt'].lower()
  assert ix['feedback']['hints'] and len(ix['feedback']['hints'])<=2
  for m in ix['measures']:
   ga=next(a for a in g[m['concept_id']]['assessment_anchors'] if a['capability']==m['capability']);assert m['fact_ids']==ga['fact_ids'] and all('#' not in f for f in m['fact_ids'])
  c=s['concept_ids'][0]
  if c not in seen:
   target=next((r['step_id'] for r in rem if c in r['concept_ids']),None);assert ix['feedback'].get('remediation_step_id')==target
  seen.add(c)
  if ix['type']=='code_exercise':
   assert ix['public']['constraints']=={k:g[c]['practice_anchor']['live_code'][k] for k in ['allowed_syntax','blocked_syntax']}
   assert not any(k in ix['grading'] for k in ['execution_provenance','hidden_checks']);assert ix['public']['workspace']['files'][0]['content']!=ix['grading']['solution_files'][0]['content']
   assert not pysyntax.judge(ix['grading']['solution_files'][0]['content'],ix['public']['constraints']['allowed_syntax'],ix['public']['constraints']['blocked_syntax'],ix['public']['workspace']['files'][0]['content'])[0]
  elif ix['type']=='choice':assert len(ix['grading']['correct_option_ids'])==1 and all(o['option_id'] in ix['grading']['option_feedback'] for o in ix['public']['options'])
  else:assert len(ix['grading']['assignments'])==len(ix['public']['items'])
json.dump(D,open(B/'interactions.json','w'),indent=2,ensure_ascii=False)
json.dump({'tiles':len(D['tiles']),'interactions':sum(counter.values()),'by_type':dict(counter),'checklist':'plan/types, bare measures/glossary facts, standalone prompts, first-concept remediation, feedback/distractors/traps, verbatim syntax, incomplete starters, pinned-derived expected reports, narrow scope and success evidence reviewed'},open(B/'04_checklist.json','w'),indent=2)
print(counter)
