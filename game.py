import camera_controller
import pygame, sys
from pygame.locals import *
from threading import Thread
import SimpleCV.Camera


def main():

    FPS = 30 # frames per second setting
    fpsClock = pygame.time.Clock()

    background_image = pygame.image.load('background.png')
    WINDOW_SIZE = (1000, int(1000.0/background_image.get_width()*background_image.get_height()))
    background_image = pygame.transform.scale(background_image, WINDOW_SIZE)
    DISPLAYSURF = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Alphabet!')

    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    my_img = pygame.image.load('plane.png')
    my_img = pygame.transform.scale(my_img, (100, int(100.0/my_img.get_width()*my_img.get_height())))
    my_x = WINDOW_SIZE[0] / 4
    my_y = WINDOW_SIZE[1] / 2
    goal_y = WINDOW_SIZE[1] / 2

    background_x_1 = 0
    background_x_2 = WINDOW_SIZE[0] 

    while True: # main game loop
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(background_image, (background_x_1, 0))
        DISPLAYSURF.blit(background_image, (background_x_2, 0))

        speed = 5
        background_x_1 -= speed
        background_x_2 -= speed

        if background_x_1 < - WINDOW_SIZE[0]:
            background_x_1 = WINDOW_SIZE[0]
        if background_x_2 < - WINDOW_SIZE[0]:
            background_x_2 = WINDOW_SIZE[0]

        my_y += (goal_y - my_y)/ 3.0
        DISPLAYSURF.blit(my_img, (my_x, my_y))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == camera_controller.MYEVENT:
                print 'myevent received'
                goal_y = event.y * WINDOW_SIZE[1]
                # pygame.event.clear(camera_controller.MYEVENT)
                # break;
        pygame.display.update()
        fpsClock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    # This line caused program to hang when run from
    # camera_controller.run_camera_controller. When we pass it in however it
    # works.
    camera = SimpleCV.Camera()
    thread = Thread(target=camera_controller.run_camera_controller, args=(camera,))
    # thread = Thread(target=camera.test_random)
    thread.daemon = True
    thread.start()
    main()
