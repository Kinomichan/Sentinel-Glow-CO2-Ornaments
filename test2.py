import threading
import time

from neopixshow.effects import *

#hue_wheel_fill()
#rainbow_blink_gradually_bright,
#rainbow_blink,
#rgbw_sequence

stop_event = threading.Event()

t = threading.Thread(target=hue_wheel_fill, args=(stop_event,))
t.start()

print("starting task...")

try:
    time.sleep(5)
except KeyboardInterrupt:
    print("\nCtrl+C detected!")

finally:
    stop_event.set()

    t.join()
    print("Program finished.")
