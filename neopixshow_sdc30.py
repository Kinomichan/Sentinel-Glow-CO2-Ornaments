import threading
import time
import sys

from neopixshow.effects import *

def main():
    neopixTasks = [
        hue_wheel_fill,
        rainbow_blink_gradually_bright,
        rainbow_blink,
        rgbw_sequence
    ]

    stop_event = threading.Event()
    current_thread = None

    print("=== Start NeoPixel Demo ===")
    print("Press Ctrl+C to exit.\n")

    try:
        while True:
            for neopix in neopixTasks:
                stop_event.clear()
    
                task_name = neopix.__name__
                print(f"--- Starting task: {task_name} ---")
                
                current_thread = threading.Thread(target=neopix, args=(stop_event,))
                current_thread.start()
    
                try:
                    time.sleep(3)
                except KeyboardInterrupt:
                    raise
    
                print(f"Stopping task: {task_name}...")
                stop_event.set()
                current_thread.join()
                print("Next task...\n")

    except KeyboardInterrupt:
        print("\n\n!!! Keyboard Interrupt Detected !!!")

    finally:
        if current_thread is not None and current_thread.is_alive():
            print("Cleaning up running thread...")
            stop_event.set()
            current_thread.join()
        
        print("=== Program Finished Safely ===")

if __name__ == '__main__':
    main()
