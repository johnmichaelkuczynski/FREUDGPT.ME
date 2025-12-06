import json
import re

def extract_positions_from_file(file_path, position_prefix):
    """Extract philosophical positions from a text file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    paragraphs = content.split('\n\n')
    
    positions = []
    position_counter = 1
    
    argumentative_indicators = [
        'therefore', 'thus', 'hence', 'consequently', 'it follows',
        'because', 'since', 'given that', 'suppose', 'assume',
        'if', 'then', 'implies', 'entails', 'proves', 'shows',
        'demonstrates', 'establishes', 'argument', 'claim', 'thesis',
        'proposition', 'conclusion', 'premise', 'evidence', 'reason',
        'moreover', 'furthermore', 'in addition', 'however', 'but',
        'nevertheless', 'although', 'whereas', 'contrast', 'contrary',
        'fallacy', 'error', 'mistake', 'wrong', 'correct', 'true', 'false',
        'must', 'cannot', 'necessary', 'sufficient', 'condition',
        'definition', 'concept', 'notion', 'idea', 'belief', 'knowledge',
        'conscious', 'unconscious', 'repression', 'self-deception',
        'rationalization', 'mental', 'psychological', 'cognitive'
    ]
    
    for para in paragraphs:
        para_clean = para.strip()
        
        if len(para_clean) < 100:
            continue
        
        if para_clean.startswith('﻿'):
            para_clean = para_clean[1:]
        
        if any(header in para_clean[:50] for header in ['Philosophy Shorts', 'Volume', 'Table of Contents', 'Chapter', 'Section']):
            continue
        
        if re.match(r'^\d+(\.\d+)*\s', para_clean):
            para_clean = re.sub(r'^\d+(\.\d+)*\s+', '', para_clean)
        
        para_lower = para_clean.lower()
        if any(indicator in para_lower for indicator in argumentative_indicators):
            if len(para_clean) >= 100:
                position_id = f"{position_prefix}{position_counter:04d}"
                
                positions.append({
                    "position_id": position_id,
                    "text": para_clean,
                    "metadata": {
                        "source": "How is Rationalization Possible? Philosophy Shorts Volume 34",
                        "topic": "Philosophy of Mind, Psychoanalysis, Epistemology",
                        "extraction_batch": "batch10"
                    }
                })
                position_counter += 1
    
    return positions

print("=" * 60)
print("BATCH 10 EXTRACTION: RATIONALIZATION")
print("=" * 60)

file_info = {
    "file_path": "attached_assets/How is Rationalization Possible__ Philosophy Shorts Volume 34_1763712024396.txt",
    "prefix": "RATIONAL-",
    "name": "How is Rationalization Possible"
}

print(f"\nProcessing: {file_info['name']}")
print(f"File: {file_info['file_path']}")

try:
    positions = extract_positions_from_file(file_info['file_path'], file_info['prefix'])
    print(f"✓ Extracted {len(positions)} positions")
    
    output_file = f"extraction_scripts/batch10_{file_info['prefix'].replace('-', '').lower()}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(positions, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved to {output_file}")
    
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 60)
print("BATCH 10 EXTRACTION COMPLETE")
print("=" * 60)
