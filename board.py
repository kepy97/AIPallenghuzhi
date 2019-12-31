# This class contains the size of the board and a list of pits
# 2X7 pits board- 7 pits of 1 row belong to player 1 and 7 pits on other row belong to player 2(i.e. one player on each side)
# Each player start with 5 pieces in each pit (i.e. each player gets 35 pieces)
# End up with the most pieces
import copy

class board:

    """
        Initialize class varaibles with pit counts and number of pieces in each board
    """
    def __init__(self, no_of_pits, pieces):
        self.board = [pieces] * no_of_pits
        self.no_of_pits = no_of_pits
        self.pieces = pieces

    """
        This function prints the current state of the game with their score
    """
    def printBoard(self, current_score):
        size = int(self.no_of_pits/2)
        new_list = self.board[::-1]
        print("")
        print("Current position")
        print("")
        print("")
        
        print("                ######## Player 0 ########")
        print("")      
        print("            Position | 7 | 6 | 5 | 4 | 3 | 2 | 1 |")
        print("            --------------------------------------")
        print("            Count    | " + ' | '.join( [str(pit) for pit in new_list[size:] ] ) + " |")
        
        print("")
        print("Player 1 Pot                                  Player 0 Pot")
        print("     {0}                                             {1}".format(current_score[1],current_score[0]))
        print("")
        
        print("               ######## Player 1 ########")
        print("")
        print("            Position | 1 | 2 | 3 | 4 | 5 | 6 | 7 |")
        print("            --------------------------------------")
        print("            Count    | " + ' | '.join( [str(pit) for pit in self.board[size:] ] ) + " |")
        print("")
        print("")
        
    '''
        This function checks if any of the side pieces are zero or not.
        If it is zero then it returns true and game will be over.
    '''
    def isEmptyBoard(self):

        # check if any one side of the board leaves the player with no option to choose from
        return self.getCurrentChoices(0) == [] or self.getCurrentChoices(1) == []
        
    '''
        This function returns the copy of the original board
    '''
    def clone(self):
        
        new = board(len(self.board),self.pieces)
        new.board = copy.copy(self.board)
        return new
    
    '''
        This function returns a list of indices the current player is eligable to choose from
        their side of the board
    '''
    def getCurrentChoices(self, current_player):
        
        choices = []
        side = []
        size = int(len(self.board)/2)

        if current_player == 0:
            for index in range(0,size):
                if self.board[index] != 0:
                    choices.append(index)
        else:
            for index in range(size,size*2):
                if self.board[index] != 0:
                    choices.append(index)
            
        return choices
                
    '''
        This function increments the current pit
    '''
    def getNextPitIndex(self, pit):
        return (pit + 1) % self.no_of_pits
    
    '''
        This function the start index and then
        the move ends when there the next pit is empty
        the move function returns a score
    '''
    def move(self, start, isCloneMove, current_score):
        #print the board before starting a move
        if isCloneMove ==False:
            self.getFourPiecesElements(current_score)

        #scores, get coins to move around and set the start pit to zero coins
        score = 0
        coins = self.board[start]
        self.board[start] = 0

        #move the coins to corresponding pits
        for coin in range(coins):
            start = self.getNextPitIndex(start)
            self.board[start] = self.board[start] + 1            

        nextIndex = self.getNextPitIndex(start)

        #check if next pit after the move is empty or not
        #if empty the move is over, take the coin from the consecutive pit to return as score
        #if not empty, recursively move again starting from the next pit
        if self.board[nextIndex] == 0:
            score_pit = self.getNextPitIndex(nextIndex)
            score = self.board[score_pit]

            if isCloneMove == False:
                self.getFourPiecesElements(current_score)
            
            self.board[score_pit] = 0
                    
        else:
            score = self.move(nextIndex, isCloneMove, current_score)

        if isCloneMove == False:
            self.getFourPiecesElements(current_score)
        return score

    """
        This function get those that have four pieces and add to the corresponding player's pit
    """
    def getFourPiecesElements(self, current_score):
        for i in range(len(self.board)):
            if self.board[i] == 4:
                if i > 6:
                    self.board[i] = 0
                    current_score[1] = current_score[1] + 4
                else:
                    self.board[i] = 0
                    current_score[0] = current_score[0] + 4

    """
        This function get all pieces to each players pit
    """
    def getAllPiecesElements(self, current_score):
        for i in range(len(self.board)):
            if self.board[i] != 0:
                if i > 6:
                    current_score[1] = current_score[1] + self.board[i]
                    self.board[i] = 0
                else:
                    current_score[0] = current_score[0] + self.board[i]
                    self.board[i] = 0


            







