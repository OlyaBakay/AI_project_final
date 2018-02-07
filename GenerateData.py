import cv2
import numpy as np
import pandas as pd
import os


def remove_files(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


def read_eq_data(source_path, final_path, source_label_path, csv_path):
    remove_files(final_path)

    with open(source_path) as f:
        equations = [l.rstrip() for l in f.readlines()]

    with open(source_label_path) as text_file:
        binary_labels = [l.rstrip() for l in text_file.readlines()]
    img_creator_eq(equations, final_path, binary_labels, csv_path)


def img_creator_eq(equations, eq_path, labels, lab_path):
    counter = 0
    labels_list = []
    for unicode_text in equations:
        photo = np.zeros(shape=(28, 165))
        photo.fill(250)
        parts = unicode_text.split(" ")

        for i, p in enumerate(parts):
            if "x" in p:
                parts[i] = parts[i].replace('x', "")
                parts.insert(i+1, "x")
                break
        parts = "".join(parts)
        cv2.putText(photo, parts, (0, 24), cv2.FONT_ITALIC, 1, 0, 2)
        name = eq_path + "/eq_{}.jpeg".format(counter)
        cv2.imwrite(name, photo)
        labels_list.append(["eq_{}.jpeg".format(counter), unicode_text, int(labels[counter]), ])
        counter += 1
    df = pd.DataFrame(labels_list, columns=['EquationNumber', 'Equation', 'AnswerIsCorrect'])
    df.to_csv(lab_path)


def read_an_data(source_path, final_path):
    remove_files(final_path)

    with open(source_path) as text_file:
        answers, cor_ans = [], []
        for l in text_file.readlines():
            answers.append(l.rstrip().split('_')[1])
            cor_ans.append(l.rstrip().split('_')[0])
    img_creator_ans(answers, cor_ans, final_path)


def img_creator_ans(answers, correct_ans, eq_path):
    df = pd.read_csv('./data/info.csv',  index_col=0)
    df['Answer'] = answers
    df['CorrectAnswer'] = correct_ans
    df.to_csv('./data/info.csv')
    counter = 0
    for unicode_text in answers:
        photo = np.zeros(shape=(28, 165))
        photo.fill(250)
        cv2.putText(photo, unicode_text, (50, 24), cv2.FONT_ITALIC, 1, 0, 2)
        name = eq_path + "/eq_{}.jpeg".format(counter)
        cv2.imwrite(name, photo)
        counter += 1
