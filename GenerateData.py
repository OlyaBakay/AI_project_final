from PIL import Image, ImageDraw, ImageFont


def text_image(text_path):
    with open('text.txt') as text_file:
        lines = [l.rstrip() for l in text_file.readlines()]
    return img_creator(lines)


def img_creator(equations):
    font = ImageFont.truetype("FreeMono.ttf", 28, encoding="unic")
    counter_eq, counter_res = 1, 1
    counter = 0
    for unicode_text in equations:
        text_width, text_height = font.getsize(unicode_text)

        # create a blank canvas with extra space between lines
        canvas = Image.new('RGB', (text_width + 20, text_height + 20), "white")

        # draw the text onto the text canvas, and use black as the text color
        draw = ImageDraw.Draw(canvas)
        draw.text((10, 10), unicode_text, 'black', font)

        # saves img with diff names
        if counter % 2 == 0:
            canvas.save("tmp/eq_{}.jpeg".format(counter_eq))
            counter_eq += 1
        else:
            canvas.save("tmp/result_{}.jpeg".format(counter_res))
            counter_res += 1
        counter += 1
        # canvas.show()


if __name__ == '__main__':
    text_image('text.txt')
