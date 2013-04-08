# Emily Schultz, ess2183
# COMS 4735, Visual Interfaces to Computers
# Assignment 3
# Due 4/9/2013


import Tkinter
from Tkinter import *
import Image, ImageTk


root = Tkinter.Tk()

# use ppm file so green/red regions easy to display
modified_file = "ass3-campus-mod.ppm"
image1 = Image.open(modified_file)

# set size of window to be size of image
root.geometry('%dx%d' %(image1.size[0],image1.size[1]))
tkpi = ImageTk.PhotoImage(image1)

# add the image to the display
label_image = Tkinter.Label(root, image=tkpi)
label_image.place(x=0, y=0, width=image1.size[0], height=image1.size[1])

# print location of mouse click
def callback(event):
    '''Display location of mouse click.'''
    image1 = Image.open(modified_file)

    SIZE = 4
    minx = event.x-2
    if minx < 0:
        minx = 0
    miny = event.y-2
    if miny < 0:
        miny = 0
    maxx = event.x+2+1
    if maxx >= image1.size[0]:
        minx = image1.size[0]-1
    maxy = event.y+2+1
    if maxy >= image1.size[1]:
        miny = image1.size[1]-1


    for i in range(minx, maxx):
        for j in range(miny,maxy):
            image1.putpixel((i, j), (255,0,255))

    root.geometry('%dx%d' %(image1.size[0],image1.size[1]))
    tkpi = ImageTk.PhotoImage(image1)
    
    label_image = Tkinter.Label(root, image=tkpi)
    label_image.place(x=0, y=0,\
                      width=image1.size[0], height=image1.size[1])
    root.mainloop()
    

# mouse click for coordinates
root.bind("<Button-1>", callback)

# start display
root.mainloop()

