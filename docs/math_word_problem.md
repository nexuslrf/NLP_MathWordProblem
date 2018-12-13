# Solving Math Word Problems Using Deep Neural Feature Categorization and Word Mapping



## Abstract

This paper presents a model to enable machines to automatically solve math word problems. Instead of using end-to-end learning strategies, we divide the problem into two parts and solve each part using recurrent neural networks. With a given text which describes the problem, we first find a template in our database that best fit the problem. Then, we align the numbers in the given problem with the variables or constants in the template.

## I. Introduction

Solving math word problems has always been a challenge in the field of natural language problems. In order to solve a problem correctly, a system is required to have the capability of dig out the logic behind the natural language, ignore the useless or deceptive information and finally generate the correct equations.

A considerable number of researches have been conducted on this problem. Huang et al. 2017[2] improved the template retrieval model to search the template that best fit the given problem. Wang et al. 2017[3] proposed RNN-based model to solve math word problems, which was the time deep neural networks were used in this area. However, these models still have their limitations. Traditional template retrieval models involves human defined features to evaluate the similarity between two math word problems. Features including the frequency of words might be irrelevant to the similarity and misleading. For instance, two problems may have the same context, with a lot of same words occur in both problems, while the goals of them are totally different. Under this circumstance, the system might mistakenly choose the wrong template.  End-to-end models such as [3] are also imperfect. The model presented in [3] transfer a math word problem to traditional classification problems by sequentially selecting operators or variables and building them up to generate an equation. However, the model fails to deal with mathematically equivalent equations which are differently written. Therefore, the model will be difficult to train as the equations in datasets are not written in the same form.

We discover that in elementary schools, kids are first taught to do basic calculations such as adding or subtracting. Then, several very classic problems are introduced to the kids and the kids will learn to first map the problem they are confronted to those they have already familiar with, and then use the numbers provided in the new problem to do the calculation. Inspired by this, we design a two-step neural network model. Firstly, we trained a neural network which accepts the original text as input and outputs the template that best fits the input problem. Afterwards, the numbers in the new problem go through another neural network that decides the right place they should go in the template equation. In this way, artificial selections of features will be avoided and problems that requires two or more equations can also be solved.





## Reference

[1] Bobrow, D.G., 1964. Natural language input for a computer problem solving system.

[2] Huang, D., Shi, S., Lin, C.Y. and Yin, J., 2017. Learning fine-grained expressions to solve math word problems. In *Proceedings of the 2017 Conference on Empirical Methods in Natural Language Processing* (pp. 805-814).

[3] Wang, Y., Liu, X. and Shi, S., 2017. Deep neural solver for math word problems. In *Proceedings of the 2017 Conference on Empirical Methods in Natural Language Processing* (pp. 845-854).

