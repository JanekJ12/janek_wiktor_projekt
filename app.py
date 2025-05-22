from flask import Flask, request, redirect, url_for, render_template, send_from_directory, jsonify
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'rar'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Upewnij się, że folder na pliki istnieje
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Główna strona
@app.route('/')
def index():
    return render_template('index.html')

# Strona upload
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'Brak pliku'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nie wybrano pliku'}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            return jsonify({'message': 'Plik zapisany', 'filename': filename}), 200
        return jsonify({'error': 'Nieprawidłowy typ pliku'}), 400
    return render_template('Drop.html')

# Strona pobierania
@app.route('/download')
def download_page():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('Dowland.html', files=files)

# Strona o nas
@app.route('/about')
def about_page():
    return render_template('About.html')

# Pobieranie konkretnych plików
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
