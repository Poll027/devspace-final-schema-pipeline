#!/usr/bin/env python3
"""Make the solution match the starter exactly for data definitions."""

import json

# Files to patch
files_to_patch = ['interactions.part.c0_canary.json', 'interactions.json']

for filename in files_to_patch:
    print(f"\nPatching {filename}...")
    
    with open(filename, 'r') as f:
        data = json.load(f)

    for tile in data['tiles']:
        if tile['tile_id'] == 'tile_pandas_dataframe_reading':
            for item in tile['interactions']:
                ix = item['interaction']
                
                # Fix s05: Make solution match starter exactly
                if ix['interaction_id'] == 'ix.tile_pandas_dataframe_reading.s05':
                    # Get the starter content
                    starter_content = ix['public']['workspace']['files'][0]['content']
                    
                    # The solution should be: starter content with TODOs replaced by actual code
                    solution_content = starter_content.replace(
                        "# TODO: Create a Series from delivery_times and print it",
                        "# Create a Series from delivery_times and print it\ns = pd.Series(delivery_times)\nprint(s)"
                    ).replace(
                        "# TODO: Create a DataFrame from data and print it",
                        "# Create a DataFrame from data and print it\ndf = pd.DataFrame(data)\nprint(df)"
                    ).replace(
                        "# TODO: Pull out the 'delivery_time_minutes' column and print its type",
                        "# Pull out the 'delivery_time_minutes' column and print its type\ncol = df['delivery_time_minutes']\nprint(type(col))"
                    )
                    
                    for sf in ix['grading']['solution_files']:
                        if sf['path'] == 'starter.py':
                            sf['content'] = solution_content
                            print(f"  Fixed {ix['interaction_id']}: Solution matches starter")
                
                # Fix s10: Make solution match starter exactly
                elif ix['interaction_id'] == 'ix.tile_pandas_dataframe_reading.s10':
                    # Get the starter content
                    starter_content = ix['public']['workspace']['files'][0]['content']
                    
                    # The solution should be: starter content with TODO replaced by actual code
                    solution_content = starter_content.replace(
                        "# TODO: Load the CSV file and print the DataFrame",
                        "# Load the CSV file and print the DataFrame\norders = pd.read_csv(file_path)\nprint(orders)"
                    )
                    
                    for sf in ix['grading']['solution_files']:
                        if sf['path'] == 'starter.py':
                            sf['content'] = solution_content
                            print(f"  Fixed {ix['interaction_id']}: Solution matches starter")

    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

print("\nPatching complete!")
