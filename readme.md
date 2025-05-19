CodeSampleGen

A Python script to generate question-answer pairs from Python code functions in a local repository using a StarCoder GGUF model and Tree-sitter for parsing.

Overview

This script processes Python files in a specified repository (e.g., [USER_HOME]/Documents/flask), extracts function definitions using Tree-sitter, and generates question-answer pairs using a locally stored StarCoder GGUF model (e.g., [USER_HOME]/models/starcoder-q5_K_M.gguf). The output is saved as a JSON file in a designated directory (e.g., [USER_HOME]/Documents/output_data/qa_pairs.json).

Requirements





Python: 3.10 or higher



Dependencies:





llama-cpp-python>=0.3.8



tree-sitter>=0.20.0



tree-sitter-python



pandas



Model File: StarCoder GGUF model (e.g., starcoder-q5_K_M.gguf, downloadable from Hugging Face TheBloke/StarCoder-GGUF)



Repository: A local Git repository with Python files (e.g., Flask)

Installation





Install Python 3.10: Ensure Python 3.10 is installed. Download from python.org.



Set up a virtual environment (recommended):

python -m venv [USER_HOME]/.venv
[USER_HOME]/.venv/Scripts/Activate.ps1  # Windows



Install dependencies:

pip install tree-sitter tree-sitter-python pandas llama-cpp-python



Download the StarCoder GGUF model:





Download starcoder-q5_K_M.gguf from Hugging Face TheBloke/StarCoder-GGUF.



Save it to [USER_HOME]/models/starcoder-q5_K_M.gguf.



Prepare the repository:





Clone or ensure a local repository exists (e.g., [USER_HOME]/Documents/flask):

cd [USER_HOME]/Documents
git clone https://github.com/pallets/flask.git

Usage





Update configuration (if needed): Edit codeSampleGen.py to set:





REPO_PATH: Path to your repository (default: [USER_HOME]/Documents/flask)



OUTPUT_PATH: Output directory (default: [USER_HOME]/Documents/output_data)



MODEL_PATH: Path to the GGUF model (default: [USER_HOME]/models/starcoder-q5_K_M.gguf)



FILE_EXTENSION: File type to process (default: .py)



Run the script:

python [USER_HOME]/.ssh/codeSampleGen.py

Or, if using the full Python path:

C:/Users/[USER]/AppData/Local/Programs/Python/Python310/python.exe [USER_HOME]/.ssh/codeSampleGen.py



Output:





QA pairs are saved as [USER_HOME]/Documents/output_data/qa_pairs.json.



Example entry:

{
  "question": "What is the purpose of the route function in Flask?",
  "answer": "The route function defines a URL pattern and associates it with a view function.",
  "code_snippet": "def route(self, rule, **options):\n    ...",
  "reasoning": "Generated from function route in src/flask/app.py using StarCoder GGUF.",
  "file": "src/flask/app.py",
  "repo": "flask"
}

Troubleshooting





Model not found:





Verify the GGUF file exists:

dir [USER_HOME]/models/starcoder-q5_K_M.gguf



Re-download from Hugging Face if missing.



Dependency errors:





Ensure all dependencies are installed:

pip list



Reinstall:

pip install tree-sitter tree-sitter-python pandas llama-cpp-python --force-reinstall



No QA pairs generated:





Confirm the repository contains Python files with functions:

dir [USER_HOME]/Documents/flask -Recurse -Include *.py



Try a different repository (e.g., requests):

cd [USER_HOME]/Documents
git clone https://github.com/kennethreitz/requests.git



Memory issues:





Ensure at least 4-8GB of free RAM:

systeminfo | findstr "Available Physical Memory"



Close other applications.

Contributing

Feel free to submit issues or pull requests to improve the script, such as adding support for other programming languages or optimizing model inference.

License

MIT License
