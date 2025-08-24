# pdf_summrizer

https://architadey.pythonanywhere.com/


PDF Summarizer App Flowchart
This flowchart outlines the main logic of the Flask application, from a user uploading a file to receiving a summary.

1. Initial Request (Homepage)

A user visits the root URL (/) of the web application.

The @app.route('/') decorator triggers the index() function.

The index() function uses render_template('index.html') to serve the HTML form to the user.

2. File Submission

The user selects a PDF file and clicks the "Summarize PDF" button.

The browser sends an HTTP POST request to the /summarize URL, including the PDF file data.

3. Request Handling

The @app.route('/summarize', methods=['POST']) decorator directs the request to the summarize_pdf() function.

The function first checks if a file was included in the request and if it has a .pdf extension.

If the file is missing or the wrong type, the function returns an error message as JSON.

4. Text Extraction

If the file is a valid PDF, the code reads the file's binary data into memory using io.BytesIO().

A PyPDF2.PdfReader object is created to parse the PDF data.

The code iterates through each page of the PDF, extracting the text and concatenating it into a single string called full_text.

5. Summarization

The full_text string is passed to the simple_summarizer() function.

This function splits the text into individual sentences.

It then takes the first 10 sentences and joins them back together to create a summary string.

6. Response

The summarize_pdf() function receives the summary string.

It packages the summary into a JSON object with the key 'summary'.

This JSON response is sent back to the user's browser.

The JavaScript on the webpage receives the JSON and updates the display to show the summarized text.

7. Error Handling

The entire process is wrapped in a try...except block to catch any unexpected errors during file processing or summarization. If an error occurs, a detailed error message is returned to the user instead of the application crashing.
