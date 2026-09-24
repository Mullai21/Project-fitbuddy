from google import genai
import os
import logging

def generate_workout_gemini(goal: str, intensity: str, age: int, weight: float) -> str:
    try:
        client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
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

        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=prompt
        )
        return response.text
    except Exception as e:
        logging.error(f"Error generating workout plan: {e}")
        return "⚠️ We couldn't generate your workout plan right now. Please try again in a moment. If the issue persists, check your API key configuration."
