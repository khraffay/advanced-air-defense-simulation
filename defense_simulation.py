import random
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# This class defines the incoming threat projectiles
class Projectile:
    def __init__(self, protected_x, protected_y):
        # All threats originate from the left side of the screen
        self.x = 0  # Fixed starting X position at left edge
        self.y = random.randint(10, 110)  # Random Y position along left edge
        
        # Store the coordinates of the protected zone for trajectory calculation
        self.protected_x = protected_x
        self.protected_y = protected_y
        
        # Calculate the direction vector toward the protected zone
        dx = protected_x - self.x
        dy = protected_y - self.y
        distance = math.sqrt(dx**2 + dy**2)  # Euclidean distance to target
        
        # Set a moderate speed for visible movement
        self.speed = random.uniform(0.8, 1.2)
        # Normalize the direction vector and scale by speed
        self.dx = dx / distance * self.speed
        self.dy = dy / distance * self.speed

    def move(self):
        """Update the projectile's position each frame along its trajectory"""
        self.x += self.dx
        self.y += self.dy

    def distance_to_target(self, target_x, target_y):
        """Calculate straight-line distance to any specified target coordinates"""
        return math.sqrt((self.x - target_x)**2 + (self.y - target_y)**2)

# This class implements the defense system logic
class AirDefense:
    def __init__(self, protected_x, protected_y, defense_radius):
        # Coordinates of the area being protected
        self.protected_x = protected_x
        self.protected_y = protected_y
        # Radius of the defense perimeter
        self.defense_radius = defense_radius

    def detect_projectile(self, projectile):
        """Check if a projectile has entered the defense perimeter"""
        distance = projectile.distance_to_target(self.protected_x, self.protected_y)
        return distance < self.defense_radius

    def engage_target(self, projectile):
        """Handle the interception of a threat and report its position"""
        print(f"Target neutralized at coordinates ({projectile.x:.2f}, {projectile.y:.2f})!")
        return True

# Configuration parameters for the simulation
protected_x = 60  # X coordinate of protected zone center
protected_y = 60  # Y coordinate of protected zone center
defense_radius = 20  # Radius of defense perimeter

# Initialize the defense system with our parameters
defense = AirDefense(protected_x, protected_y, defense_radius)

# Create a new projectile threat
projectile = Projectile(protected_x, protected_y)

# Set up the visualization window
fig, ax = plt.subplots(figsize=(8, 8))
# Define the coordinate system bounds
ax.set_xlim(0, 120)
ax.set_ylim(0, 120)

# Visual marker for the protected zone (purple circle)
protected_marker = plt.scatter(protected_x, protected_y, color='purple', s=200, label='Protected Zone')

# Visual marker for the incoming projectile (orange circle)
projectile_marker = plt.scatter(projectile.x, projectile.y, color='orange', s=50, label='Incoming Projectile')

# Draw the defense perimeter as a cyan circle
defense_perimeter = plt.Circle(
    (protected_x, protected_y), 
    defense_radius, 
    color='cyan', 
    fill=False, 
    linestyle='-',
    linewidth=2,
    alpha=0.7  # Slightly transparent
)
ax.add_artist(defense_perimeter)

# Track interception status and count
interception_count = 0
intercepted = False

# Animation update function - called each frame
def update(frame):
    """Update the simulation state and visualization each frame"""
    global interception_count, intercepted
    
    # Only process movement if not already intercepted
    if not intercepted:
        # Move the projectile along its trajectory
        projectile.move()
        
        # Update the projectile's visual position
        projectile_marker.set_offsets([projectile.x, projectile.y])

        # Check if projectile has entered defense perimeter
        if defense.detect_projectile(projectile):
            # Execute interception
            defense.engage_target(projectile)
            interception_count += 1
            intercepted = True
            # Visual feedback for interception (red explosion)
            projectile_marker.set_color('red')
            projectile_marker.set_sizes([150])
            # Update title to show successful interception
            plt.title(f"Air Defense Simulation - Target Neutralized! (Total: {interception_count})")
        else:
            # Update title to show tracking in progress
            plt.title("Air Defense Simulation - Tracking Threat")
    
    return projectile_marker,

# Create the animation with 150 frames, updating every 200ms
ani = FuncAnimation(fig, update, frames=range(150), interval=200, repeat=False)

# Add chart elements and formatting
plt.legend(loc="upper right")  # Position the legend
plt.grid(True, linestyle='--', alpha=0.7)  # Add grid lines
plt.xlabel("X Coordinate")  # X-axis label
plt.ylabel("Y Coordinate")  # Y-axis label
plt.tight_layout()  # Automatically adjust layout

# Adjust top margin to ensure title is fully visible
plt.subplots_adjust(top=0.92)

# Display the simulation
plt.show()