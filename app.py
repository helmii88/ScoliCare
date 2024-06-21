from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)


@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image = request.files['image']
    image_path = os.path.join("uploads", image.filename)
    image.save(image_path)

    try:
        # Run the executable with the image path as an argument
        result = subprocess.run(["Main.exe", image_path], capture_output=True, text=True)
        if result.returncode != 0:
            return jsonify({"error": "Error processing image", "details": result.stderr}), 500

        # Process the output from the executable
        output = result.stdout.strip()
        return jsonify({"result": output})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
