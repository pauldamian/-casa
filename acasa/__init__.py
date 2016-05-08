TEST = False


def set_test_mode():
    global TEST
    TEST = True


def mode():
    global TEST
    print TEST
