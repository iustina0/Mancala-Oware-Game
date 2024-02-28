import sys
from tkinter import *
from PIL import Image
from PIL import ImageTk
from src.board import *
from tkinter import Label
from tkinter import font

class MenuPage(Frame):
    """Class representing the menu page of the Mancala board game.

    Attributes:
        controller: The game frame window.
        canvas: The Tkinter canvas for drawing the menu interface.
        options(dict): Dictionary containing default game options.
        bg_image: ImageTk instance for the background image.
        title_card: ImageTk instance for the title card image.
        txt_marble_no, txt_pocket_no: Tkinter Labels for displaying marble and pocket numbers.
        buttons_bg, play_button, bush_b1, bush_b2, multi, single, arrow1, arrow2, play_button_id, bush_b1_id, bush_b2_id, multi_id, single_id, arrow11_id, arrow12_id, arrow21_id, arrow22_id: Tkinter canvas item IDs for various graphic elements.
    """
    def __init__(self, parent, controller):
        """Initializer for MenuPage canvas instance.

        :param parent: The parent widget.
        :param controller: The game frame window.

        """
        Frame.__init__(self, parent)
        self.controller = controller
        self.canvas = Canvas(self, width=1220, height=646, bg="white")
        self.canvas.pack()
        self.options = {}
        self.options["game type"] = "multiplayer"
        self.options["pocket number"] = 6
        self.options["marble number"] = 6
        self.bg_image = ImageTk.PhotoImage(Image.open("./resources/table.jpg").resize((1220, 700), resample=Image.BICUBIC))
        self.title_card = ImageTk.PhotoImage(Image.open("./resources/bg-menu.png").resize((1220, 700), resample=Image.BICUBIC))
        
        self.play_button = ImageTk.PhotoImage(Image.open("./resources/play_button.png").resize((186,70), resample=Image.BICUBIC))
        self.bush_b1 = ImageTk.PhotoImage(Image.open("./resources/bush1-quit.png").resize((140,75), resample=Image.BICUBIC))
        self.bush_b2 = ImageTk.PhotoImage(Image.open("./resources/bush2.png").resize((122, 70), resample=Image.BICUBIC))
        self.buttons_bg = ImageTk.PhotoImage(Image.open("./resources/buttons-bg.png").resize((255, 335), resample=Image.BICUBIC))
        self.multi = ImageTk.PhotoImage(Image.open("./resources/multi-player.png").resize((130, 50), resample=Image.BICUBIC))
        self.single = ImageTk.PhotoImage(Image.open("./resources/single-player.png").resize((130, 50), resample=Image.BICUBIC))
        self.arrow1 = ImageTk.PhotoImage(Image.open("./resources/arrow.png").resize((58, 50), resample=Image.BICUBIC))
        self.arrow2 = ImageTk.PhotoImage(Image.open("./resources/arrow.png").resize((58, 50), resample=Image.BICUBIC).rotate(180))

        self.txt_marble_no = Label(self, text=str(self.options["marble number"]), bg = "#CC8860",fg = "#FFF9E3" , font=font.Font(family="Helvetica", size=24, weight="bold"))
        self.txt_pocket_no = Label(self, text=str(self.options["pocket number"]), bg = "#CC8860",fg = "#FFF9E3" , font=font.Font(family="Helvetica", size=24, weight="bold"))
        self.draw_menu()
        self.play_button_id = self.canvas.create_image(247, 361, anchor=NW, image=self.play_button)
        self.bush_b1_id = self.canvas.create_image(80, 499, anchor=NW, image=self.bush_b1)
        self.bush_b2_id = self.canvas.create_image(431, 506, anchor=NW, image=self.bush_b2)
        self.multi_id = self.canvas.create_image(879, 256, anchor=NW, image=self.multi)
        self.single_id = self.canvas.create_image(757, 253, anchor=NW, image=self.single)
        self.arrow11_id = self.canvas.create_image(769, 365, anchor=NW, image=self.arrow1)
        self.arrow12_id = self.canvas.create_image(930, 365, anchor=NW, image=self.arrow2)
        self.arrow21_id = self.canvas.create_image(769, 478, anchor=NW, image=self.arrow1)
        self.arrow22_id = self.canvas.create_image(930, 478, anchor=NW, image=self.arrow2)
        self.button_binding()

    def draw_menu(self):
        """Function for drawing the menu instance on the canvas.
       
        """
        self.txt_pocket_no.place(x=865, y=368)
        self.txt_marble_no.place(x=865, y=480)
        self.canvas.create_image(0, 0, anchor=NW, image=self.bg_image)
        self.canvas.create_image(0, 0, anchor=NW, image=self.title_card)
        self.canvas.create_image(751, 200, anchor=NW, image=self.buttons_bg)

    def button_binding(self):
        """Method used to bind the buttons to the wanted function after their creation.
        
        """
        self.canvas.tag_bind(self.play_button_id, "<Button-1>", self.play_game)
        self.canvas.tag_bind(self.play_button_id, "<Enter>", lambda event, id=self.play_button_id: self.button_hover_effect(event, id, 3, 1))
        self.canvas.tag_bind(self.play_button_id, "<Leave>", lambda event, id=self.play_button_id: self.button_leave_effect(event, id, 3, 1))

        self.canvas.tag_bind(self.bush_b1_id, "<Button-1>", sys.exit)
        self.canvas.tag_bind(self.bush_b1_id, "<Enter>", lambda event, id=self.bush_b1_id: self.button_hover_effect(event, id, 8, 0))
        self.canvas.tag_bind(self.bush_b1_id, "<Leave>", lambda event, id=self.bush_b1_id: self.button_leave_effect(event, id, 8, 0))

        self.canvas.tag_bind(self.single_id, "<Button-1>", self.single_player_change)

        self.canvas.tag_bind(self.arrow11_id, "<Button-1>", lambda event: self.change_pocket_nr(event, -1))
        self.canvas.tag_bind(self.arrow11_id, "<Enter>", lambda event, id=self.arrow11_id: self.button_hover_effect(event, id, 2, 2))
        self.canvas.tag_bind(self.arrow11_id, "<Leave>", lambda event, id=self.arrow11_id: self.button_leave_effect(event, id, 2, 2))
        
        self.canvas.tag_bind(self.arrow12_id, "<Button-1>", lambda event: self.change_pocket_nr(event, 1))
        self.canvas.tag_bind(self.arrow12_id, "<Enter>", lambda event, id=self.arrow12_id: self.button_hover_effect(event, id, 2, 2))
        self.canvas.tag_bind(self.arrow12_id, "<Leave>", lambda event, id=self.arrow12_id: self.button_leave_effect(event, id, 2, 2))
        
        self.canvas.tag_bind(self.arrow21_id, "<Button-1>", lambda event: self.change_marble_nr(event, -1))
        self.canvas.tag_bind(self.arrow21_id, "<Enter>", lambda event, id=self.arrow21_id: self.button_hover_effect(event, id, 2, 2))
        self.canvas.tag_bind(self.arrow21_id, "<Leave>", lambda event, id=self.arrow21_id: self.button_leave_effect(event, id, 2, 2))
        
        self.canvas.tag_bind(self.arrow22_id, "<Button-1>", lambda event: self.change_marble_nr(event, 1))
        self.canvas.tag_bind(self.arrow22_id, "<Enter>", lambda event, id=self.arrow22_id: self.button_hover_effect(event, id, 2, 2))
        self.canvas.tag_bind(self.arrow22_id, "<Leave>", lambda event, id=self.arrow22_id: self.button_leave_effect(event, id, 2, 2))
        
    def change_pocket_nr(self, event, increment):
        """Method to change the pocket number in the game options.

        :param event: Tkinter event object.
        :param increment: Increment value for changing the pocket number.
        """
        if self.options["pocket number"] + increment < 11 and self.options["pocket number"] + increment  > 3:
            self.options["pocket number"] += increment
            self.txt_pocket_no.config(text=str(self.options["pocket number"]))
            if self.options["pocket number"] == 10:
                self.txt_pocket_no.place(x=860, y=368)
            else:  
                self.txt_pocket_no.place(x=865, y=368)

    def change_marble_nr(self, event, increment):
        """Method to change the marble number in the game options.

        :param event: Tkinter event object.
        :param increment: Increment value for changing the marble number.
        """
        if self.options["marble number"] + increment < 11 and self.options["marble number"] + increment  > 3:
            self.options["marble number"] += increment
            self.txt_marble_no.config(text=str(self.options["marble number"]))
            if self.options["marble number"] == 10:
                self.txt_marble_no.place(x=860, y=480)
            else:  
                self.txt_marble_no.place(x=865, y=480)
    
    def single_player_change(self, event=None):
        """Method to switch to single-player mode in the game options.

        :param event: Tkinter event object (default is None).
        """
        self.options["game type"] = "singleplayer"
        xm, ym = self.canvas.coords(self.multi_id)
        xs, ys = self.canvas.coords(self.single_id)
        self.canvas.coords(self.multi_id, xm + 6, ym - 3)
        self.canvas.coords(self.single_id, xs - 6, ys + 3)
        self.canvas.tag_unbind(self.single_id, "<Button-1>")
        self.canvas.tag_bind(self.multi_id, "<Button-1>", self.multi_player_change)

    def multi_player_change(self, event=None):
        """Method to switch to multiplayer mode in the game options.

        :param event: Tkinter event object (default is None).
        """
        self.options["game type"] = "multiplayer"
        xm, ym = self.canvas.coords(self.multi_id)
        xs, ys = self.canvas.coords(self.single_id)
        self.canvas.coords(self.multi_id, xm - 6, ym + 3)
        self.canvas.coords(self.single_id, xs + 6, ys - 3)
        self.canvas.tag_bind(self.single_id, "<Button-1>", self.single_player_change)
        self.canvas.tag_unbind(self.multi_id, "<Button-1>")

    def button_hover_effect(self, event, button_id, dx, dy):
        """Method for button hover effect.

        :param event: Tkinter event object.
        :param button_id: Tkinter canvas item ID of the button.
        :param dx: X-axis shift for hover effect.
        :param dy: Y-axis shift for hover effect.
        """
        x,y = self.canvas.coords(button_id)
        self.canvas.coords(button_id, x + dx, y - dy)

    def button_leave_effect(self, event, button_id, dx, dy):
        """Method for button leave effect.

        :param event: Tkinter event object.
        :param button_id: Tkinter canvas item ID of the button.
        :param dx: X-axis shift for leave effect.
        :param dy: Y-axis shift for leave effect.
        """
        x,y = self.canvas.coords(button_id)
        self.canvas.coords(button_id, x - dx, y + dy)

    def play_game(self, event=None):
        """Method to start the game with updated options.
        
        """
        self.controller.update_settings(self.options)
        self.controller.play_game()

