from GenerateData import text_to_image
from GenerateEquations import generate_equations


def gen_pics_from_equation():
    # generates pics of the equations
    text_to_image('./data/train.txt', "./pics/data", "./pics/info.csv")

    # generates pics of the answers
    text_to_image('./data/text_label.txt', "./pics/labels")


if __name__ == '__main__':
    generate_equations(10000)
    gen_pics_from_equation()
