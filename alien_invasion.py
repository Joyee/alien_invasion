import sys

import pygame

from settings import Settings

from ship import Ship

import game_functions as gf

# 首先创建一个空的Pygame窗口，供后面用来绘制游戏
# 元素，如飞船和外星人。我们还将让这个游戏响应用户输入、设置背景色以及加载飞船图像。
def run_game():
  # 初始化游戏并创建一个屏幕对象
  pygame.init()
  ai_settings = Settings()
  screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height)) # 宽1200px 高800px screen是一个surface，在Pygame中，surface是屏幕的一部分，用于显示游戏元素。在这个游戏中，每个元素(如外星人或飞船)都是一个surface。display.set_mode()返回的surface表示整个游戏窗口。激活游戏的动画循环后，每经过一次循环都将自动重绘这个surface。
  pygame.display.set_caption("Alien Invasion")
  
  # 创建一艘飞船
  ship = Ship(screen)
  
  # 开始游戏的主循环
  while True:
    # 监视键盘和鼠标事件
    gf.check_events()
    
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    
    # 让最近绘制的屏幕可见
    pygame.display.flip() # 在这里，它在每次执行while循环时都绘制一个空屏幕，并擦去旧屏幕，使得只有新屏幕可见。
    
run_game()