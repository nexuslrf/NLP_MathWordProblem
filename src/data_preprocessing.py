import os
from equation_tree import *

UNKNOWN = 999
CONSTANT = 0


class TemplateTree(EquationTree):
    @classmethod
    def build_with_exp(cls, exp):
        if exp[0] == '(' and exp[-1] == ')':
            exp = exp[1:-1]
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
        assert 0


def is_same_template(exp1, exp2):
    def exp_to_tree(exp, unk='x'):
        exp = exp.replace(unk, str(UNKNOWN))
        return TemplateTree.build_with_exp(exp)
    tree1 = exp_to_tree(exp1)
    tree2 = exp_to_tree(exp2)
    return tree1.equals(tree2)


if __name__ == "__main__":
    print(is_same_template("x=2+3", "x=9+2"))
    # with open(os.path.abspath('../data/eval_cleaned.json'), 'r', encoding='UTF-8') as f:
    #     raw_data = f.read()
    #
    # json_data = eval(raw_data)
    # print(len(json_data))
    #
    # single_equ = 0
    #
    # for quest in json_data:
    #     equation = str(quest["equations"])
    #     equation.replace(' ', '')
    #     if str(equation).count("\r\n") == 1:
    #         single_equ += 1
    #
    #         print(equation)
    #
    # print(single_equ)
