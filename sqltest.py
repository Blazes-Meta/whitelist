def f(hex_color):
    if hex_color.startswith("#"):
        hex_color = hex_color[1:]
    return int(hex_color, 16)

print(f("#e93848"))
