"""
this script is used to calibrate the machine cameras with fish eye lens
"""
import numpy as np
import cv2
import glob
import os

# the format of the chessboard used
row = 6         # the number of row in the picture take away 1
column = 79     # the number of column in the picture take away 1

# saving path, the path can be nonexistent
saving_folder = 'Q:\\test\\2\\cali'
if not os.path.exists(saving_folder):
    os.makedirs(saving_folder)

# where pictures need to be calbrated are saved
path = 'Q:\\test\\2'

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((column*row,3), np.float32)

objp[:,:2] = np.mgrid[0:row,0:column].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('chessboard/*.bmp')
"""
    glob.glob('A')  A: the folder where cheeseboard is saved 
"""

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (row,column),None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (row,column), corners2,ret)
        #cv2.imshow('img',img)
        #cv2.waitKey(0)

cv2.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

picture_name = glob.glob(path+'/*.jpg')
for files in picture_name:
    img = cv2.imread(files)
    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

    # undistort
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

    # crop the image
    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]
    cv2.imwrite(files.replace(path,saving_folder), dst)