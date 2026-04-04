import math
from turtle import distance
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

print("Welcome to the Hexapod Inverse Kinematics Test!")
print("This program calculates the angles of the joints needed to reach a specific endpoint in 2D space.")
print("Note: The hexapod has two joints (J1 and J2) and an endpoint that you want to reach. All measurements are in the same unit (e.g., centimeters).")

J1 = float(input("Enter the length of the first joint (J1): "))
J2 = float(input("Enter the length of the second joint (J2): "))

Endpoint = float(input("Enter the x-coordinate of the first endpoint: ")), float(input("Enter the y-coordinate of the first endpoint: "))
Endpoint2 = float(input("Enter the x-coordinate of the second endpoint: ")), float(input("Enter the y-coordinate of the second endpoint: "))
# Calculate the distance from the origin to the endpoint


def calculate_ik(x, y):
    distance = math.sqrt(x**2 + y**2)

    # Check if the point is reachable
    if distance > J1 + J2 or distance < abs(J1 - J2):
        print("The endpoint is unreachable with the given joint lengths.")
        exit()

    # Finding the internal Knee Angle using Law of Cosines
    cos_knee_angle = (J1**2 + J2**2 - distance**2) / (2 * J1 * J2)

    # Finding the internal Hip Angle using Law of Cosines
    cos_hip_angle = (distance**2 + J1**2 - J2**2) / (2 * distance * J1)

    # Calculate the target angle
    target_angle = math.atan2(y, x)

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
    return joint1_x, joint1_y, joint2_x, joint2_y

calculate_ik(Endpoint[0], Endpoint[1])
calculate_ik(Endpoint2[0], Endpoint2[1])

#Plotting and Animation
# Defining number of frames for animation

num_frames = 60

#Defining a list of x and y targets for the animation

x_targets = np.linspace(Endpoint[0], Endpoint2[0], num_frames)

y_targets = np.linspace(Endpoint[1], Endpoint2[1], num_frames)

# --- 1. Setting up the "Stage" ---
# We create a figure (the window) and an axis (the graph itself)
fig, ax = plt.subplots(figsize=(8, 8))

# We create empty lines that we will update later. 
# 'leg_line' is the blue arm, and 'target_point' is the red X.
leg_line, = ax.plot([], [], marker='o', linewidth=3, color='blue')
target_point, = ax.plot([], [], marker='x', color='red', markersize=10)

# Set the boundaries of the graph so it doesn't jump around
ax.set_xlim(-J1 - J2 - 1, J1 + J2 + 1)
ax.set_ylim(-J1 - J2 - 1, J1 + J2 + 1)
ax.set_title('Hexapod Inverse Kinematics Animation')
ax.grid(True)

# --- 2. The Animation Function ---
def animate(frame):
    """This function runs over and over, once for every frame (0 to 59)."""
    
    # Grab the exact X and Y coordinates for this specific frame
    current_x = x_targets[frame]
    current_y = y_targets[frame]
    
    # Run our math blender from Step 1!
    positions = calculate_ik(current_x, current_y)
    
    # If the math worked (the point is reachable), update the drawing
    if positions:
        j1x, j1y, j2x, j2y = positions
        
        # Give the leg_line its new calculated coordinates
        leg_line.set_data([0, j1x, j2x], [0, j1y, j2y])
        
        # Move the red X to the new target coordinate
        target_point.set_data([current_x], [current_y])
        
    return leg_line, target_point

# --- 3. Running the Show ---
# This is the command that actually starts the animation loop.
# 'interval=50' means wait 50 milliseconds between frames.
ani = animation.FuncAnimation(fig, animate, frames=num_frames, interval=25, blit=True)

# Open the window and watch it move!
plt.show()

