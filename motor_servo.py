import RPi.GPIO as GPIO
import time

def motor_servo(GPIO_PIN):
    angle_down = 60
    angle_up = 0
    pwm = GPIO.PWM(GPIO_PIN, 50)
    pwm.start(0)
    pwm.ChangeDutyCycle((angle_up / 18) + 2.5)
    time.sleep(0.5)
    pwm.ChangeDutyCycle((angle_down / 18) + 2.5)
    time.sleep(0.5)
    pwm.ChangeDutyCycle((angle_up / 18) + 2.5)
    time.sleep(0.5)
    pwm.stop()

if __name__ == "__main__":
    GPIO_PIN = 12
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GPIO_PIN, GPIO.OUT)
    motor_servo(GPIO_PIN=GPIO_PIN)
    GPIO.cleanup()