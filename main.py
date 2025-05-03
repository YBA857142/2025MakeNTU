from flask import Flask, send_from_directory, jsonify, request
import os
import base64
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='frontend', static_url_path='')

# Create directory to store captured images
IMAGES_DIR = 'images_working'
os.makedirs(IMAGES_DIR, exist_ok=True)

# Serve static files (HTML, CSS, JS) from /frontend
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_file(path):
    file_path = os.path.join(app.static_folder, path)
    if os.path.isfile(file_path):
        return send_from_directory(app.static_folder, path)
    else:
        return "404 Not Found", 404

# API Post endpoint for receiving images
@app.route('/api/image', methods=['POST'])
def receive_image():
    try:
        data = request.json
        
        if not data or 'imageData' not in data:
            return jsonify({"error": "No image data received"}), 400
        
        # Get image data and timestamp
        image_data = data.get('imageData')
        timestamp = int(round(datetime.now().timestamp() * 1000))
        
        # Save the image to disk
        filename = f"image_{timestamp}.jpg"
        file_path = os.path.join(IMAGES_DIR, filename)
        
        # Decode base64 and save to file
        with open(file_path, 'wb') as f:
            f.write(base64.b64decode(image_data))
        
        logger.info(f"Image saved: {filename}")
        
        return jsonify({
            "status": "success",
            "message": "Image received and saved",
            "filename": filename,
            "timestamp": timestamp
        })
    
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return jsonify({"error": str(e)}), 500

"""
# Endpoint to list all captured images
@app.route('/api/images', methods=['GET'])
def list_images():
    try:
        images = [f for f in os.listdir(IMAGES_DIR) if f.endswith('.jpg')]
        images.sort(reverse=True)  # Show newest first
        
        return jsonify({
            "count": len(images),
            "images": images
        })
    
    except Exception as e:
        logger.error(f"Error listing images: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Endpoint to retrieve a specific image
@app.route('/api/images/<filename>', methods=['GET'])
def get_image(filename):
    try:
        return send_from_directory(IMAGES_DIR, filename)
    except Exception as e:
        logger.error(f"Error retrieving image {filename}: {str(e)}")
        return jsonify({"error": str(e)}), 404
"""

if __name__ == '__main__':
    # For development only - use a production WSGI server in production
    app.run(host='0.0.0.0', port=80, debug=True)