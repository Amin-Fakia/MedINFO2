import pygame
import math  
import random

pygame.init()


# Define screen width and height
WIDTH = 920
HEIGHT = 400
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


counter = 0
counterF = 0
times = [] # to store the times between clicking and appearance of the dots
def get_counter():
    return font.render(f"sucesses: {counter}",1, pygame.Color("coral"))
def get_failCounter():
    return font.render(f"failuers: {counterF}",1, pygame.Color("coral"))
def game_over():
    return font.render("Game Over",10, pygame.Color("coral"))
def get_percentage():
    # Try to think how we can skip a line so it looks like this
    #                   Game Over
    #    your sucess to failure percent is: 0.9
    # \n doesnt work for font render we probably need to split it into 2 objects (2 font renderers)
    return font.render(f"Game Over - your failure to sucess percentage is: {(counterF/(counter+counterF)) *100:.2f} %",5, pygame.Color("coral"))
# Main loop
while True:
    current_time = pygame.time.get_ticks()
    display.fill(BLACK)
    display.blit(get_counter(),(WIDTH-100,0))
    display.blit(get_failCounter(),(0,0))
    pygame.draw.circle(display, WHITE, (cx, cy), width_of_circle)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit() # The reason for this is to prevent errors due to the loop going on, we need to quit the whole Python application
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            # TODO: implement a timer in miliseconds 
            if math.sqrt((pos[0]-cx)**2+(pos[1] - cy)**2) < width_of_circle:
                counter +=1
                cx = random.randint(20, WIDTH - 20)
                cy = random.randint(20, HEIGHT - 20)
                width_of_circle = random.randint(14, 20)
                pygame.draw.circle(display, WHITE, (cx, cy), width_of_circle)
            else:
                counterF +=1
                

    if counter > 10 or counterF > 10:
        while True:
            display.fill(BLACK)
            display.blit(get_percentage(),(WIDTH/2.15,HEIGHT/2))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            clock.tick(60)
            pygame.display.update()
    
    clock.tick(60)
    pygame.display.update()
