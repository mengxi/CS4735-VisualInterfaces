#
# Emily Schultz (ess2183
# COMS 4735, A2
# Due: 3/12/13
#

import Image
import numpy as np
from numpy import linalg as la

TOTAL_IM = 40 #i01.ppm - i40.ppm
BINS = 50

def main():

    hist = readfiles()
    #Step 1:
    compimcolor(hist)

def readfiles():
    '''Read file pixel information for histogram array'''
    filepre = "images/i" #prefix
    filepost = ".ppm"    #postfix

    # for the histogram: [image#-1][red][green][blue]
    hist = np.zeros((TOTAL_IM, BINS, BINS, BINS))
    for i in range(1, TOTAL_IM+1):
        if i < 10:
            filename = filepre + "0" + str(i) + filepost
        else:
            filename = filepre + str(i) + filepost
        p = readfile(filename)

        hist = fillhist(p, i, hist)
    return hist
    
def compimcolor(hist):
    '''Compare all the images using L1-norm of the color hist array'''
    overallmin = 1.0
    overallmax = 0.0
    overallminim = 0
    overallmaxim = 0
    #iterate through the images
    for im1 in range(0,TOTAL_IM):
        maxim = 0
        minim = 0
        maxval = 0
        minval = 10000
        total1 = sum(sum(sum(hist[im1])))
        for im2 in range(0,TOTAL_IM):
            #don't compare the image to itself
            if im1 != im2:
                #compute the l1-norm
                total2 = sum(sum(sum(hist[im2])))
                diff = abs((hist[im1]/float(total1)) - (hist[im2]/float(total2)))
                l1norm = sum(sum(sum(diff)))/2.0
                #update the max and min images
                if maxval < l1norm:
                    maxval = l1norm
                    maxim = im2+1
                if minval > l1norm:
                    minval = l1norm
                    minim = im2+1
        #display the max and min images for this image
        print im1+1, "min = ", minim,"\t", minval
        print im1+1, "max = ", maxim,"\t", maxval
        #update the overall max and min images
        if overallmin > minval:
            overallmin = minval
            overallminim = [im1+1, minim]
        if overallmax < maxval:
            overallmax = maxval
            overallmaxim = [im1+1, maxim]
    #display the max and min images
    print "Overall min = ", overallmin,"\t", overallminim
    print "Overall max = ", overallmax,"\t", overallmaxim

def fillhist(pixels, inum, hist):
    '''Fill the hist array for inum image given pixels'''
    blackcount = 0
    for pixel in pixels:
        #ignore black pixels
        if pixel[0] < 50 and pixel[1] < 50 and pixel[2] < 50:
            blackcount = blackcount + 1
        else:
            r = pixel[0]/BINS
            g = pixel[1]/BINS
            b = pixel[2]/BINS
            hist[inum-1][r][g][b] = hist[inum-1][r][g][b] + 1
    return hist
     
def readfile(filename):
    ''' Read in the ppm file with the given filename '''
    im = Image.open(filename)
    pixels = list(im.getdata())
    return pixels

main()
