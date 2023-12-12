#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Experiment 1 - Basins of Atrraction and Julia Sets
# Consider the complex feedback process z -> z^2 + c
# Since infinity is always an attractor for this process we set the goal 
# to color the domanin of attraction. 
# The colors will indicate how long it takes a point to escape towards infinity
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from cmath import isnan
import math
import numpy
from PIL import Image, ImageDraw, ImageColor
import os
import shutil

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# convert complex number to img coordinates and plot point
def drawPoint(x,y,w,h,xrange,yrange,image,color):
    if ( abs(x) > xrange ) | ( abs(y) > yrange) | isnan(x) | isnan(y):
        return 

    a = w/2 + int(round(x/xrange*(w/2-1))) 
    b = h - (h/2 + int(round(y/yrange*(h/2-1))))

    shape = [(a, b), (a, b)]
    image.rectangle(shape, fill =color, outline =color)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Settings

# Image size (pixels)
w, h = 800, 800

# Number of frames to generate
nframes = 100

# Video frame rate 
fps = 12

# Video output name
video_name = '/Users/riccardomorgana/Desktop/Fractals.mp4'

# Temp dir for storing rendered frames
framesdir = "/Users/riccardomorgana/Desktop/Frames"

# Set image range, centered (+-range) in the complex domain
xrange = 1.5
yrange = 1.5

# Magnitude threshold above which we consider the number to escape towards inf
M = 100.0

# Number of Iterations (max), shades of colors
K = 100

# RGB increments per step
rsat,gsat,bsat = 20,20,20

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Generate Frames

deltax = 2*xrange / (w-1)
deltay = 2*yrange / (h-1)

# creating new Image object
img = Image.new("RGB", (w, h))
img1 = ImageDraw.Draw(img) 

if os.path.isdir(framesdir):    
    shutil.rmtree(framesdir)
    
os.mkdir(framesdir)

for m in range(nframes): 

    # step 0 - choose c = p + iq 
    #p = 0.5 + 0.01 * m
    #q = 0
    
    p = -0.28 + 0.001 * m
    q = -0.7

    print( "Generating frame " + str(m) + ", c = " + str(p) + str(q) + "i" )

    # for all pixels in the image, we check in how many steps it runs to infinity
    # the faster a point will run to inf, the darker it will look

    # since the image is symmetric, generate half of it and mirror
    for nx in range(int(w/2)):
        for ny in range(int(h)):

            x0 = -xrange + nx*deltax
            y0 = -yrange + ny*deltay

            # step 1 - iterate the feedback process 
            x,y = x0,y0

            for k in range(K):
                xprev = x
                yprev = y
                x = xprev*xprev - yprev*yprev + p
                y = 2 * xprev * yprev + q

                # compute magnitude
                r = x*x + y*y
                if (r > M):

                    # this point escaped to infinity, paint it
                    
                    # greyscale - the brighter, the slower to infinity
                    #color = (k*rsat,k*gsat,k*bsat)
                    
                    # colors palette 1
                    R = (k < K/2) * k * rsat
                    G = (k > K/3 and k < 2*K/3 ) * k * gsat
                    B = ( k > K/2 ) * k * bsat
                    color = (R,G,B)

                    drawPoint(x0,y0,w,h,xrange,yrange,img1,color)
                    drawPoint(-x0,-y0,w,h,xrange,yrange,img1,color)
                    break

                    # paint black if reached last iter/color
                #if (k >= K):
                 #   drawPoint(x0,y0,w,h,xrange,yrange,img1,(0,0,0))
                  #  break

    #img.show()
    img.save( framesdir + "/frame-000" + str(m) +".png")
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Render video
import cv2
import re

# get a list of images filenames from folder
images = [img for img in os.listdir(framesdir) if img.endswith(".png")]

# sort by number
images.sort(key=lambda f: int(re.sub('\D', '', f)))

# get shape from the first
frame = cv2.imread(os.path.join(framesdir, images[0]))
height, width, layers = frame.shape

# render mp4 video
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

for image in images:
    video.write(cv2.imread(os.path.join(framesdir, image)))

cv2.destroyAllWindows()
video.release()    

# cleanup
#os.rmdir(framesdir)