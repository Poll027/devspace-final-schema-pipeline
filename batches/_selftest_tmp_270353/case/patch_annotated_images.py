#!/usr/bin/env python3
"""
Patch script to replace annotated_image blocks with diagram blocks.
The registry has no image assets, so we must use the allowed alternate: diagram.
"""
import json

def create_cross_sheet_diagram():
    """Create SVG diagram for cross-sheet reference syntax."""
    return {
        "type": "diagram",
        "block_id": "tile_spreadsheet_cleaning_cross_sheet.s09.img1",
        "svg": """<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg">
  <!-- Example 1: Simple cross-sheet reference -->
  <text x="50" y="40" font-size="16" font-weight="bold">Drivers!B1</text>
  <rect x="45" y="50" width="80" height="30" fill="none" stroke="#0066cc" stroke-width="2"/>
  <text x="50" y="70" font-size="12" fill="#0066cc">Sheet name</text>
  
  <rect x="125" y="50" width="15" height="30" fill="none" stroke="#00aa00" stroke-width="2"/>
  <text x="127" y="70" font-size="12" fill="#00aa00">!</text>
  
  <rect x="140" y="50" width="40" height="30" fill="none" stroke="#cc6600" stroke-width="2"/>
  <text x="145" y="70" font-size="12" fill="#cc6600">Cell</text>
  
  <line x1="65" y1="80" x2="65" y2="100" stroke="#0066cc" stroke-width="1"/>
  <text x="20" y="115" font-size="11" fill="#333">No spaces, no quotes needed</text>
  
  <line x1="132" y1="80" x2="132" y2="100" stroke="#00aa00" stroke-width="1"/>
  <text x="100" y="130" font-size="11" fill="#333">Separates sheet from cell</text>
  
  <line x1="160" y1="80" x2="160" y2="100" stroke="#cc6600" stroke-width="1"/>
  <text x="140" y="115" font-size="11" fill="#333">Cell address</text>
  
  <!-- Example 2: Sheet name with space -->
  <text x="50" y="180" font-size="16" font-weight="bold">'January Revenue'!A1</text>
  <rect x="45" y="190" width="150" height="30" fill="none" stroke="#0066cc" stroke-width="2"/>
  <text x="50" y="210" font-size="12" fill="#0066cc">Sheet name with quotes</text>
  
  <line x1="120" y1="220" x2="120" y2="240" stroke="#0066cc" stroke-width="1"/>
  <text x="30" y="255" font-size="11" fill="#333">Single quotes required when name contains space</text>
  
  <!-- Example 3: External workbook reference -->
  <text x="50" y="300" font-size="16" font-weight="bold">[Budget.xlsx]Annual!C10:C25</text>
  <rect x="45" y="310" width="110" height="30" fill="none" stroke="#9900cc" stroke-width="2"/>
  <text x="50" y="330" font-size="12" fill="#9900cc">Workbook name</text>
  
  <line x1="100" y1="340" x2="100" y2="360" stroke="#9900cc" stroke-width="1"/>
  <text x="30" y="375" font-size="11" fill="#333">Square brackets around external workbook name</text>
</svg>""",
        "caption": "Cross-sheet reference syntax: sheet name, exclamation point, then cell address. Single quotes wrap sheet names that contain spaces. External references include the workbook name in square brackets.",
        "lineage": {
            "concept_ids": ["spreadsheet.cross_sheet_references"],
            "teaching_block_ids": ["spreadsheet.cross_sheet_references#tb3"],
            "fact_ids": ["spreadsheet.cross_sheet_references#f3"],
            "anchors": ["spreadsheet.cross_sheet_references#visual"]
        }
    }

def create_sort_dialog_diagram():
    """Create SVG diagram for Excel Sort dialog with multi-level sort."""
    return {
        "type": "diagram",
        "block_id": "tile_spreadsheet_sorting_filtering.s01.img1",
        "svg": """<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg">
  <!-- Dialog box -->
  <rect x="50" y="30" width="500" height="340" fill="#f5f5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="70" y="60" font-size="18" font-weight="bold">Sort</text>
  
  <!-- Level 1 -->
  <rect x="70" y="90" width="460" height="60" fill="white" stroke="#666" stroke-width="1" rx="3"/>
  <text x="85" y="110" font-size="14" font-weight="bold">Level 1</text>
  
  <text x="85" y="130" font-size="12">Sort by:</text>
  <rect x="140" y="115" width="120" height="25" fill="white" stroke="#999" stroke-width="1" rx="2"/>
  <text x="150" y="133" font-size="12" font-weight="bold">order_date</text>
  
  <text x="280" y="130" font-size="12">Order:</text>
  <rect x="330" y="115" width="180" height="25" fill="white" stroke="#999" stroke-width="1" rx="2"/>
  <text x="340" y="133" font-size="12" font-weight="bold">Oldest to Newest</text>
  
  <line x1="200" y1="150" x2="200" y2="170" stroke="#0066cc" stroke-width="1"/>
  <text x="120" y="185" font-size="10" fill="#0066cc">Primary sort column</text>
  
  <!-- Level 2 -->
  <rect x="70" y="200" width="460" height="60" fill="white" stroke="#666" stroke-width="1" rx="3"/>
  <text x="85" y="220" font-size="14" font-weight="bold">Level 2</text>
  
  <text x="85" y="240" font-size="12">Then by:</text>
  <rect x="140" y="225" width="120" height="25" fill="white" stroke="#999" stroke-width="1" rx="2"/>
  <text x="150" y="243" font-size="12" font-weight="bold">amount</text>
  
  <text x="280" y="240" font-size="12">Order:</text>
  <rect x="330" y="225" width="180" height="25" fill="white" stroke="#999" stroke-width="1" rx="2"/>
  <text x="340" y="243" font-size="12" font-weight="bold">Largest to Smallest</text>
  
  <line x1="420" y1="150" x2="420" y2="170" stroke="#00aa00" stroke-width="1"/>
  <text x="340" y="185" font-size="10" fill="#00aa00">Independent direction</text>
  
  <line x1="420" y1="260" x2="420" y2="280" stroke="#00aa00" stroke-width="1"/>
  <text x="340" y="295" font-size="10" fill="#00aa00">Different direction for tiebreaker</text>
  
  <!-- Add Level button -->
  <rect x="70" y="280" width="100" height="30" fill="#e0e0e0" stroke="#999" stroke-width="1" rx="3"/>
  <text x="85" y="300" font-size="12">+ Add Level</text>
  
  <!-- OK/Cancel buttons -->
  <rect x="380" y="330" width="70" height="30" fill="#0066cc" stroke="#0066cc" stroke-width="1" rx="3"/>
  <text x="400" y="350" font-size="12" fill="white" font-weight="bold">OK</text>
  
  <rect x="460" y="330" width="70" height="30" fill="#e0e0e0" stroke="#999" stroke-width="1" rx="3"/>
  <text x="472" y="350" font-size="12">Cancel</text>
</svg>""",
        "caption": "Excel Sort dialog with two levels. Level 1 sorts by order_date (Oldest to Newest), Level 2 sorts by amount (Largest to Smallest) as a tiebreaker. Each level has its own independent Order setting.",
        "lineage": {
            "concept_ids": ["spreadsheet.sorting"],
            "teaching_block_ids": [
                "spreadsheet.sorting#tb1",
                "spreadsheet.sorting#tb2",
                "spreadsheet.sorting#tb3"
            ],
            "fact_ids": [
                "spreadsheet.sorting#f1",
                "spreadsheet.sorting#f2",
                "spreadsheet.sorting#f3",
                "spreadsheet.sorting#f4"
            ],
            "anchors": ["spreadsheet.sorting#visual"]
        }
    }

def main():
    # Read the screens file
    with open('batches/final_batch_011_da_spreadsheet/screens.part.c2.json', 'r') as f:
        data = json.load(f)
    
    # Find and replace the annotated_image blocks
    replacements_made = 0
    
    for tile in data['tiles']:
        for step in tile['steps']:
            if 'blocks' not in step:
                continue
            
            for i, block in enumerate(step['blocks']):
                if block.get('type') == 'annotated_image':
                    block_id = block['block_id']
                    
                    if block_id == 'tile_spreadsheet_cleaning_cross_sheet.s09.img1':
                        step['blocks'][i] = create_cross_sheet_diagram()
                        replacements_made += 1
                        print(f"✓ Replaced {block_id} with diagram")
                    
                    elif block_id == 'tile_spreadsheet_sorting_filtering.s01.img1':
                        step['blocks'][i] = create_sort_dialog_diagram()
                        replacements_made += 1
                        print(f"✓ Replaced {block_id} with diagram")
    
    # Write the patched file
    with open('batches/final_batch_011_da_spreadsheet/screens.part.c2.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\nTotal replacements: {replacements_made}")
    print("Patched file written successfully.")

if __name__ == '__main__':
    main()
