import pygame, pygame.camera
# Add a camera to the Pygame window
camera = pygame.camera.Camera(pygame.display.get_surface(), (1200, 2000))

# Start the camera
camera.start()

# Get an image from the camera
image = camera.get_image()
screen.blit(image, (0,0))
pygame.display.update()