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
        r'\bargument:\b', r'\bclaim:\b', r'\bthesis:\b', r'\bproposition:\b',
        r'\bfor example\b', r'\bfor instance\b', r'\bconsider\b', r'\bsuppose\b',
        r'\blet us\b', r'\bthe answer is\b', r'\bthe key is\b', r'\bwhat this means\b'
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

# Files to process (NEW files only, skipping Batch 6 duplicates)
files = [
    ("attached_assets/Philosophical Knowledge_ What it is and why philosophy-departments don't want you to have it_1763704334971.txt",
     "extraction_scripts/batch7_phil_knowledge.json", "PHILKNOW",
     "Philosophical Knowledge: What it is and why philosophy departments don't want you to have it", "Epistemology/Philosophy of Science"),
    
    ("attached_assets/PHIL SCI BLOG_1763704334973.txt",
     "extraction_scripts/batch7_phil_sci_blog.json", "PHILSCI",
     "Philosophy and Science Blog Posts", "Philosophy/Science/Culture"),
    
    ("attached_assets/Philosophical Dialogues_1763704334974.txt",
     "extraction_scripts/batch7_dialogues.json", "DIALOG",
     "Philosophical Dialogues", "Logic/Epistemology/Ethics/Philosophy")
]

total = 0
for input_file, output_file, prefix, source, topic in files:
    count = extract_positions(input_file, output_file, prefix, source, topic)
    total += count

print("=" * 60)
print(f"🎯 BATCH 7 COMPLETE: {total} total positions")
print("=" * 60)
