from google import genai
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Ensure .env is loaded
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / '.env')
load_dotenv()

MODELS = ['gemini-3.6-flash', 'gemini-3.5-flash', 'gemini-3.5-flash-lite', 'gemini-3.1-flash-lite']

def update_workout_plan(original_plan: str, feedback: str) -> str:
    prompt = f"""You are a clinical fitness coach refining an existing program. Below is the original 7-day workout plan and the user's feedback.

Original Plan:
{original_plan}

User Feedback:
{feedback}

Modify ONLY the aspects required by the feedback (e.g., swapping barbell movements to dumbbell variations for joint discomfort, adjusting the weekly split). Keep unaffected days, volume safety, and the exact formatting intact. Return the complete revised 7-day plan in the same Markdown format."""

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

        logging.error(f"Error updating workout plan across all models: {last_error}")
        return "⚠️ We couldn't update your workout plan right now. Please try again in a moment. If the issue persists, check your API key configuration."
    except Exception as e:
        logging.error(f"Error initializing Gemini client: {e}")
        return "⚠️ We couldn't update your workout plan right now. Please try again in a moment. If the issue persists, check your API key configuration."
