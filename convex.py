import ast, cmath, copy, fractions, functools, itertools, locale, math, mpmath, operator, parser, random, re, sympy, sys, time, urllib.request
# import dictionary, numpy

stack = []
marks = []
mpmath.mp.dps = 10000
last_op = 'N/A'
safe_mode = False
debug_mode = False
CONVEX_VERSION = "0.6.3"


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
            self.char = ord(character.replace("'", '')[0])
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

    def __len__(self):
        return 1

    def __getitem__(self, item):
        return chr(self.char)

    def __float__(self):
        return float(self.char)

    def __int__(self):
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

    def __float__(self):
        return self.a


class InvalidOperatorError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidArgumentError(Exception):
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


def push(*items):
    for x in items:
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


def mark():
    marks.append(len(stack))


def pop_mark():
    start = 0 if len(marks) == 0 else marks.pop()
    result = []
    for _ in range(start, len(stack)):
        result.append(stack.pop(start))
    push(result)


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


def list_contains(list, item):
    for i in list:
        if check_equal(item, i):
            return True
    return False


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


def to_new_list(x):
    if is_string(x):
        return x
    if is_list(x):
        return x.copy()
    return [x]


def to_list(x):
    if is_list(x):
        if is_string(x):
            result = []
            for char in x:
                result.append(Char(char))
            return result
        return x
    else:
        return [x]


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
    return None


def any_char(*values):
    for item in values:
        if is_char(item):
            return True
    return False


def any_number(*values):
    for item in values:
        if is_number(item):
            return True
    return False


def any_list(*values):
    for item in values:
        if is_list(item):
            return True
    return False


def any_block(*values):
    for item in values:
        if is_block(item):
            return True
    return False


def any_string(*values):
    for item in values:
        if is_string(item):
            return True
    return False


def any_int(*values):
    for item in values:
        if is_int(item):
            return True
    return False


def any_float(*values):
    for item in values:
        if is_float(item):
            return True
    return False


def all_char(*values):
    for item in values:
        if not is_char(item):
            return False
    return True


def all_number(*values):
    for item in values:
        if not is_number(item):
            return False
    return True


def all_list(*values):
    for item in values:
        if not is_list(item):
            return False
    return True


def all_block(*values):
    for item in values:
        if not is_block(item):
            return False
    return True


def all_string(*values):
    for item in values:
        if not is_string(item):
            return False
    return True


def all_int(*values):
    for item in values:
        if not is_int(item):
            return False
    return True


def all_float(*values):
    for item in values:
        if not is_float(item):
            return False
    return True


def fix_list(list):
    string = True
    for item in list:
        if not (is_char(item) or is_string(item)):
            string = False
    if string:
        temp = ''
        for item in list:
            temp += str(item)
        return temp
    return list


def pair(x, y):
    return [x, y]


def find_index(x, y):
    if is_list(x):
        if is_block(y):
            for i in range(len(x)):
                if is_string(x):
                    push(Char(ord(x[i])))
                else:
                    push(x[i])
                run_block(y)
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


def run(code, dump=False):
    global last_op
    code_stack = split_code(code)
    current_line = 0
    index = 0
    while index < len(code_stack[current_line]):
        if re.match("^-?([0-9]+\.?[0-9]*|[0-9]*\.?[0-9]+)$", code_stack[current_line][index]):
            push(to_number(code_stack[current_line][index]))
            index += 1
        elif len(code_stack[current_line][index]) == 1:
            if re.match("[A-Z¢è]", code_stack[current_line][index]):
                push(variables[code_stack[current_line][index]])
                index += 1
            # Infix ops
            elif code_stack[current_line][index][0] == ':':
                if index + 1 == len(code_stack):
                    print('Unfinished operator: \':\'')
                    break
                else:
                    if re.match("[A-Z¢è]", code_stack[current_line][index + 1]):
                        variables[code_stack[current_line][index + 1]] = peek()
                    elif len(code_stack[current_line][index + 1]) == 1:
                        try:
                            arity = operators[code_stack[current_line][index + 1]]['arity']
                            if arity == 1:
                                push(quick_map(pop(), code_stack[current_line][index + 1]))
                            elif arity == 2:
                                push(quick_fold(pop(), code_stack[current_line][index + 1]))
                            else:
                                print('Unhandled operator after \':\': ' + code_stack[current_line][index + 1])
                                break
                        except KeyError:
                            raise InvalidOperatorError(code_stack[current_line][index + 1])
                    else:
                        print('Unhandled operator after \':\': ' + code_stack[current_line][index + 1])
                        break
                    index += 2
            elif code_stack[current_line][index][0] == '.':
                if index + 1 == len(code_stack):
                    print('Unfinished operator: \'.\'')
                    break
                else:
                    if code_stack[current_line][index + 1][0] == '{':
                        block = Block(code_stack[current_line][index + 1])
                        push(vectorize(block))
                    elif len(code_stack[current_line][index + 1]) == 1:
                        if operators[code_stack[current_line][index + 1]]['arity'] == 2:
                            block = Block('{' + code_stack[current_line][index + 1] + '}')
                            push(vectorize(block))
                        else:
                            print('Unhandled operator after \'.\': ' + code_stack[current_line][index + 1])
                            break
                    else:
                        print('Unhandled operator after \'.\': ' + code_stack[current_line][index + 1])
                        break
                    index += 2
            elif code_stack[current_line][index][0] == 'e':
                if index + 1 == len(code_stack):
                    print('Unfinished operator: \'e\'')
                    break
                else:
                    if re.match("^-?([0-9]+\.?[0-9]*|[0-9]*\.?[0-9]+)$", code_stack[current_line][index + 1]):
                        push(pop() * 10 ** to_number(code_stack[current_line][index + 1]))
                    index += 2
            elif code_stack[current_line][index][0] == 'f':
                if index + 1 == len(code_stack):
                    print('Unfinished operator: \'f\'')
                    break
                else:
                    if re.match("^[A-Z¢è]$", code_stack[current_line][index + 1]):
                        var = code_stack[current_line][index + 1][0]
                        y = pop()
                        x = pop()
                        if is_block(y):
                            if is_number(x):
                                for i in range(int(x)):
                                    variables[var] = i
                                    run_block(y)
                            elif is_list(x):
                                for i in to_list(x):
                                    variables[var] = i
                                    run_block(y)
                        elif is_block(x):
                            if is_number(y):
                                for i in range(int(y)):
                                    variables[var] = i
                                    run_block(x)
                            elif is_list(y):
                                for i in to_list(y):
                                    variables[var] = i
                                    run_block(x)
                        else:
                            raise InvalidOverloadError(x, y, 'f')
                    else:
                        if code_stack[current_line][index + 1][0] == '{':
                            op = Block(code_stack[current_line][index + 1])
                        else:
                            op = Block('{' + code_stack[current_line][index + 1] + '}')
                        y = pop()
                        x = pop()
                        if is_list(x):
                            mark()
                            for o in to_list(x):
                                push(o)
                                push(y)
                                run_block(op)
                            pop_mark()
                        elif is_list(y):
                            mark()
                            for o in to_list(y):
                                push(x)
                                push(o)
                                run_block(op)
                            pop_mark()
                        else:
                            raise InvalidOverloadError(x, y, 'f')
                    index += 2
            elif code_stack[current_line][index][0] == 'u':
                if not is_number(peek()):
                    raise InvalidOverloadError(peek(), 'u')
                current_line = int(pop())
                index = 0
            elif code_stack[current_line][index][0] == 'v':
                y = pop()
                x = pop()
                if not (any_list(x, y)):
                    raise InvalidOverloadError(x, y, 'v')
                if is_list(y):
                    z = find_index(y, x)
                else:
                    z = find_index(x, y)
                current_line = int(z)
                index = 0
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
                mark()
                run(code_stack[current_line][index][1:len(code_stack[current_line][index])-1])
                pop_mark()
            elif code_stack[current_line][index][0] == '{':
                push(Block(code_stack[current_line][index]))
            elif code_stack[current_line][index][0] == '®':
                push(Regex(code_stack[current_line][index][1:len(code_stack[current_line][index])-1]))
            index += 1
    if dump:
        dump_print(stack)
        print()


def run_block(block):
    run(str(block)[1:len(str(block)) - 1])


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


def op_tilda(obj):
    if is_number(obj):
        if is_float(obj):
            raise InvalidOverloadError(obj)
        elif is_int(obj):
            return ~obj
    elif is_block(obj):
        run_block(obj)
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
                run_block(y)
                if pop():
                    if is_string(x):
                        return Char(x[i])
                    else:
                        return x[i]
            return None
    raise InvalidOverloadError(x, y)


def quick_map(list, op):
    if not is_list(list):
        raise InvalidOverloadError(list, op)
    mark()
    for item in list:
        push(item)
        run(op)
    pop_mark()
    push(fix_list(pop()))
    return None


def quick_fold(list, op):
    if not is_list(list):
        raise InvalidOverloadError(list, op)
    push(list[0])
    for i in range(1, len(list)):
        push(list[i])
        run(op)
    return None


def op_percent(x, y):
    if is_block(x):
        if is_block(y):
            raise InvalidOverloadError(x, y)
        return op_percent(y, x)
    if is_number(x):
        if is_list(y):
            return op_percent(y, x)
        if is_number(y):
            return simplify(mod(x, y))
        if is_block(y):
            mark()
            for i in range(int(x)):
                push(i)
                run_block(y)
            pop_mark()
            push(fix_list(pop()))
            return None
    if is_list(x):
        if is_number(y):
            return x[::int(y)]
        if is_block(y):
            mark()
            for item in x:
                push(item)
                run_block(y)
            pop_mark()
            push(fix_list(pop()))
            return None
        if is_list(y) or is_char(y):
            return split(x, y, False)
    raise InvalidOverloadError(x, y)


def split(list, sub, empty):
    p = pre_proc(sub)
    x = 0
    m = 0
    result = []
    for i in range(len(list)):
        while m >= 0 and sub[m] != list[i]:
            m = p[m]
        if m == len(sub) - 1:
            t = list[x:i-m]
            if empty or len(t) != 0:
                result.append(t)
            x = i + 1
            m = -1
        m += 1
    t = list[x:len(list)]
    if empty or len(t) != 0:
        result.append(t)
    return result


def mod(x, y):
    a = math.fabs(x)
    b = math.fabs(y)
    if b == 0:
        raise ZeroDivisionError("modulus division by zero")
    r = a
    while r - b >= 0:
        r -= b
    return r * (1 if x >= 0 else -1)


def op_dollar(x):
    if is_number(x):
        y = -1 - x if x < 0 else len(stack) - 1 - x
        if y < 0 or y >= len(stack):
            raise IndexError("stack index out of range")
        return stack[y]
    if is_string(x):
        return ''.join(sorted(x))
    if is_list(x):
        return sort(to_new_list(x))
    if is_block(x):
        block = x
        list = pop()
        if not is_list(list):
            raise InvalidOverloadError(list, block)
        result = []
        for item in list:
            push(item)
            run_block(block)
            result.append([item, pop()])
        l = sort(result, lambda a, b: compare(a[1], b[1]))
        r = []
        for t in l:
            r.append(t[0])
        return r


def compare(x, y):
    if is_list(x) and is_list(y):
        return compare_lists(x, y)
    if all_char(x, y) or all_number(x, y) or (any_char(x, y) and any_number(x, y)):
        if check_equal(x, y):
            return 0
        return -1 if float(x) > float(y) else 1
    raise TypeError("Can't compare types " + type(x) + " and " + type(y))


def compare_lists(x, y):
    a = to_list(x)
    b = to_list(y)
    n = min(len(a), len(b))
    for i in range(n):
        z = compare(a[i], b[i])
        if z:
            return z
    return len(x) - len(y)


def sort(list, comp=compare):
    result = list.copy()
    while True:
        is_sorted = True
        index = 0
        while index + 1 < len(result):
            z = comp(result[index], result[index + 1])
            if z == -1:
                temp = result[index]
                result[index] = result[index + 1]
                result[index + 1] = temp
                is_sorted = False
            index += 1
        if is_sorted:
            return result


def op_ampersand(x, y):
    if all_int(x, y):
        return x & y
    if is_block(y):
        if x:
            run_block(y)
        return None
    if any_string(x, y):
        if not (all_string(x, y) or any_char(x, y)):
            raise InvalidOverloadError(x, y)
        l1 = to_list(x)
        l2 = to_list(y)
        result = op_ampersand(l1, l2)
        # string = ''
        # for i in result:
        #     string += chr(i)
        # return string
        return fix_list(result)
    if any_list(x, y):
        result = []
        l1 = to_list(x)
        l2 = to_list(y)
        for item in l1:
            try:
                if list_contains(l2, item) and not list_contains(result, item):
                    result.append(item)
            except ValueError:
                pass
        return result
    if all_char(x, y) or (any_char(x, y) and any_number(x, y)):
        return Char(int(x) & int(y))
    raise InvalidOverloadError(x, y)


def inc(x):
    if is_number(x):
        return x + 1
    if is_char(x):
        return Char(int(x) + 1)


def dec(x):
    if is_number(x):
        return x - 1
    if is_char(x):
        return Char(int(x) - 1)


def uncon(x, dir='right'):
    if not is_list(x):
        raise InvalidOverloadError(x)
    if dir == 'right':
        push(x[:len(x)-1])
        return Char(x[len(x)-1]) if is_string(x) else x[len(x)-1]
    if dir == 'left':
        push(x[1:len(x)])
        return Char(x[0]) if is_string(x) else x[0]
    raise InvalidOverloadError(x)


def op_asterisk(x, y):
    if is_number(x) and (is_list(y) or is_char(y) or is_block(y)):
        return op_asterisk(y, x)
    if (is_block(x) or is_char(x)) and is_list(y):
        return op_asterisk(y, x)
    if (is_list(x) or is_char(x)) and is_number(y):
        if len(x) * int(y) == 0:
            return "" if is_string(x) else []
        if is_char(x):
            return str(x) * int(y)
        return x * int(y)
    if is_block(x) and is_number(y):
        for _ in range(int(y)):
            run_block(x)
        return None
    if is_list(x):
        if is_block(y):
            push(x[0])
            for i in range(1, len(x)):
                push(x[i])
                run_block(y)
            return None
        if is_list(y) or is_char(y):
            result = [x[0]]
            l = to_list(y)
            for i in range(1, len(x)):
                result += l
                result.append(x[i])
            return fix_list(result)
    raise InvalidOverloadError(x, y)


def op_plus(x, y):
    if (is_list(x) or is_list(y)) or all_char(x, y):
        result = to_list(x) + to_list(y)
        return fix_list(result)
    if any_char(x, y) and any_number(x, y):
        return Char(int(x) + int(y))
    raise InvalidOverloadError(x, y)


def op_comma(x):
    if is_number(x):
        return list(range(int(x)))
    if is_char(x):
        result = ''
        for char in list(range(int(x))):
            result += chr(char)
        return result
    if is_list(x):
        return len(x)
    if is_block(x):
        y = pop()
        if is_list(y):
            result = []
            for item in y:
                push(item)
                run_block(x)
                if pop():
                    result.append(item)
            return fix_list(result)
        if is_number(y):
            result = []
            for i in range(y):
                push(i)
                run_block(x)
                if pop():
                    result.append(i)
            return result
        raise InvalidOverloadError(y, x)
    raise InvalidOverloadError(x)


def op_minus(x, y):
    if all_char(x, y):
        return int(x) - int(y)
    if any_char(x, y) and any_number(x, y):
        return Char(int(x) - int(y))
    if any_list(x, y):
        if any_block(x, y):
            raise InvalidOverloadError(x, y)
        result = [z for z in to_list(x) if not list_contains(to_list(y), z)]
        return fix_list(result)
    raise InvalidOverloadError(x, y)


def vectorize(block):
    y = pop()
    x = pop()
    if not all_list(x, y):
        raise InvalidOverloadError(x, y)
    xl = to_list(x)
    xn = len(xl)
    yl = to_list(y)
    yn = len(yl)
    mark()
    for i in range(max(xn, yn)):
        if i < xn:
            push(xl[i])
            if i < yn:
                push(yl[i])
                run_block(block)
        else:
            push(yl[i])
    pop_mark()


def op_fslash(x, y):
    if all_number(x, y):
        if all_int(x, y):
            return simplify(x // y)
        return simplify(x / y)
    if is_block(x):
        if is_block(y):
            raise InvalidOverloadError(x, y)
        return op_fslash(y, x)
    if is_number(x):
        if is_list(y):
            return op_fslash(y, x)
        if is_block(y):
            for i in range(x):
                push(i)
                run_block(y)
            return None
    if is_list(x):
        if is_block(y):
            for item in to_list(x):
                push(item)
                run_block(y)
            return None
        if is_list(y) or is_char(y):
            return split(x, y, True)
        if is_number(y):
            if y <= 0:
                raise IndexError("split size out of range")
            result = []
            for i in range(0, len(x), y):
                result.append(x[i:min(i + y, len(x))])
            return result
    raise InvalidOverloadError(x, y)


def op_lt(x, y):
    if is_number(x) and is_list(y):
        return op_lt(y, x)
    if is_list(x) and is_number(y):
        return x[:y % len(x)]
    return compare(x, y) > 0


def op_gt(x, y):
    if is_number(x) and is_list(y):
        return op_gt(y, x)
    if is_list(x) and is_number(y):
        return x[y % len(x):]
    return compare(x, y) < 0


def op_ternary(x, y, z):
    o = y if x else z
    if is_block(o):
        run_block(o)
        return None
    return o


def stack_rotate(x, y, z):
    push(y)
    push(z)
    push(x)
    return None


def stack_swap(x, y):
    push(y)
    push(x)
    return None


def op_caret(x, y):
    if all_int(x, y):
        return x ^ y
    if any_list(x, y):
        if any_block(x, y):
            raise InvalidOverloadError(x, y)
        result = []
        l1 = to_list(x)
        l2 = to_list(y)
        for item in l1:
            try:
                if not list_contains(l2, item) and not list_contains(result, item):
                    result.append(item)
            except ValueError:
                pass
        for item in l2:
            try:
                if not list_contains(l1, item) and not list_contains(result, item):
                    result.append(item)
            except ValueError:
                pass
        return fix_list(result)
    if all_char(x, y):
        return int(x) ^ int(y)
    if any_char(x, y) and any_int(x, y):
        return Char(int(x) ^ int(y))
    raise InvalidOverloadError(x, y)


def base_convert(x, y):
    if is_number(x) and is_list(y):
        return base_convert(y, x)
    if not is_number(y) or any_float(x, y):
        raise InvalidOverloadError(x, y)
    if is_number(x):
        l = []
        ai = abs(int(x))
        bi = abs(int(y))
        if bi == 1:
            l = [1] * ai
        else:
            while ai != 0:
                l.append(ai % bi)
                ai //= bi
        if len(l) == 0:
            l.append(0)
        return l[::-1]
    if is_list(x):
        i = abs(int(y))
        t = 0
        for o in to_list(x):
            t = t * i + int(o)
        return t
    raise InvalidOverloadError(x, y)


def op_g(x):
    if is_block(x):
        while True:
            run_block(x)
            if not pop():
                break
        return None
    if is_number(x):
        if x > 0:
            return 1
        elif x < 0:
            return -1
        else:
            return 0
    if not is_string(x) or safe_mode:
        raise InvalidOverloadError(x)
    link = x
    if not link.__contains__("://"):
        link = "http://" + link
    f = urllib.request.urlopen(link)
    return f.read().decode("utf-8")


def op_h(x):
    if not is_block(x):
        raise InvalidOverloadError(x)
    while True:
        run_block(x)
        if not peek():
            break
    return None


def read_token():
    token = ''
    while True:
        c = sys.stdin.read(1)
        if re.match("\\s", c):
            return token
        token += c


def dump_string(stack_list):
    s = ''
    for item in stack_list:
        if type(item) is list:
            s += dump_string(item)
        else:
            s += to_string(item)
    return s


def set_item(x, y, z):
    if is_number(x) and is_list(y):
        return set_item(y, x, z)
    if is_string(x) and is_number(y):
        l = x
        return l[:y % len(l)] + dump_string(to_new_list(z)) + (l[y % len(l) + 1] if y % len(l) + 1 < len(l) else [])
    if is_list(x) and is_number(y):
        l = to_new_list(x)
        l[y % len(l)] = z
        return l
    raise InvalidOverloadError(x, y, z)


def while_loop(x, y):
    if not all_block(x, y):
        raise InvalidOverloadError(x, y)
    while True:
        run_block(x)
        if not pop():
            break
        run_block(y)
    return None


def transpose(x):
    if is_list(x):
        l = []
        for o in to_list(x):
            l2 = to_list(o)
            for j in range(len(l2)):
                lj = None
                if j == len(l):
                    lj = []
                    l.append(to_list(lj))
                else:
                    lj = to_list(l[j])
                lj.append(l2[j])
        r = []
        for i in l:
            r.append(fix_list(i))
        return r
    raise InvalidOverloadError(x)


def op_bar(x, y):
    if all_int(x, y):
        return x | y
    if is_block(x):
        raise InvalidOverloadError(x, y)
    if is_block(y):
        if not x:
            run_block(y)
        return None
    if any_list(x, y):
        l = []
        for i in to_list(x):
            if not list_contains(l, i):
                l.append(i)
        for j in to_list(y):
            if not list_contains(l, j):
                l.append(j)
        return fix_list(l)
    if any_char(x, y) and any_int(x, y):
        return Char(int(x) | int(y))
    raise InvalidOverloadError(x, y)


def cum_sum(x):
    if not is_list(x):
        raise InvalidOverloadError(x)
    temp = variables['O']
    push(x)
    run("_ª0*:O;{O\\+:O}%")
    variables['O'] = temp
    return None


def halve(x):
    if not is_number(x):
        raise InvalidOverloadError(x)
    return simplify(x / 2)


def square(x):
    if not is_number(x):
        raise InvalidOverloadError(x)
    return simplify(x * x)


def cube(x):
    if not is_number(x):
        raise InvalidOverloadError(x)
    return simplify(x * x * x)


def op_flip(x):
    if is_char(x):
        return Char(int(x) ^ 32)
    if is_string(x):
        r = ''
        for i in x:
            r += str(Char(int(Char(i)) ^ 32))
        return r
    if is_number(x):
        return simplify(-x)
    raise InvalidOverloadError(x)


def deg(x):
    if not is_number(x):
        raise InvalidOverloadError(x)
    return simplify(math.degrees(x))


def rad(x):
    if is_number(x):
        return simplify(math.radians(x))
    if is_string(x):
        return Regex(x)
    if is_list(x):
        push(x)
        run("'|*þ")
        return None
    raise InvalidOverloadError(x)


def reciprocal(x):
    if not is_number(x):
        raise InvalidOverloadError(x)
    return simplify(1 / x)


def lower(x):
    if is_char(x):
        return Char(str(x).lower())
    if is_string(x):
        return x.lower()
    raise InvalidOverloadError(x)


def upper(x):
    if is_char(x):
        return Char(str(x).upper())
    if is_string(x):
        return x.upper()
    raise InvalidOverloadError(x)


def is_prime(n):
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


def prime_num(index):
    if not is_number(index):
        raise InvalidOverloadError(index)
    count = 0
    candidate = 2
    while True:
        if is_prime(candidate):
            count += 1
            if count > int(index):
                break
        candidate += 1
    return candidate


def gcd(x, y):
    if not all_number(x, y):
        raise InvalidOverloadError(x, y)
    while y:
        x, y = y, x % y
    return simplify(x)


def lcm(x, y):
    if not all_number(x, y):
        raise InvalidOverloadError(x, y)
    return simplify(x * y / gcd(x, y))


def range1(x):
    if not is_number(x):
        raise InvalidOverloadError(x)
    return list(range(1, int(x) + 1))


def type_equal(x, y):
    if not any_list(x, y):
        return type(x) == type(y)
    if all_list(x, y):
        xl = to_list(x)
        yl = to_list(y)
        if len(xl) != len(yl):
            return False
        for i in range(len(xl)):
            if not type_equal(xl[i], yl[i]):
                return False
        return True
    if is_list(x):
        xl = to_list(x)
        for i in xl:
            if not type_equal(i, y):
                return False
        return True
    else:
        yl = to_list(y)
        for i in yl:
            if not type_equal(i, x):
                return False
        return True


def unique(x):
    if not is_list(x):
        raise InvalidOverloadError(x)
    u = []
    for o in x:
        if not list_contains(u, o):
            u.append(o)
    return u


def connected_unique(x):
    if not is_list(x):
        raise InvalidOverloadError(x)
    u = []
    l = None
    for o in x:
        if l != o:
            u.append(o)
            l = o
    return u


def rand(x):
    if is_number(x):
        if is_float(x):
            return random.random() * x
        if is_int(x):
            if x < 0:
                raise InvalidArgumentError("Argument must be positive.")
            return random.randrange(x)
    if is_list(x):
        random.shuffle(x)
        return x
    raise InvalidOverloadError(x)


def transliterate(x, y, z):
    if not is_list(x):
        raise InvalidOverloadError(x, y, z)
    xl = to_list(x)
    yl = to_list(y)
    zl = to_list(z)
    n = len(zl)
    l = []
    for o in xl:
        try:
            t = find_index(yl, o)
        except ValueError:
            if is_char(o) and is_string(y):
                try:
                    t = y.index(str(o))
                except ValueError:
                    t = -1
            else:
                t = -1
        if t < 0:
            l.append(o)
        elif t < n:
            l.append(zl[t])
        else:
            l.append(zl[n-1])
    return fix_list(l)


def double(x):
    if is_number(x) or is_list(x):
        return simplify(x * 2)
    raise InvalidOverloadError(x)


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

var_defaults = variables.copy()

operators = {
    ' ': attrdict(
        arity=0,
        call=lambda: None
    ),
    '\t': attrdict(
        arity=0,
        call=lambda: None
    ),
    'Þ': attrdict(
        arity=1,
        call=lambda x: eval(x) if is_string(x) and not safe_mode else change_variable_accuracy(x)
    ),
    '~': attrdict(
        arity=1,
        call=op_tilda
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
        arity=1,
        call=lambda x: push(x, x)
    ),
    '#': attrdict(
        arity=2,
        call=lambda x, y: power(x, y) if is_number(x) and is_number(y) else find_index(x, y)
    ),
    '=': attrdict(
        arity=2,
        call=lambda x, y: check_equal(x, y) if check_equal(x, y) is not None else get_value(x, y)
    ),
    '%': attrdict(
        arity=2,
        call=op_percent
    ),
    "$": attrdict(
        arity=1,
        call=op_dollar
    ),
    '&': attrdict(
        arity=2,
        call=op_ampersand
    ),
    '(': attrdict(
        arity=1,
        call=lambda x: dec(x) if is_number(x) or is_char(x) else uncon(x, dir='left')
    ),
    ')': attrdict(
        arity=1,
        call=lambda x: inc(x) if is_number(x) or is_char(x) else uncon(x, dir='right')
    ),
    '*': attrdict(
        arity=2,
        call=lambda x, y: simplify(x * y) if all_number(x, y) else op_asterisk(x, y)
    ),
    '+': attrdict(
        arity=2,
        call=lambda x, y: simplify(x + y) if all_number(x, y) else op_plus(x, y)
    ),
    ',': attrdict(
        arity=1,
        call=op_comma
    ),
    '-': attrdict(
        arity=2,
        call=lambda x, y: simplify(x - y) if all_number(x, y) else op_minus(x, y)
    ),
    '/': attrdict(
        arity=2,
        call=lambda x, y: op_fslash(x, y)
    ),
    '<': attrdict(
        arity=2,
        call=op_lt
    ),
    '>': attrdict(
        arity=2,
        call=op_gt
    ),
    '?': attrdict(
        arity=3,
        call=op_ternary
    ),
    '@': attrdict(
        arity=3,
        call=stack_rotate
    ),
    '\\': attrdict(
        arity=2,
        call=stack_swap
    ),
    '^': attrdict(
        arity=2,
        call=op_caret
    ),
    'a': attrdict(
        arity=1,
        call=lambda x: [x]
    ),
    'b': attrdict(
        arity=2,
        call=base_convert
    ),
    'c': attrdict(
        arity=1,
        call=lambda x: Char(x)
    ),
    'd': attrdict(
        arity=1,
        call=lambda x: float(x)
    ),
    'g': attrdict(
        arity=1,
        call=op_g
    ),
    'h': attrdict(
        arity=1,
        call=op_h
    ),
    'i': attrdict(
        arity=1,
        call=lambda x: int(x)
    ),
    'l': attrdict(
        arity=0,
        call=lambda: sys.stdin.readline()[:-1]
    ),
    'o': attrdict(
        arity=1,
        call=lambda x: print(to_string(x))
    ),
    'p': attrdict(
        arity=1,
        call=lambda x: print(to_string_repr(x))
    ),
    'q': attrdict(
        arity=0,
        call=lambda: sys.stdin.read()[:-1]
    ),
    'r': attrdict(
        arity=0,
        call=read_token
    ),
    's': attrdict(
        arity=1,
        call=lambda x: dump_string(to_list(x))
    ),
    't': attrdict(
        arity=3,
        call=set_item
    ),
    'w': attrdict(
        arity=2,
        call=while_loop
    ),
    'z': attrdict(
        arity=1,
        call=lambda x: abs(x) if is_number(x) else transpose(x)
    ),
    '|': attrdict(
        arity=2,
        call=op_bar
    ),
    '¡': attrdict(
        arity=1,
        call=lambda x: simplify(math.gamma(x+1)) if is_number(x) else cum_sum(x)
    ),
    '½': attrdict(
        arity=1,
        call=halve
    ),
    '²': attrdict(
        arity=1,
        call=square
    ),
    '³': attrdict(
        arity=1,
        call=cube
    ),
    '±': attrdict(
        arity=1,
        call=op_flip
    ),
    '°': attrdict(
        arity=1,
        call=deg
    ),
    'þ': attrdict(
        arity=1,
        call=rad
    ),
    '¹': attrdict(
        arity=1,
        call=reciprocal
    ),
    '¬': attrdict(
        arity=1,
        call=lambda x: simplify(math.floor(x)) if is_number(x) else lower(x)
    ),
    '¯': attrdict(
        arity=1,
        call=lambda x: simplify(math.ceil(x)) if is_number(x) else upper(x)
    ),
    '¶': attrdict(
        arity=2,
        call=pair
    ),
    'µ': attrdict(
        arity=1,
        call=prime_num
    ),
    'Ð': attrdict(
        arity=2,
        call=gcd
    ),
    '´': attrdict(
        arity=1,
        call=range1
    ),
    'æ': attrdict(
        arity=2,
        call=lambda x, y: push(x, x, y, y)
    ),
    'Û': attrdict(
        arity=2,
        call=type_equal
    ),
    '×': attrdict(
        arity=1,
        call=lambda x: quick_fold(x, '*')
    ),
    'ª': attrdict(
        arity=1,
        call=lambda x: quick_fold(x, '+')
    ),
    '¿': attrdict(
        arity=1,
        call=lambda x: x == 0 or x == 1 if is_number(x) else push(x, x[::-1])
    ),
    'Å': attrdict(
        arity=1,
        call=unique
    ),
    'Ä': attrdict(
        arity=1,
        call=connected_unique
    ),
    '¥': attrdict(
        arity=1,
        call=lambda x: x[::-1]
    ),
    'Ø': attrdict(
        arity=2,
        call=lambda x, y: x.format(*(y if is_list(y) else [y])) if is_string(x) else y.format(*(x if is_list(x) else [x]))
    ),
    '£': attrdict(
        arity=1,
        call=rand
    ),
    'Ë': attrdict(
        arity=3,
        call=transliterate
    ),
    '«': attrdict(
        arity=2,
        call=lambda x, y: x if compare(x, y) > 0 else y
    ),
    '»': attrdict(
        arity=2,
        call=lambda x, y: x if compare(x, y) < 0 else y
    ),
    '¸': attrdict(
        arity=2,
        call=lcm
    ),
    '¦': attrdict(
        arity=1,
        call=double
    ),
    'Ã': attrdict(
        arity=0,
        call=lambda: run(sys.stdin.readline()[:-1])
    ),
    'Â': attrdict(
        arity=0,
        call=lambda: run(sys.stdin.read()[:-1])
    )
}


if len(sys.argv) == 1:
    print("Not enough arguments.\nFor help use the -help flag.")
else:
    index = 1
    while index < len(sys.argv):
        if sys.argv[index] in ("-help", "-h", "-?"):
            print("Convex Help")
            print()
            print("Usage: convex [-flag] <program>")
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
            print("-shell: starts an interactive Convex independent shell.")
            print("-s: starts an interactive Convex independent shell.")
            print("-repl: starts and interactive Convex REPL shell.")
            print("-r: starts and interactive Convex REPL shell.")
            print("-safe: disables file IO, Python eval, and operators with internet access.")
            print("-sm: disables file IO, Python eval, and operators with internet access.")
            print("-debug: prints the stack in list form after program execution.")
            print("-d: prints the stack in list form after program execution.")
            index += 1
        elif sys.argv[index] in ("-accuracy", "-a"):
            if index + 1 == len(sys.argv):
                print("Not enough arguments.\nFor help use the -help flag.")
                break
            else:
                if 'k' in sys.argv[index + 1] or 'm' in sys.argv[index + 1]:
                    mpmath.mp.dps = int(sys.argv[index + 1][:len(sys.argv[index + 1])-1]) * {'k': 1000, 'm': 1000000}[sys.argv[index + 1][len(sys.argv[index + 1])-1]]
                else:
                    mpmath.mp.dps = int(sys.argv[index + 1])
                index += 2
        elif sys.argv[index] in ("-file", "-f"):
            if index + 1 == len(sys.argv):
                print("Not enough arguments.\nFor help use the -help flag.")
                break
            else:
                file = open(sys.argv[index + 1])
                run(file.read(), True)
                if debug_mode:
                    print("\nStack: ", to_string_repr(stack))
                index += 2
        elif sys.argv[index] in ("-code", "-c"):
            if index + 1 == len(sys.argv):
                print("Not enough arguments.\nFor help use the -help flag.")
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
                variables = var_defaults.copy()
                try:
                    run(input(">>> "), True)
                    if debug_mode:
                        print("\nStack: ", to_string_repr(stack))
                except InvalidOperatorError as err:
                    print("Invalid operator:", err)
                except InvalidOverloadError as err:
                    print(err)
        elif sys.argv[index] in ("-repl", "-r"):
            while True:
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
        elif sys.argv[index] in ("-version", "-v"):
            print("Convex Version: " + CONVEX_VERSION)
            index += 1
        else:
            print("Invalid flag: " + sys.argv[index])
            print("For help use the -help flag.")
            break
