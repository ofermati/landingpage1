from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import openai

app = Flask(__name__)

# Load environment variables from the .env file
load_dotenv()

# OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def request_chat_gpt(user_message):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return completion.choices[0].message['content']
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""  # Return an empty string or handle the error appropriately

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve form data
        destination = request.form.get('destination')
        duration = request.form.get('duration')
        travel_companion = request.form.get('travel_companion')
        vacation_style = request.form.get('vacation_style')

        # Create a user message for ChatGPT
        user_message = f"I'm planning a {vacation_style} vacation to {destination} for {duration} days with {travel_companion}. Any recommendations?"

        # Get response from ChatGPT (in practice, you'd get this from the API)
        chatgpt_response = request_chat_gpt(user_message)

        # Debug print to check response
        print(chatgpt_response)

        # Gather the form data
        selected_options = {
            'Destination': destination,
            'Duration': duration,
            'Travel Companion': travel_companion,
            'Vacation Style': vacation_style
        }

        # Render the result page with the gathered data
        return render_template('planingTrip.html', selected_options=selected_options, chatgpt_response=chatgpt_response)

    # Render the form page if the request is GET
    return render_template('landingpage.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
