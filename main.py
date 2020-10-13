import time
from image_to_ascii import generate_ascii


settings_file = open("settings.txt", "r")
settings_file.readline()
PATH = settings_file.readline().strip().split()[1]
settings_file.readline()
WIDTH = int(settings_file.readline().strip().split()[1])  # Number of characters per line
settings_file.close()

frame_rate_file = open("%sframe_rate.txt" % PATH, "r")
FRAME_RATE = float(frame_rate_file.readline().strip())
frame_rate_file.close()

# Loops and generates ASCII art for each frame
frame = 0
ascii = list()
try:
    while True:
        ascii.append(generate_ascii("%s%d.jpg" % (PATH, frame), WIDTH))

        frame += 1
        if (frame) % 100 == 0:
            print("Generated up to frame " + str(frame) + ".")

except FileNotFoundError:
    pass

input("ASCII generation finished. Generated " + str(frame) + " frames. Press enter.")

# Prints according to FRAME_RATE
a = 0
start_time = time.time()
while a < len(ascii):
    if time.time() - start_time >= a / FRAME_RATE:
        print('\n' + ascii[a], end='')
        a += 1

input("\n\nProcess finished. Press enter.")
