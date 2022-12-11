from PIL import Image, ImageDraw, ImageFont


def get_font(font_path, num_chars, target_width):
    sample_text = "X" * num_chars

    # Make two initial guesses
    prev_font_size = 12
    font = ImageFont.truetype(font_path, prev_font_size)
    prev_width = font.getsize(sample_text)[0]
    curr_font_size = 120
    font = ImageFont.truetype(font_path, curr_font_size)
    curr_width = font.getsize(sample_text)[0]

    while True:
        # Linearly interpolate next guess from previous two
        next_font_size = int(prev_font_size + (target_width - prev_width) * (curr_font_size - prev_font_size) / (curr_width - prev_width))
        if next_font_size == prev_font_size and prev_width < target_width or next_font_size == curr_font_size and curr_width < target_width:
            next_font_size += 1
        elif next_font_size == prev_font_size and prev_width > target_width or next_font_size == curr_font_size and curr_width > target_width:
            next_font_size -= 1
        font = ImageFont.truetype(font_path, next_font_size)
        next_width = font.getsize(sample_text)[0]

        # Store two closest guesses
        closest_array = [abs(w - target_width) for w in [prev_width, curr_width, next_width]]
        if closest_array[0] == max(closest_array):
            prev_font_size = next_font_size
            prev_width = next_width
        elif closest_array[1] == max(closest_array):
            curr_font_size = next_font_size
            curr_width = next_width

        if abs(prev_font_size - curr_font_size) <= 1:
            return ImageFont.truetype(font_path, curr_font_size - 1 if curr_width >= target_width else curr_font_size)  # If guess is on the larger end, subtract 1


def get_font_height_to_width(font):
    num_lines = 100
    sample_text = "\n".join(["X"] * num_lines)

    draw = ImageDraw.Draw(Image.new('RGB', (100, 100)))
    width, height = draw.textsize(sample_text, font)
    return height / width / num_lines
