from flask import Flask, request, Response
import requests
import urllib.parse

app = Flask(__name__)

TARGET_URL = "http://10.10.32.179"

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def proxy(path):
    # Build the target URL
    target_url = f"{TARGET_URL}/{path}"
    
    # Get request headers and exclude some headers that might cause issues
    headers = {key: value for key, value in request.headers.items()
               if key.lower() not in ('host', 'content-length')}
    
    # Get query string parameters
    args = request.args
    
    try:
        # If there are query parameters, append them to the target URL
        if args:
            target_url = f"{target_url}?{urllib.parse.urlencode(args, doseq=True)}"
        
        # Forward the request to the target server
        response = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            stream=True
        )
        
        # Create a Flask response object
        proxy_response = Response(
            response=response.content,
            status=response.status_code
        )
        
        # Add headers from the target response to our response
        for header, value in response.headers.items():
            # Skip headers that Flask/Werkzeug will set
            if header.lower() not in ('content-length', 'connection', 'content-encoding', 'transfer-encoding'):
                proxy_response.headers[header] = value
                
        return proxy_response
    
    except requests.exceptions.RequestException as e:
        return f"Error proxying request: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)