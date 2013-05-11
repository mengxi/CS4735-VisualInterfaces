# Emily Schultz (ess2183)
# May 15, 2013
# Visual Interfaces Final Project
# Main Method

import game
import card
import unoimage

def main():
    '''Run and test the project.'''
    mode = raw_input("Game mode (G) or Test mode (T)? ")
    if mode == 'G':
        # play a whole game
        playagain = True
        while(playagain):
            cur_game = game.Game()
            # stuff goes here
            playagain = (bool)(raw_input("Play Again? (Y/N) ") == 'Y')
    elif mode == 'T':
        #just get one picture and test it

        #test card class
        c = card.Card('Skip', 'yellow')
        print c

        
        imfilen = raw_input("Filename of image? ")
        lastcard = unoimage.topcard(imfilen)
        print "Last Card:", lastcard
    else:
        print 'So long...'

if __name__ == "__main__":
    main()
