# Emily Schultz, ess2183
# COMS4735: Visual Interfaces to Computers
# Assignment 3: Columbia Map
# Due: 4/9/2013


import numpy as np
import matplotlib.pyplot as plt
import Image
import scipy.ndimage.measurements as snm


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

    # perform list of all relationships
    step2()
    
    # Step 3: Source and goal description and user interface
    # Step 4: Creativity - Path generation

def step2():
    '''
    Generate all binary spatial relationships for every pair,
    and apply transitive reduction.
    '''
    # arrays for all relationships
    n_array = np.zeros((num_buildings, num_buildings),bool)
    s_array = np.zeros((num_buildings, num_buildings),bool)
    w_array = np.zeros((num_buildings, num_buildings),bool)
    e_array = np.zeros((num_buildings, num_buildings),bool)
    near_array = np.zeros((num_buildings, num_buildings),bool)

    # generate all relationships
    for b1 in range(0, num_buildings):
        for b2 in range(0, num_buildings):
            if b1 != b2:
                n_array[b1][b2] = North(b1, b2)
                s_array[b1][b2] = South(b1, b2)
                e_array[b1][b2] = East(b1, b2)
                w_array[b1][b2] = West(b1, b2)
                near_array[b1][b2] = Near(b1, b2)


    # transitive reduction
    for j in range(0, num_buildings):
        for i in range(0, num_buildings):
            if n_array[i][j]:
                for k in range(0, num_buildings):
                    if n_array[j][k]:
                        n_array[i][k] = False
            if s_array[i][j]:
                for k in range(0, num_buildings):
                    if s_array[j][k]:
                        s_array[i][k] = False
            if w_array[i][j]:
                for k in range(0, num_buildings):
                    if w_array[j][k]:
                        w_array[i][k] = False
            if e_array[i][j]:
                for k in range(0, num_buildings):
                    if e_array[j][k]:
                        e_array[i][k] = False
    # If it's north then we don't need south, if it's east we don't need west
##    for i in range(0, num_buildings):
##        for j in range(0, num_buildings):
##            if n_array[i][j]:
##                s_array[j][i] = False
##            if e_array[i][j]:
##                w_array[j][i] = False

    count = 0
    ncount = 0
    for i in range(0, num_buildings):
        for j in range(0, num_buildings):
            if n_array[i][j]:
                print "North of ", i+1," is ", j+1
                count += 1
            if s_array[i][j]:
                print "South of ", i+1," is ", j+1
                count += 1
            if w_array[i][j]:
                print "West of ", i+1," is ", j+1
                count += 1
            if e_array[i][j]:
                print "East of ", i+1," is ", j+1
                count += 1
            if near_array[i][j]:
                #print "Near to ", i+1, " is ", j+1
                ncount += 1
    print count, ncount

def North(S,G):
    '''Returns True if North of S is G.'''
    # if it's a building number, get its mbr
    if isinstance(G, int):
        var1 = mbrs[G][3]
    # otherwise, its a point, so get its x coordinate
    else:
        var1 = G[1]
    if isinstance(S, int):
        var2 = mbrs[S][1]
    else:
        var2 = S[1]
    if var1 < var2:
        return True
    return False

def South(S,G):
    '''Returns True if South of S is G.'''
    if isinstance(G, int):
        var1 = mbrs[G][1]
    else:
        var1 = G[1]
    if isinstance(S, int):
        var2 = mbrs[S][3]
    else:
        var2 = S[1]
    if var1 > var2:
        return True
    return False

def East(S,G):
    '''Returns True if East of S is G.'''
    if isinstance(G, int):
        var1 = mbrs[G][0]
    else:
        var1 = G[0]
    if isinstance(S, int):
        var2 = mbrs[S][2]
    else:
        var2 = S[0]
    if var1 > var2:
        return True
    return False

def West(S,G):
    '''Returns True if West of S is G.'''
    if isinstance(G, int):
        var1 = mbrs[G][2]
    else:
        var1 = G[0]
    if isinstance(S, int):
        var2 = mbrs[S][0]
    else:
        var2 = S[0]
    if var1 < var2:
        return True
    return False

def Near(S,G):
    '''Returns True if Near to S is G.'''
    # check distance of min bounding rectangle away for goal
    Sxloc = coms[S][0]
    Syloc = coms[S][1]
    Smbr = mbrs[S]
    Sxlen = Smbr[2] - Smbr[0]
    Sylen = Smbr[3] - Smbr[1]

    # get all pixels within the min bound rect distance of this building
    minSx = Smbr[0] - Sxlen
    if minSx < 0:           #edge condition
        minSx = 0
    maxSx = Smbr[2] + Sxlen + 1
    if maxSx >= width:      #edge condition
        maxSx = width - 1
    minSy = Smbr[1] - Sylen
    if minSy < 0:           #edge condition
        minSy = 0
    maxSy = Smbr[3] + Sylen + 1
    if maxSy >= height:     #edge condition
        maxSy = height - 1

    # get all pixels within min/max range
    values = pix_grid[minSy:maxSy][:,minSx:maxSx]
    # check for the goal building number in the pixels
    places = np.where(values == (G+1))

    # if where returns nothing, G is not near to S
    if np.size(places) == 0:
        return False
    return True

def readmaps(label_file, table_file):
    '''Given two filenames, reads in the files and stores the information.'''
    # get the pixel information of the buildings from label_file
    lab_im = Image.open(label_file)
    global num_buildings
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

    global width
    global height
    width = campus_im.size[0] #275
    height = campus_im.size[1] #495

    pix_list = np.array(campus_im.getdata())        #list of 275x495 items
    global pix_grid
    pix_grid = np.reshape(pix_list, (height,width)) #495x275 array

    global areas
    global coms
    global mbrs
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
        coms[bnum-1] = [ycom,xcom]

        # Minimum Bounding Rectangle: upper left and lower right coordinates
        maxx = max(indices[0])
        maxy = max(indices[1])
        minx = min(indices[0])
        miny = min(indices[1])
        mbrs[bnum-1] = [miny,minx,maxy,maxx]

    # Descriptions list
    global descriptions
    descriptions = [[] for i in range(0,len(names))]
    # Geometry
    shape()
    # Size
    size()
    # Orientation
    orientation()
    # Extrema
    extrema()


    # Display all info for each building
    for bnum in range(0, len(names)):
        print "Building #%d: %s" %(bnum+1,names[bnum])
        print "\tCenter of Mass: (%f, %f)" %(coms[bnum][0],coms[bnum][1])
        print "\tArea: ", areas[bnum]
        print "\tMin Bounding Rect: (%d,%d) to (%d,%d)" \
            %(mbrs[bnum][0],mbrs[bnum][1],mbrs[bnum][2],mbrs[bnum][3])
        print "\tDescription: ", descriptions[bnum]

def shape():
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
            if bwidth >= (bheight - sqerrorval) and \
               bwidth <= (bheight + sqerrorval):
                descriptions[bnum].append('square')
            # exactly rectangular
            else:
                descriptions[bnum].append('rectangular')
        # some 0 pixels, but not may
        elif sval >= (mbrarea-isherrorval) and sval <= (mbrarea+isherrorval):
            # squarish
            if bwidth >= (bheight - sqerrorval) and \
               bwidth <= (bheight + sqerrorval):
                descriptions[bnum].append('squarish')
            # rectangularish
            else:
                descriptions[bnum].append('rectangularish')
        # narrow
        if bwidth >= 3 * bheight or bheight >= 3 * bwidth:
            descriptions[bnum].append('narrow')
        # L-shaped
        nums = pix_grid[mbr[1]:mbr[3]+1][:,mbr[0]:mbr[2]+1].copy()
        # assign 1 to all zeros and zero to all non-zero numbers
        nums[np.where(nums != bnum+1)] = 0
        nums[np.where(nums != 0)] = -1
        nums = nums + 1
        # if more than one component and not a squarish or rectangularish it's L
        if snm.label(nums)[1] > 1 and 'squarish' not in descriptions[bnum]\
           and 'rectangularish' not in descriptions[bnum]:
            descriptions[bnum].append('L-shaped')
        # With a hole: increase mbr by one pixel if possible
        minx = mbr[1] - 1
        if minx < 0:
            minx = 0
        miny = mbr[0] - 1
        if miny < 0:
            miny = 0
        maxx = mbr[3] + 2
        if maxx > width:
            maxx = width
        maxy = mbr[2] + 2
        if maxy > height:
            maxy = height
        # assign one to all zeros, zero to all numbers
        nums = pix_grid[minx:maxx][:,miny:maxy].copy()
        nums[np.where(nums != bnum+1)] = 0
        nums[np.where(nums != 0)] = -1
        nums = nums + 1
        # get the number of componenets (if more than one, there's a hole
        if snm.label(nums)[1] > 1:
            descriptions[bnum].append('with a hole')
                
def size():
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
            descriptions[bnum].append('average sized')    #.30 to .21 (5)
        elif area > .1 * maxarea:
            descriptions[bnum].append('small')      #.21 to .10 (7)
        else:
            descriptions[bnum].append('tiny')       #.10 to .00 (3)
        
    # Get the smallest and largest buildings
    maxi = np.argmax(areas)
    mini = np.argmin(areas)
    descriptions[mini].append('smallest')
    descriptions[maxi].append('largest')

def orientation():
    '''Adds orientation descriptions to the descriptions list.'''
    for bnum in range(0, len(descriptions)):
        mbr = mbrs[bnum]
        bwidth = mbr[2] - mbr[0] # x diff
        bheight = mbr[3] - mbr[1] # y diff
        # East to West oriented
        if bwidth >= 1.5 * bheight:
            descriptions[bnum].append('oriented E to W')
        # North to South oriented
        elif bheight >= 1.5 * bwidth:
            descriptions[bnum].append('oriented N to S')
        # Not really oriented either way
        else:
            descriptions[bnum].append('symmetrically oriented')

def extrema():
    '''Adds extrema descriptions to the descriptions list.'''
    # widest and tallest and central
    wid_bnum = -1
    hei_bnum = -1
    cen_bnum = -1
    maxwidth = 0
    maxheight = 0
    mincen = width + height

    # most central, east, west, north, south
    east_bnum = -1
    west_bnum = -1
    nor_bnum = -1
    sou_bnum = -1
    
    mineast = width + height
    minwest = width + height
    minnorth = width + height
    minsouth = width + height

    # most SE, SW, NE, NW
    SE_bnum = -1
    SW_bnum = -1
    NE_bnum = -1
    NW_bnum = -1
    
    minSE = width + height
    minSW = width + height
    minNE = width + height
    minNW = width + height
    
    for bnum in range(0, len(descriptions)):
        mbr = mbrs[bnum]
        # widest?
        cur_width = mbr[2] - mbr[0]
        if cur_width >= maxwidth:
            wid_bnum = bnum
            maxwidth = cur_width
        # tallest?
        cur_height = mbr[3] - mbr[1]
        if cur_height >= maxheight:
            hei_bnum = bnum
            maxheight = cur_height
        # central?
        centrality = abs((height/2) - coms[bnum][1]) + \
                     abs((width/2) - coms[bnum][0])
        if centrality <= mincen:
            cen_bnum = bnum
            mincen = centrality
        # north?
        northerness = abs((width/2) - coms[bnum][0]) + mbr[1]
        if northerness < minnorth:
            nor_bnum = bnum
            minnorth = northerness
        # south?
        southerness = abs((width/2) - coms[bnum][0]) + (height - mbr[3])
        if southerness <= minsouth:
            sou_bnum = bnum
            minsouth = southerness
        # east?
        easterness = abs((height/2) - coms[bnum][1]) + (width - mbr[2])
        if easterness <= mineast:
            east_bnum = bnum
            mineast = easterness
        # west?
        westerness = abs((height/2) - coms[bnum][1]) + mbr[0]
        if westerness <= minwest:
            west_bnum = bnum
            minwest = westerness
        # northeast?
        if mbr[1] + (width - mbr[2]) < minNE:
            minNE = mbr[1] + (width - mbr[2])
            NE_bnum = bnum
        # northwest?
        if mbr[1] + mbr[0] < minNW:
            minNW = mbr[0] + mbr[1]
            NW_bnum = bnum
        # southeast?
        if (height-mbr[3]) + (width - mbr[2]) < minSE:
            minSE = (height-mbr[3]) + (width - mbr[2])
            SE_bnum = bnum
        # southwest?
        if (height-mbr[3]) + mbr[0] < minSW:
            minSW = (height-mbr[3]) + mbr[0]
            SW_bnum = bnum

    # add descriptions
    descriptions[hei_bnum].append("tallest (N/S)")
    descriptions[wid_bnum].append("widest (E/W)")
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
