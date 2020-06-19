def filetobytes(filename):
    with open(filename, 'rb') as file:
        data = file.read()
    return data


def bytestofile(directory, filename, extension, data: bytes):
    with open(f'{directory}/{filename}.{extension}', 'wb') as file:
        file.write(data)
