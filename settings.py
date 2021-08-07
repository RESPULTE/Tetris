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
GREY = pygame.Color("Grey")
BLUE = pygame.Color("Blue")
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

GAME_FPS = 25
MENU_FPS = 15

# scoring system
SCORE_SYSTEM = {
      1: 100,
      2: 300,
      3: 500,
      4: 800,
      "hard_drop": 10,
      "soft_drop": 5
}

# SFX for the game
pygame.mixer.music.load(os.path.join(os.getcwd(), 'utils','musics', 'Tetris.mp3'))
CLEAR_ROW_SFX = pygame.mixer.Sound(os.path.join(os.getcwd(), 'utils','musics', 'clear.wav'))
BLOCK_COLLIDE_SFX = pygame.mixer.Sound(os.path.join(os.getcwd(), 'utils','musics', 'fall.wav'))
CLICK_SFX = pygame.mixer.Sound(os.path.join(os.getcwd(), 'utils','musics', 'selection.wav'))
HOVER_SFX = pygame.mixer.Sound(os.path.join(os.getcwd(), 'utils','musics', 'hover.mp3'))

# BBackground for the game
BACKGROUND = {
      "STARRY_BACKGROUND": pygame.image.load(os.path.join(os.getcwd(), 'utils','images', 'evening_background.jpg')),
      "SCENARY_BACKGROUND": pygame.image.load(os.path.join(os.getcwd(), 'utils','images', 'scenary_background.jpg')),
      "CITY_LIFE_BACKGROUND": pygame.image.load(os.path.join(os.getcwd(), 'utils','images', 'hongkong_2.gif')),
      "CITYSCAPE_BACKGROUND": pygame.image.load(os.path.join(os.getcwd(), 'utils','images', 'city.gif')),
      "JAPAN_STREET_BACKGROUND": pygame.image.load(os.path.join(os.getcwd(), 'utils','images', 'japan_2.gif')),
      "CITYSCAPE_JAPAN_BACKGROUND": pygame.image.load(os.path.join(os.getcwd(), 'utils','images', 'japan.gif')),
      "MARIO_BACKGROUND": pygame.image.load(os.path.join(os.getcwd(), 'utils','images', 'mario.jpg')),
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

SOUND_BUTTON_WIDTH = 50
SOUND_BUTTON_HEIGHT = 50
SOUND_BUTTON_X = WIN_WIDTH - 70
SOUND_BUTTON_Y = WIN_HEIGHT - 70
SOUND_BUTTON = pygame.Rect((SOUND_BUTTON_X, SOUND_BUTTON_Y),(SOUND_BUTTON_WIDTH, SOUND_BUTTON_HEIGHT))

TETRIS_MENU_LOGO_WIDTH = 350
TETRIS_MENU_LOGO_HEIGHT = 100
TETRIS_MENU_LOGO_X = (WIN_WIDTH - TETRIS_MENU_LOGO_WIDTH)//2 + 5
TETRIS_MENU_LOGO_Y = 225
TETRIS_MENU_LOGO = pygame.Rect((TETRIS_MENU_LOGO_X, TETRIS_MENU_LOGO_Y),(TETRIS_MENU_LOGO_WIDTH, TETRIS_MENU_LOGO_HEIGHT))

TETRIS_GAME_LOGO_WIDTH = 250
TETRIS_GAME_LOGO_HEIGHT = 80
TETRIS_GAME_LOGO_X = (WIN_WIDTH - TETRIS_GAME_LOGO_WIDTH)//2
TETRIS_GAME_LOGO_Y = 10
TETRIS_GAME_LOGO = pygame.Rect((TETRIS_GAME_LOGO_X, TETRIS_GAME_LOGO_Y),(TETRIS_GAME_LOGO_WIDTH, TETRIS_GAME_LOGO_HEIGHT))

DRAW_GRID_LINES = False
GAME_SOUND = True
BLOCK_COLOR = COLOR_SCEHEME['default']
BACKGROUND = BACKGROUND["STARRY_BACKGROUND"]
SOUND_CHANNEL = pygame.mixer.Channel(0)

