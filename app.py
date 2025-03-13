from flask import Flask, request, send_file
from flask_cors import CORS  # Import CORS
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return {'error': 'No image file provided'}, 400

    image_file = request.files['image']
    image = Image.open(image_file.stream)

    output = remove(image)
    
    img_io = io.BytesIO()
    output.save(img_io, format='PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
