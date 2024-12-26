from picographics import PicoGraphics, DISPLAY_TUFTY_2040
import pngdec

### Overridables
POWERMANAGEMENT = True
LED_GLIMMER = True

LOGO_OFFSET_Y = 20

NAME_MAX_SIZE = 8
PRONOUNS_MAX_SIZE = 20
SOCIAL_MAX_SIZE = 20
###

display = PicoGraphics(display=DISPLAY_TUFTY_2040)
WIDTH, HEIGHT = display.get_bounds()

# List of available pen colours, add more if necessary
RED = display.create_pen(209, 34, 41)
ORANGE = display.create_pen(246, 138, 30)
YELLOW = display.create_pen(255, 216, 0)
GREEN = display.create_pen(0, 121, 64)
INDIGO = display.create_pen(36, 64, 142)
VIOLET = display.create_pen(115, 41, 130)
WHITE = display.create_pen(255, 255, 255)
PINK = display.create_pen(255, 175, 200)
BLUE = display.create_pen(116, 215, 238)
BROWN = display.create_pen(97, 57, 21)
BLACK = display.create_pen(0, 0, 0)
MAGENTA = display.create_pen(255, 33, 140)
CYAN = display.create_pen(33, 177, 255)
AMETHYST = display.create_pen(156, 89, 209)

# load logo
png = pngdec.PNG(display)
try:
    png.open_file("rg_badge.png")
    # Decode our PNG file (320x240) to whole of screen
    png.decode(0, LOGO_OFFSET_Y)
except OSError:
    print("rg_badge.png missing")

# Details are autoloaded
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

# Change the colour of the text (swapping these works better on a light background)
NAME_COLOUR = CYAN
PRONOUNS_COLOUR = AMETHYST
SOCIAL_COLOUR = AMETHYST

#DROP_SHADOW_COLOUR = BLACK

# Set a starting scale for text size.
# This is intentionally bigger than will fit on the screen, we'll shrink it to fit.
name_size = NAME_MAX_SIZE
pronouns_size = PRONOUNS_MAX_SIZE
social_size = SOCIAL_MAX_SIZE

# These loops adjust the scale of the text until it fits on the screen
while True:
    display.set_font("bitmap8")
    name_length = display.measure_text(name, name_size)
    if name_length >= WIDTH - 20:
        name_size -= 1
    else:
        # comment out this section if you hate drop shadow
        #DROP_SHADOW_OFFSET = 5
        #display.set_pen(DROP_SHADOW_COLOUR)
        #display.text(NAME, int((WIDTH - name_length) / 2 + 10) - DROP_SHADOW_OFFSET, 10 + DROP_SHADOW_OFFSET, WIDTH, name_size)

        # draw name and stop looping
        display.set_pen(NAME_COLOUR)
        display.text(name, int((WIDTH - name_length) / 2), 0, WIDTH, name_size)
        break

while True:
    display.set_font("bitmap8")
    pronouns_length = display.measure_text(pronouns, pronouns_size)
    if pronouns_length >= WIDTH/2-20:
        pronouns_size -= 1
    else:
        # draw pronouns and stop looping
        display.set_pen(PRONOUNS_COLOUR)
        display.text(pronouns, WIDTH - pronouns_length, 0+(name_size*8), WIDTH, pronouns_size)
        break

while True:
    display.set_font("bitmap8")
    social_length = display.measure_text(social, social_size)
    if social_length >= WIDTH - 60:
        social_size -= 1
    else:
        # draw social and stop looping
        display.set_pen(SOCIAL_COLOUR)
        display.text(social, int((WIDTH - social_length) / 2), 240-(social_size*8), WIDTH, social_size)
        break

# Once all the adjusting and drawing is done, update the display.
display.update()

###
# automatic backlight management
import time
import micropython
from machine import ADC, Pin, PWM

pwm = PWM(Pin(25))
pwm.freq(1000)

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

low_battery = False

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
def powman():
    global luminance,backlight,vbat,on_usb,low_battery
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

print("entering backlight loop")
while POWERMANAGEMENT and not low_battery:
  if not LED_GLIMMER:
    # measure only every 100ms
    powman()
    time.sleep(0.1)
  else:
    # measure roughly every 100ms, fade the LED in the meantime
    for duty in range(65025):
      if duty % 1000 == 0:
        powman()
      pwm.duty_u16(duty)
      time.sleep(0.0001)
    for duty in range(65025, 0, -1):
      if duty % 1000 == 0:
        powman()
      pwm.duty_u16(duty)
      time.sleep(0.0001)

print("low power, reducing backlight to min")
display.set_backlight(BACKLIGHT_LOW)
