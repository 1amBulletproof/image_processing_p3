#!/usr/local/bin/python2

# @Author: Brandon Tarney
# @Date: 10/2017

# Usage class is for encapsulating user keyboard handling

import cv2
import numpy as np

class KeyboardHandler:
    def __init__(self, key='0', img=np.zeros(1)):
        self.key = key
        self.img = img

    def do_work(self):
        #insert logic here!
        if self.key == ord('s'):
            print("Saving file to output_file.jpg")
            cv2.imwrite('output_file.jpg', self.img)
            cv2.destroyAllWindows()
        else:
            cv2.destroyAllWindows()

    def handle_keyboard_input(self, key, img):
        #insert logic here!
        if key == ord('s'):
            print("Saving file to output_file.jpg")
            cv2.imwrite('output_file.jpg', img)
            cv2.destroyAllWindows()
        else:
            cv2.destroyAllWindows()
