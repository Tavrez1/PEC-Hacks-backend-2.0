import os
import json
from google import genai
from google.genai import types
from PIL import Image
import io

# --- CONFIGURATION ---
# Replace with your actual API key or set it as an environment variable

def analyze_food_image(image):
    client = genai.Client(api_key=os.getenv("API_KEY"))

    # 1. Load the image
    # try:
    #     image = Image.open(image_path)
    # except Exception as e:
    #     return {"error": f"Could not load image: {e}"}

    # 2. Define the prompt (The "Brain" of the operation)
    # We ask for JSON specifically so your app can parse it easily later.
    prompt = """
    You are an expert nutritionist and food analyst. Analyze the provided image of food.

    Identify every food item in the picture. For each item, estimate:
    1. The Name of the food.
    2. The Portion Quantity (e.g., '1 cup', '2 slices', 'approx 150g'). Use visual cues to estimate size.
    3. Calories (kcal) for that portion.
    4. Macronutrients (Protein, Carbs, Fat) in grams.

    Finally, provide a total calorie count for the entire meal.

    Return the result ONLY as a raw JSON object with this structure:
    {
        "items": [
            {
                "name": "Food Name",
                "quantity_estimate": "Quantity",
                "calories": 0,
                "nutrients": {
                    "protein_g": 0,
                    "carbs_g": 0,
                    "fat_g": 0,
                    ....
                }
            }
        ],
        "total_calories": 0,
        "health_rating_1_to_10": 0,
        "brief_summary": "A short 1-sentence summary of the meal's nutritional value.",
        "Is this really the right meal?": is this actually what you predicted? like is this actually paneer tikka pizza or cheeze pizza"
    }
    """

    # 3. Call the Gemini 1.5 Flash API
    try:
        response = client.models.generate_content(
            model="gemini-robotics-er-1.5-preview",
            contents=[prompt, image],
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

