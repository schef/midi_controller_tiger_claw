import digitalio
from board import *
import time
import usb_midi

LED_PIN = GP25
BUTTON_SELECT_LEFT = [GP10, GP9, GP8, GP7, GP11]
BUTTON_SELECT_RIGHT = [GP21, GP22, GP26, GP27, GP20]
BUTTON_DATA_A = [GP12, GP14, GP16, GP17]  # L1, L2, R1, R2
BUTTON_DATA_B = [GP_13, GP_15, GP18, GP19]  # L1, L2, R1, R2


def get_millis():
    return int(time.monotonic_ns() / 1000 / 1000)


def millis_passed(timestamp):
    return get_millis() - timestamp


def create_output(pin):
    gpio_out = digitalio.DigitalInOut(pin)
    gpio_out.direction = digitalio.Direction.OUTPUT
    return gpio_out


def create_input(pin):
    gpio_in = digitalio.DigitalInOut(pin)
    gpio_in.direction = digitalio.Direction.INPUT
    gpio_in.pull = digitalio.Pull.DOWN
    return gpio_in


class Select():
    def __init__(self, pin):
        self.output = create_output(pin)
        self.output.value = False


class SelectPair():
    def __init__(self, pin_a, pin_b):
        self.a = Select(pin_a)
        self.b = Select(pin_b)

    def set_state(self, state):
        self.a.output.value = state
        self.b.output.value = state


class Data():
    def __init__(self, pin):
        self.input = create_input(pin)

    def get_state(self):
        return self.input.value


class DataPair():
    def __init__(self, pin_a, pin_b):
        self.a = Data(pin_a)
        self.b = Data(pin_b)


class Button():
    def __init__(self, select_index, data_index):
        self.select_index = select_index
        self.data_index = data_index
        self.state_a = -1
        self.state_b = -1
        self.timestamp_a = -1
        self.timestamp_b = -1


def get_button_index(select_index, data_index, max_data):
    return select_index * max_data + data_index


def test_peripherals():
    select = []
    data = []
    buttons = []
    for index in range(len(BUTTON_SELECT_LEFT)):
        select.append(SelectPair(BUTTON_SELECT_LEFT[index], BUTTON_SELECT_RIGHT[index]))
    for index in range(len(BUTTON_DATA_A)):
        data.append(DataPair(BUTTON_DATA_A[index], BUTTON_DATA_B[index]))

    for select_index in range(len(select)):
        for data_index in range(len(data)):
            buttons.append(Button(select_index, data_index))

    while True:
        for select_index in range(len(select)):
            select[select_index].set_state(True)
            for data_index in range(len(data)):
                button = buttons[get_button_index(select_index, data_index, len(data))]
                state_a = data[data_index].a.get_state()
                state_b = data[data_index].b.get_state()
                if state_a != button.state_a:
                    print("button_changed A[%d:%d] = %d" % (select_index, data_index, state_a))
                    button.state_a = state_a
                    button.timestamp_a = get_millis()
                if state_b != button.state_b:
                    print("button_changed B[%d:%d] = %d" % (select_index, data_index, state_b))
                    button.state_b = state_b
                    button.timestamp_b = get_millis()
                if button.state_a and button.state_b:
                    if button.timestamp_a > button.timestamp_b:
                        print("button_time[%d:%d] A>B : %d" % (select_index, data_index, button.timestamp_a - button.timestamp_b))
                    elif button.timestamp_b > button.timestamp_a:
                        print("button_time[%d:%d] A<B : %d" % (select_index, data_index, button.timestamp_b - button.timestamp_a))
                    else:
                        print("button_time[%d:%d] A=B : %d" % (select_index, data_index, 0))
            select[select_index].set_state(False)


def send_usb_midi_message(data):
    usb_midi.ports[1].write(bytearray(data))
