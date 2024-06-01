import  sys, pygame
from random import randint

class Star(object):
    speed = 1
    warp = False

    @classmethod
    def set_midpoints(cls, mid_x, mid_y):
        cls.mid_x = mid_x
        cls.mid_y = mid_y

    
    def __init__(self):
        self.x = randint(-mid_x, mid_x)
        self.y = randint(-mid_y, mid_y)
        self.z = randint(1, self.mid_x) + Star.speed
        self.r = 1
        self.prev_z = self.z


    def plot(self):
        offset_x = int((self.x / self.z) * 100)
        offset_y = int((self.y / self.z) * 100)
        offset_r = int((self.r / self.z) * 200)
        pygame.draw.circle(pygame.display.get_surface(),
                           (255, 255, 255),
                           (offset_x+Star.mid_x, offset_y+Star.mid_y),
                           offset_r)
        if Star.warp:
            offset_px = int((self.x / self.prev_z) * 100)
            offset_py = int((self.y / self.prev_z) * 100)
            pygame.draw.line(pygame.display.get_surface(),
                             (255, 255, 255),
                             (offset_px+Star.mid_x, offset_py+Star.mid_y),
                             (offset_x+Star.mid_x, offset_y+Star.mid_y))
        self.prev_z = self.z

    def update(self):
        self.z -= Star.speed
        if self.z <= 0:
            self.z = randint(1, self.mid_x)
            self.x = randint(-Star.mid_x, Star.mid_x)
            self.y = randint(-Star.mid_y, Star.mid_y)
            self.z = randint(1, self.mid_x) + Star.speed
            self.prev_x = self.x
            self.prev_y = self.y
            self.r = 1
        self.plot()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 2000, 1600
    mid_x = width // 2
    mid_y = height // 2
    
    black = 0, 0, 0
    white = 255, 255, 255
    
    screen = pygame.display.set_mode(size)
    screen.fill(black)
    
    Star.set_midpoints(mid_x, mid_y)
    stars = []
    for s in range (100):
        stars.append(Star())
        stars[s].plot()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                Star.speed = round((mx / Star.mid_x) * 2)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                b_left, b_right, b_mid = pygame.mouse.get_pressed(num_buttons=3)
                if b_left:
                    Star.warp = True
            elif event.type == pygame.MOUSEBUTTONUP:
                b_left, b_right, b_mid = pygame.mouse.get_pressed(num_buttons=3)
                if not b_left:
                    Star.warp = False

        screen.fill(black)
        for s in stars:
            s.update()
        pygame.display.flip()