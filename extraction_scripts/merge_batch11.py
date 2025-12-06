import json
from datetime import datetime

print("=" * 60)
print("MERGING BATCH 11 INTO v42 DATABASE")
print("=" * 60)

with open('data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v41_WITH_BATCH10.json', 'r', encoding='utf-8') as f:
    database = json.load(f)

print(f"\nLoaded v41 database: {len(database['positions'])} positions")

with open('extraction_scripts/batch11_all.json', 'r', encoding='utf-8') as f:
    new_positions = json.load(f)

database['positions'].extend(new_positions)
total_added = len(new_positions)

database['database_metadata']['version'] = 'v42_WITH_BATCH11'
database['database_metadata']['last_updated'] = datetime.now().isoformat()
database['database_metadata']['total_positions'] = len(database['positions'])

if 'extraction_batches' not in database['database_metadata']:
    database['database_metadata']['extraction_batches'] = []

database['database_metadata']['extraction_batches'].append({
    'batch_number': 11,
    'date': datetime.now().isoformat(),
    'positions_added': total_added,
    'works': [
        {
            'title': 'OCD, Bureaucracy and Psychopathy Volume 1',
            'positions': 37,
            'topics': ['Psychopathology', 'OCD', 'Bureaucracy', 'Political Philosophy']
        },
        {
            'title': 'What is a Formal Language?',
            'positions': 10,
            'topics': ['Philosophy of Language', 'Formal Semantics', 'Logic']
        },
        {
            'title': 'One Way to Get Over Writer\'s Block',
            'positions': 1,
            'topics': ['Philosophy of Mind', 'Creativity']
        },
        {
            'title': 'Knowledge of Past, Possible, and Future',
            'positions': 0,
            'topics': ['Epistemology', 'Modal Logic', 'Causation']
        }
    ]
})

output_file = 'data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v42_WITH_BATCH11.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(database, f, indent=2, ensure_ascii=False)

print(f"\n{'=' * 60}")
print(f"v42 DATABASE CREATED")
print(f"{'=' * 60}")
print(f"Previous positions (v41): {len(database['positions']) - total_added}")
print(f"New positions (Batch 11): {total_added}")
print(f"Total positions (v42): {len(database['positions'])}")
print(f"Saved to: {output_file}")
print(f"{'=' * 60}")
