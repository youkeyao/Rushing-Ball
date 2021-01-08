import pygame
import sys
import random
import math
from Ball import *

if __name__ == '__main__':
    pygame.init()

    #加载图片
    bg_image = 'picture/background.png'
    redball_image = 'picture/redball.png'
    greenball_image = 'picture/greenball.png'

    #加载背景音乐
    pygame.mixer.music.load("music/bg_music.mp3")
    pygame.mixer.music.play()

    #加载音效
    win_sound = pygame.mixer.Sound("music/win.wav")
    current_sound = pygame.mixer.Sound("music/current.wav")
    hole_sound = pygame.mixer.Sound("music/hole.wav")

    #状态
    pressing = False
    win = False

    #自定义事件
    MusicContinue = pygame.USEREVENT
    pygame.mixer.music.set_endevent(MusicContinue)

    #画面
    bg_size = width, height = 992, 611
    screen = pygame.display.set_mode(bg_size)
    pygame.display.set_caption("Rushing Ball")

    background = pygame.image.load(bg_image).convert_alpha()

    #参数
    BALL_NUM = 5
    black_hole = [(121, 123, 131, 133), (225, 227, 362, 364), (465, 467, 259, 261), (661, 663, 131, 133), (840, 842, 422, 424)]
    win_font = pygame.font.SysFont('宋体', 50)
    win_text = win_font.render('YOU WIN', True, (0, 0, 0))

    #是否可碰撞
    cancolide = [[1 for i in range(BALL_NUM)] for j in range(BALL_NUM)]

    #泡
    balls = []
    group = pygame.sprite.Group()

    for i in range(BALL_NUM):
        position = random.randint(0, width - 60), random.randint(0, height - 60)
        speed = [random.randint(-10, 10), random.randint(-10, 10)]
        ball = Ball(redball_image, greenball_image, position, speed, bg_size)
        while pygame.sprite.spritecollide(ball, group, False, pygame.sprite.collide_circle):
            ball.rect.left, ball.rect.top = random.randint(0, width - 60), random.randint(0, height - 60)
        balls.append(ball)
        group.add(ball)

    clock = pygame.time.Clock()

    while True:
        #事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MusicContinue and not win:
                pygame.mixer.music.play()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mouse.set_cursor(*pygame.cursors.broken_x)
                pressing = True
            elif event.type == pygame.MOUSEBUTTONUP:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
                pressing = False
        
        screen.blit(background, (0, 0))

        #画泡
        for each in balls:
            screen.blit(each.image, each.rect)
            if not each.isfixed:
                each.move(group)
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                dx = x - each.rect.center[0]
                dy = y - each.rect.center[1]
                d = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
                #画线
                if pressing and 0 < d and d < 120:
                    pygame.draw.line(screen, (0, 0, 255), (each.rect.center[0], each.rect.center[1]), (x, y), 2)
                    each.speed[0] += 0.1 * dx/d
                    each.speed[1] += 0.1 * dy/d
                    current_sound.play()
                    #进洞
                    for dest in black_hole:
                        if dest[0] <= each.rect.left and each.rect.left <= dest[1] and\
                            dest[2] <= each.rect.top and each.rect.top <= dest[3]:
                            current_sound.stop()
                            hole_sound.play()
                            black_hole.remove(dest)
                            each.fix()
                            each.rect.left = dest[0] + 1
                            each.rect.top = dest[2] + 1
                            tmp = balls.pop(balls.index(each))
                            balls.insert(0, tmp)

        #计算速度
        for i in range(BALL_NUM):
            if balls[i].isfixed:
                continue
            for j in range(i + 1, BALL_NUM):
                if balls[j].isfixed:
                    continue
                if pygame.sprite.collide_circle(balls[i], balls[j]):
                    vx1 = balls[i].speed[0]
                    vy1 = balls[i].speed[1]
                    vx2 = balls[j].speed[0]
                    vy2 = balls[j].speed[1]

                    dx = balls[i].rect.center[0] - balls[j].rect.center[0]
                    dy = balls[i].rect.center[1] - balls[j].rect.center[1]
                    d = math.sqrt(dx * dx + dy * dy)

                    if cancolide[i][j] and cancolide[j][i]:
                        balls[i].speed[0] = (vx1*dy*dy + vx2*dx*dx - vy1*dx*dy + vy2*dx*dy) / (dx*dx + dy*dy)
                        balls[i].speed[1] = (vy1*dx*dx + vy2*dy*dy - vx1*dx*dy + vx2*dx*dy) / (dx*dx + dy*dy)
                        
                        balls[j].speed[0] = (vx2*dy*dy + vx1*dx*dx - vy2*dx*dy + vy1*dx*dy) / (dx*dx + dy*dy)
                        balls[j].speed[1] = (vy2*dx*dx + vy1*dy*dy - vx2*dx*dy + vx1*dx*dy) / (dx*dx + dy*dy)
                        
                    cancolide[i][j] = cancolide[j][i] = 0
                else:
                    cancolide[i][j] = cancolide[j][i] = 1

        #胜利
        if not black_hole and not win:
            pygame.mixer.music.stop()
            win_sound.play()
            win = True

        if win:
            screen.blit(win_text, (430, 155))
    
        pygame.display.flip()

        clock.tick(60)