import json

# Load current database
print("Loading current Kuczynski database...")
with open('data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v32_MERGED.json', 'r', encoding='utf-8') as f:
    db_structure = json.load(f)

current_db = db_structure['positions']
metadata = db_structure['database_metadata']
works_inventory = db_structure['works_inventory']

print(f"Current database: {len(current_db)} positions")
print(f"Database version: {metadata.get('version', 'unknown')}")

# Load all new batch files
batch_files = [
    'kuczynski_batch5_part1_mmse.json',
    'kuczynski_batch5_part2_lmcc.json',
    'kuczynski_batch5_part3_lspm.json',
    'kuczynski_batch4_part2_imr.json',
    'kuczynski_batch4_part3_khind.json',
    'kuczynski_batch4_part4_defdesc.json',
    'kuczynski_batch4_part5_abstr.json',
    'kuczynski_batch4_part6_intfound.json'
]

new_positions = []
for batch_file in batch_files:
    with open(batch_file, 'r', encoding='utf-8') as f:
        positions = json.load(f)
        new_positions.extend(positions)
        print(f"  Loaded {len(positions)} positions from {batch_file}")

print(f"\nTotal new positions to add: {len(new_positions)}")

# Rename 'id' to 'position_id' to match existing database format
print("\nConverting new positions to database format...")
for pos in new_positions:
    pos['position_id'] = pos.pop('id')  # Rename id -> position_id
    pos['title'] = f"{pos['position_id']} Position"
    pos['thesis'] = pos.pop('text')  # Rename text -> thesis
    pos['domain'] = pos.pop('topic')  # Rename topic -> domain
    pos['consistency'] = "N/A"  # Add required fields
    pos['development'] = "N/A"

print(f"✅ Converted {len(new_positions)} positions to database format")

# Merge
merged_positions = current_db + new_positions
print(f"\nMerged positions: {len(merged_positions)} total")
print(f"Added: {len(new_positions)} new positions")

# Update metadata
metadata['version'] = 'v33_EXPANDED'
metadata['total_positions'] = len(merged_positions)
metadata['latest_addition'] = f"Batch 4+5 extraction: +{len(new_positions)} positions from 8 works (Mind/Meaning/Science, Literal Meaning/Content, Logic/Set Theory, and 5 others)"

# Create new database structure
new_db_structure = {
    'database_metadata': metadata,
    'works_inventory': works_inventory,
    'positions': merged_positions
}

# Save merged database
output_file = 'data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v33_EXPANDED.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(new_db_structure, f, indent=2, ensure_ascii=False)

print(f"\n✅ Saved merged database to: {output_file}")
print(f"\n📊 DATABASE GROWTH:")
print(f"   Before: {len(current_db)} positions")
print(f"   After:  {len(merged_positions)} positions")
print(f"   Growth: +{len(new_positions)} positions ({len(new_positions)/len(current_db)*100:.1f}% increase)")
