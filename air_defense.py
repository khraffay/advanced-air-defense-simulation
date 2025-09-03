import math
import random
import pygame

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Game parameters
DEFENSE_MISSILE_SPEED = 10
DETECTION_RANGE = 150
RADAR_POSITION = (400, 500)
RADAR_SWEEP_SPEED = 0.05
FRAME_RATE = 60

# Threat types with different properties
THREAT_TYPES = {
    "Swift": {"color": (255, 165, 0), "speed": random.uniform(6, 10), "size": 5},
    "Heavy": {"color": (128, 0, 128), "speed": random.uniform(2, 5), "size": 7},
}

# Initialize pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Air Defense Simulation")
clock = pygame.time.Clock()

# Load sound effects
missile_sound = pygame.mixer.Sound(r"C:\Users\Abdul Raffay\Desktop\Air_Defense\missile_launch.mp3")
explosion_sound = pygame.mixer.Sound(r"C:\Users\Abdul Raffay\Desktop\Air_Defense\explosion.mp3")

# Font for UI elements
font = pygame.font.Font(None, 36)

class Threat:
    """Represents an incoming threat missile"""
    def __init__(self, start_x, start_y, target_x, target_y, threat_type):
        self.start_x = start_x
        self.start_y = start_y
        self.x = start_x
        self.y = start_y
        self.target_x = target_x
        self.target_y = target_y
        self.color = threat_type["color"]
        self.speed = threat_type["speed"]
        self.size = threat_type["size"]
        # Calculate angle towards target
        self.angle = math.atan2(target_y - start_y, target_x - start_x)

    def update_position(self):
        """Move the threat along its trajectory"""
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

    def is_at_target(self):
        """Check if threat has reached its target"""
        return math.hypot(self.x - self.target_x, self.y - self.target_y) < 5

    def is_in_detection_range(self, radar_x, radar_y):
        """Check if threat is within radar detection range"""
        return math.hypot(self.x - radar_x, self.y - radar_y) <= DETECTION_RANGE

class DefenseMissile:
    """Represents a defensive missile that intercepts threats"""
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y
        self.speed = DEFENSE_MISSILE_SPEED
        self.target_x = None
        self.target_y = None
        self.angle = None

    def calculate_interception(self, threat):
        """Calculate interception course towards a threat"""
        self.target_x = threat.x
        self.target_y = threat.y
        self.angle = math.atan2(self.target_y - self.y, self.target_x - self.x)

    def update_position(self):
        """Move the defense missile toward its target"""
        if self.target_x is not None and self.target_y is not None:
            self.x += self.speed * math.cos(self.angle)
            self.y += self.speed * math.sin(self.angle)

    def has_intercepted(self, threat):
        """Check if defense missile has intercepted a threat"""
        return math.hypot(self.x - threat.x, self.y - threat.y) < 5

class DetectionSystem:
    """Radar system that detects threats and launches interceptors"""
    def __init__(self, radar_x, radar_y):
        self.x = radar_x
        self.y = radar_y
        self.defense_missiles = []
        self.sweep_angle = 0

    def detect_and_launch(self, threats):
        """Detect threats and launch interceptors when needed"""
        for threat in threats:
            if (threat.is_in_detection_range(self.x, self.y) and 
                not self.is_defense_missile_launched_for(threat)):
                self.launch_defense_missile(threat)

    def is_defense_missile_launched_for(self, threat):
        """Check if a threat is already being targeted"""
        for defense_missile in self.defense_missiles:
            if (defense_missile.target_x == threat.x and 
                defense_missile.target_y == threat.y):
                return True
        return False

    def launch_defense_missile(self, threat):
        """Launch a defense missile towards a threat"""
        defense_missile = DefenseMissile(self.x, self.y)
        defense_missile.calculate_interception(threat)
        self.defense_missiles.append(defense_missile)
        missile_sound.play()

    def update_defense_missiles(self, threats):
        """Update all defense missiles and check for interceptions"""
        intercepted_threats = []
        for defense_missile in self.defense_missiles:
            defense_missile.update_position()
            for threat in threats:
                if defense_missile.has_intercepted(threat):
                    intercepted_threats.append(threat)
                    explosion_sound.play()
        return intercepted_threats

    def draw_radar(self):
        """Draw the radar with sweeping animation"""
        # Draw detection range
        pygame.draw.circle(screen, (70, 130, 180), (self.x, self.y), DETECTION_RANGE, 1)
        
        # Draw sweep line
        sweep_x = self.x + DETECTION_RANGE * math.cos(self.sweep_angle)
        sweep_y = self.y + DETECTION_RANGE * math.sin(self.sweep_angle)
        pygame.draw.line(screen, (0, 255, 255), (self.x, self.y), (sweep_x, sweep_y), 2)
        
        # Draw sweep arc
        start_angle = self.sweep_angle - 0.1
        end_angle = self.sweep_angle + 0.1
        pygame.draw.arc(screen, (0, 255, 255), 
                       (self.x - DETECTION_RANGE, self.y - DETECTION_RANGE, 
                        DETECTION_RANGE * 2, DETECTION_RANGE * 2), 
                       start_angle, end_angle, 2)
        
        # Update sweep angle
        self.sweep_angle += RADAR_SWEEP_SPEED
        if self.sweep_angle >= 2 * math.pi:
            self.sweep_angle = 0

def draw_explosion(position):
    """Draw an explosion effect at the given position"""
    pygame.draw.circle(screen, (255, 215, 0), (int(position[0]), int(position[1])), 15)
    pygame.draw.circle(screen, (255, 69, 0), (int(position[0]), int(position[1])), 10)

def draw_buttons():
    """Draw the threat launch buttons"""
    # Swift threat button
    pygame.draw.rect(screen, (255, 165, 0), (50, 50, 100, 40))
    swift_text = font.render("Swift", True, (0, 0, 0))
    screen.blit(swift_text, (65, 55))

    # Heavy threat button
    pygame.draw.rect(screen, (128, 0, 128), (200, 50, 100, 40))
    heavy_text = font.render("Heavy", True, (255, 255, 255))
    screen.blit(heavy_text, (215, 55))

def check_button_click(pos):
    """Check if a button was clicked and return which one"""
    x, y = pos
    if 50 <= x <= 150 and 50 <= y <= 90:    # Swift button
        return 'Swift'
    elif 200 <= x <= 300 and 50 <= y <= 90:  # Heavy button
        return 'Heavy'
    return None

def launch_threat(threat_type, threats):
    """Launch a new threat of the specified type"""
    start_x = random.randint(0, SCREEN_WIDTH)
    start_y = 0
    target_x, target_y = RADAR_POSITION
    threat = Threat(start_x, start_y, target_x, target_y, THREAT_TYPES[threat_type])
    threats.append(threat)
    missile_sound.play()

def main_simulation():
    """Main game loop"""
    threats = []
    detection_system = DetectionSystem(*RADAR_POSITION)
    score = 0
    running = True

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_action = check_button_click(event.pos)
                if button_action == 'Swift':
                    launch_threat("Swift", threats)
                elif button_action == 'Heavy':
                    launch_threat("Heavy", threats)

        # Clear screen
        screen.fill((0, 0, 0))

        # Update radar
        detection_system.draw_radar()
        detection_system.detect_and_launch(threats)

        # Update threats
        for threat in threats.copy():
            threat.update_position()
            if threat.is_at_target():
                threats.remove(threat)
            detection_system.detect_and_launch(threats)

        # Update defense missiles
        intercepted_threats = detection_system.update_defense_missiles(threats)
        for threat in intercepted_threats:
            threats.remove(threat)
            score += 1

        # Draw all objects
        for threat in threats:
            pygame.draw.circle(screen, threat.color, (int(threat.x), int(threat.y)), threat.size)

        for defense_missile in detection_system.defense_missiles:
            pygame.draw.circle(screen, (200, 200, 200), (int(defense_missile.x), int(defense_missile.y)), 5)

        for threat in intercepted_threats:
            draw_explosion((threat.x, threat.y))

        # Draw UI
        draw_buttons()
        score_text = font.render(f"Interceptions: {score}", True, (255, 255, 255))
        screen.blit(score_text, (600, 20))

        # Update display
        pygame.display.flip()
        clock.tick(FRAME_RATE)

    pygame.quit()

# Start the simulation
if __name__ == "__main__":
    main_simulation()