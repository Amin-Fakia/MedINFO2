import pygame
import math
import random
import time
import matplotlib
matplotlib.use("Agg")
from datetime import date
from datetime import datetime
import json
import pylab
from pygame.locals import *
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg

fig = pylab.figure(figsize=[4, 4], # Inches
                   dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                   )
ax = fig.gca()
ax.plot()
# Remove top and right border
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

canvas = agg.FigureCanvasAgg(fig)
canvas.draw()
renderer = canvas.get_renderer()
raw_data = renderer.tostring_rgb()
size = canvas.get_width_height()
surf = pygame.image.fromstring(raw_data, size, "RGB")


pygame.init()



# Get time and date
now = datetime.now()
dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")


# Define screen width and height
WIDTH = 1240
HEIGHT = 720
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Running Dots')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

clock = pygame.time.Clock()  # To set the frame rate
font = pygame.font.SysFont("Calibri", 22)  # set up font
font1 = pygame.font.SysFont("Calibri", 19)
font2 = pygame.font.SysFont("Calibri", 40)

cx = random.randint(110, 790)
cy = random.randint(110, 660)
width_of_circle = 15

# Variables
rts = ""
et = 0
tic = 0
toc = 0
counter = 0
counterF = 0
num_t = 20 # number of tries
times = []  # to store the times between clicking and appearance of the dots

# Get text for start screen
def game_start():
    return font.render("Versuche so schnell wie möglich auf den schwarzen Punkt zu klicken", True, BLACK)


# get counter for successful clicks
def get_counter():
    return font.render(f"Hits: {counter}", True, GREEN)


# get counter for failed clicks
def get_failCounter():
    return font.render(f"Misses: {counterF}", True, RED)


def get_time():
    return font.render(f"Reaktionszeit: {int(et)} ms", True, BLUE)

def get_average():
    sm = sum(times)/(counter) if counter > 0 else counter == 1
    return sm




# Get text for game over screen
def game_over():
    return font2.render("Game Over", True, RED)


def game_success():
    return font1.render(f"Deine Treffer in Prozente: {(counter / (counter + counterF)) * 100:.2f} %", True, BLACK)


def get_percentage():
    sm = sum(times) / counter if counter > 0 else counter == 1

    return font1.render(
        f"Deine durchschnittliche Reaktionszeit: {sm:.2f} ms", True, BLACK)


def start():
    return font.render(f"{rts}", True, BLACK)

def getData():
    return 1

# Main loop
while True:
    display.fill(WHITE)
    display.blit(game_start(), (20, 30))
    display.blit(get_counter(), (820, 100))
    display.blit(get_failCounter(), (820, 125))
    
    pygame.draw.polygon(display, BLACK, ((20, 100), (20, 670), (800, 670), (800, 100)), 2)
    pygame.draw.circle(display, BLACK, (cx, cy), width_of_circle)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()  # The reason for this is to prevent errors due to the loop going on, we need to quit the whole Python application
        if event.type == pygame.MOUSEBUTTONUP and event.button ==1:
            
            pos = pygame.mouse.get_pos()
            if math.sqrt((pos[0] - cx) ** 2 + (pos[1] - cy) ** 2) < width_of_circle:
                tic = time.time()
                if counter > 0:  # Start the time count when we click on the first circle
                    tic = toc
                rts = "Reaction Time Test Started"
                toc = time.time()
                et = (toc - tic) * 1000
                counter += 1
                cx = random.randint(110, 790)
                cy = random.randint(110, 660)
                times.append(et)
                ax.plot(times,'blue')
                canvas = agg.FigureCanvasAgg(fig)
                canvas.draw()
                renderer = canvas.get_renderer()
                raw_data = renderer.tostring_rgb()
                size = canvas.get_width_height()
                surf = pygame.image.fromstring(raw_data, size, "RGB")
                
            else:
                counterF += 1

    display.blit(get_time(), (820, 150))
    display.blit(start(), ((WIDTH / 2) - 125, HEIGHT - 35))
    display.blit(surf, (WIDTH-425,HEIGHT-400))
    # max numbers of tries is: 10
    if counter > num_t or counterF > num_t or counter + counterF > num_t:
        # Load a new loop/screen
        while True:
            # display.fill(WHITE)
            display.blit(game_over(), (320, (HEIGHT / 2)))
            display.blit(game_success(), (820, (HEIGHT / 2)-60))
            display.blit(get_percentage(), (820, (HEIGHT / 2)-40))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with open(f"Data/{dt_string}.json", 'w') as f:
                        json.dump({"date and time":dt_string,"average":get_average(),
                                   "failures":counterF,
                                   "successes":counter,
                                   "Success to failure percentage":counter/(counter+counterF),
                                   "failure to success percentage":counterF/(counter+counterF) },f)
                    pygame.quit()
                    quit()
            clock.tick(60)
            pygame.display.update()

    pygame.display.flip()
    clock.tick(60)
    pygame.display.update()

