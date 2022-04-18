import cv2
import numpy as np
import os


#test image 0_1 and 0_2 are made with the assumptions from volume_estimation0.py


def create_test_image0_1():
    im = np.full((512,512,3), 255, np.uint8)
    im = cv2.ellipse(im, (220, 100), (100, 50), 0, 0, 360, (0, 0, 0), -1)

    im = cv2.ellipse(im, (220, 300), (40, 27), 0, 0, 360, (0, 0, 0), -1)
    return im

def create_test_image0_2():
    im = np.full((512,512,3), 255, np.uint8)
    im = cv2.ellipse(im, (420, 100), (30, 50), 0, 0, 360, (0, 0, 0), -1)

    im = cv2.ellipse(im, (150, 300), (100, 30), 0, 0, 360, (0, 0, 0), -1)
    return im

if __name__ == '__main__':

    im1 = create_test_image0_1()
    im2 = create_test_image0_2()
    cv2.imshow('im1', im1)
    cv2.imshow('im2', im2)
    cv2.waitKey(0)
    cv2.imwrite('test_image0_1.png', im1)
    cv2.imwrite('test_image0_2.png', im2)
    cv2.destroyAllWindows()
    print()
