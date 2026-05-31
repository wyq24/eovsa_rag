#!/usr/bin/env python3
"""
Enhanced Radio Telescope Documentation Processor
Comprehensive processing for EOVSA telescope system documentation and code
Multi-language support: Python, Fortran, C/C++, Shell
"""

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


class MultiLanguageCodeAnalyzer:
    """Advanced multi-language code analysis for telescope control software"""

    def __init__(self):
        self.function_graph = defaultdict(set)  # func -> functions it calls
        self.reverse_graph = defaultdict(set)  # func -> functions that call it
        self.import_graph = defaultdict(set)  # module -> imported modules
        self.global_usage = defaultdict(set)  # func -> globals used
        self.command_handlers = {}  # command -> handler function

        # Language-specific patterns
        self.language_patterns = {
            'fortran': {
                'subroutine': r'^\s*subroutine\s+(\w+)\s*\(',
                'function': r'^\s*(?:integer|real|double\s+precision|character|logical)?\s*function\s+(\w+)\s*\(',
                'module': r'^\s*module\s+(\w+)',
                'program': r'^\s*program\s+(\w+)',
                'use': r'^\s*use\s+(\w+)',
                'include': r'^\s*include\s+[\'"]([^\'"]+)[\'"]',
                'parameter': r'^\s*parameter\s*\(\s*(\w+)\s*=',
                'common': r'^\s*common\s*/(\w+)/',
                'comment': r'^\s*[!cC]',
                'end': r'^\s*end\s*(?:subroutine|function|module|program)?'
            },
            'c': {
                'function': r'^\s*(?:static\s+|extern\s+)?(?:\w+\s+)*(\w+)\s*\([^)]*\)\s*{',
                'struct': r'^\s*(?:typedef\s+)?struct\s+(\w+)',
                'enum': r'^\s*(?:typedef\s+)?enum\s+(\w+)',
                'typedef': r'^\s*typedef\s+.*\s+(\w+);',
                'define': r'^\s*#define\s+(\w+)',
                'include': r'^\s*#include\s*[<"]([^>"]+)[>"]',
                'ifdef': r'^\s*#ifdef\s+(\w+)',
                'ifndef': r'^\s*#ifndef\s+(\w+)',
                'global_var': r'^\s*(?:static\s+|extern\s+)?(?:const\s+)?\w+\s+(\w+)\s*[;=]',
                'comment_single': r'^\s*//',
                'comment_multi_start': r'/\*',
                'comment_multi_end': r'\*/'
            },
            'cpp': {
                'function': r'^\s*(?:virtual\s+|static\s+|inline\s+)*(?:\w+\s+)*(\w+)\s*\([^)]*\)\s*(?:const\s*)?{',
                'class': r'^\s*class\s+(\w+)',
                'namespace': r'^\s*namespace\s+(\w+)',
                'template': r'^\s*template\s*<',
                'constructor': r'^\s*(\w+)\s*\([^)]*\)\s*:',
                'destructor': r'^\s*~(\w+)\s*\(\s*\)',
                'operator': r'^\s*(?:\w+\s+)?operator\s*([^\s(]+)',
                'using': r'^\s*using\s+(?:namespace\s+)?(\w+)',
                'include': r'^\s*#include\s*[<"]([^>"]+)[>"]'
            },
            'shell': {
                'function': r'^\s*(\w+)\s*\(\s*\)\s*{',
                'function_alt': r'^\s*function\s+(\w+)',
                'variable': r'^\s*(\w+)=',
                'export': r'^\s*export\s+(\w+)',
                'alias': r'^\s*alias\s+(\w+)=',
                'source': r'^\s*(?:source|\.) ([^\s]+)',
                'if': r'^\s*if\s+',
                'for': r'^\s*for\s+(\w+)',
                'while': r'^\s*while\s+',
                'case': r'^\s*case\s+',
                'comment': r'^\s*#',
                'shebang': r'^#!/'
            }
        }

    def get_file_language(self, filepath: str) -> str:
        """Determine programming language from file extension"""
        ext = Path(filepath).suffix.lower()
        language_map = {
            '.py': 'python',
            '.f': 'fortran', '.f77': 'fortran', '.f90': 'fortran',
            '.f95': 'fortran', '.f03': 'fortran', '.for': 'fortran',
            '.c': 'c', '.h': 'c',
            '.cpp': 'cpp', '.cxx': 'cpp', '.cc': 'cpp',
            '.hpp': 'cpp', '.hxx': 'cpp', '.hh': 'cpp',
            '.sh': 'shell', '.bash': 'shell', '.csh': 'shell',
            '.ksh': 'shell', '.zsh': 'shell'
        }
        return language_map.get(ext, 'unknown')

    def analyze_file(self, filepath: str) -> List[Dict]:
        """Comprehensive analysis of any supported file type"""
        language = self.get_file_language(filepath)

        print(f"🔍 Analyzing {language} file: {Path(filepath).name}")

        if language == 'python':
            return self.analyze_python_file(filepath)
        elif language == 'fortran':
            return self.analyze_fortran_file(filepath)
        elif language in ['c', 'cpp']:
            return self.analyze_c_cpp_file(filepath, language)
        elif language == 'shell':
            return self.analyze_shell_file(filepath)
        else:
            print(f"⚠️  Unsupported language: {language}")
            return self.analyze_generic_file(filepath)

    def analyze_python_file(self, filepath: str) -> List[Dict]:
        """Python analysis (existing functionality preserved)"""
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

        # Extract command handlers
        command_chunks = self._extract_command_handlers(content, filepath)
        chunks.extend(command_chunks)

        # Build relationships
        self._build_relationships(chunks)

        return chunks

    def analyze_fortran_file(self, filepath: str) -> List[Dict]:
        """Analyze Fortran files (F77, F90, F95, F03)"""
        chunks = []

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Create module-level chunk
        module_chunk = self._create_fortran_module_chunk(filepath, content)
        chunks.append(module_chunk)

        # Extract Fortran constructs
        lines = content.split('\n')
        current_construct = None
        current_lines = []
        construct_start = 0

        for i, line in enumerate(lines):
            line_clean = line.strip().lower()

            # Skip comments and empty lines for construct detection
            if self._is_fortran_comment(line) or not line_clean:
                if current_construct:
                    current_lines.append(line)
                continue

            # Check for new construct
            new_construct = self._detect_fortran_construct(line, i)

            if new_construct:
                # Save previous construct
                if current_construct and current_lines:
                    chunk = self._create_fortran_construct_chunk(
                        current_construct, current_lines, filepath, construct_start
                    )
                    chunks.append(chunk)

                # Start new construct
                current_construct = new_construct
                current_lines = [line]
                construct_start = i
            elif current_construct:
                current_lines.append(line)

                # Check for end of construct
                if self._is_fortran_end(line, current_construct['type']):
                    chunk = self._create_fortran_construct_chunk(
                        current_construct, current_lines, filepath, construct_start
                    )
                    chunks.append(chunk)
                    current_construct = None
                    current_lines = []

        # Handle any remaining construct
        if current_construct and current_lines:
            chunk = self._create_fortran_construct_chunk(
                current_construct, current_lines, filepath, construct_start
            )
            chunks.append(chunk)

        return chunks

    def analyze_c_cpp_file(self, filepath: str, language: str) -> List[Dict]:
        """Analyze C/C++ files"""
        chunks = []

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Create module-level chunk
        module_chunk = self._create_c_module_chunk(filepath, content, language)
        chunks.append(module_chunk)

        # Extract functions
        chunks.extend(self._extract_c_functions(filepath, content, language))

        return chunks

    def analyze_shell_file(self, filepath: str) -> List[Dict]:
        """Analyze shell script files"""
        chunks = []

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Create module-level chunk
        module_chunk = self._create_shell_module_chunk(filepath, content)
        chunks.append(module_chunk)

        # Extract shell functions
        chunks.extend(self._extract_shell_functions(filepath, content))

        return chunks

    def analyze_generic_file(self, filepath: str) -> List[Dict]:
        """Fallback analysis for unsupported file types"""

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Create a single chunk for the entire file
        chunk_id = f"{Path(filepath).stem}_generic"

        metadata = ChunkMetadata(
            chunk_id=chunk_id,
            source_file=filepath,
            chunk_type="function",
            chunk_level=1,
            function_signature=f"function {func_name}()",
            key_concepts=self._extract_key_concepts(content, func_name),
            operational_context=self._determine_shell_context(content, func_name)
        )

        return {
            'content': content,
            'metadata': asdict(metadata)
        }

    def _determine_shell_context(self, content: str, name: str) -> str:
        """Determine operational context for shell code"""
        content_lower = content.lower()
        name_lower = name.lower()

        contexts = {
            'system_control': ['start', 'stop', 'restart', 'status', 'service'],
            'file_management': ['copy', 'move', 'backup', 'archive', 'sync'],
            'observation': ['observe', 'scan', 'record', 'schedule'],
            'maintenance': ['check', 'test', 'repair', 'update', 'install'],
            'monitoring': ['monitor', 'watch', 'log', 'alert', 'notify']
        }

        for context, keywords in contexts.items():
            if any(keyword in name_lower or keyword in content_lower for keyword in keywords):
                return context

        return 'general'

    def _create_shell_module_chunk(self, filepath: str, content: str) -> Dict:
        """Create module-level chunk for shell script"""

        header_lines = []
        for i, line in enumerate(content.split('\n')):
            if i > 50:
                break

            if (line.startswith('#') or
                    'source' in line or
                    '. ' in line or
                    not line.strip()):
                header_lines.append(line)
            elif any(pattern in line for pattern in ['function', '() {', 'if ', 'for ', 'while ']):
                break

        metadata = ChunkMetadata(
            chunk_id=f"{Path(filepath).stem}_shell_module",
            source_file=filepath,
            chunk_type="module",
            chunk_level=3,
            key_concepts=self._extract_key_concepts('\n'.join(header_lines), Path(filepath).stem)
        )

        return {
            'content': f"Shell Script: {Path(filepath).name}\n\n" + '\n'.join(header_lines),
            'metadata': asdict(metadata)
        }

    # Python helper methods (preserved from original)
    def _extract_function_calls(self, node: ast.FunctionDef) -> Set[str]:
        """Extract all function calls within a Python function"""
        calls = set()
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    calls.add(child.func.id)
                elif isinstance(child.func, ast.Attribute):
                    calls.add(child.func.attr)
        return calls

    def _extract_exceptions(self, node: ast.FunctionDef) -> List[str]:
        """Extract exception types handled in Python function"""
        exceptions = []
        for child in ast.walk(node):
            if isinstance(child, ast.ExceptHandler):
                if child.type:
                    if isinstance(child.type, ast.Name):
                        exceptions.append(child.type.id)
        return exceptions

    def _extract_global_usage(self, node: ast.FunctionDef) -> Set[str]:
        """Extract global variables used in Python function"""
        globals_used = set()
        for child in ast.walk(node):
            if isinstance(child, ast.Global):
                globals_used.update(child.names)
        return globals_used

    def _get_function_signature(self, node: ast.FunctionDef, content: str) -> str:
        """Extract Python function signature as string"""
        lines = content.split('\n')
        sig_lines = []

        current_line = node.lineno - 1

        while current_line < len(lines):
            line = lines[current_line]
            sig_lines.append(line.strip())
            if ')' in line and ':' in line:
                break
            current_line += 1

        return ' '.join(sig_lines)

    def _extract_function_comments(self, node: ast.FunctionDef, content: str) -> List[str]:
        """Extract inline comments from Python function body"""
        comments = []
        lines = content.split('\n')[node.lineno:node.end_lineno]

        for line in lines:
            if '#' in line:
                comment_start = line.find('#')
                comment = line[comment_start:].strip()
                if comment and not comment.startswith('#####'):
                    comments.append(comment)

        return comments

    def _extract_handled_commands(self, node: ast.FunctionDef, content: str) -> List[str]:
        """Extract commands handled by Python function"""
        commands = []

        func_lines = content.split('\n')[node.lineno - 1:node.end_lineno]
        func_text = '\n'.join(func_lines)

        patterns = [
            r"['\"](\$[A-Z\-]+)['\"]",
            r"command\s*==\s*['\"]([A-Z\-]+)['\"]",
            r"\.send\(['\"]([A-Z\-]+\s+[^'\"]*)['\"]",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, func_text)
            commands.extend(matches)

        return list(set(commands))

    def _extract_hardware_components(self, node: ast.FunctionDef, content: str) -> List[str]:
        """Extract hardware components mentioned in Python function"""
        func_lines = content.split('\n')[node.lineno - 1:node.end_lineno]
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
        """Determine operational context from Python function content and name"""
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

    def _extract_imports(self, tree: ast.AST) -> Dict[str, List[str]]:
        """Extract all imports from Python module"""
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
        """Create module-level chunk for Python file with imports and globals"""

        module_docstring = ast.get_docstring(tree)
        imports = self._extract_imports(tree)

        globals_defined = []
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        globals_defined.append(target.id)

        import_lines = []
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith(('import ', 'from ')):
                import_lines.append(line)
            elif line.strip() and not line.strip().startswith('#'):
                if i > 10:
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

    def _analyze_class(self, node: ast.ClassDef, filepath: str,
                       full_content: str, imports: Dict) -> List[Dict]:
        """Analyze a Python class and its methods"""
        chunks = []

        class_id = f"{Path(filepath).stem}_{node.name}_class"
        class_docstring = ast.get_docstring(node)

        class_start = node.lineno - 1
        first_method_line = min([m.lineno for m in node.body
                                 if isinstance(m, ast.FunctionDef)],
                                default=node.end_lineno)
        class_def_lines = full_content.split('\n')[class_start:first_method_line - 1]
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

        method_ids = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_chunk = self._analyze_function(item, filepath, full_content, imports)
                method_chunk['metadata']['parent_chunk_id'] = class_id
                method_chunk['metadata']['chunk_type'] = 'method'
                method_ids.append(method_chunk['metadata']['chunk_id'])
                chunks.append(method_chunk)

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
    # def _extract_command_handlers(self, content: str, filepath: str) -> List[Dict]:
    #     """Extract command handling patterns from Python code"""
    #     chunks = []
    #
    #     command_pattern = r"if\s+.*?\.upper\(\)\s*==\s*['\"](\$?[A-Z\-]+)['\"]:(.*?)(?=(?:elif|else:|if\s+.*?\.upper\(\)|$))"
    #
    #     matches = re.finditer(command_pattern, content, re.DOTALL | re.MULTILINE)
    #
    #     for match in matches:
    #         command = match.group(1)
    #         handler_code = match.group(2)
    #
    #         chunk_id = f"{Path(filepath).stem}_cmd_{command.replace('_file=filepath,
    #         chunk_type="generic",
    #         chunk_level = 3,
    #         key_concepts = self._extract_key_concepts(content[:1000], Path(filepath).stem)
    #         )
    #
    #         return [{
    #             'content': content,
    #             'metadata': asdict(metadata)
    #         }]

        # Helper methods for all languages
    def _extract_key_concepts(self, content: str, name: str) -> List[str]:
        """Extract key concepts from content"""
        concepts = []

        # Add name variants
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

    def process_code_directory_enhanced(self, code_dir: str) -> List[Dict]:
        """Enhanced code processing with multi-language support"""

        all_chunks = []
        code_path = Path(code_dir)

        # Supported extensions
        supported_extensions = [
            '.py',  # Python
            '.f', '.f77', '.f90', '.f95', '.f03', '.for',  # Fortran
            '.c', '.h',  # C
            '.cpp', '.cxx', '.cc', '.hpp', '.hxx', '.hh',  # C++
            '.sh', '.bash', '.csh', '.ksh', '.zsh'  # Shell
        ]

        # Find all supported code files
        code_files = []
        for ext in supported_extensions:
            code_files.extend(code_path.rglob(f"*{ext}"))

        print(f"🔍 Found {len(code_files)} code files with multi-language support")

        # Analyze each file
        for code_file in code_files:
            try:
                file_chunks = self.analyze_file(str(code_file))
                all_chunks.extend(file_chunks)

                if len(file_chunks) > 0:
                    print(f"   ✅ {code_file.name}: {len(file_chunks)} chunks")

            except Exception as e:
                print(f"   ❌ Error processing {code_file.name}: {e}")
                continue

        print(f"📊 Total chunks extracted: {len(all_chunks)}")

        # Analyze language distribution
        language_stats = {}
        for chunk in all_chunks:
            source_file = chunk['metadata']['source_file']
            language = self.get_file_language(source_file)
            language_stats[language] = language_stats.get(language, 0) + 1

        print(f"📈 Language distribution:")
        for lang, count in sorted(language_stats.items()):
            print(f"   {lang}: {count} chunks")

        return all_chunks

    # Python-specific methods (preserved from original)
    def _analyze_function(self, node: ast.FunctionDef, filepath: str,
                          full_content: str, imports: Dict) -> Dict:
        """Detailed Python function analysis"""

        chunk_id = f"{Path(filepath).stem}_{node.name}_{node.lineno}"
        docstring = ast.get_docstring(node)
        signature = self._get_function_signature(node, full_content)
        comments = self._extract_function_comments(node, full_content)
        calls = self._extract_function_calls(node)
        exceptions = self._extract_exceptions(node)
        globals_used = self._extract_global_usage(node)
        commands = self._extract_handled_commands(node, full_content)
        hardware = self._extract_hardware_components(node, full_content)

        func_lines = full_content.split('\n')[node.lineno - 1:node.end_lineno]
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
            'ast_node': node
        }

    # Fortran-specific methods
    def _detect_fortran_construct(self, line: str, line_num: int) -> Optional[Dict]:
        """Detect Fortran language constructs"""
        line_clean = line.strip().lower()
        patterns = self.language_patterns['fortran']

        for construct_type, pattern in [
            ('subroutine', patterns['subroutine']),
            ('function', patterns['function']),
            ('module', patterns['module']),
            ('program', patterns['program'])
        ]:
            match = re.match(pattern, line_clean)
            if match:
                return {'type': construct_type, 'name': match.group(1), 'line': line_num}

        return None

    def _is_fortran_comment(self, line: str) -> bool:
        """Check if line is a Fortran comment"""
        line_clean = line.strip()
        return (line_clean.startswith('!') or
                line_clean.startswith('c') or
                line_clean.startswith('C') or
                line_clean.startswith('*'))

    def _is_fortran_end(self, line: str, construct_type: str) -> bool:
        """Check if line ends a Fortran construct"""
        line_clean = line.strip().lower()

        if re.match(r'^\s*end\s*$', line_clean):
            return True

        specific_ends = {
            'subroutine': r'^\s*end\s+subroutine',
            'function': r'^\s*end\s+function',
            'module': r'^\s*end\s+module',
            'program': r'^\s*end\s+program'
        }

        if construct_type in specific_ends:
            return bool(re.match(specific_ends[construct_type], line_clean))

        return False

    def _create_fortran_construct_chunk(self, construct: Dict, lines: List[str],
                                        filepath: str, start_line: int) -> Dict:
        """Create chunk for Fortran construct"""

        content = '\n'.join(lines)
        construct_name = construct['name']
        construct_type = construct['type']

        chunk_id = f"{Path(filepath).stem}_{construct_type}_{construct_name}_{start_line}"

        metadata = ChunkMetadata(
            chunk_id=chunk_id,
            source_file=filepath,
            chunk_type=construct_type,
            chunk_level=1,
            function_signature=f"{construct_type} {construct_name}",
            key_concepts=self._extract_key_concepts(content, construct_name),
            operational_context=self._determine_fortran_context(content, construct_name)
        )

        return {
            'content': content,
            'metadata': asdict(metadata)
        }

    def _determine_fortran_context(self, content: str, name: str) -> str:
        """Determine operational context for Fortran code"""
        content_lower = content.lower()
        name_lower = name.lower()

        contexts = {
            'calibration': ['calib', 'gain', 'phase', 'amplitude', 'flux'],
            'tracking': ['track', 'point', 'position', 'coordinate', 'ra', 'dec'],
            'observation': ['observe', 'scan', 'data', 'record', 'acquire'],
            'processing': ['process', 'reduce', 'filter', 'transform', 'fft'],
            'control': ['control', 'command', 'move', 'set', 'init'],
            'analysis': ['analyze', 'compute', 'calculate', 'solve', 'fit']
        }

        for context, keywords in contexts.items():
            if any(keyword in name_lower or keyword in content_lower for keyword in keywords):
                return context

        return 'general'

    def _create_fortran_module_chunk(self, filepath: str, content: str) -> Dict:
        """Create module-level chunk for Fortran file"""

        header_lines = []
        for i, line in enumerate(content.split('\n')):
            if i > 50:
                break
            if (self._is_fortran_comment(line) or
                    'include' in line.lower() or
                    'use' in line.lower() or
                    not line.strip()):
                header_lines.append(line)
            elif any(pattern in line.lower() for pattern in ['subroutine', 'function', 'program', 'module']):
                break

        metadata = ChunkMetadata(
            chunk_id=f"{Path(filepath).stem}_fortran_module",
            source_file=filepath,
            chunk_type="module",
            chunk_level=3,
            key_concepts=self._extract_key_concepts('\n'.join(header_lines), Path(filepath).stem)
        )

        return {
            'content': f"Fortran Module: {Path(filepath).name}\n\n" + '\n'.join(header_lines),
            'metadata': asdict(metadata)
        }

    # C/C++ specific methods
    def _extract_c_functions(self, filepath: str, content: str, language: str) -> List[Dict]:
        """Extract C/C++ functions"""
        chunks = []
        lines = content.split('\n')
        patterns = self.language_patterns['c'] if language == 'c' else self.language_patterns['cpp']

        in_function = False
        brace_count = 0
        current_function = None
        function_lines = []

        for i, line in enumerate(lines):
            if line.strip().startswith('#') or not line.strip():
                if in_function:
                    function_lines.append(line)
                continue

            func_match = re.search(patterns['function'], line)
            if func_match and not in_function:
                current_function = func_match.group(1)
                function_lines = [line]
                in_function = True
                brace_count = line.count('{') - line.count('}')
            elif in_function:
                function_lines.append(line)
                brace_count += line.count('{') - line.count('}')

                if brace_count <= 0:
                    chunk = self._create_c_function_chunk(
                        current_function, function_lines, filepath, i - len(function_lines) + 1, language
                    )
                    chunks.append(chunk)
                    in_function = False
                    current_function = None
                    function_lines = []

        return chunks

    def _create_c_function_chunk(self, func_name: str, lines: List[str],
                                 filepath: str, start_line: int, language: str) -> Dict:
        """Create chunk for C/C++ function"""

        content = '\n'.join(lines)
        chunk_id = f"{Path(filepath).stem}_{language}_func_{func_name}_{start_line}"

        metadata = ChunkMetadata(
            chunk_id=chunk_id,
            source_file=filepath,
            chunk_type="function",
            chunk_level=1,
            function_signature=lines[0].strip() if lines else f"{func_name}()",
            key_concepts=self._extract_key_concepts(content, func_name),
            operational_context=self._determine_c_context(content, func_name)
        )

        return {
            'content': content,
            'metadata': asdict(metadata)
        }

    def _determine_c_context(self, content: str, name: str) -> str:
        """Determine operational context for C/C++ code"""
        content_lower = content.lower()
        name_lower = name.lower()

        contexts = {
            'hardware_control': ['gpio', 'i2c', 'spi', 'serial', 'motor', 'sensor'],
            'data_processing': ['fft', 'filter', 'process', 'analyze', 'compute'],
            'communication': ['socket', 'tcp', 'udp', 'send', 'receive'],
            'calibration': ['calib', 'gain', 'offset', 'correct'],
            'timing': ['timer', 'clock', 'delay', 'wait', 'time']
        }

        for context, keywords in contexts.items():
            if any(keyword in name_lower or keyword in content_lower for keyword in keywords):
                return context

        return 'general'

    def _create_c_module_chunk(self, filepath: str, content: str, language: str) -> Dict:
        """Create module-level chunk for C/C++ file"""

        header_lines = []
        for i, line in enumerate(content.split('\n')):
            if i > 100:
                break
            if (line.strip().startswith('//') or
                    line.strip().startswith('/*') or
                    '#include' in line or
                    '#define' in line or
                    not line.strip()):
                header_lines.append(line)
            elif any(pattern in line for pattern in ['{', 'int main', 'void main']):
                break

        metadata = ChunkMetadata(
            chunk_id=f"{Path(filepath).stem}_{language}_module",
            source_file=filepath,
            chunk_type="module",
            chunk_level=3,
            key_concepts=self._extract_key_concepts('\n'.join(header_lines), Path(filepath).stem)
        )

        return {
            'content': f"{language.upper()} Module: {Path(filepath).name}\n\n" + '\n'.join(header_lines),
            'metadata': asdict(metadata)
        }

    # Shell specific methods
    def _extract_shell_functions(self, filepath: str, content: str) -> List[Dict]:
        """Extract shell script functions"""
        chunks = []
        lines = content.split('\n')
        patterns = self.language_patterns['shell']

        in_function = False
        brace_count = 0
        current_function = None
        function_lines = []

        for i, line in enumerate(lines):
            if re.match(patterns['comment'], line) or not line.strip():
                if in_function:
                    function_lines.append(line)
                continue

            func_match = re.search(patterns['function'], line)
            func_alt_match = re.search(patterns['function_alt'], line)

            if (func_match or func_alt_match) and not in_function:
                current_function = func_match.group(1) if func_match else func_alt_match.group(1)
                function_lines = [line]
                in_function = True
                brace_count = line.count('{') - line.count('}')
            elif in_function:
                function_lines.append(line)
                brace_count += line.count('{') - line.count('}')

                if brace_count <= 0 and '}' in line:
                    chunk = self._create_shell_function_chunk(
                        current_function, function_lines, filepath, i - len(function_lines) + 1
                    )
                    chunks.append(chunk)
                    in_function = False
                    current_function = None
                    function_lines = []

        return chunks

    def _create_shell_function_chunk(self, func_name: str, lines: List[str],
                                     filepath: str, start_line: int) -> Dict:
        """Create chunk for shell function"""

        content = '\n'.join(lines)

        # Extract shell metadata
        commands = self._extract_shell_commands(lines)
        variables = self._extract_shell_vars_in_function(lines)

        chunk_id = f"{Path(filepath).stem}_shell_func_{func_name}_{start_line}"

        metadata = ChunkMetadata(
            chunk_id=chunk_id,
            source_file=filepath,
            chunk_type="function",
            chunk_level=1,
            function_signature=f"function {func_name}()",
            commands_handled=commands,
            global_vars_accessed=variables,
            key_concepts=self._extract_key_concepts(content, func_name),
            operational_context=self._determine_shell_context(content, func_name)
        )

        return {
            'content': content,
            'metadata': asdict(metadata)
        }

    def _extract_command_handlers(self, content: str, filepath: str) -> List[Dict]:
        """Extract command handling patterns from Python code"""
        chunks = []

        command_pattern = r"if\s+.*?\.upper\(\)\s*==\s*['\"](\$?[A-Z\-]+)['\"]:(.*?)(?=(?:elif|else:|if\s+.*?\.upper\(\)|$))"

        matches = re.finditer(command_pattern, content, re.DOTALL | re.MULTILINE)

        for match in matches:
            command = match.group(1)
            handler_code = match.group(2)

            chunk_id = f"{Path(filepath).stem}_cmd_{command.replace('$', 'DOLLAR')}"

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


    def _fallback_text_analysis(self, filepath: str, content: str) -> List[Dict]:
        """Fallback analysis when Python AST parsing fails"""
        chunks = []

        func_pattern = r'^def\s+(\w+)\s*\([^)]*\):\s*\n((?:\s{4,}.*\n)*)'

        for match in re.finditer(func_pattern, content, re.MULTILINE):
            func_name = match.group(1)
            func_body = match.group(0)

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





class EnhancedDocumentProcessor:
    """Main processor class that orchestrates all analyzers with multi-language support"""

    def __init__(self, use_ai: bool = True, cost_limit: float = 10.0):
        self.code_analyzer = MultiLanguageCodeAnalyzer()  # Updated to use multi-language analyzer
        self.wiki_analyzer = WikiAnalyzer()

        self.use_ai = use_ai
        self.cost_limit = cost_limit

        if use_ai:
            try:
                from ai_enhanced_processor import AIEnhancer
                self.ai_enhancer = AIEnhancer()
            except ImportError:
                print("⚠️  AI enhancement not available")
                self.ai_enhancer = None
        else:
            self.ai_enhancer = None

    def process_directory(self, data_dir: str) -> List[Dict]:
        """Process all files in a directory with multi-language support"""

        all_chunks = []
        data_path = Path(data_dir)

        print(f"🔍 Processing directory with multi-language support: {data_dir}")

        # Process code files with multi-language support
        if (data_path / "code").exists():
            print("💻 Processing multi-language codebase...")
            code_chunks = self.code_analyzer.process_code_directory_enhanced(str(data_path / "code"))
            all_chunks.extend(code_chunks)
            print(f"✅ Added {len(code_chunks)} multi-language code chunks")

        # Process documentation files
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

        # AI enhancement (if enabled)
        if self.use_ai and self.ai_enhancer:
            print(f"🤖 Enhancing chunks with AI (cost limit: ${self.cost_limit})")
            enhanced_count = 0

            for i, chunk in enumerate(all_chunks):
                if hasattr(self.ai_enhancer, 'cost_tracker') and self.ai_enhancer.cost_tracker > self.cost_limit:
                    print(f"💰 Cost limit reached (${self.cost_limit}), stopping AI enhancement")
                    break

                if i % 10 == 0:
                    cost = getattr(self.ai_enhancer, 'cost_tracker', 0)
                    print(f"  Enhanced {i}/{len(all_chunks)} chunks (cost: ${cost:.2f})")

                try:
                    enhanced_chunk = self.ai_enhancer.enhance_chunk(chunk)
                    all_chunks[i] = enhanced_chunk
                    enhanced_count += 1
                except:
                    # Continue without AI enhancement for this chunk
                    continue

            print(f"🤖 Enhanced {enhanced_count} chunks with AI")

        # Build cross-references between chunks
        print("🔗 Building cross-references...")
        self._build_cross_references(all_chunks)

        # Generate summary statistics
        self._print_statistics(all_chunks)

        return all_chunks

    def process_existing_documents(self, input_file: str) -> List[Dict]:
        """Process existing processed documents with multi-language support"""

        print(f"📂 Loading existing documents from {input_file}")

        with open(input_file, 'r', encoding='utf-8') as f:
            documents = json.load(f)

        all_chunks = []

        for doc in documents:
            if doc.get('type') == 'source_code':
                # Re-process code with enhanced multi-language analysis
                print(f"  Re-analyzing code: {doc.get('title', 'Unknown')}")
                try:
                    # Determine language and reprocess
                    source_path = doc['source']
                    language = self.code_analyzer.get_file_language(source_path)

                    if language != 'unknown':
                        # Create temporary file content for analysis
                        temp_chunks = self.code_analyzer._analyze_content_by_language(
                            doc['content'], source_path, language
                        )
                        all_chunks.extend(temp_chunks)
                    else:
                        # Keep as generic chunk
                        all_chunks.append(self._convert_legacy_chunk(doc))

                except Exception as e:
                    print(f"  ❌ Error re-processing {doc.get('title')}: {e}")
                    all_chunks.append(self._convert_legacy_chunk(doc))
            else:
                # Convert existing document to new chunk format
                all_chunks.append(self._convert_legacy_chunk(doc))

        # Build cross-references and AI enhancement
        print("🔗 Building cross-references...")
        self._build_cross_references(all_chunks)

        if self.use_ai and self.ai_enhancer:
            print(f"🤖 Enhancing chunks with AI...")
            for i, chunk in enumerate(all_chunks):
                if hasattr(self.ai_enhancer, 'cost_tracker') and self.ai_enhancer.cost_tracker > self.cost_limit:
                    break
                try:
                    all_chunks[i] = self.ai_enhancer.enhance_chunk(chunk)
                except:
                    continue

        self._print_statistics(all_chunks)

        return all_chunks

    def _convert_legacy_chunk(self, doc: Dict) -> Dict:
        """Convert legacy document format to new chunk format"""

        chunk_id = f"legacy_{hashlib.md5(doc['source'].encode()).hexdigest()[:8]}"

        metadata = ChunkMetadata(
            chunk_id=chunk_id,
            source_file=doc['source'],
            chunk_type=doc.get('type', 'general'),
            chunk_level=2,
            key_concepts=doc.get('metadata', {}).get('key_concepts', [])
        )

        return {
            'content': doc['content'],
            'metadata': asdict(metadata)
        }

    def _build_cross_references(self, chunks: List[Dict]):
        """Build cross-references between chunks across all languages"""

        # Build indices for cross-referencing
        function_index = defaultdict(list)  # function_name -> [chunk_ids]
        command_index = defaultdict(list)  # command -> [chunk_ids]
        concept_index = defaultdict(list)  # concept -> [chunk_ids]

        for chunk in chunks:
            metadata = chunk['metadata']
            chunk_id = metadata['chunk_id']

            # Index by function names
            if metadata['chunk_type'] in ['function', 'subroutine', 'method']:
                func_name = self._extract_function_name_from_id(chunk_id)
                if func_name:
                    function_index[func_name].append(chunk_id)

            # Index by commands
            for command in metadata.get('commands_handled', []):
                command_index[command.lower()].append(chunk_id)

            # Index by concepts
            for concept in metadata.get('key_concepts', []):
                concept_index[concept.lower()].append(chunk_id)

        # Build cross-references
        for chunk in chunks:
            metadata = chunk['metadata']
            chunk_id = metadata['chunk_id']
            related_chunks = set()

            # Find related chunks by function calls
            for called_func in metadata.get('functions_called', []):
                if called_func.lower() in function_index:
                    related_chunks.update(function_index[called_func.lower()])

            # Find related chunks by shared commands
            for command in metadata.get('commands_handled', []):
                if command.lower() in command_index:
                    related_chunks.update(command_index[command.lower()])

            # Find related chunks by shared concepts
            for concept in metadata.get('key_concepts', []):
                if concept.lower() in concept_index:
                    # Only add if significant overlap (avoid too many loose connections)
                    concept_chunks = concept_index[concept.lower()]
                    if len(concept_chunks) <= 10:  # Avoid very common concepts
                        related_chunks.update(concept_chunks)

            # Remove self-reference
            related_chunks.discard(chunk_id)

            # Update metadata with cross-references
            if related_chunks:
                existing_related = set(metadata.get('related_code_chunks', []))
                metadata['related_code_chunks'] = list(existing_related.union(related_chunks))

        print(f"🔗 Built cross-references for {len(chunks)} chunks")

    def _extract_function_name_from_id(self, chunk_id: str) -> Optional[str]:
        """Extract function name from chunk ID"""
        parts = chunk_id.split('_')
        if len(parts) >= 3:
            # Format: filename_language_func_name_line or filename_type_name_line
            if 'func' in parts:
                func_idx = parts.index('func')
                if func_idx + 1 < len(parts):
                    return parts[func_idx + 1]
            elif len(parts) >= 2 and not parts[1].isdigit():
                return parts[1]
        return None

    def save_processed_chunks(self, chunks: List[Dict], output_file: str):
        """Save processed chunks to file"""

        # Convert chunks to serializable format
        serializable_chunks = []
        for chunk in chunks:
            # Remove non-serializable items
            clean_chunk = {
                'content': chunk['content'],
                'metadata': {k: v for k, v in chunk['metadata'].items()
                             if k not in ['ast_node']}  # Remove AST nodes and other non-serializable items
            }
            serializable_chunks.append(clean_chunk)

        # Save to file
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(serializable_chunks, f, indent=2, ensure_ascii=False)

        print(f"💾 Saved {len(serializable_chunks)} processed chunks to {output_file}")

    def _print_statistics(self, chunks: List[Dict]):
        """Print processing statistics with language breakdown"""

        print("\n" + "=" * 60)
        print("📊 MULTI-LANGUAGE PROCESSING STATISTICS")
        print("=" * 60)

        total_chunks = len(chunks)
        print(f"Total chunks: {total_chunks}")

        # Count by type and language
        type_counts = defaultdict(int)
        language_counts = defaultdict(int)
        context_counts = defaultdict(int)

        for chunk in chunks:
            metadata = chunk['metadata']
            type_counts[metadata['chunk_type']] += 1

            # Determine language from source file
            source_file = metadata['source_file']
            if source_file:
                language = self.code_analyzer.get_file_language(source_file)
                language_counts[language] += 1

            # Count operational contexts
            context = metadata.get('operational_context', 'unknown')
            if context:
                context_counts[context] += 1

        print("\nChunk Types:")
        for chunk_type, count in sorted(type_counts.items()):
            print(f"  {chunk_type}: {count}")

        print("\nLanguage Distribution:")
        for language, count in sorted(language_counts.items()):
            if language != 'unknown':
                print(f"  {language}: {count}")

        print("\nOperational Contexts:")
        for context, count in sorted(context_counts.items()):
            if context != 'unknown':
                print(f"  {context}: {count}")

        # Count cross-references
        cross_refs = sum(1 for chunk in chunks
                         if chunk['metadata'].get('related_code_chunks'))

        print(f"\nChunks with cross-references: {cross_refs}")

        # Count AI enhancements
        ai_enhanced = sum(1 for chunk in chunks
                          if chunk['metadata'].get('ai_summary'))

        print(f"AI-enhanced chunks: {ai_enhanced}")
        print("=" * 60)




def main():
    """Test the enhanced multi-language processor"""

    import argparse

    parser = argparse.ArgumentParser(description='Enhanced Multi-Language Radio Telescope Document Processor')
    parser.add_argument('--input-dir', required=True, help='Input directory or existing JSON file')
    parser.add_argument('--output', default='data/processed/multilang_enhanced_chunks.json',
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

    print(f"\n✅ Multi-language processing complete!")
    print(f"📁 Enhanced chunks saved to: {args.output}")
    print(f"🔍 Ready for advanced multi-language RAG retrieval!")


if __name__ == "__main__":
    main()