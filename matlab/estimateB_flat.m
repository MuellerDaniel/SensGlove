function n = estimateB_flat(r,h,b)
calcB(r,h)
n = norm(b - calcB(r,h));