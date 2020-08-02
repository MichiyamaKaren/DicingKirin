from random import randint


class Expression:
    def __init__(self, exp):
        self.exp = exp
        self.i = 0

        self.config()

    def config(self):
        self.EOF = '\0'
        self.NUMBERS = '0123456789'
        self.OPERATORS = '+-*/Dd'
        self.NULLCHAR = ' \t\n'

        self.priority = {'+': 0, '-': 0, '*': 1, '/': 1, 'D': 2, 'd': 2, self.EOF: -1}
        self.calculate = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            'D': lambda n, m: sum([randint(1, m) for _ in range(n)]),
            'd': lambda n, m: sum([randint(1, m) for _ in range(n)])
        }

    def get(self):
        if self.i >= len(self.exp):
            return self.EOF
        while self.exp[self.i] in self.NULLCHAR:
            self.i += 1
        self.i += 1
        return self.exp[self.i - 1]

    def stepback(self):
        self.i -= 1
        while self.exp[self.i] in self.NULLCHAR:
            self.i -= 1

    def get_number(self, init_number=0):
        num = init_number
        while True:
            c = self.get()
            if c == self.EOF:
                return num
            elif c in self.NUMBERS:
                num = 10 * num + int(c)
            else:
                self.stepback()
                return num

    def reduce(self, current_op, num_stack, op_stack):
        while op_stack and self.priority[current_op] <= self.priority[op_stack[-1]]:
            op = op_stack.pop()
            y, x = num_stack.pop(), num_stack.pop()
            num_stack.append(self.calculate[op](x, y))
        op_stack.append(current_op)

    def parse(self):
        num_stack = []
        op_stack = []

        while True:
            current = self.get()
            if current in self.NUMBERS:
                num_stack.append(self.get_number(int(current)))
            elif current in self.OPERATORS:
                self.reduce(current, num_stack, op_stack)
            elif current == self.EOF:
                self.reduce(current, num_stack, op_stack)
                if len(op_stack) > 1 or len(num_stack) > 1:
                    raise IllegalExpressionError('expression not finished')
                break
            else:
                raise IllegalExpressionError('illegal symbol')

        return num_stack[-1]


class IllegalExpressionError(Exception):
    pass
