#!/usr/bin/env python3
"""
Build Freud Database v8 - Ultimate Edition
Merges v7 (706 positions, 6 works) + v6 unique positions
Adds: Preface to Young Girl's Diary + missing Dreams/Essays positions
Target: ~754 positions across 7 works
"""

import json
import re
from collections import defaultdict

def normalize_text(text):
    """Normalize text for comparison"""
    # Remove extra whitespace, lowercase, remove punctuation
    text = re.sub(r'[^\w\s]', '', text.lower())
    text = ' '.join(text.split())
    return text

def find_duplicates(v7_positions, v6_positions, work_id_v7):
    """Compare v6 positions against v7 to find unique ones"""
    # Get all v7 texts for this work
    v7_texts = set()
    for pos in v7_positions:
        if pos['work_id'] == work_id_v7:
            # Normalize the text evidence
            norm = normalize_text(pos.get('text_evidence', pos.get('title', '')))
            v7_texts.add(norm)
    
    # Find v6 positions not in v7
    unique_v6 = []
    for v6_pos in v6_positions:
        norm_v6 = normalize_text(v6_pos['text'])
        # Check if this text is already in v7
        if norm_v6 not in v7_texts and len(norm_v6) > 10:  # Ignore very short texts
            unique_v6.append(v6_pos)
    
    return unique_v6

def get_next_position_id(existing_positions, prefix):
    """Get next available position ID with given prefix"""
    max_num = 0
    for pos in existing_positions:
        if pos['id'].startswith(prefix):
            try:
                num = int(pos['id'].split('-')[1])
                max_num = max(max_num, num)
            except (IndexError, ValueError):
                continue
    return f"{prefix}-{max_num + 1:03d}"

def create_position(v6_pos, pos_id, work_id, work_title, work_year, domain_map):
    """Convert v6 position format to v7 format"""
    # Map domain from v6 to v7 style
    domain = v6_pos.get('domain', 'GENERAL')
    if not domain or domain == 'None':
        domain = 'GENERAL'
    
    return {
        "id": pos_id,
        "position_id": pos_id,
        "title": v6_pos['text'][:100] + ("..." if len(v6_pos['text']) > 100 else ""),
        "text_evidence": v6_pos['text'],
        "domain": domain.upper().replace(' / ', '_').replace(' ', '_'),
        "work_id": work_id,
        "work_title": work_title,
        "source": [work_title],
        "year": work_year
    }

def main():
    print("=" * 60)
    print("BUILDING FREUD DATABASE v8 - ULTIMATE EDITION")
    print("=" * 60)
    
    # Load v7 database
    print("\n[1/6] Loading v7 database...")
    with open('data/FREUD_DATABASE.json', 'r') as f:
        v7_db = json.load(f)
    print(f"  ✓ Loaded {len(v7_db['positions'])} positions from v7")
    
    # Load v6 positions to merge
    print("\n[2/6] Loading v6 positions...")
    with open('/tmp/v6_to_merge.json', 'r') as f:
        v6_data = json.load(f)
    print(f"  ✓ Loaded v6 Dreams: {len(v6_data['v6_dreams'])} positions")
    print(f"  ✓ Loaded v6 Essays: {len(v6_data['v6_essays'])} positions")
    print(f"  ✓ Loaded v6 Preface: {len(v6_data['v6_preface'])} positions")
    
    # Find unique positions
    print("\n[3/6] Comparing positions to find unique ones...")
    
    unique_dreams = find_duplicates(v7_db['positions'], v6_data['v6_dreams'], 'WORK-004')
    print(f"  ✓ Found {len(unique_dreams)} unique Dreams positions to add")
    
    unique_essays = find_duplicates(v7_db['positions'], v6_data['v6_essays'], 'WORK-003')
    print(f"  ✓ Found {len(unique_essays)} unique Essays positions to add")
    
    # All preface positions are new
    unique_preface = v6_data['v6_preface']
    print(f"  ✓ Found {len(unique_preface)} Preface positions (NEW WORK)")
    
    # Build v8
    print("\n[4/6] Building v8 database...")
    v8_positions = list(v7_db['positions'])
    
    # Add unique Dreams positions to WORK-004
    if unique_dreams:
        for v6_pos in unique_dreams:
            pos_id = get_next_position_id(v8_positions, 'DREAM')
            new_pos = create_position(
                v6_pos, pos_id, 'WORK-004',
                'Interpretation of Dreams', 1900, {}
            )
            v8_positions.append(new_pos)
        print(f"  ✓ Added {len(unique_dreams)} Dreams positions")
    
    # Add unique Essays positions to WORK-003
    if unique_essays:
        for v6_pos in unique_essays:
            pos_id = get_next_position_id(v8_positions, 'SEX')
            new_pos = create_position(
                v6_pos, pos_id, 'WORK-003',
                'Three Essays on Sexuality', 1905, {}
            )
            v8_positions.append(new_pos)
        print(f"  ✓ Added {len(unique_essays)} Essays positions")
    
    # Add Preface as WORK-007
    if unique_preface:
        for v6_pos in unique_preface:
            pos_id = get_next_position_id(v8_positions, 'PREF')
            new_pos = create_position(
                v6_pos, pos_id, 'WORK-007',
                'Preface to Young Girl\'s Diary', 1915, {}
            )
            v8_positions.append(new_pos)
        print(f"  ✓ Added {len(unique_preface)} Preface positions as WORK-007")
    
    # Create v8 database structure
    v8_db = {
        "metadata": {
            "version": "8.0",
            "compilation_date": "2025-11-17",
            "compiler": "Replit Agent + JMK",
            "total_positions": len(v8_positions),
            "total_works": 7,
            "description": "Ultimate Freud Database - merged v7 + v6 unique positions"
        },
        "cross_reference_clusters": v7_db.get('cross_reference_clusters', []),
        "positions": v8_positions
    }
    
    # Validate and report
    print("\n[5/6] Validating v8 database...")
    work_counts = defaultdict(int)
    for pos in v8_positions:
        work_counts[pos['work_id']] += 1
    
    print("\n  Work Distribution:")
    for work_id in sorted(work_counts.keys()):
        print(f"    {work_id}: {work_counts[work_id]} positions")
    print(f"\n  TOTAL: {len(v8_positions)} positions across {len(work_counts)} works")
    
    # Save v8
    print("\n[6/6] Saving v8 database...")
    with open('data/FREUD_DATABASE_v8.json', 'w') as f:
        json.dump(v8_db, f, indent=2)
    print(f"  ✓ Saved to data/FREUD_DATABASE_v8.json")
    
    # Generate summary
    print("\n" + "=" * 60)
    print("V8 DATABASE COMPLETE")
    print("=" * 60)
    print(f"Total positions: {len(v8_positions)}")
    print(f"Added from v6: {len(unique_dreams) + len(unique_essays) + len(unique_preface)}")
    print(f"  - Dreams: +{len(unique_dreams)}")
    print(f"  - Essays: +{len(unique_essays)}")
    print(f"  - Preface: +{len(unique_preface)} (NEW WORK-007)")
    print("=" * 60)
    
    return v8_db

if __name__ == "__main__":
    main()
