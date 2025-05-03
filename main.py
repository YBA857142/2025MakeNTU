from flask import Flask, send_from_directory, jsonify, request
import os

app = Flask(__name__, static_folder='frontend', static_url_path='')

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

# API Post endpoints
@app.route('/api/echo', methods=['POST'])
def api_echo():
    data = request.json
    return jsonify({"you_sent": data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
