#!/usr/bin/env python3
"""
Generate screens for chunk c2: tile_viz_labeling_chart_selection, 
tile_viz_custom_multi_panel, tile_viz_seaborn_stats_themes
"""
import json
import sys

def load_data():
    """Load all necessary data files"""
    with open('inputs/path_glossary_bundle.json', 'r') as f:
        glossary = json.load(f)
    
    with open('scenario_asset_registry.json', 'r') as f:
        registry = json.load(f)
    
    with open('tile_plans.json', 'r') as f:
        plans_data = json.load(f)
    
    # Build concept lookup
    concepts = {}
    for bundle in glossary['bundles']:
        concept_id = bundle['context']['concept_id']
        concepts[concept_id] = bundle
    
    return glossary, registry, plans_data, concepts

def get_teaching_blocks(concept, tb_ids):
    """Extract teaching blocks"""
    blocks = []
    for tb_id in tb_ids:
        tb_num = tb_id.split('#')[1] if '#' in tb_id else tb_id
        for tb in concept.get('teaching_blocks', []):
            if tb['block_id'] == tb_num:
                blocks.append(tb)
                break
    return blocks

def get_facts(concept, fact_ids):
    """Extract facts"""
    facts = []
    coverage = concept.get('coverage', {})
    all_facts = coverage.get('facts', [])
    
    for fact_id in fact_ids:
        f_num = fact_id.split('#')[1] if '#' in fact_id else fact_id
        for fact in all_facts:
            if fact['fact_id'] == f_num:
                facts.append(fact)
                break
    return facts

def generate_screens():
    """Generate screens for the three target tiles"""
    glossary, registry, plans_data, concepts = load_data()
    
    target_tiles = [
        "tile_viz_labeling_chart_selection",
        "tile_viz_custom_multi_panel",
        "tile_viz_seaborn_stats_themes"
    ]
    
    # Extract plans for target tiles
    tile_plans = []
    for tile in plans_data['tiles']:
        if tile['tile_id'] in target_tiles:
            tile_plans.append(tile)
    
    # Build output structure
    output = {
        "schema_version": "1.0",
        "kind": "screens_part",
        "path_id": plans_data['path_id'],
        "batch_id": plans_data['batch_id'],
        "tiles": []
    }
    
    # Process each tile
    for tile_plan in tile_plans:
        tile_screens = generate_tile_screens(tile_plan, concepts, registry, plans_data)
        output['tiles'].append(tile_screens)
    
    return output

def generate_tile_screens(tile_plan, concepts, registry, plans_data):
    """Generate screens for a single tile"""
    tile_id = tile_plan['tile_id']
    
    tile_output = {
        "tile_id": tile_id,
        "title": tile_plan['title'],
        "steps": []
    }
    
    # Track remediation steps needed
    remediation_needed = {}
    
    # Process each step
    for step_plan in tile_plan['steps']:
        step = generate_step(step_plan, tile_plan, concepts, registry, plans_data)
        if step:
            tile_output['steps'].append(step)
            
            # Track first check/hands_on per concept for remediation
            if step_plan['type'] in ['check', 'hands_on']:
                for concept_id in step_plan['concept_ids']:
                    if concept_id not in remediation_needed:
                        remediation_needed[concept_id] = {
                            'step_id': step_plan['step_id'],
                            'fact_ids': step_plan.get('fact_ids', [])
                        }
    
    # Add remediation steps
    for concept_id, info in remediation_needed.items():
        remediation_step = generate_remediation_step(
            tile_id, concept_id, info, concepts, registry
        )
        if remediation_step:
            tile_output['steps'].append(remediation_step)
    
    return tile_output

def generate_step(step_plan, tile_plan, concepts, registry, plans_data):
    """Generate a single step"""
    step_type = step_plan['type']
    
    if step_type in ['check', 'hands_on']:
        return generate_check_or_handson_step(step_plan, concepts)
    elif step_type == 'explainer':
        return generate_explainer_step(step_plan, tile_plan, concepts, registry)
    elif step_type == 'video':
        return generate_video_step(step_plan, concepts)
    elif step_type == 'recap':
        return generate_recap_step(step_plan, tile_plan, concepts, plans_data)
    
    return None

def generate_check_or_handson_step(step_plan, concepts):
    """Generate framing for check/hands_on step"""
    concept_id = step_plan['concept_ids'][0]
    concept = concepts.get(concept_id, {})
    concept_name = concept.get('context', {}).get('concept_name', concept_id)
    
    step = {
        "step_id": step_plan['step_id'],
        "type": step_plan['type'],
        "concept_ids": step_plan['concept_ids'],
        "eyebrow": concept_name,
        "title": "Check your understanding" if step_plan['type'] == 'check' else "Practice",
        "lede": "",
        "blocks": [],
        "reward": None,
        "lineage": {
            "concept_ids": step_plan['concept_ids'],
            "teaching_block_ids": step_plan.get('teaching_block_ids', []),
            "fact_ids": step_plan.get('fact_ids', [])
        }
    }
    
    return step

def generate_explainer_step(step_plan, tile_plan, concepts, registry):
    """Generate explainer step with prose and visual blocks"""
    concept_id = step_plan['concept_ids'][0]
    concept = concepts.get(concept_id, {})
    concept_name = concept.get('context', {}).get('concept_name', concept_id)
    
    # Get teaching blocks and facts
    teaching_blocks = get_teaching_blocks(concept, step_plan.get('teaching_block_ids', []))
    facts = get_facts(concept, step_plan.get('fact_ids', []))
    
    step = {
        "step_id": step_plan['step_id'],
        "type": "explainer",
        "concept_ids": step_plan['concept_ids'],
        "eyebrow": concept_name,
        "title": "",
        "lede": "",
        "blocks": [],
        "reward": None,
        "lineage": {
            "concept_ids": step_plan['concept_ids'],
            "teaching_block_ids": step_plan.get('teaching_block_ids', []),
            "fact_ids": step_plan.get('fact_ids', [])
        }
    }
    
    # Generate content based on the specific step
    blocks = generate_explainer_blocks(
        step_plan, concept, teaching_blocks, facts, registry
    )
    step['blocks'] = blocks
    
    # Set title and lede
    if blocks:
        step['title'] = generate_step_title(step_plan, concept, teaching_blocks)
        step['lede'] = generate_step_lede(step_plan, concept, teaching_blocks)
    
    return step

def generate_explainer_blocks(step_plan, concept, teaching_blocks, facts, registry):
    """Generate blocks for an explainer step"""
    blocks = []
    block_counter = 1
    step_id = step_plan['step_id']
    concept_id = concept['context']['concept_id']
    
    # Generate prose blocks from teaching blocks
    for tb in teaching_blocks:
        prose_block = {
            "type": "prose",
            "block_id": f"{step_id}.b{block_counter:02d}",
            "role": "explanation",
            "text": revoice_teaching_block(tb, registry),
            "lineage": {
                "concept_ids": [concept_id],
                "teaching_block_ids": [f"{concept_id}#{tb['block_id']}"],
                "fact_ids": [f"{concept_id}#{f['fact_id']}" for f in facts if f['fact_id'] in tb.get('fact_ids', [])]
            }
        }
        blocks.append(prose_block)
        block_counter += 1
    
    # Add visual block if planned
    if step_plan.get('planned_visual_block_type'):
        visual_block = generate_visual_block(
            step_plan, concept, registry, block_counter
        )
        if visual_block:
            blocks.append(visual_block)
            block_counter += 1
    
    return blocks

def revoice_teaching_block(tb, registry):
    """Convert teaching block text to screen text using registry values"""
    text = tb.get('text', '')
    
    # This is a simplified version - in reality, we'd need to:
    # 1. Parse the teaching block text
    # 2. Replace generic references with scenario-specific values
    # 3. Shorten and adapt for screen reading
    
    # For now, return the text as-is (will be filled in properly below)
    return text

def generate_visual_block(step_plan, concept, registry, block_counter):
    """Generate a visual block based on the plan"""
    visual_type = step_plan.get('planned_visual_block_type')
    step_id = step_plan['step_id']
    concept_id = concept['context']['concept_id']
    
    if not visual_type:
        return None
    
    block = {
        "type": visual_type,
        "block_id": f"{step_id}.b{block_counter:02d}",
        "lineage": {
            "concept_ids": [concept_id],
            "teaching_block_ids": step_plan.get('teaching_block_ids', []),
            "fact_ids": step_plan.get('fact_ids', []),
            "anchors": step_plan.get('anchors', [])
        }
    }
    
    # Add type-specific fields (will be filled in properly below)
    if visual_type == "before_after":
        block.update({
            "before": {},
            "after": {},
            "change_summary": ""
        })
    elif visual_type == "side_by_side":
        block.update({
            "left_label": "",
            "right_label": "",
            "left": {},
            "right": {},
            "takeaway": ""
        })
    elif visual_type == "chart":
        block.update({
            "chart_kind": "",
            "asset_ref": {},
            "title": "",
            "alt_text": "",
            "encoding": {}
        })
    
    return block

def generate_step_title(step_plan, concept, teaching_blocks):
    """Generate a title for the step"""
    # Extract key idea from first teaching block
    if teaching_blocks:
        return teaching_blocks[0].get('title', '')
    return ""

def generate_step_lede(step_plan, concept, teaching_blocks):
    """Generate a lede for the step"""
    # Short intro sentence
    return ""

def generate_video_step(step_plan, concepts):
    """Generate video step with media_group"""
    concept_id = step_plan['concept_ids'][0]
    concept = concepts.get(concept_id, {})
    concept_name = concept.get('context', {}).get('concept_name', concept_id)
    
    step = {
        "step_id": step_plan['step_id'],
        "type": "video",
        "concept_ids": step_plan['concept_ids'],
        "eyebrow": concept_name,
        "title": "Video walkthrough",
        "lede": "",
        "blocks": [],
        "reward": None,
        "lineage": {
            "concept_ids": step_plan['concept_ids'],
            "teaching_block_ids": step_plan.get('teaching_block_ids', []),
            "fact_ids": step_plan.get('fact_ids', []),
            "segment_ids": step_plan.get('segment_ids', [])
        }
    }
    
    # Add media_group block
    if step_plan.get('segment_ids'):
        media_block = {
            "type": "media_group",
            "block_id": f"{step_plan['step_id']}.media",
            "segment_ids": step_plan['segment_ids'],
            "lineage": {
                "concept_ids": step_plan['concept_ids'],
                "segment_ids": step_plan['segment_ids']
            }
        }
        step['blocks'].append(media_block)
    
    return step

def generate_recap_step(step_plan, tile_plan, concepts, plans_data):
    """Generate recap step"""
    concept_ids = step_plan['concept_ids']
    
    step = {
        "step_id": step_plan['step_id'],
        "type": "recap",
        "concept_ids": concept_ids,
        "eyebrow": "Recap",
        "title": "What you learned",
        "lede": "",
        "blocks": [],
        "reward": None,
        "lineage": {
            "concept_ids": concept_ids,
            "teaching_block_ids": [],
            "fact_ids": []
        }
    }
    
    # Add takeaway blocks for each concept
    block_counter = 1
    for concept_id in concept_ids:
        concept = concepts.get(concept_id, {})
        concept_name = concept.get('context', {}).get('concept_name', concept_id)
        
        # Get key facts
        coverage = concept.get('coverage', {})
        facts = coverage.get('facts', [])
        
        if facts:
            takeaway_text = f"{concept_name}: " + " ".join([f['statement'] for f in facts[:2]])
            
            prose_block = {
                "type": "prose",
                "block_id": f"{step_plan['step_id']}.b{block_counter:02d}",
                "role": "takeaway",
                "text": takeaway_text[:150],  # Truncate if too long
                "lineage": {
                    "concept_ids": [concept_id],
                    "teaching_block_ids": [],
                    "fact_ids": [f"{concept_id}#{f['fact_id']}" for f in facts[:2]]
                }
            }
            step['blocks'].append(prose_block)
            block_counter += 1
    
    # Add up_next block
    next_tile_id = tile_plan.get('next_tile_id')
    if next_tile_id:
        # Find next tile in plans
        next_tile_title = "the next lesson"
        for tile in plans_data['tiles']:
            if tile['tile_id'] == next_tile_id:
                next_tile_title = tile.get('title', next_tile_id)
                break
        
        up_next_block = {
            "type": "up_next",
            "block_id": f"{step_plan['step_id']}.up_next",
            "next_tile_id": next_tile_id,
            "preview_text": f"Next: {next_tile_title}",
            "lineage": {
                "concept_ids": [],
                "teaching_block_ids": [],
                "fact_ids": []
            }
        }
        step['blocks'].append(up_next_block)
    
    return step

def generate_remediation_step(tile_id, concept_id, info, concepts, registry):
    """Generate a remediation step for a concept"""
    concept = concepts.get(concept_id, {})
    concept_name = concept.get('context', {}).get('concept_name', concept_id)
    
    # Generate remediation step ID
    # Count existing remediation steps for this concept
    step_id = f"{tile_id}.r01_{concept_id.split('.')[-1]}"
    
    step = {
        "step_id": step_id,
        "type": "remediation",
        "concept_ids": [concept_id],
        "eyebrow": concept_name,
        "title": "Let's review",
        "lede": "Here's another way to think about it.",
        "blocks": [],
        "reward": None,
        "lineage": {
            "concept_ids": [concept_id],
            "teaching_block_ids": [],
            "fact_ids": info['fact_ids']
        }
    }
    
    # Add a simple prose block re-teaching the facts
    facts = get_facts(concept, info['fact_ids'])
    if facts:
        remediation_text = "Remember: " + " ".join([f['statement'] for f in facts])
        
        prose_block = {
            "type": "prose",
            "block_id": f"{step_id}.b01",
            "role": "remediation",
            "text": remediation_text[:200],
            "lineage": {
                "concept_ids": [concept_id],
                "teaching_block_ids": [],
                "fact_ids": info['fact_ids']
            }
        }
        step['blocks'].append(prose_block)
    
    return step

if __name__ == '__main__':
    output = generate_screens()
    print(json.dumps(output, indent=2))
