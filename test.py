from main import get_position_delta
from math import pi, sqrt


# create test cases
test_cases = []
test_cases.append(
    {
        'comment': 'stand still',
        'distance_left': 0,
        'distance_right': 0,
        'previous_angle': 0,
        'expected': {
            'x': 0,
            'y': 0,
            'angle': 0,
            'distance': 0,
        }
    }
)
test_cases.append(
    {
        'comment': 'go forward for 42',
        'distance_left': 42,
        'distance_right': 42,
        'previous_angle': 0,
        'expected': {
            'x': 0,
            'y': 42,
            'angle': 0,
            'distance': 42,
        }
    }
)
test_cases.append(
    {
        'comment': 'go backward for 17',
        'distance_left': -17,
        'distance_right': -17,
        'previous_angle': 0,
        'expected': {
            'x': 0,
            'y': -17,
            'angle': 0,
            'distance': 17,
        }
    }
)
test_cases.append(
    {
        'comment': '90 degree right turn, start facing north',
        'distance_left': 16 * pi,
        'distance_right': 10 * pi,
        'previous_angle': 0,
        'expected': {
            'x': 26,
            'y': 26,
            'angle': 0.5 * pi,
            'distance': 13 * pi,
        }
    }
)
test_cases.append(
    {
        'comment': '90 degree left turn, start facing north',
        'distance_left': 10 * pi,
        'distance_right': 16 * pi,
        'previous_angle': 0,
        'expected': {
            'x': -26,
            'y': 26,
            'angle': 1.5 * pi,
            'distance': 13 * pi,
        }
    }
)
test_cases.append(
    {
        'comment': '90 degree left turn, start facing east',
        'distance_left': 10 * pi,
        'distance_right': 16 * pi,
        'previous_angle': 0.5 * pi,
        'expected': {
            'x': 26,
            'y': 26,
            'angle': -0.5 * pi,
            'distance': 13 * pi,
        }
    }
)
test_cases.append(
    {
        'comment': '90 degree right turn, start facing south',
        'distance_left': 16 * pi,
        'distance_right': 10 * pi,
        'previous_angle': pi,
        'expected': {
            'x': -26,
            'y': -26,
            'angle': 0.5 * pi,
            'distance': 13 * pi,
        }
    }
)
test_cases.append(
    {
        'comment': 'U-Turn to the right',
        'distance_left': 32 * pi,
        'distance_right': 20 * pi,
        'previous_angle': 0,
        'expected': {
            'x': 26 * 2,
            'y': 0,
            'angle': pi,
            'distance': 26 * pi,
        }
    }
)
test_cases.append(
    {
        'comment': '45 degree right turn, start facing south',
        'distance_left': 8 * pi,
        'distance_right': 5 * pi,
        'previous_angle': pi,
        'expected': {
            'x': (sqrt(2) * 0.5 * (26)) - 26,
            'y': sqrt(2) * 0.5 * 26 * (-1),
            'angle': 0.25 * pi,
            'distance': 26 * 0.25 * pi,
        }
    }
)
test_cases.append(
    {
        'comment': 'U turn, start facing south',
        'distance_left': 32 * pi,
        'distance_right': 20 * pi,
        'previous_angle': pi,
        'expected': {
            'x': -52,
            'y': 0,
            'angle': pi,
            'distance': 26 * pi,
        }
    }
)
test_cases.append(
    {
        'comment': '90 degree right turn, start facing west',
        'distance_left': 16 * pi,
        'distance_right': 10 * pi,
        'previous_angle': 1.5 * pi,
        'expected': {
            'x': -26,
            'y': 26,
            'angle': 0.5 * pi,
            'distance': 13 * pi,
        }
    }
)
test_cases.append(
    {
        'comment': 'do a 180 (turn on current spot)',
        'distance_left': 6 * pi,
        'distance_right': -6 * pi,
        'previous_angle': 0,
        'expected': {
            'x': 0,
            'y': 0,
            'angle': pi,
            'distance': 0,
        }
    }
)
test_cases.append(
    {
        'comment': 'do a 360 (turn on current spot)',
        'distance_left': 12 * pi,
        'distance_right': -12 * pi,
        'previous_angle': 0,
        'expected': {
            'x': 0,
            'y': 0,
            'angle': 0,
            'distance': 0,
        }
    }
)
test_cases.append(
    {
        'comment': 'do a 270 degree turn to the right',
        'distance_left': 48 * pi,
        'distance_right': 30 * pi,
        'previous_angle': 0,
        'expected': {
            'x': 26,
            'y': -26,
            'angle': 1.5 * pi,
            'distance': 26 * pi * 1.5,
        }
    }
)
test_cases.append(
    {
        'comment': 'do a 270 degree turn to the left',
        'distance_left': 30 * pi,
        'distance_right': 48 * pi,
        'previous_angle': 0,
        'expected': {
            'x': -26,
            'y': -26,
            'angle': -1.5 * pi,
            'distance': 26 * pi * 1.5,
        }
    }
)
test_cases.append(
    {
        'comment': '360 + 180',
        'distance_left': 18 * pi,
        'distance_right': -18 * pi,
        'previous_angle': 0,
        'expected': {
            'x': 0,
            'y': 0,
            'angle': pi,
            'distance': 0,
        }
    }
)
test_cases.append(
    {
        'comment': '360 + 90',
        'distance_left': 15 * pi,
        'distance_right': -15 * pi,
        'previous_angle': 0,
        'expected': {
            'x': 0,
            'y': 0,
            'angle': 0.5 * pi,
            'distance': 0,
        }
    }
)
test_cases.append(
    {
        'comment': 'go forward for 5 facing west',
        'distance_left': 5,
        'distance_right': 5,
        'previous_angle': 1.5 * pi,
        'expected': {
            'x': -5,
            'y': 0,
            'angle': 0,
            'distance': 5,
        }
    }
)
test_cases.append(
    {
        'comment': '90 degree right turn reversed, start facing north',
        'distance_left': -16 * pi,
        'distance_right': -10 * pi,
        'previous_angle': 0,
        'expected': {
            'x': -26,
            'y': 26,
            'angle': 1.5 * pi,
            'distance': 13 * pi,
        }
    }
)

# get longest msg
longest_msg_len = None
for single_test_case in test_cases:
    if longest_msg_len is None:
        longest_msg_len = len(single_test_case['comment'])
    if len(single_test_case['comment']) > longest_msg_len:
        longest_msg_len = len(single_test_case['comment'])

# execute test cases
cnt = 0
for single_test_case in test_cases:
    cnt += 1
    delta_dict = get_position_delta(
        single_test_case['distance_left'],
        single_test_case['distance_right'],
        single_test_case['previous_angle'],
        wheel_distance=12
    )
    success_x = round(single_test_case['expected']['x']) == round(delta_dict['delta_x'])
    success_y = round(single_test_case['expected']['y']) == round(delta_dict['delta_y'])
    success_angle = round(single_test_case['expected']['angle'] % (pi * 2), 2) == round(delta_dict['delta_angle'] % (pi * 2), 2)
    success_distance = round(single_test_case['expected']['distance']) == round(delta_dict['delta_distance'])
    success_all = success_x and success_y and success_angle and success_distance

    if success_all:
        success_msg = 'success'
    else:
        success_msg = 'failure'

    spaces = ' ' * (longest_msg_len - len(single_test_case['comment']))

    print('[' + str(cnt).zfill(2) + '/' + str(len(test_cases)) + '] "' + single_test_case['comment'] + '":' + spaces + ' ' + success_msg)
    # test for return cases
    if not success_all:
        if success_x:
            print('  delta x:        success')
        else:
            print('  delta x:        failure')
            print('    expected: ' + str(single_test_case['expected']['x']))
            print('    returned: ' + str(delta_dict['delta_x']))
        if success_y:
            print('  delta Y:        success')
        else:
            print('  delta Y:        failure')
            print('    expected: ' + str(single_test_case['expected']['y']))
            print('    returned: ' + str(delta_dict['delta_y']))
        if success_angle:
            print('  delta angle:    success')
        else:
            print('  delta angle:    failure')
            print('    expected: ' + str(single_test_case['expected']['angle']))
            print('    returned: ' + str(delta_dict['delta_angle']))
        if success_distance:
            print('  delta distance: success')
        else:
            print('  delta distance: failure')
            print('    expected: ' + str(single_test_case['expected']['distance']))
            print('    returned: ' + str(delta_dict['delta_distance']))
