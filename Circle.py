""" Module containing Circle class """
import cv2
import numpy as np
from Config import CONFIG
from Logger import Logger

LOGGER = Logger(__name__)


class Circle():
    """ This class is used to create and detect circles. """

    def __init__(self, image_path):
        self.image_path = image_path
        self.center, self.radious = self._detectCircle()

    def _detectCircle(self):
        # Read image.
        img = cv2.imread(self.image_path, cv2.IMREAD_COLOR)

        # Convert to grayscale.
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Blur using 3 * 3 kernel.
        gray_blurred = cv2.blur(gray, (3, 3))

        # Apply Hough transform on the blurred image.
        detected_circles = cv2.HoughCircles(gray_blurred,
                                            cv2.HOUGH_GRADIENT, dp=CONFIG.CV2_CONFIG["dp"], minDist=CONFIG.CV2_CONFIG[
                                                "minDist"], param1=CONFIG.CV2_CONFIG["param1"],
                                            param2=CONFIG.CV2_CONFIG["param2"], minRadius=CONFIG.CV2_CONFIG["minRadius"], maxRadius=CONFIG.CV2_CONFIG["maxRadius"])
        if (detected_circles is None):
            raise Exception("No circles detected")

        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))
        # Draw circle detected
        Circle.drawDetectedCircle(
            img, detected_circles[0][0][0], detected_circles[0][0][1], detected_circles[0][0][2])

        return detected_circles[0][0][0:2], detected_circles[0][0][2]

    def _isInsideCircle(self, point):
        """ Return true if point given is inside circle """
        if (((point[0] - self.center[0]) ** 2 + (point[1] - self.center[1]) ** 2) < (self.radious + CONFIG.CIRCLE_MARGIN) ** 2):
            return True
        return False

    def _printAttribues(self):
        """ Log the circle's attributes """
        LOGGER.logMessage(
            f"Circle found with attributes: Center: {self.center}, radious: {self.radious}", "debug")

    def drawDetectedCircle(img, x, y, radious):
        """ Class method to draw circle detected from opencv """
        cv2.circle(img, (x, y), radious, (255, 255, 255), 2)

        # Draw a small circle (of radius 1) to show the center.
        cv2.circle(img, (x, y), 1, (255, 255, 255), 3)
        cv2.imshow("Detected Circle", img)
        cv2.waitKey()
