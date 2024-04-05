import time
import gc
import displayio
import random
import digitalio
import math
import array
import board
import microcontroller
import terminalio
from adafruit_display_shapes.circle import Circle
from adafruit_display_text import label
from adafruit_ticks import ticks_ms

# Set up display
display = board.DISPLAY
display.auto_refresh=False

# Make the display context
main_group = displayio.Group()

# Make a background color fill
color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x000000
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
main_group.append(bg_sprite)

# Define Circle characteristics
circle_radius = int(display.height / 10)
circle = Circle(circle_radius+1, circle_radius+1, circle_radius, fill=0x00FF00, outline=0xFF00FF)
main_group.append(circle)

# Define Circle Animation Steps
delta_x = 1
delta_y = 1

# Text label
cpu_temp = label.Label(terminalio.FONT, text=" "*15, color=0xFF0000, scale=3)
cpu_temp.text = "CPU Temp:"+str(microcontroller.cpu.temperature)+"C"
cpu_temp.x = 10
cpu_temp.y = 15
fps_text = label.Label(terminalio.FONT, text=" "*15, color=0xFF0000, scale=3)
fps_text.x = 10
fps_text.y = 50
main_group.append(cpu_temp)
main_group.append(fps_text)

# Showing the items on the screen
display.root_group = main_group

# Counters for FPS calculation
last_frame = ticks_ms()
loop_count = 0

while True:
    loop_count += 1
    this_frame = ticks_ms()

    # If circle hits a wall
    if circle.y + circle_radius >= display.height - circle_radius:
        delta_y = -delta_y
        circle.fill = random.getrandbits(24)
    if circle.x + circle_radius >= display.width - circle_radius:
        delta_x = -delta_x
        circle.fill= random.getrandbits(24)
    if circle.x - circle_radius <= 0 - circle_radius:
        delta_x = -delta_x
        circle.fill=random.getrandbits(24)
    if circle.y - circle_radius <= 0 - circle_radius:
        delta_y = -delta_y
        circle.fill= random.getrandbits(24)

    # Update circle position
    circle.x = circle.x + delta_x
    circle.y = circle.y + delta_y

    # FPS and CPU data
    if(loop_count % 100 == 0):
        if((this_frame - last_frame) > 0):
            fps = 1000.0/(this_frame - last_frame)
            fps_text.text = "FPS:"+str(int(fps))
    if(loop_count > 1000):
        cpu_temp.text = "CPU Temp:"+str(microcontroller.cpu.temperature)+"C"
        loop_count = 0

    # Clean up and refresh display
    gc.collect()
    display.refresh()

    # Reset time for FPS calculation
    last_frame = this_frame



