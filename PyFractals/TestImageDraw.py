
# importing image object from PIL
import math
import numpy
from PIL import Image, ImageDraw
  
#image size
w, h = 500, 500
x0,y0 = w/2, h/2

# creating new Image object
img = Image.new("RGB", (w, h))
img1 = ImageDraw.Draw(img) 

x,y = 3,3

for n in range(10):
    x = int(round( x + n*1.67 ) )
    y = int(round(y*3.14))
    shape = [(x, y), (x+4, y+4)]
    img1.rectangle(shape, fill ="#ffffff", outline ="blue")

img.show()
