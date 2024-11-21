# Import the Python SDK
import google.generativeai as genai
# Used to securely store your API key
from google.colab import userdata
import json

# API key configuration
GOOGLE_API_KEY = userdata.get('API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Gemini model configuration
model = genai.GenerativeModel('gemini-1.5-flash')

# Functions to calculate BMR and TDEE
def calculate_bmr(weight, height, age, gender):
    """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation."""
    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    return bmr

def calculate_tdee(bmr, activity_level):
    """Calculate Total Daily Energy Expenditure based on activity level."""
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very active': 1.9
    }
    return bmr * activity_multipliers.get(activity_level, 1.2)

# # Function to filter questions based on fitness topics
# def is_fitness_related(question):
#     fitness_keywords = ["fitness", "diet", "gym", "exercise", "nutrition", "workout", "calories", "muscle", "fat loss"]
#     return any(keyword in question.lower() for keyword in fitness_keywords)

# Main chatbot conversation
print("Hello! Welcome to NutriFit AI Chatbot. How can I help you today?")
print("1. I want to find something in the app.")
print("2. Personalized Diet and Fitness plan with NutriAI")
print("3. Question & Answer with NutriAI")
print("4. Chat with manager")
choice = input("Enter your choice: ")

if choice == "1":
    print("What do you want to find in the app?")
    
    # User inputs their request in natural language
    user_input = input("Enter what you are looking for: ")

    # Use Gemini AI to analyze the user's input
    if is_fitness_related(user_input):
        response = model.generate_content(user_input)
        intent = response.candidates[0]

        # Map AI-generated intent to app sections
        if "recipe" in intent or "cook" in intent or "meal" in intent:
            print("Click here to view recipes: app://nutrifit/recipes")
        elif "workout" in intent or "exercise" in intent:
            print("Click here to view workouts: app://nutrifit/workouts")
        elif "diet" in intent or "plan" in intent:
            print("Click here to view diet plans: app://nutrifit/dietplans")
        elif "supplement" in intent or "vitamin" in intent:
            print("Click here to view supplements: app://nutrifit/supplements")
        else:
            print("Sorry, I couldn't find what you're looking for. Please try again.")
    else:
        print("Please ask a question related to fitness, gym, or diet.")
      
elif choice == "2":
    # Get user data for personalized fitness recommendations
    name = input("What is your name? ")
    age = int(input("What is your age? "))
    weight = float(input("What is your weight (kg)? "))
    height = float(input("What is your height (cm)? "))
    gender = input("What is your gender (male/female)? ").lower()
    activity_level = input("What is your activity level (sedentary, light, moderate, active, very active)? ").lower()
    goal = input("What is your fitness goal (muscle gain, fat loss, etc.)? ").lower()

    # Calculate BMR and TDEE
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = calculate_tdee(bmr, activity_level)

    # Create personalized prompt for Gemini AI
    prompt = f"""
    The user is {name}, a {age}-year-old {gender} who weighs {weight} kg and is {height} cm tall. 
    Their fitness goal is {goal}, and their activity level is {activity_level}. 
    Their Total Daily Energy Expenditure (TDEE) is {tdee} calories. 
    Based on this information, provide specific advice regarding daily calorie intake, macronutrient ratios, 
    and a personalized workout plan.
    """

    # Get a response from Gemini AI
    response = model.generate_content(prompt)

    # Display personalized response
    print(response.text)

    # Store user data in JSON file
    user_data = {
        "name": name,
        "age": age,
        "weight": weight,
        "height": height,
        "gender": gender,
        "activity_level": activity_level,
        "goal": goal,
        "bmr": bmr,
        "tdee": tdee,
        "personalized_advice": response.text
    }

    with open('user_data.json', 'w') as f:
        json.dump(user_data, f)

    print("User data and personalized advice stored successfully.")
    
elif choice == "3":
    print("You are now chatting with NutriAI. Type 'exit' to end the chat.")
    
    # Initialize an empty list to store conversation history
    conversation_history = []

    while True:
        # Get user question for NutriAI
        question = input("What is your question for NutriAI? ")

        # Exit the loop if the user types 'exit'
        if question.lower() == 'exit':
            print("Thank you for chatting with NutriAI. Goodbye!")
            break

        # Add user input to conversation history
        conversation_history.append(f"User: {question}")

        # Build prompt with conversation history for Gemini
        # Keep previous exchanges in the prompt for context
        conversation_context = "\n".join(conversation_history)
        prompt = f"""
        You are NutriAI, a fitness chatbot. You are in a conversation with the user. 
        The user is asking fitness-related questions about gym, diet, workouts, or health.
        Provide responses only if the question is relevant to fitness.
        
        Conversation history:
        {conversation_context}

        Respond appropriately to the user's latest message.
        """

        # Get a response from Gemini AI
        response = model.generate_content(prompt)

        # Display the response
        answer = response.text
        print(answer)

        # Add AI's response to conversation history
        conversation_history.append(f"NutriAI: {answer}")
elif choice == "4":
    # Contact via Github
    hyperlink_format = '<a href="https://github.com/whorvn/NutriFit">Contact us via WhatsApp</a>'
    print(hyperlink_format)
    
else:
    print("Invalid choice. Please try again.")
