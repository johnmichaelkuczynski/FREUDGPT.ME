#!/usr/bin/env python3
"""Incremental extraction - one part at a time with progress saving"""

import json
import re
import os
import sys
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def extract_from_part(filepath, part_num, chunks_to_process=20, start_id=2329):
    """Extract positions from one part file"""
    
    print(f"Processing Part {part_num}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Clean
    text = text.replace('\ufeff', '')
    text = re.sub(r'\n\s*(The Interpretation Of Dreams|Studies On Hysteria)\s*\n', '\n', text)
    text = re.sub(r'\n\s*\d{3,4}\s*\n', '\n', text)
    
    # Chunk by words
    words = text.split()
    chunk_size = 2500
    chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size) if len(words[i:i+chunk_size]) > 100]
    
    print(f"  Total chunks available: {len(chunks)}")
    print(f"  Processing {min(chunks_to_process, len(chunks))} chunks...")
    
    positions = []
    
    for i, chunk in enumerate(chunks[:chunks_to_process], 1):
        if i % 5 == 1:
            print(f"    Chunk {i}...")
        
        prompt = f"""Extract 2-5 atomic philosophical positions from Freud.

Return JSON {{"positions": [...]}}. Each position:
- "title": Brief (5-10 words)
- "text_evidence": The claim (15-120 words)
- "domain": DREAM_THEORY, PSYCHOPATHOLOGY, METAPSYCHOLOGY, CLINICAL_THEORY, SEXUALITY_THEORY, CULTURAL_THEORY, DEVELOPMENTAL_THEORY, or TECHNIQUE

TEXT (Part {part_num}):
{chunk[:3000]}"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            for pos in result.get('positions', []):
                if all(k in pos for k in ['title', 'text_evidence', 'domain']):
                    positions.append(pos)
        except Exception as e:
            print(f"      Error: {e}")
    
    # Format with IDs
    formatted = []
    for i, pos in enumerate(positions):
        formatted.append({
            'position_id': f'FREUD-{start_id + i:04d}',
            'id': f'FREUD-{start_id + i:04d}',
            'title': pos['title'],
            'text_evidence': pos['text_evidence'],
            'domain': pos['domain'],
            'source': [f'Complete Works Part {part_num}'],
            'work_id': f'PART{part_num}',
            'work_title': f'Complete Works Part {part_num}'
        })
    
    print(f"  ✓ Extracted {len(formatted)} positions")
    return formatted

def main():
    """Process specified part"""
    
    if len(sys.argv) < 2:
        print("Usage: python extract_incremental.py <part_number> [chunks]")
        print("Example: python extract_incremental.py 1 20")
        sys.exit(1)
    
    part_num = int(sys.argv[1])
    chunks = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    
    files = {
        1: 'attached_assets/Freud - Complete Works (Over 4000 pages, Most Comprehensive Version Available)_Part1_1763442245951.txt',
        2: 'attached_assets/Freud - Complete Works (Over 4000 pages, Most Comprehensive Version Available)_Part2_1763442245951.txt',
        3: 'attached_assets/Freud - Complete Works (Over 4000 pages, Most Comprehensive Version Available)_Part3_1763442245949.txt',
        4: 'attached_assets/Freud - Complete Works (Over 4000 pages, Most Comprehensive Version Available)_Part4_1763442245950.txt',
        5: 'attached_assets/Freud - Complete Works (Over 4000 pages, Most Comprehensive Version Available)_Part5_1763442245950.txt',
        6: 'attached_assets/Freud - Complete Works (Over 4000 pages, Most Comprehensive Version Available)_Part6_1763446328694.txt',
        7: 'attached_assets/Freud - Complete Works (Over 4000 pages, Most Comprehensive Version Available)_Part7_1763446328694.txt',
        8: 'attached_assets/Freud - Complete Works (Over 4000 pages, Most Comprehensive Version Available)_Part8_1763446328695.txt',
        9: 'attached_assets/Freud - Complete Works (Over 4000 pages, Most Comprehensive Version Available)_Part9_1763446328695.txt',
        10: 'attached_assets/Freud - Complete Works (Over 4000 pages, Most Comprehensive Version Available)_Part10_1763446328693.txt',
        11: 'attached_assets/Freud - Complete Works (Over 4000 pages, Most Comprehensive Version Available)_Part11_1763446328694.txt',
        12: 'attached_assets/Freud - Complete Works (Over 4000 pages, Most Comprehensive Version Available)_Part12_1763447196429.txt',
        13: 'attached_assets/Freud - Complete Works (Over 4000 pages, Most Comprehensive Version Available)_Part13_1763447196429.txt',
        14: 'attached_assets/Freud - Complete Works (Over 4000 pages, Most Comprehensive Version Available)_Part14_1763447196427.txt',
        15: 'attached_assets/Freud - Complete Works (Over 4000 pages, Most Comprehensive Version Available)_Part15_1763447196427.txt',
        16: 'attached_assets/Freud - Complete Works (Over 4000 pages, Most Comprehensive Version Available)_Part16_1763447196428.txt',
        17: 'attached_assets/Freud - Complete Works (Over 4000 pages, Most Comprehensive Version Available)_Part17_1763447331651.txt',
        18: 'attached_assets/Freud - Complete Works (Over 4000 pages, Most Comprehensive Version Available)_Part18_1763447331648.txt',
        19: 'attached_assets/Freud - Complete Works (Over 4000 pages, Most Comprehensive Version Available)_Part19_1763447331649.txt',
        20: 'attached_assets/Freud - Complete Works (Over 4000 pages, Most Comprehensive Version Available)_Part20_1763447331650.txt'
    }
    
    filepath = files.get(part_num)
    if not filepath or not os.path.exists(filepath):
        print(f"ERROR: Part {part_num} not found")
        sys.exit(1)
    
    # Calculate starting ID
    start_id = 2329 + (part_num - 1) * 200
    
    positions = extract_from_part(filepath, part_num, chunks, start_id)
    
    # Save individual part
    output_file = f'data/FREUD_PART{part_num}_EXTRACTED.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({'positions': positions, 'part': part_num, 'count': len(positions)}, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Saved to: {output_file}")

if __name__ == '__main__':
    main()
