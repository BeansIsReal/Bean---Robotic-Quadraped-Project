import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

print("Sup")

# 1. Initialize the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# 2. Create the PCA9685 object using the I2C bus
pca_board = PCA9685(i2c)

# 3. Set frequency to 50Hz
pca_board.frequency = 50

# 4. Initialize the servos
standard_servo_hip = servo.Servo(pca_board.channels[1], min_pulse=500, max_pulse=2500)
standard_servo_knee = servo.Servo(pca_board.channels[2], min_pulse=500, max_pulse=2500)

Answer = str(input("90 degrees - Yes or No:"))

if Answer.lower() == "yes":
    print("Moving to 90 degrees...")
    standard_servo_hip.angle = 90
    standard_servo_knee.angle = 90
    time.sleep(2)  # Keep the script alive for 2 seconds so the motors have time to turn

if Answer.lower() == "no":
    print("Moving to 0 degrees...")
    standard_servo_hip.angle = 0
    standard_servo_knee.angle = 0
    time.sleep(2)  # Keep the script alive for 2 seconds so the motors have time to turn

print("Test complete!")
