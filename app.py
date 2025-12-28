from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
from food_detection import analyze_food_image
from sleepAnalytics import analyze_sleep

from dotenv import load_dotenv
load_dotenv()  # This will load the variables from .env


app = Flask(__name__)
CORS(app)

# Set a limit for the maximum allowed payload (e.g., 16MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/process-image', methods=['POST'])
def process_image():
    # 1. Check if the file is part of the request
    if 'image' not in request.files:
        return jsonify({"error": "No image part in the request"}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({"error": "No image selected for uploading"}), 400

    try:
        # 2. Open the image using Pillow
        img = Image.open(file.stream)
        
        # 3. Perform some basic logic (e.g., get metadata)
        width, height = img.size
        format = img.format
        mode = img.mode

        #My food detection
        output = analyze_food_image(img)

        # 4. Return a JSON response
        return output, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/sleepAnalysis', methods=['POST'])
def sleep_analysis():
    try:
        sleep_data = request.get_json()

        if not sleep_data:
            return jsonify({"error": "Request body is required"}), 400

        result = analyze_sleep(sleep_data)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)