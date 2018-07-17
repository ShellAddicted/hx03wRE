
This project provides a Python API compatible Bluetooth low energy (BLE) smartbands.  
it's specifically designed to work with Lenovo HX06W but should work with other similiar smartbands.

Supported Features:  
- [X] HRM  
- [X] Clock Settings  
- [X] Battery Status  
- [X] Pedometer

Missing Features:
- [ ] Anti-sleep function  
- [ ] instant messaging Notifications  
- [ ] Alarm Settings  
- [ ] Vibration Settings  

I will add more features as soon I discover how they works (reverse engineering)

# Getting Started

## Clock Settings
`set_time()` permits to adjust date and time using a `datetime.datetime` object. (timezone is required)


## Handlers:

Override handlers of `hx03w` class to implement your own events

- `handle_beep()`
called when 'FindMyPhone' function is activated from smartband.
the master device (e.g: smartphone) should vibrate or emit sound making itself easier to find.

- `handle_hrm_read(self,value)`  
use `trigger_hrm()` to perform an HRM read, and expect a response inside this handler.

- `handle_battery_read(self,value)`  
use `trigger_battery()` to get the battery charge state, and expect a response inside this handler.

- `handle_pedometer_read(self,value)`  
use `trigger_pedometer()` to get the battery charge state, and expect a response inside this handler.


see [examples/](https://github.com/ShellAddicted/hx03wRE/tree/master/examples) for more details