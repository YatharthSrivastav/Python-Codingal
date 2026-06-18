import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def display_image(title, image):
    plt.figure(figsize= (8, 8))
    if len(image.shape) == 2:
        plt.imshow(image, cmap= 'gray')
    else:
        plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.show()

def edge_detection(image_path):
    image = cv.imread(image_path)
    if image is None:
        print("Error Image Is Not Found")
        return
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    display_image("Original Grayscale Image", gray_image)

    print("Select an option:")
    print("1. Sobel Detection")
    print("2. Canny Edge Detection")
    print("3. Laplacian Edge Detection")
    print("4. Gaussian Smoothening")
    print("5. Median Filtering")
    print("Exit\n")

    while True:
        choice = input("Enter a number between 1 to 6\n")

        if choice == '1':
            sobel_x = cv.Sobel(gray_image, cv.CV_64F, 1, 0, ksize = 3)
            sobel_y = cv.Sobel(gray_image, cv.CV_64F, 0, 1, ksize = 3)
            sobel_combined = cv.bitwise_or(sobel_x.astype(np.uint8), sobel_y.astype(np.uint8))
            display_image("Sobel Image Detection", sobel_combined)

        elif choice == '2':
            print("Adjust thresholds for Canny. Default is 100 - 200")
            lower_threshold = int(input("Enter the lower threshold: "))
            upper_threshold = int(input("Enter the upper threshold: "))
            edges = cv.Canny(gray_image, lower_threshold, upper_threshold)
            display_image("Canny Edge Detection", edges)
        
        elif choice == '3':
            laplacian = cv.Laplacian(gray_image, cv.CV_64F)
            display_image("Laplacian Edge Detection", np.abs(laplacian).astype(np.uint8))
        
        elif choice == '4':
            print("Adjust kernel size. Must be an odd number and the default size is 5")
            kernel_size = int(input("Enter the kernel size:  "))
            blurred = cv.GaussianBlur(image, (kernel_size, kernel_size), 0)
            display_image("Gaussian Smooth Image", blurred)

        elif choice == '5':
            print("Adjust the kernel size. Must be an add number and the default size is always 5")
            kernel_size = int(input("Enter the kernel size: "))
            median_filter = cv.medianBlur(image, kernel_size)
            display_image("Medain Filter Image", median_filter)

        elif choice == '6':
            print("See You! Bye!")
            break

        else:
            print("Please enter a valid choice from 1 to 6!")

edge_detection('Module 2\\Lesson 4\\Sun.jpg')
