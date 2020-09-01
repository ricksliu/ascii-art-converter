from time import sleep
from image_to_ascii import generate_ascii

PATH = "frames/"
WIDTH = 180
FRAME_RATE = 24

# Loops and generates ASCII art for each frame
ascii = list()
frame = 0
try:
    while True:
        ascii.append(generate_ascii("%s%d.jpg" % (PATH, frame), WIDTH))

        if (frame + 1) % 100 == 0:
            print("Generated up to frame " + str(frame + 1) + ".")

        frame += 1

except FileNotFoundError:
    pass

input("ASCII generation finished. Generated " + str(frame + 1) + " frames. Press enter.")

# Prints according to FRAME_RATE
for a in ascii:
    print(a)
    sleep(1.0 / FRAME_RATE)

input("Process finished. Press enter.")
