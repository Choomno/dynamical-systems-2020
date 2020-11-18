# Choomno Moos
# Oct 29, 2020

from PIL import Image 
   
w = 1920
h = 1080
   
julia = Image.new("RGB", (w, h), "white") 
  
pix = julia.load() 

c = -0.7269 + 0.1889j
max_iterations = 255

def f(z):
    return z**2 + c

# The reason for z being defined as seen here is to center the picture.
for x in range(w): 
    for y in range(h):
        z = 1.5*(x - 0.5*w)/(0.3*w) + 1.0*(y - 0.5*h)/(0.3*h)*1j
        i = max_iterations
        while (abs(z) <= 2 and i > 1):
            z = f(z)
            i -= 1 
        pix[x,y] = (i << 20) + (i << 12) + i*8
julia.save("julia.png")