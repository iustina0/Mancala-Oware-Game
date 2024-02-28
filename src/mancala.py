import random
from tkinter import *
from PIL import Image
from PIL import ImageTk


class MancalaGame:
    """Class representing the Mancala game logic.

    Attributes:
        gameframe: The game frame window.
        board: An instance of the MancalaBoard representing the game board.
        current_player: The current player's turn (1 or 2).
        gametype: The type of game ("multiplayer" or "singleplayer").
        p1: ImageTk instance for player 1 image.
        p2: ImageTk instance for player 2 image.
        end_button: Tkinter Button for returning to the menu.
    """
    def __init__(self, board, frame) -> None:
        """Initializer for MancalaGame class.

        :param board: An instance of the MancalaBoard representing the game board.
        :param frame: The gameGUI frame window that initialized the object(the parent).
        """
        self.gameframe = frame
        self.board = board
        self.current_player = 1
        self.gametype = self.gameframe.options["game type"]
        self.update_score()
        
        if self.gametype == "multiplayer":
            self.p1 = ImageTk.PhotoImage(Image.open("./resources/player1.png").resize((200, 250), resample=Image.BICUBIC))
            self.p2 = ImageTk.PhotoImage(Image.open("./resources/player2.png").resize((200, 250), resample=Image.BICUBIC))
        else:
            self.p1 = ImageTk.PhotoImage(Image.open("./resources/player.png").resize((200, 250), resample=Image.BICUBIC))
            self.p2 = ImageTk.PhotoImage(Image.open("./resources/player_computer.png").resize((200, 250), resample=Image.BICUBIC))
        self.end_button = Button(self.gameframe, text ="Menu", command = self.go_to_menu)
       
    def pocket_clicked(self, event):
        """Method to handle pocket click event. 
        If a pocket is clicked and the pocket belongs to the current player a move is made

        :param  event: Tkinter event object.

        """
        x, y = event.x, event.y
        flag = False
        radius = self.gameframe.circle_radius
        for h in self.gameframe.pocket_coords[self.current_player-1]:
            distance = ((x - h[0])**2 + (y - h[1])**2)**0.5
            if distance < radius:
                flag = True
                hole = (h)

        if flag:
            self.make_move(self.gameframe.pocket_coords[self.current_player-1].index(hole))

    def make_move(self, pocket):
        """Method to make a move in the game.
        After a pocket is picked it plays the move in the game board object and inthe graphics throug an animation

        :param pocket: The pocket index where the move is made.

        """
        marbles = self.board.column_p1[pocket] if self.current_player == 1 else self.board.column_p2[pocket]
        if marbles == 0:
            return
        go_again = self.board.make_move(self.current_player, pocket)
        self.animate_move(self.current_player, pocket, marbles, go_again)
        self.update_score()

    def computer_move(self):
        """Method to handle the computer's move in single-player mode.
        It gets what are the posible moves and then it chooses one of them
        
        """
        posible_moves = self.board.get_posible_move(2)
        if len(posible_moves) == 0:
            self.continue_play(2, False)
            return
        move = random.choice(posible_moves)
        marbles = self.board.column_p2[move]
        go_again = self.board.make_move(2, move)
        self.animate_move(2, move, marbles, go_again)
        self.update_score()

    def animate_move(self, player, pocket, marbles, go_again):
        """Method to animate the move on the game board.
        For each marbles in the pocket it determins where it needs to go and the origin point

        :param player: The player making the move.
        :param pocket: The pocket index where the move is made.
        :param marbles: Number of marbles in the pocket.
        :param go_again: Tuple indicating if the player gets another turn or a capture accurs.
        """
        origin = self.gameframe.pocket_coords[player-1][pocket]
        go_to = self.get_go_to_cells(player, pocket, marbles)
        marbles = []

        for i in range(len(go_to)):
            dic = {}
            dic["marble"] = self.gameframe.canvas.create_image(origin[0], origin[1], anchor=CENTER, image=self.gameframe.marble_image)
            dic["origin"] = origin
            dic["position"] = origin
            dic["get to"] = go_to[i]
            marbles.append(dic)
        self.animate_marble_helper(marbles, 0, player, go_again)

    def animate_marble_helper(self, marbles, index, player, go_again):
        """Helper method for animating marbles on the game board.
        Recursive function that moves each marble a 1/40 of the distance it needs to traves thours the destination
        After the animation is over it calls the method that reasignes vales for the next move

        :param marbles: List of marble dictionaries containing information about each marble.
        :param index: Current animation frame index.
        :param player: The player making the move.
        :param go_again: Tuple indicating if the player gets another turn and the type of move (e.g., "capture").
        """
        if index < 40:
            for m in marbles:
                dx = (m["get to"][0] - m["origin"][0]) / 40
                dy = (m["get to"][1] - m["origin"][1]) / 40

                x = m["position"][0] + dx
                y = m["position"][1] + dy

                self.gameframe.canvas.coords(m["marble"], x, y)
                self.gameframe.canvas.tag_raise(m["marble"])
                m["position"] = (x, y)

            self.gameframe.canvas.after(8, self.animate_marble_helper, marbles, index + 1, player, go_again)
        else:
            self.delete_all_marbles(marbles)
            self.continue_play(player, go_again)

    def get_go_to_cells(self, player, pocket, marbles):
        """Method to calculate the target cells for marbles during animation.

        :param player: The player making the move.
        :param pocket: The pocket index where the move is made.
        :param marbles: Number of marbles in the pocket.

        :return List of target cells for the marbles.
        """
        go_to = []
        if player == 1:
            player_house = (180, 283)
        else:
            player_house = (1020, 283)
        
        centers = self.gameframe.pocket_coords

        column = player
        if pocket == self.board.pockets - 1 and player == 2 or pocket == 0 and player == 1:
            column = -1
            index = 0
        else:
            index = pocket + 1 if player == 2 else pocket - 1
        for i in range(marbles):
            if column == -1:
                go_to.append(player_house)
                column = 2 if player == 1 else 1
                index = 0 if player == 1 else self.board.pockets - 1
            else:
                go_to.append(centers[column-1][index])

                index = index + 1 if column == 2 else index - 1

                if index == self.board.pockets and column == 2 and player == 1:
                    index = self.board.pockets - 1
                    column = 1
                elif index == self.board.pockets and column == 2 and player == 2:
                    column = -1
                    index = 0
                elif index == -1 and column == 1 and player == 2:
                    index = 0
                    column = 2
                elif  index == -1 and column == 1 and player == 1:
                    column = -1
                    index = 0

        return go_to

    def continue_play(self, player, go_again):
        """Method to continue the game after a move.
        It reasignes values to current player for the next move, or calls for a computer move.
        Before that it makes sure that the game isn't over or a capture needs to happen

        :param player: The player who made the move.
        :param go_again: Tuple indicating if the player gets another turn and the type of move (e.g., "capture").
        """
        for i in range(self.gameframe.pockets):
            self.gameframe.draw_marbles_in_pocket((i, 0), self.board.column_p1[i])
            self.gameframe.draw_marbles_in_pocket((i, 1), self.board.column_p2[i])
        self.gameframe.draw_marbles_in_house(1, self.board.house_p1)
        self.gameframe.draw_marbles_in_house(2, self.board.house_p2)

        if self.board.check_finish():
            self.animate_end_game(player)
            self.gameframe.canvas.after(4000, self.endgame_screen)
            return

        if go_again[0] == "capture":
            player_house = (180, 283) if player ==1 else (1020, 283)
            self.animate_capture(player, go_again[1], player_house)
            if self.board.check_finish():
                self.animate_end_game(player % 2 + 1)
                self.gameframe.canvas.after(4000, self.endgame_screen)
            return

        if go_again[0] == True and player == 2 and self.gametype == "singleplayer":
            self.computer_move()
        elif go_again[0] == True and self.gametype == "multiplayer":
            pass
        elif go_again[0] == True and self.gametype == "singleplayer":
            pass
        elif go_again[0] == False and self.gametype == "multiplayer":
            self.current_player = (self.current_player % 2) + 1
            self.gameframe.current_player = self.current_player
        elif go_again[0] == False and self.gametype == "singleplayer" and player == 1:
            self.computer_move()

    def animate_capture(self, player, pocket, player_house):
        """Method to animate the capture of marbles.
        It animates each marble in the pocket that is captures to the house of the current player

        :param player: The player capturing marbles.
        :param pocket: The pocket index from which marbles are captured.
        :param player_house: Coordinates of the player's house.
        """
        marble = self.board.column_p1[pocket] if player ==2 else self.board.column_p2[pocket]
        origin = self.gameframe.pocket_coords[0][pocket] if player == 2 else self.gameframe.pocket_coords[1][pocket]

        marbles = []
        for _ in range(marble):
            dic = {}
            dic["marble"] = self.gameframe.canvas.create_image(origin[0], origin[1], anchor=CENTER, image=self.gameframe.marble_image)
            dic["origin"] = origin
            dic["position"] = origin
            marbles.append(dic)
        if self.board.check_finish():
            if player == 1:
                self.board.house_p2 += self.board.column_p2[pocket]
                self.board.column_p2[pocket] = 0
            elif player == 2:
                self.board.house_p1 += self.board.column_p1[pocket]
                self.board.column_p1[pocket] = 0
        else:
            self.board.capture(player, pocket)
        self.update_score()
        self.animate_capture_helper(marbles, player_house, player, pocket,  0)
        self.update_score()

    def animate_capture_helper(self, marbles, house, player, pocket, index):
        """Helper method for animating the capture of marbles.
        Recursive function that moves that marbles 1/40 of their way to the player house

        :param marbles: List of marble dictionaries containing information about each marble.
        :param house: Coordinates of the player's house.
        :param player: The player capturing marbles.
        :param pocket: The pocket index from which marbles are captured.
        :param index: Current animation frame index.
        """
        if index < 40:
            for m in marbles:
                dx = (house[0] - m["origin"][0]) / 40
                dy = (house[1] - 30 + ((len(marbles)/2 - marbles.index(m)) * 20)%90 - m["origin"][1]) / 40

                x = m["position"][0] + dx
                y = m["position"][1] + dy

                self.gameframe.canvas.coords(m["marble"], x, y)
                self.gameframe.canvas.tag_raise(m["marble"])
                m["position"] = (x, y)

            self.gameframe.canvas.after(8, self.animate_capture_helper, marbles, house, player, pocket, index + 1)
        else:
            self.delete_all_marbles(marbles)
            if player == 1:
                self.gameframe.draw_marbles_in_house(1, self.board.house_p1)
                self.gameframe.draw_marbles_in_house(2, self.board.house_p2)
                self.gameframe.draw_marbles_in_pocket((pocket, 1), 0)
            else:
                self.gameframe.draw_marbles_in_house(1, self.board.house_p1)
                self.gameframe.draw_marbles_in_house(2, self.board.house_p2)
                self.gameframe.draw_marbles_in_pocket((pocket, 0), 0)
            if not self.board.check_finish():
                if self.gametype == "singleplayer" and player == 1:
                    self.computer_move()
                elif self.gametype == "multiplayer":
                    self.current_player = (self.current_player % 2) + 1
                    self.gameframe.current_player = self.current_player
            self.update_score()

    def delete_all_marbles(self, marbles):
        """Helper function that delets all the animated marbles
        
        """
        for m in marbles:
            self.gameframe.canvas.delete(m["marble"])

    def update_score(self):
        """Method to update and display the current score.
        
        """
        self.gameframe.score_p1.lift()
        self.gameframe.score_p2.lift()
        self.gameframe.score_p1.config(text = str(self.board.house_p1))
        self.gameframe.score_p2.config(text = str(self.board.house_p2))

    def animate_end_game(self, player):
        """Method to animate the end of the game.
        The method puts in motion the ending of the game when a player column is left empty.
        The left marbles are moves to the coresonding player house in an animation

        :param player: The winning player.

        """
        player = player % 2 + 1
        player_house = (180, 283) if player ==1 else (1020, 283)
        marbles = self.board.column_p1 if player == 1 else self.board.column_p2
        for i in range(self.gameframe.pockets):
            if marbles[i] != 0:
                self.animate_capture(player % 2 + 1, i, player_house)
        
    def endgame_screen(self):
        """Method to display the endgame screen and animations.
        
        """
        
        self.gameframe.score_p1.lower()
        self.gameframe.score_p2.lower()
        self.gameframe.unbind_buttons()
        end_screen = self.gameframe.canvas.create_image(610, 1000, anchor = CENTER, image = self.gameframe.end_screen)
        self.animate_end_screen(end_screen, 1000, 0)

    def animate_end_screen(self, screen, cy, index):
        """Method to animate the endgame screen.
        It raises the end screen and places the score and playes 

        :param screen: The endgame screen image.
        :param cy: Current y-coordinate of the screen.
        :param index: Current animation frame index.
        """
        if index < 40:
            dy = (333 - 1000) / 40
            y = cy + dy

            self.gameframe.canvas.coords(screen, 610, y)
            self.gameframe.canvas.tag_raise(screen)
            cy = y

            self.gameframe.canvas.after(8, self.animate_end_screen, screen, cy, index + 1)
        else:
            p1 = self.gameframe.canvas.create_image(200, 333, anchor = CENTER, image = self.p1)
            p2 = self.gameframe.canvas.create_image(1020, 333, anchor = CENTER, image = self.p2)
            self.gameframe.canvas.tag_raise(p1)
            self.gameframe.canvas.tag_raise(p2)
            s1 = self.board.house_p1
            s2 = self.board.house_p2
            self.gameframe.end_s1.place(x = 450 , y= 333)
            self.gameframe.end_s2.place(x = 750 , y= 333)
            self.gameframe.canvas.after(3000, lambda: None)
            self.gameframe.end_s1.lift()
            self.gameframe.end_s2.lift()
            self.end_button.lift()
            self.animate_score(0, s1, 1)
            self.animate_score(0, s2, 2)
            self.end_button.place(x= 600, y = 600)

    def animate_score(self, i, score, player):
        """Method to animate the display of scores.
        Animates the score to increment till it reaches the target

        :param i: Current score.
        :param score: The final score.
        :param player: The player whose score is being animated.
        """
        if i < score:
            if player == 1:
                new_s = i + 1
                self.gameframe.end_s1.config(text = str(new_s))
                self.gameframe.canvas.after(50, self.animate_score, new_s, score, player)
                
            elif player == 2:
                new_s = i + 1
                self.gameframe.end_s2.config(text = str(new_s))
                self.gameframe.canvas.after(50, self.animate_score, new_s, score, player)
        else:
            pass

    def go_to_menu(self):
        """Method to return to the main menu.
        
        """
        self.gameframe.end_s1.lower()
        self.gameframe.end_s2.lower()
        self.end_button.lower()
        self.gameframe.controller.go_to_menu()



    