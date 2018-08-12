import sys
sys.path.append("..")
import logging
import random
import datetime
import time
from hx03w import hx03w
import pytz


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

    x = hx03w("AA:BB:CC:DD:EE:FF")  # Replace with your smartband mac address

    # Examples:
    # x.set_time(datetime.datetime(2017, 12, 31, 17, 45, 00, tzinfo=pytz.timezone("Europe/Amsterdam")), False)
    # x.set_time(datetime.datetime.now(pytz.timezone("Europe/Amsterdam")))

    while True:
        x.set_time(datetime.datetime(2017, random.randint(1, 12), random.randint(1, 31), random.randint(0, 23),
                                     random.randint(0, 59), random.randint(0, 59),
                                     tzinfo=pytz.timezone("Europe/Amsterdam")), True)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
