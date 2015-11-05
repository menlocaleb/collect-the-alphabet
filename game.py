import camera_controller
import sprites
import pygame, sys
from pygame.locals import *
import pygame.freetype
import random
from threading import Thread
import SimpleCV.Camera


class CollectTheAlphabetGame():
    def __init__(self):
        pygame.init()
        self.FPS = 30 # frames per second setting
        self.fpsClock = pygame.time.Clock()

        self.score = sprites.GameScore()

        self.player = sprites.Player()
        self.backgrounds = []
        self.backgrounds.append(sprites.Background(0))
        self.backgrounds.append(sprites.Background(1))

        self.WINDOW_SIZE = self.backgrounds[0].image.get_size()
        self.DISPLAYSURF = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption('Alphabet!')

        # TODO make sure in right order
        self.letters = []
        for i in range(3):
            self.letters.append(sprites.Letter((self.WINDOW_SIZE[0] + random.randint(0, 500),
                                                self.WINDOW_SIZE[1]/2 + random.randint(-100, 100))))

        self.render_group = pygame.sprite.OrderedUpdates()
        self.render_group.add(self.backgrounds)
        self.render_group.add(self.letters)
        self.render_group.add(self.score)
        self.render_group.add(self.player)

        self.letter_group = pygame.sprite.Group()
        self.letter_group.add(self.letters)


    def isGameOver(self):
        return len(self.letter_group.sprites()) == 0


    def main(self):
        while True: # main game loop
            self.render_group.update()

            if self.isGameOver():
                if self.score.getScore() == len(sprites.Letter.letters):
                    print 'You Win!'
                else:
                    print 'Game Over. You scored %d points!' % self.score.getScore()
                return

            collision_list = pygame.sprite.spritecollide(self.player, self.letter_group, False)

            for letter in collision_list:
                self.score.incrementScore()
                letter.rect.right = 0

            self.render_group.draw(self.DISPLAYSURF)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == camera_controller.MYEVENT:
                    # print 'myevent received'
                    self.player.target_y = event.y * self.WINDOW_SIZE[1]

            pygame.display.update()
            self.fpsClock.tick(self.FPS)


if __name__ == '__main__':
    game = CollectTheAlphabetGame()
    # This line caused program to hang when run from
    # camera_controller.run_camera_controller. When we pass it in however it
    # works.
    camera = SimpleCV.Camera()
    thread = Thread(target=camera_controller.run_camera_controller, args=(camera,))
    thread.daemon = True
    thread.start()
    game.main()
