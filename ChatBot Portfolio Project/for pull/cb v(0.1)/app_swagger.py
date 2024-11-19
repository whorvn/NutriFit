from flask import Flask, render_template, request, jsonify
from flasgger import Swagger
import google.generativeai as genai
import threading
from time import sleep
import json
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
swagger = Swagger(app)  # Initialize Swagger
run_with_ngrok(app)  # Start ngrok when app is run

conversation_history = dict()

GOOGLE_API_KEY = 'AIzaSyA5x0J0Pqjuv8l7OtbrJWn3aTEZz-kLgGE'
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

@app.route('/personalized_plan', methods=['POST'])
def personalized_plan():
    """
    Generate a personalized fitness plan.
    ---
    tags:
      - Fitness
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            age:
              type: integer
            weight:
              type: number
            height:
              type: number
            gender:
              type: string
            activity_level:
              type: string
            goal:
              type: string
    responses:
      200:
        description: A JSON object with personalized fitness advice.
        schema:
          type: object
          properties:
            personalized_advice:
              type: string
    """
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
    """
    Respond to fitness-related questions.
    ---
    tags:
      - Chatbot
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            user_id:
              type: string
            question:
              type: string
    responses:
      200:
        description: A JSON object with the chatbot response.
        schema:
          type: object
          properties:
            response:
              type: string
    """
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

def clean_conversation_history():
    while True:
        conversation_history.clear()
        sleep(86400)

if __name__ == '__main__':
    threading.Thread(target=clean_conversation_history).start()
    app.run(host='0.0.0.0', port=5000, debug=True)
