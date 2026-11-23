import ast,json
from pathlib import Path
p=Path('batches/final_batch_persistence')
s=json.loads((p/'screens.json').read_text())
b={x['context']['concept_id']:x for x in json.loads((p/'inputs/path_glossary_bundle.json').read_text())['bundles']}
def response(c):
 syntax=next(x for x in b[c]['practice_anchor']['live_code']['allowed_syntax'] if 'JSONResponse(' in x)
 expr=ast.parse(syntax.removeprefix('return '),mode='eval').body
 return {x.arg:ast.literal_eval(x.value) for x in expr.keywords if x.arg=='content' or (x.arg=='status_code' and isinstance(x.value,ast.Constant))}
t=next(t for t in s['tiles'] if t['tile_id']=='tile_067')
steps={x['step_id']:x for x in t['steps']}
r=response('fastapi.domain_error_translation')
x=steps['tile_067.s05']['blocks'][0]
old='The fixture declares 409 for its recognized uniqueness conflict and the public reason order conflict.'
new=f'The fixture declares HTTP {r["status_code"]} with the fixed public body {json.dumps(r["content"])} for its recognized uniqueness conflict.'
assert x['text'].startswith(old)
x['text']=new+x['text'][len(old):]
x=next(x for x in steps['tile_067.s09']['blocks'] if x['type']=='code_walkthrough')
oldcode=x['code']
assert '    public_reason = choose_intended_public_reason(exception)\n' in oldcode
x['code']=oldcode.replace('    public_reason = choose_intended_public_reason(exception)\n','').replace("content={'reason': public_reason}", 'content='+json.dumps(response('fastapi.public_error_envelopes')['content']))
a=x['annotations'][1]
a['start_line']=6
a['end_line']=len(x['code'].splitlines())-1
a['text']='Use the fixed public envelope; preserve the recognized status and headers. Raw exception detail is not public content.'
(p/'screens.json').write_text(json.dumps(s,indent=2)+'\n')
print('tiles:',len(s['tiles']),'steps:',sum(len(t['steps']) for t in s['tiles']),'remediation:',sum(len(t.get('remediation_steps',[])) for t in s['tiles']))
