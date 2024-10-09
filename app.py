
from db import get_record
from flask import Flask, request, jsonify
import requests
import pickle
import glob

"""

TODO: Update the following:
- Update database to include the ph feature
- Use the weather API to get the rainfall, also add this feature to the database
- Update the features in clean() to include the new features

Model currently returns N/A as not all features are provided.

"""


app = Flask(__name__)
app.config["DEBUG"] = True

try:
    all_models = glob.glob("*-model.pkl", root_dir="models/")
    if not all_models:
        raise FileNotFoundError()
    # just choosing the first model
    model_path = all_models[0]

    with open(model_path, 'rb') as model_file:
        MODEL = pickle.load(model_file)

except FileNotFoundError:
    print("Error: Model file not found. Ensure that there is a model under 'models/' directory.")
    MODEL = None

except Exception as e:
    print(f"Error loading model: {str(e)}")
    MODEL = None


def clean():
    record = get_record()
    features = ['n', 'p', 'k', 'temp', 'moisture']
    return {k: record[k] for k in features if k in record}


@app.route('/predict', methods=['POST'])
def predict():
    if MODEL is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.get_json()
        if not data or 'features' not in data:
            return jsonify({'error': 'No features provided'}), 400
        
        prediction = MODEL.predict([data['features']])
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/', methods=['GET'])
def home():
    try:
        record = clean()
        response = requests.post('http://localhost:5000/predict', json=record)
        return f"<h1>Prediction: {response.json().get('prediction', 'N/A')}</h1>"

    except requests.RequestException as e:
        return f"<h1>Error: {str(e)}</h1>", 500


if __name__ == '__main__':
    print(MODEL)
    app.run()
