from flask import Flask, send_from_directory, jsonify, request
import os
import base64
from datetime import datetime
import logging
import RPi.GPIO as GPIO
import time
from rpi.motor_tt import motor_tt
from rpi.led import set_strip_color, clear_strip
from rpi_ws281x import PixelStrip, Color
from rpi.motor_servo import motor_servo

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='frontend', static_url_path='')

# Create directory to store captured images
IMAGES_DIR = 'images_working'
os.makedirs(IMAGES_DIR, exist_ok=True)

"""
███████╗███████╗████████╗██╗   ██╗██████╗ 
██╔════╝██╔════╝╚══██╔══╝██║   ██║██╔══██╗
███████╗█████╗     ██║   ██║   ██║██████╔╝
╚════██║██╔══╝     ██║   ██║   ██║██╔═══╝ 
███████║███████╗   ██║   ╚██████╔╝██║     
╚══════╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝     
"""

""" ==============================
            GPIO SETUP
    ============================== """
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

""" ==============================
            TT MOTOR
    ============================== """

PWMA = 32
AIN1 = 31
AIN2 = 33
BIN1 = 35
BIN2 = 37
PWMB = 38
motor_pins = [PWMA, AIN1, AIN2, BIN1, BIN2, PWMB]
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
pwm_A = GPIO.PWM(PWMA, 1000)
pwm_B = GPIO.PWM(PWMB, 1000)
pwm_A.start(0)
pwm_B.start(0)

""" ==============================
            LED
    ============================== """
LED_COUNT = 11
LED_PIN = 18
LED_BRIGHTNESS = 10
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_INVERT = False
LED_CHANNEL = 0
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

for i in range(strip.numPixels()-1):
    strip.setPixelColor(i, Color(255, 0, 0))
strip.show()
time.sleep(0.25)
for i in range(strip.numPixels()-1):
    strip.setPixelColor(i, Color(0, 255, 0))
strip.show()
time.sleep(0.25)
for i in range(strip.numPixels()-1):
    strip.setPixelColor(i, Color(0, 0, 255))
strip.show()
time.sleep(0.25)
idx = strip.numPixels() - 1
strip.setPixelColor(idx, Color(255, 0, 0))
strip.show()

""" ==============================
            SERVO MOTOR
    ============================== """
SERVOPIN = 11
GPIO.setup(SERVOPIN, GPIO.OUT)

""" ==============================
            MOTOR CONTROL
    ============================== """
# from motor_control import control
r = 0

"""
██╗    ██╗██╗  ██╗██╗██╗     ███████╗
██║    ██║██║  ██║██║██║     ██╔════╝
██║ █╗ ██║███████║██║██║     █████╗  
██║███╗██║██╔══██║██║██║     ██╔══╝  
╚███╔███╔╝██║  ██║██║███████╗███████╗
 ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝
"""

# prev_pos:       tuple(int, int)
# cur_pos:        tuple(int, int)
# prev_rgb:       tuple(int, int, int)
# cur_rgb:        tuple(int, int, int)
# has_cockroach:  bool

rgb = [(0, 0, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), ]
def call_rpi():
    global cur_pos, prev_rgb, has_hit
    global rgb
    global pwm_A, pwm_B
    global strip, prev_rgb, cur_rgb, has_hit

    for i in range(5):
        cur_pos = [4-i, 4-i]
        prev_rgb = rgb[i]
        cur_rgb = rgb[i+1]
        has_hit = cur_pos[0] ** 2 + cur_pos[1] ** 2 <= r
        # motor_control()
        motor_tt(0, pwm_A, pwm_B, AIN1, AIN2, BIN1, BIN2)
        set_strip_color(strip, prev_rgb, cur_rgb, has_hit)
        time.sleep(2)
        if has_hit:
            motor_servo(SERVOPIN)
            set_strip_color(strip, prev_rgb, cur_rgb, has_hit)
            break

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

        # Process Image and Call RPI
        
        return jsonify({
            "status": "success",
            "message": "Image received and saved",
            "filename": filename,
            "timestamp": timestamp
        })
    
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # For development only - use a production WSGI server in production
    app.run(host='0.0.0.0', port=80, debug=True)