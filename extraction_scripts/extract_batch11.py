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
        'language', 'semantic', 'syntax', 'grammar', 'meaning', 'truth',
        'recursion', 'expression', 'formal', 'logic'
    ]
    
    for para in paragraphs:
        para_clean = para.strip()
        
        if len(para_clean) < 100:
            continue
        
        if para_clean.startswith('﻿'):
            para_clean = para_clean[1:]
        
        if any(header in para_clean[:80] for header in ['Table of Contents', 'Chapter', 'Section', 'Volume', 'FREUD INSTITUTE', 'https://']):
            continue
        
        if re.match(r'^\d+(\.\d+)*\s', para_clean):
            para_clean = re.sub(r'^\d+(\.\d+)*\s+', '', para_clean)
        
        para_lower = para_clean.lower()
        if any(indicator in para_lower for indicator in argumentative_indicators):
            if len(para_clean) >= 100:
                positions.append(para_clean)
                position_counter += 1
    
    return positions

print("=" * 60)
print("BATCH 11 EXTRACTION: 4 KUCZYNSKI WORKS")
print("=" * 60)

files = [
    {
        "file_path": "attached_assets/OCD, Bureaucracy and Psychopathy_ Volume 1_1763740381312.txt",
        "prefix": "OCDBUREAU-",
        "name": "OCD, Bureaucracy and Psychopathy Volume 1",
        "topics": "Psychopathology, OCD, Bureaucracy, Political Philosophy"
    },
    {
        "file_path": "attached_assets/What is a Formal Language_1763740381313.txt",
        "prefix": "FORMLANG-",
        "name": "What is a Formal Language?",
        "topics": "Philosophy of Language, Formal Semantics, Logic"
    },
    {
        "file_path": "attached_assets/One Way to Get Over Writer_s Block_ With Link to Video Version of Book_1763740381314.txt",
        "prefix": "WRITER-",
        "name": "One Way to Get Over Writer's Block",
        "topics": "Philosophy of Mind, Creativity"
    },
    {
        "file_path": "attached_assets/knowledge of past possible future_1763740381315.txt",
        "prefix": "KNOWTIME-",
        "name": "Knowledge of Past, Possible, and Future",
        "topics": "Epistemology, Modal Logic, Causation"
    }
]

all_positions = []
file_counts = {}

for file_info in files:
    print(f"\nProcessing: {file_info['name']}")
    print(f"File: {file_info['file_path']}")
    
    try:
        raw_positions = extract_positions_from_file(file_info['file_path'], file_info['prefix'])
        
        # Create properly formatted positions with metadata
        formatted_positions = []
        for i, text in enumerate(raw_positions, 1):
            position_id = f"{file_info['prefix']}{i:04d}"
            formatted_positions.append({
                "position_id": position_id,
                "text": text,
                "metadata": {
                    "source": file_info['name'],
                    "topic": file_info['topics'],
                    "extraction_batch": "batch11"
                }
            })
        
        all_positions.extend(formatted_positions)
        file_counts[file_info['name']] = len(formatted_positions)
        print(f"✓ Extracted {len(formatted_positions)} positions")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        file_counts[file_info['name']] = 0

output_file = "extraction_scripts/batch11_all.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_positions, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 60)
print("BATCH 11 EXTRACTION COMPLETE")
print("=" * 60)
print(f"Total positions extracted: {len(all_positions)}")
print("\nBreakdown by file:")
for name, count in file_counts.items():
    print(f"  - {name}: {count}")
print(f"\nSaved to: {output_file}")
print("=" * 60)
