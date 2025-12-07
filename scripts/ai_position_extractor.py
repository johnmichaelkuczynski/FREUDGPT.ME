"""
AI-Powered Comprehensive Position Extractor for Kuczynski Works

This script uses Claude to extract philosophical positions with:
1. Verbatim quotes from the source text
2. Major claims identification
3. Argument mapping (which positions support which claims)
4. Hierarchical structure (claims → arguments → sub-arguments)
"""

import json
import os
import re
import time
from typing import List, Dict, Optional
import anthropic

client = anthropic.Anthropic()

EXTRACTION_PROMPT = """You are a philosophical position extractor. Your task is to extract EVERY philosophical claim, argument, definition, and example from the following text section.

For each position, provide:
1. A clear statement of the position
2. The EXACT verbatim quote from the text (copy the text EXACTLY)
3. The type of position (major_claim, argument, definition, example, implication, conclusion)
4. Keywords/terms used
5. Topic area (logic, language, epistemology, AI, mathematics, psychology, metaphysics, philosophy_of_science)

CRITICAL RULES:
- Extract EVERY substantive claim, not just major ones
- Verbatim quotes must be EXACT - copy the text character for character
- Include rhetorical questions that imply claims
- Include definitions (explicit and implicit)
- Include examples with their philosophical point
- Include implications and conclusions
- Aim for 15-30 positions per section

TEXT SECTION TO ANALYZE:
---
{text_section}
---

Respond with a JSON array of positions:
```json
[
  {{
    "statement": "Clear formulation of the position",
    "verbatim_quote": "Exact quote from the text - copy EXACTLY",
    "position_type": "major_claim|argument|definition|example|implication|conclusion",
    "keywords": ["keyword1", "keyword2"],
    "topic_area": "logic|language|epistemology|AI|mathematics|psychology|metaphysics|philosophy_of_science"
  }}
]
```

Extract ALL philosophical content. Be comprehensive."""

def load_text_file(filepath: str) -> str:
    """Load text from file with encoding fallback"""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'utf-16']
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Could not decode file {filepath}")

def split_into_sections(text: str, section_size: int = 3000) -> List[Dict]:
    """Split text into manageable sections for API processing"""
    lines = text.split('\n')
    sections = []
    current_section = []
    current_size = 0
    current_heading = "Introduction"
    
    heading_pattern = re.compile(r'^(Part [IVX0-9]+:?|[0-9]+\.|##|###|\*\*[A-Z])', re.IGNORECASE)
    
    for line in lines:
        if heading_pattern.match(line.strip()):
            if current_section and current_size > 500:
                sections.append({
                    "heading": current_heading,
                    "text": '\n'.join(current_section)
                })
            current_heading = line.strip()[:100]
            current_section = [line]
            current_size = len(line)
        else:
            current_section.append(line)
            current_size += len(line)
            
            if current_size >= section_size:
                sections.append({
                    "heading": current_heading,
                    "text": '\n'.join(current_section)
                })
                current_section = []
                current_size = 0
    
    if current_section and current_size > 200:
        sections.append({
            "heading": current_heading,
            "text": '\n'.join(current_section)
        })
    
    return sections

def extract_positions_from_section(section_text: str, section_heading: str, work_id: str, start_id: int) -> List[Dict]:
    """Use Claude to extract positions from a text section"""
    
    prompt = EXTRACTION_PROMPT.format(text_section=section_text)
    
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = ""
        for block in response.content:
            if hasattr(block, 'text'):
                response_text += block.text
        
        json_match = re.search(r'\[[\s\S]*\]', response_text)
        if not json_match:
            print(f"  Warning: No JSON found in response for section: {section_heading[:50]}")
            return []
        
        positions_raw = json.loads(json_match.group())
        
        positions = []
        for i, pos in enumerate(positions_raw):
            position = {
                "id": f"{work_id}-{start_id + i:04d}",
                "position_type": pos.get("position_type", "claim"),
                "statement": pos.get("statement", ""),
                "verbatim_quote": pos.get("verbatim_quote", ""),
                "quote_location": section_heading,
                "supports_claims": [],
                "supported_by": [],
                "keywords": pos.get("keywords", []),
                "topic_area": pos.get("topic_area", "philosophy")
            }
            positions.append(position)
        
        return positions
        
    except json.JSONDecodeError as e:
        print(f"  JSON parse error for section {section_heading[:50]}: {e}")
        return []
    except Exception as e:
        print(f"  API error for section {section_heading[:50]}: {e}")
        return []

def link_arguments_to_claims(positions: List[Dict]) -> List[Dict]:
    """Link arguments to the claims they support based on keywords and topic"""
    major_claims = [p for p in positions if p["position_type"] == "major_claim"]
    arguments = [p for p in positions if p["position_type"] in ["argument", "conclusion", "implication"]]
    
    for arg in arguments:
        arg_keywords = set(arg.get("keywords", []))
        arg_topic = arg.get("topic_area", "")
        
        best_match = None
        best_score = 0
        
        for claim in major_claims:
            claim_keywords = set(claim.get("keywords", []))
            claim_topic = claim.get("topic_area", "")
            
            keyword_overlap = len(arg_keywords & claim_keywords)
            topic_match = 2 if arg_topic == claim_topic else 0
            
            score = keyword_overlap + topic_match
            
            if score > best_score:
                best_score = score
                best_match = claim
        
        if best_match and best_score >= 2:
            arg["supports_claims"].append(best_match["id"])
            if arg["id"] not in best_match["supported_by"]:
                best_match["supported_by"].append(arg["id"])
    
    return positions

def extract_work(
    input_file: str,
    work_id: str,
    work_title: str,
    output_file: str,
    min_positions: int = 100,
    max_positions: int = 500
) -> Dict:
    """Extract all positions from a work using AI"""
    
    print(f"\n{'='*60}")
    print(f"Extracting: {work_title}")
    print(f"File: {input_file}")
    print(f"Target: {min_positions}-{max_positions} positions")
    print(f"{'='*60}")
    
    text = load_text_file(input_file)
    print(f"Loaded {len(text)} characters")
    
    sections = split_into_sections(text)
    print(f"Split into {len(sections)} sections")
    
    all_positions = []
    current_id = 1
    
    for i, section in enumerate(sections):
        if len(section["text"]) < 200:
            continue
            
        print(f"  Processing section {i+1}/{len(sections)}: {section['heading'][:50]}...")
        
        positions = extract_positions_from_section(
            section["text"],
            section["heading"],
            work_id,
            current_id
        )
        
        all_positions.extend(positions)
        current_id += len(positions)
        
        print(f"    Extracted {len(positions)} positions (total: {len(all_positions)})")
        
        if len(all_positions) >= max_positions:
            print(f"  Reached max positions ({max_positions}), stopping.")
            break
        
        time.sleep(0.5)
    
    print(f"\nLinking arguments to claims...")
    all_positions = link_arguments_to_claims(all_positions)
    
    result = {
        "work_id": work_id,
        "work_title": work_title,
        "source_file": input_file,
        "total_positions": len(all_positions),
        "positions": all_positions
    }
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"COMPLETE: {work_title}")
    print(f"Extracted {len(all_positions)} positions")
    print(f"Saved to {output_file}")
    print(f"{'='*60}")
    
    position_types = {}
    for p in all_positions:
        pt = p["position_type"]
        position_types[pt] = position_types.get(pt, 0) + 1
    print("Position types:", position_types)
    
    return result

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python ai_position_extractor.py <input_file> <work_id> <work_title> [output_file]")
        print("\nExample:")
        print('  python ai_position_extractor.py "attached_assets/MyFile.txt" "kuc-logic" "The Incompleteness of Logic"')
        sys.exit(1)
    
    input_file = sys.argv[1]
    work_id = sys.argv[2]
    work_title = sys.argv[3]
    output_file = sys.argv[4] if len(sys.argv) > 4 else f"data/extracted_{work_id}.json"
    
    extract_work(input_file, work_id, work_title, output_file)
