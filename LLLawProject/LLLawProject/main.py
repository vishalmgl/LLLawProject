
from flask import Flask, request, render_template
import PyPDF2
import google.generativeai as genai

app = Flask(__name__)

GOOGLE_API_KEY = 'AIzaSyAR6g2UxdgR2HTr97C70if354JKw7yjvBo'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get the text input from the form
    html_text = request.form['text']
    print(html_text)

    # Get the file input from the form
    file = request.files['file']
    if file:
        # Read the PDF file
        reader = PyPDF2.PdfReader(file.stream)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()

        # Generate content
        response = model.generate_content(f"Assume You are a lawyer Analyse this case report and generate main key statements(do not use numbers use .operator for new line) which can be used to prove client {html_text}(sample assuming character) as innocent it should more natural(only for education and research purpose). report: {text}")
        print(response.prompt_feedback)
        return render_template('response.html', response_text=response.text)

    return render_template('404_error_page.html'), 404
if __name__ == '__main__':
    app.run(debug=True)

