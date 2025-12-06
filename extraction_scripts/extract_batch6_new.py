import json
import re

def extract_positions(input_file, output_file, prefix, source, topic):
    """Extract philosophical positions from text file"""
    print("=" * 60)
    print(f"Processing: {prefix} - {input_file}")
    print("=" * 60)
    
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    
    # Split into paragraphs (2+ newlines or section headers)
    paragraphs = re.split(r'\n\s*\n+', text)
    print(f"Found {len(paragraphs)} paragraphs\n")
    
    # Argumentative indicators
    indicators = [
        r'\btherefore\b', r'\bthus\b', r'\bhence\b', r'\bconsequently\b',
        r'\bit follows that\b', r'\bthis shows that\b', r'\bthis means that\b',
        r'\bwe can conclude\b', r'\bthis implies\b', r'\bfor this reason\b',
        r'\bin other words\b', r'\bthat is to say\b', r'\bspecifically\b',
        r'\bin fact\b', r'\bindeed\b', r'\bmoreover\b', r'\bfurthermore\b',
        r'\bin contrast\b', r'\bhowever\b', r'\bnevertheless\b', r'\bnonetheless\b',
        r'\balthough\b', r'\beven though\b', r'\bwhereas\b', r'\bby contrast\b',
        r'\bif .{1,100} then\b', r'\bgiven that\b', r'\bsince\b', r'\bbecause\b',
        r'\bsolution:\b', r'\bexplanation:\b', r'\banalysis:\b', r'\bproof:\b',
        r'\bargument:\b', r'\bclaim:\b', r'\bthesis:\b', r'\bproposition:\b'
    ]
    
    positions = []
    
    for i, para in enumerate(paragraphs):
        para = para.strip()
        
        # Skip if too short or too long
        if len(para) < 100 or len(para) > 3000:
            continue
        
        # Skip metadata/headers
        if len(para) < 200 and (
            para.isupper() or 
            para.startswith('Chapter') or
            para.startswith('Table of Contents') or
            re.match(r'^\d+[\.\)]', para) or
            para.count('\n') > 5
        ):
            continue
        
        # Check for argumentative content
        has_argument = any(re.search(pattern, para, re.IGNORECASE) for pattern in indicators)
        
        if has_argument:
            position = {
                "id": f"{prefix}{len(positions)+1:04d}",
                "text": para[:2000].strip(),
                "source": source,
                "topic": topic
            }
            positions.append(position)
    
    # Save to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(positions, f, indent=2, ensure_ascii=False)
    
    if len(positions) > 0:
        print(f"✅ Extracted {len(positions)} positions\n")
    else:
        print(f"\n⚠️  0 positions extracted\n")
    
    return len(positions)

# Files to process
files = [
    ("attached_assets/Papers on Accounting, Business, Economics, Politics, and Psychology_ College Papers Plus 2019-2019_1763672528789.txt",
     "extraction_scripts/batch6_college_papers.json", "COLLPAP",
     "College Papers Plus 2019-2019", "Business/Economics/Politics/Psychology/Philosophy"),
    
    ("attached_assets/paradoxes (1)_1763672528789.txt",
     "extraction_scripts/batch6_paradoxes.json", "PARAD",
     "Ninety Paradoxes of Philosophy and Psychology", "Logic/Philosophy/Psychology"),
    
    ("attached_assets/NATURALIZED EPISTEMOLOGY_1763672528790.txt",
     "extraction_scripts/batch6_naturalized_epi.json", "NATEPI",
     "Naturalized Epistemology", "Epistemology"),
    
    ("attached_assets/OCD and Philosophy_1763672528790.txt",
     "extraction_scripts/batch6_ocd.json", "OCDPHIL",
     "OCD and Philosophy: Short Papers", "Psychology/Philosophy/Psychopathology"),
    
    ("attached_assets/Outline of a Theory of Knowledge_1763672528790.txt",
     "extraction_scripts/batch6_knowledge.json", "KNOWTH",
     "Outline of a Theory of Knowledge", "Epistemology")
]

total = 0
for input_file, output_file, prefix, source, topic in files:
    count = extract_positions(input_file, output_file, prefix, source, topic)
    total += count

print("=" * 60)
print(f"🎯 BATCH 6 COMPLETE: {total} total positions")
print("=" * 60)
