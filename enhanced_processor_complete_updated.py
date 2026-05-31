
#!/usr/bin/env python3
"""
Enhanced Radio Telescope Documentation Processor
Comprehensive processing for EOVSA telescope system documentation and code
"""
#python enhanced_processor_complete.py --input-dir data/raw/ --cost-limit 2500
import os
import re
import ast
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple
from datetime import datetime
from collections import defaultdict
import numpy as np

# For code analysis
import inspect
import textwrap
from dataclasses import dataclass, field, asdict

# OpenAI for enhanced metadata
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

@dataclass
class ChunkMetadata:
    """Enhanced metadata structure for chunks"""
    # Core identification
    chunk_id: str
    source_file: str
    chunk_type: str  # function|class|procedure|troubleshooting|command|module
    chunk_level: int  # 1=atomic, 2=contextual, 3=system
    parent_chunk_id: Optional[str] = None
    child_chunk_ids: List[str] = field(default_factory=list)
    
    # Code-specific metadata
    function_signature: Optional[str] = None
    docstring: Optional[str] = None
    inline_comments: List[str] = field(default_factory=list)
    imports_used: List[str] = field(default_factory=list)
    functions_called: List[str] = field(default_factory=list)
    functions_that_call_this: List[str] = field(default_factory=list)
    global_vars_accessed: List[str] = field(default_factory=list)
    exception_types: List[str] = field(default_factory=list)
    
    # Operational metadata
    commands_handled: List[str] = field(default_factory=list)
    hardware_components: List[str] = field(default_factory=list)
    operational_context: Optional[str] = None
    criticality: str = "routine"  # routine|important|critical|emergency
    time_sensitivity: str = "none"  # immediate|minutes|hours|none
    
    # Cross-references
    related_wiki_sections: List[str] = field(default_factory=list)
    related_code_chunks: List[str] = field(default_factory=list)
    prerequisite_chunks: List[str] = field(default_factory=list)
    see_also_chunks: List[str] = field(default_factory=list)
    
    # Semantic metadata
    problem_symptoms: List[str] = field(default_factory=list)
    solutions_provided: List[str] = field(default_factory=list)
    key_concepts: List[str] = field(default_factory=list)
    search_keywords: List[str] = field(default_factory=list)
    
    # AI-enhanced metadata
    ai_summary: Optional[str] = None
    ai_purpose: Optional[str] = None
    ai_dependencies: Optional[str] = None
    ai_error_scenarios: List[str] = field(default_factory=list)
    ai_usage_examples: List[str] = field(default_factory=list)


class CodeAnalyzer:
    """Advanced code analysis for telescope control software"""
    
    def __init__(self):
        self.function_graph = defaultdict(set)  # func -> functions it calls
        self.reverse_graph = defaultdict(set)  # func -> functions that call it
        self.import_graph = defaultdict(set)   # module -> imported modules
        self.global_usage = defaultdict(set)  # func -> globals used
        self.command_handlers = {}  # command -> handler function
        
    def analyze_file(self, filepath: str) -> List[Dict]:
        """Comprehensive analysis of a Python file"""
        chunks = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        try:
            tree = ast.parse(content)
        except SyntaxError:
            print(f"Syntax error in {filepath}, falling back to text analysis")
            return self._fallback_text_analysis(filepath, content)
        
        # Extract module-level information
        module_chunk = self._create_module_chunk(filepath, tree, content)
        chunks.append(module_chunk)
        
        # Analyze imports
        imports = self._extract_imports(tree)
        
        # Analyze functions and classes
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_chunk = self._analyze_function(node, filepath, content, imports)
                chunks.append(func_chunk)
            elif isinstance(node, ast.ClassDef):
                class_chunks = self._analyze_class(node, filepath, content, imports)
                chunks.extend(class_chunks)
        
        # Extract command handlers (special case for schedule.py pattern)
        command_chunks = self._extract_command_handlers(content, filepath)
        chunks.extend(command_chunks)
        
        # Build relationships
        self._build_relationships(chunks)
        
        return chunks
    
    def _analyze_function(self, node: ast.FunctionDef, filepath: str, 
                         full_content: str, imports: Dict) -> Dict:
        """Detailed function analysis"""
        
        # Generate unique ID
        chunk_id = f"{Path(filepath).stem}_{node.name}_{node.lineno}"
        
        # Extract docstring
        docstring = ast.get_docstring(node)
        
        # Extract function signature
        signature = self._get_function_signature(node, full_content)
        
        # Extract inline comments
        comments = self._extract_function_comments(node, full_content)
        
        # Extract function calls
        calls = self._extract_function_calls(node)
        
        # Extract exception handling
        exceptions = self._extract_exceptions(node)
        
        # Extract global variable usage
        globals_used = self._extract_global_usage(node)
        
        # Extract command handling (if any)
        commands = self._extract_handled_commands(node, full_content)
        
        # Extract hardware components mentioned
        hardware = self._extract_hardware_components(node, full_content)
        
        # Get function body
        func_lines = full_content.split('\n')[node.lineno-1:node.end_lineno]
        func_content = '\n'.join(func_lines)
        
        metadata = ChunkMetadata(
            chunk_id=chunk_id,
            source_file=filepath,
            chunk_type="function",
            chunk_level=1,
            function_signature=signature,
            docstring=docstring,
            inline_comments=comments,
            functions_called=list(calls),
            global_vars_accessed=list(globals_used),
            exception_types=exceptions,
            commands_handled=commands,
            hardware_components=hardware,
            operational_context=self._determine_operational_context(func_content, node.name),
            key_concepts=self._extract_key_concepts(func_content, node.name)
        )
        
        return {
            'content': func_content,
            'metadata': asdict(metadata),
            'ast_node': node  # Keep for relationship building
        }
    
    def _analyze_class(self, node: ast.ClassDef, filepath: str, 
                      full_content: str, imports: Dict) -> List[Dict]:
        """Analyze a class and its methods"""
        chunks = []
        
        # Create class-level chunk
        class_id = f"{Path(filepath).stem}_{node.name}_class"
        class_docstring = ast.get_docstring(node)
        
        # Get class definition lines
        class_start = node.lineno - 1
        # Find first method or end of class
        first_method_line = min([m.lineno for m in node.body 
                                if isinstance(m, ast.FunctionDef)], 
                               default=node.end_lineno)
        class_def_lines = full_content.split('\n')[class_start:first_method_line-1]
        class_def = '\n'.join(class_def_lines)
        
        class_metadata = ChunkMetadata(
            chunk_id=class_id,
            source_file=filepath,
            chunk_type="class",
            chunk_level=2,
            docstring=class_docstring,
            key_concepts=self._extract_key_concepts(class_def, node.name)
        )
        
        chunks.append({
            'content': class_def,
            'metadata': asdict(class_metadata)
        })
        
        # Analyze each method
        method_ids = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_chunk = self._analyze_function(item, filepath, full_content, imports)
                method_chunk['metadata']['parent_chunk_id'] = class_id
                method_chunk['metadata']['chunk_type'] = 'method'
                method_ids.append(method_chunk['metadata']['chunk_id'])
                chunks.append(method_chunk)
        
        # Update class chunk with method references
        chunks[0]['metadata']['child_chunk_ids'] = method_ids
        
        return chunks
    
    def _extract_command_handlers(self, content: str, filepath: str) -> List[Dict]:
        """Extract command handling patterns from code"""
        chunks = []
        
        # Pattern for schedule.py style commands
        command_pattern = r"if\s+.*?\.upper\(\)\s*==\s*['\"](\$?[A-Z\-]+)['\"]:(.*?)(?=(?:elif|else:|if\s+.*?\.upper\(\)|$))"
        
        matches = re.finditer(command_pattern, content, re.DOTALL | re.MULTILINE)
        
        for match in matches:
            command = match.group(1)
            handler_code = match.group(2)
            
            # Generate chunk ID
            chunk_id = f"{Path(filepath).stem}_cmd_{command.replace('$', 'DOLLAR')}"
            
            # Extract any function calls in the handler
            calls = re.findall(r'(\w+)\s*\(', handler_code)
            
            metadata = ChunkMetadata(
                chunk_id=chunk_id,
                source_file=filepath,
                chunk_type="command_handler",
                chunk_level=1,
                commands_handled=[command],
                functions_called=calls,
                operational_context="command_execution",
                key_concepts=[command, "command_handling"]
            )
            
            chunks.append({
                'content': f"Command: {command}\n{handler_code}",
                'metadata': asdict(metadata)
            })
        
        return chunks
    
    def _extract_function_calls(self, node: ast.FunctionDef) -> Set[str]:
        """Extract all function calls within a function"""
        calls = set()
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    calls.add(child.func.id)
                elif isinstance(child.func, ast.Attribute):
                    calls.add(child.func.attr)
        return calls
    
    def _extract_exceptions(self, node: ast.FunctionDef) -> List[str]:
        """Extract exception types handled in function"""
        exceptions = []
        for child in ast.walk(node):
            if isinstance(child, ast.ExceptHandler):
                if child.type:
                    if isinstance(child.type, ast.Name):
                        exceptions.append(child.type.id)
        return exceptions
    
    def _extract_global_usage(self, node: ast.FunctionDef) -> Set[str]:
        """Extract global variables used in function"""
        globals_used = set()
        for child in ast.walk(node):
            if isinstance(child, ast.Global):
                globals_used.update(child.names)
        return globals_used
    
    def _get_function_signature(self, node: ast.FunctionDef, content: str) -> str:
        """Extract function signature as string"""
        lines = content.split('\n')
        sig_lines = []
        
        # Start from function definition line
        current_line = node.lineno - 1
        
        # Extract until we find the closing parenthesis
        while current_line < len(lines):
            line = lines[current_line]
            sig_lines.append(line.strip())
            if ')' in line and ':' in line:
                break
            current_line += 1
        
        return ' '.join(sig_lines)
    
    def _extract_function_comments(self, node: ast.FunctionDef, content: str) -> List[str]:
        """Extract inline comments from function body"""
        comments = []
        lines = content.split('\n')[node.lineno:node.end_lineno]
        
        for line in lines:
            # Find inline comments
            if '#' in line:
                comment_start = line.find('#')
                comment = line[comment_start:].strip()
                if comment and not comment.startswith('#####'):  # Skip decorative comments
                    comments.append(comment)
        
        return comments
    
    def _extract_handled_commands(self, node: ast.FunctionDef, content: str) -> List[str]:
        """Extract commands handled by this function"""
        commands = []
        
        # Look for command patterns in function body
        func_lines = content.split('\n')[node.lineno-1:node.end_lineno]
        func_text = '\n'.join(func_lines)
        
        # Common command patterns
        patterns = [
            r"['\"](\$[A-Z\-]+)['\"]",  # $COMMAND style
            r"command\s*==\s*['\"]([A-Z\-]+)['\"]",  # command == "COMMAND"
            r"\.send\(['\"]([A-Z\-]+\s+[^'\"]*)['\"]",  # socket.send("COMMAND ...")
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, func_text)
            commands.extend(matches)
        
        return list(set(commands))
    
    def _extract_hardware_components(self, node: ast.FunctionDef, content: str) -> List[str]:
        """Extract hardware components mentioned in function"""
        func_lines = content.split('\n')[node.lineno-1:node.end_lineno]
        func_text = '\n'.join(func_lines).lower()
        
        hardware_terms = [
            'antenna', 'roach', 'acc', 'correlator', 'receiver', 'feed',
            'lo', 'if', 'motor', 'sensor', 'synthesizer', 'frontend',
            'backend', 'nd_filter', 'power_meter', 'dish'
        ]
        
        found_hardware = []
        for term in hardware_terms:
            if term in func_text:
                found_hardware.append(term)
        
        return found_hardware
    
    def _determine_operational_context(self, content: str, name: str) -> str:
        """Determine operational context from function content and name"""
        content_lower = content.lower()
        name_lower = name.lower()
        
        contexts = {
            'calibration': ['calib', 'cal_', 'gain', 'phase', 'offset'],
            'tracking': ['track', 'point', 'position', 'move', 'goto'],
            'observation': ['observe', 'scan', 'record', 'data'],
            'monitoring': ['status', 'check', 'monitor', 'get_', 'read'],
            'control': ['set_', 'send', 'command', 'control'],
            'troubleshooting': ['error', 'debug', 'fix', 'repair'],
            'configuration': ['config', 'setup', 'init', 'configure']
        }
        
        for context, keywords in contexts.items():
            if any(keyword in name_lower or keyword in content_lower for keyword in keywords):
                return context
        
        return 'general'
    
    def _extract_key_concepts(self, content: str, name: str) -> List[str]:
        """Extract key concepts from content"""
        concepts = []
        
        # Add function/class name variants
        concepts.append(name.lower())
        concepts.extend(name.split('_'))
        
        # Look for telescope-specific terms
        telescope_terms = [
            'antenna', 'roach', 'delay', 'tracking', 'stateframe',
            'calibration', 'pointing', 'frequency', 'tuning', 'scan',
            'observation', 'correlator', 'receiver', 'attenuation'
        ]
        
        content_lower = content.lower()
        for term in telescope_terms:
            if term in content_lower:
                concepts.append(term)
        
        return list(set(concepts))
    
    def _extract_imports(self, tree: ast.AST) -> Dict[str, List[str]]:
        """Extract all imports from module"""
        imports = defaultdict(list)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports['direct'].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    for alias in node.names:
                        imports[node.module].append(alias.name)
        
        return dict(imports)
    
    def _create_module_chunk(self, filepath: str, tree: ast.AST, content: str) -> Dict:
        """Create module-level chunk with imports and globals"""
        
        # Extract module docstring
        module_docstring = ast.get_docstring(tree)
        
        # Extract all imports
        imports = self._extract_imports(tree)
        
        # Extract global variables
        globals_defined = []
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        globals_defined.append(target.id)
        
        # Create import section content
        import_lines = []
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith(('import ', 'from ')):
                import_lines.append(line)
            elif line.strip() and not line.strip().startswith('#'):
                # Stop at first non-import, non-comment line
                if i > 10:  # But check at least first 10 lines
                    break
        
        import_section = '\n'.join(import_lines)
        
        metadata = ChunkMetadata(
            chunk_id=f"{Path(filepath).stem}_module",
            source_file=filepath,
            chunk_type="module",
            chunk_level=3,
            docstring=module_docstring,
            imports_used=[f"{mod}.{func}" for mod, funcs in imports.items() 
                         for func in funcs],
            global_vars_accessed=globals_defined,
            key_concepts=self._extract_key_concepts(content[:500], Path(filepath).stem)
        )
        
        return {
            'content': f"Module: {Path(filepath).name}\n{module_docstring or ''}\n\n{import_section}",
            'metadata': asdict(metadata)
        }
    
    def _build_relationships(self, chunks: List[Dict]):
        """Build cross-references between chunks"""
        
        # Build function name to chunk ID mapping
        func_to_chunk = {}
        for chunk in chunks:
            if chunk['metadata']['chunk_type'] in ['function', 'method']:
                # Extract function name from chunk_id
                parts = chunk['metadata']['chunk_id'].split('_')
                if len(parts) >= 2:
                    func_name = parts[1]
                    func_to_chunk[func_name] = chunk['metadata']['chunk_id']
        
        # Update chunks with relationship information
        for chunk in chunks:
            if chunk['metadata']['functions_called']:
                # Find chunks for called functions
                related = []
                for called_func in chunk['metadata']['functions_called']:
                    if called_func in func_to_chunk:
                        related.append(func_to_chunk[called_func])
                chunk['metadata']['related_code_chunks'] = related
            
            # Set up reverse relationships
            chunk_id = chunk['metadata']['chunk_id']
            for other in chunks:
                if chunk_id in other['metadata'].get('related_code_chunks', []):
                    if 'functions_that_call_this' not in chunk['metadata']:
                        chunk['metadata']['functions_that_call_this'] = []
                    chunk['metadata']['functions_that_call_this'].append(
                        other['metadata']['chunk_id']
                    )
    
    def _fallback_text_analysis(self, filepath: str, content: str) -> List[Dict]:
        """Fallback analysis when AST parsing fails"""
        chunks = []
        
        # Try to extract functions using regex
        func_pattern = r'^def\s+(\w+)\s*\([^)]*\):\s*\n((?:\s{4,}.*\n)*)'
        
        for match in re.finditer(func_pattern, content, re.MULTILINE):
            func_name = match.group(1)
            func_body = match.group(0)
            
            # Extract docstring if present
            docstring_match = re.search(r'"""(.*?)"""', func_body, re.DOTALL)
            docstring = docstring_match.group(1) if docstring_match else None
            
            metadata = ChunkMetadata(
                chunk_id=f"{Path(filepath).stem}_{func_name}_text",
                source_file=filepath,
                chunk_type="function",
                chunk_level=1,
                function_signature=f"def {func_name}(...)",
                docstring=docstring,
                key_concepts=self._extract_key_concepts(func_body, func_name)
            )
            
            chunks.append({
                'content': func_body,
                'metadata': asdict(metadata)
            })
        
        return chunks


class WikiAnalyzer:
    """Analyzer for wiki/markdown documentation"""
    
    def analyze_wiki(self, content: str, source_file: str) -> List[Dict]:
        """Analyze wiki/markdown content"""
        chunks = []
        
        # Extract sections
        sections = self._extract_sections(content)
        
        for section in sections:
            # Determine section type
            section_type = self._classify_section(section)
            
            if section_type == 'troubleshooting':
                problem_chunks = self._extract_problem_solutions(section, source_file)
                chunks.extend(problem_chunks)
            elif section_type == 'procedure':
                procedure_chunk = self._create_procedure_chunk(section, source_file)
                chunks.append(procedure_chunk)
            elif section_type == 'command_reference':
                command_chunks = self._extract_command_docs(section, source_file)
                chunks.extend(command_chunks)
            else:
                # Generic section chunk
                generic_chunk = self._create_generic_chunk(section, source_file)
                chunks.append(generic_chunk)
        
        return chunks
    
    def _extract_sections(self, content: str) -> List[Dict]:
        """Extract sections based on headers"""
        sections = []
        
        # Split by headers (##, ###, etc.)
        header_pattern = r'^(#{1,4})\s+(.+)$'
        
        current_section = {'title': 'Introduction', 'level': 0, 'content': '', 'subsections': []}
        
        for line in content.split('\n'):
            header_match = re.match(header_pattern, line)
            
            if header_match:
                # Save current section if it has content
                if current_section['content'].strip():
                    sections.append(current_section)
                
                # Start new section
                level = len(header_match.group(1))
                title = header_match.group(2)
                current_section = {
                    'title': title,
                    'level': level,
                    'content': '',
                    'subsections': []
                }
            else:
                current_section['content'] += line + '\n'
        
        # Add last section
        if current_section['content'].strip():
            sections.append(current_section)
        
        return sections
    
    def _classify_section(self, section: Dict) -> str:
        """Classify section type based on content and title"""
        title_lower = section['title'].lower()
        content_lower = section['content'].lower()
        
        # Troubleshooting indicators
        if any(word in title_lower for word in ['troubleshoot', 'problem', 'issue', 'error']):
            return 'troubleshooting'
        
        if 'if' in content_lower and 'then' in content_lower and 'fix' in content_lower:
            return 'troubleshooting'
        
        # Procedure indicators
        if any(word in title_lower for word in ['procedure', 'how to', 'guide', 'steps']):
            return 'procedure'
        
        if re.search(r'\d+\.\s+\w+', section['content']):  # Numbered steps
            return 'procedure'
        
        # Command reference
        if any(word in title_lower for word in ['command', 'reference', 'syntax']):
            return 'command_reference'
        
        return 'general'
    
    def _extract_problem_solutions(self, section: Dict, source_file: str) -> List[Dict]:
        """Extract problem-solution pairs from troubleshooting sections"""
        chunks = []
        
        # Pattern for problem-solution pairs
        # Looking for headers followed by solution text
        problem_pattern = r'###\s+(.+?)\n((?:(?!###).)+)'
        
        matches = re.finditer(problem_pattern, section['content'], re.DOTALL)
        
        for match in matches:
            problem = match.group(1).strip()
            solution = match.group(2).strip()
            
            # Extract symptoms (usually in first paragraph)
            symptoms = self._extract_symptoms(solution)
            
            # Extract solution steps
            steps = self._extract_steps(solution)
            
            # Generate chunk ID
            chunk_id = f"wiki_{hashlib.md5(problem.encode()).hexdigest()[:8]}"
            
            metadata = ChunkMetadata(
                chunk_id=chunk_id,
                source_file=source_file,
                chunk_type="troubleshooting",
                chunk_level=1,
                problem_symptoms=symptoms,
                solutions_provided=steps,
                operational_context="troubleshooting",
                criticality=self._assess_criticality(problem, solution),
                time_sensitivity=self._assess_time_sensitivity(solution),
                key_concepts=self._extract_key_concepts(f"{problem} {solution}", "troubleshooting")
            )
            
            chunks.append({
                'content': f"Problem: {problem}\n\nSolution:\n{solution}",
                'metadata': asdict(metadata)
            })
        
        return chunks
    
    def _extract_symptoms(self, text: str) -> List[str]:
        """Extract symptom descriptions from text"""
        symptoms = []
        
        # Look for symptom indicators
        symptom_patterns = [
            r'shows?\s+(.+)',
            r'displays?\s+(.+)',
            r'returns?\s+(.+)',
            r'(?:is|are)\s+(?:showing|displaying)\s+(.+)',
            r'error:?\s*(.+)',
        ]
        
        for pattern in symptom_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            symptoms.extend([m.strip() for m in matches if len(m.strip()) < 100])
        
        return symptoms[:5]  # Limit to 5 symptoms
    
    def _extract_steps(self, text: str) -> List[str]:
        """Extract solution steps from text"""
        steps = []
        
        # Look for numbered steps
        step_pattern = r'(?:\d+\.|Step\s+\d+:?)\s*(.+?)(?=(?:\d+\.|Step\s+\d+:|$))'
        matches = re.findall(step_pattern, text, re.DOTALL | re.IGNORECASE)
        
        if matches:
            steps = [step.strip().replace('\n', ' ') for step in matches]
        else:
            # Look for command patterns as steps
            cmd_pattern = r'(?:type|enter|issue|send|execute)\s+["\']?([^"\'\n]+)["\']?'
            matches = re.findall(cmd_pattern, text, re.IGNORECASE)
            steps = matches
        
        return steps
    
    def _assess_criticality(self, problem: str, solution: str) -> str:
        """Assess the criticality level of a problem"""
        text = f"{problem} {solution}".lower()
        
        if any(word in text for word in ['emergency', 'critical', 'immediately', 'urgent']):
            return 'emergency'
        elif any(word in text for word in ['important', 'soon', 'quickly']):
            return 'critical'
        elif any(word in text for word in ['should', 'recommend']):
            return 'important'
        else:
            return 'routine'
    
    def _assess_time_sensitivity(self, text: str) -> str:
        """Assess time sensitivity of a solution"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['immediately', 'right away', 'urgent']):
            return 'immediate'
        elif any(word in text_lower for word in ['within minutes', 'quickly', 'soon']):
            return 'minutes'
        elif any(word in text_lower for word in ['within hours', 'today']):
            return 'hours'
        else:
            return 'none'
    
    def _create_procedure_chunk(self, section: Dict, source_file: str) -> Dict:
        """Create chunk for a procedure section"""
        
        # Extract steps
        steps = self._extract_steps(section['content'])
        
        # Identify prerequisites
        prereqs = self._extract_prerequisites(section['content'])
        
        chunk_id = f"proc_{hashlib.md5(section['title'].encode()).hexdigest()[:8]}"
        
        metadata = ChunkMetadata(
            chunk_id=chunk_id,
            source_file=source_file,
            chunk_type="procedure",
            chunk_level=2,
            solutions_provided=steps,
            prerequisite_chunks=prereqs,
            operational_context="procedure",
            key_concepts=self._extract_key_concepts(section['content'], section['title'])
        )
        
        return {
            'content': f"## {section['title']}\n\n{section['content']}",
            'metadata': asdict(metadata)
        }
    
    def _extract_prerequisites(self, text: str) -> List[str]:
        """Extract prerequisites from procedure text"""
        prereqs = []
        
        # Look for prerequisite indicators
        prereq_patterns = [
            r'(?:before|prior to|must first)\s+(.+)',
            r'(?:requires?|needs?)\s+(.+)',
            r'(?:ensure|make sure|check that)\s+(.+)',
        ]
        
        for pattern in prereq_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            prereqs.extend([m.strip() for m in matches if len(m.strip()) < 100])
        
        return prereqs[:3]  # Limit to 3 prerequisites
    
    def _extract_command_docs(self, section: Dict, source_file: str) -> List[Dict]:
        """Extract command documentation"""
        chunks = []
        
        # Look for command definitions
        cmd_pattern = r'(?:^|\n)([A-Z$][A-Z\-_$]+)\s+(.+?)(?=(?:^|\n)[A-Z$][A-Z\-_$]+\s+|$)'
        
        matches = re.finditer(cmd_pattern, section['content'], re.DOTALL | re.MULTILINE)
        
        for match in matches:
            command = match.group(1).strip()
            description = match.group(2).strip()
            
            chunk_id = f"cmd_doc_{command.replace('$', 'DOLLAR')}"
            
            metadata = ChunkMetadata(
                chunk_id=chunk_id,
                source_file=source_file,
                chunk_type="command_reference",
                chunk_level=1,
                commands_handled=[command],
                key_concepts=[command.lower(), 'command']
            )
            
            chunks.append({
                'content': f"Command: {command}\n\n{description}",
                'metadata': asdict(metadata)
            })
        
        return chunks
    
    def _create_generic_chunk(self, section: Dict, source_file: str) -> Dict:
        """Create a generic chunk for unclassified sections"""
        
        chunk_id = f"section_{hashlib.md5(section['title'].encode()).hexdigest()[:8]}"
        
        metadata = ChunkMetadata(
            chunk_id=chunk_id,
            source_file=source_file,
            chunk_type="general",
            chunk_level=2,
            key_concepts=self._extract_key_concepts(section['content'], section['title'])
        )
        
        return {
            'content': f"## {section['title']}\n\n{section['content']}",
            'metadata': asdict(metadata)
        }
    
    def _extract_key_concepts(self, content: str, title: str) -> List[str]:
        """Extract key concepts from wiki content"""
        concepts = []
        
        # Add title words
        title_words = re.findall(r'\w+', title.lower())
        concepts.extend([word for word in title_words if len(word) > 2])
        
        # Look for telescope-specific terms
        telescope_terms = [
            'antenna', 'roach', 'delay', 'tracking', 'stateframe',
            'calibration', 'pointing', 'frequency', 'tuning', 'scan',
            'observation', 'correlator', 'receiver', 'attenuation',
            'solar', 'flare', 'eovsa', 'command', 'schedule'
        ]
        
        content_lower = content.lower()
        for term in telescope_terms:
            if term in content_lower:
                concepts.append(term)
        
        # Look for command patterns
        command_matches = re.findall(r'\$[A-Z\-]+', content)
        concepts.extend([cmd.lower().replace('$', 'DOLLAR') for cmd in command_matches[:3]])
        
        return list(set(concepts))


class AIEnhancer:
    """AI-powered metadata enhancement using OpenAI"""
    
    def __init__(self, api_key: str = None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.cost_tracker = 0.0
        
    def enhance_chunk(self, chunk: Dict) -> Dict:
        """Enhance chunk with AI-generated metadata"""
        
        metadata = chunk['metadata']
        content = chunk['content']
        chunk_type = metadata['chunk_type']
        
        try:
            if chunk_type == 'function':
                enhancement = self._enhance_function(content, metadata)
            elif chunk_type == 'troubleshooting':
                enhancement = self._enhance_troubleshooting(content, metadata)
            elif chunk_type == 'procedure':
                enhancement = self._enhance_procedure(content, metadata)
            elif chunk_type == 'command_handler':
                enhancement = self._enhance_command(content, metadata)
            else:
                enhancement = self._enhance_generic(content, metadata)
            
            # Update metadata with AI enhancements
            metadata.update(enhancement)
            
        except Exception as e:
            print(f"AI enhancement failed for chunk {metadata['chunk_id']}: {e}")
            # Continue without AI enhancement
            
        return chunk
    
    
    def _enhance_function(self, content: str, metadata: Dict) -> Dict:
        """AI enhancement for function chunks (using strict JSON schema for GPT-5-mini)"""
        
        # Prepare the input without embedding the schema in the prompt
        prompt = f"""
        Analyze this EOVSA telescope control function.
        
        Function: {metadata.get('function_signature', 'Unknown')}
        Code: {content[:1000]}...
        Docstring: {metadata.get('docstring', 'None')}
        Commands handled: {metadata.get('commands_handled', [])}
        Hardware components: {metadata.get('hardware_components', [])}
        """
        
        # JSON schema for the response
        schema = {
            "name": "function_analysis",
            "schema": {
                "type": "object",
                "properties": {
                    "ai_summary": {"type": "string"},
                    "ai_purpose": {"type": "string"},
                    "ai_dependencies": {"type": "string"},
                    "ai_error_scenarios": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "ai_usage_examples": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "search_keywords": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": [
                    "ai_summary",
                    "ai_purpose",
                    "ai_dependencies",
                    "ai_error_scenarios",
                    "ai_usage_examples",
                    "search_keywords"
                ]
            }
        }
        
        # Call the OpenAI API with strict structured output
        response = self.client.responses.create(
            model="gpt-5-mini",
            input=prompt,
            max_output_tokens=500,
            response_format={
                "type": "json_schema",
                "json_schema": schema,
                "strict": True
            }
        )
        
        # The response is already valid JSON according to schema
        return response.output_parsed

    def _enhance_troubleshooting(self, content: str, metadata: Dict) -> Dict:
        """AI enhancement for troubleshooting chunks"""
        
        prompt = f"""
        Analyze this telescope troubleshooting information:
        
        Content: {content[:800]}
        Problem symptoms: {metadata.get('problem_symptoms', [])}
        Solution steps: {metadata.get('solutions_provided', [])}
        
        Provide analysis in JSON format:
        {{
            "ai_summary": "Brief description of the problem and solution",
            "ai_purpose": "What this troubleshooting addresses",
            "ai_dependencies": "Prerequisites or conditions needed",
            "ai_error_scenarios": ["related problems that might occur"],
            "search_keywords": ["terms people would search for this problem"]
        }}
        """
        
        response = self._call_openai(prompt, max_tokens=400)
        return self._parse_json_response(response)
    
    def _enhance_procedure(self, content: str, metadata: Dict) -> Dict:
        """AI enhancement for procedure chunks"""
        
        prompt = f"""
        Analyze this telescope procedure:
        
        Content: {content[:800]}
        Steps: {metadata.get('solutions_provided', [])}
        
        Provide analysis in JSON format:
        {{
            "ai_summary": "What this procedure accomplishes",
            "ai_purpose": "When and why to use this procedure",
            "ai_dependencies": "What must be done or checked first",
            "ai_error_scenarios": ["potential problems during execution"],
            "search_keywords": ["terms for finding this procedure"]
        }}
        """
        
        response = self._call_openai(prompt, max_tokens=400)
        return self._parse_json_response(response)
    
    def _enhance_command(self, content: str, metadata: Dict) -> Dict:
        """AI enhancement for command handler chunks"""
        
        prompt = f"""
        Analyze this telescope command handler:
        
        Content: {content[:600]}
        Commands: {metadata.get('commands_handled', [])}
        
        Provide analysis in JSON format:
        {{
            "ai_summary": "What this command does",
            "ai_purpose": "Purpose of this command in operations",
            "ai_dependencies": "System state or conditions required",
            "ai_error_scenarios": ["potential command failures"],
            "search_keywords": ["terms for finding this command"]
        }}
        """
        
        response = self._call_openai(prompt, max_tokens=300)
        return self._parse_json_response(response)
    
    def _enhance_generic(self, content: str, metadata: Dict) -> Dict:
        """AI enhancement for generic chunks"""
        
        prompt = f"""
        Analyze this telescope documentation:
        
        Content: {content[:600]}
        Type: {metadata.get('chunk_type', 'unknown')}
        
        Provide analysis in JSON format:
        {{
            "ai_summary": "Brief description of content",
            "ai_purpose": "Purpose or relevance to telescope operations",
            "search_keywords": ["relevant search terms"]
        }}
        """
        
        response = self._call_openai(prompt, max_tokens=200)
        return self._parse_json_response(response)
    
    def _call_openai(self, prompt: str, max_tokens: int = 500) -> str:
        """Make OpenAI API call with error handling"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-5-mini",
                messages=[
                    {"role": "system", "content": "You are an expert in radio telescope systems. Provide concise, accurate analysis in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.1
            )
            
            # Track costs (approximate)
            self.cost_tracker += max_tokens * 0.0001  # Rough estimate
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"OpenAI API call failed: {e}")
            return "{}"
    
    def _parse_json_response(self, response: str) -> Dict:
        """Parse JSON response with fallback"""
        
        try:
            # Clean up response (remove markdown formatting if present)
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
            
            return json.loads(response)
        except json.JSONDecodeError:
            print(f"Failed to parse JSON response: {response[:100]}...")
            return {}


class CrossReferenceBuilder:
    """Build cross-references between chunks"""
    
    def __init__(self):
        self.command_to_chunks = defaultdict(list)
        self.function_to_chunks = defaultdict(list)
        self.concept_to_chunks = defaultdict(list)
        self.hardware_to_chunks = defaultdict(list)
    
    def build_references(self, all_chunks: List[Dict]) -> List[Dict]:
        """Build cross-reference indices and update chunks"""
        
        # Build indices
        self._build_indices(all_chunks)
        
        # Update chunks with cross-references
        for chunk in all_chunks:
            self._add_cross_references(chunk)
        
        return all_chunks
    
    def _build_indices(self, chunks: List[Dict]):
        """Build various indices for cross-referencing"""
        
        for chunk in chunks:
            metadata = chunk['metadata']
            chunk_id = metadata['chunk_id']
            
            # Index by commands
            for command in metadata.get('commands_handled', []):
                self.command_to_chunks[command.lower()].append(chunk_id)
            
            # Index by functions
            if metadata['chunk_type'] in ['function', 'method']:
                func_name = self._extract_function_name(chunk_id)
                if func_name:
                    self.function_to_chunks[func_name].append(chunk_id)
            
            # Index by concepts
            for concept in metadata.get('key_concepts', []):
                self.concept_to_chunks[concept.lower()].append(chunk_id)
            
            # Index by hardware
            for hardware in metadata.get('hardware_components', []):
                self.hardware_to_chunks[hardware.lower()].append(chunk_id)
    
    def _add_cross_references(self, chunk: Dict):
        """Add cross-references to a chunk"""
        
        metadata = chunk['metadata']
        chunk_id = metadata['chunk_id']
        
        related_chunks = set()
        
        # Find chunks with shared commands
        for command in metadata.get('commands_handled', []):
            related_chunks.update(self.command_to_chunks[command.lower()])
        
        # Find chunks with shared concepts
        for concept in metadata.get('key_concepts', []):
            related_chunks.update(self.concept_to_chunks[concept.lower()])
        
        # Find chunks with shared hardware
        for hardware in metadata.get('hardware_components', []):
            related_chunks.update(self.hardware_to_chunks[hardware.lower()])
        
        # Remove self-reference
        related_chunks.discard(chunk_id)
        
        # Update metadata
        if related_chunks:
            existing_related = set(metadata.get('see_also_chunks', []))
            metadata['see_also_chunks'] = list(existing_related.union(related_chunks))
    
    def _extract_function_name(self, chunk_id: str) -> Optional[str]:
        """Extract function name from chunk ID"""
        parts = chunk_id.split('_')
        if len(parts) >= 2 and not parts[1].isdigit():
            return parts[1]
        return None


class EnhancedDocumentProcessor:
    """Main processor class that orchestrates all analyzers"""
    
    def __init__(self, use_ai: bool = True, cost_limit: float = 10.0):
        self.code_analyzer = CodeAnalyzer()
        self.wiki_analyzer = WikiAnalyzer()
        self.cross_ref_builder = CrossReferenceBuilder()
        
        self.use_ai = use_ai
        self.cost_limit = cost_limit
        
        if use_ai:
            self.ai_enhancer = AIEnhancer()
        else:
            self.ai_enhancer = None
    
    def process_directory(self, data_dir: str) -> List[Dict]:
        """Process all files in a directory"""
        
        all_chunks = []
        data_path = Path(data_dir)
        
        print(f"🔍 Processing directory: {data_dir}")
        
        # Process Python files
        code_files = list(data_path.rglob("*.py"))
        print(f"📝 Found {len(code_files)} Python files")
        
        for py_file in code_files:
            print(f"  Analyzing: {py_file.name}")
            try:
                file_chunks = self.code_analyzer.analyze_file(str(py_file))
                all_chunks.extend(file_chunks)
            except Exception as e:
                print(f"  ❌ Error processing {py_file}: {e}")
        
        # Process markdown/wiki files
        wiki_files = list(data_path.rglob("*.md")) + list(data_path.rglob("*.txt"))
        print(f"📄 Found {len(wiki_files)} documentation files")
        
        for wiki_file in wiki_files:
            if wiki_file.name.lower() in ['readme.md', 'license.txt']:
                continue
                
            print(f"  Analyzing: {wiki_file.name}")
            try:
                with open(wiki_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                file_chunks = self.wiki_analyzer.analyze_wiki(content, str(wiki_file))
                all_chunks.extend(file_chunks)
            except Exception as e:
                print(f"  ❌ Error processing {wiki_file}: {e}")
        
        print(f"✅ Extracted {len(all_chunks)} chunks total")
        
        # Build cross-references
        print("🔗 Building cross-references...")
        all_chunks = self.cross_ref_builder.build_references(all_chunks)
        
        # AI enhancement (if enabled)
        if self.use_ai and self.ai_enhancer:
            print(f"🤖 Enhancing chunks with AI (cost limit: ${self.cost_limit})")
            enhanced_count = 0
            
            for i, chunk in enumerate(all_chunks):
                if self.ai_enhancer.cost_tracker > self.cost_limit:
                    print(f"💰 Cost limit reached (${self.cost_limit}), stopping AI enhancement")
                    break
                
                if i % 10 == 0:
                    print(f"  Enhanced {i}/{len(all_chunks)} chunks (cost: ${self.ai_enhancer.cost_tracker:.2f})")
                
                enhanced_chunk = self.ai_enhancer.enhance_chunk(chunk)
                all_chunks[i] = enhanced_chunk
                enhanced_count += 1
            
            print(f"🤖 Enhanced {enhanced_count} chunks with AI")
            print(f"💰 Total AI cost: ${self.ai_enhancer.cost_tracker:.2f}")
        
        # Generate summary statistics
        self._print_statistics(all_chunks)
        
        return all_chunks
    
    def process_existing_documents(self, input_file: str) -> List[Dict]:
        """Process existing processed documents"""
        
        print(f"📂 Loading existing documents from {input_file}")
        
        with open(input_file, 'r', encoding='utf-8') as f:
            documents = json.load(f)
        
        all_chunks = []
        
        for doc in documents:
            if doc.get('type') == 'source_code':
                # Re-process code with enhanced analysis
                print(f"  Re-analyzing code: {doc.get('title', 'Unknown')}")
                try:
                    # Create temporary file to analyze
                    temp_content = doc['content']
                    file_chunks = self.code_analyzer._fallback_text_analysis(
                        doc['source'], temp_content
                    )
                    all_chunks.extend(file_chunks)
                except Exception as e:
                    print(f"  ❌ Error re-processing {doc.get('title')}: {e}")
            else:
                # Convert existing document to chunk format
                chunk_id = f"legacy_{hashlib.md5(doc['source'].encode()).hexdigest()[:8]}"
                
                metadata = ChunkMetadata(
                    chunk_id=chunk_id,
                    source_file=doc['source'],
                    chunk_type=doc.get('type', 'general'),
                    chunk_level=2,
                    key_concepts=doc.get('metadata', {}).get('key_concepts', [])
                )
                
                chunk = {
                    'content': doc['content'],
                    'metadata': asdict(metadata)
                }
                
                all_chunks.append(chunk)
        
        # Continue with cross-references and AI enhancement
        print("🔗 Building cross-references...")
        all_chunks = self.cross_ref_builder.build_references(all_chunks)
        
        if self.use_ai and self.ai_enhancer:
            print(f"🤖 Enhancing chunks with AI...")
            for i, chunk in enumerate(all_chunks):
                if self.ai_enhancer.cost_tracker > self.cost_limit:
                    break
                all_chunks[i] = self.ai_enhancer.enhance_chunk(chunk)
        
        self._print_statistics(all_chunks)
        
        return all_chunks
    
    def save_processed_chunks(self, chunks: List[Dict], output_file: str):
        """Save processed chunks to file"""
        
        # Convert chunks to serializable format
        serializable_chunks = []
        for chunk in chunks:
            # Remove non-serializable items
            clean_chunk = {
                'chunk_id': chunk['metadata']['chunk_id'],
                'content': chunk['content'],
                'metadata': {k: v for k, v in chunk['metadata'].items() 
                           if k != 'ast_node'}  # Remove AST nodes
            }
            serializable_chunks.append(clean_chunk)
        
        # Save to file
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(serializable_chunks, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved {len(serializable_chunks)} processed chunks to {output_file}")
    
    def _print_statistics(self, chunks: List[Dict]):
        """Print processing statistics"""
        
        print("\n" + "="*60)
        print("📊 PROCESSING STATISTICS")
        print("="*60)
        
        total_chunks = len(chunks)
        print(f"Total chunks: {total_chunks}")
        
        # Count by type
        type_counts = defaultdict(int)
        level_counts = defaultdict(int)
        
        for chunk in chunks:
            metadata = chunk['metadata']
            type_counts[metadata['chunk_type']] += 1
            level_counts[metadata['chunk_level']] += 1
        
        print("\nChunk Types:")
        for chunk_type, count in sorted(type_counts.items()):
            print(f"  {chunk_type}: {count}")
        
        print("\nChunk Levels:")
        for level, count in sorted(level_counts.items()):
            level_name = {1: "Atomic", 2: "Contextual", 3: "System"}
            print(f"  Level {level} ({level_name.get(level, 'Unknown')}): {count}")
        
        # Count cross-references
        cross_refs = sum(1 for chunk in chunks 
                        if chunk['metadata'].get('related_code_chunks') or 
                           chunk['metadata'].get('see_also_chunks'))
        
        print(f"\nChunks with cross-references: {cross_refs}")
        
        # Count AI enhancements
        ai_enhanced = sum(1 for chunk in chunks 
                         if chunk['metadata'].get('ai_summary'))
        
        print(f"AI-enhanced chunks: {ai_enhanced}")
        print("="*60)


def main():
    """Main execution function"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Enhanced Radio Telescope Document Processor')
    parser.add_argument('--input-dir', required=True, help='Input directory or existing JSON file')
    parser.add_argument('--output', default='data/processed/enhanced_chunks.json', 
                       help='Output file path')
    parser.add_argument('--no-ai', action='store_true', help='Disable AI enhancement')
    parser.add_argument('--cost-limit', type=float, default=10.0, help='AI cost limit in USD')
    
    args = parser.parse_args()
    
    # Initialize processor
    processor = EnhancedDocumentProcessor(
        use_ai=not args.no_ai,
        cost_limit=args.cost_limit
    )
    
    # Process input
    input_path = Path(args.input_dir)
    
    if input_path.is_file() and input_path.suffix == '.json':
        # Process existing JSON file
        chunks = processor.process_existing_documents(str(input_path))
    elif input_path.is_dir():
        # Process directory
        chunks = processor.process_directory(str(input_path))
    else:
        print(f"❌ Invalid input path: {input_path}")
        return
    
    # Save results
    processor.save_processed_chunks(chunks, args.output)
    
    print(f"\n✅ Processing complete!")
    print(f"📁 Enhanced chunks saved to: {args.output}")
    print(f"🔍 Ready for advanced RAG retrieval!")


if __name__ == "__main__":
    main()
        