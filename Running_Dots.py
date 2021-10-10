import pygame
import math  
import random
import time
import pygame.gfxdraw
from datetime import date
from datetime import datetime
import json
pygame.init()

# Get time and date
now = datetime.now()
dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")


# Define screen width and height
WIDTH = 1240
HEIGHT = 720
display = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)




clock = pygame.time.Clock()  # To set the frame rate
font = pygame.font.SysFont("Arial", 26) # set up font 


cx = random.randint(20, WIDTH - 20)
cy = random.randint(20, HEIGHT - 20)
width_of_circle = 30



#Variables
rts = ""
et = 0
tic = 0
toc = 0
counter = 0
counterF = 0
times = [] # to store the times between clicking and appearance of the dots

# get counter for successfull clicks
def get_counter():
    return font.render(f"successes: {counter}",5, pygame.Color("cyan"))
# get counter for failed clicks
def get_failCounter():
    return font.render(f"failuers: {counterF}",5, pygame.Color("red"))

# TODO:
# both game_over and get_percentage should be one method
# Make it so it shows percentages and numbers in a readable way

# Get texts for game over screen
def get_average():
    sm = sum(times)/(counter) if counter > 0 else counter == 1
    return sm
def game_over():
    return font.render(f"your sucess to failure percentage is: {(counter/(counter+counterF)) *100:.2f} %",20, pygame.Color("white"))
def get_percentage():
    # Try to think how we can skip a line so it looks like this
    #                   Game Over
    #    your sucess to failure percent is: 0.9
    # \n doesnt work for font render we probably need to split it into 2 objects (2 font renderers)
    
    
    return font.render(f"Game Over - your failure to sucess percentage is: {(counterF/(counter+counterF)) *100:.2f} % - your reaction time average: {get_average():.2f} in ms",1, pygame.Color("white"))

def get_time():
    return font.render(f"Reaction Time: {int(et)} in ms",1, pygame.Color("coral"))
def start():

    return font.render(f"{rts}",3, pygame.Color("white"))
# Main loop
while True:
    display.fill(BLACK)
    display.blit(get_counter(),(0,25))
    display.blit(get_failCounter(),(0,0))
    pygame.draw.circle(display,WHITE,  (cx, cy), width_of_circle)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit() # The reason for this is to prevent errors due to the loop going on, we need to quit the whole Python application
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if math.sqrt((pos[0]-cx)**2+(pos[1] - cy)**2) < width_of_circle:
                tic = time.time()
                if counter > 0: # Start the time count when we on the first circle
                    tic = toc
                rts = "Reaction Time Test Started"
                toc = time.time()
                et = (toc - tic) * 1000
                counter +=1
                cx = random.randint(20, WIDTH - 20)
                cy = random.randint(20, HEIGHT - 20)
                times.append(et)
            else:
                counterF +=1
                
    display.blit(get_time(),(0,50))
    display.blit(start(),((WIDTH/2)-125,HEIGHT-35))
    # max numbers of tries is: 10
    if counter > 10 or counterF > 9 or counter+counterF > 9:
        # Load a new loop/screen
        while True:
            display.fill(BLACK)
            display.blit(get_percentage(),(200,HEIGHT/2))
            display.blit(game_over(),(200,(HEIGHT/2)+30))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with open(f"Data/{dt_string}.json", 'w') as f:
                        json.dump({"date and time":dt_string,"average":get_average(), "failures":counterF,"successes":counter,"Success to failure percentage":counter/(counter+counterF),"failure to success percentage":counterF/(counter+counterF) },f)
                    pygame.quit()
                    quit()
            clock.tick(60)
            pygame.display.update()
    
    clock.tick(60)
    pygame.display.update()