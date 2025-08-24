# app.py
# This script creates a simple Flask web application to summarize PDF files.
# It uses PyPDF2 for PDF text extraction and a basic text summarization function.

import os
from flask import Flask, request, jsonify, render_template
import PyPDF2
import json
import io
import re

# Initialize the Flask application
app = Flask(__name__)

# --- Text Summarization Function ---
def simple_summarizer(text, num_sentences=10):
    """
    A simple function to summarize text by extracting the first `num_sentences`
    and returning them as a list of points. This avoids using large machine
    learning models, ensuring low memory usage.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    # Join sentences with a newline character and a bullet point
    summary = '\n• ' + '\n• '.join(sentences[:num_sentences])
    return summary


# --- Web Routes ---

@app.route('/')
def index():
    """Renders the main page with the file upload form."""
    return render_template('index.html')


@app.route('/summarize', methods=['POST'])
def summarize_pdf():
    """
    Handles the PDF file upload, extracts text, and returns a summary.
    """
    if 'pdf_file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['pdf_file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.pdf'):
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
            full_text = ""

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                full_text += page.extract_text()

            # Generate the summary using the simple summarizer function
            summary_text = simple_summarizer(full_text)
            
            return jsonify({'summary': summary_text})

        except Exception as e:
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Invalid file format. Please upload a PDF file.'}), 400


# Run the application
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 5000), debug=False)
