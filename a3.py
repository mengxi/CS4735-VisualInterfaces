# Emily Schultz, ess2183
# COMS4735: Visual Interfaces to Computers
# Assignment 3: Columbia Map
# Due: 4/9/2013


import numpy as np
import matplotlib.pyplot as plt
import Image


def main():
    ''' Does the work for this program.'''
    # input files
    labeled_file = "ass3-labeled.pgm"
    table_file = "ass3-table.txt"
    display_file = "ass3-campus.pgm"

    # read in the information
    map_im, b_names = readmaps(labeled_file, table_file)

    # Step 1: Basic infrastructure and building features/descriptions
    step1(map_im, b_names)

    # Step 2: Describing compact spatial relations

    # Step 3: Source and goal description and user interface
    # Step 4: Creativity - Path generation
    
def readmaps(label_file, table_file):
    '''Given two filenames, reads in the files and stores the information.'''
    # get the pixel information of the buildings from label_file
    lab_im = Image.open(label_file)
    num_buildings = lab_im.getextrema()[1] #27

    # create a list of the buildings names from table_file
    tab_in = open(table_file, 'r')
    building_names = []
    for i in range(0, num_buildings):
        cur_line = tab_in.readline()
        cur_name = cur_line.split('"')[1]
        building_names.append(cur_name)

    return lab_im, building_names

def step1(campus_im, names):
    '''Prints out features and descriptions for each building'''

    width = campus_im.size[0] #275
    height = campus_im.size[1] #495

    pix_list = np.array(campus_im.getdata())        #list of 275x495 items
    pix_grid = np.reshape(pix_list, (height,width)) #495x275 array

    areas = np.zeros(len(names))    # list of areas
    coms = np.zeros((len(names),2)) # list of centers of mass
    mbrs = np.zeros((len(names),4)) # list of min bound rect coords
    
    # get each buildings features
    for bnum in range(1, len(names)+1):
        indices = np.where(pix_grid == bnum) # row,col list of occurences

        # Area
        area = len(indices[0])
        areas[bnum-1] = area

        # Center of Mass (where x oriented east and y oriented south)
        xcom = sum(indices[0])/float(area)
        ycom = sum(indices[1])/float(area)
        coms[bnum-1] = [xcom,ycom]

        # Minimum Bounding Rectangle: upper left and lower right coordinates
        maxx = max(indices[0])
        maxy = max(indices[1])
        minx = min(indices[0])
        miny = min(indices[1])
        mbrs[bnum-1] = [miny,minx,maxy,maxx]

    # Descriptions list
    descriptions = [[] for i in range(0,len(names))]
    # Geometry
    shape(descriptions, areas, coms, mbrs, pix_grid)
    # Size
    size(descriptions, areas)
    # Orientation
    orientation(descriptions, mbrs)
    # Extrema
    extrema(descriptions, coms, mbrs, width, height)

    # Display all info for each building
    for bnum in range(0, len(names)):
        print "Building #%d: %s" %(bnum+1,names[bnum])
        print "\tCenter of Mass: (%f, %f)" %(coms[bnum][1],coms[bnum][0])
        print "\tArea: ", areas[bnum]
        print "\tMin Bounding Rect: (%d,%d) to (%d,%d)" \
            %(mbrs[bnum][0],mbrs[bnum][1],mbrs[bnum][2],mbrs[bnum][3])
        print "\tDescription: ", descriptions[bnum]

def shape(descriptions, areas, coms, mbrs, pix_grid):
    '''Adds shape descriptions to the desciptions list.'''
    for bnum in range(0, len(descriptions)):
        # get the current min bounding rectangle
        mbr = mbrs[bnum]
        bwidth = mbr[2] - mbr[0] # x diff
        bheight = mbr[3] - mbr[1] # y diff

        # get all pixels in the min bound rect of this building
        values = pix_grid[mbr[1]:mbr[3]+1][:,mbr[0]:mbr[2]+1]
        sval = sum(sum(values))/(bnum + 1)
        mbrarea = (mbr[2]-mbr[0]+1) * (mbr[3]-mbr[1]+1)

        # a little off still alright
        isherrorval = .2 * mbrarea
        sqerrorval = .1* bwidth + .1*bheight
        
        # compare the area of the MBR to the sum of the values in MBR
        if sval == mbrarea:
            # exactly square
            if bwidth >= (bheight - sqerrorval) and bwidth <= (bheight + sqerrorval):
                descriptions[bnum].append('square')
            # exactly rectangular
            else:
                descriptions[bnum].append('rectangular')
        # some 0 pixels, but not may
        elif sval >= (mbrarea-isherrorval) and sval <= (mbrarea+isherrorval):
            # squarish
            if bwidth >= (bheight - sqerrorval) and bwidth <= (bheight + sqerrorval):
                descriptions[bnum].append('squarish')
            # rectangularish
            else:
                descriptions[bnum].append('rectangularish')
        # narrow
        if bwidth >= 3 * bheight or bheight >= 3 * bwidth:
            descriptions[bnum].append('narrow')
        # l-shaped
        
def size(descriptions, areas):
    '''Adds size descriptions to the descriptions list.'''
    # largest building's area
    maxarea = max(areas)
    for bnum in range(0, len(areas)):
        # this building's area
        area = areas[bnum]
        # relationship between two areas:
        if area > .8 * maxarea:
            descriptions[bnum].append('very large') #1.0 to .80 (6)
        elif area > .3 * maxarea:
            descriptions[bnum].append('large')      #.80 to .30 (6)
        elif area > .21 * maxarea:
            descriptions[bnum].append('average')    #.30 to .21 (5)
        elif area > .1 * maxarea:
            descriptions[bnum].append('small')      #.21 to .10 (7)
        else:
            descriptions[bnum].append('tiny')       #.10 to .00 (3)
        
    # Get the smallest and largest buildings
    maxi = np.argmax(areas)
    mini = np.argmin(areas)
    descriptions[mini].append('smallest')
    descriptions[maxi].append('largest')

def orientation(descriptions, mbrs):
    '''Adds orientation descriptions to the descriptions list.'''
    for bnum in range(0, len(descriptions)):
        mbr = mbrs[bnum]
        bwidth = mbr[2] - mbr[0] # x diff
        bheight = mbr[3] - mbr[1] # y diff
        # East to West oriented
        if bwidth >= 1.5 * bheight:
            descriptions[bnum].append('E to W')
        # North to South oriented
        elif bheight >= 1.5 * bwidth:
            descriptions[bnum].append('N to S')
        # Not really oriented either way
        else:
            descriptions[bnum].append('symmetric')

def extrema(descriptions, coms, mbrs, W, H):
    '''Adds extrema descriptions to the descriptions list.'''
    # widest and tallest and central
    wid_bnum = -1
    hei_bnum = -1
    cen_bnum = -1
    maxwidth = 0
    maxheight = 0
    mincen = W+H

    # most central, east, west, north, south
    east_bnum = -1
    west_bnum = -1
    nor_bnum = -1
    sou_bnum = -1
    
    mineast = W+H
    minwest = W+H
    minnorth = W+H
    minsouth = W+H

    # most SE, SW, NE, NW
    SE_bnum = -1
    SW_bnum = -1
    NE_bnum = -1
    NW_bnum = -1
    
    minSE = W+H
    minSW = W+H
    minNE = W+H
    minNW = W+H
    
    for bnum in range(0, len(descriptions)):
        mbr = mbrs[bnum]
        # widest?
        width = mbr[3] - mbr[1]
        if width >= maxwidth:
            wid_bnum = bnum
            maxwidth = width
        # tallest?
        height = mbr[2] - mbr[0]
        if height >= maxheight:
            hei_bnum = bnum
            maxheight = height
        # central?
        centrality = abs((H/2) - coms[bnum][0]) + abs((W/2) - coms[bnum][1])
        if centrality <= mincen:
            cen_bnum = bnum
            mincen = centrality
        # north?
        northerness = abs((W/2) - coms[bnum][1]) + mbr[1]
        if northerness < minnorth:
            nor_bnum = bnum
            minnorth = northerness
        # south?
        southerness = abs((W/2) - coms[bnum][1]) + (H - mbr[3])
        if southerness <= minsouth:
            sou_bnum = bnum
            minsouth = southerness
        # east?
        easterness = abs((H/2) - coms[bnum][0]) + (W - mbr[2])
        if easterness <= mineast:
            east_bnum = bnum
            mineast = easterness
        # west?
        westerness = abs((H/2) - coms[bnum][0]) + mbr[0]
        if westerness <= minwest:
            west_bnum = bnum
            minwest = westerness
        # northeast?
        if mbr[1] + (W - mbr[2]) < minNE:
            minNE = mbr[1] + (W - mbr[2])
            NE_bnum = bnum
        # northwest?
        if mbr[1] + mbr[0] < minNW:
            minNW = mbr[0] + mbr[1]
            NW_bnum = bnum
        # southeast?
        if (H-mbr[3]) + (W - mbr[2]) < minSE:
            minSE = (H-mbr[3]) + (W - mbr[2])
            SE_bnum = bnum
        # southwest?
        if (H-mbr[3]) + mbr[0] < minSW:
            minSW = (H-mbr[3]) + mbr[0]
            SW_bnum = bnum

    # add descriptions
    descriptions[wid_bnum].append("tallest (N/S)")
    descriptions[hei_bnum].append("widest (E/W)")
    descriptions[cen_bnum].append("central-most")

    # directions
    descriptions[nor_bnum].append("northern-most")
    descriptions[sou_bnum].append("southern-most")
    descriptions[east_bnum].append("eastern-most")
    descriptions[west_bnum].append("western-most")

    descriptions[NE_bnum].append("northeastern-most")
    descriptions[NW_bnum].append("northwestern-most")
    descriptions[SE_bnum].append("southeastern-most")
    descriptions[SW_bnum].append("southwestern-most")

main()
