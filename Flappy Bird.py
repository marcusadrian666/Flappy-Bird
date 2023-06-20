# 导入pygame模块
import pygame
import random

# 初始化pygame
pygame.init()

# 设置窗口大小和标题
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Flappy Bird")

# 加载小鸟的图片，你可以自己选择
bird = pygame.image.load("bird.png")
bird_rect = bird.get_rect()
bird_rect.center = (100, 300)

# 加载柱子的图片，你可以自己选择，有8种柱子，随机循环出现
pipes = []
for i in range(1, 9):
    pipes.append(pygame.image.load(f"pipe{i}.png"))

# 创建柱子的矩形列表，每个矩形包含上下两根柱子
pipes_rects = []
for i in range(3):
    # 随机生成上下柱子的高度
    top_height = random.randint(100, 400)
    bottom_height = 600 - top_height - 100
    # 随机选择柱子的图片
    pipe_index = random.randint(0, 7)
    # 创建上下柱子的矩形，并设置初始位置
    top_rect = pipes[pipe_index].get_rect()
    top_rect.bottomleft = (800 + i * 300, top_height)
    bottom_rect = pipes[pipe_index].get_rect()
    bottom_rect.topleft = (800 + i * 300, top_height + 100)
    # 将上下柱子的矩形添加到列表中
    pipes_rects.append((top_rect, bottom_rect))

# 设置游戏的状态变量
running = True # 游戏是否运行中
jumping = False # 小鸟是否跳跃中
gravity = 0.5 # 重力加速度
velocity = 0 # 小鸟的垂直速度
score = 0 # 得分
font = pygame.font.SysFont("Arial", 32) # 字体

# 游戏主循环
while running:
    # 处理事件
    for event in pygame.event.get():
        # 如果点击了关闭按钮，退出游戏
        if event.type == pygame.QUIT:
            running = False
        # 如果按下了空格键，让小鸟跳跃
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            jumping = True
            velocity = -10

    # 更新游戏逻辑
    # 如果小鸟跳跃中，更新速度和位置，并检查是否落地或碰到柱子
    if jumping:
        velocity += gravity
        bird_rect.centery += velocity
        if bird_rect.top <= 0 or bird_rect.bottom >= 600:
            jumping = False
        for top_rect, bottom_rect in pipes_rects:
            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                jumping = False

    # 如果小鸟没有跳跃中，重置位置和速度，并显示游戏结束和得分信息
    else:
        bird_rect.center = (100, 300)
        velocity = 0
        screen.fill((135, 206, 235))
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(game_over_text, (350, 250))
        screen.blit(score_text, (350, 300))
        pygame.display.flip()
        pygame.time.wait(3000)
        score = 0

    # 更新柱子的位置，并检查是否超出屏幕或通过小鸟，如果是则重新生成或增加得分
    for i in range(3):
        pipes_rects[i][0].centerx -= 5
        pipes_rects[i][1].centerx -= 5
        if pipes_rects[i][0].right <= 0:
            top_height = random.randint(100, 400)
            bottom_height = 600 - top_height - 100
            pipe_index = random.randint(0, 7)
            pipes_rects[i][0].bottomleft = (800, top_height)
            pipes_rects[i][1].topleft = (800, top_height + 100)
        if pipes_rects[i][0].centerx == 100:
            score += 1

    # 绘制游戏画面
    # 填充背景颜色
    screen.fill((135, 206, 235))
    # 绘制小鸟
    screen.blit(bird, bird_rect)
    # 绘制柱子
    for i in range(3):
        screen.blit(pipes[pipe_index], pipes_rects[i][0])
        screen.blit(pipes[pipe_index], pipes_rects[i][1])
    # 绘制得分
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (700, 50))
    # 更新屏幕
    pygame.display.flip()

# 退出pygame
pygame.quit()
