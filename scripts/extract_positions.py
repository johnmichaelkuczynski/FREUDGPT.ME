#!/usr/bin/env python3
"""
Kuczynski Position Extraction Pipeline v2

Extracts hierarchical positions (claims, arguments, quotes) from Kuczynski's works.
Uses Claude to analyze text and extract structured philosophical content.

Usage:
    python scripts/extract_positions.py --work-id "KUC-WORK-ID" --title "Work Title" --input input.txt
"""

import json
import os
import sys
import argparse
from datetime import datetime
from anthropic import Anthropic

DATABASE_PATH = "data/kuczynski_v2/database.json"
POSITIONS_DIR = "data/kuczynski_v2/positions"

EXTRACTION_PROMPT = """You are an expert philosopher tasked with extracting structured philosophical positions from the works of Peter Kuczynski.

WORK TITLE: {title}
WORK ID: {work_id}

TEXT TO ANALYZE:
{text}

YOUR TASK:
Extract between {min_positions} and {max_positions} philosophical positions from this text. For EACH position you must provide:

1. **position_type**: One of:
   - "major_claim" - A thesis-level claim that the work argues for
   - "supporting_argument" - An argument that directly supports a major claim
   - "sub_argument" - An argument that supports another argument
   - "example" - A concrete example used to illustrate or support a claim
   - "definition" - A key term definition
   - "objection_response" - A response to a potential objection

2. **claim**: The philosophical claim or argument stated clearly (1-3 sentences)

3. **quote**: A VERBATIM quote from the text that expresses or supports this claim. This MUST be an exact word-for-word quote from the text. Include enough context to be meaningful (typically 1-4 sentences).

4. **domain**: The philosophical domain (e.g., "metaphysics", "epistemology", "philosophy_of_language", "logic", "philosophy_of_mind")

5. **topics**: Array of specific topics (e.g., ["propositions", "composition", "truth", "instantiation"])

6. **supports**: Which position IDs this position argues FOR (use format {work_id}-XXX where XXX is the number)

7. **is_major_claim**: true if this is a thesis-level major claim of the work

8. **keywords**: Array of key search terms

CRITICAL REQUIREMENTS:
- The "quote" field MUST contain VERBATIM text from the source. Do NOT paraphrase.
- Identify ALL major claims/theses of the work
- For each major claim, extract the supporting arguments
- Build the argument hierarchy (what supports what)
- Extract Kuczynski's ACTUAL arguments, not generic philosophy
- Preserve his technical terminology exactly
- Include his examples and rhetorical questions when they make arguments

OUTPUT FORMAT:
Return a JSON array of position objects. Example:
[
  {{
    "position_id": "{work_id}-001",
    "position_type": "major_claim",
    "claim": "Propositions are not composed of concepts in the way sentences are composed of words.",
    "quote": "The view that propositions are somehow 'built up' from concepts faces an insurmountable difficulty: if propositions were literally composed of concepts as parts, then any two propositions sharing a concept would share a part, which leads to absurdity.",
    "domain": "metaphysics",
    "topics": ["propositions", "composition", "concepts"],
    "supports": [],
    "is_major_claim": true,
    "keywords": ["proposition", "composition", "concept", "parts"]
  }},
  {{
    "position_id": "{work_id}-002",
    "position_type": "supporting_argument",
    "claim": "Shared concepts cannot be shared parts because this would make propositions overlap materially.",
    "quote": "Consider the propositions that snow is white and that snow is cold. Both involve the concept of snow. If concepts were parts of propositions, these two propositions would literally share a part—they would overlap. But propositions are abstract objects; they cannot overlap in the way physical objects do.",
    "domain": "metaphysics",
    "topics": ["propositions", "concepts", "abstract_objects"],
    "supports": ["{work_id}-001"],
    "is_major_claim": false,
    "keywords": ["shared concept", "overlap", "abstract object", "parts"]
  }}
]

Now analyze the text and extract {min_positions}-{max_positions} positions with proper hierarchy and VERBATIM quotes:"""


def estimate_positions_count(text):
    """Estimate how many positions to extract based on text length"""
    word_count = len(text.split())
    if word_count < 2000:
        return 50, 100
    elif word_count < 5000:
        return 100, 200
    elif word_count < 10000:
        return 150, 300
    elif word_count < 20000:
        return 200, 400
    else:
        return 300, 500


def chunk_text(text, max_chunk_size=15000):
    """Split text into chunks for processing, respecting paragraph boundaries"""
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


def extract_positions_from_chunk(client, text, work_id, title, min_pos, max_pos, chunk_num=1, total_chunks=1):
    """Extract positions from a single chunk of text"""
    
    if total_chunks > 1:
        adj_min = max(20, min_pos // total_chunks)
        adj_max = max(50, max_pos // total_chunks)
    else:
        adj_min, adj_max = min_pos, max_pos
    
    prompt = EXTRACTION_PROMPT.format(
        title=title,
        work_id=work_id,
        text=text,
        min_positions=adj_min,
        max_positions=adj_max
    )
    
    print(f"  Processing chunk {chunk_num}/{total_chunks} ({len(text)} chars)...")
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=16000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    response_text = response.content[0].text
    
    try:
        start_idx = response_text.find('[')
        end_idx = response_text.rfind(']') + 1
        if start_idx >= 0 and end_idx > start_idx:
            json_str = response_text[start_idx:end_idx]
            positions = json.loads(json_str)
            return positions
    except json.JSONDecodeError as e:
        print(f"  Warning: Failed to parse JSON from chunk {chunk_num}: {e}")
        return []
    
    return []


def validate_positions(positions, text):
    """Validate extracted positions - check quotes exist in source"""
    validated = []
    issues = []
    
    text_lower = text.lower()
    
    for pos in positions:
        quote = pos.get('quote', '')
        quote_words = quote.lower().split()[:10]
        quote_start = ' '.join(quote_words)
        
        if quote_start in text_lower or len(quote) < 50:
            validated.append(pos)
        else:
            first_sentence = quote.split('.')[0].lower() if quote else ''
            if first_sentence and first_sentence in text_lower:
                validated.append(pos)
            else:
                issues.append(f"Quote not found in source: '{quote[:100]}...'")
                pos['quote_verified'] = False
                validated.append(pos)
    
    return validated, issues


def build_argument_hierarchy(positions):
    """Build supported_by links from supports links"""
    id_to_pos = {p['position_id']: p for p in positions}
    
    for pos in positions:
        pos['supported_by'] = []
    
    for pos in positions:
        for supported_id in pos.get('supports', []):
            if supported_id in id_to_pos:
                id_to_pos[supported_id]['supported_by'].append(pos['position_id'])
    
    for pos in positions:
        chain = []
        current_supports = pos.get('supports', [])
        visited = {pos['position_id']}
        
        while current_supports:
            next_supports = []
            for sup_id in current_supports:
                if sup_id not in visited and sup_id in id_to_pos:
                    chain.append(sup_id)
                    visited.add(sup_id)
                    next_supports.extend(id_to_pos[sup_id].get('supports', []))
            current_supports = next_supports
        
        pos['argument_chain'] = chain
    
    return positions


def save_positions(positions, work_id, title):
    """Save extracted positions to database"""
    os.makedirs(POSITIONS_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    work_file = os.path.join(POSITIONS_DIR, f"{work_id}.json")
    work_data = {
        "work_id": work_id,
        "title": title,
        "extracted_at": datetime.now().isoformat(),
        "position_count": len(positions),
        "positions": positions
    }
    
    with open(work_file, 'w', encoding='utf-8') as f:
        json.dump(work_data, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(positions)} positions to {work_file}")
    
    if os.path.exists(DATABASE_PATH):
        with open(DATABASE_PATH, 'r', encoding='utf-8') as f:
            db = json.load(f)
    else:
        db = {
            "version": "2.0",
            "last_updated": datetime.now().isoformat(),
            "works": [],
            "positions": []
        }
    
    db['works'] = [w for w in db['works'] if w['work_id'] != work_id]
    db['works'].append({
        "work_id": work_id,
        "title": title,
        "position_count": len(positions)
    })
    
    db['positions'] = [p for p in db['positions'] if p['work_id'] != work_id]
    for pos in positions:
        pos['work_id'] = work_id
        db['positions'].append(pos)
    
    db['last_updated'] = datetime.now().isoformat()
    
    with open(DATABASE_PATH, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    
    print(f"Updated main database: {len(db['positions'])} total positions from {len(db['works'])} works")
    
    return work_file


def process_work(text, work_id, title):
    """Main function to process a work and extract positions"""
    
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)
    
    client = Anthropic(api_key=api_key)
    
    min_pos, max_pos = estimate_positions_count(text)
    print(f"\nProcessing: {title}")
    print(f"Work ID: {work_id}")
    print(f"Text length: {len(text)} chars, {len(text.split())} words")
    print(f"Target positions: {min_pos}-{max_pos}")
    
    chunks = chunk_text(text)
    print(f"Split into {len(chunks)} chunks")
    
    all_positions = []
    for i, chunk in enumerate(chunks):
        positions = extract_positions_from_chunk(
            client, chunk, work_id, title, 
            min_pos, max_pos,
            chunk_num=i+1, total_chunks=len(chunks)
        )
        all_positions.extend(positions)
        print(f"  Extracted {len(positions)} positions from chunk {i+1}")
    
    for i, pos in enumerate(all_positions):
        pos['position_id'] = f"{work_id}-{i+1:03d}"
    
    all_positions, issues = validate_positions(all_positions, text)
    if issues:
        print(f"\nValidation issues ({len(issues)}):")
        for issue in issues[:5]:
            print(f"  - {issue}")
    
    all_positions = build_argument_hierarchy(all_positions)
    
    major_claims = [p for p in all_positions if p.get('is_major_claim')]
    print(f"\nExtraction complete:")
    print(f"  Total positions: {len(all_positions)}")
    print(f"  Major claims: {len(major_claims)}")
    
    output_file = save_positions(all_positions, work_id, title)
    
    return all_positions, output_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract positions from Kuczynski work")
    parser.add_argument("--work-id", required=True, help="Unique ID for the work (e.g., KUC-PROP-COMP)")
    parser.add_argument("--title", required=True, help="Full title of the work")
    parser.add_argument("--input", required=True, help="Input file path (txt or md)")
    
    args = parser.parse_args()
    
    with open(args.input, 'r', encoding='utf-8') as f:
        text = f.read()
    
    positions, output_file = process_work(text, args.work_id, args.title)
    
    print(f"\nDone! Positions saved to {output_file}")
