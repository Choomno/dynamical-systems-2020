# Choomno Moos
# Oct 29, 2020

from PIL import Image 
   
w = 1920
h = 1080
   
mandelbrot = Image.new("RGB", (w, h), "white") 
  
pix = mandelbrot.load() 

max_iterations = 255

def f(z):
    return z**2 + c

# The reason for c being defined as seen here is to center the picture.
# It is also possible to zoom in and shift the picture by changing c.
for x in range(w): 
    for y in range(h):
        c = 2.0*(x - 0.7*w)/(0.5*w) + 1.5*(y - h/2)/(0.5*h)*1j
        z = 0
        i = max_iterations
        while (abs(z) <= 2 and i > 1):
            z = f(z)
            i -= 1 
        pix[x,y] = (i << 20) + (i << 12) + i*8
mandelbrot.save("mandelbrot.png")