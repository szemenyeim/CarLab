import numpy as np
import cv2

# Compute scaled absolute image gradients
def create_sobels(image, sobel_kernel=3):
    # Convert to gray
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Compute x and y derivatives using sobel
    sobelx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=sobel_kernel)
    # Get absolute value
    abs_sobelx = np.absolute(sobelx)
    abs_sobely = np.absolute(sobely)
    # Compute scaling factor
    multx = 255/np.max(abs_sobelx)
    multy = 255/np.max(abs_sobely)
    # Scale gradients
    scaled_sobelx = np.uint8(multx*abs_sobelx)
    scaled_sobely = np.uint8(multy*abs_sobely)

    return abs_sobelx,abs_sobely,scaled_sobelx,scaled_sobely

# Threshold gradients based on magintude
def mag_thresh(scaled_sobelx, scaled_sobely, mag_thresh=(0, 255)):
    # Compute gradient magnitude
    scaled_sobel = scaled_sobelx + scaled_sobely
    # Threshold using inRange
    mag_binary = cv2.inRange(scaled_sobel, mag_thresh[0]*2, mag_thresh[1]*2)

    return mag_binary

# Threshold gradients based on direction
def dir_threshold(abs_sobelx, abs_sobely, thresh=(0, np.pi/2)):
    # Compute gradient direction
    grad_dir = np.arctan2(abs_sobely, abs_sobelx)
    # Threshold using inRange
    dir_binary = cv2.inRange(grad_dir, thresh[0], thresh[1])

    return dir_binary

# Apply color threshold
def color_threshold(image):
    # Convert to hls
    hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
    # Get luminance
    l_channel = hls[:,:,2]
    # Threshold using inRange
    l_binary = cv2.inRange(l_channel, 170, 255)

    return l_binary

# Combine all kinds of thresholds
def apply_thresholds(image, ksize=3):
    # Get derivatives
    abs_sobelx, abs_sobely, scaled_sobelx, scaled_sobely = create_sobels(image, sobel_kernel=ksize)
    # Compute magnitude and direction threshold
    mag_binary = mag_thresh(scaled_sobelx, scaled_sobely, mag_thresh=(30, 100))
    dir_binary = dir_threshold(abs_sobelx, abs_sobely,  thresh=(0.7, 1.3))
    # Compute color threshold
    color_binary = color_threshold(image)

    # Combine all thresholded images
    combined = np.zeros_like(dir_binary)
    combined[((mag_binary == 255) & (dir_binary == 255)) | (color_binary == 255)] = 1

    return combined

def warp(img):
    img_size = (img.shape[1], img.shape[0])

    # Source and destination points
    src = np.float32(
        [[380, 0],
          [875, 235],
          [60, 235],
          [470, 0]])

    dst = np.float32(
        [[150, 0],
         [800, 260],
         [150, 260],
         [800, 0]])

    # Get perspective transforms
    M = cv2.getPerspectiveTransform(src, dst)
    Minv = cv2.getPerspectiveTransform(dst, src)

    # Warp image
    binary_warped = cv2.warpPerspective(img, M, img_size, flags=cv2.INTER_LINEAR)

    return binary_warped, Minv

def get_histogram(binary_warped):
    histogram = np.sum(binary_warped[binary_warped.shape[0]//2:,:], axis=0)

    return histogram