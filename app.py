import os
from flask import Flask, request, render_template, flash, redirect, send_from_directory
from gptHandler import generate_response
import json

app = Flask(__name__)

app.config['FILES_DIR'] = "files"
app.config['SECRET_KEY'] = os.urandom(12).hex()

notes = ''

def list_directory():
    files = os.listdir(app.config['FILES_DIR'])
    file_links = ""
    for file in files:
        file_links += f"<a href='files/{file}'>{file}</a><br>"
    return files

@app.route('/', methods=['GET', 'POST'])
def index():
    global notes
    if request.method == 'POST':
        try:
            notes = request.form['notes']

        # check if the post request has the file part
        except :
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file:
                filename = file.filename
                file.save(os.path.join(app.config['FILES_DIR'] , filename))
                print("Downloaded to " , os.path.join(app.config['FILES_DIR'] , filename))

    return render_template('index.html', notes=notes, files = list_directory())


@app.route('/files/<path:path>')
def serve_file(path):
    return send_from_directory(app.config['FILES_DIR'], path)


prompt = ''
@app.route('/gpt', methods=['GET', 'POST'])
def gpt():
    global prompt

    if request.method == 'POST':
        prompt = request.form['prompt']

    generate_response(prompt)
    with open("gptHistory/chat_history.json", "r") as history_json:
        history = json.load(history_json)

    return render_template('gpt.html', chat = history)  


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

