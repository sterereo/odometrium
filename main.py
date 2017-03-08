import ev3dev.ev3 as ev3
import time.perf_counter


class Odometrium:
    def __init__(self, left=None, right=None, wheel_diameter=5.5, wheel_distance=12):
        allowed_ports = ['A', 'B', 'C', 'D']
        if left not in allowed_ports or right not in allowed_ports:
            if left not in allowed_ports:
                error_location = 'left'
            if right not in allowed_ports:
                if left not in allowed_ports:
                    error_location = 'left and right'
                error_location = 'right'
            raise RuntimeError('The ' + error_location + ' motor port given is none of the allowed ports: ' + ', '.join(allowed_ports))

        self.__wheel_diameter = wheel_diameter
        # init motor wheel
        self.__motor_left = ev3.LargeMotor('out' + left)
        self.__motor_right = ev3.LargeMotor('out' + right)
        self.__movement_logs = []
        self.__last_log_time = time.perf_counter()
        self.stop()

    def __add_log(self):
        # generate current log
        current_time = time.perf_counter()
        elapsed_time = current_time - self.__last_log_time
        new_log = {
            'speed_left': self.speed_left,
            'speed_right': self.speed_right,
            'time': elapsed_time,
        }
        # only record log if there is movement at all
        if 0 != self.speed_left or 0 != self.speed_right:
            self.__movement_logs.append(new_log)
        # set reference point for the next log
        self.__last_log_time = time.perf_counter()

    def stop(self):
        self.__add_log()
        self.__motor_left.stop()
        self.__motor_right.stop()

    def wait(self):
        self.__motor_left.wait_while('running')
        self.__motor_right.wait_while('running')

    def move(self, right=0, left=0, time=None, blocking=None):
        self.stop()
        if time is not None:
            self.__motor_left.run_timed(time_sp=time * 1000, speed_sp=left)
            self.__motor_right.run_timed(time_sp=time * 1000, speed_sp=right)
            # time given: blocking by default
            # => block when blocking=None (default) or blocking=True
            if blocking is None or blocking:
                self.wait()
        else:
            # no time is set => run indefinitely
            self.__motor_left.run_forever(speed_sp=left)
            self.__motor_right.run_forever(speed_sp=right)
            # no time given: non-blocking by default
            # => only block when blocking=True is given
            if blocking:
                self.wait()

    def change_speed(self, left=0, right=0):
        self.__add_log()
        self.__motor_left.run_forever(speed_sp=self.speed_left + left)
        self.__motor_right.run_forever(speed_sp=self.speed_right + right)

    @property
    def speed_left(self):
        return self.__motor_left.speed

    @speed_left.setter
    def speed_left(self, new_speed):
        self.change_speed(left=new_speed)

    @property
    def speed_right(self):
        return self.__motor_right.speed

    @speed_right.setter
    def speed_right(self, new_speed):
        self.change_speed(right=new_speed)

    def __exit__(self):
        self.stop()

    def __del__(self):
        for single_log in self.__movement_logs:
            log_line = ''
            log_line += 'Left:  ' + str(single_log['speed_left']) + '; '
            log_line += 'Right: ' + str(single_log['speed_right']) + '; '
            log_line += 'Time:  ' + str(single_log['time'])
            print(log_line)
