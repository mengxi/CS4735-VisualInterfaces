#
# Emily Schultz (ess2183
# COMS 4735, A2
# Due: 3/12/13
#

import Image
import numpy as np
from numpy import linalg as la

def main():

    readfiles()

def readfiles():
    filepre = "images/i" #prefix
    filepost = ".ppm"    #postfix
    bins = 30
    TOTAL_IM = 40
    hist = np.zeros((TOTAL_IM, bins, bins, bins))
    for i in range(1, TOTAL_IM+1): #i01.ppm - i40.ppm
        if i < 10:
            filename = filepre + "0" + str(i) + filepost
        else:
            filename = filepre + str(i) + filepost
        p = readfile(filename)

        blackcount = 0
        for pixel in p:
            #ignore black pixels
            if pixel[0] < 50 and pixel[1] < 50 and pixel[2] < 50:
                blackcount = blackcount + 1
            else:
                r = pixel[0]/bins
                g = pixel[1]/bins
                b = pixel[2]/bins
                hist[i-1][r][g][b] = hist[i-1][r][g][b] + 1
    for im1 in range(0,TOTAL_IM):
        maxim = 0
        minim = 0
        maxval = 0
        minval = 10000
        for im2 in range(0,TOTAL_IM):
            if im1 != im2:
                diff = abs(hist[im1] - hist[im2])
                a = la.norm(diff)
                if maxval < a:
                    maxval = a
                    maxim = im2+1
                if minval > a:
                    minval = a
                    minim = im2+1
                if (im1 == 31 and im2 == 33) or (im1 == 33 and im2 == 38):
                    print im1+1, im2+1, a
        print im1+1, "min = ", minim, minval
        print im1+1, "max = ", maxim, maxval
        
def readfile(filename):
    ''' Read in the ppm file with the given filename '''
    im = Image.open(filename)
    pixels = list(im.getdata())
    return pixels

main()
