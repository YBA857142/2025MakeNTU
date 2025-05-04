import RPi.GPIO as GPIO
import time

def motor_tt(scale, pwm_A, pwm_B, AIN1, AIN2, BIN1, BIN2):
    scale0 = 5
    speed = 50
    speed_A = scale0 + scale
    speed_B = scale0 - scale
    pwm_A.ChangeDutyCycle(speed * speed_A / max(speed_B, speed_A))
    pwm_B.ChangeDutyCycle(speed * speed_B / max(speed_B, speed_A))
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)

if __name__ == "__main__":
    try:
        # TB6612FNG pin definitions (BOARD numbering)
        PWMA = 32     # Motor A PWM
        AIN1 = 31     # Motor A input 1
        AIN2 = 33     # Motor A input 2

        BIN1 = 35     # Motor B input 1
        BIN2 = 37     # Motor B input 2
        PWMB = 38     # Motor B PWM

        # Setup GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        # Set up all pins as output
        motor_pins = [PWMA, AIN1, AIN2, BIN1, BIN2, PWMB]
        for pin in motor_pins:
            GPIO.setup(pin, GPIO.OUT)

        # Initialize PWM on PWMA and PWMB
        pwm_A = GPIO.PWM(PWMA, 1000)
        pwm_B = GPIO.PWM(PWMB, 1000)
        pwm_A.start(0)
        pwm_B.start(0)

        motor_tt(0, pwm_A, pwm_B, AIN1, AIN2, BIN1, BIN2)
        time.sleep(1)
    finally:
        pwm_A.stop()
        pwm_B.stop()
        GPIO.cleanup()
