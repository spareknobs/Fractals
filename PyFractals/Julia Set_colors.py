#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Julia Sets: Basins of Attraction of the complex feedback process z -> z^2 + c
# Color version
#
# Since infinity is always an attractor for this process we set the goal to color the domanin 
# of attraction. The colors will indicate how long it takes a point to escape towards infinity
#
# riccardo marogna 2022 - from Peitgen,Richter, The Beauty of Fractals
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from cmath import isnan
import math
import numpy
from PIL import Image, ImageDraw, ImageColor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# convert complex number to img coordinates and plot point
def drawPoint(x,y,w,h,xrange,yrange,image,color):
    if ( abs(x) > xrange ) | ( abs(y) > yrange) | isnan(x) | isnan(y):
        return 

    a = w/2 + int( round( x/xrange * ( w/2 - 1 ) ) ) 
    b = h - (h/2 + int( round(y / yrange * ( h/2 - 1 ) ) ))

    shape = [(a, b), (a, b)]
    image.rectangle(shape, fill =color, outline =color)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Settings

# image size
#w, h = 200, 200
#w, h = 2500, 2500
w, h = 400, 400

# set image range, centered (+-range) in the complex domain
xrange = 1.5
yrange = 1.5

# creating new Image object
img = Image.new("RGB", (w, h))
img1 = ImageDraw.Draw(img) 

###########################
# Choose c = p + iq 
p = 0.0
q = 0.7
############################

# Magnitude threshold above which we consider the number to escape towards inf
M = 100.0

# Number of Iterations (max), shades of colors
K = 100

# RGB increments per step
sat = 600
rsat,gsat,bsat = int(sat/K),int(sat/K),int(sat/K)

deltax = 2*xrange / (w-1)
deltay = 2*yrange / (h-1)

# For all pixels in the image, we check in how many steps it runs to infinity
# if faster -> brighter

# use symmetry for optim
for nx in range(int(w/2)):

    x0 = -xrange + nx*deltax

    for ny in range(h):

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
                
                # this point escaped, assign to it a color according to k

                # greyscale
                # color = ((k+1)*rsat,(k+1)*gsat,(k+1)*bsat)
                    
                # colors palette 1
                R = (k < K/2) * k * rsat
                G = (k > K/3 and k < 2*K/3 ) * k * gsat
                B = ( k > K/2 ) * k * bsat
                color = (R,G,B)
                
                drawPoint(x0,y0,w,h,xrange,yrange,img1,color)
                drawPoint(-x0,-y0,w,h,xrange,yrange,img1,color)
                
                break

img.show()
#img.save("/Users/riccardomorgana/Desktop/Fractals/JuliaSetRGB_" + str(w) + "_" + str(h) + "_c_" + str(p) + "_" + str(q) + ".png")
