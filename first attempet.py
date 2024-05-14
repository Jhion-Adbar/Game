import pygame, sys
from player import Player 
import obstacle
from alien import Alien, Extra
from random import choice, randint
from laser import Laser
import time

class Game:
    def __init__(self):
        # setpu for player
                                                # player re position kore
        player_sprite = Player((screen_width / 2, screen_height ),screen_width,5)
        self.player = pygame.sprite.GroupSingle(player_sprite)


        # player ar count and score ano theke hobe it is a init funtion under work
        self.lives = 5  #life count ja hobe
        self.live_surf = pygame.image.load('../python project/22115-5948.png').convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 4 + 40) # 4 ta life show hoi

        #  for score 
        self.score = 0
        self.font = pygame.font.Font('../python project/Pixeled.ttf', 20 )         # score board ar text



        # obstacle are setted by opi

        self.shape = obstacle.shape # obastacle ar shape anchi class theke
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4   # obstacle number
        self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start = screen_width / 10, y_start = 575) 
                                                                            # obstacle ar position


        #aline ano theke #####################
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()


        self.alien_setup(rows = 6, cols = 8) # number of alien ja hobe 
        self.alien_direction = 1

        # extra alien on up 
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(400,800)


        # sound debo dum dum dum

        music = pygame.mixer.Sound('../python project/Memory Reboot.wav')
        music.set_volume(0.5) # ano volum
        music.play(loops= -1)   # bar bar gurbe

        self.gunshot = pygame.mixer.Sound('../python project/Gunshot.wav')  # ai sound alien ar
        self.gunshot.set_volume(0.3)
        
        self.bomb = pygame.mixer.Sound('../python project/Bomb.wav')  # sound ami more jalem
        self.bomb.set_volume(0.5)

        ######################
        self.ex = pygame.mixer.Sound('../python project/ex.wav')  # sound alien more galo
        self.ex.set_volume(0.5)




        # ato kichy 53-68 akta obstacle ar jonno
    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':    
                    x = x_start + col_index * self.block_size + offset_x  # shape ar modhe check position
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size,(241,79,80),x,y)
                    self.blocks.add(block)



                                                            # *offset hoiche packing operator
    def create_multiple_obstacles(self, *offset, x_start, y_start ):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)



    def alien_setup(self,rows,cols,x_distance = 170,y_distance = 50,x_offset = 100, y_offset = 80):
         for row_index, row in enumerate(range(rows)):
              for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                alien_sprite = Alien('red',x,y)
                if row_index == 0: alien_sprite = Alien('yellow',x,y)
                elif 1 <= row_index <= 2: alien_sprite = Alien('green',x,y)
                else: alien_sprite = Alien('red',x,y)
                self.aliens.add(alien_sprite)



    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)


    def alien_move_down(self,distance):
        if self.aliens:
             for alien in self.aliens.sprites():
                 alien.rect.y += distance


    
    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center,6,screen_height)
            self.alien_lasers.add(laser_sprite)
            self.gunshot.play() # gunshot play hobe

                ####################################################
    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right','left']),screen_width))
            self.extra_spawn_time = randint(400,800)


    
    def collision_checks(self):
        # player lasers ta ano theke kaj korbe
        if self.player.sprite.lasers:
             for laser in self.player.sprite.lasers:
                
                

                # obstacle collisions block ta kill kore leaser dea then leaser gone by block break
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                    
                
                
                # alien collisions dea alien marbo feu feu player ar leaser hit korle alien morbe
                aliens_hit = pygame.sprite.spritecollide(laser,self.aliens,True)
                if aliens_hit:

                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()
                    self.ex.play()   # bomb sound #################### 

                
                
                
                # extra collision ano hobe
                if pygame.sprite.spritecollide(laser,self.extra,True):
                    laser.kill()
                    self.score += 500

                
		    #alien laser anotheke aline gula amake marbe
        if self.alien_lasers:
            for laser in self.alien_lasers:
                # alien ano obastical block ke hit korbr
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()

                if pygame.sprite.spritecollide(laser,self.player,False): 
                    laser.kill()
                    print('great creator opi_da')
                    self.bomb.play()#########################################################################################################

                    self.lives -= 1
                    if self.lives  <= 0: 
                        self.game_over() ####### ai line ta game over show korbe ..............................................
                        pygame.quit()
                        sys.exit()





            #aliens gula block ke dhor distroy kore then player k dhorlei game end
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien,self.blocks,True)

                if pygame.sprite.spritecollide(alien,self.player,False):
                    pygame.quit()
                    sys.exit()







    def display_lives(self):   # life gula ano theke show korbe , +10 use for offset, -1 kore kumbe, 
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf,(x,8))



        # score ar jonno funtion handle the score sys
    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}',False,'white')
        score_rect = score_surf.get_rect(topleft = (10,-10))
        screen.blit(score_surf,score_rect)


        # vicotry massage 
    def victory_message(self):
        if not self.aliens.sprites():
            victory_surf = self.font.render('GAME DEV THANKS \n THE WINNER',False,'white')
            victory_rect = victory_surf.get_rect(center = (screen_width / 2, screen_height / 2))
            screen.blit(victory_surf,victory_rect)





            # up a call hole ai khane ashbe jodi game over hoi
    def game_over(self):
        game_over_surf = self.font.render('GAME OVER \n Thanks From GAME DEV Team', True, 'white')
        game_over_rect = game_over_surf.get_rect(center = (screen_width / 2, screen_height / 2))
        screen.blit(game_over_surf, game_over_rect)
        pygame.display.flip()
        pygame.time.wait(5000)  # 5 second wait korbo
        pygame.quit()
        sys.exit()

             #.................................................................................................................


				




    def run(self):
        self.player.update()

        self.aliens.update(self.alien_direction)

        self.alien_position_checker()

        self.alien_lasers.update()

        #extra
        self.extra_alien_timer()
        self.extra.update()

        # collision hoche shob gula ga oi funtion a ache
        self.collision_checks()


        

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)

        self.blocks.draw(screen)

        self.aliens.draw(screen) 

        self.alien_lasers.draw(screen)


        #extra
        self.extra.draw(screen)

        #lives gula show korbe
        self.display_lives()

        # score
        self.display_score()

        #victory massage
        self.victory_message()


        #update all sprite for main 
        #draw all sprite for main to work





if __name__ == '__main__':
    pygame.init()
    screen_width = 1500                 # screen ar size ano theke ok kore (chowre)
    screen_height = 765                # lomba
    screen = pygame.display.set_mode((screen_width,screen_height)) # ano theke display serface hoiche
    clock = pygame.time.Clock()
    game = Game()


    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER,800)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()
        if event.type == ALIENLASER:
            game.alien_shoot()


    screen.fill((30,30,30))
    game.run()

    pygame.display.flip()
    clock.tick(60)    # frem ret limit 60 korchi

    # pygame.sprite.sprite hoilo  a two dimensional image that is part of the larger graphical scene.