import json, re
from pathlib import Path
from collections import Counter
B=Path(__file__).parent
load=lambda f:json.loads((B/f).read_text())
p=load('tile_plans.json'); o=load('interactions.json'); s=load('screens.json'); g=load('inputs/path_glossary_bundle.json')
bundles={b['context']['concept_id']:b for b in g['bundles']}
counts=Counter(); item_count=0
for t in o['tiles']:
    pt=next(x for x in p['tiles'] if x['tile_id']==t['tile_id'])
    st=next(x for x in s['tiles'] if x['tile_id']==t['tile_id'])
    expected={x['step_id']:x for x in pt['steps'] if x['type'] in ('check','hands_on')}
    assert set(expected)=={x['step_id'] for x in t['interactions']}
    rem={x['step_id'] for x in st.get('remediation_steps',[])}
    for entry in t['interactions']:
        ix=entry['interaction']; ps=expected[entry['step_id']]; counts[ix['type']]+=1
        assert ix['type']==ps['planned_interaction_type'] and ix['anchors']==ps['anchors']
        assert ix['grading_mode']=='client'
        for m in ix['measures']:
            a=next(a for a in bundles[m['concept_id']]['assessment_anchors'] if a['capability']==m['capability'])
            assert m['fact_ids']==a['fact_ids'] and all('#' not in f for f in m['fact_ids'])
        assert 1<=len(ix['feedback']['hints'])<=2
        if 'remediation_step_id' in ix['feedback']:assert ix['feedback']['remediation_step_id'] in rem
        if ps['type']=='hands_on':assert ps['concept_ids'][0]+'#practice' in ix['anchors']
        if ix['type']=='choice':
            assert len(ix['grading']['correct_option_ids'])==1
            assert {x['option_id'] for x in ix['public']['options']}==set(ix['grading']['option_feedback'])
        else:
            assert set(ix['grading']['assignments'].values())=={'meets','violates'}
            assert {x['item_id'] for x in ix['public']['items']}==set(ix['grading']['item_feedback'])
            assert not any('source' in x for x in ix['public']['items']) # inspect-and-judge: authored inline evidence, not dataset classification
            assert 'asset_ref' not in ix['public'] and 'runtime' not in ix['public']
            prompt=ix['public']['prompt'].lower()
            assert not re.search(r'\b(workspace|readme|implement|submit|train|provision|write|produce)\b', prompt)
            item_count+=len(ix['public']['items'])
        assert 'table above' not in ix['public']['prompt'].lower()
report={'tiles':len(o['tiles']),'interactions':sum(counts.values()),'counts_by_type':dict(counts),'classification_items':item_count,'automated_checklist':'passed','manual_review':{'one_defensible_answer':'Each choice has one contract-consistent verdict; classification excerpts explicitly state their local requirement.','distractor_grounding':'Wrong options and trap items contrast glossary rules, with a reason for each.','taught_before_tested':'Earlier text mechanism and examples reviewed; deterministic gate verifies fact lineage.','practice_success':'Inline implementations and recorded acceptance outcomes cover the practice success criteria as inspect-and-judge tasks.','derived_values':'Registry trial, controller and hardware rows copied by script; selection computed from registered eligibility quantities; glossary numerical acceptance outcomes copied from source.','runtime_checks':'No executable interaction planned: SQL/Python expected-output, starter and syntax checks not applicable.','classification_sources':'Source and role_map are not used: all hands-on classifications use the explicit inspect-and-judge inline-evidence exemption.'}}
(B/'stage04_checklist.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
