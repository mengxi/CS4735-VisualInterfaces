# Emily Schultz (ess2183)
# May 15, 2013
# Visual Interfaces Final Project
# Main Method

import game
import card    # should remove in final version
import unoimage
import Image   #necessary?

def main():
    '''Run and test the project.'''
    mode = raw_input("Game mode (G) or Test mode (T)? ")
    
    if mode == 'G':
        # play a whole game
        playagain = True
        while(playagain):
            cur_game = game.Game()
            winner = cur_game.play()
            print "Congratulations, %s! You won!"%(winner)
            playagain = (bool)(raw_input("Play Again? (Y/N) ") == 'Y')
            
    elif mode == 'T':
        # just get one picture and test it

        # test card class
        #c = card.Card(8,'green')
        #print c
        #a = [c, card.Card('skip','yellow')]
        #print a

        imfilen = raw_input("Filename of image? ")
        # all images in images folder
        filepre = "images/"
        imfilen = filepre + imfilen
        
        # test color check: red green blue yellow
        #print unoimage.cardcolor(Image.open("images/red5.png"))
        #print unoimage.cardcolor(Image.open("images/green9.png"))
        #print unoimage.cardcolor(Image.open("images/blue2.png"))
        #print unoimage.cardcolor(Image.open("images/yellow3.png"))
        #print unoimage.cardcolor(Image.open("images/wild4.png"))
        
        # process the image
        lastcard = unoimage.topcard(imfilen)
        #hand = unoimage.hand(imfilen)
        
        # display what you see
        print "Last Card:", lastcard
        #print "Computer Hand:", hand
        
    else:
        print 'So long...'

if __name__ == "__main__":
    main()
