from util import *
import numpy as np

UNKNOWN = 999999
CONSTANT = 0


class EquationTree:
    def __init__(self, operator=None, left=None, right=None):
        # elements of the branches can be numbers or trees
        self.left = left
        self.right = right
        self.operator = operator

    @classmethod
    def build_with_exp(cls, ex):
        exp = ex[:]
        # deal with ()
        level = 0
        levels = []
        for i in range(len(exp)):
            # in reverse order
            if exp[i] == '(':
                level += 1
            if exp[i] == ')':
                level -= 1
            levels.append(level)
        if len(exp) > 1 and np.min(levels[:-1]) > 0:
            if exp[0] == '(' and exp[-1] == ')':
                levels = (np.array(levels) - 1).tolist()
                exp = exp[1:-1]
            else:
                print(exp)
                raise ArithmeticError
        # deal with pure number
        try:
            number = float(exp)
            return number
        except:
            pass
        # deal with '='
        index = -1
        op = None
        for i in range(len(exp) - 1, -1, -1):
            if exp[i] == '=':
                index = i
                op = Operators.equal
        if index != -1:
            # expression
            t_left = cls.build_with_exp(exp[0: index])
            t_right = cls.build_with_exp(exp[index + 1:])
            return cls(op, t_left, t_right)

        # find the rightest + or -
        index = -1
        op = None
        for i in range(len(exp)-1, -1, -1):
            if (levels[i] == 0) and (exp[i] == '+' or exp[i] == '-'):
                index = i
                if exp[i] == '+':
                    op = Operators.plus
                elif exp[i] == '-':
                    op = Operators.minus
                else:
                    assert 0
        if index != -1:
            # expression
            t_left = cls.build_with_exp(exp[0: index])
            t_right = cls.build_with_exp(exp[index+1:])
            return cls(op, t_left, t_right)

        # find * and /
        index = -1
        op = None
        for i in range(len(exp) - 1, -1, -1):
            if (levels[i] == 0) and (exp[i] == '*' or exp[i] == '/'):
                index = i
                if exp[i] == '*':
                    op = Operators.times
                elif exp[i] == '/':
                    op = Operators.divide
                else:
                    assert 0
                break
        if index != -1:
            # expression
            t_left = cls.build_with_exp(exp[0: index])
            t_right = cls.build_with_exp(exp[index + 1:])
            return cls(op, t_left, t_right)
        assert 0

    def print_tree(self, indent=0):
        oper_dict = dict({0: '=', 1: '+', 2: '-', 3: '*', 4: '/'})
        indent_str = 2 * indent * ' '

        # print left
        print(indent_str, "[left(")
        if type(self.left) == type(self):
            self.left.print_tree(indent+1)
        else:
            print(indent_str + '  ', self.left)
        print(indent_str, ")")

        # print operator
        print(indent_str, 'op(', oper_dict[self.operator.value], ')')

        # print right
        print(indent_str, "right(")
        if type(self.right) == type(self):
            self.right.print_tree(indent + 1)
        else:
            print(indent_str + '  ', self.right)
        print(indent_str, ")]")

    def equals(self, tree2):
        result = True
        if type(self) != type(tree2):
            result = False
        if type(self.left) == type(self):
            result = result and self.left.equals(tree2.left)
        else:
            result = result and (self.left == tree2.left)
        if type(self.right) == type(self):
            result = result and self.right.equals(tree2.right)
        else:
            result = result and (self.right == tree2.right)
        result = result and (self.operator == tree2.operator)
        if self.operator == Operators.equal or self.operator == Operators.plus or self.operator == Operators.times:
            result2 = True
            if type(self) != type(tree2):
                result2 = False
            if type(self.left) == type(self):
                result2 = result2 and self.left.equals(tree2.right)
            else:
                result2 = result2 and (self.left == tree2.right)
            if type(self.right) == type(self):
                result2 = result2 and self.right.equals(tree2.left)
            else:
                result2 = result2 and (self.right == tree2.left)
            result2 = result2 and (self.operator == tree2.operator)
            return result or result2

        return result

    def calculate(self):
        if type(self.left) == type(self):
            left_val = self.left.calculate()
        else:
            left_val = self.left
        if type(self.right) == type(self):
            right_val = self.right.calculate()
        else:
            right_val = self.right
        if self.operator == Operators.plus:
            return left_val + right_val
        elif self.operator == Operators.minus:
            return left_val - right_val
        elif self.operator == Operators.times:
            return left_val * right_val
        elif self.operator == Operators.divide:
            return left_val / right_val
        assert 0

    def reverse(self):
        return EquationTree(self.operator, self.right, self.left)


class TemplateTree(EquationTree):
    @classmethod
    def build_with_exp(cls, ex):
        exp = ex[:]
        # deal with ()
        level = 0
        levels = []
        for i in range(len(exp)):
            # in reverse order
            if exp[i] == '(':
                level += 1
            if exp[i] == ')':
                level -= 1
            levels.append(level)
        if len(ex) > 1 and np.min(levels[:-1]) > 0:
            if exp[0] == '(' and exp[-1] == ')':
                exp = exp[1:-1]
                levels = (np.array(levels)-1).tolist()
            else:
                print(exp)
                raise ArithmeticError
        # replace all '-'s
        exp = exp.replace('*-', '*')
        exp = exp.replace('/-', '/')
        if exp[0] == '-':
            exp = exp[1:]
        # deal with pure number
        try:
            number = float(exp)
            if number != UNKNOWN:
                number = CONSTANT
            return number
        except:
            pass
        # deal with '='
        index = -1
        op = None
        for i in range(len(exp) - 1, -1, -1):
            if exp[i] == '=':
                index = i
                op = Operators.equal
        if index != -1:
            # expression
            t_left = cls.build_with_exp(exp[0: index])
            t_right = cls.build_with_exp(exp[index + 1:])
            return cls(op, t_left, t_right)

        # find the rightest + or -
        index = -1
        op = None
        for i in range(len(exp) - 1, -1, -1):
            if (levels[i] == 0) and (exp[i] == '+' or exp[i] == '-'):
                index = i
                if exp[i] == '+':
                    op = Operators.plus
                elif exp[i] == '-':
                    op = Operators.minus
                else:
                    assert 0
        if index != -1:
            # expression
            t_left = cls.build_with_exp(exp[0: index])
            t_right = cls.build_with_exp(exp[index + 1:])
            return cls(op, t_left, t_right)

        # find * and /
        index = -1
        op = None
        for i in range(len(exp) - 1, -1, -1):
            if (levels[i] == 0) and (exp[i] == '*' or exp[i] == '/'):
                index = i
                if exp[i] == '*':
                    op = Operators.times
                elif exp[i] == '/':
                    op = Operators.divide
                else:
                    assert 0
                break
        if index != -1:
            # expression
            t_left = cls.build_with_exp(exp[0: index])
            t_right = cls.build_with_exp(exp[index + 1:])
            return cls(op, t_left, t_right)
        raise NotImplementedError

    def reverse(self):
        return TemplateTree(self.operator, self.right, self.left)


if __name__ == "__main__":
    # left = EquationTree(operator=Operators.plus, left=1, right=3)
    # tree = EquationTree(operator=Operators.times, left=left, right=4)
    # tree.print_tree()

    tree2 = TemplateTree.build_with_exp("2*2=999")
    tree2.print_tree()
    tree2.reverse().print_tree()

    tree3 = TemplateTree.build_with_exp("999=2*2")

    print(tree2.reverse().equals(tree3))

    # print(tree2.calculate())
    #
    # print(tree.equals(tree2))






