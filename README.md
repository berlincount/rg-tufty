# rg-tufty
Relationship Geeks Assembly Badge 38C3

License is MIT because is https://github.com/pimoroni/pimoroni-pico

Steps:

- Full: https://learn.pimoroni.com/article/getting-started-with-tufty-2040
- Minimal: install https://thonny.org/
- Download current Firmware Version with Vector support from https://github.com/pimoroni/pimoroni-pico/actions/runs/12372911360/artifacts/2331699103
- Connect badge via USB-C
- Turn badge on in Firmware Upgrade Mode by holding "boot" on the backside, then pressing PWR - badge shows up in Finder/Explorer as RPI-RP2
- Copy the .uf2 file from within the tufty2040-4cf9f44c55d3498dc46656eb9540b3008d25e0e0-pimoroni-micropython.uf2.zip downloaded above onto the badge
- Badge will automatically restart into Menu after upload is complete
- Start Thonny
- Select "MicroPython (RP2040)" with badge in lower right corner of Thonny
- Menu animatiion should stop, if not, try pressing the "Stop" button in the upper menu
- Select View->Files from the menu to see and edit files on the badge
- If you select file from the upper selector, you can upload from there; from the lower selector you can download

The following files can be uploaded directly, and will automatically show up in the menu:

(if you don't want the menu, rename and replace the main.py with the app you want to boot)

| Filename        | Purpose                                                  |
| --------------- | -------------------------------------------------------- |
| 38c3\_badge.py  | 38c3\_badge.png logo + badge text + backlight management |
| 38c3\_badge.png | 38c3 Badge logo                                          |
| badge.txt       | Simple example with name, pronouns, social               |
| button_test.py  | Button test with all buttons                             |
| main.py         | Alternate main.py using all buttons for start            |
| manekineko.py   | Waving cat with + badge text + backlight management      |
| name\_badge.py  | Simple name badge with backlight management              |
| pride\_badge.py | Pride badge with backlight management                    |
| rg\_badge.png   | Relationship Geeks logo background                       |
| rg\_badge.py    | rg\_badge.png logo + badge text + backlight management   |
