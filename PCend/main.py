from flask import Flask, send_from_directory, jsonify, request
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__, static_folder='frontend', static_url_path='')

if __name__ == "__main__":
    """
    ███████╗██╗      █████╗ ███████╗██╗  ██╗
    ██╔════╝██║     ██╔══██╗██╔════╝██║ ██╔╝
    █████╗  ██║     ███████║███████╗█████╔╝ 
    ██╔══╝  ██║     ██╔══██║╚════██║██╔═██╗ 
    ██║     ███████╗██║  ██║███████║██║  ██╗
    ╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝                                 
    """

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

    # API Post endpoint for receiving cockroach position
    # position: (x, y)
    # color: (r, g, b)
    # has_cockroach: Boolean
    @app.route('/api/movement', methods=['POST'])
    def receive_position():
        global cur_pos
        global cur_rgb
        global has_cockroach

        try:
            data = request.json
            
            if (not data 
                or 'compassData' not in data
                or 'movementData' not in data
            ):
                return jsonify({"error": "No data received"}), 400
            
            # Get data for call_rpi()
            raw_compassData = data.get("compassData")
            raw_movementData = data.get("movementData")
            try:
                compassData = raw_compassData
            except:
                return jsonify({"error": "Wrong compassData format"}), 400
            try:
                movementData = raw_movementData
            except:
                return jsonify({"error": "Wrong color format"})
            
            return jsonify({"status": "success"})
        
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return jsonify({"error": str(e)}), 500

    # For development only - use a production WSGI server in production
    app.run(host='0.0.0.0', port=80, debug=False)