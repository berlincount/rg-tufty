from picographics import PicoGraphics, DISPLAY_TUFTY_2040
from pimoroni import Button

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

# support buttons
button_a = Button(7, invert=False)
button_b = Button(8, invert=False)
button_c = Button(9, invert=False)
button_up = Button(22, invert=False)
button_down = Button(6, invert=False)
button_boot = Button(23, invert=True)

# vector
vector = False
transform = False
def init_vector():
  global vector,transform
  from picovector import PicoVector, ANTIALIAS_BEST
  vector = PicoVector(display)
  transform = Transform()
  vector.set_transform(transform)
  vector.set_antialiasing(ANTIALIAS_BEST)
  print("vector initialized")

def measure_text_bitmap(display,config):
  cur_size = config["max_size"]
  while True:
    cur_width = display.measure_text(config["text"], cur_size)
    if cur_width >= config["max_width"]:
      cur_size -= 1
    else:
      break

  # FIXME: the height is only correct for bitmap8
  return {
    "size": cur_size,
    "width": cur_width,
    "height": cur_size*8,
    "x_offset": 0,
    "y_offset": 0,
  }

def measure_text(display, config):
  if not "font" in config:
    display.set_font("bitmap8")
    return measure_text_bitmap(display,config)
  elif config["font"].startswith("bitmap"):
    display.set_font(config["font"])
    return measure_text_bitmap(display,config)

  if not vector or not transform:
    init_vector()

  cur_size = config["max_size"]

  fontfile = "fonts/"+config["font"]+".af"
  try:
    vector.set_font(fontfile,cur_size)
  except OSError:
    print("font file %s could not be loaded" % fontfile)

  x = 0
  y = 0
  while True:
    vector.set_font_size(cur_size)
    x,y,cur_width,cur_height = vector.measure_text(config["text"])
    print(config["font"],x,y,cur_width,cur_height)
    if cur_width >= config["max_width"]:
      cur_size -= 1
    else:
      break

  return {
    "size": cur_size,
    "width": cur_width,
    "height": cur_height,
    "x_offset": -x,
    "y_offset": -y,
  }

def draw_text_bitmap(display,config):
  display.text(
    config["text"],
    int(config["x_pos"])+int(config["x_offset"]),
    int(config["y_pos"])+int(config["y_offset"]),
    int(WIDTH),
    int(config["size"])
  )

def draw_text(display,config):
  # print(config)
  display.set_pen(config["color"])
  if not "font" in config:
    display.set_font("bitmap8")
    return draw_text_bitmap(display,config)
  elif config["font"].startswith("bitmap"):
    display.set_font(config["font"])
    return draw_text_bitmap(display,config)

  if not vector or not transform:
    init_vector()

  fontfile = "fonts/"+config["font"]+".af"
  try:
    vector.set_font(fontfile, int(config["size"]))
  except OSError:
    print("font file %s could not be loaded" % fontfile)

  print(config)
  vector.text(
    config["text"],
    int(config["x_pos"]+config["x_offset"]),
    int(config["y_pos"]+config["y_offset"]+config["height"]),
  )

def load_badge(filename = "badge.txt"):
  # Read name from file
  try:
    file = open(filename, "r")
  except OSError:
    with open(filename, "w") as f:
        f.write("edit %s :)\n" % filename)
        f.write("pronouns can be given\n")
        f.write("and social as well\n")
        f.flush()
    file = open(filename, "r")

  # Read the name in any case
  name = file.readline().strip()

  # Try reading the pronouns
  try:
    pronouns = file.readline().strip()
  except:
    pronouns = ""

  # Try reading the dect
  try:
    dect = file.readline().strip()
  except:
    dect = ""
    
  # Try reading the social
  try:
    social = file.readline().strip()
  except:
    social = ""

  file.close()

  return name, pronouns, dect, social

### Powermanagement / Brightness from here on
import time
import micropython
from machine import ADC,Pin,PWM

POWERMANAGEMENT = False
LED_GLIMMER = False

BACKLIGHT_LOW = micropython.const(0.375)
BACKLIGHT_HIGH = micropython.const(1.0)
LUMINANCE_LOW = micropython.const(384)
LUMINANCE_HIGH = micropython.const(1260)
LOW_BATTERY_VOLTAGE = micropython.const(3.1)

# measurables
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
low_battery = False
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
brighttimer = 0

def powman():
  global luminance,backlight,vbat,on_usb,low_battery,brighttimer
  if brighttimer and time.time() < brighttimer:
    # bright backlight on timer
    display.set_backlight(BACKLIGHT_HIGH)
    return
  elif brighttimer:
    print("brighttimer expired")
    brighttimer = 0

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

def default_loop():
  global button_boot,brighttimer
  display.set_backlight(1.0)

  print("entering default loop")
  while not low_battery:
    if button_boot.is_pressed and not brighttimer:
      print("setting brighttimer for 10s brightness")
      brighttimer = time.time()+10

    powman()
    time.sleep(0.1)

  print("low power, reducing backlight to min")
  display.set_backlight(BACKLIGHT_LOW)

def glimmer_loop(POWERMANAGEMENT):
  global button_boot,brighttimer
  pwm = PWM(Pin(25))
  pwm.freq(1000)

  display.set_backlight(1.0)

  print("entering glimmer loop")
  while not low_battery:
    if POWERMANAGEMENT and button_boot.is_pressed and not brighttimer:
      print("setting brighttimer for 10s brightness")
      brighttimer = time.time()+10

    for duty in range(65025):
      if POWERMANAGEMENT and duty % 1000 == 0:
        powman()
      pwm.duty_u16(duty)
      time.sleep(0.0001)
      if button_boot.is_pressed:
        # handle immediately
        break
    for duty in range(65025, 0, -1):
      if POWERMANAGEMENT and duty % 1000 == 0:
        powman()
      pwm.duty_u16(duty)
      time.sleep(0.0001)
      if button_boot.is_pressed:
        # handle immediately
        break

  print("low power, reducing backlight to min")
  display.set_backlight(BACKLIGHT_LOW)

def main_loop(powermanagement,led_glimmer):
  if led_glimmer:
    glimmer_loop(powermanagement)
  elif powermanagement:
    default_loop()
  else:
    print("no loop type selected")
