"""
Merge all extracted positions into unified database and generate embeddings.
"""

import json
import os
import pickle
import numpy as np
from openai import OpenAI

client = OpenAI()

def load_all_extracted_positions():
    """Load positions from all extracted JSON files"""
    all_positions = []
    data_dir = "data"
    
    for filename in os.listdir(data_dir):
        if filename.startswith("extracted_") and filename.endswith(".json"):
            filepath = os.path.join(data_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                work_title = data.get("work_title", filename.replace("extracted_", "").replace(".json", ""))
                work_id = data.get("work_id", "unknown")
                
                if isinstance(data, dict) and "positions" in data:
                    for p in data["positions"]:
                        p["work_title"] = work_title
                        p["work_id"] = work_id
                        all_positions.append(p)
                elif isinstance(data, list):
                    for p in data:
                        if not p.get("work_title"):
                            p["work_title"] = work_title
                        if not p.get("work_id"):
                            p["work_id"] = work_id
                        all_positions.append(p)
                
                count = len(data["positions"]) if isinstance(data, dict) and "positions" in data else len(data)
                print(f"  Loaded {count} positions from {filename}")
            except Exception as e:
                print(f"  Error loading {filename}: {e}")
    
    return all_positions

def load_5works_positions():
    """Load positions from kuczynski_5works_extracted.json"""
    try:
        with open("data/kuczynski_5works_extracted.json", 'r') as f:
            positions = json.load(f)
        print(f"  Loaded {len(positions)} positions from kuczynski_5works_extracted.json")
        
        converted = []
        for p in positions:
            converted.append({
                "id": p.get("position_id", ""),
                "position_id": p.get("position_id", ""),
                "statement": p.get("claim", p.get("text", "")),
                "verbatim_quote": p.get("quote", p.get("text", "")),
                "position_type": p.get("position_type", "claim"),
                "work_title": p.get("work_title", "Unknown"),
                "work_id": p.get("work_id", "kuc-5works"),
                "keywords": p.get("topics", []),
                "topic_area": p.get("domain", "philosophy")
            })
        return converted
    except Exception as e:
        print(f"  Error loading 5works positions: {e}")
        return []

def load_existing_v2_positions():
    """Load existing V2 positions that have different structure"""
    try:
        with open("data/kuczynski_positions_v2.json", 'r') as f:
            positions = json.load(f)
        print(f"  Loaded {len(positions)} positions from kuczynski_positions_v2.json")
        
        converted = []
        for p in positions:
            converted.append({
                "id": p.get("position_id", ""),
                "position_id": p.get("position_id", ""),
                "statement": p.get("text", ""),
                "verbatim_quote": p.get("text", ""),
                "position_type": "claim",
                "work_title": p.get("work", "Unknown"),
                "work_id": "kuc-v2",
                "keywords": [],
                "topic_area": p.get("domain", "philosophy")
            })
        return converted
    except Exception as e:
        print(f"  Error loading V2 positions: {e}")
        return []

def load_v42_positions():
    """Load positions from v42 database (contains canonical IDs like LMCC-323)"""
    try:
        with open("data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v42_WITH_BATCH11.json", 'r') as f:
            data = json.load(f)
        
        positions = data.get("positions", [])
        print(f"  Loaded {len(positions)} positions from v42 database")
        
        converted = []
        for p in positions:
            converted.append({
                "id": p.get("position_id", ""),
                "position_id": p.get("position_id", ""),
                "statement": p.get("thesis", ""),
                "verbatim_quote": p.get("thesis", ""),
                "position_type": "claim",
                "work_title": p.get("source", "Unknown"),
                "work_id": "kuc-v42",
                "keywords": [],
                "topic_area": p.get("domain", "philosophy")
            })
        return converted
    except Exception as e:
        print(f"  Error loading v42 positions: {e}")
        return []

def deduplicate_positions(positions):
    """Remove duplicates based on statement text"""
    seen = set()
    unique = []
    for p in positions:
        key = p.get("statement", "")[:200].lower().strip()
        if key and key not in seen:
            seen.add(key)
            unique.append(p)
    return unique

def generate_embeddings(positions, batch_size=100):
    """Generate embeddings for all positions"""
    print(f"\nGenerating embeddings for {len(positions)} positions...")
    
    embeddings = []
    texts = [p.get("statement", "") + " " + p.get("verbatim_quote", "")[:500] for p in positions]
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        print(f"  Processing batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}...")
        
        try:
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=batch
            )
            for item in response.data:
                embeddings.append(item.embedding)
        except Exception as e:
            print(f"  Error in batch {i//batch_size + 1}: {e}")
            for _ in batch:
                embeddings.append([0.0] * 1536)
    
    return embeddings

def save_database(positions, embeddings, output_prefix="data/KUCZYNSKI_COMPREHENSIVE"):
    """Save positions and embeddings"""
    
    db = {
        "total_positions": len(positions),
        "positions": positions
    }
    with open(f"{output_prefix}_DATABASE.json", 'w') as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(positions)} positions to {output_prefix}_DATABASE.json")
    
    embedding_array = np.array(embeddings)
    with open(f"{output_prefix}_EMBEDDINGS.pkl", 'wb') as f:
        pickle.dump(embedding_array, f)
    print(f"Saved embeddings shape {embedding_array.shape} to {output_prefix}_EMBEDDINGS.pkl")
    
    return db

def main():
    print("="*60)
    print("MERGING ALL EXTRACTED POSITIONS")
    print("="*60)
    
    print("\nLoading extracted positions...")
    extracted = load_all_extracted_positions()
    print(f"Total from extracted files: {len(extracted)}")
    
    print("\nLoading 5works positions...")
    fiveworks = load_5works_positions()
    print(f"Total from 5works: {len(fiveworks)}")
    
    print("\nLoading existing V2 positions...")
    v2_positions = load_existing_v2_positions()
    print(f"Total from V2: {len(v2_positions)}")
    
    print("\nLoading v42 database (canonical IDs)...")
    v42_positions = load_v42_positions()
    print(f"Total from v42: {len(v42_positions)}")
    
    all_positions = extracted + fiveworks + v2_positions + v42_positions
    print(f"\nTotal before deduplication: {len(all_positions)}")
    
    unique = deduplicate_positions(all_positions)
    print(f"Total after deduplication: {len(unique)}")
    
    for i, p in enumerate(unique):
        original_id = p.get("position_id") or p.get("id") or ""
        if original_id:
            p["position_id"] = original_id
        else:
            p["position_id"] = f"kuc-{i+1:05d}"
        p["id"] = f"kuc-{i+1:05d}"
    
    embeddings = generate_embeddings(unique)
    
    save_database(unique, embeddings)
    
    print("\n" + "="*60)
    print("MERGE COMPLETE!")
    print("="*60)
    
    works = {}
    for p in unique:
        w = p.get("work_title", "Unknown")
        if isinstance(w, list):
            w = w[0] if w else "Unknown"
        w = str(w)[:50]
        works[w] = works.get(w, 0) + 1
    print("\nPositions by work:")
    for w, c in sorted(works.items(), key=lambda x: -x[1]):
        print(f"  {c:4d} - {w}")

if __name__ == "__main__":
    main()
