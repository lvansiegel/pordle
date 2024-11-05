
def addToHex(hx, r, g, b):
    '''adds a number (0-255) to each value of a hex code (format #xxxxxx)'''
    try:
        if len(hx) != 7:
            raise(Exception)
        ro = int(hx[1:3], 16)
        go = int(hx[3:5], 16)
        bo = int(hx[5:7], 16)
    except:
        return "\"{0}\" is an invalid hex code".format(hx)
    red = "{:02}".format(hex(int(max(0, min(255, ro+r)))))
    green = "{:02}".format(hex(int(max(0, min(255, go+g)))))
    blue = "{:02}".format(hex(int(max(0, min(255, bo+b)))))
    if len(red[2:]) == 1:
        red = "0x0"+red[2]
    if len(green[2:]) == 1:
        green = "0x0"+green[2]
    if len(blue[2:]) == 1:
        blue = "0x0"+blue[2]
    rh = "#{0}{1}{2}".format(red[2:],green[2:],blue[2:])
    return rh

if __name__ == "__main__":
    print("#ffaa99 converted to hex and (-300, -50, 2) is")
    print(addToHex("#202020", -300, -20, 2))