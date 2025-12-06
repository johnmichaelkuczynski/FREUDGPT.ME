import json
from datetime import datetime

print("=" * 60)
print("CONSOLIDATING ALL FREUD DATABASES INTO UNIFIED DATABASE")
print("=" * 60)

all_positions = []
position_ids_seen = set()
duplicates_skipped = 0

databases = [
    ('Primary', 'data/FREUD_DATABASE.json'),
    ('Extended', 'data/FREUD_DATABASE_v9.json'),
    ('Extracted', 'data/FREUD_DATABASE_v10.json')
]

for name, filepath in databases:
    print(f"\nLoading {name} database from {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    positions = data.get('positions', [])
    added = 0
    
    for pos in positions:
        pos_id = pos.get('position_id', pos.get('id', ''))
        if pos_id and pos_id not in position_ids_seen:
            position_ids_seen.add(pos_id)
            all_positions.append(pos)
            added += 1
        else:
            duplicates_skipped += 1
    
    print(f"  Added {added} positions from {name}")

print(f"\n{'=' * 60}")
print(f"Duplicates skipped: {duplicates_skipped}")
print(f"Total unique positions: {len(all_positions)}")

unified_database = {
    'metadata': {
        'name': 'Freud Unified Database',
        'version': 'unified_v1',
        'created': datetime.now().isoformat(),
        'description': 'Consolidated Freud database combining Primary (3792), Extended (2328), and Extracted (271) collections',
        'total_positions': len(all_positions),
        'sources': [
            {'name': 'Primary', 'file': 'FREUD_DATABASE.json', 'positions': 3792},
            {'name': 'Extended', 'file': 'FREUD_DATABASE_v9.json', 'positions': 2328},
            {'name': 'Extracted', 'file': 'FREUD_DATABASE_v10.json', 'positions': 271}
        ]
    },
    'positions': all_positions
}

output_file = 'data/FREUD_DATABASE_UNIFIED.json'
print(f"\nSaving unified database to {output_file}...")
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(unified_database, f, indent=2, ensure_ascii=False)

print(f"\n{'=' * 60}")
print(f"UNIFIED FREUD DATABASE CREATED")
print(f"{'=' * 60}")
print(f"Total positions: {len(all_positions)}")
print(f"Expected: 6391 (3792 + 2328 + 271)")
print(f"Match: {'YES' if len(all_positions) == 6391 else 'NO - check for duplicates'}")
print(f"Saved to: {output_file}")
print(f"{'=' * 60}")
