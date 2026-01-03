import time
import threading
import board
import busio
import adafruit_scd30

class scd30Monitor:
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
        self.scd = adafruit_scd30.SCD30(self.i2c)
        
        self.co2 = 0
        self.temperature = 0
        self.humidity = 0
        
        self._stop_event = threading.Event()
        self._thread = None

    def start(self):
        if self._thread is None or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()
            print("SCD30 Monitor Started")

    def stop(self):
        if self._thread and self._thread.is_alive():
            self._stop_event.set()
            self._thread.join()
            print("SCD30 Monitor Stopped")

    def _run(self):
        while not self._stop_event.is_set():
            try:
                if self.scd.data_available:
                    self.co2 = self.scd.CO2
                    self.temperature = self.scd.temperature
                    self.humidity = self.scd.relative_humidity
                time.sleep(1.0)
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(1)
