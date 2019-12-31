# This class contains algorithms of all agent techniques
# Here you can found:
# Greedy Algorithm
# Min Max Algorithm
# Min Max with Alpha Beta Prunning Algorithm
# Reinforcement Learning Algorithm
# However this class uses other class data structure values
# Also it modifies it from here

import board
import random

# This is the global variable for defining depth of the tree
depth = 0
stack = []
class game:

   """
        Initialize class varaibles with pit counts and number of pieces in each board
        Also initailize current score with 0 for each player and current player turn
   """
   def __init__(self, no_of_pits, pieces):
       self.current_game_board = board.board(no_of_pits, pieces)
       self.current_score = [0,0]
       self.current_player = 0

   '''
      This function switch the current player
   '''
   def changePlayerTurn(self):
      # this value stored in class variable so all of the function can use it
      self.current_player = (self.current_player + 1) % 2
      
   '''
      This function update the current scores for the current player
   '''
   def updateScore(self, score):
      # Score value added to current player score
      self.current_score[self.current_player] = self.current_score[self.current_player] + score
      
   '''
      This function returns True if game is end
      or it will return False otherwise
   '''
   def checkGameStatus(self):
      if self.current_game_board.isEmptyBoard():
         return False
      else:
         return True

   '''
      This function get win this game currently
      Also it return the winning player once called after the game is over
   '''
   def getCurrentWinner(self):
      return max(xrange(2), key=self.current_score.__getitem__)

   '''
      This function prints move of the current player in the console
   '''
   def printMove(self, value):
      if value > 6:
         value = value - 6
      else:
         value = value + 1
      print("                                                                         Player {0} choosed {1} ".format(self.current_player, value))
      
   '''
      This is the Naive Agent
   '''
   def naiveAgent(self):         
      # Random choice from the current choices
      pit = random.choice(self.current_game_board.getCurrentChoices(self.current_player))

      # Make moves and switchting the player
      self.printMove(pit)
      score = self.current_game_board.move(pit, False, self.current_score)
      self.updateScore(score)
      self.changePlayerTurn()
      return pit

   '''
      This is the greedy agent
   '''
   def greedyAgent(self):   
      # Gets current choices for this agent
      max_score = float("-inf")
      max_move = 0
      moves = self.current_game_board.getCurrentChoices(self.current_player)
      isCloneMove = True

      # It finds the best move to play to increse the winning chances
      for move_option in moves:
         new_board = self.current_game_board.clone()
         new_board_score = new_board.move(move_option, isCloneMove, self.current_score)
         if new_board_score > max_score:
            max_score = new_board_score
            max_move = move_option
      pit = max_move

      # Make moves and switchting the player  
      self.printMove(pit)
      score = self.current_game_board.move(pit, False, self.current_score)
      self.updateScore(score)
      self.changePlayerTurn()
      return pit

   '''
      This is the Min Max agent
   '''
   def miniMaxValue(self, board, limit, player, checker = 0):
      # The function changes min/max utility based on the player passed

      # Getting class depth value
      global depth
      depth = depth + 1

      # If the board is half empty the game is over 
      if board.isEmptyBoard():
         return 0

      # Gets current choices for this agent
      max_score = float("-inf")
      max_move = 0
      moves = board.getCurrentChoices(player)
      isCloneMove = True

      # The algorithm take moves such that the selection is made based on maximizing one score and minimizing a different score at each step
      # First of all check if the game state is in the level just above the limit in the min max tree
      # Then Only check for maximum profit of the current player and return the best move
      if ((depth == (limit - 1)) or ((depth == limit) and (limit == 1))):
         for move_option in moves:         
            
            new_board = board.clone()
            new_board_score = new_board.move(move_option, isCloneMove, self.current_score)
                      
            if new_board_score > max_score:
               max_score = new_board_score
               max_move = move_option       

      # On any depth other than limit - 1 recursively call the function and get the best score of the opponent in the resulting stage of the current move
      # Calculate the ratio of the addition to current player score by the move, to best potential addition to the opponent score of the resulting game state by the move
      # Choose the move with maximum ratio
      else:
         max_ratio = float("-inf")

         # Iterate over all of the choices
         for move_option in moves:
            new_board = board.clone()
            new_player = (player + 1) % 2
            score = new_board.move(move_option, isCloneMove, self.current_score)

            # This is the recursion call for another player
            # This time will be minimizing the score for oppenents
            opponent_score = self.miniMaxValue(new_board, limit, new_player, depth)

            if opponent_score != 0:
               if float(score/opponent_score) > max_ratio:
                  max_score = score
                  max_ratio = float(score/opponent_score)
                  max_move = move_option
            else:
                  max_score = score
                  max_move = move_option

      if checker == 1:
            return max_move
      else:
            return max_score

   '''
      This is the Min Max agent
   '''            
   def minMaxAgent(self, limit):
      
      # It plays the game based on miniMaxValue function value
      # since the entire tree traversal is not good choice, a depth limit is provided
      # Getting class depth value
      global depth
      
      # Getting next move value
      pit = self.miniMaxValue(self.current_game_board, limit, self.current_player, 1)
      depth = depth - 1
      
      # Make moves and switchting the player  
      self.printMove(pit)
      score = self.current_game_board.move(pit, False, self.current_score)
      self.updateScore(score)
      self.changePlayerTurn()
      return pit

   '''
      This is the Min Max agent
   '''
   def GetAlphaBetaScore(self, board, limit, player, alpha, beta, checker = 0):
      # The function changes min/max utility with alpha beta prunning based on the player passed

      # Getting class depth value
      global depth
      depth = depth + 1

      # If the board is half empty the game is over 
      if board.isEmptyBoard():
         return 0

      # Gets current choices for this agent
      max_score = float("-inf")
      max_move = 0
      moves = board.getCurrentChoices(player)
      isCloneMove = True


      # The algorithm take moves such that the selection is made based on maximizing one score and minimizing a different score at each step
      # Also it prunes the some of the tree to avoid bigger space requirement and to decrease time complexity
      # First of all check if the game state is in the level just above the limit in the min max tree
      # Then Only check for maximum profit of the current player and return the best move
      if ((depth == (limit - 1)) or ((depth == limit) and (limit == 1))):
         for move_option in moves:         
            
            new_board = board.clone()
            new_board_score = new_board.move(move_option, isCloneMove, self.current_score)
                      
            if new_board_score > max_score:
               max_score = new_board_score
               max_move = move_option   

      # On any depth other than limit - 1 recursively call the function and get the best score of the opponent in the resulting stage of the current move
      # Calculate the ratio of the addition to current player score by the move, to best potential addition to the opponent score of the resulting game state by the move
      # Choose the move with maximum ratio
      else:
         max_ratio = float("-inf")

         # Iterate over all of the choices
         for move_option in moves:
            new_board = board.clone()
            new_player = (player + 1) % 2
            score = new_board.move(move_option, isCloneMove, self.current_score)

            # if new score is smaller than alpha value then prune rest of tree branch
            if (score <= alpha):
               return score
            # if new score is greater than beta value then prune rest of tree branch
            if (score >= beta):
               return score
            
            # This is the recursion call for another player
            # This time will be minimizing the score for oppenents
            opponent_score = self.GetAlphaBetaScore(new_board, limit, new_player, alpha + score, beta + score)

            if opponent_score != 0:
               if float(score/opponent_score) > max_ratio:
                  max_score = score
                  max_ratio = float(score/opponent_score)
                  max_move = move_option
            else:
                  max_score = score
                  max_move = move_option

      if checker == 1:
            return max_move
      else:
            return max_score         
                  
   def AlphaBetaPlay(self, limit):
      # It plays the game based on modified GetAlphaBetaScore function value
      # since the entire tree traversal is not optimal, a depth limit is provided
      # Getting class depth value
      global depth
      
      #choosing a pit
      alpha = -float('inf')
      beta = -alpha

      # Getting next move value
      pit = self.GetAlphaBetaScore(self.current_game_board, limit, self.current_player, alpha, beta, 1)
      depth = depth - 1

      # Make moves and switchting the player  
      self.printMove(pit)
      score = self.current_game_board.move(pit, False, self.current_score)
      self.updateScore(score)
      self.changePlayerTurn()
      return pit

   '''
      This function switch the current player
   '''
   def addtostack(self,x,y,z):
      global stack
      stack.append([x,y,z])

   """
      This is the reinforcement learning agent
   """
   def rlagent(self, board):
       # A simple reinforcement learning agent 
       # first the agent is trained a small number of times
      global stack
      x = 0
      moves = self.current_game_board.getCurrentChoices(self.current_player)
      possibilities = []
      pit = random.choice(moves)
      
      # it finds possible solution from previous results and make optimal choice 
      for i in stack:
         if i[0] == tuple(board):
            possibilities.append(i)

      # If there was same state in the dataset then it checks rewards if it is higher then it will choose that pit
      for poss in possibilities:
         if poss[2] >= 0:
             for choice in moves:
                if poss[1]==choice:
                    poss[2] = poss[2]+1
                    pit = poss[1]
      self.printMove(pit)
      score = self.current_game_board.move(pit, False, self.current_score)
      self.updateScore(score)
      self.changePlayerTurn()
      return pit

   """
      This function trains the agent by playing the games.
   """
   def trainAgent(self):
      l=[]
      for i in self.current_game_board.board:
          l.append(i)
      #print(tuple(l))
      pit = random.choice(self.current_game_board.getCurrentChoices(self.current_player))
      global stack
      # Make moves and switchting the player
      score = self.current_game_board.move(pit, False, self.current_score)
      if score>0:
          reward = 1
      else:
          reward = -1
      self.updateScore(score)
      self.addtostack(tuple(l), pit+1, reward)
      self.changePlayerTurn()

   """
      This function starts the game
   """
   def Play(self):
      '''
         It play the game until a end of the game state is not reached
      '''
      # Asking for input from the user
      global stack
      x = 0
      # Getting previously trained data
      file=open("data.txt","r")
      for line in file:
         stack.append(line)
      stack = [y.strip() for y in stack]
      print("Enter 1 for Naive Agent")
      print("Enter 2 for Greedy Agent")
      print("Enter 3 for Min Max Agent")
      print("Enter 4 for Min Max with alpha beta Agent")
      print("Enter 5 for reinforcement learning Agent")
      player = [0,0]
      # For Player 0
      while player[0] not in [1,2,3,4,5]:
         try:
            # It will take 1, 2, 3, and 4 as a input only
            player[0] = int(input("Enter number for player 0:"))
            if player[0] not in [1,2,3,4,5]:
               print("Please enter correct number")
         except:
            print("Please provide valid input")
      # For Player 1
      while player[1] not in [1,2,3,4,5]:
         try:
            # It will take 1, 2, 3, and 4 as a input only
            player[1] = int(input("Enter number for player 1:"))
            if player[1] not in [1,2,3,4,5]:
               print("Please enter correct number")
         except:
            print("Please provide valid input")

      print("----------------------------------------------------")
      print("                      Initial Board:")
      print("----------------------------------------------------")
      self.current_game_board.printBoard(self.current_score)
      player0_stack = []
      player1_stack = []
      # Starts playing the game
      # It will choose agent according to the give output
      while self.checkGameStatus():
         if self.current_player == 0:
            current_state = []
            pit = 0
            if player[0] == 1:
               pit = self.naiveAgent()
            elif player[0] == 2:
               pit = self.greedyAgent()
            elif player[0] == 3:
               pit = self.minMaxAgent(2)
            elif player[0] == 4:
               pit = self.AlphaBetaPlay(2)
            elif player[0] == 5:
               pit = self.rlagent(self.current_game_board.board)
            player0_stack.append([tuple(self.current_game_board.board), pit, 0])
            self.current_game_board.printBoard(self.current_score)
         else:
            current_state = []
            pit = 0
            if player[1] == 1:
               pit = self.naiveAgent()
            elif player[1] == 2:
               pit = self.greedyAgent()
            elif player[1] == 3:
               pit = self.minMaxAgent(2)
            elif player[1] == 4:
               pit = self.AlphaBetaPlay(2)
            elif player[1] == 5:
               pit = self.rlagent(self.current_game_board.board)
            player1_stack.append([tuple(self.current_game_board.board), pit, 0])
            self.current_game_board.printBoard(self.current_score)

      # adding reward to winning player
      if self.current_score[0] > self.current_score[1]:
         for x in player0_stack:
            x[2] = x[2] + 1
      else:
         for x in player1_stack:
            x[2] = x[2] + 1
      
      player0_stack.extend(player1_stack)
      self.current_game_board.getAllPiecesElements(self.current_score)

      # Adding new states and moves to the file
      f = open("data.txt","a")
      for i in player0_stack:
         f.writelines(str(i))
         f.write("\n")
      self.printGame()
      
   """
      This function declares the result of the current game
      The output will be
      Player 0 won or
      Player 1 won or
      It's a draw
   """
   def printGame(self):
      print("----------------------------------------------------")
      print("                      Final Board:")
      print("----------------------------------------------------")
      self.current_game_board.printBoard(self.current_score)
      if self.current_score[0]>self.current_score[1]:
         print("")
         print("##########################################################")
         print("                Player 0 won!!                            ")
         print("##########################################################")
         print("")
      elif self.current_score[1]>self.current_score[0]:
         print("")
         print("##########################################################")
         print("                Player 1 won!!                            ")
         print("##########################################################")
         print("")
      else:
         print("")
         print("##########################################################")
         print("                It's a draw!!                            ")
         print("##########################################################")
         print("")

      
   def __main__(self):
      self.Play()

# This is the driver function for playing the games
# Initialize the game and starts playing
# You can pass different pieces for each pits or different number of pits
# Here 14 is the number of pits
# 5 is the number of pieces in each pit
newgame = game(14, 5)
newgame.__main__()



