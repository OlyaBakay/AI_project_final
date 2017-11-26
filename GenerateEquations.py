import random
from sympy.solvers import solve
from sympy import Symbol
import re

def generate_equations(amount):
    with open('equations_template') as file:
        templates = file.readlines()
    for i in range(amount):
        generate_equation(random.choice(templates).rstrip())

def generate_equation(template):
    print(template)
    file = open("text.txt", "a")
    characters = ["+", "-", "*", "/"]
    count = template.count("{number}")
    count += template.count("{character}")
    allowed_numbers = list(range(-99, 100))
    allowed_numbers.remove(0)
    equation = template
    for number in range(count):
        random_number = random.choice(allowed_numbers)
        random_character = characters[random.randint(0, len(characters)-1)]
        equation = equation.replace("{character}", random_character, 1)
        equation = equation.replace("{number}", str(random_number), 1)
    equation = equation.replace("- -", "+ ")
    equation = equation.replace("+ -", "- ")

    file.write(equation)
    file.write("\n")
    file.write(solveEq(equation))
    file.write("\n")
    file.close()
    return equation

def solveEq(eq):
    eq = re.sub(r'(\d+)x', r'\g<1> * x', eq)
    left, right = eq.split('=')
    eq = left + "-(" + right + ")"
    result = round(solve(eq, 'x')[0], 2)
    return "x = " + str(result)

generate_equations(50)