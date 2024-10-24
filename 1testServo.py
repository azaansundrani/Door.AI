import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BOARD)

# Define GPIO pins for servo control
servo_signal_pin = 12  # Signal pin
#servo_power_pin = 2    # Power pin
#servo_ground_pin = 30  # Ground pin

# Set up GPIO pins for servo control
GPIO.setup(servo_signal_pin, GPIO.OUT)
#GPIO.setup(servo_power_pin, GPIO.OUT)
#GPIO.setup(servo_ground_pin, GPIO.OUT)

# Create PWM instance
servo_pwm = GPIO.PWM(servo_signal_pin, 50)  # 50 Hz (standard for servos)

# Start PWM
servo_pwm.start(0)

def set_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(servo_signal_pin, True)
    servo_pwm.ChangeDutyCycle(duty)
    time.sleep(1)  # Wait for the servo to move
    GPIO.output(servo_signal_pin, False)
    servo_pwm.ChangeDutyCycle(0)


count = 0
direction = 1

try:
    while count < 2:
        # set_angle(0)   # Move to 0 degrees
        # time.sleep(1)
        # set_angle(90)  # Move to 90 degrees
        # time.sleep(1)
        set_angle(360) # Move to 360 degrees
        # time.sleep(1)

        count += 1

    time.sleep(5)

    direction *= 1

except KeyboardInterrupt:

    pass
    # Clean up GPIO
    # servo_pwm.stop()
    # GPIO.cleanup()

finally:
    # print("setting angle to 0")
    count = 0
    while count < 1:
        set_angle(0)
        # time.sleep(1)
        count += 1


    servo_pwm.stop()
    GPIO.cleanup()
