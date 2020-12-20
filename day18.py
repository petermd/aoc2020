import tokenize
import io

def read(file):
    prog = []
    with open(file, "rb") as f:
        for line in f.readlines():
            yield [token for token in tokenize.tokenize(io.BytesIO(line).readline) if token.type in [tokenize.NUMBER, tokenize.OP]]

class Evaluator:

    def __init__(self, prog):
        self.prog = prog

    def read_value(self):
        next = self.prog.pop(0)
        if next.type == tokenize.NUMBER:
            return int(next.string)
        elif next.type == tokenize.OP and next.string == '(':
            return self.eval()

    def eval(self):
        expr = []
        expr.append(("push",self.read_value()))
        while len(self.prog) > 0:

            op = self.next()

            if op.string == ')':
                break

            expr.append(("push", self.read_value()))

            if op.string == '*':
                expr.append(("*", 2))
            elif op.string == '+':
                expr.append(("+", 2))

        return self.exec(expr)

    def next(self):
        return self.prog.pop(0)

    def peek(self):
        return self.prog[0] if len(self.prog) > 0 else 1

    def exec(self, expr):
        stack = []
        for e in expr:
            if e[0] == 'push':
                stack.append(e[1])
            elif e[0] == '*':
                stack.append(stack.pop() * stack.pop())
            elif e[0] == '+':
                stack.append(stack.pop() + stack.pop())
        return stack[0]


class PrecedenceEvaluator(Evaluator):

    def eval(self):
        expr = []
        defer = []
        expr.append(("push",self.read_value()))
        while len(self.prog) > 0:

            op = self.next()

            if op.string == ')':
                break

            expr.append(("push", self.read_value()))

            if op.string == '*':
                defer.append(("*", 2))
            elif op.string == '+':
                expr.append(("+", 2))

        expr.extend(defer)
        return self.exec(expr)

def partone():
    return sum(Evaluator(prog).eval() for prog in read("day18.dat"))

def parttwo():
    return sum(PrecedenceEvaluator(prog).eval() for prog in read("day18.dat"))

print(partone())
print(parttwo())
