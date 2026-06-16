import cv2 as cv
import matplotlib.pyplot as plt

img_path = 'Module 2\\Lesson 3\\Sun.jpg'
img = cv.imread(img_path)
img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

h, w, _ = img_rgb.shape

rect1_width, rect1_height = 150, 150
top_left1 = (20, 20)
bottom_right1 = (top_left1[0] + rect1_width, top_left1[1] + rect1_height)
cv.rectangle(img_rgb, top_left1, bottom_right1, (0, 255, 255), 3)

rect2_width, rect2_height = 200, 150
top_left2 = (w - rect2_width - 20, h - rect2_height - 20)
bottom_right2 = (top_left2[0] + rect2_width, top_left2[1] + rect2_height)
cv.rectangle(img_rgb, top_left2, bottom_right2, (0, 255, 255), 3)

center1_x = top_left1[0] + rect1_width // 2
center1_y = top_left1[1] + rect1_height // 2
center2_x = top_left2[0] + rect2_width // 2
center2_y = top_left2[1] + rect2_height // 2
cv.circle(img_rgb, (center1_x, center1_y), 15, (0, 255, 0), -1)
cv.circle(img_rgb, (center2_x, center2_y), 15, (0, 255, 0), -1)

font = cv.FONT_HERSHEY_SIMPLEX
cv.putText(img_rgb, 'Region 1', (top_left1[0], top_left1[1] - 10), font, 0.7, (0, 0, 0), 2, cv.LINE_AA)
cv.putText(img_rgb, 'Region 2', (top_left2[0], top_left2[1] - 10), font, 0.7, (0, 0, 0), 2, cv.LINE_AA)
cv.putText(img_rgb, 'Center 1', (center1_x - 40, center1_y + 40), font, 0.6, (0, 255, 0), 2, cv.LINE_AA)
cv.putText(img_rgb, 'Center 2', (center2_x - 40, center2_y + 40), font, 0.6, (0, 255, 0), 2, cv.LINE_AA)

arrow_start = (w -50, 20)
arrow_end = (w - 50, h - 20)
cv.arrowedLine(img_rgb, arrow_start,arrow_end, (255, 255, 0), 3, tipLength= 0.05)
cv.arrowedLine(img_rgb, arrow_end,arrow_start, (255, 255, 0), 3, tipLength= 0.05)

plt.figure(figsize = (30, 20))
plt.imshow(img_rgb)
plt.title("Annoted Image")
plt.show()

