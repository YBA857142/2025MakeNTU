from flask import Flask, send_from_directory, jsonify, request
import os
import base64
from datetime import datetime
import logging
import RPi.GPIO as GPIO
import time
from motor_tt import motor_tt
from led import set_strip_color, clear_strip
from rpi_ws281x import PixelStrip, Color
from motor_servo import motor_servo
from motor_control import motor_control

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__, static_folder='frontend', static_url_path='')

if __name__ == "__main__":

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
    r = 3
    prev_predict = 0
    predict = 0

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

    run_rpi = True

    cur_pos = (-1, -1)
    prev_pos = (-1, -1)
    has_cockroach = False
    prev_rgb = (0, 0, 0)
    cur_rgb = (0, 0, 0)
    has_hit = False

    def call_rpi():
        global prev_predict, predict
        global cur_pos, prev_pos, has_cockroach
        global pwm_A, pwm_B, AIN1, AIN2, BIN1, BIN2
        global prev_rgb, cur_rgb, has_hit
        global strip
        global SERVOPIN
        global run_rpi

        # If cockroach is hit, return
        if not run_rpi:
            return

        # Only one image is captured
        if prev_pos == (-1, -1):
            prev_pos = cur_pos
            prev_rgb = cur_rgb
            return
        
        try:
            prev_predict = predict
            has_hit = cur_pos[0] ** 2 + cur_pos[1] ** 2 <= r
            predict = motor_control(prev_pos, cur_pos, has_cockroach, prev_predict, pwm_A, pwm_B, AIN1, AIN2, BIN1, BIN2)
            set_strip_color(strip, prev_rgb, cur_rgb, has_hit)
            # time.sleep(0.1)
            if has_hit:
                motor_servo(SERVOPIN)
                set_strip_color(strip, prev_rgb, cur_rgb, has_hit)
                # run_rpi = False
            
            # Update prev
            prev_rgb = cur_rgb
            prev_pos = cur_pos
        except Exception as e:
            logger.error(f"Error: {str(e)}")

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
    @app.route('/api/position', methods=['POST'])
    def receive_position():
        global cur_pos
        global cur_rgb
        global has_cockroach

    # try:
        data = request.json
        
        if (not data 
            or 'position' not in data
            or 'color' not in data
            or 'has_cockroach' not in data
        ):
            return jsonify({"error": "No position data received"}), 400
        
        # Get data for call_rpi()
        raw_pos = data.get("position")
        raw_rgb = data.get("color")
        has_cockroach = True if data.get("has_cockroach") else False
        try:
            cur_pos = (raw_pos[0], raw_pos[1])
        except:
            return jsonify({"error": "Wrong position format"}), 400
        try:
            cur_rgb = (raw_rgb[0], raw_rgb[1], raw_rgb[2])
        except:
            return jsonify({"error": "Wrong color format"})
        
        print(raw_pos, raw_rgb, has_cockroach)
        call_rpi()
        
        return jsonify({"status": "success"})
    
    # except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

    # For development only - use a production WSGI server in production
    app.run(host='0.0.0.0', port=80, debug=False)