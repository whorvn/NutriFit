import threading
from time import sleep
from flask import Flask, render_template, request, jsonify
from flasgger import Swagger
import google.generativeai as genai
import json

app = Flask(__name__)

conversation_history = dict()

# Configure Google API

GOOGLE_API_KEY = 'AIzaSyB_8Kay0ZASSYflMblOdcnAp37qcHveRDE'
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    raise RuntimeError("Failed to initialize the Generative AI model") from e

def calculate_bmr(weight, height, age, gender):
    try:
        if gender == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        elif gender == 'female':
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        else:
            raise ValueError("Invalid gender. Must be 'male' or 'female'.")
        return bmr
    except Exception as e:
        raise ValueError(f"Error calculating BMR: {e}") from e

def calculate_tdee(bmr, activity_level):
    try:
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very active': 1.9
        }
        return bmr * activity_multipliers.get(activity_level, 1.2)
    except Exception as e:
        raise ValueError(f"Error calculating TDEE: {e}") from e

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error loading the index page: {e}", 500

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
    try:
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
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {e}"}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

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
    try:
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
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {e}"}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

def clean_conversation_history():
    while True:
        try:
            conversation_history.clear()
            sleep(86400)
        except Exception as e:
            print(f"Error in cleaning conversation history: {e}")

if __name__ == '__main__':
    try:
        # threading.Thread(target=clean_conversation_history).start()
        # import logging
        # logging.basicConfig(level=logging.DEBUG)
        swagger = Swagger(app)
        app.run(host="0.0.0.0", port=5000, debug=True)
    except Exception as e:
        print(f"Error starting the application: {e}")
