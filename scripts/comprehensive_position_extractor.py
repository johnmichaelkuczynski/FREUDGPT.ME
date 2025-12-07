"""
Comprehensive Position Extractor for Kuczynski Works

This script extracts philosophical positions with:
1. Verbatim quotes from the source text
2. Major claims identification
3. Argument mapping (which positions support which claims)
4. Hierarchical structure (claims → arguments → sub-arguments)

Output format:
{
    "work_id": "kuc-incompleteness",
    "work_title": "The Incompleteness of Deductive Logic",
    "positions": [
        {
            "id": "kuc-incompleteness-001",
            "position_type": "major_claim" | "argument" | "sub_argument" | "definition" | "example" | "implication",
            "statement": "Clear statement of the position",
            "verbatim_quote": "Exact quote from the text that supports this position",
            "quote_location": "Part/Section/Paragraph reference",
            "supports_claims": ["id1", "id2"],  # Which major claims this argues for
            "supported_by": ["id3", "id4"],      # Which arguments support this position
            "keywords": ["recursion", "logic", "incompleteness"],
            "topic_area": "logic" | "language" | "epistemology" | "philosophy_of_science" | "AI" | "mathematics"
        }
    ]
}
"""

import json
import re
import os
from typing import List, Dict, Optional

def clean_text(text: str) -> str:
    """Clean text for processing"""
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def extract_sentences(text: str) -> List[str]:
    """Extract sentences from text"""
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
    return [s.strip() for s in sentences if len(s.strip()) > 20]

def identify_claim_type(text: str) -> str:
    """Identify the type of claim based on linguistic markers"""
    text_lower = text.lower()
    
    if any(marker in text_lower for marker in ['therefore', 'it follows that', 'thus', 'hence', 'consequently', 'this proves', 'q.e.d']):
        return "conclusion"
    elif any(marker in text_lower for marker in ['definition:', 'let', 'we define', 'by a', 'is defined as', 'is called']):
        return "definition"
    elif any(marker in text_lower for marker in ['for example', 'consider', 'suppose', 'imagine', 'instance']):
        return "example"
    elif any(marker in text_lower for marker in ['proof:', 'because', 'since', 'given that', 'the reason']):
        return "argument"
    elif any(marker in text_lower for marker in ['this means', 'implication', 'consequence', 'this shows']):
        return "implication"
    elif any(marker in text_lower for marker in ['the core', 'main result', 'thesis', 'central claim', 'key insight']):
        return "major_claim"
    else:
        return "claim"

def extract_positions_from_text(
    text: str,
    work_id: str,
    work_title: str,
    min_positions: int = 100,
    max_positions: int = 500
) -> Dict:
    """
    Extract structured positions from philosophical text
    """
    
    positions = []
    position_counter = 1
    
    paragraphs = re.split(r'\n\s*\n', text)
    
    for para_idx, paragraph in enumerate(paragraphs):
        paragraph = clean_text(paragraph)
        if len(paragraph) < 50:
            continue
            
        sentences = extract_sentences(paragraph)
        
        for sent in sentences:
            if len(sent) < 30 or len(sent) > 1000:
                continue
            
            claim_type = identify_claim_type(sent)
            
            position = {
                "id": f"{work_id}-{position_counter:04d}",
                "position_type": claim_type,
                "statement": sent,
                "verbatim_quote": sent,
                "quote_location": f"Paragraph {para_idx + 1}",
                "supports_claims": [],
                "supported_by": [],
                "keywords": extract_keywords(sent),
                "topic_area": identify_topic(sent)
            }
            
            positions.append(position)
            position_counter += 1
            
            if position_counter > max_positions:
                break
        
        if position_counter > max_positions:
            break
    
    return {
        "work_id": work_id,
        "work_title": work_title,
        "total_positions": len(positions),
        "positions": positions
    }

def extract_keywords(text: str) -> List[str]:
    """Extract key philosophical/technical terms"""
    keywords = []
    
    keyword_patterns = [
        r'\b(recursion|recursive|recursively)\b',
        r'\b(logic|logical|logics)\b',
        r'\b(language|linguistic|languages)\b',
        r'\b(truth|true|false|falsity)\b',
        r'\b(meaning|semantic|semantics)\b',
        r'\b(syntax|syntactic|syntactical)\b',
        r'\b(proposition|propositional)\b',
        r'\b(inference|infer|inferential)\b',
        r'\b(deduction|deductive|deduce)\b',
        r'\b(induction|inductive|induce)\b',
        r'\b(rational|rationality|reason)\b',
        r'\b(knowledge|epistemology|epistemic)\b',
        r'\b(pattern|recognition)\b',
        r'\b(formal|formalism|formalization)\b',
        r'\b(algorithm|algorithmic|computation)\b',
        r'\b(neural|network|AI|artificial)\b',
        r'\b(Gödel|incompleteness|completeness)\b',
        r'\b(Kant|Hume|Wittgenstein|Chomsky|Popper)\b',
        r'\b(monad|Leibniz)\b',
        r'\b(psychosis|neurosis|psychological)\b',
        r'\b(infinite|infinity|transfinite|cardinal|ordinal)\b',
        r'\b(class|set|element|subset)\b',
        r'\b(function|bijection|mapping)\b',
    ]
    
    text_lower = text.lower()
    for pattern in keyword_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                keywords.append(match.group(1).lower())
    
    return list(set(keywords))

def identify_topic(text: str) -> str:
    """Identify the primary topic area"""
    text_lower = text.lower()
    
    topic_markers = {
        "logic": ["logic", "proof", "theorem", "gödel", "recursive", "formal", "deduction"],
        "language": ["language", "semantic", "syntax", "sentence", "meaning", "expression", "linguistic"],
        "epistemology": ["knowledge", "justification", "belief", "truth", "epistem"],
        "philosophy_of_science": ["science", "discovery", "theory", "hypothesis", "popper", "induction"],
        "AI": ["neural", "network", "AI", "artificial", "computation", "algorithm", "machine"],
        "mathematics": ["number", "infinite", "set", "class", "cardinal", "ordinal", "arithmetic"],
        "psychology": ["psychosis", "neurosis", "mental", "psychological", "freud", "unconscious"],
        "metaphysics": ["monad", "leibniz", "substance", "existence", "reality", "god"]
    }
    
    scores = {topic: 0 for topic in topic_markers}
    
    for topic, markers in topic_markers.items():
        for marker in markers:
            if marker in text_lower:
                scores[topic] += 1
    
    max_topic = max(scores, key=lambda x: scores[x])
    return max_topic if scores[max_topic] > 0 else "philosophy"

def link_arguments_to_claims(positions: List[Dict]) -> List[Dict]:
    """
    Link arguments to the claims they support based on proximity and content
    """
    major_claims = [p for p in positions if p["position_type"] == "major_claim"]
    arguments = [p for p in positions if p["position_type"] in ["argument", "sub_argument", "conclusion"]]
    
    for arg in arguments:
        arg_keywords = set(arg.get("keywords", []))
        arg_topic = arg.get("topic_area", "")
        
        best_match = None
        best_score = 0
        
        for claim in major_claims:
            claim_keywords = set(claim.get("keywords", []))
            claim_topic = claim.get("topic_area", "")
            
            keyword_overlap = len(arg_keywords & claim_keywords)
            topic_match = 1 if arg_topic == claim_topic else 0
            
            score = keyword_overlap + topic_match
            
            if score > best_score:
                best_score = score
                best_match = claim
        
        if best_match and best_score > 0:
            arg["supports_claims"].append(best_match["id"])
            best_match["supported_by"].append(arg["id"])
    
    return positions

def save_database(data: Dict, output_path: str):
    """Save the extracted database to JSON"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved {data['total_positions']} positions to {output_path}")

def load_text_file(filepath: str) -> str:
    """Load text from file"""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'utf-16']
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Could not decode file {filepath}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python comprehensive_position_extractor.py <input_file> <work_id> <work_title> [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    work_id = sys.argv[2]
    work_title = sys.argv[3]
    output_file = sys.argv[4] if len(sys.argv) > 4 else f"data/extracted_{work_id}.json"
    
    text = load_text_file(input_file)
    
    data = extract_positions_from_text(text, work_id, work_title)
    
    data["positions"] = link_arguments_to_claims(data["positions"])
    
    save_database(data, output_file)
