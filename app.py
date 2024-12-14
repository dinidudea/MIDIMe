import os
import tempfile
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'mp3'}
# Set the maximum allowed file size to 16 MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def mp3_to_midi(mp3_path):
     # Placeholder for MP3 to MIDI conversion logic.  
    print("Attempting to convert the uploaded MP3 to MIDI, but this function is a placeholder. Outputting MP3 instead")
    return mp3_path  # Placeholder, return original MP3


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error='No file part')

        file = request.files['file']

        if file.filename == '':
            return render_template('index.html', error='No file selected')

        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)


                # Perform MP3 to MIDI Conversion
                midi_path = mp3_to_midi(filepath) # Placeholder
                
                # Return processed file. If the processing fails, this will return the original file
                return send_file(midi_path, as_attachment=True, download_name=filename.rsplit('.', 1)[0] + (".mid" if midi_path != filepath else ".mp3"))

            except Exception as e:
                return render_template('index.html', error=f'Error during processing: {str(e)}')
        else:
            return render_template('index.html', error='Invalid file type. Please upload an MP3 file.')

    return render_template('index.html', error=None)

if __name__ == '__main__':
    app.run(debug=True)
