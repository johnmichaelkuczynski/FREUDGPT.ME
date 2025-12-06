import json
import re

print("="*60)
print("EXTRACTING: ANALYTIC PHILOSOPHY COMPLETE")
print("="*60)

positions = []
position_id = 1

input_file = "attached_assets/Analytic Philosophy Complete_1763621003995.txt"
print(f"Processing: {input_file}\n")

with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and len(p.strip()) > 100]
print(f"Found {len(paragraphs)} paragraphs\n")

for para in paragraphs:
    # Skip headers, TOC, etc
    if re.match(r'^(Chapter|Part|Introduction|Section|\d+\.|Table of|References|Bibliography)', para):
        continue
    if len(para) < 150:
        continue
    if para.count('\n') < 2:
        continue
        
    indicators = ['thus', 'therefore', 'it follows', 'consequently', 'given', 
                 'this means', 'in other words', 'the reason', 'consider',
                 'argument', 'proof', 'theorem', 'principle', 'analysis',
                 'must be', 'cannot be', 'necessarily', 'it is clear',
                 'suppose', 'assume', 'if and only if', 'exactly if']
    
    has_indicator = any(ind in para.lower() for ind in indicators)
    
    if has_indicator or len(para) > 300:
        cleaned = para.replace('\n', ' ').strip()
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        words = cleaned.split()
        if len(words) > 400:
            cleaned = ' '.join(words[:400]) + '...'
        
        position = {
            "id": f"ANALPHIL-{position_id:03d}",
            "text": cleaned,
            "source": "Analytic Philosophy Complete",
            "topic": "Analytic Philosophy/Various",
            "keywords": []
        }
        
        positions.append(position)
        position_id += 1
        
        if position_id % 100 == 0:
            print(f"  Extracted {position_id} positions...")

# Save
output_file = "large_analytic_philosophy.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(positions, f, indent=2, ensure_ascii=False)

print(f"\n{'='*60}")
print(f"✅ ANALYTIC PHILOSOPHY EXTRACTION COMPLETE")
print(f"   Total positions: {len(positions)}")
print(f"   Saved to: {output_file}")
print(f"{'='*60}")
