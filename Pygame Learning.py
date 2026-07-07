# Importing the pygame library
import pygame
pygame.init()

# ------------------------------window setup------------------------------
# Setting screen size
win_width = 750
win_height = 750

# naming the window
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Demo Platformer')
# ------------------------------------------------------------------------

# ------------------------------loading images------------------------------
dirt_img = pygame.image.load('images/dirt.png')
player_img = pygame.image.load('images/white_character_square.png')
restart_img = pygame.image.load('images/restart.jpg')
start_img = pygame.image.load('images/start.jpg')
quit_img = pygame.image.load('images/quit.jpg')
# --------------------------------------------------------------------------

# ------------------------------loading fonts------------------------------
title_font = pygame.font.SysFont('Bauhaus 93', 50)
# -------------------------------------------------------------------------

# ------------------------------defining colours------------------------------
white = (255,255,255)
black = (0,0,0)
# ---------------------------------------------------------------------------

# ------------------------------general game variables------------------------------
start_menu = True
# ----------------------------------------------------------------------------------

# making a function to draw text on the screen
def draw_text(text, font, colour, x, y):
    img = font.render(text, True, colour)
    win.blit(img, (x, y))

# ------------------------------world setup------------------------------
lvl1_data = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,1,1,1],
    [1,0,0,0,0,0,1,1,1,1],  
    [1,0,0,0,0,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1]
]

tile_size = 75

class World():
    def __init__(self,data):
        self.tile_list = []

        row_count = 0
        for row in data:
            column_count = 0
            for tile in row:
                if tile == 1:
                    self.img = pygame.transform.scale(dirt_img, (tile_size,tile_size))
                    self.rect = self.img.get_rect()
                    self.rect.x = column_count * tile_size
                    self.rect.y = row_count * tile_size
                    tile = (self.img,self.rect)
                    self.tile_list.append(tile)
                column_count += 1
            row_count += 1
        
    def draw(self):
        for tile in self.tile_list:
            win.blit(tile[0],tile[1])
#-----------------------------------------------------------------------

# ------------------------------character setup------------------------------
class Player():
    def __init__(self, x, y):
        self.start(x, y)

    def update(self):
        dx = 0
        dy = 0

        # player movement
        key = pygame.key.get_pressed()
        
        if key[pygame.K_LEFT]:
            dx -= self.vel
        if key[pygame.K_RIGHT]:
            dx += self.vel
        if key[pygame.K_UP] and self.jump_vel == 0:
            self.jump_vel = -15.1

        # gravity
        self.jump_vel += 1
        if self.jump_vel > 15:
            self.jump_vel = 15
        dy += self.jump_vel

        # checking for collision
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # if jumping, if hits head
                if self.jump_vel < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.jump_vel = 0.1
                # if falling, if hits the ground
                elif self.jump_vel >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.jump_vel = 0

        # update coordinates
        self.rect.x += dx
        self.rect.y += dy

        # drawing character onto screen
        win.blit(self.img,self.rect)

    def start(self, x, y):
        self.img = pygame.transform.scale(player_img,(tile_size,tile_size*1.75))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.vel = 5
        self.jump_vel = 0
# ---------------------------------------------------------------------------

# ------------------------------button setup------------------------------
class Button():
    def __init__(self, x, y, image, width, height):
        self.img = pygame.transform.scale(image,(width, height))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        # store mouse position in 'pos'
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked == True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked == False

        win.blit(self.img, self.rect)

        return action
# ------------------------------------------------------------------------

# Setting the starting x and y positions of the character
x = 100
y = 650

# loading level 1
world = World(lvl1_data)

# loading player
player = Player(x,y)

# loading restart button
restart_button = Button(win_width - tile_size + tile_size*0.25/2, tile_size*0.25/2, restart_img, tile_size*0.75, tile_size*0.75)

# loading start and quit buttons for the start menu
start_button = Button(win_width / 2, win_height / 2 - 100, start_img, tile_size*3, tile_size)
quit_button = Button(win_width / 2, win_height / 2 + 100, quit_img, tile_size*3, tile_size)


# Game loop
run = True
while run:
    pygame.time.delay(17)
    
    # stops the game when the window closes
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # setting background colour
    win.fill(black)

    if start_menu:
        draw_text('Demo Platformer', title_font, white, win_width / 2 - 200, 100)

        if start_button.draw():
            start_menu = False
        if quit_button.draw():
            run = False
    else:
        # drawing the level onto the screen
        world.draw()

        # updating player
        player.update()

        # drawing restart button
        if restart_button.draw():
            player.start(x, y)

    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
        run = False

    # updates the game constantly so that the drawings appear and change
    pygame.display.update()

pygame.quit
exit()