from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import PyPDF2
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

app = Flask(__name__)
CORS(app)

extracted_chunks = []

# PDF text extraction and chunking
def extract_text_chunks(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = "".join([page.extract_text() for page in pdf_reader.pages])
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    return splitter.split_text(text)


def extract_visualization_data(answer):
    try:
        json_content = re.search(r'```json\s*(\{.*\})\s*```', answer, re.DOTALL).group(1)
        return eval(json_content)
    except Exception as error:
        print("An error occurred:", error)
        return None

@app.route('/upload', methods=['POST'])
def upload_file():
    global extracted_chunks
    file = request.files['file']
    extracted_chunks = extract_text_chunks(file)

    summary = ""
    for chunk in extracted_chunks:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant skilled in summarizing documents in multiple languages."},
                {"role": "user", "content": f"Summarize: {chunk}"}
            ]
        )
        summary += response.choices[0].message.content + "\n"

    return jsonify({"summary": summary.strip()})

@app.route('/ask', methods=['POST'])
def ask_question():
    global extracted_chunks
    data = request.get_json()
    question = data['question']
    chat_history = data.get('chatHistory', [])
    long_context = data.get('longContext', "")

    combined_context = "\n".join(extracted_chunks)

    messages = [
        {"role": "system", "content": "You are a helpful assistant answering only based on the uploaded document. Detect and decline off-topic questions. Use context and prior answers to assist user effectively. Do not hallucinate."},
        {"role": "system", "content": f"Document Context: {combined_context}"},
        {"role": "system", "content": f"Long-Term Context: {long_context}"}
    ]

    for chat in chat_history[-5:]:
        messages.append({"role": "user", "content": chat['question']})
        messages.append({"role": "assistant", "content": chat['answer']})

    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(model="gpt-4o", messages=messages)
    answer = response.choices[0].message.content

    if len(long_context.split()) < 500:
        long_context += f"\nUser: {question}\nAssistant: {answer}"

    if 'json' in answer.lower():
        visualization_data = extract_visualization_data(answer)
        return jsonify({"answer": answer, "longContext": long_context, "visualizationData": visualization_data})

    return jsonify({"answer": answer, "longContext": long_context})

@app.route('/visualize', methods=['POST'])
def visualize():
    data = request.get_json()
    numbers = data['numbers']
    labels = data.get('labels', [f"Item {i+1}" for i in range(len(numbers))])

    plt.figure(figsize=(10, 6))
    plt.bar(labels, numbers)
    plt.xlabel('Labels')
    plt.ylabel('Values')
    plt.title('Visualization of Numbers')
    plt.tight_layout()

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
