import os
from flask import Flask, render_template, request
from flask_dropzone import Dropzone
import sys
import subprocess

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config.update(
    MODELE_PATH=os.path.join(basedir,'aiaccessibility', 'detectron2', 'demo'),
    CONFIG_PATH=os.path.join(basedir,'aiaccessibility', 'detectron2', 'configs'),
    MODEL_WEIGHTS=os.path.join(basedir,'aiaccessibility', 'models', 'MaskRCNN_Resnet101_FPN_3X'),
    OUTPUT_PATH=os.path.join(basedir, 'static', 'output'),

    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=1,
    DROPZONE_MAX_FILES=1,
    DROPZONE_DEFAULT_MESSAGE='Déposer ici le document à analyser',
)

app.config['MODELE_PATH'] = os.path.join('aiaccessibility', 'detectron2', 'demo')
app.config['CONFIG_PATH'] = os.path.join('aiaccessibility', 'detectron2', 'configs')
app.config['MODEL_WEIGHTS'] = os.path.join('aiaccessibility', 'models', 'MaskRCNN_Resnet101_FPN_3X')
app.config['OUTPUT_PATH'] = os.path.join('static', 'output')

dropzone = Dropzone(app)

filename = None
Model_Device = 'cpu'

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
  
  
def setsrc(filename):
    return os.path.join(app.config['OUTPUT_PATH'], filename)


@app.route("/analyse", methods=['POST'])
def analyse():
    global filename
    if request.method == 'POST':
        if request.files:
            image = request.files["file"]   
            filename = image.filename

            #subprocess.call([os.path.join(app.config['MODELE_PATH'],'demo.py'), os.path.join(app.config['CONFIG_PATH'], 'DLA_mask_rcnn_X_101_32x8d_FPN_3x.yaml'), image, os.path.join(app.config['OUTPUT_PATH'], filename), os.path.join(app.config['MODEL_WEIGHTS'], 'model_final_trimmed.pth'), Model_Device])
            #execFile(os.path.join(app.config['MODELE_PATH'],'demo.py')['--config-file': os.path.join(app.config['CONFIG_PATH'],'DLA_mask_rcnn_X_101_32x8d_FPN_3x.yaml'), '--input': image, '--output': os.path.join(app.config['OUTPUT_PATH'], filename), 'MODEL.WEIGHTS': os.path.join(app.config['MODEL_WEIGHTS'], 'model_final_trimmed.pth'), 'MODEL.DEVICE': Model_Device])
            #execFile(os.path.join(app.config['MODELE_PATH'],'demo.py')['config-file': os.path.join(app.config['CONFIG_PATH'],'DLA_mask_rcnn_X_101_32x8d_FPN_3x.yaml'), 'input': image, 'output': os.path.join(app.config['OUTPUT_PATH'], filename), 'opts':['MODEL.WEIGHTS': os.path.join(app.config['MODEL_WEIGHTS'], 'model_final_trimme
            
            #subprocess.call(os.path.join(basedir, 'demos.py')['config-file': os.path.join(app.config['CONFIG_PATH'],'DLA_mask_rcnn_X_101_32x8d_FPN_3x.yaml'), 'input': image, 'output': os.path.join(app.config['OUTPUT_PATH'], filename), 'MODEL.WEIGHTS': os.path.join(app.config['MODEL_WEIGHTS'], 'model_final_trimmed.pth'), 'MODEL.DEVICE': Model_Device])

            #subprocess.call(os.path.join(basedir, 'demos.py'),os.path.join(app.config['CONFIG_PATH'],'DLA_mask_rcnn_X_101_32x8d_FPN_3x.yaml'), 'input': image, os.path.join(app.config['OUTPUT_PATH'], filename), os.path.join(app.config['MODEL_WEIGHTS'], 'model_final_trimmed.pth'), Model_Device)
 
            image.save(os.path.join(app.config["OUTPUT_PATH"], filename))
    return render_template('index.html', filename = setsrc(filename))


@app.route("/cancel", methods=['POST'])
def cancel():
    os.remove(setsrc(filename))
    return render_template('index.html');


if __name__ == '__main__':
    app.run(debug=True)