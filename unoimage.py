# Emily Schultz (ess2183)
# May 15, 2013
# Visual Interfaces Final Project
# Uno Image Processing Module

import Image
import numpy as np
import card

def topcard(filename):
    '''Return the last card played from the image.'''

    im = Image.open(filename)

    # get top half of the image
    (width, height) = im.size
    im = im.crop((0, 0 , width, height/2))

    # get (two) connected components        scipy.ndimage?
    # ignore the one that is on the left

    # dummy return
    return card.Card(9,'red')

def hand(filename):
    '''Return a list of all cards in the hand given in the image.'''
    im = Image.open(filename)

    # get bottom half of the image
    (width, height) = im.size
    im = im.crop((0, height/2, width, height))

    # get (all) connected components
    # loop through each, identify it, and add it to the list of cards

    # dummy return
    return [card.Card('Skip','blue')]
