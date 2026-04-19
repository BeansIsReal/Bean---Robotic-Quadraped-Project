# Note: Every time code is used, run command in RPi terminal: 
    # cd ~/servo_project
    # source env/bin/activate

import time
import math
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# ==========================================
# HARDWARE INITIALIZATION FIX
# ==========================================
# 1. Initialize the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# 2. Create the PCA9685 object using the I2C bus
pca_board = PCA9685(i2c)

# 3. Set frequency to 50Hz (crucial for standard servos)
pca_board.frequency = 50

# 4. Initialize the servos on the correct channels
standard_servo_hip = servo.Servo(pca_board.channels[1], min_pulse=500, max_pulse=2500)
standard_servo_knee = servo.Servo(pca_board.channels[2], min_pulse=500, max_pulse=2500)

# ==========================================
# MAIN PROGRAM
# ==========================================
print("Welcome to the Hexapod Inverse Kinematics Main!")
print("This program calculates the angles of the joints needed to reach a specific endpoint in 2D space.")

J1 = float(input("Enter the length of the first joint (J1): "))
J2 = float(input("Enter the length of the second joint (J2): "))

Endpoint_x = float(input("Enter the x-coordinate of the first endpoint: "))
Endpoint_y = float(input("Enter the y-coordinate of the first endpoint: "))

Endpoint2_x = float(input("Enter the x-coordinate of the second endpoint: "))
Endpoint2_y = float(input("Enter the y-coordinate of the second endpoint: "))

def calculate_ik(x, y):
    distance = math.sqrt(x**2 + y**2)

    # Check if the point is reachable
    if distance > J1 + J2 or distance < abs(J1 - J2):
        print(f"The endpoint ({x}, {y}) is unreachable with the given joint lengths.")
        exit()

    # Finding the internal Knee Angle using Law of Cosines
    cos_knee_angle = (J1**2 + J2**2 - distance**2) / (2 * J1 * J2)
    # Finding the internal Hip Angle using Law of Cosines
    cos_hip_angle = (distance**2 + J1**2 - J2**2) / (2 * distance * J1)

    # Calculate the target angle
    target_angle = math.atan2(y, x)

    # Calculate the actual angles (elbow down configuration)
    hip_angle = target_angle - math.acos(cos_hip_angle) * -1
    # Subtracting the internal angle from pi (180 degrees) 
    knee_angle = math.pi - math.acos(cos_knee_angle) * -1

    print(f"\nDistance to Endpoint: {distance:.2f}")
    print(f"Knee Angle (in degrees): {math.degrees(knee_angle):.2f}")
    print(f"Hip Angle (in degrees): {math.degrees(hip_angle):.2f}")

    # FIX: Return only the angles so the servos get the right data
    return math.degrees(hip_angle), math.degrees(knee_angle)

try:
    # --- Move to Endpoint 1 ---
    hip_deg, knee_deg = calculate_ik(Endpoint_x, Endpoint_y)
    
    # Ensure angles are within the 0-180 degree limits of the servo library
    standard_servo_hip.angle = max(0, min(180, hip_deg))
    standard_servo_knee.angle = max(0, min(180, knee_deg))
    
    time.sleep(2)

    # --- Move to Endpoint 2 ---
    hip_deg2, knee_deg2 = calculate_ik(Endpoint2_x, Endpoint2_y)
    
    standard_servo_hip.angle = max(0, min(180, hip_deg2))
    standard_servo_knee.angle = max(0, min(180, knee_deg2))
    
    time.sleep(2)

finally:
    # Always safely turn off the I2C connection when the script finishes
    pca_board.deinit()