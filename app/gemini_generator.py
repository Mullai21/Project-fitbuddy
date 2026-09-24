from google import genai
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Ensure .env is loaded
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / '.env')
load_dotenv()

MODELS = ['gemini-3.6-flash', 'gemini-3.5-flash', 'gemini-3.5-flash-lite', 'gemini-3.1-flash-lite']

def generate_workout_gemini(goal: str, intensity: str, age: int, weight: float) -> str:
    prompt = f"""You are an elite, evidence-based Strength & Conditioning Specialist. Design a safe, scientific 7-day training split for the following user profile:
- Age: {age}
- Weight: {weight} kg
- Fitness Goal: {goal}
- Workout Intensity: {intensity}

Core Principles:
- Prescribe intensity using Reps in Reserve (RIR) or Rate of Perceived Exertion (RPE).
- Ensure 10-20 working sets per target muscle group per week.
- Order compound multi-joint movements first, followed by isolation work.
- Include 1-2 active recovery or complete rest days to manage systemic fatigue.

Format: Output clean Markdown. Each day must include:
## Day X: [Focus Area]
### Dynamic Warm-up (5-10 min)
### Main Workout
| Exercise | Sets | Reps | Rest (sec) | Target RIR |
### Cooldown"""

    try:
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            logging.error("GOOGLE_API_KEY environment variable is not set.")
            return "⚠️ API Key not configured. Please set GOOGLE_API_KEY in your .env file."

        client = genai.Client(api_key=api_key)
        
        last_error = None
        for model_name in MODELS:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                logging.warning(f"Failed with {model_name}: {e}")
                last_error = e

        logging.error(f"Error generating workout plan across all models: {last_error}")
        return "⚠️ We couldn't generate your workout plan right now. Please try again in a moment. If the issue persists, check your API key configuration."
    except Exception as e:
        logging.error(f"Error initializing Gemini client: {e}")
        return "⚠️ We couldn't generate your workout plan right now. Please try again in a moment. If the issue persists, check your API key configuration."
