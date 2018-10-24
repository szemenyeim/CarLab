import numpy as np
import cv2

# Compute scaled absolute image gradients
def create_sobels(image, sobel_kernel=3):
    # Convert to gray

    # Compute x and y derivatives using sobel

    # Get absolute value

    # Compute scaling factor

    # Scale gradients


    return abs_sobelx,abs_sobely,scaled_sobelx,scaled_sobely

# Threshold gradients based on magintude
def mag_thresh(scaled_sobelx, scaled_sobely, mag_thresh=(0, 255)):
    # Compute gradient magnitude

    # Threshold using inRange


    return mag_binary

# Threshold gradients based on direction
def dir_threshold(abs_sobelx, abs_sobely, thresh=(0, np.pi/2)):
    # Compute gradient direction

    # Threshold using inRange


    return dir_binary

# Apply color threshold
def color_threshold(image):
    # Convert to hls

    # Get luminance

    # Threshold using inRange


    return l_binary

# Combine all kinds of thresholds
def apply_thresholds(image, ksize=3):
    # Get derivatives

    # Threshold scaled gradient images using inRange

    # Compute magnitude and direction threshold

    # Compute color threshold


    # Combine all thresholded images


    return combined