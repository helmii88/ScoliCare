from flask import Flask, request, jsonify
import subprocess
import os


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/upload/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Save the uploaded file temporarily
    temp_image_path = 'temp_image.jpg'
    file.save(temp_image_path)

    try:
        # Execute the .exe file with the temporary image as an argument
        cmd = ['C:/Users/mido/apii/Exe file/Main/Main.exe', temp_image_path]
        subprocess.run(cmd, check=True)
        
        # Read the results
        with open('results.txt', 'r') as f:
            result_data = f.read()
        return jsonify({'result': result_data})
    except subprocess.CalledProcessError as e:
        # Check if an error log was generated
        if os.path.exists('error.log'):
            with open('error.log', 'r') as f:
                error_log = f.read()
            return jsonify({'error': f'Error executing the .exe file: {error_log}'})
        else:
            return jsonify({'error': f'Error executing the .exe file: {str(e)}'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 4000))
    app.run(host='0.0.0.0', port=port)
    app.run(debug=True)
