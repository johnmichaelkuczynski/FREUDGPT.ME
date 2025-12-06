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
        r'\blet us\b', r'\bthe answer is\b', r'\bthe key is\b', r'\bwhat this means\b',
        r'\bpoint #\d+\b', r'\bargument #\d+\b', r'\bcontention\b', r'\bcorollary\b',
        r'\bI argue\b', r'\bI submit\b', r'\bI will show\b', r'\bmy argument\b',
        r'\bthis argument\b', r'\bthis shows\b', r'\bwe can see\b', r'\bit is clear\b'
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
            para.startswith('Preface') or
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

# Files to process (5 readable files from Batch 9)
files = [
    ("attached_assets/The Moral Structure of Legal Obligation_1763707295917.txt",
     "extraction_scripts/batch9_legal.json", "LEGAL",
     "The Moral Structure of Legal Obligation", "Legal Philosophy/Ethics"),
    
    ("attached_assets/ZHI SYSTEMS JOURNAL_1763707299002.txt",
     "extraction_scripts/batch9_zhi.json", "ZHI",
     "ZHI Systems Journal: Kant, McTaggart, and Network Epistemology", "Metaphysics/Epistemology"),
    
    ("attached_assets/Sorites_1763707295917.txt",
     "extraction_scripts/batch9_sorites.json", "SORITES",
     "Sorites Paradox and Implicit Comparatives", "Logic/Philosophy of Language"),
    
    ("attached_assets/What is Borderline Personality Disorder__1763707295916.txt",
     "extraction_scripts/batch9_bpd.json", "BPD",
     "Borderline Personality Disorder Analysis", "Psychopathology/Psychology"),
    
    ("attached_assets/Three Kinds of Psychopaths_ With Link to Video Version of Book_1763707295916.txt",
     "extraction_scripts/batch9_psycho.json", "PSYCHO",
     "Three Kinds of Psychopaths", "Psychopathology/Psychology")
]

total = 0
for input_file, output_file, prefix, source, topic in files:
    count = extract_positions(input_file, output_file, prefix, source, topic)
    total += count

print("=" * 60)
print(f"🎯 BATCH 9 COMPLETE: {total} total positions")
print("=" * 60)
