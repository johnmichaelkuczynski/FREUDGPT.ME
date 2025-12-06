import json
from datetime import datetime

print("=" * 60)
print("MERGING BATCH 10 INTO v41 DATABASE")
print("=" * 60)

with open('data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v40_WITH_BATCH9.json', 'r', encoding='utf-8') as f:
    database = json.load(f)

print(f"\nLoaded v40 database: {len(database['positions'])} positions")

batch10_files = [
    'extraction_scripts/batch10_rational.json'
]

total_added = 0

for batch_file in batch10_files:
    try:
        with open(batch_file, 'r', encoding='utf-8') as f:
            new_positions = json.load(f)
        
        database['positions'].extend(new_positions)
        total_added += len(new_positions)
        print(f"✓ Added {len(new_positions)} positions from {batch_file}")
    except Exception as e:
        print(f"✗ Error loading {batch_file}: {e}")

database['database_metadata']['version'] = 'v41_WITH_BATCH10'
database['database_metadata']['last_updated'] = datetime.now().isoformat()
database['database_metadata']['total_positions'] = len(database['positions'])

if 'extraction_batches' not in database['database_metadata']:
    database['database_metadata']['extraction_batches'] = []

database['database_metadata']['extraction_batches'].append({
    'batch_number': 10,
    'date': datetime.now().isoformat(),
    'positions_added': total_added,
    'works': [
        {
            'title': 'How is Rationalization Possible? Philosophy Shorts Volume 34',
            'positions': 59,
            'topics': ['Philosophy of Mind', 'Psychoanalysis', 'Epistemology', 'Self-Deception', 'Repression']
        }
    ]
})

output_file = 'data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v41_WITH_BATCH10.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(database, f, indent=2, ensure_ascii=False)

print(f"\n{'=' * 60}")
print(f"v41 DATABASE CREATED")
print(f"{'=' * 60}")
print(f"Previous positions (v40): {len(database['positions']) - total_added}")
print(f"New positions (Batch 10): {total_added}")
print(f"Total positions (v41): {len(database['positions'])}")
print(f"Saved to: {output_file}")
print(f"{'=' * 60}")
