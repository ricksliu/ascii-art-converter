import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import time


def image_to_ascii(input_image, output_width, pattern, font_height_to_width):
    input_width = input_image.shape[1]
    input_height = input_image.shape[0]
    output_height = int(output_width * input_height / input_width / font_height_to_width)
    output_ascii = []

    for h in range(int(output_height)):
        for w in range(int(output_width)):
            bgr = input_image[int(h * input_height / output_height), int(w * input_width / output_width)].tolist()
            brightness = (bgr[0] + bgr[1] + bgr[2]) / 3

            pattern_ix = int(brightness * len(pattern) / 256)
            output_ascii.append(pattern[pattern_ix])

        output_ascii.append("\n")

    return ("".join(output_ascii))[:-1]

def ascii_to_image(input_ascii, image_width, image_height, font):
    # Use PIL image and convert to cv2 at the end; cv2 does not support custom fonts
    output_image_pil = Image.new("RGB", (image_width, image_height), color=(0, 0, 0))
    draw = ImageDraw.Draw(output_image_pil)
    ascii_width, ascii_height = draw.textsize(input_ascii, font)
    draw.text(((image_width - ascii_width) / 2, (image_height - ascii_height) / 2), input_ascii, (255, 255, 255), font=font)
    output_image = np.array(output_image_pil)

    return output_image
