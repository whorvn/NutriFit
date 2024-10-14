# Import the Python SDK
import google.generativeai as genai
# Used to securely store your API key
from google.colab import userdata

GOOGLE_API_KEY=userdata.get('API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

#ask user for if he wants to find something in app or want to use ai chatbot for fitness
print("Hello! Welcome to NutriFit AI Chatbot. How can I help you today?")
print("1. I want to find something in the app.")
print("2. I want to use AI chatbot for fitness.")
choice = input("Enter your choice: ")
if choice == "1":
    #navigating user for endpoints based and analyzed on his/her request
    print("What do you want to find in the app?")
    print("1. Find a recipe.")
    print("2. Find a workout.")
    print("3. Find a diet plan.")
    print("4. Find a supplement.")
    choice = input("Enter your choice: ")
    #based on choice make it possible for user that he can navigate with touching answer of chatbot (answer of chatbot is linked to endpoint of flutter)
    #in final version user wont need ente manual, in-app he will touch text-bubbles 
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
if choice == "2":
    #get user data's from flatter database(firebase) and use them when answering user question
    
    
        