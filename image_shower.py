#!/usr/local/bin/python2

# @Author: Brandon Tarney
# @Date: 10/2017

# Usage: class is for encapsulating showing an image

import cv2
import numpy as np

class ImageShower:
    def __init__(self, img=np.zeros(5), description="no description", duration_ms=-1):
        self.image = img
        self.description = description
        self.duration_ms = duration_ms

    def show(self):
        cv2.imshow(self.description, self.image)
        if(self.duration_ms == -1):
            key = cv2.waitKey()
        else:
            key = cv2.waitKey(duration_ms)
        return key


    def show_image(self, img, description, duration_ms=-1):
        cv2.imshow(description, img)
        if(duration_ms == -1):
            key = cv2.waitKey()
        else:
            key = cv2.waitKey(duration_ms)
        return key
