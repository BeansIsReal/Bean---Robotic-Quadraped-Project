import math
import matplotlib.pyplot as plt
import numpy as np

print("Welcome to the Hexapod Inverse Kinematics Test!")
print("This program calculates the angles of the joints needed to reach a specific endpoint in 2D space.")
print("Note: The hexapod has two joints (J1 and J2) and an endpoint that you want to reach. All measurements are in the same unit (e.g., centimeters).")

J1 = float(input("Enter the length of the first joint (J1): "))
J2 = float(input("Enter the length of the second joint (J2): "))

Endpoint = float(input("Enter the x-coordinate of the endpoint: ")), float(input("Enter the y-coordinate of the endpoint: "))

# Calculate the distance from the origin to the endpoint
distance = math.sqrt(Endpoint[0]**2 + Endpoint[1]**2)

# Check if the point is reachable
if distance > J1 + J2 or distance < abs(J1 - J2):
    print("The endpoint is unreachable with the given joint lengths.")
    exit()

# Finding the internal Knee Angle using Law of Cosines
cos_knee_angle = (J1**2 + J2**2 - distance**2) / (2 * J1 * J2)

# Finding the internal Hip Angle using Law of Cosines
cos_hip_angle = (distance**2 + J1**2 - J2**2) / (2 * distance * J1)

# Calculate the target angle
target_angle = math.atan2(Endpoint[1], Endpoint[0])

# Calculate the actual angles (elbow down configuration)
hip_angle = target_angle - math.acos(cos_hip_angle) * -1

# FIX APPLIED HERE: Subtracting the internal angle from pi (180 degrees) 
# to get the exterior angle for the servo and the plot.
knee_angle = math.pi - math.acos(cos_knee_angle) * -1

# Output of all angles and measurements
print(f"Distance to Endpoint: {distance:.2f}")
print(f"Knee Angle (in degrees): {math.degrees(knee_angle):.2f}")
print(f"Hip Angle (in degrees): {math.degrees(hip_angle):.2f}")

# Calculate the positions of the joints
joint1_x = J1 * math.cos(hip_angle)
joint1_y = J1 * math.sin(hip_angle)
joint2_x = joint1_x + J2 * math.cos(hip_angle + knee_angle)
joint2_y = joint1_y + J2 * math.sin(hip_angle + knee_angle)

# Plotting
plt.figure(figsize=(8, 8))
plt.plot([0, joint1_x, joint2_x], [0, joint1_y, joint2_y], marker='o')
plt.plot(Endpoint[0], Endpoint[1], marker='x', color='red', label='Endpoint')
plt.xlim(-J1 - J2 - 1, J1 + J2 + 1)
plt.ylim(-J1 - J2 - 1, J1 + J2 + 1)
plt.title('Hexapod Inverse Kinematics')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.grid()
plt.axhline(y=0, color='black', linewidth=1)
plt.axvline(x=0, color='black', linewidth=1)
plt.legend()
plt.show()