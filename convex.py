import ast, cmath, copy, fractions, functools, itertools, locale, math, mpmath, operator, parser, random, re, sympy, sys, time
# import dictionary, numpy

stack = []
mpmath.mp.dps = 10000
last_op = 'N/A'
safe_mode = False
debug_mode = False


"""
============
Type Classes
============
"""


class Char(object):
    def __init__(self, character):
        if type(character) == Char:
            self.char = character.char
        elif type(character) == str:
            self.char = ord(character.replace("'", ''))
        else:
            self.char = character

    def __str__(self):
        return chr(self.char)

    def __bool__(self):
        return self.char > 0

    def __add__(self, other):
        if type(other) is Char:
            self.char += other.char
        elif type(other) is int:
            self.char += other
        return self

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __sub__(self, other):
        if type(other) is Char:
            self.char -= other.char
        elif type(other) is int:
            self.char -= other
        return self

    def __rsub__(self, other):
        if other == 0:
            return self
        else:
            return self.__sub__(other)


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

    def __bool__(self):
        return len(self.block) > 2


class Regex(object):
    regex_flags = {
        'i': re.IGNORECASE,
        'a': re.ASCII,
        'm': re.MULTILINE
    }

    def __init__(self, pattern, *flags):
        global regex_flags
        if type(pattern) == Regex:
            self.pattern = str(pattern)
            self.flags = pattern.flags
        else:
            flag_list = []
            for flag in flags:
                flag_list.append(flag)
            if '`' in pattern:
                for flag in pattern.split('`')[0]:
                    flag_list.append(regex_flags[flag])
                self.pattern = pattern.split('`')[1]
            else:
                self.pattern = pattern
            self.flags = flag_list

    def __str__(self):
        return self.pattern

    def flags(self):
        return self.flags

    def __bool__(self):
        return self.pattern != ''


class Quaternion(object):
    def __init__(self, a, b=0, c=0, d=0):
        if type(a) is Quaternion:
            self.a = a.a
            self.b = a.b
            self.c = a.c
            self.d = a.d
        else:
            self.a = a
            self.b = b
            self.c = c
            self.d = d

    def add(self, a, b=0, c=0, d=0):
        if type(a) is Quaternion:
            self.a += a.a
            self.b += a.b
            self.c += a.c
            self.d += a.d
        else:
            self.a += a
            self.b += b
            self.c += c
            self.d += d
        return self

    def subtract(self, a, b=0, c=0, d=0):
        if type(a) is Quaternion:
            self.a -= a.a
            self.b -= a.b
            self.c -= a.c
            self.d -= a.d
        else:
            self.a -= a
            self.b -= b
            self.c -= c
            self.d -= d
        return self

    def multiply(self, a, b=0, c=0, d=0):
        if type(a) is int or type(a) is float:
            self.a *= a
            self.b *= a
            self.c *= a
            self.d *= a
        elif type(a) is Quaternion:
            self.a = self.a * a.a - self.b * a.b - self.c * a.c - self.d * a.d
            self.b = self.b * a.a + self.a * a.b + self.c * a.d - self.d * a.c
            self.c = self.a * a.c - self.b * a.d + self.c * a.a + self.d * a.b
            self.d = self.a * a.d + self.b * a.c - self.c * a.b + self.d * a.a
        else:
            self.multiply(Quaternion(a, b, c, d))
        return self

    def norm(self, q=None):
        if type(q) is Quaternion:
            return q.a**2 + q.b**2 + q.c**2 + q.d**2
        else:
            return self.a ** 2 + self.b ** 2 + self.c ** 2 + self.d ** 2

    def conj(self, q=None):
        if type(q) is Quaternion:
            return Quaternion(q.a, -q.b, -q.c, -q.d)
        else:
            self.b *= -1
            self.c *= -1
            self.d *= -1
            return self

    def magnitude(self, q=None):
        if type(q) is Quaternion:
            return q.norm()**0.5
        else:
            return self.norm()**0.5

    def divide(self, a, b=0, c=0, d=0):
        if type(a) is int or type(a) is float:
            self.a /= a
            self.b /= a
            self.c /= a
            self.d /= a
        elif type(a) is Quaternion:
            self.multiply(a.conj()).divide(a.norm())
        else:
            self.divide(Quaternion(a, b, c, d))
        return self

    def __str__(self):
        result = ""
        if self.a != 0:
            result += str(simplify(self.a))
        if self.b != 0:
            if self.a != 0 and self.b > 0:
                result += '+'
            if self.b == -1:
                result += '-'
            else:
                result += str(simplify(self.b)) if self.b != 1 else ''
            result += 'i'
        if self.c != 0:
            if (self.a != 0 or self.b != 0) and self.c > 0:
                result += '+'
            if self.c == -1:
                result += '-'
            else:
                result += str(simplify(self.c)) if self.c != 1 else ''
            result += 'j'
        if self.d != 0:
            if (self.a != 0 or self.b != 0 or self.c != 0) and self.d > 0:
                result += '+'
            if self.d == -1:
                result += '-'
            else:
                result += str(simplify(self.d)) if self.d != 1 else ''
            result += 'k'
        return result

    def __bool__(self):
        return self.norm() != 0


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
    return type(obj) is list or type(obj) is str or type(obj) is Regex


def is_string(obj):
    return type(obj) is str or type(obj) is Regex


def is_number(obj):
    return type(obj) is int or type(obj) is float


def is_int(obj):
    return type(obj) is int


def is_float(obj):
    return type(obj) is float


def is_char(obj):
    return type(obj) is Char


def is_block(obj):
    return type(obj) is Block


def is_regex(obj):
    return type(obj) is Regex


def push(x):
    if x is True:
        stack.append(1)
    elif x is False:
        stack.append(0)
    elif x is not None:
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


def to_string_repr(obj):
    if type(obj) is str:
        result = "\""
        index = 0
        while index < len(obj):
            char = obj[index]
            if char == '"':
                result += '\\"'
            elif char == '\\':
                if index == len(obj)-1:
                    result += "\\\\"
                else:
                    char2 = obj[index + 1]
                    if char2 == '"' or char2 == '\\':
                        result += "\\\\"
                    else:
                        result += '\\'
            else:
                result += char
            index += 1
        result += "\""
        return result
    elif type(obj) is list:
        result = '['
        for item in obj:
            result += to_string_repr(item)
            result += ' '
        if len(result) > 1:
            result = result[0:len(result)-1] + ']'
        else:
            result += ']'
        return result
    elif type(obj) is Char:
        return "'" + str(obj)
    else:
        return str(obj)


def to_number(num):
    if num == '.':
        return num
    elif '.' in num:
        return float(num)
    else:
        return int(num)


def simplify(num):
    if type(num) is float and int(num) == num:
        return int(num)
    else:
        return num

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
                elif line[index] == '\\':
                    if line[index + 1] == '\\':
                        block += '\\'
                    block += line[index + 1]
                    index += 2
                    continue
                block += line[index]
                if line[index] == open_literals[len(open_literals)-1]:
                    open_literals.pop()
                    if len(open_literals) == 0:
                        line_stack.append(block)
                        block = ''
                index += 1
            elif line[index] == '®':
                open_literals.append('®')
                block += '®'
                index += 1
            elif line[index] == '"':
                open_literals.append('"')
                block += '"'
                index += 1
            elif line[index] == '\'':
                line_stack.append(line[index] + line[index + 1])
                index += 2
            elif line[index] in '0 1 2 3 4 5 6 7 8 9 . -'.split(' '):
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
    if arity == 0:
        return operators[name]['call']()
    elif arity == 1:
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
        if x is True:
            stack.append(1)
        elif x is False:
            stack.append(0)
        elif x is not None:
            temp_stack.append(x)

    def pop_temp_stack():
        if len(temp_stack) > 0:
            return temp_stack.pop()
        else:
            return stack.pop()

    def run_op_temp_stack(name):
        arity = operators[name]['arity']
        if arity == 0:
            return operators[name]['call']()
        elif arity == 1:
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
        if re.match("^-?[0-9.]+$", code_stack[index]):
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
            elif code_stack[index][0] == '®':
                push_temp_stack(Regex(code_stack[index][1:len(code_stack[index]) - 1]))
            index += 1
    return temp_stack


def run(code, dump=False):
    global last_op
    code_stack = split_code(code)
    current_line = 0
    index = 0
    while index < len(code_stack[current_line]):
        if re.match("^-?[0-9.]+$", code_stack[current_line][index]):
            push(to_number(code_stack[current_line][index]))
            index += 1
        elif len(code_stack[current_line][index]) == 1:
            if re.match("[A-Z¢è]", code_stack[current_line][index]):
                push(variables[code_stack[current_line][index]])
                index += 1
            else:
                try:
                    last_op = code_stack[current_line][index]
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
            elif code_stack[current_line][index][0] == '®':
                push(Regex(code_stack[current_line][index][1:len(code_stack[current_line][index])-1]))
            index += 1
    if dump:
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


def wrap_stack():
    global stack
    stack = [stack]
    return None


def power(x, y):
    return simplify(x ** y)


def find_index(x, y):
    if is_list(x):
        if is_block(y):
            for i in range(len(x)):
                if is_string(x):
                    push(Char(ord(x[i])))
                else:
                    push(x[i])
                run(str(y)[1:len(str(y)) - 1])
                if pop():
                    return i
            return -1
        return find(x, y) if is_list(y) else x.index(y)
    if is_list(y):
        if is_block(x):
            return find_index(y, x)
        return y.index(x)
    raise InvalidOverloadError(x, y)


def find(list, sub):
    p = pre_proc(sub)
    m = 0
    for i in range(len(list)):
        while m >= 0 and sub[m] != list[i]:
            m = p[m]
        if m == len(sub) - 1:
            return i - m
        m += 1
    return -1


def pre_proc(list):
    p = [-1]
    n = 0
    for i in range(1, len(list)):
        if list[i] == list[n]:
            p.append(p[n])
        else:
            p.append(n)
            while True:
                n = p[n]
                if not (n >= 0 and list[i] != list[n]):
                    break
        n += 1
    return p


def check_equal(x, y):
    if is_char(x) and is_char(y):
        return x.char == y.char
    if type(x) == type(y):
        return x == y
    if is_number(x) and is_number(y):
        return float(x) == float(y)
    if is_char(x) and is_number(y):
        return x.char == int(y)
    if is_number(x) and is_char(y):
        return int(x) == y.char
    return get_value(x, y)


def get_value(x, y):
    if is_list(y) and not is_list(x):
        return get_value(y, x)
    if is_list(x):
        if is_number(y):
            if is_string(x):
                return Char(ord(x[int(y) % len(x)]))
            else:
                return x[int(y) % len(x)]
        if is_block(y):
            for i in range(len(x)):
                if is_string(x):
                    push(Char(ord(x[i])))
                else:
                    push(x[i])
                run(str(y)[1:len(str(y)) - 1])
                if pop():
                    if is_string(x):
                        return Char(x[i])
                    else:
                        return x[i]
            return None
    raise InvalidOverloadError(x, y)


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
        call=lambda: None
    ),
    'a': attrdict(
        arity=1,
        call=lambda x: [x]
    ),
    'Þ': attrdict(
        arity=1,
        call=lambda x: eval(x) if is_string(x) and not safe_mode else change_variable_accuracy(x)
    ),
    '~': attrdict(
        arity=1,
        call=tilda
    ),
    '`': attrdict(
        arity=1,
        call=to_string_repr
    ),
    ']': attrdict(
        arity=0,
        call=wrap_stack
    ),
    '!': attrdict(
        arity=1,
        call=lambda x: not x
    ),
    ';': attrdict(
        arity=1,
        call=lambda x: None
    ),
    '_': attrdict(
        arity=0,
        call=lambda: push(peek())
    ),
    '#': attrdict(
        arity=2,
        call=lambda x, y: power(x, y) if is_number(x) and is_number(y) else find_index(x, y)
    ),
    '=': attrdict(
        arity=2,
        call=check_equal
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
            print("-safe: disables file IO, Python eval, and operators with internet access.")
            print("-sm: disables file IO, Python eval, and operators with internet access.")
            print("-debug: prints the stack in list form after program execution.")
            print("-d: prints the stack in list form after program execution.")
            index += 1
        elif sys.argv[index] in ("-accuracy", "-a"):
            if index + 1 == len(sys.argv):
                print("Not enough arguments.\nFor Help: python convex.py --help")
                break
            else:
                if 'k' in sys.argv[index + 1] or 'm' in sys.argv[index + 1]:
                    mpmath.mp.dps = int(sys.argv[index + 1][:len(sys.argv[index + 1])-1]) * {'k': 1000, 'm': 1000000}[sys.argv[index + 1][len(sys.argv[index + 1])-1]]
                else:
                    mpmath.mp.dps = int(sys.argv[index + 1])
                index += 2
        elif sys.argv[index] in ("-file", "-f"):
            if index + 1 == len(sys.argv):
                print("Not enough arguments.\nFor Help: python convex.py --help")
                break
            else:
                file = open(sys.argv[index + 1])
                run(file.read(), True)
                if debug_mode:
                    print("\nStack: ", to_string_repr(stack))
                index += 2
        elif sys.argv[index] in ("-code", "-c"):
            if index + 1 == len(sys.argv):
                print("Not enough arguments.\nFor Help: python convex.py --help")
                break
            else:
                run(sys.argv[index + 1], True)
                if debug_mode:
                    print("\nStack: ", to_string_repr(stack))
                index += 2
        elif sys.argv[index] in ("-shell", "-s"):
            while True:
                stack = []
                mpmath.mp.dps = 10000
                try:
                    run(input(">>> "), True)
                    if debug_mode:
                        print("\nStack: ", to_string_repr(stack))
                except InvalidOperatorError as err:
                    print("Invalid operator:", err)
                except InvalidOverloadError as err:
                    print(err)
        elif sys.argv[index] in ("-safe", "-sm"):
            safe_mode = True
            index += 1
        elif sys.argv[index] in ("-debug", "-d"):
            debug_mode = True
            index += 1
