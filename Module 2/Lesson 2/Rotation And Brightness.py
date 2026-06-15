import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

img = cv.imread('Module 2\\Lesson 2\\Image.jpg')
img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

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

