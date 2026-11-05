#!/usr/bin/env python3
"""Fix choice interaction schema issues in interactions.part.c3.json"""
import json

# Read the artifact
with open('batches/final_batch_009_da_pandas/interactions.part.c3.json', 'r') as f:
    data = json.load(f)

# Fix all choice interactions
for tile in data['tiles']:
    for interaction_entry in tile['interactions']:
        interaction = interaction_entry['interaction']
        if interaction.get('type') == 'choice':
            public = interaction.get('public', {})
            grading = interaction.get('grading', {})
            feedback = interaction.get('feedback', {})
            
            # Add missing 'selection' field
            if 'selection' not in public:
                public['selection'] = 'single'
            
            # Rename 'label' to 'text' in all options
            for opt in public.get('options', []):
                if 'label' in opt and 'text' not in opt:
                    opt['text'] = opt.pop('label')
            
            # Convert 'correct_answer' to 'correct_option_ids'
            if 'correct_answer' in grading and 'correct_option_ids' not in grading:
                grading['correct_option_ids'] = [grading.pop('correct_answer')]
            
            # Move per-option feedback from feedback.incorrect to grading.option_feedback
            if 'incorrect' in feedback and isinstance(feedback['incorrect'], dict):
                incorrect = feedback['incorrect']
                # Check if it has option-specific feedback (keys like 'a', 'b', 'c', 'd')
                if any(k in incorrect for k in ['a', 'b', 'c', 'd', 'opt_a', 'opt_b', 'opt_c', 'opt_d']):
                    # Move to grading.option_feedback
                    if 'option_feedback' not in grading:
                        grading['option_feedback'] = {}
                    
                    # Collect all option-specific messages
                    for opt_id, opt_feedback in list(incorrect.items()):
                        if isinstance(opt_feedback, dict) and 'message' in opt_feedback:
                            grading['option_feedback'][opt_id] = opt_feedback
                    
                    # Replace feedback.incorrect with a general message
                    # Use the first incorrect option's message as a fallback
                    general_message = "Not quite. Review the concept and try again."
                    for opt_id in incorrect:
                        if isinstance(incorrect[opt_id], dict) and 'message' in incorrect[opt_id]:
                            general_message = "Not quite. Review how the operation works."
                            break
                    
                    feedback['incorrect'] = {'message': general_message}

# Write back
with open('batches/final_batch_009_da_pandas/interactions.part.c3.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Fixed choice interaction schema issues")
