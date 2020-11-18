import cmath as cm
from PIL import Image 
   
w = 1920
h = 1080
   
julia = Image.new("RGB", (w, h), "white") 
pix = julia.load() 

n = 4
c = -1
max_iterations = 40

def f(z):
    return z**n + c

# The reason for z being defined as seen here is to center the picture.
for x in range(w): 
    for y in range(h):
        z = 1.5*(x - 0.5*w)/(0.5*w) + 1.0*(y - h/2)/(0.5*h)*1j
        z_old = 0
        i = max_iterations
        while (abs(z) != 0 and i > 1):
            z = z - (z**4.0 - 1.0)/(4.0*z**3.0)
            i -= 1 
        pix[x,y] = (i << 20) + (i << 12) + i*8
julia.show()