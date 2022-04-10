# Author: Sean Colasito
# Date: 7/31/2021
# Description: Class for playing a board game called Quoridor

class Cell:
    """ A class that creates a Cell in a Quoridor board game. """
    def __init__(self, x, y):
        """ Initializes data members of the Cell class. """
        self._x = x  # column number
        self._y = y  # row number
        self._pawn = 0  # 0, 1, 2 depending if a pawn is in the cell; returns 1 for Player1 Pawn and 2 for Player2 Pawn
        self._v_fence = 0  # 0 or 1 depending if a vertical fence is in the cell
        self._h_fence = 0  # 0 or 1 depending if a horizontal fence is in the cell
        self._baseline_cell = 0  # 0, 1 or 2 depending if the cell is a baseline cell; 1 means it is Player1's baseline
        self._painted_cell = 0  # 0 or 1 depending if the cell is painted; if a cell is painted then it is allowed move

    def get_coordinates(self):
        """ Returns the coordinates of the Cell. """
        return self._x, self._y

    def get_pawn(self):
        """
        Returns 0, 1 or 2 depending if pawn is in the cell.
        Returns 1 for Player1's Pawn and 2 for Player 2's Pawn.
        """
        return self._pawn

    def get_v_fence(self):
        """ Returns 0 or 1 depending if a vertical fence is in the cell. """
        return self._v_fence

    def get_h_fence(self):
        """ Returns 0 or 1 depending if horizontal fence is in the cell. """
        return self._h_fence

    def get_painted_cell(self):
        """ Returns 0 or 1 depending if the cell is painted. """
        return self._painted_cell

    def get_baseline_cell(self):
        """ Returns 0, 1, 2 depending if the cell is a baseline cell and a baseline cell of P1 or P2. """
        return self._baseline_cell

    def set_pawn(self, player):
        """ Places the Pawn on the Cell."""
        self._pawn = player

    def set_baseline_cell(self, player):
        """ Activates a cell into a Baseline Cell of P1 or P2. """
        self._baseline_cell = player

    def set_v_fence(self):
        """ Places a vertical fence in the cell. """
        self._v_fence = 1

    def set_h_fence(self):
        """ Places a horizontal fence in the cell. """
        self._h_fence = 1


class Pawn:
    """ A class that creates a Pawn in a Quoridor board game."""
    def __init__(self, x, y, player):
        self._x = x   # current column number location of the pawn
        self._y = y   # current row number location of the pawn
        self._player = player  # either 1 or 2 depending if Player1's or Player2's pawn

    def get_coordinates(self):
        """ Returns the coordinates of the Pawn. """
        return self._x, self._y

    def set_coordinates(self, coordinates):
        """ Sets the new coordinates of the Pawn. """
        self._x = coordinates[0]
        self._y = coordinates[1]


class Fence:
    """ A class that creates a Pawn in a Quoridor board game."""
    def __init__(self, player, x=None, y=None):
        self._x = x  # current column number location of the fence; value is None at the beginning of game
        self._y = y  # current row number location of the fence; value is None at the beginning of game
        self._player = player  # either 1 or 2 depending if Player1's or Player2's fence

    def get_coordinates(self):
        """ Returns the coordinates of the Fence. """
        return self._x, self._y

    def set_coordinates(self, coordinates):
        """ Sets the new coordinates of the Fence. """
        self._x = coordinates[0]
        self._y = coordinates[1]


class QuoridorGame:
    """ A class that creates a Quoridor board game. """

    def __init__(self):
        """
        Initializes data members of the QuoridorGame class.
        """
        # Create a 2d array with 9 rows and 9 columns to create the Quoridor board
        rows, columns = (9, 9)
        self._board = []
        for i in range(rows):  # iterates from 0 to 9 since there are 9 columns
            column = []  # create an empty array to be nested in the other array
            for j in range(columns):  # iterates from 0 to 9 since there are 9 rows
                column.append(Cell(j, i))  # creates a Cell object with the coordinates j, i
            self._board.append(column)  # once iteration is finished over a row, adds the row array to the main array

        # Initiate 10 fences for Player1 and Player2
        self._p1_fences = []
        for i in range(1, 11):
            self._p1_fences.append(Fence(1))  # Create a Fence object for Player 1
        self._p2_fences = []
        for i in range(1, 11):
            self._p2_fences.append(Fence(2))  # Create a Fence object for Player 2

        # Initiate pawns for Player1 and Player 2 in the correct starting position
        self._p1 = Pawn(4, 0, 1)  # Creates a Pawn object for Player1 at location 4, 0
        self._p2 = Pawn(4, 8, 2)  # Creates a Pawn object for Player2 at location 4, 8
        self._board[0][4].set_pawn(1), self._board[8][4].set_pawn(2)  # Sets the Cell pawn status to 1

        # Initiate baseline cells from 0 to 1
        self._p1_baseline = []  # P1's baseline cells; P2 must reach this baseline in order to win
        self._p2_baseline = []  # P2's baseline cells; P1 must reach this baseline in order to win
        for i in range(9):
            self._p1_baseline.append(self._board[0][i].get_coordinates())
            self._p2_baseline.append(self._board[8][i].get_coordinates())
            self._board[0][i].set_baseline_cell(1), self._board[8][i].set_baseline_cell(2)

        # Set player turn and current game state
        self._current_turn = 1
        self._current_state = 0  # 0 means unfinished, 1 or 2 means Player1 or Player2 has won respectively

    @staticmethod
    def pos_adjacent_moves(player_pawn):
        """
        Returns a list of possible adjacent moves.
        """
        # First, create a list of tuples/coordinates of adjacent squares
        adjacent_squares = [(player_pawn[0] - 1, player_pawn[1]),
                            (player_pawn[0] + 1, player_pawn[1]),
                            (player_pawn[0], player_pawn[1] - 1),
                            (player_pawn[0], player_pawn[1] + 1),
                            ]
        # Then, remove coordinates less than 0 or greater than 8 since these are out of bounds
        for coordinates in adjacent_squares:
            for i in coordinates:
                if i < 0 or i > 8:
                    adjacent_squares.remove(coordinates)
        return adjacent_squares

    def fence_checker(self, player_pawn, adjacent_squares):
        """
        Checks for Fences and returns a list of valid adjacent moves.
        """
        # 1. Check for validity of upward movement; if current cell has a horizontal fence, can't move upwards
        row = player_pawn[1]  # the second element in the Tuple is the row
        column = player_pawn[0]  # the first element in the Tuple is the column
        if self._board[row][column].get_h_fence() == 1:  # if current cell has a horizontal fence
            adjacent_squares.remove((player_pawn[0], player_pawn[1] - 1))  # remove coordinates from list

        # 2. Check for validity of downward movement; if cell downwards has a horizontal fence, can't move downwards
        row = player_pawn[1] + 1
        column = player_pawn[0]

        # Use try except block to handle out of range for checking cell near corners
        try:
            if self._board[row][column].get_h_fence() == 1:  # if the downward cell has a horizontal fence
                adjacent_squares.remove((player_pawn[0], player_pawn[1] + 1))  # remove coordinates from list
        except IndexError:
            pass

        # 3. Check for validity of left movement; if current cell has a vertical fence, can't move leftwards
        row = player_pawn[1]
        column = player_pawn[0]
        if self._board[row][column].get_v_fence() == 1:  # if the current cell has a vertical fence
            adjacent_squares.remove((player_pawn[0] - 1, player_pawn[1]))  # remove coordinates from list

        # 4. Check for validity of right movement; if rightward cell has a vertical fence, can't move rightwards
        row = player_pawn[1]
        column = player_pawn[0] + 1
        if self._board[row][column].get_v_fence() == 1:  # if the rightward cell has a vertical fence
            adjacent_squares.remove((player_pawn[0] + 1, player_pawn[1]))  # remove coordinates from list

        cleared_squares = adjacent_squares
        return cleared_squares  # Cleared list of valid moves (without Fence restrictions)

    def pawn_interaction(self, player_pawn, opponent_pawn, new_list):
        # When a pawn is face to face with another - special interaction allows a hop or a diagonal movement
        # depending on the surrounding fences
        # 1. Check if there is pawn face to face
        # A pawn is face to face if it's in the adjacent list we made earlier
        # compare opponent pawn to new_list to see if it's face to face with current player pawn
        if opponent_pawn in new_list:  # if opponent is face to face with the other pawn
            # if both pawns are in the same column, that means they are vertically face to face
            face_orientation = None
            if opponent_pawn[0] == player_pawn[0]:
                face_orientation = "vertical"
            # if both pawns are in the same row, that means they are horizontally face to face
            elif opponent_pawn[1] == player_pawn[1]:
                face_orientation = "horizontal"

            # remove opponent pawns coordinates from painted cells since two pawns can't be on the same cell
            new_list.remove(self._board[opponent_pawn[1]][opponent_pawn[0]].get_coordinates())

            # if they are face to face vertically
            if face_orientation == "vertical":
                if player_pawn < opponent_pawn:  # < or > determines direction of hop by comparing both tuples
                    # if opponent pawn's cell has no horizontal fence (in between the two pawns), allow hop
                    if self._board[opponent_pawn[1]][opponent_pawn[0]].get_h_fence() == 0:
                        # if the destination cell to jump to has a horizontal wall, allow diagonal move
                        # if the destination cell to jump to has no horizontal wall, allow hop
                        if self._board[opponent_pawn[1] + 1][opponent_pawn[0]].get_h_fence() == 1:  # if horizontal wall
                            # if no vertical walls stopping hop, add possible diagonal moves to painted cells
                            if self._board[opponent_pawn[1]][opponent_pawn[0]].get_v_fence() != 1:
                                new_list.append(
                                    self._board[opponent_pawn[1]][opponent_pawn[0] - 1].get_coordinates())
                            if self._board[opponent_pawn[1]][opponent_pawn[0] + 1].get_v_fence() != 1:
                                new_list.append(
                                    self._board[opponent_pawn[1]][opponent_pawn[0] + 1].get_coordinates())
                        else:  # if no horizontal wall, allow hop and add coordinates to possible moves/painted cells
                            new_list.append(self._board[opponent_pawn[1] + 1][opponent_pawn[0]].get_coordinates())
                elif player_pawn > opponent_pawn:
                    # if opponent pawn's cell has no horizontal fence (in between the two pawns), allow hop
                    if self._board[player_pawn[1]][player_pawn[0]].get_h_fence() == 0:
                        # add coordinates to possible moves/painted cells
                        print(self._board[opponent_pawn[1]][opponent_pawn[0] + 1].get_coordinates())
                        if self._board[opponent_pawn[1]][opponent_pawn[0]].get_h_fence() == 1:  # if horizontal wall
                            # if no vertical walls stopping hop, add possible diagonal moves to painted cells
                            if self._board[opponent_pawn[1]][opponent_pawn[0]].get_v_fence() != 1:
                                new_list.append(
                                    self._board[opponent_pawn[1]][opponent_pawn[0] - 1].get_coordinates())
                            if self._board[opponent_pawn[1]][opponent_pawn[0] + 1].get_v_fence() != 1:
                                new_list.append(
                                    self._board[opponent_pawn[1]][opponent_pawn[0] + 1].get_coordinates())
                        else:  # if no horizontal wall, allow hop and add coordinates to possible moves/painted cells
                            new_list.append(self._board[opponent_pawn[1] - 1][opponent_pawn[0]].get_coordinates())

            # if they are face to face horizontally
            elif face_orientation == "horizontal":
                if player_pawn < opponent_pawn:
                    # if opponent pawn's cell has no vertical fence (in between the two pawns), allow hop
                    if self._board[opponent_pawn[1]][opponent_pawn[0]].get_v_fence() == 0:
                        # if the destination cell to jump to has a vertical wall, allow diagonal move
                        # if the destination cell to jump to has no vertical wall, allow hop
                        if self._board[opponent_pawn[1]][opponent_pawn[0] + 1].get_v_fence() == 1:  # if vertical wall
                            # if no vertical walls stopping hop, add possible diagonal moves to painted cells
                            if self._board[opponent_pawn[1]][opponent_pawn[0]].get_h_fence() != 1:
                                new_list.append(
                                    self._board[opponent_pawn[1] - 1][opponent_pawn[0]].get_coordinates())
                            if self._board[opponent_pawn[1] + 1][opponent_pawn[0]].get_h_fence() != 1:
                                new_list.append(
                                    self._board[opponent_pawn[1] + 1][opponent_pawn[0]].get_coordinates())
                        else:  # if the destination cell to jump to has no vertical wall, allow hop
                            new_list.append(
                                self._board[opponent_pawn[1]][opponent_pawn[0] + 1].get_coordinates())
                elif player_pawn > opponent_pawn:
                    # if opponent pawn's cell has no vertical fence (in between the two pawns), allow hop
                    if self._board[player_pawn[1]][player_pawn[0]].get_v_fence() == 0:
                        # if the destination cell to jump to has a vertical wall, allow diagonal move
                        # if the destination cell to jump to has no vertical wall, allow hop
                        if self._board[opponent_pawn[1]][opponent_pawn[0]].get_v_fence() == 1:
                            # if no vertical walls stopping hop, add possible diagonal moves to painted cells
                            if self._board[opponent_pawn[1]][opponent_pawn[0]].get_h_fence() != 1:
                                new_list.append(
                                    self._board[opponent_pawn[1] - 1][opponent_pawn[0]].get_coordinates())
                            if self._board[opponent_pawn[1] + 1][opponent_pawn[0]].get_h_fence() != 1:
                                new_list.append(
                                    self._board[opponent_pawn[1] + 1][opponent_pawn[0]].get_coordinates())
                        # add coordinates to possible moves/painted cells
                        else:
                            new_list.append(
                                self._board[opponent_pawn[1]][opponent_pawn[0] - 1].get_coordinates())

            return new_list

    def valid_moves(self):
        """
        Returns a list of possible tuple/coordinates of valid moves.
        """
        # Assign appropriate player Pawn to be moved
        player_pawn = None
        opponent_pawn = None
        if self._current_turn == 1:
            player_pawn = self._p1.get_coordinates()  # Assign coordinates of the Pawn object
            opponent_pawn = self._p2.get_coordinates()
        elif self._current_turn == 2:
            player_pawn = self._p2.get_coordinates()
            opponent_pawn = self._p1.get_coordinates()

        # Check possible adjacent square moves by calling adjacent_moves()
        adjacent_squares = self.pos_adjacent_moves(player_pawn)  # Returns a list of possible adjacent moves

        # Create a new list for use later for pawn to pawn interaction/diagonal movement.
        new_list = adjacent_squares[:]  # A copy of the above list will be used for checking Pawn restrictions

        # Check for movement restrictions
        # A. Fences
        # Returns a list of Fence-cleared moves
        cleared_fences = self.fence_checker(player_pawn, adjacent_squares)

        # B. Pawn
        # Returns a list of valid Pawn-to-Pawn interaction moves
        cleared_pawn = self.pawn_interaction(player_pawn, opponent_pawn, new_list)

        # Adds both Fence-cleared and Pawn-to-Pawn interaction moves
        # and returns the final list of tuples/coordinates for possible moves for current player's Pawn
        # Use try-except block to avoid error if there is no pawn to pawn interaction.
        try:
            valid_moves = cleared_fences + cleared_pawn
        except TypeError:
            return cleared_fences

        return valid_moves

    def get_current_state(self):
        """
        Returns 0 if game state is unfinished, or 1 or 2 if Player1 or Player2 has won respectively
        """
        return self._current_state

    def get_current_turn(self):
        """
        Returns 1 or 2 if it's Player1 or Player2's turn
        """
        return self._current_turn

    def move_pawn(self, player_turn, coordinates):
        """
        Takes an integer that represents the player making the move
        and a tuple with the (x, y) coordinates of where the pawn is going to be moved to.
        :param player_turn: 1 or 2 depending if it's Player1 or Player2's turn
        :param coordinates: x, y coordinates of where the pawn is going to be moved to
        :return: True or False depending on validity of move
        """

        # Check if the game has been won
        if self.get_current_state() != 0:
            return False

        # Check if it's the appropriate player's turn
        if player_turn != self.get_current_turn():
            return False

        # Check if coordinates (tuple (x, y)) is a valid move
        # Call valid_moves() to get a list of tuples/coordinates of the valid moves
        # and check if the given coordinates is in the list
        # 1. Return false if it's not a valid move
        if coordinates not in self.valid_moves():
            return False
        # 2. Return True if it is a valid move.
        elif coordinates in self.valid_moves():
            # Check if it's a winning move
            if self.get_current_turn() == 1:
                # if player turn is 1 and the baseline cell is player 2's baseline, player 1 wins
                if self._board[coordinates[1]][coordinates[0]].get_baseline_cell() == 2:
                    self._current_state = 1  # set game state to Player1 won
                    return True
            elif self.get_current_turn() == 2:
                # if player turn is 2 and the baseline cell is player 1's baseline, player 2 wins
                if self._board[coordinates[1]][coordinates[0]].get_baseline_cell() == 1:
                    self._current_state = 2  # set game state to Player2 won
                    return True

        # Move the pawn from it's original position
        if self.get_current_turn() == 1:
            # Set original cell pawn status to 0
            self._board[self._p1.get_coordinates()[1]][self._p1.get_coordinates()[0]].set_pawn(0)
            # Move pawn to new position
            self._p1.set_coordinates(coordinates)
            # Set new pawn coordinates and set new cell pawn status to 1
            self._board[self._p1.get_coordinates()[1]][self._p1.get_coordinates()[0]].set_pawn(1)
        elif self.get_current_turn() == 2:
            # Set original cell pawn status to 0
            self._board[self._p2.get_coordinates()[1]][self._p2.get_coordinates()[0]].set_pawn(0)
            # Move pawn to new position
            self._p2.set_coordinates(coordinates)
            # Set new pawn coordinates and set new cell pawn status to 2
            self._board[self._p2.get_coordinates()[1]][self._p2.get_coordinates()[0]].set_pawn(2)

        # Switch to next player's turn
        if self.get_current_turn() == 1:
            self._current_turn = 2
        elif self.get_current_turn() == 2:
            self._current_turn = 1

        # Return True if the move is valid and successful
        return True

    def place_fence(self, player_turn, fence_type, coordinates):
        """
        Takes an integer that represents the player making the move
        a letter (v or h) indicating a vertical or horizontal fence
        and the x, y coordinates of where the fence is going to be placed
        :param player_turn: 1 or 2 depending if it's Player1 or Player2's turn
        :param fence_type: v or h depending on the orientation of the fence
        :param coordinates: x, y coordinates of where the fence is going to be placed
        :return: True or False depending on validity of fence placement
        """
        # Check to see if the game has been already won
        if self.get_current_state() != 0:
            return False

        # Check if it's the appropriate player's turn
        if player_turn != self.get_current_turn():  # if player_turn is not equal to current player turn, return False
            return False

        # Check to see if a player has fences
        if player_turn == 1:
            if len(self._p1_fences) == 0:  # if Player1 has 0 fences, return False
                return False
        elif player_turn == 2:  # if Player2 has 0 fences, return False
            if len(self._p2_fences) == 0:
                return False

        # Check to see if the coordinates are valid
        # Cannot place fence out of bounds (x > 9 or y > 9)
        if coordinates[0] > 8 or coordinates[1] > 8:
            return False

        # Cannot place horizontal fence from (0,0) to (8,0)
        # and vertical fence from (0,0) to (0,8) since these are the edges of the board
        invalid_coordinates = []  # list of tuple coordinates that are invalid
        if fence_type == "h":
            for i in range(0, 9):
                invalid_coordinates.append((i, 0))
        elif fence_type == "v":
            for i in range(0, 9):
                invalid_coordinates.append((0, i))
        # If given tuple of coordinates in invalid coordinates - the move is invalid and return False
        if coordinates in invalid_coordinates:
            return False

        # Place the fence using given x, y coordinates
        # Syntax is self._board[row][column] to access coordinates
        # Ex. coordinates given is (6,4), syntax is self._board[5][6] (5th array, 6rd element in the array) to access
        # the cell with (6,5) coordinates
        row = coordinates[1]  # the second element in the Tuple is the row
        column = coordinates[0]  # the first element in the Tuple is the column

        # Check to see if the player is placing a horizontal fence or vertical fence
        if fence_type == "v":  # check to see if the player is placing a horizontal fence or vertical fence
            # Check to see if there is already a fence of that type there, otherwise place the fence
            if self._board[row][column].get_v_fence() == 1:
                return False  # return False if there is already a vertical fence there
            else:
                self._board[row][column].set_v_fence()  # set that cell (6, 5) to have a vertical fence
        elif fence_type == "h":
            if self._board[row][column].get_h_fence() == 1:
                return False  # return False if there is already a horizontal fence there
            else:
                self._board[row][column].set_h_fence()  # set that cell (6, 5) to have a horizontal fence

        # Remove a fence from the Player's fence tab and set new coordinates of the fence
        if player_turn == 1:
            fence = self._p1_fences.pop(0)  # remove the first fence on Player1's fence tab
            fence.set_coordinates(coordinates)

        elif player_turn == 2:
            fence = self._p2_fences.pop(0)  # remove the first fence on Player2's fence tab
            fence.set_coordinates(coordinates)

        # Switch to next player's turn
        if self.get_current_turn() == 1:
            self._current_turn = 2
        elif self.get_current_turn() == 2:
            self._current_turn = 1

        # return True if fence placement is valid
        return True

    def is_winner(self, player):
        """
        Takes a single integer representing the player number and returns True if the player has own and
        False if the player has not won
        :param player: integer
        :return: boolean
        """
        if player == self._current_state:  # self._current_state would be either 0, 1, or 2
            return True
        else:
            return False

    def print_board(self):
        """
        Prints a visual of the Quoridor board.

        Legend:
        | denotes a vertical fence
        ‾‾ denotes a horizontal fence
        ‾P1_Pawn‾ denotes a horizontal fence above the pawn
        | P1_Pawn denotes a vertical fence to the left of the pawn
        | ‾P1_Pawn‾ denotes the presence of both a horizontal and vertical fence in the cell
        """

        array = []  # create empty array
        for row in self._board:  # iterate over each row array
            new_row = []  # empty array to add Cell coordinates
            for cell in row:  # iterate over each Cell in row
                # append the specific Cell to the new_row
                if cell.get_pawn() == 1:  # if the pawn is in that coordinate, print "Pawn"
                    if cell.get_v_fence() == 1 and cell.get_h_fence() == 1:
                        new_row.append("| ‾P1_Pawn‾")
                    elif cell.get_v_fence() == 1:
                        new_row.append("| P1_Pawn")  # | denotes a vertical fence
                    elif cell.get_h_fence() == 1:
                        new_row.append("‾P1_Pawn‾")  # ‾‾ denotes a horizontal fence
                    else:
                        new_row.append("P1_Pawn")
                elif cell.get_pawn() == 2:
                    if cell.get_v_fence() == 1 and cell.get_h_fence() == 1:
                        new_row.append("| ‾P2_Pawn‾")
                    elif cell.get_v_fence() == 1:
                        new_row.append("| P2_Pawn")
                    elif cell.get_h_fence() == 1:
                        new_row.append("‾P2_Pawn‾")
                    else:
                        new_row.append("P2_Pawn")
                elif cell.get_v_fence() == 1 and cell.get_h_fence() == 1:
                    new_row.append("|‾‾")
                elif cell.get_v_fence() == 1:
                    new_row.append("|")  # if a vertical fence is in that coordinate, print "V Fence"
                elif cell.get_h_fence() == 1:
                    new_row.append("‾‾")  # if a horizontal fence is in that coordinate, print "H Fence"
                else:
                    new_row.append(cell.get_coordinates())  # otherwise, print the coordinates of the Cell
            array.append(new_row)  # append the row/new_array of coordinates to main array

        for row in array:  # print each row to create a visual
            print(row)


my_game = QuoridorGame()
my_game.print_board()