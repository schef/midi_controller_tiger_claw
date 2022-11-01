import peripherals
import midi_player
import common

CHANNEL = 1


def get_button_midi_num(select_index, data_index):
    return 65 - 7 + select_index * 5 + data_index * 1


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
