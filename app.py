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
app = Flask(__name__)

# Load the summarization pipeline from Hugging Face.
# We're now using 'sshleifer/distilbart-cnn-6-6', which is a much smaller
# and more memory-efficient model for free hosting tiers like Render.
try:
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-6-6")
except Exception as e:
    print(f"Error loading the summarization model: {e}")
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

            # The summarizer model has a maximum token limit.
            max_input_length = summarizer.tokenizer.model_max_length
            if len(full_text) > max_input_length:
                full_text = full_text[:max_input_length]

            if summarizer:
                summary_output = summarizer(full_text, max_length=150, min_length=30, do_sample=False)
                summary_text = summary_output[0]['summary_text']
                return jsonify({'summary': summary_text})
            else:
                return jsonify({'error': 'Summarization model not loaded.'}), 500

        except Exception as e:
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Invalid file format. Please upload a PDF file.'}), 400


# Run the application
if __name__ == '__main__':
    # The 'host' parameter is set to '0.0.0.0' to listen on all public IPs,
    # and the 'port' is fetched from the environment variables provided by Render.
    # The `debug=False` line is important for a production environment.
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 5000), debug=False)
