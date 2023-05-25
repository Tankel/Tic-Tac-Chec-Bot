def check_four_numbers(board, aremypieces):
    target_numbers = {1, 2, 3, 4} if aremypieces else {-1, -2, -3, -4}

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


def findMissingNumbers(board, pieceColor):
    numbers = {1, 2, 3, 4} if pieceColor == 1 else {-1, -2, -3, -4}
    present_numbers = set()

    for row in board:
        for num in row:
            if num != 0:
                if (num > 0 and pieceColor == 1) or (num < 0 and pieceColor == -1):
                    present_numbers.add(num)

    missing_numbers = list(numbers - present_numbers)
    return missing_numbers


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

def maxAlignedValue(board, number_sign):
    target_numbers = {1, 2, 3, 4} if number_sign == 1 else {-1, -2, -3, -4}
    max_value = 0
    aligned_numbers = set()
    missing_numbers = set(target_numbers)
    missing_positions = set()

    # Check horizontally
    for row in range(len(board)):
        aligned_values = [board[row][col] for col in range(len(board[row])) if board[row][col] != 0 and board[row][col] in target_numbers]
        if len(aligned_values) > max_value:
            max_value = len(aligned_values)
            aligned_numbers = set(aligned_values)
            missing_numbers = target_numbers - aligned_numbers
            missing_positions = {(row, col) for col in range(len(board[row])) if (board[row][col] == 0 or board[row][col] not in target_numbers)}

    # Check vertically
    for col in range(len(board[0])):
        aligned_values = [board[row][col] for row in range(len(board)) if board[row][col] != 0 and board[row][col] in target_numbers]
        if len(aligned_values) > max_value:
            max_value = len(aligned_values)
            aligned_numbers = set(aligned_values)
            missing_numbers = target_numbers - aligned_numbers
            missing_positions = {(row, col) for row in range(len(board)) if (board[row][col] == 0 or board[row][col] not in target_numbers)}

    # Check diagonals
    diagonal_values = [board[i][i] for i in range(len(board)) if board[i][i] != 0 and board[i][i] in target_numbers]
    print(diagonal_values)
    if len(diagonal_values) > max_value:
        max_value = len(diagonal_values)
        aligned_numbers = set(diagonal_values)
        missing_numbers = target_numbers - aligned_numbers
        missing_positions = {(i, i) for i in range(len(board)) if (board[i][i] == 0 or board[i][i] not in target_numbers)}

    reverse_diagonal_values = [board[i][len(board)-1-i] for i in range(len(board)) if board[i][len(board)-1-i] != 0 and board[i][len(board)-1-i] in target_numbers]
    print(reverse_diagonal_values)
    if len(reverse_diagonal_values) > max_value:
        max_value = len(reverse_diagonal_values)
        aligned_numbers = set(reverse_diagonal_values)
        missing_numbers = target_numbers - aligned_numbers
        missing_positions = {(i, len(board)-1-i) for i in range(len(board)) if (board[i][len(board)-1-i] == 0 or board[i][len(board)-1-i] not in target_numbers)}

    return max_value, aligned_numbers, missing_numbers, missing_positions

def is_valid_move(piece, x, y, new_x, new_y):
    # Check if the piece is a pawn
    if abs(piece) == 1:
        # Pawns can move one step forward (up for white, down for black)
        if (piece == 1 and new_x == x - 1 and new_y == y) or (piece == -1 and new_x == x + 1 and new_y == y):
            return True
        # Pawns can also capture diagonally
        if (piece == 1 and new_x == x - 1 and abs(new_y - y) == 1) or (piece == -1 and new_x == x + 1 and abs(new_y - y) == 1):
            return True

    # Check if the piece is a bishop
    if abs(piece) == 2:
        # Bishops can move diagonally
        if abs(new_x - x) == abs(new_y - y):
            return True

    # Check if the piece is a knight
    if abs(piece) == 3:
        # Knights can move in an L-shape
        if abs(new_x - x) == 2 and abs(new_y - y) == 1:
            return True
        if abs(new_x - x) == 1 and abs(new_y - y) == 2:
            return True

    # Check if the piece is a rook
    if abs(piece) == 4:
        # Rooks can move horizontally or vertically
        if new_x == x or new_y == y:
            return True

    return False

def can_pawn_move_vertically(board, current_position, target_position):
    current_row, current_col = current_position
    target_row, target_col = target_position

    if abs(target_row-current_row) == abs(target_col-current_col) == 1 and board[target_row][target_col] != 0:
        return True

    if current_col != target_col:
        return False  # Pawns can only move vertically, not horizontally

    if current_row == target_row:
        return False  # The pawn is already on the target position

    if current_row < target_row:
        # Check if there are any pieces blocking the pawn's vertical movement
        for row in range(current_row + 1, target_row):
            if board[row][current_col] != 0:
                return False  # There is a piece blocking the pawn's path

    else:  # current_row > target_row
        # Check if there are any pieces blocking the pawn's vertical movement
        for row in range(target_row + 1, current_row):
            if board[row][current_col] != 0:
                return False  # There is a piece blocking the pawn's path

    return True  # The pawn can move vertically to the target position

def isValidMove(board, piece, target_position):
    # Check if the piece is already aligned or missing
    if piece == 0:
        return True


    for piece, position in zip(piece, target_position):
        x, y = position
        if piece == 1 or piece == -1:
            row = -1
            col = -1
            for i in range(4):
                for j in range(4):
                    if board[i][j] == piece:
                        row = i
                        col = j
                        break
            if(can_pawn_move_vertically(board, (row,col), (x,y))): 
                return True
            
        elif piece == 2 or piece == -2:
            row = -1
            col = -1
            for i in range(4):
                for j in range(4):
                    if board[i][j] == piece:
                        row = i
                        col = j
                        break
            # Bishop can go to cells with the same parity as the initial position
            if (x + y) % 2 == (row + col) % 2:
                return True

        elif piece == 3 or piece == -3:
            # Knight can go to any cell, no restrictions
            return True

        elif piece == 4 or piece == -4:
            # Rook can go to any cell, no restrictions
            return True

        # Invalid piece value
        return False
def checkVictory( board, piecesColor):
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

board = [
    [2, 0, 0, 0],
    [0, 3, 0, 0],
    [0, -3, 1, 1],
    [0, 0, 0, 0]
]

if checkVictory(board, 1):
    print("YES")
else:
    print("NO")

board2 = [
    [0, 0, 0, 0],
    [-2, 0, -3, -4],
    [0, -1, 0, 0],
    [0, 0, 0, 0]
]
number_sign = -1

#max_value, aligned_numbers, missing_numbers, missing_positions = maxAlignedValue(board, number_sign)
#print("mmm:", aligned_numbers, missing_numbers, missing_positions)

#if isValidMove(board, missing_numbers, missing_positions):
    #print("Si es posible alinea")
#else:
    #print("NO es posible")
#max_value, aligned_numbers, missing_numbers, missing_positions = maxAlignedValue(board, number_sign)
#print("Max aligned value:", max_value)
#print("Aligned numbers:", aligned_numbers)
#print("Missing numbers:", missing_numbers)
#print("Missing positions:", missing_positions)

#player1_count = countCenterPieces(board, 1)
#player2_count = countCenterPieces(board, -1)

#print("Player 1:", player1_count)
#print("Player 2:", player2_count)
#max_value, aligned_numbers = max_aligned_value(board, number_sign=1)
#print(f"The maximum value of aligned pieces in the board is: {max_value}")
#print(f"The numbers aligned are: {aligned_numbers}")

#missing_nums = findMissingNumbers(board, -1)
#print("Missing numbers:", missing_nums)

lista = []
for i in range(10):
    lista.append(((i,i+4),4))


for i, j in lista:
    i1, i2 = i
    #print(i1, i2, i, j)
# print(lista)
# false -1, -2, -3, -4
# true 1, 2, 3, 4
'''
if check_four_numbers(board, False):
    print("There are four numbers aligned.")
else:
    print("No alignment of four numbers found.")
'''
#max_value = max_aligned_value(board, -1)
#print(f"The maximum value of aligned pieces in the board is: {max_value}")