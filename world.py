from character import Character
from items import Item
import constants

class World():
    def __init__(self):
        self.map_tiles = []
        self.obstacle_tiles = []
        self.exit_tile = None
        self.item_list = []
        self.player = None
        self.villain_list = []
    
    def process_data(self, data, tile_list, item_images, mob_animations):
        self.level_length = len(data)
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image = tile_list[tile]
                image_rect = image.get_rect()
                image_x = x * constants.TILE_SIZE
                image_y = y * constants.TILE_SIZE
                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y]
                if tile == 7:
                    self.obstacle_tiles.append(tile_data)
                elif tile == 8:
                    self.exit_tile = tile_data
                elif tile == 9: # coin
                    coin = Item(image_x, image_y, 0, item_images[0])
                    self.item_list.append(coin)
                    tile_data[0] = tile_list[0]
                elif tile == 10: # aid
                    aid = Item(image_x, image_y, 1, item_images[1])
                    self.item_list.append(aid)
                    tile_data[0] = tile_list[0]
                elif tile == 11: # player
                    player = Character(image_x, image_y, 100, mob_animations, 0, False, 2, self.villain_list)
                    self.player = player
                    tile_data[0] = tile_list[0]
                elif tile == 12: # villain
                    villain = Character(image_x, image_y, 100, mob_animations, 1, False, 2, self.villain_list)
                    self.villain_list.append(villain)
                    tile_data[0] = tile_list[0]
                elif tile == 14: # blaze
                    blaze = Item(image_x, image_y, 2, item_images[2])
                    self.item_list.append(blaze)
                    tile_data[0] = tile_list[0]
                elif tile == 15: # flagger
                    flagger = Item(image_x, image_y, 3, item_images[3])
                    self.item_list.append(flagger)
                    tile_data[0] = tile_list[0]
                if tile >= 0:
                    self.map_tiles.append(tile_data)

    def update(self, screen_scroll):
        for tile in self.map_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])

    
    def draw(self, surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])