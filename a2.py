#
# Emily Schultz (ess2183
# COMS 4735, A2
# Due: 3/12/13
#

import Image

def main():

    readfiles()

def readfiles():
    filepre = "images/i" #prefix
    filepost = ".ppm"    #postfix
    for i in range(1, 41): #i01.ppm - i40.ppm
        if i < 10:
            filename = filepre + "0" + str(i) + filepost
        else:
            filename = filepre + str(i) + filepost
        p = readfile(filename)
        firstp = p[0]
        print firstp[0] # r value of first pixel

def readfile(filename):
    ''' Read in the ppm file with the given filename '''
    im = Image.open(filename)
    pixels = list(im.getdata())
    return pixels

main()
