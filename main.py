from time import sleep
from image_to_ascii import print_ascii

PATH = "frames/"
WIDTH = 180
frame_rate = 24

input("")

frame = 0
try:
    while True:
        print_ascii("%s%d.jpg" % (PATH, frame), WIDTH)
        frame += 1
        # sleep(1.0 / frame_rate)
except:
    pass

input("")
