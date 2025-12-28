import os
import json
from google import genai
from google.genai import types
from PIL import Image
import io

# --- CONFIGURATION ---
# Replace with your actual API key or set it as an environment variable
API_KEY = os.getenv("API_KEY")
print(f"API_KEY: {API_KEY}")

def analyze_sleep(sleep_data):
    client = genai.Client(api_key=API_KEY)

    # 1. Load the image
    # try:
    #     image = Image.open(image_path)
    # except Exception as e:
    #     return {"error": f"Could not load image: {e}"}

    # 2. Define the prompt (The "Brain" of the operation)
    # We ask for JSON specifically so your app can parse it easily later.

    # prompt = """
    # You are an expert nutritionist and food analyst. Analyze the provided image of food.

    # Identify every food item in the picture. For each item, estimate:
    # 1. The Name of the food.
    # 2. The Portion Quantity (e.g., '1 cup', '2 slices', 'approx 150g'). Use visual cues to estimate size.
    # 3. Calories (kcal) for that portion.
    # 4. Macronutrients (Protein, Carbs, Fat) in grams.

    # Finally, provide a total calorie count for the entire meal.

    # Return the result ONLY as a raw JSON object with this structure:
    # {
    #     "items": [
    #         {
    #             "name": "Food Name",
    #             "quantity_estimate": "Quantity",
    #             "calories": 0,
    #             "nutrients": {
    #                 "protein_g": 0,
    #                 "carbs_g": 0,
    #                 "fat_g": 0,
    #                 ....
    #             }
    #         }
    #     ],
    #     "total_calories": 0,
    #     "health_rating_1_to_10": 0,
    #     "brief_summary": "A short 1-sentence summary of the meal's nutritional value.",
    #     "Is this really the right meal?": is this actually what you predicted? like is this actually paneer tikka pizza or cheeze pizza"
    # }
    # """

    prompt = f"""
        You are a health assistant.

        Analyze the following sleep data for today and explain the effects of irregular sleep. The Sleep data is in UTC format convert it into IST and answer basaed on IST timings.

        Sleep data:
        {sleep_data}

        Explain everything in very simple, user-friendly language, as if talking to someone without a medical background. Use relatable examples (such as hunger timing, bloating, low energy, or irritability) and practical, actionable advice. Also, include comments on how today's sleep pattern interacts with the user's natural circadian rhythm.

        Return the result ONLY as a raw JSON object with the following structure (no markdown, no extra text):

        {{
            "digestive_system_impact": {{
                "summary": "Simple explanation of how today's sleep pattern may affect digestion",
                "possible_symptoms": [
                    "symptom 1",
                    "symptom 2"
                ],
                "why_this_happens": "Short, easy explanation linking sleep timing and digestion"
            }},
            "liver_and_metabolism_impact": {{
                "summary": "Simple explanation of how irregular sleep may affect the liver or metabolism",
                "possible_effects": [
                    "effect 1",
                    "effect 2"
                ],
                "why_this_happens": "Easy explanation related to circadian rhythm, hormones, or energy processing"
            }},
            "circadian_rhythm_comment": {{
                "summary": "Brief comment on how today's sleep aligns or misaligns with natural circadian rhythm",
                "possible_implications": [
                    "implication 1",
                    "implication 2"
                ],
                "why_this_happens": "Simple explanation of circadian disruption or alignment"
            }},
            "practical_advice": {{
                "overall_tip": "One-line overall advice",
                "actionable_steps": [
                    "step the user can do today",
                    "step the user can do today",
                    "step the user can do today"
                ],
                "food_and_timing_tip": "Simple suggestion related to meal timing or food choices",
                "sleep_improvement_tip": "Small, realistic suggestion to improve tonight's sleep"
            }},
            "overall_health_signal": {{
                "severity": "LOW | MODERATE | HIGH",
                "one_line_summary": "Short, reassuring 1-sentence summary for the user"
            }}
        }}
    """



    # 3. Call the Gemini 1.5 Flash API
    try:
        response = client.models.generate_content(
            model="gemini-robotics-er-1.5-preview",
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json" # Forces valid JSON output
            )
        )

        # 4. Parse and Return
        return json.loads(response.text)

    except Exception as e:
        return {"error": f"API Request failed: {e}"}

# --- TEST THE APP ---
if __name__ == "__main__":
    # Create a dummy image or use a real path like "my_lunch.jpg"
    img_path = "food.jpg"
    img_path1 = "food.jpeg"

    # Check if file exists before running
    if os.path.exists(img_path):
        print("Scanning food... Please wait...")
        result = analyze_food_image(img_path)

        # Pretty print the result
        print(json.dumps(result, indent=2))
    elif os.path.exists(img_path1):
        print("Scanning food... Please wait...")
        result = analyze_food_image(img_path1)

        # Pretty print the result
        print(json.dumps(result, indent=2))
    else:
        print(f"Please place an image named '{img_path}' or '{img_path1}' in this folder to test.")

