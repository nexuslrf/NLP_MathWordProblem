import os
from equation_tree import *


def is_same_template(exp1, exp2):
    def exp_to_tree(e, unk='x'):
        e = e.replace(unk, str(UNKNOWN))
        return TemplateTree.build_with_exp(e)
    tree1 = exp_to_tree(exp1)
    tree2 = exp_to_tree(exp2)
    return tree1.equals(tree2)


def standardize(eq):
    equation = eq[:]
    equation = equation.replace(' ', '')
    unk = equation[equation.find('unkn:') + len('unkn:')]
    exp = equation[equation.find('equ:') + len('equ:'):]
    exp = exp.replace(unk, 'x')
    left = 0
    # add '*' before '('
    while exp.find('(', left) != -1:
        left = exp.find('(', left)
        if left > 0 and (exp[left - 1].isdigit() or exp[left - 1] == 'x'):
            exp = exp[:left] + '*' + exp[left:]
            left += 1
        left += 1
    return equation, exp


if __name__ == "__main__":
    # TemplateTree.build_with_exp('(999/4)-3=5/4').print_tree()
    templates_tuples = []  # elements:tuple(raw_text_list, template_tree)
    with open(os.path.abspath('../data/eval_cleaned.json'), 'r', encoding='UTF-8') as f:
        raw_data = f.read()

    json_data = eval(raw_data)
    print(len(json_data))

    single_equ = 0

    for quest in json_data:
        equation = str(quest["equations"])
        text = str(quest["text"])
        if str(equation).count("\r\n") == 1:
            equation, exp = standardize(equation)
            try:
                # print(equation)
                exp = exp.replace('x', str(UNKNOWN))
                exp_tree = TemplateTree.build_with_exp(exp)
                for templates_tuple in templates_tuples:
                    if exp_tree.equals(templates_tuple[1]) or exp_tree.equals(templates_tuple[1].reverse()):
                        templates_tuple[0].append((text, exp))
                        break
                else:
                    templates_tuples.append(([(text, exp)], exp_tree))
            except NotImplementedError:
                # print(exp)
                pass

    print(templates_tuples)
    with open("template_info.csv", 'w') as f:
        for templates_tuple in templates_tuples:
            f.write(str(len(templates_tuple[0])) + '\n')
            if len(templates_tuple[0]) == 448:
                templates_tuple[1].print_tree()
