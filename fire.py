#Imports
import numpy as np
import matplotlib.pyplot as plt

#Global Variables
EMPTY = 0
TREE = 1
HOUSE = 2
FIRE = 3

# Given a 2d array, return a list with the x-coordinates (in a list) and the
# y-coordinates (in another list) of the cells that have the color passed.
def points_for_grid(grid, color, w, h):
	xc = []
	yc = []
		
	for x in range(w):
		for y in range(h):
			if grid[x,y] == color:
				xc.append(x)
				yc.append(y)
	return [xc, yc]

def neighbor_on_fire(grid, x, y, w, h):
	if x < w - 1 and grid[x + 1, y] == FIRE:
		return True
	if x > 0 and grid[x - 1, y] == FIRE:
		return True
	if y < h - 1 and grid[x, y + 1] == FIRE:
		return True
	if y > 0 and grid[x, y - 1] == FIRE:
		return True
	
	return False;

# Simulation parameters.
def runsim(
	WIDTH = 50,
	HEIGHT = 50,
	NUM_GEN = 200,
	HOUSE_DENSITY = 0.4,
	FOREST_DENSITY = 0.5,
	PROB_LIGHTNING = .1,
	PROB_TREE_IMMUNE = 0.25,
	PROB_HOUSE_IMMUNE = 0.5,
	TIME_TO_BURN = 3,
	PLOT = False
	):
	# Create Cube
	cube = np.empty((WIDTH, HEIGHT, NUM_GEN))

	# Place Trees in cells
	trees = np.random.choice([EMPTY, TREE], p = [1 - FOREST_DENSITY, FOREST_DENSITY], size = (WIDTH - 1) * HEIGHT)
	trees.shape = (WIDTH - 1, HEIGHT)
	cube[: - 1, :, 0] = trees

	# Place Houses in far right cells
	houses = np.random.choice([EMPTY, HOUSE], p = [1 - HOUSE_DENSITY, HOUSE_DENSITY], size = HEIGHT)
	cube[-1, :, 0] = houses
	
	HOUSE_COUNT = list(houses).count(HOUSE)

	for c in range(1, NUM_GEN):
		cube[:, :, c] = cube[:, :, 0]	

	# Run the simulation.
	for gen in range(1, NUM_GEN):
		for x in range(WIDTH):
			for y in range(HEIGHT):
				cube[x, y, gen] = cube[x, y, gen - 1]

				if cube[x, y, gen - 1] in [TREE, HOUSE] and cube[x, y, gen] != FIRE:
					#check neighbors for fire
					if neighbor_on_fire(cube[:, :, gen - 1], x, y, WIDTH, HEIGHT):
						if cube[x, y, gen - 1] == TREE:
							cube[x, y, gen] = np.random.choice([TREE, FIRE], p=[PROB_TREE_IMMUNE, 1 - PROB_TREE_IMMUNE], size = 1)
						else:
							cube[x, y, gen] = np.random.choice([HOUSE, FIRE], p=[PROB_HOUSE_IMMUNE, 1 - PROB_HOUSE_IMMUNE], size = 1)

				if cube[x, y, gen - 1] >= FIRE and cube[x, y, gen - 1] < FIRE + TIME_TO_BURN:
					cube[x, y, gen] += 1;
				elif cube[x, y, gen - 1] == FIRE + TIME_TO_BURN:
					cube[x, y, gen] = EMPTY;

		if np.random.choice([True, False], p = [PROB_LIGHTNING, 1 - PROB_LIGHTNING]):
			strike_x = np.random.choice(int(WIDTH / 2))
			strike_y = np.random.choice(int(HEIGHT))
			if cube[strike_x, strike_y, gen - 1] == TREE:
				cube[strike_x, strike_y, gen] = FIRE

	if PLOT:
		fire_vals = [FIRE + i for i in range(TIME_TO_BURN)]
		for gen in range(0, NUM_GEN):
			plt.clf()
			xc, yc = points_for_grid(cube[:, :, gen], TREE, WIDTH, HEIGHT)
			plt.scatter(xc, yc, marker = "^",color = "green")
			for f in fire_vals:
				xc, yc = points_for_grid(cube[:, :, gen], f, WIDTH, HEIGHT)
				plt.scatter(xc, yc, marker = "D", color = "orange")
			xc, yc = points_for_grid(cube[:, :, gen], HOUSE, WIDTH, HEIGHT)
			plt.scatter(xc, yc, marker = "p", color = "brown")
			plt.title("Generation #" + str(gen))
			plt.pause(.01)

	SURVIVED_HOUSES = list(cube[-1, :, NUM_GEN - 2]).count(HOUSE)
	
	#RETURN frac of houses that burn down
	return 1 - (SURVIVED_HOUSES / HOUSE_COUNT)

def parameterSweep(sweep_count = 50):
	burn_range = np.arange(1, 11, 1)
	ranges = np.arange(0, 1.1, .1)

	res = np.zeros(len(ranges))
	for i in range(0, len(ranges)):
		print("Prob_lightning: " + str(ranges[i]))	
		count = 0

		for j in range(0, sweep_count):
			count += runsim(PROB_LIGHTNING = ranges[i])

		res[i] = count / sweep_count

	plt.clf()
	plt.ylim(0, 1)
	plt.xlabel("Probability of Lightning")
	plt.ylabel("Average of Survived Houses")
	plt.suptitle("Probability of Lightning VS. Survived Houses")
	plt.plot(ranges, res)
	plt.show()

	res = np.zeros(len(ranges))
	for i in range(0, len(ranges)):
		print("tree immunity: " + str(ranges[i]))
		count = 0

		for j in range(0, sweep_count):
			count += runsim(PROB_TREE_IMMUNE = ranges[i])

		res[i] = count / sweep_count

	plt.clf()
	plt.ylim(0, 1)
	plt.xlabel("Tree Immunity")
	plt.ylabel("Average of Survived Houses")
	plt.suptitle("Tree Immunity VS. Survived Houses")
	plt.plot(ranges, res)
	plt.show()

	res = np.zeros(len(ranges))
	for i in range(0, len(ranges)):
		print("house immunity: " + str(ranges[i]))
		count = 0

		for j in range(0, sweep_count):
			count += runsim(PROB_HOUSE_IMMUNE = ranges[i])

		res[i] = count / sweep_count

	plt.clf()
	plt.ylim(0, 1)
	plt.xlabel("House Immunity")
	plt.ylabel("Average of Survived Houses")
	plt.suptitle("House Immunity VS. Survived Houses")
	plt.plot(ranges, res)
	plt.show()

	res = np.zeros(len(burn_range))
	for i in range(0, len(burn_range)):
		print("Burn Length: " + str(burn_range[i]))
		count = 0

		for j in range(0, sweep_count):
			count += runsim(TIME_TO_BURN = burn_range[i])

		res[i] = count / sweep_count

	plt.clf()
	plt.ylim(0, 1)
	plt.xlabel("Burn Length")
	plt.ylabel("Average of Survived Houses")
	plt.suptitle("Burn Length VS. Survived Houses")
	plt.plot(burn_range, res)
	plt.show()

	res = np.zeros(len(ranges))
	for i in range(0, len(ranges)):
		print("Forest Density: " + str(ranges[i]))
		count = 0

		for j in range(0, sweep_count):
			count += runsim(FOREST_DENSITY = ranges[i])

		res[i] = count / sweep_count

	plt.clf()
	plt.ylim(0, 1)
	plt.xlabel("Forest Density")
	plt.ylabel("Average of Survived Houses")
	plt.suptitle("Forest Density VS. Survived Houses")
	plt.plot(ranges, res)
	plt.show()

		
#parameterSweep();
runsim(PLOT=True)
