from pathlib import Path
p=Path(__file__).with_name('build_interactions.py')
s=p.read_text(); start=s.index(" if key=='101':\n"); end=s.index(" if key=='102':",start)
s=s[:start]+''' if key=='101':
  a='ds.change_record';rs=rows(a);record={r['evidence_kind']:r['evidence'] for r in rs};complete=excerpt(record)
  incomplete={k:v for k,v in record.items() if k not in ['execution','verification']}
  mismatched=dict(record);mismatched['execution']='CI applied a different plan, not the approved saved plan'
  context='Reviewed record:\\n```text\\n'+complete+'\\n```\\nThe supplied focused files were staged with git add FILES, committed with git commit -m "MESSAGE", pushed with git push, and review requested through the supplied pull-request interface. Verification identifies a single resulting exercise EC2 instance.'
  return classify(a,'Read each complete or alternate change-record excerpt. Decide whether it establishes a coherent, traceable reviewed EC2 change followed by approved saved-plan execution and single-instance verification, or is insufficient. Treat each record independently.',{'complete':'Complete coherent submission and approved execution evidence','incomplete':'Insufficient or mismatched execution evidence'},lambda r:'complete' if all(k in record for k in ['intent','diff','commit_reference','saved_plan','approval','execution','verification']) else 'incomplete','evidence_kind',context,selected=[0],additions=[('Alternate record (all other supplied staging, commit, push and review steps are unchanged):\\n```text\\n'+excerpt(incomplete)+'\\n```\\nCI execution and resulting-instance verification are not recorded.','incomplete'),('Alternate record (the same supplied submission steps were completed):\\n```text\\n'+excerpt(mismatched)+'\\n```','incomplete')])
''' + s[end:]
p.write_text(s)
