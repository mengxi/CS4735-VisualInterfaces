# Emily Schultz (ess2183)
# May 15, 2013
# Visual Interfaces Final Project
# Uno Image Processing Module

import Image
import numpy as np
import card
import scipy.ndimage.measurements as ndimage
import matplotlib.pyplot as plt

def topcard(filename):
    '''Return the last card played from the image.'''
    # open the image
    im = Image.open(filename)

    # get top half of the image
    (width, height) = im.size
    im = im.crop((0, 0 , width, height/2))

    # get all card locations in top half of image (should be two)
    coords = getcardlocations(im)
            
    # ignore the one that is on the left
    index = 0
    if coords[0][1] < coords[1][1]:
        index = 1

    #coords list of type: (vmin, hmin, vmax, hmax)
    bbox = coords[index]
    # crop requires: left, upper, right, lower
    im = im.crop((bbox[1],bbox[0], bbox[3], bbox[2]))
    im = im.resize((400,600))
    im.save('topcard.png', 'PNG')

    # get color and value of top card
    topcolor = cardcolor(im)
    topvalue = cardvalue(im)

    return card.Card(topvalue,topcolor)

def hand(filename):
    '''Return a list of all cards in the hand given in the image.'''
    im1 = Image.open(filename)

    # get bottom half of the image
    (width, height) = im1.size
    im1 = im1.crop((0, height/2, width, height))

    # get all cards in computer hand
    coords = getcardlocations(im1)
    print "Computer hand has %d cards."%(len(coords))

    # loop through cards, identify it, and add it to the list of cards
    cardsinhand = []
    for cardbbox in coords:
        # get original image since crop is lazy
        im2 = Image.open(filename).crop((0, height/2, width, height))
        im2 = im2.crop((cardbbox[1],cardbbox[0], cardbbox[3], cardbbox[2]))
        im2 = im2.resize((400,600))
        im2.save('handcard%d.png'%len(cardsinhand), 'PNG')

        color = cardcolor(im2)
        print color
        value = cardvalue(im2)
        cardsinhand.append(card.Card(value, color))
        
    return cardsinhand

def cardcolor(im):
    '''Returns the color of the card in the image.'''

    # get all pixel values
    pixels = list(im.getdata())
    
    # iterate through pixels, ignoring black and white,
    rgby = [0,0,0,0] # red green blue yellow
    colors = ['red','green','blue','yellow']

    for pix in pixels:
        psum = sum(pix)
        # ignore black and white pixels
        if psum > 150 and psum < 600:
            # create sums of r,g,b,y pixels
            if pix[2] > pix[0] and pix[2] > pix[1]:
                # blue
                #print pix
                rgby[2] += 1
            elif pix[0] > 200 and pix[1] > 200:
                # yellow
                rgby[3] += 1
            elif pix[0] > pix[1] and pix[0] > pix[2]:
                # red
                rgby[0] += 1
            elif pix[1] > pix[0] and pix[1] > pix[2]:
                # green
                rgby[1] += 1
                
    # max is the color of the card
    maxc = rgby.index(max(rgby))
    c = colors[maxc]

    # black if no true max
    if rgby[maxc] < sum(rgby)-rgby[maxc]:
        c = 'black'
    
    return c

def getcardlocations(im):
    '''Return the bbox coordinates for each card in the image.'''

    (width, height) = im.size

    # convert to grayscale (0 - 255)
    gim = im.convert('1')

    # pixels that aren't white are black
    pixels = np.reshape(np.array(gim.getdata()), (height, width))
    pixels = pixels > 240

    # get (two) connected components
    labarr, labcount = ndimage.label(pixels)
    sizes = ndimage.sum(pixels, labarr, range(labcount + 1))

    # ignore small regions - get just the two cards
    totalpixels = height/2 * width
    
    #**** MAX SIZE OF COMPONENTS INSTEAD? ******
    #print sizes
    #print max(sizes)
    
    mask_size = sizes < 0.01 * totalpixels    #remove based on size of image
    remove_pixel = mask_size[labarr]
    labarr[remove_pixel] = 0

    # relabel
    labarr, labcount = ndimage.label(labarr)

    # get locations of all cards
    cardlocs = []
    for label in range(labcount):
        locs = np.where(labarr == (label+1))
        # get bounding box
        vmin = min(locs[0])
        vmax = max(locs[0])
        hmin = min(locs[1])
        hmax = max(locs[1])
        cardlocs.append((vmin, hmin, vmax, hmax))

    # display labeled image
    #plt.imshow(labarr)
    #plt.show()

    return cardlocs

def cardvalue(im):
    '''Returns the value of the card in the image.'''
    return 'TESTTEST'
