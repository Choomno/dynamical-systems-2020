import numpy as np
import matplotlib.pyplot as plt

n = 10000
iterations = 40

x = y = np.linspace(-1,1,n)
X,Y = np.meshgrid(x,y)
Z = X + Y*1j

for i in range(iterations):
    Z = Z - (Z**4.0 - 1.0)/(4.0*Z**3.0)
    print(i)
    
phi = np.angle(Z)
plt.contourf(X,Y,4*phi,cmap='jet')