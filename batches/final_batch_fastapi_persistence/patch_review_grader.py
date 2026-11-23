import ast, copy, json, re
from pathlib import Path
p=Path('batches/final_batch_persistence/interactions.json')
d=json.loads(p.read_text())
x=next(i['interaction'] for t in d['tiles'] for i in t['interactions'] if i['step_id']=='tile_065.s04')
src=x['public']['workspace']['files'][0]['content']
old=ast.literal_eval(ast.parse(src).body[0].value)
new=old.replace('("won\'t", "will not")', '("won\'t", "will not"), ("isn\'t", "is not"), ("wouldn\'t", "would not")')
start=new.index('    recovery_claim = any(')
end=new.index('    loss = loss and not loss_denial',start)
new=new[:start]+r'''    # Recovery polarity belongs to the recovery predicate, not any earlier
    # negation in the review. Keep sentence boundaries (except qualified names).
    clauses = re.split(r'[.!?;\n]+', re.sub(r'(?<=\w)\.(?=\w)', ' ', requirement_text))
    recovery_claim = False
    for clause in clauses:
        # The subject must be the proposed inverse/schema recreation, not a
        # different recovery mechanism mentioned elsewhere in the review.
        subject = re.search(r'\b(?:recreate|downgrade|original column|schema)\b', clause)
        if not subject:
            continue
        tail = clause[subject.start():]
        for match in re.finditer(r'\brestore\b|\bbring\b(?=.{0,50}\bdata\b.{0,15}\bback\b)', tail):
            before, after = tail[:match.start()], tail[match.end():]
            data_object = re.match(r'\s+(?:(?:all|every|the|any|those|these|its|their|former|previous|drop|lose|existing|original|stored|of)\s+){0,8}data\b', after)
            negated = re.search(r'\b(?:not|never|cannot|can not|fails? to|rather than|instead of)\s+(?:(?:be|necessarily|automatically|reliably|actually|assumed|to|able)\s+){0,5}$', before)
            if data_object and not negated:
                recovery_claim = True
    # Equivalent explanations may describe an empty/schema-only replacement
    # instead of using the literal 'does not restore deleted data' phrase.
    no_recovery = no_recovery or proposition(r'(?:recreate|downgrade|original column).{0,80}(?:empty column|column.{0,15}empty)')
    no_recovery = no_recovery or proposition(r'(?:recreate|downgrade).{0,80}(?:only|just).{0,20}(?:schema|column).{0,50}(?:not|without).{0,30}data')
    no_recovery = no_recovery or proposition(r'(?:recreate|downgrade).{0,80}restore.{0,25}(?:schema|column).{0,25}(?:but not|not).{0,25}data')
    no_recovery = no_recovery or proposition(r'(?:recreate|downgrade).{0,80}(?:cannot|does not|will not).{0,20}undo.{0,20}data loss')
''' +new[end:]
assert new!=old
# Change the identical supplied grader in starter and reference solution only.
for f in x['public']['workspace']['files']+x['grading']['solution_files']:
 tree=ast.parse(f['content']); value=ast.literal_eval(tree.body[0].value)
 assert value==old
 line=f['content'].split('\n',1)
 f['content']='_SUPPLIED_SCAFFOLD = '+repr(new)+'\n'+line[1]
# Regression expectations reuse the existing compliant/noncompliant predicates;
# no existing answer key changes.
base=next(t for t in x['grading']['tests'] if t['test_id'].endswith('accept_confirm_downgrade'))
wrong=next(t for t in x['grading']['tests'] if t['test_id'].endswith('reject_unrelated_negation_recovery_downgrade'))
common='Dropping orders.note loses existing notes; adding orders.customer_note does not preserve them. '
requirements=' Manual correction is required before approval. Confirm upgrade and downgrade on a test database before approval.'
for name, phrase, template in [
 ('accept_schema_only', 'The downgrade restores only the schema, not the deleted values.', base),
 ('accept_empty_recreation', 'Recreating orders.note produces an empty column.', base),
 ('reject_recovery_despite_negation', 'The downgrade is not unsafe: it restores all lost notes.', wrong),
 ('reject_contradictory_recovery', 'Recreating orders.note does not restore deleted data. The downgrade restores all lost notes.', wrong),
]:
 t=copy.deepcopy(template); t['test_id']='tile_065.s04.'+name
 t['spec']['requests'][-1]['json']['args'][0]=common+phrase+requirements
 t['message_on_fail']='Judge schema recreation and deleted-data recovery separately; attach negation to its own predicate.'
 x['grading']['tests'].append(t)
# Independently execute all supplied grader checks before writing.
ns={};exec(new.split('def check_review')[0],ns)
for t in x['grading']['tests']:
 r=t['spec'].get('requests',[{}])[-1].get('json',{})
 if r.get('function')=='review_findings':
  got=ns['review_findings'](*r['args']); exp=t['spec']['expected']['json']
  assert got==exp,(t['test_id'],got,exp)
p.write_text(json.dumps(d,indent=2)+'\n')
print('Patched one interaction; all direct review_findings regression tests pass.')
