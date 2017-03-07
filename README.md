# Odometrium
Odometrium is a class that implements odometry using the ev3dev language bindings for LEGO Mindstorm roboters.

Instead of controlling the motors directly via the ev3dev commands, you instead use the Odometrium class.  
While driving around, the class automatically keeps track of your position and orientation.

# Usage

If your folder structure is
```
main
|---include
|   +---odometrium
|       +---main.py
+---run.py
```

Your `run.py` should contain:
```python
import ev3dev.ev3 as ev3
from include.odometrium.main import Odometrium
from time import sleep

# the left wheel is connected to port A
# the right wheel is connected to port B
# the wheel diameter is 5.5 cm (default lego wheel diameter)
pos_info = Odometrium(left='A', right='B', wheel_diameter='5.5')

# drive for 3 seconds with both wheels at the speed of 50 deg/second
# when time is used, the command is by default blocking:
pos_info.move(left=50, right=50, time=3)
print('Done moving.')

# the command can be made non-blocking by using the parameter:
pos_info.move(left=50, right=50, time=3, blocking=False)
print('Movement started...')
# now wait until the motors stopped
pos_info.wait()
print('Movement stopped.')

# start driving with the left wheel at 50 deg/s and the right wheel at 80 deg/s
pos_info.move(left=50, right=80)
# wait for 3 seconds...
sleep(3)
# ... and stop both motors
pos_info.stop()


# increase speed of the left wheel by 10 deg/s
# and decrease the speed of the right wheel by 20 deg/s
pos_info.change_speed(left=10, right=-20)

# decrease speed of the left wheel by 5 deg/s
pos_info.change_speed(left=-5)

# speed of the left & right wheel
pos_info.speed_left
pos_info.speed_right

# returns the current position as tuple
x, y = pos_info.get_current_pos()
# or query the parameters individually
x = pos_info.x
y = pos_info.y

# get the current orientation in degrees
# the returned value is ≥0 and <360
orientation = pos_info.orientation
# or as a method
orientation = pos_info.get_orientation()
```