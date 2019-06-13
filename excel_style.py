import xlwt

def set_color(color,bold):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.colour_index=color
    font.bold = bold
    style.font=font
    return style
