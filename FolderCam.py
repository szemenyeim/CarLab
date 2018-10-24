import cv2
import glob
import os.path as osp

class FolderCam(object):
    def __init__(self,folder="./images", extension="*.jpg"):
        self.folder = folder
        self.images = glob.glob1(folder,extension)
        self.images.sort()
        self.cntr = 0

    def read(self):
        success = self.cntr < len(self.images)
        img = cv2.imread(osp.join(self.folder, self.images[self.cntr])) if success else None
        self.cntr += 1
        return success, img