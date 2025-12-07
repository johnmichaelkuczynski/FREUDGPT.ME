# FreudGPT - The Thinker's Workshop

## Overview
FreudGPT is an intelligent conversational AI application that delivers in-depth, streaming responses grounded in the works of various philosophers. Its core purpose is to make extensive philosophical works accessible and interactive, enabling detailed inquiry through semantic search over comprehensive databases. The application currently supports Freud, Kuczynski, and Jung, with a total of 19,425 unique philosophical positions. The vision is to bridge foundational texts with modern inquiry by transforming from simple impersonation to "executable philosophical reasoning" via forward-chaining inference engines, which deduce theoretical principles before LLM prose generation.

## User Preferences
- **API Integration**: Prefers direct Anthropic API integration over Replit AI Integrations
- **Response Style**: AI responses must faithfully represent Kuczynski's actual arguments, examples, and rigorous writing style, not glib paraphrases. This means quoting or very closely paraphrasing the actual text from positions, using his exact examples and rhetorical questions, preserving his step-by-step argumentative structure, and matching his rigorous, technical, methodical, and detailed tone. The AI should not summarize, simplify, or "make accessible" his work.
- **Argumentation**: The AI prompt is configured to not argue against user input when they present a position; it defaults to SUPPORT/EXPAND mode, but acknowledges mismatches if retrieved positions conflict.
- **External Knowledge Assimilation**: When questions involve topics outside the database (e.g., "How do your theories differ from Harry Stack Sullivan's?"), the app automatically detects low-relevance searches (similarity < 0.40) and activates External Knowledge mode, which explicitly authorizes the LLM to: (1) research the topic using its broader knowledge, (2) cross-reference with the database, (3) respond from the thinker's perspective with substantive analysis rather than refusals. This implements the vision of "Freud's brain with Claude/GPT attached" rather than purely historical responses.

## System Architecture

### UI/UX: The Thinker's Workshop
- **Theme**: Bright Wellness with a color palette of deep teal (#0F766E), warm off-white (#FFFDFB), light mint (#F0FDFA), and coral-orange accents (#F97316).
- **Typography**: Playfair Display (headings), Inter (body), Crimson Pro (quotes).
- **Layout**: Dual-panel design with "The Dialogue" (70%) for real-time AI responses and "The Archive" (30%) for synchronized source texts.
- **Interactive Features**: Avatar-based thinker selection, knowledge panel popups during wait times, source highlighting, styled controls for response length and Enhanced Mode, and in-app reader for viewing full philosophical works.
- **In-App Reader**: Source links open a modal reader displaying the complete work text from the `texts/` folder (27 Kuczynski works available). Features include text search with highlighting, adjustable font sizes, and keyboard navigation.
- **Animations**: Orbiting thinker emojis, typewriter streaming effects, and smooth panel transitions.

### Technical Implementations
- **Core Functionality**: Supports multi-database (Freud, Kuczynski, Jung), semantic search, streaming AI responses, multi-AI provider integration, conversation memory with self-contradiction detection, content ingestion from various file types, and source citations.
- **Dual Response Modes**: Basic Mode for faithful summarization/paraphrasing and External Knowledge Assimilation, and Enhanced Mode for creative theoretical extension and modern knowledge integration within the thinker's framework.
- **Backend**: Flask handles application logic, SSE streaming, and integration with the semantic search module.
- **Frontend**: Minimal HTML, CSS, and vanilla JavaScript for dynamic interactions and SSE.
- **Data Management**: Philosophical positions are stored in JSON files with cached pre-computed embeddings.
- **ML/NLP**: Utilizes OpenAI's `text-embedding-3-small` API for embeddings and scikit-learn for cosine similarity. `PyPDF2` and `python-docx` are used for text extraction.
- **Design Decisions**: Emphasizes faithful representation of thinkers' styles, token-by-token streaming, a simplified data model focusing on philosophical positions, and CPU-only PyTorch for Replit compatibility.

## Recent Progress (December 2025)
- **Resizable Panels**: Users can now drag the divider between "The Dialogue" and "The Archive" panels to adjust their widths. Sizes persist across sessions via localStorage.
- **UI Color Scheme Overhaul**: Transformed from dark academia to bright wellness theme with teal, mint, and coral-orange colors for a fresh, modern look
- **Memory-Optimized Lazy Loading**: Startup memory reduced from 500+ MB to ~166 MB for Render deployment compatibility (512 MB limit). Databases and embeddings now lazy-load on first query, not at startup. Random-quotes endpoint uses cached positions without loading embeddings.
- **Answer Quality Significantly Improved**: Prompt hardening now requires VERBATIM quotes only, forbids invented terminology, and enforces exact formulations from the database
- **Canonical Query Mapping**: Force-injects correct positions for key philosophical queries (proposition composition, truth/instantiation) bypassing semantic search limitations; retrieval depth increased to top_k=15
- **Contemplation UX**: Scrolling marquee displays real position statements (30-400 chars) during thinking animation with smooth CSS animations
- **Archive Panel Redesigned**: Quote font increased to 1.4em, complete position statements (100-800 chars) displayed without truncation

## External Dependencies
- **AI Providers**: Anthropic Claude, OpenAI, DeepSeek, Perplexity, Grok (xAI).
- **Python Libraries**: Flask, sentence-transformers, scikit-learn, PyTorch (CPU), PyPDF2, python-docx, Gunicorn, gevent.