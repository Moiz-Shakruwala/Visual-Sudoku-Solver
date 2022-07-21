import cv2
import numpy as np
import matplotlib.pyplot as plt
import predict

sudoku_a = cv2.imread('sudoku_d.png')
sudoku_a = cv2.resize(sudoku_a, (504,504))
gray = cv2.cvtColor(sudoku_a, cv2.COLOR_BGR2GRAY) 
blur = cv2.GaussianBlur(gray, (3,3),6) 
threshold = cv2.adaptiveThreshold(blur,255,1,1,11,2)
contour, hierarchy = cv2.findContours(threshold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

def main_outline(contour):
    biggest = np.array([])
    max_area = 0
    for i in contour:
        area = cv2.contourArea(i)
        if area >50:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i , 0.02* peri, True)
            if area > max_area and len(approx) ==4:
                biggest = approx
                max_area = area
    return biggest 

def reframe(points):
    points = points.reshape((4, 2))
    points_new = np.zeros((4,1,2),dtype = np.int32)
    add = points.sum(1)
    points_new[0] = points[np.argmin(add)]
    points_new[3] = points[np.argmax(add)]
    diff = np.diff(points, axis =1)
    points_new[1] = points[np.argmin(diff)]
    points_new[2] = points[np.argmax(diff)]
    return points_new

def splitcells(img):
    rows = np.vsplit(img,9)
    boxes = []
    for r in rows:
        cols = np.hsplit(r,9)
        for box in cols:
            boxes.append(box)
    return boxes

biggest = main_outline(contour)
biggest = reframe(biggest)

pts1 = np.float32(biggest)
pts2 = np.float32([[0,0],[504,0],[0,504],[504,504]])

matrix = cv2.getPerspectiveTransform(pts1,pts2)
imagewrap = cv2.warpPerspective(sudoku_a,matrix,(504,504))
imagewrap =cv2.cvtColor(imagewrap, cv2.COLOR_BGR2GRAY)

sudoku_cell = splitcells(imagewrap)
predictions=[]
# cv2.imshow('image1',sudoku_cell[35])

# cv2.waitKey(0)
# print(predict.predict(sudoku_cell[35]))
for cell in sudoku_cell:
    predictions.append(predict.predict(cell))

problem = [[0 for j in range(9)] for i in range(9)]

for i in range(81):
    row = i//9
    col = i%9
    problem[row][col]=predictions[i]