def to_rgb(h: str):
        h = h.lstrip('#')
        return list(int(h[i:i+2], 16) for i in (0, 2, 4))

def to_hex(rgb: list):
    return '#%02x%02x%02x' % tuple (rgb)

def scale_rgb(rgb: list, percentage: int):
    step = (percentage * 100) / 255
    return [int(255 if i + step > 255 else i + step) for i in rgb]