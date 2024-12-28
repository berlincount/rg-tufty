# If you have a Display Pack 2.0" or 2.8" use DISPLAY_PICO_DISPLAY_2 instead of DISPLAY_PICO_DISPLAY

from includes import *
import qrcode

#display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, rotate=0)
display.set_backlight(1.0)

WIDTH, HEIGHT = display.get_bounds()


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

FG = DARK_AUBERGINE_38C3
BG = CORAL_RED_38C3


def measure_qr_code(size, code):
    w, h = code.get_size()
    module_size = int(size / w)
    return module_size * w, module_size


def draw_qr_code(ox, oy, size, code):
    size, module_size = measure_qr_code(size, code)
    display.set_pen(FG)
    display.rectangle(ox, oy, size, size)
    display.set_pen(BG)
    for x in range(size):
        for y in range(size):
            if code.get_module(x, y):
                display.rectangle(ox + x * module_size, oy + y * module_size, module_size, module_size)


code = qrcode.QRCode()
code.set_text("https://signal.group/#CjQKIMGDvwWArEiCYitSUc14rYzceB5xQpwcNoAbhSj84RT0EhBQWoqUFepq__ZB9nrTS6g4")

display.set_pen(FG)
display.clear()
display.set_pen(BG)

max_size = min(WIDTH, HEIGHT)

size, module_size = measure_qr_code(max_size, code)
left = int((WIDTH // 2) - (size // 2))
top = int((HEIGHT // 2) - (size // 2))
draw_qr_code(left, top, max_size, code)

display.update()

while True:
    pass
