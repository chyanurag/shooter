import pygame as pg

class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface([100, 100])
        self.image.fill('red')
        self.rect = self.image.get_rect()

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface([5, 5])
        self.image.fill('blue')
        self.rect = self.image.get_rect()
    
    def update(self):
        self.rect.x = pg.mouse.get_pos()[0]
        self.rect.y = pg.mouse.get_pos()[1]

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1200, 800))
        pg.mouse.set_visible(False)
        self.clock = pg.time.Clock()
        self.state = 'home'
        self.FPS = 60
        self.enemies = pg.sprite.Group()
        self.enemies.add(Enemy())
        self.players = pg.sprite.Group()
        self.player = Player()
        self.players.add(self.player)

    def handle_events(self, e):
        pass
    
    def draw(self):
        self.screen.fill('black')
        self.enemies.draw(self.screen)
        self.enemies.update()
        self.players.draw(self.screen)
        self.players.update()

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
