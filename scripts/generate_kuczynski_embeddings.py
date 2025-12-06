import json
import os
import pickle
import numpy as np
from openai import OpenAI

def generate_embeddings():
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    
    with open('data/kuczynski_positions_v2.json', 'r') as f:
        positions = json.load(f)
    
    print(f"Generating embeddings for {len(positions)} positions...")
    
    db_format = {"positions": positions}
    with open('data/KUCZYNSKI_V2_DATABASE.json', 'w') as f:
        json.dump(db_format, f, indent=2, ensure_ascii=False)
    print("Saved database in expected format")
    
    batch_size = 100
    all_embeddings = []
    
    for i in range(0, len(positions), batch_size):
        batch = positions[i:i+batch_size]
        texts = [p['text'] for p in batch]
        
        print(f"  Processing batch {i//batch_size + 1}/{(len(positions)-1)//batch_size + 1}...")
        
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=texts
        )
        
        batch_embeddings = [item.embedding for item in response.data]
        all_embeddings.extend(batch_embeddings)
    
    embeddings_array = np.array(all_embeddings)
    print(f"Generated {embeddings_array.shape[0]} embeddings")
    
    chunk_size = 500
    base_path = 'data/kuczynski_v2_embeddings'
    
    for i in range(0, len(embeddings_array), chunk_size):
        chunk = embeddings_array[i:i+chunk_size]
        part_num = i // chunk_size + 1
        chunk_path = f"{base_path}_part{part_num}_chunk1.pkl"
        with open(chunk_path, 'wb') as f:
            pickle.dump(chunk, f)
        print(f"Saved {chunk_path}")
    
    print("Done!")

if __name__ == '__main__':
    generate_embeddings()
