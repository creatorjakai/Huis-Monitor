#Importeren van Libraries
import pygame
import time
import socket
import os
import sys
import random

#Initializeren van onderdelen
pygame.init()

#Laad belangerijke afbeeldingen
icon = pygame.image.load("Assets/Icons/icon.png")

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

#Inializeren van belangerijke variabelen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Huis Monitor v26.0.25 BETA")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 15)
typfont = pygame.font.SysFont("Arial", 25)
running = True
connected = False
os.system('cls' if os.name == 'nt' else 'clear')

def bootmessage():
        global loadingtext
        screen.fill((0,0,0))
        version_pygame = font.render((pygame.version.ver), True ,(255, 255, 255))
        loading_text = font.render(str(loadingtext), True, (255, 255, 255))
        print(loadingtext)
        screen.blit(loading_text, (5,(SCREEN_HEIGHT - 20)))
        screen.blit(version_pygame, (5, 5))
        pygame.display.flip()

def errormessage():
    global errortext, running
    screen.fill((255, 0, 0))
    error_text = font.render(str(errortext), True, (255, 255, 255))
    print(errortext)
    screen.blit(error_text, (5,(SCREEN_HEIGHT - 20)))
    pygame.display.flip()
    time.sleep(5)
    running = False

def askpassword():
    global serverpassword, client, errortext, menu, randomsearch, clientip, randomip, rndport, searchip, searchport
    if randomsearch:
        screen.fill((255, 255, 255))
        client.sendall((serverpassword + "\n").encode())
        clientip = f"Wachten op reactie van: {randomip}:{rndport}..."
        screen.blit(typfont.render(clientip, True, (0, 0, 0)), (5,(SCREEN_HEIGHT - 20)))
        pygame.display.flip()
        datareceive = client.recv(1024).decode()
        if datareceive.strip() == "LOGIN_OK":
            screen.blit(typfont.render(f"Wachtwoord goedgekeurd door: {clientip}", True, (0, 0, 0)), (5,(SCREEN_HEIGHT - 20)))
            pygame.display.flip()
            menu = "temperatuur"
            return main()
        else:
            errortext = "Error: verkeerd wachtwoord :("
            errormessage()
    else:
        screen.fill((255, 255, 255))
        client.sendall((serverpassword + "\n").encode())
        clientip = f"Wachten op reactie van: {searchip}:{searchport}..."
        screen.blit(typfont.render(clientip, True, (0, 0, 0)), (5,(SCREEN_HEIGHT - 20)))
        pygame.display.flip()
        datareceive = client.recv(1024).decode()
        if datareceive.strip() == "LOGIN_OK":
            screen.blit(typfont.render(f"Wachtwoord goedgekeurd door: {clientip}", True, (0, 0, 0)), (5,(SCREEN_HEIGHT - 20)))
            pygame.display.flip()
            menu = "temperatuur"
            return main()
        else:
           errortext = "Error: verkeerd wachtwoord :("
           errormessage() 

def typserverpassword():
    global randomip, rndport, searchip, searchport, user_input, serverpassword
    user_input = ""
    typing = True

    while typing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    typing = False
                    serverpassword = user_input
                    return askpassword()
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode
    
        screen.fill((255, 255, 255))
    
        pygame.draw.rect(screen, (128, 128, 128), (350, 250, 500, 50))
        screen.blit(typfont.render("Typ IP:", True, (0, 0, 0)), (550, 215))
        screen.blit(typfont.render(user_input, True, (0, 0, 0)), (360, 260))
    
        pygame.display.flip()
        clock.tick(60)

def chooseip():
    global rndport, deviceip, start2, start3, start4, startport, menu
    screen.fill((255, 255, 255))
    img_rect = button_nee.get_rect()
    img_rect.center = (450, 500)
    screen.blit(button_nee, img_rect)
    img_rect = button_ja.get_rect()
    img_rect.center = (750, 500)
    screen.blit(button_ja, img_rect)
    asktest = f"Is dit jou apparaat?: {randomip}:{rndport}"
    screen.blit(typfont.render(asktest, True, (0, 0, 0)), (360, 260))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and pygame.mouse.get_pos() >= (380, 475) and pygame.mouse.get_pos() <= (520, 525):
                start2 = int((randomip.split(".")[1]))
                start3 = int((randomip.split(".")[2]))
                start4 = int((randomip.split(".")[3]))
                startport = int(rndport)
                return searchfordeviceonip()
            if event.button == 1 and pygame.mouse.get_pos() >= (680, 475) and pygame.mouse.get_pos() <= (820, 525):
                deviceip = randomip, rndport
                return typserverpassword()

def searchfordeviceonip():
    global searchip, randomip, menu, errortext, fps, start2, start3, start4, client, rndport, searchport
    searchip = user_input.split(":")[0]
    searchport = user_input.split(":")[1]
    hostname = socket.gethostname()
    socketmyip = socket.gethostbyname(hostname)
    myip = socketmyip.split(".")[0]
    screen.fill((255, 255, 255))
    if randomsearch:
        rndport = 0
        for rnd2 in range(start2, 256):
            for rnd3 in range(start3, 256):
                for rnd4 in range(start4, 256):
                    randomip = f"{myip}.{rnd2}.{rnd3}.{rnd4}"
                    rndport = 0
                    for rndport in range(startport, 8001):
                        fps = clock.get_fps()
                        if fps < 5:
                            pygame.display.quit()
                            pygame.quit()
                            sys.exit()
                        screen.fill((255, 255, 255))
                        searchtext = f"Proberen van: {randomip}:{rndport}"
                        print(searchtext)
                        screen.blit(typfont.render(searchtext, True, (0, 0, 0)),(360, 260))
                        pygame.display.flip()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.display.quit()
                                pygame.quit()
                                sys.exit()
                        try:
                            client = socket.create_connection((randomip, rndport), timeout=0.1)
                            return chooseip()
                        except OSError:
                            pass
                        time.sleep(0.01)

        errortext = "Error: Kan apparaat niet vinden op lokaal netwerk :("
        return errormessage()

    else:
        try:
            client = socket.create_connection((searchip, searchport), timeout=10)
            return typserverpassword()
        except OSError:
            errortext = "Error: Kan apparaat niet vinden:("
            return errormessage()

def userinput_keyboard():
    global user_input, randomsearch
    user_input = ""
    typing = True

    while typing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    typing = False
                    randomsearch = False
                    return searchfordeviceonip()
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

        screen.fill((255, 255, 255))

        pygame.draw.rect(screen, (128, 128, 128), (350, 250, 500, 50))
        screen.blit(typfont.render("Typ IP:", True, (0, 0, 0)), (550, 215))
        screen.blit(typfont.render(user_input, True, (0, 0, 0)), (360, 260))

        pygame.display.flip()
        clock.tick(60)

def screen_setup():
    global user_input, typing
    frame = 1
    framing = True
    while framing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                framing = False       
        if frame == 1:
            screen.fill((255, 255, 255))
            img_rect = image_radar.get_rect()
            img_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            screen.blit(image_radar, img_rect)
            img_rect = button_typip.get_rect()
            img_rect.center = (450, 500)
            screen.blit(button_typip, img_rect)
            img_rect = button_vindip.get_rect()
            img_rect.center = (750, 500)
            screen.blit(button_vindip, img_rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and pygame.mouse.get_pos() >= (380, 475) and pygame.mouse.get_pos() <= (520, 525):
                        frame = 2
                    if event.button == 1 and pygame.mouse.get_pos() >= (680, 475) and pygame.mouse.get_pos() <= (820, 525):
                        frame = 3
        elif frame == 2:
            screen.fill((255, 255, 255))
            pygame.draw.rect(screen, (180, 180, 180), (350, 250, 500, 50))
            screen.blit((typfont.render("Typ IP: ", True, (0, 0, 0))), (550, 215))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and pygame.mouse.get_pos() >= (350, 250) and pygame.mouse.get_pos() <= (850, 300):
                        pygame.draw.rect(screen, (128, 128, 128), (350, 250, 500, 50))
                        pygame.display.flip()
                        return userinput_keyboard()
        elif frame == 3:
            global randomsearch, start2, start3, start4, startport
            randomsearch = True
            start2 = 1
            start3 = 1
            start4 = 1
            startport = 1
            return searchfordeviceonip()
        
        clock.tick(60)
    pygame.display.quit()
    pygame.quit()

def screen_tmp():
    client.sendall(("tmp" + "\n").encode())
    crnttmp = client.recv(1024).decode()
    screen.blit(typfont.render(f"Temperatuur: {crnttmp}", True, (0, 0, 0)), (5, 5))


def connect():
    global connected, loadingtext
    connected = True
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        loadingtext = str("Verbonden met het internet!")
        bootmessage()
    except OSError:
        loadingtext = str("Niet verbonden met het internet :(")
        bootmessage()
        connected = False
    if connected:
        loadingtext = str("Starten van setup.py...")
        bootmessage()
        main()
    else:
        pygame.display.quit()
        pygame.quit()
        while True:
            break

def main():
    global running, errortext
    menu = "setup"
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if menu == "setup":
            return screen_setup()
        elif menu == "temperatuur":
            return screen_tmp()
        else:
            errortext = str("Error: Deze functie bestaat niet")
            errormessage()

        pygame.display.flip()
    
        clock.tick(60)
    #Als het script voorbij is sluit dan pygame af
    pygame.display.quit()
    pygame.quit()

#Laden van onderdelen in het algemeen
#Laden van afbeeldingen
loadingtext = str("Loading: Assets/Buttons/temperatuur.png")
bootmessage()
button_tmp = pygame.image.load("Assets/Buttons/temperatuur.png")
#
loadingtext = str("Loading: Assets/Buttons/temperatuurgeselecteerd.png")
bootmessage()
button_tmpselected = pygame.image.load("Assets/Buttons/temperatuurgeselecteerd.png")
#
loadingtext = str("Loading: Assets/Buttons/camera.png")
bootmessage()
button_cam = pygame.image.load("Assets/Buttons/camera.png")
#
loadingtext = str("Loading: Assets/Buttons/camerageselecteerd.png")
bootmessage()
button_camselected = pygame.image.load("Assets/Buttons/camerageselecteerd.png")
#
loadingtext = str("Loading: Assets/Buttons/bewegingsensor.png")
bootmessage()
button_bwg = pygame.image.load("Assets/Buttons/bewegingsensor.png")
#
loadingtext = str("Loading: Assets/Buttons/bewegingsensorgeselecteerd.png")
bootmessage()
button_bwgselected = pygame.image.load("Assets/Buttons/bewegingsensorgeselecteerd.png")
#
loadingtext = str("Loading: Assets/Buttons/trillingsensor.png")
bootmessage()
button_trl = pygame.image.load("Assets/Buttons/trillingsensor.png")
#
loadingtext = str("Loading: Assets/Buttons/trillingsensorgeselecteerd.png")
bootmessage()
button_trlselected = pygame.image.load("Assets/Buttons/trillingsensorgeselecteerd.png")
#
loadingtext = str("Loading: Assets/Buttons/ventilatie.png")
bootmessage()
button_ven = pygame.image.load("Assets/Buttons/ventilatie.png")
#
loadingtext = str("Loading: Assets/Buttons/ventilatiegeselecteerd.png")
bootmessage()
button_venselected = pygame.image.load("Assets/Buttons/ventilatiegeselecteerd.png")
#
loadingtext = str("Loading: Assets/Buttons/warmtesensor.png")
bootmessage()
button_wrm = pygame.image.load("Assets/Buttons/warmtesensor.png")
#
loadingtext = str("Loading: Assets/Buttons/warmtesensorgeselecteerd.png")
bootmessage()
button_wrmselected = pygame.image.load("Assets/Buttons/warmtesensorgeselecteerd.png")
#
loadingtext = str("Loading: Assets/Images/radar.png")
bootmessage()
image_radar = pygame.image.load("Assets/Images/radar.png")
#
loadingtext = str("Loading: Assets/Buttons/vindip.png")
bootmessage()
button_vindip = pygame.transform.scale(pygame.image.load("Assets/Buttons/vindip.png"), (140, 50))
#
loadingtext = str("Loading: Assets/Buttons/typip.png")
bootmessage()
button_typip = pygame.transform.scale(pygame.image.load("Assets/Buttons/typip.png"), (140, 50))
#
loadingtext = str("Creating list: user_input")
bootmessage()
user_input = []
#
loadingtext = str("Loading: Assets/Buttons/ja.png")
bootmessage()
button_ja = pygame.transform.scale(pygame.image.load("Assets/Buttons/nee.png"), (140, 50))
#
loadingtext = str("Loading: Assets/Buttons/nee.png")
bootmessage()
button_nee = pygame.transform.scale(pygame.image.load("Assets/Buttons/nee.png"), (140, 50))

#Wachten voor 0.5 seconden
time.sleep(0.5)

#Kijken of ik ben verbonden met het internet
connect()