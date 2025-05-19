import os
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
from llama_cpp import Llama
from tree_sitter import Parser
from tree_sitter_python import language as python_language

# Configuration constants
REPO_PATH = "C:/Users/cym/Documents/flask"  # Local repository path
OUTPUT_PATH = "C:/Users/cym/Documents/output_data"  # Output directory for QA pairs
FILE_EXTENSION = ".py"  # File extension to process
MODEL_PATH = "C:/Users/cym/models/starcoder-q5_K_M.gguf"  # Path to GGUF model

def initialize_model(model_path: str, n_ctx: int = 2048) -> Llama:
    """Initialize the StarCoder GGUF model.
    
    Args:
        model_path: Path to the GGUF model file (e.g., [USER_HOME]/models/starcoder-q5_K_M.gguf)
        n_ctx: Context length for the model
    
    Returns:
        Llama: Initialized model instance
    
    Raises:
        FileNotFoundError: If model file does not exist
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at [USER_HOME]/models/starcoder-q5_K_M.gguf")
    return Llama(model_path=model_path, n_ctx=n_ctx)

def initialize_parser() -> Parser:
    """Initialize Tree-sitter parser for Python.
    
    Returns:
        Parser: Configured parser with Python language
    
    Raises:
        RuntimeError: If parser initialization fails
    """
    try:
        parser = Parser()
        PY_LANGUAGE = python_language()  # Get Python language object
        parser.set_language(PY_LANGUAGE)
        return parser
    except Exception as e:
        raise RuntimeError(f"Failed to initialize parser: {e}")

def extract_code(repo_path: str, file_extension: str) -> List[Dict[str, Any]]:
    """Extract Python code files from a local repository.
    
    Args:
        repo_path: Path to the repository (e.g., [USER_HOME]/Documents/flask)
        file_extension: File extension to filter (e.g., .py)
    
    Returns:
        List of dictionaries containing file path, content, and repo name
    
    Raises:
        ValueError: If repository path does not exist
    """
    code_files = []
    repo_path = Path(repo_path)
    
    if not repo_path.exists():
        raise ValueError(f"Repository path [USER_HOME]/Documents/flask does not exist")
    
    for file_path in repo_path.rglob(f"*{file_extension}"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
            code_files.append({
                "path": str(file_path.relative_to(repo_path)),
                "content": code,
                "repo": repo_path.name
            })
            print(f"Extracted file: [USER_HOME]/Documents/flask/{file_path.relative_to(repo_path)}")
        except Exception as e:
            print(f"Failed to read file {file_path.relative_to(repo_path)}: {e}")
    
    return code_files

def generate_qa_pairs(code_files: List[Dict[str, Any]], parser: Parser, model: Llama) -> List[Dict[str, Any]]:
    """Generate question-answer pairs for Python functions in code files.
    
    Args:
        code_files: List of code file dictionaries
        parser: Tree-sitter parser for Python
        model: StarCoder model for generating QA pairs
    
    Returns:
        List of dictionaries containing QA pairs and metadata
    """
    qa_pairs = []
    
    for file in code_files:
        try:
            tree = parser.parse(bytes(file["content"], "utf-8"))
            query = PY_LANGUAGE.query("""
                (function_definition
                    name: (identifier) @func_name)
            """)
            captures = query.captures(tree.root_node)
            
            for node, _ in captures:
                func_name = node.text.decode("utf-8")
                func_code = file["content"][node.start_byte:node.end_byte]
                prompt = (
                    f"Generate 3 questions and answers to help understand the functionality of this Python function:\n"
                    f"{func_code}\n\nFormat:\nQuestion: ...\nAnswer: ..."
                )
                try:
                    response = model(prompt, max_tokens=2048, temperature=0.7)["choices"][0]["text"]
                    lines = response.split('\n')
                    current_q = None
                    for line in lines:
                        if line.startswith("Question:"):
                            current_q = line.replace("Question:", "").strip()
                        elif line.startswith("Answer:"):
                            if current_q:
                                answer = line.replace("Answer:", "").strip()
                                qa_pairs.append({
                                    "question": current_q,
                                    "answer": answer,
                                    "code_snippet": func_code,
                                    "reasoning": f"Generated from function {func_name} in {file['path']} using StarCoder GGUF.",
                                    "file": file['path'],
                                    "repo": file['repo']
                                })
                                current_q = None
                except Exception as e:
                    print(f"Failed to generate QA for {file['path']}, function {func_name}: {e}")
        except Exception as e:
            print(f"Error processing file {file['path']}: {e}")
    
    return qa_pairs

def save_qa_pairs(qa_pairs: List[Dict[str, Any]], output_dir: str) -> None:
    """Save QA pairs to a JSON file.
    
    Args:
        qa_pairs: List of QA pair dictionaries
        output_dir: Directory to save the output (e.g., [USER_HOME]/Documents/output_data)
    """
    Path(output_dir).mkdir(exist_ok=True)
    output_file = os.path.join(output_dir, "qa_pairs.json")
    try:
        df = pd.DataFrame(qa_pairs)
        df.to_json(output_file, orient="records", lines=True, force_ascii=False)
        print(f"QA pairs saved to [USER_HOME]/Documents/output_data/qa_pairs.json")
    except Exception as e:
        print(f"Failed to save QA pairs to {output_file}: {e}")

def main() -> None:
    """Main function to generate and save QA pairs."""
    print("Starting QA pair generation...")
    
    try:
        # Initialize model and parser
        model = initialize_model(MODEL_PATH)
        parser = initialize_parser()
        
        # Extract code and generate QA pairs
        code_files = extract_code(REPO_PATH, FILE_EXTENSION)
        qa_pairs = generate_qa_pairs(code_files, parser, model)
        
        # Save results
        save_qa_pairs(qa_pairs, OUTPUT_PATH)
        print("QA pair generation completed.")
        
    except Exception as e:
        print(f"Error in main execution: {e}")
        raise

if __name__ == "__main__":
    main()
