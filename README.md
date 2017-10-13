# image_processing_p3
Histogram Matching + Masking
- Brandon Tarney
- 10/5/2017

## Program Overview:
- Description:
    - Given a reference image and a target image, histogram-match the reference image to the target image
        - Sizes of the images don't have to be the same
    - Given an optional third image as a mask, mask the output image
        - Typically the mask will be a gausian mask

## How to Run:
- python2 hist_match src_img_path ref_img_path [mask_img_path]
- Expect to see the input image and reference image displayed followed by the histogram matched image and the final image with the mask applied (if that input was provided)
- Press 'esc' to move forward from an image and press 's' to save the final image
