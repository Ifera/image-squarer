import os

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def strip_invalid_chars(name: str):
    chars = ['\\', '/', ':', '|', "*", '?', '<', '>', '"']

    for c in chars:

        if c == ':' or c == '/':
            rep = '-'
        else:
            rep = ''

        name = name.replace(c, rep)

    return name

