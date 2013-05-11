# Emily Schultz (ess2183)
# May 15, 2013
# Visual Interfaces Final Project
# Card Class

class Card:
    '''Class for each card, with a type, value, and color.'''

    def __init__(self, value = '0', color = 'black'):
        '''Instantiate the card.'''
        #color = 'red','green','blue','yellow','black'
        self.color = color
        self.value = value
        #type:
        try:
            int(self.value)
            #number = 0 to 9
            self.type = 'number'
        except ValueError:
            #action = 'skip','draw two','reverse','wild','wild draw four'
            self.type = 'action'

    def getValue(self):
        '''Return the value of the card.'''
        return self.value
    def getColor(self):
        '''Return the color of the card.'''
        return self.color
    def isColor(self):
        '''Return true if it is a color card (vs. a wild).'''
        return (bool)(self.color != 'black')
    def isAction(self):
        '''Return true if it is an action card.'''
        return (bool)(self.type == 'action')
