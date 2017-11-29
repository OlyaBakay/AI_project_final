import random
from sympy.solvers import solve
import re


def generate_equations(amount):
    with open('equations_template') as file:
        templates = file.readlines()
    file = open("./data/train.txt", "w")
    file_label = open("./data/text_label.txt", "w")
    for i in range(amount):
    #     generate_equation(random.choice(templates).rstrip())
        generate_equation(templates[2].rstrip(), file, file_label)
    file.close()
    file_label.close()


def generate_equation(template, file, file_label):

    characters = ["+", "-", "*", "/"]
    count = template.count("{number}")
    count += template.count("{character}")
    allowed_numbers = list(range(-99, 100))
    allowed_numbers.remove(0)
    equation = template
    for number in range(count):
        random_number = random.choice(allowed_numbers)
        random_character = random.choice(characters)
        equation = equation.replace("{character}", random_character, 1)
        equation = equation.replace("{number}", str(random_number), 1)
    equation = equation.replace("- -", "+ ")
    equation = equation.replace("+ -", "- ")


    file.write(equation.split('=')[0])
    file.write("\n")
    file_label.write(solveEq(equation))
    file_label.write("\n")

    return equation


def solveEq(eq):
    eq = re.sub(r'(\d+)x', r'\g<1> * x', eq)
    left, right = eq.split('=')
    eq = left + "-(" + right + ")"
    result = round(solve(eq, 'x')[0], 2)
    return str(result)


