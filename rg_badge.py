## we have a set of default includes, including color names etc
from includes import *

### Overridables
POWERMANAGEMENT = True
# LED_GLIMMER = True

BACKGROUND_COLOR = BLACK
LOGO_OFFSET_Y = 20

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
name_config["size"],name_config["width"]         = measure_text(display,name_config)
pronouns_config["size"],pronouns_config["width"] = measure_text(display,pronouns_config)
social_config["size"],social_config["width"]     = measure_text(display,social_config)

# position texts relative to each other
name_config["x_pos"] = (WIDTH-name_config["width"])/2
pronouns_config["x_pos"] = WIDTH-pronouns_config["width"]
pronouns_config["y_pos"] = 0+(name_config["size"]*8)
social_config["x_pos"] = (WIDTH-social_config["width"])/2
social_config["y_pos"] = HEIGHT-(social_config["size"]*8)

###
# clear display
display.set_pen(BACKGROUND_COLOR)
display.clear()

# load and show logo
import pngdec
png = pngdec.PNG(display)
try:
    png.open_file("rg_badge.png")
    # Decode our PNG file (320x240) to whole of screen
    png.decode(0, LOGO_OFFSET_Y)
except OSError:
    print("rg_badge.png missing")

# draw the texts as configured
draw_text(display,name_config)
draw_text(display,pronouns_config)
draw_text(display,social_config)

# Once all the adjusting and drawing is done, update the display.
display.update()

# run an event loop with glimmer, powermanagement, etc
main_loop(POWERMANAGEMENT,LED_GLIMMER)