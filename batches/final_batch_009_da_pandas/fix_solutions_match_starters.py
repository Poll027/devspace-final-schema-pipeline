import json

# Load the interactions file
with open('interactions.part.c3.json', 'r') as f:
    data = json.load(f)

# Fix solutions to match starters exactly for scaffolding
fixes = {
    'ix.tile_pandas_map_apply.s03': {
        'solution': '''import pandas as pd

orders = pd.read_csv('orders.csv')

city_lookup = {'LOS': 'Lagos', 'ABJ': 'Abuja', 'KAN': 'Kano'}

orders['city_name'] = orders['city_code'].map(city_lookup)

print(orders['city_name'])
'''
    },
    'ix.tile_pandas_map_apply.s07': {
        'solution': '''import pandas as pd

orders = pd.read_csv('orders.csv')

def label_speed(row):
    if row['delivery_time_minutes'] > 25:
        return 'slow'
    else:
        return 'fast'

orders['speed_label'] = orders.apply(label_speed, axis=1)

print(orders['speed_label'])
'''
    },
}

# Apply fixes
for tile in data['tiles']:
    for interaction_obj in tile['interactions']:
        ix_id = interaction_obj['interaction']['interaction_id']
        if ix_id in fixes:
            fix = fixes[ix_id]
            interaction = interaction_obj['interaction']
            
            # Update solution
            if 'solution' in fix:
                for sf in interaction.get('grading', {}).get('solution_files', []):
                    sf['content'] = fix['solution']

# Write back
with open('interactions.part.c3.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fixed solutions to match starters")
