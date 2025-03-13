from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)
CORS(app, resources={r"/remove-bg": {"origins": "*"}})  # ✅ Allow only /remove-bg route

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image_file = request.files['image']
    try:
        image = Image.open(image_file.stream)
        output = remove(image)

        img_io = io.BytesIO()
        output.save(img_io, format='PNG')
        img_io.seek(0)

        response = send_file(img_io, mimetype='image/png')
        response.headers["Access-Control-Allow-Origin"] = "*"  # ✅ CORS Fix
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)