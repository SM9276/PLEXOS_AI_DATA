import os
import ast
import pandas as pd
import ollama

# Define the directory containing Python files
directory = '/Users/sm9276/Plexos_AI/Extracted_Data'


def read_python_files(directory):
    code_snippets = {}
    for filename in os.listdir(directory):
        if filename.endswith('.py'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                code_snippets[filename] = file.read()
    return code_snippets


def generate_code_questions(code, filename):
    questions = []
    tree = ast.parse(code)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            docstring = ast.get_docstring(node)
            questions.append((f"In file `{filename}`, what is the purpose of the `{func_name}` function?", code))
            questions.append((
                             f"In file `{filename}`, what are the parameters of the `{func_name}` function, and what is each used for?",
                             code))
            questions.append((f"In file `{filename}`, what does the `{func_name}` function return?", code))

            if docstring:
                questions.append((
                                 f"In file `{filename}`, explain the docstring for the `{func_name}` function: \"{docstring}\"",
                                 code))

        elif isinstance(node, ast.ClassDef):
            class_name = node.name
            questions.append((f"In file `{filename}`, what is the purpose of the `{class_name}` class?", code))
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    func_name = item.name
                    questions.append((
                                     f"In file `{filename}`, what is the purpose of the `{func_name}` method in the `{class_name}` class?",
                                     code))
                    docstring = ast.get_docstring(item)
                    if docstring:
                        questions.append((
                                         f"In file `{filename}`, explain the docstring for the `{func_name}` method in the `{class_name}` class: \"{docstring}\"",
                                         code))

    return questions


def get_llm_answer(question, code):
    message = f"{question}\n\nCode:\n{code}\n\nAnswer:"
    response = ollama.chat(model='llama3.1', messages=[
        {'role': 'user', 'content': message},
    ])
    return response['message']['content']


def process_code_directory(directory):
    code_snippets = read_python_files(directory)
    qna_data = []

    for filename, code in code_snippets.items():
        print(f"Processing file: {filename}")
        questions = generate_code_questions(code, filename)
        for question, code_snippet in questions:
            answer = get_llm_answer(question, code_snippet)
            qna_data.append({
                'Filename': filename,
                'Prompt': question,
                'Code': code_snippet,
                'Answer': answer
            })

    return qna_data


def save_to_excel(data, file_path):
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)


# Main process
qna_data = process_code_directory(directory)
save_to_excel(qna_data, 'code_qna.xlsx')
print("Saved Q&A to 'code_qna.xlsx'")
