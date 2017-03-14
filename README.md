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
|	|---__init__.py
|   +---odometrium
|		|---__init__.py       
|		|---main.py
|		+---README.md
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
# debug=True makes that the current position is automatically explained
pos_info = Odometrium(left='A', right='B', wheel_diameter=5.5, wheel_distance=12, debug=True)

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

# also available as blocking, but quite useless then
# and your motors don't stop spinning!
pos_info.move(left=50, right=80, blocking=True)


# increase speed of the left wheel by 10 deg/s
# and decrease the speed of the right wheel by 20 deg/s
pos_info.change_speed(left=10, right=-20)

# decrease speed of the left wheel by 5 deg/s
pos_info.change_speed(left=-5)

# make the left wheel 10 faster than the right wheel
pos_info.speed_left = pos_info.speed_right + 10

# returns the current position as tuple
x, y = pos_info.get_current_pos()
# or query the parameters individually
x = pos_info.x
y = pos_info.y

# get the current orientation in degrees
# the returned value is ≥0 and <360
orientation = pos_info.orientation

# get the total driven distance
total_distance = pos_info.distance
```

# Percision
The values you have to provide to Odometrium are usually different from the values of the real robot.

You probably have to use a larger wheel distance for driving calculations and the odometry than your real bot has.

You will have to use a lot of debugging to find out the wheel distance and the wheel diameter of your robot.

# Maths
All movement is split in to individual segments. Within one segment, the speed of each motor is constant.
This way there are two types of movement.

The wheels width is assumed to be zero, the reference point for all movement is the middle between the wheels.

Each segment either describes a straight movement (both motors went at the same speed) or a curve (both motors went at different speeds). Depending on how the robot moved, different calculations are executed.

Default Units:

Physical Quantity | Unit
--- | ---
time | seconds
distance | centimeters
angle | radiant
motor speed | tacho counts per second (motor-specific)

Some sample segments:

Speed Left | Speed Right | Time (in s) | Comment
--- | --- | --- | ---
360 | 360 | 2 | Rush forward for 2s
-100 | -100 | 3 | Reverse carefully for 3s
0 | 180 | 4 | a left turn, taking 4s


## Given Data
### Constants
(The same for all movement segments.)

Var Name | Description | Default Value
--- | --- | ---
`wheel_diameter` | diameter of a single wheel | 5.5
`wheel_distance` | distance between (the center of) both wheels | 12
`count_per_rot` | amount of tacho counts per full rotation | 360
`pi` | pi, loaded from the python lib | 3.14....

### Vars
(Different for all the movement segments.)

Var Name | Description
--- | ---
`speed_left` | speed of the left wheel
`speed_right` | speed of the right wheel
`time` | duration of that segment
`previous_angle` | the angle before this segment
`previous_x` | the x coordinate before this segment
`previous_y` | the y coordinate before this segment
`previous_distance` | the total distances traveled before this segment

## General
### Constants
Var Name | Description
--- | ---
`circumference` | circumference of one wheel | `circumference = wheel_diameter * pi`

### Vars
Var Name | Description | Formula
--- | --- | ---
`tacho_counts_left` | amount of tacho counts the left motor rotated | `tacho_counts_left = speed_left * time`
`tacho_counts_right` | amount of tacho counts the right motor rotated | `tacho_counts_right = speed_right * time`
`rotations_left` | count of full rotations the left motor turned | `rotations_left = tacho_counts_left / count_per_rot`
`rotations_right` | count of full rotations the right motor turned | `rotations_right = tacho_counts_right / count_per_rot`
`distance_left` | distance traveled by the left wheel | `distance_left = rotations_left * circumference`
`distance_right` | distance traveled by the right wheel | `distance_right = rotations_right * circumference`

## Straight
Var Name | Description | Formula
--- | --- | ---
`delta_angle` | the angle change | `delta_angle = 0`
`delta_distance` | the distance traveled | `delta_distance = distance_left`
`delta_x` | the change between the previous and the current x coordinate | `delta_x = delta_distance * sin(previous_angle)`
`delta_y` | the change between the previous and the current y coordinate | `delta_y = delta_distance * cos(previous_angle)`

## Curve
All curves are approximated to circular movement.

Var Name | Description | Formula
--- | --- | ---
`angle` | the angle of the full circle the bot went. `2 * pi` for a full circle, `0.5 * pi` for a 90 degree turn. | `angle = (distance_right * (distance_left - distance_right)) / (distance_right * wheel_distance)`
`distance_delta` | the difference between the distances traveled by both wheels. always ≥0 | `distance_delta = abs(distance_right - distance_left)`
`radius_left` | the radius of the circle the left wheel follows | `radius_left = (distance_left * wheel_distance) / distance_delta`
`radius_right` | the radius of the circle the right wheel follows | `radius_right = (distance_right * wheel_distance) / distance_delta`
`radius` | the radius of the circle the reference point follows | `radius = (radius_left + radius_right) / 2`
`delta_angle` | the change between the previous and the current orientation | `delta_angle = angle`
`euclidean_distance` | euclidean distance (distance of a straight line) between the start and end point | `euclidean_distance = sqrt(2 * radius * radius * (1 - cos(angle)))`
`delta_x` | the change between the previous and the current x coordinate | `delta_x = euclidean_distance * sin((pi / 2) - (((pi - angle) / 2) - previous_angle))`
`delta_y` | the change between the previous and the current y coordinate | `delta_y = euclidean_distance * sin(((pi - angle) / 2) - previous_angle)`
`delta_distance` | the distance traveled | `delta_distance = radius * angle`

## Final Calculations
Var Name | Description | Formula
--- | --- | ---
`current_x` | the current x coordinate | `current_x = previous_x + delta_x`
`current_y` | the current y coordinate | `current_y = previous_y + delta_y`
`current_angle` | the current angle | `current_angle = previous_angle + delta_angle % 360`
`current_distance` | the total distance traveled | `current_distance = previous_distance + distance_delta`