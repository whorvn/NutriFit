from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import json

app = Flask(__name__)

# Configure Google API
GOOGLE_API_KEY = 'AIzaSyA5x0J0Pqjuv8l7OtbrJWn3aTEZz-kLgGE'  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Functions to calculate BMR and TDEE
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
    question = request.json['question']
    prompt = f"""
    You are NutriAI, a fitness chatbot. You are in a conversation with the user.
    The user is asking fitness-related questions about gym, diet, workouts, or health.
    Provide responses only if the question is relevant to fitness.

    Conversation history:
    {question}

    Respond appropriately to the user's latest message.
    """

    response = model.generate_content(prompt)

    return jsonify({"response": response.text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1002, debug=True)