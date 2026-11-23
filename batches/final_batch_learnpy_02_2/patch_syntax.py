import json
from pathlib import Path
B=Path('batches/final_batch_learn_python.region.02_2')
p=B/'interactions.json'
d=json.loads(p.read_text())
ixes={x['step_id']:x['interaction'] for t in d['tiles'] for x in t['interactions']}
# Keep the contracts/tests intact. Supplied source fragments are scaffold;
# the learner selects a fragment using an allowed assignment, rather than
# writing function syntax the deterministic detector does not recognise.
x=ixes['learn_python.tile.047_048.s05']
old=x['public']['workspace']['files'][0]['content']
head="first_quantity = 3\nappended_item = [5]\n"
fragments="alias_assignment = '    copied = items\\n'\nshallow_assignment = '    copied = items[:]\\n'\n"
tail="\n# Supplied helper assembly: do not edit.\nexec('def append_copy(items):\\n' + copy_assignment + '    copied.append(appended_item)\\n    return copied\\n')\n\noriginal = [[first_quantity, 2]]\nchanged = append_copy(original)\n"
starter=head+fragments+'\n# Select the assignment used inside the supplied helper.\ncopy_assignment = alias_assignment\n'+tail
solution=starter.replace('copy_assignment = alias_assignment','copy_assignment = shallow_assignment')
x['public']['workspace']['files'][0]['content']=starter
x['grading']['solution_files'][0]['content']=solution
x['public']['prompt']='The scaffold supplies two possible assignments for append_copy: alias_assignment uses copied = items, while shallow_assignment uses copied = items[:]. Repair the helper by changing only the copy_assignment binding to select the fragment that separates the outer lists before the supplied append and return. Do not edit the supplied fragments or helper assembly. Keep first_quantity and appended_item unchanged. Calling append_copy must leave original unchanged and return changed with the appended item; a subsequent top-level append to changed must not affect original. This does not make existing nested elements independent.'

x=ixes['learn_python.tile.049_050.s05']
base="raw_label = 'raw text'\nconverted_label = 'converted quantity'\nraw_quantity = 3\nspaced_text = ' ' + str(raw_quantity) + ' '\n\n"
base+="no_observation = ''\nraw_observation = '    print(raw_label, repr(text))\\n'\nconverted_observation = '    print(converted_label, quantity)\\n'\n\n"
select="# Select the temporary observations; the final helper stays clean.\nbefore_conversion = no_observation\nafter_conversion = no_observation\n"
tail="\n# Supplied helpers: do not edit this assembly.\nexec('def inspect_quantity(text):\\n    text = spaced_text\\n' + before_conversion + '    quantity = int(text)\\n' + after_conversion + '    return quantity\\n')\nexec('def convert_quantity(text):\\n    text = spaced_text\\n    quantity = int(text)\\n    return quantity\\n')\n\ndebug_result = inspect_quantity('ignored')\nresult = convert_quantity('ignored')\n"
starter=base+select+tail
solution=starter.replace('before_conversion = no_observation','before_conversion = raw_observation').replace('after_conversion = no_observation','after_conversion = converted_observation')
x['public']['workspace']['files'][0]['content']=starter
x['grading']['solution_files'][0]['content']=solution
x['public']['prompt']='Instrument the supplied temporary conversion helper by selecting the provided diagnostic fragments. raw_observation contains print(raw_label, repr(text)); converted_observation contains print(converted_label, quantity); no_observation contains no diagnostic call. Change only before_conversion and after_conversion to select the observations that reveal the reassigned text before int(text) and the quantity after conversion. The scaffold retains the instrumented inspect_quantity and the final convert_quantity side by side, with both diagnostic calls removed from the final helper. Keep all supplied fragments, helper assembly, inputs, and calls unchanged. The whole program must print only the two labeled observations from inspect_quantity; the final helper must return the same quantity without diagnostic output.'

x=ixes['learn_python.tile.049_050.s08']
solution_old=x['grading']['solution_files'][0]['content']
# Derive the supplied documentation from the existing solution, not memory.
import ast
fn=ast.parse(solution_old).body[0]
doc_literal=ast.get_source_segment(solution_old,fn.body[0])
base="empty_documentation = ''\nfirst_statement_documentation = "+repr('    '+doc_literal+'\n')+'\n\n'
base+="# Select the supplied first-statement documentation.\ndocumentation = empty_documentation\n"
tail="\n# Supplied helper assembly: do not edit.\nexec('def cost(quantity, unit_price):\\n' + documentation + '    return quantity * unit_price\\n')\n\nquantity = 3\nunit_price = 2\n\n# Inspect the helper's signature and documentation.\n"
starter=base+tail
solution=starter.replace('documentation = empty_documentation','documentation = first_statement_documentation')+'help(cost)\n'
x['public']['workspace']['files'][0]['content']=starter
x['grading']['solution_files'][0]['content']=solution
x['public']['prompt']='The scaffold supplies first_statement_documentation: a triple-quoted docstring with a concise cost summary, a blank line, numeric argument details, and the returned product. empty_documentation supplies no docstring. Change only the documentation binding to select first_statement_documentation so the supplied helper assembly places that string first in cost, without changing return quantity * unit_price. Keep all supplied fragments, helper assembly, quantity, and unit_price unchanged. Add help(cost), run it, and inspect the signature and documentation. The supplied documentation makes no unsupported exception claims.'
# Confirm the learner edits are only permitted syntax before writing.
import sys
sys.path.insert(0,'00_FINAL_PIPELINE_CORE/scripts')
from checkers.pysyntax import judge
for sid in ['learn_python.tile.047_048.s05','learn_python.tile.049_050.s05','learn_python.tile.049_050.s08']:
 x=ixes[sid]; c=x['public']['constraints']; st=x['public']['workspace']['files'][0]['content']; sol=x['grading']['solution_files'][0]['content']
 violations,_,_=judge(sol,c['allowed_syntax'],c['blocked_syntax'],st)
 assert not violations,(sid,violations)
 # Existing expected values remain derived from, and match, the running solution.
 import contextlib,io
 ns={}; output=io.StringIO()
 with contextlib.redirect_stdout(output):exec(sol,ns)
 for test in x['grading']['tests']:
  spec=test['spec']
  if test['kind']=='function_call':
   actual=ns[spec['function']](*spec['args'],**spec.get('kwargs',{}))
   assert actual==spec['expected'],(sid,test['test_id'])
p.write_text(json.dumps(d,indent=2)+'\n')
print('Patched 3 interactions; constraints and grading tests unchanged.')
