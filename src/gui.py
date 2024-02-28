from tkinter import *
from tkinter import Tk
from src.menu_gui import MenuPage
from src.game_gui import GamePage

class AppGUI(Tk):
    """Class representing the main application GUI for the Mancala game.

    Attributes:
        frames(dict): Dictionary to store different frames (MenuPage, GamePage).
        options(dict): Dictionary containing default game options.
    """
    def __init__(self, *args, **kwargs):
        """Initializer for AppGUI, sets up the main application window.

        :param args: Variable length argument list.
        :param kwargs: Arbitrary keyword arguments.
        """
        Tk.__init__(self, *args, **kwargs)
        self.title("Mancala")
        container = Frame(self) 
        container.pack(side = "top", fill = "both", expand = True) 
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {} 
        self.options = {}
        self.options["pocket number"] = 6
        self.options["marble number"] = 6
        self.options["game type"] = "multiplayer"
        for F in (MenuPage, GamePage):
            frame = F(container, self)
            self.frames[F] = frame 
            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.go_to_menu()


    def update_settings(self, options):
        """Updates the game settings with the provided options.

        :param options(dict): Dictionary containing game options.

        """
        self.options = options

    def play_game(self):
        """Switches to the GamePage frame and updates its settings.
        
        """
        frame = self.frames[GamePage]
        frame.update_settings(self.options)
        frame.tkraise()

    def go_to_menu(self):
        """Switches to the MenuPage frame.
        
        """
        frame = self.frames[MenuPage]
        frame.tkraise()
        frame = self.frames[MenuPage]
        frame.tkraise()
