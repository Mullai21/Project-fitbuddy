from google import genai
import os
import logging

def update_workout_plan(original_plan: str, feedback: str) -> str:
    try:
        client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
        prompt = f"""You are a clinical fitness coach refining an existing program. Below is the original 7-day workout plan and the user's feedback.

Original Plan:
{original_plan}

User Feedback:
{feedback}

Modify ONLY the aspects required by the feedback (e.g., swapping barbell movements to dumbbell variations for joint discomfort, adjusting the weekly split). Keep unaffected days, volume safety, and the exact formatting intact. Return the complete revised 7-day plan in the same Markdown format."""

        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=prompt
        )
        return response.text
    except Exception as e:
        logging.error(f"Error updating workout plan: {e}")
        return "⚠️ We couldn't update your workout plan right now. Please try again in a moment. If the issue persists, check your API key configuration."
