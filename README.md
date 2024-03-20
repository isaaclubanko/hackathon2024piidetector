# hackathon2024piidetector
AI Powered PII Detector. Using Flask, Python 3.10 and Angular 16

Text typed into the comments section will be sent to a pretrained AI model (lakshyakh93/deberta_finetuned_pii) which will return any words determined to be PII

# Install instructions

1. In a Python 3.10 virtual env, exec into the backend directory and run 
`pip install -3 depdencies.lst` 

2. Run the flask backend in a terminal using `flask --app run backend`

3. using NPM, exec into `angular_frontend` and npm install and serve the angular app in another terminal