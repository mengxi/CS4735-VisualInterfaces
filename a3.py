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

    # display the map to check visually
    check_im = Image.open(display_file)
    check_im.show()

def step1(campus_im, names):
    '''Prints out features and descriptions for each building'''

    width = campus_im.size[0] #275
    height = campus_im.size[1] #495

    arr = np.array(campus_im.getdata())
    aal = np.reshape(arr, (height,width))
    # Display Descriptors for Each building
    for bnum in range(1, len(names)+1):
        print "Building #%d: %s"%(bnum,names[bnum-1])
        indices = np.where(aal == bnum) # gives list of row,col of occurences
        # Area
        area = len(indices[0])
        print "\tArea: ",area
        # Center of Mass (where x oriented east and y oriented south)
        xcom = sum(indices[0])/float(area)
        ycom = sum(indices[1])/float(area)
        print "\tCenter of Mass: (%f, %f)"%(xcom,ycom)
        # Minimum Bounding Rectangle: upper left and lower right coordinates
        maxx = max(indices[0])
        maxy = max(indices[1])
        minx = min(indices[0])
        miny = min(indices[1])
        print "\tMin Bounding Rect: (%d,%d) to (%d,%d)"%(minx,miny,maxx,maxy)
        # Descriptions
        # Geometry
        # Size
        # Orientation
        # Extrema




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

main()
