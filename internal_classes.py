import math
from tkinter import messagebox as mb

class DataManager:
    def __init__(self):
        self.shared_data = {}

    def set_data(self, key, value):
        self.shared_data[key] = value

    def get_data(self, key):
        return self.shared_data.get(key)

    def validate_manual_input(self):
        """
        Validate manual input for distance and pole size.
        Show error messages for invalid input.

        Returns:
        --------
        bool:
            True if input is valid, False otherwise.
        """

        required_keys = ["distance_input", "distance_to_pole2", "real_pole_size", "desired_distance_input", "camera_height", "number_of_sleepers"]

        if any(self.shared_data.get(key) is None for key in required_keys):
            mb.showerror("Error", "Cannot estimate distances without all input values")
            return False

        dist_to_pole1 = self.shared_data["distance_input"]
        dist_to_pole2 = self.shared_data["distance_to_pole2"]
        pole_width = self.shared_data["real_pole_size"]
        desired_dist = self.shared_data["desired_distance_input"]
        
        # Check if distance to pole 1 is greater than distance to pole 2
        if dist_to_pole1 > dist_to_pole2:
            mb.showerror("Error", "Distance to pole 1 must be smaller than distance to pole 2")
            return False

        # Check if all values are positive
        if not (pole_width > 0 and dist_to_pole1 > 0 and dist_to_pole2 > 0 and desired_dist > 0):
            mb.showerror("Error", "All values must be positive")
            return False
        
        # check if number of poles is an integer and larger than 3
        if not isinstance(self.shared_data["number_of_sleepers"], int):
            mb.showerror("Error", "Number of sleepers must be an integer")
            return False
        
        if self.shared_data["number_of_sleepers"] < 4:
            mb.showerror("Error", "Number of sleepers must be at least 4")
            return False        

        # Return True if all checks passed
        return True

class CoordinatePoint:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

class SimpleLinearEquation:
    def __init__(self, slope=None, intercept=None):
        self.slope = slope
        self.intercept = intercept

class StraightLine:
    def __init__(self, xA=None, yA_at_railline=None, xB=None, yB_at_railline=None, length=None):
        self.length = length
        self.yA_at_railline = yA_at_railline
        self.yB_at_railline = yB_at_railline
        self.xA = xA
        self.xB = xB
        self.coordinateA = CoordinatePoint(xA, yA_at_railline)
        self.coordinateB = CoordinatePoint(xB, yB_at_railline)
        self.equation = SimpleLinearEquation()
        self.coordinate_at_x0 = CoordinatePoint()
        self.coordinate_at_img_width = CoordinatePoint()
    
    def save_line_extension(self, x0, y0, xend, yend):
        self.coordinate_at_x0 = CoordinatePoint(x0, y0)
        self.coordinate_at_img_width = CoordinatePoint(xend, yend)

class VerticalLine(StraightLine):
    def __init__(self, equation=None, coordinate_at_pole1=CoordinatePoint(), coordinate_at_horizon=CoordinatePoint()):
        super().__init__()  # Call the __init__ method of the base class
        self.equation = equation
        self.coordinate_at_pole1 = coordinate_at_pole1
        self.coordinate_at_horizon = coordinate_at_horizon

class SystemTravellingLine(StraightLine):
    def __init__(self, xA=None, yA_at_railline=None, xB=None, yB_at_railline=None, length=None):
        super().__init__(xA, yA_at_railline, xB, yB_at_railline, length)
        self.ncs_coordinate_A = None
        self.ncs_coordinate_B = None
        self.ncs_equation = SimpleLinearEquation()

