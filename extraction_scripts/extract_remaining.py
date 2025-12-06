import json
import re

def extract_positions(input_file, output_file, id_prefix, source_title, topic):
    """Extract positions from remaining files"""
    
    positions = []
    position_id = 1
    
    print(f"\n{'='*60}")
    print(f"Processing: {id_prefix} - {input_file}")
    print(f"{'='*60}")
    
    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"⚠️  File not found, skipping...")
        return 0
    
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and len(p.strip()) > 100]
    print(f"Found {len(paragraphs)} paragraphs")
    
    for para in paragraphs:
        if re.match(r'^(Chapter|Part|Introduction|Section|\d+\.|Table of|References)', para):
            continue
        if len(para) < 150:
            continue
        if para.count('\n') < 2:
            continue
            
        indicators = ['thus', 'therefore', 'it follows', 'consequently', 'given', 
                     'this means', 'the reason', 'consider', 'argument',
                     'must be', 'cannot be', 'necessarily', 'suppose', 'assume']
        
        has_indicator = any(ind in para.lower() for ind in indicators)
        
        if has_indicator or len(para) > 300:
            cleaned = para.replace('\n', ' ').strip()
            cleaned = re.sub(r'\s+', ' ', cleaned)
            
            words = cleaned.split()
            if len(words) > 400:
                cleaned = ' '.join(words[:400]) + '...'
            
            position = {
                "id": f"{id_prefix}-{position_id:03d}",
                "text": cleaned,
                "source": source_title,
                "topic": topic,
                "keywords": []
            }
            
            positions.append(position)
            position_id += 1
            
            if position_id % 50 == 0:
                print(f"  Extracted {position_id} positions...")
    
    if positions:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(positions, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Extracted {len(positions)} positions")
    else:
        print(f"\n⚠️  0 positions extracted")
    
    return len(positions)

# Files to process - using grep results to find exact names
files = [
    ("attached_assets/COMPLETE BOOK ON INCOMPLETENESS OF DEDUCTIVE LOGIC_1763621131059.txt",
     "remaining_incompleteness.json", "INCOMP",
     "Complete Book on Incompleteness of Deductive Logic", "Logic/Mathematics"),
    
    ("attached_assets/FOR INGRAM INCOMPLETENESS BOOK_1763621448537.txt",
     "remaining_ingram.json", "INGRAM",
     "FOR INGRAM: Incompleteness Book", "Logic/Mathematics"),
    
    ("attached_assets/Ask Me Anything about Psychopathy!_ With Link to Video Version of Book!(1)_1763621003996.txt",
     "remaining_psychopathy.json", "PSYCHQA",
     "Psychopathy Q&A (Ask Me Anything)", "Psychology/Psychopathology")
]

total = 0
for input_file, output_file, prefix, source, topic in files:
    count = extract_positions(input_file, output_file, prefix, source, topic)
    total += count

print(f"\n{'='*60}")
print(f"🎯 REMAINING FILES COMPLETE: {total} total positions")
print(f"{'='*60}")
