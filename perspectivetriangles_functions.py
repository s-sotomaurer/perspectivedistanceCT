from algebra_and_geometry_functions import find_ymc_from_two_points, find_crossing_twoequations
from internal_classes import SimpleLinearEquation, CoordinatePoint, SystemTravellingLine

from tkinter import messagebox as mb

class PerspectiveTriangle:
    def __init__(self, canvas_manager):
        self.line_A = SystemTravellingLine()
        self.line_B = SystemTravellingLine()
        self.vanishing_point = None
        self.ncs_vanishing_point = None
        self.line_ids = {'line_A': None, 'line_B': None}

    def draw_line_on_canvas(self, canvas_managers_canvas, start_x, start_y, end_x, end_y, color='DeepPink2'):
        # Method to draw a line on the canvas using given coordinates
        return canvas_managers_canvas.create_line(start_x, start_y, end_x, end_y, fill=color)

    def draw_triangle(self, canvas_managers_canvas, img_height):
        if self.line_A.equation and self.line_B.equation and self.vanishing_point:
            # make sure the necessary data are there
            
            # get coordinates of line A
            start_y_A = img_height # start at the bottom of the image
            start_x_A = (start_y_A - self.line_A.equation.intercept) / self.line_A.equation.slope # get corresponding x value

            # Draw line for equation A on the canvas using calculated coordinates
            line_A_id = self.draw_line_on_canvas(canvas_managers_canvas, start_x_A, start_y_A, self.vanishing_point.x, self.vanishing_point.y)

            
            # get coordinates of line B
            start_y_B = img_height # start at the bottom of the image
            start_x_B = (start_y_B - self.line_B.equation.intercept) / self.line_B.equation.slope # get corresponding x value
            
            # Draw line for equation B on the canvas
            line_B_id = self.draw_line_on_canvas(canvas_managers_canvas, start_x_B, start_y_B, self.vanishing_point.x, self.vanishing_point.y)

            self.line_ids = {'line_A': line_A_id, 'line_B': line_B_id}

    def calculate_vanishing_points(self):
        # I. Calculate vanishing point
        x_coordinate, y_coordinate = find_crossing_twoequations(self.line_A.equation, self.line_B.equation)
        self.vanishing_point = CoordinatePoint(x_coordinate, y_coordinate)
        
        # II. vanishing point in NCS
        x_coordinate, y_coordinate = find_crossing_twoequations(self.line_A.ncs_equation, self.line_B.ncs_equation)
        self.ncs_vanishing_point = CoordinatePoint(x_coordinate, y_coordinate)
        

    # def check_parallelism(self, canvas_manager, startpole1_coord, endpole1_coord, startpole2_coord, endpole2_coord):
    #     # Check if poles are parallel
    #     m_slope, c_intercept = find_ymc_from_two_points(startpole1_coord, endpole1_coord)
    #     canvas_manager.poles['1'].equation = SimpleLinearEquation(m_slope, c_intercept)

    #     m_slope, c_intercept = find_ymc_from_two_points(startpole2_coord, endpole2_coord)
    #     canvas_manager.poles['2'].equation = SimpleLinearEquation(m_slope, c_intercept)

    #    # if the test for parallelism of the equations of pole 1 and pole 2 is false, write a tkinter warning

    #     if not test_for_parallelism(
    #         canvas_manager.poles['1'].equation,
    #         canvas_manager.poles['2'].equation
    #     ):
    #         mb.showerror("Error", "Poles are not parallel!")

    def calculate_equations(self, pole1, pole2):
        # Calculate equation for line_A, equation for line_B (original KS on canvas)
        m_slope, c_intercept = find_ymc_from_two_points(pole1.coordinateA, pole2.coordinateA)
        self.line_A.equation = SimpleLinearEquation(m_slope, c_intercept)

        m_slope, c_intercept = find_ymc_from_two_points(pole1.coordinateB, pole2.coordinateB)
        self.line_B.equation = SimpleLinearEquation(m_slope, c_intercept)

        # calculate same on new coordinate system
        m_slope, c_intercept = find_ymc_from_two_points(pole1.ncs_coordinate_A, pole2.ncs_coordinate_A)
        self.line_A.ncs_equation = SimpleLinearEquation(m_slope, c_intercept)

        m_slope, c_intercept = find_ymc_from_two_points(pole1.ncs_coordinate_B, pole2.ncs_coordinate_B)
        self.line_B.ncs_equation = SimpleLinearEquation(m_slope, c_intercept)

    def calculate_triangle(self, canvas_manager):
        # logic for calculating perspective triangle

        # Calculate equation_line_A, equation_line_B, vanishing_point
        
        # 2 create equations and save in self
        self.calculate_equations(
            canvas_manager.poles['1'],
            canvas_manager.poles['2']
        )

        # 3 create vanishing point
        self.calculate_vanishing_points()

    def remove_triangle(self, canvas_managers_canvas):
        # Remove the lines representing the triangle from the canvas
        for line_id in self.line_ids.values(): # all the lines in the id list
            if line_id: # if they exist
                canvas_managers_canvas.delete(line_id) # delete them
        self.line_ids = {'line_A': None, 'line_B': None}

    def update_and_redraw_triangle(self, data_manager, img_height, canvas_manager):
        # Update triangle based on new data and redraw
        self.remove_triangle(canvas_manager.canvas)  # Remove the existing triangle
        self.calculate_triangle(canvas_manager)  # Recalculate triangle with updated data
        self.draw_triangle(canvas_manager.canvas, img_height)  # Draw the updated triangle


