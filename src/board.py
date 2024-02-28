import numpy as np


class Board:
    """Class for representing the Mancala board.
    
    Attributes:
        pockets(int): the number of pockets per column
        start_stones(int): the initial number of marbels in each pocket
        column_p1, column_p2(list): a list of the current state of a player's column with each element being the number of marbels in the index pocket
        house_p1, house_p2(int): the nr of marbles in a player's house
        
    """

    def __init__(self, pockets, marbles) -> None:
        """Initializer for the Mancala board.

        :param pockets: Number of pockets a player has in their column.
        :param marbles: Number of marbles in each pocket in the beginning.
        """
        self.pockets = pockets
        self.start_stones = marbles
        self.column_p1 = np.zeros((self.pockets,), dtype=np.int32)
        self.column_p2 = np.zeros((self.pockets,), dtype=np.int32)

        for i in range(self.pockets):
            self.column_p1[i] = self.start_stones
            self.column_p2[i] = self.start_stones

        self.house_p1 = 0
        self.house_p2 = 0

    def get_posible_move(self, player) -> list:
        """Get the posible move for a player. The posible moves are the pockets that have marbels in them

        :param player(int): The player that wants to make a move

        :return: A list of indexes of pockest with marbles in the player column 

        """
        if player == 1:
            return [i for i in range(self.pockets) if self.column_p1[i] != 0]
        elif player == 2:
            return [i for i in range(self.pockets) if self.column_p2[i] != 0]
    
    def capture(self, player, index) -> None:
        """Capturing of a oposite pockets acoording to the game rules (when the last marble is placed in a empty pocket in the current playes collum the player captures the marbels in the oposite pocket)
        
        :param player(int): the player that placed the marbel
        :param index(int): the index of the pocket

        :return: None

        """
        if player == 1:
            self.house_p1 += self.column_p2[index]
            self.column_p2[index] = 0
        elif player == 2:
            self.house_p2 += self.column_p1[index]
            self.column_p1[index] = 0

    def make_move(self, player, pocket) -> tuple:
        """Make a move in the Mancala board based on the game rules. 
        The player choses a pocket on their side of the board and places the marbels in the next pockets in a clockwise direction 
        When the player gets to their house a marble is placed in in but the oponents house is skiped.
        If the last marble is placed in the player's house they get another turn
        If the last marble is placed in a empty pocket on the player's side a capture accurs
        

        :param player(int): the current player that makes the move
        :param pocket(int): the pocket the player chose for the move

        :return tuple:  (True, 0) - if the player get another turn
                        ("capture", index) - if a cupture needs to happen
                        (False, 0) - else
        
        """
        if player == 1:
            stone_count = self.column_p1[pocket]
            if pocket == 0:
                place_column = "house_p1"
                place_index = 0
            else:
                place_column = "p1"
                place_index = pocket - 1
            self.column_p1[pocket] = 0

        elif player == 2:
            stone_count = self.column_p2[pocket]
            if pocket == self.pockets - 1:
                place_column = "house_p2"
                place_index = 0
            else:
                place_column = "p2"
                place_index = pocket + 1
            self.column_p2[pocket] = 0

        while stone_count != 0:
            if place_column == "p1":
                if stone_count == 1 and player == 1 and self.column_p1[place_index] == 0:
                    self.column_p1[place_index] = 1
                    stone_count = 0
                    return ("capture", place_index)
                    capture(player, place_index)
                else:
                    self.column_p1[place_index] += 1
                    stone_count -= 1
                    if place_index == 0:
                        place_index = 0
                        place_column = "house_p1"
                    else:
                        place_index -= 1
                    
            elif place_column == "house_p1":
                if player == 2:
                    place_index = 0
                    place_column = "p2"
                else:
                    self.house_p1 += 1
                    if stone_count == 1:
                        stone_count = 0
                        return (True, 0)
                    else:
                        stone_count -= 1
                        place_index = 0
                        place_column = "p2"

            elif place_column == "p2":
                if stone_count == 1 and player == 2 and self.column_p2[place_index] == 0:
                    self.column_p2[place_index] = 1
                    stone_count = 0
                    return ("capture", place_index)
                else:
                    self.column_p2[place_index] += 1
                    stone_count -= 1
                    if place_index == self.pockets - 1:
                        place_index = 0
                        place_column = "house_p2"
                    else:
                        place_index += 1
                    
            elif place_column == "house_p2":
                if player == 1:
                    place_index = self.pockets - 1
                    place_column = "p1"
                else:
                    self.house_p2 += 1
                    if stone_count == 1:
                        stone_count = 0
                        return (True, 0)
                    else:
                        stone_count -= 1
                        place_index = self.pockets - 1
                        place_column = "p1"

        return (False, 0)

    def check_finish(self):
        """Checks if the game is over based on the game rules. The game is over when one of the player collums is empty

        :return: the player that has an empty collum or False if the game isn't over
        
        """
        if not [i for i in range(self.pockets) if self.column_p1[i] != 0]:
            return 1
        elif not [i for i in range(self.pockets) if self.column_p2[i] != 0]:
            return 2
        return False

    def end_game(self):
        """Executes the end game logic after the game rules. The player that still has marbels in the pockets captures all of them.

        :return: None
        
        """
        collum = self.check_finish()
        if collum == 1:
            self.house_p2 += sum([i for i in self.column_p2])
            self.column_p2 = np.zeros(self.pockets, dtype=np.int32)
        else:
            self.house_p1 += sum([i for i in self.column_p1])
            self.column_p1 = np.zeros(self.pockets, dtype=np.int32)
