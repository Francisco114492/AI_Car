import pygame

# Constants
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 500
TRACK_IMAGE = "Track3.png"  # Make sure this file exists

# Load best path from file
def main():
    coll = []
    try:
        with open("collisions.txt", "r") as f:
            coll = [tuple(map(float, line.strip().split(","))) for line in f]
    except FileNotFoundError:
        print("Error: collisions.txt not found! Run the training first.")

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Collision locations")

    # Load and scale the track image
    track = pygame.image.load(TRACK_IMAGE).convert()
    track = pygame.transform.scale(track, (WINDOW_WIDTH, WINDOW_HEIGHT))

    running = True
    while running:
        screen.blit(track, (0, 0))  # Draw the track

        # Draw the path on top of the track
        for i in range(len(coll) - 1):
            pygame.draw.circle(screen, (255, 0, 0), coll[i], 3)  # Red line for path

        pygame.display.flip()  # Update display
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
