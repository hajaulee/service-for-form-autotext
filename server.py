import os
import json
import sys
import time
import cv2
from flask import Flask, request, flash, redirect, render_template, send_from_directory
from flask_cors import CORS, cross_origin
from werkzeug.datastructures import ImmutableMultiDict
sys.path.append(os.getcwd())
if not os.path.exists('tmp'):
    os.makedirs('tmp')

app = Flask(__name__)
app.secret_key = 'ai_biet_dau'
app.config['SESSION_TYPE'] = 'filesystem'
CORS(app)


""" 
LOAD MODEL OR PREPARE ANYTHING HERE 
"""

def process(img_path, boxes):
    # TODO
    # Edit this function for real predicted result
    
    img = cv2.imread(img_path)
    for box in boxes:
        coo = box['box']
        img = cv2.rectangle(img, (coo['xmin'], coo['ymin']),
                                 (coo['xmax'], coo['ymax']), 
                                 [0, 255, 0], 4)
        img = cv2.putText(img, box['name'], 
                            (coo['xmin']+5, coo['ymax']-10), 
                            cv2.FONT_HERSHEY_SIMPLEX ,  
                            1, (255, 0, 0), 2, cv2.LINE_AA)

    filename, file_extension = os.path.splitext(img_path)
    out_file = filename + '-output' + file_extension
    out_file = out_file.replace('tmp', 'static')
    cv2.imwrite(out_file, img)

    return out_file

@app.route('/')
def home():
    return send_from_directory('', 'index.html')

@app.route('/upload', methods=["POST"])
def upload():
    # print("CCCCC", request.form.to_dict())
    # print(request.files.to_dict())

    # Save uploadeed file
    f = request.files.to_dict()['file']
    fullname = f.filename
    filename, file_extension = os.path.splitext(fullname)
    from_path = 'tmp/' + fullname + str(time.time()) + file_extension
    f.save(from_path)

    # Boxes
    boxes = json.loads(request.form.to_dict()['boxes'])

    # Process image
    output_path = process(from_path, boxes)

    return render_template('output.html', output=output_path)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8000')
