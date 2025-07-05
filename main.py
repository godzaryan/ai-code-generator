from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import json
import re

app = Flask(__name__)
CORS(app)

API_KEY = "YOUR_GEMINI_API_KEY"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-2.0-flash')

def guess_file_info(language):
    lang_map = {
        "python": (".py", "script.py"),
        "javascript": (".js", "script.js"),
        "html": (".html", "index.html"),
        "css": (".css", "style.css"),
        "java": (".java", "Main.java"),
        "c++": (".cpp", "main.cpp"),
        "c#": (".cs", "Program.cs"),
        "go": (".go", "main.go"),
        "ruby": (".rb", "script.rb"),
        "php": (".php", "index.php"),
        "swift": (".swift", "main.swift"),
        "kotlin": (".kt", "main.kt"),
        "typescript": (".ts", "script.ts"),
        "json": (".json", "data.json"),
        "text": (".txt", "output.txt"),
        "markdown": (".md", "README.md")
    }
    ext, default_name = lang_map.get(language.lower(), (".txt", "untitled.txt"))
    return ext, default_name

@app.route('/')
def home():
    return "Backend is running. Open index.html in your browser."

@app.route('/generate-code', methods=['POST'])
def generate_code():
    try:
        data = request.get_json()
        prompt = data.get('prompt')

        if not prompt:
            return jsonify({"error": "Prompt is missing"}), 400

        full_prompt = f"""Generate code based on the following request: "{prompt}"

        If the request implies multiple distinct files (e.g., frontend and backend, or multiple classes),
        generate separate code blocks for each file.
        For each code block, identify its language and suggest a valid, descriptive filename.

        Your response should be a single JSON object with two main keys:
        'files': An array of objects, where each object represents a file and has the following keys:
            'code': The generated code content for this specific file (string).
            'language': The programming language of this file (e.g., 'python', 'javascript', 'html', 'css').
            'suggested_filename': A valid and descriptive filename for this file (e.g., 'main.py', 'index.html', 'style.css').
        'overall_details': An object containing aggregated details about the entire solution. This object should have the following keys:
            'language': The primary or predominant programming language(s) of the solution (e.g., 'Python & HTML', 'JavaScript').
            'lines': The approximate total number of lines across all generated code files (integer).
            'complexity': The common time complexity of the most significant part of the solution (e.g., 'O(1)', 'O(n)', 'O(n log n)', 'O(n^2)').
            'space_complexity': The common space complexity (e.g., 'O(1)', 'O(n)').
            'purpose': A concise explanation of what the entire solution does and its main goal.
            'dependencies': A list of required libraries or frameworks for the overall solution (e.g., ['Flask', 'React']). Return an empty list if none.
            'file_extension': A representative file extension or 'Mixed' if multiple (e.g., '.py', '.html', 'Mixed').
            'input_output_examples': A string providing simple input/output examples for the overall solution, clearly formatted.
            'usage_instructions': A string with brief instructions on how to set up and run the entire solution, including any setup steps.
            'num_functions_classes': The total number of distinct functions or classes defined across all files (integer).
            'error_handling_details': A string describing any error handling implemented or recommended for the overall solution.
            'assumptions': A string outlining any assumptions the solution makes about its environment or input.
            'best_practices_followed': Boolean, true if common best practices are visibly followed across the solution, false otherwise.
            'target_environment': The environment where the solution is intended to run (e.g., 'Web Browser & Server', 'Python 3.x CLI').

        Ensure the JSON is perfectly formed and escaped if necessary.
        """

        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
                response_schema={
                    "type": "OBJECT",
                    "properties": {
                        "files": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "code": {"type": "STRING"},
                                    "language": {"type": "STRING"},
                                    "suggested_filename": {"type": "STRING"}
                                },
                                "required": ["code", "language", "suggested_filename"]
                            }
                        },
                        "overall_details": {
                            "type": "OBJECT",
                            "properties": {
                                "language": {"type": "STRING"},
                                "lines": {"type": "NUMBER"},
                                "complexity": {"type": "STRING"},
                                "space_complexity": {"type": "STRING"},
                                "purpose": {"type": "STRING"},
                                "dependencies": {"type": "ARRAY", "items": {"type": "STRING"}},
                                "file_extension": {"type": "STRING"},
                                "input_output_examples": {"type": "STRING"},
                                "usage_instructions": {"type": "STRING"},
                                "num_functions_classes": {"type": "NUMBER"},
                                "error_handling_details": {"type": "STRING"},
                                "assumptions": {"type": "STRING"},
                                "best_practices_followed": {"type": "BOOLEAN"},
                                "target_environment": {"type": "STRING"}
                            },
                            "required": [
                                "language", "lines", "complexity", "space_complexity", "purpose",
                                "dependencies", "file_extension", "input_output_examples",
                                "usage_instructions", "num_functions_classes", "error_handling_details",
                                "assumptions", "best_practices_followed", "target_environment"
                            ]
                        }
                    },
                    "required": ["files", "overall_details"]
                }
            )
        )

        raw_response_text = response.text
        cleaned_response_text = re.sub(r'```json\n|\n```', '', raw_response_text).strip()

        generated_data = json.loads(cleaned_response_text)

        total_lines = 0
        file_extensions_set = set()
        for file in generated_data.get('files', []):
            if 'code' in file and file['code']:
                file['lines'] = len(file['code'].strip().split('\n'))
                total_lines += file['lines']
            else:
                file['lines'] = 0

            if 'language' in file and not file.get('suggested_filename'):
                _, default_name = guess_file_info(file['language'])
                file['suggested_filename'] = default_name
            elif not file.get('suggested_filename'):
                file['suggested_filename'] = "untitled.txt"

            if file.get('file_extension'):
                file_extensions_set.add(file['file_extension'])
            elif file.get('language'):
                ext, _ = guess_file_info(file['language'])
                file_extensions_set.add(ext)

        generated_data['overall_details']['lines'] = total_lines

        if len(file_extensions_set) > 1:
            generated_data['overall_details']['file_extension'] = "Mixed"
        elif file_extensions_set:
            generated_data['overall_details']['file_extension'] = list(file_extensions_set)[0]
        else:
            generated_data['overall_details']['file_extension'] = "N/A"

        if not isinstance(generated_data['overall_details'].get('dependencies'), list):
            generated_data['overall_details']['dependencies'] = []

        return jsonify(generated_data)

    except json.JSONDecodeError as jde:
        print(f"JSON decoding error: {jde}")
        print(f"Raw response text that caused error: {response.text}")
        return jsonify({"error": f"Invalid JSON format from API. Please try again. Raw response: {response.text}"}), 500
    except Exception as e:
        print(f"Error generating code: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
