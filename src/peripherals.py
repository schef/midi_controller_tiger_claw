from common import *

select = []
data = []
buttons = []
on_button_change_cb = None


def init():
    global select, data, buttons
    for index in range(len(BUTTON_SELECT_LEFT)):
        select.append(SelectPair(BUTTON_SELECT_LEFT[index], BUTTON_SELECT_RIGHT[index]))
    for index in range(len(BUTTON_DATA_A)):
        data.append(DataPair(BUTTON_DATA_A[index], BUTTON_DATA_B[index]))

    for select_index in range(len(select)):
        for data_index in range(len(data)):
            buttons.append(Button(select_index, data_index))


def get_button_index(select_index, data_index, max_data):
    return select_index * max_data + data_index


def loop():
    global select, data, buttons
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
                        if on_button_change_cb is not None:
                            on_button_change_cb(select_index, data_index, True, 100)
                    else:
                        print("button_time[%d:%d] A=B : %d" % (select_index, data_index, 0))
                else:
                    if on_button_change_cb is not None:
                        on_button_change_cb(select_index, data_index, False, 0)
        select[select_index].set_state(False)


def register_on_button_change_cb(cb):
    global on_button_change_cb
    on_button_change_cb = cb


def test_loop():
    init()
    while True:
        loop()
