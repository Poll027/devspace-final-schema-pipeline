"""Patch interactions.part.c1.json to fix all gate errors."""
import json, copy, re

with open('interactions.part.c1.json') as f:
    data = json.load(f)

def strip_fact_prefix(fact_id):
    """Convert 'concept.id#fN' -> 'fN', leave 'fN' alone."""
    if '#' in fact_id:
        return fact_id.split('#', 1)[1]
    return fact_id

# Remediation step mappings
# tile_spreadsheet_formula_syntax_refs:
#   r01 = formula_syntax, r02 = formula_syntax, r03 = relative_absolute_references
# tile_spreadsheet_aggregation_logical:
#   r01 = aggregation_functions, r02 = logical_functions, r03 = logical_functions
# tile_spreadsheet_text_date_conditional_agg:
#   r01 = text_combining, r02 = text_extraction, r03 = date_functions, r04 = conditional_aggregation, r05 = conditional_aggregation

REM_MAP = {
    'tile_spreadsheet_formula_syntax_refs.s01': 'tile_spreadsheet_formula_syntax_refs.r01',
    'tile_spreadsheet_formula_syntax_refs.s07': 'tile_spreadsheet_formula_syntax_refs.r03',
    'tile_spreadsheet_aggregation_logical.s01':  'tile_spreadsheet_aggregation_logical.r01',
    'tile_spreadsheet_aggregation_logical.s06':  'tile_spreadsheet_aggregation_logical.r02',
    'tile_spreadsheet_text_date_conditional_agg.s01': 'tile_spreadsheet_text_date_conditional_agg.r01',
    'tile_spreadsheet_text_date_conditional_agg.s04': 'tile_spreadsheet_text_date_conditional_agg.r02',
    'tile_spreadsheet_text_date_conditional_agg.s08': 'tile_spreadsheet_text_date_conditional_agg.r03',
    'tile_spreadsheet_text_date_conditional_agg.s11': 'tile_spreadsheet_text_date_conditional_agg.r04',
}

# Allowed syntax fixes for code_exercise steps
ALLOWED_SYNTAX_FIX = {
    # s06 formula_syntax_refs: =D3-D2 and =(D2+D3)*2
    # tags: op_sub, ref_rel, op_add, op_mul, paren_group, lit_num
    'tile_spreadsheet_formula_syntax_refs.s06': {
        'allowed_syntax': ['+ - * /', 'parentheses', 'relative cell references', 'numbers'],
        'blocked_syntax': ['SUM', 'IF', 'VLOOKUP'],
    },
    # s11 formula_syntax_refs: =D2*$H$1 etc.
    # tags: op_mul, ref_rel, ref_abs
    'tile_spreadsheet_formula_syntax_refs.s11': {
        'allowed_syntax': ['+ - * /', 'relative cell references', 'absolute references ($A$1)'],
        'blocked_syntax': ['SUM', 'IF', 'VLOOKUP'],
    },
    # s10 aggregation_logical: nested IF with AND, comparisons, text, numbers, rel refs
    'tile_spreadsheet_aggregation_logical.s10': {
        'allowed_syntax': [
            'IF(logical_test, value_if_true, value_if_false)',
            'AND(condition1, condition2)',
            'OR(condition1, condition2)',
            'comparison operators',
            'text in quotes',
            'numbers',
            'relative cell references',
        ],
        'blocked_syntax': ['IFS', 'SWITCH', 'CHOOSE'],
    },
    # s10 text_date_conditional_agg: DATEDIF with rel refs and text in quotes
    'tile_spreadsheet_text_date_conditional_agg.s10': {
        'allowed_syntax': [
            'DATEDIF(start_date, end_date, unit)',
            'relative cell references',
            'text in quotes',
        ],
        'blocked_syntax': ['TODAY', 'NOW', 'DAYS'],
    },
}

for tile in data['tiles']:
    for step in tile['interactions']:
        sid = step['step_id']
        ix = step['interaction']

        # 1. Strip concept_id prefix from all fact_ids in measures
        for m in ix.get('measures', []):
            m['fact_ids'] = [strip_fact_prefix(f) for f in m.get('fact_ids', [])]

        # 2. Fix remediation_step_id
        fb = ix.get('feedback', {})
        rid = fb.get('remediation_step_id')
        if rid and rid in REM_MAP:
            fb['remediation_step_id'] = REM_MAP[rid]

        # 3. Fix allowed_syntax for code_exercise steps
        if sid in ALLOWED_SYNTAX_FIX and ix.get('type') == 'code_exercise':
            fix = ALLOWED_SYNTAX_FIX[sid]
            ix['public']['constraints']['allowed_syntax'] = fix['allowed_syntax']
            ix['public']['constraints']['blocked_syntax'] = fix['blocked_syntax']

        # 4. Fix s11 formula_uses test with empty functions list
        if sid == 'tile_spreadsheet_formula_syntax_refs.s11':
            tests = ix.get('grading', {}).get('tests', [])
            ix['grading']['tests'] = [
                t for t in tests
                if not (t.get('kind') == 'formula_uses' and not t.get('spec', {}).get('functions'))
            ]

with open('interactions.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2)
print("Patched interactions.part.c1.json")
