import json
import os
import ollama


# Function to read the text document
def read_text_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content


# Function to call the Ollama API for generating questions
def generate_questions(text, model='gemma2', num_questions=5):
    response = ollama.chat(model=model, messages=[
        {'role': 'user', 'content': f"Generate {num_questions} questions based on the following text: {text}"}
    ])

    questions_text = response['message']['content'].strip()
    print(questions_text)
    questions = questions_text.split('\n')

    return [q.strip() for q in questions if q.strip()]


# Function to call the Ollama API for generating answers
def generate_answer(question, text, model='gemma2'):
    response = ollama.chat(model=model, messages=[
        {'role': 'user',
         'content': f"Based on the following text, provide an answer to the question: '{question}'\n\nText: {text}"}
    ])

    answer_text = response['message']['content'].strip()
    print(answer_text)
    return answer_text


# Function to save the QA pairs to a JSONL file
def save_to_jsonl(output_folder, file_name, qa_pairs):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_file = os.path.join(output_folder, f"{file_name}_questions.jsonl")
    with open(output_file, 'w') as file:
        for qa_pair in qa_pairs:
            prompt = qa_pair['question']
            completion = qa_pair['answer']
            json_line = json.dumps({"prompt": prompt, "completion": completion})
            file.write(json_line + '\n')
    return output_file


# Main script
if __name__ == "__main__":
    input_folder = "/Users/sm9276/PycharmProjects/PLEXOS-Help-Data/Extracted_Data"  # Replace with your folder path
    output_folder = "/Users/sm9276/PycharmProjects/PLEXOS-Help-Data/Q&A"  # Replace with your output folder path

    # Iterate through each text file in the folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.txt'):
            file_path = os.path.join(input_folder, file_name)

            # Read the input text file
            text_content = read_text_file(file_path)

            # Generate questions
            questions = generate_questions(text_content)

            # Generate answers and create QA pairs
            qa_pairs = []
            for question in questions[1:6]:
                answer = generate_answer(question, text_content)
                qa_pairs.append({"question": question, "answer": answer})

            # Save the QA pairs to a JSONL file
            jsonl_file = save_to_jsonl(output_folder, os.path.splitext(file_name)[0], qa_pairs)

            print(f"QA pairs for {file_name} saved to {jsonl_file}")
