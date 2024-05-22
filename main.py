# import tkinter as tk # for the UI
import tkinter as tk
from tkinter import filedialog # for the file selection in UI
# from PIL import Image, ImageTk, ImageOps # for the image import and then transforming it to a TK-friendly image

# internal dependencies
from internal_classes import DataManager
from userinterface import UserInterface
from imagemanipulation import CanvasManager


if __name__ == "__main__":
    root = tk.Tk() # Creating Tk instance
    root.title("Perspective Distance Estimation") # window title
    data_manager = DataManager() # creating DataManager instance
    canvas_manager = CanvasManager(root) # and CanvasManager with the root as an argument
    #canvas_manager.import_image("/home/ssotoma/Documentos/Universidad/Master/Abschlussarbeit/Data/test2.jpg")
    # create_ui(root, data_manager, canvas_manager) # now we can start the UI
    my_userinterface = UserInterface(root, data_manager, canvas_manager)