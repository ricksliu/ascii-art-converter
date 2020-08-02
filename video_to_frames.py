import cv2

FILE = "video.mp4"
PATH = "frames/"
FRAME_SKIP = 3  # Every Xth frame is captured


def get_frames(file, path, frame_skip):
    video_capture = cv2.VideoCapture(file)

    success, image = video_capture.read()
    frame = 0
    while success:
        cv2.imwrite("%s%d.jpg" % (path, frame), image)  # save frame as JPEG file

        for i in range(frame_skip):
            success, image = video_capture.read()

        frame += 1


get_frames(FILE, PATH, FRAME_SKIP)
