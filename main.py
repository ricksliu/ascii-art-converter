from time import sleep
from image_to_ascii import print_ascii

PATH = "frames/"
WIDTH = 201
images = 719
frame_rate = 5

input()

for frame in range(719):
    print_ascii("%s%d.jpg" % (PATH, frame), WIDTH)
    sleep(1.0 / frame_rate)
