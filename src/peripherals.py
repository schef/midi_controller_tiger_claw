import common

on_button_change_cb = None


def init():
    pass


def loop():
    pass


def register_on_button_change_cb(cb):
    global on_button_change_cb
    on_button_change_cb = cb


def test_loop():
    init()
    while True:
        loop()
