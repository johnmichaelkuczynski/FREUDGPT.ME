import json

# Load current database (v33b)
print("Loading v33b database...")
with open('data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v33b_WITH_BATCH23.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

current_positions = db['positions']
print(f"Current: {len(current_positions)} positions")

# Load medium files
batch_files = [
    'medium_conception_causation.json',
    'medium_conceptual_atomism.json'
]

new_positions = []
for batch_file in batch_files:
    with open(batch_file, 'r') as f:
        positions = json.load(f)
        new_positions.extend(positions)
        print(f"  Loaded {len(positions)} from {batch_file}")

print(f"\nNew positions to add: {len(new_positions)}")

# Convert format
for pos in new_positions:
    pos['position_id'] = pos.pop('id')
    pos['title'] = f"{pos['position_id']} Position"
    pos['thesis'] = pos.pop('text')
    pos['domain'] = pos.pop('topic')
    pos['consistency'] = "N/A"
    pos['development'] = "N/A"

# Merge
merged = current_positions + new_positions
db['positions'] = merged
db['database_metadata']['total_positions'] = len(merged)
db['database_metadata']['version'] = 'v34_MEDIUM_FILES'

# Save
with open('data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v34_MEDIUM_FILES.json', 'w') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print(f"\n✅ Merged! {len(current_positions)} → {len(merged)} (+{len(new_positions)})")
print(f"Saved to: data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v34_MEDIUM_FILES.json")
print(f"\n🎯 MILESTONE STATUS: {len(merged)}/3,000 ({len(merged)/3000*100:.1f}%)")
