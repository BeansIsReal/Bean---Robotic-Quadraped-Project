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
# HARDWARE INITIALIZATION
# ==========================================
i2c = busio.I2C(board.SCL, board.SDA)
pca_board = PCA9685(i2c)
pca_board.frequency = 50

standard_servo_hip = servo.Servo(pca_board.channels[0], min_pulse=500, max_pulse=2500)
standard_servo_knee = servo.Servo(pca_board.channels[1], min_pulse=500, max_pulse=2500)

# ==========================================
# CALIBRATION CONSTANTS
# ==========================================
# Assuming you mechanically set the leg to horizontal/vertical at 90 degrees:
HIP_OFFSET = 90  
KNEE_OFFSET = 90 

# Change these to -1 if the servo moves the opposite direction you expect
HIP_DIR =-1      
KNEE_DIR = 1    

# ==========================================
# MAIN PROGRAM
# ==========================================
print("Welcome to the Hexapod Inverse Kinematics Main!")

J1 = 56.8
J2 = 108.2

Endpoint_x = float(input("Enter the x-coordinate of the FIRST endpoint: "))
Endpoint_y = float(input("Enter the y-coordinate of the FIRST endpoint: "))

Endpoint2_x = float(input("Enter the x-coordinate of the SECOND endpoint: "))
Endpoint2_y = float(input("Enter the y-coordinate of the SECOND endpoint: "))

def calculate_ik(x, y):
    distance = math.sqrt(x**2 + y**2)

    # Check if the point is reachable
    if distance > J1 + J2 or distance < abs(J1 - J2):
        print(f"Warning: The endpoint ({x}, {y}) is unreachable.")
        return None, None

    # Law of Cosines for internal angles
    cos_knee_angle = (J1**2 + J2**2 - distance**2) / (2 * J1 * J2)
    cos_hip_angle = (distance**2 + J1**2 - J2**2) / (2 * distance * J1)

    # Protect against floating point errors slightly outside [-1, 1]
    cos_knee_angle = max(-1.0, min(1.0, cos_knee_angle))
    cos_hip_angle = max(-1.0, min(1.0, cos_hip_angle))

    internal_knee = math.acos(cos_knee_angle)
    internal_hip = math.acos(cos_hip_angle)

    target_angle = math.atan2(y, x)

    # Mathematical Angles
    hip_math = target_angle + internal_hip
    knee_math = math.pi - internal_knee

    # Map Mathematical Angles to Physical Servo Angles
    servo_hip = HIP_OFFSET + (math.degrees(hip_math) * HIP_DIR)
    
    # The "- 90" aligns the math L-shape to our physical center
    servo_knee = KNEE_OFFSET + ((math.degrees(knee_math) - 90) * KNEE_DIR)

    # Constrain to 0-180 limits before returning
    safe_hip = max(0, min(180, servo_hip))
    safe_knee = max(0, min(180, servo_knee))

    return safe_hip, safe_knee

# --- Pre-calculate both positions ---
print("\nCalculating kinematics...")
hip1, knee1 = calculate_ik(Endpoint_x, Endpoint_y)
hip2, knee2 = calculate_ik(Endpoint2_x, Endpoint2_y)

# Only proceed if both endpoints are reachable
if None in (hip1, knee1, hip2, knee2):
    print("One or both endpoints are out of bounds. Exiting.")
    exit()

print(f"Endpoint 1 Servo Targets -> Hip: {hip1:.1f} | Knee: {knee1:.1f}")
print(f"Endpoint 2 Servo Targets -> Hip: {hip2:.1f} | Knee: {knee2:.1f}")
print("\nStarting movement loop...")

# --- Movement Loop ---
for i in range(16):
    print(f"Cycle {i+1}/16: Moving to Endpoint 1")
    # Command both servos back-to-back instantly
    standard_servo_hip.angle = hip1
    time.sleep(0.05)
    standard_servo_knee.angle = knee1
    
    # Sleep only AFTER both commands are sent so they move simultaneously 
    time.sleep(2) 

    print(f"Cycle {i+1}/16: Moving to Endpoint 2")
    # Command both servos back-to-back instantly
    standard_servo_hip.angle = hip2
    time.sleep(0.05)
    standard_servo_knee.angle = knee2
    
    # Sleep only AFTER both commands are sent
    time.sleep(2) 

print("Test complete. Powering down servos.")
# Releasing the servos at the end to prevent overheating
standard_servo_hip.angle = None
