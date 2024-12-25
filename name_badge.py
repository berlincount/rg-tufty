from picographics import PicoGraphics, DISPLAY_TUFTY_2040

display = PicoGraphics(display=DISPLAY_TUFTY_2040)
WIDTH, HEIGHT = display.get_bounds()

###
# Tufty constants
A = 7
B = 8
C = 15
UP = 22
DOWN = 6
LED = 25

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
RED = display.create_pen(200, 0, 0)
BLUE = display.create_pen(0, 0, 200)

###
# Read name from file
try:
    file = open("badge.txt", "r")
except OSError:
    with open("badge.txt", "w") as f:
        f.write("edit badge.txt :)\n")
        f.write("pronouns can be given\n")
        f.write("and social as well\n")
        f.flush()
    file = open("badge.txt", "r")

# Read the name in any case
name = file.readline().strip()

# Try reading the pronouns
try:
  pronouns = file.readline().strip()
except:
  pronouns = ""

# Try reading the social
try:
  social = file.readline().strip()
except:
  social = ""

file.close()

text_size1 = 12
text_size2 = 12
text_size3 = 12

text_x1 = 0
text_y1 = 100

# Clear the screen
display.set_pen(WHITE)
display.clear()
display.update()
print("screen cleared")

# Draws a blank badge
def draw_badge():
    display.set_pen(RED)
    display.rectangle(0, 0, WIDTH, 60)
    display.rectangle(0, HEIGHT - 20, WIDTH, 50)
    display.set_pen(WHITE)
    display.text("HELLO", 125, 5, 0, 3)
    display.text("My name is:", 110, 35, 320, 2)
    display.update()
    print("badge drawn")


def calculate_text_size(text, text_size):
    new_text_size = text_size
    text_width = display.measure_text(text, text_size)
    # Calculate the width of the text in pixels, adjusts according to the screen width
    while text_width > 290:
        new_text_size -= 1
        text_width = display.measure_text(text, new_text_size)

    # Calculate the margin to be applied on X
    margin_x = (WIDTH - text_width) / 2

    return int(margin_x), new_text_size


draw_badge()
text_x1,text_size1 = calculate_text_size(name, text_size1)
text_size2 = text_size1-1 # pronouns always smaller than name
text_x2,text_size2 = calculate_text_size(pronouns, text_size2)
text_size3 = text_size1-1 # social always smaller than name
text_x3,text_size3 = calculate_text_size(social, text_size3)

display.set_pen(BLACK)

# leave space for pronouns and social if needed (8 is the bitmap font height, size is the scale factor)
if name and pronouns and social:
    text_y1 = 60
    text_y2 = text_y1+8*(text_size1-1)
    text_y3 = text_y1+8*(text_size1-1)+8*(text_size2-1)
elif (name and pronouns) or (name and social):
    text_y1 = 85
    text_y2 = text_y1+8*(text_size1)
    text_y3 = text_y1+8*(text_size1)
    
display.text(name, text_x1, text_y1, 300, text_size1)
# display.set_pen(BLUE)
if pronouns:
  display.text(pronouns, text_x2, text_y2, 300, text_size2)
if social:
  display.text(social, text_x3, text_y3, 300, text_size3)
display.update()
print("texts drawn")

###
# automatic backlight management
import time
import micropython
from machine import ADC, Pin

display.set_backlight(1.0)
BACKLIGHT_LOW = micropython.const(0.375)
BACKLIGHT_HIGH = micropython.const(1.0)
LUMINANCE_LOW = micropython.const(384)
LUMINANCE_HIGH = micropython.const(2048)
LOW_BATTERY_VOLTAGE = micropython.const(3.1)
lux_vref_pwr = Pin(27, Pin.OUT)
lux = ADC(Pin(26))
vbat_adc = ADC(Pin(29))
vref_adc = ADC(Pin(28))
usb_power = Pin(24, Pin.IN)

# Returns a tuple of the raw luminance value, and the brightness to now use.
def auto_brightness(previous: float) -> (float, float):
    luminance = lux.read_u16()
    luminance_frac = max(0.0, float(luminance - LUMINANCE_LOW))
    luminance_frac = min(1.0, luminance_frac / (LUMINANCE_HIGH - LUMINANCE_LOW))
    backlight = BACKLIGHT_LOW + (luminance_frac * (BACKLIGHT_HIGH - BACKLIGHT_LOW))
    # Use the previous value to smooth out changes to reduce flickering.
    # The "32" value here controls how quickly it reacts (larger = slower).
    # The rate at which the main loop calls us also affects that!
    backlight_diff = backlight - previous
    backlight = previous + (backlight_diff * (1.0 / 32.0))
    return (luminance, backlight)


# Returns a tuple of voltage (fake value if on USB), "is on USB", and "is low".
def measure_battery() -> (float, bool, bool):
    if usb_power.value():
        return (5.0, True, False)

    # See the battery.py example for how this works.
    vdd = 1.24 * (65535 / vref_adc.read_u16())
    vbat = ((vbat_adc.read_u16() / 65535) * 3 * vdd)

    low_battery = False
    if vbat < LOW_BATTERY_VOLTAGE:
        low_battery = True
    return (vbat, False, low_battery)

backlight = BACKLIGHT_LOW
print("entering backlight loop")
while True:
    # Turn on VREF and LUX only while we measure things.
    lux_vref_pwr.value(1)
    (vbat, on_usb, low_battery) = measure_battery()
    if low_battery:
        backlight = BACKLIGHT_LOW
    else:
        (luminance, backlight) = auto_brightness(backlight)
    lux_vref_pwr.value(0)

    # Set the new backlight value.
    display.set_backlight(backlight)

    # measure every 100ms
    time.sleep(0.1)
