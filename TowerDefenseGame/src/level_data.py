import pygame
from level import Level
# Create the first level
level_one = Level()
level_one.background = pygame.image.load('images/maps/TowerDefenseMap.png')
level_one.add_grid_to_tiles(level_one.get_grid_from_csv('images/maps/TowerDefenseMap_Layer 4 Path.csv'),
                            level_one.blocked_tiles)
level_one.add_grid_to_tiles(level_one.get_grid_from_csv('images/maps/TowerDefenseMap_Layer 3 Mine and Trees.csv'),
                            level_one.blocked_tiles)
level_one.create_waypoint_vectors([
    (30, 0),
    (30, 8),
    (6, 8),
    (6,22),
    (24, 22),
    (24,34),
    (8,34),
    (8, 32)
])
# Can add more levels here then just import when you are done