import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os

# Display a single image
def display_image(title, image):
    plt.figure(figsize=(8, 8))
    if len(image.shape) == 2:
        plt.imshow(image, cmap='gray')
    else:
        plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.show()

# Display two images side by side
def display_side_by_side(title1, image1, title2, image2):
    fig, axes = plt.subplots(1, 2, figsize=(15, 7))
    
    if len(image1.shape) == 2:
        axes[0].imshow(image1, cmap='gray')
    else:
        axes[0].imshow(cv.cvtColor(image1, cv.COLOR_BGR2RGB))
    axes[0].set_title(title1)
    axes[0].axis('off')
    
    if len(image2.shape) == 2:
        axes[1].imshow(image2, cmap='gray')
    else:
        axes[1].imshow(cv.cvtColor(image2, cv.COLOR_BGR2RGB))
    axes[1].set_title(title2)
    axes[1].axis('off')
    
    plt.show()

# Load image from images folder
def load_image():
    images_folder = 'Module 2\\Lesson 4\\Images'
    
    if not os.path.exists(images_folder):
        print(f"Error: '{images_folder}' folder does not exist!")
        return None
    
    image_files = [f for f in os.listdir(images_folder) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    
    if not image_files:
        print(f"Error: No images found in {images_folder}")
        return None
    
    print("\nAvailable Images:")
    for i, img in enumerate(image_files, 1):
        print(f"{i}. {img}")
    
    while True:
        choice = input("\nEnter the number of the image you want: ")
        if choice.isdigit() and 1 <= int(choice) <= len(image_files):
            image_path = os.path.join(images_folder, image_files[int(choice) - 1])
            image = cv.imread(image_path)
            if image is not None:
                print(f"Loaded: {image_files[int(choice) - 1]}")
                return image
            else:
                print("Error loading image!")
        else:
            print(f"Please enter a number between 1 and {len(image_files)}")

# Save the processed image
def save_image(image):
    filename = input("Enter filename to save (e.g., result.jpg): ")
    output_path = f'Module 2\\Lesson 4\\Images\\{filename}'
    cv.imwrite(output_path, image)
    print(f"Image saved: {output_path}")

# Main edge detection function
def edge_detection():
    image = load_image()
    if image is None:
        print("Cannot proceed without an image!")
        return
    
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    display_image("Original Image", image)
    display_image("Grayscale Image", gray_image)

    last_image = gray_image.copy()  # Store for undo

    while True:
        print("\n=== Edge Detection & Filtering Menu ===")
        print("1. Sobel Edge Detection")
        print("2. Canny Edge Detection")
        print("3. Laplacian Edge Detection")
        print("4. Gaussian Smoothing")
        print("5. Median Filtering")
        print("6. Save Image")
        print("7. Reset")
        print("8. Undo")
        print("9. Exit")
        print("========================================")

        choice = input("Enter your choice (1-9): ")

        if choice == '1':
            sobel_x = cv.Sobel(gray_image, cv.CV_64F, 1, 0, ksize=3)
            sobel_y = cv.Sobel(gray_image, cv.CV_64F, 0, 1, ksize=3)
            sobel_combined = cv.bitwise_or(sobel_x.astype(np.uint8), sobel_y.astype(np.uint8))
            last_image = gray_image.copy()
            display_side_by_side("Original Grayscale", gray_image, "Sobel Detection", sobel_combined)

        elif choice == '2':
            print("Canny Edge Detection")
            lower = int(input("Enter lower threshold (default 100): ") or "100")
            upper = int(input("Enter upper threshold (default 200): ") or "200")
            edges = cv.Canny(gray_image, lower, upper)
            last_image = gray_image.copy()
            display_side_by_side("Original Grayscale", gray_image, "Canny Detection", edges)
        
        elif choice == '3':
            laplacian = cv.Laplacian(gray_image, cv.CV_64F)
            laplacian_display = np.abs(laplacian).astype(np.uint8)
            last_image = gray_image.copy()
            display_side_by_side("Original Grayscale", gray_image, "Laplacian Detection", laplacian_display)
        
        elif choice == '4':
            size = int(input("Enter kernel size - must be odd (default 5): ") or "5")
            if size % 2 == 0:
                size += 1
            blurred = cv.GaussianBlur(image, (size, size), 0)
            last_image = image.copy()
            display_side_by_side("Original Image", image, "Gaussian Blur", blurred)

        elif choice == '5':
            size = int(input("Enter kernel size - must be odd (default 5): ") or "5")
            if size % 2 == 0:
                size += 1
            median = cv.medianBlur(image, size)
            last_image = image.copy()
            display_side_by_side("Original Image", image, "Median Filter", median)

        elif choice == '6':
            save_image(gray_image)

        elif choice == '7':
            gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            print("Reset! Back to original image.")
            display_image("Original Image", image)

        elif choice == '8':
            gray_image = last_image.copy()
            print("Undo! Back to previous state.")
            display_image("Image", gray_image)

        elif choice == '9':
            print("See you! Goodbye!")
            break

        else:
            print("Invalid choice! Please enter a number between 1 and 9.")

# Run the program
edge_detection()
