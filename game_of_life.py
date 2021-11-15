"""
Simple game of life implementation
using numpy and matplotlib

Under options, you can specify the total number 
of generations you want to run.
You also need to specify the initial conditions
in the form of a 2-D boolean array
(1 = alive, 0 = dead).

The rules are implemented in lines 73-81.
These are:
* A dead cell comes to live 
  if it has 3 alive neighbors
* An alive cell stays alive if it has
  2 or 3 alive neighbors
Feel free to experiment with different ones.
"""

import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as anim
# need to specity the path to the ffmpeg.exe
path = 'C:\\Programme\\ffmpeg\\bin\\ffmpeg.exe'
plt.rcParams['animation.ffmpeg_path'] = path
from joblib import Parallel, delayed

def place_glider_se(array,x,y):
	array[y][x+1] = 1
	array[y-1][x] = 1
	array[y+1][x] = 1
	array[y+1][x-1] = 1
	array[y+1][x+1] = 1


# Options
##################################################
# random IC
"""
rng = np.random.default_rng()
IC = rng.integers(low=0, high=2, size=(100,100))
"""

# line IC
"""
IC = np.zeros((750,1000))
for i in range(175,575):
	IC[i][500] = 1
"""

# Stripes IC
"""
IC = np.zeros((750,1000))
for i in range(175,575):
	for j in range(300,700,2):
		IC[i][j] = 1
"""

# stable block
IC = np.zeros((750,1000))

for i in range(175,575,3):
	for j in range(300,700,3):
		IC[i][j] = 1

for i in range(175,575,3):
	for j in range(301,701,3):
		IC[i][j] = 1

for i in range(176,576,3):
	for j in range(300,700,3):
		IC[i][j] = 1

for i in range(176,576,3):
	for j in range(301,701,3):
		IC[i][j] = 1

place_glider_se(IC,285,160)

plt.imshow(IC,cmap='gist_gray',aspect='equal')
plt.show()

n_gens = 1000
##################################################

def next_gen(array):

	# get shape of array
	shape = np.shape(array)
	xlen = shape[0]
	ylen = shape[1]

	new_array = np.zeros(shape)

	# add frame of zeros to deal with cells on edge
	array = np.pad(array, [(1,1),(1,1)])

	# loop over cells
	for i in range(1,xlen-1):
		for j in range(1,ylen-1):
			cell = array[i][j]
			
			# get number of alive neighbors
			num_alive = np.sum([array[i-1][j-1],
						 array[i-1][j],array[i-1][j+1],
						 array[i][j-1],array[i][j+1],
						 array[i+1][j-1],array[i+1][j],
						 array[i+1][j+1]])
			
			# apply rules 
			if cell == 0:
				# if cell is dead
				if num_alive == 3:
					new_array[i-1][j-1] = 1
			
			if cell == 1:
				# if cell is alive
				if num_alive == 2 or num_alive == 3:
					new_array[i-1][j-1] = 1

	return new_array

fig = plt.figure(frameon=False)
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, 
									  wspace=None, hspace=None)

ims = []
gen = IC
for i in range(n_gens):
	print('Generation ',i)
	gen = next_gen(gen)
	ax = plt.Axes(fig, [0., 0., 1., 1.])
	ax.set_axis_off()
	fig.add_axes(ax)
	img = plt.imshow(gen, cmap='gist_gray')
	ims.append([img])

ani = anim.ArtistAnimation(fig, ims, interval=50, 
						   blit=True, repeat_delay=0)

ani.save('game_of_life.mp4',dpi=200)
plt.show()