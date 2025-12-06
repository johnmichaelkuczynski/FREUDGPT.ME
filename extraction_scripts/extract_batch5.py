import json
import re

def extract_positions_mmse(input_file, output_file, id_prefix="MMSE"):
    """Extract philosophical positions from Mind, Meaning & Scientific Explanation"""
    
    positions = []
    position_id = 1
    
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Split into paragraphs
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and len(p.strip()) > 100]
    
    print(f"Processing {len(paragraphs)} paragraphs from {input_file}")
    
    # Extract positions from substantive paragraphs
    for para in paragraphs:
        # Skip table of contents, headers, page numbers
        if re.match(r'^(Chapter|Part|Introduction|Section|\d+\.)', para):
            continue
        if len(para) < 150:  # Skip very short paragraphs
            continue
        if para.count('\n') < 2:  # Skip single-line entries
            continue
            
        # Look for argumentative/theoretical content
        indicators = ['thus', 'therefore', 'it follows', 'consequently', 'given', 
                     'this means', 'in other words', 'the reason', 'consider',
                     'argument', 'proof', 'theorem', 'principle', 'analysis',
                     'must be', 'cannot be', 'necessarily', 'it is clear',
                     'suppose', 'assume', 'if and only if', 'exactly if']
        
        has_indicator = any(ind in para.lower() for ind in indicators)
        
        if has_indicator or len(para) > 300:
            # Clean up the text
            cleaned = para.replace('\n', ' ').strip()
            cleaned = re.sub(r'\s+', ' ', cleaned)
            
            # Truncate if too long (max ~400 words)
            words = cleaned.split()
            if len(words) > 400:
                cleaned = ' '.join(words[:400]) + '...'
            
            position = {
                "id": f"{id_prefix}-{position_id:03d}",
                "text": cleaned,
                "source": "Mind, Meaning & Scientific Explanation (2018)",
                "topic": "Philosophy of Mind/Science/Language",
                "keywords": []
            }
            
            positions.append(position)
            position_id += 1
            
            # Progress update
            if position_id % 20 == 0:
                print(f"  Extracted {position_id} positions...")
    
    # Save to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(positions, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Extracted {len(positions)} positions from {input_file}")
    print(f"   Saved to: {output_file}")
    return len(positions)

if __name__ == "__main__":
    count = extract_positions_mmse(
        "attached_assets/Mind, Meaning & Scientific Explanation_1763667661349.txt",
        "kuczynski_batch5_part1_mmse.json",
        "MMSE"
    )
    print(f"\n🎯 Total positions extracted: {count}")
