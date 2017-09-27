import pygame
import sys
import random
import time
import os
from pygame.locals import *


value = [] #list will contain 0,1,2,3 only. 0 for unmarked, 1 for marked,
#2 for flagged,3 for red_mine
mine_nlist = [] #contains indices of mines on board
board = [] #main game_board
flag_list = [] #contains indices of mines marked

game_time = 0
running = True
game_not_over = True
Flag = False

GREY = 192,192,192
RED = 255,0,0
BLUE = 51,204,255
BLACK = 0,0,0
GREEN = 102,255,102
YELLOW = 255,255,0

LEFT = 1
RIGHT = 3

block_size = 30

#images used 
img_size = (block_size,block_size)
zero = pygame.image.load('zero.jpg')
zero_t = pygame.transform.scale(zero,img_size)
one = pygame.image.load("one.jpg")
one_t = pygame.transform.scale(one,img_size)
two = pygame.image.load("two.jpg")
two_t = pygame.transform.scale(two,img_size)
three = pygame.image.load("three.jpg")
three_t = pygame.transform.scale(three,img_size)
four = pygame.image.load("four.jpg")
four_t = pygame.transform.scale(four,img_size)
five = pygame.image.load("five.jpg")
five_t = pygame.transform.scale(five,img_size)
six = pygame.image.load("six.jpg")
six_t = pygame.transform.scale(six,img_size)
seven = pygame.image.load("seven.jpg")
seven_t = pygame.transform.scale(seven,img_size)
eight = pygame.image.load("eight.jpg")
eight_t = pygame.transform.scale(eight,img_size)
cover = pygame.image.load("cover.jpg")
cover_t = pygame.transform.scale(cover,img_size)
flag = pygame.image.load("flag.jpg")
flag_t = pygame.transform.scale(flag,img_size)
mine = pygame.image.load("mine.jpg")
mine_t = pygame.transform.scale(mine,img_size)
red_mine = pygame.image.load("red_mine.jpg")
red_mine_t = pygame.transform.scale(red_mine,img_size)

def clean_variables():
    #empties each global variable after every game 
    global mine_nlist, flag_list,running,Flag
    Flag = False
    running = True
    mine_nlist,flag_list = [],[]

def index(x):
    #returns index of list
    index = x/block_size
    return index 

def game_state(board,value):
    #displays game current state (displayed on pygame window)
    screen.fill(GREY)
    for i in range (len(board)):
        for j in range (len(board[i])):
            info = value[i][j]
            pic_x = block_size*(i+1)
            pic_y = block_size*(j)
            pos = (pic_y,pic_x)
            if info == 0:
                screen.blit(cover_t,pos)
            elif info == 1:
                element = board[i][j]
                if element == 'M':
                    screen.blit(mine_t,pos)
                elif element == 0:
                    screen.blit(zero_t,pos)
                elif element == 1:
                    screen.blit(one_t,pos)
                elif element == 2:
                    screen.blit(two_t,pos)
                elif element == 3:
                    screen.blit(three_t,pos)
                elif element == 4:
                    screen.blit(four_t,pos)
                elif element == 5:
                    screen.blit(five_t,pos)
                elif element == 6:
                    screen.blit(six_t,pos)
                elif element == 7:
                    screen.blit(seven_t,pos)
                elif element == 8:
                    screen.blit(eight_t,pos)
            elif info == 2:
                screen.blit(flag_t,pos)
            else:
                screen.blit(red_mine_t,pos)

def board_gen(mine_nlist,m,block_no_row,block_no_column):
    #m = no. of mines
    #creates a new game board for every game
    #also places mines
    value,L,l = [],[],[]
    for i in range (block_no_row): 
        for j in range (block_no_column):
            l.append(0)
        L.append(l)
        l = []
    for i in range (block_no_row):
        for j in range (block_no_column):
            l.append(0)
        value.append(l)
        l = []
    

    count = 1
    while count <= m:
        r = random.randint(0,block_no_row-1)
        c = random.randint(0,block_no_column-1)
        if [r,c] not in mine_nlist:
            L[r][c] = 'M'
            mine_nlist.append([r,c])
            count += 1
    L = mine_count(L)

    return L,value,mine_nlist

def open_board(L,value,row,column):
    # this function is called only when element selected is zero or empty
    value[row][column] = 1
    for b in range (-1,2):
        for a in range (-1,2):
            if row+b >= 0 and column+a >= 0:
                try:
                    if value[row+b][column+a] == 0:
                        value[row+b][column+a] = 1
                        if L[row+b][column+a] == 0:
                            L,value = open_board(L,value,row+b,column+a)
                except:
                    pass

    return L,value

def mine_count(L):
    #counts the number of mines in the adjacent 3x3 blocks 
    for y in range (0,len(L)):
        for x in range (0,len(L[y])):
            for b in range (-1,2):
                for a in range (-1,2):
                    if y+b >= 0 and x+a >= 0:
                        try:
                            if L[y+b][x+a] == 'M':
                                L[y][x] += 1
                        except:
                            pass
                        
    return L
def game_over_screen(board,value,row,column):
    #displayed when the game is lost
    for i in range (0,len(value)):
        for j in range (0,len(value[i])):
            if i == row and j == column :
                value[row][column] = 3
            else:
                value[i][j] = 1

    return board,value

def block_assign(board,value,row,column):
    #called when left mouse click is used 
    global running,flag_list
    info = value[row][column]
    element = board[row][column]

    if element == 'M' and info == 0:
        board,value = game_over_screen(board,value,row,column)
        game_state(board,value)
        pygame.display.update()
        time.sleep(3)
        game_not_over,running = set2('GAME OVER. ANOTHER GAME ?')
    elif element == 0:
        L,value = open_board(board,value,row,column)
    else:
        if info == 0:
            value[row][column] = 1
        elif info == 1 or info == 2:
            pass
    if len(flag_list) == m:
        Flag = win_check(value,flag_list,mine_nlist)
        if Flag is True:
           game_not_over,running = set2('YOU WIN! ANOTHER GAME ?')
            

    return board,value

def win_check(value,flag_list,mine_nlist):
    #returns True if game is won otherwise False
    for i in range (0,len(value)):
        if 0 in value[i]:
            return False
        
    for var in mine_nlist:
        if var not in flag_list:
            return False

    return True



def flag_remove(flag_list,row,column):
    #remove a flag index from a list
    for i in range (0,len(flag_list)):
        if flag_list[i] == [row,column]:
            flag_list.remove([row,column])
            return flag_list


def mine_mark(board,value,row,column,m):
    #flags a block as mine
    global flag_list,Flag,game_not_over,running
    info = value[row][column]

    if info == 0:
        value[row][column] = 2
        flag_list.append([row,column])
    elif info == 2:
        value[row][column] = 0
        flag_list = flag_remove(flag_list,row,column)
    else:
        pass
    
    if len(flag_list) == m:
        Flag = win_check(value,flag_list,mine_nlist)
        
        if Flag is True:
            game_not_over,running = set2('YOU WIN !!,ANOTHER GAME ?')
    
    return board,value         

def print_list(l):
    #displays the board matrice
    print 
    for i in range (0,len(l)):
        for j in range (0,len(l[i])):
            print l[i][j],
        print
            
def choose_level(level):
    if level == 1:
        return beginner_level()
    elif level == 2:
        return intermediate_level()
    else:
        return advanced_level()
def beginner_level():
    #level 1
    m = 10
    block_no_row = 9
    block_no_column = 9
    level = 'beginner'
    return m,block_no_row,block_no_column,level

def intermediate_level():
    #level 2
    m = 40
    block_no_row = 16
    block_no_column = 16
    level = 'intermediate'
    return m,block_no_row,block_no_column,level

def advanced_level():
    #level 3
    m = 80
    block_no_row = 16
    block_no_column = 30
    level = 'advanced'
    return m,block_no_row,block_no_column,level

def game_window2(m,x,y):
    #to diplay pygame window
    global screen
    pygame.init()
    resolution= block_size*y,block_size*(x+1) #width,height
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption ("MINESWEEPER")

class game_window():
    def __init__(self,w,h,col,c):
        self.resolution = w,h
        self.bckg_color = col
        self.caption = c

    def display_text(self,text,color,size,font,x,y):
        self.font = pygame.font.SysFont(font,size)
        self.text = text
        self.label = self.font.render(self.text,1,color)
        self.screen.blit(self.label,(x,y))
        pygame.display.update()

    def draw_rect(self,color,x,y,width,height):
        pygame.draw.rect(self.screen,color,(x,y,width,height))
        pygame.display.update()

    def check_tab(self,x1,x2,mouse_x,mouse_y):
        if mouse_x >= x1 and mouse_x <= x2:
            for i in range (1,4):
                if mouse_y >= 100*i and mouse_y <= 100*i +50:
                    return i
        else:
            return None
    def Pygame_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.resolution)
        self.screen.fill(self.bckg_color)
        pygame.display.update()
        
    def events(self,x1,x2):
        while True:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN\
                   and event.button == LEFT:
                    mouse_x,mouse_y = event.pos
                    try:
                        answer = self.check_tab(x1,x2,mouse_x,mouse_y)
                        return answer
                    except:
                        pass
                elif event.type == pygame.QUIT:
                    running = False
                    game_not_over = False
                    pygame.quit()
                    sys.exit()
            pygame.display.update()



def set1():
    #initial window
    scene = game_window(800,400,GREY,'MINESWEEPER')
    scene.Pygame_init()
    scene.display_text('CHOOSE LEVEL',BLACK,50,'Times New Roman',50,0)
    for i in range (1,7,2):
        scene.draw_rect(BLUE,50,50*(i+1),600,50)

    scene.display_text('LEVEL 1: BEGINNER - 10 mines 9X9 GRID',BLACK,25,'Times New Roman',75,112.5)
    scene.display_text('LEVEL 2: INTERMEDIATE - 40 mines 16X16 GRID',BLACK,25,'Times New Roman',75,212.5)
    scene.display_text('LEVEL 3: ADVANCED - 99 mines 16X30 GRID',BLACK,25,'Times New Roman',75,312.5)
    
    ans=scene.events(50,600)
    return choose_level(ans)

def set2(text):
    #final window
    scene = game_window(500,300,GREY,'MINESWEEPER')
    scene.Pygame_init()
    scene.display_text(text,BLACK,25,'Times New Roman',50,0)
    for i in range (1,5,2):
        scene.draw_rect(BLUE,50,50*(i+1),100,50)
    scene.display_text('YES',BLACK,25,'Times New Roman',75,112.5)
    scene.display_text('NO',BLACK,25,'Times New Roman',75,212.5)
    ans = scene.events(100,200)
    running = False
    if ans == 1:
        game_not_over = True
        game_time = time_now
        
    else:
        game_not_over = False
        pygame.quit()
        sys.exit()
    return game_not_over,running

def insert(File,username,score,count,file_name):
    #for entering highscore record
    temp_file = open('temp.txt','w')
    text = username+" "+str(score)+'\n'
    for i in range (0,10):
        rec = File.readline()
        if i == count :
            temp_file.write(text)
            emp_file.write(rec)
        else:
            temp_file.write(rec)
    temp_file.close()
    File.close()
    os.remove(file_name)
    os.rename('temp.txt',file_name)
    
def edit(file_n,score):
    #for getting the rank
    File = open(file_n,'r+')
    recs = ' '
    count = -1
    while recs :
        count += 1
        recs = File.readline()
        rec_split = recs.split()
        if score <= int(rec_split[1]):
            print 
            username = raw_input('enter username')
            insert(File,username,score,count,file_n)
            break


def Highscore_save(time_now,level):
    #prompt for saving highscore
    print 
    print 'NEW HIGHSCORE!'
    if level == 'beginner':
        edit('Scores_beginner.txt',time_now)
    elif level == 'intermediate':
        edit('Scores_intermediate.txt',time_now)
    else:
        edit('Scores_advanced.txt',time_now)




#main game_loop()
while game_not_over:
    clean_variables()
    m,block_no_row,block_no_column,level = set1()
    game_window2(m,block_no_row,block_no_column)
    board,value,mine_nlist= board_gen(mine_nlist,m,block_no_row,block_no_column)
    myfont = pygame.font.SysFont("OCR A Extended", 20)

##    print_list(board)
    
    time_now = 0
    start = False 


    while running :
        for event in pygame.event.get():
            

            if event.type == MOUSEBUTTONDOWN\
               and event.button == LEFT:
                if start == False:
                    start = True
                    game_time = time.clock()

                mousex,mousey = event.pos
                index_x = index(mousex) #column
                index_y = index(mousey)-1  #row
                board,value = block_assign(board,value,index_y,index_x)

            elif event.type == MOUSEBUTTONDOWN\
                and event.button == RIGHT:
                if start == False:
                    start = True
                    game_time = time.clock()
                mousex,mousey = event.pos
                index_x = index(mousex)
                index_y = index(mousey)-1
                board,value = mine_mark(board,value,index_y,index_x,m)

            elif event.type == pygame.QUIT:
                running = False
                game_not_over = False
                pygame.quit()
                sys.exit()

        game_state(board,value)
        if start is True :
            time_now = int(time.clock() - game_time)
            text = "TIME : "+str(time_now)
            label = myfont.render(text, 10,RED)
            screen.blit(label, (0,0))
        pygame.display.update()

    if Flag is True:
        Highscore_save(time_now,level)
    
            
















