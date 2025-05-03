import RPi.GPIO as GPIO
import time

# GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(False)

# SERVO_PIN = 12
# GPIO.setup(SERVO_PIN, GPIO.OUT)

# pwm = GPIO.PWM(SERVO_PIN, 50)  # 50 Hz for servo
# pwm.start(0)

# def set_angle(angle):
#     duty = 2 + (angle / 18)
#     pwm.ChangeDutyCycle(duty)
#     time.sleep(0.5)  # Wait for servo to reach position
#     pwm.ChangeDutyCycle(0)

# try:
#     for i in range(4):
#         set_angle(i*90)
#         time.sleep(0.3)
# finally:
#     pwm.stop()
#     GPIO.cleanup()

def angle_to_duty_cycle(angle):
    return (angle / 18) + 2.5

def motor_servo(GPIO_PIN):
    angle_down = 90
    angle_up = 0
    pwm = GPIO.PWM(GPIO_PIN, 50)
    pwm.start(0)
    pwm.ChangeDutyCycle(angle_to_duty_cycle(angle_up))
    time.sleep(0.5)
    pwm.ChangeDutyCycle(angle_to_duty_cycle(angle_down))
    time.sleep(0.5)
    pwm.ChangeDutyCycle(angle_to_duty_cycle(angle_up))
    time.sleep(0.5)
    pwm.stop()

if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    GPIO_PIN = 15
    GPIO.setup(GPIO_PIN, GPIO.OUT)
    motor_servo(GPIO_PIN=GPIO_PIN)
    GPIO.cleanup()