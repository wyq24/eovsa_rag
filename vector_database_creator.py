#!/usr/bin/env python3
"""
Enhanced Vector Database Creator for Radio Telescope RAG System
Creates intelligent vector database with metadata filtering and cross-references
"""

import json
import os
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import hashlib

# Vector database options
try:
    import chromadb
    from chromadb.config import Settings

    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False
    print("⚠️  ChromaDB not available. Install with: pip install chromadb")

# try:
#     import pinecone
#
#     PINECONE_AVAILABLE = True
# except ImportError:
#     PINECONE_AVAILABLE = False
#     print("⚠️  Pinecone not available. Install with: pip install pinecone-client")

# try:
#     from sentence_transformers import SentenceTransformer
#
#     SENTENCE_TRANSFORMERS_AVAILABLE = True
# except ImportError:
#     SENTENCE_TRANSFORMERS_AVAILABLE = False
#     print("⚠️  SentenceTransformers not available. Install with: pip install sentence-transformers")

# OpenAI for embeddings
try:
    from openai import OpenAI
    import tiktoken

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️  OpenAI not available. Install with: pip install openai tiktoken")

from dotenv import load_dotenv

load_dotenv()


class EmbeddingGenerator:
    """Generate embeddings using various models"""

    def __init__(self, model_type: str = "sentence-transformers"):
        self.model_type = model_type
        self.model = None
        self.client = None

        if model_type == "sentence-transformers" and SENTENCE_TRANSFORMERS_AVAILABLE:
            # Use a model optimized for technical/scientific content
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✅ Using SentenceTransformers model: all-MiniLM-L6-v2")
        elif model_type == "openai" and OPENAI_AVAILABLE:
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            print("✅ Using OpenAI embeddings model")
        else:
            raise ValueError(f"Model type {model_type} not available or not installed")

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text"""

        if self.model_type == "sentence-transformers":
            embedding = self.model.encode(text, convert_to_tensor=False)
            return embedding.tolist()

        elif self.model_type == "openai":
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding

    def generate_batch_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for batch of texts"""

        if self.model_type == "sentence-transformers":
            embeddings = self.model.encode(texts, convert_to_tensor=False)
            return embeddings.tolist()

        elif self.model_type == "openai":
            # Process in smaller batches to avoid rate limits
            batch_size = 20  # Reduced from 100
            all_embeddings = []

            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]

                # Retry logic for API calls
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        response = self.client.embeddings.create(
                            model="text-embedding-3-small",
                            input=batch
                        )
                        batch_embeddings = [item.embedding for item in response.data]
                        all_embeddings.extend(batch_embeddings)

                        print(f"✅ Processed batch {i // batch_size + 1}/{(len(texts) - 1) // batch_size + 1}")
                        break

                    except Exception as e:
                        if attempt == max_retries - 1:
                            print(f"❌ Failed to process batch after {max_retries} attempts: {e}")
                            raise
                        else:
                            print(f"⚠️  Batch failed, retrying... (attempt {attempt + 1})")
                            import time
                            time.sleep(2 ** attempt)  # Exponential backoff

            return all_embeddings


class TokenManager:
    """Manage token counting and text truncation for embeddings"""

    def __init__(self):
        if OPENAI_AVAILABLE:
            try:
                self.encoding = tiktoken.get_encoding("cl100k_base")
            except:
                self.encoding = None
                print("⚠️  tiktoken encoding failed, using approximation")

    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        if not text:
            return 0

        if hasattr(self, 'encoding') and self.encoding:
            return len(self.encoding.encode(str(text)))
        else:
            # Fallback approximation
            return int(len(str(text).split()) * 1.3)

    def truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        """Truncate text to fit within token limit"""
        if not text or max_tokens <= 0:
            return ""

        current_tokens = self.count_tokens(text)
        if current_tokens <= max_tokens:
            return text

        # Binary search to find the right length
        words = text.split()
        if not words:
            return ""

        left, right = 0, len(words)
        result = ""

        while left <= right:
            mid = (left + right) // 2
            candidate = ' '.join(words[:mid])
            candidate_tokens = self.count_tokens(candidate)

            if candidate_tokens <= max_tokens:
                result = candidate
                left = mid + 1
            else:
                right = mid - 1

        return result + "..." if result != text else result


class MetadataProcessor:
    """Process and optimize metadata for vector database storage"""

    def __init__(self):
        self.token_manager = TokenManager()

    @staticmethod
    def prepare_chunk_for_vectordb(chunk: Dict) -> Dict:
        """Prepare chunk data for vector database insertion"""

        metadata = chunk['metadata']
        content = chunk['content']

        # Initialize processor instance for token management
        processor = MetadataProcessor()

        # Create enhanced text for embedding with token limits
        enhanced_text = processor._create_enhanced_text_with_limits(content, metadata)

        # Create searchable metadata
        searchable_metadata = MetadataProcessor._create_searchable_metadata(metadata)

        # Create display metadata (for results)
        display_metadata = MetadataProcessor._create_display_metadata(metadata)

        return {
            'id': metadata['chunk_id'],
            'text': content,
            'enhanced_text': enhanced_text,
            'searchable_metadata': searchable_metadata,
            'display_metadata': display_metadata,
            'full_metadata': metadata
        }

    def _create_enhanced_text_with_limits(self, content: str, metadata: Dict, max_tokens: int = 7500) -> str:
        """Create enhanced text with smart truncation and prioritization"""

        if not content:
            content = "No content available"

        enhanced_parts = []
        current_tokens = 0

        # Priority 1: Original content (most important)
        content_tokens = self.token_manager.count_tokens(content)

        if content_tokens > max_tokens - 500:  # Leave room for some metadata
            # Truncate content but keep most of it
            truncated_content = self.token_manager.truncate_to_tokens(content, max_tokens - 500)
            enhanced_parts.append(truncated_content)
            current_tokens = self.token_manager.count_tokens(truncated_content)
        else:
            enhanced_parts.append(content)
            current_tokens = content_tokens

        # Priority-ordered metadata additions
        metadata_additions = [
            ("Signature", metadata.get('function_signature')),
            ("Doc", metadata.get('docstring')),
            ("Summary", metadata.get('ai_summary')),
            ("Commands", self._safe_join(metadata.get('commands_handled', []))),
            ("Hardware", self._safe_join(metadata.get('hardware_components', []))),
            ("Concepts", self._safe_join(metadata.get('key_concepts', []))),
            ("Context", metadata.get('operational_context'))
        ]

        for label, value in metadata_additions:
            if not value or current_tokens >= max_tokens:
                continue

            # Clean and truncate the value
            clean_value = str(value).strip() if value else ""
            if not clean_value:
                continue

            addition = f"{label}: {clean_value}"
            addition_tokens = self.token_manager.count_tokens(addition)

            if current_tokens + addition_tokens <= max_tokens:
                enhanced_parts.append(addition)
                current_tokens += addition_tokens
            else:
                # Try to fit a truncated version
                remaining_tokens = max_tokens - current_tokens - 10  # buffer
                if remaining_tokens > 20:  # Only if meaningful space left
                    truncated_addition = self.token_manager.truncate_to_tokens(addition, remaining_tokens)
                    if truncated_addition:
                        enhanced_parts.append(truncated_addition)
                break

        result = ' | '.join(enhanced_parts)

        # Final safety check
        if self.token_manager.count_tokens(result) > max_tokens:
            result = self.token_manager.truncate_to_tokens(result, max_tokens)

        return result

    def _safe_join(self, items: List[str]) -> str:
        """Safely join list items, handling None values"""
        if not items:
            return ""
        clean_items = [str(item).strip() for item in items if item]
        return ' '.join(clean_items[:5])  # Limit to first 5 items

    @staticmethod
    def _create_enhanced_text(content: str, metadata: Dict) -> str:
        """Create enhanced text for better embedding by including metadata context"""

        enhanced_parts = [content]

        # Add chunk type context
        chunk_type = metadata.get('chunk_type', '')
        if chunk_type:
            enhanced_parts.append(f"Type: {chunk_type}")

        # Add function signature if available
        signature = metadata.get('function_signature')
        if signature:
            enhanced_parts.append(f"Signature: {signature}")

        # Add docstring if available
        docstring = metadata.get('docstring')
        if docstring:
            enhanced_parts.append(f"Documentation: {docstring}")

        # Add AI summary if available
        ai_summary = metadata.get('ai_summary')
        if ai_summary:
            enhanced_parts.append(f"Summary: {ai_summary}")

        # Add commands handled
        commands = metadata.get('commands_handled', [])
        if commands:
            enhanced_parts.append(f"Commands: {' '.join(commands)}")

        # Add hardware components
        hardware = metadata.get('hardware_components', [])
        if hardware:
            enhanced_parts.append(f"Hardware: {' '.join(hardware)}")

        # Add key concepts
        concepts = metadata.get('key_concepts', [])
        if concepts:
            enhanced_parts.append(f"Concepts: {' '.join(concepts)}")

        # Add operational context
        op_context = metadata.get('operational_context')
        if op_context:
            enhanced_parts.append(f"Context: {op_context}")

        return ' | '.join(enhanced_parts)

    @staticmethod
    def _create_searchable_metadata(metadata: Dict) -> Dict:
        """Create metadata optimized for filtering and search"""

        return {
            # Basic identifiers
            'chunk_id': metadata.get('chunk_id', ''),
            'chunk_type': metadata.get('chunk_type', ''),
            'chunk_level': metadata.get('chunk_level', 0),
            'source_file': metadata.get('source_file', ''),

            # Operational metadata (with null safety)
            'operational_context': metadata.get('operational_context') or '',
            'criticality': metadata.get('criticality') or 'routine',
            'time_sensitivity': metadata.get('time_sensitivity') or 'none',

            # Content flags
            'has_code': metadata.get('chunk_type') in ['function', 'method', 'class'],
            'has_commands': len(metadata.get('commands_handled', []) or []) > 0,
            'has_hardware': len(metadata.get('hardware_components', []) or []) > 0,
            'has_troubleshooting': metadata.get('chunk_type') == 'troubleshooting',
            'has_procedures': metadata.get('chunk_type') == 'procedure',

            # List fields (converted to strings for easier filtering, with null safety)
            'commands': '|'.join(metadata.get('commands_handled', []) or []),
            'hardware_components': '|'.join(metadata.get('hardware_components', []) or []),
            'key_concepts': '|'.join(metadata.get('key_concepts', []) or []),
            'search_keywords': '|'.join(metadata.get('search_keywords', []) or []),

            # Relationship flags (with null safety)
            'has_related_chunks': len(metadata.get('related_code_chunks', []) or []) > 0,
            'has_prerequisites': len(metadata.get('prerequisite_chunks', []) or []) > 0,
            'has_cross_refs': len(metadata.get('see_also_chunks', []) or []) > 0,
        }

    @staticmethod
    def _create_display_metadata(metadata: Dict) -> Dict:
        """Create metadata for displaying results to users"""

        return {
            'title': MetadataProcessor._generate_display_title(metadata),
            'type': metadata.get('chunk_type', 'unknown').replace('_', ' ').title(),
            'source': Path(metadata.get('source_file', '')).name,
            'summary': metadata.get('ai_summary') or MetadataProcessor._generate_fallback_summary(metadata),
            'commands': (metadata.get('commands_handled', []) or [])[:3],  # Limit for display
            'hardware': (metadata.get('hardware_components', []) or [])[:3],
            'criticality': metadata.get('criticality') or 'routine',
            'context': (metadata.get('operational_context') or '').replace('_', ' ').title(),
        }

    @staticmethod
    def _generate_display_title(metadata: Dict) -> str:
        """Generate a user-friendly title for display"""

        chunk_type = metadata.get('chunk_type', '')
        chunk_id = metadata.get('chunk_id', '')

        if chunk_type == 'function':
            # Extract function name from chunk_id
            parts = chunk_id.split('_')
            if len(parts) >= 2:
                return f"Function: {parts[1]}()"
        elif chunk_type == 'command_handler':
            commands = metadata.get('commands_handled', [])
            if commands:
                return f"Command: {commands[0]}"
        elif chunk_type == 'troubleshooting':
            symptoms = metadata.get('problem_symptoms', []) or []
            if symptoms:
                return f"Fix: {symptoms[0][:50]}..."
        elif chunk_type == 'procedure':
            # Try to extract from chunk_id or use generic title
            return f"Procedure: {chunk_id.replace('_', ' ').title()}"

        # Fallback
        source_name = Path(metadata.get('source_file', '')).stem
        return f"{chunk_type.title()}: {source_name}"

    @staticmethod
    def _generate_fallback_summary(metadata: Dict) -> str:
        """Generate fallback summary when AI summary not available"""

        chunk_type = metadata.get('chunk_type', '')

        if chunk_type == 'function':
            docstring = metadata.get('docstring')
            if docstring:
                return docstring[:100] + "..." if len(docstring) > 100 else docstring
            else:
                return f"Function in {Path(metadata.get('source_file', '')).name}"

        elif chunk_type == 'troubleshooting':
            symptoms = metadata.get('problem_symptoms', []) or []
            if symptoms:
                return f"Troubleshooting: {symptoms[0]}"

        elif chunk_type == 'command_handler':
            commands = metadata.get('commands_handled', []) or []
            if commands:
                return f"Handles {commands[0]} command"

        return f"Radio telescope {chunk_type} documentation"


class ChromaDBManager:
    """Manage ChromaDB vector database"""

    def __init__(self, db_path: str = "data/vector_db/chroma"):
        if not CHROMA_AVAILABLE:
            raise ValueError("ChromaDB not available. Install with: pip install chromadb")

        self.db_path = Path(db_path)
        self.db_path.mkdir(parents=True, exist_ok=True)

        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(path=str(self.db_path))
        self.collection = None

    def create_collection(self, collection_name: str = "telescope_docs"):
        """Create or get collection"""

        # Delete existing collection if it exists (for fresh start)
        try:
            self.client.delete_collection(name=collection_name)
            print(f"🗑️  Deleted existing collection: {collection_name}")
        except:
            pass

        # Create new collection
        self.collection = self.client.create_collection(
            name=collection_name,
            metadata={"description": "EOVSA Radio Telescope Documentation"}
        )

        print(f"✅ Created ChromaDB collection: {collection_name}")
        return self.collection

    def add_chunks(self, processed_chunks: List[Dict], embeddings: List[List[float]]):
        """Add chunks to ChromaDB with deduplication"""

        if not self.collection:
            raise ValueError("Collection not initialized. Call create_collection() first.")

        # Deduplicate chunks (keep first occurrence of each ID)
        seen_ids = set()
        deduplicated_chunks = []
        deduplicated_embeddings = []
        duplicate_count = 0

        for chunk, embedding in zip(processed_chunks, embeddings):
            chunk_id = chunk['id']
            if chunk_id not in seen_ids:
                seen_ids.add(chunk_id)
                deduplicated_chunks.append(chunk)
                deduplicated_embeddings.append(embedding)
            else:
                duplicate_count += 1

        # Store for later use in metadata saving
        self._last_deduplicated_chunks = deduplicated_chunks

        if duplicate_count > 0:
            print(f"⚠️  Removed {duplicate_count} duplicate chunks (kept first occurrence of each)")
            print(f"📊 Processing {len(deduplicated_chunks)} unique chunks")

        # Prepare data for ChromaDB
        ids = []
        documents = []
        metadatas = []
        embeddings_list = []

        for chunk, embedding in zip(deduplicated_chunks, deduplicated_embeddings):
            ids.append(chunk['id'])
            documents.append(chunk['enhanced_text'])
            metadatas.append(chunk['searchable_metadata'])
            embeddings_list.append(embedding)

        # Add to collection in batches
        batch_size = 1000
        for i in range(0, len(ids), batch_size):
            batch_end = min(i + batch_size, len(ids))

            self.collection.add(
                ids=ids[i:batch_end],
                documents=documents[i:batch_end],
                metadatas=metadatas[i:batch_end],
                embeddings=embeddings_list[i:batch_end]
            )

            print(f"📦 Added batch {i // batch_size + 1}: {batch_end - i} chunks")

        print(f"✅ Added {len(ids)} unique chunks to ChromaDB")

    def search(self, query: str, n_results: int = 10,
               filters: Optional[Dict] = None) -> List[Dict]:
        """Search the collection"""

        if not self.collection:
            raise ValueError("Collection not initialized")

        # Build ChromaDB where clause from filters
        where_clause = {}
        if filters:
            for key, value in filters.items():
                if isinstance(value, list):
                    where_clause[key] = {"$in": value}
                else:
                    where_clause[key] = value

        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_clause if where_clause else None
        )

        return results


class VectorDatabaseCreator:
    """Main class for creating the vector database"""

    def __init__(self,
                 embedding_model: str = "sentence-transformers",
                 db_type: str = "chromadb",
                 db_path: str = "data/vector_db"):

        self.embedding_generator = EmbeddingGenerator(embedding_model)
        self.metadata_processor = MetadataProcessor()
        self.db_type = db_type
        self.db_path = Path(db_path)

        # Initialize database manager
        if db_type == "chromadb":
            self.db_manager = ChromaDBManager(str(self.db_path / "chroma"))
        else:
            raise ValueError(f"Database type {db_type} not yet implemented")

    def create_database(self, input_json: str, collection_name: str = "telescope_docs"):
        """Create vector database from processed chunks JSON"""

        print(f"🚀 Creating vector database from {input_json}")

        # Load processed chunks
        with open(input_json, 'r', encoding='utf-8') as f:
            chunks = json.load(f)

        print(f"📊 Loaded {len(chunks)} processed chunks")

        # Process chunks for vector database
        print("🔄 Preparing chunks for vector database...")
        processed_chunks = []
        failed_chunks = 0

        for i, chunk in enumerate(chunks):
            try:
                processed_chunk = self.metadata_processor.prepare_chunk_for_vectordb(chunk)
                processed_chunks.append(processed_chunk)

                if (i + 1) % 100 == 0:
                    print(f"  Processed {i + 1}/{len(chunks)} chunks...")

            except Exception as e:
                print(f"  ⚠️  Failed to process chunk {i + 1}: {e}")
                failed_chunks += 1
                continue

        if failed_chunks > 0:
            print(f"⚠️  {failed_chunks} chunks failed processing, continuing with {len(processed_chunks)} chunks")

        # Generate embeddings
        print("🧠 Generating embeddings (this may take a while)...")
        texts_to_embed = [chunk['enhanced_text'] for chunk in processed_chunks]

        # Show token statistics for debugging
        if hasattr(self.metadata_processor, 'token_manager'):
            token_counts = [self.metadata_processor.token_manager.count_tokens(text) for text in texts_to_embed]
            print(f"📊 Token statistics:")
            print(f"   Average tokens per chunk: {np.mean(token_counts):.1f}")
            print(f"   Max tokens: {np.max(token_counts)}")
            print(f"   Chunks over 7500 tokens: {sum(1 for t in token_counts if t > 7500)}")

        embeddings = self.embedding_generator.generate_batch_embeddings(texts_to_embed)

        print(f"✅ Generated {len(embeddings)} embeddings")

        # Create database collection
        print("📚 Creating database collection...")
        self.db_manager.create_collection(collection_name)

        # Add chunks to database
        print("💾 Adding chunks to database...")
        self.db_manager.add_chunks(processed_chunks, embeddings)

        # Save metadata for retrieval system (use deduplicated chunks)
        metadata_file = self.db_path / "chunk_metadata.json"

        # Get the deduplicated chunks from db_manager (if available)
        final_processed_chunks = processed_chunks
        if hasattr(self.db_manager, '_last_deduplicated_chunks'):
            final_processed_chunks = self.db_manager._last_deduplicated_chunks

        chunk_metadata = {chunk['id']: {
            'display_metadata': chunk['display_metadata'],
            'full_metadata': chunk['full_metadata']
        } for chunk in final_processed_chunks}

        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(chunk_metadata, f, indent=2)

        print(f"💾 Saved chunk metadata to {metadata_file}")

        # Generate statistics (use deduplicated data)
        self._generate_database_stats(final_processed_chunks)

        print(f"\n✅ Vector database created successfully!")
        print(f"📁 Database location: {self.db_path}")
        print(f"🔍 Ready for intelligent telescope documentation retrieval!")

    def _generate_database_stats(self, chunks: List[Dict]):
        """Generate and save database statistics"""

        stats = {
            'total_chunks': len(chunks),
            'creation_date': datetime.now().isoformat(),
            'chunk_types': {},
            'chunk_levels': {},
            'operational_contexts': {},
            'hardware_coverage': {},
            'command_coverage': {},
            'criticality_levels': {}
        }

        # Analyze chunks
        for chunk in chunks:
            metadata = chunk['searchable_metadata']

            # Count chunk types
            chunk_type = metadata.get('chunk_type', 'unknown')
            stats['chunk_types'][chunk_type] = stats['chunk_types'].get(chunk_type, 0) + 1

            # Count chunk levels
            level = metadata.get('chunk_level', 0)
            stats['chunk_levels'][f'level_{level}'] = stats['chunk_levels'].get(f'level_{level}', 0) + 1

            # Count operational contexts
            context = metadata.get('operational_context', 'none')
            if context:
                stats['operational_contexts'][context] = stats['operational_contexts'].get(context, 0) + 1

            # Count hardware components
            hardware_str = metadata.get('hardware_components', '')
            if hardware_str:
                hardware_list = [h.strip() for h in hardware_str.split('|') if h.strip()]
                for hardware in hardware_list:
                    stats['hardware_coverage'][hardware] = stats['hardware_coverage'].get(hardware, 0) + 1

            # Count commands
            commands_str = metadata.get('commands', '')
            if commands_str:
                command_list = [c.strip() for c in commands_str.split('|') if c.strip()]
                for command in command_list:
                    stats['command_coverage'][command] = stats['command_coverage'].get(command, 0) + 1

            # Count criticality
            criticality = metadata.get('criticality', 'routine')
            stats['criticality_levels'][criticality] = stats['criticality_levels'].get(criticality, 0) + 1

        # Save stats
        stats_file = self.db_path / "database_stats.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)

        # Print key statistics
        print(f"\n📊 DATABASE STATISTICS")
        print(f"Total chunks: {stats['total_chunks']}")
        print(f"Chunk types: {len(stats['chunk_types'])}")
        print(f"Hardware components: {len(stats['hardware_coverage'])}")
        print(f"Commands covered: {len(stats['command_coverage'])}")
        print(f"Operational contexts: {len(stats['operational_contexts'])}")


def main():
    """Main execution function"""

    import argparse

    parser = argparse.ArgumentParser(description='Create Vector Database for Radio Telescope RAG')
    parser.add_argument('--input', required=True, help='Input JSON file with processed chunks')
    parser.add_argument('--output-dir', default='data/vector_db', help='Output directory for vector database')
    parser.add_argument('--collection', default='telescope_docs', help='Collection name')
    parser.add_argument('--embedding-model', choices=['sentence-transformers', 'openai'],
                        default='openai', help='Embedding model to use')
    parser.add_argument('--db-type', choices=['chromadb'], default='chromadb',
                        help='Vector database type')

    args = parser.parse_args()

    # Validate input file
    if not Path(args.input).exists():
        print(f"❌ Input file not found: {args.input}")
        return

    # Check dependencies
    if args.embedding_model == "sentence-transformers" and not SENTENCE_TRANSFORMERS_AVAILABLE:
        print("❌ SentenceTransformers not available. Install with: pip install sentence-transformers")
        return

    if args.embedding_model == "openai" and not OPENAI_AVAILABLE:
        print("❌ OpenAI not available. Install with: pip install openai tiktoken")
        return

    if args.db_type == "chromadb" and not CHROMA_AVAILABLE:
        print("❌ ChromaDB not available. Install with: pip install chromadb")
        return

    # Create vector database
    creator = VectorDatabaseCreator(
        embedding_model=args.embedding_model,
        db_type=args.db_type,
        db_path=args.output_dir
    )

    creator.create_database(args.input, args.collection)

    print(f"\n🎉 Vector database creation complete!")
    print(f"📁 Database saved to: {args.output_dir}")
    print(f"🔍 Use the retrieval system to query your telescope documentation!")


if __name__ == "__main__":
    main()