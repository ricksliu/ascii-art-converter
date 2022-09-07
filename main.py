import os
import glob
import json
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip

# Find font with size that will fit string perfectly across screen
def get_font(font_path, num_chars, target_width):
    sample_text = "X" * num_chars

    # Make two size guesses and record widths
    prev_font_size = 12
    font = ImageFont.truetype(font_path, prev_font_size)
    prev_width = font.getsize(sample_text)[0]
    curr_font_size = 24
    font = ImageFont.truetype(font_path, curr_font_size)
    curr_width = font.getsize(sample_text)[0]

    while True:
        # Interpolate next size guess from previous two guesses
        next_font_size = int(prev_font_size + (target_width - prev_width) * (curr_font_size - prev_font_size) / (curr_width - prev_width))
        if next_font_size == prev_font_size or next_font_size == curr_font_size:
            next_font_size = int((prev_font_size + curr_font_size) / 2)

        # If cannot refine further, return
        if next_font_size == prev_font_size or next_font_size == curr_font_size:
            return ImageFont.truetype(font_path, next_font_size)

        # Record next width
        font = ImageFont.truetype(font_path, next_font_size)
        next_width = font.getsize(sample_text)[0]

        # Keep closest two guesses
        closest_array = [abs(w - target_width) for w in [prev_width, curr_width, next_width]]
        if closest_array[0] == max(closest_array):
            prev_font_size = next_font_size
            prev_width = next_width
        elif closest_array[1] == max(closest_array):
            curr_font_size = next_font_size
            curr_width = next_width

# Get ratio of height of char to width
def get_font_height_to_width(font):
    num_lines = 100
    sample_text = "\n".join(["X"] * num_lines)

    draw = ImageDraw.Draw(Image.new('RGB', (100, 100)))
    width, height = draw.textsize(sample_text, font)
    return height / width / num_lines

# Convert cv2 image to ASCII string
def image_to_ascii(input_image, ascii_pattern, ascii_length, font_height_to_width):
    input_width = input_image.shape[1]
    input_height = input_image.shape[0]

    output_height = int(ascii_length * input_height / input_width / font_height_to_width)
    output_ascii = []

    # For each sampled pixel in image
    for h in range(int(output_height)):
        for w in range(int(ascii_length)):
            # Calculate brightness
            bgr = input_image[int(h * input_height / output_height), int(w * input_width / ascii_length)].tolist()
            brightness = (bgr[0] + bgr[1] + bgr[2]) / 3

            # Append corresponding ASCII character
            ascii_pattern_ix = int(brightness * len(ascii_pattern) / 256)
            output_ascii.append(ascii_pattern[ascii_pattern_ix])

        output_ascii.append("\n")

    return ("".join(output_ascii))[:-1]

# Convert ASCII string to cv2 image
def ascii_to_image(input_ascii, image_width, image_height, font):
    # Create black PIL image and write text; cv2 does not support custom fonts
    output_image_pil = Image.new("RGB", (image_width, image_height), color=(0, 0, 0))
    draw = ImageDraw.Draw(output_image_pil)
    ascii_width, ascii_height = draw.textsize(input_ascii, font)
    draw.text(((image_width - ascii_width) / 2, (image_height - ascii_height) / 2), input_ascii, (255, 255, 255), font=font)

    # Convert to cv2 image
    output_image = np.array(output_image_pil)

    return output_image

# Get settings from config file
config_path = "config.json"
with open(config_path) as file:
    config = json.load(file)
    INPUT_PATH = glob.glob(config["inputPath"])
    OUTPUT_PATH = config["outputPath"]
    ASCII_PATTERN = config["asciiPattern"]
    ASCII_LENGTH = config["asciiLength"]

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

    font = get_font("consolas.ttf", ASCII_LENGTH, width)
    font_height_to_width = get_font_height_to_width(font)

    # For each frame in input video
    success, input_image = input_video.read()
    curr_frame = 1
    while success:
        # Generate ASCII frame and write to output video
        output_ascii = image_to_ascii(input_image, ASCII_PATTERN, ASCII_LENGTH, font_height_to_width)
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
