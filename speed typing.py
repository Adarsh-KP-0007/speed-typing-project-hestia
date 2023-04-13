from unicodedata import name
import pygame
import mysql.connector
from pygame.locals import *
import sys
import time
import random
mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="speedtype")
mycursor=mydb.cursor()


# 750 x 500    
    
class Game:

   
    def __init__(self):
        self.w=1920
        self.h=1080
        self.reset=True
        self.active = False
        self.input_text=''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = '0%'
        self.results = 'Time:0 Accuracy:0 % Wpm:0 '
        self.wpm = 0
        self.end = False
        self.HEAD_C = (0,238,238)
        self.TEXT_C = (240,240,240)
        self.RESULT_C = (255,70,70)
        
       
        pygame.init()
        self.open_img = pygame.image.load('type-speed-open.png')
        self.open_img = pygame.transform.scale(self.open_img, (self.w,self.h))


        self.bg = pygame.image.load('background.jpg')
        self.bg = pygame.transform.scale(self.bg, (1920,1080))

        self.bg1 = pygame.image.load("photo.jpg")
        self.bg1 = pygame.transform.scale(self.bg1, (1920,1080))


        self.screen = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('TYPING SPEED TEST')

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True  
                
        
    def draw_text(self, screen, msg, y ,fsize, color):
        font = pygame.font.Font('utale.ttf', fsize)
        text = font.render(msg, 1,color)
        text_rect = text.get_rect(center=(self.w/2, y))
        screen.blit(text, text_rect)
        pygame.display.update()   
        
    def get_sentence(self):
        f = open('sentences.txt').read()
        sentences = f.split('\n')
        sentence = random.choice(sentences)
        return sentence

    def congratulations(self):
        #update leaderboard
        mycursor.execute("INSERT INTO leaderboard VALUES('{}',{},{})".format(self.playername,round(self.accuracy),round(self.wpm)))
        mydb.commit() 
        self.screen.fill((0,0,0))
        self.time_img = pygame.image.load('firework.png')
        self.time_img = pygame.transform.scale(self.time_img, (1280,720))
        self.screen.blit(self.time_img, (self.w/2-500,self.h/2-400))
        msg = "CONGRATULATIONS"
        self.draw_text(self.screen, msg,170, 130,self.HEAD_C)
        self.draw_text(self.screen, "You are the fastest typer",300,80,self.HEAD_C)
        while self.running:
            # draw icon image
            self.time_img = pygame.image.load('icon.png')
            self.time_img = pygame.transform.scale(self.time_img, (390,105))
            #screen.blit(self.time_img, (80,320))
            self.screen.blit(self.time_img, (self.w/2-205,self.h-220))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()
                    # position of input box
                    if(x>=340 and x<=1600 and y>=300 and y<=500):
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time() 
                     # position of reset box
                    if(x>=self.w/2-100 and x<=self.w/2+100 and y>=700 and self.end):
                        Game().run()
                        x,y = pygame.mouse.get_pos()

    def leaderboard(self):
        
        mycursor.execute("SELECT * from leaderboard order by accuracy*wpm desc")
        data=mycursor.fetchall()
        pygame.display.update()
        self.screen.fill((0,0,0))
        msg = "LEADERBOARD"
        self.draw_text(self.screen, msg,170, 130,self.HEAD_C)
        self.draw_text(self.screen, "Name                          Accuracy                     WPM",250, 50,self.HEAD_C) 
        j=-1
        for x in data:
            i=0
            j=j+1
            while i<3:  
                name=x[i]
                print(name)
                font = pygame.font.Font(None, 50)
                text = font.render(str(name), 1,(255,255,255))
                text_rect = text.get_rect(center=(self.w/2-320+340*i, 300+j*50))
                self.screen.blit(text, text_rect)
                pygame.display.update()
                i=i+1 
            
        pygame.display.update()
        self.time_img = pygame.image.load('icon.png')
        self.time_img = pygame.transform.scale(self.time_img, (390,105))
        #screen.blit(self.time_img, (80,320))
        self.screen.blit(self.time_img, (self.w/2-205,self.h-220))
        pygame.display.update()
        while self.running:
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()
                    # position of input box
                    if(x>=340 and x<=1600 and y>=300 and y<=500):
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time() 
                     # position of reset box
                    if(x>=self.w/2-100 and x<=self.w/2+100 and y>=700 and self.end):
                        Game().run()
                        x,y = pygame.mouse.get_pos()
                     
        

    def show_results(self, screen):
        if(not self.end):
            #Calculate time
            self.total_time = time.time() - self.time_start
               
            #Calculate accuracy
            count = 0
            for i,c in enumerate(self.word):
                try:
                    if self.input_text[i] == c:
                        count += 1
                except:
                    pass
            self.accuracy = count/len(self.word)*100
           
            #Calculate words per minute
            self.wpm = len(self.input_text)*60/(5*self.total_time)
            self.end = True
            print(self.total_time)
                
            self.results = 'Time:'+str(round(self.total_time)) +" secs   Accuracy:"+ str(round(self.accuracy)) + "%" + '   Wpm: ' + str(round(self.wpm))

            # draw icon image
            self.time_img = pygame.image.load('icon.png')
            self.time_img = pygame.transform.scale(self.time_img, (390,105))
            #screen.blit(self.time_img, (80,320))
            screen.blit(self.time_img, (self.w/2-205,self.h-220))
            # draw trophy image
            self.time_img = pygame.image.load('trophy.png')
            self.time_img = pygame.transform.scale(self.time_img, (100,179))
            #screen.blit(self.time_img, (80,320))
            screen.blit(self.time_img, (250,self.h-300))
            
            
            print(self.results)
            pygame.display.update()

    def run(self):
        self.reset_game()
        self.running=True
        while(self.running):
            clock = pygame.time.Clock()
            self.screen.fill((0,0,0), (340,400,1300,80))
            pygame.draw.rect(self.screen,self.HEAD_C,(340,400,1300,80), 2)
            # update the text of user input
            self.draw_text(self.screen, self.input_text, 440, 40,(250,250,250))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()
                    # position of input box
                    if(x>=340 and x<=1600 and y>=300 and y<=500):
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time() 
                     # position of reset box
                    if(x>=self.w/2-100 and x<=self.w/2+100 and y>=700 and self.end):
                        Game().run()
                        x,y = pygame.mouse.get_pos()
                     #position of leaderboard box
                    if(x>=0 and x<=self.w/2-500 and y>=700 and self.end):
                        self.leaderboard()
                        x,y = pygame.mouse.get_pos()
                        
         
                        
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            mycursor.execute("SELECT * from leaderboard order by accuracy*wpm desc")
                            data=mycursor.fetchall()
                            top=data[0]
                            accuracy_top=top[1]
                            wpm_top=top[2]

                            self.show_results(self.screen)
                            print(self.results)
                            self.draw_text(self.screen, self.results,600, 40, self.RESULT_C)
                            print(self.wpm)
                            print(self.accuracy)
                            print(accuracy_top)
                            print(wpm_top)
                            if int(self.wpm)*int(self.accuracy)>accuracy_top*wpm_top:
                                self.congratulations()
                            #update leaderboard
                            mycursor.execute("INSERT INTO leaderboard VALUES('{}',{},{})".format(self.playername,round(self.accuracy),round(self.wpm)))
                            mydb.commit() 

                            self.end = True
                            
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass
            
            pygame.display.update()
             
                
        clock.tick(60)

    def reset_game(self):
        self.running=True
        self.screen.blit(self.bg1,(0,0))
        pygame.display.update()
        while(self.running):
            msg = "ENTER  NAME"
            self.draw_text(self.screen, msg,170, 130,self.HEAD_C)
            self.screen.fill((0,0,0), (340,400,1300,80))
            pygame.draw.rect(self.screen,self.HEAD_C,(340,400,1300,80), 2)
            # update the text of user input
            self.draw_text(self.screen, self.input_text, 440, 50,(250,250,250))
            self.time_img = pygame.image.load('trophy.png')
            self.time_img = pygame.transform.scale(self.time_img, (100,179))
            self.screen.blit(self.time_img, (1600,self.h-300))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()
                    # position of input box
                    if(x>=340 and x<=1600 and y>=300 and y<=500):
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time() 
                     #position of leaderboard box
                    if(x>=0 and x<=self.w/2-500 and y>=700 and self.end):
                        self.leaderboard()
                        x,y = pygame.mouse.get_pos()
                          

                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            self.playername=self.input_text
                            self.running=False
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass
            
            pygame.display.update()
             
        self.screen.blit(self.open_img, (0,0))

        pygame.display.update()
        time.sleep(1)
        
        self.reset=False
        self.end = False

        self.input_text=''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0

        # Get random sentence 
        self.word = self.get_sentence()
        if (not self.word): self.reset_game()
        #drawing heading
        self.screen.fill((0,0,0))
        self.screen.blit(self.bg,(0,0))
        msg = "TYPING SPEED TEST"
        self.draw_text(self.screen, msg,170, 130,self.HEAD_C) 
        self.draw_text(self.screen, "Click on the box to start timer",500,60,self.HEAD_C) 
        # draw the rectangle for input box
        pygame.draw.rect(self.screen,(255,192,25), (340,400,1300,80), 2)

        # draw the sentence string
        self.draw_text(self.screen, self.word,320, 50,self.TEXT_C)
        
        pygame.display.update()



Game().run()
