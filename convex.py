import ast, cmath, copy, fractions, functools, itertools, locale, math, operator, parser, random, re, sympy, sys, time
# import dictionary, numpy

stack = []


"""
============
Type Classes
============
"""


class Char(object):
    def __init__(self, character):
        if type(character) == Char:
            self.char = character.to_string()
        else:
            self.char = character[1]

    def to_string(self):
        return self.char


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
    return is_string(obj) and obj[0] == '{'


def push(x):
    if x is not None:
        stack.append(x)


def pop():
    return stack.pop()


def peek():
    return stack[len(stack)-1]


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
            else:
                line_stack.append(line[index])
                index += 1
        result.append(line_stack)
        # print(result)
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
        if len(code_stack[index]) == 1:
            if re.match("[A-Z¢è]", code_stack[index]):
                push_temp_stack(variables[code_stack[index]])
                index += 1
            else:
                push_temp_stack(run_op_temp_stack(code_stack[index]))
                index += 1
        else:
            if code_stack[index][0] == '"':
                push_temp_stack(exec(code_stack[index]))
            elif code_stack[index][0] == '\'':
                push_temp_stack(Char(code_stack[index]))
            elif code_stack[index][0] == '[':
                push_temp_stack(run_temp_stack(code_stack[index][1:len(code_stack[index]) - 1]))
            index += 1
    return temp_stack


def run(code):
    code_stack = split_code(code)
    current_line = 0
    index = 0
    while index < len(code_stack[current_line]):
        if len(code_stack[current_line][index]) == 1:
            if re.match("[A-Z¢è]", code_stack[current_line][index]):
                push(variables[code_stack[current_line][index]])
                index += 1
            else:
                push(run_op(code_stack[current_line][index]))
                index += 1
        else:
            if code_stack[current_line][index][0] == '"':
                push(exec(code_stack[current_line][index]))
            elif code_stack[current_line][index][0] == '\'':
                push(Char(code_stack[current_line][index]))
            elif code_stack[current_line][index][0] == '[':
                push(run_temp_stack(code_stack[current_line][index][1:len(code_stack[current_line][index])-1]))
            index += 1


"""
==================
Operator Functions
==================
"""


def base_convert(list_a, base):
    if is_number(list_a) and is_list(base):
        return base_convert(base, list_a)


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
    'P': math.pi,
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
    '¢': (1 + 5 ** 0.5) / 2,
    'è': math.e
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
    )
}


run('[][A B[C]]')
print(stack)
