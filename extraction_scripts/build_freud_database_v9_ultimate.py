#!/usr/bin/env python3
"""
Build Freud Database v9 - ULTIMATE COMPREHENSIVE EDITION
Merges v8.0 (1,089) + Lectures 16-24 (1090-1440) + Lectures 25-28 (1441+)
Target: ~1,600+ positions across 8 major works
"""

import json
import re
from collections import defaultdict

def create_position_entry(pos_data, position_id_prefix):
    """Convert parsed position to database format"""
    # Generate position ID based on work and number
    pos_id = f"{position_id_prefix}-{pos_data['number']:04d}"
    
    # Clean and prepare text
    text = pos_data['text'].strip()
    
    # Extract title (first 80-100 chars)
    title = text[:100] + ("..." if len(text) > 100 else "")
    
    return {
        "id": pos_id,
        "position_id": pos_id,
        "title": title,
        "text_evidence": text,
        "domain": pos_data.get('section', 'GENERAL').upper().replace(' ', '_'),
        "work_id": pos_data['work_id'],
        "work_title": pos_data['work_title'],
        "source": [pos_data['work_title']],
        "year": int(pos_data['year'])
    }

def main():
    print("=" * 70)
    print("BUILDING FREUD DATABASE v9 - ULTIMATE COMPREHENSIVE EDITION")
    print("=" * 70)
    
    # Load all parsed data
    print("\n[1/7] Loading parsed data...")
    
    with open('/tmp/v8_base_positions.json', 'r') as f:
        base_positions = json.load(f)
    print(f"  ✓ Loaded v8 base: {len(base_positions)} positions")
    
    with open('/tmp/lectures_16_24.json', 'r') as f:
        lec_16_24 = json.load(f)
    print(f"  ✓ Loaded Lectures 16-24: {len(lec_16_24)} positions")
    
    with open('/tmp/lectures_25_28.json', 'r') as f:
        lec_25_28 = json.load(f)
    print(f"  ✓ Loaded Lectures 25-28: {len(lec_25_28)} positions")
    
    # De-duplicate by position number (keep unique numbers)
    print("\n[2/7] De-duplicating positions...")
    all_raw = base_positions + lec_16_24 + lec_25_28
    
    # Sort by position number and de-duplicate
    unique_positions = {}
    for pos in all_raw:
        num = pos['number']
        if num not in unique_positions:
            unique_positions[num] = pos
    
    sorted_positions = sorted(unique_positions.values(), key=lambda x: x['number'])
    print(f"  ✓ De-duplicated: {len(sorted_positions)} unique positions")
    
    # Organize by work
    print("\n[3/7] Organizing by work...")
    by_work = defaultdict(list)
    for pos in sorted_positions:
        by_work[pos['work_id']].append(pos)
    
    for work_id in sorted(by_work.keys()):
        count = len(by_work[work_id])
        title = by_work[work_id][0]['work_title']
        print(f"  {work_id}: {count} positions - {title}")
    
    # Create database entries with proper IDs
    print("\n[4/7] Creating database entries...")
    
    # ID prefixes for each work
    id_prefixes = {
        'WORK-001': 'BPP',    # Beyond Pleasure Principle
        'WORK-002': 'SEX',    # Three Essays
        'WORK-003': 'DREAM',  # Dreams
        'WORK-004': 'PREF',   # Preface
        'WORK-005': 'GSOC',   # Group Psychology
        'WORK-007': 'INTRO'   # General Introduction
    }
    
    v9_positions = []
    for work_id in sorted(by_work.keys()):
        prefix = id_prefixes.get(work_id, 'MISC')
        work_positions = by_work[work_id]
        
        for i, pos in enumerate(work_positions, 1):
            entry = create_position_entry(pos, prefix)
            # Override ID to be sequential per work
            entry['id'] = f"{prefix}-{i:04d}"
            entry['position_id'] = f"{prefix}-{i:04d}"
            v9_positions.append(entry)
    
    print(f"  ✓ Created {len(v9_positions)} database entries")
    
    # Create v9 database structure
    print("\n[5/7] Building v9 database structure...")
    
    v9_db = {
        "metadata": {
            "version": "9.0",
            "edition": "ULTIMATE_COMPREHENSIVE",
            "compilation_date": "2025-11-17",
            "compiler": "Replit Agent + JMK",
            "total_positions": len(v9_positions),
            "total_works": len(by_work),
            "description": "Most comprehensive Freud database ever created - all major works + complete General Introduction lectures"
        },
        "cross_reference_clusters": [],
        "positions": v9_positions
    }
    
    # Validate
    print("\n[6/7] Validating v9 database...")
    work_counts = defaultdict(int)
    for pos in v9_positions:
        work_counts[pos['work_id']] += 1
    
    print("\n  Work Distribution:")
    for work_id in sorted(work_counts.keys()):
        sample_pos = next(p for p in v9_positions if p['work_id'] == work_id)
        title = sample_pos['work_title']
        print(f"    {work_id}: {work_counts[work_id]:4d} positions - {title}")
    
    print(f"\n  TOTAL: {len(v9_positions)} positions across {len(work_counts)} works")
    
    # Check for duplicates
    ids = [p['id'] for p in v9_positions]
    duplicates = [id for id in set(ids) if ids.count(id) > 1]
    if duplicates:
        print(f"  ⚠️ WARNING: {len(duplicates)} duplicate IDs found")
    else:
        print(f"  ✓ No duplicate IDs")
    
    # Save v9
    print("\n[7/7] Saving v9 database...")
    with open('data/FREUD_DATABASE_v9.json', 'w') as f:
        json.dump(v9_db, f, indent=2)
    print(f"  ✓ Saved to data/FREUD_DATABASE_v9.json")
    
    # Summary
    print("\n" + "=" * 70)
    print("V9 ULTIMATE DATABASE COMPLETE")
    print("=" * 70)
    print(f"Total positions: {len(v9_positions)}")
    print(f"Total works: {len(work_counts)}")
    print(f"Unique positions from merge: {len(sorted_positions)}")
    print("=" * 70)
    
    return v9_db

if __name__ == "__main__":
    main()
