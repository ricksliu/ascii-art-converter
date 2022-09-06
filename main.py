import os
import glob
import json
from math import ceil
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip

# Convert cv2 image to ASCII string
def image_to_ascii(input_image, output_pattern, output_width, sx):
    input_width = input_image.shape[1]
    input_height = input_image.shape[0]
    output_height = ceil(float(output_width) * input_height / input_width * 0.55)
    output_ascii = ""

    # For each sampled pixel in image
    for h in range(int(output_height)):
        for w in range(int(output_width)):
            # Calculate brightness
            x = int(w * input_width / output_width)
            y = int(h * input_height / output_height)
            bgr = input_image[y, x].tolist()
            brightness = float(bgr[0] + bgr[1] + bgr[2]) / 3

            # Append corresponding ASCII character
            output_pattern_ix = int(brightness * len(output_pattern) / 256)
            output_ascii += output_pattern[output_pattern_ix]

        output_ascii += "\n"

    return output_ascii

# Convert ASCII string to cv2 image
def ascii_to_image(input_ascii, output_width, output_height, output_font):
    # Create black PIL image and write text
    output_image_pil = Image.new("RGB", (output_width, output_height), color=(0, 0, 0))
    draw = ImageDraw.Draw(output_image_pil)
    draw.text((0, 0), input_ascii, (255, 255, 255), font=output_font)

    # Convert to cv2 image
    output_image = np.array(output_image_pil)

    return output_image

# Get settings from config file
config_path = "config.json"
with open(config_path) as file:
    config = json.load(file)
    INPUT_PATH = glob.glob(config["inputPath"])
    OUTPUT_PATH = config["outputPath"]
    OUTPUT_PATTERN = config["outputPattern"][::-1]
    OUTPUT_WIDTH = config["outputWidth"]

# For each video in input directory
for input_path in INPUT_PATH:
    file_name = os.path.basename(input_path)
    print("Converting '{}'.".format(file_name))
    input_video = cv2.VideoCapture(input_path)
    width = int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_rate = input_video.get(cv2.CAP_PROP_FPS)
    num_frames = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))

    output_path = OUTPUT_PATH + file_name
    temp_output_path = OUTPUT_PATH + "temp_" + file_name
    output_video = cv2.VideoWriter(temp_output_path, 0, -1, frame_rate, (width, height))
    font = ImageFont.truetype("consolas.ttf", ceil(1.81 * width / OUTPUT_WIDTH))

    # For each frame in input video
    success, input_image = input_video.read()
    curr_frame = 1
    while success:
        # Generate ASCII frame and write to output video
        output_ascii = image_to_ascii(input_image, OUTPUT_PATTERN, OUTPUT_WIDTH, curr_frame)
        output_image = ascii_to_image(output_ascii, width, height, font)
        output_video.write(output_image)

        if curr_frame % 10 == 0:
            print("Progress: {}/{} frames.".format(curr_frame, num_frames))
        success, input_image = input_video.read()
        curr_frame += 1

    output_video.release()

    # Add audio
    print("Adding audio to {}.".format(file_name))
    audio_clip = VideoFileClip(input_path).audio
    video_clip = VideoFileClip(temp_output_path)
    video_clip = video_clip.set_audio(audio_clip)
    video_clip.write_videofile(output_path)
    os.remove(temp_output_path)

    print("Saving '{}'.\n".format(file_name))
