#!/usr/bin/env python3
"""
Freud Complete Works Position Extraction Pipeline
Extracts atomic philosophical positions from raw text files
"""

import json
import re
import os
from typing import List, Dict, Optional
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class FreudTextPreprocessor:
    """Cleans and segments raw Freud text files"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.raw_text = self._load_file()
        self.part_number = self._extract_part_number()
        
    def _load_file(self) -> str:
        """Load raw text file"""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _extract_part_number(self) -> Optional[int]:
        """Extract part number from filename"""
        match = re.search(r'Part(\d+)', self.filepath)
        return int(match.group(1)) if match else None
    
    def clean_text(self, text: str) -> str:
        """Remove headers, page numbers, and normalize text"""
        # Remove page headers/footers that repeat
        text = re.sub(r'\n\s*The Interpretation Of Dreams\s*\n', '\n', text)
        text = re.sub(r'\n\s*Studies On Hysteria\s*\n', '\n', text)
        text = re.sub(r'\n\s*\d{3,4}\s*\n', '\n', text)  # Remove standalone page numbers
        
        # Normalize Unicode issues
        text = text.replace('\ufeff', '')  # Remove BOM
        text = text.replace('\u2019', "'")  # Normalize apostrophes
        text = text.replace('\u2013', '-')  # Normalize dashes
        text = text.replace('\u2014', '--')
        
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        
        return text.strip()
    
    def extract_work_sections(self) -> List[Dict[str, str]]:
        """Detect and extract individual works and major sections"""
        cleaned = self.clean_text(self.raw_text)
        
        # Split by major section headers (all caps titles)
        sections = []
        
        # Look for section patterns
        section_pattern = r'\n\s*([A-Z][A-Z\s&\-,\']+)\n\s*\n'
        matches = list(re.finditer(section_pattern, cleaned))
        
        for i, match in enumerate(matches):
            title = match.group(1).strip()
            start_pos = match.end()
            end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(cleaned)
            content = cleaned[start_pos:end_pos].strip()
            
            # Only include substantial sections (>500 chars)
            if len(content) > 500 and not self._is_table_of_contents(title):
                sections.append({
                    'title': title,
                    'content': content,
                    'part': self.part_number,
                    'word_count': len(content.split())
                })
        
        return sections
    
    def _is_table_of_contents(self, title: str) -> bool:
        """Check if section is table of contents"""
        toc_keywords = ['TABLE OF CONTENTS', 'CONTENTS', 'ALPHABETICAL', 'CHRONOLOGICAL']
        return any(kw in title.upper() for kw in toc_keywords)
    
    def chunk_text(self, text: str, chunk_size: int = 3000) -> List[str]:
        """Split text into manageable chunks by paragraphs"""
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = []
        current_length = 0
        
        for para in paragraphs:
            para_length = len(para.split())
            
            if current_length + para_length > chunk_size and current_chunk:
                chunks.append('\n\n'.join(current_chunk))
                current_chunk = [para]
                current_length = para_length
            else:
                current_chunk.append(para)
                current_length += para_length
        
        if current_chunk:
            chunks.append('\n\n'.join(current_chunk))
        
        return chunks


class PositionExtractor:
    """Extracts atomic philosophical positions using LLM"""
    
    def __init__(self, client: OpenAI):
        self.client = client
        
    def extract_positions(self, text_chunk: str, work_title: str, part: int) -> List[Dict]:
        """Extract atomic philosophical positions from a text chunk"""
        
        extraction_prompt = f"""You are analyzing Sigmund Freud's philosophical and psychoanalytic writings to extract discrete, atomic philosophical positions.

WORK: {work_title}
SOURCE: Complete Works Part {part}

INSTRUCTIONS:
1. Extract ONLY clear, discrete philosophical claims, theories, or positions
2. Each position must be atomic (one core idea)
3. Focus on theoretical claims, not case descriptions or biographical details
4. Extract positions that are substantive and significant
5. Each position should be 10-150 words

For each position, output JSON with:
- "title": Brief descriptive title (5-10 words)
- "text_evidence": The actual philosophical claim/position
- "domain": Category (choose from: PHILOSOPHY_OF_MIND_&_PSYCHOLOGY, METAPSYCHOLOGY, CLINICAL_THEORY, DREAM_THEORY, SEXUALITY_THEORY, CULTURAL_THEORY, DEVELOPMENTAL_THEORY, PSYCHOPATHOLOGY, TECHNIQUE, GENERAL_PHILOSOPHY)
- "quote": Direct quote from text if available (optional)

TEXT TO ANALYZE:
{text_chunk[:4000]}

Output a JSON array of positions. If no clear positions exist, return empty array []."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert in philosophy and psychoanalytic theory, specialized in extracting atomic philosophical positions from dense academic texts."},
                    {"role": "user", "content": extraction_prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Handle both array and object with positions key
            if isinstance(result, list):
                positions = result
            elif 'positions' in result:
                positions = result['positions']
            else:
                positions = []
            
            return positions
            
        except Exception as e:
            print(f"Extraction error: {e}")
            return []
    
    def validate_position(self, position: Dict) -> bool:
        """Validate extracted position meets quality standards"""
        required_fields = ['title', 'text_evidence', 'domain']
        
        # Check required fields exist
        if not all(field in position for field in required_fields):
            return False
        
        # Check text length
        text_len = len(position['text_evidence'].split())
        if text_len < 10 or text_len > 200:
            return False
        
        # Check domain is valid
        valid_domains = [
            'PHILOSOPHY_OF_MIND_&_PSYCHOLOGY',
            'METAPSYCHOLOGY',
            'CLINICAL_THEORY',
            'DREAM_THEORY',
            'SEXUALITY_THEORY',
            'CULTURAL_THEORY',
            'DEVELOPMENTAL_THEORY',
            'PSYCHOPATHOLOGY',
            'TECHNIQUE',
            'GENERAL_PHILOSOPHY'
        ]
        if position['domain'] not in valid_domains:
            return False
        
        return True


class DatabaseBuilder:
    """Builds structured database from extracted positions"""
    
    def __init__(self, existing_db_path: Optional[str] = None):
        self.positions = []
        self.position_counter = 1
        
        if existing_db_path and os.path.exists(existing_db_path):
            with open(existing_db_path, 'r') as f:
                existing = json.load(f)
                if isinstance(existing, dict) and 'positions' in existing:
                    self.position_counter = len(existing['positions']) + 1
    
    def add_position(self, position: Dict, work_title: str, work_id: str, year: Optional[int] = None):
        """Add validated position to database"""
        
        # Generate position ID
        position_id = f"FREUD-{self.position_counter:04d}"
        self.position_counter += 1
        
        # Build complete position record
        record = {
            'position_id': position_id,
            'id': position_id,
            'title': position['title'],
            'text_evidence': position['text_evidence'],
            'domain': position['domain'],
            'source': [work_title],
            'work_id': work_id,
            'work_title': work_title,
            'year': year
        }
        
        if 'quote' in position and position['quote']:
            record['quote'] = position['quote']
        
        self.positions.append(record)
    
    def save_database(self, output_path: str, version: str = "10.0"):
        """Save database to JSON file"""
        
        database = {
            'metadata': {
                'version': version,
                'edition': 'COMPLETE_WORKS_EXTRACTION',
                'compilation_date': '2025-11-18',
                'compiler': 'Automated LLM Extraction Pipeline',
                'total_positions': len(self.positions),
                'description': 'Philosophical positions extracted from Freud Complete Works raw text'
            },
            'positions': self.positions
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(database, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved {len(self.positions)} positions to {output_path}")


def main():
    """Main extraction pipeline"""
    
    print("=" * 60)
    print("FREUD COMPLETE WORKS POSITION EXTRACTION PIPELINE")
    print("=" * 60)
    
    # Files to process
    text_files = [
        'attached_assets/Freud - Complete Works (Over 4000 pages, Most Comprehensive Version Available)_Part1_1763442245951.txt',
        'attached_assets/Freud - Complete Works (Over 4000 pages, Most Comprehensive Version Available)_Part2_1763442245951.txt',
        'attached_assets/Freud - Complete Works (Over 4000 pages, Most Comprehensive Version Available)_Part3_1763442245949.txt',
        'attached_assets/Freud - Complete Works (Over 4000 pages, Most Comprehensive Version Available)_Part4_1763442245950.txt',
        'attached_assets/Freud - Complete Works (Over 4000 pages, Most Comprehensive Version Available)_Part5_1763442245950.txt'
    ]
    
    # Initialize components
    extractor = PositionExtractor(client)
    db_builder = DatabaseBuilder('data/FREUD_DATABASE_v9.json')
    
    total_extracted = 0
    total_valid = 0
    
    # Process each file
    for filepath in text_files:
        if not os.path.exists(filepath):
            print(f"⚠ File not found: {filepath}")
            continue
        
        print(f"\n Processing: {os.path.basename(filepath)}")
        
        # Preprocess
        preprocessor = FreudTextPreprocessor(filepath)
        sections = preprocessor.extract_work_sections()
        
        print(f"   Found {len(sections)} sections")
        
        # Process each section
        for section in sections[:5]:  # Limit to first 5 sections per file for initial run
            print(f"   Extracting from: {section['title'][:50]}...")
            
            # Chunk large sections
            chunks = preprocessor.chunk_text(section['content'], chunk_size=2500)
            
            for chunk in chunks[:3]:  # Limit chunks per section
                positions = extractor.extract_positions(
                    chunk,
                    section['title'],
                    section['part']
                )
                
                # Validate and add
                for pos in positions:
                    if extractor.validate_position(pos):
                        db_builder.add_position(
                            pos,
                            work_title=section['title'],
                            work_id=f"WORK-PART{section['part']}"
                        )
                        total_valid += 1
                    total_extracted += 1
    
    print(f"\n{'=' * 60}")
    print(f"EXTRACTION COMPLETE")
    print(f"Total extracted: {total_extracted}")
    print(f"Total valid: {total_valid}")
    print(f"Validation rate: {(total_valid/total_extracted*100) if total_extracted > 0 else 0:.1f}%")
    print(f"{'=' * 60}\n")
    
    # Save database
    output_path = 'data/FREUD_DATABASE_EXTRACTED.json'
    db_builder.save_database(output_path)
    
    print(f"\n✓ Pipeline complete! New database saved to: {output_path}")
    print(f"  Next steps:")
    print(f"  1. Review extracted positions for quality")
    print(f"  2. Generate embeddings using search.py")
    print(f"  3. Integrate into FreudGPT app")


if __name__ == '__main__':
    main()
