import os
import logging
import requests
import json
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("Set the GROQ API key in the .env file!")

logging.basicConfig(level=logging.DEBUG)

def get_chatbot_response(user_query):
    try:
        logging.debug(f"Received query: {user_query}")

        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        # Added system message for restricting responses to finance domain
        data = {
            "model": "llama3-8b-8192",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant that ONLY answers financial-related questions. "
                        "If the question is not related to finance, politely say you can only answer financial questions."
                    )
                },
                {
                    "role": "user",
                    "content": user_query
                }
            ],
            "temperature": 0.7,
            "max_tokens": 150
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        result = response.json()
        logging.debug(f"Full API Response: {json.dumps(result, indent=2)}")

        chat_response = result["choices"][0]["message"]["content"].strip()

        if not chat_response:
            raise ValueError("Empty response from the API.")

        logging.debug(f"Response: {chat_response}")
        return chat_response

    except requests.exceptions.RequestException as e:
        logging.error(f"API Request Error: {e}")
        return "An error occurred while communicating with the chatbot."
    except Exception as e:
        logging.error(f"Unexpected Error: {e}")
        return "An unexpected error occurred."

if __name__ == "__main__":
    user_input = input("Enter your message: ")
    response = get_chatbot_response(user_input)
    print(f"Chatbot response: {response}")
