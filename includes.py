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

def measure_text(display,config):
  if not "font" in config:
    display.set_font("bitmap8")

  cur_size = config["max_size"]
  while True:
    cur_width = display.measure_text(config["text"], cur_size)
    if cur_width >= WIDTH/2:
      cur_size -= 1
    else:
      break

  return cur_size

def draw_text(display,config):
  print(config)
  if not "font" in config:
    display.set_font("bitmap8")
  display.set_pen(config["color"])
  display.text(config["text"], int(config["x_pos"]), int(config["y_pos"]), int(WIDTH), int(config["size"]))

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

  # Try reading the social
  try:
    social = file.readline().strip()
  except:
    social = ""

  file.close()

  return name, pronouns, social
