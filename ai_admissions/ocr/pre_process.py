# Copyright 2020, AI Admissions: Ahmed, Aman, Paschal, Varun (Boston University)
import math
import cv2 as cv
import numpy as np
import PIL.ImageOps as ImgOp

from PIL import Image
from pathlib import Path
from scipy import ndimage
from typing import Tuple, Union
from deskew import determine_skew
from ..utilities.config import error

def rotate(image: np.ndarray, angle: float, background: Union[int, Tuple[int, int, int]]):
    old_width, old_height = image.shape[:2]
    angle_radian = math.radians(angle)
    width = abs(np.sin(angle_radian) * old_height) + abs(np.cos(angle_radian) * old_width)
    height = abs(np.sin(angle_radian) * old_width) + abs(np.cos(angle_radian) * old_height)
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv.getRotationMatrix2D(image_center, angle, 1.0)
    rot_mat[1, 2] += (width - old_width) / 2
    rot_mat[0, 2] += (height - old_height) / 2
    my_size = (cv.warpAffine(image, rot_mat, (int(round(height)), int(round(width))), borderValue=background)).shape
    return cv.warpAffine(image, rot_mat, (int(round(height)), int(round(width))), borderValue=background)

# Read:
# https://www.danvk.org/2015/01/07/finding-blocks-of-text-in-an-image-using-python-opencv-and-numpy.html
def CannyThreshold(img, val):
    """ Input: cv image, val: the lower threshold value
        Output: Img with edges highlighted in white and black background
        Method: I add Gaussiann Blur with standard deviations 1 for both x and y
                I use the Canny library to detect the edges and 
                I use a kernel size of 3, High_threshold=3*low_threshold which is 
                recommended by canny
    """
    low_threshold = val
    max_lowThreshold = 100
    ratio = 3
    kernel_size = 3
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # Convert image to grayscale
    img_blur = cv.GaussianBlur(img_gray, (5,5), 1, 1) # Remove gaussian noise
    img_filter = cv.bilateralFilter(img_blur, 9, 75, 75) # Remove noise near edges
    detected_edges = cv.Canny(img_filter, low_threshold, low_threshold*ratio, kernel_size, L2gradient=True)
    mask = (detected_edges != 0)
    dst = img * (mask[:,:,None].astype(img.dtype))
    return dst

def remove_edges(img, ksize):
    no_edge_img = cv.medianBlur(img, ksize)
    # cv.imwrite('enhanced_no_edge.png', no_edge_img)
    return no_edge_img

def dilate_img(img,dilationX,dilationY):
    kernel = cv.getStructuringElement(cv.MORPH_RECT,(dilationX,dilationY))
    dilated = cv.dilate(img, kernel, iterations = 10) # dilate
    # cv.imwrite('dilate.png', dilated)
    return dilated

def get_contour(img, dilated_img):
    img_cv = cv.cvtColor(dilated_img, cv.COLOR_BGR2GRAY)
    contours, hierarchy = cv.findContours(img_cv,\
                                            cv.RETR_EXTERNAL,\
                                            cv.CHAIN_APPROX_SIMPLE)
    # for each contour found, draw a rectangle around it on original image
    ROI = img
    for contour in contours:
        # get rectangle bounding contour
        [x,y,w,h] = cv.boundingRect(contour)
        # discard areas that are too small
        if h<300 or w<300:
            continue
        cv.rectangle(dilated_img,(x,y),(x+w,y+h),(255,0,255),2)
        ROI = img[y:y+h, x:x+w]
    # write original image with added contours to disk  
    # cv.imwrite("contoured.png", dilated_img)
    return ROI

def image_smoothening(img):
    ret1, th1 = cv.threshold(img, 180, 255, cv.THRESH_BINARY)
    ret2, th2 = cv.threshold(cv.cvtColor(th1, cv.COLOR_BGR2GRAY),\
                            0, 255,\
                            cv.THRESH_BINARY + cv.THRESH_OTSU)
    blur = cv.GaussianBlur(th2, (1, 1), 0)
    ret3, th3 = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    return th3

def deskew_img(img):
    """ Input: img_path-Image file path, output-flag to produce output
        Output: error_flag (), a cv image (in RGB) which is deskewed.
        Sample ouptputs at https://github.com/sbrunner/deskew
        uses deskew library in python.
        returns error code for deskew failure and the original image if
        error is found, otherwise it returns error code for no failure and the
        deskewed image
    """
    deskew_error = error['NONE']
    try:
        grayscale = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        angle = determine_skew(grayscale)
        deskewed_img = rotate(img, angle, (255,255,255))
    except Exception:
        deskew_error = error['PP_DSKF']
        deskewed_img = img
    return deskew_error, deskewed_img

def border_removal(img):
    """ returns error code for failure in border removal and original image if
        error is found, otherwise it returns error code for no failure and the
        image with borders removed
    """
    border_removal_error = error['NONE']
    try:
        edge = CannyThreshold(img, 0)
        no_edge = remove_edges(edge, 3)
        # repeat once more
        invert_no_edge = cv.bitwise_not(no_edge)
        new_edge = CannyThreshold(invert_no_edge, 0)
        no_border = remove_edges(new_edge, 3)
        # dilate the image to get connected compnents
        dilated_img = dilate_img(no_border, 3, 6)
        # Get coordinates of bounding box on majority text area
        ROI_img = get_contour(img, dilated_img)
    except Exception:
        border_removal_error = error['PP_BRF']
        ROI_img = img
    return border_removal_error, ROI_img

def remove_noise_and_smooth(img):
    """ returns error code for failure in image denoising and original image if
        error is found, otherwise it returns error code for no failure and the
        image with noise removed
    """
    denoising_error = error['NONE']
    try:
        filtered = cv.adaptiveThreshold(cv.cvtColor(img, cv.COLOR_BGR2GRAY),
                                        255,
                                        cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv.THRESH_BINARY,
                                        41,
                                        3)
        kernel = np.ones((1, 1), np.uint8)
        opening = cv.morphologyEx(filtered, cv.MORPH_OPEN, kernel)
        closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel)
        img = image_smoothening(img)
        or_image = cv.bitwise_or(img, closing)
    except Exception:
        denoising_error = error['PP_DNF']
        or_image = img
    return denoising_error, or_image

def process_img(img):
    # Image Deskewing
    r1, deskewed_img = deskew_img(img) 

    # Border Removal
    r2, cropped_img = border_removal(deskewed_img)
    
    # Image De-noising
    r3, final_img = remove_noise_and_smooth(cropped_img)

    r = [r1, r2, r3]
    return r, Image.fromarray(final_img)

# def main():
#     output_dir_path=Path().cwd()
#     output=True
#     img = cv.imread('boston_cooking_a.jpg')
#     r, out = process_img(img)
#     out.save('out.png')
# main()