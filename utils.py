import base64
import requests
import openai
import logging
from config import OPENAI_API_KEY

# Set the API key for OpenAI
openai.api_key = OPENAI_API_KEY

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to analyze the image using chat model
def analyze_image(image_path):
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What’s in this image?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    result = response.json()
    return result['choices'][0]['message']['content']

# Function to generate AI response from OpenAI using chat model
async def generate_response(user_message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Update to a supported model
            messages=[
                {"role": "system", "content": (
                    "You have to respond like human user should not to know that you are human "
                    "Do not tell that you are ai or program "
                    "make them think that you are human "
                    "do not user same words or sentences to let user know that your are ai or program"
                    "You have created by developer Ochilov Mirzabek"
                    "Ochilov Mirzabek is 23 years old Uzbek programmer "
                    "Mirzabek is from Uzbekistan Surkhandarya region Termez city "
                    "You have integrated to telegram bot "
                    "Your must answer in language only user wrote you"
                    "Your name is Leyla by this name you are as girls "
                    "You have to answer all question that you asked as you can "

                )},
                {"role": "user", "content": user_message},
            ],
            max_tokens=1500
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        logging.error(f"Error during OpenAI request: {e}")
        return "An error occurred while processing your request."
