import logging
import datetime

try:
    import pygatt
except ImportError:
    raise ImportError("Install pygatt, it's requried. #pip3 install pygatt")

try:
    import pytz
except ImportError:
    raise ImportError("Install pytz, it's requried. #pip3 install pytz")


class hx03w:

    def __init__(self, mac_addr):
        self._adap = pygatt.GATTToolBackend()
        self._adap.start()
        while True:
            try:
                self._device = self._adap.connect(mac_addr, timeout=5, address_type=pygatt.BLEAddressType.random)
                self._device.subscribe('00000002-0000-1000-8000-00805f9b34fb', callback=self._ble_notifications_handler )
                logging.info("Connected")
                break
            except KeyboardInterrupt:
                break
            except pygatt.exceptions.NotConnectedError:
                logging.info("Waiting for connection...")

    def __del__(self):
        self._adap.stop()

    def _ble_notifications_handler(self, handle, value):
        try:
            v = value.decode().strip()
            logging.debug("decoded value={0}".format(value))
        except UnicodeDecodeError:
            logging.error("Cannot decode value as utf-8, Skip message")
            return

        if v == "NT+BEEP":
            self.handle_beep()

        elif v.startswith("AT+HEART:"):
            try:
                bpm = int(v.split(":")[1])
            except ValueError:
                bpm = None
            self.handle_hrm_read(bpm)

        elif v.startswith("AT+BATT:"):
            try:
                batt = int(v.split(":")[1])
            except ValueError:
                batt = None
            self.handle_battery_read(batt)

        elif v.startswith("AT+PACE:"):
            try:
                steps = int(v.split(":")[1])
            except (ValueError, IndexError):
                steps = None
            self.handle_pedometer_read(steps)

    def _send(self, cmd, chunk_len=20):
        cmd += "\r\n"
        for chunk in [cmd[i:i + chunk_len] for i in range(0, len(cmd), chunk_len)]:
            self._device.char_write('00000001-0000-1000-8000-00805f9b34fb', chunk.encode("utf-8"), True)

    def set_time(self, current_time=datetime.datetime.now(pytz.UTC), h12=False):
        try:
            tzs = current_time.utcoffset().total_seconds()
        except AttributeError:
            raise ValueError("Specify TimeZone, see pytz docs")

        # Set Current time as AT+DT=YYYYMMDDHHMMSS
        self._send(current_time.strftime("AT+DT=%Y%m%d%H%M%S"))

        # Set timezone offset (as Seconds) Ex: +02:00 is 7200 seconds
        self._send("AT+TIMEZONE={0}".format(int(tzs)))

        # Set 12h (0) or 24h (1)
        self._send("AT+TIMEFORMAT={0}".format(int(not h12)))

    def show_sync_logo(self, state=True):
        self._send("AT+SYN={0}".format(int(state)))

    def trigger_hrm(self):
        self._send("AT+HEART=1")

    def trigger_battery(self):
        self._send("AT+BATT")

    def trigger_pedometer(self):
        self._send("AT+PACE")

    # Handlers -> Override this methods to implement your own events

    def handle_beep(self):
        """
        called when FindMyPhone function is enabled
        :return:
        """
        logging.info("BEEP!")

    def handle_hrm_read(self, value):
        if value is None:
            logging.error("BPM: read failed.")
        else:
            logging.info("BPM:{0}".format(value))

    def handle_battery_read(self, value):
        if value is None:
            logging.error("BATT: read failed.")
        else:
            logging.info("BATT:{0}".format(value))

    def handle_pedometer_read(self, value):
        if value is None:
            logging.error("Steps: read failed.")
        else:
            logging.info("Steps:{0}".format(value))
