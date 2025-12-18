# ai_integration/analyze_plate.py

from openai import OpenAI
from dotenv import load_dotenv
import os
import base64

load_dotenv()  # <-- REQUIRED HERE

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def analyze_plate(image_path: str, prompt: str) -> str:
    with open(image_path, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode()

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                           "url": f"data:image/png;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
