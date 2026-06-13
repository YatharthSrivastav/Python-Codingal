import cv2 as cv

img = cv.imread("Module 2\\Lesson 1\\Image.jpg")
gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img_resize = cv.resize(gray_img, (800, 800))


cv.imshow("Loaded Image", img_resize)

key = cv.waitKey(0) & 0xFF

if key == ord ('s'):
    cv.imwrite("Grayscale.jpg",img_resize)
    print("Image has been saved as 'Grayscale.jpg'")
else:
    print("Error, image not saved")


cv.destroyAllWindows()

print(f"Image Dimensions {img.shape}")

