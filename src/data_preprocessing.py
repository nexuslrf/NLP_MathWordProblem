import os
from equation_tree import *
from re import sub
import json


def is_same_template(exp1, exp2):
    def exp_to_tree(e, unk='x'):
        e = e.replace(unk, str(UNKNOWN))
        return TemplateTree.build_with_exp(e)
    tree1 = exp_to_tree(exp1)
    tree2 = exp_to_tree(exp2)
    return tree1.equals(tree2) or tree1.reverse().equals(tree2)


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


def clean_text(t):
    text = t[:]
    text = str(text)
    text = text.lower()

    text = sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
    text = sub(r"what's", "what is ", text)
    text = sub(r"\'s", " ", text)
    text = sub(r"\'ve", " have ", text)
    text = sub(r"can't", "cannot ", text)
    text = sub(r"n't", " not ", text)
    text = sub(r"i'm", "i am ", text)
    text = sub(r"\'re", " are ", text)
    text = sub(r"\'d", " would ", text)
    text = sub(r"\'ll", " will ", text)
    text = sub(r",", " ", text)
    text = sub(r"\.", " ", text)
    text = sub(r"!", " ! ", text)
    text = sub(r"\/", " ", text)
    text = sub(r"\^", " ^ ", text)
    text = sub(r"\n", " + ", text)
    text = sub(r"\+", " ", text)
    text = sub(r"\-", " - ", text)
    text = sub(r"\=", " = ", text)
    text = sub(r"'", " ", text)
    text = sub(r"(\d+)(k)", r"\g<1>000", text)
    text = sub(r":", " : ", text)
    text = sub(r" e g ", " eg ", text)
    text = sub(r" b g ", " bg ", text)
    text = sub(r" u s ", " american ", text)
    text = sub(r"\0s", "0", text)
    text = sub(r" 9 11 ", "911", text)
    text = sub(r"e - mail", "email", text)
    text = sub(r"j k", "jk", text)
    text = sub(r"\s{2,}", " ", text)
    return text


def output_template_label(tuples):
    with open("template_labels.csv", 'w') as f1:
        with open("template_id.csv", 'w') as f2:
            f2.write('tid, template, count\n')
            f1.write('qid, tid\n')
            for i in range(len(tuples)):
                f2.write(str(i) + ', ' +
                         str(tuples[i][0][0][1]).replace(str(UNKNOWN), 'x') +
                         ', ' + str(len(tuples[i][0])) + '\n')
                # ignore templates that are too unusual
                if len(tuples[i][0]) < 3:
                    continue
                for tp in tuples[i][0]:
                    qid = str(tp[0])
                    tid = str(i)
                    f1.write(qid + ', ' + tid + '\n')





if __name__ == "__main__":
    # TemplateTree.build_with_exp('(999/4)-3=5/4').print_tree()
    templates_tuples = []  # elements:tuple(raw_text_list, template_tree)
    with open(os.path.abspath('../data/eval_cleaned.json'), 'r', encoding='UTF-8') as f:
        raw_data = f.read()

    json_data = json.loads(raw_data)
    print(len(json_data))

    single_equ = 0
    qid = 0

    for quest in json_data:
        equation = str(quest["equations"])
        text = str(quest["text"])
        text = clean_text(text)
        if len(text.split()) < 3:
            continue
        qid += 1
        if str(equation).count("\r\n") == 1:
            equation, exp = standardize(equation)
            try:
                # print(equation)
                exp = exp.replace('x', str(UNKNOWN))
                exp_tree = TemplateTree.build_with_exp(exp)
                for templates_tuple in templates_tuples:
                    if exp_tree.equals(templates_tuple[1]) or exp_tree.equals(templates_tuple[1].reverse()):
                        templates_tuple[0].append((qid, exp))
                        break
                else:
                    templates_tuples.append(([(qid, exp)], exp_tree))
            except NotImplementedError:
                # print(exp)
                pass

    print(templates_tuples)
    output_template_label(templates_tuples)
    # with open("template_info.csv", 'w') as f:
    #     for templates_tuple in templates_tuples:
    #         f.write(str(len(templates_tuple[0])) + '\n')


