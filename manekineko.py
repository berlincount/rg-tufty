## we have a set of default includes, including color names etc
from includes import *

### Overridables
POWERMANAGEMENT = True

BACKGROUND = BLACK

name_config = {
  "color": CYAN,
  "max_size": 8,
  "max_width": WIDTH/2,
  "x_pos": WIDTH/2,
  "y_pos": 0,
}

pronouns_config = {
  "color": AMETHYST,
  "max_size": 20,
  "max_width": WIDTH/2,
  "x_pos": WIDTH/2,
  "y_pos": 80,
}

social_config = {
  "color": AMETHYST,
  "max_size": 20,
  "max_width": WIDTH/2+40,
  "x_pos": WIDTH/2,
  "y_pos": 200,
}

###

# load badge entries from file
name_config["text"], pronouns_config["text"], social_config["text"] = load_badge()

# calculate sizes of texts
name_config["size"]     = measure_text(display,name_config)
pronouns_config["size"] = measure_text(display,pronouns_config)
social_config["size"]   = measure_text(display,social_config)

# position texts relative to each other
pronouns_config["y_pos"] = 0+(name_config["size"]*8)
social_config["y_pos"] = HEIGHT-(social_config["size"]*8)

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

print("entering loop")
import pngdec
display.set_backlight(BACKLIGHT_HIGH)
if not low_battery:
  for i in range(60):
    framestart = time.time_ns()
    display.set_pen(BACKGROUND)
    display.clear()
    png = pngdec.PNG(display)
    try:
      png.open_file('manekineko_pngs/frame_%02d_delay-0.1s.png' % i)
    except OSError:
      # file not found, last frame
      break
    png.decode(0,0)

    draw_text(display,name_config)
    draw_text(display,pronouns_config)
    draw_text(display,social_config)

    display.update()
    
    # measure only every 100ms
    if POWERMANAGEMENT:
      if button_boot.is_pressed and not brighttimer:
        print("setting brighttimer for 10s brightness")
        brighttimer = time.time()+10
      powman()
    # the slowest frame we know needs 300ms - sync speed on that one
    time.sleep(0.3-((time.time_ns()-framestart)/1000000000))

print("low power, reducing backlight to min")
display.set_backlight(BACKLIGHT_LOW)
