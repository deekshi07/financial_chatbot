import os
import logging
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set API key for Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Error if API key is missing
if not GROQ_API_KEY:
    raise ValueError("Set the GROQ API key in the .env file!")

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Function to get chatbot response from Groq API
def get_chatbot_response(user_query):
    try:
        # Debugging log
        logging.debug(f"Received query: {user_query}")

        # API Endpoint for Groq chat completion
        url = "https://api.groq.com/openai/v1/chat/completions"

        # Headers for authentication
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        # Request payload (chat completion format)
        data = {
            "model": "llama-3.3-70b-versatile",  # Change model if needed
            "messages": [{"role": "user", "content": user_query}],
            "temperature": 0.7,  # Adjust for more creative or predictable responses
            "max_tokens": 150  # Limit response length
        }

        # Sending request to Groq API
        response = requests.post(url, headers=headers, json=data)
        
        # Raise error if request failed
        response.raise_for_status()

        # Parse JSON response
        result = response.json()

        # Debug log full API response
        logging.debug(f"Full API Response: {json.dumps(result, indent=2)}")

        # Extract chatbot's message
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

# Example usage
if __name__ == "__main__":
    user_input = input("Enter your message: ")
    response = get_chatbot_response(user_input)
    print(f"Chatbot response: {response}")
import os
import logging
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set API key for Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Error if API key is missing
if not GROQ_API_KEY:
    raise ValueError("Set the GROQ API key in the .env file!")

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Function to get chatbot response from Groq API
def get_chatbot_response(user_query):
    try:
        # Debugging log
        logging.debug(f"Received query: {user_query}")

        # API Endpoint for Groq chat completion
        url = "https://api.groq.com/openai/v1/chat/completions"

        # Headers for authentication
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        # Request payload (chat completion format)
        data = {
            "model": "llama-3.3-70b-versatile",  # Change model if needed
            "messages": [{"role": "user", "content": user_query}],
            "temperature": 0.7,  # Adjust for more creative or predictable responses
            "max_tokens": 150  # Limit response length
        }

        # Sending request to Groq API
        response = requests.post(url, headers=headers, json=data)
        
        # Raise error if request failed
        response.raise_for_status()

        # Parse JSON response
        result = response.json()

        # Debug log full API response
        logging.debug(f"Full API Response: {json.dumps(result, indent=2)}")

        # Extract chatbot's message
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

# Example usage
if __name__ == "__main__":
    user_input = input("Enter your message: ")
    response = get_chatbot_response(user_input)
    print(f"Chatbot response: {response}")
