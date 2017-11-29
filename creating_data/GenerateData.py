from PIL import Image, ImageDraw, ImageFont


def text_image_trial(sourse_path, final_path):
    with open(sourse_path) as text_file:
        lines = [l.rstrip() for l in text_file.readlines()]
    img_creator_trial(lines, final_path)


def img_creator_trial(equations, path):
    font = ImageFont.truetype("FreeMono.ttf", 28, encoding="unic")
    counter = 0
    l = max(list(map(font.getsize, equations)))

    for unicode_text in equations:
        # create a blank canvas with extra space between lines
        canvas = Image.new('RGB', (l[0] + 20, l[1] + 20), "white")
        # canvas = Image.new('RGB', (250,100), "white")

        # draw the text onto the text canvas, and use black as the text color
        draw = ImageDraw.Draw(canvas)
        draw.text((10, 10), unicode_text, 'black', font)

        # saves img with diff names
        canvas.save(path + "/eq_{}.jpeg".format(counter))
        counter += 1


