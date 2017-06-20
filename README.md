# Odometrium
Odometrium is a class that implements odometry using the ev3dev language bindings for LEGO Mindstorm roboters.

Instead of controlling the motors directly via the ev3dev commands, you instead use the Odometrium class.  
While driving around, the class automatically keeps track of your position and orientation.

# Odometry?
Odometry is a method to calculate the current position and orientation of your robot in a room just by knowing how your robot moved.

# What Is Odometrium Then?
Odometrium is a python class using the ev3dev library for the LEGO Mindstorm EV3.

# How Does It Work?
All the motor controlls are done using the Odometrium python class. While you control the motors, Odometrium automatically keeps track when and how your robot moved. From this long log of all movement the current position and orientation can be calculated at any time. (For mathematical details see below.)

# How Do I Use It?
Suppose your folder structure is:
```
src
|---include
|   |---__init__.py
|   +---odometrium
|       |---__init__.py
|       |---main.py
|       |---README.md
|       +---test.py
+---run.py
```

Your `run.py` should contain:
```python
import ev3dev.ev3 as ev3
from include.odometrium.main import Odometrium
from time import sleep

# left='B'                  the left wheel is connected to port B
# right='C'                 the right wheel is connected to port C
# wheel_diameter=5.5        the wheel diameter is 5.5cm
# wheel_distance=12         the wheel distance is 12cm
# unit sidenote: as long as you are consistent, you can also use mm, inches, km.
# returned values are in these units
# counts per rotation are is the number of motor-internal 'tacho-counts'
# that the motor has to travel for one full revolution
# this is motor specific
#
# count_per_rot_left=None   use the default value returned by the motor for the left motor
# count_per_rot_right=360   for the right motor treat 360 tacho counts as one full revolution
# debug=False               print the current position (on motor speed change) and
#                           echo all the movement logs when the object is destroyed
# curve_adjustment=0.873    use curve adjustment factor of 0.873, see below ('percision')  
pos_info = Odometrium(left='B', right='C', wheel_diameter=5.5, wheel_distance=12,
                      count_per_rot_left=None, count_per_rot_right=360, debug=False,
                      curve_adjustment=1)

# drive for 3 seconds with both wheels at the speed of 50 (internal motor speed)
# when time is used, the command is by default blocking:
pos_info.move(left=50, right=50, time=3)
print('Done moving.')

# the command can be made non-blocking by using the parameter 'blocking':
pos_info.move(left=50, right=50, time=3, blocking=False)
print('Movement started...')
# now wait until the motors stopped
pos_info.wait()
print('Movement stopped.')

# start driving with the left wheel at 50 and the right wheel at 80
pos_info.move(left=50, right=80)
# wait for 3 seconds...
sleep(3)
# ... and stop both motors
pos_info.stop()

# also available as blocking, but quite useless then
# and your motors don't stop spinning!
pos_info.move(left=50, right=80, blocking=True)

# increase speed of the left wheel by 10
# and decrease the speed of the right wheel by 20
pos_info.change_speed(left=10, right=-20)

# decrease speed of the left wheel by 5
pos_info.change_speed(left=-5)

# make the left wheel 10 faster than the right wheel
pos_info.speed_left = pos_info.speed_right + 10

# and stop the right motor completly
pos_info.speed_right = 0

# query the current position
x = pos_info.x
y = pos_info.y

# get the current orientation in degrees
# the returned value is ≥0 and <2 * pi
# the start value is 0 degrees by default
# one quarter to the right e.g. return 0.5 * pi
orientation = pos_info.orientation

# get the total driven distance
total_distance = pos_info.distance

# recalibrate the position to be 17, 42
pos_info.x = 17
pos_info.y = 42

# and also the current orientation to be the same way as the starting position (0)
pos_info.orientation = 0
```

# Orientation
A short table to convert the orientation

orientation | angle in degrees | relative to axis | direction
--- | --- | --- | ---
`0` | `0°` | facing towards `y=+∞` | north
`0.5 * pi` | `90°` | facing towards `x=+∞` | east
`1.0 * pi` | `180°` | facing towards `y=-∞` | south
`1.5 * pi` | `270°` | facing towards `x=-∞` | west

# Percision
It is highly recommended to re-calibrate your position during the run. On the tested robot, the measured distances driven by the wheels in curve where too long compared to the actually driven distance. Somehow this does not occur while driving straight.

The workaround in place simply shortens the distance that is used for the calculations in curves. This behaviour is disabled during the tests, as it is not required mathematically.

To set the factor that is used to shorten the curve can be specified in the constructor. Its default value is 1 (no curve adjustment).

# Testing
To execute the given tests use:
```bash
python3 test.py
```
The ev3dev language bindings have to be installed.

# Maths
All movement is split in to individual segments. Within one segment, the speed of each motor is constant.
This way there are only two general types of movement to calculate.

Each segment either describes a straight movement (both motors went at the same speed) or a curve (both motors went at different speeds). Depending on whetĥer the movement is a curve or a straight line, different calculations are executed.

The wheels width is assumed to be zero, the reference point for all movement is the center between the wheels.

The logging is based on the internal rotation counter of the motors, each segments records the change of these two values. The duration of the recorded segment is completly ignored, as only the driven distances are important (and the fact that they are driven during the same time using constant speeds).

Default Units:

Physical Quantity | Unit
--- | ---
time | seconds
distance | centimeters (or as given in constructor)
angle | radiant
motor speed | tacho counts per second (motor-specific)

Some sample segments:

Delta Ticks Left | Delta Ticks Right | Comment
--- | --- | ---
360 | 360 | Straight movement forward
-180 | -180 | Reverse backwards for half the distance
0 | 180 | a left turn

The calculations are performed in two steps:

1. convert motor ticks to driven distances
2. calculate position differences

# Driven Distance
## Consts
Var Name | Description | Example Value
--- | --- | ---
`wheel_diameter` | the wheel diameter | 5.5 (cm)
`wheel_distance` | the wheel distance from each other | 9.9 (cm) 
`count_per_rot_left` | tacho counts per full revolution for the left wheel | 360
`count_per_rot_right` | tacho counts per full revolution for the right wheel | 359

## Vars
Var Name | Description
--- | ---
`delta_position_left` | tacho counts moved by the left motor
`delta_position_right` | tacho counts moved by the right motor

## Calculations
Var Name | Description | Formula
--- | --- | ---
`circumference` | wheel circumference | `wheel_diameter * pi`
`rotations_left` | full revolutions by the left wheel | `tacho_counts_left / count_per_rot_left`
`rotations_right` | full revolutions by the right wheel | `tacho_counts_right / count_per_rot_right`
`distance_left` | distance driven by the left wheel | `rotations_left * circumference`
`distance_right` | distance driven by the right wheel | `rotations_right * circumference`

# Position differences
## Consts
Var Name | Description | Example Value
--- | --- | ---
`wheel_distance` | the wheel distance from each other | 9.9 (cm)

## Vars
Var Name | Description
--- | ---
`distance_left` | distance driven by the left wheel
`distance_right` | distance driven by the right wheel
`previous_angle` | the orientation of the robot before the segment
`factor` | factor for curve movement (see 'percision'). is either `1.0` or `0.877`

## Calculations - Straight Movement
Var Name | Description | Formula
--- | --- | ---
`delta_angle` | the difference to the new angle | `0`
`delta_distance` | the driven distance | `abs(distance_left)`
`delta_x` | the difference to the new x value | `distance_left * sin(previous_angle)`
`delta_y` | the difference to the new y value | `distance_left * cos(previous_angle)`

## Calculations - Curve
The curve movement is calculated as circular movement.

Var Name | Description | Formula
--- | --- | ---
`relation` | the relation between the movement of the left and right wheel | `distance_left / distance_right`, 0 if `distance_right` is 0
`distance_difference` | difference between the driven distance | `(distance_left * factor) - (distance_right * factor)`
`radius_left` | radius of the circle the left wheel follows | `((distance_left * factor) * wheel_distance) / distance_difference`
`radius_right` | radius of the circle the right wheel follows | `((distance_right * factor) * wheel_distance) / distance_difference`
`angle` | angle of the circle followed | `(distance_left * factor) / radius_left`, on ZeroDivisionError `(distance_right * factor) / radius_right`
`radius` | the radius of the circle the center between both wheels follows | `(radius_left + radius_right) / 2`
`delta_angle` | the difference between the starting and final orientation | `angle`
`euclidean_distance` | distance of a straight line between the starting and end point | `sqrt(2 * radius * radius * (1 - cos(angle)))`
`angle_lambda` | the angle between the x-axis and the straight line between the starting and end point | `((pi - angle) / 2) - previous_angle`
`delta_x` | difference between starting and final x value | `euclidean_distance * cos(angle_lambda)`
`delta_y` | difference between starting and final x value | `euclidean_distance * sin(angle_lambda)`
`delta_distance` | driven distance | `abs(radius * angle)`
