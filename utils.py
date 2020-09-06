"""
Created on Sun Sep 06 20:21 2020

@author: erebos
"""
def mean(x):
    return sum(x) / len(x)

def sum_norm(x, x_mu = None, square = False):
    if x_mu is None:
        x_mu = mean(x)
    s = 0
    for i in x:
        if square:
            s += (i - x_mu) * (i - x_mu)
        else:
            s += i - x_mu
    return s

def lr1d(x, y):
    x_mu, y_mu = mean(x), mean(y)
    b = sum_norm(x, x_mu) * sum_norm(y, y_mu) / sum_norm(x, x_mu, square = True)
    a = y_mu - x_mu * b
    return b, a

def cubic_y(v0, v1, v2, v3, x):
    v32 = v3 - v2
    v01 = v0 - v1
    v20 = v2 - v0
    res = (v32 - v01) * x
    res = (res + v01 * 2 - v32) * x
    res = (res + v20) * x + v1
    return res

def cubic1d(x, y, dts):
    ptx = 0
    res_y = []
    for i in range(len(x)-3):
        if i == 0:
            while dts[ptx] < x[i+1]:
                t = dts[ptx]
                x01 = x[i] - x[i+1]
                x02 = x[i] - x[i+2]
                x12 = x[i+1] - x[i+2]
                pty = (t - x[i+1])*(t-x[i+2])/x01/x02*y[i]-(t-x[i])*(t-x[i+2])/x01/x12*y[i+1]+(t-x[i])*(t-x[i+1])/x02/x12*y[i+2]
                res_y.append(pty)
                ptx += 1
        while dts[ptx] < x[i+2]:
            if dts[ptx] < x[i+2] and dts[ptx] >= x[i+1]:
                t = (dts[ptx] - x[i+1]) / (x[i+2] - x[i+1])
                pty = cubic_y(y[i], y[i+1], y[i+2], y[i+3], t)
                res_y.append(pty)
            ptx += 1
    while ptx < len(dts) and dts[ptx] < x[-1]:
        t = dts[ptx]
        x01 = x[-3] - x[-2]
        x02 = x[-3] - x[-1]
        x12 = x[-2] - x[-1]
        pty = (t - x[-2])*(t-x[-1])/x01/x02*y[-3]-(t-x[-3])*(t-x[-1])/x01/x12*y[-2]+(t-x[-3])*(t-x[-2])/x02/x12*y[-1]
        res_y.append(pty)
        ptx += 1
    return res_y