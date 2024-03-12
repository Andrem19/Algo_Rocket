import math

def find_sqrt(target: int, number: int, prec: float):
    res = number*prec
    if res*res <= target:
        return res
    return find_sqrt(target, res, prec)

res = find_sqrt(1000, 1000, 0.98)
print(res)