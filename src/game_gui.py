import random
from tkinter import *
from PIL import Image
from PIL import ImageTk
from src.board import Board
from src.mancala import MancalaGame
from tkinter import Label
from tkinter import font

class GamePage(Frame):
    """Class representing the game page of the Mancala board game.

    Attributes:
        controller: The game frame window.
        options(dict): Dictionary containing game options.
        pockets(int): Number of pockets for each player.
        marbles(int): Number of marbles in each pocket.
        game_type(str): Type of the game ("multiplayer" or "single player").
        board(Board): The Mancala board instance.
        current_player(int): The current player (1 or 2).
        canvas: The Tkinter canvas for drawing the game interface.
        circle_radius(int): Radius of the circle for highlighting pockets.
        circle_id: Identifier for the circle highlighting a hovered pocket.
        ord_marbles: Random order of marbles displayed in a house.
        ord_overlap_marbles: Random order of marbles displayed in a house after the first layer is compleated.
        ord_pockets: Random order of marbles displayed in a pocket.
        end_s1, end_s2, score_p1, score_p2: Tkinter Labels for displaying scores.
        player1, player2, player, playerc, end_screen, table_image, board_image, house_image, hole_image, star_image, marble_image, pauseimg, bush_b1, bush_b2: ImageTk instances for various graphic elements.
    """
    def __init__(self, parent, controller):
        """Initializer for GamePage canvas instance.
        """
        Frame.__init__(self, parent)
        self.controller = controller
        self.options = self.controller.options
        self.pockets = self.options["pocket number"]
        self.marbles = self.options["marble number"]
        self.game_type = self.options["game type"]
        self.board = None
        self.current_player = 1
        self.canvas = Canvas(self, width=1220, height=646, bg="white")
        self.canvas.pack()

        self.circle_radius = int(((int(960/(self.pockets + 2)/2))+20)/2)
        self.circle_id = None

        self.ord_marbles = [random.sample(range(20), 20), random.sample(range(20), 20)]
        self.ord_ovelap_marbles = [random.sample(range(20), 20), random.sample(range(20), 20)]
        self.ord_pockets = random.sample(range(9), 9)

        self.end_s1 = Label(self, text=str(0), bg = "#FACD59",fg = "#880015" , font=font.Font(family="Helvetica", size=40, weight="bold"))
        self.end_s2 = Label(self, text=str(0), bg = "#880015",fg = "#FACD59" , font=font.Font(family="Helvetica", size=40, weight="bold"))
        self.score_p1 = Label(self, text=str(0), bg = "#BDD3E0",fg = "#000000" , font=font.Font(family="Helvetica", size=18, weight="bold"))
        self.score_p2 = Label(self, text=str(0), bg = "#CAE9FD",fg = "#000000" , font=font.Font(family="Helvetica", size=18, weight="bold"))
        
        self.player1 = ImageTk.PhotoImage(Image.open("./resources/player1.png").resize((100, 125), resample=Image.BICUBIC))
        self.player2 = ImageTk.PhotoImage(Image.open("./resources/player2.png").resize((100, 125), resample=Image.BICUBIC))
        self.player = ImageTk.PhotoImage(Image.open("./resources/player.png").resize((100, 125), resample=Image.BICUBIC))
        self.playerc = ImageTk.PhotoImage(Image.open("./resources/player_computer.png").resize((100, 125), resample=Image.BICUBIC))
        self.end_screen = ImageTk.PhotoImage(Image.open("./resources/end_screen.png").resize((1220, 666), resample=Image.BICUBIC))
        self.tabel_image = ImageTk.PhotoImage(Image.open("./resources/table.jpg").resize((1220, 700), resample=Image.BICUBIC))
        self.board_image = ImageTk.PhotoImage(Image.open("./resources/board.png").resize((980, 310), resample=Image.BICUBIC))
        self.house_image = ImageTk.PhotoImage(Image.open("./resources/house.png").resize((70, 180), resample=Image.BICUBIC))
        self.hole_image = ImageTk.PhotoImage(Image.open("./resources/hole.png").resize((self.circle_radius*2, self.circle_radius*2), resample=Image.BICUBIC))
        self.star_image = ImageTk.PhotoImage(Image.open("./resources/star.png").resize((50, 50), resample=Image.BICUBIC))
        self.marble_image = ImageTk.PhotoImage(Image.open("./resources/marble.png").resize((20, 20), resample=Image.BICUBIC))
        self.pauseimg = ImageTk.PhotoImage(Image.open("./resources/pause-blurr.png").resize((1220,666), resample=Image.BICUBIC))
        self.bush_b1 = ImageTk.PhotoImage(Image.open("./resources/bush1-pause.png").resize((140,75), resample=Image.BICUBIC))
        self.bush_b2 = ImageTk.PhotoImage(Image.open("./resources/bush2-menu.png").resize((122, 75), resample=Image.BICUBIC))

    def update_settings(self, options):
        """This method gets the game option form the menu page through the controller. 
        When changing the frame this method is called in the controller object and the game is updated with the wanted settings
        
        """
        self.options = options
        self.pockets = self.options["pocket number"]
        self.marbles = self.options["marble number"]
        self.game_type = self.options["game type"]
        if self.board:
            del self.board
        self.board = Board(self.pockets, self.marbles)
        self.draw_game()

    def draw_game(self):
        """Function for drawing a game instace on the canvas. 
        Starting with deleting all previos canvas elements and then drawing the background, buttons and in the end the board, playes and score
        
        """
        self.canvas.delete("all")

        self.pocket_marbles = [[0 for _ in range(self.pockets)] for _ in range(2)]
        self.house_marbles = [0, 0]
        self.canvas.create_image(0, 0, anchor=NW, image=self.tabel_image)
        self.canvas.create_image(612, 288, anchor=CENTER, image=self.board_image)
        self.house1_id = self.canvas.create_image(180, 283, anchor=CENTER, image=self.house_image)
        self.house2_id = self.canvas.create_image(1020, 283, anchor=CENTER, image=self.house_image)
        self.pause_id = None
        self.puse_btn_id = None
        self.bush_b2_id = self.canvas.create_image(431, 500, anchor=NW, image=self.bush_b2)
        self.bush_b1_id = self.canvas.create_image(80, 499, anchor=NW, image=self.bush_b1)
        self.bind_buttons()
        self.draw_pockets()
        for i in range(self.pockets):
            for j in range(2):
                self.draw_marbles_in_pocket((i,j),self.marbles)
        self.draw_player()
        self.start_game()

    def start_game(self):
        """Function that starts the game by creating a game object using the current board, setting the current player to 1 and adding a listener to determin when a pockes is clicked 
        
        """
        self.current_player = 1
        game = MancalaGame(self.board, self)
        self.canvas.bind("<Button-1>", game.pocket_clicked)

    def bind_buttons(self):
        """Method used to bind the buttons to the wanted function after their creation
        
        """
        self.canvas.bind("<Motion>", self.on_hover_over_pocket)

        self.canvas.tag_bind(self.bush_b1_id, "<Button-1>", self.pause)
        self.canvas.tag_bind(self.bush_b1_id, "<Enter>", lambda event, id=self.bush_b1_id: self.button_hover_effect(event, id, 8, 0))
        self.canvas.tag_bind(self.bush_b1_id, "<Leave>", lambda event, id=self.bush_b1_id: self.button_leave_effect(event, id, 8, 0))

        self.canvas.tag_bind(self.bush_b2_id, "<Button-1>", lambda event: self.controller.go_to_menu())
        self.canvas.tag_bind(self.bush_b2_id, "<Enter>", lambda event, id=self.bush_b2_id: self.button_hover_effect(event, id, 8, 0))
        self.canvas.tag_bind(self.bush_b2_id, "<Leave>", lambda event, id=self.bush_b2_id: self.button_leave_effect(event, id, 8, 0))

    def unbind_buttons(self):
        """Method that unbind the buttons from the asociated function.
        This method is used when pause is called so that the binded objects loose their functionalites
        
        """
        self.canvas.unbind("<Motion>")

        self.canvas.tag_unbind(self.bush_b1_id, "<Button-1>")
        self.canvas.tag_unbind(self.bush_b1_id, "<Enter>")
        self.canvas.tag_unbind(self.bush_b1_id, "<Leave>")

        self.canvas.tag_unbind(self.bush_b2_id, "<Button-1>")
        self.canvas.tag_unbind(self.bush_b2_id, "<Enter>")
        self.canvas.tag_unbind(self.bush_b2_id, "<Leave>")

    def pause(self, event = None):
        """Pause method used as a function for the pause button.
        When used the screen would be blured and the game would be put on pause
        
        """
        def unpause():
            self.bind_buttons()
            self.score_p1.lift()
            self.score_p2.lift()
            self.canvas.delete(self.pause_id)
            self.pause_btn_id.destroy()

        self.unbind_buttons()
        self.button_leave_effect(None, self.bush_b1_id, 6,0)
        self.pause_id = self.canvas.create_image(0,0, anchor=NW, image=self.pauseimg)
        self.canvas.tag_raise(self.pause_id)
        self.score_p1.lower()
        self.score_p2.lower()
        self.pause_btn_id = Button(self, text ="UNPAUSE", command = unpause)
        self.pause_btn_id.place(x=580,y=333)

    def draw_pockets(self):
        """Method used for drawing the board pockets based on the number of the pockes per player.
        The function calculates the radius and placement based on how meny need to be placed.
        It saves the id of each pocket image that is created for later manipulation 
        
        """
        center_1 = []
        id1 = []
        center_2 = []
        id2 = []
        column_wight =  int(760/self.pockets)

        for i in range(self.pockets):
            x,y = 220 + int(column_wight/2) + i * column_wight , 228
            id = self.canvas.create_image(x,y, anchor=CENTER, image=self.hole_image)
            center_1.append((x,y))
            id1.append(id)

        for i in range(self.pockets-1):
            self.canvas.create_image(220 + (i+1) * column_wight , 283, anchor=CENTER, image=self.star_image)

        for i in range(self.pockets):
            x,y = 220 + int(column_wight/2) + i * column_wight , 338
            id = self.canvas.create_image(x,y, anchor=CENTER, image=self.hole_image)
            center_2.append((x,y))
            id2.append(id)

        self.pocket_coords = [center_1,center_2]
        self.pocket_ids = [id1, id2]

    def draw_marbles_in_pocket(self, pocket, no_marbles):
        """Method for putting marbles in a pocket determined by the pocket position
        It starts by deleting all the previous marbles and raising the pocket so that it starts on a clear slate.
        Next based on the random order from the class initiation it places the marbles on 2 levels based on the numbers.
        The position within the pocket is determined by a 3*3 grid for the first layer and a 2*2 grid for the overlap.
        The maximum marbles that can be shown in a pocket is 13

        :param pocket(tuple): the position of the pocket with [0] being the player column and [1] being the pocket index on the column
        :param no_marbles: the number of marbles that it needs to place
        
        """
        if self.pocket_marbles[pocket[1]][pocket[0]] != 0:
            for m in self.pocket_marbles[pocket[1]][pocket[0]]:
                self.canvas.delete(m)
        if no_marbles == 0:
            self.canvas.tag_raise(self.pocket_ids[pocket[1]][pocket[0]])
            self.pocket_marbles[pocket[1]][pocket[0]] = 0
            return
        
        ids = []
        circle_dim = int(960/(self.pockets + 2)/2)+20
        sqr_dim = int(circle_dim - circle_dim/8)
        shift = sqr_dim/4
        small_shift = shift/2
        center = self.pocket_coords[pocket[1]][pocket[0]]
        self.canvas.tag_raise(self.pocket_ids[pocket[1]][pocket[0]])
        ordine_afisare = self.ord_pockets
        positions = [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]
        overlap_positions = [(0,0), (0,0), (0,0), (0,0)]
        for i in range(3):
            for j in range(3):
                x = center[0] + (-1 + j) * shift
                y = center[1] + (-1 + i) * shift
                positions[i*3+j] = (x,y)
        for i in range(2):
            for j in range(2):
                x = center[0] + (2*j - 1) * small_shift
                y = center[1] + (2*i - 1) * small_shift
                overlap_positions[i*2+j] = (x,y)
        for i in range(no_marbles):
            if i < 9:
                m=ordine_afisare[i]
                id = self.canvas.create_image(positions[m][0], positions[m][1], anchor=CENTER, image=self.marble_image)
            elif i < 13:
                id = self.canvas.create_image(overlap_positions[i%9][0], overlap_positions[i%9][1], anchor=CENTER, image=self.marble_image)
            else:
                break
            ids.append(id)
        self.pocket_marbles[pocket[1]][pocket[0]] = ids

    def draw_marbles_in_house(self, player, no_marbles):
        """Method for putting marbles in the player houses.
        As the pocket marbles placement it starts with deleting all the old marbles and raising the house image
        It continues with placing the marbles in a random preditermened pattern on 2 layers.
        The maximum nr of marbles that can be shown in a house is 40

        :param palyer(int): for picking the house
        :param no_marbles(int): the number of marbles that need to be placed
        
        """
        if no_marbles == 0: 
            if player == 1:
                self.canvas.tag_raise(self.house1_id)
                self.house_marbles[player - 1] = 0
            else:
                self.canvas.tag_raise(self.house2_id)
                self.house_marbles[player - 1] = 0
            return
        
        if self.house_marbles[player - 1] != 0:
            for m in self.house_marbles[player - 1]:
                self.canvas.delete(m)
            self.house_marbles[player - 1] = 0
        if player == 1:
            self.canvas.tag_raise(self.house1_id)
        else:
            self.canvas.tag_raise(self.house2_id)
        ordine = self.ord_marbles[player-1]
        ordine_overlap = self.ord_ovelap_marbles[player-1]
        positions = []
        positions_overlap = []
        if player == 1:
            x_c = 180
        else:
            x_c = 1020
        for i in range(8):
            for j in range(3):
                if not (i == 0 and j==0 or i==0 and j==2 or i==7 and j==0 or i==7 and j==2):
                    x = x_c - 35 +  18 + 18 * j 
                    y = 203 + 18 + i*18
                    positions.append((x,y))
        for i in range(20):
            x = positions[i][0] + 5
            y = positions[i][1] + 5
            positions_overlap.append((x,y))
        ids = []
        for i in range(no_marbles):
            if i < 20:
                m = ordine[i]
                id = self.canvas.create_image(positions[m][0], positions[m][1], anchor=CENTER, image=self.marble_image)
            elif i < 40:
                m = ordine_overlap[i%20]
                id = self.canvas.create_image(positions_overlap[m][0], positions_overlap[m][1], anchor=CENTER, image=self.marble_image)
            else:
                break
            ids.append(id)
        self.house_marbles[player - 1] = ids

    def draw_player(self):
        """method for placing the player images depending on the game type
        The function will use players labled 1 and 2 for multiplayer and a simple player and one labled C for playing with a computer
        Afetr the players are place the individual score for each one is also placed on the canvas.
        
        """
        if self.game_type == "multiplayer":
            self.canvas.create_image(60, 283, anchor=CENTER, image=self.player1)
            self.canvas.create_image(1160, 283, anchor=CENTER, image=self.player2)
        else:
            self.canvas.create_image(60, 283, anchor=CENTER, image=self.player)
            self.canvas.create_image(1160, 283, anchor=CENTER, image=self.playerc)
        self.score_p1.place(x=50, y=360)
        self.score_p2.place(x=1150, y=360)

    def button_hover_effect(self, event, button_id, dx, dy):
        """Method for moving a button object when hovered over
        
        """
        x,y = self.canvas.coords(button_id)
        self.canvas.coords(button_id, x + dx, y - dy)

    def button_leave_effect(self, event, button_id, dx, dy):
        """Method for moving the button object back after the mouse leaves the area
        
        """
        x,y = self.canvas.coords(button_id)
        self.canvas.coords(button_id, x - dx, y + dy)

    def on_hover_over_pocket(self, event):
        """Method for higlighting the hovered pocket so that the player knows what they pick.
        The higlighting only apears over the current players pockets
        
        """
        x, y = event.x, event.y
        flag = False
        radius = self.circle_radius
        for h in self.pocket_coords[self.current_player-1]:
            distance = ((x - h[0])**2 + (y - h[1])**2)**0.5
            if distance < radius:
                flag = True
                hole = (h)
        if flag:
            if self.circle_id is not None:
                self.canvas.delete(self.circle_id)
                self.circle_id = None
            color = "#A2853A" if self.current_player == 2 else "#880015"
            self.circle_id = self.canvas.create_oval(hole[0] - self.circle_radius, hole[1] - self.circle_radius,
                                                    hole[0] + self.circle_radius, hole[1] + self.circle_radius,
                                                    outline=color, width=2)
        else:
            if self.circle_id is not None:
                self.canvas.delete(self.circle_id)
                self.circle_id = None

    
    