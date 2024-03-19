from flask import Flask, request, abort
from transformers import pipeline
app = Flask(__name__)
import json

global MODEL
MODEL = None

@app.route('/') # ‘https://www.google.com/‘
def home():
    # allows the app to preload the model 
	gen = pipeline("token-classification", "lakshyakh93/deberta_finetuned_pii", device=-1)
	MODEL = gen
	return "Model Loaded"


@app.route('/detect_pii/', methods=['POST'])
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


app.run(port=3000)
