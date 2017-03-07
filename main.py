import ev3dev.ev3 as ev3


class Odometrium:
    def __init__(self, left=None, right=None, wheel_diameter=5.5):
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
        self.stop()

    def stop(self):
        self.__motor_left.stop()
        self.__motor_right.stop()

    def wait(self):
        self.__motor_left.wait_while('running')
        self.__motor_right.wait_while('running')

    def move(self, right=0, left=0, time=None, blocking=None):
        # if time is set: make function blocking
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
