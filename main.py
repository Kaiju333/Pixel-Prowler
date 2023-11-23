import pygame
import random
from settings import screen_width, screen_height
from level import Level, ai_generate_level

pygame.init()
pygame.font.init()
startMenu = True
gameRunning = True
chooseCharacterScreen = True
generate_certificate = False
userInputText = ""
inputBoxActive = False
inputBoxRect = pygame.Rect(315, 240, 250, 36)
reset_background = False
mute = False
startMenuTitleFont = pygame.font.Font("RussoOne-Regular.ttf", 84)
startMenuTextFont = pygame.font.SysFont(None, 24)
tutorialTitleFont = pygame.font.SysFont(None, 72)
tutorialTextFont = pygame.font.SysFont(None, 36)
certificateFont = pygame.font.Font("AlexBrush-Regular.ttf", 84)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pixel Prowler")
clock = pygame.time.Clock()
level = Level(screen)
background_number, music_number = random.randint(1,13), random.randint(1,3)
background_image = pygame.image.load(f"background_image{background_number}.png")
pygame.mixer.music.load(f"backgroundMusic{music_number}.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
white = (255,255,255)
black = (0,0,0)
grey = (140,140,140)
light_grey = (190,190,190)
startButton = pygame.image.load("startButton.png")
startButtonHover = pygame.image.load("startButtonHover.png")
tutorialButton = pygame.image.load("tutorialButton.png")
tutorialButtonHover = pygame.image.load("tutorialButtonHover.png")
quitButton = pygame.image.load("quitButton.png")
quitButtonSmall = pygame.image.load("quitButtonSmall.png")
quitButtonHover = pygame.image.load("quitButtonHover.png")
quitButtonSmallHover = pygame.image.load("quitButtonSmallHover.png")
speaker_icon = pygame.image.load("speaker.png")
mute_icon = pygame.image.load("mute.png")
speaker_hover_icon = pygame.image.load("speakerHover.png")
mute_hover_icon = pygame.image.load("muteHover.png")
title = startMenuTitleFont.render("Pixel Prowler", True, black)
text = startMenuTextFont.render("A game that uses AI to generate all its levels", True, black)
tutorialTitle1Text = tutorialTitleFont.render("Keybinds", True, black)
tutorialMovementText = tutorialTextFont.render("A, D  /  Left Arrow, Right Arrow  -  Horizontal Movement", True, black)
tutorialJumpText = tutorialTextFont.render("W  /  Space  /  Up Arrow  -  Jump", True, black)
tutorialSprintText = tutorialTextFont.render("Shift  -  Sprint", True, black)
tutorialQuitText = tutorialTextFont.render("Press Alt+F4 to rage quit (It will be helpful if you're constantly dying)", True, black)
tutorialTitle2Text = tutorialTitleFont.render("Aim", True, black)
tutorialAimText = tutorialTextFont.render("Complete 100 levels in a row without dying to win the game! Cool background and music at Level 60!", True, black)
generateCertificateText = tutorialTextFont.render("Enter your name below to generate your certificate for completing the game:", True, black)

while True:
  if generate_certificate:
    certificate = pygame.image.load(f"certificate{level.trophy_number}.png")
    while generate_certificate:
      mouse = pygame.mouse.get_pos()
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
          if (mouse[0] >= 315 and mouse[0] <= 315 + inputBoxRect.w) and (mouse[1] >= 240 and mouse[1] <= 276):
            inputBoxActive = True
          else:
            inputBoxActive = False
          if (mouse[0] >= 1450 and mouse[0] <= 1510) and (mouse[1] >= 10 and mouse[1] <= 70):
            if mute:
              pygame.mixer.music.set_volume(0.3)
              mute = False
            else:
              pygame.mixer.music.set_volume(0)
              mute = True
        if event.type == pygame.KEYDOWN and inputBoxActive:
          if event.key == pygame.K_RETURN:
            certificateText = certificateFont.render(userInputText, True, black)
            certificateTextRect = certificateText.get_rect(center=(screen_width/2, screen_height/2))
            screen.fill(white)
            screen.blit(pygame.transform.smoothscale(certificate, (1089, 770)), (216,0))
            screen.blit(certificateText, certificateTextRect)
            pygame.display.update()
            while generate_certificate:
              keys = pygame.key.get_pressed()
              for event in pygame.event.get():
                if event.type == pygame.QUIT:
                  quit()
              if keys[pygame.K_ESCAPE]:
                generate_certificate = False
                startMenu = True
                background_number, music_number = random.randint(1,13), random.randint(1,3)
                background_image = pygame.image.load(f"background_image{background_number}.png")
                pygame.mixer.music.load(f"backgroundMusic{music_number}.mp3")
                pygame.mixer.music.play(-1)
                break
          if event.key == pygame.K_BACKSPACE:
            userInputText = userInputText[:-1]
          else:
            if len(userInputText) <= 50:
              userInputText += event.unicode
      screen.fill(white)
      screen.blit(generateCertificateText, (315, 200))
      if inputBoxActive or ((mouse[0] >= 315 and mouse[0] <= 315 + inputBoxRect.w) and (mouse[1] >= 240 and mouse[1] <= 276)):
        colour = light_grey
      else:
        colour = grey
      pygame.draw.rect(screen, colour, inputBoxRect)
      inputText = tutorialTextFont.render(userInputText, True, black)
      screen.blit(inputText, (inputBoxRect.x+5, inputBoxRect.y+5))
      inputBoxRect.w = max(250, inputText.get_width()+10)
      if mute:
        if (mouse[0] >= 1450 and mouse[0] <= 1510) and (mouse[1] >= 10 and mouse[1] <= 70):
          screen.blit(mute_hover_icon, (1450, 10))
        else:
          screen.blit(mute_icon, (1450, 10))
      else:
        if (mouse[0] >= 1450 and mouse[0] <= 1510) and (mouse[1] >= 10 and mouse[1] <= 70):
          screen.blit(speaker_hover_icon, (1450, 10))
        else:
          screen.blit(speaker_icon, (1450, 10))
      pygame.display.update()

  if startMenu:
    if level.high_score == "100% Game Complete!":
      highScoreText = tutorialTextFont.render(f"Highest Level Reached: {level.high_score}", True, black)
    else:
      highScoreText = tutorialTextFont.render(f"Highest Level Reached: Level {level.high_score}", True, black)
    while startMenu:
      mouse = pygame.mouse.get_pos()
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
          if (mouse[0] >= 622 and mouse[0] <= 922) and (mouse[1] >= 220 and mouse[1] <= 326):
            while chooseCharacterScreen:
              chooseCharacterScreen = level.chooseCharacter()
              pygame.display.update()        
            level.setup_level(ai_generate_level())
            startMenu = False
            gameRunning = True
            chooseCharacterScreen = True
          if (mouse[0] >= 636 and mouse[0] <= 936) and (mouse[1] >= 540 and mouse[1] <= 646):
            quit()
          if (mouse[0] >= 1450 and mouse[0] <= 1510) and (mouse[1] >= 10 and mouse[1] <= 70):
            if mute:
              pygame.mixer.music.set_volume(0.3)
              mute = False
            else:
              pygame.mixer.music.set_volume(0)
              mute = True
          if (mouse[0] >= 551 and mouse[0] <= 1019) and (mouse[1] >= 380 and mouse[1] <= 486):
            tutorialMenu = True
            screen.fill(white)
            screen.blit(tutorialTitle1Text, (655, 50))
            screen.blit(tutorialMovementText, (452, 140))
            screen.blit(tutorialJumpText, (580, 200))
            screen.blit(tutorialSprintText, (688, 260))
            screen.blit(tutorialQuitText, (368, 320))
            screen.blit(tutorialTitle2Text, (722, 430))
            screen.blit(tutorialAimText, (186, 510))
            while tutorialMenu:
              mouse = pygame.mouse.get_pos()
              for event in pygame.event.get():
                if event.type == pygame.QUIT:
                  quit()
                if event.type == pygame.MOUSEBUTTONDOWN and (mouse[0] >= 656 and mouse[0] <= 881) and (mouse[1] >= 625 and mouse[1] <= 705):
                  tutorialMenu = False
              if (mouse[0] >= 656 and mouse[0] <= 881) and (mouse[1] >= 625 and mouse[1] <= 705):
                screen.blit(quitButtonSmallHover, (656, 625))
              else:
                screen.blit(quitButtonSmall, (656, 625))
              pygame.display.update()

        screen.fill(white)
        screen.blit(title, (500, 50))
        screen.blit(text, (608, 140))
        if (mouse[0] >= 636 and mouse[0] <= 936) and (mouse[1] >= 220 and mouse[1] <= 326):
          screen.blit(startButtonHover, (636, 220))
        else:
          screen.blit(startButton, (636, 220))
        if (mouse[0] >= 551 and mouse[0] <= 1019) and (mouse[1] >= 380 and mouse[1] <= 486):
          screen.blit(tutorialButtonHover, (551, 380))
        else:
          screen.blit(tutorialButton, (551, 380))
        if (mouse[0] >= 636 and mouse[0] <= 936) and (mouse[1] >= 540 and mouse[1] <= 646):
          screen.blit(quitButtonHover, (636, 540))
        else:
          screen.blit(quitButton, (636, 540))
        if mute:
          if (mouse[0] >= 1450 and mouse[0] <= 1510) and (mouse[1] >= 10 and mouse[1] <= 70):
            screen.blit(mute_hover_icon, (1450, 10))
          else:
            screen.blit(mute_icon, (1450, 10))
        else:
          if (mouse[0] >= 1450 and mouse[0] <= 1510) and (mouse[1] >= 10 and mouse[1] <= 70):
            screen.blit(speaker_hover_icon, (1450, 10))
          else:
            screen.blit(speaker_icon, (1450, 10))
        if level.high_score == "100% Game Complete!":
          screen.blit(highScoreText, (960, 720))
        else:
          screen.blit(highScoreText, (1125, 720))
        pygame.display.update()

  while gameRunning:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        quit()

    screen.blit(pygame.transform.smoothscale(background_image, (screen_width, screen_height)), (0,0))
    level.run()
    gameRunning, startMenu, reset_background, generate_certificate = level.game_over()
    if level.switch_background:
      if level.level_number == 101:
        background_image = pygame.image.load(f"background_image23.png")
      elif level.level_number == 100:
        background_image = pygame.image.load(f"background_image22.png")
      elif level.level_number >= 60:
        background_number = random.randint(14,21)
        background_image = pygame.image.load(f"background_image{background_number}.png")
      else:
        background_number = random.randint(1,13)
        background_image = pygame.image.load(f"background_image{background_number}.png")
      level.switch_background = False
    if reset_background:
      background_number = random.randint(1,13)
      background_image = pygame.image.load(f"background_image{background_number}.png")
      reset_background = False

    pygame.display.update()
    clock.tick(60)
