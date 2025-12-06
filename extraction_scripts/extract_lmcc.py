import json
import re

def extract_positions_lmcc(input_file, output_file, id_prefix="LMCC"):
    """Extract from Literal Meaning & Cognitive Content"""
    
    positions = []
    position_id = 1
    
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and len(p.strip()) > 100]
    
    print(f"Processing {len(paragraphs)} paragraphs from {input_file}")
    
    for para in paragraphs:
        if re.match(r'^(Chapter|Part|Introduction|Section|\d+\.)', para):
            continue
        if len(para) < 150:
            continue
        if para.count('\n') < 2:
            continue
            
        indicators = ['thus', 'therefore', 'it follows', 'consequently', 'given', 
                     'this means', 'in other words', 'the reason', 'consider',
                     'argument', 'proof', 'theorem', 'principle', 'analysis',
                     'must be', 'cannot be', 'necessarily', 'it is clear',
                     'suppose', 'assume', 'if and only if', 'exactly if',
                     'reference', 'meaning', 'proposition', 'semantic', 'truth-value']
        
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
                "source": "Literal Meaning and Cognitive Content (unpublished)",
                "topic": "Philosophy of Language/Semantics",
                "keywords": []
            }
            
            positions.append(position)
            position_id += 1
            
            if position_id % 20 == 0:
                print(f"  Extracted {position_id} positions...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(positions, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Extracted {len(positions)} positions from {input_file}")
    print(f"   Saved to: {output_file}")
    return len(positions)

if __name__ == "__main__":
    count = extract_positions_lmcc(
        "attached_assets/Literal Meaning _ Cognitive Content_1763667661350.txt",
        "kuczynski_batch5_part2_lmcc.json",
        "LMCC"
    )
    print(f"\n🎯 Total positions extracted: {count}")
