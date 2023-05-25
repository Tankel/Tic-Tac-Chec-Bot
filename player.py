"""
Value code for each piece is as follows:
    - pawn = 1 for white, -1 for black
    - bishop =  2 for white, -2 for black
    - knight =  3 for white, -3 for black
    - rook =  4 for white, -4 for black

* It is recommended to store the direction of movement of both your pawn and opponent's pawn.

"""
import math
import copy
import random
import time

class TTCPlayer:
    # valuesCode is a list containing the value code that you must use to represent your pieces over the board. 
    # The sign of the value code will tell you if you are playing as white or black pieces.
    # The values are in the order: pawn, bishop, knight, rook
    def __init__(self, name):
        self.name = name
        self.pawnDirection = -1
        self.currentTurn = -1

        self.piecesOnBoard = [0] * 5

    def setColor(self, piecesColor):
        self.piecesCode = [0, 1, 2, 3, 4]
        self.piecesCode = [x*piecesColor for x in self.piecesCode]
        self.piecesColor = piecesColor

    def __updatePawnDirection(self, board):
        # If the pawn is in the limit of the board, it should reverse
        if self.piecesColor in board[0]:
            self.pawnDirection = 1
        
        # If the pawn is in the start of the board, it should go forward
        if self.piecesColor in board[3]:
            self.pawnDirection = -1

    def __sameSign(self, a, b):
        return ((a < 0 and b < 0) or (a > 0  and b > 0))
    
    def __isInsideBoard(self, row, col):
        return (row >= 0 and row < 4 and col >= 0 and col < 4)

        # Function to check whether a movement was a movement or not
    # If it was a movement, it also checks if it was a capture or not.
    # For a movement to be classified as a capture, 2 conditions have to occur
    # 1. Only 2 squares changed value
    # 2. One square has to change from used to empty and the other from used to used with different color    
    def __wasPieceMovement(self, oldBoard, newBoard):
        changedSquares = []

        for i in range(4):
            for j in range(4):
                if oldBoard[i][j] != newBoard[i][j]:
                    changedSquares.append((i, j))

        if len(changedSquares) != 2:
            return False, False
        
        def areChangesFromCapture(row1, col1, row2, col2):
            return (newBoard[row1][col1] == 0
                    and oldBoard[row2][col2] != 0 
                    and newBoard[row2][col2] == oldBoard[row1][col1])
        
        def areChangesFromMovement(row1, col1, row2, col2):
            return (newBoard[row1][col1] == 0
                    and newBoard[row2][col2] == oldBoard[row1][col1])
        
        wasMovement = (areChangesFromMovement(changedSquares[0][0], changedSquares[0][1], changedSquares[1][0], changedSquares[1][1]) 
                or areChangesFromMovement(changedSquares[1][0], changedSquares[1][1], changedSquares[0][0], changedSquares[0][1]))
        
        wasCapture = (areChangesFromCapture(changedSquares[0][0], changedSquares[0][1], changedSquares[1][0], changedSquares[1][1]) 
                or areChangesFromCapture(changedSquares[1][0], changedSquares[1][1], changedSquares[0][0], changedSquares[0][1]))

        return (wasMovement, wasCapture)

    def __getPawnValidMovements(self, position, board, pawnDirection):
        validMovements = []
        
        row = position[0]
        col = position[1]

        # Move 1 to the front
        newRow = row + pawnDirection
        if self.__isInsideBoard(newRow, col) and board[newRow][col] == 0:
            validMovements.append((newRow, col))

        # Attack to the left
        newCol = col - 1
        if self.__isInsideBoard(newRow, newCol) and board[newRow][newCol] != 0 and not self.__sameSign(board[newRow][newCol], board[row][col]):
            validMovements.append((newRow, newCol))

        # Attack to the right
        newCol = col + 1
        if self.__isInsideBoard(newRow, newCol) and board[newRow][newCol] != 0 and not self.__sameSign(board[newRow][newCol], board[row][col]):
            validMovements.append((newRow, newCol))

        return validMovements
    
    def __getBishopValidMovements(self, position, board):
        validMovements = []

        row = position[0]
        col = position[1]

        # To check whether I already encountered a piece in this diagonal or not
        # 0 -> Up-Left Diagonal
        # 1 -> Up-Right Diagonal
        # 2 -> Down-Left Diagonal
        # 3 -> Down-Right Diagonal
        diagEncounteredPiece = [False] * 4

        # Describe the direction of the movement for the bishop in the same
        # order as described above
        movDirection = [[-1, -1],
                     [-1, 1],
                     [1, -1],
                     [1, 1]]

        # A bishop can move at most 3 squares
        for i in range(1,4):
            # Check 4 directions of movement
            for j in range(4):
                newCol = col + i * movDirection[j][0]
                newRow = row + i * movDirection[j][1]

                # If I haven't found a piece yet in this direction and its inside the board
                if not diagEncounteredPiece[j] and self.__isInsideBoard(newRow, newCol):
                    # If the proposed square its occupied
                    if board[newRow][newCol] != 0:
                        # If the piece that occupies the square its from the opponent, then its a valid movement
                        if not self.__sameSign(board[row][col], board[newRow][newCol]):
                            validMovements.append((newRow, newCol))
                        diagEncounteredPiece[j] = True
                    else: # If not, just append the movement
                        validMovements.append((newRow, newCol))

        return validMovements

    def __getKnightValidMovements(self, position, board):
        validMovements = []

        row = position[0]
        col = position[1]


        # Describe the movements of the knight
        movements = [[-2, 1],
                     [-1, 2],
                     [1, 2],
                     [2, 1],
                     [2, -1],
                     [1, -2],
                     [-1, -2],
                     [-2, -1]]
        
        # Loop through all possible movements
        for move in movements:
            newRow = row + move[0]
            newCol = col + move[1]

            # For the knight we just need to check if the new square is valid and it is not occupied by a piece of the same color
            if self.__isInsideBoard(newRow, newCol) and not self.__sameSign(board[row][col], board[newRow][newCol]):
                validMovements.append((newRow, newCol))

        return validMovements

    def __getRookValidMovements(self, position, board):
        validMovements = []

        row = position[0]
        col = position[1]

        # Checks whether or not I have found a piece in this direction
        # 0 - Up
        # 1 - Right
        # 2 - Down
        # 3 - Left
        dirPieceEncountered = [False] * 4

        # Describe the direction of movement for the rook
        # The order is the same as described above
        movDirection = [[-1, 0],
                        [0, 1],
                        [1, 0],
                        [0, -1]]
        
        # The rook can move maximum 3 squares
        for i in range(1, 4):
            # Loop through all possible movements
            for j in range(4):
                newRow = row + i * movDirection[j][0]
                newCol = col + i * movDirection[j][1]

                if not dirPieceEncountered[j] and self.__isInsideBoard(newRow, newCol):
                    if board[newRow][newCol] != 0:
                        if not self.__sameSign(board[newRow][newCol], board[row][col]):
                            validMovements.append((newRow, newCol))
                        dirPieceEncountered[j] = True
                    else:
                        validMovements.append((newRow, newCol))

        return validMovements        

    def __getValidMovements(self, pieceCode, position, board):
        if abs(pieceCode) == 1:
            return self.__getPawnValidMovements(position, board, self.pawnDirection)
        elif abs(pieceCode) == 2:
            return self.__getBishopValidMovements(position, board)
        elif abs(pieceCode) == 3:
            return self.__getKnightValidMovements(position, board)
        elif abs(pieceCode) == 4:
            return self.__getRookValidMovements(position, board)
        else:
            print("Piece ", pieceCode, " not recognized")
            return []

    def __getCurrentValidMovements(self, board, piecesColor):
        pieces = [1, 2, 3, 4] if piecesColor == 1 else [-1, -2, -3, -4]
        validMovements = []
        
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j]-1 in pieces:
                    pieceCode = pieces[board[i][j]-1]
                    #piecesOnBoard.append(board[i][j])
                    validMovements.append((self.__getValidMovements(pieceCode, (i, j), board), pieceCode))

        return validMovements

    def __movePiece(self, currentBoard):
        #print(self.name, "::moveRandomPiece")
        row = -1
        col = -1

        #Copy the board
        board = [row[:] for row in currentBoard]
        #Set bestScore to a very small value
        bestScore = -math.inf

        move = None
        bestPiece = None
        #For every possible move
        pieces = self.getMissingPieces(board, self.piecesColor)

        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    for k in pieces:
                        #Put 'O' in the available position
                        board[i][j] = k

                        #Call minimax to see how good the move is
                        #isMaximizing is false because it would be the human's turn
                        #Set alpha to a very small value and beta to a very large one
                        score = self.minimaxAB(board, 0, -math.inf, math.inf, False)

                        #Undo the change to the board
                        board[i][j] = 0

                        #If the score is bigger than the current best score
                        if score > bestScore:
                            #Set bestScore to score and save the move
                            bestScore = score
                            lastPosition = [i, j]
                            move = [i, j]
                            bestPiece = k

                elif board[i][j] in self.piecesCode and board[i][j] != 0:
                    kValidMoves = self.__getValidMovements(board[i][j], (i,j), board)
                    for coor in kValidMoves:
                        #print(coor)
                        a, b = coor
                        #Put 'O' in the available position
                        pastPiece = board[a][b]
                        board[a][b] = board[i][j]

                        #Call minimax to see how good the move is
                        #isMaxismizing is false because it would be the human's turn
                        #Set alpha to a very small value and beta to a very large one
                        score = self.minimaxAB(board, 0, -math.inf, math.inf, False)

                        #Undo the change to the board
                        board[a][b] = pastPiece

                        #If the score is bigger than the current best score
                        if score > bestScore:
                            #Set bestScore to score and save the move
                            bestScore = score
                            lastPosition = [i, j]
                            move = [a, b]
                            bestPiece = board[i][j]


        #After we checked every move, return the best one
        #print("a", move)
        if move is None:
            print("ES NONE!!!")
        newRow, newCol = move
        row, col = lastPosition
        #validMovements = self.__getCurrentValidMovements(board, self.piecesColor)

        #if len(validMovements) == 0:
        #   return board
        
        #newRow, newCol, piece = self.minimaxAB(board, 0, -math.inf, math.inf, True, validMovements)
        #newRow, newCol = validMovements[random.randint(0, len(validMovements)-1)]


        board[row][col] = 0
        board[newRow][newCol] = bestPiece

        return board

    def __updatePiecesOnBoard(self, board):
        self.piecesOnBoard = [0] * 5

        for i in range(len(board)):
            for j in range(len(board[0])):
                if self.__sameSign(board[i][j], self.piecesColor):
                    self.piecesOnBoard[abs(board[i][j])] = 1

    def __putRandomPiece(self, board):
        piece = -1
        while(piece == -1 or self.piecesOnBoard[piece] != 0):
            piece = random.randint(1, 4)

        newRow = random.randint(0, 3)
        newCol = random.randint(0, 3)

        while (board[newRow][newCol] != 0):
            newRow = random.randint(0, 3)
            newCol = random.randint(0, 3)

        board[newRow][newCol] = piece * self.piecesColor

        # If a new pawn is put on the board, we should reset its direction.
        if piece == 1:
            self.pawnDirection = -1

        return board
    
    def countCenterPieces(board, player):
        center = [(1, 1), (1, 2), (2, 1), (2, 2)]  # Coordinates of the center square

        count = 0  # Counter for the player's pieces

        for x, y in center:
            piece = board[x][y]
            if player == 1 and piece in [1, 2, 3, 4]:
                count += 1
            elif player == -1 and piece in [-1, -2, -3, -4]:
                count += 1

        return count
    
    def play(self, board):
        start = time.time()
        self.currentTurn += 1
        self.__updatePiecesOnBoard(board)

        originalBoard = copy.deepcopy(board)

        # We put a limit since there can be a really rare case when the only valid movement is a capture
        # And if in that moment it happens that you can no longer make any capture, it will cicle. That's why we put a limit.
        for _ in range(1000):
            if self.currentTurn < 3: # or sum(self.piecesOnBoard) == 0:
                newBoard = self.__putRandomPiece(board)
            else: # All the pieces are on the board
                newBoard = self.__movePiece(board)

            _, wasCapture = self.__wasPieceMovement(originalBoard, newBoard)

            if wasCapture:
                if self.availableCaptures > 0:
                    self.availableCaptures -= 1
                else:
                    board = copy.deepcopy(originalBoard)
                    continue

            if newBoard != originalBoard:
                break
        
        self.__updatePawnDirection(newBoard)
        print("Time taken: ", time.time() - start)
        
        #for i in newBoard:
            #print(i)
        #print(newBoard, flush=True)

        #return utils.updateSyncBoard(syncBoard, newBoard)
        return newBoard

    #Minimax with Alpha-Beta pruning
    def minimaxAB(self, currentBoard, depth, alpha, beta, isMaximizing):
        #Copy the board
        board = [row[:] for row in currentBoard]

        #Evaluate the current position
        result = self.evaluatePosition(board)

        #If someone won
        if result == 10 or result == -10 or depth == 6:
            #Set eval to the value of the result in the dictionary
            
            #If the bot won, return the evaluation minus the depth, we want the fastest way to win
            #If the human won, return the evaluation plus the depth, the human would want the fastest win
            return result - depth if result > 0 else result + depth

        #When is the bot's turn
        if isMaximizing:
            #Set maxEval to a very small value
            maxEval = -math.inf

            #For every possible position in the board
            validMovements = self.__getCurrentValidMovements(board, self.piecesColor)  
            for coorx, piece in validMovements:
                #Put 'O' in the position
                for coor in coorx:
                    #print(coor)
                    i,j = coor
                    board[i][j] = piece

                    #New call to the minimax function with the new position
                    #Add one to the depth to know how many moves have been done
                    #isMaximizing is false because it would be the human's turn   
                    eval = self.minimaxAB(board, depth + 1, alpha, beta, False)

                    #Undo the move
                    board[i][j] = 0

                    #Set maxEval to the maximum between the current maxEval and the eval minimax returned
                    maxEval = max(maxEval, eval)
                    #Set alpha to the maximum between the current alpha and the eval minimax returned
                    alpha = max(alpha, eval)
                    #If beta is less or equal to alpha, we dont need to continue trying moves, so we break the loop
                    if beta <= alpha:
                        break

            #After all the moves, return the maxEval
            return maxEval    

        else:
            #Set minEval to a very large value
            minEval = math.inf

            #For every possible position in the board
            validMovements = self.__getCurrentValidMovements(board, self.piecesColor*-1)  
            for coorx, piece in validMovements:
                #Put 'O' in the position
                for coor in coorx:
                    i,j = coor
                    board[i][j] = piece

                    #New call to the minimax function with the new position
                    #Add one to the depth to know how many moves have been done
                    #isMaximizing is true because it would be the bot's turn    
                    eval = self.minimaxAB(board, depth + 1, alpha, beta, True)

                    #Undo the move
                    board[i][j] = 0

                    #Set minEval to the minimum between the current minEval and the eval minimax returned
                    minEval = min(minEval, eval)
                    #Set beta to the minimum between the current beta and the eval minimax returned
                    beta = min(beta, eval)
                    #If beta is less or equal to alpha, we dont need to continue trying moves, so we break the loop
                    if beta <= alpha:
                        break

            #After all the moves, return the minEval
            return minEval
    
    def evaluatePosition(self, board):
        
        if self.checkVictory(board, self.piecesColor):
            return 10
        elif self.checkVictory(board, self.piecesColor*-1):
            return -10
    
        myPiecesAligned = self.maxAlignedValue(board, self.piecesColor)
        opponentPiecesAligned = self.maxAlignedValue(board, self.piecesColor*-1)
        #if myPiecesAligned == opponentPiecesAligned:
            #return -1
        return myPiecesAligned - opponentPiecesAligned


    def checkVictory(self, board, piecesColor):
        target_numbers = {1, 2, 3, 4} if piecesColor == 1 else {-1, -2, -3, -4}

        # Check horizontally
        for row in board:
            if set(row) - {0} == target_numbers:
                return True

        # Check vertically
        for col in range(len(board[0])):
            column_values = [board[row][col] for row in range(len(board))]
            if set(column_values) - {0} == target_numbers:
                return True

        # Check diagonals
        diagonal_values = [board[i][i] for i in range(len(board))]
        if set(diagonal_values) - {0} == target_numbers:
            return True

        reverse_diagonal_values = [board[i][len(board)-1-i] for i in range(len(board))]
        if set(reverse_diagonal_values) - {0} == target_numbers:
            return True

        return False

    def getMissingPieces(self, board, pieceColor):
        numbers = {1, 2, 3, 4} if pieceColor == 1 else {-1, -2, -3, -4}
        present_numbers = set()

        for row in board:
            for num in row:
                if num != 0:
                    if (num > 0 and pieceColor == 1) or (num < 0 and pieceColor == -1):
                        present_numbers.add(num)

        missing_numbers = list(numbers - present_numbers)
        return missing_numbers

    def maxAlignedValue(self, board, piecesColor):
        target_numbers = {1, 2, 3, 4} if piecesColor == 1 else {-1, -2, -3, -4}
        max_value = 0

        # Check horizontally
        for row in board:
            aligned_values = [value for value in row if value != 0 and value in target_numbers]
            max_value = max(max_value, len(set(aligned_values)))

        # Check vertically
        for col in range(len(board[0])):
            aligned_values = [board[row][col] for row in range(len(board)) if board[row][col] != 0 and board[row][col] in target_numbers]
            max_value = max(max_value, len(set(aligned_values)))

        # Check diagonals
        diagonal_values = [board[i][i] for i in range(len(board)) if board[i][i] != 0 and board[i][i] in target_numbers]
        max_value = max(max_value, len(set(diagonal_values)))

        reverse_diagonal_values = [board[i][len(board)-1-i] for i in range(len(board)) if board[i][len(board)-1-i] != 0 and board[i][len(board)-1-i] in target_numbers]
        max_value = max(max_value, len(set(reverse_diagonal_values)))

        return max_value

    def reset(self):
        self.pawnDirection = -1
        self.piecesOnBoard = [0] * 5
        self.currentTurn = -1
        self.availableCaptures = 5