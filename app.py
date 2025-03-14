from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io
import logging

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

# ✅ Setup logging
logging.basicConfig(level=logging.INFO)

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image_file = request.files['image']
    
    try:
        # ✅ Open image safely
        image = Image.open(image_file.stream)

        # ✅ Remove background
        output = remove(image)

        # ✅ Convert to BytesIO
        img_io = io.BytesIO()
        output.save(img_io, format='PNG')
        img_io.seek(0)

        logging.info("Background removed successfully!")
        
        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name="processed-image.png")

    except Exception as e:
        logging.error(f"Error processing image: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
