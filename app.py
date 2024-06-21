from flask import Flask, request, jsonify
import subprocess
import os
import re

app = Flask(__name__)

# Directory to save uploaded images
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def run_executable(image_path):
    try:
        result = subprocess.run([r'C:\Users\mido\OneDrive\Desktop\git uploads\ScoliCare\Main.exe', image_path], check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output}"


def extract_cobb_angle(result_str):
    match = re.search(r'Cobb Angle: ([\d.]+)', result_str)
    if match:
        return float(match.group(1))
    return None


def extract_classification(result_str):
    match = re.search(r'Classification: (\w+)', result_str)
    if match:
        return match.group(1)
    return None


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image part in the request"}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No image selected for uploading"}), 400
    if file:
        image_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(image_path)

        # Run the executable with the image path
        result = run_executable(image_path)

        # Extract Cobb angle and classification from the result
        cobb_angle = extract_cobb_angle(result)
        classification = extract_classification(result)

        if cobb_angle is None or classification is None:
            return jsonify({"error": "Failed to extract Cobb angle or classification"}), 500

        return jsonify({"cobb_angle": cobb_angle, "classification": classification})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 4000))
    app.run(host='0.0.0.0', port=port)
    app.run(debug=True)
