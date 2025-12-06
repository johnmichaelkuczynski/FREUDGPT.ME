#!/usr/bin/env python3
"""
AI-Powered Position Extraction for Kuczynski Works
Extracts structured positions (claim + quote + hierarchy) using Anthropic Claude.
"""

import os
import json
import re
from datetime import datetime
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

EXTRACTION_PROMPT = """You are extracting philosophical positions from a work by J.-M. Kuczynski.

For this text, identify and extract ALL significant philosophical claims, arguments, and positions.

For EACH position, provide:
1. **position_type**: One of: major_claim, supporting_argument, sub_argument, example, definition, objection_response
2. **claim**: A clear statement of the philosophical position (your paraphrase of the key point)
3. **quote**: The EXACT VERBATIM quote from the text that supports this claim (must be word-for-word from the source)
4. **domain**: The philosophical domain (e.g., metaphysics, epistemology, philosophy_of_language, philosophy_of_mind, ethics, logic, psychoanalysis)
5. **topics**: List of specific topics covered (e.g., ["propositions", "truth", "instantiation"])
6. **supports**: If this position supports another position you've identified, list its number
7. **is_major_claim**: true if this is a thesis-level claim that other positions support

Extract between {min_positions} and {max_positions} positions from this text, depending on its richness.

Prioritize:
- Central theses and arguments
- Definitions of key terms
- Arguments with clear logical structure
- Claims that distinguish Kuczynski's view from others
- Important examples that illustrate key points

Output as a JSON array of position objects.

TEXT TO ANALYZE:
{text}

Respond with ONLY the JSON array, no other text."""


def extract_positions_from_work(text, work_id, work_title, min_positions=50, max_positions=200):
    """Extract structured positions from a philosophical work using Claude."""
    
    text_length = len(text)
    if text_length < 5000:
        min_positions = 20
        max_positions = 50
    elif text_length < 20000:
        min_positions = 50
        max_positions = 150
    elif text_length < 50000:
        min_positions = 100
        max_positions = 300
    else:
        min_positions = 150
        max_positions = 500
    
    print(f"Extracting {min_positions}-{max_positions} positions from '{work_title}' ({text_length} chars)...")
    
    if text_length > 100000:
        chunks = split_text_into_chunks(text, max_chunk_size=80000)
        all_positions = []
        for i, chunk in enumerate(chunks):
            print(f"  Processing chunk {i+1}/{len(chunks)}...")
            chunk_positions = extract_chunk(chunk, work_id, work_title, 
                                           min_positions // len(chunks), 
                                           max_positions // len(chunks))
            all_positions.extend(chunk_positions)
        return all_positions
    else:
        return extract_chunk(text, work_id, work_title, min_positions, max_positions)


def split_text_into_chunks(text, max_chunk_size=80000):
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


def extract_chunk(text, work_id, work_title, min_positions, max_positions):
    """Extract positions from a single chunk of text."""
    
    prompt = EXTRACTION_PROMPT.format(
        text=text,
        min_positions=min_positions,
        max_positions=max_positions
    )
    
    try:
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
        
        formatted_positions = []
        for i, pos in enumerate(positions, 1):
            formatted_pos = {
                'position_id': f'{work_id}-{i:03d}',
                'work_id': work_id,
                'work_title': work_title,
                'position_type': pos.get('position_type', 'supporting_argument'),
                'claim': pos.get('claim', ''),
                'text': pos.get('claim', ''),
                'quote': pos.get('quote', ''),
                'domain': pos.get('domain', 'philosophy'),
                'topics': pos.get('topics', []),
                'is_major_claim': pos.get('is_major_claim', False),
                'supports': pos.get('supports', []),
                'extraction_date': datetime.now().isoformat()[:10]
            }
            formatted_positions.append(formatted_pos)
        
        print(f"  Extracted {len(formatted_positions)} positions")
        return formatted_positions
        
    except json.JSONDecodeError as e:
        print(f"  ERROR: Failed to parse JSON response: {e}")
        print(f"  Response was: {content[:500]}...")
        return []
    except Exception as e:
        print(f"  ERROR: {e}")
        return []


def process_work_file(file_path, work_id, work_title):
    """Process a single work file and extract positions."""
    
    print(f"\n{'='*60}")
    print(f"Processing: {work_title}")
    print(f"File: {file_path}")
    print(f"{'='*60}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    positions = extract_positions_from_work(text, work_id, work_title)
    
    output_file = f'data/extracted_{work_id.lower()}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(positions, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved {len(positions)} positions to {output_file}")
    
    return positions


def main():
    """Process the 5 works provided by the user."""
    
    works = [
        {
            'file': 'attached_assets/Neurosis_vs._Psychosis_1765023519235.txt',
            'id': 'KUC-NVP',
            'title': 'Neurosis vs. Psychosis'
        },
        {
            'file': 'attached_assets/Analytic_Summary_of_Leibniz_s_Monadology_1765023519236.txt',
            'id': 'KUC-MONAD',
            'title': "Analytic Summary of Leibniz's Monadology"
        },
        {
            'file': 'attached_assets/KANTANALOGUEDIGITALPAPER_1765023519237.txt',
            'id': 'KUC-KANT',
            'title': 'Kant and Hume on Induction, Causation'
        },
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
    
    all_positions = []
    
    for work in works:
        if not os.path.exists(work['file']):
            print(f"WARNING: File not found: {work['file']}")
            continue
        
        positions = process_work_file(work['file'], work['id'], work['title'])
        all_positions.extend(positions)
    
    merged_file = 'data/kuczynski_new_works_positions.json'
    with open(merged_file, 'w', encoding='utf-8') as f:
        json.dump(all_positions, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"COMPLETE: Extracted {len(all_positions)} total positions")
    print(f"Merged database saved to: {merged_file}")
    print(f"{'='*60}")
    
    return all_positions


if __name__ == '__main__':
    main()
