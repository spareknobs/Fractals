#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Mandelbrot Set
#
# Consider the complex feedback process z -> z^2 + c for each c in the complex domain, 
# starting from z=z0 and draw the set of points c for which the process does not diverge 
# to infinity. Mandelbrot set is similar to Julia sets, but it maps the numbers c instead of z
#
#   "there is a close correspondence between the geometry of the Mandelbrot set at a given point 
#   and the structure of the corresponding Julia set. For instance, a value of c belongs 
#   to the Mandelbrot set if the corresponding Julia set is connected. 
#   Thus, the Mandelbrot set may be seen as a map of the connected Julia sets. " (WikiPedia)
#
# riccardo marogna 2022 - from Peitgen,Richter, The Beauty of Fractals
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from cmath import isnan
import math
import numpy
from PIL import Image, ImageDraw

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# convert complex number to img coordinates and plot point
def drawPoint(x,y,w,h,xmin,xmax,ymin,ymax,image,color):
    if ( x > xmax ) | ( x < xmin ) |( y > ymax) | ( y < ymin ) |isnan(x) | isnan(y):
        return 
    xrange = xmax-xmin
    yrange = ymax-ymin
    a = int(round( (x-xmin)/xrange*(w-1))) 
    b = h - (int(round((y-ymin)/yrange*(h-1))))
    shape = [(a, b), (a, b)]
    image.rectangle(shape, fill =color, outline =color)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# image size
w, h = 1500, 1500

# set image range, centered (+-range) in the complex domain
xmin, xmax = 0.0, 0.6
ymin, ymax = 0.0, 0.6

# creating new Image object
img = Image.new("RGB", (w, h))
img1 = ImageDraw.Draw(img) 

# Magnitude threshold above which we consider the number to escape towards inf
M = 50.0

# Max Num Iterations
K=50

xrange = xmax-xmin
yrange = ymax-ymin
deltax = xrange / (w-1)
deltay = yrange / (h-1)

# For all pixels in the image, we check if it runs to infinity
# if yes -> we paint it white, otherw black
for nx in range(w):
    for ny in range(h):

        p = xmin + nx*deltax
        q = ymin + ny*deltay

        # iterate from point z = (0,0)
        x,y = 0,0

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
                drawPoint(p,q,w,h,xmin,xmax,ymin,ymax,img1,color)
                break

img.show()
#img.save("Mandelbrot.png")
