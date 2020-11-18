iterations = 20


mu = 3.25
n=3
N = 2**(n-1)
for i in range(iterations):
    x = 0.5
    dx = 0
    for i in range(N):
        x = mu * x * (1 - x)
        dx = x * (1 - x) + mu  * (1 - 2 * x) * dx
    mu = mu - (x - 0.5)/(dx)
    print(mu)