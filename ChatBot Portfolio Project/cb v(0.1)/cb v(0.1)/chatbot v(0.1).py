# Import the Python SDK
import google.generativeai as genai
# Used to securely store your API key
# from google.colab import userdata
import json

GOOGLE_API_KEY="AIzaSyACNkBzvg7M-Ks3szJMSkp_8ks9aB0ZqPE"
genai.configure(api_key=GOOGLE_API_KEY)
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

# Main chatbot conversation
print("Hello! Welcome to NutriFit AI Chatbot. How can I help you today?")
print("1. I want to find something in the app.")
print("2. Personalized Diet and Fitness plan with NutriAI")
print("3. Quetion&Answer with NutriAI")
choice = input("Enter your choice: ")

if choice == "1":
    # Navigate to app sections based on user's choice
    print("What do you want to find in the app?")
    print("1. Find a recipe.")
    print("2. Find a workout.")
    print("3. Find a diet plan.")
    print("4. Find a supplement.")
    choice = input("Enter your choice: ")
    if choice == "1":
        print("Click here to view recipes: app://nutrifit/recipes")
    elif choice == "2":
        print("Click here to view workouts: app://nutrifit/workouts")
    elif choice == "3":
        print("Click here to view diet plans: app://nutrifit/dietplans")
    elif choice == "4":
        print("Click here to view supplements: app://nutrifit/supplements")
    else:
        print("Invalid choice.")
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

    # Display personalized response
    # print(response.text)

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
    # Get user question for NutriAI
    question = input("What is your question for NutriAI? ")
    
    # Get a response from Gemini AI
    response = model.generate_content(question)

    # Display personalized response
    print(response.text)
    
else:
    print("Invalid choice. Please try again.")