## we have a set of default includes, including color names etc
from includes import *

### Overridables
POWERMANAGEMENT = True
# LED_GLIMMER = True

BACKGROUND_COLOR = BLACK
LOGO_OFFSET_Y = 20

# 38C3 Colors
# Primary - Coral Red - #FF5053
CORAL_RED_38C3 = display.create_pen(255, 80, 83)
# Highlight - Pearl White - #FEF2FF
PEARL_WHITE_38C3 = display.create_pen(254, 242, 255)
# Accent 2 - Periwinkle - #B2AAFF
PERIWINKLE_38C3 = display.create_pen(178,170,255)
# Accent 1 - Amethyst - #6A5FDB
AMETHYST_38C3 = display.create_pen(106, 95, 219)
# Accent 3 - Dark Purple - #261A66
DARK_PURPLE_38C3 = display.create_pen(38, 26, 102)
# Accent 4 - Aubergine - #29114C
AUBERGINE_38C3 = display.create_pen(41, 17, 76)
# Accent 5 - Dark Aubergine - #190B2F
DARK_AUBERGINE_38C3 = display.create_pen(25, 11, 47)

name_config = {
  "font": "Pilowlava-Regular",
  "color": CORAL_RED_38C3,
  "max_size": 120,
  "max_width": WIDTH/2,
  "x_pos": WIDTH/2,
  "y_pos": 0,
}

pronouns_config = {
  "font": "SpaceMono-Regular",
  "color": AMETHYST_38C3,
  "max_size": 120,
  "max_width": WIDTH/2,
  "x_pos": WIDTH/2,
  "y_pos": 80,
}

social_config = {
  "font": "SpaceMono-Regular",
  "color": AMETHYST_38C3,
  "max_size": 120,
  "max_width": WIDTH/2+40,
  "x_pos": WIDTH/2,
  "y_pos": 200,
}

###

# load badge entries from file
name_config["text"], pronouns_config["text"], social_config["text"] = load_badge()

# calculate sizes of texts
name_config.update(measure_text(display,name_config))
pronouns_config.update(measure_text(display,pronouns_config))
social_config.update(measure_text(display,social_config))

# position texts relative to each other
name_config["x_pos"] = (WIDTH-name_config["width"])/2
pronouns_config["x_pos"] = WIDTH-pronouns_config["width"]
pronouns_config["y_pos"] = 0+(name_config["height"])
social_config["x_pos"] = (WIDTH-social_config["width"])/2
social_config["y_pos"] = HEIGHT-(social_config["height"])

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