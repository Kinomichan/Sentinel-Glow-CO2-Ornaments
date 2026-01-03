#!/usr/bin/env python3

import threading
import time
import sys

from neopixshow.effects import *
from scd30.scd30_monitor import scd30Monitor

# CO2 Threshold levels (ppm)
TH_WARN = 1000
TH_HIGH = 2500
TH_CRITICAL = 5000

EFFECT_DURATION = 10
CHECK_INTERVAL = 1

def run_effect(effect_func, stop_event, args=(), **kwargs):
    task_kwargs = {'event': stop_event}
    task_kwargs.update(kwargs)

    t = threading.Thread(target=effect_func, args=args, kwargs=task_kwargs)
    t.start()
    return t


def get_alert_speed(co2_value):
    if co2_value >= TH_CRITICAL:
        return 0.1
    elif co2_value >= TH_HIGH:
        return 0.5
    elif co2_value >= TH_WARN:
        return 1.0
    else:
        return None # No alert


def main():
    neopixTasks = [
        hue_wheel_fill,
        rainbow_blink_gradually_bright,
        rainbow_blink,
        rgbw_sequence
    ]

    sensor = scd30Monitor()
    sensor.start()
    
    # Wait for sensor to stabilize
    time.sleep(2)

    stop_event = threading.Event()
    current_thread = None
    task_index = 0

    print("=== Start Sentinel-Glow CO2 Ornaments ===")
    print(f"Thresholds -> Warn: {TH_WARN}, High: {TH_HIGH}, Critical: {TH_CRITICAL} ppm")
    print("Press Ctrl+C to exit.\n")

    try:
        while True:
            current_co2 = sensor.co2
            current_temp = sensor.temperature
            
            print(f"Status -> CO2: {current_co2:.0f}ppm, Temp: {current_temp:.1f}C")

            # --- 1. Warning Mode (CO2 >= 1000) ---
            if current_co2 >= TH_WARN:
                print(f"!!! ALERT MODE: CO2 is {current_co2:.0f}ppm !!!")
                
                # Determine initial blink speed
                current_speed = get_alert_speed(current_co2)
                
                stop_event.clear()
                # Start blink_red with the determined speed
                current_thread = run_effect(blink_red, stop_event, sleepTime=current_speed)
                print(f"   -> Alert Level Started. Blink speed: {current_speed}s")

                # Keep looping as long as CO2 is above the warning threshold
                try:
                    while sensor.co2 >= TH_WARN:
                        new_co2 = sensor.co2
                        new_temp = sensor.temperature

                        new_speed = get_alert_speed(new_co2)
                        
                        if new_speed != current_speed:
                            print(f"   -> Level Changed! CO2: {new_co2:.0f}ppm. Adjusting speed to {new_speed}s")
                            
                            # Stop current thread
                            stop_event.set()
                            current_thread.join()
                            
                            # Start new thread with new speed
                            stop_event.clear()
                            current_thread = run_effect(blink_red, stop_event, args=(new_speed,))
                            current_speed = new_speed
                        
                        print(f"Status -> CO2: {new_co2:.0f}ppm, Temp: {new_temp:.1f}C")
                        time.sleep(CHECK_INTERVAL)

                finally:
                    # Clean up before returning to normal mode
                    stop_event.set()
                    current_thread.join()
                    print("--- Alert Cleared. Returning to Normal Mode ---")

            # --- 2. Normal Mode (Effect Rotation) ---
            else:
                task_func = neopixTasks[task_index]
                task_name = task_func.__name__
                
                print(f"--- Normal Mode: Playing {task_name} ---")
                
                stop_event.clear()
                current_thread = run_effect(task_func, stop_event)

                start_time = time.time()
                interrupted = False
                
                try:
                    # Run effect for EFFECT_DURATION, but check CO2 frequently
                    while (time.time() - start_time) < EFFECT_DURATION:
                        if sensor.co2 >= TH_WARN:
                            print("Interrupting normal effect for CO2 Alert!")
                            interrupted = True
                            break
                        time.sleep(CHECK_INTERVAL)

                finally:
                    stop_event.set()
                    current_thread.join()

                # Move to next task only if finished successfully
                if not interrupted:
                    task_index = (task_index + 1) % len(neopixTasks)

    except KeyboardInterrupt:
        print("\n\n!!! Keyboard Interrupt Detected !!!")

    finally:
        print("Cleaning up...")
        stop_event.set()
        if current_thread is not None and current_thread.is_alive():
            current_thread.join()
        
        print("=== Sentinel-Glow CO2 Ornaments Finished Safely ===")

if __name__ == '__main__':
    main()
