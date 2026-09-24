from google import genai
import os
import logging

def generate_nutrition_tip_with_flash(goal: str) -> str:
    try:
        client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
        prompt = f"""You are an evidence-based sports nutritionist. Provide a concise, practical, and scientifically sound nutrition or recovery tip (maximum 3 sentences) for someone whose fitness goal is: {goal}.

Guidelines:
- Muscle Gain: Emphasize daily protein intake (1.6-2.2 g/kg), protein distribution, and a modest caloric surplus (250-400 kcal).
- Weight Loss: Focus on a sustainable caloric deficit, dietary fiber for satiety, and non-exercise activity thermogenesis (NEAT).
- General: Prioritize hydration, sleep hygiene (7-9 hours), and micronutrient variety. No detox teas, crash diets, or arbitrary food demonization."""

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        logging.error(f"Error generating nutrition tip: {e}")
        return "⚠️ We couldn't generate your nutrition tip right now. Please try again in a moment. If the issue persists, check your API key configuration."
