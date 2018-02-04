import random
from sympy.solvers import solve
import re
import numpy as np


def generate_equations(amount):
    """
    generate certain amount of equations
    """

    with open('equations_template') as file:
        templates = file.readlines()
    file = open("./data/train.txt", "w")
    file_label = open("./data/text_label.txt", "w")
    file_label_binary = open("./data/binary_labels.txt", "w")
    for i in range(amount):
        # create_equation(random.choice(templates).rstrip(), file, file_label, file_label_binary)
        create_equation(templates[2].rstrip(), file, file_label, file_label_binary)
    file, file_label, file_label_binary.close()


def create_equation(template, file, file_label, file_label_binary):

    # characters = ["+", "-", "*", "/"]
    characters = ["+", "-"]
    count = template.count("{number}")
    count += template.count("{character}")
    allowed_numbers = list(range(-99, 100))
    allowed_numbers.remove(0)
    equation = template
    for number in range(count):
        random_number = random.choice(allowed_numbers)
        random_character = random.choice(characters)
        random_number = str(random_number)
        equation = equation.replace("{number}", random_number, 1)
        equation = equation.replace("{character}", random_character, 1)
    equation = equation.replace("- -", "+ ")
    equation = equation.replace("+ -", "- ")

    file.write(equation.split('=')[0])
    file.write("\n")
    check = np.random.choice([0, 1], p=[0.5, 0.5])
    if check == 1: file_label.write(solve_eq(equation))
    else: file_label.write(str(random.randint(-100, 100)))
    file_label.write("\n")
    file_label_binary.write(str(check))
    file_label_binary.write("\n")
    return equation


def solve_eq(eq):
    eq = re.sub(r'(\d+)x', r'\g<1> * x', eq)
    left, right = eq.split('=')
    eq = left + "-(" + right + ")"
    result = round(solve(eq, 'x')[0], 2)
    return str(result)
