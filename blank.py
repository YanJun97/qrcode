import cv2
import numpy


img = cv2.imread("images/{154csvlw2l5b342443.jpg")
print(img.dtype)
origin = img.copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
element = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
gray = cv2.GaussianBlur(gray, (5, 5), 0)[:,:gray.shape[1]//2]
# gray = cv2.erode(gray,element)
# gray = cv2.dilate(gray,element)

_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
cv2.imshow("adap", gray)
cv2.waitKey(0)
cv2.imshow("binary", binary)
cv2.waitKey(0)
edge = cv2.Canny(gray,100,200)
cv2.imshow("edge", edge)
cv2.waitKey(0)
contours, hierachy = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
hierachy = hierachy[0]
print(hierachy.shape)
targets = []
for i in range(len(hierachy)):
    child = hierachy[i][2]
    level = 1
    while hierachy[child][2] >= 0:
        child = hierachy[child][2]
        level += 1
    if level >= 2:
        targets.append(i)
for i in range(len(targets)):
    cv2.drawContours(origin, contours, targets[i], (0,255,0), 2)

cv2.imshow("contours", origin)
cv2.waitKey(0)