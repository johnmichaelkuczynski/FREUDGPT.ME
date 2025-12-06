import json

# Load v39 database
with open('data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v39_WITH_BATCH8.json', 'r') as f:
    db = json.load(f)

print(f'Current database: {len(db["positions"])} positions')

# Load all batch 9 extractions
batch_files = [
    'extraction_scripts/batch9_legal.json',
    'extraction_scripts/batch9_zhi.json',
    'extraction_scripts/batch9_sorites.json',
    'extraction_scripts/batch9_bpd.json',
    'extraction_scripts/batch9_psycho.json'
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
db['database_metadata']['version'] = 'v40_WITH_BATCH9'
db['database_metadata']['description'] = 'Kuczynski Philosophical Database v40 - Expanded to 4,337 positions through systematic extraction of 47+ philosophical works. Latest batch adds ZHI Systems Journal (324), Legal Philosophy (99), Sorites analysis (18), and Psychopathology (3). November 2025 extraction campaign reaches 43.4% of 10k goal.'
db['database_metadata']['last_updated'] = '2025-11-21'

# Save
with open('data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v40_WITH_BATCH9.json', 'w') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print(f'\n✅ Database merged successfully!')
print(f'   Final count: {len(db["positions"])} positions')
print(f'   Saved to: data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v40_WITH_BATCH9.json')
