# Author: Richard Silva
# Date: 8/12/2021
# Description: This program is a representation of the board game Quoridor complete with all its rules.

class Board:
    """
    A representation of a board with respective fences and cells, contains the horizontal fences, vertical fences
    and cells in their respective dictionary. The positions on the board are the keys and the values are a string
    that signifies if a pawn or a fence is present.
    """
    def __init__(self):
        """
        Creates private members (dictionaries) for horizontal rows, vertical rows and cells. Iterates through loops
        to construct a dictionary containing all possible positions of fences and cells.
        Populates the end of the rows with each player's pawns at their starting point.
        """
        self._vertical_row = {}
        self._horizontal_row = {}
        self._cells = {}
        for x_value in range(1, 9):
            for y_value in range(0, 9):
                self._vertical_row[(x_value, y_value)] = None
        for x_value in range(0, 9):
            for y_value in range(1, 9):
                self._horizontal_row[(x_value, y_value)] = None
        for x_value in range(0, 9):
            for y_value in range(0, 9):
                self._cells[(x_value, y_value)] = None
        self._cells.update({(4, 0): "P1"})
        self._cells.update({(4, 8): "P2"})

    def get_vertical_rows(self):
        """
        Returns a dictionary of the vertical rows portion of the board dictionary
        """
        return self._vertical_row

    def get_horizontal_rows(self):
        """
        Returns a dictionary of the horizontal rows portion of the board dictionary
        """
        return self._horizontal_row

    def get_cells(self):
        """
        Returns a dictionary of the cells portion of the board dictionary
        """
        return self._cells

    def get_vertical_row(self, position):
        """
        Returns the value in a key (tuple position parameter) in the vertical rows dictionary
        """
        return self._vertical_row.get(position)

    def get_horizontal_row(self, position):
        """
        Returns the value in a key (tuple position parameter) in the horizontal rows dictionary
        """
        return self._horizontal_row.get(position)

    def get_cell(self, position):
        """
        Returns the value in a key (tuple position parameter) in the cells dictionary
        """
        return self._cells.get(position)

    def set_vertical_fence(self, position):
        """
        Sets a vertical fence at the desired position taking a tuple representing a position as a parameter
        """
        vertical_rows = self.get_vertical_rows()
        vertical_rows.update({position: "W"})

    def set_horizontal_fence(self, position):
        """
        Sets a horizontal fence at the desired position taking a tuple representing a position as a parameter
        """
        horizontal_rows = self.get_horizontal_rows()
        horizontal_rows.update({position: "W"})

    def set_cell(self, player, position):
        """
        Sets new pawn position in desired cell, player parameter must be passed along with a tuple representing
        a position
        """
        cells = self.get_cells()
        if player == 1:
            cells.update({position: "P1"})
        elif player == 2:
            cells.update({position: "P2"})

    def remove_pawn_position(self, position):
        """
        Takes the tuple position as a parameter and changes the value of the dictionary value to None.
        """
        cells = self.get_cells()
        cells.update({position: None})

    def remove_fence_position(self, direction, position):
        """
        Takes the tuple position as a parameter and changes the value of a fence position to None
        """
        if direction == 'h':
            horizontal_walls = self.get_horizontal_rows()
            horizontal_walls.update({position: None})
        elif direction == 'v':
            vertical_walls = self.get_vertical_rows()
            vertical_walls.update({position: None})

    def display_board(self):
        """
        Prints a board display of the current state of the board, displaying "P1" for player 1, "P2" for player 2,
        "==" for a horizontal fence and "|" for a vertical fence. "+" are board corners. This function specifically
        prints the top and bottom row of board, calling a secondary function to print the interior
        """
        first_string = "+"
        for num in range(0, 9):
            first_string += "==+"
        print(first_string)
        horizontal_string = "+"
        vertical_string = "|"
        all_horizontal_positions = self.get_horizontal_rows()
        all_vertical_positions = self.get_vertical_rows()
        self.helper_display_board(horizontal_string, vertical_string, all_horizontal_positions, all_vertical_positions)
        last_string = "+"
        for num in range(0, 9):
            last_string += "==+"
        print(last_string)

    def helper_display_board(self, horizontal_string, vertical_string, all_horizontal_positions,
                             all_vertical_positions):
        """
        Contains loop which prints out the state of the board, prints the interior of the board, helper function
        to display_board, takes internal function parameters as parameters
        """
        for num in range(0, 9):
            for other_num in range(0, 9):
                if (other_num, num) in all_horizontal_positions.keys():
                    if self.get_horizontal_row((other_num, num)) is None:
                        horizontal_string += "  "
                    else:
                        horizontal_string += "=="
                    horizontal_string += "+"
                if (other_num, num) in all_vertical_positions.keys():
                    if self.get_vertical_row((other_num, num)) is None:
                        vertical_string += " "
                    else:
                        vertical_string += "|"
                if self.get_cell((other_num, num)) is None:
                    vertical_string += "  "
                else:
                    vertical_string += self.get_cell((other_num, num))
            vertical_string += "|"
            if num != 0:
                print(horizontal_string)
            print(vertical_string)
            vertical_string = "|"
            horizontal_string = "+"


class QuoridorGame:
    """
    Represents a game of Quoridor between two players, initializes the board and allows you to move a pawn, place a
    fence, verify if a certain player has won and has a fair_play function that verifies if a fencing move is considered
    "fair play"
    """
    def __init__(self):
        """
        Initializes a board object by calling the Board class, also initializes private members that hold data
        on how many remaining fences each player has. Initializes a game winner member initialized to None,
        will be initialized to a player if said player has won the game. Contains private members holding the positions
        of each player so the class can properly remove a player's old position once their new position is determined
        valid. Finally, initializes a private member that states which player's turn it is. Initialized to 1.
        """
        self._board = Board()
        self._player_one_fences = 10
        self._player_two_fences = 10
        self._game_winner = None
        self._current_player_turn = 1
        self._player_one_position = (4, 0)
        self._player_two_position = (4, 8)

    def get_board(self):
        """
        Returns the board object
        """
        return self._board

    def get_player_fences(self, player):
        """
        Takes parameter player as an integer and returns number of fences remaining for that player
        """
        if player == 1:
            return self._player_one_fences
        elif player == 2:
            return self._player_two_fences

    def get_game_winner(self):
        """
        Returns winner of game as an integer (1 for player 1, 2 for player 2)
        """
        return self._game_winner

    def get_player_turn(self):
        """
        Returns which player's turn it is currently in the game
        """
        return self._current_player_turn

    def get_player_position(self, player):
        """
        Retrieves player's current position for removal purposes
        """
        if player == 1:
            return self._player_one_position
        elif player == 2:
            return self._player_two_position

    def set_player_turn(self, player):
        """
        Sets player's turn to the desired player in which the player parameter is passed as an integer
        """
        self._current_player_turn = player

    def set_game_winner(self, player):
        """
        Sets game winner to the desired player in which the player parameter is passed as an integer
        """
        if player == 1:
            self._game_winner = 1
        elif player == 2:
            self._game_winner = 2

    def set_player_position(self, player, position):
        """
        Sets the player's new position in the class's private member, takes a player parameter as an integer
        and a position parameter as a tuple
        """
        if player == 1:
            self._player_one_position = position
        elif player == 2:
            self._player_two_position = position

    def switch_player_turn(self):
        """
        Switches player's turn private member to 1 if 2 and 2 if 1.
        """
        if self.get_player_turn() == 1:
            self.set_player_turn(2)
        elif self.get_player_turn() == 2:
            self.set_player_turn(1)

    def move_pawn(self, player, position):
        """
        Determines if move is legal such as checking if a fence is blocking the path and if a pawn is jumping above
        the opposing player's piece or going diagonally, the method checks if the required conditions exist for
        the aforementioned moves to be legal. If move is not legal, returns False. Calls helper functions to verify
        whether a move is legal to determine if move is valid. Also calls is_winner to determine if game is already won.
        If so, returns False. Takes an integer of either 1 or 2 as a player parameter and a tuple as a position
        parameter. If player has managed to move their pawn to the other piece of the board, updates game status
        private member to the player that won. Switches player's turn if move is successful.
        """
        if self.is_winner(1) is True or self.is_winner(2) is True:
            return False
        if position not in self.get_board().get_cells().keys():
            return False
        if self.get_player_turn() != player:
            return False
        current_position = self.get_player_position(player)
        move_valid = self.verify_orthogonal_moves(position, current_position)
        if move_valid is False:
            move_valid = self.verify_two_space_moves(player, position, current_position)
        if move_valid is False:
            move_valid = self.verify_diagonal_moves(player, position, current_position)
        if move_valid is True:
            self.get_board().set_cell(player, position)
            self.get_board().remove_pawn_position(current_position)
            self.switch_player_turn()
            self.set_player_position(player, position)
            if player == 1 and position[1] == 8:
                self.set_game_winner(1)
            elif player == 2 and position[1] == 0:
                self.set_game_winner(2)
            return True
        else:
            return False

    def place_fence(self, player, direction, position):
        """
        Determines if game has been won by calling is_winner, returns False if game has already been won. Determines
        if game is legal by using direction to look up values in the vertical or horizontal dictionary
        then uses position as a key to determine if fence is already placed in the corresponding value.
        Calls is_fair_play to determine if move follows the fair play rule. If move follows fair play rule, method
        determines if the move is legal by checking if the player has the appropriate number of fences or if the
        position does not exist/already occupied. Returns False if move is not legal, returns True if move is legal
        then places fence in position. Takes player as an integer, direction as a string of either "h" or "v" (standing
        for horizontal and vertical respectively) and a tuple as a position.
        """
        if self.is_winner(1) is True or self.is_winner(2) is True:
            return False
        if self.get_player_turn() != player:
            return False
        if direction == "h":
            if position not in self.get_board().get_horizontal_rows():
                return False
        elif direction == "v":
            if position not in self.get_board().get_vertical_rows():
                return False
        if self.get_player_fences(player) == 0:
            return False
        space_found = self.helper_place_fence(position, direction)
        if space_found is True:
            if self.is_fair_play() is False:
                self.get_board().remove_fence_position(direction, position)
                return "breaks the fair play rule"
            self.switch_player_turn()
            self.decrement_player_fence(player)
            return True
        else:
            return False

    def helper_place_fence(self, position, direction):
        """
        Sets a player's fence if position is empty, called by the place_fence function
        """
        if direction == "h":
            if self.get_board().get_horizontal_row(position) is None:
                self.get_board().set_horizontal_fence(position)
            else:
                return False
        elif direction == "v":
            if self.get_board().get_vertical_row(position) is None:
                self.get_board().set_vertical_fence(position)
            else:
                return False
        return True

    def is_winner(self, player):
        """
        Takes an integer as the parameter player and calls get_game_winner. If result is equivalent to player,
        returns True. Else, returns False.
        """
        if self.get_game_winner() == player:
            return True
        else:
            return False

    def is_fair_play(self, position=None, moves_made=None, fair_play=False, player=None):
        """
        Iterative function that runs through all cells and determines if there remains a win condition after a fence
        is placed. If the other player can win, returns True. Else, returns False.
        """
        if moves_made is None:
            moves_made = []
            if self.get_player_turn() == 1:
                player = 2
            elif self.get_player_turn() == 2:
                player = 1
            position = self.get_player_position(player)
        if position in moves_made:
            return fair_play
        else:
            moves_made.append(position)
        if player == 1 and position[1] == 8:
            fair_play = True
            return fair_play
        elif player == 2 and position[1] == 0:
            fair_play = True
            return fair_play
        fair_play = self.helper_fair_play(position, moves_made, fair_play, player)
        return fair_play

    def helper_fair_play(self, position, moves_made, fair_play, player):
        """
        Helper function to fair_play, returns fair_play as a boolean value depending on whether a path to victory
        is possible
        """
        if (position[0] - 1, position[1]) in self.get_board().get_cells():
            if self.get_board().get_vertical_row(position) is None:
                fair_play = self.is_fair_play((position[0] - 1, position[1]), moves_made, fair_play, player) \
                            or fair_play
        if (position[0] + 1, position[1]) in self.get_board().get_cells():
            if self.get_board().get_vertical_row((position[0] + 1, position[1])) is None:
                fair_play = self.is_fair_play((position[0] + 1, position[1]), moves_made, fair_play, player) \
                            or fair_play
        if (position[0], position[1] - 1) in self.get_board().get_cells():
            if self.get_board().get_horizontal_row(position) is None:
                fair_play = self.is_fair_play((position[0], position[1] - 1), moves_made, fair_play, player) \
                            or fair_play
        if (position[0], position[1] + 1) in self.get_board().get_cells():
            if self.get_board().get_horizontal_row((position[0], position[1] + 1)) is None:
                fair_play = self.is_fair_play((position[0], position[1] + 1), moves_made, fair_play, player) \
                            or fair_play
        return fair_play

    def verify_left_move(self, position, current_position):
        """
        Verifies if a player moving left on the board is valid, returns True if valid, returns False if not
        """
        cells = self.get_board().get_cells()
        vertical_walls = self.get_board().get_vertical_rows()
        if cells.get(position) is not None:
            return False
        if vertical_walls.get(current_position) is not None:
            return False
        return True

    def verify_right_move(self, position):
        """
        Verifies if a player moving right on the board is valid, returns True if valid, returns False if not
        """
        cells = self.get_board().get_cells()
        vertical_walls = self.get_board().get_vertical_rows()
        if cells.get(position) is not None:
            return False
        if vertical_walls.get(position) is not None:
            return False
        return True

    def verify_top_move(self, position, current_position):
        """
        Verifies if a player moving up on the board is valid, returns True if valid, returns False if not
        """
        cells = self.get_board().get_cells()
        horizontal_walls = self.get_board().get_horizontal_rows()
        if cells.get(position) is not None:
            return False
        if horizontal_walls.get(current_position) is not None:
            return False
        return True

    def verify_bottom_move(self, position):
        """
        Verifies if a player moving down on the board is valid, returns True if valid, returns False if not
        """
        cells = self.get_board().get_cells()
        horizontal_walls = self.get_board().get_horizontal_rows()
        if cells.get(position) is not None:
            return False
        if horizontal_walls.get(position) is not None:
            return False
        return True

    def verify_orthogonal_moves(self, position, current_position):
        """
        Verifies left, right, top and down moves. Returns True if move is valid, False if not
        """
        move_valid = False
        if (current_position[0] - 1, current_position[1]) == position:
            move_valid = self.verify_left_move(position, current_position)
        if (current_position[0] + 1, current_position[1]) == position:
            move_valid = self.verify_right_move(position)
        if (current_position[0], current_position[1] - 1) == position:
            move_valid = self.verify_top_move(position, current_position)
        if (current_position[0], current_position[1] + 1) == position:
            move_valid = self.verify_bottom_move(position)
        return move_valid

    def verify_diagonal_moves(self, player, position, current_position):
        """
        Using an integer player parameter and a tuple as the position parameter, we verify whether a diagonal move is
        valid. Iterates through all scenarios to determine if wall obstructs diagonal move. Returns False is move
        is not valid, returns True if valid.
        """
        move_valid = False
        if (current_position[0] - 1, current_position[1] - 1) == position:
            move_valid = self.verify_northwest_move(player, position, current_position)
        if (current_position[0] + 1, current_position[1] - 1) == position:
            move_valid = self.verify_northeast_move(player, position, current_position)
        if (current_position[0] - 1, current_position[1] + 1) == position:
            move_valid = self.verify_southwest_move(player, position, current_position)
        if (current_position[0] + 1, current_position[1] + 1) == position:
            move_valid = self.verify_southeast_move(player, position, current_position)
        return move_valid

    def verify_northwest_move(self, player, position, current_position):
        """
        Verifies if moves to the northwest are valid, takes player, position and current_position as a parameter,
        returns True is move is valid, False if not
        """
        other_player = ""
        if player == 1:
            other_player = "P2"
        elif player == 2:
            other_player = "P1"
        cells = self.get_board().get_cells()
        horizontal_walls = self.get_board().get_horizontal_rows()
        if cells.get(position) is None:
            if cells.get((current_position[0], current_position[1] - 1)) == other_player:
                if horizontal_walls.get((current_position[0], current_position[1] - 1)) is not None:
                    if horizontal_walls.get(current_position) is None:
                        return True
        return False

    def verify_northeast_move(self, player, position, current_position):
        """
        Verifies if a move is valid to the northeast, takes player, position and current_position as parameters,
        returns True if move is valid, False if not
        """
        other_player = ""
        if player == 1:
            other_player = "P2"
        elif player == 2:
            other_player = "P1"
        cells = self.get_board().get_cells()
        horizontal_walls = self.get_board().get_horizontal_rows()
        if cells.get(position) is None:
            if cells.get((current_position[0], current_position[1] - 1)) == other_player:
                if horizontal_walls.get((current_position[0], current_position[1] - 1)) is not None:
                    if horizontal_walls.get(current_position) is None:
                        return True
        return False

    def verify_southwest_move(self, player, position, current_position):
        """
        Verifies if a move is valid to the southwest, takes player, position and current_position as parameters,
        returns True if move is valid, False if not
        """
        other_player = ""
        if player == 1:
            other_player = "P2"
        elif player == 2:
            other_player = "P1"
        cells = self.get_board().get_cells()
        horizontal_walls = self.get_board().get_horizontal_rows()
        if cells.get(position) is None:
            if cells.get((current_position[0], current_position[1] + 1)) == other_player:
                if horizontal_walls.get((current_position[0], current_position[1] + 1)) is None:
                    if horizontal_walls.get((current_position[0], current_position[1] + 2)) is not None:
                        return True
        return False

    def verify_southeast_move(self, player, position, current_position):
        """
        Verifies if a diagonal move to the southeast is valid. Takes player, position and current_position as a
        parameter. Returns True if move is valid, False if not
        """
        other_player = ""
        if player == 1:
            other_player = "P2"
        elif player == 2:
            other_player = "P1"
        cells = self.get_board().get_cells()
        horizontal_walls = self.get_board().get_horizontal_rows()
        if cells.get(position) is None:
            if cells.get((current_position[0], current_position[1] + 1)) == other_player:
                if horizontal_walls.get((current_position[0], current_position[1] + 1)) is None:
                    if horizontal_walls.get((current_position[0], current_position[1] + 2)) is not None:
                        return True
        return False

    def verify_two_space_moves(self, player, position, current_position):
        """
        Verify if moves that hop over an opposing piece are valid, takes player, position and current position
        as parameters, returns True if move is valid, False if not
        """
        move_valid = False
        if (current_position[0], current_position[1] - 2) == position:
            move_valid = self.verify_two_up_move(player, position, current_position)
        if (current_position[0], current_position[1] + 2) == position:
            move_valid = self.verify_two_down_move(player, position, current_position)
        return move_valid

    def verify_two_up_move(self, player, position, current_position):
        """
        Verifies if a move two spaces up from where the current pawn is at is valid. Takes player, position and
        current position as parameters, returns True if move is valid, False if not
        """
        other_player = ""
        if player == 1:
            other_player = "P2"
        elif player == 2:
            other_player = "P1"
        cells = self.get_board().get_cells()
        horizontal_walls = self.get_board().get_horizontal_rows()
        if cells.get(position) is None:
            if cells.get((current_position[0], current_position[1] - 1)) == other_player:
                if horizontal_walls.get((current_position[0], current_position[1] - 1)) is None:
                    if horizontal_walls.get(current_position) is None:
                        return True
        return False

    def verify_two_down_move(self, player, position, current_position):
        """
        Verifies if a move two spaces down from where the current pawn is at is valid. Takes player, position and
        current position as parameters. Returns True if move is valid, False if not
        """
        other_player = ""
        if player == 1:
            other_player = "P2"
        elif player == 2:
            other_player = "P1"
        cells = self.get_board().get_cells()
        horizontal_walls = self.get_board().get_horizontal_rows()
        if cells.get(position) is None:
            if cells.get((current_position[0], current_position[1] + 1)) == other_player:
                if horizontal_walls.get((current_position[0], current_position[1] + 2)) is None:
                    if horizontal_walls.get((current_position[0], current_position[1] + 1)) is None:
                        return True
        return False

    def decrement_player_fence(self, player):
        """
        Decreases a player's fence by one, takes a player parameter as an integer
        """
        if player == 1:
            self._player_one_fences -= 1
        elif player == 2:
            self._player_two_fences -= 1

    def print_board(self):
        """
        Prints current state of the board
        """
        board = self.get_board()
        board.display_board()

q = QuoridorGame()
q.move_pawn(1, (4,1))
q.move_pawn(2, (4,7))
q.move_pawn(1, (4,2))
q.place_fence(2, 'v', (4,2)) #p2 starts putting fence left fence
q.place_fence(1, 'v', (7,1)) #dumb move to pass
q.place_fence(2, 'v', (5,2)) #right fence
q.place_fence(1,'v', (7,3)) #dumb move to pass
print(q.place_fence(2, 'h', (2,4))) #northern fence
q.place_fence(1, 'v', (7,2)) #dumb move to pass
q.print_board()