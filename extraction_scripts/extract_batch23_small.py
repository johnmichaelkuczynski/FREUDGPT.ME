import json
import re

def extract_positions(input_file, output_file, id_prefix, source_title, topic):
    """Extract positions from small Batch 2-3 files"""
    
    positions = []
    position_id = 1
    
    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"⚠️  File not found: {input_file}, skipping...")
        return 0
    
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and len(p.strip()) > 80]
    
    for para in paragraphs:
        if re.match(r'^(Chapter|Part|Introduction|Section|\d+\.|Table of|References)', para):
            continue
        if len(para) < 120:
            continue
            
        indicators = ['thus', 'therefore', 'it follows', 'consequently', 'given', 
                     'this means', 'the reason', 'consider', 'argument', 'must be',
                     'cannot be', 'necessarily', 'suppose', 'assume']
        
        has_indicator = any(ind in para.lower() for ind in indicators)
        
        if has_indicator or len(para) > 250:
            cleaned = para.replace('\n', ' ').strip()
            cleaned = re.sub(r'\s+', ' ', cleaned)
            
            words = cleaned.split()
            if len(words) > 400:
                cleaned = ' '.join(words[:400]) + '...'
            
            position = {
                "id": f"{id_prefix}-{position_id:03d}",
                "text": cleaned,
                "source": source_title,
                "topic": topic,
                "keywords": []
            }
            
            positions.append(position)
            position_id += 1
    
    if positions:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(positions, f, indent=2, ensure_ascii=False)
        print(f"✅ {id_prefix}: {len(positions)} positions")
    else:
        print(f"⚠️  {id_prefix}: 0 positions extracted")
    
    return len(positions)

# Process Batch 2-3 small files
files = [
    ("attached_assets/Goldman, Rousseau and von Hayek on the Ideal State_1763621448534.txt", 
     "batch23_goldman.json", "GOLDMAN", 
     "Goldman, Rousseau and von Hayek on the Ideal State", "Political Philosophy"),
    
    ("attached_assets/EMERGENCY AND REFLEXIVITY CLEAN ARTICLE FOR DATABASE_1763621448536.txt",
     "batch23_emergency.json", "EMERG",
     "Emergency and Reflexivity (economics)", "Philosophy of Economics"),
    
    ("attached_assets/1 Final Free Will for Randal Johnson_1763619387921.txt",
     "batch23_freewill.json", "FREEWILL",
     "Free Will dialogue for Randal Johnson", "Free Will/Determinism"),
    
    ("attached_assets/counterfactuals1_1763621131055.txt",
     "batch23_counterfact.json", "CFACT",
     "Counterfactuals (short essay)", "Causation/Modality"),
    
    ("attached_assets/dialogue about logic_1763621131056.txt",
     "batch23_logicdial.json", "LOGDIAL",
     "Dialogue about Logic", "Logic/Philosophy of Mathematics"),
    
    ("attached_assets/EGO SYNTONIC VS ego dystonic_1763621131057.txt",
     "batch23_egosyntonic.json", "EGOSYN",
     "Ego Syntonic vs Dystonic", "Psychology/Psychopathology"),
    
    ("attached_assets/Functional vs structural delusiveness_1763621448538.txt",
     "batch23_delusiveness.json", "DELUS",
     "Functional vs Structural Delusiveness", "Psychology/Psychopathology"),
    
    ("attached_assets/Group Psychology is More Basic than Individual Psychology.docx_1763621448535.txt",
     "batch23_grouppsych.json", "GRPPSYCH",
     "Group Psychology is More Basic", "Psychology")
]

total = 0
for input_file, output_file, prefix, source, topic in files:
    count = extract_positions(input_file, output_file, prefix, source, topic)
    total += count

print(f"\n🎯 BATCH 2-3 COMPLETE: {total} total positions extracted")
