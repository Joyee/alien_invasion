import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

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

def update_screen(ai_settings, screen, ship, aliens, bullets):
  """更新屏幕上的图像，并切换到新屏幕"""
  # 每次循环时都重绘屏幕
  screen.fill(ai_settings.bg_color)
  for bullet in bullets.sprites():
    bullet.draw_bullet()
  ship.blitme()
  # alien.blitme()
  aliens.draw(screen)
  
  # 让最近绘制的屏幕可见
  pygame.display.flip() # 在这里，它在每次执行while循环时都绘制一个空屏幕，并擦去旧屏幕，使得只有新屏幕可见。
  
def update_bullets(ai_settings, screen, ship, aliens, bullets):
  # 删除已消失的子弹
  for bullet in bullets.copy():
    if bullet.rect.bottom <= 0:
      bullets.remove(bullet)
  check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets)
  
def fire_bullet(ai_settings, screen, ship, bullets):
  """如果还没有到达限制，就发射一颗子弹"""
  if len(bullets) < ai_settings.bullet_allowed:
    new_bullet = Bullet(ai_settings, screen, ship)
    bullets.add(new_bullet)
    
def create_fleet(ai_settings, screen, ship, aliens):
  """创建外星人群"""
  # 创建一个外星人，并计算一行可容纳多少个外星人
  # 外星人间距为外星人宽度
  alien = Alien(ai_settings, screen)
  alien_width = alien.rect.width
  number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
  number_rows = get_number_aliens_rows(ai_settings, ship.rect.height, alien.rect.height)
  
  # 创建外星人群
  for row_number in range(number_rows):
    # 创建第一行外星人
    for alien_number in range(number_aliens_x):
      create_alien(ai_settings, screen, aliens, alien_number, row_number)
    
def get_number_aliens_x(ai_settings, alien_width):
  available_space_x = ai_settings.screen_width - 2 * alien_width
  number_aliens_x = int(available_space_x / (2 * alien_width))
  return number_aliens_x

def get_number_aliens_rows(ai_settings, ship_height, alien_height):
  """计算屏幕可容纳多少行外星人"""
  available_sapce_y = ai_settings.screen_height - 3 * alien_height - ship_height
  number_rows = int(available_sapce_y / (2 * alien_height))
  return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
  """创建一个外星人并将其加入当前行"""
  alien = Alien(ai_settings, screen)
  alien_width = alien.rect.width
  alien_height = alien.rect.height
  alien.x = alien_width + 2 * alien_width * alien_number
  alien.rect.x = alien.x
  alien.rect.y = alien_height + 2 * alien_height * row_number
  aliens.add(alien)
  
def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
  """检查是否有外星人位于屏幕边缘，并更新外星人群中所有外星人的位置"""
  check_fleet_edges(ai_settings, aliens)
  aliens.update()
  
  # 检测外星人和飞船之间的碰撞
  if pygame.sprite.spritecollideany(ship, aliens): # 如果没有发生碰撞 spritecollideany()将返回None
    ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    
  check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)
  
def change_fleet_direction(ai_settings, aliens):
  for alien in aliens.sprites():
    alien.rect.y += ai_settings.fleet_drop_speed
  ai_settings.fleet_direction *= -1
    
def check_fleet_edges(ai_settings, aliens):
  """有外星人到达边缘时采取相应的措施"""
  for alien in aliens.sprites():
    if alien.check_edges():
      change_fleet_direction(ai_settings, aliens)
      break
    
def check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets):
  """响应子弹和外星人的碰撞"""
  # pygame.sprite.groupcollide(group1, group2, dokill1, dokill2, collided = None)
  # group1 和 group2：需要检测碰撞的两个精灵组
  # dokill1 和 dokill2 这是两个布尔值，如果设置为 True，当碰撞发生时，相应的精灵将被自动从其组中删除。
  # collided：这是一个可选参数，用于指定用于计算碰撞的函数。如果没有指定，将使用每个精灵的 rect 属性进行碰撞检测。
  collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
  
  if len(aliens) == 0:
    # 删除现有的子弹并新建一群外星人
    bullets.empty()
    create_fleet(ai_settings, screen, ship, aliens)
    
def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
  """响应被外星人撞到的飞船"""
  if stats.ships_left > 0:
    # 将ships_left减1
    stats.ships_left -= 1
    
    # 清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()
    
    # 创建一群新的外星人，并将飞船放到屏幕底端中央
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()
    
    # 暂停
    sleep(0.5)
  else:
    stats.game_active = False
  
def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
  """检查是否有外星人到达了屏幕底端"""
  screen_rect = screen.get_rect()
  for alien in aliens.sprites():
    if alien.rect.bottom >= screen_rect.bottom:
      # 像飞船被撞到一样进行处理
      ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
      break