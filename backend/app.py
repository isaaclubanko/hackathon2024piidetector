from flask import Flask, request, abort
from transformers import pipeline
import json
import yaml
import os
app = Flask(__name__)

global MODEL
MODEL = None

@app.route('/api/')
def home():
    # allows the app to preload the model 
    gen = pipeline("token-classification", "lakshyakh93/deberta_finetuned_pii", device=-1)
    global MODEL
    MODEL = gen
    return json.dumps({"model_loaded": True})


@app.route('/swagger.json')
def get_swagger():
    print(os.getcwd())
    print(os.listdir())
    with open('piidetector/swagger.yaml', 'r') as f:
        yaml_object = yaml.load(f, Loader=yaml.FullLoader)
        return json.dumps(yaml_object)


@app.route('/api/detect_pii/', methods=['POST'])
def detect_pii():
    text_string = request.get_json().get('text_input', None)

    if not text_string:
        abort(400)

    global MODEL
    if not MODEL:
        MODEL = pipeline("token-classification", "lakshyakh93/deberta_finetuned_pii", device=-1)
    
    analysis = MODEL(text_string, aggregation_strategy="first")

    return_fields = []
    for a in analysis:
        return_fields.append({
            'entity_group': a['entity_group'],
            'word': a['word']
        })
    return json.dumps(return_fields)


app.run(port=8002)
