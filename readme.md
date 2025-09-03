# Advanced Tactical Air Defense Interception and Threat Neutralization Simulation System



A real-time interactive simulation of modern air defense systems built with Python and Pygame. This project demonstrates threat detection, interception algorithms, and defense mechanisms in an engaging visual environment.

## What This Simulation Does

This Python program creates a interactive air defense simulation where:

- **Threats** (missiles) are launched from the top of the screen
- A **radar system** detects incoming threats within its range
- **Defense missiles** are automatically launched to intercept threats
- **Visual and audio feedback** provides engagement information
- **Score tracking** monitors successful interceptions
- **User interaction** allows launching different types of threats

The simulation demonstrates principles of:
- Real-time collision detection
- Trigonometric trajectory calculations
- Radar sweep animation mathematics
- Threat interception prediction algorithms

## Installation

### Prerequisites
- Python 3.8 or higher
- Pip package manager

### Steps
1. Clone the repository:
```bash
git clone https://github.com/your-username/advanced-air-defense-simulation.git
cd advanced-air-defense-simulation

install required dependencies:
pip install pygame

How to Use the Code
Running the Simulation

python air_defense.py

Controls
Click "Swift" button (orange): Launches a fast-moving threat

Click "Heavy" button (purple): Launches a slow-moving, larger threat

Close window: Exit the simulation

Gameplay Instructions
The simulation starts with a radar system at the bottom of the screen

Click either threat button to launch missiles from the top of the screen

The radar will automatically detect incoming threats within its range (blue circle)

Defense missiles (gray) will launch to intercept threats

Successful interceptions create explosion animations and play sound effects

Your score (number of interceptions) is displayed in the top-right corner

Threats that reach the radar base will be removed from the simulation

Audio Setup
For full functionality, add these audio files in an Air_Defense folder:

missile_launch.wav - played when threats or interceptors are launched

explosion.mp3 - played when threats are successfully intercepted

Project Structure
advanced-air-defense-simulation/
│
├── air_defense.py          # Main simulation code
├── Air_Defense/            # Audio assets directory (create this)
│   ├── missile_launch.wav  # Launch sound effect
│   └── explosion.mp3       # Explosion sound effect
├── requirements.txt        # Python dependencies
└── README.md              # This file

Code Customization
You can modify these parameters in the code:
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Game mechanics
DEFENSE_MISSILE_SPEED = 10  # Interceptor speed
DETECTION_RANGE = 150       # Radar detection radius
RADAR_SWEEP_SPEED = 0.05    # Radar animation speed

# Threat properties (in THREAT_TYPES dictionary)
"Swift": {"color": (255, 165, 0), "speed": random.uniform(6, 10), "size": 5}
"Heavy": {"color": (128, 0, 128), "speed": random.uniform(2, 5), "size": 7}

Troubleshooting
Common issues:

Audio files not found: Create Air_Defense folder with required sound files

Pygame not installed: Run pip install pygame

Module errors: Ensure you're using Python 3.8+

License
This project is licensed under the MIT License - see the LICENSE file for details.