#!/usr/local/bin/python2

#Framework for basic openCV2 dev in python 2

#Usage: <program> <image_path> 

#lib: ImageShower.show_image(), Usage.show(), MouseHandler.show(), KeyboardHandler.handle_keyboard_input(), 

import time
import sys
import cv2
from matplotlib import pyplot as plt
import numpy as np


from keyboard_handler import KeyboardHandler
from mouse_handler import MouseHandler
from usage import Usage
from image_shower import ImageShower

def main():
    usage = Usage("USAGE: python2 %s <src_img_path> <ref_image_path> <optional_mask_path>" % (sys.argv[0]))
    img_helper = ImageShower()
    key_helper = KeyboardHandler()

    #------------------------------------------------
    #Check and Read arguments
    #------------------------------------------------
    if len(sys.argv) > 4 or len(sys.argv) < 2:
        print "ERROR: Missing Arguments"
        usage.show()
        sys.exit(1)
    elif sys.argv[1] == "-h":
        usage.show()
        sys.exit(0)
    elif len(sys.argv) == 4:
        input_mask = sys.argv[3]
        ref_img_name = sys.argv[2]
        src_img_name = sys.argv[1]
        mask = True;
    elif len(sys.argv) == 3:
        ref_img_name = sys.argv[2]
        src_img_name = sys.argv[1]
        mask = False

    #------------------------------------------------
    #Read/load image:
    #------------------------------------------------
    src_img = cv2.imread(src_img_name,1) #color img
    ref_img = cv2.imread(ref_img_name,1) #color img

    #------------------------------------------------
    #Show OG image (sanity check):
    #------------------------------------------------
    img_helper.show_image(src_img, "Input Image")
    img_helper.show_image(ref_img, "Reference Image")

    #------------------------------------------------
    #Img Processing
    #------------------------------------------------
    print("MATCH THE REFERENCE HISTOGRAM")
    transformed_img = match_histogram(src_img, ref_img)
    print
    img_helper.show_image(transformed_img, "Histogram Matched Image")

    if mask :
        mask = cv2.imread(input_mask, 0) #grayscale mask
        print("MASK THE IMAGE")
        masked_img = mask_image(transformed_img, mask)
        print
        transformed_img = masked_img

    #------------------------------------------------
    #Show Final Image (with changes):
    #------------------------------------------------
    #Show image and wait: '<esc>' to quit or 's' to save
    key = img_helper.show_image(transformed_img, "Final IMG")
    key_helper.handle_keyboard_input(key, transformed_img)


    '''
    #matplotLIB show src and ref img & output img
    #- also potentially plot src, ref, and final cdf
    
    plt.subplot(331),plt.imshow(sobel, 'gray'),plt.title('Sobel'),plt.axis('off')
    plt.subplot(332),plt.imshow(scharr, 'gray'),plt.title('Scharr'),plt.axis('off')
    plt.subplot(333),plt.imshow(laplacian, 'gray'),plt.title('Laplacian'),plt.axis('off')
    plt.subplot(334),plt.imshow(canny20, 'gray'),plt.title('Canny(Thresh1=20)'),plt.axis('off')
    plt.subplot(335),plt.imshow(canny40, 'gray'),plt.title('Canny(Thresh1=40)'),plt.axis('off')
    plt.subplot(336),plt.imshow(canny80, 'gray'),plt.title('Canny(Thresh1=80)'),plt.axis('off')
    plt.subplot(337),plt.imshow(canny100, 'gray'),plt.title('Canny(Thresh1=100)'),plt.axis('off')
    plt.show(block=True)
    '''

def match_histogram(src_img, ref_img):

    print("Split the img to manipulate 1 color at a time")
    src_b,src_g,src_r = cv2.split(src_img)
    ref_b,ref_g,ref_r = cv2.split(ref_img)

    print("calculate each b,g,r histogram ")
    src_blue_hist, bins = np.histogram(src_b.flatten(), 256, [0,256])
    src_green_hist, bins2 = np.histogram(src_g.flatten(), 256, [0,256])
    src_red_hist, bins3 = np.histogram(src_r.flatten(), 256, [0,256])    

    ref_blue_hist, bins4 = np.histogram(ref_b.flatten(), 256, [0,256])    
    ref_green_hist, bins5 = np.histogram(ref_g.flatten(), 256, [0,256])
    ref_red_hist, bins6 = np.histogram(ref_r.flatten(), 256, [0,256])

    print("Calculate (normalized) CDF for each image")
    src_blue_cdf = src_blue_hist.cumsum()
    src_blue_cdf = src_blue_cdf / float(src_blue_cdf.max())
    src_green_cdf = src_green_hist.cumsum()
    src_green_cdf = src_green_cdf / float(src_green_cdf.max())
    src_red_cdf = src_red_hist.cumsum()
    src_red_cdf = src_red_cdf / float(src_red_cdf.max())

    ref_blue_cdf = ref_blue_hist.cumsum()
    ref_blue_cdf = ref_blue_cdf / float(ref_blue_cdf.max())
    ref_green_cdf = ref_green_hist.cumsum()
    ref_green_cdf = ref_green_cdf / float(ref_green_cdf.max())
    ref_red_cdf = ref_red_hist.cumsum()
    ref_red_cdf = ref_red_cdf / float(ref_red_cdf.max())

    print("Create a lookup table for each color")
    blue_lookup_table = np.zeros(256)
    tmp_lookup_value = 0
    for srcPixelValue in range(len(src_blue_cdf)):
        tmp_lookup_value
        for refPixelValue in range(len(ref_blue_cdf)):
            if ref_blue_cdf[refPixelValue] >= src_blue_cdf[srcPixelValue]:
                tmp_lookup_value = refPixelValue
                break
        blue_lookup_table[srcPixelValue] = tmp_lookup_value

    green_lookup_table = np.zeros(256)
    tmp_lookup_value = 0
    for srcPixelValue in range(len(src_green_cdf)):
        tmp_lookup_value = 0
        for refPixelValue in range(len(ref_green_cdf)):
            if ref_green_cdf[refPixelValue] >= src_green_cdf[srcPixelValue]:
                tmp_lookup_value = refPixelValue
                break
        green_lookup_table[srcPixelValue] = tmp_lookup_value

    red_lookup_table = np.zeros(256)
    tmp_lookup_value = 0
    for srcPixelValue in range(len(src_red_cdf)):
        tmp_lookup_value = 0
        for refPixelValue in range(len(ref_red_cdf)):
            if ref_red_cdf[refPixelValue] >= src_red_cdf[srcPixelValue]:
                tmp_lookup_value = refPixelValue
                break
        red_lookup_table[srcPixelValue] = tmp_lookup_value

    print("Transform the original colors by the lookup function")
    transformed_blue = cv2.LUT(src_b, blue_lookup_table)
    transformed_green = cv2.LUT(src_g, green_lookup_table)
    transformed_red = cv2.LUT(src_r, red_lookup_table)

    print("Compare (graph?) Normalized histograms or CDF's to see the matching")
    transformed_blue_hist, bin = np.histogram(transformed_blue.flatten(), 256, [0,256])
    transformed_green_hist, bin = np.histogram(transformed_green.flatten(), 256, [0,256])
    transformed_red_hist, bin = np.histogram(transformed_red.flatten(), 256, [0,256])

    transformed_blue_hist = transformed_blue_hist / float(src_img.shape[0] * src_img.shape[1])
    transformed_blue_cdf = transformed_blue_hist.cumsum()
    transformed_blue_cdf = transformed_blue_cdf / float(transformed_blue_cdf.max())

    transformed_green_hist = transformed_green_hist / float(src_img.shape[0] * src_img.shape[1])
    transformed_green_cdf = transformed_green_hist.cumsum()
    transformed_green_cdf = transformed_green_cdf / float(transformed_green_cdf.max())

    transformed_red_hist = transformed_red_hist / float(src_img.shape[0] * src_img.shape[1])
    transformed_red_cdf = transformed_red_hist.cumsum()
    transformed_red_cdf = transformed_red_cdf / float(transformed_red_cdf.max())

    print("recombine/return the image")
    transformed_img = cv2.merge([transformed_blue, transformed_green, transformed_red])
    transformed_img = cv2.convertScaleAbs(transformed_img)
    return transformed_img

def mask_image(img, mask):
    print("splitting the colors")
    color1, color2, color3 = cv2.split(img)

    print("Resizing mask to fit image")
    scaled_mask = cv2.resize(mask, (img.shape[1], img.shape[0]), cv2.INTER_NEAREST)
    print("Img Dimensions: {0} by {1} vs. mask dimensions {2} by {3}".format(
        img.shape[0], img.shape[1], scaled_mask.shape[0], scaled_mask.shape[1])) 

    print("Normalizing the mask")
    normalized_scaled_mask = scaled_mask / float(255)

    print("Scale/mask color values")
    color1 = color1 * normalized_scaled_mask
    color1 = color1.astype(int)
    color2 = color2 * normalized_scaled_mask
    color2 = color2.astype(int)
    color3 = color3 * normalized_scaled_mask
    color3 = color3.astype(int)

    print("Recombine/return the image")
    merge = cv2.merge([color1, color2, color3])
    final_img = cv2.convertScaleAbs(merge)
    return final_img


    #OUTPUT USING MATPLOTLIB!


if __name__ == "__main__":
        main()
