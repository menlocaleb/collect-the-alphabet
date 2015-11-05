import pygame.freetype
import pygame.sprite


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        sprite_width = 70
        self.original_image = pygame.image.load('assets/plane.png')
        img_width, img_height = self.original_image.get_size()
        self.original_image = pygame.transform.scale(
            self.original_image,
            (sprite_width, int(1.0 * sprite_width/img_width*img_height)))

        self.image = self.original_image

        self.rect = self.image.get_rect()

        self.rect.left = 75

        self.target_y = 50
        self.ease_in = 6.0


    def update(self):
        delta_y = (self.target_y - self.rect.centery)/ self.ease_in
        self.rect.centery += delta_y
        self.image = pygame.transform.rotate(self.original_image, - delta_y)


class Letter(pygame.sprite.Sprite):

    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    letter_index = 0

    def __init__(self, start_location):
        super(Letter, self).__init__()

        self.font = pygame.freetype.SysFont('monospace', 40)
        self.image, self.rect = self.get_image_and_rect()

        self.start_location = start_location

        self.rect.center = self.start_location

        self.speed = 5

    def get_image_and_rect(self):
        return self.font.render(self.get_next_letter(), fgcolor=(255, 255, 0), style=pygame.freetype.STYLE_STRONG)

    def get_next_letter(self):
        letter = Letter.letters[Letter.letter_index]
        Letter.letter_index += 1
        return letter

    def update(self):
        self.rect.centerx -= self.speed
        if self.rect.right < 0:
            if not Letter.done_with_letters():
                self.image, self.rect = self.get_image_and_rect()
                self.rect.center = self.start_location
            else:
                self.kill()
            
    @classmethod
    def done_with_letters(cls):
        return cls.letter_index >= len(cls.letters) 
        
class GameScore(pygame.sprite.Sprite):
    def __init__(self):
        super(GameScore, self).__init__()

        self.score = 0

        self.font = pygame.freetype.SysFont('monospace', 30)
        self.image, self.rect = self.font.render('Score: ' + str(self.score),
                                                fgcolor=(255, 255, 0),
                                                style=pygame.freetype.STYLE_STRONG)


    def incrementScore(self):
        self.score += 1
        self.image, self.rect = self.font.render('Score: ' + str(self.score),
                                                fgcolor=(255, 255, 0),
                                                style=pygame.freetype.STYLE_STRONG)

    def getScore(self):
        return self.score
            

class Background(pygame.sprite.Sprite):
    def __init__(self, index):
        super(Background, self).__init__()

        img = pygame.image.load('assets/background.png')
        width = 1000
        background_size = (
            width,
            int(1.0 * width/img.get_width()*img.get_height()))

        self.image = pygame.transform.scale(img, background_size)
        self.rect = self.image.get_rect()

        if index % 2 == 0:
            self.rect.left = 0
        else:
            self.rect.left = self.rect.width

        self.scroll_speed = 5

    def update(self):
        self.rect.left -= self.scroll_speed
        if self.rect.left < - self.rect.width:
            self.rect.left = self.rect.width
