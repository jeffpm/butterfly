from machine import Pin
from neopixel import Neopixel
from neotimer import *
import random
import time
import micropython

num_pixels = 21
#random lights come on if min_brightness is not 0
# TODO figure it out
min_brightness = 0
max_brightness = 50
chase_max_brightness = 100
chase_min_brightness = 10
pixels = Neopixel(num_pixels, 0, 28, "GRB")
pixels.brightness(max_brightness)
pixels.clear()
pixels.show

LIGHT_PINK = (204, 0, 102)
LIGHT_PURPLE = (102, 0, 204)
LIGHT_GREEN = (0, 255, 50)
LIGHT_BLUE = (0, 204, 102)
LIGHT_YELLOW = (255, 255, 50)
WHITE = (255, 255, 255)

COLORS = [LIGHT_PINK, LIGHT_PURPLE, LIGHT_GREEN, LIGHT_BLUE, LIGHT_YELLOW, WHITE]

def test_colors():
    for x in COLORS:
        pixels.clear()
        pixels.fill(x, max_brightness)
        pixels.show()
        time.sleep(3)

def get_unique_random_colors(num=2):
    unique_colors = list()
    while len(unique_colors) < num:
        x1 = random.randint(0, len(COLORS)-1)
        if COLORS[x1] not in unique_colors:
            unique_colors.append(COLORS[x1])
    
    return unique_colors
def show_fade():
    brightness = min_brightness
    color = COLORS[random.randint(0, len(COLORS) - 1)]

    for x in range(min_brightness, max_brightness):
        pixels.fill(color, x)
        pixels.show()
        time.sleep(.05)
        
    for x in range(max_brightness, min_brightness, -1):
        pixels.fill(color, x)
        pixels.show()
        time.sleep(.05)
        
def show_pinwheel():
    our_colors = get_unique_random_colors(2)
    pixels.clear()
    pixels.set_pixel_line(0, int(num_pixels / 2), our_colors[0], int(max_brightness / 3))
    pixels.set_pixel_line(int(num_pixels / 2), num_pixels - 1, our_colors[1], int(max_brightness / 3))
    pixels.show()
    pinwheel_timer = Neotimer(10000)
    pinwheel_timer.start()
    while (not pinwheel_timer.finished()):
        pixels.rotate_right(1)
        pixels.show()
        time.sleep(0.025)
    
    
def show_swirl():
    x1 = random.randint(0, len(COLORS)-1)
    x2 = random.randint(0, len(COLORS)-1)
    while (x1 == x2):
        x2 = random.randint(0, len(COLORS)-1)
    
    pixels.clear()
    
    # fade in
    x = min_brightness
    pixels.set_pixel_line_gradient(0, num_pixels-1, COLORS[x1], COLORS[x2], x)
    pixels.show()
    while (x < int(max_brightness / 2)):
        time.sleep(0.02)
        pixels.set_pixel_line_gradient(0, num_pixels-1, COLORS[x1], COLORS[x2], x)
        pixels.show()
        x += 1
    
    #pixels.set_pixel_line_gradient(0, num_pixels-1, COLORS[x1], COLORS[x2], int(max_brightness / 2))
    pixels.show()
    swirl_timer = Neotimer(10000)
    swirl_timer.start()
    while (not swirl_timer.finished()):
        pixels.rotate_right()
        pixels.show()
        time.sleep(0.1)
    
    #fade out
    x = int(max_brightness / 2)
    pixels.set_pixel_line_gradient(0, num_pixels-1, COLORS[x1], COLORS[x2], x)
    pixels.show()
    while (x > min_brightness):
        time.sleep(0.02)
        pixels.set_pixel_line_gradient(0, num_pixels-1, COLORS[x1], COLORS[x2], x)
        pixels.show()
        x -= 1

def show_chase():
    pixels.clear()
    brightness = random.randint(0, chase_max_brightness)
    pixels.set_pixel(0, WHITE, brightness)
    pixels.show()
    for _ in range(0, num_pixels - 1):
        pixels.rotate_left()
        pixels.show()
        interval = int(chase_max_brightness / 10)
        if (random.randint(0, 1)):
            interval *= -1
            
        brightness += interval
        if brightness < chase_min_brightness:
            brightness = chase_min_brightness
        elif brightness > chase_max_brightness:
            brightness = chase_max_brightness
        time.sleep(0.05)
        

def show_twinkle():
    pixels.clear()
    led_slots = list()
    brightness_slots = list()
    color_slots = list()
    
    # generate a list of random leds to show
    while (len(led_slots) < num_pixels/2):
        x = random.randint(0, num_pixels - 1)
        if x not in led_slots:
            led_slots.append(x)
            
    #generate a random list of starting brightness
    #each element is a list of (brightness value, and iterator (1/-1)
    for x in range(num_pixels):
        brightness_slots.append([random.randint(0, int(max_brightness / 2)), 1])
        
    #generate a random list of starting colors
    for x in range(num_pixels):
        color_slots.append(COLORS[random.randint(0, len(COLORS)-1)])
    
    # generate a random color and brightness for each led
    for x in led_slots:
        pixels.set_pixel(x, color_slots[x], brightness_slots[x][0])
        pixels.show()
        time.sleep((random.random()*5)/10)
        
    # run the fade for x number of seconds
    fader_timer = Neotimer(10000)
    fader_timer.start()
    while (not fader_timer.finished()):
    # increase/decrease the brightness of an led
        for x in brightness_slots:
            if x[0] >= max_brightness:
                x[1] = -2
                x[0] = max_brightness
            elif x[0] <= min_brightness:
                x[1] = 2
                x[0] = min_brightness
                
            x[0] += x[1]
        for x in led_slots:
            pixels.set_pixel(x, color_slots[x], brightness_slots[x][0])
            pixels.show()
            time.sleep(0.001)

    time.sleep(0.5)
    #shutdown (fade all leds to min_brightness)
    while (not all([b[0] == min_brightness for b in brightness_slots])):
        for x in brightness_slots:
            if x[0] != min_brightness:
                x[0] -= 2
        for x in led_slots:
            pixels.set_pixel(x, color_slots[x], brightness_slots[x][0])
            pixels.show()
        time.sleep(0.05)
    #time.sleep(1)

pixels.clear()
pixels.show()
while(True):
    
#     test_colors()
    for x in range(random.randint(2,4)):
        show_fade()
    for x in range(random.randint(1,3)):
        show_swirl()
    for x in range(random.randint(1,3)):
        show_twinkle()
    for x in range(random.randint(1,3)):
        show_pinwheel()
    for x in range(random.randint(2,5)):
        show_chase()


