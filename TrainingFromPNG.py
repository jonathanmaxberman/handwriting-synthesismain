#import cv2
import numpy as np
import cv2
#from google.colab.patches import cv2_imshow
from StrokestoNPY import handle_draw_data
def simplify_contour(contour, epsilon=0.5):  # Adjust the epsilon for simplification
    return cv2.approxPolyDP(contour, epsilon, True)

# Load and process the image
img = cv2.imread('spock.png')
resized_img = cv2.resize(img, (500, 50))
gray_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
thresh_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY_INV)[1]  # Adjust thresholding if necessary

# Find contours
contours, _ = cv2.findContours(thresh_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

# Draw original contours for comparison (in red)
cv2.drawContours(resized_img, contours, -1, (0, 0, 255), 1)

strokes = []
penup = 1


for cnt in contours:
    simplified_cnt = simplify_contour(cnt, epsilon=0.1)
    cv2.drawContours(resized_img, [simplified_cnt], -1, (255, 0, 0), 1)  # Blue color in BGR
    for i, point in enumerate(simplified_cnt):
        x_point, y_point = point.ravel()  # Use ravel() to flatten the array
        strokes.append((x_point, y_point, penup))  # Append a tuple with x, y, penup
        penup = 0  # Pen is down

    # Mark the end of a contour with a pen-up
    if strokes:
        strokes[-1] = (strokes[-1][0], strokes[-1][1], 1)
    penup = 1  # Next contour starts with pen-up

# Convert to numpy array
#strokes_array = np.array(strokes, dtype=[('x', 'float32'), ('y', 'float32'), ('penup', 'int')])

# Show the image with original and simplified contours
#cv2_imshow(resized_img)
cv2.imshow('Image', resized_img)  # 'Image' is the window title
cv2.waitKey(0)  # Waits indefinitely for a key press
cv2.destroyAllWindows()
input_string = "to be able to do"
#byte_stream = np.frombuffer(input_string.encode('utf-8'), dtype=np.uint8)

print(strokes)
# Initialize lists for X and Y values
x_values = []
y_values = []

# Initialize a list to store the final formatted data
formatted_data = []

# Iterate through your original data
for item in strokes:
    x_value, y_value, pen_down = item
    if pen_down == 1:
        # If pen_down is 1, it marks the start of a new stroke
        # Append the previous stroke (X and Y values) to the formatted_data list
        if x_values:
            formatted_data.append({"x": x_values, "y": y_values})
        # Reset X and Y lists for the new stroke
        x_values = []
        y_values = []
    # Append the X and Y values to their respective lists
    x_values.append(x_value)
    y_values.append(y_value)

# Append the last stroke, if any
if x_values:
    formatted_data.append({"x": x_values, "y": y_values})

# The formatted_data list now contains the data in the desired format
print(formatted_data)
# The formatted_data list now contains the data in the desired JSON format
print(formatted_data)

handle_draw_data(formatted_data,input_string)




# Save the numpy array
#np.save('./styles/style-16-strokes.npy', strokes_array)
#np.save('./styles/style-16-chars.npy', byte_stream)