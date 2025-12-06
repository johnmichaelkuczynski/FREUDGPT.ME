import json

# Load current database (v34)
print("Loading v34 database...")
with open('data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v34_MEDIUM_FILES.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

current_positions = db['positions']
print(f"Current: {len(current_positions)} positions")

# Load Analytic Philosophy
with open('large_analytic_philosophy.json', 'r') as f:
    new_positions = json.load(f)
    print(f"Loaded {len(new_positions)} from Analytic Philosophy")

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
db['database_metadata']['version'] = 'v35_WITH_ANALYTIC_PHIL'
db['database_metadata']['latest_addition'] = f"Analytic Philosophy Complete: +{len(new_positions)} positions on various analytic philosophy topics"

# Save
with open('data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v35_WITH_ANALYTIC_PHIL.json', 'w') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print(f"\n✅ Merged! {len(current_positions)} → {len(merged)} (+{len(new_positions)})")
print(f"Saved to: data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v35_WITH_ANALYTIC_PHIL.json")
print(f"\n🎉 3,000 MILESTONE: {'ACHIEVED!' if len(merged) >= 3000 else 'NOT YET...'}")
print(f"   Current: {len(merged)} positions")
print(f"   Progress: {len(merged)/10000*100:.1f}% to 10k goal")
