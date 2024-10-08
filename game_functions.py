import sys

import pygame

from bullet import Bullet

def check_keydown_events(event, ai_settings, screen, ship, bullets):
  if event.key == pygame.K_RIGHT:
    ship.moving_right = True
  elif event.key == pygame.K_LEFT:
    ship.moving_left = True
  elif event.key == pygame.K_SPACE:
    # 创建一颗子弹，并将其加入到编组bullets中
    fire_bullet(ai_settings, screen, ship, bullets)
  elif event.key == pygame.K_q:
    sys.exit()
    
def check_keyup_events(event, ship):
  if event.key == pygame.K_RIGHT:
    ship.moving_right = False
  elif event.key == pygame.K_LEFT:
    ship.moving_left = False

def check_events(ai_settings, screen, ship, bullets):
  """响应按键和鼠标事件"""
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    elif event.type == pygame.KEYDOWN:
      check_keydown_events(event, ai_settings, screen, ship, bullets)
    elif event.type == pygame.KEYUP:
      check_keyup_events(event, ship)

def update_screen(ai_settings, screen, ship, bullets):
  """更新屏幕上的图像，并切换到新屏幕"""
  # 每次循环时都重绘屏幕
  screen.fill(ai_settings.bg_color)
  for bullet in bullets.sprites():
    bullet.draw_bullet()
  ship.blitme()
  
  # 让最近绘制的屏幕可见
  pygame.display.flip() # 在这里，它在每次执行while循环时都绘制一个空屏幕，并擦去旧屏幕，使得只有新屏幕可见。
  
def update_bullets(bullets):
  # 删除已消失的子弹
  for bullet in bullets.copy():
    if bullet.rect.bottom <= 0:
      bullets.remove(bullet)
  
def fire_bullet(ai_settings, screen, ship, bullets):
  """如果还没有到达限制，就发射一颗子弹"""
  if len(bullets) < ai_settings.bullet_allowed:
    new_bullet = Bullet(ai_settings, screen, ship)
    bullets.add(new_bullet)