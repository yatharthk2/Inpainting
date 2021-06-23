import numpy as np
import cv2 as cv
import sys
#import os
#from PIL import Image
#python manual-mask.py D:\trash\mountain.jpg

# OpenCV Utility Class for Mouse Handling
class Sketcher:
    def __init__(self, windowname, dests, colors_func):
        self.prev_pt = None
        self.windowname = windowname
        self.dests = dests
        self.colors_func = colors_func
        self.dirty = False
        self.show()
        cv.setMouseCallback(self.windowname, self.on_mouse)

    def show(self):
        cv.imshow(self.windowname, self.dests[0])
        cv.imshow(self.windowname + ": mask", self.dests[1])

    # onMouse function for Mouse Handling
    def on_mouse(self, event, x, y, flags, param):
        pt = (x, y)
        if event == cv.EVENT_LBUTTONDOWN:
            self.prev_pt = pt
        elif event == cv.EVENT_LBUTTONUP:
            self.prev_pt = None

        if self.prev_pt and flags & cv.EVENT_FLAG_LBUTTON:
            for dst, color in zip(self.dests, self.colors_func()):
                cv.line(dst, self.prev_pt, pt, color, 5)
            self.dirty = True
            self.prev_pt = pt
            self.show()


def main():

    print("Usage: python manual-mask <image_path>")
    print("Keys: ")
    print("t - inpaint using FMM")
    print("n - inpaint using NS technique")
    print("r - reset the inpainting mask")
    print("ESC - exit")

    # Read image in color mode
    img = cv.imread(sys.argv[1], cv.IMREAD_COLOR)

    # If image is not read properly, return error
    if img is None:
        print('Failed to load image file: {}'.format(args["image"]))
        return

    # Create a copy of original image
    img_mask = img.copy()
    # Create a black copy of original image
    # Acts as a mask
    inpaintMask = np.zeros(img.shape[:2], np.uint8)
    # Create sketch using OpenCV Utility Class: Sketcher
    sketch = Sketcher('image', [img_mask, inpaintMask], lambda : ((255, 255, 255), 255))
    

    #img = sketch
    #img = img.save("sketch.jpeg")

    while True:
        ch = cv.waitKey()
        if ch == 27:
            break
        if ch == ord('t'):
            # Use Algorithm proposed by Alexendra Telea: Fast Marching Method (2004)
            # Reference: https://pdfs.semanticscholar.org/622d/5f432e515da69f8f220fb92b17c8426d0427.pdf
            res = cv.inpaint(src=img_mask, inpaintMask=inpaintMask, inpaintRadius=3, flags=cv.INPAINT_TELEA)
            cv.imshow('Inpaint Output using FMM', res)
        if ch == ord('n'):
            # Use Algorithm proposed by Bertalmio, Marcelo, Andrea L. Bertozzi, and Guillermo Sapiro: Navier-Stokes, Fluid Dynamics, and Image and Video Inpainting (2001)
            res = cv.inpaint(src=img_mask, inpaintMask=inpaintMask, inpaintRadius=3, flags=cv.INPAINT_NS)
            cv.imshow('Inpaint Output using NS Technique', res)
        if ch == ord('r'):
            img_mask[:] = img
            inpaintMask[:] = 0
            sketch.show()

        if ch == ord('s'):
            #img_mask = str(img_mask)
            #img = cv.imread(img_mask)
            filename1 = 'C:/Users/yatha/OneDrive/Desktop/projects/Inpainting_project/data/val_large/Mask_Image.jpg'
            #filename2 = 'C:/Users/yatha/OneDrive/Desktop/projects/Inpainting_project/data/mask_root/Inpaint_Image.jpg'
            filename3 = 'C:/Users/yatha/OneDrive/Desktop/projects/Inpainting_project/data/mask_root/Inverted_Inpaint_Image.jpg'
            cv.imwrite(filename1, img)
            #cv.imwrite(filename2, inpaintMask)
            cv.imwrite(filename3, (cv.bitwise_not(inpaintMask)))

        
    print('Completed')


if __name__ == '__main__':
    main()
    cv.destroyAllWindows()