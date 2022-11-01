import peripherals
import midi_player
import common

CHANNEL = 1


def get_button_midi_num(select_index, data_index):
    if select_index == 0 and data_index == 1:
        return 45
    elif select_index == 1 and data_index == 1:
        return 44
    elif select_index == 2 and data_index == 1:
        return 43
    elif select_index == 3 and data_index == 1:
        return 42
    elif select_index == 4 and data_index == 0:
        return 41
    elif select_index == 0 and data_index == 2:
        return 36
    elif select_index == 1 and data_index == 2:
        return 37
    elif select_index == 2 and data_index == 2:
        return 38
    elif select_index == 3 and data_index == 2:
        return 39
    elif select_index == 4 and data_index == 3:
        return 40
    return -1

def on_button_change(select_index, data_index, state, velocity):
    midi_index = get_button_midi_num(select_index, data_index)
    if midi_index != -1:
        if state:
            midi_player.note_on(CHANNEL, midi_index, velocity)
        else:
            midi_player.note_off(CHANNEL, midi_index)


def init():
    peripherals.register_on_button_change_cb(on_button_change)


def loop():
    pass
