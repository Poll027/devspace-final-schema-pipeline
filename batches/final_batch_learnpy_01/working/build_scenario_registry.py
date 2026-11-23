import ast
import csv
import hashlib
import io
import json
import re
from pathlib import Path

B = Path(__file__).resolve().parents[1]
bundle = json.loads((B / 'inputs/path_glossary_bundle.json').read_text())
profile = json.loads(Path('00_FINAL_PIPELINE_CORE/registry/path_profiles/learn_python.json').read_text())
by_id = {b['context']['concept_id']: b for b in bundle['bundles']}

def examples(b):
    return [s for t in b['teaching_blocks'] for s in re.findall(r'```python\s*\n(.*?)```', t['content'], re.S)]

def example(cid):
    return examples(by_id['python.' + cid])[0].strip()

# Mine the vocabulary from the glossary itself, not from invented example data.
vocab = set()
for b in bundle['bundles']:
    for code in examples(b):
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                vocab.add(node.id)
            elif isinstance(node, (ast.FunctionDef, ast.arg)):
                vocab.add(node.name if isinstance(node, ast.FunctionDef) else node.arg)
            elif isinstance(node, ast.Attribute):
                vocab.add(node.attr)
            elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub) and isinstance(node.operand, ast.Constant):
                vocab.add(ast.get_source_segment(code, node))
            elif isinstance(node, ast.Constant):
                vocab.add(ast.get_source_segment(code, node))
            elif isinstance(node, ast.Import):
                vocab.update(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                vocab.add(node.module)
                vocab.update(a.name for a in node.names)
    text = '\n'.join(t['content'] for t in b['teaching_blocks']) + '\n' + json.dumps(b['practice_anchor'], ensure_ascii=False) + '\n' + json.dumps(b['visual_anchor'], ensure_ascii=False)
    # Names/files/literals mentioned in anchors but absent from executable examples.
    vocab.update(re.findall(r'\b\w+\.csv\b|\b\d+(?:\.\d+)?\b', text))
    for word in ['notebook', 'notebooks', 'pen', 'pencil', 'eraser', 'tokens', 'red', 'blue', 'green', 'yellow', 'done', 'three', 'OrderCost', 'Quantity', 'UnitPrice', 'Cost', 'selected_labels', 'grade', 'A', 'B', 'C', 'Enter a numeric quantity', 'bool', 'True', 'False']:
        if re.search(r'(?<!\w)' + re.escape(word) + r'(?!\w)', text):
            vocab.add(word)

scenario_id = 'scn.python_learning_desk'
registry = {
    'schema_version': '1.0', 'kind': 'scenario_asset_registry',
    'path_id': bundle['path_id'], 'batch_id': bundle['batch_id'],
    'scenarios': [{
        'scenario_id': scenario_id,
        'name': 'Python learning desk',
        'summary': 'A fictional learner at a small stationery desk builds notebook-order helpers and practices with product quantities, color labels, token grouping and sample grade scores. All examples are authored teaching fixtures, not observations about real customers or businesses.',
        'domain': 'Python fundamentals and stationery-order practice',
        'glossary_example_vocab': sorted(vocab - {None, ''})
    }],
    'assets': []
}

# The glossary specifies exactly one CSV record. Preserve it rather than expanding
# the base and contradicting the practice anchor's one-dictionary success state.
fio = by_id['python.file_io']['practice_anchor']['live_code']['starter_state_intent']
header = re.search(r'header (\w+,\w+)', fio).group(1).split(',')
record = re.search(r'data row (\w+,\d+)', fio).group(1).split(',')
row = [record[0], int(record[1])]
s = io.StringIO(newline='')
w = csv.writer(s, lineterminator='\n'); w.writerow(header); w.writerow(row)
csv_content = s.getvalue()
filename = re.search(r'\b\w+\.csv\b', fio).group()
(B / 'assets' / filename).write_text(csv_content)
csv_bytes = (B / 'assets' / filename).read_bytes()
asset_id = 'ds.orders'
# Hidden-check alternatives use product/quantity values already in the examples.
mapping_tree = ast.parse(example('dictionaries'))
initial_map = ast.literal_eval(mapping_tree.body[0].value)
replacement_quantity = ast.literal_eval(mapping_tree.body[2].value)
variants = []
for suffix, label, quantity in [('pen', 'pen', initial_map['pen']), ('changed_quantity', row[0], replacement_quantity)]:
    variants.append({
        'variant_id': 'v.orders.' + suffix,
        'derived_from': asset_id,
        'purpose': 'Alternate authored CSV fixture for checking that the reader uses file contents rather than a hard-coded record.',
        'ops': [
            {'op': 'set_cell', 'where': {header[0]: row[0]}, 'occurrence': 0, 'column': header[1], 'value': quantity},
            {'op': 'set_cell', 'where': {header[0]: row[0]}, 'occurrence': 0, 'column': header[0], 'value': label}
        ],
        'planted_issues': []
    })
registry['assets'].append({
    'asset_id': asset_id, 'asset_kind': 'dataset', 'scenario_id': scenario_id,
    'title': filename,
    'description': 'The exact illustrative CSV fixture for python.file_io. The quantity column is a count; csv.DictReader returns its CSV text as a string, not as an inferred integer. Alternate fixtures support content-dependent hidden checks.',
    'columns': [
        {'name': header[0], 'type': 'string', 'semantic_role': 'categorical', 'description': 'Product label used as the CSV record category.'},
        {'name': header[1], 'type': 'integer', 'semantic_role': 'numerical', 'description': 'Whole-number quantity; CSV readers expose the serialized value as text, not a numeric-looking category label.'}
    ],
    'rows': [row], 'data_file': {'uri': 'assets/' + filename, 'format': 'csv', 'sha256': hashlib.sha256(csv_bytes).hexdigest(), 'bytes': len(csv_bytes)},
    'variants': variants, 'provenance': 'authored'
})

# Starter state only: the anchor brief is copied into comments, never solved.
# Initializer lines below are extracted from the teaching example or anchor.
first_lines = {
    'comparison_operators': 1,
    'logical_operators': 2,
    'lists': 0,
    'string_basics_formatting': 2,
    'variable_scope': 1,
    'import_statements': 0,
    'for_loops': 1,
    'iterating_collections': 1,
    'comprehensions': 1,
    'type_conversion': 0,
    'while_loops': 1,
}

def starter(b):
    cid = b['context']['concept_id'].split('.', 1)[1]
    intent = b['practice_anchor']['live_code']['starter_state_intent']
    code = example(cid)
    lines = code.splitlines()
    if cid in first_lines and first_lines[cid]:
        return '\n'.join(lines[:first_lines[cid]]) + '\n'
    if cid == 'error_handling':
        initial = re.search(r'Provide (text = "[^"]*")', intent)[1]
        conversion = re.search(r'unprotected (quantity = int\(text\))', intent)[1]
        return initial + '\n' + conversion + '\n'
    if cid == 'type_conversion':
        # The anchor starts before the example's conversion and multiplication.
        value = re.search(r'quantity_text = ("[^"]*") and price = (\d+(?:\.\d+)?)', intent)
        return 'quantity_text = ' + value[1] + '\nprice = ' + value[2] + '\n'
    if cid in ('conditional_statements', 'sets', 'import_statements'):
        match = re.search(r'Provide (?:only )?(\w+ = (?:\[[^\]]*\]|\d+(?:\.\d+)?))', intent)
        return match[1] + '\n'
    if cid == 'defining_calling_functions':
        return re.search(r'body line (message = "[^"]*")', intent)[1] + '\n'
    if cid == 'parameters_arguments':
        head = re.search(r'Provide (def \w+\(\):)', intent)[1]
        body = re.search(r'indented body (.*?) followed by', intent)[1].rstrip(',')
        call = re.search(r'followed by (\w+\(\))', intent)[1]
        return head + '\n    ' + body + '\n\n' + call + '\n'
    if cid == 'return_values':
        return lines[0] + '\n    pass\n'
    if cid == 'loop_control':
        # Keep only the provided initialization and loop header, not its logic.
        return '\n'.join(lines[:2]) + '\n    pass\n'
    if cid == 'pep8_style':
        # Extract all supplied values/names from the anchor; author only formatting.
        helper = re.search(r'helper named (\w+)', intent)[1]
        params = re.search(r'parameters (\w+) and (\w+)', intent).groups()
        local = re.search(r'local variable (\w+)', intent)[1]
        args = re.search(r'arguments (\d+) and (\d+)', intent).groups()
        return f'def {helper}( {params[0]} , {params[1]} ):\n  {local}={params[0]}*{params[1]}\n  return {local}\n\n{helper}( {args[0]} , {args[1]} )\n'
    return ''

covered = []
for b in bundle['bundles']:
    cid = b['context']['concept_id']
    anchor = b['practice_anchor']
    if cid in profile.get('practice_type_by_concept', {}):
        continue
    if anchor['type'] != 'live_code':
        continue
    main = '# ' + anchor['objective'] + '\n'
    main += '\n'.join('# ' + line for line in anchor['live_code']['starter_state_intent'].splitlines()) + '\n\n'
    main += starter(b)
    files = [{'path': 'main.py', 'content': main}]
    if cid == 'python.file_io':
        files.append({'path': filename, 'content': csv_content})
    registry['assets'].append({
        'asset_id': 'ws.' + cid,
        'asset_kind': 'code_workspace', 'scenario_id': scenario_id,
        'title': b['context']['concept_name'] + ' practice',
        'runtime': profile['runtime_by_concept_prefix']['python'], 'files': files
    })
    covered.append(cid)

(B / 'scenario_asset_registry.json').write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n')
# Stage-local mistakes-to-avoid/coverage assertions.
assert len(covered) == sum(b['practice_anchor']['type'] == 'live_code' and b['context']['concept_id'] not in profile.get('practice_type_by_concept', {}) for b in bundle['bundles'])
assert all(len(r) == len(header) for r in registry['assets'][0]['rows'])
assert len({a['asset_id'] for a in registry['assets']}) == len(registry['assets'])
assert all(b['visual_anchor']['type'] == 'code' or b['visual_anchor']['type'] == 'before_after' for b in bundle['bundles'])
assert not any(b['practice_anchor']['type'] in ('field_selection', 'data_cleanup') and re.search(r'flag|problem|issue|quality|duplicate|missing', b['practice_anchor']['objective'] + b['practice_anchor']['success'], re.I) for b in bundle['bundles'])
for a in registry['assets']:
    if a['asset_kind'] == 'code_workspace':
        ast.parse(a['files'][0]['content'])
print(json.dumps({'concepts': len(bundle['bundles']), 'scenarios': len(registry['scenarios']), 'assets': len(registry['assets']), 'workspaces': len(covered), 'dataset_rows': len(registry['assets'][0]['rows']), 'variants': len(variants), 'vocabulary_terms': len(vocab)}))

# Record the self-review: all checks are computed from current artifacts.
checklist = {
    'row_width_matches_columns': all(len(r) == len(a['columns']) for a in registry['assets'] if a['asset_kind'] == 'dataset' for r in a['rows']),
    'quantity_is_count_not_digit_label': registry['assets'][0]['columns'][1]['semantic_role'] == 'numerical',
    'csv_matches_declared_base_rows': list(csv.reader(io.StringIO(csv_content)))[1:] == [[str(v) for v in row]],
    'csv_hash_matches_file': registry['assets'][0]['data_file']['sha256'] == hashlib.sha256((B / 'assets' / filename).read_bytes()).hexdigest(),
    'duplicate_occurrences_not_applicable': not any(i.get('kind') == 'duplicate_row' for v in variants for i in v['planted_issues']),
    'no_find_issues_anchor_without_variant': not any(b['practice_anchor']['type'] in ('field_selection', 'data_cleanup') for b in bundle['bundles']),
    'every_live_code_anchor_has_workspace': len(covered) == len(bundle['bundles']),
    'no_inspect_and_judge_workspace': not (set(covered) & set(profile['practice_type_by_concept'])),
    'base_preserves_glossary_single_csv_record': len(registry['assets'][0]['rows']) == 1,
    'all_visual_anchors_covered_without_plot': all(b['visual_anchor']['type'] in ('code', 'before_after') for b in bundle['bundles']),
    'starters_parse_as_python': True
}
assert all(checklist.values())
(B / 'working/stage01_checklist.json').write_text(json.dumps(checklist, indent=2) + '\n')
