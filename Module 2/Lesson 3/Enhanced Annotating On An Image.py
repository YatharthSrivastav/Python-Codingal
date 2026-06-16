import os
import cv2 as cv
import matplotlib.pyplot as plt

img_path = os.path.join('Module 2', 'Lesson 3', 'Sun.jpg')
img = cv.imread(img_path)
img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

h, w, _ = img_rgb.shape
y = h // 2
margin = 20
start_left = (margin, y)
end_right = (w - margin, y)
color = (255, 0, 0)
thickness = 4
cv.arrowedLine(img_rgb, start_left, end_right, color, thickness, tipLength=0.05)
cv.arrowedLine(img_rgb, end_right, start_left, color, thickness, tipLength=0.05)

mid_x = w // 2
text = f"Width: {w}px"
font = cv.FONT_HERSHEY_SIMPLEX
text_scale = 1.2
text_thickness = 3
(text_w, text_h), baseline = cv.getTextSize(text, font, text_scale, text_thickness)
text_x = mid_x - text_w // 2
text_y = y - 25
cv.putText(img_rgb, text, (text_x, text_y), font, text_scale, (0, 0, 0), text_thickness + 2, cv.LINE_AA)
cv.putText(img_rgb, text, (text_x, text_y), font, text_scale, (255, 255, 255), text_thickness, cv.LINE_AA)

output_dir = os.path.join('Module 2', 'Lesson 3', 'Output Images')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'Image Annotated.jpg')
bgr_out = cv.cvtColor(img_rgb, cv.COLOR_RGB2BGR)
cv.imwrite(output_path, bgr_out)

plt.figure(figsize=(12, 8))
plt.imshow(img_rgb)
plt.axis('off')
plt.title('Image Width Annotation')
plt.show()
