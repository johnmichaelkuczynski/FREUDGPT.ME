"""
Batch extraction script for all Kuczynski works.
Processes each file and creates individual JSON databases.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_position_extractor import extract_work

WORKS_TO_EXTRACT = [
    {
        "file": "attached_assets/The_Incompleteness_of_Deductive_Logic_and_Its_Consequences_for_1765023723535.txt",
        "work_id": "kuc-incompleteness",
        "title": "The Incompleteness of Deductive Logic and Its Consequences for Epistemic Engineering",
        "min_positions": 300,
        "max_positions": 500
    },
    {
        "file": "attached_assets/04_revised_Kuczynski_1765023723537.txt",
        "work_id": "kuc-language-ch4",
        "title": "What Is a Language? Chapter 4",
        "min_positions": 100,
        "max_positions": 150
    },
    {
        "file": "attached_assets/What_is_a_Formal_Language_complete_1765023723538.txt",
        "work_id": "kuc-formal-language",
        "title": "What is a Formal Language?",
        "min_positions": 150,
        "max_positions": 200
    },
    {
        "file": "attached_assets/What_is_an_infinite_number__1765023723538.txt",
        "work_id": "kuc-infinite-number",
        "title": "What is an Infinite Number?",
        "min_positions": 200,
        "max_positions": 250
    },
    {
        "file": "attached_assets/KANTANALOGUEDIGITALPAPER_1765023723539.txt",
        "work_id": "kuc-kant-hume",
        "title": "Kant and Hume on Induction",
        "min_positions": 150,
        "max_positions": 200
    },
    {
        "file": "attached_assets/Neurosis_vs._Psychosis_1765023723540.txt",
        "work_id": "kuc-neurosis-psychosis",
        "title": "Neurosis vs. Psychosis",
        "min_positions": 50,
        "max_positions": 80
    },
    {
        "file": "attached_assets/Analytic_Summary_of_Leibniz_s_Monadology_1765023723540.txt",
        "work_id": "kuc-leibniz-monadology",
        "title": "Analytic Summary of Leibniz's Monadology",
        "min_positions": 150,
        "max_positions": 200
    },
    {
        "file": "attached_assets/DATABASE_CHAPTER_4_ANALYTIC_PHILOSOPHY_1765023723541.txt",
        "work_id": "kuc-analytic-philosophy",
        "title": "Database Chapter 4: Analytic Philosophy",
        "min_positions": 300,
        "max_positions": 400
    }
]

def extract_all():
    """Extract positions from all works"""
    results = []
    
    for work in WORKS_TO_EXTRACT:
        if not os.path.exists(work["file"]):
            print(f"SKIP: File not found: {work['file']}")
            continue
            
        output_file = f"data/extracted_{work['work_id']}.json"
        
        try:
            result = extract_work(
                input_file=work["file"],
                work_id=work["work_id"],
                work_title=work["title"],
                output_file=output_file,
                min_positions=work["min_positions"],
                max_positions=work["max_positions"]
            )
            results.append({
                "work_id": work["work_id"],
                "title": work["title"],
                "positions": result["total_positions"],
                "status": "success"
            })
        except Exception as e:
            print(f"ERROR extracting {work['title']}: {e}")
            results.append({
                "work_id": work["work_id"],
                "title": work["title"],
                "positions": 0,
                "status": f"error: {e}"
            })
    
    print("\n" + "="*60)
    print("EXTRACTION SUMMARY")
    print("="*60)
    total_positions = 0
    for r in results:
        print(f"  {r['title'][:40]}: {r['positions']} positions ({r['status']})")
        total_positions += r['positions']
    print(f"\nTOTAL: {total_positions} positions extracted")
    print("="*60)
    
    return results

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--single":
        work_idx = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        work = WORKS_TO_EXTRACT[work_idx]
        output_file = f"data/extracted_{work['work_id']}.json"
        extract_work(
            input_file=work["file"],
            work_id=work["work_id"],
            work_title=work["title"],
            output_file=output_file,
            min_positions=work["min_positions"],
            max_positions=work["max_positions"]
        )
    else:
        extract_all()
