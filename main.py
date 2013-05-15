# Emily Schultz (ess2183)
# May 15, 2013
# Visual Interfaces Final Project
# Main Method

import game
import card    # should remove in final version
import unoimage
import Image   # should remove in final version

def main():
    '''Run and test the project.'''
    mode = raw_input("Game mode (G) or Test mode (T)? ")
    
    if mode == 'G':
        # play a whole game
        playagain = True
        while(playagain):
            cur_game = game.Game()
            winner = cur_game.play()
            print "Congratulations, %s! You won!\n"%(winner)
            playagain = (bool)(raw_input("Play Again? (Y/N) ") == 'Y')
            
    elif mode == 'T':
        # just get one picture and test it - debugging

        imfilen = raw_input("Filename of image? ")
        # all images in images folder
        filepre = "images/"
        imfilen = filepre + imfilen
        
        # test color check: red green blue yellow
        # yes: 1,2,3,4,5,6,7,8,9,0, draw2 skip, reverse, wild, wild4 checked
        #print unoimage.cardcolor(Image.open("images/5.png"))
        #print unoimage.cardcolor(Image.open("images/6.png"))
        #print unoimage.cardcolor(Image.open("images/7.png"))
        #print unoimage.cardcolor(Image.open("images/8.png"))
        #print unoimage.cardcolor(Image.open("images/9.png"))
        
        # process the image
        lastcard = unoimage.topcard(imfilen)
        hand = unoimage.hand(imfilen)
        
        # display what you see
        print "Last Card:", lastcard
        print "Computer Hand:", hand
        
    else:
        print 'So long...'

if __name__ == "__main__":
    main()
