#
# Emily Schultz (ess2183
# COMS 4735, A2
# Visual Information Retrieval
# Due: 3/12/13
#

import Image
import numpy as np
from numpy import linalg as la

TOTAL_IM = 40 #i01.ppm - i40.ppm
#Step 1 bins
BINS = 25
BIN_SIZE = int((255.0/BINS)+1)
#Step 2 bins
BIN2 = 100
BIN2_SIZE = int((3100.0/BIN2))         #-1357 to 1520
# +- 1550
#images are 89x60
COLS = 89 
ROWS = 60

def main():

    #hist = readfiles1()
    #Step 1
    #compimcolor(hist)
    #Step 2
    pixels = readfiles2()
    compimtexture(pixels)

def readfiles2():
    '''Read file pixel information for Step 2 histogram comparison'''
    filepre = "images/i" #prefix
    filepost = ".ppm"    #postfix

    hist = np.zeros((TOTAL_IM, BIN2))

    # for each image
    for i in range(1, TOTAL_IM+1):
        if i < 10:
            filename = filepre + "0" + str(i) + filepost
        else:
            filename = filepre + str(i) + filepost
        p = readfile(filename)
        prc = np.reshape(p, (ROWS,COLS,3)) #reshape into matrix 
        #prc[r][c] == p[COLS*r+c]
        
        #grayscale image:
        gray_im = []
        for pixel in p:
            avg = (pixel[0] + pixel[1] + pixel[2]) / 3
            gray_im.append(avg)
        grc = np.reshape(gray_im, (ROWS,COLS))
        #create laplacian images
        lap = []
        for r in range(0,ROWS):
            for c in range(0, COLS):
                #ignore edges
                if not (r == 0 or c == 0 or r == ROWS-1 or c == COLS-1):
                    maskvalue = 8 * grc[r][c] - grc[r-1][c] - grc[r+1][c] - grc[r][c-1]
                    maskvalue = maskvalue - grc[r][c+1] - grc[r-1][c-1] - grc[r-1][c+1]
                    maskvalue = maskvalue - grc[r+1][c-1] - grc[r+1][c+1]
                    lap.append(maskvalue)
        laprc = np.reshape(lap, (ROWS-2,COLS-2))


        for j in range(0,len(lap)):
            #handle background
            if gray_im[j] <= 40:
                #black
                'ignoreme'
            #create histogram
            else:
                value = (lap[j] + 1550)/BIN2_SIZE #0 to 100
                #print i, j, value
                hist[i-1][value] += 1
    return hist

def compimtexture(hist):
    overallmin = 1.0
    overallmax = 0.0
    overallminim = 0
    overallmaxim = 0
    
    for im1 in range(0, TOTAL_IM):
        maxval = 0
        minval = 10000
        maxim = 0
        minim = 0
        
        total1 = sum(hist[im1])
        for im2 in range(0, TOTAL_IM):
            if im1 != im2:
                total2 = sum(hist[im2])
                diff = abs((hist[im1]/float(total1)) - (hist[im2]/float(total2)))
                l1norm = sum(diff)/2.0
                #update max and min
                if maxval < l1norm:
                    maxval = l1norm
                    maxim = im2+1
                if minval > l1norm:
                    minval = l1norm
                    minim = im2+1
        #display max min for each image
        print im1+1, "min = ", minim, "\t", (1.0 - minval)
        print im1+1, "max = ", maxim, "\t", (1.0 - maxval)
        #update the overall max and min images
        if overallmin > minval:
            overallmin = minval
            overallminim = [im1+1, minim]
        if overallmax < maxval:
            overallmax = maxval
            overallmaxim = [im1+1, maxim]
    #display the max and min images
    print "Overall min = ", (1.0 - overallmin),"\t", overallminim
    print "Overall max = ", (1.0 - overallmax),"\t", overallmaxim

def readfiles1():
    '''Read file pixel information for histogram array'''
    filepre = "images/i" #prefix
    filepost = ".ppm"    #postfix

    # for the histogram: [image#-1][red][green][blue]
    hist = np.zeros((TOTAL_IM, BIN_SIZE, BIN_SIZE, BIN_SIZE))
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
        print im1+1, "min = ", minim,"\t", (1.0 - minval)
        print im1+1, "max = ", maxim,"\t", (1.0 - maxval)
        #update the overall max and min images
        if overallmin > minval:
            overallmin = minval
            overallminim = [im1+1, minim]
        if overallmax < maxval:
            overallmax = maxval
            overallmaxim = [im1+1, maxim]
    #display the max and min images
    print "Overall min = ", (1.0 - overallmin),"\t", overallminim
    print "Overall max = ", (1.0 - overallmax),"\t", overallmaxim

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
