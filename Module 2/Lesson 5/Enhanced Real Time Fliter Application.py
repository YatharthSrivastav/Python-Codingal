import cv2 as cv
import numpy as np
import os

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

    elif filter_type == 'increase green':
        filtered_image[:, :, 1] = cv.add(filtered_image[:, :, 1], 50)

    elif filter_type == 'decrease red':
        filtered_image[:, :, 2] = cv.subtract(filtered_image[:, :, 2], 50)

    elif filter_type == 'decrease blue':
        filtered_image[:, :, 0] = cv.subtract(filtered_image[:, :, 0], 50)

    elif filter_type == 'decrease green':
        filtered_image[:, :, 1] = cv.subtract(filtered_image[:, :, 1], 50)

    return filtered_image

def save_image(current_image):
    filename = input("Enter filename to save (e.g., result.jpg): ")
    output_path = f'Module 2\\Lesson 5\\{filename}'
    cv.imwrite(output_path, current_image)
    print(f"Image saved: {output_path}")

image_path = 'Module 2\\Lesson 5\\Sun Flower.jpg'
image = cv.imread(image_path)

if image is None:
    print("Image is not found")

else:
    current_image = image.copy()

    print("Type the following letters to apply a filter:")
    print("r - Red Tint")
    print("b - Blue Tint")
    print("g - Green Tint")
    print("1 - Increase Red Tint")
    print("2 - Increase Blue Tint")
    print("3 - Increase Green Tint")
    print("4 - Decrease Red Tint")
    print("5 - Decrease Blue Tint")
    print("6 - Decrease Green Tint")
    print("o - Original Image")
    print("s - To Save Your Image ")
    print("q - Quit")

    while True:
        cv.imshow("Filtered Image", current_image)
        key = cv.waitKey(0) & 0xFF

        if key == ord('r'):
            current_image = color_filter(current_image, 'red')

        elif key == ord('b'):
            current_image = color_filter(current_image, 'blue')

        elif key == ord('g'):
            current_image = color_filter(current_image, 'green')

        elif key == ord('1'):
            current_image = color_filter(current_image, 'increase red')

        elif key == ord('2'):
            current_image = color_filter(current_image, 'increase blue')

        elif key == ord('3'):
            current_image = color_filter(current_image, 'increase green')

        elif key == ord('4'):
            current_image = color_filter(current_image, 'decrease red')

        elif key == ord('5'):
            current_image = color_filter(current_image, 'decrease blue')

        elif key == ord('6'):
            current_image = color_filter(current_image, 'decrease green')

        elif key == ord('o'):
            current_image = image.copy()

        elif key == ord('s'):
            save_image(current_image)

        elif key == ord('q'):
            print("Thank You!")
            break

        else:
            print("Invalid! Please use the keys mentioned above")

cv.destroyAllWindows()