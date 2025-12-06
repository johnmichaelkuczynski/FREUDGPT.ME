import json
import os
import pickle
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SemanticSearch:
    """Semantic search over philosophical positions (Freud, Kuczynski, Jung) with lazy loading"""

    def __init__(self, database_path='data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v42_WITH_BATCH11.json', embeddings_path='data/position_embeddings.pkl'):
        self.database_path = database_path
        self.embeddings_path = embeddings_path
        self.positions = None
        self.embeddings = None
        self.client = None
        self._loaded = False
        self._positions_cache = None
    
    def _ensure_loaded(self):
        """Lazy-load data on first access"""
        if self._loaded:
            return
        
        print(f"Loading database from {self.database_path}...")
        with open(self.database_path, 'r', encoding='utf-8') as f:
            db = json.load(f)

        self.positions = []
        seen_ids = set()

        if 'positions' in db and isinstance(db['positions'], list):
            for pos_data in db['positions']:
                pos_id = pos_data.get('id', '') or pos_data.get('position_id', '')
                if pos_id and pos_id not in seen_ids:
                    position_text = (pos_data.get('text', '') or
                                   pos_data.get('text_evidence', '') or 
                                   pos_data.get('description', '') or
                                   pos_data.get('thesis', '') or 
                                   pos_data.get('position', '') or 
                                   pos_data.get('content', ''))
                    self.positions.append({
                        'position_id': pos_id,
                        'text': position_text,
                        'domain': pos_data.get('domain', 'Unknown'),
                        'title': pos_data.get('title', ''),
                        'source': pos_data.get('source', []) if isinstance(pos_data.get('source'), list) else [pos_data.get('source', 'Unknown')]
                    })
                    seen_ids.add(pos_id)

        elif 'integrated_core_positions' in db:
            for domain, pos_dict in db['integrated_core_positions'].items():
                for pos_id, pos_data in pos_dict.items():
                    if pos_id not in seen_ids:
                        position_text = pos_data.get('position', '') or pos_data.get('thesis', '')
                        self.positions.append({
                            'position_id': pos_id,
                            'text': position_text,
                            'domain': domain,
                            'title': pos_data.get('title', ''),
                            'source': pos_data.get('source', []) if isinstance(pos_data.get('source'), list) else [pos_data.get('source', 'Unknown')]
                        })
                        seen_ids.add(pos_id)

            if 'positions_detailed' in db:
                for domain, pos_dict in db['positions_detailed'].items():
                    if isinstance(pos_dict, dict):
                        for pos_id, pos_data in pos_dict.items():
                            if pos_id not in seen_ids:
                                position_text = pos_data.get('content', '') or pos_data.get('thesis', '')
                                if 'context' in pos_data and pos_data['context']:
                                    position_text = position_text + " " + pos_data['context']

                                self.positions.append({
                                    'position_id': pos_id,
                                    'text': position_text,
                                    'domain': domain,
                                    'title': pos_data.get('title', ''),
                                    'source': [pos_data.get('work_id', 'Unknown')]
                                })
                                seen_ids.add(pos_id)

        del db

        original_count = len(self.positions)
        self.positions = [p for p in self.positions if p['text'].strip()]
        filtered_count = original_count - len(self.positions)
        if filtered_count > 0:
            print(f"Filtered out {filtered_count} positions with empty text")
        
        print(f"Loaded {len(self.positions)} philosophical positions")

        self.client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

        embeddings_loaded = False
        
        if self.embeddings_path:
            base_path = self.embeddings_path.replace('.pkl', '')
            dir_path = os.path.dirname(self.embeddings_path) or '.'
            
            def natural_sort_key(filename):
                """Sort files by part number then chunk number for correct ordering"""
                import re
                match = re.search(r'_part(\d+)_chunk(\d+)', filename)
                if match:
                    return (int(match.group(1)), int(match.group(2)))
                return (0, 0)
            
            chunk_files = sorted([
                f for f in os.listdir(dir_path)
                if f.startswith(os.path.basename(base_path) + '_part') and f.endswith('.pkl')
            ], key=natural_sort_key)
            
            if chunk_files:
                print(f"Loading chunked embeddings from {len(chunk_files)} files...")
                chunks = []
                for chunk_file in chunk_files:
                    chunk_path = os.path.join(dir_path, chunk_file)
                    with open(chunk_path, 'rb') as f:
                        chunks.append(pickle.load(f))
                self.embeddings = np.concatenate(chunks, axis=0)
                print(f"Loaded {self.embeddings.shape[0]} embeddings from chunks")
                embeddings_loaded = True
            elif os.path.exists(self.embeddings_path):
                print(f"Loading pre-computed embeddings from {self.embeddings_path}...")
                with open(self.embeddings_path, 'rb') as f:
                    self.embeddings = pickle.load(f)
                embeddings_loaded = True

        if embeddings_loaded:
            if self.embeddings.shape[0] != len(self.positions):
                print(f"FATAL: Embeddings ({self.embeddings.shape[0]}) don't match database ({len(self.positions)})")
                print("Pre-computed embeddings are required. Run embedding generation script offline.")
                raise RuntimeError(f"Embedding count mismatch: {self.embeddings.shape[0]} embeddings vs {len(self.positions)} positions. Deploy pre-computed embeddings.")
        else:
            print(f"FATAL: No embeddings found at {self.embeddings_path}")
            print("Pre-computed embeddings are required. Embedding files must be deployed with the application.")
            raise RuntimeError(f"Missing embeddings file: {self.embeddings_path}. Deploy pre-computed embeddings.")

        print("Semantic search initialized successfully!")
        self._loaded = True

    def _generate_embeddings(self, texts, batch_size=100):
        """Generate embeddings using OpenAI API in batches"""
        if self.client is None:
            self.client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        all_embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            print(f"Processing batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}...")
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=batch
            )
            all_embeddings.extend([item.embedding for item in response.data])
        return np.array(all_embeddings)

    def _save_embeddings_chunked(self, embeddings_path, max_chunk_size_mb=40):
        """Save embeddings in chunks to stay under GitHub's 100MB file size limit"""
        if not embeddings_path:
            return
            
        os.makedirs(os.path.dirname(embeddings_path) or '.', exist_ok=True)
        
        total_size = self.embeddings.nbytes / (1024 * 1024)
        num_chunks = max(1, int(np.ceil(total_size / max_chunk_size_mb)))
        chunk_size = len(self.embeddings) // num_chunks + 1
        
        base_path = embeddings_path.replace('.pkl', '')
        
        for i in range(num_chunks):
            start_idx = i * chunk_size
            end_idx = min((i + 1) * chunk_size, len(self.embeddings))
            chunk = self.embeddings[start_idx:end_idx]
            chunk_path = f"{base_path}_part{i+1}.pkl"
            with open(chunk_path, 'wb') as f:
                pickle.dump(chunk, f)
            chunk_mb = os.path.getsize(chunk_path) / (1024 * 1024)
            print(f"Saved chunk {i+1}/{num_chunks}: {len(chunk)} embeddings ({chunk_mb:.2f} MB)")

    def search(self, query, top_k=5, min_similarity=0.25):
        """
        Find most relevant positions for query

        Args:
            query: User's question or statement
            top_k: Number of results to return
            min_similarity: Minimum similarity threshold (0-1)

        Returns:
            list of dicts with position_id, text, title, domain, similarity_score
        """
        self._ensure_loaded()
        
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=query
        )
        query_embedding = np.array(response.data[0].embedding)

        similarities = cosine_similarity([query_embedding], self.embeddings)[0]
        
        query_lower = query.lower()
        keyword_boosts = self._get_keyword_boosts(query_lower)
        if keyword_boosts:
            for i, pos in enumerate(self.positions):
                pos_id = pos['position_id']
                pos_text = pos['text'].lower()
                for prefix, text_keywords, boost in keyword_boosts:
                    if pos_id.startswith(prefix) or any(kw in pos_text for kw in text_keywords):
                        similarities[i] = min(1.0, similarities[i] + boost)

        valid_indices = [i for i, sim in enumerate(similarities) if sim >= min_similarity]

        if not valid_indices:
            print(f"Warning: No positions found with similarity >= {min_similarity}")
            return []

        valid_similarities = similarities[valid_indices]
        top_relative_indices = valid_similarities.argsort()[-min(top_k, len(valid_indices)):][::-1]
        top_indices = [valid_indices[i] for i in top_relative_indices]

        results = []
        for idx in top_indices:
            results.append({
                **self.positions[idx],
                'similarity': float(similarities[idx])
            })

        return results
    
    def get_position_count(self):
        """Get count of positions without loading full data"""
        if self._loaded:
            return len(self.positions)
        try:
            with open(self.database_path, 'r', encoding='utf-8') as f:
                db = json.load(f)
            if 'positions' in db:
                return len(db['positions'])
            return 0
        except:
            return 0
    
    def get_random_positions(self, count=10, min_len=30, max_len=400):
        """Get random positions for display without loading embeddings. Uses cached positions."""
        import random
        
        if self._loaded and self.positions:
            filtered = [p for p in self.positions if min_len <= len(p['text']) <= max_len]
            return random.sample(filtered, min(count, len(filtered)))
        
        if self._positions_cache is None:
            try:
                with open(self.database_path, 'r', encoding='utf-8') as f:
                    db = json.load(f)
                
                positions = []
                if 'positions' in db and isinstance(db['positions'], list):
                    for pos_data in db['positions']:
                        text = (pos_data.get('text', '') or pos_data.get('description', '') or '')
                        if text.strip():
                            positions.append({
                                'position_id': pos_data.get('id', '') or pos_data.get('position_id', ''),
                                'text': text,
                                'domain': pos_data.get('domain', 'Unknown')
                            })
                self._positions_cache = positions
                del db
            except Exception as e:
                print(f"Error loading positions cache: {e}")
                return []
        
        filtered = [p for p in self._positions_cache if min_len <= len(p['text']) <= max_len]
        return random.sample(filtered, min(count, len(filtered))) if filtered else []
    
    def _get_keyword_boosts(self, query_lower):
        """Return list of (id_prefix, text_keywords, boost_amount) tuples based on query keywords"""
        boosts = []
        
        if 'paradox' in query_lower:
            boosts.append(('PARAD', [], 0.25))
        
        if any(w in query_lower for w in ['university', 'universities', 'higher education', 'college', 'dmo', 'degree']):
            boosts.append(('ECON-HE', ['university', 'higher education', 'dmo'], 0.12))
        
        if any(w in query_lower for w in ['heed my wisdom', 'quotation', 'aphorism', 'wisdom']):
            boosts.append(('HMW', [], 0.10))
        
        if any(w in query_lower for w in ['sorites', 'vagueness', 'heap']):
            boosts.append(('SORITES', ['sorites'], 0.15))
        
        if any(w in query_lower for w in ['ocd', 'obsessive', 'compulsive', 'bureaucracy']):
            boosts.append(('OCDBUREAU', ['ocd', 'obsessive'], 0.12))
        
        if any(w in query_lower for w in ['dream', 'wish', 'unconscious']) and 'freud' not in query_lower:
            boosts.append(('FREUD-IOD', ['dream', 'manifest', 'latent'], 0.10))
        
        if any(w in query_lower for w in ['joke', 'humor', 'wit', 'comic']):
            boosts.append(('FREUD-JOKES', ['joke', 'humor', 'tendentious'], 0.12))
        
        return boosts
