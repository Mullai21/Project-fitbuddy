from google import genai
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Ensure .env is loaded
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / '.env')
load_dotenv()

MODELS = ['gemini-3.6-flash', 'gemini-3.5-flash', 'gemini-3.5-flash-lite', 'gemini-3.1-flash-lite']

def generate_nutrition_tip_with_flash(goal: str) -> str:
    prompt = f"""You are an evidence-based sports nutritionist. Provide a concise, practical, and scientifically sound nutrition or recovery tip (maximum 3 sentences) for someone whose fitness goal is: {goal}.

Guidelines:
- Muscle Gain: Emphasize daily protein intake (1.6-2.2 g/kg), protein distribution, and a modest caloric surplus (250-400 kcal).
- Weight Loss: Focus on a sustainable caloric deficit, dietary fiber for satiety, and non-exercise activity thermogenesis (NEAT).
- General: Prioritize hydration, sleep hygiene (7-9 hours), and micronutrient variety. No detox teas, crash diets, or arbitrary food demonization."""

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

        logging.error(f"Error generating nutrition tip across all models: {last_error}")
        return "⚠️ We couldn't generate your nutrition tip right now. Please try again in a moment. If the issue persists, check your API key configuration."
    except Exception as e:
        logging.error(f"Error initializing Gemini client: {e}")
        return "⚠️ We couldn't generate your nutrition tip right now. Please try again in a moment. If the issue persists, check your API key configuration."
