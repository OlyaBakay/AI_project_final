import json
import os

from PIL import Image, ImageDraw, ImageFont


def text_to_image(source_path, final_path, source_label_path=None, final_label_path=None):
    remove_files(final_path)

    with open(source_path) as text_file:
        data_lines = [l.rstrip() for l in text_file.readlines()]
    if source_label_path and final_label_path:
        with open(source_label_path) as text_file:
            label_lines = [l.rstrip() for l in text_file.readlines()]
        img_creator(data_lines, final_path, label_lines, final_label_path)
    else:
        img_creator(data_lines, final_path)


def img_creator(equations, eq_path, labels=None, lab_path=None):
    font = ImageFont.truetype("FreeMono.ttf", 14, encoding="unic")
    counter = 0
    # l = max(list(map(font.getsize, equations)))
    labels_map = {}

    for unicode_text in equations:
        # create a blank canvas with extra space between lines
        # canvas = Image.new('RGB', (l[0] + 20, l[1] + 20), "white")
        canvas = Image.new('RGB', (75, 15), "white")

        # draw the text onto the text canvas, and use black as the text color
        draw = ImageDraw.Draw(canvas)
        draw.text((0, 0), unicode_text, 'black', font)

        # saves img with diff names
        name = eq_path + "/eq_{}.jpeg".format(counter)
        canvas.save(name)
        if labels and lab_path:
            labels_map[name] = int(labels[counter])
        counter += 1

    if labels and lab_path:
        with open(lab_path, 'w') as file:
            file.write(json.dumps(labels_map))


def remove_files(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
