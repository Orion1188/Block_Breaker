from numpy import sign
import pygame
import pygame_menu
import os

# path

PATH = os.path.dirname(__file__)

# setup

pygame.init()
FPS = 60
clock = pygame.time.Clock()

# game screen

sc_width, sc_height = 1280, 720
screen = pygame.display.set_mode((sc_width, sc_height))

# sounds

BORDER_HIT_SOUND = pygame.mixer.Sound(f"{PATH}/border_hit.wav")
BRICK_HIT_SOUND = pygame.mixer.Sound(f"{PATH}/brick_hit.wav")
MENULOOP = pygame.mixer.music.load(f"{PATH}/menuloop.mp3")
BORDER_HIT_SOUND.set_volume(0.25)
BRICK_HIT_SOUND.set_volume(0.8)
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.12)

def game():
    pygame.mixer.music.pause()
    pygame.mouse.set_visible(False)
    class Border(pygame.sprite.Sprite):
        def __init__(self, x_pos, y_pos, texture_path):
            super().__init__()
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.image = pygame.image.load(texture_path)
            self.rect = self.image.get_rect(topleft=(x_pos, y_pos))

    class Brick(pygame.sprite.Sprite):
        def __init__(self, x_pos, y_pos, texture_path):
            super().__init__()
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.image = pygame.image.load(texture_path)
            self.rect = self.image.get_rect(topleft=(x_pos, y_pos))

    class Paddle(pygame.sprite.Sprite):
        def __init__(self, texture_path):
            super().__init__()
            self.image = pygame.image.load(texture_path)
            self.rect = self.image.get_rect(topleft=(600, 695))
        def move(self):
            if pygame.mouse.get_pos()[0] >= 40 + 75 and pygame.mouse.get_pos()[0] <= 1240 - 75:
                self.rect.center = pygame.mouse.get_pos()[0], 695
            elif pygame.mouse.get_pos()[0] < 40 + 75:
                self.rect.center = 40 + 75, 695
            else:
                self.rect.center = 1240 - 75, 695

    class Ball(pygame.sprite.Sprite):
        def __init__(self, x_pos, y_pos, texture_path, x_speed, y_speed, running = False):
            super().__init__()
            self.image = pygame.image.load(texture_path)
            self.rect = self.image.get_rect(topleft=(x_pos, y_pos))
            self.running = running
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.x_speed = x_speed
            self.y_speed = y_speed
        def update(self):
            self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))

    class Score(pygame.font.Font):
        def __init__(self, value=0):
            self.value = value
            self.text = gamefont.render(f"Score: {self.value}", True, (255, 255, 255))
        def update(self):
            self.text = gamefont.render(f"Score: {self.value}", True, (255, 255, 255))
            screen.blit(self.text, (80, 10))

    class Lives(pygame.font.Font):
        def __init__(self, value=3):
            self.value = value
            self.text = gamefont.render(f"Lives: {self.value}", True, (255, 255, 255))
        def update(self):
            self.text = gamefont.render(f"Lives: {self.value}", True, (255, 255, 255))
            screen.blit(self.text, (1100, 10))

    class Level(pygame.font.Font):
        def __init__(self, value=0):
            self.value = value
            self.text = gamefont.render(f"Level {self.value}", True, (255, 255, 255))
        def update(self):
            self.text = gamefont.render(f"Level {self.value}", True, (255, 255, 255))
            screen.blit(self.text, (1100, 50))

    def kill_player(ball, lives, level):
        if level.value != level_count:
            ball.running = False
            ball.x_pos, ball.y_pos = 675, 679
            ball.x_speed, ball.y_speed = 6, -6
            lives.value -= 1  

    def ball_movement(ball, border_group, paddle_group, bricks_group, score):
        if ball.running == True:
            ball.x_pos += ball.x_speed
            ball.y_pos += ball.y_speed
            if pygame.sprite.spritecollide(ball, border_group, False): #uderzenie o ścianę
                BORDER_HIT_SOUND.play()
                ball.x_speed *= -1
                ball.x_pos += 12 * sign(ball.x_speed)
            if ball.y_pos <= 0 or (ball.y_pos > 677 and pygame.sprite.spritecollide(ball, paddle_group, False)):
                BORDER_HIT_SOUND.play()
                ball.y_speed *= -1
            if pygame.sprite.spritecollide(ball, bricks_group, False) and pygame.sprite.spritecollideany(ball, bricks_group) != None:
                score.value += 50
                brick = pygame.sprite.spritecollideany(ball, bricks_group)
                pygame.sprite.Sprite.kill(brick)
                BRICK_HIT_SOUND.play()

            # ball trajectory after hitting a brick
                case1, case2, case3, case4 = False, False, False, False
                if brick.x_pos - 16 <= ball.x_pos <= brick.x_pos - 0 and brick.y_pos - 16 <= ball.y_pos <= brick.y_pos + 25: #lewy bok
                    case1 = True
                    ball.x_speed *= -1
                    ball.x_pos += 2 * ball.x_speed
                if brick.x_pos + 36 <= ball.x_pos <= brick.x_pos + 50 and brick.y_pos - 16 <= ball.y_pos <= brick.y_pos + 25: #prawy bok
                    case2 = True
                    ball.x_speed *= -1
                    ball.x_pos += 2 * ball.x_speed
                if brick.y_pos - 16 <= ball.y_pos <= brick.y_pos - 0 and brick.x_pos - 16 <= ball.x_pos <= brick.x_pos + 50: #
                    case3 = True
                    ball.y_speed *= -1
                    ball.y_pos += 2 * ball.y_speed
                if brick.y_pos + 9 <= ball.y_pos <= brick.y_pos + 25 and brick.x_pos - 16 <= ball.x_pos <= brick.x_pos + 50: #dół
                    case4 = True
                    ball.y_speed *= -1
                    ball.y_pos += 2 * ball.y_speed 
            # when player loses
            if ball.y_pos > 720:
                kill_player(ball, lives, level)
                if lives.value > 0:
                    ball = Ball(675, 679, f"{PATH}/ball.png", 6, -6)
        else:
            ball.x_pos = paddle.rect.center[0] - 8 

    #levels
    level_count = 3 # number of levels +1
    
    def board_1():
        ball.running = False
        ball.x_pos, ball.y_pos = 675, 679
        ball.x_speed, ball.y_speed = 6, -6
        for i in range(90, 1190, 100):
            brick = Brick(i, 200, bricksall[1])
            bricks_group.add(brick)
            bricks.append(brick)
        for i in range(140, 1190, 100):
            brick = Brick(i, 200, bricksall[4])
            bricks_group.add(brick)
            bricks.append(brick)


    def board_2():
        ball.running = False
        ball.x_pos, ball.y_pos = 675, 679
        ball.x_speed, ball.y_speed = 6, -6
        for i in range(90, 390, 50):
            brick = Brick(i, 200, bricksall[0])
            bricks_group.add(brick)
            bricks.append(brick)
        for i in range(390, 690, 50):
            brick = Brick(i, 225, bricksall[9])
            bricks_group.add(brick)
            bricks.append(brick)
        for i in range(690, 990, 50):
            brick = Brick(i, 250, bricksall[0])
            bricks_group.add(brick)
            bricks.append(brick)
        for i in range(90, 390, 50):
            brick = Brick(i, 125, bricksall[6])
            bricks_group.add(brick)
            bricks.append(brick)
        for i in range(390, 690, 50):
            brick = Brick(i, 150, bricksall[1])
            bricks_group.add(brick)
            bricks.append(brick)
        for i in range(690, 990, 50):
            brick = Brick(i, 175, bricksall[8])
            bricks_group.add(brick)
            bricks.append(brick)

    ########## SPRITES / GAME ELEMENTS

    # borders

    border_left = Border(0, 0, f"{PATH}/border_left.png")
    border_right = Border(1240, 0, f"{PATH}/border_right.png")

    border_group = pygame.sprite.Group()
    border_group.add(border_left)
    border_group.add(border_right)

    # paddle

    paddle = Paddle(f"{PATH}/paddle.png")

    paddle_group = pygame.sprite.Group()
    paddle_group.add(paddle)

    # ball

    ball = Ball(675, 679, f"{PATH}/ball.png", 6, -6)

    ball_group = pygame.sprite.Group()
    ball_group.add(ball)

    # bricks

    bricksall = [] #all brick textures
    bricksall.append(f"{PATH}/brick_black.png") #0
    bricksall.append(f"{PATH}/brick_red.png") #1
    bricksall.append(f"{PATH}/brick_orange.png") #2
    bricksall.append(f"{PATH}/brick_yellow.png") #3
    bricksall.append(f"{PATH}/brick_green.png") #4
    bricksall.append(f"{PATH}/brick_aqua.png") #5
    bricksall.append(f"{PATH}/brick_blue.png") #6
    bricksall.append(f"{PATH}/brick_purple.png") #7
    bricksall.append(f"{PATH}/brick_pink.png") #8
    bricksall.append(f"{PATH}/brick_white.png") #9

    bricks = []
    bricks_group = pygame.sprite.Group()

    # fonts

    gamefont = pygame.font.SysFont("Arial", 30)

    # score/lives/level count

    score = Score()
    lives = Lives()
    level = Level()

    # game loop
    board = 1
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    ball.running = True
                    if lives.value <= 0 or level.value == 3:
                        run = False

        if not bricks_group and lives.value != 0 and level.value != level_count: # if current level gets cleared
            if board == 1:
                board_1()
            if board == 2:
                board_2()
            board += 1
            level.value += 1
    
        if lives.value <= 0 and level.value != level_count: # if player loses all lives
            paddle_group.empty()
            ball_group.empty()
            bricks_group.empty()
            endscreen = pygame.image.load(f"{PATH}/endscreen_lose.png")
            screen.blit(endscreen, (390, 210))
            message = gamefont.render(f"Press right mouse button to continue", True, (255, 255, 255))
            screen.blit(message, (440, 530))
    
        if level.value == level_count: #if player beats last level
            paddle_group.empty()
            ball_group.empty()
            bricks_group.empty()
            endscreen = pygame.image.load(f"{PATH}/endscreen_win.png")
            screen.blit(endscreen, (390, 210))
            message = gamefont.render(f"Press right mouse button to continue", True, (255, 255, 255))
            screen.blit(message, (440, 530))

        pygame.display.flip()

        screen.fill((0, 0, 0))
        border_group.draw(screen)
        paddle_group.draw(screen)
        ball_group.draw(screen)
        bricks_group.draw(screen)

        ball_movement(ball, border_group, paddle_group, bricks_group, score)
        score.update()
        ball.update()
        lives.update()
        level.update()
        paddle.move()
    if lives.value <= 0 or level.value == level_count:
        save_score(score.value, lives.value)

def rules():
    rules = pygame_menu.Menu("Rules", 1280, 720, theme=pygame_menu.themes.THEME_DARK)
    rules.add.label("The goal is to destroy every brick on each level")
    rules.add.label("Use mouse to move the paddle and left click to release the ball")
    rules.add.button("Return to main menu", menu, margin=(0,400))
    rules.mainloop(screen)

def author():
    author = pygame_menu.Menu("Author", 1280, 720, theme=pygame_menu.themes.THEME_DARK)
    author.add.label("Game created by Oskar Matysik")
    author.add.button("Return to main menu", menu, margin=(0,400))
    author.mainloop(screen)

def save_score(score, lives):
    pygame.mixer.music.unpause()
    def save():
        allscores_file = open(f"{PATH}/allscores.txt", 'a')
        allscores_file.write(f"{player_name.get_value()} {total_score}")
        allscores_file.write("\n")
        allscores_file.close()
        leaderboards()

    total_score = score + lives * 1000
    scoreadd = pygame_menu.Menu("Your Score", 1280, 720, theme=pygame_menu.themes.THEME_DARK)
    scoreadd.add.label("Enter Your Name")
    player_name = scoreadd.add.text_input("")
    scoreadd.add.label(f"Score: {score}")
    scoreadd.add.label(f"Lives score: {lives * 1000}")
    scoreadd.add.label(f"Total score: {total_score}")
    scoreadd.add.button("Continue", save)
    scoreadd.mainloop(screen)

def leaderboards():
    def create_highscore_file():
        highscores = open(f"{PATH}/highscores.txt", 'w')
        scores = []
        allscores = open(f"{PATH}/allscores.txt", 'r')
        for line in allscores:
            scores.append(line.split())
        for i in range(len(scores)):
            scores[i][1] = int(scores[i][1])
        for i in range(10):
            maxscore = -1
            maxscorename = ""
            for score in scores:
                if score[1] > maxscore:
                    maxscore = score[1]
                    maxscorename = score[0]
            highscores.write(f"{maxscorename} {maxscore}\n")
            scores.remove([maxscorename, maxscore])
        allscores.close()
        highscores.close()

    create_highscore_file()
    highscores_file = open(f"{PATH}/highscores.txt", 'r')
        
    lboards = pygame_menu.Menu("High Scores", 1280, 720, theme=pygame_menu.themes.THEME_DARK)
    leaderboard = lboards.add.table()
    leaderboard.default_cell_padding = 7
    leaderboard.add_row(["Rank", "Name", "Total Score"])
    for i in range(1, 11):
        score = highscores_file.readline().split()
        leaderboard.add_row([i, score[0], score[1]])
    lboards.add.button("Return to main menu", menu)
    lboards.mainloop(screen)

def menu():
    pygame.mixer.music.unpause()
    menu = pygame_menu.Menu("Block Breaker", 1280, 720, theme=pygame_menu.themes.THEME_DARK)
    menu.add.button("Play", game)
    menu.add.button("Game Rules", rules)
    menu.add.button("Highest Scores", leaderboards)
    menu.add.button("Author", author)
    menu.add.button("Quit", pygame.quit)
    menu.mainloop(screen)

menu()