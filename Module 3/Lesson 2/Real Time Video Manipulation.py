import cv2 as cv
import numpy as np

def colour_filter(image, ftype):
    img = image.copy()
    if ftype == 'red tint':
        img[:, :, 1] = img[:, :, 0] = 0
    elif ftype == 'green tint':
        img[:, :, 0] = img[:, :, 2] = 0
    elif ftype == 'blue tint':
        img[:, :, 1] = img[:, :, 2] = 0
    elif ftype == 'sobel':
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        sx = cv.Sobel(gray, cv.CV_64F, 1, 0, ksize = 3)
        sy = cv.Sobel(gray, cv.CV_64F, 0, 1, ksize = 3)
        s_com = cv.bitwise_or(sx.astype('uint8'), sy.astype('uint8'))
        img = cv.cvtColor(s_com, cv.COLOR_GRAY2BGR)
    elif ftype == 'canny':
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        canny = cv.Canny(gray, 100, 200)
        img = cv.cvtColor(canny, cv.COLOR_GRAY2BGR)
    elif ftype == 'cartoon':
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        gray = cv.medianBlur(gray, 5)
        edges = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 9, 9)
        colour = cv.bilateralFilter(img, 9, 300, 300)
        img = cv.bitwise_and(colour, colour, mask = edges)
    return img

def main():
    cam = cv.VideoCapture(0)
    if not cam.isOpened():
        print("Error: Couldn't open the camera")
        return
    ftype = 'original'
    print("Keys: r = red, b = blue, g = green, s = sobel, c = canny, n = cartoon, q = quit")
    while True:
        ret, frame = cam.read()
        if not ret:
            print("Error: Couldn't open the camera")
            break
        result = colour_filter(frame, ftype)
        cv.imshow("Filter", result)
        key = cv.waitKey(0) & 0XFF
        if key == ord('r'):
            ftype = 'red tint'
        elif key == ord('b'):
            ftype = 'blue tint'
        elif key == ord('g'):
            ftype = 'green tint'
        elif key == ord('s'):
            ftype = 'sobel'
        elif key == ord('c'):
            ftype = 'canny'
        elif key == ord('n'):
            ftype = 'cartoon'
        elif key == ord('q'):
            break
        else:
            print("Enter a valid key")
    cam.release()
    cv.destroyAllWindows()
if __name__ == '__main__':
    main()

