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

def check_events(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
  """响应按键和鼠标事件"""
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    elif event.type == pygame.KEYDOWN:
      check_keydown_events(event, ai_settings, screen, ship, bullets)
    elif event.type == pygame.KEYUP:
      check_keyup_events(event, ship)
    elif event.type == pygame.MOUSEBUTTONDOWN:
      mouse_x, mouse_y = pygame.mouse.get_pos()
      check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
  """更新屏幕上的图像，并切换到新屏幕"""
  # 每次循环时都重绘屏幕
  screen.fill(ai_settings.bg_color)
  for bullet in bullets.sprites():
    bullet.draw_bullet()
  ship.blitme()
  # alien.blitme()
  aliens.draw(screen)
  # 显示得分
  sb.show_score()
  
  # 如果游戏处于非活跃状态就绘制play按钮
  if not stats.game_active:
    play_button.draw_button()
  
  # 让最近绘制的屏幕可见
  pygame.display.flip() # 在这里，它在每次执行while循环时都绘制一个空屏幕，并擦去旧屏幕，使得只有新屏幕可见。
  
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
  # 删除已消失的子弹
  for bullet in bullets.copy():
    if bullet.rect.bottom <= 0:
      bullets.remove(bullet)
  check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets)
  
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
  
def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
  """检查是否有外星人位于屏幕边缘，并更新外星人群中所有外星人的位置"""
  check_fleet_edges(ai_settings, aliens)
  aliens.update()
  
  # 检测外星人和飞船之间的碰撞
  if pygame.sprite.spritecollideany(ship, aliens): # 如果没有发生碰撞 spritecollideany()将返回None
    ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
    
  check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)
  
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
    
def check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets):
  """响应子弹和外星人的碰撞"""
  # pygame.sprite.groupcollide(group1, group2, dokill1, dokill2, collided = None)
  # group1 和 group2：需要检测碰撞的两个精灵组
  # dokill1 和 dokill2 这是两个布尔值，如果设置为 True，当碰撞发生时，相应的精灵将被自动从其组中删除。
  # collided：这是一个可选参数，用于指定用于计算碰撞的函数。如果没有指定，将使用每个精灵的 rect 属性进行碰撞检测。
  collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
  
  # 随着游戏的进行 将提高每个外星人值的点数 为确保每次开始新游戏时这个值都会被重置，在initialize_dynamic_settings()中设置它
  # 有子弹碰撞到外星人时, Pygame返回一个字典(collisions)，检查这个字典是否存在，如果存在，将得分加上一个外星人值的点数
  if collisions:
    # 如果在一次循环中有两颗子弹射中了外星人，或者因子弹更宽而同时击中了多个外星人，玩家将只能得到一个被消灭的外星人的点数。
    # 与外星人碰撞的子弹都是字典collisions中的一个键；而与每颗子弹相关的值都是一个列表，其中包含该子弹撞到的外星人。
    for aliens in collisions.values():
      stats.score += ai_settings.alien_points * len(aliens) # 更新得分
      sb.prep_score()

    check_high_score(stats, sb)
  
  if len(aliens) == 0:
    # 删除现有的子弹并新建一群外星人，加快游戏节奏，并创建一群新的外星人
    bullets.empty()
    ai_settings.increase_speed()
    
    # 提高等级
    stats.level += 1
    sb.prep_level()
    
    create_fleet(ai_settings, screen, ship, aliens)
    
def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
  """响应被外星人撞到的飞船"""
  if stats.ships_left > 0:
    # 将ships_left减1
    stats.ships_left -= 1
    
    # 更新记分牌
    sb.prep_ships()
    
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
    pygame.mouse.set_visible(True)
  
def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
  """检查是否有外星人到达了屏幕底端"""
  screen_rect = screen.get_rect()
  for alien in aliens.sprites():
    if alien.rect.bottom >= screen_rect.bottom:
      # 像飞船被撞到一样进行处理
      ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
      break
    
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
  """在玩家单击Play按钮时开始新游戏"""
  button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
  if button_clicked and not stats.game_active:
    # 重置游戏设置
    ai_settings.initialize_dynamic_settings()
    # 隐藏光标
    pygame.mouse.set_visible(False)
    # 重置游戏统计信息
    stats.reset_stats()
    stats.game_active = True
    
    # 重置记分牌图像
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()
    
    # 清空外星人群和子弹列表
    aliens.empty()
    bullets.empty()
    
    # 创建一群新的外星人，并让飞船居中
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()
    
def check_high_score(stats, sb):
  """检查是否产生了新的最高得分"""
  if stats.score > stats.high_score:
    stats.high_score = stats.score
    sb.prep_high_score()