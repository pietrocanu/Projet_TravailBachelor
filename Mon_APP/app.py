import os
from flask import Flask, render_template, request
from flask_dropzone import Dropzone
import modeles

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config.update(
    UPLOADED_PATH=os.path.join(basedir,'uploads'),
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=1,
    DROPZONE_MAX_FILES=1,
    DROPZONE_DEFAULT_MESSAGE='Déposer ici le document à analyser',
)

app.config['UPLOADED_PATH'] = 'uploads'

dropzone = Dropzone(app)

filename = None


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
  
  
def setsrc(filename):
    return os.path.join(app.config['UPLOADED_PATH'], filename)


@app.route("/analyse", methods=['POST'])
def analyse():
    global filename
    if request.method == 'POST':
        if request.files:
            image = request.files["file"]   
            
            modeles.modele(image)
            
            filename = image.filename
            f = image.save(os.path.join(app.config["UPLOADED_PATH"], filename))
			
    return render_template('index.html', filename = setsrc(filename))


@app.route("/", methods=['POST'])
def cancel():
    request.redirect('/')
    return render_template('index.html');


if __name__ == '__main__':
    app.run(debug=True)

