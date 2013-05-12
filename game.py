# Emily Schultz (ess2183)
# May 15, 2013
# Visual Interfaces Final Project
# Game Class

import card
import Image            #necessary?
import unoimage
import numpy as np    #necessary?

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
        print "Player 1 Name: Computer"
        for i in range(0,num_players - 1):
            name = raw_input("Player 2 Name: ")
            self.players.append(name)
            self.scores.append(0)
        # who goes first
        self.cur_player = 0

    def setupDeck(self):
        '''Begin the game by setting up the deck status.'''
        startfilename = raw_input("Filename of starting image? ")
        # all images in images folder
        filepre = "images/"
        startfilename = filepre + startfilename
        
        self.lastcard = unoimage.topcard(startfilename)
        self.comphand = unoimage.hand(startfilename)
        
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
    
    def getCompMove(self, **kwargs):
        '''Return a legal move for the computer to make given his hand.'''
        possible_cards = []
        
        # check for those in hand of the same color
        curcolor = self.lastcard.getColor()
        if curcolor == 'black':
            #Last card was a wild, need to know what they called it
            curcolor = kwargs['wild']
                
        # check for those in hand of the same value
        curvalue = self.lastcard.getValue()

        for c in self.comphand:
            if curvalue == c.getValue() or curcolor == c.getColor():
                possible_cards.append(c)
            elif c.getValue() == 'Wild' or c.getValue() == 'Wild Draw Four':
                possible_cards.append(c)

        if not possible_cards:
            return 'DRAW'
        else:
            # strategy for comp move here
            return possible_cards[0]
    def hasWinner(self):
        '''Return true if game has been won (ie player has reached 0 cards)'''
        return self.winner
    def play(self):
        '''Play a game of UNO.'''
        while(not self.hasWinner()):
            # stuff goes here
            'hi'
        return self.winner





















