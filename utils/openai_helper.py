import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_openai(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            timeout=10,
            messages=[
                {"role": "system", "content": "You are a helpful voice assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return "Sorry, there was an error processing your request."
