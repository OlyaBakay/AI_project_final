import random
import re
from sympy.solvers import solve
import numpy as np


def generate_equations(amount):
    """
    generates certain amount of equations from chosen template
    """

    with open('equations_template') as f:
        # templates = f.readlines()
        template = f.readlines()[0].rstrip()

    eq_file = open("./data/equations.txt", "w")
    an_file = open("./data/answers.txt", "w")
    binary_label = open("./data/binary_labels.txt", "w")
    for i in range(amount):
        # create_equation(random.choice(templates).rstrip(), eq_file, an_file, binary_label)
        create_equation(template, eq_file, an_file, binary_label)
    eq_file, an_file, binary_label.close()


def create_equation(template, eq_file, an_file, binary_label_file):
    # characters = ["+", "-", "*", "/"]
    characters = ["+", "-"]
    count = template.count("{number}") + template.count("{character}")
    allowed_numbers = list(range(-99, 100))
    allowed_numbers.remove(0)

    for number in range(count):
        random_number = str(random.choice(allowed_numbers))
        random_character = random.choice(characters)

        template = template.replace("{number}", random_number, 1).replace("{character}", random_character, 1)
        template = template.replace("- -", "+ ").replace("+ -", "- ")

    answer = solve_eq(template)
    eq_file.write(template.split('=')[0] + "\n")
    an_file.write(answer + "_")
    check = np.random.choice([0, 1], p=[0.5, 0.5])
    if check == 1:
        an_file.write(answer + "\n")
    else:
        an_file.write(str(random.randint(-100, 100)) + "\n")
    binary_label_file.write(str(check) + "\n")


def solve_eq(eq):
    eq = re.sub(r'(\d+)x', r'\g<1> * x', eq)
    left, right = eq.split('=')
    eq = left + "-(" + right + ")"
    result = round(solve(eq, 'x')[0], 2)
    return str(result)
