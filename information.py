import functools
import logging
import time
import platform
import cv2
import re


def get_current_os():
    return platform.system()


def opencv_built_with_gstreamer():
    opencv_build_information = cv2.getBuildInformation()
    for current_line in opencv_build_information.splitlines():
        gstreamer_check = re.search('GStreamer', current_line)
        gstreamer_yes_check = re.search('YES', current_line)

        if gstreamer_check is not None and gstreamer_yes_check is not None:
            return True
    return False


def get_webcam_status():
    """
        Test the ports and returns a tuple with the available ports and the ones that are working.
        """
    non_working_ports = []
    working_ports = []
    available_ports = []

    dev_port = 0

    while len(non_working_ports) < 6:  # if there are more than 5 non working ports stop the testing.
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            non_working_ports.append(dev_port)
            # print("Port %s is not working." % dev_port)
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if is_reading:
                # print("Port %s is working and reads images (%s x %s)" % (dev_port, h, w))
                working_ports.append(dev_port)
            else:
                # print("Port %s for camera ( %s x %s) is present but does not reads." % (dev_port, h, w))
                available_ports.append(dev_port)
        dev_port += 1
    return available_ports, working_ports, non_working_ports


def processing_time_format_ms(input_time, decimal=3):
    micro_second = repr(input_time).split('.')
    output_time_str = '{}.{}'.format(micro_second[0], micro_second[1][:decimal])

    return output_time_str


def try_except(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if func.__qualname__:
                output_name = func.__qualname__
            else:
                output_name = func.__name__
            func(*args, **kwargs)
        except Exception as e:
            logging.exception(output_name)

    return wrapper


def class_function_self_only_time_stamp(func):
    @functools.wraps(func)
    def wrap(self):
        if func.__qualname__:
            output_name = func.__qualname__
        else:
            output_name = func.__name__

        start_time = time.time()
        start_time_string = time.asctime(time.localtime(start_time))
        print(f'[{output_name}] Start at {start_time_string}')

        func(self)
        end_time = time.time()
        end_time_string = time.asctime(time.localtime(end_time))
        print(f'[{output_name}] End at {end_time_string}')

        cost_time = end_time - start_time
        cost_time_string = processing_time_format_ms(cost_time)

        print(f'[{output_name}] Cost: {cost_time_string} sec')

    return wrap


def class_function_time_stamp(func):
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        if func.__qualname__:
            output_name = func.__qualname__
        else:
            output_name = func.__name__

        start_time = time.time()
        start_time_string = time.asctime(time.localtime(start_time))
        print('[{}] Start at {}'.format(output_name, start_time_string))

        func(self, *args, **kwargs)
        end_time = time.time()
        end_time_string = time.asctime(time.localtime(end_time))
        print('[{}] End at {}'.format(output_name, end_time_string))
        cost_time = end_time - start_time

        cost_time_string = processing_time_format_ms(cost_time)
        print('Time cost: {}'.format(cost_time_string))

    return wrap


def function_time_stamp(func):
    def wrap():
        if func.__qualname__:
            output_name = func.__qualname__
        else:
            output_name = func.__name__

        start_time = time.time()
        start_time_string = time.asctime(time.localtime(start_time))
        print('[{}] Start at {}'.format(output_name, start_time_string))
        func()
        end_time = time.time()
        end_time_string = time.asctime(time.localtime(end_time))
        print('[{}] End at {}'.format(output_name, end_time_string))
        cost_time = end_time - start_time

        cost_time_string = processing_time_format_ms(cost_time)
        print('Time cost: {}'.format(cost_time_string))

    return wrap


def print_time_stamp(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        if func.__qualname__:
            output_name = func.__qualname__
        else:
            output_name = func.__name__

        start_time = time.time()
        start_time_string = time.asctime(time.localtime(start_time))
        print()
        print('[{}] Start at {}'.format(output_name, start_time_string))
        result = func(*args, **kwargs)
        end_time = time.time()
        end_time_string = time.asctime(time.localtime(end_time))
        print('[{}] End at {}'.format(output_name, end_time_string))
        cost_time = end_time - start_time

        cost_time_string = processing_time_format_ms(cost_time)
        print('Time cost: {}'.format(cost_time_string))
        print()
        if result:
            return result

    return wrap


@function_time_stamp
def my_func():
    time.sleep(2)


if __name__ == '__main__':
    my_func()
