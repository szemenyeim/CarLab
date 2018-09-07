import numpy as np
import cv2
import time
from EdgeDetection import apply_thresholds
import LineDetection

def draw_lane_lines(original_image, warped_image, Minv, draw_info):
    leftx = draw_info['leftx']
    rightx = draw_info['rightx']
    left_fitx = draw_info['left_fitx']
    right_fitx = draw_info['right_fitx']
    ploty = draw_info['ploty']

    warp_zero = np.zeros_like(warped_image).astype(np.uint8)
    color_warp = np.dstack((warp_zero, warp_zero, warp_zero))

    pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
    pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
    pts = np.hstack((pts_left, pts_right))

    cv2.fillPoly(color_warp, np.int_([pts]), (0,255, 0))

    newwarp = cv2.warpPerspective(color_warp, Minv, (original_image.shape[1], original_image.shape[0]))
    result = cv2.addWeighted(original_image, 1, newwarp, 0.3, 0)

    return result

global used_warped
global used_ret

def process_image(image):
    global used_warped
    global used_ret

    roi = img[450:710, 220:1150]

    # Thresholding
    binary = apply_thresholds(roi)

    # Transforming Perspective
    binary_warped, Minv = LineDetection.warp(binary)

    # Getting Histogram
    histogram = LineDetection.get_histogram(binary_warped)

    # Sliding Window to detect lane lines
    ret = LineDetection.slide_window(binary_warped, histogram)

    # Measuring Curvature
    left_curverad, right_curverad = LineDetection.measure_curvature(ret)

    # Sanity check
    if not LineDetection.sanity(ret,left_curverad,right_curverad):
        binary_warped = used_warped
        ret = used_ret

    result = image

    # Visualizing Lane Lines Info
    result[450:710, 220:1150] = draw_lane_lines(roi, binary_warped, Minv, ret)

    # Annotating curvature
    fontType = cv2.FONT_HERSHEY_SIMPLEX
    curvature_text = 'The radius of curvature = ' + str(round(left_curverad, 3)) + 'm'
    cv2.putText(result, curvature_text, (30, 60), fontType, 0.5, (255, 255, 255), 1)

    # Annotating deviation
    deviation_pixels = image.shape[1]/2 - abs(ret['right_fitx'][-1] - ret['left_fitx'][-1])
    xm_per_pix = 3.7/(650)
    deviation = deviation_pixels * xm_per_pix
    direction = "left" if deviation < 0 else "right"
    deviation_text = 'Vehicle is ' + str(round(abs(deviation), 3)) + 'm ' + direction + ' of center'
    cv2.putText(result, deviation_text, (30, 110), fontType, 0.5, (255, 255, 255), 1)

    used_warped = binary_warped
    used_ret = ret

    return result

if __name__=='__main__':
    output = 'result.mp4'
    clip = cv2.VideoCapture("original.mp4")

    sum = 0
    frameCnt = 0

    while(True):
        good, img = clip.read()
        if not good:
            break
        t1 = time.time()
        proc = process_image(img)
        t7 = time.time()
        sum += (t7 - t1)
        frameCnt += 1
        cv2.imshow("video",proc)
        if cv2.waitKey(1) == 27:
            exit(0)
    avgTime = sum / frameCnt * 1000
    print("Average time: %f" % avgTime)
    print("Average fps: %f" % (1000.0 / avgTime))