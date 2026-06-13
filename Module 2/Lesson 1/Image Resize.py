import cv2 as cv

img = cv.imread("Module 2\\Lesson 1\\Image.jpg")
cv.namedWindow("Loaded Image", cv.WINDOW_NORMAL)
cv.resizeWindow("Loaded Image", 800, 800)


cv.imshow("Loaded Image", img)

cv.waitKey(0)
cv.destroyAllWindows()

print(f"Image Dimensions {img.shape}")

