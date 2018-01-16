from GenerateData import text_to_image
from GenerateEquations import generate_equations


def gen_pics_from_equation():
    # generates pics1 of equations
    text_to_image('./data/train.txt', "./pics/data", "./data/binary_labels.txt", "./pics/binary_labels.json")

    # generates pics1 of the answers
    text_to_image('./data/text_label.txt', "./pics/labels")


if __name__ == '__main__':
    generate_equations(5000)
    gen_pics_from_equation()
