## we have a set of default includes, including color names etc
from includes import *

### Overridables
POWERMANAGEMENT = True

BACKGROUND_COLOR = BLACK

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
name_config.update(measure_text(display,name_config))
pronouns_config.update(measure_text(display,pronouns_config))
social_config.update(measure_text(display,social_config))

# position texts relative to each other
pronouns_config["y_pos"] = 0+(name_config["size"]*8)
social_config["y_pos"] = HEIGHT-(social_config["size"]*8)

print("entering animation loop")
import pngdec
display.set_backlight(BACKLIGHT_HIGH)
while not low_battery:
  mintime = 2.0
  maxtime = 0.0
  for i in range(60):
    framestart = time.time_ns()
    display.set_pen(BACKGROUND_COLOR)
    display.clear()
    png = pngdec.PNG(display)
    try:
      png.open_file('manekineko_pngs/frame_%02d_delay-0.1s.png' % i)
    except OSError:
      # file not found, last frame
      break
    png.decode(0,0,mode=pngdec.PNG_COPY)

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
    timetaken = (time.time_ns()-framestart)/1000000000
    if mintime > timetaken:
      mintime = timetaken
    if maxtime < timetaken:
      maxtime = timetaken
    time.sleep(0.3-timetaken)
  print("slowest render %fs, fastest render %fs" % (maxtime,mintime))

print("low power, reducing backlight to min")
display.set_backlight(BACKLIGHT_LOW)
