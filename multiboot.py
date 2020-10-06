import board
import busio
import displayio
import terminalio
import supervisor
import adafruit_displayio_ssd1306
from adafruit_display_text import label
import adafruit_trellism4
import os


_version = "0.1"


class Multiboot:

    def __init__(self):
        self._trellis = adafruit_trellism4.TrellisM4Express(270)
        displayio.release_displays()
        self._i2c = busio.I2C(board.SCL, board.SDA)
        self._display = displayio.I2CDisplay(self._i2c, device_address=0x3c)
        self._screen = adafruit_displayio_ssd1306.SSD1306(self._display, width=128, height=32)
        self._programs = []
        self._page = 0
        self._selected = None
        # Settings
        self._per_page = 24
        self._button_previous = [(0, 7)]
        self._button_select = [(1, 7), (2, 7)]
        self._button_next = [(3, 7)]

    def _show(self, title="MULTIBOOT", text="", note=""):
        splash = displayio.Group(max_size=10)
        if title and len(title):
            lbl_title = label.Label(terminalio.FONT, text=title, color=0xFFFF00, x=0, y=3)
            splash.append(lbl_title)
        if text and len(text):
            lbl_text = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=0, y=20)
            splash.append(lbl_text)
        if note and len(note):
            lbl_note = label.Label(terminalio.FONT, text=note, color=0xFFFF00, x=85, y=3)
            splash.append(lbl_note)
        self._screen.show(splash)

    def _clear(self):
        for col in range(4):
            for row in range(8):
                self._trellis.pixels[(col, row)] = (0, 0, 0)
        self._show("", "", "")

    def _load_programs(self):
        self._programs = os.listdir("./programs")

    def _show_controls(self, has_previous, has_next):
        # Previous
        if has_previous:
            for key in self._button_previous:
                self._trellis.pixels[key] = (0, 50, 50)
        # Launch
        for key in self._button_select:
            self._trellis.pixels[key] = (0, 50, 0)
        # Next
        if has_next:
            for key in self._button_next:
                self._trellis.pixels[key] = (0, 50, 50)

    def _get_programs_for_page(self, page=None):
        if not page:
            page = self._page
        first_index = page * self._per_page
        if first_index > len(self._programs):
            return []
        return self._programs[first_index:first_index+self._per_page]

    def _show_programs(self):
        programs = self._get_programs_for_page()
        for index in range(len(programs)):
            col = index % 4
            row = int(index / 4)
            self._trellis.pixels[(col, row)] = (60 - (col * 20), col * 10, row * 15)
        return self._page, bool(self._page > 0), bool(((self._page + 1) * self._per_page) < len(self._programs))

    def _get_program(self, index):
        return self._programs[index]

    def _print_program(self, key):
        program_index = (self._page * self._per_page) + key[0] + (key[1] * 4)
        if self._selected is None or self._selected is not program_index:
            self._selected = program_index
            self._show("MULTIBOOT", self._get_program(program_index), str(program_index))
            return False
        else:
            self._selected = None
            return True

    def _execute(self, key, has_previous, has_next):
        if key in self._button_previous and has_previous:
            self._page -= 1
            return True
        elif key in self._button_next and has_next:
            self._page += 1
            return True
        elif key in self._button_select and self._selected is not None:
            program = self._get_program(self._selected)
            self._clear()
            self._show("MULTIBOOT", program, "Boot...")
            os.chdir("/programs/" + program)
            exec('import code')
            supervisor.reload()
        elif key[1] < 6:
            return self._print_program(key)
        return False

    def run(self):
        self._show("MULTIBOOT", "Loading...", _version)
        self._load_programs()
        current_press = set()
        updated = True
        while True:
            if updated:
                self._clear()
                page, has_previous, has_next = self._show_programs()
                self._show_controls(has_previous, has_next)
                self._show("MULTIBOOT", "Select a program", "Page " + str(self._page + 1))
                updated = False
            pressed = set(self._trellis.pressed_keys)
            for key in pressed - current_press:
                updated = self._execute(key, has_previous, has_next)
            current_press = pressed

def run():
    Multiboot().run()
