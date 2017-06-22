""" 
    TCSS 435 A.I.
    Programming Assignment #2: Pentago Game
    Brandon Chambers
"""


import random
import math

'''General Movement and Rotation ----------------------------------------------------------------------------------'''


def copy_matrix(mat):
    """
       Initialize the game board matrix with no changes to nodes, ensure matrix is wiped clean.
    :param mat: matrix of the game's board
    :return: new_mat, a cleaned matrix representing game board
    """
    # To start a clean slate. i.e to ensure that change in newgrid doesn't change mat.
    # make a copy mat function for this.
    new_mat = [['.' for x in range(6)] for x in range(6)]
    for i in range(6):
        for j in range(6):
            new_mat[i][j] = mat[i][j]
    return new_mat


def rotate(mat, move):
    """
        Rotate the game board's quadrant 90 degrees clockwise or counter-c.w., as instructed by
        the AI player or the human player.
    :param mat: matrix of the game's board, representing one quadrant
    :param move: 
    :return: new_mat, the same quadrant with all play pieces intact, just rotated 90 degrees
    """
    ini_col = math.floor(((move[0] - 1) % 2) * 3)
    ini_row = math.floor(((move[0] - 1) / 2) * 3)
    # For 4 and 2
    if move[0] % 2 is 0:
        ini_row = ini_row - 1

    new_mat = copy_matrix(mat)
    if move[1] is 'R':
        for i in range(ini_row, ini_row + 3):
            for j in range(ini_col, ini_col + 3):
                new_mat[j + ini_row - ini_col][2 - i + ini_row + ini_col] = mat[i][j]

    elif move[1] is 'L':
        for i in range(ini_row, ini_row + 3):
            for j in range(ini_col, ini_col + 3):
                new_mat[2 - j + ini_row + ini_col][i - ini_row + ini_col] = mat[i][j]

    return new_mat


def do_move(mat, color, move):
    """
        "Physically" move the play piece into designated position.
    :param mat: matrix of the game's board, representing one quadrant
    :param color: the color of the game play piece ('w' or 'b')
    :param move: the coordinates to move into, a list
    :return: void
    """
    ini_col = math.floor(((move[0] - 1) % 2) * 3)
    ini_row = math.floor(((move[0] - 1) / 2) * 3)
    if move[0] % 2 is 0:
        ini_row = ini_row - 1

    if move[1] <= 3:
        if mat[ini_row][(ini_col + move[1] - 1)] is '.':
            mat[ini_row][(ini_col + move[1] - 1)] = color
    elif move[1] <= 6:
        if mat[ini_row + 1][(ini_col + move[1] - 4)] is '.':
            mat[ini_row + 1][(ini_col + move[1] - 4)] = color
    elif move[1] <= 9:
        if mat[ini_row + 2][(ini_col + move[1]) - 7] is '.':
            mat[ini_row + 2][(ini_col + move[1]) - 7] = color

    return


'''Winning! stuff --------------------------------------------------------------------------------------------------'''


def who_won(c, mat):
    """
        Find out which color play piece is residing in the winning row, 'w' or 'b', thus which player.
    :param c: the color of the game play piece ('w' or 'b')
    :param mat: matrix of the game's board, representing one quadrant
    :return: win, the determined winner
    """
    win = False
    for i in range(6):
        for j in range(6):
            if mat[i][j] is c:
                # print("TEST NODE CONTENTS for win:", mat[i][j], mat[i][j+1], mat[i][j+2], mat[i][j+3],
                #       mat[i][j+4])
                if j < 2 <= i:
                    win = (
                        mat[i][j] is mat[i][j + 1] is mat[i][j + 2] is mat[i][j + 3] is mat[i][j + 4]
                        is c)
                    # print("inside j<2<=i: win=", win)
                elif j < 2:
                    win = (
                        (mat[i][j] is mat[i + 1][j + 1] is mat[i + 2][j + 2] is mat[i + 3][j + 3] is mat[i + 4][j + 4]
                         is c)
                        or win)
                    # print("inside j<2: win=", win)
                elif i < 2:
                    win = (
                        (mat[i][j] is mat[i + 1][j] is mat[i + 2][j] is mat[i + 3][j] is mat[i + 4][j]
                         is c)
                        or win)
                    # print("inside i<2: win=", win)
            break
    return win


def is_win_state(mat):
    """
        Determine if a winning state exists on the game board at any given time, winning constitutes
        five play pieces in a row, ties can exist.  Helper function 'who_won' is utilized to search the matrix.
    :param mat: matrix of the game's board, representing one quadrant
    :return: string message reporting the result of the game
    """
    white_won = who_won('w', mat)
    # print("Value of white_won:", white_won)
    black_won = who_won('b', mat)

    if white_won and (not black_won):
        return "P1 wins!"
    elif (white_won and black_won) or '.' not in (i[0] for i in init_board):
        return "A Tie"
    elif black_won and (not white_won):
        return "P2 Wins!"

    return None


'''Heuristics, Best move/scoring move finder-----------------------------------------------------------------------'''


def heuristic_helper(mov_scr, color, mat, ptr):
    """
       Helper function for 'matrix_heuristics'
    :param mov_scr: the 'score' of a potential move for alpha beta algo
    :param color: the color of the game play piece ('w' or 'b')
    :param mat: matrix of the game's board, representing one quadrant
    :param ptr: pointer to the positions contain the color play piece under investigation
    :return: mov_scr or maximum of three score values found recursively
    """
    if ptr[0] >= 6 or ptr[1] >= 6:
        return mov_scr

    if mov_scr >= 5:
        return mov_scr

    if mat[ptr[0]][ptr[1]] is not color:
        return mov_scr

    else:
        scr1 = heuristic_helper(mov_scr + 1, color, mat, ((ptr[0] + 1), (ptr[1])))
        scr2 = heuristic_helper(mov_scr + 1, color, mat, ((ptr[0]), (ptr[1] + 1)))
        scr3 = heuristic_helper(mov_scr + 1, color, mat, ((ptr[0] + 1), (ptr[1] + 1)))
        return max(scr1, scr2, scr3, mov_scr)


def matrix_heuristics(color, mat):
    """
        Find the best possible move for the AI play piece to move to.
    :param color: the color of the game play piece ('w' or 'b')
    :param mat: matrix of the game's board, representing one quadrant
    :return: mov_score, the best scoring move for the minimax/alpha-beta algo
    """
    mov_score = 0
    for i in range(6):
        for j in range(6):
            temp = 0
            if mat[i][j] is color:
                temp = heuristic_helper(0, color, mat, (i, j))
            mov_score = max(mov_score, temp)

    return mov_score


def available_moves(mat):
    """
        Find all empty, available nodes to make a play on.
    :param mat: matrix of the game's board, representing one quadrant
    :return: moves, list of available moves
    """
    moves = []
    quad = 0  # quadrant 1,2,3,or 4
    pos = 0
    for i in range(6):
        for j in range(6):
            if mat[i][j] is '.':
                if j < 3:
                    if i < 3:
                        quad = 1
                    else:
                        quad = 3
                else:
                    if i < 3:
                        quad = 2
                    else:
                        quad = 4

                ini_row = math.floor(((quad - 1) / 2) * 3)
                ini_col = math.floor(((quad - 1) % 2) * 3)
                if quad % 2 is 0:
                    ini_row = ini_row - 1
                pos = (3 * (i - ini_row)) + (j - ini_col) + 1

                for x in [1, 2, 3, 4]:
                    moves.append(((quad, pos), (x, 'L')))
                    moves.append(((quad, pos), (x, 'R')))

    return moves


"""Random Move Generator, Mini-Max Algorithm-----------------------------------------------------------------------"""


def mini_max_algo(moves, p_num, mat, depth, alpha, beta, maximizing):
    """

    :param moves: a list of possible high-scoring moves 
    :param p_num: the player number 1 or 2
    :param mat: matrix of the game's board, representing one quadrant
    :param depth: the depth of the search tree that is allowed to be searched (compute intensive beyond 3!) 
    :param alpha: the Maximizer player -- i.e. you
    :param beta: the Minimizer adversary
    :param maximizing: for the alpha-beta algo, boolean value T/F to determine whether the
        current iteration is a maximizing or a minimizing run for adversarial minimax search
    :return: best_move
    """
    global big_node_counter
    # node_counter = 0
    colors = ['b', 'w']
    if moves is None or moves is []:
        moves = []
        moves.append(generate_rand_move(mat))
    if depth is 0:
        return (moves[-1], (matrix_heuristics(colors[p_num - 1], mat)))
    if is_win_state(mat) is not None:
        return (moves[-1], 5)

    if maximizing:
        best_move = (generate_rand_move(mat), -5)
        for move in available_moves(mat):
            # node_counter+=1
            big_node_counter+=1
            tmp_mat = copy_matrix(mat)  # temporary matrix
            do_move(tmp_mat, colors[p_num - 1], move[0])
            tmp_mat = rotate(tmp_mat, move[1])
            moves.append(move)
            score = mini_max_algo(moves, p_num, tmp_mat, depth - 1, alpha, beta, False)[1]
            if best_move[1] < score:
                best_move = (move, score)
            alpha = max(score, beta)
            if beta <= alpha:
                break
        # print("Nodes expanded:", node_counter)
        print("Running Total Nodes Expanded:", big_node_counter)
        return best_move

    else:
        best_move = (generate_rand_move(mat), 5)
        for move in available_moves(mat):
            if moves is None:
                moves = []
            # node_counter += 1
            big_node_counter += 1
            tmp_mat = copy_matrix(mat)
            do_move(tmp_mat, colors[-p_num], move[0])
            tmp_mat = rotate(tmp_mat, move[1])
            moves = moves.append(move)
            score = mini_max_algo(moves, p_num, tmp_mat, depth - 1, alpha, beta, True)[1]
            if best_move[1] > score:
                best_move = (move, score)
            beta = min(score, beta)
            if beta <= alpha:
                break
        # print("Nodes expanded:", node_counter)
        print("Running Total Nodes Expanded:", big_node_counter)
        return best_move


def generate_rand_move(mat):
    """

    :param mat: 
    :return: 
    """
    quadrant = random.choice(range(1, 4))  # which quadrant the play piece is placed
    quad_node = random.choice(range(1, 9))  # which node within the quadrant the piece is placed

    valid = False
    while not valid:
        ini_col = math.floor(((quadrant - 1) % 2) * 3)  # starting column
        ini_row = math.floor(((quadrant - 1) / 2) * 3)  # starting row
        if quadrant % 2 is 0:
            ini_row = ini_row - 1

        if quad_node <= 3:
            if mat[ini_row][(ini_col + quad_node - 1)] is '.':
                valid = True
                break

        elif quad_node <= 6:
            if mat[ini_row + 1][(ini_col + quad_node - 4)] is '.':
                valid = True
                break

        elif quad_node <= 9:
            if mat[ini_row + 2][(ini_col + quad_node - 7)] is '.':
                valid = True
                break

        quadrant = random.choice(range(1, 4))
        quad_node = random.choice(range(1, 9))

    rotate_quadrant = random.choice(range(1, 4))
    rotate_direction = random.choice(['L', 'R'])

    move = ((quadrant, quad_node), (rotate_quadrant, rotate_direction))
    return move


'''Core functions --------------------------------------------------------------------------------------------------'''


def print_matrix(mat):
    """
        Print out the game board each time a play is made or at start of game.
    :param mat: the game board matrix
    :return: 
    """
    row = ''
    print('+=====1=====+=====2=====+')
    for i in range(6):
        if i is 3:
            print('+===========+===========+')
        for j in range(6):
            if j is 3:
                row += ' | '
            row += ' ' + mat[i][j] + ' '
        print('|', row, '|')
        row = ''
    print('+=====3=====+=====4=====+')
    print('--------------------------')


def parse_human_move(usr_inpt):
    """

       :param usr_inpt: The user/human player's input
       :return: the usr_input parsed into a quadrant/node rotate#/rotateDirection
           movement/play piece placement and stored in a list.
       """
    _in = usr_inpt.split(' ')
    move = [_in[0].split('/'), list(_in[1])]
    move[0] = [int(x) for x in move[0]]
    move[1][0] = int(move[1][0])

    return move


def pentago(you, p1, p2, mat):
    """

    :param you: yourself, the human player
    :param p1: the play piece/marble representing player one
    :param p2: the play piece/marble representing player two
    :param mat: the matrix, or board game consisting of nine nodes per quadrant
    :return: void (recursion)
    """

    if is_win_state(mat) is not None:
        print("\n**** **** **** **** **** ****\n", is_win_state(mat), "\n**** **** **** **** **** ****\n")
    else:
        if is_win_state(mat) is not None:
            print(is_win_state(mat))
            return
        print("Current Game Board:")
        print_matrix(mat)
        updt_mat = mat  # update the matrix
        cur_mov = []  # current move

        # player_turn(you, p1, p2, updt_mat, cur_mov)

        # ----------------------------------------------------------------------------------------------------
        # player 1 move
        if you is 1:
            while True:
                try:
                    print(p1 + ", it's your turn: ")
                    i_mov = input()  # user's input move
                    cur_mov = parse_human_move(i_mov)
                    break
                except (ValueError, NameError, IndexError):
                    print("\nERROR: Bad Input!\n**** ****\nPlease enter your move in this format:\n"
                          "\t<quadrant#>/<node#> <rotateQuadrant#><L | R>\n"
                          "For example, to place your play piece in Quadrant #1, in node #5 (the center),\n"
                          "followed by rotating Quadrant #3 to the right, use this command:\n"
                          "\t1/5 3R\n,then press 'enter'.\n**** ****\n")

        else:
            print(p1, "is deliberating...")
            cur_mov = mini_max_algo(list(), you, updt_mat, 3, -5, 5, True)[0]
        print(cur_mov)
        do_move(updt_mat, 'w', cur_mov[0])
        updt_mat = rotate(updt_mat, cur_mov[1])

        print_matrix(updt_mat)
        if is_win_state(updt_mat) is not None:
            print(is_win_state(updt_mat))
            return

        # ---------------------------------------------------------------------------------------------------
        # player 2 move
        if you is 2:
            while True:
                try:
                    print(p2 + ", it's your turn: ")
                    i_mov = input()
                    cur_mov = parse_human_move(i_mov)
                    break
                except (ValueError, NameError, IndexError):
                    print("\nERROR: Bad Input!\n**** ****\nPlease enter your move in this format:\n"
                          "\t<quadrant#>/<node#> <rotateQuadrant#><L | R>\n"
                          "For example, to place your play piece in Quadrant #1, in node #5 (the center),\n"
                          "followed by rotating Quadrant #3 to the right, use this command:\n"
                          "\t1/5 3R\n,then press 'enter'.\n**** ****\n")

        else:
            print(p2, "is deliberating...")
            cur_mov = mini_max_algo(list(), you, updt_mat, 3, -5, 5, True)[0]

        print(cur_mov)
        do_move(updt_mat, 'b', cur_mov[0])
        updt_mat = rotate(updt_mat, cur_mov[1])

        if is_win_state(updt_mat) is not None:
            print(is_win_state(updt_mat))
            return

        pentago(you, p1, p2, updt_mat)

    return
# end pentago function


''' MAIN '''

init_board = []  # initial game board that is empty
big_node_counter = 0

def my_main():
    print("The starting board:")
    global big_node_counter
    global init_board
    init_board = [['.' for x in range(6)] for x in range(6)]
    print_matrix(init_board)
    human = int(input("Choose Player 1 or 2:"))
    p1 = input('What is Player 1\'s name?')
    p2 = input('What is Player 2\'s name?')
    pentago(human, p1, p2, init_board)
    print("Final Nodes Expanded:", big_node_counter)


if __name__ == '__main__':
    my_main()
