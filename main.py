import numpy as np
import cv2
import time
from LineDetection import process_image
from Estimator import Estimator
from Control import createContorller
import matplotlib.pyplot as plt


def drawImage(img, dev, cur):

    # Annotating curvature
    fontType = cv2.FONT_HERSHEY_SIMPLEX
    curvature_text = 'The radius of curvature = ' + str(round(cur, 3)) + 'm'
    cv2.putText(img, curvature_text, (30, 60), fontType, 0.5, (255, 255, 255), 1)

    # Annotating deviation
    direction = "left" if dev < 0 else "right"
    deviation_text = 'Vehicle is ' + str(round(abs(dev), 3)) + 'm ' + direction + ' of center'
    cv2.putText(img, deviation_text, (30, 110), fontType, 0.5, (255, 255, 255), 1)

    return img

if __name__=='__main__':

    # Measure framerate
    sum = 0
    frameCnt = 0

    # Create estimator and controller classes
    estimator = Estimator()
    controller = createContorller()

    # Create empty arrays for plotting
    devs = np.array([])
    devFilts = np.array([])
    curs = np.array([])
    curFilts = np.array([])
    slopeFilts = np.array([])
    controls = np.array([])

    # Create figures
    fig = plt.gcf()
    t = np.linspace(0, len(devs) - 1, len(devs))
    p1 = plt.subplot(311)
    p1.set_title('Deviation from lane center')
    line11, = p1.plot(t, devs, 'r')
    line12, = p1.plot(t, devFilts, 'b')
    plt.legend((line11, line12), ('Measured', 'Filtered'))
    p2 = plt.subplot(312)
    p2.set_title('Line curvature')
    line21, = p2.plot(t, np.log(curs), 'r')
    line22, = p2.plot(t, np.log(curFilts), 'b')
    plt.legend((line21, line22), ('Measured', 'Filtered'))
    p3 = plt.subplot(313)
    p3.set_title('Slope, deviation and control')
    line31, = p3.plot(t, slopeFilts * 10, 'r')
    line32, = p3.plot(t, controls, 'b')
    line33, = p3.plot(t, devFilts, 'g')
    plt.legend((line31, line32, line33), ('Slope', 'Controller Output', 'Deviation'))
    fig.show()
    fig.canvas.draw()

    # Read video file

    while(True):

        # Read frame from video

        # Start time measurement
        t1 = time.time()

        # Process image

        # Update estimates

        # Set controller inputs

        # Compute control

        # End time measurement
        t2 = time.time()

        if devEst is not None:

            # Draw on image
            img = drawImage(img,devEst,curEst)

            # Append arrays for plotting
            devs = np.append(devs,dev)
            devFilts = np.append(devFilts,devEst)
            curs = np.append(curs,cur)
            curFilts = np.append(curFilts,curEst)
            slopeFilts = np.append(slopeFilts,slopeEst)
            controls = np.append(controls,control)

            # Update plots
            t = np.linspace(0, len(devs) - 1, len(devs))
            line11.set_data(t,devs)
            line12.set_data(t,devFilts)
            line21.set_data(t,np.log(curs))
            line22.set_data(t,np.log(curFilts))
            line31.set_data(t,slopeFilts*40)
            line32.set_data(t,controls)
            line33.set_data(t,devFilts*4)
            p1.autoscale_view(True, True, True)
            p1.relim()
            p2.autoscale_view(True, True, True)
            p2.relim()
            p3.autoscale_view(True, True, True)
            p3.relim()
            fig.canvas.draw()

        # Increate time elapsed and frame counter
        sum += (t2 - t1)
        frameCnt += 1

        # Show image and exit on 'Esc'
        cv2.imshow("video",proc)
        if cv2.waitKey(1) == 27:
            exit(0)

    # Display runtime and fps
    avgTime = sum / frameCnt * 1000
    print("Average time: %f" % avgTime)
    print("Average fps: %f" % (1000.0 / avgTime))

    # Prevent quitting immediately
    plt.show()