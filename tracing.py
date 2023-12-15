import numpy as np
import cv2
import json
from imutils import resize
from imutils.contours import sort_contours
from scipy import signal
from skimage.morphology import skeletonize as skl
from StrokestoNPY import handle_draw_data


path = 'gates.png'
img = cv2.imread(path, 0)
# Some smoothing to get rid of the noise
# img = cv2.bilateralFilter(img, 5, 35, 10)
img = cv2.GaussianBlur(img, (3, 3), 3)
img = resize(img, width=1000)

# Preprocessing to get the shapes
th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                           cv2.THRESH_BINARY, 35, 11)
# Invert to hightligth the shape
th = cv2.bitwise_not(th)

# Text has mostly vertical and right-inclined lines. This kernel seems to
# work quite well
kernel = np.array([[0, 1, 1],
                  [0, 1, 0],
                  [1, 1, 0]], dtype='uint8')

th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel)

cv2.imshow('mask', th)
cv2.waitKey(0)


#def contour_sorter(contours):
#    '''Sort the contours by multiplying the y-coordinate and sorting first by
#    x, then by y-coordinate.'''
#    boxes = [cv2.boundingRect(c) for c in contours]
#    cnt = [4*y, x for y, x, , _, _ in ]

# Skeletonize the shapes
# Skimage function takes image with either True, False or 0,1
# and returns and image with values 0, 1.
th = th == 255
th = skl(th)
th = th.astype(np.uint8)*255

# Find contours of the skeletons
contours, _ = cv2.findContours(th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(type(contours), "Length:", len(contours), "First element type:", type(contours[0]), "Sample data:", contours[:1])

# Sort the contours left-to-rigth
contours, _ = sort_contours(contours, )
#
# Sort them again top-to-bottom
import json

def convert_traces(contours):
    strokes = []

    for contour in contours:
        # Extract x and y coordinates, converting them to standard Python integers
        x_coords = [int(point[0][0]) for point in contour]
        y_coords = [int(point[0][1]) for point in contour]

        # Append the formatted stroke to the strokes list
        strokes.append({"x": x_coords, "y": y_coords})

    # Return the strokes list directly, not as a string
    return strokes


converted_format = convert_traces(contours)
print(converted_format)


def skeleton_endpoints(skel):
    # Function source: https://stackoverflow.com/questions/26537313/
    # how-can-i-find-endpoints-of-binary-skeleton-image-in-opencv
    # make out input nice, possibly necessary
    skel = skel.copy()
    skel[skel != 0] = 1
    skel = np.uint8(skel)

    # apply the convolution
    kernel = np.uint8([[1,  1, 1],
                       [1, 10, 1],
                       [1,  1, 1]])
    src_depth = -1
    filtered = cv2.filter2D(skel, src_depth,kernel)

    # now look through to find the value of 11
    # this returns a mask of the endpoints, but if you just want the
    # coordinates, you could simply return np.where(filtered==11)
    out = np.zeros_like(skel)
    out[np.where(filtered == 11)] = 1
    rows, cols = np.where(filtered == 11)
    coords = list(zip(cols, rows))
    return coords

# List for endpoints
endpoints = []
# List for (x, y) coordinates of the skeletons
skeletons = []

for contour in contours:
    if cv2.arcLength(contour, True) > 100:
        # Initialize mask
        mask = np.zeros(img.shape, np.uint8)
        # Bounding rect of the contour
        x, y, w, h = cv2.boundingRect(contour)
        mask[y:y+h, x:x+w] = 255
        # Get only the skeleton in the mask area
        mask = cv2.bitwise_and(mask, th)
        # Take the coordinates of the skeleton points
        rows, cols = np.where(mask == 255)
        # Add the coordinates to the list
        skeletons.append(list(zip(cols, rows)))

        # Find the endpoints for the shape and update a list
        eps = skeleton_endpoints(mask)
        endpoints.append(eps)

        # Draw the endpoints
        [cv2.circle(th, ep, 5, 255, 1) for ep in eps]
        cv2.imshow('mask', mask)
        cv2.waitKey(500)

# Stack the original and modified
th = resize(np.hstack((img, th)), 1200)


#    cv2.waitKey(50)


cv2.imshow('mask', th)
cv2.waitKey(0)
cv2.destroyAllWindows()

#print(type(contours), "Length:", len(contours), "First element type:", type(contours[0]), "Sample data:", contours[:1])

input_string = "zero- emission"

decimated_format = []
for item in converted_format:
    decimated_x = signal.decimate(item['x'], 3)
    decimated_y = signal.decimate(item['y'], 3)
    decimated_format.append({'x': decimated_x, 'y': decimated_y})

handle_draw_data(decimated_format, input_string)