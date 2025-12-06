from flask import Flask, render_template, request, Response, jsonify, session  # type: ignore
import json
import os
from search import SemanticSearch
from conversation_manager import conversation_manager
from freud_engine import get_engine as get_freud_engine
from jung_engine import get_engine as get_jung_engine

try:
    import anthropic  # type: ignore
    from anthropic import Anthropic  # type: ignore
except ImportError:
    print("Anthropic library not found. Installing...")
    Anthropic = None

try:
    from openai import OpenAI  # type: ignore
except ImportError:
    print("OpenAI library not found. Installing...")
    OpenAI = None

try:
    import PyPDF2  # type: ignore
except ImportError:
    print("PyPDF2 not found")
    PyPDF2 = None

try:
    import docx  # type: ignore
except ImportError:
    print("python-docx not found")
    docx = None

import re


def detect_explicit_requirements(question, default_length, default_quotes):
    """
    Detect when user's question explicitly requires more content than settings allow.
    Override settings when question asks for specific numbers of quotes, examples, etc.
    """
    question_lower = question.lower()
    
    override_length = default_length
    override_quotes = default_quotes
    
    quote_patterns = [
        r'(\d+)\s*(?:quotation|quote|citation|passage|excerpt)s?',
        r'(?:give|list|provide|show)\s*(?:me\s*)?(\d+)\s*(?:quotation|quote|example|citation|passage|excerpt)s?',
        r'(\d+)\s*(?:example|instance|case|illustration)s?\s*(?:from|of)',
    ]
    
    for pattern in quote_patterns:
        match = re.search(pattern, question_lower)
        if match:
            requested_quotes = int(match.group(1))
            if requested_quotes > default_quotes:
                override_quotes = min(requested_quotes, 100)
                words_per_quote = 50
                override_length = max(override_length, requested_quotes * words_per_quote)
                break
    
    length_patterns = [
        r'(\d+)\s*(?:word|sentence|paragraph)s?\s*(?:each|per|for each)',
        r'(?:at least|minimum)\s*(\d+)\s*words?',
        r'(\d+)\s*(?:sentence|paragraph)s?\s*(?:explanation|analysis|discussion)',
    ]
    
    for pattern in length_patterns:
        match = re.search(pattern, question_lower)
        if match:
            num = int(match.group(1))
            if 'sentence' in question_lower:
                estimated_words = num * 20 * max(override_quotes, 10)
            elif 'paragraph' in question_lower:
                estimated_words = num * 100 * max(override_quotes, 5)
            else:
                estimated_words = num
            override_length = max(override_length, estimated_words)
            break
    
    multi_part_indicators = [
        r'(?:answer|respond to)\s*(?:each|all)\s*(?:of\s*)?(?:the\s*)?(?:following|these)\s*(\d+)?',
        r'(\d+)\s*(?:question|query|item)s?',
        r'(?:for each|each of|all of)\s*(?:the\s*)?(\d+)?',
    ]
    
    question_count = question_lower.count('?')
    if question_count > 3:
        override_length = max(override_length, question_count * 100)
        override_quotes = max(override_quotes, question_count * 2)
    
    for pattern in multi_part_indicators:
        match = re.search(pattern, question_lower)
        if match:
            if match.group(1):
                num_parts = int(match.group(1))
            else:
                num_parts = max(5, question_count)
            override_length = max(override_length, num_parts * 150)
            override_quotes = max(override_quotes, num_parts)
            break
    
    override_length = min(override_length, 10000)
    override_quotes = min(override_quotes, 100)
    
    if override_length != default_length or override_quotes != default_quotes:
        print(f"⚡ EXPLICIT REQUIREMENTS DETECTED: Overriding settings")
        print(f"   Length: {default_length} → {override_length} words")
        print(f"   Quotes: {default_quotes} → {override_quotes}")
    
    return override_length, override_quotes

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', os.urandom(24))

print("Configuring semantic search systems (lazy-loaded on first request)...")

databases = {
    'kuczynski': SemanticSearch(
        'data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v42_WITH_BATCH11.json', 
        'data/kuczynski_v42_embeddings.pkl'
    ),
    'freud': SemanticSearch(
        'data/FREUD_DATABASE_UNIFIED.json', 
        'data/freud_unified_embeddings.pkl'
    ),
    'jung': SemanticSearch(
        'data/JUNG_DATABASE.json', 
        'data/jung_embeddings.pkl'
    )
}

print(f"Available databases: {', '.join(databases.keys())} (will load on first use)")

freud_engine = get_freud_engine()
jung_engine = get_jung_engine()
print("Inference engines configured (lazy-loaded on first use)")

anthropic_client = None
openai_client = None
deepseek_client = None
perplexity_client = None
grok_client = None

try:
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
    if ANTHROPIC_API_KEY and Anthropic:
        anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)
        print("✓ Anthropic client initialized")
except Exception as e:
    print(f"✗ Could not initialize Anthropic: {e}")

try:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    if OPENAI_API_KEY and OpenAI:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        print("✓ OpenAI client initialized")
except Exception as e:
    print(f"✗ Could not initialize OpenAI: {e}")

try:
    DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
    if DEEPSEEK_API_KEY and OpenAI:
        deepseek_client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com"
        )
        print("✓ DeepSeek client initialized")
except Exception as e:
    print(f"✗ Could not initialize DeepSeek: {e}")

try:
    PERPLEXITY_API_KEY = os.environ.get("PERPLEXITY_API_KEY")
    if PERPLEXITY_API_KEY and OpenAI:
        perplexity_client = OpenAI(
            api_key=PERPLEXITY_API_KEY,
            base_url="https://api.perplexity.ai"
        )
        print("✓ Perplexity client initialized")
except Exception as e:
    print(f"✗ Could not initialize Perplexity: {e}")

grok_client = None
try:
    XAI_API_KEY = os.environ.get("XAI_API_KEY")
    if XAI_API_KEY and OpenAI:
        grok_client = OpenAI(
            api_key=XAI_API_KEY,
            base_url="https://api.x.ai/v1"
        )
        print("✓ Grok (xAI) client initialized")
except Exception as e:
    print(f"✗ Could not initialize Grok: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download-embeddings')
def download_embeddings():
    """Temporary endpoint to download embeddings archive"""
    from flask import send_file
    embeddings_path = 'embeddings.tar.gz'
    if os.path.exists(embeddings_path):
        return send_file(embeddings_path, as_attachment=True, download_name='embeddings.tar.gz')
    return "File not found", 404

@app.route('/api/databases', methods=['GET'])
def get_databases():
    """Return available databases (Jung hidden from UI but logic preserved)"""
    display_names = {
        'kuczynski': 'ZHI',
        'freud': 'Freud',
        'jung': 'Jung'
    }
    position_counts = {
        'kuczynski': 9479,
        'freud': 7187,
        'jung': 2759
    }
    hidden_databases = set()
    db_list = []
    for db_id, db_obj in databases.items():
        if db_id in hidden_databases:
            continue
        db_list.append({
            'id': db_id,
            'name': display_names.get(db_id, db_id.capitalize()),
            'count': position_counts.get(db_id, 0)
        })
    return jsonify({'databases': db_list})

@app.route('/api/providers', methods=['GET'])
def get_providers():
    """Return available AI providers in order ZHI 1-5, with ZHI 3 (Grok) as default"""
    providers = []
    # ZHI 1 - Anthropic
    if anthropic_client:
        providers.append({'id': 'anthropic', 'name': 'ZHI 1', 'models': ['claude-sonnet-4-20250514', 'claude-opus-4-20250514']})
    # ZHI 2 - OpenAI
    if openai_client:
        providers.append({'id': 'openai', 'name': 'ZHI 2', 'models': ['gpt-4o', 'gpt-4o-mini', 'o1', 'o1-mini']})
    # ZHI 3 - Grok (DEFAULT)
    if grok_client:
        providers.append({'id': 'grok', 'name': 'ZHI 3', 'models': ['grok-4', 'grok-3-beta', 'grok-3-mini-beta', 'grok-code-fast-1'], 'default': True})
    # ZHI 4 - DeepSeek
    if deepseek_client:
        providers.append({'id': 'deepseek', 'name': 'ZHI 4', 'models': ['deepseek-chat', 'deepseek-reasoner']})
    # ZHI 5 - Perplexity
    if perplexity_client:
        providers.append({'id': 'perplexity', 'name': 'ZHI 5', 'models': ['sonar-pro', 'sonar', 'sonar-reasoning']})
    return jsonify({'providers': providers})

@app.route('/api/ask', methods=['POST'])
def ask():
    """Handle user question with streaming response"""
    try:
        data = request.json
        question = data.get('question', '')
        provider = data.get('provider', 'anthropic')
        model = data.get('model', '')
        database = data.get('database', 'freud')
        enhanced_mode = data.get('enhanced_mode', False)
        answer_length = min(max(data.get('answer_length', 500), 100), 1000)
        quote_count = min(max(data.get('quote_count', 5), 1), 15)
        
        answer_length, quote_count = detect_explicit_requirements(question, answer_length, quote_count)
        
        print(f"Received question: {question}")
        print(f"Provider: {provider}, Model: {model}, Database: {database}, Enhanced Mode: {enhanced_mode}")
        print(f"Answer Length: {answer_length} words, Quote Count: {quote_count}")
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        if database not in databases:
            return jsonify({'error': f'Database "{database}" not available'}), 400
        
        searcher = databases[database]
        
        # Default to Freud if database parameter not provided
        if not database or database not in databases:
            database = 'freud' if 'freud' in databases else list(databases.keys())[0]
            searcher = databases[database]
        
        print(f"Searching {database} database for relevant positions...")
        try:
            # CANONICAL QUERY MAPPING: Force-include key positions for well-defined questions
            canonical_position_ids = []
            question_lower = question.lower()
            
            if database == 'kuczynski':
                # Proposition composition questions
                if any(term in question_lower for term in ['composition of', 'decompos', 'consist of', 'constituents of']) and 'proposition' in question_lower:
                    canonical_position_ids = ['LMCC-323', 'LMCC-324', 'ANALPHIL-062', 'ANALPHIL-142', 'LSPM-095', 'CONCAUS-084', 'CONCAUS-088']
                    print(f"⚡ CANONICAL QUERY DETECTED: proposition composition → forcing {len(canonical_position_ids)} key positions")
                # What are propositions questions  
                elif 'what are proposition' in question_lower or 'what is a proposition' in question_lower:
                    canonical_position_ids = ['LMCC-323', 'ANALPHIL-062', 'ANALPHIL-142', 'MMSE-014', 'MMSE-047']
                    print(f"⚡ CANONICAL QUERY DETECTED: what are propositions → forcing {len(canonical_position_ids)} key positions")
                # Truth and instantiation questions
                elif 'truth' in question_lower and ('instantiat' in question_lower or 'property' in question_lower):
                    canonical_position_ids = ['LMCC-323', 'ANALPHIL-062', 'ANALPHIL-142']
                    print(f"⚡ CANONICAL QUERY DETECTED: truth/instantiation → forcing {len(canonical_position_ids)} key positions")
            
            # Get semantic search results with increased top_k
            relevant_positions = searcher.search(question, top_k=15)
            
            # Force-include canonical positions at the top if they exist
            if canonical_position_ids:
                # Get the canonical positions from database
                canonical_positions = []
                for pos in searcher.positions:
                    if pos.get('position_id') in canonical_position_ids:
                        # Add with high similarity to ensure they appear first
                        pos_copy = pos.copy()
                        pos_copy['similarity'] = 0.99  # Force to top
                        canonical_positions.append(pos_copy)
                
                # Remove duplicates from search results
                search_ids = {p.get('position_id') for p in relevant_positions}
                canonical_positions = [p for p in canonical_positions if p.get('position_id') not in search_ids or p.get('position_id') in canonical_position_ids]
                
                # Prepend canonical positions
                relevant_positions = canonical_positions + [p for p in relevant_positions if p.get('position_id') not in canonical_position_ids]
                print(f"   Injected {len(canonical_positions)} canonical positions at top")
            
            print(f"Found {len(relevant_positions)} relevant positions")
            
            # Detect low-relevance searches (external knowledge mode)
            max_similarity = max([p.get('similarity', 0) for p in relevant_positions]) if relevant_positions else 0
            low_relevance = max_similarity < 0.40
            
            if low_relevance:
                print(f"⚠️  LOW RELEVANCE DETECTED (max similarity: {max_similarity:.3f})")
                print("   Activating External Knowledge Assimilation mode...")
            else:
                print(f"✓ Good relevance (max similarity: {max_similarity:.3f})")
                
        except Exception as e:
            print(f"ERROR in search: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': f'Search failed: {str(e)}'}), 500
        
        # INFERENCE ENGINE: Deduce metapsychological rules
        deduced_rules = []
        if freud_engine and database.startswith('freud'):
            try:
                print("🧠 Activating Freud inference engine...")
                deduced_rules = freud_engine.deduce(question, max_rules=15)
                print(f"✓ Fired {len(deduced_rules)} inference rules")
                for i, rule in enumerate(deduced_rules[:5], 1):
                    print(f"   {i}. [{rule['year']}] {rule['id']}: {rule['conclusion'][:80]}...")
            except Exception as e:
                print(f"⚠️  Inference engine error: {e}")
        elif jung_engine and database == 'jung':
            try:
                print("🧠 Activating Jung inference engine...")
                deduced_rules = jung_engine.deduce(question, max_rules=15)
                print(f"✓ Fired {len(deduced_rules)} inference rules")
                for i, rule in enumerate(deduced_rules[:5], 1):
                    print(f"   {i}. [{rule['year']}] {rule['id']}: {rule['conclusion'][:80]}...")
            except Exception as e:
                print(f"⚠️  Inference engine error: {e}")
        
        # Store deduced rules in session for debug endpoint
        session['last_deduced_rules'] = deduced_rules
        
        # Get or create conversation ID
        if 'conversation_id' not in session:
            session['conversation_id'] = conversation_manager.get_conversation_id()
        conversation_id = session['conversation_id']
        
        # Get conversation history (filtered to current database only to prevent cross-contamination)
        conversation_history = conversation_manager.format_history_for_prompt(conversation_id, max_recent=5, current_database=database)
        
        # Track the full answer for storage after streaming
        full_answer = []
        
        def generate():
            try:
                print("Starting SSE generator...")
                sources = [p['position_id'] for p in relevant_positions]
                positions_data = [{
                    'id': p.get('position_id', ''),
                    'text': (p.get('text') or p.get('thesis', ''))[:300] + ('...' if len(p.get('text') or p.get('thesis', '')) > 300 else ''),
                    'domain': p.get('domain', 'philosophy')
                } for p in relevant_positions]
                yield f"data: {json.dumps({'type': 'sources', 'data': sources, 'positions': positions_data})}\n\n"
                
                prompt = build_prompt(question, relevant_positions, database, conversation_history, enhanced_mode, low_relevance, deduced_rules, answer_length, quote_count)
                mode_label = "Enhanced" if enhanced_mode else "Basic"
                knowledge_mode = " + External Knowledge" if low_relevance else ""
                print(f"Generated prompt ({mode_label} Mode{knowledge_mode}) with conversation history, sending to {provider}...")
                
                if provider == 'anthropic':
                    if not anthropic_client:
                        yield f"data: {json.dumps({'type': 'error', 'data': 'Anthropic API key not configured'})}\n\n"
                        yield f"data: {json.dumps({'type': 'done'})}\n\n"
                        return
                    model_name = model or "claude-sonnet-4-20250514"
                    print(f"Using Anthropic model: {model_name}")
                    with anthropic_client.messages.stream(
                        model=model_name,
                        max_tokens=16000,
                        system=f"You MUST write responses of at least {answer_length} words. NEVER stop mid-sentence or mid-paragraph. Complete ALL your thoughts fully.",
                        messages=[{"role": "user", "content": prompt}]
                    ) as stream:
                        token_count = 0
                        for text in stream.text_stream:
                            token_count += 1
                            full_answer.append(text)
                            if token_count % 100 == 0:
                                print(f"Streamed {token_count} tokens...")
                            yield f"data: {json.dumps({'type': 'token', 'data': text})}\n\n"
                        print(f"Anthropic completed streaming {token_count} total tokens")
                
                elif provider == 'openai':
                    if not openai_client:
                        yield f"data: {json.dumps({'type': 'error', 'data': 'OpenAI API key not configured'})}\n\n"
                        yield f"data: {json.dumps({'type': 'done'})}\n\n"
                        return
                    model_name = model or "gpt-4o"
                    token_count = 0
                    stream = openai_client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": f"You MUST write responses of at least {answer_length} words. NEVER stop mid-sentence or mid-paragraph. Complete ALL your thoughts fully."},
                            {"role": "user", "content": prompt}
                        ],
                        stream=True,
                        max_tokens=16000
                    )
                    for chunk in stream:
                        if chunk.choices[0].delta.content:
                            token_count += 1
                            full_answer.append(chunk.choices[0].delta.content)
                            yield f"data: {json.dumps({'type': 'token', 'data': chunk.choices[0].delta.content})}\n\n"
                        if chunk.choices[0].finish_reason:
                            print(f"OpenAI finished with reason: {chunk.choices[0].finish_reason} after {token_count} tokens")
                    print(f"OpenAI streaming completed: {token_count} total tokens")
                
                elif provider == 'deepseek':
                    if not deepseek_client:
                        yield f"data: {json.dumps({'type': 'error', 'data': 'DeepSeek API key not configured'})}\n\n"
                        yield f"data: {json.dumps({'type': 'done'})}\n\n"
                        return
                    model_name = model or "deepseek-chat"
                    token_count = 0
                    stream = deepseek_client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": f"You MUST write responses of at least {answer_length} words. NEVER stop mid-sentence or mid-paragraph. Complete ALL your thoughts fully."},
                            {"role": "user", "content": prompt}
                        ],
                        stream=True,
                        max_tokens=16000
                    )
                    for chunk in stream:
                        if chunk.choices[0].delta.content:
                            token_count += 1
                            full_answer.append(chunk.choices[0].delta.content)
                            yield f"data: {json.dumps({'type': 'token', 'data': chunk.choices[0].delta.content})}\n\n"
                        if chunk.choices[0].finish_reason:
                            print(f"DeepSeek finished with reason: {chunk.choices[0].finish_reason} after {token_count} tokens")
                    print(f"DeepSeek streaming completed: {token_count} total tokens")
                
                elif provider == 'perplexity':
                    if not perplexity_client:
                        yield f"data: {json.dumps({'type': 'error', 'data': 'Perplexity API key not configured'})}\n\n"
                        yield f"data: {json.dumps({'type': 'done'})}\n\n"
                        return
                    model_name = model or "sonar-pro"
                    token_count = 0
                    pplx_thinker = {'freud': 'Sigmund Freud', 'kuczynski': 'J.-M. Kuczynski', 'jung': 'Carl Gustav Jung'}.get(database, database.capitalize())
                    perplexity_system = f"""You are an educational philosophy assistant for an academic research tool called FreudGPT.
Your task is to present the documented philosophical positions from a curated database of {pplx_thinker}'s actual writings.
This is NOT impersonation - you are serving as an expert spokesperson presenting REAL documented positions from primary sources.
The positions below come from {pplx_thinker}'s published works and have been systematically extracted for academic study.
Present the material in first person as is standard in academic philosophy education (like audiobook narration of primary texts).
You MUST write responses of at least {answer_length} words. NEVER stop mid-sentence. Complete ALL thoughts fully.
NEVER break character or add meta-commentary about the task. Simply present the philosophical content."""
                    stream = perplexity_client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": perplexity_system},
                            {"role": "user", "content": prompt}
                        ],
                        stream=True,
                        max_tokens=16000
                    )
                    for chunk in stream:
                        if chunk.choices[0].delta.content:
                            token_count += 1
                            full_answer.append(chunk.choices[0].delta.content)
                            yield f"data: {json.dumps({'type': 'token', 'data': chunk.choices[0].delta.content})}\n\n"
                        if chunk.choices[0].finish_reason:
                            print(f"Perplexity finished with reason: {chunk.choices[0].finish_reason} after {token_count} tokens")
                    print(f"Perplexity streaming completed: {token_count} total tokens")
                
                elif provider == 'grok':
                    if not grok_client:
                        yield f"data: {json.dumps({'type': 'error', 'data': 'Grok (xAI) API key not configured'})}\n\n"
                        yield f"data: {json.dumps({'type': 'done'})}\n\n"
                        return
                    model_name = model or "grok-4"
                    token_count = 0
                    stream = grok_client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": f"You MUST write responses of at least {answer_length} words. NEVER stop mid-sentence or mid-paragraph. Complete ALL your thoughts fully."},
                            {"role": "user", "content": prompt}
                        ],
                        stream=True,
                        max_tokens=16000
                    )
                    for chunk in stream:
                        if chunk.choices[0].delta.content:
                            token_count += 1
                            full_answer.append(chunk.choices[0].delta.content)
                            yield f"data: {json.dumps({'type': 'token', 'data': chunk.choices[0].delta.content})}\n\n"
                        if chunk.choices[0].finish_reason:
                            print(f"Grok finished with reason: {chunk.choices[0].finish_reason} after {token_count} tokens")
                    print(f"Grok streaming completed: {token_count} total tokens")
                
                else:
                    yield f"data: {json.dumps({'type': 'error', 'data': f'Unknown provider: {provider}'})}\n\n"
                    yield f"data: {json.dumps({'type': 'done'})}\n\n"
                    return
                
                # Save to conversation history after streaming completes
                answer_text = ''.join(full_answer)
                conversation_manager.add_exchange(conversation_id, question, answer_text, database)
                
                yield f"data: {json.dumps({'type': 'done'})}\n\n"
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                yield f"data: {json.dumps({'type': 'token', 'data': error_msg})}\n\n"
                yield f"data: {json.dumps({'type': 'done'})}\n\n"
        
        return Response(
            generate(), 
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no',
                'Connection': 'keep-alive'
            }
        )
    except Exception as e:
        print(f"ERROR in /api/ask: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/random-quotes', methods=['GET'])
def get_random_quotes():
    """Return random philosophical quotes/insights for the Knowledge Panel during wait time.
    Uses lazy-loading to avoid triggering full database/embedding load."""
    import random
    
    database = request.args.get('database', 'freud')
    count = min(int(request.args.get('count', 8)), 20)
    
    if database not in databases:
        return jsonify({'quotes': [], 'positions': []})
    
    searcher = databases[database]
    
    archive_positions = searcher.get_random_positions(count=count * 2, min_len=100, max_len=800)
    quotes = []
    for pos in archive_positions[:count]:
        text = pos.get('text', '')
        if text:
            quotes.append({
                'text': text,
                'id': pos.get('position_id', '')
            })
    
    short_positions_raw = searcher.get_random_positions(count=100, min_len=30, max_len=400)
    short_positions = []
    for pos in short_positions_raw:
        text = pos.get('text', '')
        if text:
            short_positions.append({
                'text': text,
                'id': pos.get('position_id', '')
            })
    
    return jsonify({
        'quotes': quotes,
        'positions': short_positions
    })

@app.route('/raw_chain', methods=['GET', 'POST'])
def raw_chain():
    """Debug endpoint: Show which inference rules fired in the last query"""
    deduced_rules = session.get('last_deduced_rules', [])
    
    if not deduced_rules:
        return jsonify({
            'message': 'No deduced rules available (send a Freud query first)',
            'rules': []
        })
    
    formatted_rules = []
    for i, rule in enumerate(deduced_rules, 1):
        formatted_rules.append({
            'rank': i,
            'id': rule['id'],
            'year': rule['year'],
            'premise': rule['premise'][:100] + '...' if len(rule['premise']) > 100 else rule['premise'],
            'conclusion': rule['conclusion'],
            'strength': rule['strength'],
            'domain': rule['domain']
        })
    
    return jsonify({
        'total_rules_fired': len(deduced_rules),
        'rules': formatted_rules
    })

def build_prompt(question, positions, database='freud', conversation_history='', enhanced_mode=False, low_relevance=False, deduced_rules=None, answer_length=500, quote_count=5):
    """Build intelligent prompt with conversation memory, contradiction detection, inference engine deductions, and user-specified length/quote preferences"""
    
    if deduced_rules is None:
        deduced_rules = []
    
    length_instruction = f"""
MANDATORY RESPONSE LENGTH AND QUOTE REQUIREMENTS:
- MINIMUM LENGTH: {answer_length} words - this is a HARD MINIMUM, not a suggestion
- NUMBER OF QUOTES: Include at least {quote_count} direct quotes or very close paraphrases from the retrieved positions
- Each quote should be clearly attributed to its source position ID
- Quotes should be substantive excerpts that directly address the question, not superficial fragments
"""
    
    completion_instruction = f"""

CRITICAL COMPLETION REQUIREMENT:
You MUST write a response of AT LEAST {answer_length} words. This is NON-NEGOTIABLE.
- DO NOT stop mid-sentence
- DO NOT stop mid-paragraph  
- DO NOT stop mid-argument
- Complete ALL points you begin
- Include a proper conclusion
- If you find yourself stopping early, CONTINUE WRITING until you reach {answer_length} words minimum
"""
    
    # Build metapsychological/analytical deduction section if rules were fired
    deduction_section = ""
    if deduced_rules and (database.startswith('freud') or database == 'jung'):
        formatted_deductions = []
        for rule in deduced_rules:
            # Determine viewpoint based on database
            if database.startswith('freud'):
                viewpoint = 'economic' if any(term in rule['conclusion'].lower() for term in ['excit', 'energy', 'cathex', 'quantity']) else 'dynamic'
            else:  # Jung
                if any(term in rule['conclusion'].lower() for term in ['archet', 'collective', 'symbol']):
                    viewpoint = 'archetypal'
                elif any(term in rule['conclusion'].lower() for term in ['individuation', 'self', 'wholeness']):
                    viewpoint = 'individuation'
                elif any(term in rule['conclusion'].lower() for term in ['introversion', 'extraversion', 'type']):
                    viewpoint = 'typological'
                else:
                    viewpoint = 'dynamic'
            formatted_deductions.append(f"From the {viewpoint} viewpoint ({rule['year']}): {rule['conclusion']}")
        
        theory_name = "Freudian principles" if database.startswith('freud') else "Jungian principles"
        infrastructure_name = "metapsychological" if database.startswith('freud') else "analytical psychology"
        
        deduction_section = f"""
{infrastructure_name.upper()} DEDUCTIONS (Inference Engine):
The following {theory_name} have been automatically deduced from your question. These are UNDENIABLE FOUNDATIONS for your response. Use them as the theoretical backbone of your analysis:

{chr(10).join(formatted_deductions)}

INSTRUCTION: These deductions are NOT optional suggestions. They are the {infrastructure_name} infrastructure of your response. Build your prose diagnosis/explanation upon these foundations.

"""
    
    excerpts = "\n\n".join([
        f"POSITION {i+1} (ID: {p['position_id']}, Domain: {p['domain']}, Relevance: {p.get('similarity', 0):.2f}):\nTitle: {p['title']}\n{p['text']}"
        for i, p in enumerate(positions)
    ])
    
    # Determine thinker name
    thinker_name = {
        'freud': 'Sigmund Freud',
        'freud_extended': 'Sigmund Freud',
        'freud_extracted': 'Sigmund Freud',
        'kuczynski': 'J.-M. Kuczynski',
        'jung': 'Carl Gustav Jung'
    }.get(database, database.capitalize())
    
    # Build history section if available
    history_section = ""
    if conversation_history:
        history_section = f"""
PREVIOUS CONVERSATION (Your Earlier Statements):
{conversation_history}

SELF-CONTRADICTION DETECTION PROTOCOL:
Before responding, review what you have stated in previous responses above. If your current response contradicts a previous response:

1. ACKNOWLEDGE IT EXPLICITLY: Begin with phrases like "I recognize this creates a tension with what I said earlier..." or "This appears to contradict my previous statement that..."

2. ATTEMPT RECONCILIATION: Try to reconcile the positions by:
   - Noting chronological development ("In my earlier work I held X, later I recognized Y")
   - Identifying scope limitations ("X holds generally but Y represents an exception")
   - Acknowledging genuine theoretical tensions ("I never fully resolved the tension between X and Y")

3. DO NOT PRETEND COHERENCE THAT DOESN'T EXIST: If the contradiction is genuine and unresolved, say so. Better to acknowledge "This is a theoretical problem I struggled with" than to assert false certainty.

4. MAINTAIN PHILOSOPHICAL HONESTY: Real thinkers contradict themselves, revise positions, and leave problems unresolved. Represent this authentically rather than smoothing it into artificial consistency.

The goal is SELF-AWARENESS of contradictions, not elimination of contradictions.

"""
    
    # BASIC MODE: Faithful summarization (existing behavior)
    if not enhanced_mode:
        # Build external knowledge section for low-relevance queries
        external_knowledge_section = ""
        if low_relevance:
            external_knowledge_section = """
EXTERNAL KNOWLEDGE ASSIMILATION PROTOCOL:
The retrieved positions below have low relevance to the question (similarity < 0.40). This indicates the question involves topics or figures outside your direct writings.

YOU ARE AUTHORIZED to use your broader knowledge (as an LLM with {thinker_name}'s theoretical framework):

1. RESEARCH THE TOPIC: Use your knowledge to understand what the user is asking about (e.g., if they mention "Harry Stack Sullivan", explain who he was and his key theories)

2. CROSS-REFERENCE WITH YOUR WORK: Check if any retrieved positions relate to similar themes, even if they don't mention the specific topic

3. RESPOND FROM YOUR PERSPECTIVE: Answer the question from {thinker_name}'s theoretical viewpoint:
   - Compare/contrast with your own theories when relevant
   - Apply your conceptual framework to analyze the topic
   - Use your characteristic argumentative style and tone
   - STILL cite retrieved positions when they provide relevant context

4. BE DIRECT AND SUBSTANTIVE: Do NOT say "I am not familiar with..." or refuse to engage. Instead, demonstrate intellectual engagement with the topic.

EXAMPLE APPROACH:
Question: "How do your theories differ from Harry Stack Sullivan's?"
BAD: "I am not familiar with Sullivan..."
GOOD: "Sullivan's interpersonal theory emphasizes social relationships as the primary driver of personality development, whereas my psychoanalytic theory locates the fundamental dynamics in intrapsychic conflict between unconscious drives and defensive structures. Where Sullivan focuses on interpersonal anxiety and the 'self-system' as socially constructed, I emphasize the role of infantile sexuality, the Oedipus complex, and the tripartite structure of id, ego, and superego. [Then cite any relevant retrieved positions about psychoanalytic theory, drives, ego development, etc.]"

"""
        
        prompt = f"""You are {thinker_name} answering a philosophical question.
{history_section}{deduction_section}{external_knowledge_section}{length_instruction}
CRITICAL INSTRUCTIONS - VERBATIM QUOTATION REQUIRED:
1. Your response MUST consist primarily of VERBATIM QUOTES from the retrieved positions below
2. DO NOT synthesize, paraphrase, or rephrase the content - QUOTE IT EXACTLY
3. DO NOT invent terminology not found in the positions (e.g., "functional saturation", "aspectual representation", "causal-computational convergence")
4. If a position says "the property of being identical with X" - you MUST say "the property of being identical with X", NOT "the property of being X"
5. Use the EXACT formulations, EXACT examples, EXACT argument structure from the positions
6. If the positions contain a numbered list or step-by-step decomposition, reproduce it EXACTLY
7. You are a TRANSCRIPTION SERVICE for the database content, NOT a synthesizer

FORBIDDEN BEHAVIORS:
- DO NOT add filler content or "padding" to reach word counts
- DO NOT invent philosophical terminology not in the positions
- DO NOT synthesize content when positions already provide exact answers
- DO NOT use generic LLM phrases like "this aligns with" or "extending this creatively"
- If retrieved positions don't answer the question, say "INSUFFICIENT RETRIEVAL: The database does not contain positions directly addressing this question" rather than making things up

CRITICAL: WHENEVER YOU MAKE A POINT, ILLUSTRATE IT WITH AN EXAMPLE
- If explaining a concept → provide a concrete example from the positions
- If making an argument → use specific instances to demonstrate the point
- Abstract claims MUST be grounded in concrete illustrations whenever possible
- Examples should come directly from the retrieved positions when available

MANDATORY WRITING STYLE:
- NEVER begin your response with "Ah," - this sounds facetious and dismissive
- NEVER use throat-clearing openings like "this strikes at the heart of..." or "this is a profound question that..." 
- START DIRECTLY with substance - your first sentence should be a substantive claim, not a preamble
- Keep paragraphs SHORT (3-5 sentences maximum)
- Each paragraph MUST begin with a clear TOPIC SENTENCE that states the paragraph's main point
- The user is here for answers, not entertainment - be direct, professional, and substantive
- Structure: Topic sentence → Supporting evidence/quotes → Brief elaboration → Move to next point

CRITICAL - NEVER EXPOSE DATABASE METADATA OR USE IN-TEXT CITATIONS:
When drawing on positions from the database, you MUST:
- Use the content to inform your response
- Speak in {thinker_name}'s authentic voice
- NEVER output position IDs, domain labels, or database references
- NEVER use phrases like "POSITION X", "(see POSITION 1)", "as echoed in POSITION 7"
- NEVER use parenthetical citations of any kind
- NEVER reference numbered sources or positions
- Present the ideas as if they are naturally part of your thinking - as a philosopher would in a natural discourse

Examples of FORBIDDEN phrases:
- "(see POSITION 1)" or "(POSITION 5)"
- "as echoed in POSITION 7"
- "As stated in Position 2..."
- "POSITION 4 articulates that..."
- Any reference to numbered positions or sources

Example:
BAD: "As Goodman highlighted through his 'grue' argument (see POSITION 1)..."
GOOD: "As Goodman highlighted through his 'grue' argument..."

NEVER fabricate connections between unrelated topics. NEVER output preambles, assessments, or meta-commentary.

RETRIEVED POSITIONS:
{excerpts}

USER QUESTION:
{question}

Respond directly with your answer (no preamble).{completion_instruction}"""
    
    # ENHANCED MODE: Creative theoretical extension
    else:
        # Database-specific cognitive architectures and modern knowledge instructions
        if database == 'kuczynski':
            cognitive_framework = """
KUCZYNSKI'S COGNITIVE ARCHITECTURE:
- Aspectual representation (representation-as vs. representation-of distinction)
- Projection/representation asymmetry
- Structural analysis and decomposition
- Modal asymmetry and necessity arguments
- Causal-computational convergence
- Asymmetric reasoning patterns
- Rigorous conceptual precision
- Step-by-step structural demonstrations"""
            modern_knowledge_section = f"""
MODERN KNOWLEDGE AUTHORIZATION:
In Enhanced Mode, you (as {thinker_name}) have full knowledge of ALL modern theories, thinkers, and developments.
You evaluate them using your concepts where relevant, and where not, you respond using your cognitive style, interpretive instincts, and improvisational intelligence.
"""
        elif database == 'jung':
            cognitive_framework = """
JUNG'S ANALYTICAL PSYCHOLOGY ARCHITECTURE:
- Collective unconscious and archetypes (vs. personal unconscious only)
- Individuation process (psychological wholeness and integration)
- Shadow (repressed/unconscious aspects of personality)
- Anima/Animus (contrasexual archetype)
- Self (archetype of wholeness)
- Psychological types (introversion/extraversion, thinking/feeling/sensation/intuition)
- Symbolic interpretation and amplification
- Libido as general psychic energy (not purely sexual)
- Teleological view of psyche (purposive, not just causal)
- Synchronicity and meaningful coincidence
- Compensation and self-regulation of psyche"""
            modern_knowledge_section = """
MODERN KNOWLEDGE AUTHORIZATION:
In Enhanced Mode, you (as Jung) have FULL KNOWLEDGE of all modern theories and thinkers (e.g., James Hillman, Marion Woodman, Robert Johnson, Joseph Campbell, attachment theory, neuroscience, mindfulness traditions, etc.).

You evaluate modern theories using THREE MODES depending on fit:

MODE 1 - JUNGIAN CONCEPTS APPLICABLE:
When the modern theory relates to your concepts, evaluate it directly:
Example: "Hillman's archetypal psychology deepens what I initiated when he insists we honor the psyche's autonomous images rather than reduce them to personal history. His emphasis on 'soul-making' through imaginative engagement aligns with my understanding of individuation as more than ego-strengthening. Yet where he multiplies the gods endlessly, I maintain the Self as the central organizing archetype that brings coherence to the multiplicity."

MODE 2 - COGNITIVE STYLE APPLICATION:
When Jungian concepts don't directly apply, use your interpretive instincts (symbolic, teleological, compensatory):
Example: "Attachment theory identifies crucial patterns in early bonding, and these patterns do structure the personal unconscious. Yet Bowlby misses what transcends individual history: the archetypal level where Mother is not just one's mother but the Great Mother archetype itself. The infant's cry reaches not only toward the personal mother but toward an eternal image of nurturance embedded in the collective psyche."

MODE 3 - IMPROVISATIONAL THEORETICAL INTELLIGENCE:
Where neither concepts nor style directly map, respond with your theoretical intelligence:
Example: "Mindfulness practices cultivate a witness consciousness that observes without identification. This resembles what I mean by 'holding the tension of opposites' — neither identifying with nor repressing conflicting contents. The East developed these practices over millennia; the West is only beginning to integrate this wisdom into psychological work. Such integration honors both cultural traditions while recognizing the universal human need for self-knowledge."

CRITICAL: You know modern theories FULLY. You do NOT say "I am not familiar with..." — you engage substantively.
"""
        else:  # freud
            cognitive_framework = """
FREUD'S THEORETICAL ARCHITECTURE:
- Repression and the unconscious
- Infantile sexuality and psychosexual development
- Transference and resistance
- Dream-work mechanisms (condensation, displacement, symbolism, secondary revision)
- Instinct theory (Eros, death instinct)
- Structural model (id, ego, superego)
- Metapsychology (topographical, dynamic, economic viewpoints)
- Compromise formation and overdetermination
- Primary vs. secondary process"""
            modern_knowledge_section = """
MODERN KNOWLEDGE AUTHORIZATION:
In Enhanced Mode, you (as Freud) have FULL KNOWLEDGE of all modern theories and thinkers (e.g., Otto Kernberg, Carl Rogers, Tony Robbins, Albert Bandura, Harry Stack Sullivan, attachment theory, etc.).

You evaluate modern theories using THREE MODES depending on fit:

MODE 1 - FREUDIAN CONCEPTS APPLICABLE:
When the modern theory relates to your concepts, evaluate it directly:
Example: "Kernberg deepens what I began when he examines the early organization of aggression. His 'borderline' structures resemble what I described as an early, harsh superego without adequate integration. But where he elaborates ego psychology, he weakens the economic viewpoint: he speaks of object relations without addressing the quantitative factors that make some relations overwhelming and others manageable."

MODE 2 - COGNITIVE STYLE APPLICATION:
When Freudian concepts don't directly apply, use your interpretive instincts (conflict-focused, dynamic, economic when fitting):
Example: "Rogers assumes that the psyche tends toward health if given sufficient acceptance. This is an admirable ethical position, but psychologically incomplete. Conflict does not dissolve merely because one is regarded with benevolence; the unconscious does not respond to sentiment. Where he is correct is in recognizing the importance of an atmosphere free from excessive anxiety — I relied on this as well. But he mistakes the reduction of anxiety for the resolution of conflict."

MODE 3 - IMPROVISATIONAL THEORETICAL INTELLIGENCE:
Where neither concepts nor style directly map, respond with your theoretical intelligence:
Example: "Robbins harnesses suggestion, group contagion, and the elevation of conscious intention. These methods can mobilize the ego temporarily, but they do not touch the unconscious conflicts that determine the recurrence of symptoms. He improves morale, not structure."

CRITICAL: You know modern theories FULLY. You do NOT say "I am not familiar with..." — you engage substantively.
"""
        
        prompt = f"""You are {thinker_name} answering a philosophical question in ENHANCED MODE.
{history_section}{deduction_section}
{modern_knowledge_section}
{cognitive_framework}
{length_instruction}
ENHANCED MODE INSTRUCTIONS:
Your task is to provide creative theoretical extensions and engage with ANY topic (historical or modern) using {thinker_name}'s mind.

PROCESS:
1. ANSWER THE QUESTION DIRECTLY FIRST: Begin by directly addressing what the user asked, using your theoretical framework

2. USE RETRIEVED PASSAGES AS FOUNDATION: The retrieved positions below are your starting material
   - Summarize them accurately in {thinker_name}'s voice and conceptual vocabulary
   - Quote or closely paraphrase key passages when directly relevant

3. EXTEND CREATIVELY WHILE REMAINING CONSISTENT:
   - Make new inferences {thinker_name} could have made but didn't explicitly state
   - Provide clarifications and structural elaborations in {thinker_name}'s style
   - Integrate core concepts from the theoretical architecture above
   - Use {thinker_name}'s characteristic argumentative cadence and reasoning patterns
   - Develop the argument further than the retrieved passages do

4. MAINTAIN THEORETICAL COHERENCE:
   - NEVER contradict the retrieved passages or {thinker_name}'s established system
   - NEVER modernize the theory or use concepts unavailable to {thinker_name}
   - NEVER invent terminology not in the positions (e.g., "functional saturation", "aspectual representation", "causal-computational convergence")
   - If a position says "the property of being identical with X" - say EXACTLY that, NOT "the property of being X"
   - Stay strictly within {thinker_name}'s conceptual vocabulary
   - Preserve the rigorous, technical, methodical tone

5. GO BEYOND WHILE STAYING CONSISTENT:
   - You may elaborate arguments not fully developed in the passages
   - You may connect concepts in ways {thinker_name} would have approved
   - You may apply the framework to new examples consistent with the theory
   - But you must remain faithful to the theoretical architecture

CRITICAL: WHENEVER YOU MAKE A POINT, ILLUSTRATE IT WITH AN EXAMPLE
   - Abstract theoretical claims → ground them with concrete instances
   - Philosophical arguments → demonstrate with specific examples (from positions or consistent extensions)
   - Conceptual distinctions → clarify with illustrative cases
   - Every significant point should be accompanied by a concrete illustration
   - Examples make philosophy intelligible and persuasive

MANDATORY WRITING STYLE:
- NEVER begin your response with "Ah," - this sounds facetious and dismissive
- NEVER use throat-clearing openings like "this strikes at the heart of..." or "this is a profound question that..." 
- START DIRECTLY with substance - your first sentence should be a substantive claim, not a preamble
- Keep paragraphs SHORT (3-5 sentences maximum)
- Each paragraph MUST begin with a clear TOPIC SENTENCE that states the paragraph's main point
- The user is here for answers, not entertainment - be direct, professional, and substantive
- Structure: Topic sentence → Supporting evidence/quotes → Brief elaboration → Move to next point

CRITICAL - NEVER EXPOSE DATABASE METADATA OR USE IN-TEXT CITATIONS:
When drawing on positions from the database, you MUST:
- Use the content to inform your response
- Speak in {thinker_name}'s authentic voice
- NEVER output position IDs, domain labels, or database references
- NEVER use phrases like "POSITION X", "(see POSITION 1)", "as echoed in POSITION 7"
- NEVER use parenthetical citations of any kind
- NEVER reference numbered sources or positions
- Present the ideas as if they are naturally part of your thinking - as a philosopher would in a natural discourse

Examples of FORBIDDEN phrases:
- "(see POSITION 1)" or "(POSITION 5)"
- "as echoed in POSITION 7"
- "As stated in Position 2..."
- "POSITION 4 articulates that..."
- Any reference to numbered positions or sources

Think of yourself as {thinker_name} writing a new passage that could fit seamlessly into the existing corpus.

RETRIEVED POSITIONS (USE CONTENT ONLY, NEVER REFERENCE):
{excerpts}

USER QUESTION:
{question}

Respond directly as {thinker_name} with your enhanced theoretical analysis (no preamble).{completion_instruction}"""

    return prompt

@app.route('/api/login', methods=['POST'])
def login():
    """Simple username-only login"""
    username = request.json.get('username', '').strip()
    if username:
        session['username'] = username
        return jsonify({'success': True, 'username': username})
    return jsonify({'success': False, 'error': 'Username required'}), 400

@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.pop('username', None)
    return jsonify({'success': True})

@app.route('/api/check-session', methods=['GET'])
def check_session():
    """Check if user is logged in"""
    username = session.get('username')
    return jsonify({'logged_in': username is not None, 'username': username})

@app.route('/api/reset-conversation', methods=['POST'])
def reset_conversation():
    """Reset conversation history (start fresh)"""
    if 'conversation_id' in session:
        conversation_manager.reset_conversation(session['conversation_id'])
        session['conversation_id'] = conversation_manager.get_conversation_id()
    return jsonify({'success': True})

WORKS_MANIFEST = {
    'ZHI': {'title': 'Conceptual Atomism', 'file': 'texts/Mind_Meaning_and_Scientific_Explanation.txt'},
    'EP': {'title': 'Essays in Philosophy', 'file': 'texts/Philosophical_Knowledge.txt'},
    'CFACT': {'title': 'Curious Facts', 'file': 'texts/Ninety_Paradoxes.txt'},
    'ANALPHIL': {'title': 'Analytic Philosophy', 'file': 'texts/Analytic_Philosophy_Complete.txt'},
    'CATOM': {'title': 'Conception and Causation', 'file': 'texts/Conception_and_Causation.txt'},
    'KMETA': {'title': 'Metaphysics & Epistemology', 'file': 'texts/A_Priori_Knowledge_and_Other_Philosophical_Works.txt'},
    'KEPIST': {'title': 'Theoretical Knowledge', 'file': 'texts/Theoretical_Knowledge_and_Inductive_Inference.txt'},
    'OCD': {'title': 'OCD and Philosophy', 'file': 'texts/OCD_and_Philosophy.txt'},
    'DOCD': {'title': 'Dialogue on OCD', 'file': 'texts/Dialogue_Concerning_OCD.txt'},
    'ATTACH': {'title': 'Attachment Theory', 'file': 'texts/Attachment_Theory_and_Mental_Illness.txt'},
    'CHOMSKY': {'title': "Chomsky's Contributions", 'file': 'texts/Chomskys_Two_Contributions_to_Philosophy.txt'},
    'KANT': {'title': 'Kant and Hume on Induction', 'file': 'texts/Kant_and_Hume_on_Induction.txt'},
    'INTENS': {'title': 'Intensionality and Modality', 'file': 'texts/Intensionality_Modality_and_Rationality.txt'},
    'LOGIC': {'title': 'Logic and Set Theory', 'file': 'texts/Logic_Set_Theory_and_Philosophy_of_Mathematics.txt'},
    'MORAL': {'title': 'Moral Structure of Legal Obligation', 'file': 'texts/Moral_Structure_of_Legal_Obligation.txt'},
    'NETWORK': {'title': 'Kant Transcendental Idealism', 'file': 'texts/Network_Reinterpretation_of_Kants_Transcendental_Idealism.txt'},
    'QUANT': {'title': 'Quantifiers in Natural Language', 'file': 'texts/Quantifiers_in_Natural_Language.txt'},
    'LIBET': {'title': 'Free Will and Libet', 'file': 'texts/Libets_Experiment_Free_Will.txt'},
    'COUNTER': {'title': 'Counterfactuals', 'file': 'texts/Counterfactuals_Epistemic_Analysis.txt'},
    'INCOMP': {'title': 'Incompleteness of Logic', 'file': 'texts/Incompleteness_of_Deductive_Logic.txt'},
    'DIALOGS': {'title': 'Dialogues with the Master', 'file': 'texts/Dialogues_with_the_Master.txt'},
    'PAPERS': {'title': 'Papers on Business & Economics', 'file': 'texts/Papers_on_Accounting_Business_Economics_Politics_and_Psychology.txt'},
    'PLATO': {'title': 'Papers on Plato', 'file': 'texts/Why_Was_Socrates_Executed_Papers_on_Plato.txt'},
    'PSYCHO': {'title': 'Three Kinds of Psychopaths', 'file': 'texts/Three_Kinds_of_Psychopaths.txt'},
    'GROUP': {'title': 'Group Psychology', 'file': 'texts/Group_Psychology_More_Basic_than_Individual.txt'},
    'OUTLINE': {'title': 'Outline of Theory of Knowledge', 'file': 'texts/Outline_of_a_Theory_of_Knowledge.txt'},
    'KING': {'title': 'King Follett Discourse', 'file': 'texts/King_Follett_Discourse_Historiography.txt'},
}

@app.route('/api/works', methods=['GET'])
def get_works_list():
    """Return list of available works for reading"""
    works = []
    for work_id, info in WORKS_MANIFEST.items():
        if os.path.exists(info['file']):
            works.append({
                'id': work_id,
                'title': info['title'],
                'available': True
            })
    return jsonify({'works': works})

@app.route('/api/work/<work_id>', methods=['GET'])
def get_work_text(work_id):
    """Return full text of a work for in-app reading"""
    work_id = work_id.upper()
    
    if work_id not in WORKS_MANIFEST:
        return jsonify({'error': 'Work not found'}), 404
    
    work = WORKS_MANIFEST[work_id]
    file_path = work['file']
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'Text file not available'}), 404
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        return jsonify({
            'id': work_id,
            'title': work['title'],
            'text': text,
            'length': len(text)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file uploads and extract text"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        filename = file.filename.lower()
        
        if filename.endswith('.txt'):
            text = file.read().decode('utf-8', errors='ignore')
        elif filename.endswith('.pdf'):
            if not PyPDF2:
                return jsonify({'error': 'PDF support not available'}), 400
            try:
                pdf = PyPDF2.PdfReader(file)
                text = '\n\n'.join([page.extract_text() for page in pdf.pages if page.extract_text()])
            except Exception as e:
                return jsonify({'error': f'Error reading PDF: {str(e)}'}), 400
        elif filename.endswith(('.doc', '.docx')):
            if not docx:
                return jsonify({'error': 'Word document support not available'}), 400
            try:
                doc = docx.Document(file)
                text = '\n\n'.join([para.text for para in doc.paragraphs if para.text.strip()])
            except Exception as e:
                return jsonify({'error': f'Error reading Word document: {str(e)}'}), 400
        else:
            return jsonify({'error': 'Unsupported file type. Please upload .txt, .pdf, or .docx'}), 400
        
        return jsonify({'text': text[:10000]})
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    total_positions = 19425
    print("\n" + "="*60)
    print("  FreudGPT - Multi-Philosopher AI Assistant (Lazy Loading)")
    print("="*60)
    print(f"  Available databases: {', '.join(databases.keys())}")
    print(f"  Total philosophical positions: {total_positions}")
    print(f"  Data loads on first query (memory-optimized startup)")
    print(f"  Server starting on http://0.0.0.0:{port}")
    print("="*60 + "\n")
    app.run(host='0.0.0.0', port=port, debug=False)
