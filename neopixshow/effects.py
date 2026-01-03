import time, random, colorsys
import board
import neopixel

### 
def hue_wheel_fill(event=None):
    if event is None:
        print("Error: event object is required")
        return

    pixel_pin = board.D18
    num_pixels = 100
    ORDER = neopixel.RGB # RGB
    sleepTime = 0.1

    pixels = neopixel.NeoPixel(
        pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
    )

    try:
        rainbow = rainbowGenerator()
        while True:
            pixels.fill(next(rainbow))
            pixels.show()
            if event.wait(timeout=sleepTime):
                pixels.fill((0, 0, 0)) # turn off all LEDs
                pixels.show()
                return

    except:
        pixels.fill((0, 0, 0)) # turn off all LEDs
        pixels.show()


def rainbowGenerator():
    hue = 0.0
    step = 1/256

    while True:
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        rgbTuple = tuple(int(x * 255) for x in rgb)
        ##print(rgbTuple)
        yield rgbTuple

        hue = (hue + step) % 1.0


###
def hue_wheel_sequence(event=None):
    if event is None:
        print("Error: event object is required")
        return

    pixel_pin = board.D18
    num_pixels = 100
    ORDER = neopixel.RGB # RGB
    sleepTime = 0.01

    pixels = neopixel.NeoPixel(
        pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
    )

    try:
        rainbow = rainbowGenerator()
        while True:
            for i in range(100):
                pixels[i] = next(rainbow)
                pixels.show()
                if event.wait(timeout=sleepTime):
                    pixels.fill((0, 0, 0)) # turn off all LEDs
                    pixels.show()
                    return

    except:
        pixels.fill((0, 0, 0)) # turn off all LEDs
        pixels.show()


def rainbowGenerator():
    hue = 0.0
    step = 1/(256/8)

    while True:
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        rgbTuple = tuple(int(x * 255) for x in rgb)
        yield rgbTuple

        hue = (hue + step) % 1.0


### 
def rainbow_blink_gradually_bright(event=None):
    pixel_pin = board.D18
    num_pixels = 100
    ORDER = neopixel.RGB
    sleepTime = 0.01

    pixels = neopixel.NeoPixel(
        pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
    )

    colors = [ [255, 0, 0],   # red
               [255, 165, 0], # orange
               [255, 255, 0], # yellow
               [0, 128, 0],   # green
               [0, 255, 255], # cyan
               [0, 0, 255],   # blue
               [128, 0, 128] ]# purple

    step = 100

    try:
        while True:
            for i in range(len(colors)):
                for j in range(step):
                    r = int(colors[i][0]*(j+1)/step)
                    g = int(colors[i][1]*(j+1)/step)
                    b = int(colors[i][2]*(j+1)/step)
                    #print(r, g, b)

                    pixels.fill((r, g, b))
                    pixels.show()
                    if event.wait(timeout=sleepTime):
                        pixels.fill((0, 0, 0)) # turn off all LEDs
                        pixels.show()
                        return

    except:
        pixels.fill((0, 0, 0)) # turn off all LEDs
        pixels.show()


###
def rainbow_blink(event=None):
    pixel_pin = board.D18
    num_pixels = 100
    ORDER = neopixel.RGB
    sleepTime = 1

    pixels = neopixel.NeoPixel(
        pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
    )

    colors = [ [255, 0, 0],   # red
               [255, 165, 0], # orange
               [255, 255, 0], # yellow
               [0, 128, 0],   # green
               [0, 255, 255], # cyan
               [0, 0, 255],   # blue
               [128, 0, 128] ]# purple

    try:
        while True:
            for i in range(len(colors)):
                rgb = (colors[i][0], colors[i][1], colors[i][2])
                pixels.fill(rgb)

                pixels.show()

                if event.wait(timeout=sleepTime):
                    pixels.fill((0, 0, 0)) # turn off all LEDs
                    pixels.show()
                    return

    except:
        pixels.fill((0, 0, 0)) # turn off all LEDs
        pixels.show()


### 
def rgbw_sequence(event=None):
    pixelPin = board.D18
    numPixels = 100
    ORDER = neopixel.RGB
    sleepTime = 1

    pixels = neopixel.NeoPixel(
        pixelPin, numPixels, brightness=0.2, auto_write=False, pixel_order=ORDER
    )

    colors = [ [255, 0, 0],      # red
               [0, 255, 0],      # green
               [0, 0, 255],      # blue 
               [255, 255, 255] ] # white

    try:
        turnOnLed(pixels, numPixels, sleepTime, colors, event)

    except:
        pixels.fill((0, 0, 0)) # turn off all LEDs
        pixels.show()


def turnOnLed(pixels, numPixels, sleepTime, colors, event):
    startPos = 0

    while True:
        for i in range(numPixels):
            pos = (startPos + i)%numPixels

            colorNum = pos%len(colors)
            rgb = (colors[colorNum][0], colors[colorNum][1], colors[colorNum][2])
            pixels[i] = rgb

        pixels.show()

        if event.wait(timeout=sleepTime):
            pixels.fill((0, 0, 0)) # turn off all LEDs
            pixels.show()
            return

        if startPos < numPixels - 1:
            startPos += 1
        else:
            startPos = 0


###
def blink_red(sleepTime, event=None):
    pixelPin = board.D18
    numPixels = 100
    ORDER = neopixel.RGB

    pixels = neopixel.NeoPixel(
        pixelPin, numPixels, brightness=0.2, auto_write=False, pixel_order=ORDER
    )

    try:
        while True:
            pixels.fill((255, 0, 0))
            pixels.show()
            time.sleep(sleepTime)
            pixels.fill((255, 255, 255))
            pixels.show()
            time.sleep(sleepTime)

    except:
        pixels.fill((0, 0, 0)) # turn off all LEDs
        pixels.show()


###
def turn_off_led():
    pixel_pin = board.D18
    num_pixels = 100
    ORDER = neopixel.RGB # RGB

    pixels = neopixel.NeoPixel(
        pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
    )

    pixels.fill((0, 0, 0)) # turn off all LEDs
    pixels.show()
