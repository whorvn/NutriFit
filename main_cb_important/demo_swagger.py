import threading
from time import sleep
from flask import Flask, render_template, request, jsonify
from flasgger import Swagger
# from pyngrok import ngrok
import google.generativeai as genai
import json

app = Flask(__name__)


conversation_history = dict()

# Configure Google API
# GOOGLE_API_KEY = 'AIzaSyA5x0J0Pqjuv8l7OtbrJWn3aTEZz-kLgGE'
GOOGLE_API_KEY = 'AIzaSyACNkBzvg7M-Ks3szJMSkp_8ks9aB0ZqPE'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def calculate_bmr(weight, height, age, gender):
    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    return bmr

def calculate_tdee(bmr, activity_level):
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very active': 1.9
    }
    return bmr * activity_multipliers.get(activity_level, 1.2)

@app.route('/')
def index():
    return render_template('index.html')

# Add header validation function
def validate_headers():
    content_type = request.headers.get("Content-Type", "")
    data_service_version = request.headers.get("DataServiceVersion", "")

    if not content_type.startswith("application/json"):
        return jsonify({"error": "Unsupported Media Type. Content-Type must be 'application/json' or 'application/json;odata=verbose'"}), 415

    if data_service_version and float(data_service_version) >= 3.0:
        return jsonify({"error": "Unsupported DataServiceVersion. Version must be less than 3.0."}), 400

# Use validate_headers in both endpoints
@app.route('/personalized_plan', methods=['POST'])
def personalized_plan():
    header_error = validate_headers()
    if header_error:
        return header_error

    data = request.json
    name = data['name']
    age = int(data['age'])
    weight = float(data['weight'])
    height = float(data['height'])
    gender = data['gender'].lower()
    activity_level = data['activity_level'].lower()
    goal = data['goal'].lower()

    bmr = calculate_bmr(weight, height, age, gender)
    tdee = calculate_tdee(bmr, activity_level)

    prompt = f"""
    The user is {name}, a {age}-year-old {gender} who weighs {weight} kg and is {height} cm tall. 
    Their fitness goal is {goal}, and their activity level is {activity_level}. 
    Their Total Daily Energy Expenditure (TDEE) is {tdee} calories. 
    Based on this information, provide specific advice regarding daily calorie intake, macronutrient ratios, 
    and a personalized workout plan.
    """

    response = model.generate_content(prompt)

    user_data = {
        "personalized_advice": response.text
    }

    with open('user_data.json', 'w') as f:
        json.dump(user_data, f)

    return jsonify(user_data)

@app.route('/question_answer', methods=['POST'])
def question_answer():
    header_error = validate_headers()
    if header_error:
        return header_error

    user_id = request.json["user_id"]
    question = request.json['question']
    if user_id in conversation_history:
        conversation_history[user_id].append(question)
    else:
        conversation_history[user_id] = [question]

    conversation_ctx = "\n".join(conversation_history[user_id])
    prompt = f"""
    You are NutriAI, a fitness chatbot. You are in a conversation with the user.
    The user is asking fitness-related questions about gym, diet, workouts, or health.
    Provide responses only if the question is relevant to fitness.
    
    Conversation history:
    {conversation_ctx}

    Respond appropriately to the user's latest message.
    """

    response = model.generate_content(prompt)

    return jsonify({"response": response.text})
# Define clean_conversation_history to periodically clear chat history
def clean_conversation_history():
    while True:
        conversation_history.clear()
        sleep(86400)  # Clear conversation history every 24 hours

# Main application entry point
if __name__ == '__main__':
    # Optional: Start ngrok for public access (if needed)
    # public_url = ngrok.connect(5000)
    # print(f" * Ngrok tunnel available at: {public_url}")

    # Optional: Run conversation cleaner in a separate thread
    threading.Thread(target=clean_conversation_history).start()

    # Initialize Swagger for API documentation
    swagger = Swagger(app)

    # Run Flask app
    app.run(host="0.0.0.0", port=5050, debug=True)
