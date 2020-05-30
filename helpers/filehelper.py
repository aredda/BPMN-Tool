def filetobytes(filename):
    with open(filename, 'rb') as file:
        imagedata = file.read()
    return imagedata


def bytestofile(directory, filename, extension, imagedata: bytes):
    with open(f'{directory}/{filename}.{extension}', 'wb') as file:
        file.write(imagedata)
