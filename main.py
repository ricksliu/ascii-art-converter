from PIL import Image

FILE = "test.jpg"

image = Image.open(FILE)
pixels = image.load()
print(image.size)
print(pixels[0,0])