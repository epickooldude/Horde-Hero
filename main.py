import pygame
import sys
pygame.init()
width = 600
height = 400
screen = pygame.display.set_mode((width, height))
#Background Size
bgSize = (600,400)
#Color
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
pink = (190,0,255)
#Player Size
playerSizes = (75,150)
zombieSize = (100,150)
#Lose Text
lose_font = pygame.font.Font("foul-fiend/Foul Fiend.ttf", 32)
lose_text = lose_font.render("YOU LOSE", True, red)
lose_textRect = lose_text.get_rect() 
lose_textRect.center = (150,150) 
#Win Text
win_font = pygame.font.Font("foul-fiend/Foul Fiend.ttf", 32)
win_text = win_font.render("YOU WIN", True, green)
win_textRect = win_text.get_rect()
win_textRect.center = (150,150)
#Parent Sprite Class
class Sprite(pygame.sprite.Sprite):    
    def __init__(self, image, startx, starty):
      super().__init__()
      self.image = pygame.image.load(image)
      self.image = pygame.transform.scale(self.image, playerSizes)
      self.rect = self.image.get_rect()
      self.rect.center = [startx, starty]          
    #Update Function (controls, collision, sprite position)
    def update(self, boxes, starterKnife, enemy_list, enemy):
      hsp = 0
      onground = pygame.sprite.spritecollideany(self, boxes)
      hit_list = pygame.sprite.spritecollide(starterKnife, enemy_list, False)
      hurt_list = pygame.sprite.spritecollide(self, enemy_list, False)
      enemy.rect.x += 5
      for enemy in hit_list:
        print("Enemy Health:", enemy.health)
        print("Player Health:", self.health)      
      key = pygame.key.get_pressed()
      if key[pygame.K_a]:
        self.facing_left = True
        self.walk_animation()
        hsp = -self.speed
        starterKnife.rect.x = self.rect.x - 30
      elif key[pygame.K_d]:
        self.facing_left = False
        self.walk_animation()
        hsp = self.speed
        starterKnife.rect.x = self.rect.x + 50
      else:
        self.image = self.stand_image
      if key[pygame.K_w] and onground:
        self.vsp = -self.jumpspeed
        starterKnife.rect.y = self.rect.y + 30
      if self.vsp < 10 and not onground:
        self.vsp += self.gravity
        starterKnife.rect.y = self.rect.y + 30
        self.jump_animation()
      if self.vsp > 0 and onground:
        self.vsp = 0
        starterKnife.rect.y = self.rect.y + 30
      #Knife Control & Positioning
      if key[pygame.K_SPACE]:
        self.knife_animation(starterKnife)
      self.move(hsp,self.vsp)
      if self.rect.x < 0:
        self.rect.x = 0
      if self.rect.x > 525:
        self.rect.x = 525
      if self.rect.y > starterKnife.rect.y:
        starterKnife.rect.y = self.rect.y + 15
      #Player and Enemy Collision
      if key[pygame.K_SPACE] and hit_list:
        enemy.health -= 1/4
      if enemy.rect.x > 540:
        enemy.rect.x = 0
      if hurt_list:
        self.rect.x -= 30
        self.health -= 1
      if self.health == 0:
        self.rect.x = -200
        self.rect.y = -200
    def draw(self, screen):
      screen.blit(self.image, self.rect)
    def move(self, x, y):
      self.rect.move_ip([x,y])
    #Player Sprite
class Player(Sprite):
    def __init__(self, startx, starty):
        super().__init__("heroRun/hero.png", startx, starty)
        self.stand_image = self.image
        self.jump_image = pygame.image.load("heroJump/heroJump.png")
        self.jump_image = pygame.transform.scale(self.jump_image, playerSizes)
        self.walk_cycle = [pygame.image.load(f"heroRun/hero{i:0>2}.png") 
        for i in range(1,5)]
        self.knife_cycle = [pygame.image.load(f"startKnife/startKnife{i:0>2}.png")
        for i in range(1,5)]
        self.animation_index = 0
        self.facing_left = False
        self.speed = 6
        self.jumpspeed = 20
        self.gravity = 1
        self.vsp = 0
        self.frame = 0
        self.health = 100
      #Run Animation
    def walk_animation(self):
      self.image = self.walk_cycle[self.animation_index]
      if self.facing_left:
        self.image = pygame.transform.flip(self.image, True, False)
      if self.animation_index < len(self.walk_cycle)-1:
        self.animation_index += 1
      else:
        self.animation_index = 0
      #Jump Animation
    def jump_animation(self):
      self.image = self.jump_image
      if self.facing_left:
          self.image = pygame.transform.flip(self.image, True, False)
      #Knife Animation
    def knife_animation(self, starterKnife):
      starterKnife.image = self.knife_cycle[self.animation_index]
      if self.facing_left:
          starterKnife.image = pygame.transform.flip(starterKnife.image, True, False)
      if self.animation_index < len(self.knife_cycle) - 1:
        self.animation_index += 1
      else:
        self.animation_index = 0
      #Ground Sprite
class Box(Sprite):
  def __init__(self, startx, starty):
    super().__init__("boxAlt.png", startx, starty)
    #Starter Knife Sprite
class StarterKnife(Sprite):
  def __init__(self, startx, starty):
    super().__init__("basicKnife.png", startx, starty)
    hsp = 0
    self.animation_index = 0
    self.image = pygame.transform.scale(self.image, (25,60))
    self.image = pygame.transform.rotate(self.image, -30)
    self.speed = 4
    self.facing_left = False
    #Enemy Sprite
class Enemy(Sprite):
  def __init__(self, startx, starty):
    super().__init__("ZOMBIE.png", startx, starty)
    self.image = pygame.transform.scale(self.image, zombieSize)
    Enemy.health = 100
    self.hitbox = (self.rect.x + 17, self.rect.y + 2, 31, 57)
def main():       
    bg = pygame.image.load("background169.png")
    bg = pygame.transform.scale(bg, bgSize)
    clock = pygame.time.Clock()
    player = Player(100,275)
    boxes = pygame.sprite.Group()
    enemy_list = pygame.sprite.Group()
    starterKnife = StarterKnife(147,275)
    enemy = Enemy(400,300)
    enemy_list.add(enemy)
    for bx in range(0,600,70):
      boxes.add(Box(bx,475))
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
      #Game Instructions
        game_font = pygame.font.Font("foul-fiend/Foul Fiend.ttf", 12)
        game_text = game_font.render("Press A to move left and Press D to move right", True, white)
        game_text2 = game_font.render("Press W to jump, Press and hold Spacebar to attack", True, white)
        game_textRect = game_text.get_rect()
        game_textRect.center = (300,80)
        game_text2Rect = game_text.get_rect()
        game_text2Rect.center = (300,100)
        #Player Health
        font = pygame.font.Font("foul-fiend/Foul Fiend.ttf", 12)
        text = font.render("Player Health:"+str(player.health), True, white)
        textRect = text.get_rect() 
        textRect.center = (100,50)
        #Enemy Health
        enemy_font = pygame.font.Font("foul-fiend/Foul Fiend.ttf", 12)
        enemy_text = enemy_font.render("Enemy Health:"+str(enemy.health), True, white)
        enemytextRect = enemy_text.get_rect() 
        enemytextRect.center = (500,50)
        #Respawn Enemy Text
        respawn_font = pygame.font.Font("foul-fiend/Foul Fiend.ttf", 15)
        respawn_text = respawn_font.render("Press O to respawn enemy", True, white)
        respawntextRect = respawn_text.get_rect() 
        respawntextRect.center = (200,200)
        #Respawn Player Text
        respawn_playerfont = pygame.font.Font("foul-fiend/Foul Fiend.ttf", 15)
        respawn_playertext = respawn_playerfont.render("Press R to respawn player", True, pink)
        respawn_playertextRect = respawn_playertext.get_rect() 
        respawn_playertextRect.center = (420,150)
        if player.health < 100:
          game_textRect.center = (800,800)
          game_text2Rect.center = (800,800)
      pygame.event.pump()
      player.update(boxes, starterKnife, enemy_list, enemy)
      screen.blit(bg, (0,0))
      screen.blit(text, textRect)
      screen.blit(enemy_text, enemytextRect)  
      screen.blit(game_text, game_textRect)
      screen.blit(game_text2, game_text2Rect)
      player.draw(screen)
      boxes.draw(screen)
      starterKnife.draw(screen)
      enemy_list.draw(screen)
      #Lose Screen
      if player.health == 0:
        player.kill()
        screen.blit(lose_text, lose_textRect)
        screen.blit(respawn_playertext, respawn_playertextRect)
      #Win Screen
      if enemy.health == 0:
        enemy.kill()
        screen.blit(win_text, win_textRect)
        screen.blit(respawn_text, respawntextRect) 
      key = pygame.key.get_pressed()
      #Respawn enemies
      if key[pygame.K_o]:
        enemy.add(enemy_list)
        enemy_list.draw(screen)
        enemy.health = 100 
      #Respawn Player with full health
      if key[pygame.K_r]:
        player.add()
        player.rect.x = 100
        player.rect.y = 250
        player.health = 100
      pygame.display.flip()
      clock.tick(30)
if __name__ == "__main__":
    main()        
