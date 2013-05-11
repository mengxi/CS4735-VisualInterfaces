# Emily Schultz (ess2183)
# May 15, 2013
# Visual Interfaces Final Project
# Game Class

import card
import unoimage

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
        self.players.append('Computer')
        print "Player 1 Name: Computer"
        for i in range(0,num_players - 1):
            name = raw_input("Player 2 Name: ")
            self.players.append(name)
        # who goes first
        self.cur_player = 0

    def setupDeck(self):
        '''Begin the game by setting up the deck status.'''
        startfilename = raw_input("Filename of starting image? ")
        
        
    def getCurrentPlayer(self):
        '''Return who will move next.'''
        return self.players[self.cur_player]
    def getNumPlayers(self):
        '''Return the number of players.'''
        return len(self.players)

    def 
