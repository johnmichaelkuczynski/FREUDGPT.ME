"""
Fast extraction for The Incompleteness of Deductive Logic.
Processes in larger chunks and saves incrementally.
"""

import json
import os
import re
import time
import anthropic

client = anthropic.Anthropic()

EXTRACTION_PROMPT = """Extract philosophical positions from this text. For each position:
1. A clear statement
2. EXACT verbatim quote (copy the text exactly)
3. Type: major_claim, argument, definition, example, implication, conclusion
4. Keywords
5. Topic: logic, language, epistemology, AI, philosophy_of_science

Aim for 20-40 positions. Be comprehensive - extract ALL claims.

TEXT:
---
{text}
---

Return JSON array only:
[{{"statement": "...", "verbatim_quote": "...", "position_type": "...", "keywords": [...], "topic_area": "..."}}]"""

def load_text(filepath):
    for enc in ['utf-8', 'latin-1', 'cp1252']:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                return f.read()
        except:
            continue
    return None

def extract_chunk(text, chunk_id, work_id):
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            messages=[{"role": "user", "content": EXTRACTION_PROMPT.format(text=text)}]
        )
        
        response_text = ""
        for block in response.content:
            if hasattr(block, 'text'):
                response_text += block.text
        
        match = re.search(r'\[[\s\S]*\]', response_text)
        if not match:
            return []
        
        positions = json.loads(match.group())
        result = []
        for i, p in enumerate(positions):
            result.append({
                "id": f"{work_id}-{chunk_id:02d}-{i:03d}",
                "position_type": p.get("position_type", "claim"),
                "statement": p.get("statement", ""),
                "verbatim_quote": p.get("verbatim_quote", ""),
                "keywords": p.get("keywords", []),
                "topic_area": p.get("topic_area", "philosophy")
            })
        return result
    except Exception as e:
        print(f"  Error: {e}")
        return []

def main():
    filepath = "attached_assets/The_Incompleteness_of_Deductive_Logic_and_Its_Consequences_for_1765023723535.txt"
    work_id = "kuc-incompleteness"
    output_file = "data/extracted_kuc-incompleteness.json"
    
    print("Loading text...")
    text = load_text(filepath)
    if not text:
        print("Failed to load file")
        return
    
    lines = text.split('\n')
    chunk_size = 150
    chunks = []
    for i in range(0, len(lines), chunk_size):
        chunk_text = '\n'.join(lines[i:i+chunk_size])
        if len(chunk_text.strip()) > 300:
            chunks.append(chunk_text)
    
    print(f"Processing {len(chunks)} chunks...")
    
    all_positions = []
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}/{len(chunks)}...", end=" ", flush=True)
        positions = extract_chunk(chunk, i, work_id)
        all_positions.extend(positions)
        print(f"{len(positions)} positions (total: {len(all_positions)})")
        
        if i > 0 and i % 5 == 0:
            with open(output_file, 'w') as f:
                json.dump({
                    "work_id": work_id,
                    "work_title": "The Incompleteness of Deductive Logic and Its Consequences for Epistemic Engineering",
                    "total_positions": len(all_positions),
                    "positions": all_positions
                }, f, indent=2)
            print(f"    (saved checkpoint)")
        
        time.sleep(0.3)
    
    with open(output_file, 'w') as f:
        json.dump({
            "work_id": work_id,
            "work_title": "The Incompleteness of Deductive Logic and Its Consequences for Epistemic Engineering",
            "total_positions": len(all_positions),
            "positions": all_positions
        }, f, indent=2)
    
    print(f"\nDone! Extracted {len(all_positions)} positions to {output_file}")

if __name__ == "__main__":
    main()
