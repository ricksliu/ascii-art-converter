# Takes an inputted image file and generates ASCII art from it

from PIL import Image


def generate_ascii(file, width):
    image = Image.open(file)
    pixels = image.load()

    # Number of rows of characters; halved since characters are taller than they are wide
    height = width * image.size[1] / image.size[0] / 2

    # Creates 2D list of RGB values of pixels, scaled to required dimensions
    rgb = list()
    for y in range(int(height)):
        row = list()
        for x in range(width):
            row.append(pixels[int(float(x) * image.size[0] / width), int(float(y) * image.size[1] / height)][:3])
        rgb.append(row)

    # Creates string of ascii characters based on RGB values
    output = ""
    for y in rgb:
        output += "\n"

        for pixel in y:
            # If (reasonably) gray
            average_rgb = (pixel[0] + pixel[1] + pixel[2]) / 3.0
            if abs(pixel[0] - average_rgb) < 50 and abs(pixel[1] - average_rgb) < 50 and abs(pixel[2] - average_rgb) < 50:
                if 0 <= average_rgb < 51:
                    output += " "
                elif 51 <= average_rgb < 102:
                    output += "."
                elif 102 <= average_rgb < 153:
                    output += "="
                elif 153 <= average_rgb < 204:
                    output += "?"
                else:
                    output += "@"

            # If (reasonably) red
            elif pixel[0] >= pixel[1] and pixel[0] >= pixel[2]:
                if 0 <= pixel[0] < 51:
                    output += " "
                elif 51 <= pixel[0] < 102:
                    output += ","
                elif 102 <= pixel[0] < 153:
                    output += "*"
                elif 153 <= pixel[0] < 204:
                    output += "/"
                else:
                    output += "#"

            # If (reasonably) green
            elif pixel[1] >= pixel[0] and pixel[1] >= pixel[2]:
                if 0 <= pixel[1] < 51:
                    output += " "
                elif 51 <= pixel[1] < 102:
                    output += "`"
                elif 102 <= pixel[1] < 153:
                    output += "+"
                elif 153 <= pixel[1] < 204:
                    output += "\\"
                else:
                    output += "$"

            # If (reasonably) blue
            else:
                if 0 <= pixel[2] < 51:
                    output += " "
                elif 51 <= pixel[2] < 102:
                    output += "'"
                elif 102 <= pixel[2] < 153:
                    output += "-"
                elif 153 <= pixel[2] < 204:
                    output += "|"
                else:
                    output += "&"
        
    return output
