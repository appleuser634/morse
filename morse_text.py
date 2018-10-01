import pygame
from pygame.locals import *
import sys

binary = []
morse = ""
morse_list = {"._":"A","_...":"B","_._.":"C","_..":"D",".":"E",".._.":"F",\
            "__.":"G","....":"H","..":"I",".___":"J","_._":"K","._..":"L",\
            "__":"M","_.":"N","___":"O",".__.":"P","__._":"Q","._.":"R",\
            "...":"S","_":"T",".._":"U","..._":"V",".__":"W","_.._":"X",\
            "_.__":"Y","__..":"Z",".____":"1","..___":"2","...__":"3",\
            "...._":"4",".....":"5","_....":"6","__...":"7","___..":"8",\
            "____.":"9","_____":"0"}

frame = 0
check = 0
free_sec = 0
user_text = []

def main():
    global word,frame,check,free_sec,user_text

    pygame.init()
    screen = pygame.display.set_mode((400,300))
    pygame.display.set_caption("Morse!")
    font = pygame.font.Font(None, 100)
    font2 = pygame.font.Font(None, 50)
    while True:
        
        pressed_key = pygame.key.get_pressed()

        if pressed_key[K_SPACE]:
            if check == 0:
                frame = 0
            frame += 1
            check = 1

        else:
            if check == 1:
                free_sec = 0
                encode_binary(frame)
            check = 0
            free_sec += 1

        if free_sec >= 70:
            encode_morse(binary)

        screen.fill((0,0,0))
        text = font.render(morse.encode(), True, (255,255,255))
        screen.blit(text, [170,100])
        try:
            frame_text = font.render("".join(binary).encode(), True, (255,255,255))
            screen.blit(frame_text, [170,200])
            
            if len(user_text) >= 10:
                del user_text[0]
            text = font2.render("".join(user_text).encode(), True, (255,255,255))
            screen.blit(text, [100,50])
        except:
            pass
             
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                end()
            if event.type == KEYDOWN:  
                if event.key == K_ESCAPE:
                    end()
                if event.key == K_d:
                    del user_text[-1]
                if event.key == K_c:
                    user_text = []

def encode_binary(frame):
    global binary
     
    if frame <= 8 and frame >= 1:
        binary.append(".")
    elif frame >= 9:
        binary.append("_")

def encode_morse(code):
    global morse,binary
    try:
        morse = morse_list["".join(code)]
        user_text.append(morse)
    except KeyError:
        pass
    binary = []

def end():
    print(binary)
    print(morse)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
