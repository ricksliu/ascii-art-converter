# Takes an inputted mp4 file and outputs its frames as jpeg files in a designated directory

import os
import cv2


FILE = "video.mp4"
PATH = "frames/"
FRAME_SKIP = 1  # Every Xth frame is captured; 1 means every frame is captured


def get_frames(file, path, frame_skip):
    # Clears directory of previous frames
    frames = [frame for frame in os.listdir(path) if frame.endswith(".jpg")]
    for frame in frames:
        os.remove(os.path.join(path, frame))

    video_capture = cv2.VideoCapture(file)

    # Loops until it reaches the end of the video
    success, image = video_capture.read()
    frame_num = 0
    while success:
        cv2.imwrite("%s%d.jpg" % (path, frame_num), image)  # Saves frame as JPEG file; file names start from 0.jpg

        if (frame_num + 1) % 100 == 0:
            print("Generated up to frame " + str(frame_num + 1) + ".")

        # Captures next Xth frame, based on frame_skip
        for i in range(frame_skip):
            success, image = video_capture.read()

        frame_num += 1

    input("Frame generation finished. Generated " + str(frame_num + 1) + " frames. Press enter.")


get_frames(FILE, PATH, FRAME_SKIP)
