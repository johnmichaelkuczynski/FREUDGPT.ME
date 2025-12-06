#!/usr/bin/env python3
"""
Ingest structured position documents into philosophical databases.
Parses bullet-point position lists from works and adds them to the database.
"""

import json
import re
import os
import sys
from datetime import datetime

def parse_positions_document(content):
    """Parse a structured positions document into individual positions."""
    positions = []
    current_work = None
    current_work_year = None
    current_work_short = None
    
    work_patterns = {
        'TOTEM AND TABOO': ('Totem and Taboo', '1913', 'TT'),
        'THE QUESTION OF LAY ANALYSIS': ('The Question of Lay Analysis', '1926', 'QLA'),
        'AN OUTLINE OF PSYCHOANALYSIS': ('An Outline of Psychoanalysis', '1940', 'OOP'),
        'NOTES UPON A CASE OF OBSESSIONAL NEUROSIS': ('Notes Upon a Case of Obsessional Neurosis (The Rat Man)', '1909', 'RM'),
        'THE RAT MAN': ('Notes Upon a Case of Obsessional Neurosis (The Rat Man)', '1909', 'RM'),
        'INTERPRETATION OF DREAMS': ('The Interpretation of Dreams', '1900', 'IOD'),
        'THREE ESSAYS ON THE THEORY OF SEXUALITY': ('Three Essays on the Theory of Sexuality', '1905', 'TES'),
        'BEYOND THE PLEASURE PRINCIPLE': ('Beyond the Pleasure Principle', '1920', 'BPP'),
        'THE EGO AND THE ID': ('The Ego and the Id', '1923', 'EI'),
        'CIVILIZATION AND ITS DISCONTENTS': ('Civilization and Its Discontents', '1930', 'CID'),
        'THE FUTURE OF AN ILLUSION': ('The Future of an Illusion', '1927', 'FOI'),
        'MOSES AND MONOTHEISM': ('Moses and Monotheism', '1939', 'MM'),
        'GROUP PSYCHOLOGY': ('Group Psychology and the Analysis of the Ego', '1921', 'GP'),
        'INTRODUCTORY LECTURES': ('Introductory Lectures on Psycho-Analysis', '1917', 'IL'),
        'NEW INTRODUCTORY LECTURES': ('New Introductory Lectures on Psycho-Analysis', '1933', 'NIL'),
        'STUDIES ON HYSTERIA': ('Studies on Hysteria', '1895', 'SH'),
        'THE PSYCHOPATHOLOGY OF EVERYDAY LIFE': ('The Psychopathology of Everyday Life', '1901', 'PEL'),
        'JOKES AND THEIR RELATION TO THE UNCONSCIOUS': ('Jokes and Their Relation to the Unconscious', '1905', 'JRU'),
        'MOURNING AND MELANCHOLIA': ('Mourning and Melancholia', '1917', 'MAM'),
        'ON NARCISSISM': ('On Narcissism: An Introduction', '1914', 'NAR'),
        'INHIBITIONS, SYMPTOMS AND ANXIETY': ('Inhibitions, Symptoms and Anxiety', '1926', 'ISA'),
    }
    
    lines = content.split('\n')
    position_num = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        for pattern, (work_name, year, short) in work_patterns.items():
            if pattern in line.upper() and ('PART' in line.upper() or '===' in line):
                current_work = work_name
                current_work_year = year
                current_work_short = short
                position_num = 0
                break
        
        match = re.match(r'^(\d+)\.\s+(.+)$', line)
        if match and current_work:
            num = int(match.group(1))
            text = match.group(2).strip()
            
            if text and len(text) > 20:
                position_id = f"FREUD-{current_work_short}-{num:03d}"
                
                positions.append({
                    'position_id': position_id,
                    'title': f"{current_work} - Position {num}",
                    'text': text,
                    'thesis': text,
                    'source_work': current_work,
                    'source_year': current_work_year,
                    'domain': 'Psychoanalysis',
                    'author': 'Sigmund Freud',
                    'extraction_date': datetime.now().isoformat()[:10]
                })
    
    return positions


def load_existing_database(db_path):
    """Load existing database if it exists."""
    if os.path.exists(db_path):
        with open(db_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def merge_positions(existing, new_positions):
    """Merge new positions with existing, avoiding duplicates by ID."""
    existing_ids = {p['position_id'] for p in existing}
    
    added = 0
    skipped = 0
    
    for pos in new_positions:
        if pos['position_id'] not in existing_ids:
            existing.append(pos)
            existing_ids.add(pos['position_id'])
            added += 1
        else:
            skipped += 1
    
    return existing, added, skipped


def main():
    if len(sys.argv) < 2:
        print("Usage: python ingest_work_positions.py <input_file> [database_path]")
        print("  input_file: Text file with numbered positions")
        print("  database_path: Path to JSON database (default: data/FREUD_DATABASE_UNIFIED.json)")
        sys.exit(1)
    
    input_file = sys.argv[1]
    db_path = sys.argv[2] if len(sys.argv) > 2 else 'data/FREUD_DATABASE_UNIFIED.json'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"Parsing positions from {input_file}...")
    new_positions = parse_positions_document(content)
    print(f"Found {len(new_positions)} positions")
    
    works = {}
    for p in new_positions:
        work = p['source_work']
        works[work] = works.get(work, 0) + 1
    
    print("\nPositions by work:")
    for work, count in sorted(works.items()):
        print(f"  - {work}: {count} positions")
    
    print(f"\nLoading existing database from {db_path}...")
    existing = load_existing_database(db_path)
    print(f"Existing database has {len(existing)} positions")
    
    merged, added, skipped = merge_positions(existing, new_positions)
    print(f"\nMerge results:")
    print(f"  - Added: {added} new positions")
    print(f"  - Skipped: {skipped} duplicates")
    print(f"  - Total: {len(merged)} positions")
    
    if added > 0:
        backup_path = db_path.replace('.json', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
        if os.path.exists(db_path):
            import shutil
            shutil.copy(db_path, backup_path)
            print(f"\nBackup created: {backup_path}")
        
        with open(db_path, 'w', encoding='utf-8') as f:
            json.dump(merged, f, indent=2, ensure_ascii=False)
        print(f"Updated database saved to {db_path}")
        
        print("\n*** IMPORTANT: Run embedding generation to index new positions ***")
        print("python scripts/generate_embeddings.py freud")
    else:
        print("\nNo new positions to add.")
    
    return merged


if __name__ == '__main__':
    main()
