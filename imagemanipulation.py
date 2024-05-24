import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import messagebox as mb
from pathlib import Path
from PIL import Image, ImageTk, ImageOps, ImageDraw, ImageFont
import math
import sys

from perspectivetriangles_functions import PerspectiveTriangle
from gridmanager import GridManager
from internal_classes import StraightLine, CoordinatePoint, SystemTravellingLine
from algebra_and_geometry_functions import estimate_distance, test_for_parallelism, find_ymc_from_two_points

class CanvasManager:
    # this class is here to manage the canvas and all the modifications applied to it, including the following
        # image import
        # line drawing
        # dot drawing
        # tagging of drawn lines
        # export of drawings on image

    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(self.root)
        self.image = None
        self.image_path = None
        self.imageseries_source_path = None
        self.aspect_ratio = None
        self.poles = {'1': None, '2': None}  # make place for two reference poles
        self.poleses_canvaslines_ids = [None] * 2  # Store lines for each button
        self.dot_ids = [None] * 4 * 2 # space for four dots for each pole (small+large and left+right)
        self.perspective_triangle = PerspectiveTriangle(self.canvas)
        self.grid = GridManager()
        self.img_height = None
        self.img_width = None
        self.ready_for_series = False
        # global my_global_variable

    def user_input_validation(self, data_manager):
        # 1 validate poles
        if self.validate_poles():
            # 2 validate input
            if data_manager.validate_manual_input():
                return True
        

    def validate_poles(self):
        '''
        This function validates the poles.
            - pole 1 must be defined
            - pole 2 must be defined
            - pole 1 must be larger than pole 2
            - poles must be parallel
            - pole 1 must have larger y value than pole 2
        '''

        pole1 = self.poles['1']
        pole2 = self.poles['2']
        if pole1 is None or pole2 is None:
            mb.showerror("Error", "Both poles must be defined")
            return False
        elif pole1.length < pole2.length:
            mb.showerror("Error", "Pole 1 must be larger than pole 2")
            return False
        elif not test_for_parallelism(pole1, pole2):
            mb.showerror("Error", "Poles must be parallel to each other")
            return False
        elif pole1.coordinateA.y < pole2.coordinateA.y:
            mb.showerror("Error", "Pole 1 must be below pole 2 on the image")
            return False

        return True

    def save_image_path(self, file_path):
        self.image_path = Path(file_path)

    def save_imageseries_sourcepath(self, path):
        self.imageseries_source_path = Path(path)

    def import_image(self, file_path):

        # this width was estimated from the objects in the motherframe
        motherframe_width = 290
        
        # Open the image file
        image = Image.open(file_path)
        self.img_width, self.img_height = image.size
        self.img_width_original, self.img_height_original = image.size

        # save path on canvas manager
        self.save_image_path(file_path)

        # Get the dimensions of the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Resize the screen dimensions to leave space for other UI elements
        WINDOW_SCREEN_RESIZE = 0.95
        screen_width -= motherframe_width
        screen_height *= WINDOW_SCREEN_RESIZE

        # Resize the image if it's larger than the screen
        if self.img_width > screen_width or self.img_height > screen_height:
            # Calculate the aspect ratio to maintain image proportions
            aspect_ratio = min(screen_width / self.img_width, screen_height / self.img_height)
            self.aspect_ratio = aspect_ratio
            # Resize the image based on the aspect ratio
            self.img_width = int(self.img_width * aspect_ratio)
            self.img_height = int(self.img_height * aspect_ratio)
            image = image.resize((self.img_width, self.img_height), Image.LANCZOS)
        else:
            self.aspect_ratio = 1

        # Set the geometry of the window and canvas
        window_geometry = f"{self.img_width + motherframe_width}x{self.img_height}"
        self.root.geometry(window_geometry)
        self.canvas.config(width=self.img_width, height=self.img_height)

        # Display the image on the canvas
        img_tk = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        self.canvas.image = img_tk  # Keep a reference to avoid garbage collection

        # Store the image for future reference
        self.image = image

    def calculate_translation_vector(self):
        '''
        this function is used to calculate the translation vector for the new
        coordinate system, where the x-axis is formed by the first pole. the
        translation vector moves the origin of the new coordinate system to the
        first pole's coordinate A
        '''
        x = self.poles['1'].coordinateA.x
        y = self.poles['1'].coordinateA.y
        translation_vector = CoordinatePoint(x, y)

        return translation_vector

    def calculate_rotation_angle(self, translation_vector):
        '''
        this function is used to calculate the counterclockwise rotation angle between the x-axis
        and the point B of the first pole

        input:
            - self.poles['1'].coordinateB
            - translation_vector
        
        process:
            - use grid.translation_vector and function grid.translate_point to translate point B
            - use pythagoras to calculate the distance between origin and translated point B (hypothenuse)
            - calculate the angle in radians between the original x-axis and the hypothenuse.
            - output angle
        '''

        translated_B = self.grid.translate_point(self.poles['1'].coordinateB, translation_vector)
        hypothenuse = estimate_distance(CoordinatePoint(0, 0), translated_B)

        angle = - math.asin(translated_B.y / hypothenuse)

        # if angle < 0:
        #     angle = 2 * math.pi + angle
        
        return angle

    def draw_UIpoles_lineswdots(self, start_x, start_y, end_x, end_y, pole_number, dot_color="deeppink3", dot_size=2):
        # replace the previous code with new one
        # 0 remove existing line with same name
        self.canvas.delete(self.poleses_canvaslines_ids[pole_number - 1])
        
        if pole_number == 1:
            self.canvas.delete(self.dot_ids[0])
            self.canvas.delete(self.dot_ids[1])
            self.canvas.delete(self.dot_ids[4])
            self.canvas.delete(self.dot_ids[5])
        elif pole_number == 2:
            self.canvas.delete(self.dot_ids[2])
            self.canvas.delete(self.dot_ids[3])
            self.canvas.delete(self.dot_ids[6])
            self.canvas.delete(self.dot_ids[7])

        # 1 create a line and draw on canvas
        # 2 draw the line
        line_id = self.canvas.create_line(start_x, start_y, end_x, end_y, width=3, fill='DeepPink2') #upper line
        
        # 3 draw dots at line ends and store their ids
        coords = [start_x, start_y, end_x, end_y]

        self.draw_larger_dots(coords, pole_number, dot_size)
        self.draw_small_dots(coords, pole_number, dot_color, dot_size)      
            
        # 4 store the line in the dictionary
        self.poleses_canvaslines_ids[pole_number - 1] = line_id
    
    def draw_small_dots(self, coords, pole_number, dot_color, dot_size):
        """
        This function draws small dots at the provided coordinates on the canvas.

        Args:
            coords: List containing x and y coordinates for each dot (format: [x1, y1, x2, y2]).
            dot_color: Color of the small dots.
            dot_size: Size of the small dots.
        """
        for i, (x, y) in enumerate([(coords[0], coords[1]), (coords[2], coords[3])]):
            dot_id = self.canvas.create_oval(
                x - dot_size,
                y - dot_size,
                x + dot_size,
                y + dot_size,
                fill=dot_color
            )
            # creates an oval (a dot in this case) on the canvas.
            # The returned dot_id is a unique integer identifier for this drawn oval        
            if pole_number == 1:
                self.dot_ids[i] = dot_id
            elif pole_number == 2:
                self.dot_ids[i + 2] = dot_id          

    def draw_larger_dots(self, coords, pole_number, dot_size):
        dot_size = dot_size * 3
        
        # 1 create an oval (a dot in this case) on the canvas.
        for i, (x, y) in enumerate([(coords[0], coords[1]), (coords[2], coords[3])]):
            dot_id = self.canvas.create_oval(
                x - dot_size,
                y - dot_size,
                x + dot_size,
                y + dot_size,
                fill="mediumturquoise"
            )
            # The returned dot_id is a unique integer identifier for this drawn oval
            
            if pole_number == 1:
                self.dot_ids[i + 4] = dot_id
            elif pole_number == 2:
                self.dot_ids[i + 6] = dot_id       


    def save_pole_values(self, data_manager, pole_number):
        # this function takes the user click-input and saves the coordinates
        # it also uses calculate_distance to save the image-size of the pole in pixels
        pole_coords = []  # To store coordinates for each pole

        def handle_canvas_click(event):
            '''
            this function is used to obtain the position of the start (coordinate A; leftmost) and end
            (coordinate B; rightmost) of the poles.

            the function is called for each click and does as follows: caputre the values from the click-event,
            create a pole with the two coordinates (A and B) and corresponding length, draw the pole. as soon
            as pole 1 is captured fully, a transformation matrix is created to translate points from the canvas
            coordinate system to a coordinate system where the x-axis is formed by pole 1.
            '''
            Y_TRANSFORM = 1
            x, y = event.x, event.y * Y_TRANSFORM # save the coordinates of the click "event"
            pole_coords.append(CoordinatePoint(x, y))  # Store clicked coordinates temporarily

            if len(pole_coords) == 2: # as soon as there are two coordinates (A and B) stored, do:
                # Sort coordinates based on x-value
                pole_coords.sort(key=lambda coord: coord.x)

                # save them in new objects
                pole_coord_A = pole_coords[0]
                pole_coord_B = pole_coords[1]

                # Create Pole instance
                pole = SystemTravellingLine(pole_coord_A.x, pole_coord_A.y, pole_coord_B.x, pole_coord_B.y)
                
                # estimate distance between two points and save it as the length of the pole
                pole_length = estimate_distance(pole_coord_A, pole_coord_B)
                pole.length = pole_length

                # calculate equation of pole (necessary for validation)
                slope, intercept = find_ymc_from_two_points(pole_coord_A, pole_coord_B)
                pole.equation.intercept = intercept
                pole.equation.slope = slope

                # Save Pole instance to CanvasManager through its instance
                self.poles[f"{pole_number}"] = pole
                # print(f"Pole {pole_number} coordinates captured: x{pole_coord_A.x},y{pole_coord_A.y} and x{pole_coord_B.x},y{pole_coord_B.y}")

                self.draw_UIpoles_lineswdots(
                    pole_coord_A.x,
                    pole_coord_A.y,
                    pole_coord_B.x,
                    pole_coord_B.y,
                    pole_number)

                # to-do: create a transformation matrix from the pole here

                # clear
                pole_coords.clear()

                # get ready for next click
                self.canvas.unbind("<Button-1>")

                # with the first pole create a transformation matrix to a new coordinate system
                if pole_number == 1:
                    translation_vector = self.calculate_translation_vector()
                    angle = self.calculate_rotation_angle(translation_vector)
                    self.grid.save_transformation_values(translation_vector, angle) # save values in grid instance
                    self.grid.save_pole1(pole) # save pole also in grid instance


                    ################################
                    ## delete after checking TM   ##
                    ################################
                    # temporary_left = 100
                    # temporary_up = 100
                    # temporary_right = 200
                    # temporary_down = 200
                    
                    # pole.coordinateA = CoordinatePoint(temporary_left, temporary_down)
                    # pole.coordinateB = CoordinatePoint(temporary_right, temporary_up)
                    # self.poles['1'].coordinateA.x = pole.coordinateA.x
                    # self.poles['1'].coordinateA.y = pole.coordinateA.y
                    # self.poles['1'].coordinateB = pole.coordinateB

                    # translation_vector = self.calculate_translation_vector()
                    # angle = self.calculate_rotation_angle(translation_vector)
                    # self.grid.save_transformation_values(translation_vector, angle) # save values in grid instance
                    # self.grid.save_pole1(pole) # save pole also in grid instance
                  
                    # upleft = CoordinatePoint(temporary_left, temporary_up)
                    # upright = CoordinatePoint(temporary_right, temporary_up)
                    # downright = CoordinatePoint(temporary_right, temporary_down)
                    # downleft =CoordinatePoint(temporary_left, temporary_down)
                  
                    # self.grid.save_pole1(pole)
                    # print(f'{self.grid.pole1.coordinateA.x} and {self.grid.pole1.coordinateA.y}')

                    # self.canvas.create_line(temporary_left, temporary_up, temporary_right, temporary_up, fill='blue2') #upper line
                    # self.canvas.create_line(temporary_right, temporary_up, temporary_right, temporary_down, fill='blue2') #upper line
                    # self.canvas.create_line(temporary_right, temporary_down, temporary_left, temporary_down, fill='blue2') #upper line
                    # self.canvas.create_line(temporary_left, temporary_down, temporary_left, temporary_up, fill='blue2') #upper line

                    # transf_upleft = self.grid.transformcoordinate_canvas_to_newcoordinatesystem(upleft)
                    # transf_upright = self.grid.transformcoordinate_canvas_to_newcoordinatesystem(upright)
                    # transf_downright = self.grid.transformcoordinate_canvas_to_newcoordinatesystem(downright)
                    # transf_downleft = self.grid.transformcoordinate_canvas_to_newcoordinatesystem(downleft)

                    # st_upleft = transf_upleft
                    # st_upleft.x = st_upleft.x
                    # st_upright = transf_upright
                    # st_upright.x = st_upright.x
                    # st_downright = transf_downright
                    # st_downright.x = st_downright.x
                    # st_downleft = transf_downleft
                    # st_downleft.x = st_downleft.x

                    # backt_upleft = self.grid.backtransformcoordinate_newcoordinatesystem_to_canvas(st_upleft)
                    # backt_upright = self.grid.backtransformcoordinate_newcoordinatesystem_to_canvas(st_upright)
                    # backt_downright = self.grid.backtransformcoordinate_newcoordinatesystem_to_canvas(st_downright)
                    # backt_downleft = self.grid.backtransformcoordinate_newcoordinatesystem_to_canvas(st_downleft)

                    # self.canvas.create_polygon(backt_upleft.x, backt_upleft.y, backt_upright.x, backt_upright.y, backt_downright.x, backt_downright.y, backt_downleft.x, backt_downleft.y)

                    ################################
                    ################################



                # estimate the coordinates in the new coordinate system (ncs)
                ncs_A = self.grid.transformcoordinate_canvas_to_newcoordinatesystem(pole_coord_A)
                ncs_B = self.grid.transformcoordinate_canvas_to_newcoordinatesystem(pole_coord_B)
                self.poles[f'{pole_number}'].ncs_coordinate_A = ncs_A
                self.poles[f'{pole_number}'].ncs_coordinate_B = ncs_B


                # test if functions are correct, transform the points back to the original coordinate system
                self.grid.backtransformcoordinate_newcoordinatesystem_to_canvas(ncs_A)
                self.grid.backtransformcoordinate_newcoordinatesystem_to_canvas(ncs_B)

                if pole_number == 1:
                    self.grid.save_pole1(self.poles['1'])


        self.canvas.bind("<Button-1>", handle_canvas_click)

    def preview_estimated_lines(self, data_manager):
        # validate user input
        if self.user_input_validation(data_manager):

            # estimate and draw perspective triangle
            self.perspective_triangle.update_and_redraw_triangle(data_manager, self.img_height, self)

            # create grid, get lengths of sleepers inside triangle, estimate positions, estimate longer lines and draw
            self.grid.update_and_redraw_grid(self.canvas, self.perspective_triangle, self.img_width, self.poles, data_manager)

        self.ready_for_series = True

    def save_canvas_as_image(self, data_manager, fill='deeppink'):
        '''
        This function is called when the "save images" button is clicked in the user interface.
        It first validates the user input. If the input is not valid, the function returns.
        Then, it creates an empty image and a drawing object. It prepares the directory to save the images and creates a progress bar window.
        Next, it draws lines on the empty image and overlays and saves the images to the prepared directory.
        It also displays a message box indicating that the process is done.
        '''
        if not self.validate_image_save():
            return

        if self.ready_for_series!=True:
            mb.showwarning("Error", "Please preview the grid first.")
            return

        # create an empty image of the same size as the original reference image for drawing the lines
        empty_image = self.create_empty_image()

        # prepare a drawing object with the empty image and ziel directory
        draw = self.create_drawing_object(empty_image)
        ziel_path = self.prepare_directory()

        # prepare progress bar
        progress_window, progress, progress_label = self.create_progressbar_window()
        
        FONTSIZEONIMAGE = 30
        if self.img_height < 1000:
            FONTSIZEONIMAGE = 14

        # draw line distances on image
        if 'linux' in sys.platform:
            font = ImageFont.truetype(r"./Actor.ttf", FONTSIZEONIMAGE, encoding="unic")
        elif 'win32' in sys.platform:
            font = ImageFont.truetype(r"arial.ttf", FONTSIZEONIMAGE, encoding="unic")
        elif 'darwin' in sys.platform:
            font = ImageFont.truetype(r"arial.ttf", FONTSIZEONIMAGE, encoding="unic")
        
        # draw lines on the draw from empty image and the distances to each line
        self.draw_lines(draw, fill)
        self.draw_distances(draw, data_manager, fill, font)

        # draw user input data
        # get the available font
        if 'linux' in sys.platform:
            font = ImageFont.truetype(r"./Actor.ttf", FONTSIZEONIMAGE, encoding="unic")
        elif 'win32' in sys.platform:
            font = ImageFont.truetype(r"arial.ttf", FONTSIZEONIMAGE, encoding="unic")
        elif 'darwin' in sys.platform:
            font = ImageFont.truetype(r"arial.ttf", FONTSIZEONIMAGE, encoding="unic")

        self.draw_inputdata(draw, data_manager, fill, font)

        # overlay and save images
        total_images, file_type = self.get_total_images()
        self.overlay_and_save_images(empty_image, ziel_path, progress_window, progress, progress_label, total_images, file_type)

        # finish process
        mb.showinfo("Done!", f"The modified images have been saved under {ziel_path}")

    def validate_image_save(self):
            # is there a file path to get old images from and save new images to?
            # is there an image that has been selected?
            # is there a perspective triangle? a grid?

        if self.imageseries_source_path is None:
            mb.showerror("Missing source folder", "Select a folder with images of the same perspective as the currently displayed image.")
            return False
        elif self.image_path is None:
            mb.showerror("Image missing", "Select an image with a reference object to estimate distances and draw lines on it.")
            return False
        elif self.perspective_triangle.line_A is None:
            mb.showerror("Missing reference on image", "To modify other images, first preview lines here.")
            return False

        return True


    def create_empty_image(self):
        width, height = self.img_width_original, self.img_height_original
        return Image.new("RGBA", (width, height), (0, 0, 0, 0))

    def create_drawing_object(self, empty_image):
        return ImageDraw.Draw(empty_image)

    def prepare_directory(self):
        source_directory = self.imageseries_source_path
        new_directory = 'distance_lines'
        ziel_path = source_directory / new_directory
        ziel_path.mkdir(parents=True, exist_ok=True)
        return ziel_path

    def create_progressbar_window(self):
        progress_window = tk.Tk()
        progress_window.title("Processing Images")
        progress_window.geometry("350x100")
        progress_window.resizable(False, False)
        progress = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
        progress.pack(pady=10)
        progress_label = tk.Label(progress_window, text="")
        progress_label.pack()
        return progress_window, progress, progress_label

    def draw_lines(self, draw, fill):
        # Draw perspective triangle
        # Loop through the line IDs of the perspective triangle
        for line_id in self.perspective_triangle.line_ids.values():
            # Get the coordinates of the line
            lines_coordinates = self.canvas.coords(line_id)
            # Scale the coordinates based on the aspect ratio
            lines_coordinates = [coord * (1 / self.aspect_ratio) for coord in lines_coordinates]
            # Draw the line with the scaled coordinates, deeppink color, and 3 pixels width
            draw.line(lines_coordinates, fill=fill, width=4)

        # Draw grid lines
        # Loop through the line IDs of the grid
        for line_id in self.grid.line_ids.values():
            # Get the coordinates of the line
            lines_coordinates = self.canvas.coords(line_id)
            # Scale the coordinates based on the aspect ratio
            lines_coordinates = [coord * (1 / self.aspect_ratio) for coord in lines_coordinates]
            # Draw the line with the scaled coordinates, deeppink color, and 3 pixels width
            draw.line(lines_coordinates, fill=fill, width=4)

    def draw_distances(self, draw, data_manager, fill, font):
        distance_to1 = data_manager.get_data("distance_input")
        distance_to2 = data_manager.get_data("distance_to_pole2")
        new_distance = data_manager.get_data("desired_distance_input")
        
        i = 1
        for text_id in self.grid.text_ids.values():

            # Get the text
            text = self.canvas.itemcget(text_id, 'text')
            # Get the coordinates of the text
            text_coordinates = self.canvas.coords(text_id)
            
            # Get the size of the text
            # text_width, text_height = font.getsize(text)
            text_width = draw.textlength(text, font)

            # Scale the coordinates based on the aspect ratio
            text_coordinates = [coord * (1 / self.aspect_ratio) for coord in text_coordinates]
            
            # to avoid overlaping, adapt the coordinates for every second box
            if i % 2 == 0:  # Check if the number is even
                text_coordinates[0] = text_coordinates[0] - text_width

            # Calculate coordinates for the rectangle background
            # rectangle_coordinates = [
            #     text_coordinates[0],
            #     text_coordinates[1],
            #     text_coordinates[0] + text_width + 3,  # Add some padding to the width
            #     text_coordinates[1] + text_height  # Add some padding to the height
            # ]

            bbox = draw.textbbox(text_coordinates, text, font=font)

            # Draw the rectangle background
            draw.rectangle(bbox, fill="lightcyan", outline=fill)

            # draw text
            draw.text(text_coordinates, text, font=font, fill=fill)

            # increase i by one
            i = i + 1


    def draw_inputdata(self, draw, data_manager, fill, font):
        # get user input data
        distance_input = data_manager.get_data("distance_input")
        real_pole_size = data_manager.get_data("real_pole_size")
        distance_to_pole2 = data_manager.get_data("distance_to_pole2")
        number_of_sleepers = data_manager.get_data("number_of_sleepers")
        desired_distance = data_manager.get_data("desired_distance_input")
        camera_height = data_manager.get_data("camera_height")

        # Calculate the width and height of the multiline text
        # text_id = self.grid.text_ids[0]
        # text = self.canvas.itemcget(text_id, 'text')
        # # text_width, text_height = font.getsize(text)
        # text_width = draw.textlength(text, font)

        # Calculate coordinates for the rectangle background
        # rectangle_coordinates = [
        #     10,
        #     10,
        #     10 + (text_width * 10),
        #     10 + (text_height * 8) 
        # ]
        
        bbox_starty = self.img_height - 250
        
        if self.img_height < 1000:
            bbox_starty = self.img_height - 150

        # draw the multiline textbox
        bbox = draw.multiline_textbbox((10, bbox_starty),
            f"Size of poles: {real_pole_size} m\n"
            f"Distance between camera and first line: {distance_input} m\n"
            f"Distance between camera and second line: {distance_to_pole2} m\n"
            f"Camera height: {camera_height} m\n"
            f"Selected number of lines: {number_of_sleepers}\n"
            f"Distance between horizontal lines (x-axis): {desired_distance} m\n"
            f"Distance between z-lines: {distance_input} m",
            font=font)

        # Draw the rectangle background
        # draw.rectangle(rectangle_coordinates, fill="lightcyan", outline=fill)
        # draw.rectangle(bbox, fill="lightcyan", outline=fill)

        # distance between z-lines
        z_distance = (distance_input - distance_to_pole2) / desired_distance * real_pole_size
        # draw text
        draw.multiline_text(
            (10, 10),
            f"Size of poles: {real_pole_size} m\n"
            f"Distance between camera and first line: {distance_input} m\n"
            f"Distance between camera and second line: {distance_to_pole2} m\n"
            f"Camera height: {camera_height} m\n"
            f"Selected number of lines: {number_of_sleepers}\n"
            f"Distance between horizontal lines (x-axis): {desired_distance} m\n"
            f"Distance between z-lines: {distance_input} m",
            fill=fill,
            font=font
            )

    def get_total_images(self):
        file_type = self.image_path.suffix
        image_paths = list(self.imageseries_source_path.glob(f'*{file_type}'))
        return len(image_paths), file_type

    def overlay_and_save_images(self, empty_image, ziel_path, progress_window, progress, progress_label, total_images, file_type):
        # Loop through the image files in the specified directory
        for i, image_path in enumerate(self.imageseries_source_path.glob(f'*{file_type}')):
            # Update the progress bar value and label
            progress['value'] = (i + 1) * 100 / len(list(self.imageseries_source_path.glob(f'*{file_type}')))
            progress_label.config(text=f"Processing image {i + 1} of {total_images}")
            progress_window.update()
            try:
                # Open the image, convert it to RGBA mode and use as background
                background_image = Image.open(image_path).convert("RGBA")
                # background_image = Image.open(image_path)

                # Check if the image dimensions match the original dimensions
                if background_image.width != self.img_width_original or background_image.height != self.img_height_original:
                    # Show an error message and skip processing the current image if image dimensions are not the same
                    mb.showerror(f"Image {image_path.name} has different dimensions than the reference image. It will not be processed.")
                    continue

                # Overlay the empty image (with drawn grid lines) on top of the background image (actual picture)
                result_image = Image.alpha_composite(background_image, empty_image)
                # result_image = background_image.paste(empty_image, (0, 0), mask = empty_image)
                # result_image = Image.blend(background_image, empty_image, alpha=0.5)
                
                # Define the new file extension and path for the result image (picture + grid lines)
                new_extension = 'png'
                image_filename = Path(image_path)
                new_image_path = ziel_path / f"{image_filename.stem}_distance_lines.{new_extension}"
                
                # Save the result image to the specified path
                result_image.save(new_image_path, 'PNG')
            except:
                # If an error occurs during processing, prompt the user with an error message and handle their response
                if mb.askokcancel("Processing Error", f"Error processing image {image_path.name}. It will not be processed."):
                    continue
                else:
                    break

        # Update the progress label to indicate that all images have been processed
        progress_label.config(text="All images processed")
        progress_window.update_idletasks()
        # Destroy the progress window after a delay of 1 second
        progress_window.after(1000, progress_window.destroy)

