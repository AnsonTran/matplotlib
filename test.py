# 0 0 -1 0
# 1 0 0 -2
# 0 -1 0 2
# 0 0 0 1

import numpy as np
import math

rx_90 = np.matrix([
    [1, 0, 0, 0],
    [0, 0, -1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1]
])

rx_180 = np.matrix([
    [-1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, -1, 0],
    [0, 0, 0, 1]
])


print(math.cos(math.pi))
print(math.sin(math.pi))
print(-math.sin(math.pi))
