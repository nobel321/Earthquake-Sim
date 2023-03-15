import pygame
import random
import time

"""
Description, earthquake simulation that shows the results of different fault types and the epicenter of an earthquake
- the red circle is the epicenter
- the black line represents the fault line along which the earthquake occured

Key Vocabulary:
- Fault type - fracture or zone of fractures between 2 blocks of rock; several types, including: strike-slip, normal, and reverse (thurst) faults
- Epicenter - the point on the Earth's surface directly above the hypocenter or focus, where an earthquake or underground explosion originates.
"""

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 100
EPICENTER_RADIUS = 20
CRACK_WIDTH = 10
CRACK_COLOR = (255, 0, 0)
MAX_QUAKE_INTENSITY = 15
MAX_CRACK_LENGTH = 200

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Earthquake Simulator")

# Define functions
def draw_ground():
    pygame.draw.rect(screen, (0, 200, 0), (0, SCREEN_HEIGHT-GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))

def draw_epicenter(epicenter_x, epicenter_y):
    pygame.draw.circle(screen, (255, 255, 0), (epicenter_x, epicenter_y), EPICENTER_RADIUS)

def draw_crack(x, y, length, direction):
    if direction == "horizontal":
        pygame.draw.rect(screen, CRACK_COLOR, (x, y, length, CRACK_WIDTH))
    else:
        pygame.draw.rect(screen, CRACK_COLOR, (x, y, CRACK_WIDTH, length))

def simulate_quake(magnitude, duration, fault_type, epicenter_x, epicenter_y):
    # Calculate quake intensity
    intensity = min(magnitude * 2, MAX_QUAKE_INTENSITY)

    # Calculate fault type multiplier
    fault_types = {
        "strike-slip": 1.0,
        "normal": 0.8,
        "reverse": 1.2
    }
    multiplier = fault_types.get(fault_type, 1.0)

    # Initialize crack variables
    crack_length = 0
    crack_x = epicenter_x
    crack_y = epicenter_y - CRACK_WIDTH // 2
    crack_direction = "horizontal"  # can be "horizontal" or "vertical"

    # Simulate quake
    for i in range(int(duration * 60)):
        # Draw ground
        draw_ground()

        # Draw epicenter
        draw_epicenter(epicenter_x, epicenter_y)

        # Draw crack
        draw_crack(crack_x, crack_y, crack_length, crack_direction)

        # Update crack variables
        if crack_direction == "horizontal":
            crack_length += random.randint(0, intensity)
            if crack_x + crack_length > SCREEN_WIDTH:
                crack_direction = "vertical"
                crack_x = SCREEN_WIDTH - CRACK_WIDTH // 2
                crack_y += CRACK_WIDTH // 2
                crack_length = 0
        else:
            crack_length += random.randint(0, intensity)
            if crack_y + crack_length > SCREEN_HEIGHT - GROUND_HEIGHT:
                break
            if random.random() < 0.5:
                crack_direction = "horizontal"
                crack_x -= CRACK_WIDTH // 2
                crack_y = SCREEN_HEIGHT - GROUND_HEIGHT - CRACK_WIDTH // 2
                crack_length = 0

        # Update display
        pygame.display.update()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Wait
        pygame.time.wait(10)

    # Print results
    print(f"Energy released: {10**(1.5 * magnitude + 9.05):.2e} J")
    print(f"Richter scale magnitude: {2/3 * (magnitude - 2):.2f}")
    print(f"Mercalli scale intensity: {2.28 * (magnitude):.2}")

# define fault types and their multipliers
fault_types = {
    "strike-slip": 1.0,
    "normal": 0.8,
    "reverse": 1.2
}

# get input parameters
magnitude = float(input("Enter magnitude of earthquake: "))
duration = float(input("Enter duration of earthquake (in seconds): "))
fault_type = input("Enter fault type (strike-slip, normal, or reverse): ").lower()
epicenter_x = int(input("Enter epicenter location (x-coordinate): "))
epicenter_y = int(input("Enter epicenter location (y-coordinate): "))

# calculate secondary effects
energy = 10**(1.5 * magnitude + 9.05)  # energy released in joules
richter_scale = 2/3 * (magnitude - 2)  # richter scale magnitude
mercalli_scale = 2.28 * magnitude + 2.0  # mercalli scale intensity

# calculate fault type multiplier
multiplier = fault_types.get(fault_type, 1.0)

# set up earthquake parameters
earthquake_start_time = time.time()
earthquake_end_time = earthquake_start_time + duration
max_displacement = 50 * multiplier
displacement = 0
direction = random.randint(0, 359)
velocity = max_displacement / duration

# main game loop
running = True
while running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # calculate elapsed time since start of earthquake
    elapsed_time = time.time() - earthquake_start_time
    
    # calculate displacement and direction of earthquake
    if elapsed_time < duration:
        displacement = velocity * elapsed_time
        direction += random.randint(-10, 10)
    else:
        running = False
    
    # clear screen
    screen.fill(WHITE)
    
    # draw epicenter and earthquake effects
    pygame.draw.circle(screen, RED, (epicenter_x, epicenter_y), 10)
    pygame.draw.line(screen, BLACK, (epicenter_x, epicenter_y), 
                     (epicenter_x + displacement * pygame.math.Vector2(1, 0).rotate(direction)[0],
                      epicenter_y + displacement * pygame.math.Vector2(1, 0).rotate(direction)[1]), 3)
    
    # update screen
    pygame.display.flip()
    
    # delay to control frame rate
    pygame.time.delay(10)

# print results
print("Results:")
print(f"Energy released: {energy:.2e} J")
print(f"Richter scale magnitude: {richter_scale:.2f}")
print(f"Mercalli scale intensity: {mercalli_scale:.2f}")
print(f"Fault type multiplier: {multiplier:.2f}")

# quit pygame
pygame.quit()
