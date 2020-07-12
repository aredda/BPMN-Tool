from pathlib import Path

def filetobytes(filename):
    if filename != '':
        with open(filename, 'rb') as file:
            data = file.read()
        return data


def bytestofile(directory, filename, extension, data: bytes):
    Path(directory).mkdir(parents=True, exist_ok=True)
    with open(f'{directory}/{filename}.{extension}', 'wb') as file:
        file.write(data)
