#!/usr/bin/env python
import numpy as np
from bisect import bisect
import sciencedates as sd


def INCORRECTRESULT_using_bisect(x, X0):  # pragma: no cover
    X0 = np.atleast_1d(X0)
    x.sort()
    ind = [bisect(x, x0) for x0 in X0]

    x = np.asanyarray(x)
    return np.asanyarray(ind), x[ind]


def main():
    print(sd.find_nearest([10, 15, 12, 20, 14, 33], [32, 12.01]))

    print(INCORRECTRESULT_using_bisect([10, 15, 12, 20, 14, 33], [32, 12.01]))


if __name__ == "__main__":  # pragma: no cover
    main()
