#!/usr/bin/env python3
"""
Extract positions from the 2 remaining Kuczynski works:
- Heed My Wisdom
- Economics of Higher Education
"""

import os
import json
import re
import sys
from datetime import datetime
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

EXTRACTION_PROMPT = """You are extracting philosophical positions from a work by J.-M. Kuczynski.

For this text, identify and extract ALL significant philosophical claims, arguments, and positions.

For EACH position, provide:
1. **position_type**: One of: major_claim, supporting_argument, sub_argument, example, definition, objection_response
2. **claim**: A clear statement of the philosophical position (your paraphrase of the key point)
3. **quote**: The EXACT VERBATIM quote from the text that supports this claim (must be word-for-word from the source)
4. **domain**: The philosophical domain (e.g., metaphysics, epistemology, philosophy_of_language, philosophy_of_mind, ethics, logic, psychoanalysis, economics, education)
5. **topics**: List of specific topics covered (e.g., ["propositions", "truth", "instantiation"])
6. **is_major_claim**: true if this is a thesis-level claim that other positions support

Extract between {min_positions} and {max_positions} positions from this text chunk.

Output as a JSON array of position objects.

TEXT TO ANALYZE:
{text}

Respond with ONLY the JSON array, no other text."""


def split_text_into_chunks(text, max_chunk_size=60000):
    """Split text into chunks at paragraph boundaries."""
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = []
    current_size = 0
    
    for para in paragraphs:
        para_size = len(para)
        if current_size + para_size > max_chunk_size and current_chunk:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = [para]
            current_size = para_size
        else:
            current_chunk.append(para)
            current_size += para_size
    
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    
    return chunks


def extract_chunk(text, work_id, work_title, min_positions, max_positions, chunk_num=1):
    """Extract positions from a single chunk of text."""
    
    prompt = EXTRACTION_PROMPT.format(
        text=text,
        min_positions=min_positions,
        max_positions=max_positions
    )
    
    try:
        print(f"  Sending chunk {chunk_num} to Claude ({len(text)} chars)...")
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=16000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text.strip()
        
        if content.startswith('```'):
            content = re.sub(r'^```(?:json)?\n?', '', content)
            content = re.sub(r'\n?```$', '', content)
        
        positions = json.loads(content)
        print(f"  Chunk {chunk_num}: Extracted {len(positions)} positions")
        return positions
        
    except json.JSONDecodeError as e:
        print(f"  ERROR: Failed to parse JSON response: {e}")
        print(f"  Response was: {content[:500]}...")
        return []
    except Exception as e:
        print(f"  ERROR: {e}")
        return []


def extract_positions_from_work(file_path, work_id, work_title):
    """Extract positions from a work file."""
    
    print(f"\n{'='*60}")
    print(f"Processing: {work_title}")
    print(f"File: {file_path}")
    print(f"{'='*60}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    text_length = len(text)
    print(f"Text length: {text_length} characters")
    
    chunks = split_text_into_chunks(text, max_chunk_size=60000)
    print(f"Split into {len(chunks)} chunks")
    
    all_positions = []
    position_counter = 1
    
    for i, chunk in enumerate(chunks, 1):
        positions_per_chunk = max(20, 50 // len(chunks))
        max_per_chunk = max(40, 100 // len(chunks))
        
        chunk_positions = extract_chunk(chunk, work_id, work_title, 
                                        positions_per_chunk, max_per_chunk, i)
        
        for pos in chunk_positions:
            formatted_pos = {
                'position_id': f'{work_id}-{position_counter:03d}',
                'work_id': work_id,
                'work_title': work_title,
                'position_type': pos.get('position_type', 'supporting_argument'),
                'claim': pos.get('claim', ''),
                'text': pos.get('claim', ''),
                'quote': pos.get('quote', ''),
                'domain': pos.get('domain', 'philosophy'),
                'topics': pos.get('topics', []),
                'is_major_claim': pos.get('is_major_claim', False),
                'extraction_date': datetime.now().isoformat()[:10]
            }
            all_positions.append(formatted_pos)
            position_counter += 1
    
    output_file = f'data/extracted_{work_id.lower()}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_positions, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved {len(all_positions)} positions to {output_file}")
    
    return all_positions


def main():
    """Process the 2 remaining works."""
    
    works = [
        {
            'file': 'attached_assets/Heed_My_Wisdom_cleaned.txt',
            'id': 'KUC-HMW',
            'title': 'Heed My Wisdom'
        },
        {
            'file': 'attached_assets/The_Economics_cleaned.txt',
            'id': 'KUC-ECON',
            'title': 'Economics of Higher Education'
        }
    ]
    
    if len(sys.argv) > 1:
        work_index = int(sys.argv[1])
        works = [works[work_index]]
    
    all_positions = []
    
    for work in works:
        if not os.path.exists(work['file']):
            print(f"WARNING: File not found: {work['file']}")
            continue
        
        positions = extract_positions_from_work(work['file'], work['id'], work['title'])
        all_positions.extend(positions)
    
    print(f"\n{'='*60}")
    print(f"COMPLETE: Extracted {len(all_positions)} total positions")
    print(f"{'='*60}")
    
    return all_positions


if __name__ == '__main__':
    main()
