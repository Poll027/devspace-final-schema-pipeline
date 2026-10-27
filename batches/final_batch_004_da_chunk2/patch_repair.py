"""
Repair-round patch for screens.part.c1.json
Addresses evaluator findings (all ADVISORY):
1. s04.v1 diagram: add forward-reference sentence to s04.p2 noting CIs are covered in the next step
2. s06.c1: restore f5 hedge "while it may be useful to think of it that way..."
3. s06.p2: move stat-vs-practical-significance takeaway out of CI-focused s06 into recap s16.p1
4. capstone_delivery s04.v1: "33%" -> "33.3%"
5. capstone_workflow s14.p1: "any stage open to revisiting" -> "stages such as scoping open to revisiting"
"""
import json, copy

with open('batches/final_batch_004_da_chunk2/screens.part.c1.json', 'r') as f:
    data = json.load(f)

stats_tile = next(t for t in data['tiles'] if t['tile_id'] == 'tile_stats_sample_size_significance')
capstone_workflow_tile = next(t for t in data['tiles'] if t['tile_id'] == 'tile_capstone_question_workflow')
capstone_delivery_tile = next(t for t in data['tiles'] if t['tile_id'] == 'tile_capstone_execution_narration_delivery')

# ── Fix 1: s04.v1 diagram placed before CIs are taught ──────────────────────
# Add a forward-reference sentence to s04.p2 so the diagram is contextualised.
s04 = next(s for s in stats_tile['steps'] if s['step_id'] == 'tile_stats_sample_size_significance.s04')
for b in s04['blocks']:
    if b['block_id'] == 'tile_stats_sample_size_significance.s04.p2':
        # Append a forward-reference sentence
        b['text'] = (
            b['text'].rstrip()
            + " The diagram below previews how repeated sampling produces a spread of confidence intervals — "
            "a concept covered fully in the next step."
        )
        break

# ── Fix 2: s06.c1 — restore f5 hedge ────────────────────────────────────────
# Glossary f5 / tb5 wording:
# "Describing a confidence interval as capturing the population parameter with a certain probability
#  is a common error; while it may be useful to think of it that way, the confidence level only
#  quantifies how plausible it is that the parameter is in the given interval. So it's not quite
#  right to say 'there's a 95% chance the true completion-rate difference is in this interval' --
#  the 95% describes how the method behaves across many samples, not the probability attached to
#  this one interval."
s06 = next(s for s in stats_tile['steps'] if s['step_id'] == 'tile_stats_sample_size_significance.s06')
for b in s06['blocks']:
    if b['block_id'] == 'tile_stats_sample_size_significance.s06.c1':
        b['text'] = (
            "Describing a confidence interval as capturing the population parameter with a certain "
            "probability is a common error; while it may be useful to think of it that way, the "
            "confidence level only quantifies how plausible it is that the parameter is in the given "
            "interval. So it is not quite right to say \u2018there is a 95% chance the true "
            "completion-rate difference is in this interval\u2019 \u2014 the 95% describes how the "
            "method behaves across many samples, not the probability attached to this one interval."
        )
        break

# ── Fix 3: s06.p2 — move stat-vs-practical-significance takeaway to recap ───
# Remove s06.p2 from s06 blocks and fold its content into s16.p1 (recap).
s06_p2_text = None
new_s06_blocks = []
for b in s06['blocks']:
    if b['block_id'] == 'tile_stats_sample_size_significance.s06.p2':
        s06_p2_text = b['text']
    else:
        new_s06_blocks.append(b)
s06['blocks'] = new_s06_blocks

# Also remove tb7 / f6 from s06 step-level lineage (they belong to the moved block)
s06_lineage = s06['lineage']
s06_lineage['teaching_block_ids'] = [
    tb for tb in s06_lineage.get('teaching_block_ids', [])
    if tb != 'stats.significance_confidence_concept#tb7'
]
s06_lineage['fact_ids'] = [
    f for f in s06_lineage.get('fact_ids', [])
    if f != 'stats.significance_confidence_concept#f6'
]

# Add the takeaway to s16.p1 (recap) — append a sentence
s16 = next(s for s in stats_tile['steps'] if s['step_id'] == 'tile_stats_sample_size_significance.s16')
for b in s16['blocks']:
    if b['block_id'] == 'tile_stats_sample_size_significance.s16.p1':
        # The recap already mentions the stat-vs-practical point; ensure it is explicit
        # s06.p2 text: "When the sample size becomes large, even a very small, practically
        # unimportant difference can be detected and called statistically significant..."
        # The recap p1 already contains this idea; just ensure the wording is present.
        # Check if it already covers it:
        if 'practically unimportant' not in b['text']:
            b['text'] = b['text'].rstrip() + (
                " When the sample is large enough, even a very small, practically unimportant "
                "difference can be detected and called statistically significant — significance "
                "tells you how unusual the result would be if there were truly no difference, "
                "not that the lift is big enough to matter."
            )
        # Ensure lineage covers tb7 / f6
        if 'stats.significance_confidence_concept#tb7' not in b['lineage'].get('teaching_block_ids', []):
            b['lineage'].setdefault('teaching_block_ids', []).append('stats.significance_confidence_concept#tb7')
        if 'stats.significance_confidence_concept#f6' not in b['lineage'].get('fact_ids', []):
            b['lineage'].setdefault('fact_ids', []).append('stats.significance_confidence_concept#f6')
        break

# ── Fix 4: capstone_delivery s04.v1 — "33%" -> "33.3%" ──────────────────────
s04_delivery = next(s for s in capstone_delivery_tile['steps']
                    if s['step_id'] == 'tile_capstone_execution_narration_delivery.s04')
for b in s04_delivery['blocks']:
    if b['block_id'] == 'tile_capstone_execution_narration_delivery.s04.v1':
        # Fix in before diagram node label
        for node in b.get('before', {}).get('nodes', []):
            if '33%' in node.get('label', ''):
                node['label'] = node['label'].replace('33%', '33.3%')
        # Also fix alt_text if present
        if '33%' in b.get('before', {}).get('alt_text', ''):
            b['before']['alt_text'] = b['before']['alt_text'].replace('33%', '33.3%')
        break

# ── Fix 5: capstone_workflow s14.p1 — "any stage open to revisiting" ─────────
s14_workflow = next(s for s in capstone_workflow_tile['steps']
                    if s['step_id'] == 'tile_capstone_question_workflow.s14')
for b in s14_workflow['blocks']:
    if b['block_id'] == 'tile_capstone_question_workflow.s14.p1':
        b['text'] = b['text'].replace(
            'any stage open to revisiting',
            'stages such as scoping open to revisiting'
        )
        break

with open('batches/final_batch_004_da_chunk2/screens.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Patch applied successfully.")
