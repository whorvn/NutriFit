# NutriFit AI Chatbot

Welcome to **NutriFit AI Chatbot**, a personalized fitness assistant built using Google’s Gemini AI. This chatbot provides personalized nutrition and workout advice based on the user’s fitness data. It integrates with Firebase to retrieve user details and delivers custom responses via AI.

## Features

- **Personalized Fitness Advice**: Get tailored fitness recommendations based on user data such as age, weight, height, activity level, and fitness goals.
- **Google Gemini AI Integration**: Uses Gemini AI (Google's AI model) to provide intelligent responses for nutrition and fitness queries.
- **User Data Management**: Store and retrieve user data (e.g., calorie intake, BMR, TDEE) for a seamless experience.
- **In-App Navigation**: Directs users to specific sections of a fitness app via clickable text bubbles.

## Tech Stack

- **Google Gemini AI** for AI-driven conversations
- **Python** for backend scripting
- **Firebase** for user data storage and retrieval
- **Google Colab** for API key management and testing

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/nutrifit-ai-chatbot.git
    ```

2. **Install Dependencies**:
    Navigate to the project directory and install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up API Key**:
    - Obtain your API key from [Google Cloud](https://cloud.google.com/).
    - In Google Colab, store your API key securely using the following code:
      ```python
      from google.colab import userdata
      GOOGLE_API_KEY = userdata.get('API_KEY')
      ```

4. **Set up Firebase**:
    - Follow the steps on [Firebase](https://firebase.google.com/) to create your Firebase project and configure it in your code.

## Usage

1. **Running the Chatbot**:
    - Launch the Python script in your preferred environment (Google Colab is recommended).
    - The chatbot will ask for your fitness preferences and goals.
    - Based on your data, the chatbot will provide personalized fitness advice using the Gemini AI.

2. **Example of Personalized Responses**:
    - The chatbot calculates your Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE) based on inputs such as age, height, weight, and activity level.
    - It then provides suggestions on calorie intake and a workout plan.

3. **In-App Navigation**:
    - When using the chatbot within a fitness app, users can click on options like "Find a recipe" or "Find a workout" to navigate directly to the respective sections.

## Example Code

```python
# Import the Python SDK
import google.generativeai as genai

# Example to get personalized fitness advice
response = model.generate(text="I want to lose fat and improve strength.")
print(response.generations[0].text)

