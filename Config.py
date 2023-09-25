""" 
This module contains the configuration class, with general config about the project. For simplicity reason we are using a python class
instead of env files or yaml/json
"""


class CONFIG:
    """ 
    Bellow are the config variables we can manipulate for this project. Methods could be added
    so as to configure the values through them or return them the way it suits us.
    """

    # Bellow are the colors we consider happy for this excersice
    HAPPY_COLORS = [
        (255, 255, 255),    # White
        (255, 255, 0),      # Yellow
        (255, 0, 0),        # Bright Red
        (0, 255, 0),        # Bright Green
        (135, 206, 235),    # Sky Blue
        (255, 192, 203),    # Pink
        (255, 165, 0),      # Orange
        (230, 230, 250),    # Lavender
        (255, 204, 204),    # Pastel Pink
        (255, 255, 153),    # Pastel Yellow
        (173, 255, 173),    # Pastel Green
        (173, 216, 230),    # Pastel Blue
        (221, 160, 221),    # Pastel Purple
        (255, 204, 153),    # Pastel Orange
        (230, 230, 250),    # Pastel Lavender
        (255, 218, 185),    # Pastel Peach
        (189, 252, 201),    # Pastel Mint
        (255, 192, 203)     # Pastel Coral
    ]
    # Pixels with transparency under 100 are considered transparent
    TRANSPARENT_THRESHOLD = 100
    # Color margin for a color to be considered one of the happy ones
    COLOR_MARGIN = 100
    # Circle margin to check if pixel is inside of cirle, since some pixels might be a bit ouside the radious since we are drawing it on pixels
    CIRCLE_MARGIN = 5
    # Config vars for opencv to find circles
    CV2_CONFIG = {
        "dp": 1,  # inverse ratio of the accumulator resolution to the image resolution, should be 1 in most cases
        "minDist": 200,  # minimum distance between the centers of the detected circles
        "param1": 40,  # param used for edge detection, should be around 40-100
        "param2": 9,  # sets a threshold value for the number of votes a circle candidate must receive to be considered a valid circle
        "minRadius": 100,  # min circle radious
        "maxRadius": 250,  # max circle radious
    }
