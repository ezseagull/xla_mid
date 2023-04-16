import pygame, sys
from button import Button
from pygame import mixer
import imutils
import numpy as np
import cv2
from imutils import contours
from skimage import measure
from matplotlib import pyplot as plt
from PIL import Image

pygame.init()


SCREEN = pygame.display.set_mode((830, 720))
pygame.display.set_caption("Menu")
myfont = pygame.font.SysFont(None, 50)

BG = pygame.image.load("assets/Background.png")
# PL = pygame.image.load("data/play.jpg")
GO = pygame.image.load("assets/gameover.jpg")

clock = pygame.time.Clock()
 
# background sound
# mixer.music.load('sound/music.mp3')
# mixer.music.play(-1)

def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

#Read the images
img1 = cv2.imread('data/chinh.jpg')
img2 = cv2.imread('data/easy.jpg')
img3 = cv2.imread('data/normal.jpg')
#Load the images
image1 = pygame.image.load('data/chinh.jpg')
image2 = pygame.image.load('data/easy.jpg')
image3 = pygame.image.load('play4.jpg')
image5 = pygame.image.load('play5.jpg')
image4 = pygame.image.load('re.jpg')
image6 = pygame.image.load('rn.jpg')
img_height = img1.shape[0]
#Link to image
IMG1 = 'data/chinh.jpg'
IMG2 ='data/easy.jpg'
IMG3 ='data/normal.jpg'

list = []
find_diffs = []
list2 = []
find_diffs2 = []

def threshold(tup1, tup2):
    val=0
    if(abs(tup1[0]-tup2[0])>=4):
        val+=1
    if(abs(tup1[1]-tup2[1])>=4):
        val+=1
    if(abs(tup1[2]-tup2[2])>=4):
        val+=1

    if(val>=2):
        return True
    else:
        return False

# x = np.zeros((img_height,30,3), np.uint8)
# y = np.zeros((img_height,20,3), np.uint8)
# result = np.hstack((img1, x, img3))
# cv2.imshow("Differences", result)  
# cv2.imwrite("play5.jpg", result)


def finalDetect(IMG1, IMG2, arr):
    img1 = Image.open(IMG1)
    img2 = Image.open(IMG2)    
    resultImg = img1.copy()
    x, y = min(img1.size[0], img2.size[0]), min(img1.size[1], img2.size[1])
    grid = [[0]*y]*x
    pixImg1 = img1.load()
    pixImg2 = img2.load()
    resultPix = resultImg.load()
    for i in range(x):
        for j in range(y):
            if(threshold(pixImg1[i,j], pixImg2[i,j])):
                grid[i][j]=1
                resultPix[i,j]=(255, 255, 255)
            else:
                resultPix[i, j]=(0, 0, 0)
    orgImage1 = cv2.imread(IMG1)
    orgImage2 = cv2.imread(IMG2)
    img = np.array(resultImg)
    dst = cv2.fastNlMeansDenoisingColored(img,None,180,180,7,21)
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    
    thresh = cv2.threshold(blurred, 50, 155, cv2.THRESH_BINARY)[1]
    thresh = cv2.erode(thresh, None, iterations=1)
    thresh = cv2.dilate(thresh, None, iterations=3)
    labels = measure.label(thresh, connectivity=2, background=0)
    mask = np.zeros(thresh.shape, dtype="uint8")
    for label in np.unique(labels):
        # if this is the background label, ignore it
        if label == 0:
            continue
        # otherwise, construct the label mask and count the
        # number of pixels 
        labelMask = np.zeros(thresh.shape, dtype="uint8")
        labelMask[labels == label] = 255
        numPixels = cv2.countNonZero(labelMask)
        # if the number of pixels in the component is sufficiently
        # large, then add it to our mask of "large blobs"
        if numPixels > 100:
            mask = cv2.add(mask, labelMask)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_LIST,	cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = contours.sort_contours(cnts)[0]
    # print(cnts)

    # loop over the contours
    for (i, c) in enumerate(cnts):
        # draw the bright spot on the image
        (x, y, w, h) = cv2.boundingRect(c)
        # ((cX, cY), radius) = cv2.minEnclosingCircle(c)
        # cc = ((cX, cY), radius)
        cc=(x, y, w, h)
        arr.append(cc)
    

def play():
    finalDetect(IMG1, IMG2, list) 
    pygame.display.set_caption("Easy level")
    frames = 0
    starting_time = 30
    counter = 1280
    pel = 0
    while True:
        frames += 1
        seconnds = frames / 30
        countdown = starting_time - seconnds - pel
        c_p = countdown / 100
        if countdown <= 0:
            gameover = True
            print("Game Over")
            while gameover:
                SCREEN.fill("white")
                OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
                OPTIONS_TEXT = get_font(40).render("GAME OVER", True, "Black")
                OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(415, 260))
                SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

                OPTIONS_BACK = Button(image=None, pos=(415, 460),
                              text_input="BACK", font=get_font(30), base_color="Black", hovering_color="Green")

                OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
                OPTIONS_BACK.update(SCREEN)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                                main_menu()

                clock.tick(30)
                pygame.display.update()
        
        SCREEN.blit(BG, (0, 0))
        
        if len(find_diffs) == 4:
            gamewon = True
            while gamewon:
                SCREEN.fill("white")
                OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
                OPTIONS_TEXT = get_font(40).render("WIN!!!", True, "Black")
                OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(415, 260))
                SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

                OPTIONS_BACK = Button(image=None, pos=(415, 460),
                              text_input="BACK", font=get_font(30), base_color="Black", hovering_color="Green")

                OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
                OPTIONS_BACK.update(SCREEN)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                                main_menu()
                clock.tick(30)
                pygame.display.update()
        #Game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)
                
                missed = 0
                for i,rect in enumerate(list):
                    if mouse_pos[0] > rect[0] and mouse_pos[0] < rect[0] + rect[2] \
                    and mouse_pos[1] > rect[1] and mouse_pos[1] < rect[1] + rect[3]:
                        print("got it")
                        find_diffs.append(i)
                    else:
                        print("missed it")
                        missed += 1
                if missed == 4:
                    pel += 3 
                           
        SCREEN.blit(image3, (0,0))
        time_label = myfont.render(str(int(countdown)), True, (255, 255, 255)) 
        SCREEN.blit(time_label, (390, 450))
        pygame.draw.rect(SCREEN, (255, 255, 255), (0, 420, counter * c_p * 4, 10))
        for f in find_diffs:
            rect = list[f]
            pygame.draw.rect(SCREEN, (255, 0, 0), rect, 3)
            
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        OPTIONS_TEXT = get_font(40).render("Spot 4 differences", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(415, 525))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT) 
        
        OPTIONS_RESULT = Button(image=None, pos=(207, 620),
                              text_input="RESULT", font=get_font(30), base_color="White", hovering_color="Green")

        OPTIONS_RESULT.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_RESULT.update(SCREEN)
        
        OPTIONS_BACK = Button(image=None, pos=(622, 620),
                              text_input="BACK", font=get_font(30), base_color="White", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        main_menu()
                    if OPTIONS_RESULT.checkForInput(OPTIONS_MOUSE_POS):
                        result()                       
        clock.tick(30)
        pygame.display.update()

def result():
    while result:
        
        SCREEN.blit(image4, (0,0))

        OPTIONS_BACK = Button(image=None, pos=(622, 620),
        text_input="BACK", font=get_font(30), base_color="White", hovering_color="Green")
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        main_menu()
        clock.tick(30)
        pygame.display.update()

def option():
    finalDetect(IMG1, IMG3, list2) 
    pygame.display.set_caption("Normal level")
    frames = 0
    starting_time = 30
    counter = 1280
    pel = 0
    while True:
        frames += 1
        seconnds = frames / 30
        countdown = starting_time - seconnds - pel
        c_p = countdown / 100
        if countdown <= 0:
            gameover = True
            print("Game Over")
            while gameover:
                SCREEN.fill("white")
                OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
                OPTIONS_TEXT = get_font(40).render("GAME OVER", True, "Black")
                OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(415, 260))
                SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

                OPTIONS_BACK = Button(image=None, pos=(415, 460),
                              text_input="BACK", font=get_font(30), base_color="Black", hovering_color="Green")

                OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
                OPTIONS_BACK.update(SCREEN)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                                main_menu()

                clock.tick(30)
                pygame.display.update()
        
        SCREEN.blit(BG, (0, 0))
        
        if len(find_diffs2) == 6:
            gamewon = True
            while gamewon:
                SCREEN.fill("white")
                OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
                OPTIONS_TEXT = get_font(40).render("WIN!!!", True, "Black")
                OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(415, 260))
                SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

                OPTIONS_BACK = Button(image=None, pos=(415, 460),
                              text_input="BACK", font=get_font(30), base_color="Black", hovering_color="Green")

                OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
                OPTIONS_BACK.update(SCREEN)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                                main_menu()
                clock.tick(30)
                pygame.display.update()
        #Game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)
                
                missed = 0
                for i,rect in enumerate(list2):
                    if mouse_pos[0] > rect[0] and mouse_pos[0] < rect[0] + rect[2] \
                    and mouse_pos[1] > rect[1] and mouse_pos[1] < rect[1] + rect[3]:
                        print("got it")
                        find_diffs2.append(i)
                    else:
                        print("missed it")
                        missed += 1
                if missed == 4:
                    pel += 3 
                           
        SCREEN.blit(image5, (0,0))
        time_label = myfont.render(str(int(countdown)), True, (255, 255, 255)) 
        SCREEN.blit(time_label, (390, 450))
        pygame.draw.rect(SCREEN, (255, 255, 255), (0, 420, counter * c_p * 4, 10))
        for f in find_diffs2:
            rect = list2[f]
            pygame.draw.rect(SCREEN, (255, 0, 0), rect, 3)
            
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        OPTIONS_TEXT = get_font(40).render("Spot 6 differences", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(415, 525))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT) 
        
        OPTIONS_RESULT = Button(image=None, pos=(207, 620),
                              text_input="RESULT", font=get_font(30), base_color="White", hovering_color="Green")

        OPTIONS_RESULT.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_RESULT.update(SCREEN)
        
        OPTIONS_BACK = Button(image=None, pos=(622, 620),
                              text_input="BACK", font=get_font(30), base_color="White", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        main_menu()
                    if OPTIONS_RESULT.checkForInput(OPTIONS_MOUSE_POS):
                        result2()                       
        clock.tick(30)
        pygame.display.update()
def result2():
    while result:
        
        SCREEN.blit(image6, (0,0))

        OPTIONS_BACK = Button(image=None, pos=(622, 620),
        text_input="BACK", font=get_font(30), base_color="White", hovering_color="Green")
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        main_menu()
        clock.tick(30)
        pygame.display.update()
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(60).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(415,100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(415, 250),
                             text_input="EASY", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(415, 400),
                                text_input="NORMAL", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(415, 550),
                             text_input="QUIT", font=get_font(35), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    option()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
