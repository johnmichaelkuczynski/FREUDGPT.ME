import json
import re

def extract_positions(input_file, output_file, id_prefix, source_title, topic):
    """Generic extraction function for Batch 4 files"""
    
    positions = []
    position_id = 1
    
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and len(p.strip()) > 100]
    
    print(f"Processing {len(paragraphs)} paragraphs from {input_file}")
    
    for para in paragraphs:
        # Skip headers, TOC
        if re.match(r'^(Chapter|Part|Introduction|Section|\d+\.|Table of|References)', para):
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
                "id": f"{id_prefix}-{position_id:03d}",
                "text": cleaned,
                "source": source_title,
                "topic": topic,
                "keywords": []
            }
            
            positions.append(position)
            position_id += 1
            
            if position_id % 20 == 0:
                print(f"  Extracted {position_id} positions...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(positions, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Extracted {len(positions)} positions")
    return len(positions)

# Process all Batch 4 files
files = [
    ("attached_assets/KUCZYNSKI PHILOSOPHY OF MATHEMATICS_1763621600349.txt", 
     "kuczynski_batch4_part1_phmath.json", "PHMATH", 
     "Philosophy of Mathematics (selected papers)", "Logic/Mathematics/Set Theory"),
    
    ("attached_assets/Intensionality Modality and Rationality_1763621600351.txt",
     "kuczynski_batch4_part2_imr.json", "IMR",
     "Intensionality, Modality, and Rationality (2010)", "Semantics/Modality"),
    
    ("attached_assets/Kantanalogue-digital_1763621600353.txt",
     "kuczynski_batch4_part3_khind.json", "KHIND",
     "Kant and Hume on Induction, Causation (2014)", "Epistemology/Causation"),
    
    ("attached_assets/Kuczynski review of reimers on definite descriptions_1763621600350.txt",
     "kuczynski_batch4_part4_defdesc.json", "DEFDESC",
     "Review: Descriptions and Beyond (book review)", "Philosophy of Language"),
    
    ("attached_assets/KUCZYNSKI ABSTRACT_1763621600347.txt",
     "kuczynski_batch4_part5_abstr.json", "ABSTR",
     "Abstracts of Published Works (index)", "Various"),
    
    ("attached_assets/intentionalism and foundationalism_1763621600352.txt",
     "kuczynski_batch4_part6_intfound.json", "INTFOUND",
     "Intentionalism and Foundationalism (unpublished)", "Phenomenology/Epistemology")
]

total = 0
for input_file, output_file, prefix, source, topic in files:
    print(f"\n{'='*60}")
    print(f"Processing: {prefix}")
    print(f"{'='*60}")
    count = extract_positions(input_file, output_file, prefix, source, topic)
    total += count

print(f"\n{'='*60}")
print(f"🎯 BATCH 4 COMPLETE: {total} total positions extracted")
print(f"{'='*60}")
