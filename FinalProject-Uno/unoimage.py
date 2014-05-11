# Emily Schultz (ess2183)
# May 15, 2013
# Visual Interfaces Final Project
# Uno Image Processing Module (ie. The Guts and The Glory)

import Image
import numpy as np
import card
import scipy
import scipy.ndimage.measurements as ndimage
import matplotlib.pyplot as plt
import math
#import scipy.signal.signaltools as sig
#from scipy.misc import imread

def topcard(filename):
    '''Return the last card played from the image.'''
    # open the image and set to default size
    im = Image.open(filename)
    im = im.resize((2500,1500))
    im.save(filename, "PNG")
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
    im = im.crop((bbox[1], bbox[0], bbox[3], bbox[2]))
    im = im.resize((400,600))
    im.save('topcard.png', 'PNG')

    # get color and value of top card
    topcolor = cardcolor(im)
    topvalue = cardvalue('topcard.png', topcolor)

    return card.Card(topvalue, topcolor)

def hand(filename):
    '''Return a list of all cards in the hand given in the image.'''
    # open image and set to default size
    im1 = Image.open(filename)
    im1 = im1.resize((2500, 1500))
    im1.save(filename, "PNG")
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
        fname = 'handcard%d.png'%len(cardsinhand)
        im2.save(fname, 'PNG')
        color = cardcolor(im2)
        value = cardvalue(fname, color)
        cardsinhand.append(card.Card(value, color))
    return cardsinhand

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
    
    #remove based on size of image
    mask_size = sizes < 0.01 * totalpixels
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
    if rgby[maxc] < 2 * (sum(rgby)-rgby[maxc]):
        c = 'black'
    
    return c

def cardvalue(filename, color):
    '''Returns the value of the card in the image.'''
    values = ['0','1','2','3','4','5','6','7','8','9','skip','draw2','reverse']
    prefix = "images/db/"
    postfix = ".png"

    cardvalue = 'TEMP'

    if color == 'black':
        # only options are Wild and Wild Draw Four
        # wild4 should have more white pixels
        whites = [0,0,0]

        # open our card's image
        cardpix = Image.open(filename)
        cardpix = list(cardpix.getdata())

        # open the wild images to compare
        im2 = Image.open(prefix+'wild'+postfix)
        pix2 = list(im2.getdata())

        im3 = Image.open(prefix+'wild4'+postfix)
        pix3 = list(im3.getdata())

        # images should always be the same size
        if len(cardpix) != len(pix2) or len(cardpix) != len(pix3):
            print 'Uh oh.'

        # count white pixels
        for i in range(0,len(cardpix)):
            if sum(cardpix[i]) > 600:
                whites[0] += 1
            if sum(pix2[i]) > 600:
                whites[1] += 1
            if sum(pix3[i]) > 600:
                whites[2] += 1
        # see if it's closer to a wild or a wild draw four
        if math.fabs(whites[0] - whites[1]) < math.fabs(whites[0] - whites[2]):
            cardvalue = 'Wild'
        else:
            cardvalue = 'Wild Draw Four'
    else:
        # 0-9, Skip, Reverse, Draw Two
        # Image Subtraction

### attempt at normalizing and finding correlation - inaccurate
        #c = imread(filename)
        # convert to grayscale
        #c = scipy.average(c, -1)
        #c = (c - c.mean())/ c.std()

        #totes1 = []
        #totes2 = []
        #for imname in values:
            #im2 = Image.open(prefix+imname+postfix)
            #pix2 = list(im2.getdata())
            
            # if len(cardpix) != len(pix2):
            #   print 'Uh oh.'

##            d1 = imread(prefix+imname+postfix)
##            
##            # convert to grayscale (avg the color values)
##            d1 = scipy.average(d1, -1)
##
##            d1 = (d1 - d1.mean())/d1.std()
##
##
##            totes1.append(sig.correlate2d(c, d1))   
        #cardvalue = totes1.index(max(totes1))
        # open our card's image

        
        cardpix = Image.open(filename)
        cardpix = list(cardpix.getdata())

        least = len(cardpix)*255*3

        for imname in values:
            pix2 = Image.open(prefix+imname+postfix)
            pix2 = list(pix2.getdata())

            diffsum = []
            
            for i in range(0,len(cardpix)):
                if sum(cardpix[i]) < 150 and sum(pix2[i]) < 150:
                    # black - ignore
                    'black'
                elif sum(cardpix[i]) > 600 and sum(pix2[i]) > 600:
                    # white - ignore
                    'white'
                else:
                    diffsum.append(math.fabs(sum(cardpix[i]) - sum(pix2[i])))
            if sum(diffsum) < least:
                least = sum(diffsum)
                cardvalue = imname
                
        if cardvalue == 'skip':
            cardvalue = 'Skip'
        elif cardvalue == 'reverse':
            cardvalue = 'Reverse'
        elif cardvalue == 'draw2':
            cardvalue = 'Draw 2'
        else:
            cardvalue = int(cardvalue)
    
    return cardvalue















