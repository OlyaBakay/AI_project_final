import cv2
import numpy as np
import json
import os


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


def remove_files(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


def img_creator_eq(equations, eq_path, labels=None, lab_path=None):
    counter = 0
    labels_map = {}
    for unicode_text in equations:
        photo = np.zeros(shape=(28, 165)).fill(250)
        parts = unicode_text.split(" ")
        parts[0] = parts[0].replace("x", "")
        parts.insert(1, "x")
        cv2.putText(photo, parts[0], (0, 24), cv2.FONT_ITALIC, 1, 0, 2)
        cv2.putText(photo, parts[1], (70, 24), cv2.FONT_ITALIC, 1, 0, 2)
        cv2.putText(photo, parts[2], (90, 24), cv2.FONT_ITALIC, 1, 0, 2)
        cv2.putText(photo, parts[3], (120, 24), cv2.FONT_ITALIC, 1, 0, 2)
        name = eq_path + "/eq_{}.jpeg".format(counter)
        cv2.imwrite(name, photo)
        if labels and lab_path:
            labels_map[name] = int(labels[counter])
        counter += 1
    if labels and lab_path:
        with open(lab_path, 'w') as file:
            file.write(json.dumps(labels_map))


def img_creator_ans(equations, eq_path):
    counter = 0
    for unicode_text in equations:
        photo = np.zeros(shape=(28, 165)).fill(250)
        cv2.putText(photo, unicode_text, (80, 24), cv2.FONT_ITALIC, 1, 0, 2)
        name = eq_path + "/eq_{}.jpeg".format(counter)
        cv2.imwrite(name, photo)
        counter += 1
