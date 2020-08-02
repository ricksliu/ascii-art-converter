from PIL import Image

FILE = "gradient.jpg"
size = 201


def print_ascii(file, width):
    image = Image.open(file)
    pixels = image.load()

    w = image.size[0]
    h = image.size[1]

    # Outputted dimensions
    w_out = width
    h_out = w_out * 2 * h / w / 5  # Height scaled down 5/2 times since characters are taller than they are wide

    # 2D list of RGB values of pixels
    rgb = list()
    y = 0
    while y < h_out:
        x = 0
        row = list()

        while x < w_out:
            row.append(pixels[int(float(x) * w / w_out), int(float(y) * h / h_out)][:3])
            x += 1

        rgb.append(row)
        y += 1

    # Creates 2D list of ascii characters based on RGB values
    ascii = list()
    for y in rgb:
        row = list()

        for pixel in y:
            # If (reasonably) gray
            average_rgb = (pixel[0] + pixel[1] + pixel[2]) / 3.0
            if abs(pixel[0] - average_rgb) < 50 and abs(pixel[1] - average_rgb) < 50 and abs(pixel[2] - average_rgb) < 50:
                if 0 <= average_rgb < 51:
                    row.append(" ")
                elif 51 <= average_rgb < 102:
                    row.append(".")
                elif 102 <= average_rgb < 153:
                    row.append("=")
                elif 153 <= average_rgb < 204:
                    row.append("?")
                else:
                    row.append("@")

            # If (reasonably) red
            elif pixel[0] >= pixel[1] and pixel[0] >= pixel[2]:
                if 0 <= pixel[0] < 51:
                    row.append(" ")
                elif 51 <= pixel[0] < 102:
                    row.append(",")
                elif 102 <= pixel[0] < 153:
                    row.append("*")
                elif 153 <= pixel[0] < 204:
                    row.append("/")
                else:
                    row.append("#")

            # If (reasonably) green
            elif pixel[1] >= pixel[0] and pixel[1] >= pixel[2]:
                if 0 <= pixel[1] < 51:
                    row.append(" ")
                elif 51 <= pixel[1] < 102:
                    row.append("`")
                elif 102 <= pixel[1] < 153:
                    row.append("+")
                elif 153 <= pixel[1] < 204:
                    row.append("\\")
                else:
                    row.append("$")

            # If (reasonably) blue
            elif pixel[2] >= pixel[0] and pixel[2] >= pixel[1]:
                if 0 <= pixel[2] < 51:
                    row.append(" ")
                elif 51 <= pixel[2] < 102:
                    row.append("'")
                elif 102 <= pixel[2] < 153:
                    row.append("-")
                elif 153 <= pixel[2] < 204:
                    row.append("|")
                else:
                    row.append("&")

        ascii.append(row)

    # Prints single string rather than line by line so the entire image appears instantaneously
    output = ""
    for row in ascii:
        output += "\n" + "".join(row)
    print(output)
    input()


print_ascii(FILE, size)
