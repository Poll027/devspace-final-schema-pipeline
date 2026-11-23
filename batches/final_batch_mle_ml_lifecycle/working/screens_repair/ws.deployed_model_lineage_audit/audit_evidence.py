import json, hashlib, subprocess, os
from pathlib import Path
from storage_sim import StorageClient, PreconditionFailed
load=lambda p:json.loads(Path(p).read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
def audit(c):
 checks={}; result={'checks':checks}; missing=[]
 def get(d,k,label):
  if k not in d: missing.append(label); return None
  return d[k]
 d=c['deployment']; a=c['approval']; r=get(c['registry'],d['registry_version'],'deployment -> registry')
 if r is None: return {'missing_links':missing,'verified':False,'checks':checks}
 checks['deployment -> registry artifact']=d['artifact_id']==r['artifact_id']
 checks['deployment -> registry version']=d['registry_version']==r['version']
 checks['approval -> deployed artifact']=a['artifact_id']==d['artifact_id']
 checks['approval -> deployed version']=a['registry_version']==d['registry_version']
 checks['approval authorized']=a['authorized']
 artifact=get(c['artifacts'],r['artifact_id'],'registry -> artifact')
 run_id=get(r,'run_id','registry -> run')
 run=get(c['runs'],run_id,'registry -> run') if run_id is not None else None
 if artifact:
  for rk,ak in [('artifact_id','artifact_id'),('artifact_source','uri'),('generation','generation'),('sha256','sha256')]: checks['registry -> artifact '+rk]=r[rk]==artifact[ak]
  client=StorageClient({artifact['uri']:{'generation':artifact['generation'],'data':Path('outputs/'+artifact['artifact_id']+'.txt').read_bytes()}})
  request={'uri':r['artifact_source'],'if_generation_match':r['generation']}
  result['exact_generation_download_request']=request
  try: content=client.blob(request['uri']).download_as_bytes(if_generation_match=request['if_generation_match'])
  except (PreconditionFailed,KeyError) as e: checks['exact generation download']=False;result['download_error']=str(e)
  else:
   checks['exact generation download']=True
   digest=sha(content);checks['downloaded content -> registry hash']=digest==r['sha256'];checks['downloaded content -> artifact hash']=digest==artifact['sha256']
   result['content_comparison']={'computed_sha256':digest,'registry_sha256':r['sha256'],'artifact_sha256':artifact['sha256']}
 if run:
  checks['registry -> originating run']=r['run_id']==run['run_id']
  checks['run -> artifact identity']=run['artifact_id']==r['artifact_id']
  checks['run -> artifact hash']=run['artifact_sha256']==r['sha256']
  for field,collection in [('dataset_id','datasets'),('configuration_id','configurations'),('code_id','code')]:
   record=get(c[collection],run[field],'run -> '+field)
   if record is None: continue
   if collection=='datasets':
    digest=sha(Path(record['file']).read_bytes());checks['run -> dataset content identity']=digest==record['sha256'];result['dataset_comparison']={'computed_sha256':digest,'recorded_sha256':record['sha256']}
   elif collection=='configurations':
    digest=sha(json.dumps(record['resolved'],sort_keys=True,separators=(',',':')).encode());checks['run -> resolved configuration identity']=digest==record['sha256'];result['configuration_comparison']={'resolved':record['resolved'],'computed_sha256':digest,'recorded_sha256':record['sha256']}
   else:
    git=[]; env=dict(os.environ,GIT_DIR=str(Path(record['repository']).resolve()/'.git'))
    for cmd in [['git','rev-parse','--verify',record['revision']],['git','show',record['revision']]]:
     p=subprocess.run(cmd,env=env,text=True,capture_output=True)
     git.append({'command':cmd,'cwd':str(Path.cwd()),'GIT_DIR':env['GIT_DIR'],'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
    result['executed_git_inspections']=git
    checks['code revision -> existing local commit']=all(g['exit_code']==0 for g in git) and git[0]['stdout'].strip()==record['revision']
 result['missing_links']=missing
 result['mismatched_or_unverified_links']=[k for k,v in checks.items() if not v]
 result['verified']=not missing and all(checks.values())
 result['audit_verdict']='verified' if result['verified'] else 'missing or mismatched link; not verified'
 return result
if __name__=='__main__':
 cases=load('fixtures/lineage_cases.json'); evidence={}
 for name,c in cases.items():
  result=audit(c)
  assert result['verified']==(not result['missing_links'] and all(result['checks'].values()))
  if name=='approval_A_deployment_B': assert not result['checks']['approval -> deployed artifact']
  if name=='missing_run_link': assert 'registry -> run' in result['missing_links']
  evidence[name]={'records':c,'computed_audit':result,'case_assertions':{'verdict_agrees_with_all_required_checks':True}}
 Path('audit_evidence.json').write_text(json.dumps(evidence,indent=2))
