#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Julia Sets: Basins of Attraction of the complex feedback process z -> z^2 + c
#
# B/N version:
# For each complex number in the grid, iterate the process. 
# If it diverges to infinite, paint the point in white. Otherwise it will stay black
#
# riccardo marogna 2022 - from Peitgen,Richter, The Beauty of Fractals
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from cmath import isnan
import math
import numpy
from PIL import Image, ImageDraw

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# convert complex number to img coordinates and plot point
def drawPoint(x,y,w,h,xrange,yrange,image,color):
    if ( abs(x) > xrange ) | ( abs(y) > yrange) | isnan(x) | isnan(y):
        return 

    a = w/2 + int(round(x/xrange*(w/2-1))) 
    b = h - (h/2 + int(round(y/yrange*(h/2-1))))
    shape = [(a, b), (a, b)]
    image.rectangle(shape, fill =color, outline =color)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# image size
w, h = 500, 500

# set image range, centered (+-range) in the complex domain
xrange = 1.5
yrange = 1.5

# creating new Image object
img = Image.new("RGB", (w, h))
img1 = ImageDraw.Draw(img) 

# step 0 - choose c = p + iq 
p = 0.5
q = -0.1

# Magnitude threshold above which we consider the number to escape towards inf
M = 100.0

# Max Num Iterations
K=10

deltax = 2*xrange / (w-1)
deltay = 2*yrange / (h-1)

# For all numbers in the grid, we check if it runs to infinity
# if yes -> we paint it white, otherw black
for nx in range(w):
    for ny in range(h):

        x0 = -xrange + nx*deltax
        y0 = -yrange + ny*deltay

        # step 2 - iterate the feedback process 
        x,y = x0,y0

        for k in range(K):
            xprev = x
            yprev = y
            x = xprev*xprev - yprev*yprev + p
            y = 2 * xprev * yprev + q

            # compute magnitude
            r = x*x + y*y
            if (r > M):
                # this point escaped, paint it white
                color = (255,255,255)
                drawPoint(x0,y0,w,h,xrange,yrange,img1,color)
                break

img.show()
#img.save("JuliaSet_c_" + str(p) + str(q) + ".png")
