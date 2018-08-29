"""
this srcript is used for split a video to frames
"""
import cv2
import os

video_path = 'C:\\Users\\FlumeLab9\\Desktop\\zma\\trackpy'
video_name = 'DSC_0296'
vidcap = cv2.VideoCapture(video_path + '\\' + video_name + '.mov')
saving_folder = 'C:\\Users\\FlumeLab9\\Desktop\\zma\\trackpy\\' + video_name
if not os.path.exists(saving_folder):
    os.makedirs(saving_folder)
success,image = vidcap.read()
count = 0
success = True
while success:
    success,image = vidcap.read()
    # crop the pictures
    image = image[420:560,520:1370]   # [y1:y2, x1:x2]
    cv2.imwrite(saving_folder + "/%d.jpg" % count, image)     # save frame as JPEG file
    if cv2.waitKey(10) == 27:
        break
    count += 1
