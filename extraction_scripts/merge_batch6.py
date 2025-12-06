import json

# Load v36 database
with open('data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v36_FINAL.json', 'r') as f:
    db = json.load(f)

print(f'Current database: {len(db["positions"])} positions')

# Load all batch 6 extractions
batch_files = [
    'extraction_scripts/batch6_college_papers.json',
    'extraction_scripts/batch6_paradoxes.json',
    'extraction_scripts/batch6_ocd.json',
    'extraction_scripts/batch6_knowledge.json'
]

all_new_positions = []
for batch_file in batch_files:
    with open(batch_file, 'r') as f:
        positions = json.load(f)
        print(f'{batch_file}: {len(positions)} positions')
        all_new_positions.extend(positions)

print(f'\nTotal new positions: {len(all_new_positions)}')

# Convert format
for pos in all_new_positions:
    pos['position_id'] = pos.pop('id')
    pos['title'] = f"{pos['position_id']} Position"
    pos['thesis'] = pos.pop('text')
    pos['domain'] = pos.pop('topic')
    pos['consistency'] = 'N/A'
    pos['development'] = 'N/A'

# Merge
db['positions'].extend(all_new_positions)
db['database_metadata']['total_positions'] = len(db['positions'])
db['database_metadata']['version'] = 'v37_WITH_BATCH6'
db['database_metadata']['description'] = 'Kuczynski Philosophical Database v37 - Expanded to 3,516 positions through systematic extraction of 35+ philosophical works. Includes College Papers Plus (121 positions), 90 Paradoxes (62 positions), OCD and Philosophy (27 positions), and other epistemology/logic works. November 2025 extraction campaign continues.'
db['database_metadata']['last_updated'] = '2025-11-20'

# Save
with open('data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v37_WITH_BATCH6.json', 'w') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print(f'\n✅ Database merged successfully!')
print(f'   Final count: {len(db["positions"])} positions')
print(f'   Saved to: data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v37_WITH_BATCH6.json')
