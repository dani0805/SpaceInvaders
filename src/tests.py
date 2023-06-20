import time

import numpy as np
import scipy.signal

# fix random seed for reproducibility
np.random.seed(0)

W = 10000
H = 10000

size = 2

n_ships = 8000

# create a random array of x,y position in a 800x600 image
ships = np.random.rand(n_ships, 2)
ships[:, 0] *= W
ships[:, 1] *= H

# time the two methods

now = time.time()
# count the number of ships in each patch
# first, create a 2D histogram of the indices
hist, xedges, yedges = np.histogram2d(ships[:, 0], ships[:, 1], bins=(200, 200), range=((0, W), (0, H)))

print(f"hist: {hist}")

# then, use the histogram as an index into the ships array
# the first index is the x index, the second index is the y index
# the result is a 2D array with the number of ships in each patch


collisions = hist >= 1
print(collisions)

# use a 2d convolution to find the number of ships in each patch and its neighbors
# first, create a 2D kernel with 1s everywhere
kernel = np.ones((2, 2))

# then, use scipy 2d convolution to convolve the kernel with the histogram
# the result is a 2D array with the number of ships in each patch and its neighbors
convolved = scipy.signal.convolve2d(hist, kernel, mode='same')
print(convolved)

# loop over the patches
for i in range(200):
    for j in range(200):
        # if there are more than 1 ships in the patch and its neighbors, there is a collision
        if convolved[i, j] > 1:
            # find the indices of the ships in the patch
            # the first index is the x index, the second index is the y index
            # the result is a 2D array with the indices of the ships in the patch
            indices = np.where((ships[:, 0] >= xedges[i]) & (ships[:, 0] < xedges[i + 1]) & (ships[:, 1] >= yedges[j]) & (ships[:, 1] < yedges[j + 1]))
            #print(f"i: {i}, j: {j}, indices: {indices}")
            # check for collision between all pairs of ships in the patch and its neighbors
            for k in range(len(indices[0])):
                for l in range(k + 1, len(indices[0])):
                    # if the ships are closer than the size of the ship, there is a collision
                    if np.linalg.norm(ships[indices[0][k], :] - ships[indices[0][l], :]) < size:
                        print(f"Collision between ship {indices[0][k]} and ship {indices[0][l]}")
                        # print the coordinates of the ships
                        print(f"Ship {indices[0][k]}: {ships[indices[0][k], :]}")
                        print(f"Ship {indices[0][l]}: {ships[indices[0][l], :]}")

print(f"Time: {time.time() - now}")


now = time.time()
# for comparison check the naive approach
for i in range(n_ships):
    for j in range(i + 1, n_ships):
        if np.linalg.norm(ships[i, :] - ships[j, :]) < size:
            print(f"Collision between ship {i} and ship {j}")

print(f"Time: {time.time() - now}")
