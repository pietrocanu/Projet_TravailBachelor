#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from flask import Flask, render_template, request
from flask_dropzone import Dropzone
import subprocess

from pdf2image import convert_from_path
import filetype

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config.update(
    MODELE_PATH=os.path.join('aiaccessibility', 'detectron2', 'demo'),
    CONFIG_PATH=os.path.join('aiaccessibility', 'detectron2', 'configs'),
    MODEL_WEIGHTS=os.path.join('aiaccessibility', 'models', 'MaskRCNN_Resnet101_FPN_3X'),
    INPUT_PATH=os.path.join(basedir, 'static', 'inputs'),
    OUTPUT_PATH=os.path.join(basedir, 'static', 'outputs'),
	UPLOAD_PATH=os.path.join(basedir, 'static', 'uploads'),

    DROPZONE_ALLOWED_FILE_CUSTOM= True,
    DROPZONE_ALLOWED_FILE_TYPE= 'image/*, .pdf',
    DROPZONE_MAX_FILE_SIZE=1,
    DROPZONE_MAX_FILES=1,
    DROPZONE_DEFAULT_MESSAGE='Déposer ici le document à analyser',
)
app.config['MODELE_PATH'] = os.path.join('aiaccessibility', 'detectron2', 'demo')
app.config['CONFIG_PATH'] = os.path.join('aiaccessibility', 'detectron2', 'configs')
app.config['MODEL_WEIGHTS'] = os.path.join('aiaccessibility', 'models', 'MaskRCNN_Resnet101_FPN_3X')
app.config['INPUT_PATH'] = os.path.join('static', 'inputs')
app.config['OUTPUT_PATH'] = os.path.join('static', 'outputs')
app.config['UPLOAD_PATH'] = os.path.join('static', 'uploads')

app.config['PROPAGATE_EXCEPTIONS'] = True

dropzone = Dropzone(app)

filename = None
Model_Device = 'cpu'

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
  
@app.errorhandler(500)
def internal_error(error):
    return "500 error"

@app.errorhandler(404)
def not_found(error):
    return "404 error",404

def createInputFile(filename):
    cwd = os.getcwd()
    return os.path.join(cwd, app.config["INPUT_PATH"], filename)

def getOutputFile(filename):
    return os.path.join(app.config["OUTPUT_PATH"], filename)
   
def executeModel(input_filename, output_filename):
    cmd = """python3.8 /home/pietro/aiaccessibility/detectron2/demo/demo.py --config-file /home/pietro/aiaccessibility/detectron2/configs/DLA_mask_rcnn_R_50_FPN_3x.yaml --input {0} --output {1} --opts MODEL.WEIGHTS /home/pietro/aiaccessibility/models/MaskRCNN_Resnet101_FPN_3X/model_final_trimmed.pth MODEL.DEVICE cpu""".format(input_filename, output_filename)
    print(cmd)
    subprocess.Popen(cmd.split(" ")).wait()


@app.route("/analyse", methods=['POST'])
def analyse():
    global filename
    print("++++++++++++++")
    print(filename)
    if request.method == 'POST':
        print(request.files)
        if request.files:
            image = request.files["file"]   
            filename = image.filename
            print(filename)
            input_filename = createInputFile(filename)
            print(app.config["INPUT_PATH"])
            print(input_filename)
            image.save(input_filename)
            imageExtension = filetype.guess(input_filename)
            print(imageExtension)
            #if imageExtension != '.jpg':
            #    images = convert_from_path(input_filename)
            #    for image in images:
            #        image.save(createInputFile(image.filename)+'.jpg', 'JPEG')
            #else:
            #    print('already saved') 
            return render_template('index.html', filename = getOutputFile(filename))
        else:
            input_filename = createInputFile(filename)
            output_filename = getOutputFile(filename) 
            print(app.config["OUTPUT_PATH"])
            print(output_filename)
            executeModel(input_filename, output_filename)
            return render_template('index.html', filename = getOutputFile(filename))


@app.route("/cancel", methods=['POST'])
def cancel():
    os.remove(getOutputFile(filename))
    return render_template('index.html');


if __name__ == '__main__':
    try:
        app.run(threaded=True, debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(str(e))
