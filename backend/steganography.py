from PIL import Image

STOP_MARKER = "###END###"

def gen_data(data):
    return [format(ord(i), '08b') for i in data]

def modify_pixels(pixels, data):
    datalist = gen_data(data)
    data_len = len(datalist)
    pixel_iter = iter(pixels)

    for i in range(data_len):
        pixel_block = [
            value
            for value in next(pixel_iter)[:3]
            + next(pixel_iter)[:3]
            + next(pixel_iter)[:3]
        ]

        for j in range(8):
            if datalist[i][j] == '0' and pixel_block[j] % 2 != 0:
                pixel_block[j] -= 1
            elif datalist[i][j] == '1' and pixel_block[j] % 2 == 0:
                pixel_block[j] += 1

        # STOP FLAG
        if i == data_len - 1:
            if pixel_block[-1] % 2 == 0:
                pixel_block[-1] += 1
        else:
            if pixel_block[-1] % 2 != 0:
                pixel_block[-1] -= 1

        yield tuple(pixel_block[:3])
        yield tuple(pixel_block[3:6])
        yield tuple(pixel_block[6:9])

def encode_image(image, message):
    message += STOP_MARKER
    new_image = image.copy()
    width = new_image.size[0]

    x = y = 0
    for pixel in modify_pixels(new_image.getdata(), message):
        new_image.putpixel((x, y), pixel)
        if x == width - 1:
            x = 0
            y += 1
        else:
            x += 1

    return new_image

def decode_image(image):
    data = ""
    pixel_iter = iter(image.getdata())

    while True:
        pixels = [
            value
            for value in next(pixel_iter)[:3]
            + next(pixel_iter)[:3]
            + next(pixel_iter)[:3]
        ]

        binary = ""
        for i in pixels[:8]:
            binary += '0' if i % 2 == 0 else '1'

        data += chr(int(binary, 2))

        if pixels[-1] % 2 != 0:
            break

    return data.replace(STOP_MARKER, "")
