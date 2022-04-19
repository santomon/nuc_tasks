"""
volume estimation from 2 orthogonal images:

v1 assumptions:

"good" thresholds,
shapes are ellipsoids, i.e. volume = 1 / 2 * a * b * c (roughly; should be pi / 6 abc)
no rotation, i.e. axes are parallel to x and y,
no shear, i.e. axes are orthogonal,

no overlaps of shapes

shapes at different heights
"""

import cv2
import numpy
# import pydicom
import argparse #


def create_parser():
    """
    returns parser object,
    arguments are image 1 as im1, image 2 as im2, threshold with default value of 200,
    and a millimeter to pixel ratio with default value of 1,
    currently the dataformat for the images is expected to be png or jpeg,
    optional draw contours parameter
    """
    parser = argparse.ArgumentParser(description='Volume estimation from 2 orthogonal images')
    parser.add_argument('--im1', help='image 1')
    parser.add_argument('--im2', help='image 2')
    parser.add_argument('-t', '--threshold', default=200, type=float, help='threshold value')
    parser.add_argument('-m', '--ratio', default=1, type=float, help='millimeter to pixel ratio')
    parser.add_argument('-d', '--draw', action='store_true', help='draw contours')
    return parser


def make_contour(image, threshold):
    """
    returns contour of image with threshold
    """
    # threshold image
    ret, thresh = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    # find contours
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # discard a contour, if the first point is (0, 0)
    # because the contouring might create one spanning the whole image
    contours = [contour for contour in contours if contour[0][0][0] != 0 and contour[0][0][1] != 0]
    return contours, hierarchy


def estimate_volume(contour, width, ratio):
    """
    returns volume of contour
    the main contour will be from the sagital image; width estimation should be done from frontal image

    ratio is the mm/pixel ratio
    """
    area = cv2.contourArea(contour)
    volume = ratio**3 * area * width * 2 / 3 # 2 / 3 is correction factor for estimating elipsoid volume using elipse area
    return volume

def get_width(contour):
    """
    returns width of contour
    """
    x, y, w, h = cv2.boundingRect(contour)
    return w

# we can now compute volumes... last remaining question is, how do we match contours together?
# IDEA 1: sort by height of the contour and match accordingly; assuming that we have the same number of contours
# which should be the case, since we make the assumption that there are no overlaps...

def rearrange_contours(contours):
    """
    returns contours sorted by height
    """
    contours_sorted = sorted(contours, key=lambda x: cv2.boundingRect(x)[1])  # AI CODING FTW
    return contours_sorted

def main(args):

    # read images
    im1 = cv2.imread(args.im1)
    im2 = cv2.imread(args.im2)
    imgray1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    imgray2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

    # make contours
    contours1, hierarchy1 = make_contour(imgray1, args.threshold)
    contours2, hierarchy2 = make_contour(imgray2, args.threshold)
    # rearrange contours
    contours1 = rearrange_contours(contours1)
    contours2 = rearrange_contours(contours2)

    if args.draw:
        # draw contours
        preview1 = cv2.drawContours(im1, contours1, -1, (255, 0, 0), 3)
        preview2 = cv2.drawContours(im2, contours2, -1, (255, 0, 0), 3)
        cv2.imshow(f"previewing contours for {args.im1}", preview1)
        cv2.imshow(f"previewing contours for {args.im2}", preview2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # estimate width
    widths = [get_width(contour) for contour in contours2]
    # estimate volume
    volumes = [estimate_volume(contour, w, args.ratio) for contour, w in zip(contours1, widths)]

    # estimate volume
    # print volume
    print(volumes)



if __name__ == '__main__':

    # parse arguments
    parser = create_parser()
    args = parser.parse_args()

    main(args)