import tkinter as tk
import os
from tkinter import filedialog
from pathlib import Path
from internal_classes import DataManager

# user interface functions (input)

# def create_ui(root, data_manager, canvas_manager):

#     # Create a button frame and place it in the first column
#     motherframe = tk.Frame(root)
#     motherframe.grid(row=0, column=0, rowspan=4, columnspan=1,sticky= "nsew")
#     motherframe.columnconfigure(0, weight=0)
#     motherframe.columnconfigure(1, weight=0)
#     motherframe.columnconfigure(2, weight=0)
#     # motherframe.rowconfigure(0, weight=1)
#     # motherframe.rowconfigure(1, weight=1)
#     # motherframe.rowconfigure(2, weight=1)
#     # motherframe.rowconfigure(3, weight=1)

#     button_frame_refimg = tk.Frame(motherframe)
#     button_frame_realdata = tk.Frame(motherframe)
#     button_frame_preview = tk.Frame(motherframe)
#     button_frame_save = tk.Frame(motherframe)

#     configure_frame(button_frame_refimg, column=0, row=0)
#     configure_frame(button_frame_realdata, column=0, row=1)
#     configure_frame(button_frame_preview, column=0, row=2)
#     configure_frame(button_frame_save, column=0, row=3)

#     # create map of frames to pass to button creation
#     frame_button_map = {
#     "1": button_frame_refimg,
#     "2": button_frame_realdata,
#     "3": button_frame_preview,
#     "4": button_frame_save
#     }

#     # create input fields and bind them to data manager
#     var_dict = create_input_fields(button_frame_preview, frame_button_map)
#     bind_input_fields(data_manager, var_dict)

#     # Create buttons for data management and canvas manipulation
#     create_buttons(data_manager, canvas_manager, frame_button_map)
#     # button_frame_realdata.grid_rowconfigure(7, weight=1)  # Allow the button frame to expand vertically

#     # place the canvas in the second column
#     canvas_manager.canvas.grid(row=0, column=3, sticky="nsew")
#     # root.columnconfigure(0, weight=1)  # Allow the motherframe to expand horizontally
#     root.columnconfigure(3, weight=1)  # Allow the canvas to expand horizontally

#     # Configure rows and columns to expand with the window
#     # canvas_manager.configure_grid_weights()  # Call the method to set grid weights
    
#     # Configure rows and columns inside the motherframe
#     motherframe.columnconfigure(0, weight=1)  # Allow the button frame to expand horizontally

#     # # Configure rows and columns to expand with the window inside the motherframe
#     # for frame in [button_frame_refimg, button_frame_realdata, button_frame_preview, button_frame_save]:
#     #     frame.columnconfigure(0, weight=1)
#     #     frame.columnconfigure(1, weight=1)

#     root.mainloop()

def configure_frame(frame, column, row):
    padx = 10
    pady = 20
    frame.grid(column=column, row=row, padx=padx, pady=pady, sticky="n")
    frame.configure(borderwidth=1, relief="raised")

def only_numeric_input(char):
    # Function to allow only numeric input and decimal point in Entry widget
    return char.isdigit() or char == '.'

def select_directory(canvas_manager):
    dir_path = filedialog.askdirectory(parent=canvas_manager.root)  # Pass the existing root window as parent
    if dir_path:
        canvas_manager.save_imageseries_sourcepath(dir_path)

def select_image(canvas_manager):
    file_path = filedialog.askopenfilename(parent=canvas_manager.root)  # Pass the existing root window as parent
    if file_path:
        canvas_manager.import_image(file_path)
        canvas_manager.save_image_path(file_path)
        file_path = Path(file_path)
        canvas_manager.save_imageseries_sourcepath(file_path.parent)
        

def create_input_fields(root, frame_button_map):
    """
    Creates and configures input fields for user interaction in a Tkinter GUI.

    Parameters:
        - root (Tk): The root Tkinter window where the input fields will be created.

    Returns:
        dict: A dictionary containing StringVar objects associated with each input field.

    This function sets up a user interface with labeled input fields for specific parameters.
    It uses Tkinter to create labels and entry fields in a grid layout. Each entry field is
    validated to accept only numeric input. The created StringVar objects are linked to the
    entry fields, allowing dynamic tracking of user input. The function returns a dictionary
    containing these StringVar objects for further use in updating the GUI and managing data.

    The function also includes user input validation, such that distance to 1 is smaller than
    distance to 2.
    """

    # Register the validation function for numeric input
    validate_numeric = root.register(only_numeric_input)

    # Define constant values for row and column indices
    ROW_POLE_WIDTH, ROW_DISTANCE_CAMERA_POLE1, ROW_DISTANCE_CAMERA_POLE2, ROW_DESIRED_DISTANCE, ROW_NUM_LINES, ROW_CAMERA_SIZE = 0, 1, 2, 0, 1, 3
    ROW_FILE_PATHS = 1
    COL_LABEL, COL_ENTRY = 0, 1

    # Information about labels, their row and column positions
    labels_info = [
        {"text": "Width of poles", "row": ROW_POLE_WIDTH, "column": COL_LABEL, "frame": "2"},
        {"text": "Distance camera - pole 1", "row": ROW_DISTANCE_CAMERA_POLE1, "column": COL_LABEL, "frame": "2"},
        {"text": "Distance camera - pole 2", "row": ROW_DISTANCE_CAMERA_POLE2, "column": COL_LABEL, "frame": "2"},
        {"text": "Grid distance", "row": ROW_DESIRED_DISTANCE, "column": COL_LABEL, "frame": "3"},
        {"text": "Number of new lines", "row": ROW_NUM_LINES, "column": COL_LABEL, "frame": "3"},
        {"text": "Camera height", "row": ROW_CAMERA_SIZE, "column": COL_LABEL, "frame": "2"},
        {"text": "Image series", "row": ROW_POLE_WIDTH, "column": COL_LABEL, "frame": "4"},
        {"text": "Reference image", "row": ROW_POLE_WIDTH, "column": COL_LABEL, "frame": "1"}
    ]

    # Information about entry fields, their row and column positions
    entry_info = [
        {"row": ROW_POLE_WIDTH, "column": COL_ENTRY, "frame": "2", "field_width": 4, "span": 1}, # pole width
        {"row": ROW_DISTANCE_CAMERA_POLE1, "column": COL_ENTRY, "frame": "2", "field_width": 4, "span": 1}, # distance to pole 1
        {"row": ROW_DISTANCE_CAMERA_POLE2, "column": COL_ENTRY, "frame": "2", "field_width": 4, "span": 1}, # distance to pole 2
        {"row": ROW_DESIRED_DISTANCE, "column": COL_ENTRY, "frame": "3", "field_width": 4, "span": 1}, # desired distance
        {"row": ROW_NUM_LINES, "column": COL_ENTRY, "frame": "3", "field_width": 4, "span": 1}, # number of lines
        {"row": ROW_CAMERA_SIZE, "column": COL_ENTRY, "frame": "2", "field_width": 4, "span": 1}, # camera
        {"row": ROW_FILE_PATHS, "column": 0, "frame": "4", "field_width": 35, "span": 2}, # image series
        {"row": ROW_FILE_PATHS, "column": 0, "frame": "1", "field_width": 35, "span": 2} # reference image
    ]

    # Dictionary to store StringVar objects for each entry field
    var_dict = {}

    # Create labels in the specified positions
    for label_info in labels_info:
        label_text = label_info["text"]
        label_row = label_info["row"]
        label_column = label_info["column"]
        frame_number = frame_button_map[label_info["frame"]]
        # Create labels with the specified text and positions
        label = tk.Label(frame_number, text=label_text)
        label.grid(
            column=label_column,
            row=label_row,
            pady = 5,
            padx = 5,
            sticky="e"
        )

    # Create entry fields with validation and store StringVar objects in the dictionary
    # for (row, col), text_var in zip(entry_info, ["real_pole_size", "distance_input", "distance_to_pole2", "desired_distance_input", "number_of_sleepers", "camera_height"]):
    #     # Create StringVar objects and associate them with entry fields
    #     var_dict[text_var] = tk.StringVar()
    #     # Create entry fields with key validation and link them to StringVar objects
    #     entry = tk.Entry(root, validate="key", validatecommand=(validate_numeric, '%S'), textvariable=var_dict[text_var])
    #     # Set entry fields in the specified positions and make them expandable in the "ew" direction
    #     entry.grid(row=row, column=col, sticky="w")    
    
    for entry_info, text_var in zip(entry_info, ["real_pole_size", "distance_input", "distance_to_pole2", "desired_distance_input", "number_of_sleepers", "camera_height", "path_image", "path_series"]):
        var_dict[text_var] = tk.StringVar()
        entry_row = entry_info["row"]
        entry_column = entry_info["column"]
        entry_frame = frame_button_map[entry_info["frame"]]
        entry_width = entry_info["field_width"]
        # Create entry fields with the specified positions
        entry = tk.Entry(entry_frame, width=entry_width, validate="key", validatecommand=(validate_numeric, '%S'), textvariable=var_dict[text_var])
        entry.grid(
            row=entry_row,
            pady = 5,
            padx = 5,
            column=entry_column,
            columnspan=entry_info["span"],
            sticky="e"
        )

    return var_dict

def bind_input_fields(data_manager, var_dict):
    """
    Binds Tkinter input fields to a DataManager to update data dynamically.

    Parameters:
        - data_manager (DataManager): An instance of the DataManager class to manage and store data.
        - var_dict (dict): A dictionary containing StringVar objects associated with Tkinter input fields.

    This function establishes a dynamic connection between Tkinter input fields and a DataManager.
    It creates callback functions that are triggered whenever the associated StringVar objects change.
    Each callback attempts to convert the user's input to a float and updates the corresponding data
    in the DataManager. If the input is not a valid number, an error message is printed. The function
    sets up traces to monitor changes in the input fields and ensures live updates to the data_manager.
    """
    def create_callback(data_key):
        """
        Creates a callback function for a specific data key.
        Parameters: - data_key (str): The key representing the data to be updated in the DataManager.
        Returns:
            function: A callback function associated with the specified data_key.
        """
        def callback(*args):
            # Retrieve user input from the associated StringVar
            user_input_string = var_dict[data_key].get()

            # Check if the input is empty
            if not user_input_string:
                # Handle the case where the input is empty (you can set the DataManager data to a default value or handle it as needed)
                data_manager.set_data(data_key, None)  # Set it to None or any other default value
                return

            try:
                # Attempt to convert user input to a float and update DataManager
                user_input_float = float(user_input_string)
                data_manager.set_data(data_key, user_input_float)
                if data_key == "number_of_sleepers":
                    user_input_int = int(user_input_string)
                    data_manager.set_data(data_key, user_input_int)
            except ValueError:
                # Print an error message for invalid input
                print(f"Invalid input for {data_key}: {user_input_string}")

        return callback

    # Define callback functions before creating the trace_info
    on_width = create_callback("Width")
    on_distance = create_callback("Distance")
    on_distance_cameratopole2 = create_callback("DistanceCameraToPole2")
    on_desired_distance = create_callback("DesiredDistance")
    on_number_of_sleepers = create_callback("NumberOfSleepers")
    on_camera_height = create_callback("CameraHeight")

    # List of tuples containing data keys and their associated callback functions
    trace_info = [
        ("real_pole_size", on_width),
        ("distance_input", on_distance),
        ("distance_to_pole2", on_distance_cameratopole2),
        ("desired_distance_input", on_desired_distance),
        ("number_of_sleepers", on_number_of_sleepers),
        ("camera_height", on_camera_height)
    ]
    # Set up traces to monitor changes in the input fields and trigger the corresponding callbacks
    for data_key, callback_func in trace_info:
        var_dict[data_key].trace("w", create_callback(data_key))

def create_buttons(data_manager, canvas_manager, frame_button_map):
    '''
    This function creates buttons with specified text, commands, and grid positions in a Tkinter GUI.
    The buttons are associated with various actions such as selecting an image, previewing lines, and saving images.
    '''
    # Function to create buttons

    # Define constant values for row and column indices
    ROW_SELECT_IMAGE, ROW_SELECT_DIR, ROW_DRAW_LINES, ROW_POLE1, ROW_POLE2, ROW_SAVE = 0, 0, 3, 4, 5, 2
    COL_SELECT_IMAGE, COL_SELECT_DIR, COL_DRAW_LINES, COL_POLE1, COL_POLE2, COL_SAVE = 1, 1, 0, 0, 0, 0

    # List of dictionaries containing details for each button
    button_list = [
        {"text": "Browse", "frame":  "1", "command": lambda: select_image(canvas_manager), "row": ROW_SELECT_IMAGE, "col": COL_SELECT_IMAGE, "sticky": "e", "span": 1},
        {"text": "Browse", "frame":  "4", "command": lambda: select_directory(canvas_manager), "row": ROW_SELECT_DIR, "col": COL_SELECT_DIR, "sticky": "e", "span": 1},
        {"text": "Preview Lines", "frame": "3", "command": lambda: canvas_manager.preview_estimated_lines(data_manager), "row": ROW_DRAW_LINES, "col": COL_DRAW_LINES, "sticky": "ew", "span": 2},
        {"text": "Point Pole 1", "frame": "2", "command": lambda: canvas_manager.save_pole_values(data_manager, 1), "row": ROW_POLE1, "col": COL_POLE1, "sticky": "", "span": 2},
        {"text": "Point Pole 2", "frame": "2", "command": lambda: canvas_manager.save_pole_values(data_manager, 2), "row": ROW_POLE2, "col": COL_POLE2, "sticky": "", "span": 2},
        {"text": "Save to Image", "frame": "4", "command": lambda: canvas_manager.save_canvas_as_image(), "row": ROW_SAVE, "col": COL_SAVE, "sticky": "ew", "span": 2}
    ]

    # Create buttons in the specified positions
    for details in button_list:
        # create buttons using the canvas root and their respective text and command function
        button = tk.Button(frame_button_map[details["frame"]], text=details["text"], command=details["command"])
        # Set buttons in the specified grid positions and make them expandable in the "ew" direction
        button.grid(
            row=details["row"],
            column=details["col"],
            columnspan=details["span"],
            sticky=details["sticky"],
            pady = 5,
            padx = 5
        )


# replace all above functions with a class called UserInterface

class UserInterface:
    def __init__(self, root, data_manager, canvas_manager):
        self.root = root
        self.var_dict = {}
        self.frame_button_map = {}
        self.entry_directories = {}
        self.create_ui(root, data_manager, canvas_manager)

    def create_ui(self, root, data_manager, canvas_manager):
        # Create a button frame and place it in the first column
        motherframe = tk.Frame(root)
        motherframe.grid(row=0, column=0, rowspan=4, columnspan=1,sticky= "nsew")
        motherframe.columnconfigure(0, weight=0)
        motherframe.columnconfigure(1, weight=0)
        motherframe.columnconfigure(2, weight=0)

        button_frame_refimg = tk.Frame(motherframe)
        button_frame_realdata = tk.Frame(motherframe)
        button_frame_preview = tk.Frame(motherframe)
        button_frame_save = tk.Frame(motherframe)

        self.configure_frame(button_frame_refimg, column=0, row=0)
        self.configure_frame(button_frame_realdata, column=0, row=1)
        self.configure_frame(button_frame_preview, column=0, row=2)
        self.configure_frame(button_frame_save, column=0, row=3)

        # create map of frames to pass to button creation
        self.frame_button_map = {
        "1": button_frame_refimg,
        "2": button_frame_realdata,
        "3": button_frame_preview,
        "4": button_frame_save
        }

        # set up where and how labels and entries should be
        labels_info, entry_info = self.setup_labels_and_entries()

        # create labels and entries
        self.create_labels(labels_info)
        self.create_entry_fields(entry_info, root)

        # bind entries (or input fields) to data manager
        self.bind_entry_fields(data_manager)

        # Create buttons for data management and canvas manipulation
        self.create_buttons(data_manager, canvas_manager)
        # button_frame_realdata.grid_rowconfigure(7, weight=1)  # Allow the button frame to expand vertically

        # place the canvas in the third column
        canvas_manager.canvas.grid(row=0, column=3, sticky="nsew")
        root.columnconfigure(3, weight=1)  # Allow the canvas to expand horizontally

        # Configure rows and columns inside the motherframe
        motherframe.columnconfigure(0, weight=1)  # Allow the button frame to expand horizontally

        root.mainloop()

    def configure_frame(self, frame, column, row):
        padx = 10
        pady = 20
        frame.grid(column=column, row=row, padx=padx, pady=pady, sticky="n")
        frame.configure(borderwidth=1, relief="raised")

    def only_numeric_input(self, char):
        # Function to allow only numeric input and decimal point in Entry widget
        return char.isdigit() or char == '.'

    def select_directory(self, canvas_manager):
        dir_path = filedialog.askdirectory(parent=canvas_manager.root)  # Pass the existing root window as parent
        if dir_path:
            canvas_manager.save_imageseries_sourcepath(dir_path)
            self.var_dict["path_series"].set(dir_path)

    def select_image(self, canvas_manager):
        file_path = filedialog.askopenfilename(parent=canvas_manager.root)  # Pass the existing root window as parent
        if file_path:
            canvas_manager.import_image(file_path)
            canvas_manager.save_image_path(file_path)
            file_path = Path(file_path)

            # automatically set the series source path to the parent directory of the selected image
            canvas_manager.save_imageseries_sourcepath(file_path.parent)
            self.var_dict["path_series"].set(file_path.parent)

            # print the path to the corresponding tk entryfield
            self.var_dict["path_image"].set(file_path)


    def setup_labels_and_entries(self):
        # Define constant values for row and column indices
        ROW_POLE_WIDTH, ROW_DISTANCE_CAMERA_POLE1, ROW_DISTANCE_CAMERA_POLE2, ROW_DESIRED_DISTANCE, ROW_NUM_LINES, ROW_CAMERA_SIZE = 0, 1, 2, 0, 1, 3
        ROW_FILE_PATHS = 1
        COL_LABEL, COL_ENTRY = 0, 1

        # Information about labels, their row and column positions
        labels_info = [
            {"text": "Width of poles [m]", "row": ROW_POLE_WIDTH, "column": COL_LABEL, "frame": "2"},
            {"text": "Distance camera - pole 1 [m]", "row": ROW_DISTANCE_CAMERA_POLE1, "column": COL_LABEL, "frame": "2"},
            {"text": "Distance camera - pole 2 [m]", "row": ROW_DISTANCE_CAMERA_POLE2, "column": COL_LABEL, "frame": "2"},
            {"text": "Distance between horizontal lines [m]", "row": ROW_DESIRED_DISTANCE, "column": COL_LABEL, "frame": "3"},
            {"text": "Number of new lines", "row": ROW_NUM_LINES, "column": COL_LABEL, "frame": "3"},
            {"text": "Camera height [m]", "row": ROW_CAMERA_SIZE, "column": COL_LABEL, "frame": "2"},
            {"text": "Path to image series", "row": ROW_POLE_WIDTH, "column": COL_LABEL, "frame": "4"},
            {"text": "Path to selected image", "row": ROW_POLE_WIDTH, "column": COL_LABEL, "frame": "1"}
        ]

        # Information about entry fields, their row and column positions
        entry_info = [
            {"row": ROW_POLE_WIDTH, "column": COL_ENTRY, "frame": "2", "field_width": 4, "span": 1}, # pole width
            {"row": ROW_DISTANCE_CAMERA_POLE1, "column": COL_ENTRY, "frame": "2", "field_width": 4, "span": 1}, # distance to pole 1
            {"row": ROW_DISTANCE_CAMERA_POLE2, "column": COL_ENTRY, "frame": "2", "field_width": 4, "span": 1}, # distance to pole 2
            {"row": ROW_DESIRED_DISTANCE, "column": COL_ENTRY, "frame": "3", "field_width": 4, "span": 1}, # desired distance
            {"row": ROW_NUM_LINES, "column": COL_ENTRY, "frame": "3", "field_width": 4, "span": 1}, # number of lines
            {"row": ROW_CAMERA_SIZE, "column": COL_ENTRY, "frame": "2", "field_width": 4, "span": 1}, # camera
            {"row": ROW_FILE_PATHS, "column": 0, "frame": "4", "field_width": 35, "span": 2}, # image series
            {"row": ROW_FILE_PATHS, "column": 0, "frame": "1", "field_width": 35, "span": 2} # reference image
        ]

        return labels_info, entry_info

    def create_labels(self, labels_info):
        for label_info in labels_info:
            label_text = label_info["text"]
            label_row = label_info["row"]
            label_column = label_info["column"]
            frame_number = self.frame_button_map[label_info["frame"]]
            label = tk.Label(frame_number, text=label_text)
            label.grid(
                column=label_column,
                row=label_row,
                pady=5,
                padx=5,
                sticky="e"
            )
    def create_entry_fields(self, entry_info, root):
        # Register the validation function for numeric input
        validate_numeric = root.register(only_numeric_input)

        for entry_info, text_var in zip(entry_info, ["real_pole_size", "distance_input", "distance_to_pole2", "desired_distance_input", "number_of_sleepers", "camera_height", "path_series", "path_image"]):
            self.var_dict[text_var] = tk.StringVar()
            entry_row = entry_info["row"]
            entry_column = entry_info["column"]
            entry_frame = self.frame_button_map[entry_info["frame"]]
            entry_width = entry_info["field_width"]

            # Create entry fields with the specified positions
            entry = tk.Entry(entry_frame, width=entry_width, validate="key", validatecommand=(validate_numeric, '%S'), textvariable=self.var_dict[text_var])
            entry.grid(
                row=entry_row,
                pady = 5,
                padx = 5,
                column=entry_column,
                columnspan=entry_info["span"],
                sticky="e"
            )

            self.entry_directories[text_var] = entry

    def bind_entry_fields(self, data_manager):
        """
        Binds Tkinter input fields to a DataManager to update data dynamically.

        Parameters:
            - data_manager (DataManager): An instance of the DataManager class to manage and store data.
            - var_dict (dict): A dictionary containing StringVar objects associated with Tkinter input fields.

        This function establishes a dynamic connection between Tkinter input fields and a DataManager.
        It creates callback functions that are triggered whenever the associated StringVar objects change.
        Each callback attempts to convert the user's input to a float and updates the corresponding data
        in the DataManager. If the input is not a valid number, an error message is printed. The function
        sets up traces to monitor changes in the input fields and ensures live updates to the data_manager.
        """
        def create_callback(data_key):
            """
            Creates a callback function for a specific data key.
            Parameters: - data_key (str): The key representing the data to be updated in the DataManager.
            Returns:
                function: A callback function associated with the specified data_key.
            """
            def callback(*args):
                # Retrieve user input from the associated StringVar
                user_input_string = self.var_dict[data_key].get()

                # Check if the input is empty
                if not user_input_string:
                    # Handle the case where the input is empty (you can set the DataManager data to a default value or handle it as needed)
                    data_manager.set_data(data_key, None)  # Set it to None or any other default value
                    return

                try:
                    # Attempt to convert user input to a float and update DataManager
                    user_input_float = float(user_input_string)
                    data_manager.set_data(data_key, user_input_float)
                    if data_key == "number_of_sleepers":
                        user_input_int = int(user_input_string)
                        data_manager.set_data(data_key, user_input_int)
                except ValueError:
                    # Print an error message for invalid input
                    print(f"Invalid input for {data_key}: {user_input_string}")

            return callback

        # Define callback functions before creating the trace_info
        on_width = create_callback("Width")
        on_distance = create_callback("Distance")
        on_distance_cameratopole2 = create_callback("DistanceCameraToPole2")
        on_desired_distance = create_callback("DesiredDistance")
        on_number_of_sleepers = create_callback("NumberOfSleepers")
        on_camera_height = create_callback("CameraHeight")

        # List of tuples containing data keys and their associated callback functions
        trace_info = [
            ("real_pole_size", on_width),
            ("distance_input", on_distance),
            ("distance_to_pole2", on_distance_cameratopole2),
            ("desired_distance_input", on_desired_distance),
            ("number_of_sleepers", on_number_of_sleepers),
            ("camera_height", on_camera_height)
        ]

        # Set up traces to monitor changes in the input fields and trigger the corresponding callbacks
        for data_key, callback_func in trace_info:
            self.var_dict[data_key].trace("w", create_callback(data_key))


    def create_buttons(self, data_manager, canvas_manager):
        '''
        This function creates buttons with specified text, commands, and grid positions in a Tkinter GUI.
        The buttons are associated with various actions such as selecting an image, previewing lines, and saving images.
        '''

        # Function to create buttons

        # Define constant values for row and column indices
        ROW_SELECT_IMAGE, ROW_SELECT_DIR, ROW_DRAW_LINES, ROW_POLE1, ROW_POLE2, ROW_SAVE = 0, 0, 3, 4, 5, 2
        COL_SELECT_IMAGE, COL_SELECT_DIR, COL_DRAW_LINES, COL_POLE1, COL_POLE2, COL_SAVE = 1, 1, 0, 0, 0, 0

        # List of dictionaries containing details for each button
        button_list = [
            {"text": "Browse", "frame":  "1", "command": lambda: self.select_image(canvas_manager), "row": ROW_SELECT_IMAGE, "col": COL_SELECT_IMAGE, "sticky": "e", "span": 1},
            {"text": "Browse", "frame":  "4", "command": lambda: self.select_directory(canvas_manager), "row": ROW_SELECT_DIR, "col": COL_SELECT_DIR, "sticky": "e", "span": 1},
            {"text": "Preview Lines", "frame": "3", "command": lambda: canvas_manager.preview_estimated_lines(data_manager), "row": ROW_DRAW_LINES, "col": COL_DRAW_LINES, "sticky": "ew", "span": 2},
            {"text": "Point Pole 1", "frame": "2", "command": lambda: canvas_manager.save_pole_values(data_manager, 1), "row": ROW_POLE1, "col": COL_POLE1, "sticky": "", "span": 2},
            {"text": "Point Pole 2", "frame": "2", "command": lambda: canvas_manager.save_pole_values(data_manager, 2), "row": ROW_POLE2, "col": COL_POLE2, "sticky": "", "span": 2},
            {"text": "Apply to Series", "frame": "4", "command": lambda: canvas_manager.save_canvas_as_image(data_manager), "row": ROW_SAVE, "col": COL_SAVE, "sticky": "ew", "span": 2}
        ]

        # Create buttons in the specified positions
        for details in button_list:
            # create buttons using the canvas root and their respective text and command function
            button = tk.Button(self.frame_button_map[details["frame"]], text=details["text"], command=details["command"])
            # Set buttons in the specified grid positions and make them expandable in the "ew" direction
            button.grid(
                row=details["row"],
                column=details["col"],
                columnspan=details["span"],
                sticky=details["sticky"],
                pady = 5,
                padx = 5
            )