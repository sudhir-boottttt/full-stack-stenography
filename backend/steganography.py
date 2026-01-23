from PIL import Image

STOP_MARKER = "###END###"

def text_to_binary(text):
    return [format(ord(c), '08b') for c in text]


def modify_pixels(pixels, binary_data):
    data_index = 0
    new_pixels = []

    for pixel in pixels:
        if data_index >= len(binary_data):
            new_pixels.append(pixel)
            continue

        r, g, b = pixel
        bits = binary_data[data_index]

        r = r - 1 if bits[0] == '0' and r % 2 != 0 else r
        r = r + 1 if bits[0] == '1' and r % 2 == 0 else r

        g = g - 1 if bits[1] == '0' and g % 2 != 0 else g
        g = g + 1 if bits[1] == '1' and g % 2 == 0 else g

        b = b - 1 if bits[2] == '0' and b % 2 != 0 else b
        b = b + 1 if bits[2] == '1' and b % 2 == 0 else b

        new_pixels.append((r, g, b))
        data_index += 1

    return new_pixels


def encode_image(image, message):
    message += STOP_MARKER
    binary_data = text_to_binary(message)

    pixels = list(image.getdata())
    new_pixels = modify_pixels(pixels, binary_data)

    encoded_image = image.copy()
    encoded_image.putdata(new_pixels)
    return encoded_image


def decode_image(image):
    pixels = list(image.getdata())
    binary = ""

    for r, g, b in pixels:
        binary += str(r % 2)
        binary += str(g % 2)
        binary += str(b % 2)

    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    message = ""

    for c in chars:
        try:
            message += chr(int(c, 2))
            if message.endswith(STOP_MARKER):
                return message.replace(STOP_MARKER, "")
        except:
            break

    return message
