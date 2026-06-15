import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

img = cv.imread('Module 2\\Lesson 2\\Image.jpg')
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
plt.imshow(img_gray, cmap = 'gray')
plt.title("Grayscale Image")
plt.show()

img_crpd = img[100:300, 200:400]
crpd_rgb = cv.cvtColor(img_crpd, cv.COLOR_BGR2RGB)
plt.imshow(crpd_rgb)
plt.title("Cropped Image")
plt.show()

(h, w) = img.shape[:2]
center = (w//2, h//2)
m = cv.getRotationMatrix2D(center, 145, 0.5)
rotate = cv.warpAffine(img, m, (w, h))
rotate_rgb = cv.cvtColor(rotate, cv.COLOR_BGR2RGB)
plt.imshow(rotate_rgb)
plt.title("Rotated Image")
plt.show()

brightness = np.ones(img.shape, dtype = 'uint8') * 100
brighter = cv.add(img, brightness)
bright_rgb = cv.cvtColor(brighter, cv.COLOR_BGR2RGB)
plt.imshow(bright_rgb)
plt.title("Brighter Image")
plt.show()

cv.imwrite("Grayscale Image.jpg", img_gray)
cv.imwrite("Cropped Image.jpg", crpd_rgb)
cv.imwrite("Rotated Image.jpg", rotate_rgb)
cv.imwrite("Brighter Image.jpg", bright_rgb)