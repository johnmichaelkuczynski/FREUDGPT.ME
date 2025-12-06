#!/usr/bin/env python3
"""
Merge 5 works extracted positions into Kuczynski V2 database and generate embeddings.
"""
import json
import pickle
import os
import numpy as np
from openai import OpenAI

def convert_to_v2_format(extracted_positions):
    """Convert extracted positions to V2 database format"""
    v2_positions = []
    for pos in extracted_positions:
        text = pos.get('text', '') or pos.get('quote', '') or pos.get('claim', '')
        if not text.strip():
            continue
        v2_pos = {
            'position_id': pos['position_id'],
            'text': text.strip(),
            'domain': pos.get('domain', 'philosophy'),
            'work': pos.get('work_title', 'Collected Works'),
            'year': 2024
        }
        v2_positions.append(v2_pos)
    return v2_positions

def generate_embeddings(texts, api_key, batch_size=100):
    """Generate embeddings using OpenAI API"""
    client = OpenAI(api_key=api_key)
    all_embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        print(f"Generating embeddings for batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1} ({len(batch)} texts)...")
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=batch
        )
        all_embeddings.extend([item.embedding for item in response.data])
    
    return np.array(all_embeddings)

def main():
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set")
        return
    
    print("Loading extracted positions from 5 works...")
    with open('data/kuczynski_5works_extracted.json', 'r', encoding='utf-8') as f:
        extracted = json.load(f)
    print(f"Loaded {len(extracted)} extracted positions")
    
    new_positions = convert_to_v2_format(extracted)
    print(f"Converted {len(new_positions)} positions to V2 format")
    
    print("Loading existing V2 database...")
    with open('data/KUCZYNSKI_V2_DATABASE.json', 'r', encoding='utf-8') as f:
        v2_db = json.load(f)
    
    existing_count = len(v2_db['positions'])
    print(f"Existing positions: {existing_count}")
    
    existing_ids = {p['position_id'] for p in v2_db['positions']}
    new_unique = [p for p in new_positions if p['position_id'] not in existing_ids]
    print(f"New unique positions (not already in DB): {len(new_unique)}")
    
    if not new_unique:
        print("No new positions to add!")
        return
    
    print(f"\nGenerating embeddings for {len(new_unique)} new positions...")
    texts = [p['text'] for p in new_unique]
    new_embeddings = generate_embeddings(texts, api_key)
    print(f"Generated embeddings shape: {new_embeddings.shape}")
    
    v2_db['positions'].extend(new_unique)
    print(f"Total positions after merge: {len(v2_db['positions'])}")
    
    with open('data/KUCZYNSKI_V2_DATABASE.json', 'w', encoding='utf-8') as f:
        json.dump(v2_db, f, indent=2, ensure_ascii=False)
    print("Saved updated V2 database")
    
    print("\nLoading existing embeddings...")
    chunk_files = sorted([f for f in os.listdir('data') 
                         if f.startswith('kuczynski_v2_embeddings_part') and f.endswith('.pkl')])
    
    all_existing = []
    for f in chunk_files:
        with open(f'data/{f}', 'rb') as file:
            all_existing.append(pickle.load(file))
    
    existing_embeddings = np.concatenate(all_existing)
    print(f"Existing embeddings: {existing_embeddings.shape}")
    
    combined = np.concatenate([existing_embeddings, new_embeddings], axis=0)
    print(f"Combined embeddings: {combined.shape}")
    
    print("\nRemoving old chunk files...")
    for f in chunk_files:
        os.remove(f'data/{f}')
    
    print("Saving new chunked embeddings...")
    max_chunk_size_mb = 40
    total_size = combined.nbytes / (1024 * 1024)
    num_chunks = max(1, int(np.ceil(total_size / max_chunk_size_mb)))
    chunk_size = len(combined) // num_chunks + 1
    
    for i in range(num_chunks):
        start_idx = i * chunk_size
        end_idx = min((i + 1) * chunk_size, len(combined))
        chunk = combined[start_idx:end_idx]
        chunk_path = f'data/kuczynski_v2_embeddings_part{i+1}_chunk1.pkl'
        with open(chunk_path, 'wb') as f:
            pickle.dump(chunk, f)
        chunk_mb = os.path.getsize(chunk_path) / (1024 * 1024)
        print(f"Saved {chunk_path}: {len(chunk)} embeddings ({chunk_mb:.2f} MB)")
    
    print(f"\nDone! Database now has {len(v2_db['positions'])} positions with matching embeddings")

if __name__ == '__main__':
    main()
