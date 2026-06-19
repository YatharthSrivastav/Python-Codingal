import cv2 as cv
import numpy as np

def color_filter(image, filter_type):
    filtered_image = image.copy()
    if filter_type == 'red':
        filtered_image[:, :, 1] = 0
        filtered_image[:, :, 0] = 0
    
    elif filter_type == 'blue':
        filtered_image[:, :, 1] = 0
        filtered_image[:, :, 2] = 0

    elif filter_type == 'green':
        filtered_image[:, :, 0] = 0
        filtered_image[:, :, 2] = 0

    elif filter_type == 'increase red':
        filtered_image[:, :, 2] = cv.add(filtered_image[:, :, 2], 50)

    elif filter_type == 'increase blue':
        filtered_image[:, :, 0] = cv.add(filtered_image[:, :, 0], 50)
    return filtered_image

image_path = 'Module 2\\Lesson 5\\Sun Flower.jpg'
image = cv.imread(image_path)

if image is None:
    print("Image is not found")
else:
    filter_type = 'original'
    print("Type the following letters to apply a filter:")
    print("r - Red Tint")
    print("b - Blue Tint")
    print("g - Green Tint")
    print("i - Increase Red Tint")
    print("c - Increase Blue Tint")
    print("q - Quit")

    while True:
        filtered_image = color_filter(image, filter_type)
        cv.imshow("Filtered Image", filtered_image)
        key = cv.waitKey(0) & 0xFF

        if key == ord('r'):
            filter_type = 'red'

        elif key == ord('b'):
            filter_type = 'blue'

        elif key == ord('g'):
            filter_type = 'green'

        elif key == ord('i'):
            filter_type = 'increase red'

        elif key == ord('c'):
            filter_type = 'increase blue'
        
        elif key == ord('q'):
            print("THank You!")
            break

        else:
            print("Invalid! Please use the keys mentioned above")

cv.destroyAllWindows()