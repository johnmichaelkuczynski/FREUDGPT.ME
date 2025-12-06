import json

# Load v38 database
with open('data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v38_WITH_BATCH7.json', 'r') as f:
    db = json.load(f)

print(f'Current database: {len(db["positions"])} positions')

# Load all batch 8 extractions
batch_files = [
    'extraction_scripts/batch8_quantifiers.json',
    'extraction_scripts/batch8_economics.json',
    'extraction_scripts/batch8_mormon.json',
    'extraction_scripts/batch8_modal.json'
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
db['database_metadata']['version'] = 'v39_WITH_BATCH8'
db['database_metadata']['description'] = 'Kuczynski Philosophical Database v39 - Expanded to 3,893 positions through systematic extraction of 42+ philosophical works. Latest batch adds quantifier analysis (39), modal logic critique (114), Mormon theology (3), and economics (1). November 2025 extraction campaign continues toward 10k goal.'
db['database_metadata']['last_updated'] = '2025-11-21'

# Save
with open('data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v39_WITH_BATCH8.json', 'w') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print(f'\n✅ Database merged successfully!')
print(f'   Final count: {len(db["positions"])} positions')
print(f'   Saved to: data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v39_WITH_BATCH8.json')
