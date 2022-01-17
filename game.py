import random

import pygame
import pygame.examples.midi
import pytmx
import pyscroll

from mermaid import Player


class Game:

    def __init__(self):
        # definir si notre jeu a commencé ou non
        self.is_playing = False
        # creer la fenetre du jeu
        self.screen = pygame.display.set_mode((800, 800))
        icon = pygame.image.load('asperia.jpg')
        pygame.display.set_icon(icon)
        pygame.display.set_caption("WAH - tresor hunting ")

        # charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame('map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1




        # generer un joueur
        player_position = tmx_data.get_object_by_name("pp")
        self.player = Player(player_position.x, player_position.y)

        #definir une liste qui va stocker les rectangles de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=10)
        self.group.add(self.player)

        # cree la poisition du tresor
        self.tresor_position_x = random.randrange(32, 766, 23)
        self.tresor_position_y = random.randrange(112, 681, 18)
        self.tresor = 30


    def handle_input(self):
        life_index = 100
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')
            life_index = life_index - 4
            print (life_index)

        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')

        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')

        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')


    def update(self):
        self.group.update()

        #verification de la collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def run(self, game=None):

        clock = pygame.time.Clock()
        font = pygame.font.Font(pygame.font.get_default_font(), 24)
        lives = 5
        heart_image = pygame.image.load('heart.png')

        # la boucle du jeu

        running = True
        x = 400
        y = 400
        life_index = 100

        tmx_data = pytmx.util_pygame.load_pygame('map.tmx')
        while running:

            screen = pygame.display.set_mode((800, 800))
            opening = pygame.image.load('asperia.jpg')

            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)


            # afficher le tresor
            pygame.draw.rect(self.screen, (255, 0, 0), (self.tresor_position_x, self.tresor_position_y, self.tresor, self.tresor))





            # lives
            for l in range(lives):
                screen.blit(heart_image, (0+ (l*50), 30))

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(20)
        pygame.quit()

