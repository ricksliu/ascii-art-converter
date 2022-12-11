import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont


def get_brightness(image, x, y):
    bgr = image[y, x].tolist()
    return (bgr[0] + bgr[1] + bgr[2]) / 3


def image_to_ascii(input_image, output_width, pattern, font_height_to_width, contrast_boost):
    input_width = input_image.shape[1]
    input_height = input_image.shape[0]
    output_height = int(output_width * input_height / input_width / font_height_to_width)
    brightnesses = []

    min_brightness = 256
    max_brightness = -1
    for h in range(int(output_height)):
        for w in range(int(output_width)):
            brightness = get_brightness(input_image, int(w * input_width / output_width), int(h * input_height / output_height))
            min_brightness = brightness if brightness < min_brightness else min_brightness
            max_brightness = brightness if brightness > max_brightness else max_brightness
            brightnesses.append(brightness)
        brightnesses.append(-1)  # Represent newline as -1

    adjust = lambda b : b
    if contrast_boost > 0:
        if contrast_boost > 1:
            contrast_boost = 1
        min_brightness = min_brightness * contrast_boost
        max_brightness = max_brightness * contrast_boost + 255 * (1 - contrast_boost)
        adjust = lambda b : (b - min_brightness) * 255 / (max_brightness - min_brightness)

    output_ascii = [(pattern[int(adjust(b) * len(pattern) / 256)] if b != -1 else "\n") for b in brightnesses]
    return ("".join(output_ascii))[:-1]


def ascii_to_image(input_ascii, image_width, image_height, font):
    # Use PIL image and convert to cv2 at the end; cv2 does not support custom fonts
    output_image_pil = Image.new("RGB", (image_width, image_height), color=(0, 0, 0))
    draw = ImageDraw.Draw(output_image_pil)
    ascii_width, ascii_height = draw.textsize(input_ascii, font)
    draw.text(((image_width - ascii_width) / 2, (image_height - ascii_height) / 2), input_ascii, (255, 255, 255), font=font)
    output_image = np.array(output_image_pil)

    return output_image
