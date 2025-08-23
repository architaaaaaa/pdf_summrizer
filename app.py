# app.py
# This script creates a simple Flask web application to summarize PDF files.
# It uses the Hugging Face transformers library for summarization and PyPDF2
# for PDF text extraction.

import os
from flask import Flask, request, jsonify, render_template
import PyPDF2
from transformers import pipeline
import json
import io

# Initialize the Flask application
# This is the crucial line that was causing the previous error.
app = Flask(__name__)

# Load the summarization pipeline from Hugging Face.
# We're using the 'sshleifer/distilbart-cnn-12-6' model, which is a good
# general-purpose summarization model.
try:
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
except Exception as e:
    print(f"Error loading the summarization model: {e}")
    # You might want to handle this error more gracefully, but for a simple
    # app, printing the error and proceeding is fine. The summarization
    # will fail later if the model isn't loaded.
    summarizer = None


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
    # Check if a file was uploaded in the request
    if 'pdf_file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['pdf_file']

    # If the user submits an empty form, the browser might send an empty file.
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Ensure the uploaded file is a PDF
    if file and file.filename.endswith('.pdf'):
        try:
            # Read the PDF file from the in-memory stream
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
            full_text = ""

            # Extract text page by page
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                full_text += page.extract_text()

            # The summarizer model has a maximum token limit.
            # We'll truncate the text to fit the model's input size.
            # This is a simple but effective way to handle large documents.
            max_input_length = summarizer.tokenizer.model_max_length
            if len(full_text) > max_input_length:
                full_text = full_text[:max_input_length]

            # Generate the summary using the loaded pipeline
            if summarizer:
                summary_output = summarizer(full_text, max_length=150, min_length=30, do_sample=False)
                summary_text = summary_output[0]['summary_text']
                return jsonify({'summary': summary_text})
            else:
                return jsonify({'error': 'Summarization model not loaded.'}), 500

        except Exception as e:
            # Handle potential errors during PDF processing or summarization
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Invalid file format. Please upload a PDF file.'}), 400


# Run the application
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 5000), debug=False)
