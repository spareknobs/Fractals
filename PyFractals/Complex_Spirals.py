#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# iterate the map: z -> z^2
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
w, h = 1000, 1000
#w, h = 2500, 2500
#w, h = 4000, 4000

# set image range, centered (+-range) in the complex domain
xrange = 2.5
yrange = 2.5

# creating new Image object
img = Image.new("RGB", (w, h))
img1 = ImageDraw.Draw(img) 

################################################
# Choose starting point z0 = x0 + iy0 

# polar coordinates 
r = 1.001
ph = 0 #numpy.pi
x0 = r * numpy.cos(ph)
y0 = r * numpy.sin(ph)

# cartesian coordinates
#x0 = 0.9999
#y0 = 0.5

################################################
# Number of Iterations (max), shades of colors
K = 1000

# RGB increments per step
sat = 255*K
rsat,gsat,bsat = int(sat/K),int(sat/K),int(sat/K)

# iterate the feedback process 
x,y = x0,y0

for k in range(K):

    # greyscale
    # color = ((k+1)*rsat,(k+1)*gsat,(k+1)*bsat)

    # white
    R = 255
    G = 255
    B = 255

    # colors palette 1
    R = (k < K/2) * k * rsat
    G = (k > K/3 and k < 2*K/3 ) * k * gsat
    B = ( k > K/2 ) * k * bsat
    
    color = (R,G,B)
    drawPoint(x,y,w,h,xrange,yrange,img1,color)

    xprev, yprev = x, y

    # (x + yi) * (x0 + iy0)
    x = xprev * x0 - yprev * y0
    y =  yprev * x0 + xprev * y0
            
img.show()
#img.save("/Users/riccardomorgana/Desktop/ComplexSpiral_" + str(w) + "_" + str(h) + "_z_" + str(x0) + "_" + str(y0) + ".png")
