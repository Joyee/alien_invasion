import sys

import pygame

from settings import Settings

from ship import Ship

import game_functions as gf

from pygame.sprite import Group

# 首先创建一个空的Pygame窗口，供后面用来绘制游戏
# 元素，如飞船和外星人。我们还将让这个游戏响应用户输入、设置背景色以及加载飞船图像。
def run_game():
  # 初始化游戏并创建一个屏幕对象
  pygame.init()
  ai_settings = Settings()
  screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height)) # 宽1200px 高800px screen是一个surface，在Pygame中，surface是屏幕的一部分，用于显示游戏元素。在这个游戏中，每个元素(如外星人或飞船)都是一个surface。display.set_mode()返回的surface表示整个游戏窗口。激活游戏的动画循环后，每经过一次循环都将自动重绘这个surface。
  pygame.display.set_caption("Alien Invasion")
  
  # 创建一艘飞船
  ship = Ship(ai_settings, screen)
  # 创建一个用于存储子弹的编组
  bullets = Group()
  
  # 开始游戏的主循环
  while True:
    # 监视键盘和鼠标事件
    gf.check_events(ai_settings, screen, ship, bullets)
    ship.update()
    bullets.update()
    gf.update_bullets(bullets)
    gf.update_screen(ai_settings, screen, ship, bullets)
    
run_game()