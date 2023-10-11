from __future__ import print_function, unicode_literals

import signal
import sys
import time

from iphone_checker import IphoneChecker 

def signal_handler(signal, frame):
    print(" - Stop Monitoring")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

MONITOR_INTERVAL = 10

class StockMonitor:

    def __init__(self):
        """Initializer."""
        print("Apple Store Monitoring \n")
        self.stock_checker = IphoneChecker()

    def start_monitoring(self):
        """Start monitoring store's stock."""
        while True:
            self.stock_checker.refreshStock()
            time.sleep(MONITOR_INTERVAL)

if __name__ == "__main__":
    monitor = StockMonitor()
    monitor.start_monitoring()