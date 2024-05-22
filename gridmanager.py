import numpy as np
import math

from algebra_and_geometry_functions import find_ymc_from_two_points, find_crossing_twoequations, findxA_givendistance_givenequationsAandB, findy_given_x_m_c, findintercept_given_x_y_m, extend_line
from internal_classes import StraightLine, SimpleLinearEquation, CoordinatePoint, VerticalLine

class GridManager:
    def __init__(self):
        self.sleepers = []
        self.verticals = []
        self.horizon_line = None
        self.line_ids = {}
        self.text_ids = {}
        self.textbox_ids = {}
        self.translation_vector = None
        self.rotation_angle = None
        self.pole1 = None

    def save_transformation_values(self, translation_vector, angle):
        self.translation_vector = translation_vector
        self.rotation_angle = angle

    def save_pole1(self, pole1):
        self.pole1 = pole1

    @staticmethod
    def estimate_length_onesleeper(pole2_imagesize_pixels, current_luftlinie, desired_luftlinie):
        """
        Estimate the length of a pole in pixels on an image.

        Args:
        pole2_imagesize_pixels (int): Size of the current pole on the image in pixels
        current_distance (int): distance to the current pole in real world units
        desired_distance_input (int): Desired distance to the new pole in real world units

        Returns:
        float: size of the new pole on the image in pixels
        """

        pole_size_on_image_pixels = (pole2_imagesize_pixels * current_luftlinie) / desired_luftlinie

        return pole_size_on_image_pixels

    def estimate_lengths_of_imaginary_sleepers(self, data_manager, pole2_imagesize_pixels, number_of_sleepers):
        '''
        input:
            - real size of poles in meters
            - distance between camera and pole 2
            - distance that should separate each new pole (sleeper) from the previous one
            - number of pixels in camera sensor (img_width)
            - wished number of sleepers
        objective: estimate how wide new lines would be, if in reality they were separated from pole2 by a given distance.
        logic: from the sizes of pole 2 and the camera data
        '''
        
        # import values from user input
        real_pole_size = data_manager.get_data("real_pole_size") # - take real length of poles W
        print(f"real pole size is {real_pole_size}")
        distance_to_pole2 = data_manager.get_data("distance_to_pole2") # - take real distance to second pole D
        print(f"distance to pole 2 is {distance_to_pole2}")
        desired_distance_input = data_manager.get_data("desired_distance_input") # get desired distance D' between each new pole
        camera_height = data_manager.get_data("camera_height") # get camera height

        # lengths_imaginary_sleepers = []
        current_distance = distance_to_pole2
        current_pole_size = pole2_imagesize_pixels

        """
        for-loop to estimate the sizes of the sleepers one by one
        """
        for iteration in range(2, number_of_sleepers - 1):
            # estimate current luftlinie
            current_luftlinie = math.sqrt(current_distance**2 + camera_height**2)

            #  estimate desired luftdistance
            desired_luftlinie = math.sqrt((current_distance + desired_distance_input)**2 + camera_height**2)

            # estimate pole size on image
            ip = self.estimate_length_onesleeper(current_pole_size, current_luftlinie, desired_luftlinie)

            # Assign the calculated value to the 'length' attribute
            self.sleepers[iteration].length = ip

            # update pole size for next iteration
            current_pole_size = ip

            # update distance for next iteration
            current_distance += desired_distance_input
    
    def translate_point(self, given_point, translation_vector=None, backtransform=False):
        '''
        this function is used to translate a point from the original coordinate system to the midway coordinate system.

        input:
            - translation vector (class CoordinatePoint)
            - point on the original coordinate system (class CoordinatePoint)

        process:
            - translate the point using the translation vector

        output:
            - midway point
        '''
        # if a translation vector is contained, use it, else take the argument
        if translation_vector is None: translation_vector = self.translation_vector

        if backtransform:
            new_point = CoordinatePoint(
                given_point.x + translation_vector.x,
                given_point.y + translation_vector.y
            )

        else:
            new_point = CoordinatePoint(
                given_point.x - translation_vector.x,
                given_point.y - translation_vector.y
            )

        return new_point


    def rotate_point(self, point, backtransform=False):
        '''
        this function is used to rotate a point counterclockwise on the canvas by a given angle.

        input:
            - given point (class CoordinatePoint)
            - angle in radians

        process:
            - rotate the point using the given angle

        output:
            - new point
        '''
        
        angle = self.rotation_angle

        if backtransform:
            angle = 2 * math.pi - angle

        new_point = CoordinatePoint(
            point.x * math.cos(angle) - point.y * math.sin(angle),
            point.x * math.sin(angle) + point.y * math.cos(angle)
        )

        return new_point
            

    def transformcoordinate_canvas_to_newcoordinatesystem(self, given_point_on_canvas):
        '''
        this function translates a given point from the original to the new coordinate
        system. it first translates the point using translate_point and then rotates
        it using rotate_point. for translate_point and rotate_point, the backtransform
        parameter is set to False.
        '''

        # Translate the point using translate_point
        translated_point = self.translate_point(given_point_on_canvas, backtransform=False)

        # Rotate the point using rotate_point
        new_point = self.rotate_point(translated_point, backtransform=False)

        return new_point

    def backtransformcoordinate_newcoordinatesystem_to_canvas(self, point_new_system):
        '''
        this function translates a given point from the new to the original coordinate
        system. it first rotates the point using rotate_point and then translates it
        using translate_point. for rotate_point and translate_point, the backtransform
        parameter is set to True.
        '''

        # Rotate the point using rotate_point
        rotated_point = self.rotate_point(point_new_system, backtransform=True)

        # Translate the point using translate_point
        new_point = self.translate_point(rotated_point, backtransform=True)

        return new_point

    def save_sleepers_data_and_extend(self, iteration, xyA, xyB, img_width):
        """
        Save the x and ys as coordinates and use them to get an equation for each sleeper.
        """

        # use the coordinates to get an equation for each sleeper
        m_slope, c_intercept = find_ymc_from_two_points(xyA, xyB)  # get the equation parameters for the current sleeper
        sleeper_equation = SimpleLinearEquation(m_slope, c_intercept)
        self.sleepers[iteration].equation = sleeper_equation

        # get y at x0 and xend
        # use the equation of the sleeper to find the limit of the line at the left and right side of the image
        self.sleepers[iteration].coordinate_at_x0.y = findy_given_x_m_c(sleeper_equation, 0)
        self.sleepers[iteration].coordinate_at_img_width.y = findy_given_x_m_c(sleeper_equation, img_width)

        # save the obtained y, and xA and xB values
        self.sleepers[iteration].coordinateA.x = xyA.x
        self.sleepers[iteration].coordinateA.y = xyA.y
        self.sleepers[iteration].coordinateB.x = xyB.x
        self.sleepers[iteration].coordinateB.y = xyB.y


    def estimate_sleeper_positions(self, equation_A, equation_B, img_width, number_of_sleepers):
        """
        This function uses the lengths of the sleepers and estimates their positions inside the perspective triangle.
        The function further estimates the lengthening of the sleepers to the right and left end of the image to
        draw horizontal lines of the grid.
        """

        for iteration in range(2, number_of_sleepers - 1):
            sleeper_length = self.sleepers[iteration].length

            # get coordinates for sleeper in terms of new coordinate system NCS
            xA = findxA_givendistance_givenequationsAandB(equation_A, equation_B, sleeper_length)
            yA = findy_given_x_m_c(equation_A, xA)
            xB = sleeper_length + xA
            yB = findy_given_x_m_c(equation_B, xB)

            # save the x and ys as coordinates
            xyA = CoordinatePoint(xA, yA)
            xyB = CoordinatePoint(xB, yB)

            # transform back to the original coordinate system NCS
            original_xyA = self.backtransformcoordinate_newcoordinatesystem_to_canvas(xyA)
            original_xyB = self.backtransformcoordinate_newcoordinatesystem_to_canvas(xyB)

            self.save_sleepers_data_and_extend(iteration, original_xyA, original_xyB, img_width)


    def create_sleepers(self, poles, number_of_sleepers):
        self.sleepers.append(poles['1'])
        self.sleepers.append(poles['2'])

        for _ in range(2, number_of_sleepers):
            new_sleeper = StraightLine()  # Create a new instance of Sleeper
            self.sleepers.append(new_sleeper)  # Append the instance to the list
    
    def remove_sleepers(self):
        self.sleepers = []

    def extend_reference_poles(self, poles, img_width):
        # elongate poles 1 and 2
        x0, y0, xend, yend = extend_line(poles['1'], img_width)
        poles['1'].save_line_extension(x0, y0, xend, yend)
        x0, y0, xend, yend = extend_line(poles['2'], img_width)
        poles['2'].save_line_extension(x0, y0, xend, yend)

    def create_horizon_line(self, canvas_managers_canvas, vanishing_point, img_width, number_of_sleepers):
        # Create a horizon line
        self.horizon_line = StraightLine()
        
        # Get slope from sleepers and adapt intercept
        horizon_slope = self.sleepers[number_of_sleepers - 2].equation.slope
        self.horizon_line.equation.slope = horizon_slope
        self.horizon_line.equation.intercept = findintercept_given_x_y_m(vanishing_point.x , vanishing_point.y, horizon_slope)
        
        # Get and save coordinates
        start_x = 0
        start_y = findy_given_x_m_c(self.horizon_line.equation, start_x)
        end_x = img_width
        end_y = findy_given_x_m_c(self.horizon_line.equation, end_x)

        self.horizon_line.coordinate_at_x0.x = start_x
        self.horizon_line.coordinate_at_x0.y = start_y
        self.horizon_line.coordinate_at_img_width.x = end_x
        self.horizon_line.coordinate_at_img_width.y = end_y


    def create_first_and_last_horizontals(self, poles, canvas_managers_canvas, vanishing_point, img_width, number_of_sleepers):
        self.extend_reference_poles(poles, img_width)
        self.create_horizon_line(canvas_managers_canvas, vanishing_point, img_width, number_of_sleepers)

    def find_vertical_coordinates(self, side, n, equation_A, equation_B, vanishing_point):
        '''
        objective: for each vertical line, we need two points each estimated from a different
        square of the grid. the for loop goes through the first and second point

        logic:
        we are creating a second railway on each side of the given one.

        using coordinates from the "railline", a diagonal line crossing a the
        rectangle formed between two consecutive sleepers will be extended. if the
        sleeper contiguous to said square is also extended, the crossing between
        the (extended) diagonal line and the extended contiguous sleeper should be (in the real
        plane) equal to the length of the reference pole.

        '''
        two_points_on_vertical = []

        if side == 'left':
            horizontal_line_1 = self.sleepers[0]
            horizontal_line_2 = self.sleepers[1]
            
        else:
            horizontal_line_1 = self.sleepers[1]
            horizontal_line_2 = self.sleepers[0]

        horizontal_line_3 = self.sleepers[n + 2]

        crossB_x, crossB_y = find_crossing_twoequations(horizontal_line_1.equation, equation_B)
        crossA_x, crossA_y = find_crossing_twoequations(horizontal_line_2.equation, equation_A)
        
        crossB = CoordinatePoint(crossB_x, crossB_y)
        crossA = CoordinatePoint(crossA_x, crossA_y)
        
        m_slope, c_axiscut = find_ymc_from_two_points(crossA, crossB)
        diagonal_equation = SimpleLinearEquation(m_slope, c_axiscut)
        
        x_on_vertical, y_on_vertical = find_crossing_twoequations(diagonal_equation, horizontal_line_3.equation)
        point_on_vertical = CoordinatePoint(x_on_vertical, y_on_vertical)
        
        two_points_on_vertical.append(point_on_vertical)
        two_points_on_vertical.append(vanishing_point)

        return two_points_on_vertical

    def create_verticals(self, perspective_triangle, number_of_sleepers, img_width):
        '''
        objective: estimate where vertical lines should be and get two coordinates for
        the drawing function to work with.
        '''        

        equation_A = perspective_triangle.line_A.equation
        equation_B = perspective_triangle.line_B.equation
        vanishing_point = perspective_triangle.vanishing_point

        # process
        for side in ['left', 'right']:
            '''for each side, we need to go through the sleepers of the railway. to estimate
            each vertical line we need three consecutive sleepers, thus the loop ends three
            sleepers before the last one
            '''
            for n in range(number_of_sleepers - 4):
                # get two coordinates for each vertical line by extending and crossing lines
                two_points_onvertical = self.find_vertical_coordinates(side, n, equation_A, equation_B, vanishing_point)

                # II. vertical line equation and shortening 
                # take the two output crossing coordinates and create vertical equation
                m_slope, c_intercept = find_ymc_from_two_points(
                    two_points_onvertical[0],
                    two_points_onvertical[1]
                )
                vertical_equation = SimpleLinearEquation(m_slope, c_intercept)

                # create VerticalLine with equation
                vertical_line = VerticalLine(vertical_equation)

                # find where vertical line crosses pole1 line and horizon line
                x_bottom, y_bottom = find_crossing_twoequations(
                    vertical_line.equation,
                    self.pole1.equation
                )

                if  x_bottom > img_width and side == 'right':
                    x_bottom = img_width
                    y_bottom = findy_given_x_m_c(
                        vertical_line.equation,
                        img_width
                    )
                
                x_top, y_top = find_crossing_twoequations(
                    vertical_line.equation,
                    self.horizon_line.equation
                )

                # save values in vertical_line.coordinate_at_pole1 and .coordinate_at_horizon
                vertical_line.coordinate_at_pole1 = CoordinatePoint(x_bottom, y_bottom)
                vertical_line.coordinate_at_horizon = CoordinatePoint(x_top, y_top)

                self.verticals.append(vertical_line)

    def remove_verticals(self):
        self.verticals = []

    def create_grid(self, canvas_managers_canvas, data_manager, perspective_triangle, img_width, poles, number_of_sleepers):
        # create sleepers
        self.create_sleepers(poles, number_of_sleepers)

        # get their lengths
        self.estimate_lengths_of_imaginary_sleepers(
            data_manager,
            poles['2'].length,
            number_of_sleepers
        )
        
        # get position of sleepers, extend lines to end of image and save values
        self.estimate_sleeper_positions(
            perspective_triangle.line_A.ncs_equation,
            perspective_triangle.line_B.ncs_equation,
            img_width,
            number_of_sleepers
        )

        # get the first two (extended reference poles) and the last one (on vanishing point) horizontal lines
        self.create_first_and_last_horizontals(
            poles,
            canvas_managers_canvas,
            perspective_triangle.vanishing_point,
            img_width,
            number_of_sleepers
        )

        # get the vertical lines
        self.create_verticals(perspective_triangle, number_of_sleepers, img_width)

    def remove_grid(self, canvas_managers_canvas):
        # remove lines representing the grid from canvas
        for i in range(len(self.line_ids)):
            if self.line_ids[i]:
                canvas_managers_canvas.delete(self.line_ids[i])

        for i in range(len(self.text_ids)):
            if self.text_ids[i]:
                canvas_managers_canvas.delete(self.text_ids[i])

        for i in range(len(self.textbox_ids)):
            if self.textbox_ids[i]:
                canvas_managers_canvas.delete(self.textbox_ids[i])

        self.line_ids = {}
        self.text_ids = {}
        self.textbox_ids = {}

        self.remove_sleepers()
        self.remove_verticals()

    def draw_horizon_line(self, canvas_managers_canvas, number_of_sleepers, color='DeepPink2'):

        # draw horizon
        self.line_ids[number_of_sleepers - 1] = canvas_managers_canvas.create_line(
            self.horizon_line.coordinate_at_x0.x,
            self.horizon_line.coordinate_at_x0.y,
            self.horizon_line.coordinate_at_img_width.x,
            self.horizon_line.coordinate_at_img_width.y,
            fill=color
        )

    def draw_verticals(self, canvas_managers_canvas, number_of_sleepers, color="DeepPink2"):
        for n in range(len(self.verticals)):
            line_id = canvas_managers_canvas.create_line(
                self.verticals[n].coordinate_at_pole1.x,
                self.verticals[n].coordinate_at_pole1.y,
                self.verticals[n].coordinate_at_horizon.x,
                self.verticals[n].coordinate_at_horizon.y,
                fill=color
            )

            self.line_ids[n + number_of_sleepers] = line_id
            

    def draw_grid(self, canvas_managers_canvas, data_manager, img_width, poles, number_of_sleepers, color='DeepPink2'):
        '''
        this function is to draw all the sleepers on the canvas and to call the drawing
        of the first two lines, which are the extended reference poles, and the last line,
        which is a line parallel to the sleepers that passes through the vanishing point
        '''

        # first call the drawing of first and last
        self.draw_horizon_line(canvas_managers_canvas, number_of_sleepers, color=color)

        # loop through the line_id (excluding 0, 1 and the last number) and draw lines
        for iteration in range(0, number_of_sleepers - 1):
            start_x = 0
            start_y = self.sleepers[iteration].coordinate_at_x0.y
            end_x = img_width
            end_y = self.sleepers[iteration].coordinate_at_img_width.y

            # draw and get id
            line_id = canvas_managers_canvas.create_line(start_x, start_y, end_x, end_y, fill=color)

            # save id
            self.line_ids[iteration] = line_id

        self.draw_verticals(canvas_managers_canvas, number_of_sleepers, color=color)

        self.draw_distances(data_manager, number_of_sleepers, canvas_managers_canvas, color=color)

    def draw_distances(self, data_manager, number_of_sleepers, canvas_managers_canvas, color):
        '''
        for each drawn horizontal line, this function draws the distance between the line and the camera using a sum of the input "distance to pole 1"
        and "distance to pole 2" and then using the "desired distance".
        input:
            - data_manager
            - number_of_sleepers
            - canvas_managers_canvas
            - self.sleepers
        '''
        # Get the distances from the data manager
        distance_to1 = data_manager.get_data("distance_input")
        distance_to2 = data_manager.get_data("distance_to_pole2")
        new_distance = data_manager.get_data("desired_distance_input")
        
        # Loop through the sleepers and get the distance from the camera for each one
        for iteration in range(number_of_sleepers - 1):
            if iteration == 0:
                distance = distance_to1
            elif iteration == 1:
                distance = distance_to2
            else:
                distance = distance_to2 + new_distance * (iteration - 1)
            
            # truncate the distance to 4 decimal places
            distance = round(distance, 4)


            # Calculate the coordinates for displaying the distance text
            x_coord = self.sleepers[iteration].coordinateA.x - 20
            y_coord = self.sleepers[iteration].coordinateA.y - 7

            # Display the distance on the canvas
            text_id = canvas_managers_canvas.create_text(x_coord, y_coord, text=str(distance) + " m", font=('Actor'), fill=color)
            self.text_ids[iteration] = text_id


    def update_and_redraw_grid(self, canvas_managers_canvas, perspective_triangle, img_width, poles, data_manager):
        # get number of sleepers
        number_of_sleepers = data_manager.get_data("number_of_sleepers")
        # remove old grid
        self.remove_grid(canvas_managers_canvas)
        # create grid
        self.create_grid(canvas_managers_canvas, data_manager, perspective_triangle, img_width, poles, number_of_sleepers)
        # draw grid
        self.draw_grid(canvas_managers_canvas, data_manager, img_width, poles, number_of_sleepers)
