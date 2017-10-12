#!/usr/local/bin/python2

# @Author: Brandon Tarney
# @Date: 10/2017

# Usage class is for encapsulating user mouse input

import cv2
import numpy as np

class MouseHandler:
    def __init__(self, windowname, image ):
        self.windowname = windowname
        self.image = image
        cv2.setMouseCallback(self.windowname, self.mouse_callback())
        self.show()

    def show(self):
        cv2.imshow(self.windowname, self.images[0])

    def mouse_callback(self, event, x_pt, y_pt, flags, param):
        pt = (x,y)
        if event == cv2.EVENT_LBUTTONDOWN:
            print("Left button click")
        elif event == cv2.EVENT_LBUTTONUP:
            print("Left button up")
        
