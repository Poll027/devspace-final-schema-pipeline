import json, ast, re
from pathlib import Path
p=Path('batches/final_batch_persistence/interactions.json')
d=json.loads(p.read_text())
ix={s['step_id']:s['interaction'] for t in d['tiles'] for s in t['interactions']}
original=json.loads(p.read_text())
def move(src,dst,cap):
    a,b=ix[src],ix[dst]
    m=next(m for m in a['measures'] if m['capability']==cap)
    a['measures'].remove(m);b['measures'].append(m)
    anchor=next(v for v in a['anchors'] if v.endswith('#assessment:'+cap))
    a['anchors'].remove(anchor);b['anchors'].append(anchor)
def choice(sid,prompt,options,feedback,correct):
    x=ix[sid];x['public']['prompt']=prompt
    x['public']['options']=[{'option_id':'o'+str(i+1),'text':s} for i,s in enumerate(options)]
    x['grading']['option_feedback']={'o'+str(i+2):{'message':s} for i,s in enumerate(feedback)}
    x['feedback']['correct']['message']=correct
    x['feedback']['incorrect']['message']=correct
move('tile_063.s04','tile_063.s03','distinguish_bearer_extraction_from_credential_validity')
choice('tile_063.s03',"Which statement correctly describes HTTPBearer’s default extraction behavior?",[
 'A nonempty Bearer credential reaches the handler, but extraction does not establish validity; absent, Basic, and empty Bearer headers are rejected.',
 'Every Authorization header reaches the handler and is valid',
 'A nonempty Bearer credential reaches the handler and extraction proves validity',
 'Empty Bearer headers pass, but Basic headers are rejected.'
],[
 'Not every header passes: absent, Basic, and empty Bearer credentials are rejected. Extracting a credential does not establish its validity.',
 'A nonempty Bearer credential can reach the handler, but extraction does not prove that credential is valid.',
 'Basic headers are rejected, but empty Bearer headers are also rejected; a nonempty Bearer credential is needed to pass extraction.'
], 'Default extraction rejects absent, Basic, and empty Bearer headers. A nonempty Bearer credential can reach the handler, but receiving it does not establish validity.')
move('tile_064.s05','tile_064.s04','choose_cache_eligible_reads')
choice('tile_064.s04', 'Repeated order reads permit reuse within the application’s staleness requirements and support notes and quantity representations. Which design fits?',[
 'Consider cache-aside for these reads and include both order identity and representation in each key.',
 'Consider cache-aside but key only by order identity',
 'Consider cache-aside but key only by representation',
 'Cache every read regardless of staleness requirements, using both identity and representation.'
],[
 'The reads are eligible for consideration, but omitting representation lets notes and quantity results for the same order collide.',
 'The reads are eligible for consideration, but omitting order identity lets different orders with the same representation collide.',
 'Including identity and representation distinguishes results, but eligibility still depends on reuse fitting the application’s staleness requirements; not every read qualifies.'
], 'These repeated reads permit reuse within the stated staleness requirements, so consider cache-aside. Include both order identity and representation to distinguish different results.')
move('tile_072.s03','tile_072.s02','distinguish_correlation_context_from_caller_authority')
choice('tile_072.s02', 'Local events contain chain-a while the outbound header contains chain-b. Which judgement is correct?',[
 'The request chain is broken, and neither identifier proves caller authority.',
 'The chain is intact because timestamps replace identifiers',
 'The chain is broken, but chain-b proves greater caller authority',
 'The identifiers prove authority, so their mismatch is harmless.'
],[
 'Timestamps do not replace the same identifier across local and outbound records. The mismatch breaks correlation, and identifiers provide context rather than proof of authority.',
 'The mismatch does break correlation, but chain-b is only correlation context and proves no greater caller authority.',
 'Neither identifier proves caller authority. Their mismatch is not harmless: it breaks the shared request-chain context.'
], 'Local and outbound records must retain the same request-chain identifier. This mismatch breaks correlation; neither identifier is proof of caller authority.')

def files(sid):
    x=ix[sid]
    return x['public']['workspace']['files']+x['grading']['solution_files']
def scaffold_edit(f,fn):
    c=f['content'];n=next(n for n in ast.parse(c).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_SUPPLIED_SCAFFOLD' for t in n.targets))
    lines=c.splitlines(keepends=True)
    lines[n.lineno-1:n.end_lineno]=['_SUPPLIED_SCAFFOLD = '+repr(fn(ast.literal_eval(n.value)))+'\n']
    f['content']=''.join(lines)
review='''def check_review(direction):
    import ast, re
    src=Path('exercise.py').read_text().split('# BEGIN LEARNER EDITS\\n',1)[1].split('# END LEARNER EDITS',1)[0]
    node=next(n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name==direction)
    comments=[line.split('#',1)[1] for line in src.splitlines()[node.lineno:node.end_lineno] if '#' in line and not re.search(r'#\\s*(candidate|todo)',line,re.I)]
    text=re.sub(r'[^a-z0-9]+',' ',' '.join(comments).lower()).strip()
    def has(pattern): return bool(re.search(pattern,text))
    correction=has(r'correct|fix|repair|revis|replace|amend') and has(r'before approv|prior to approv|before sign off|must.*approv|do not approv.*until|approv.*only after')
    verification=has(r'test database|test db|disposable database|disposable db|scratch database|testing database') and has(r'upgrad|forward migration') and has(r'downgrad|reverse migration') and has(r'verif|test|check|validat') and has(r'requir|must|need|before approv|prior to approv|only after')
    loss=has(r'data|notes|values|contents') and has(r'loss|lost|loses|destroy|discard|eras|delet|wip|not restor|cannot restor|can t restor|won t restor|not recover|cannot recover|does not bring back')
    findings={'direction':direction,'correction_before_approval':correction,'test_verification_required':verification}
    if direction=='upgrade':
        findings['possible_rename']=has(r'renam') and loss and has(r'drop|delet|remov') and has(r'add|creat|replac')
    else:
        findings['deleted_data_not_restored']=loss and has(r'not restor|cannot restor|can t restor|won t restor|not recover|cannot recover|can t recover|not bring back|irrevers|unrecover|lost forever|permanent')
    return findings
'''
x=ix['tile_065.s04']
x['public']['prompt']='Review only; do not execute schema changes.\nIntent: preserve existing notes while renaming orders.note to orders.customer_note. Candidate upgrade: drop orders.note; add orders.customer_note. Candidate downgrade: drop orders.customer_note; add orders.note.\nAnnotate upgrade() and downgrade() to identify whether the candidate implements the stated intent safely, explain the data-loss risk, and record correction and test-database verification requirements before approval. Leave both pass statements. Edit only BEGIN LEARNER EDITS; the rest is supplied scaffolding.'
for f in files('tile_065.s04'):
    scaffold_edit(f,lambda c: c[:c.index('def check_review(')]+review+c[c.index('\nimport inspect'):])
    f['content']=f['content'].replace('# Candidate: drop an existing column and add a replacement column.','# Candidate upgrade: drop orders.note; add orders.customer_note.').replace('# Candidate inverse: drop the replacement and recreate the original column.','# Candidate downgrade: drop orders.customer_note; add orders.note.')
sol=x['grading']['solution_files'][0]
start=sol['content'].index('# BEGIN LEARNER EDITS\n')+len('# BEGIN LEARNER EDITS\n')
end=sol['content'].index('# END LEARNER EDITS')
sol['content']=sol['content'][:start]+'''def upgrade():
    # REVIEW: This is a rename of orders.note to orders.customer_note, not a safe drop and add.
    # REVIEW: Dropping orders.note loses existing notes; adding customer_note does not preserve them.
    # REVIEW: Manual correction to preserve data is required before approval.
    # REVIEW: Test-database upgrade and downgrade verification is required before approval.
    pass

def downgrade():
    # REVIEW: Dropping customer_note loses its values; recreating orders.note does not restore deleted data.
    # REVIEW: Manual correction required before approval.
    # REVIEW: Test-database upgrade and downgrade verification required before approval.
    pass
'''+sol['content'][end:]
for f in files('tile_071.s04'):
    scaffold_edit(f,lambda c:c.replace('response=await receive(OrderEvent(**body),recorder)','response=receive(OrderEvent(**body),recorder)\n        if inspect.isawaitable(response): response=await response'))
for f in files('tile_076.s08'):
    def deletion(c):
        needle="        async with factory() as fresh:\n            target=await fresh.get(Order,identity);other=await fresh.get(Order,other_identity)\n            return {'target':snapshot(target),'other':snapshot(other),'raised':raised,'events':s.events}"
        replacement="""        operations=[event for event in s.events if event!='get']
        if fail:
            contract={'failure_order': operations==['delete','flush','rollback'] and 'commit' not in s.events}
        elif result is None:
            contract={'absence_no_delete': 'delete' not in s.events}
        else:
            contract={'success_order': operations==['delete','flush','commit'] and 'get' in s.events[:s.events.index('delete')]}
        assert all(contract.values())
        async with factory() as fresh:
            target=await fresh.get(Order,identity);other=await fresh.get(Order,other_identity)
            return {'target':snapshot(target),'other':snapshot(other),'raised':raised,**contract}"""
        assert needle in c
        return c.replace(needle,replacement)
    scaffold_edit(f,deletion)
# Advisory edits limited to the named fields/exercises.
for f in files('tile_065.s09'):
    scaffold_edit(f,lambda c:c.replace('external_reference: Mapped[str]=mapped_column(String,unique=True)','external_reference: Mapped[str]=mapped_column(String)'))
for f in files('tile_067.s12'):
    f['content']=f['content'].replace('# Contract: body contains only {"reason": public_reason}.',"# Contract: body contains only {'error': {'reason': 'The request could not be completed.'}}.")
ix['tile_080.s08']['public']['prompt']=ix['tile_080.s08']['public']['prompt'].replace('A Redis population write fails after a miss.','A Redis population write raises ConnectionError or TimeoutError after a miss.')
# Execute the review validator against actual solution comments to derive test results.
import tempfile,os
x=ix['tile_065.s04'];c=x['grading']['solution_files'][0]['content'];sc=ast.literal_eval(ast.parse(c).body[0].value)
with tempfile.TemporaryDirectory(dir='batches/final_batch_persistence/working') as td:
    q=Path(td).resolve();(q/'exercise.py').write_text(c);cwd=Path.cwd();os.chdir(q)
    try:
        env={};exec(sc[:sc.index('\nimport inspect')],env)
        for t in x['grading']['tests']:
            direction=t['spec']['requests'][0]['json']['args'][0]
            result=env['check_review'](direction);assert all(v is True for k,v in result.items() if k!='direction')
            t['spec']['expected']['json']=result
    finally:os.chdir(cwd)
# Operation-contract outputs are derived from the previously executed event traces.
for t in ix['tile_076.s08']['grading']['tests']:
    expected=t['spec']['expected']['json'];events=expected.pop('events');ops=[e for e in events if e!='get']
    if t['spec']['requests'][0]['json']['args'][1]:
        expected['failure_order']=ops==['delete','flush','rollback'] and 'commit' not in events
    elif 'delete' not in events:expected['absence_no_delete']='delete' not in events
    else:expected['success_order']=ops==['delete','flush','commit'] and 'get' in events[:events.index('delete')]
changed={s['step_id'] for t,ot in zip(d['tiles'],original['tiles']) for s,os_ in zip(t['interactions'],ot['interactions']) if s!=os_}
allowed={'tile_063.s03','tile_063.s04','tile_064.s04','tile_064.s05','tile_065.s04','tile_065.s09','tile_067.s12','tile_071.s04','tile_072.s02','tile_072.s03','tile_076.s08','tile_080.s08'}
assert changed==allowed,(changed,allowed)
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print('Patched:',sorted(changed))
from collections import Counter
print('Counts:',len(d['tiles']),sum(len(t['interactions']) for t in d['tiles']),Counter(s['interaction']['type'] for t in d['tiles'] for s in t['interactions']))
