import pygame

pygame.init()
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Treasure Hunting Game")
clock = pygame.time.Clock()
player = pygame.Rect((300, 250, 50, 50))
font1 = pygame.font.Font("font/superpixelfont.ttf", 50)

sky1_surface = pygame.image.load("graphics/pixelsky.png")
ground1_surface = pygame.image.load("graphics/ground1.png")
text1_surface = font1.render("Its fanta", False, "Black")

run = True
while run:
  screen.fill((0, 0, 0))
  screen.blit(sky1_surface,(0,0))
  screen.blit(ground1_surface,(0,350))
  screen.blit(text1_surface, (500, 100))
  pygame.draw.rect(screen, (255, 0, 0), player)
 
  key = pygame.key.get_pressed()
  if key[pygame.K_a] == True:
    player.move_ip(-1,0)
  if key[pygame.K_d] == True:
    player.move_ip(1,0)
  if key[pygame.K_w] == True:
    player.move_ip(0,-1)
  if key[pygame.K_s] == True:
    player.move_ip(0,1)
 
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
 
  pygame.display.update()
  clock.tick(60)
pygame.quit()