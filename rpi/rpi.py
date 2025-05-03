import RPi.GPIO as GPIO
import time

'''
███████╗███████╗████████╗██╗   ██╗██████╗ 
██╔════╝██╔════╝╚══██╔══╝██║   ██║██╔══██╗
███████╗█████╗     ██║   ██║   ██║██████╔╝
╚════██║██╔══╝     ██║   ██║   ██║██╔═══╝ 
███████║███████╗   ██║   ╚██████╔╝██║     
╚══════╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝     
'''

''' ==============================
            GPIO SETUP
    ============================== '''
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

''' ==============================
            TT MOTOR
    ============================== '''
from motor_tt import motor_tt
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

''' ==============================
            LED
    ============================== '''
from led import set_strip_color, clear_strip
from rpi_ws281x import PixelStrip, Color
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

''' ==============================
            SERVO MOTOR
    ============================== '''
from motor_servo import motor_servo
SERVOPIN = 11
GPIO.setup(SERVOPIN, GPIO.OUT)

''' ==============================
            MOTOR CONTROL
    ============================== '''
# from motor_control import control
r = 0

'''
██╗    ██╗██╗  ██╗██╗██╗     ███████╗
██║    ██║██║  ██║██║██║     ██╔════╝
██║ █╗ ██║███████║██║██║     █████╗  
██║███╗██║██╔══██║██║██║     ██╔══╝  
╚███╔███╔╝██║  ██║██║███████╗███████╗
 ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝
'''

# prev_pos:       tuple(int, int)
# cur_pos:        tuple(int, int)
# prev_rgb:       tuple(int, int, int)
# cur_rgb:        tuple(int, int, int)
# has_cockroach:  bool

# while 1:
rgb = [(0, 0, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), ]
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

'''
███████╗██╗███╗   ██╗██╗███████╗██╗  ██╗
██╔════╝██║████╗  ██║██║██╔════╝██║  ██║
█████╗  ██║██╔██╗ ██║██║███████╗███████║
██╔══╝  ██║██║╚██╗██║██║╚════██║██╔══██║
██║     ██║██║ ╚████║██║███████║██║  ██║
╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝╚══════╝╚═╝  ╚═╝
'''

clear_strip(strip)
time.sleep(0.5)
pwm_A.stop()
pwm_B.stop()
GPIO.cleanup()