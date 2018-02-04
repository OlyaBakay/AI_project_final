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


def text_to_image(source_path, final_path, source_label_path=None, final_label_path=None):
    remove_files(final_path)

    with open(source_path) as text_file:
        data_lines = [l.rstrip() for l in text_file.readlines()]

    if source_label_path and final_label_path:
        with open(source_label_path) as text_file:
            label_lines = [l.rstrip() for l in text_file.readlines()]
        img_creator_eq(data_lines, final_path, label_lines, final_label_path)
    else:
        img_creator_ans(data_lines, final_path)


def img_creator_eq(equations, eq_path, labels, lab_path):
    counter = 0
    labels_list = []
    for unicode_text in equations:
        photo = np.zeros(shape=(28, 165))
        photo.fill(250)
        parts = unicode_text.split(" ")
        parts[0] = parts[0].replace("x", "")
        parts.insert(1, "x")
        cv2.putText(photo, parts[0], (0, 24), cv2.FONT_ITALIC, 1, 0, 2)
        cv2.putText(photo, parts[1], (70, 24), cv2.FONT_ITALIC, 1, 0, 2)
        cv2.putText(photo, parts[2], (90, 24), cv2.FONT_ITALIC, 1, 0, 2)
        cv2.putText(photo, parts[3], (120, 24), cv2.FONT_ITALIC, 1, 0, 2)
        name = eq_path + "/eq_{}.jpeg".format(counter)
        cv2.imwrite(name, photo)
        labels_list.append([name, unicode_text, int(labels[counter]), ])
        counter += 1

    df = pd.DataFrame(labels_list, columns=['EquationNumber', 'Equation', 'IsCorrectAnswer'])
    df.to_csv(lab_path)


def img_creator_ans(equations, eq_path):
    df = pd.read_csv('./pics/info.csv',  index_col=0)
    df['Answer'] = equations
    df.to_csv('./pics/info.csv')
    counter = 0
    for unicode_text in equations:
        photo = np.zeros(shape=(28, 165))
        photo.fill(250)
        cv2.putText(photo, unicode_text, (70, 24), cv2.FONT_ITALIC, 1, 0, 2)
        name = eq_path + "/eq_{}.jpeg".format(counter)
        cv2.imwrite(name, photo)
        counter += 1
