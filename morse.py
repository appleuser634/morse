import pygame
from pygame.locals import *
import sys
import os
import time
import pickle
import requests
import random

binary = []
morse = ""
morse_list = {"._":"A","_...":"B","_._.":"C","_..":"D",".":"E",".._.":"F",\
            "__.":"G","....":"H","..":"I",".___":"J","_._":"K","._..":"L",\
            "__":"M","_.":"N","___":"O",".__.":"P","__._":"Q","._.":"R",\
            "...":"S","_":"T",".._":"U","..._":"V",".__":"W","_.._":"X",\
            "_.__":"Y","__..":"Z",".____":"1","..___":"2","...__":"3",\
            "...._":"4",".....":"5","_....":"6","__...":"7","___..":"8",\
            "____.":"9","_____":"0","........":"del"}

typed_words = ""

frame = 0
check = 0
free_sec = 0


def main():
    global word,frame,check,free_sec,typed_words

    pygame.init()
    screen = pygame.display.set_mode((400,300))
    pygame.display.set_caption("Morse!")
    font = pygame.font.Font(None, 100)
    font2 = pygame.font.Font(None, 50)
    font3 = pygame.font.Font(None, 30)

    if 'kp_save.pickle' in os.listdir():
        with open('./kp_save.pickle','rb') as kp:
            key_pitch = pickle.load(kp)
    else:
        key_pitch = 100
    
    random_words = get_words()

    word_index = random.randint(0,len(random_words))
    word = random_words[word_index].decode()
    word = str.upper(word)

    score = 0
     
    while True:
        
        pressed_key = pygame.key.get_pressed()
        
        # SET Key Pith.
        if pressed_key[K_s]:
            
            key_pitch += 2
            time.sleep(0.2)

        elif pressed_key[K_f]:
            
            if key_pitch >= 5:
            
                key_pitch -= 2
                time.sleep(0.2)
        
        # Get next Sample Words.
        elif pressed_key[K_n]:
            
            typed_words = ""

            word_index = random.randint(0,len(random_words))
            word = random_words[word_index].decode()
            word = str.upper(word)

        # Get Morse Code.
        if pressed_key[K_SPACE]:
            if check == 0:
                frame = 0
            frame += 1
            check = 1
        
        else:
            if check == 1:
                free_sec = 0
                encode_binary(frame,key_pitch)
            check = 0
            free_sec += 1

        if free_sec >= key_pitch + 300:
            encode_morse(binary)


        screen.fill((0,0,0))
        
        # Display Enterd Charctor.
        text = font.render(morse, True, (255,255,255))
        screen.blit(text, [170,150])
        
        try:
            frame_text = font.render("".join(binary).encode(), True, (255,255,255))
            screen.blit(frame_text, [170,200])
        except:
            pass
        
        # Display Key Pith Speed.
        kp_stat = font3.render("KeyPith:" + str(key_pitch), True, (255,255,255))
        screen.blit(kp_stat, [10,10])

        # Display Sample Words.
        kp_stat = font2.render(word, True, (255,255,255))
        screen.blit(kp_stat, [10,50])

        # Display Typed Words.
        kp_stat = font2.render(typed_words, True, (255,255,255))
        screen.blit(kp_stat, [10,80])
        
        # Display Score.
        kp_stat = font2.render("Score:" + str(score), True, (255,255,255))
        screen.blit(kp_stat, [230,5])


        pygame.display.update()

        if typed_words == word:
            
            typed_words = ""

            word_index = random.randint(0,len(random_words))
            word = random_words[word_index].decode()
            word = str.upper(word)
            
            score += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                end(key_pitch)
            if event.type == KEYDOWN:  
                if event.key == K_ESCAPE:
                    end(key_pitch)
            else:
                pygame.mixer.music.stop()
                pass

def encode_binary(frame,key_pitch):
    global binary
     
    if frame <= key_pitch and frame >= 1:
        binary.append(".")
    elif frame > key_pitch:
        binary.append("_")

def encode_morse(code):
    global morse,binary,typed_words
    try:
        morse = morse_list["".join(code)]

        if morse == "del":
            typed_words = typed_words[:-1]
        else:
            typed_words += morse

    except KeyError:
        pass
    binary = []

def get_words():
    
    if 'random_words.pickle' in os.listdir():
        with open('./random_words.pickle', 'rb') as rw:
            random_words = pickle.load(rw)
    else:
        word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
        response = requests.get(word_site)
        random_words = response.content.splitlines()
        
        with open('./random_words.pickle', 'wb') as rw:
            pickle.dump(random_words,rw)
    
    return random_words

def check_morse():
    pass

def end(key_pitch):
    print(binary)
    print(morse)
    
    with open('./kp_save.pickle','wb') as kp:
        pickle.dump(key_pitch,kp)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
