import ast, cmath, copy, fractions, functools, itertools, locale, math, mpmath, operator, parser, random, re, sympy, sys, time
# import dictionary, numpy

stack = []
mpmath.mp.dps = 10000
last_op = 'N/A'


"""
============
Type Classes
============
"""


class Char(object):
    def __init__(self, character):
        if type(character) == Char:
            self.char = str(character)
        else:
            self.char = character[1]

    def __str__(self):
        return self.char


class Block(object):
    def __init__(self, block):
        if type(block) == Block:
            self.block = str(block)
        else:
            self.block = block

    def __str__(self):
        return self.block

    def run(self):
        return run(self.block)


class InvalidOperatorError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidOverloadError(Exception):
    def __init__(self, a, b=None, c=None, op=None):
        self.a = a
        self.b = b
        self.c = c
        if op is None:
            self.op = last_op
        else:
            self.op = op

    def __str__(self):
        if self.a and self.b and self.c:
            return "Invalid overload for {} {} {} [{}]" .format(type(self.a), type(self.b), type(self.c), self.op)
        elif self.a and self.b:
            return "Invalid overload for {} {} [{}]" .format(type(self.a), type(self.b), self.op)
        elif self.a:
            return "Invalid overload for {} [{}]".format(type(self.a), self.op)

"""
==============
Util Functions
==============
"""


class attrdict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self


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
    return type(obj) is Block


def push(x):
    if x is not None:
        stack.append(x)


def pop():
    return stack.pop()


def peek():
    return stack[len(stack)-1]


def to_string(obj):
    if type(obj) is str:
        return obj
    elif type(obj) is int or type(obj) is float or type(obj) is Char:
        return str(obj)
    elif type(obj) is list:
        result = ""
        for item in obj:
            result += to_string(item)
        return result
    else:
        return str(obj)


# TODO: FINISH
def to_string_repr(obj):
    return "Not Ready Yet"


def to_number(num):
    if num == '.':
        return num
    elif '.' in num:
        return float(num)
    else:
        return int(num)

"""
=======================
Convex Runner Functions
=======================
"""


def split_code(code):
    lines = re.split("(?<!')\n", code)
    result = []
    for line in lines:
        line_stack = []
        block = ''
        index = 0
        open_literals = []
        while index < len(line):
            if line[index] == '{':
                open_literals.append('}')
                block += '{'
                index += 1
            elif line[index] == '[':
                open_literals.append(']')
                block += '['
                index += 1
            elif open_literals:
                if line[index] == '\\' and open_literals[len(open_literals)-1] == '"' and line[index + 1] == '"':
                    block += '\\"'
                    index += 2
                    continue
                block += line[index]
                if line[index] == open_literals[len(open_literals)-1]:
                    open_literals.pop()
                    if len(open_literals) == 0:
                        line_stack.append(block)
                        block = ''
                index += 1
            elif line[index] == '"':
                open_literals.append('"')
                block += '"'
                index += 1
            elif line[index] == '\'':
                line_stack.append(line[index] + line[index + 1])
                index += 2
            elif line[index] in '0 1 2 3 4 5 6 7 8 9 .'.split(' '):
                dot = line[index] == '.'
                num = line[index]
                index += 1
                while index < len(line):
                    if line[index] == '.':
                        if dot:
                            break
                        else:
                            num += '.'
                            dot = True
                        index += 1
                    elif line[index] in '0 1 2 3 4 5 6 7 8 9'.split(' '):
                        num += line[index]
                        index += 1
                    else:
                        break
                line_stack.append(num)
                # print(num)
            else:
                line_stack.append(line[index])
                index += 1
        result.append(line_stack)
    return result


def run_op(name):
    arity = operators[name]['arity']
    if arity == 1:
        a = pop()
        return operators[name]['call'](a)
    elif arity == 2:
        a = pop()
        b = pop()
        return operators[name]['call'](b, a)
    elif arity == 3:
        a = pop()
        b = pop()
        c = pop()
        return operators[name]['call'](c, b, a)


def run_temp_stack(code):
    global last_op
    temp_stack = []
    code_stack = split_code(code)[0]

    def push_temp_stack(x):
        if x is not None:
            temp_stack.append(x)

    def pop_temp_stack():
        if len(temp_stack) > 0:
            return temp_stack.pop()
        else:
            return stack.pop()

    def run_op_temp_stack(name):
        arity = operators[name]['arity']
        if arity == 1:
            a = pop_temp_stack()
            return operators[name]['call'](a)
        elif arity == 2:
            a = pop_temp_stack()
            b = pop_temp_stack()
            return operators[name]['call'](b, a)
        elif arity == 3:
            a = pop_temp_stack()
            b = pop_temp_stack()
            c = pop_temp_stack()
            return operators[name]['call'](c, b, a)
    index = 0
    while index < len(code_stack):
        if re.match("^[0-9.]+$", code_stack[index]):
            push_temp_stack(to_number(code_stack[index]))
            index += 1
        elif len(code_stack[index]) == 1:
            if re.match("[A-Z¢è]", code_stack[index]):
                push_temp_stack(variables[code_stack[index]])
                index += 1
            else:
                try:
                    last_op = code_stack[index]
                    push_temp_stack(run_op_temp_stack(code_stack[index]))
                except KeyError:
                    raise InvalidOperatorError(code_stack[index])
                index += 1
        else:
            if code_stack[index][0] == '"':
                push_temp_stack(eval(code_stack[index]))
            elif code_stack[index][0] == '\'':
                push_temp_stack(Char(code_stack[index]))
            elif code_stack[index][0] == '[':
                push_temp_stack(run_temp_stack(code_stack[index][1:len(code_stack[index]) - 1]))
            elif code_stack[index][0] == '{':
                push_temp_stack(Block(code_stack[index]))
            index += 1
    return temp_stack


def run(code):
    global last_op
    code_stack = split_code(code)
    current_line = 0
    index = 0
    while index < len(code_stack[current_line]):
        if re.match("^[0-9.]+$", code_stack[current_line][index]):
            push(to_number(code_stack[current_line][index]))
            index += 1
        elif len(code_stack[current_line][index]) == 1:
            if re.match("[A-Z¢è]", code_stack[current_line][index]):
                push(variables[code_stack[current_line][index]])
                index += 1
            else:
                try:
                    last_op = code_stack[current_line][index]
                    print(code_stack[current_line][index])
                    push(run_op(code_stack[current_line][index]))
                except KeyError:
                    raise InvalidOperatorError(code_stack[current_line][index])
                index += 1
        else:
            if code_stack[current_line][index][0] == '"':
                push(eval(code_stack[current_line][index]))
            elif code_stack[current_line][index][0] == '\'':
                push(Char(code_stack[current_line][index]))
            elif code_stack[current_line][index][0] == '[':
                push(run_temp_stack(code_stack[current_line][index][1:len(code_stack[current_line][index])-1]))
            elif code_stack[current_line][index][0] == '{':
                push(Block(code_stack[current_line][index]))
            index += 1
    dump_print(stack)
    print()


def dump_print(stack_list):
    for item in stack_list:
        if type(item) is list:
            dump_print(item)
        else:
            print(to_string(item), end="")


"""
==================
Operator Functions
==================
"""


def base_convert(list_a, base):
    if is_number(list_a) and is_list(base):
        return base_convert(base, list_a)


def change_variable_accuracy(accuracy):
    if is_number(accuracy):
        mpmath.mp.dps = int(accuracy)


def tilda(obj):
    if is_number(obj):
        if is_float(obj):
            raise InvalidOverloadError(obj)
        elif is_int(obj):
            return ~obj
    elif is_block(obj):
        run(str(obj)[1:len(str(obj))-1])
        return None
    elif is_string(obj) or is_char(obj):
        run(str(obj))
        return None
    elif is_list(obj):
        for item in obj:
            push(item)
        return None
    else:
        raise InvalidOverloadError(obj)


variables = {
    'A': 10,
    'B': 11,
    'C': 12,
    'D': 13,
    'E': 14,
    'F': 15,
    'G': 16,
    'H': 17,
    'I': 18,
    'J': 19,
    'K': 20,
    'L': [],
    'M': '',
    'N': '\n',
    'O': '',
    'P': mpmath.pi,
    'Q': 0,
    'R': 0,
    'S': ' ',
    'T': 'abcdefghijklmnopqrstuvwxyz',
    'U': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'V': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'W': -1,
    'X': 1,
    'Y': 2,
    'Z': 3,
    '¢': mpmath.phi,
    'è': mpmath.e
}

operators = {
    ' ': attrdict(
        arity=0,
        call=None
    ),
    'a': attrdict(
        arity=1,
        call=lambda x: [x]
    ),
    'b': attrdict(
        arity=2,
        call=base_convert
    ),
    'Þ': attrdict(
        arity=1,
        call=lambda x: eval(x) if is_string(x) else change_variable_accuracy(x)
    ),
    '~': attrdict(
        arity=1,
        call=tilda
    )
}


if len(sys.argv) == 1:
    print("Not enough arguments.\nFor Help: python convex.py --help")
else:
    index = 1
    while index < len(sys.argv):
        if sys.argv[index] in ("-help", "-h", "-?"):
            print("Convex Help")
            print()
            print("Usage: python convex.py [--flag] <program>")
            print()
            print("Flags:")
            print("-help: display the usage information of this program.")
            print("-h: display the usage information of this program.")
            print("-?: display the usage information of this program.")
            print("-accuracy <digits>: changes the accuracy for mathematical operations and constants.")
            print("-a <digits>: changes the accuracy for mathematical operations and constants.")
            print("-file <file>: runs the program specified in the file at the path provided, using the CP-1252 encoding.")
            print("-f <file>: runs the program specified in the file at the path provided, using the CP-1252 encoding.")
            print("-code <code>: runs the code provided.")
            print("-c <code>: runs the code provided.")
            print("-shell: starts an interactive Convex shell.")
            print("-s: starts an interactive Convex shell.")
            index += 1
        elif sys.argv[index] in ("-accuracy", "-a"):
            if index + 1 == len(sys.argv):
                print("Not enough arguments.\nFor Help: python convex.py --help")
                break
            else:
                mpmath.mp.dps = int(sys.argv[index + 1])
                index += 2
        elif sys.argv[index] in ("-file", "-f"):
            if index + 1 == len(sys.argv):
                print("Not enough arguments.\nFor Help: python convex.py --help")
                break
            else:
                file = open(sys.argv[index + 1])
                run(file.read())
                index += 2
        elif sys.argv[index] in ("-code", "-c"):
            if index + 1 == len(sys.argv):
                print("Not enough arguments.\nFor Help: python convex.py --help")
                break
            else:
                run(sys.argv[index + 1])
                index += 2
        elif sys.argv[index] in ("-shell", "-s"):
            while True:
                stack = []
                mpmath.mp.dps = 10000
                try:
                    run(input(">>> "))
                    print(stack)
                except InvalidOperatorError as err:
                    print("Invalid operator:", err)
                except InvalidOverloadError as err:
                    print(err)
