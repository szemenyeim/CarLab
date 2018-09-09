import numpy as np
import cv2
import time
from LineDetection import process_image
from Estimator import Estimator
import matplotlib.pyplot as plt


def drawImage(img, dev, cur, devFilt, curFilt, slope):

    # Annotating curvature
    fontType = cv2.FONT_HERSHEY_SIMPLEX
    curvature_text = 'The radius of curvature = ' + str(round(cur, 3)) + 'm'
    cv2.putText(img, curvature_text, (30, 60), fontType, 0.5, (255, 255, 255), 1)

    curvature_text = 'The radius of filtered curvature = ' + str(round(curFilt, 3)) + 'm'
    cv2.putText(img, curvature_text, (30, 160), fontType, 0.5, (255, 255, 255), 1)

    # Annotating deviation
    direction = "left" if dev < 0 else "right"
    deviation_text = 'Vehicle is ' + str(round(abs(dev), 3)) + 'm ' + direction + ' of center'
    cv2.putText(img, deviation_text, (30, 110), fontType, 0.5, (255, 255, 255), 1)

    direction = "left" if devFilt < 0 else "right"
    deviation_text = 'Vehicle is ' + str(round(abs(devFilt), 3)) + 'm ' + direction + ' of center (filtered)'
    cv2.putText(img, deviation_text, (30, 210), fontType, 0.5, (255, 255, 255), 1)

    return img

if __name__=='__main__':
    output = 'result.mp4'
    clip = cv2.VideoCapture("original.mp4")

    sum = 0
    frameCnt = 0

    estimator = Estimator()

    devs = np.array([])
    devFilts = np.array([])
    curs = np.array([])
    curFilts = np.array([])
    slopeFilts = np.array([])

    fig = plt.gcf()
    t = np.linspace(0, len(devs) - 1, len(devs))
    p1 = plt.subplot(311)
    p1.set_title('Deviation from lane center')
    line11, = p1.plot(t, devs, 'r')
    line12, = p1.plot(t, devFilts, 'b')
    p2 = plt.subplot(312)
    p2.set_title('Line curvature')
    line21, = p2.plot(t, np.log(curs), 'r')
    line22, = p2.plot(t, np.log(curFilts), 'b')
    p3 = plt.subplot(313)
    p3.set_title('Slope and deviation')
    line31, = p3.plot(t, slopeFilts * 10, 'r')
    line32, = p3.plot(t, slopeFilts * 10, 'b')
    line33, = p3.plot(t, devFilts, 'g')
    fig.show()
    fig.canvas.draw()

    while(True):

        good, img = clip.read()
        if not good:
            break

        t1 = time.time()
        proc, dev, cur = process_image(img)
        curProc, slope, devProc = estimator.update(cur,dev)
        proc = drawImage(proc,dev,cur,devProc,curProc,slope)
        t2 = time.time()

        devs = np.append(devs,dev)
        devFilts = np.append(devFilts,devProc)
        curs = np.append(curs,cur)
        curFilts = np.append(curFilts,curProc)
        slopeFilts = np.append(slopeFilts,slope)

        # Separate
        pos_signal = slopeFilts.copy()*10
        neg_signal = slopeFilts.copy()*10
        pos_signal[pos_signal <= -0.05] = np.nan
        neg_signal[neg_signal > 0.00] = np.nan

        t = np.linspace(0, len(devs) - 1, len(devs))
        line11.set_data(t,devs)
        line12.set_data(t,devFilts)
        line21.set_data(t,np.log(curs))
        line22.set_data(t,np.log(curFilts))
        line31.set_data(t,pos_signal)
        line32.set_data(t,neg_signal)
        line33.set_data(t,devFilts)
        p1.autoscale_view(True, True, True)
        p1.relim()
        p2.autoscale_view(True, True, True)
        p2.relim()
        p3.autoscale_view(True, True, True)
        p3.relim()
        fig.canvas.draw()

        sum += (t2 - t1)
        frameCnt += 1

        cv2.imshow("video",proc)
        if cv2.waitKey(1) == 27:
            exit(0)


    plt.show()

    avgTime = sum / frameCnt * 1000
    print("Average time: %f" % avgTime)
    print("Average fps: %f" % (1000.0 / avgTime))