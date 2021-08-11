import pygame
import os
pygame.init()
pygame.mixer.init()
pygame.font.init()
# To be converted block shapes 
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

BLOCKS = [S, Z, I, O, J, L, T]

# some default colors to use
TOMATO_RED = pygame.Color("Tomato")
BLACK = pygame.Color("Black")
WHITE = pygame.Color("White")

COLOR_SCEHEME = { 
      'default': [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)], 
      'pastel': [(255, 173, 173), (255, 214, 165), (253, 255, 182), (202, 255, 191), (155, 246, 255), (160, 196, 255), (189, 178, 255)],
      'neon': [(116, 0, 184), (94, 96, 206), (83, 144, 217), (78, 168, 222), (72, 191, 227), (86, 207, 225), (128, 255, 219)],
      'warm': [(249, 65, 68), (249, 65, 68), (249, 199, 79), (144, 190, 109), (67, 170, 139), (87, 117, 144), (39, 125, 161)]
}

# Basic settings for the game
COLUMN = 10
ROW = 20
BLOCK_SIZE = 30

WIN_WIDTH = 400
WIN_HEIGHT = 710

FIELD_WIDTH = COLUMN * BLOCK_SIZE
FIELD_HEIGHT = ROW * BLOCK_SIZE
FIELD_X = (WIN_WIDTH - FIELD_WIDTH) // 2 
FIELD_Y = WIN_HEIGHT - FIELD_HEIGHT - 20

MIDDLE_OF_SCREEN_X = WIN_WIDTH // 2

FPS = 25
ROW_NEEDED_TO_LEVEL_UP = 5

# Level System
LEVEL_SYSTEM = {
      1: 500,
      2: 475,
      3: 450,
      4: 425,
      5: 400,
      6: 375,
      7: 350,
      8: 325,
      9: 300,
      10: 275,
      11: 275,
      12: 225,
      13: 225,
      14: 175,
      15: 175,
      16: 150,
      17: 150,
      18: 125,
      20: 125,
      20: 100,
      21: 90,
      22: 80,
      23: 70,
      24: 60,
      25: 50,
}

# scoring system
SCORE_SYSTEM = {
      1: 50,
      2: 100,
      3: 200,
      4: 400,
      "hard_drop": 5
}

# timer for events in th game
GAME_SPEED = pygame.USEREVENT

# SFX for the game
pygame.mixer.music.load(os.path.join(os.getcwd(), 'utils','musics', 'Tetris.mp3'))
pygame.mixer.music.set_volume(0.1)
CLEAR_ROW_SFX = pygame.mixer.Sound(os.path.join(os.getcwd(), 'utils','musics', 'clear.wav'))
BLOCK_COLLIDE_SFX = pygame.mixer.Sound(os.path.join(os.getcwd(), 'utils','musics', 'fall.wav'))
CLICK_SFX = pygame.mixer.Sound(os.path.join(os.getcwd(), 'utils','musics', 'selection.wav'))
HOVER_SFX = pygame.mixer.Sound(os.path.join(os.getcwd(), 'utils','musics', 'hover.mp3'))

# BBackground for the game
BACKGROUND = {
      "STARRY_BACKGROUND": pygame.image.load(os.path.join(os.getcwd(), 'utils','images', 'evening_background.jpg')),
      "SCENARY_BACKGROUND": pygame.image.load(os.path.join(os.getcwd(), 'utils','images', 'scenary_background.jpg')),
      "NIGHT_CITY_BACKGROUND": pygame.image.load(os.path.join(os.getcwd(), 'utils','images', 'night_city.gif'))
}

# Font
RETRO_FONT = os.path.join(os.getcwd(), 'utils','fonts', 'Retro_Gaming.ttf')
TETRIS_LOGO_FONT = os.path.join(os.getcwd(), 'utils','fonts', '8-bit.ttf')

# 8-Bit buton png
SOUND_BUTTON_ON = pygame.image.load(os.path.join(os.getcwd(), 'utils','images', 'sound_on.png'))
SOUND_BUTTON_OFF = pygame.image.load(os.path.join(os.getcwd(), 'utils','images', 'sound_off.png'))

# Button Positions!
PLAY_BUTTON_WIDTH = 120
PLAY_BUTTON_HEIGHT = 60
PLAY_BUTTON_X = (WIN_WIDTH - PLAY_BUTTON_WIDTH)//2 
PLAY_BUTTON_Y = 385
PLAY_BUTTON = pygame.Rect((PLAY_BUTTON_X, PLAY_BUTTON_Y),(PLAY_BUTTON_WIDTH, PLAY_BUTTON_HEIGHT))
PLAY_BUTTON.centerx = MIDDLE_OF_SCREEN_X

SOUND_BUTTON_WIDTH = 50
SOUND_BUTTON_HEIGHT = 50
SOUND_BUTTON_X = WIN_WIDTH - 70
SOUND_BUTTON_Y = WIN_HEIGHT - 70
SOUND_BUTTON = pygame.Rect((SOUND_BUTTON_X, SOUND_BUTTON_Y),(SOUND_BUTTON_WIDTH, SOUND_BUTTON_HEIGHT))

TETRIS_MENU_LOGO_WIDTH = 350
TETRIS_MENU_LOGO_HEIGHT = 100
TETRIS_MENU_LOGO_X = (WIN_WIDTH - TETRIS_MENU_LOGO_WIDTH)//2 
TETRIS_MENU_LOGO_Y = 225
TETRIS_MENU_LOGO = pygame.Rect((TETRIS_MENU_LOGO_X, TETRIS_MENU_LOGO_Y),(TETRIS_MENU_LOGO_WIDTH, TETRIS_MENU_LOGO_HEIGHT))
TETRIS_MENU_LOGO.centerx = MIDDLE_OF_SCREEN_X

TETRIS_GAME_LOGO_WIDTH = 250
TETRIS_GAME_LOGO_HEIGHT = 80
TETRIS_GAME_LOGO_X = (WIN_WIDTH - TETRIS_GAME_LOGO_WIDTH)//2 
TETRIS_GAME_LOGO_Y = 10
TETRIS_GAME_LOGO = pygame.Rect((TETRIS_GAME_LOGO_X, TETRIS_GAME_LOGO_Y),(TETRIS_GAME_LOGO_WIDTH, TETRIS_GAME_LOGO_HEIGHT))
TETRIS_GAME_LOGO.centerx = MIDDLE_OF_SCREEN_X
 
SCOREBOARD_WIDTH = 140
SCOREBOARD_HEIGHT = 50
SCOREBOARD_X = (WIN_WIDTH  - SCOREBOARD_WIDTH)//2 
SCOREBOARD_Y = 250
SCOREBOARD =  pygame.Rect((SCOREBOARD_X, SCOREBOARD_Y),(SCOREBOARD_WIDTH, SCOREBOARD_HEIGHT))

LEVEL_WIDTH = 250
LEVEL_HEIGHT = 80
LEVEL_X = (WIN_WIDTH - LEVEL_WIDTH)//2 
LEVEL_Y = 160
LEVEL = pygame.Rect((LEVEL_X, LEVEL_Y),(LEVEL_WIDTH, LEVEL_HEIGHT))

DRAW_GRID_LINES = False
BLOCK_COLOR = COLOR_SCEHEME['default']
BACKGROUND = BACKGROUND["SCENARY_BACKGROUND"]
SOUND_CHANNEL = pygame.mixer.Channel(0)
SOUND_VOLUME = 0.2


