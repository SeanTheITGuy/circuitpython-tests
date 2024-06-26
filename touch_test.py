import time
import board
import displayio
import terminalio
from adafruit_display_text import label
from xpt2046 import Touch

DISPLAY_WIDTH = 320
DISPLAY_HEIGHT = 240
DISPLAY_ROTATION = 0

# Touch calibration
TOUCH_X_MIN = 100
TOUCH_X_MAX = 1996
TOUCH_Y_MIN = 100
TOUCH_Y_MAX = 1996

spi = board.TOUCH_SPI()
display=board.DISPLAY

# Instantiate the touchpad
touch = Touch(
    spi=spi,
    cs=board.TOUCH_CS,
    width=DISPLAY_WIDTH,
    height=DISPLAY_HEIGHT,
    rotation=DISPLAY_ROTATION,
    x_min=TOUCH_X_MIN,
    x_max=TOUCH_X_MAX,
    y_min=TOUCH_Y_MIN,
    y_max=TOUCH_Y_MAX,
)

# Quick Colors for Labels
TEXT_BLACK = 0x000000
TEXT_BLUE = 0x0000FF
TEXT_CYAN = 0x00FFFF
TEXT_GRAY = 0x8B8B8B
TEXT_GREEN = 0x00FF00
TEXT_LIGHTBLUE = 0x90C7FF
TEXT_MAGENTA = 0xFF00FF
TEXT_ORANGE = 0xFFA500
TEXT_PURPLE = 0x800080
TEXT_RED = 0xFF0000
TEXT_WHITE = 0xFFFFFF
TEXT_YELLOW = 0xFFFF00

def make_my_label(font, anchor_point, anchored_position, scale, color):
    func_label = label.Label(font)
    func_label.anchor_point = anchor_point
    func_label.anchored_position = anchored_position
    func_label.scale = scale
    func_label.color = color
    return func_label

instructions_label = make_my_label(
    terminalio.FONT, (0.5, 0.5), (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 4), 2, TEXT_WHITE
)
x_min_label = make_my_label(
    terminalio.FONT, (0.0, 0.0), (10, DISPLAY_HEIGHT/2), 2, TEXT_WHITE
)
x_max_label = make_my_label(
    terminalio.FONT, (1.0, 0.0), (DISPLAY_WIDTH - 10, DISPLAY_HEIGHT/2), 2, TEXT_WHITE
)
y_min_label = make_my_label(
    terminalio.FONT, (0.5, 0.0), (DISPLAY_WIDTH / 2, 10), 2, TEXT_WHITE
)
y_max_label = make_my_label(
    terminalio.FONT, (0.5, 1.0), (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT - 10), 2, TEXT_WHITE
)

main_group = displayio.Group()
main_group.append(x_min_label)
main_group.append(x_max_label)
main_group.append(y_min_label)
main_group.append(y_max_label)
main_group.append(instructions_label)
display.root_group = main_group

                
print("Go Ahead - Touch the Screen - Make My Day!")

x = y = 0
x_min = y_min = x_max = y_max = min(DISPLAY_WIDTH, DISPLAY_HEIGHT) // 2
x_min_label.text = f"X-Min:{x_min}"
x_max_label.text = f"X-Max:{x_max}"
y_min_label.text = f"Y-Min:{y_min}"
y_max_label.text = f"Y-Max:{y_max}"
instructions_label.text = f"draw swirlies on corners to calibrate"

while True:
    x = touch.raw_touch()
    if x is not None:
        x_min = min(x_min, x[0])
        x_max = max(x_max, x[0])
        y_min = min(y_min, x[1])
        y_max = max(y_max, x[1])
        print(f"(({x_min}, {x_max}), ({y_min}, {y_max}))")
        x_min_label.text = f"X-Min:{x_min}"
        x_max_label.text = f"X-Max:{x_max}"
        y_min_label.text = f"Y-Min:{y_min}"
        y_max_label.text = f"Y-Max:{y_max}"
        time.sleep(0.05)