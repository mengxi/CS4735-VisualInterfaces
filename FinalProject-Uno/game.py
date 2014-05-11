# Emily Schultz (ess2183)
# May 15, 2013
# Visual Interfaces Final Project
# Game Class for an Uno Game

import card
import unoimage
from random import choice

class Game:
    '''Class for a game.'''
    def __init__(self):
        '''Create the game, with players'''
        # add all the players
        self.setupPlayers()
        self.setupDeck()
        
    def setupPlayers(self):
        '''Add all the players to the game'''
        num_players = input("How many players in this game? ")
        # list of players
        self.players = []
        self.scores = []
        self.winner = False
        self.players.append('Computer')
        self.scores.append(0)
        print "Player 1 Name: Computer"
        # get player names
        for i in range(0,num_players - 1):
            name = raw_input("Player %d Name: "%i)
            self.players.append(name)
            self.scores.append(0)
        # who goes first
        self.cur_player = 0
        # used for reverse
        self.direction = 1
        self.uno = 0

    def setupDeck(self):
        '''Begin the game by setting up the deck status.'''
        startfilename = raw_input("Filename of starting image? ")
        # all images in images folder
        filepre = "images/"
        startfilename = filepre + startfilename
        
        self.lastcard = unoimage.topcard(startfilename)
        print "Top Card is:",self.lastcard
        self.comphand = unoimage.hand(startfilename)
        print "Computer Hand is:",self.comphand
        
    def getCurrentPlayer(self):
        '''Return who will move next.'''
        return self.players[self.cur_player]
    
    def getNumPlayers(self):
        '''Return the number of players.'''
        return len(self.players)
    
    def getPlayerScore(self, player):
        '''Return the score of player (number or name), or -1 if invalid.'''
        try:
            #number
            index = int(player)
            if index > self.getNumPlayers:
                print 'Invalid player number'
                return -1
        except ValueError:
            #name
            if self.players.count(player) > 0:
                index = self.players.index(player)
            else:
                print 'Invalid player name'
                return -1
        return self.scores[index]
    
    def getCurrentWinner(self):
        '''Return the player with the highest score (ties ? TEST)'''
        return self.scores.index(max(self.scores))
    
    def getCompMove(self):
        '''Return a legal move for the computer to make given his hand.'''
        possible_cards = []
        
        # check for those in hand of the same color
        curcolor = self.lastcard.getColor()
        if curcolor == 'black':
            # last card was a wild, need to know what they called it
            curcolor = self.wildcolor
                
        # check for those in hand of the same value
        curvalue = self.lastcard.getValue()

        # get rid of colored cards first (most accurate)
        choiceindex = -1

        for c in self.comphand:
            if curcolor == c.getColor():
                possible_cards.append(c)
                choiceindex = len(possible_cards)-1
            elif curvalue == c.getValue():
                possible_cards.append(c)
            elif c.getValue() == 'Wild' or c.getValue() == 'Wild Draw Four':
                possible_cards.append(c)

        if not possible_cards:
            return 'DRAW'
        else:
            # strategy for comp move (HERE) if time permits
            if choiceindex == -1:
                choiceindex = 0
            print "Computer's Possible Options: "
            print possible_cards
            return possible_cards[choiceindex]
   
    def hasWinner(self):
        '''Return true if game has been won (ie player has reached 0 cards)'''
        # play until someone scores 50
        if max(self.scores) > 50:
            self.winner = self.players[self.scores.index(max(self.scores))]
        return self.winner
    
    def play(self):
        '''Play a game of UNO.'''
        # first move - already have image
        while(not self.hasWinner()):
            
            # computer's turn
            if self.cur_player == 0:
                cardtoplay = self.getCompMove()
                # display move / update score
                if cardtoplay != 'DRAW':
                    print "Computer Plays Card:", cardtoplay
                    self.comphand.remove(cardtoplay)
                    # choose a wild color at random
                    if cardtoplay.getValue() == 'Wild':
                        colors = ['red','green','blue','yellow']
                        self.wildcolor = random.choice(colors)
                        print "Computer declares the wild to be",self.wildcolor
                    if len(self.comphand) == 1:
                        print "Computer cries, UNO!"
                    elif len(self.comphand) == 0:
                        self.winner = self.cur_player
                    self.scores[self.cur_player] += 1
                else:
                    print "Computer is forced to draw a card."
                    
            # other player's move (computer will advise)        
            else:
                print "%s's Turn" %(self.players[self.cur_player])
                print "Computer suggests you play: "
                if self.lastcard.getColor() != 'black':
                    print "a card of value: " + str(self.lastcard.getValue())
                    print "a card of color: " + self.lastcard.getColor()
                print 'a Wild or Wild Draw Four card'
                if self.lastcard.getValue() == 'Wild':
                    print "a card of color: " + self.wildcolor
                playermove = raw_input("What is your move? (DRAW or card)")
                # update score if they played a card
                if playermove != 'DRAW':
                    self.scores[self.cur_player] += 1
                    if 'Wild' in playermove:
                        self.wildcolor = raw_input("What color is the Wild? ")
                    query = raw_input("WON or UNO? ")
                    if query == "WON":
                        self.winner = self.cur_player
                    elif query == "UNO":
                        self.uno = 1
            print '\n'
            if not self.hasWinner():
                # next player's turn
                self.cur_player += self.direction
                if self.cur_player >= len(self.players):
                    self.cur_player = 0
                if self.cur_player < 0:
                    self.cur_player = len(self.players) - 1

                # get the image for the next play
                gamefilename = raw_input("Filename of image? ")
                filepre = "images/"
                gamefilename = filepre + gamefilename

                # process the image
                self.lastcard = unoimage.topcard(gamefilename)
                print "Top Card is:",self.lastcard
                self.comphand = unoimage.hand(gamefilename)
                print "Computer Hand is:",self.comphand

                # deal with action cards
                # Skip a Player
                if self.lastcard.getValue() == 'Skip':
                    print "Player %s Gets Skipped!"
                    self.cur_player += self.direction
                    if self.cur_player >= len(self.players):
                        self.cur_player = 0
                    if self.cur_player < 0:
                        self.cur_player = len(self.players) - 1
                # Reverse the Direction of Play
                if self.lastcard.getValue() == 'Reverse':
                    print "Direction of Play is Reversed!"
                    self.direction = self.direction * (-1)
                

        return self.winner
