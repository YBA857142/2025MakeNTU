import RPi.GPIO as GPIO
import time as time
from led import set_strip_color, clear_strip
from motor_servo import motor_servo as motor_servo
from motor_tt import motor_tt as motor_tt
from rpi_ws281x import PixelStrip, Color
if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

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

    LED_COUNT = 11
    LED_PIN = 18
    LED_BRIGHTNESS = 10
    LED_FREQ_HZ = 800000
    LED_DMA = 10
    LED_INVERT = False
    LED_CHANNEL = 0
    prev_rgb = (0, 0, 0)
    cur_rgb = (0, 0, 0)
    has_hit = False

    SERVOPIN = 11

    """
    LED
    """
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    set_strip_color(strip, prev_rgb, cur_rgb, has_hit)

    """
    SERVO
    """
    motor_servo(GPIO_PIN=SERVOPIN)

    """
    TT
    """
    motor_tt(1, PWMA, PWMB, AIN1, AIN2, BIN1, BIN2)

    GPIO.cleanup()
