import random, sys
from macros import *
import __init__ as meta


class Item:
    def __init__(self, images):
        self.items_floor = []
        self.images      = images.values()

        self.reset()

    def reset(self):
        self.image = random.choice(self.images)
        self.size  = self.image.get_size()

        self.X = random.randint(0, RESOLUTION[WIDTH] - 200)
        self.Y = -self.size[HEIGHT]

        self.center_X = self.X + self.size[WIDTH] // 2
        self.dY = 20 + random.randint(-5, 5)

    @property
    def position(self):
        return self.X, self.Y

    def hit_collapsing_line(self):
        return self.Y + self.size[HEIGHT] >= Context.collapsing_line

    def hit_ground(self):
        return self.Y + self.size[HEIGHT] + self.dY >= RESOLUTION[HEIGHT]

    def collapsed(self, basket):
        return basket.X - basket.size[WIDTH] < self.X < basket.X + basket.size[WIDTH]

    def get_center(self):
        return self.center_X, self.Y

    def add_item_floor(self, shirt):
        sitting_shirt = self.ItemThumbnail(shirt)
        self.items_floor.append(sitting_shirt)

    def draw_items(self, screen):
        for shirt in self.items_floor:
            thumbnail = shirt.get_thumbnail()
            screen.blit(thumbnail[0], thumbnail[1])

    class ItemThumbnail:
        def __init__(self, shirt):
            self.image      = shirt.image
            self.position   = shirt.X, shirt.Y

        def get_thumbnail(self):
            return self.image, self.position


class Basket(object):
    standard_speed       = 3
    friction_coefficient = 1.5

    def __init__(self):
        self.images = Context.load_basket_images()
        self.image  = None

        self.load = 0
        self.size = self.image.get_size()

        self.X = -random.randint(750, 1300)
        self.Y = RESOLUTION[HEIGHT] - self.size[HEIGHT] - BOTTOM_PADDING

        self.centerY = self.Y + self.size[HEIGHT] // 2
        self.half_width = self.size[WIDTH] // 2

        self.direction  = 1
        self.dX         = 0

        self.speed      = self.standard_speed
        self.vel        = self.direction * self.speed

    def action(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.direction = -1
            elif event.key == pygame.K_d:
                self.direction = 1
        elif event.type == pygame.KEYUP:
            self.stop()

            pressed_ = pygame.key.get_pressed()
            if pressed_[pygame.K_a]:        #
                self.direction = -1         # solves double pressing bug
            elif pressed_[pygame.K_d]:      #
                self.direction = 1          #

        self.vel = self.direction * self.speed

    def move(self, runtime=True):
        friction = 0
        if self.vel == 0 and not self.dX == 0:
            friction = -self.dX // abs(self.dX) * self.friction_coefficient

        self.dX = int(self.dX + self.vel + friction)
        self.X  += self.dX

        if runtime:
            self.hit_edges()

    @property
    def position(self):
        return self.X, self.Y

    def entrance(self):
        if self.X > 0 and self.direction == 1:
            self.direction = -1
            self.vel = self.direction * self.speed
        elif self.dX < -30 and self.direction == -1:
            self.stop()

        self.move(False)

    def exit(self):
        if self.X + self.size[WIDTH] >= 0:
            self.dX -= self.standard_speed

    def hit_edges(self):
        hit_left    = self.X + self.dX < 0
        hit_right   = self.X + self.dX + self.size[WIDTH] >= RESOLUTION[WIDTH]
        if hit_left or hit_right:
            self.X = 0 if hit_left else RESOLUTION[WIDTH] - self.size[WIDTH]
            self.dX = -self.dX / 2

    def scores(self, context):
        if self.X + self.size[WIDTH] >= RESOLUTION[WIDTH] - 100:
            context.update_score(self.load)
            self.load = 0

    def update(self):
        if self._load < len(self.images):
            self.image = self.images[self._load]

    def get_center(self):
        return self.X + self.half_width, self.centerY

    def stop(self):
        self.direction = 0
        self.vel = 0

    @property
    def load(self):
        return self._load

    @load.setter
    def load(self, value):
        self._load = value
        if value == 0:
            self.speed = 3
        else:
            self.speed -= self.speed / 2
        self.update()


class Grandma(object):
    GRANDMA_STD_POSITION    = 1400, 400
    speed                   = 3

    def __init__(self):
        self.images = Context.load_grandma_images()
        self.image  = self.images[0]

        self.position = [RESOLUTION[WIDTH], self.GRANDMA_STD_POSITION[HEIGHT]]

    def at_position(self):
        return self.position[WIDTH] <= self.GRANDMA_STD_POSITION[WIDTH]

    def update(self, items_on_floor):
        if items_on_floor < len(self.images):
            self.image = self.images[items_on_floor]
        self.humor = items_on_floor

    def entrance(self):
        if self.position[WIDTH] > self.GRANDMA_STD_POSITION[WIDTH]:
            self.position[WIDTH] -= self.speed

    def exit(self):
        if self.position[WIDTH] <= RESOLUTION[WIDTH]:
            self.position[WIDTH] += self.speed


class Background:
    def __init__(self, images):
        self.background = images[IMG_BACKGROUND]
        self.foreground = images[IMG_FOREGROUND]

        self.cloud_manager = self.CloudManager(images[KEY_CLOUDS].values())
        self.cloud_manager.generate_cloud()

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        self.cloud_manager.move()

        if self.cloud_manager.clouds[len(self.cloud_manager.clouds) - 1][1][WIDTH] <= self.cloud_manager.create_next:
            self.cloud_manager.generate_cloud()

        clouds = self.cloud_manager.clouds
        for cloud in clouds:
            screen.blit(cloud[0], (cloud[1][WIDTH], cloud[1][HEIGHT]))

        screen.blit(self.foreground, (0, 0))

    class CloudManager:
        starting_X  = RESOLUTION[WIDTH]
        cluster_max = 3

        def __init__(self, images):
            self.images = images
            self.clouds = []

            self.create_next = 0

        def cloud_factory(self):
            image   = random.choice(self.images)
            dX      = -random.randint(1, 3) / 3
            position= self.starting_X, random.randint(-10, 400)

            return image, position, dX

        def generate_cloud(self):
            self.clouds.append(self.cloud_factory())
            self.create_next = random.randint(500, 1200)

        def move(self):
            temp_cloud = []
            for i in range(0, len(self.clouds)):
                cloud = self.clouds[i]
                temp_cloud.append((cloud[0], (cloud[1][WIDTH] + cloud[2], cloud[1][HEIGHT]), cloud[2]))

            self.clouds = temp_cloud

        def get_clouds(self):
            return self.clouds


class Context:
    fps             = FPS
    collapsing_line = RESOLUTION[HEIGHT]
    delivering_line = RESOLUTION[WIDTH] - 200   # right edge minus grandma's width
    center_screen   = RESOLUTION[WIDTH] // 2, RESOLUTION[HEIGHT] // 2
    best_score      = 0

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(RESOLUTION, pygame.HWSURFACE | pygame.DOUBLEBUF)

        pygame.display.set_caption(meta.__title__)

        self.font       = pygame.font.SysFont(FONT_TYPE, 50)
        self._images    = get_image_map()
        self.score      = 0

        self.audio_score    = load_audio(AUDIO_SCORE)
        self.audio_scream   = load_audio(AUDIO_OVER_SCREAM)
        self.audio_load     = load_audio(AUDIO_TAKE_ITEM)

        pygame.mixer.music.load(RES_AUDIO + AUDIO_MAIN_THEME)
        self.start_music()

    def get_image(self, key):
        return self._images[key]

    def draw_text(self):
        text_score      = TEXT_SCORE + str(self.score)
        text_best_score = TEXT_BEST_SCORE + str(self.best_score)

        surface_score       = self.font.render(text_score, False, FONT_COLOR)
        surface_best_score  = self.font.render(text_best_score, False, FONT_COLOR)

        self.screen.blit(surface_best_score, (50, 100))
        self.screen.blit(surface_score, (50, 50))

    def update_score(self, load):
        self.score += load
        if self.score > self.best_score:
            self.best_score = self.score

    @staticmethod
    def load_basket_images():
        basket_images = get_image_map()[KEY_BASKET]
        return (basket_images[IMG_BASKET_EMPTY],
                basket_images[IMG_BASKET_FULL],
                basket_images[IMG_BASKET_FULL_TOTAL],
                basket_images[IMG_BASKET_LOADED])

    @staticmethod
    def load_grandma_images():
        grandma_images = get_image_map()[KEY_GRANDMA]
        return (grandma_images[IMG_GRANDMA_UNHAPPY],
                grandma_images[IMG_GRANDMA_MAD],
                grandma_images[IMG_GRANDMA_ANGRY],
                grandma_images[IMG_GRANDMA_RAGED])

    @staticmethod
    def start_music():
        pygame.mixer.music.play(-1)

    @staticmethod
    def set_collapsing_line(height):
        Context.collapsing_line = RESOLUTION[HEIGHT] - height

    class Blinker:
        timer       = 0
        position    = 600, 500

        def __init__(self, screen, text, lap=30):
            self.screen = screen
            self.text   = text
            self.lap    = lap

        def update(self):
            self.timer += 1
            if self.timer < self.lap:
                self.screen.blit(self.text, self.position)
            elif self.timer == self.lap * 2:
                self.timer = 0

        def __del__(self):
            self.timer = 0


class Game:
    context     = Context()
    background  = Background(context.get_image(KEY_BACKGROUND))
    clock       = pygame.time.Clock()
    fps         = context.fps
    alpha       = 255

    def __init__(self):
        self.game_on    = True

        self.basket     = Basket()
        self.item       = Item(self.context.get_image(KEY_ITEMS))
        self.grandma    = Grandma()

        self.context.set_collapsing_line(self.basket.size[HEIGHT])
        self.fade_surface = pygame.Surface(RESOLUTION)

    def run(self):
        self.start()

        while self.game_on:
            self.event_loop()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.fps)

        return self.end()

    def event_loop(self):
        for event in pygame.event.get():
            if len(self.item.items_floor) >= 4:
                self.basket.stop()
                if self.basket.dX == 0:
                    self.game_on = False
            else:
                self.basket.action(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause()
            if event.type == pygame.QUIT:
                self.quit()

    def pause(self):
        text    = self.context.font.render(TEXT_PAUSE, False, FONT_COLOR)
        blinker = self.context.Blinker(self.context.screen, text)

        on_pause = True
        while on_pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        on_pause = False
                elif event.type == pygame.QUIT:
                    self.quit()

            self.draw()

            blinker.update()
            pygame.display.update()

            self.clock.tick(self.fps)

    def update(self):
        self.basket.move()
        self.basket.scores(self.context)

        print self.context.score
        if self.item.hit_collapsing_line():
            if self.item.collapsed(self.basket):
                self.basket.load += 1
                self.item.reset()
            elif self.item.hit_ground():
                self.item.add_item_floor(self.item)
                self.item.reset()

        self.item.Y = self.item.Y + self.item.dY

    def draw(self):
        self.background.draw(self.context.screen)
        self.item.draw_items(self.context.screen)

        self.grandma.update(len(self.item.items_floor))

        self.context.screen.blit(self.grandma.image, self.grandma.position)
        self.context.screen.blit(self.item.image, self.item.position)
        self.context.screen.blit(self.basket.image, self.basket.position)

        self.context.draw_text()

        pygame.display.flip()

    def start(self):
        text    = self.context.font.render(TEXT_START, False, FONT_COLOR)
        blinker = self.context.Blinker(self.context.screen, text)

        animation = True
        while animation:
            self.grandma.entrance()
            self.basket.entrance()

            self.background.draw(self.context.screen)

            self.context.screen.blit(self.grandma.image, self.grandma.position)
            self.context.screen.blit(self.basket.image, self.basket.position)

            if self.grandma.position[WIDTH] <= self.grandma.GRANDMA_STD_POSITION[WIDTH]:
                blinker.update()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            animation = False
                    elif event.type == pygame.QUIT:
                        self.quit()

            self.fade(-1)

            pygame.display.flip()
            pygame.display.update()

            self.clock.tick(self.fps)

    def end(self):
        self.context.score = 0

        over_images = get_image_map()[KEY_OVER]
        face_open   = over_images[IMG_OVER_FACE_OPEN]
        face_closed = over_images[IMG_OVER_FACE_CLOSED]

        face = face_closed
        body = over_images[IMG_OVER_BODY]

        face_position = [660, RESOLUTION[HEIGHT] + 100]

        text    = self.context.font.render(TEXT_LOST, False, (255, 255, 255))
        blinker = self.context.Blinker(self.context.screen, text)
        dir = 1
        dY = 0
        pressed_start = False

        animation = True
        while animation: # TODO improve this
            self.background.draw(self.context.screen)
            self.item.draw_items(self.context.screen)

            self.context.screen.blit(self.basket.image, self.basket.position)

            if blinker.timer % 10:
                dir = -dir

            face_position[WIDTH] += dir * (blinker.timer % 5)

            if self.grandma.position[WIDTH] >= RESOLUTION[WIDTH] and face_position[HEIGHT] >= 150:
                dY += 5
                face_position[HEIGHT] -= 5
                self.context.screen.blit(body, (0, RESOLUTION[HEIGHT] - dY))
                self.context.screen.blit(face, face_position)
            elif self.basket.dX == 0:
                self.grandma.exit()
                self.context.screen.blit(self.grandma.image, self.grandma.position)

            if face_position[HEIGHT] <= 150:
                self.context.screen.blit(body, (0, RESOLUTION[HEIGHT] - dY))
                self.context.screen.blit(face, face_position)
                if blinker.timer == blinker.lap:
                    face = face_open

            if face == face_open:
                self.basket.exit()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pressed_start = True
                elif event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                    self.quit()

            if pressed_start:
                self.fade()
            else:
                blinker.update()

            pygame.display.flip()
            pygame.display.update()

            self.clock.tick(self.fps)
            if self.alpha >= 255:
                return True
        return False

    def fade(self, multiplier=1):
        if 0 <= self.alpha <= 255:
            self.alpha += 8 * multiplier
            self.fade_surface.set_alpha(self.alpha)
            self.fade_surface.fill((0, 0, 0))
            self.context.screen.blit(self.fade_surface, (0, 0))
        elif self.alpha < 0:
            self.alpha = 0
        elif self.alpha > 255:
            self.alpha = 255

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()
