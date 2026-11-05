import json

# Load the interactions file
with open('interactions.part.c3.json', 'r') as f:
    data = json.load(f)

# Fix ix.tile_pandas_map_apply.s03 - don't redefine the dict
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_pandas_map_apply':
        for interaction_obj in tile['interactions']:
            if interaction_obj['interaction']['interaction_id'] == 'ix.tile_pandas_map_apply.s03':
                interaction = interaction_obj['interaction']
                
                # Update solution to not redefine the dict
                for sf in interaction.get('grading', {}).get('solution_files', []):
                    sf['content'] = '''import pandas as pd

orders = pd.read_csv('orders.csv')

city_lookup = {'LOS': 'Lagos', 'ABJ': 'Abuja', 'KAN': 'Kano'}

orders['city_name'] = orders['city_code'].map(city_lookup)

print(orders['city_name'])
'''
                
                # Remove 'lit_str' from allowed_syntax if it was added
                allowed = interaction['public']['constraints'].get('allowed_syntax', [])
                if 'lit_str' in allowed:
                    allowed.remove('lit_str')
                interaction['public']['constraints']['allowed_syntax'] = allowed

# Write back
with open('interactions.part.c3.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fixed ix.tile_pandas_map_apply.s03")
