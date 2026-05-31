#!/usr/bin/env python3
"""
Enhanced Radio Telescope LLM Agent
Works with ChromaDB vector database and enhanced metadata structure
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv
import logging

# ChromaDB for vector retrieval
try:
    import chromadb

    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    print("❌ ChromaDB not available. Install with: pip install chromadb")

# OpenAI for LLM
try:
    from openai import OpenAI

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("❌ OpenAI not available. Install with: pip install openai")

load_dotenv()


class EnhancedTelescopeRetriever:
    """Enhanced retriever that uses ChromaDB with intelligent filtering"""

    def __init__(self, db_path: str = "data/vector_db", collection_name: str = "telescope_docs"):
        if not CHROMADB_AVAILABLE:
            raise ValueError("ChromaDB not available")
        if not OPENAI_AVAILABLE:
            raise ValueError("OpenAI not available for embeddings")

        self.db_path = Path(db_path)
        self.collection_name = collection_name

        # Initialize OpenAI client for embeddings
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=str(self.db_path / "chroma"))

        # Try requested collection, fall back to any available if missing
        try:
            self.collection = self.client.get_collection(name=collection_name)
        except Exception as exc:
            fallback_collection = None
            try:
                existing = self.client.list_collections()
                if existing:
                    # Prefer telescope_docs if present
                    names = {c.name for c in existing}
                    preferred = "telescope_docs" if "telescope_docs" in names else None
                    fallback_collection = next((c for c in existing if c.name == preferred), existing[0])
            except Exception:
                existing = []

            if fallback_collection:
                print(f"⚠️  Collection '{collection_name}' not found; using '{fallback_collection.name}' instead.")
                self.collection = self.client.get_collection(name=fallback_collection.name)
            else:
                raise exc

        # Load chunk metadata
        metadata_file = self.db_path / "chunk_metadata.json"
        with open(metadata_file, 'r', encoding='utf-8') as f:
            self.chunk_metadata = json.load(f)

        print(f"✅ Connected to ChromaDB collection: {collection_name}")
        print(f"📊 Loaded metadata for {len(self.chunk_metadata)} chunks")

    def _get_query_embedding(self, query: str) -> List[float]:
        """Generate OpenAI embedding for query (matching the database embeddings)"""
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=query
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"❌ Failed to generate query embedding: {e}")
            raise

    def retrieve(self, query: str, top_k: int = 15, filters: Optional[Dict] = None,
                 include_cross_refs: bool = True) -> List[Dict]:
        """Retrieve relevant chunks with enhanced metadata"""

        # Generate query embedding using OpenAI (same as database)
        query_embedding = self._get_query_embedding(query)

        # Build ChromaDB where clause
        where_clause = {}
        if filters:
            for key, value in filters.items():
                if isinstance(value, list):
                    where_clause[key] = {"$in": value}
                else:
                    where_clause[key] = value

        # Perform vector search with our embedding
        results = self.collection.query(
            query_embeddings=[query_embedding],  # Use query_embeddings instead of query_texts
            n_results=top_k,
            where=where_clause if where_clause else None
        )

        # Process results with enhanced metadata
        processed_results = []

        for i, chunk_id in enumerate(results['ids'][0]):
            # Get chunk metadata
            chunk_meta = self.chunk_metadata.get(chunk_id, {})
            display_meta = chunk_meta.get('display_metadata', {})
            full_meta = chunk_meta.get('full_metadata', {})

            # Create enhanced result with safe defaults
            result = {
                'chunk_id': chunk_id,
                'content': results['documents'][0][i],
                'distance': results['distances'][0][i] if results['distances'] else 0.0,
                'score': 1.0 - (results['distances'][0][i] if results['distances'] else 0.0),
                'metadata': results['metadatas'][0][i],

                # Enhanced display information with safe defaults
                'title': display_meta.get('title', 'Unknown'),
                'type': display_meta.get('type', 'Unknown'),
                'source': display_meta.get('source', 'Unknown'),
                'summary': display_meta.get('summary', ''),
                'commands': display_meta.get('commands', []) or [],
                'hardware': display_meta.get('hardware', []) or [],
                'criticality': display_meta.get('criticality', 'routine'),
                'context': display_meta.get('context', ''),

                # Full metadata for advanced processing
                'full_metadata': full_meta,

                # Content flags with safe checks
                'has_code': self._safe_check_has_code(full_meta),
                'has_troubleshooting': full_meta.get('chunk_type') == 'troubleshooting',
                'has_commands': self._safe_check_has_commands(full_meta),
                'has_hardware': self._safe_check_has_hardware(full_meta),
            }

            processed_results.append(result)

        # Optionally include cross-references
        if include_cross_refs:
            processed_results = self._expand_with_cross_references(processed_results, max_additional=5)

        return processed_results

    def _safe_check_has_code(self, metadata: Dict) -> bool:
        """Safely check if chunk has code"""
        chunk_type = metadata.get('chunk_type', '')
        return chunk_type in ['function', 'method', 'class', 'code_function', 'code_module', 'source_code']

    def _safe_check_has_commands(self, metadata: Dict) -> bool:
        """Safely check if chunk has commands"""
        commands = metadata.get('commands_handled', []) or []
        return len(commands) > 0

    def _safe_check_has_hardware(self, metadata: Dict) -> bool:
        """Safely check if chunk has hardware"""
        hardware = metadata.get('hardware_components', []) or []
        return len(hardware) > 0

    def _expand_with_cross_references(self, results: List[Dict], max_additional: int = 5) -> List[Dict]:
        """Expand results with cross-referenced chunks"""

        expanded_results = results.copy()
        added_ids = {r['chunk_id'] for r in results}
        additional_count = 0

        for result in results:
            if additional_count >= max_additional:
                break

            full_meta = result['full_metadata']

            # Get related chunk IDs
            related_ids = []
            related_ids.extend(full_meta.get('related_code_chunks', []) or [])
            related_ids.extend(full_meta.get('see_also_chunks', []) or [])
            related_ids.extend(full_meta.get('prerequisite_chunks', []) or [])

            # Add related chunks
            for related_id in related_ids:
                if related_id not in added_ids and additional_count < max_additional:
                    try:
                        # Get the related chunk
                        related_results = self.collection.get(ids=[related_id])
                        if related_results['ids']:
                            related_meta = self.chunk_metadata.get(related_id, {})

                            related_result = {
                                'chunk_id': related_id,
                                'content': related_results['documents'][0],
                                'distance': 0.8,  # Assign moderate distance for cross-refs
                                'score': 0.2,  # Lower score than direct matches
                                'metadata': related_results['metadatas'][0],
                                'title': related_meta.get('display_metadata', {}).get('title', 'Cross-reference'),
                                'type': 'Cross-reference',
                                'source': related_meta.get('display_metadata', {}).get('source', 'Unknown'),
                                'full_metadata': related_meta.get('full_metadata', {}),
                                'is_cross_reference': True,
                                'referenced_from': result['chunk_id'],
                                # Safe defaults for required fields
                                'summary': '',
                                'commands': [],
                                'hardware': [],
                                'criticality': 'routine',
                                'context': '',
                                'has_code': False,
                                'has_troubleshooting': False,
                                'has_commands': False,
                                'has_hardware': False
                            }

                            expanded_results.append(related_result)
                            added_ids.add(related_id)
                            additional_count += 1

                    except Exception as e:
                        print(f"⚠️  Failed to get cross-reference {related_id}: {e}")
                        continue

        return expanded_results

    def retrieve_by_filters(self, filters: Dict, top_k: int = 10) -> List[Dict]:
        """Retrieve chunks purely by metadata filters (no vector search)"""

        # Build where clause
        where_clause = {}
        for key, value in filters.items():
            if isinstance(value, list):
                where_clause[key] = {"$in": value}
            else:
                where_clause[key] = value

        # Get filtered results
        results = self.collection.get(
            where=where_clause,
            limit=top_k
        )

        # Process results
        processed_results = []
        for i, chunk_id in enumerate(results['ids']):
            chunk_meta = self.chunk_metadata.get(chunk_id, {})

            result = {
                'chunk_id': chunk_id,
                'content': results['documents'][i],
                'metadata': results['metadatas'][i],
                'title': chunk_meta.get('display_metadata', {}).get('title', 'Unknown'),
                'type': chunk_meta.get('display_metadata', {}).get('type', 'Unknown'),
                'full_metadata': chunk_meta.get('full_metadata', {}),
                'score': 1.0,  # Max score for exact filter matches
                # Safe defaults for required fields
                'summary': chunk_meta.get('display_metadata', {}).get('summary', ''),
                'commands': chunk_meta.get('display_metadata', {}).get('commands', []) or [],
                'hardware': chunk_meta.get('display_metadata', {}).get('hardware', []) or [],
                'criticality': chunk_meta.get('display_metadata', {}).get('criticality', 'routine'),
                'context': chunk_meta.get('display_metadata', {}).get('context', ''),
                'source': chunk_meta.get('display_metadata', {}).get('source', 'Unknown'),
                'has_code': self._safe_check_has_code(chunk_meta.get('full_metadata', {})),
                'has_troubleshooting': chunk_meta.get('full_metadata', {}).get('chunk_type') == 'troubleshooting',
                'has_commands': self._safe_check_has_commands(chunk_meta.get('full_metadata', {})),
                'has_hardware': self._safe_check_has_hardware(chunk_meta.get('full_metadata', {}))
            }
            processed_results.append(result)

        return processed_results


class EnhancedTelescopeLLMAgent:
    """Enhanced LLM Agent using ChromaDB and rich metadata"""

    def __init__(self, db_path: str = "data/vector_db", collection_name: str = "telescope_docs",
                 top_k: Optional[int] = None, chroma_path: Optional[str] = None,
                 model: Optional[str] = None):
        if not OPENAI_AVAILABLE:
            raise ValueError("OpenAI not available")

        # Support legacy chroma_path argument while keeping db_path as the base directory
        if chroma_path:
            db_path = chroma_path

        resolved_db = Path(db_path)
        if resolved_db.name == "chroma":
            candidate_base = resolved_db.parent
            if (candidate_base / "chunk_metadata.json").exists():
                resolved_db = candidate_base

        # Initialize retriever
        self.retriever = EnhancedTelescopeRetriever(str(resolved_db), collection_name)

        # Initialize OpenAI client
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Configuration
        max_docs_env = os.getenv("MAX_RETRIEVED_DOCS", 15)
        self.max_retrieved_docs = int(top_k if top_k is not None else max_docs_env)
        default_model = os.getenv("OPENAI_MODEL", "gpt-5")
        self.model = model or default_model

        # Conversation history
        self.conversation_history = []

        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        print(f"✅ Enhanced Telescope LLM Agent initialized")
        print(f"   Model: {self.model}")
        print(f"   Max retrieved docs: {self.max_retrieved_docs}")

    def ask(self, question: str, context: Optional[str] = None,
            filters: Optional[Dict] = None, include_cross_refs: bool = True,
            use_history: bool = True, history_turns: int = 5) -> Dict:
        """Ask a question with enhanced context, optional filters, and chat history"""

        self.logger.info(f"Question: {question}")

        # Add context to question if provided
        if context:
            enhanced_question = f"Context: {context}\n\nQuestion: {question}"
        else:
            enhanced_question = question

        history_tail = []
        history_context = ""
        if use_history and self.conversation_history:
            history_tail = self.conversation_history[-max(history_turns, 1):]
            history_context = "\n\n".join(
                f"Q: {turn.get('question', '')}\nA: {turn.get('answer', '')}"
                for turn in history_tail
                if turn.get('question') and turn.get('answer')
            )

        retrieval_query = enhanced_question
        if history_context:
            retrieval_query = f"Previous conversation:\n{history_context}\n\nCurrent question: {enhanced_question}"

        try:
            # Retrieve relevant chunks
            results = self.retriever.retrieve(
                query=retrieval_query,
                top_k=self.max_retrieved_docs,
                filters=filters,
                include_cross_refs=include_cross_refs
            )

            if not results:
                return {
                    'answer': "I couldn't find any relevant information for your question.",
                    'sources': [],
                    'confidence': 0.0,
                    'question': question,
                    'total_sources': 0,
                    'cross_references': 0,
                    'has_code': False,
                    'has_troubleshooting': False,
                    'has_commands': False,
                    'criticality_levels': [],
                    'hardware_involved': [],
                    'commands_involved': []
                }

            # Build context from results
            context_parts = []
            for i, result in enumerate(results):
                context_part = f"Source {i + 1} [{result['type']}]: {result['title']}\n{result['content']}"

                # Add metadata context for functions
                if result['has_code']:
                    full_meta = result['full_metadata']
                    if full_meta.get('function_signature'):
                        context_part += f"\nFunction: {full_meta['function_signature']}"
                    if full_meta.get('docstring'):
                        context_part += f"\nDocstring: {full_meta['docstring']}"

                # Add command information
                if result['commands']:
                    context_part += f"\nCommands: {', '.join(result['commands'])}"

                # Add hardware information
                if result['hardware']:
                    context_part += f"\nHardware: {', '.join(result['hardware'])}"

                context_parts.append(context_part)

            # Create system prompt with enhanced context
            system_prompt = self._create_system_prompt(results)

            # Generate response (handle model-specific token parameter)
            messages = [{"role": "system", "content": system_prompt}]

            if use_history and history_tail:
                for turn in history_tail:
                    if turn.get('question'):
                        messages.append({"role": "user", "content": turn['question']})
                    if turn.get('answer'):
                        messages.append({"role": "assistant", "content": turn['answer']})

            messages.append({
                "role": "user",
                "content": f"Context:\n\n{chr(10).join(context_parts)}\n\nQuestion: {question}"
            })

            completion_args = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.3,
            }

            response = None
            try:
                response = self.client.chat.completions.create(
                    **completion_args,
                    max_completion_tokens=2000
                )
            except Exception as inner_exc:
                # Fallback for older models that still expect max_tokens
                if "max_completion_tokens" in str(inner_exc):
                    response = self.client.chat.completions.create(
                        **completion_args,
                        max_tokens=2000
                    )
                else:
                    raise

            answer = response.choices[0].message.content

            # Calculate confidence and create response
            confidence = self._calculate_confidence(results, question)

            # Prepare response with enhanced metadata
            response_data = {
                'answer': answer,
                'sources': self._format_sources(results),
                'confidence': confidence,
                'question': question,
                'total_sources': len(results),
                'cross_references': sum(1 for r in results if r.get('is_cross_reference', False)),
                'has_code': any(r.get('has_code', False) for r in results),
                'has_troubleshooting': any(r.get('has_troubleshooting', False) for r in results),
                'has_commands': any(r.get('has_commands', False) for r in results),
                'criticality_levels': list(set(r.get('criticality', 'routine') for r in results)),
                'hardware_involved': list(set([hw for r in results for hw in r.get('hardware', [])])),
                'commands_involved': list(set([cmd for r in results for cmd in r.get('commands', [])]))
            }

            # Add safety warning if critical
            if any(r.get('criticality', 'routine') in ['critical', 'emergency'] for r in results):
                response_data[
                    'answer'] += "\n\n⚠️ **SAFETY CRITICAL**: This response contains safety-critical information. Please follow all safety procedures and protocols."
                response_data['safety_critical'] = True
            else:
                response_data['safety_critical'] = False

            # Add to conversation history
            self.conversation_history.append({
                'question': question,
                'answer': answer,
                'sources_count': len(results),
                'confidence': confidence,
                'safety_critical': response_data.get('safety_critical', False)
            })

            self.logger.info(f"Response generated with {len(results)} sources, confidence: {confidence:.2f}")

            return response_data

        except Exception as e:
            self.logger.error(f"Error generating response: {e}")

            # Fallback response with safe defaults to keep callers running
            return {
                'answer': f"I apologize, but I encountered an error while processing your question: {str(e)}",
                'sources': [],
                'confidence': 0.0,
                'question': question,
                'error': str(e),
                'total_sources': 0,
                'cross_references': 0,
                'has_code': False,
                'has_troubleshooting': False,
                'has_commands': False,
                'criticality_levels': [],
                'hardware_involved': [],
                'commands_involved': [],
                'safety_critical': False
            }

    def _create_system_prompt(self, results: List[Dict]) -> str:
        """Create system prompt based on retrieved results"""

        # Analyze what types of content we have
        has_code = any(r.get('has_code', False) for r in results)
        has_troubleshooting = any(r.get('has_troubleshooting', False) for r in results)
        has_commands = any(r.get('has_commands', False) for r in results)

        base_prompt = """You are an expert EOVSA radio telescope operations and maintenance assistant. 
You have access to detailed documentation about telescope systems, hardware, software, and procedures.

Your expertise includes:
- Hardware troubleshooting and diagnostics
- Telescope control software and scripts
- Maintenance procedures and schedules
- Safety protocols and best practices
- EOVSA-specific operations and components

Guidelines:
1. Provide specific, actionable advice based on the provided documentation
2. Use information from ALL relevant sources in your response
3. When multiple sources provide related information, synthesize them into a comprehensive answer
4. Reference specific sources when mentioning details
5. If generating code, include comments and error handling"""

        # Add specialized instructions based on content type
        if has_code:
            base_prompt += """
6. CODE GENERATION: When working with code, ensure it follows EOVSA conventions and includes proper error handling"""

        if has_troubleshooting:
            base_prompt += """
7. TROUBLESHOOTING: Provide step-by-step procedures and include safety considerations"""

        if has_commands:
            base_prompt += """
8. COMMANDS: Explain command syntax, parameters, and provide usage examples when relevant"""

        # Add criticality warning if needed
        critical_sources = [r for r in results if r.get('criticality', 'routine') in ['critical', 'emergency']]
        if critical_sources:
            base_prompt += """

⚠️ IMPORTANT: Some sources contain safety-critical information. Always prioritize safety procedures and protocols."""

        return base_prompt

    def _format_sources(self, results: List[Dict]) -> List[Dict]:
        """Format sources for response"""

        formatted_sources = []

        for result in results:
            source_info = {
                'title': result.get('title', 'Unknown'),
                'type': result.get('type', 'Unknown'),
                'source': result.get('source', 'Unknown'),
                'score': result.get('score', 0.0),
                'summary': result.get('summary', ''),
                'criticality': result.get('criticality', 'routine'),
                'context': result.get('context', ''),
                'has_code': result.get('has_code', False),
                'has_commands': result.get('has_commands', False),
                'commands': result.get('commands', []),
                'hardware': result.get('hardware', []),
                'excerpt': result['content'][:200] + "..." if len(result['content']) > 200 else result['content']
            }

            # Add cross-reference info
            if result.get('is_cross_reference'):
                source_info['is_cross_reference'] = True
                source_info['referenced_from'] = result.get('referenced_from')

            formatted_sources.append(source_info)

        return formatted_sources

    def _calculate_confidence(self, results: List[Dict], question: str) -> float:
        """Calculate confidence score"""

        if not results:
            return 0.0

        # Base confidence from retrieval scores
        avg_score = sum(r['score'] for r in results) / len(results)

        # Boost for number of sources
        source_count_factor = min(len(results) / 10.0, 1.0)

        # Boost for exact metadata matches
        exact_match_boost = 0.0
        question_lower = question.lower()

        # Check for command mentions
        all_commands = [cmd for r in results for cmd in r['commands']]
        command_mentions = sum(1 for cmd in all_commands if cmd.lower() in question_lower)
        if command_mentions > 0:
            exact_match_boost += 0.1

        # Check for hardware mentions
        all_hardware = [hw for r in results for hw in r.get('hardware', [])]
        hardware_mentions = sum(1 for hw in all_hardware if hw.lower() in question_lower)
        if hardware_mentions > 0:
            exact_match_boost += 0.1

        # Boost for high-quality content types
        quality_boost = 0.0
        if any(r.get('has_code', False) for r in results):
            quality_boost += 0.05
        if any(r.get('has_troubleshooting', False) for r in results):
            quality_boost += 0.05

        # Calculate final confidence
        confidence = (avg_score * 0.5) + (source_count_factor * 0.3) + exact_match_boost + quality_boost

        return min(confidence, 1.0)

    def ask_with_filters(self, question: str, chunk_type: str = None,
                         criticality: str = None, has_code: bool = None,
                         has_commands: bool = None, operational_context: str = None) -> Dict:
        """Ask with specific filters"""

        filters = {}

        if chunk_type:
            filters['chunk_type'] = chunk_type
        if criticality:
            filters['criticality'] = criticality
        if has_code is not None:
            filters['has_code'] = has_code
        if has_commands is not None:
            filters['has_commands'] = has_commands
        if operational_context:
            filters['operational_context'] = operational_context

        return self.ask(question, filters=filters)

    def troubleshoot(self, problem_description: str) -> Dict:
        """Specialized troubleshooting with targeted retrieval"""

        # Use filters to get troubleshooting content
        filters = {
            'chunk_type': 'troubleshooting'
        }

        enhanced_question = f"""I'm experiencing the following problem with the EOVSA telescope system:
        {problem_description}

        Please provide:
        1. Likely causes of this problem
        2. Step-by-step troubleshooting procedure
        3. Safety considerations
        4. When to escalate to senior staff
        """

        result = self.ask(enhanced_question, filters=filters)
        result['request_type'] = 'troubleshooting'

        return result

    def get_code(self, function_or_command: str) -> Dict:
        """Get code implementation for functions or commands"""

        filters = {
            'has_code': True
        }

        question = f"Show me the source code and implementation details for: {function_or_command}"

        result = self.ask(question, filters=filters)
        result['request_type'] = 'code_retrieval'

        return result

    def get_commands(self, operation_type: str = None) -> Dict:
        """Get available commands, optionally filtered by operation type"""

        filters = {
            'has_commands': True
        }

        if operation_type:
            filters['operational_context'] = operation_type

        question = f"What commands are available for {operation_type or 'telescope operations'}? Please include syntax and examples."

        result = self.ask(question, filters=filters)
        result['request_type'] = 'command_reference'

        return result

    def get_maintenance_procedure(self, component: str) -> Dict:
        """Get maintenance procedures for specific components"""

        question = f"""Please provide the maintenance procedure for: {component}

        Include:
        1. Required tools and materials
        2. Safety precautions
        3. Step-by-step procedure
        4. Testing and verification steps
        5. Documentation requirements
        """

        result = self.ask(question)
        result['request_type'] = 'maintenance'

        return result

    def get_conversation_summary(self) -> Dict:
        """Get summary of conversation history"""

        if not self.conversation_history:
            return {'total_questions': 0, 'summary': 'No conversation history'}

        total_questions = len(self.conversation_history)
        avg_confidence = sum(conv['confidence'] for conv in self.conversation_history) / total_questions
        safety_critical_count = sum(1 for conv in self.conversation_history if conv.get('safety_critical', False))

        return {
            'total_questions': total_questions,
            'average_confidence': avg_confidence,
            'safety_critical_responses': safety_critical_count,
            'recent_questions': [conv['question'] for conv in self.conversation_history[-5:]],
            'recent_confidence_scores': [conv['confidence'] for conv in self.conversation_history[-5:]]
        }


def main():
    """Test the enhanced agent"""

    # Initialize agent
    try:
        agent = EnhancedTelescopeLLMAgent()

        # Test questions
        test_questions = [
            #"how to apply a customized calibration table to eovsa data?",
            #"What steps are needed to add a monitor point to the stateframe? Check carefully the function I/O make the code executable",
            #"how to stow all the antennas?",
            #"if the 6-hour GOES light curves on the https://ovsa.njit.edu/status.php# stopped updating, what could be the reason? mean while the eovsa data is still recording, flare monitor still working, but the OVRO-LWA stucked, which machine could be problematic?",
            #"where is https://ovsa.njit.edu/status.php# reading data from? how to add an plot to this website?"
            #"what is the freq of spw7? what is the frequency? what is the spatial resolution? what is the dimension of the resotring beam at that spw?"
            #'how does DCMauto work? how often it updates the attn? I found some vertical strip across all the band, is that possibly related to the DCM-AUTO? how to diagnose?'
            #"give me a function that read out the msfile like /data1/eovsa/fits/UDBms/202206/UDB20220614.ms in python"
            #'where is the plot that show the required and the actual coordinates of each antenna? or the code that draw it? and what is get_sql_info?'
            #'how to get 27m feed angle?'
            #'can you explain what is the ctl file?'
            #"if in the PHASECAL.ctl file I set $PA-TRACK ANT4. is that true that during the calibraion, the feed was rotate with x degree, where x is the paralatic angle of ant4?"
            #'give me a step by step instrucntion on how to convert the voltage read from the attenuator in teh FEM to the power which is displayed on the stateframe (which code and functions are used)?'
            #'which codes are involved in how to convert the voltage read from the attenuator in teh FEM to the power which is displayed on the stateframe?'
            #"where and the name of the code is that  **Configuration used by conversion:** antenna `/ni-rt/startup/crio.ini`, section **`[FEM Power Scale]`** (coefficients `c0..c4`)"
            #'in the stateframe, all the dcm read including the voltage and attns are 0, the other part of sf_display works fine'
            #'explain what does the adc_plot do, what is the purposse and how it is done and how it is related to attenuation  setting of fem and dcm'
            #'phase tracking in stateframe display show a date at 1904 and tracking is false '
            #'In [315]: files = fs.calIDB(Time([\'2026-01-08 19:45\',\'2026-01-08 20:00\']))Processing: /data1/eovsa/fits/IDB/20260108/IDB20260108194748 Reading file took 88.65385818481445 s Reading SQL info took 1.1604118347167969 s WARNING: TimeDeltaMissingUnitWarning: Numerical value without unit or explicit format passed to TimeDelta, assuming days [astropy.time.core] Note, SKYCAL is being read from 2026-01-04 to match TP calibration date. Error processing /data1/eovsa/fits/IDB/20260108/IDB20260108194748: \'Timestamp\''
            #'the dppxmp\'s TIME+ get refreshed every a few seconds and the File is not being recorded'
            #'the power and attenuation rows show yellow and the attenuation can not be modified'
            #'in sf_display, what is alarm 10 (temperature) related'
            #"where is gen_fem_sf function? if I want to do something to modify the shown dbm, where should I modified the code?"
            #'ant14 (27m) shows inactive, axis locked, tripped in second column, how to bring it back?'
            #'27m power is off'
            #'ant3 got tripped, brake, inactive in both first 2 columns, loading track table then track it only solved the problem on the first column, the second column still got inactive, brake, axis lock, communication is still on'
            #'how to check if interface board (PCB board) is working or not'
            #'how to start crio for fem, is there a crio along for the fem of an antenna, or there is only one crio for each anteena? hwo to start it if it is shut down'
            #'sync or $pcycle crio ant* keep get error 314100'
            #'does the crio need to be powered up so stateframe can recieve the signal from interface board of the FEM?'
            #'how to manually move the antenna?'
            'Ant 15 Viking unit isnt accepting the command $pcycle fem ant15, what could be the possible issue? is the signal control and execution inside the FEM? or outside the FEM?'
            #"How to create a special schedule to observed a selected source? Check carefully the function I/O make the code executable",
            #"can you draw me a plot show what happened when I send out a command start with $ in the schedule?"

            #"What commands are available for antenna tracking?",
            #"Show me troubleshooting procedures for correlator issues",
            #"What are the safety procedures for maintenance?",
            #"How do I calibrate the receivers?"
        ]

        for question in test_questions:
            print(f"\n{'=' * 60}")
            print(f"Q: {question}")

            response = agent.ask(question)

            print(f"\nA: {response['answer']}...")
            print(f"Confidence: {response['confidence']:.2f}")
            print(f"Sources: {response['total_sources']}")
            print(f"Has code: {response['has_code']}")
            print(f"Safety critical: {response.get('safety_critical', False)}")

            if response['hardware_involved']:
                print(f"Hardware: {', '.join(response['hardware_involved'][:3])}")

            if response['commands_involved']:
                print(f"Commands: {', '.join(response['commands_involved'][:3])}")

        # Show conversation summary
        print(f"\n{'=' * 60}")
        print("CONVERSATION SUMMARY")
        summary = agent.get_conversation_summary()
        print(f"Total questions: {summary['total_questions']}")
        print(f"Average confidence: {summary['average_confidence']:.2f}")
        print(f"Safety critical responses: {summary['safety_critical_responses']}")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure you have:")
        print("1. Created the vector database with vector_database_creator.py")
        print("2. Set your OPENAI_API_KEY environment variable")
        print("3. Installed required packages: chromadb openai")


if __name__ == "__main__":
    main()
