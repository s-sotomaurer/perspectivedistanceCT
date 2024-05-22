# import tkinter as tk # for the UI
import tkinter as tk
from tkinter import filedialog # for the file selection in UI
from pathlib import Path

# internal dependencies
from internal_classes import DataManager
from userinterface import UserInterface
from imagemanipulation import CanvasManager


if __name__ == "__main__":
    root = tk.Tk() # Creating Tk instance
    root.title("Perspective Distance Estimation") # window title
    data_manager = DataManager() # creating DataManager instance
    canvas_manager = CanvasManager(root) # and CanvasManager with the root as an argument
    canvas_manager.import_image(Path(__file__).parent / 'HelpImage.png')
    my_userinterface = UserInterface(root, data_manager, canvas_manager)
