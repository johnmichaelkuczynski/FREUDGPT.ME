import json
import re
import os

def parse_positions(filepath):
    """Parse numbered position statements from file."""
    positions = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    pos_id = 1
    
    for line in lines:
        line = line.strip()
        match = re.match(r'^\d+\.\s+(.+)$', line)
        if match:
            statement = match.group(1).strip()
            if len(statement) >= 20:
                positions.append({
                    'position_id': f'ZHI-{pos_id:05d}',
                    'text': statement,
                    'domain': 'philosophy',
                    'work': 'Collected Works',
                    'year': 2024
                })
                pos_id += 1
    
    return positions

def main():
    input_file = 'data/kuczynski_positions_raw.txt'
    output_file = 'data/kuczynski_positions_v2.json'
    
    positions = parse_positions(input_file)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(positions, f, indent=2, ensure_ascii=False)
    
    print(f"Parsed {len(positions)} positions")
    print(f"Saved to {output_file}")
    
    # Show sample
    for p in positions[:3]:
        print(f"  {p['position_id']}: {p['text'][:60]}...")

if __name__ == '__main__':
    main()
