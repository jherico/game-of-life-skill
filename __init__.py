from mycroft import MycroftSkill, intent_file_handler
from mycroft.skills import resting_screen_handler
import threading
import os
import random
import numpy as np
import json

ON = 255
OFF = 0

def random_grid(W, H):
    """returns a grid of NxN random values"""
    return np.random.choice([ON, OFF], W*H, p=[0.2, 0.8]).reshape(W, H)

def update(frameNum, img, grid, W, H):
    # copy grid since we require 8 neighbors 
    # for calculation and we go line by line 
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            # compute 8-neghbor sum
            # using toroidal boundary conditions - x and y wrap around 
            # so that the simulaton takes place on a toroidal surface.
            total = int((grid[i, (j-1)%H] + grid[i, (j+1)%H] +
                        grid[(i-1)%W, j] + grid[(i+1)%W, j] +
                        grid[(i-1)%W, (j-1)%H] + grid[(i-1)%W, (j+1)%H] +
                        grid[(i+1)%W, (j-1)%H] + grid[(i+1)%W, (j+1)%H])/255)

            # apply Conway's rules
            if grid[i, j] == ON:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = OFF
            else:
                if total == 3:
                    newGrid[i, j] = ON

    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

def grid_to_model(grid):
    result = [{ "age": int(x)} for x in grid.reshape(-1)]
    return result

def model_to_grid(grid, w, h):
    return np.reshape([x['age'] for x in grid], w, h)

class GameOfLife(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.timer = False
        self.width = 0
        self.height = 0
        self.cells = []

    def initialize(self):
        self.gui.register_handler("gameoflife.notvisible", self.handle_gui_hidden)
        self.gui.register_handler("gameoflife.gridComplete", self.handle_grid_complete)
        self.log.info(f"Initializing skill")
        self.gui['rootPath'] = f"file://{self.root_dir}"
        self.gui["model"] = self.cells
        self.gui['cellSize'] = int(10)
    
    def handle_gui_hidden(self, message):
        self.log.info("got not visible")
        self.timer = False

    def handle_grid_complete(self, message):
        self.log.info("got grid complete " + str(message.data['width']) +  " " + str(message.data['height']))
        self.width = int(message.data['width'])
        self.height = int(message.data['height'])
        model = grid_to_model(random_grid(self.width, self.height))
        self.log.info(json.dumps(model))
        self.gui["model"] = model


    def update_cells(self):
        if (len(self.cells) != 0):
            return
        self.gui["model"] = grid_to_model(random_grid(self.width, self.height))

    @intent_file_handler('life.of.game.intent')
    def handle_life_of_game(self, message):
        self.log.info(f"handling intent skill")
        self.log.info(f"show UI")
        self.gui.show_page("life.qml")
        self.timer = True
        self.on_timer()

    @resting_screen_handler('Life')
    def handle_idle(self, message):
        self.log.info(f"handling idle event")

    def next_color(self): 
        result = self.colors[self.index]
        self.index += 1
        self.index = self.index % len(self.colors)
        return result

    def on_timer(self):
        self.log.info(f"handling timer event")
        self.update_cells()
        if self.timer:
            threading.Timer(1, self.on_timer).start()

    def stop(self):
        self.log.info(f"Stopping skill")
        self.timer = False

    def shutdown(self):
        self.log.info(f"Shutdown skill")

def create_skill():
    return GameOfLife()



# def addGlider(i, j, grid):

#     """adds a glider with top left cell at (i, j)"""
#     glider = np.array([[0, 0, 255], 
#                     [255, 0, 255], 
#                     [0, 255, 255]])
#     grid[i:i+3, j:j+3] = glider

# def addGosperGliderGun(i, j, grid):

#     """adds a Gosper Glider Gun with top left
#     cell at (i, j)"""
#     gun = np.zeros(11*38).reshape(11, 38)

#     gun[5][1] = gun[5][2] = 255
#     gun[6][1] = gun[6][2] = 255

#     gun[3][13] = gun[3][14] = 255
#     gun[4][12] = gun[4][16] = 255
#     gun[5][11] = gun[5][17] = 255
#     gun[6][11] = gun[6][15] = gun[6][17] = gun[6][18] = 255
#     gun[7][11] = gun[7][17] = 255
#     gun[8][12] = gun[8][16] = 255
#     gun[9][13] = gun[9][14] = 255

#     gun[1][25] = 255
#     gun[2][23] = gun[2][25] = 255
#     gun[3][21] = gun[3][22] = 255
#     gun[4][21] = gun[4][22] = 255
#     gun[5][21] = gun[5][22] = 255
#     gun[6][23] = gun[6][25] = 255
#     gun[7][25] = 255

#     gun[3][35] = gun[3][36] = 255
#     gun[4][35] = gun[4][36] = 255

#     grid[i:i+11, j:j+38] = gun



# # main() function
# def main():

#     # Command line args are in sys.argv[1], sys.argv[2] ..
#     # sys.argv[0] is the script name itself and can be ignored
#     # parse arguments
#     parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")

#     # add arguments
#     parser.add_argument('--grid-size', dest='N', required=False)
#     parser.add_argument('--mov-file', dest='movfile', required=False)
#     parser.add_argument('--interval', dest='interval', required=False)
#     parser.add_argument('--glider', action='store_true', required=False)
#     parser.add_argument('--gosper', action='store_true', required=False)
#     args = parser.parse_args()
    
#     # set grid size
#     N = 100
#     if args.N and int(args.N) > 8:
#         N = int(args.N)
        
#     # set animation update interval
#     updateInterval = 50
#     if args.interval:
#         updateInterval = int(args.interval)

#     # declare grid
#     grid = np.array([])

#     # check if "glider" demo flag is specified
#     if args.glider:
#         grid = np.zeros(N*N).reshape(N, N)
#         addGlider(1, 1, grid)
#     elif args.gosper:
#         grid = np.zeros(N*N).reshape(N, N)
#         addGosperGliderGun(10, 10, grid)

#     else: # populate grid with random on/off -
#             # more off than on
#         grid = randomGrid(N)

#     # set up animation
#     fig, ax = plt.subplots()
#     img = ax.imshow(grid, interpolation='nearest')
#     ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
#                                 frames = 10,
#                                 interval=updateInterval,
#                                 save_count=50)

#     # # of frames? 
#     # set output file
#     if args.movfile:
#         ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])

#     plt.show()

# # call main
# if __name__ == '__main__':
#     main()
