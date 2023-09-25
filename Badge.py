""" Module containing Avatar class """
import random
from PIL import Image
from Circle import Circle
from Config import CONFIG
from Logger import Logger

LOGGER = Logger(__name__)


class Badge:
    """ This class represents the badge objects. """

    def __init__(self, image_path):
        """ Constructor """
        self.image_path = image_path
        self.image = Image.open(image_path)

    def perform_checks(self):
        """ 
        Perfom the checks required for the excercise: 
          * Check if image is 512x512
          * If it is png
          * If the only non trasparent pixels are within the circle
          * If the colors are "happy"
        """
        self._check_image_png()
        self._check_size()
        self._check_transparency()
        self._check_happy_colors()

    def transform_image(self):
        """
        Perform the transformations required for the excercise:
        * Convert image to png
        * Convert image to 512x512 size
        * Make all pixels outiside the circle transparent
        * Make the colors happy
        """
        self._convertPhotoToPng()
        self._resizeImage()
        self._makePixelsTransparent()
        self._makeColorsHappy()

    def _check_size(self):
        """ Raise Exception if image is not size 512x512  """
        if (self.image.size != (512, 512)):
            raise Exception("Image size is not 512 x 512")
        LOGGER.logMessage("Image size is 512x512", "info")

    def _check_image_png(self):
        """ Check if the image is png type or else throws error """
        if (self.image.format != "PNG"):
            raise TypeError("Image type is not png!")
        LOGGER.logMessage("Image is in png format", "info")

    def _check_transparency(self):
        """ Check if non transparent pixels are within the circle """
        if (len(self.image.getextrema()) < 3 or self.image.getextrema()[3][0] >= CONFIG.TRANSPARENT_THRESHOLD):
            # Check if the lowest alpha value is less than transparent threshold.
            raise Exception("Image has no transparent pixels")

        circle = Circle(self.image_path)
        circle._printAttribues()
        # Check if there are non transparent pixels outside circle
        for x in range(512):
            for y in range(512):
                if (not Badge.pixelIsTransparent(self.image.getpixel((x, y))) and not circle._isInsideCircle([x, y])):
                    LOGGER.logMessage(
                        f"Pixel: x: {x}, y: {y}, values: {self.image.getpixel((x,y))}", "warning")
                    raise Exception(
                        "Image has non transparent pixels outside the circle")

        LOGGER.logMessage("Transparency rules apply")

    def _check_happy_colors(self):
        """ Check if colors of each pixel are considred happy according to our margin and return non-happy pixels"""
        non_happy_pixels = []
        for x in range(512):
            for y in range(512):
                pixel = self.image.getpixel((x, y))
                # If pixel is not fully non transparent we don't check it
                if (pixel[3] != 255):
                    continue
                color_is_happy = False
                for happy_color in CONFIG.HAPPY_COLORS:
                    RGB_check = [False, False, False]
                    # Check R channel
                    if (happy_color[0] - CONFIG.COLOR_MARGIN <= pixel[0] <= happy_color[0] + CONFIG.COLOR_MARGIN):
                        RGB_check[0] = True
                    # Check G channel
                    if (happy_color[1] - CONFIG.COLOR_MARGIN <= pixel[1] <= happy_color[1] + CONFIG.COLOR_MARGIN):
                        RGB_check[1] = True
                    # Check B channel
                    if (happy_color[2] - CONFIG.COLOR_MARGIN <= pixel[2] <= happy_color[2] + CONFIG.COLOR_MARGIN):
                        RGB_check[2] = True

                    if (False not in RGB_check):
                        color_is_happy = True
                        break
                if (not color_is_happy):
                    non_happy_pixels.append([x, y])
        # Log a message in case pixels are or are not happy
        if (len(non_happy_pixels) > 0):
            LOGGER.logMessage("Colors are not happy", "warning")
        else:
            LOGGER.logMessage("Colors are happy")
        return non_happy_pixels

    def _convertPhotoToPng(self):
        """ Take the given photo and store it in png format """
        if (self.image_path.rsplit('.', 1)[1] != 'png'):
            self.image_path = self.image_path.rsplit('.', 1)[0] + ".png"
            self.image.save(self.image_path)
            self.image = Image.open(self.image_path)
            LOGGER.logMessage("Image converted to png", "info")
        else:
            LOGGER.logMessage("Image already in png format", "info")

    def _resizeImage(self):
        """ Resize image to 512x512 pixels """
        try:
            self._check_size()
        except Exception:
            self.image = self.image.resize((512, 512))
            self.image.save(self.image_path)
            LOGGER.logMessage("Image has been resized", "info")

    def _makePixelsTransparent(self):
        """ Make all pixels ouside of the circle transparent """
        circle = Circle(self.image_path)

        for x in range(512):
            for y in range(512):
                # Check if pixel is not transparent and outisde of the circle
                if (not Badge.pixelIsTransparent(self.image.getpixel((x, y))) and not circle._isInsideCircle([x, y])):
                    # Change the alpha of pixel to 0
                    pixel_color = list(self.image.getpixel((x, y)))
                    pixel_color[3] = 0
                    new_color = tuple(pixel_color)
                    self.image.putpixel((x, y), new_color)
        # Save new image with transparent pixels outside of circle
        LOGGER.logMessage(
            "All non transparent pixels are in the circle", "info")
        # self.image.save(self.image_path)

    def _makeColorsHappy(self):
        """
        Change colors of non happy pixels to the happy ones.
        Create a dictionary with colors as strings as its keys (e.g 255-255-255) and use a random color
        from our happy colors as its values. Reuse the same color for the same unhappy color. 
        """
        non_happy_pixels = self._check_happy_colors()
        # If all pixels have happy colors return
        if (len(non_happy_pixels) == 0):
            return
        # Dict with unhappy colors as keys and happy ones as values
        colorsFound = {}
        for pixel in non_happy_pixels:
            pixel_values = self.image.getpixel(tuple(pixel))
            # Create the color key
            colorKey = '-'.join([str(x) for x in list(pixel_values[0:3])])
            if (colorKey not in colorsFound.keys()):
                colorsFound[colorKey] = CONFIG.HAPPY_COLORS[random.randint(
                    0, len(CONFIG.HAPPY_COLORS)-1)]
            # Use the color from colors already found and use the same alpha the pixel had
            new_color = list(colorsFound[colorKey])
            new_color.append(pixel_values[3])
            # Put new pixel and show image
            self.image.putpixel(tuple(pixel), tuple(new_color))
        self.image.show()
        # self.image.save(self.image_path)

    def pixelIsTransparent(pixel):
        """ Class method that returns True if pixel transparency is under the specified Threshold or False otherwise """
        return True if (pixel[3] <= CONFIG.TRANSPARENT_THRESHOLD) else False
