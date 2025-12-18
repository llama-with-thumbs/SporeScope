import sys
from pathlib import Path
from ai_integration.analyze_plate import analyze_plate

BASE_PROMPT = """
You are a mycology lab assistant.
Analyze agar plate images conservatively.
Keep responses under 50 words.
"""

def chatgpt_client(image_path: str, cycle_data: str) -> str:
    prompt = BASE_PROMPT + "\n\n" + cycle_data
    return analyze_plate(image_path, prompt)