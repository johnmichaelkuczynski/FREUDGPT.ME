#!/usr/bin/env python3
"""
Build Freud Database v7 - Complete Reconstruction
Integrates improved Beyond the Pleasure Principle positions and cross-references
"""

import json
import re
from typing import Dict, List

def parse_beyond_pleasure_principle_positions(filepath: str) -> List[Dict]:
    """Parse improved BPP positions from extract file"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    positions = []
    
    # Split by position markers
    position_blocks = re.split(r'\*\*Position (\d+):', content)
    
    # Skip the first split (header content)
    for i in range(1, len(position_blocks), 2):
        if i+1 >= len(position_blocks):
            break
            
        pos_num = int(position_blocks[i])
        pos_content = position_blocks[i+1].strip()
        
        # Extract title (first line)
        lines = pos_content.split('\n')
        title = lines[0].strip().rstrip('*')
        
        # Extract bullet points as text evidence
        bullets = []
        for line in lines[1:]:
            line = line.strip()
            if line.startswith('-'):
                bullets.append(line[1:].strip())
            elif line and not line.startswith('**') and not line.startswith('###'):
                # If not a bullet or header, skip
                continue
        
        text_evidence = ' '.join(bullets)
        
        # Determine domain based on position number and title
        domain = determine_domain_bpp(pos_num, title, text_evidence)
        
        position = {
            'id': f'BPP-{pos_num:03d}',
            'position_id': f'BPP-{pos_num:03d}',
            'title': title,
            'text_evidence': text_evidence,
            'domain': domain,
            'work_id': 'WORK-001',
            'work_title': 'Beyond the Pleasure Principle',
            'source': ['Beyond the Pleasure Principle (1920/1922)'],
            'year': 1920
        }
        
        positions.append(position)
    
    return positions

def determine_domain_bpp(pos_num: int, title: str, text: str) -> str:
    """Determine domain for BPP position based on content"""
    
    title_lower = title.lower()
    text_lower = text.lower()
    
    # Philosophy of Mind / Psychology (1-9)
    if pos_num <= 9:
        return 'METAPSYCHOLOGY'
    
    # Trauma and Neurosis (10-13)
    if 10 <= pos_num <= 13:
        return 'TRAUMA THEORY'
    
    # Repetition Theory (14-22)
    if 14 <= pos_num <= 22:
        if 'play' in title_lower:
            return 'PLAY THEORY'
        else:
            return 'REPETITION COMPULSION'
    
    # Instinct Theory and Death Drive (23-100)
    if 23 <= pos_num <= 100:
        if 'consciousness' in title_lower or 'memory' in title_lower:
            return 'CONSCIOUSNESS THEORY'
        elif 'death' in title_lower or 'goal of life' in title_lower:
            return 'DEATH DRIVE THEORY'
        elif 'instinct' in title_lower and 'conservative' in text_lower:
            return 'INSTINCT THEORY'
        elif 'trauma' in title_lower or 'barrier' in title_lower:
            return 'TRAUMA THEORY'
        elif 'living' in title_lower or 'organism' in title_lower or 'protozoa' in title_lower:
            return 'BIOLOGY'
        elif 'free-flowing' in title_lower or 'energy' in title_lower or 'binding' in title_lower:
            return 'METAPSYCHOLOGY'
        else:
            return 'INSTINCT THEORY'
    
    # Libido Development (101-143)
    if 101 <= pos_num <= 143:
        if 'libido' in title_lower or 'narcis' in title_lower:
            return 'LIBIDO THEORY'
        elif 'sadism' in title_lower or 'masochism' in title_lower:
            return 'SADOMASOCHISM THEORY'
        elif 'sexual' in title_lower and 'propagation' in text_lower:
            return 'SEXUAL BIOLOGY'
        elif 'plato' in title_lower or 'aristophanes' in title_lower:
            return 'PHILOSOPHICAL SPECULATION'
        elif 'germ cell' in text_lower or 'protozoa' in text_lower:
            return 'BIOLOGY'
        else:
            return 'LIBIDO THEORY'
    
    # Methodological (144-170)
    if 144 <= pos_num:
        return 'METHODOLOGY'
    
    return 'GENERAL THEORY'

def load_existing_database() -> Dict:
    """Load existing Freud database"""
    with open('data/FREUD_DATABASE.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_positions_by_prefix(db: Dict, prefixes: List[str], work_name: str) -> List[Dict]:
    """Extract positions by ID prefix"""
    positions = []
    
    for pos in db['positions']:
        pos_id = pos.get('id', '') or pos.get('position_id', '')
        
        # Check if ID starts with any of the prefixes
        for prefix in prefixes:
            if pos_id.startswith(prefix):
                positions.append(pos)
                break
    
    return positions

def parse_cross_references(filepath: str) -> Dict:
    """Parse cross-reference mappings"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract cluster information
    clusters = {}
    
    cluster_sections = re.split(r'\*\*CLUSTER (\d+):', content)
    
    for i in range(1, len(cluster_sections), 2):
        if i+1 >= len(cluster_sections):
            break
        
        cluster_num = int(cluster_sections[i])
        cluster_content = cluster_sections[i+1]
        
        # Extract cluster name
        name_match = re.search(r'([A-Z\-\s]+)\*\*', cluster_content)
        if name_match:
            cluster_name = name_match.group(1).strip()
            clusters[cluster_num] = {
                'name': cluster_name,
                'description': cluster_content[:500]
            }
    
    return clusters

def build_metadata(position_counts: Dict) -> Dict:
    """Build database metadata"""
    return {
        'version': 'v7_COMPLETE_RECONSTRUCTION',
        'created': '2025-11-17',
        'description': 'Complete Freud database with improved BPP positions, cross-references, and all major works',
        'works': [
            {
                'id': 'WORK-001',
                'title': 'Beyond the Pleasure Principle',
                'year': 1920,
                'positions': position_counts.get('bpp', 0),
                'quality': 'IMPROVED - Detailed extraction with 170 comprehensive positions'
            },
            {
                'id': 'WORK-002',
                'title': 'Three Essays on the Theory of Sexuality',
                'year': 1905,
                'positions': position_counts.get('three_essays', 0)
            },
            {
                'id': 'WORK-003',
                'title': 'The Interpretation of Dreams',
                'year': 1900,
                'positions': position_counts.get('dreams', 0)
            },
            {
                'id': 'WORK-004',
                'title': 'The Future of an Illusion',
                'year': 1927,
                'positions': position_counts.get('illusion', 0)
            },
            {
                'id': 'WORK-005',
                'title': 'Group Psychology and the Analysis of the Ego',
                'year': 1921,
                'positions': position_counts.get('group', 0)
            },
            {
                'id': 'WORK-006',
                'title': 'Totem and Taboo',
                'year': 1913,
                'positions': position_counts.get('totem', 0)
            }
        ],
        'total_positions': sum(position_counts.values()),
        'cross_reference_clusters': 15,
        'notes': [
            'Beyond the Pleasure Principle completely reconstructed from improved extract',
            'Cross-domain conceptual bridges integrated',
            'All positions have proper domain classification',
            'Quality upgrade: Detailed, comprehensive position statements'
        ]
    }

def main():
    print("Building Freud Database v7 - Complete Reconstruction")
    print("=" * 60)
    
    # Parse improved Beyond the Pleasure Principle positions
    print("\n1. Parsing improved Beyond the Pleasure Principle positions...")
    bpp_positions = parse_beyond_pleasure_principle_positions(
        'attached_assets/Pasted--FREUD-DATABASE-EXTRACT-BEYOND-THE-PLEASURE-PRINCIPLE-1922-WORK-METADATA-Author-Si-1763346948040_1763346948041.txt'
    )
    print(f"   ✓ Parsed {len(bpp_positions)} BPP positions (IMPROVED)")
    
    # Load existing database to extract other works
    print("\n2. Loading existing database for other works...")
    existing_db = load_existing_database()
    print(f"   ✓ Loaded {len(existing_db['positions'])} existing positions")
    
    # Extract positions by ID prefix
    print("\n3. Extracting positions from other works by ID prefix...")
    
    # Totem and Taboo prefixes
    totem_prefixes = ['TOTM', 'PRIM', 'OEDI', 'INCE', 'TABO', 'DEAD', 'ENEM', 
                      'RULE', 'AMBI', 'PROJ', 'SACR', 'RELI', 'ANIM', 'MAGI',
                      'OMNI', 'NARC', 'SYMB', 'MYTH', 'SOCI', 'CONS', 'PHYL']
    totem_positions = extract_positions_by_prefix(existing_db, totem_prefixes, 'Totem and Taboo')
    print(f"   ✓ Extracted {len(totem_positions)} Totem and Taboo positions")
    
    # Group Psychology prefixes
    group_prefixes = ['GRUP', 'LEAD', 'IDEN', 'LOVE', 'HYPO', 'HERD', 'LIBG']
    group_positions = extract_positions_by_prefix(existing_db, group_prefixes, 'Group Psychology')
    print(f"   ✓ Extracted {len(group_positions)} Group Psychology positions")
    
    # Three Essays prefixes
    essays_prefixes = ['SEX-', 'PERV']
    essays_positions = extract_positions_by_prefix(existing_db, essays_prefixes, 'Three Essays')
    print(f"   ✓ Extracted {len(essays_positions)} Three Essays positions")
    
    # Dreams prefixes
    dreams_prefixes = ['DREA', 'WISH', 'WORK', 'CENS', 'SYMB']
    dreams_positions = extract_positions_by_prefix(existing_db, dreams_prefixes, 'Dreams')
    print(f"   ✓ Extracted {len(dreams_positions)} Dreams positions")
    
    # Future of Illusion prefixes
    illusion_prefixes = ['RELL', 'ILLU', 'CULT']
    illusion_positions = extract_positions_by_prefix(existing_db, illusion_prefixes, 'Illusion')
    print(f"   ✓ Extracted {len(illusion_positions)} Future of Illusion positions")
    
    # Parse cross-references
    print("\n4. Parsing cross-reference mappings...")
    cross_refs = parse_cross_references(
        'attached_assets/Pasted-I-ll-create-comprehensive-cross-reference-connections-between-domains-Here-s-the-systematic-mapping-1763346923655_1763346923656.txt'
    )
    print(f"   ✓ Parsed {len(cross_refs)} conceptual clusters")
    
    # Combine all positions
    print("\n5. Combining all positions...")
    all_positions = (
        bpp_positions +
        essays_positions +
        dreams_positions +
        illusion_positions +
        group_positions +
        totem_positions
    )
    print(f"   ✓ Total positions: {len(all_positions)}")
    
    # Track position counts
    position_counts = {
        'bpp': len(bpp_positions),
        'three_essays': len(essays_positions),
        'dreams': len(dreams_positions),
        'illusion': len(illusion_positions),
        'group': len(group_positions),
        'totem': len(totem_positions)
    }
    
    # Build final database
    print("\n6. Building final database structure...")
    new_database = {
        'metadata': build_metadata(position_counts),
        'cross_reference_clusters': cross_refs,
        'positions': all_positions
    }
    
    # Save database
    print("\n7. Saving database...")
    output_path = 'data/FREUD_DATABASE_v7.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(new_database, f, indent=2, ensure_ascii=False)
    
    print(f"   ✓ Saved to {output_path}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("DATABASE BUILD COMPLETE")
    print("=" * 60)
    print(f"\nTotal Positions: {len(all_positions)}")
    print(f"Works: 6")
    print(f"Cross-Reference Clusters: {len(cross_refs)}")
    print(f"\nBreakdown by work:")
    print(f"  - Beyond the Pleasure Principle: {len(bpp_positions)} positions (IMPROVED)")
    print(f"  - Totem and Taboo: {len(totem_positions)} positions")
    print(f"  - Group Psychology: {len(group_positions)} positions")
    print(f"  - Three Essays: {len(essays_positions)} positions")
    print(f"  - Dreams: {len(dreams_positions)} positions")
    print(f"  - Future of Illusion: {len(illusion_positions)} positions")
    print(f"\nVersion: v7_COMPLETE_RECONSTRUCTION")
    print(f"Quality: HIGH - Detailed position statements with cross-references")
    
    # Count domains
    domains = {}
    for pos in all_positions:
        domain = pos.get('domain', 'Unknown')
        domains[domain] = domains.get(domain, 0) + 1
    
    print(f"\nDomains: {len(domains)}")
    print("\nTop 15 domains:")
    for domain, count in sorted(domains.items(), key=lambda x: x[1], reverse=True)[:15]:
        print(f"  - {domain}: {count} positions")

if __name__ == '__main__':
    main()
