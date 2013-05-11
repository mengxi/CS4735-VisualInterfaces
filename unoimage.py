# Emily Schultz (ess2183)
# May 15, 2013
# Visual Interfaces Final Project
# Uno Image Processing Module

import Image
import numpy as np
import card

def topcard(filename):
    '''Return the last card played from the image.'''
    # all images in images folder
    filepre = "images/"
    filename = filepre + filename

    im = Image.open(filename)

    (width, height) = im.size

    im = im.crop((0, 0 , width, height/2))
    im.show()
    
    return card.Card(9,'red')
