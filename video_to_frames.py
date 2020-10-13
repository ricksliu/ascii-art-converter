# Takes an inputted mp4 file and outputs its frames as jpeg files in a designated directory

import os
import cv2


settings_file = open("settings.txt", "r")
FILE = settings_file.readline().strip().split()[1]
PATH = settings_file.readline().strip().split()[1]
FRAME_SKIP = int(settings_file.readline().strip().split()[1])  # Every Xth frame is captured; 1 means every frame is captured
settings_file.close()


def get_frames(file, path, frame_skip):
    # Clears directory of previous frames
    frames = [frame for frame in os.listdir(path) if frame.endswith(".jpg")]
    for frame in frames:
        os.remove(os.path.join(path, frame))

    video = cv2.VideoCapture(file)

    # Stores frame rate of video in file
    frame_rate_file = open("%sframe_rate.txt" % path, "w")
    frame_rate_file.write(str(video.get(cv2.CAP_PROP_FPS) / frame_skip))
    frame_rate_file.close()

    # Loops until it reaches the end of the video
    frame = 0
    success, image = video.read()
    while success:
        cv2.imwrite("%s%d.jpg" % (path, frame), image)  # Saves frame as JPEG file; file names start from 0.jpg

        frame += 1
        if (frame) % 100 == 0:
            print("Generated up to frame " + str(frame) + ".")

        # Captures next Xth frame, based on frame_skip
        for i in range(frame_skip):
            success, image = video.read()

    input("Frame generation finished. Generated " + str(frame) + " frames. Press enter.")


get_frames(FILE, PATH, FRAME_SKIP)
