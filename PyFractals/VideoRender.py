############################################################
# Render video
import cv2
import os
import re
framesdir = "/Users/riccardomorgana/Desktop/Frames"
video_name = '/Users/riccardomorgana/Desktop/video.mp4'

images = [img for img in os.listdir(framesdir) if img.endswith(".png")]

images.sort(key=lambda f: int(re.sub('\D', '', f)))

# get frame shape from 1st frame
frame = cv2.imread(os.path.join(framesdir, images[0]))
height, width, layers = frame.shape

fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
fps = 12
video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

for image in images:
    video.write(cv2.imread(os.path.join(framesdir, image)))

cv2.destroyAllWindows()
video.release()    