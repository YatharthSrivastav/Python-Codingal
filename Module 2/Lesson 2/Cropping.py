import cv2 as cv
import matplotlib.pyplot as plt

img = cv.imread('Module 2\\Lesson 2\\Image.jpg')

img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
plt.imshow(img_rgb)
plt.title("RGB Image")
plt.show()

img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
plt.imshow(img_gray)
plt.title("Gray Image")
plt.show()

crpd_img = img[100:300, 200:400]
plt.imshow(crpd_img)
plt.title("Cropped Image")
plt.show()