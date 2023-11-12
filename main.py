import pygame as pg
import pygame.mixer as mixer

class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y, scale): # scale - 0.1 to 1
        super().__init__()
        self.image = pg.Surface([100, 100])
        self.image = pg.transform.scale(self.image, (100*scale, 100*scale))
        self.image.fill('red')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface([5, 5])
        self.image.fill('blue')
        self.rect = self.image.get_rect()
        self.shot = mixer.Sound('sfx/shot.wav')
        self.cooldown = 0
    
    def update(self):
        self.rect.x = pg.mouse.get_pos()[0]
        self.rect.y = pg.mouse.get_pos()[1]
        self.cooldown += .1

    def fire(self, enemies):
        if self.cooldown > 4:
            self.shot.play()
            self.cooldown = 0
            for enemy in enemies:
                if enemy.rect.contains(self.rect):
                    enemy.kill()

class Game:
    def __init__(self):
        pg.init()
        mixer.init()
        self.screen = pg.display.set_mode((1200, 800))
        pg.mouse.set_visible(False)
        self.clock = pg.time.Clock()
        self.state = 'home'
        self.FPS = 60
        self.enemies = pg.sprite.Group()
        self.enemies.add(Enemy(100, 100, 0.4))
        self.enemies.add(Enemy(300, 300, 1))
        self.players = pg.sprite.Group()
        self.player = Player()
        self.players.add(self.player)
        self.home_font = pg.font.SysFont('Hack', 30)
        self.play_text = self.home_font.render('Play', True, pg.Color('white'))
        self.levels = [[[100, 100, .4], [400, 400, .5], [300, 200, 1]], [[400, 500, .9], [300, 200, .8]]]
        self.level = 0
        self.setup_level(self.level)

    def setup_level(self, level):
        self.enemies = pg.sprite.Group()
        for enemy in self.levels[level]:
            self.enemies.add(Enemy(enemy[0], enemy[1], enemy[2]))

    def handle_events(self, e):
        if self.state == 'home':
            if e.type == pg.MOUSEBUTTONDOWN:
                rect = self.play_text.get_rect()
                rect.x += 100
                rect.y += 100
                if rect.collidepoint(pg.mouse.get_pos()):
                    self.state = 'play'

        elif self.state == 'play':
            if e.type == pg.MOUSEBUTTONDOWN:
                self.player.fire(self.enemies)
                if len(self.enemies) <= 0:
                    self.level += 1
                    self.setup_level(self.level)
    
    def draw(self):
        if self.state == 'home':
            self.screen.fill('black')
            pg.mouse.set_visible(True)
            self.screen.blit(self.play_text, (100, 100))
        elif self.state == 'play':
            self.screen.fill('black')
            self.players.draw(self.screen)
            self.player.update()
            self.enemies.draw(self.screen)
            self.enemies.update()

    def run(self):
        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                else:
                    self.handle_events(e)
            self.draw()
            pg.display.update()
            self.clock.tick(self.FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
