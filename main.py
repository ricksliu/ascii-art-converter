from PIL import Image

FILE = "test2.jpg"

image = Image.open(FILE)
pixels = image.load()

w = image.size[0]
h = image.size[1]

w_out = 180
h_out = w_out * h / w

rgb = list()

x = 0
while x < w_out:
    y = 0
    column = list()
    while y < h_out:
        column.append(pixels[int(float(x) * w / w_out), int(float(y) * h / h_out)][:3])
        y += 1
    rgb.append(column)
    x += 1

# for col in rgb:
#     print(col)
