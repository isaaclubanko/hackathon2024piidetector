from flask import flash, Flask, render_template, redirect, request, abort
from transformers import pipeline
app = Flask(__name__)
import json

import cv2
import pytesseract
import numpy as np
import os
from pytesseract import Output


global MODEL
MODEL = None
SKIP_ENTITY_GROUPS = ('SSN', 'USERNAME', 'EMAIL', 'DISPLAYNAME')

def get_image_text(file_path: str):
    img = cv2.imread(file_path)
    image_text = pytesseract.image_to_string(img)
    image_phrases = image_text.split('\n')
    return list(filter(None, image_phrases))

def detect_pii(text: list[str]):
    if not text:
        return ''

    global MODEL
    if not MODEL:
        MODEL = pipeline("token-classification", "lakshyakh93/deberta_finetuned_pii", device=-1)
    
    return_fields = []
    for line in text:
        analysis = MODEL(line, aggregation_strategy="first")

        for a in analysis:
            if a['entity_group'] in SKIP_ENTITY_GROUPS:
                continue
            return_fields.append({
                'entity_group': a['entity_group'],
                'word': a['word'].strip(',').strip()
            })
    return return_fields

def box_detected_pii(filename, detected_pii_words):
    file_path = os.path.join(os.getcwd(), 'uploads/' + filename)
    img = cv2.imread(file_path)
    details = pytesseract.image_to_data(img, output_type=Output.DICT)

    color = (0, 0, 255)
    thickness = 5
    for i in range(len(details['text'])):
        if details['text'][i].strip(',') in detected_pii_words:
            # print(details['text'][i])
            # print(f"left: {details['left'][i]}")
            # print(f"top: {details['top'][i]}")
            # print(f"width: {details['width'][i]}")
            # print(f"height: {details['height'][i]}")
            cv2.rectangle(
                img,
                (details['left'][i], details['top'][i]),
                (details['left'][i] + details['width'][i], details['top'][i] + details['height'][i]),
                color,
                thickness
            )
    # static isn't the best name but this renders the image easily
    write_path = os.path.join(os.getcwd(), 'static/' + filename)
    cv2.imwrite(write_path, img)
    
    return write_path


@app.route('/') # ‘https://www.google.com/‘
def home():
    # allows the app to preload the model 
    global MODEL
    if not MODEL:
        MODEL = pipeline("token-classification", "lakshyakh93/deberta_finetuned_pii", device=-1)

    return render_template('home.html')

@app.route('/detect_image_pii', methods=['POST'])
def detect_image_pii():
    if request.method == 'POST':
        # check if the post request has the file part
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
            file_path = os.path.join(os.getcwd(), 'uploads/' + filename)
            file.save(file_path)
            image_text = get_image_text(file_path)
            detected_pii_data = detect_pii(image_text)

            # Have only figured out how to box individual words at a time, not multiple words 
            # such as full names and addresses. Surely there's a better way to flatten this list...
            # but I have a demo to prep...
            detected_pii_words = [
                data['word'] if ' ' not in data['word']
                else [word for word in data['word'].split(' ')]
                for data in detected_pii_data
            ]
            individual_detected_pii_words = []
            for words in detected_pii_words:
                if isinstance(words, list): individual_detected_pii_words.extend(words)
                else: individual_detected_pii_words.append(words)

            pii_detected_file_path = box_detected_pii(filename, individual_detected_pii_words)
            return render_template(
                'detect_image_pii.html',
                file_path='static/' + filename,
                detected_pii=detected_pii_data
            )
    return



# @app.route('/detect_pii/', methods=['POST'])
# def detect_pii():
#     text_string = request.get_json().get('text_input', None)

#     if not text_string:
#         abort(400)

#     global MODEL
#     if not MODEL:
#         MODEL = pipeline("token-classification", "lakshyakh93/deberta_finetuned_pii", device=-1)
    
#     analysis = MODEL(text_string, aggregation_strategy="first")

#     return_fields = []
#     for a in analysis:
#         return_fields.append({
#             'entity_group': a['entity_group'],
#             'word': a['word']
#         })
#     return json.dumps(return_fields)


app.run(port=3000)
