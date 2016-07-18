class Char(object):
    def __init__(self, character):
        if type(character) == Char:
            self.char = character.to_string()
        else:
            self.char = character[1]

    def to_string(self):
        return self.char


def is_list(obj):
    return type(obj) is list


def is_string(obj):
    return type(obj) is str


def is_number(obj):
    return type(obj) is int or obj is float


def is_int(obj):
    return type(obj) is int


def is_float(obj):
    return type(obj) is float


def is_char(obj):
    return type(obj) is Char


def is_block(obj):
    return is_string(obj) and obj[0] == '{'
