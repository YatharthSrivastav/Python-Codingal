import cv2 as cv

img = cv.imread("Module 2\\Lesson 1\\Image.jpg")
small_img = cv.resize(img , (200, 200))
mid_img = cv.resize(img , (400, 400))
large_img = cv.resize(img , (600, 600))

cv.imshow("Small Image", small_img)
cv.imshow("Medium Image", mid_img)
cv.imshow("Large Image", large_img)

key = cv.waitKey(0) & 0xFF

if key == ord ('s'):
    cv.imwrite("Small Image.jpg",small_img)
    print("Image has been saved as 'Small Image.jpg'")

    cv.imwrite("Medium Image.jpg",mid_img)
    print("Image has been saved as 'Medium Image.jpg'")

    cv.imwrite("Large Image.jpg",large_img)
    print("Image has been saved as 'Large Image.jpg'")

else:
    print("Error, image not saved")

cv.destroyAllWindows()

