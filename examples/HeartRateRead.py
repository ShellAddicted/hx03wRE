import sys
sys.path.append("..")
import logging
import time
from hx03w import hx03w


class MyBand(hx03w):
    def handle_hrm_read(self, value):
        if value is None:
            print("Error")
            return
        print("{0} BPM".format(value))


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

    x = MyBand("AA:BB:CC:DD:EE:FF")  # Replace with your smartband mac address

    while True:
        x.trigger_hrm()
        time.sleep(0.5)


if __name__ == '__main__':
    main()
