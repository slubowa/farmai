from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session
import pandas as pd
import os
from dotenv import load_dotenv
from openai import OpenAI
from models.fertilizer_recomm_oo import FertilizerPredictor
from models.credit_scoring_model import CreditScoringModel

load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.getenv('FLASK_APP_SECRET_KEY')
Session(app)

# Load the credit scoring model

model_path = os.path.join(os.path.dirname(__file__), 'models', 'credit_scoring_model.pkl')
credit_model = CreditScoringModel()
credit_model.load_model(model_path)

@app.before_request
def handle_options_request():
    if request.method == 'OPTIONS':
        response = app.make_response('')
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    print("Received data:", data)
    df = pd.DataFrame(data)
    predictions = credit_model.predict(df)
    return jsonify(predictions.tolist())

@app.route('/fertilizer_recommendation', methods=['POST'])
def fertilizer_recommendation_route():
    data = request.json
    print("Received data:", data)  
    area_name = data.get('area_name')
    crop_type = data.get('crop_type')
    farm_size_acres = float( data.get('farm_size_acres'))
    weather_api_key = os.getenv('WEATHER_API_KEY')

    if not all([area_name, crop_type, farm_size_acres, weather_api_key]):
        return jsonify({"error": "Missing required parameters"}), 400

    predictor = FertilizerPredictor(area_name, weather_api_key, crop_type, farm_size_acres)
    fertilizer_requirement = predictor.run()
    
    if fertilizer_requirement is not None:
        return jsonify(fertilizer_requirement)
    else:
        return jsonify({"error": "Failed to get fertilizer recommendation"}), 400

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        question = data.get('question')
        if not question:
            return jsonify({"error": "Question parameter is missing"}), 400

        # Check if a thread exists in the session
        thread_id = session.get('thread_id', None)
        if thread_id is None:
            # Create a new thread if one doesn't exist
            thread = client.beta.threads.create()
            session['thread_id'] = thread.id  
        else:
            # Load existing thread
            thread = client.beta.threads.retrieve(thread_id)

        # Create a message in the thread
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=question
        )

        # Run the thread with the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id="asst_oOrSqSp5jAGLs4N7g1cQ7J7X"
        )

        # Wait for the run to complete
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        while run_status.status != 'completed':
            run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        # Fetch messages from the thread
        messages = client.beta.threads.messages.list(thread.id)
        
        # Filter and get the assistant's last message
        assistant_messages = [msg for msg in messages if msg.role == 'assistant']

        if assistant_messages:
            last_message = assistant_messages[-1]
            answer = ''.join([block.text.value for block in last_message.content]).strip()
        else:
            answer = "No response from assistant."

        return jsonify({"answer": answer})
    except Exception as e:
        print(f"Exception occurred: {e}")
        return jsonify({"error": "Failed to get response from AI"}), 500

if __name__ == '__main__':
    app.run(debug=True)