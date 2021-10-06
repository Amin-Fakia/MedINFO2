import pygame
import math  
import random

pygame.init()


# Define screen width and height
WIDTH = 1600
HEIGHT = 900
display = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)




clock = pygame.time.Clock()  # To set the frame rate

font = pygame.font.SysFont("Arial", 18)


cx = random.randint(20, WIDTH - 20)
cy = random.randint(20, HEIGHT - 20)
width_of_circle = random.randint(14, 20)
cn = 0

def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text

def timer():
    txt = str()
# Main loop
while True:
    current_time = pygame.time.get_ticks()
    display.fill(BLACK)
    display.blit(update_fps(), (10,0))
    
    
    pygame.draw.circle(display, WHITE, (cx, cy), width_of_circle)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit() # The reason for this is to prevent errors due to the loop going on, we need to quit the whole Python application
    
    # TODO: Extract to a method
    mousex = pygame.mouse.get_pos()[0]
    mousey = pygame.mouse.get_pos()[1]
    click = pygame.mouse.get_pressed()
    sqx = (mousex - cx)**2
    sqy = (mousey - cy)**2

    # TODO: Extract to a method
    if math.sqrt(sqx + sqy) < width_of_circle and click[0] == 1:
        cx = random.randint(20, WIDTH - 20)
        cy = random.randint(20, HEIGHT - 20)
        width_of_circle = random.randint(14, 20)
        pygame.draw.circle(display, WHITE, (cx, cy), width_of_circle)
    
    
    clock.tick(60)
    pygame.display.update()
