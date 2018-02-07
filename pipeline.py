from GenerateData import read_eq_data, read_an_data
from GenerateEquations import generate_equations


def gen_pics_from_equation():
    # generates pics of the equations
    read_eq_data('./data/equations.txt', "./data/pics/data", "./data/binary_labels.txt", "./data/info.csv")
    read_an_data('./data/answers.txt', "./data/pics/labels")


if __name__ == '__main__':
    generate_equations(10000)
    gen_pics_from_equation()
