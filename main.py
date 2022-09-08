import os
import glob
import json
import cv2
from moviepy.editor import VideoFileClip

import font_util
import image_ascii_util


config_path = "config.json"
with open(config_path) as file:
    config = json.load(file)
    INPUT_PATH = glob.glob(config["inputPath"])
    OUTPUT_PATH = config["outputPath"]
    PATTERN = config["pattern"]
    ASCII_RES_W = config["asciiResW"]
    VIDEO_RES_H = config["videoResH"]
    CONTRAST_BOOST = config["contrastBoost"]

for input_path in INPUT_PATH:
    file_name = os.path.basename(input_path)

    print("Started converting '{}'.".format(file_name))
    input_video = cv2.VideoCapture(input_path)
    frame_rate = input_video.get(cv2.CAP_PROP_FPS)
    num_frames = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))

    output_path = OUTPUT_PATH + file_name
    temp_output_path = OUTPUT_PATH + "temp_" + file_name
    output_height = VIDEO_RES_H
    output_width = int(output_height * int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH)) / int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    output_video = cv2.VideoWriter(temp_output_path, 0, -1, frame_rate, (output_width, output_height))

    font = font_util.get_font("consolas.ttf", ASCII_RES_W, output_width)
    font_height_to_width = font_util.get_font_height_to_width(font)

    success, input_image = input_video.read()
    curr_frame = 1
    while success:
        output_ascii = image_ascii_util.image_to_ascii(input_image, ASCII_RES_W, PATTERN, font_height_to_width, CONTRAST_BOOST)
        output_image = image_ascii_util.ascii_to_image(output_ascii, output_width, output_height, font)
        output_video.write(output_image)

        if curr_frame % 10 == 0:
            print("Progress: {}/{} frames.".format(curr_frame, num_frames))
        success, input_image = input_video.read()
        curr_frame += 1

    print("Progress: {}/{} frames.".format(num_frames, num_frames))
    output_video.release()

    audio_clip = VideoFileClip(input_path).audio
    video_clip = VideoFileClip(temp_output_path)
    video_clip = video_clip.set_audio(audio_clip)
    video_clip.write_videofile(output_path)  # Save as new file and delete old file; overwriting old file causes video to glitch
    os.remove(temp_output_path)

    print("Finished converting '{}'.".format(file_name))
