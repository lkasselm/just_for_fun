"""
Simple 2D gravity simulation

TODO:
* Implement particle-mesh technique
* Implement adaptive time steps
"""

import numpy as np
from numpy import transpose as tr
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as anim
# need to specity the path to the ffmpeg.exe
path = 'C:\\Programme\\ffmpeg\\bin\\ffmpeg.exe'
plt.rcParams['animation.ffmpeg_path'] = path
from joblib import Parallel, delayed
from random import randint as ri
import random
from scipy.ndimage.filters import gaussian_filter
from skimage.transform import resize
import sys

#############################################################
# Options
#############################################################
# random IC
coords = []
vels = []
masses = []
for i in range(1000):
	coords.append([random.uniform(0,20),
								 random.uniform(0,40)])
#	vels.append([random.uniform(-2,2),random.uniform(-2,2)])
	vels.append([0,0])
	masses.append(0.001)

#coords = tr(coords)

#vels = tr(vels)

#coords = [[1,5],[5,8]]
#vels = [[0,0],[0,0]]

coords = np.array(coords)
vels = np.array(vels)

force_constant = 0.1 # stength of gravity
dt = 1
softening_length = 0.001 
# to prevent singularities in potential

n_gens = 2000 # total amount of time-steps
num_recursions = 1
#############################################################

def next_gen(coords,vels):
#	print('called next_gen')
#	print(coords)
	# calculate forces for all particle pairs

	new_coords = []
	new_vels = []

	# loop over particles
	for i in range(len(coords)):
		ax_t = 0
		ay_t = 0
		# sum accelerations from all particles
		for j in range(len(coords)):
			if i != j:
				# get distance
				r = np.sqrt((coords[i][0]-coords[j][0])**2+
										(coords[i][1]-coords[j][1])**2)
#				print(r)
				# acceleration magnitude
				a = force_constant * masses[j]/np.sqrt(
							r**2+softening_length**2)
				# multiply by unit vector to get direction
				# The 0.001 is there to get rid of 
				# divide by zero errors
				# There is probably a better way to do this
				ax_t += a * (coords[j][0] - coords[i][0]
								) / np.sqrt(r**2+0.001**2)
				ay_t += a * (coords[j][1] - coords[i][1]
								) / np.sqrt(r**2+0.001**2)
		# update positions and velocities
		new_vel = [vels[i][0]+ax_t*dt,vels[i][1]+ay_t*dt]
		new_coord = [coords[i][0]+new_vel[0]*dt,coords[i][1]
								+new_vel[1]*dt]
		new_coords.append(new_coord)
		new_vels.append(new_vel)
#		print(coords[0])
#		print(new_coords)

	return np.array(new_coords), np.array(new_vels)

fig = plt.figure(frameon=False)
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, 
										wspace=None, hspace=None)

ims = []
for i in range(n_gens):
	print('Generation ', i)
#	print(coords, vels)
	ax = plt.Axes(fig, [0., 0., 1., 1.])
	ax.set_axis_off()
	fig.add_axes(ax)
#	print(coords)
	hist = np.histogram2d(tr(coords)[0], tr(coords)[1], 
					bins=[1000,1334], range=[[0,20],
					[0,40]])[0]
	hist[hist > 0] = 1
	hist = gaussian_filter(hist, sigma=1.3)
	im = plt.imshow(hist, cmap='gist_gray',
									vmin=0,vmax=0.05)
	ims.append([im])
	coords, vels = next_gen(coords, vels)

ani = anim.ArtistAnimation(fig, ims, interval=50, 
						   blit=True, repeat_delay=0)

ani.save('gravity.mp4', dpi=200)
plt.show()