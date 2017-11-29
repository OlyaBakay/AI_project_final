from GenerateData import text_image_trial
from GenerateEquations import generate_equations


def gen_pics_from_equation():
    text_image_trial('./data/train.txt', "./pics/data")
    text_image_trial('./data/text_label.txt', "./pics/labels")


def gen_equations(number):
    generate_equations(number)

if __name__ == '__main__':
    gen_equations(500)
    gen_pics_from_equation()
