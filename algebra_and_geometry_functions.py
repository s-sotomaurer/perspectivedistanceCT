import math

def estimate_distance(point1, point2):
    x1, y1 = point1.x, point1.y
    x2, y2 = point2.x, point2.y
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

def find_ymc_from_two_points(coordinate1, coordinate2): # a.k.a function4
    x1, y1, x2, y2 = coordinate1.x, coordinate1.y, coordinate2.x, coordinate2.y
    # m_slope = ((y2 - ((x2 * y1) / (x1))) / (1 - x2 / x1))
    if y1 != y2:
        m_slope = (y2 - y1) / (x2 - x1)
    else:
        m_slope = 0

    c_axiscut = y1 - m_slope * x1

    return m_slope, c_axiscut

def findintercept_given_x_y_m(x, y, slope):
    # clearing from a y = mx + c, we get that c = y - mx
    c_intercept = y - slope * x
    return c_intercept

def find_crossing_twoequations(equationA, equationB): # a.k.a. function5
    slopeA, interceptA, slopeB, interceptB = equationA.slope, equationA.intercept, equationB.slope, equationB.intercept
    
    # to-do: write a case for when slopeA and slopeB are equal (division by zero!!!)
    if slopeA - slopeB == 0:
        crossing_x = (interceptB - interceptA) / (2e-10)
    else:
        crossing_x = (interceptB - interceptA) / (slopeA - slopeB)
    
    crossing_y = slopeA * crossing_x + interceptA

    return crossing_x, crossing_y

def findx_given_y_m_c(equation, y_coordinate): # aka function8
    # objective find x value given y, m and c in a first-degree function (y = mx + c)
    x_coordinate = (y_coordinate - equation.intercept) / equation.slope
    return x_coordinate

def findy_given_x_m_c(equation, x_coordinate):
    y_coordinate = equation.slope * x_coordinate + equation.intercept
    return y_coordinate

def test_for_parallelism(pole1, pole2):
    # Retrieve slopes from DataManager
    pole1_slope = pole1.equation.slope
    pole2_slope = pole2.equation.slope

    # Check if slopes are approximately equal (adjust the threshold as needed)
    return abs(pole1_slope - pole2_slope) < 0.03  # Adjust threshold for parallelism

def findxA_givendistance_givenequationsAandB(equationA, equationB, sleeper_size): # aka function7
    # given two equations and the distance at a certain point between both, this function finds the
    # location of xA, which is the x value for the point at equationA (leftmost equation in a positive quarter of a xy plane)

    factor1 = equationA.intercept - equationB.intercept - equationB.slope * sleeper_size
    factor2 = equationB.slope - equationA.slope
    
    xA = factor1 / factor2
    
    return xA

def extend_line(line, img_width):
    x0 = 0
    y0 = findy_given_x_m_c(line.equation, x0)
    xend = img_width
    yend = findy_given_x_m_c(line.equation, xend)

    return x0, y0, xend, yend