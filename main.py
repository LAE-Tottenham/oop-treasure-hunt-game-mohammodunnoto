import pygame

pygame.init()
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Taz Fanta")
clock = pygame.time.Clock()

player_surface = pygame.image.load("graphics/twilight1.png").convert_alpha()
player_rect = player_surface.get_rect(midbottom = (100, 350))
font1 = pygame.font.Font("fonts/superpixelfont.ttf", 50)

sky1_surface = pygame.image.load("graphics/pixelsky.png").convert()
ground1_surface = pygame.image.load("graphics/ground1.png").convert()
text1_surface = font1.render("Its fanta", False, "Black")

taz_enemy_surface = pygame.image.load("graphics/enemies/idiotpixel.png").convert_alpha()
taz_enemy_rect = taz_enemy_surface.get_rect(bottomright = (1200,350))

run = True
while run:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    #if event.type == pygame.MOUSEMOTION:
    #  if player_rect.collidepoint(event.pos): print("Fanta")

  screen.fill((0, 0, 0))
  screen.blit(sky1_surface,(0,0))
  screen.blit(ground1_surface,(0,350))
  screen.blit(text1_surface, (315, 100))
  
  taz_enemy_rect.left -= 4
  if taz_enemy_rect.right <= 0: taz_enemy_rect.left = 1200
  screen.blit(taz_enemy_surface, taz_enemy_rect)
  screen.blit(player_surface, player_rect)

  #if player_rect.colliderect(taz_enemy_rect):
  #  print("its fanta")

  #mouse_pos = pygame.mouse.get_pos()
  #if player_rect.collidepoint(mouse_pos):
  #  print(pygame.mouse.get_pressed())
 
  key = pygame.key.get_pressed()
  if key[pygame.K_a] == True:
    player_rect.move_ip(-1,0)
  if key[pygame.K_d] == True:
    player_rect.move_ip(1,0)
  if key[pygame.K_w] == True:
    player_rect.move_ip(0,-1)
  if key[pygame.K_s] == True:
    player_rect.move_ip(0,1)
 
  pygame.display.update()
  clock.tick(60)
pygame.quit()