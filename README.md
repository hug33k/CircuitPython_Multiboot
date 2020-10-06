# Multiboot for NeoTrellis M4 (CircuitPython)

This tool will let you store multiple programs on your NeoTrellis M4 (using CircuitPython).

## Setup

1. Download this repository
2. Copy `code.py` and `multiboot.py` on your board
3. Create a folder named `programs`
4. Create a subfolder inside `programs` for each program that you want to store

## Usage

Layout:
(Note: Multiboot is working on portrait mode (USB on left) for now)

````
PRG | PRG | PRG | PRG
---------------------
PRG | PRG | PRG | PRG
---------------------
PRG | PRG | PRG | PRG
---------------------
PRG | PRG | PRG | PRG
---------------------
PRG | PRG | PRG | PRG
---------------------
PRG | PRG | PRG | PRG
---------------------
    |     |     |
---------------------
PREV|ENTER|ENTER|NEXT
````

To select a program, press on its button.
To unselect it, press on its button again.
You can also select another program by pressing on its button.

To execute a program, press on `ENTER`.

If you have more than 24 programs, you can use `PREV` and `NEXT` to navigate over pages.

## Config

TODO

## Versions

v0.1
- Setup codebase

## Roadmap

- [ ] Support multiple orientations (Accelerometer?)
- [ ] Screen support should be optional
- [ ] Custom color for programs
- [ ] Custom order for programs
- [ ] requirements.txt

Feel free to create an issue/PR if there is a missing feature for you

## My setup

NeoTrellis M4
- CircuitPython 6.0.0-beta.2
- Screen soldered on JST port (SSD1306 128x32px)
- Mostly in portrait mode (USB on left, rotation at 270).

I don't have any other CircuitPython-compatible board so I won't be able to test properly support for another device.
