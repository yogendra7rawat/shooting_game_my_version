import pygame as py
import sys
import time
import math
import random

py.init();




#display


screen = py.display.set_mode((800,600));

py.display.set_caption('Yogendra')

icon = py.image.load('spaceship.png');

py.display.set_icon(icon);



Game_over  = py.font.Font('freesansbold.ttf',32);

GO_x = 400;
GO_y = 300;

def over(x,y):
    o = Game_over.render('GAME OVER',True,(255,100,10));
    screen.blit(o,(x,y))

#player
score =0;
font  = py.font.Font('freesansbold.ttf',32);





text_x = 10;
text_y = 10;

def show(x,y):
    s= font.render(f'Score: {score}',True,(255,0,0))
    screen.blit(s,(x,y));

player_img = py.image.load('lancelot.png'); 
playerX = 470;
playerY = 350;
playerX_change =0;
playerY_change =0;
def player(x,y):
    screen.blit(player_img,(x,y));



    
# enemy
enemy_img = [];
enemyX = []
enemyY = []
enemyX_change =[]
enemyY_change =[]
global num_of_enemy
num_of_enemy = 13;

for i in range(num_of_enemy):

    enemy_img.append(py.image.load('target.png'));
    enemyX.append(random.randint(0,800));
    enemyY.append(random.randint(50,150));
    enemyX_change.append(0.2);
    enemyY_change.append(40);


def enemy(x,y,i):
    screen.blit(enemy_img[i],(x,y));





#meteorite

m_img = [];
mX = []
mY = []
mX_change =[]
mY_change =[]
global num_of_m
num_of_m = 3;

for i in range(num_of_enemy):

    m_img.append(py.image.load('meteorite.png'));
    mX.append(random.randint(0,800));
    mY.append(random.randint(50,150));
    mX_change.append(0.5);
    mY_change.append(40);




# bullet


bulletX =0;
bulletY = playerY;
bullet_state ='ready';
bulletY_change =1.2;
bullet_img = py.image.load('bullet.png');


    

def fire(current_x,current_y):
    global bullet_state;
    bullet_state = 'fire';
    screen.blit(bullet_img,(current_x+16,current_y+10));
    




def hit(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2));

    if(distance<27):
        return True;
    else:
        return False;




background  = py.image.load('space.png');

running = True
  
while running:
    
    screen.fill((0,0,0));

    screen.blit(background,(0,0));
    

    
    show(text_x,text_y);
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False;

        if(event.type == py.KEYDOWN):
            if(event.key == py.K_LEFT):
                playerX_change -=0.3;
                
                
            if(event.key == py.K_RIGHT):
                playerX_change+=0.3;
                

            if(event.key == py.K_UP):
                playerY_change-=0.3;

            if(event.key == py.K_DOWN):
                playerY_change+=0.3;

            if event.key == py.K_SPACE and bullet_state == 'ready':
                bulletX = playerX
                fire(bulletX,bulletY);
                
                

        if event.type == py.KEYUP:
            if event.key == py.K_LEFT or event.key == py.K_RIGHT:
                playerX_change = 0;
               
            if event.key == py.K_UP or event.key == py.K_DOWN:
                 playerY_change = 0;

            
    
                 

                 

  

    
    playerX+=playerX_change;
    playerY+=playerY_change;
    
    if playerX<=0:
        playerX = 0;

    elif playerX>=736:
        playerX = 736;


    if playerY<=0:
        playerY = 0;

    elif playerY>=536:
        playerY = 536;
    
        
    

    # enemy part
    for i in range(num_of_enemy):
        
        enemyX[i]+=enemyX_change[i];
    
    
        if(enemyX[i]<=0):
            enemyX_change[i] = 0.2;
            enemyY[i]+=enemyY_change[i];

        elif enemyX[i]>=736:
            enemyX_change[i] = -0.2;
            enemyY[i]+=enemyY_change[i];


        collosion = hit(enemyX[i],enemyY[i],bulletX,bulletY);

        if(collosion):
            bulletY = playerY;
            bullet_state = 'ready';
            score+=1;
            print("score = ",score);
            enemyX[i] = random.randint(0,800);
            enemyY[i] = random.randint(50,150);
            num_of_enemy-=1;

        enemy(enemyX[i],enemyY[i],i);


    if(num_of_enemy == 0):
        over(GO_y,GO_y);


    #for i in range(num_of_m):

    #bullet part


    if bulletY<=0:
        bulletY = playerY;
        bullet_state = 'ready';

    if bullet_state is 'fire':
        fire(bulletX,bulletY);
        bulletY-=bulletY_change;




    

    
    player(playerX,playerY); # player display
    
    




    py.display.update();


py.quit()
