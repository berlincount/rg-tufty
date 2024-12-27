## we have a set of default includes, including color names etc
from includes import *

### Overridables
POWERMANAGEMENT = True

BACKGROUND_COLOR = BLACK

name_config = {
  "font": "SpaceMono-Regular",
  "color": WHITE,
  "max_size": 90,
  "max_width": WIDTH-20,
  "x_pos": WIDTH/2,
  "y_pos": 10,
}

pronouns_config = {
  "font": "SpaceMono-Regular",
  "color": WHITE,
  "max_size": 60,
  "max_width": WIDTH-60,
  "x_pos": WIDTH/2,
  "y_pos": 175,
}

# A name badge with customisable Pride flag background.

# If adding your own, colour order is left to right (or top to bottom)
COLOUR_ORDER = [RED, ORANGE, YELLOW, GREEN, INDIGO, VIOLET]  # traditional pride flag
# COLOUR_ORDER = [BLACK, BROWN, RED, ORANGE, YELLOW, GREEN, INDIGO, VIOLET]  # Philadelphia pride flag
# COLOUR_ORDER = [BLUE, PINK, WHITE, PINK, BLUE]  # trans flag
# COLOUR_ORDER = [MAGENTA, YELLOW, CYAN]  # pan flag
# COLOUR_ORDER = [MAGENTA, VIOLET, INDIGO]  # bi flag
# COLOUR_ORDER = [YELLOW, WHITE, AMETHYST, BLACK]  # non-binary flag

# Add chevrons to the left
# CHEVRONS = [] # No chevrons
CHEVRONS = [WHITE, PINK, BLUE, BROWN, BLACK]  # Progress Pride Flag
# Initial chevron height compared to screen height
FIRST_CHEVRON_HEIGHT = 0.4

# Change this for vertical stripes
STRIPES_DIRECTION = "horizontal"

###

# load badge entries from file
name_config["text"], pronouns_config["text"], _ = load_badge()

# calculate sizes of texts
name_config.update(measure_text(display,name_config))
pronouns_config.update(measure_text(display,pronouns_config))

# position texts relative to each other
name_config["x_pos"] = (WIDTH-name_config["width"])/2+10
pronouns_config["x_pos"] = (WIDTH-pronouns_config["width"])/2

# Draw the flag
if STRIPES_DIRECTION == "horizontal":
    stripe_width = round(HEIGHT / len(COLOUR_ORDER))
    for x in range(len(COLOUR_ORDER)):
        display.set_pen(COLOUR_ORDER[x])
        display.rectangle(0, stripe_width * x, WIDTH, stripe_width)

if STRIPES_DIRECTION == "vertical":
    stripe_width = round(WIDTH / len(COLOUR_ORDER))
    for x in range(len(COLOUR_ORDER)):
        display.set_pen(COLOUR_ORDER[x])
        display.rectangle(stripe_width * x, 0, stripe_width, HEIGHT)

if len(CHEVRONS) > 0:
    import math
    stripe_width = round((HEIGHT * (1 - FIRST_CHEVRON_HEIGHT)) / len(CHEVRONS))
    offset = -stripe_width * math.floor((len(CHEVRONS) + 1) / 2)
    middle = round(HEIGHT / 2)
    for x in range(len(CHEVRONS) - 1, -1, -1):
        display.set_pen(CHEVRONS[x])
        display.triangle(
            x * stripe_width + offset, -stripe_width,
            (x + 1) * stripe_width + offset + middle, middle,
            x * stripe_width + offset, HEIGHT + stripe_width)

# Once all the adjusting and drawing is done, update the display.
draw_text(display,name_config)
draw_text(display,pronouns_config)
display.update()

# run an event loop with glimmer, powermanagement, etc
main_loop(POWERMANAGEMENT,LED_GLIMMER)
