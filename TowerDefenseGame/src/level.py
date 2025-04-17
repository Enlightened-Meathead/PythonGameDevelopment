import csv
import pygame
import game_settings

class Level():
    def __init__(self):
        self.background = None
        # Make a list that contains boolean values for each x,y coordinate pair according to the game setting
        self.blocked_tiles = [[False for i in range(game_settings.NUM_OF_COLS)] for r in range(game_settings.NUM_OF_ROWS)]
        self.enemy_waypoints = []


    def get_grid_from_csv(self, path_to_csv):
        file = open(path_to_csv, "r")
        grid = list(csv.reader(file))
        file.close()
        return grid

    def add_cell_to_tiles(self, cell, tiles):
        tiles[cell[0]][cell[1]] = True
    # Adding a grid to the blockedt tiles
    def add_grid_to_tiles(self, grid_to_add, tiles):
        # Grid represents csv
        # Tiles represents the blocked tiles attribute
        for row in range(len(tiles)):
            for col in range(len(tiles[row])):
                grid_value = int(grid_to_add[row][col])
                if grid_value >= 0:
                    # That means something is here, and we need to switch from false to true
                    tiles[row][col] = True
    def create_waypoint_vectors(self, waypoints):
        for waypoint in waypoints:
            x = waypoint[0] * game_settings.COL_SIZE // 2
            y = waypoint[1] * game_settings.ROW_SIZE // 2
            self.enemy_waypoints.append(pygame.Vector2(x,y))

    # Print the grid for debugging/testing
    def print_grid(self):
        for row in range(len(self.blocked_tiles)):
            for col in range(len(self.blocked_tiles[row])):
                print(self.blocked_tiles[row][col], "\t", end="")
            print()

# level = Level()
# level.print_grid()
#
# path = level.get_grid_from_csv('images/maps/TowerDefenseMap_Layer 3 Mine and Trees.csv')
# level.add_grid_to_tiles(path, level.blocked_tiles)
# level.print_grid()
