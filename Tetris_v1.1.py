from utils import *

class Block:

      def __init__(self, x, y):
            self.x = x
            self.y = y
            self.rotation = 0
            self.shape = random.choice(BLOCKS)
            self.color = BLOCK_COLOR[BLOCKS.index(self.shape)]   

      def convert_to_positions(self):
            positions = []
            for j, row in enumerate(self.shape[self.rotation]):
                  for i, col in enumerate(row):
                        if col == "0":
                              positions.append((self.x + i-2, self.y + j-4))   
            return positions

      def __str__(self):
            return f"X: {self.x} |Y: {self.y}| rotation:{self.rotation}\npositions:{self.convert_to_positions()}"

class Tetris:

      def __init__(self):
            self.grid = [[BLACK for _ in range(COLUMN)] for _ in range(ROW)]
            self.block = Block(5, 0)
            self.locked_positions = {}
            self.block_positions = []
            self.accepted_position = []
            self.paused = False
            self.total_cleared_row = 0
            self.level = 1
            self.speed = LEVEL_SYSTEM[self.level]
            self.score = 0
            self.delay = 0

      def handle_user_input(self, event):
            if event.key == pygame.K_SPACE:
                  self.paused = not self.paused
            if not self.paused:
                  if event.key == pygame.K_d:
                        self.block.x += 1
                        if self.check_collisions():
                              self.block.x -= 1
                  elif event.key == pygame.K_a:
                        self.block.x -= 1
                        if self.check_collisions():
                              self.block.x += 1
                  elif event.key == pygame.K_w:
                        self.block.rotation = (self.block.rotation + 1) % len(self.block.shape)
                        if self.check_collisions():
                              self.block.rotation = (self.block.rotation - 1) % len(self.block.shape)
                  elif event.key == pygame.K_s:
                        self.hard_drop()
                        if self.check_collisions():
                              self.block.y -= 1
                              return True

      def update_grid(self):
            self.block_positions = self.block.convert_to_positions()
            for pos in self.block_positions:
                  i, j = pos
                  if pos[1] > -1:
                        self.grid[j][i] = self.block.color

      def refresh_grid(self):
            self.grid = [[self.locked_positions[(i, j)] if (i, j) in self.locked_positions else BLACK for i in range(COLUMN)] for j in range(ROW)]

      def refresh_accepted_positions(self):
            self.accepted_position = [(i, j) for j in range(-4, ROW) for i in range(COLUMN) if (i, j) not in self.locked_positions]

      def check_lost(self):
            self.block_positions = self.block.convert_to_positions()
            for pos in self.block_positions:
                  if pos[1] <= 0:
                        return True

      def check_collisions(self):
            self.refresh_accepted_positions()
            # Needs to call this function twice so that the positions being used is the latest
            self.block_positions = self.block.convert_to_positions()
            for pos in self.block_positions:
                  if pos not in self.accepted_position:
                        return True

      def update_score_level(self, rows_cleared=0, drop=None):

            if rows_cleared:
                  score_gained = SCORE_SYSTEM[rows_cleared] 
            if drop:
                  score_gained = SCORE_SYSTEM[drop] 
            self.score += (score_gained * (self.level//2))

            self.total_cleared_row += rows_cleared
            if self.total_cleared_row >= ROW_NEEDED_TO_LEVEL_UP:
                  self.total_cleared_row -= ROW_NEEDED_TO_LEVEL_UP
                  self.level += 1
                  if self.level <= len(LEVEL_SYSTEM):
                        pygame.time.set_timer(GAME_SPEED, self.speed)

      def lock_old_spawn_new(self):
            self.block_positions = self.block.convert_to_positions()
            for (i, j) in self.block_positions:
                  self.locked_positions[(i, j)] = self.block.color
            self.block = Block(COLUMN//2, 0)

      def hard_drop(self):
            self.refresh_accepted_positions()
            while set(self.block_positions).issubset(self.accepted_position):
                  self.block.y +=1
                  self.block_positions = self.block.convert_to_positions()

      def check_clear_rows(self):
            rows_cleared = []
            for j in range(ROW-1, -1, -1):
                  if BLACK not in self.grid[j]:
                        for i in range(COLUMN):
                              rows_cleared.append((i, j))
                              try:
                                    del self.locked_positions[(i, j)]
                              except:
                                    continue
            return rows_cleared
            
      def move_rows_down(self):
            block_groups = self.calibrate_block_positions()
            sorted_block_groups = sorted(block_groups, key=lambda x: list(x.keys())[0][1], reverse=True)

            for ind, block_clump in enumerate(sorted_block_groups):
                  self.refresh_accepted_positions()
                  sorted_locked_positions = sorted(block_clump, key=lambda pos: pos[0], reverse=True)
                  new_block_clump_bottom_pos = [max(items) for key, items in groupby(sorted_locked_positions, key = itemgetter(0))]
                  old_block_clump_bottom_pos = new_block_clump_bottom_pos.copy()

                  if len(self.grid)-1 not in set(map(lambda x: x[1], new_block_clump_bottom_pos)):
                        temp_accepted_pos = [(i, j) for (i, j) in self.accepted_position for (x, y) in new_block_clump_bottom_pos if i == x]
                        while set(new_block_clump_bottom_pos).issubset(temp_accepted_pos):
                              new_block_clump_bottom_pos = [(i, j+1) for (i, j) in new_block_clump_bottom_pos]
                        else:
                              new_block_clump_bottom_pos = [(i, j-1) for (i, j) in new_block_clump_bottom_pos]
                        offset = new_block_clump_bottom_pos[0][1] - old_block_clump_bottom_pos[0][1]
                        block_clump = {(i, j + offset): v for (i,j), v in block_clump.items()}

                  self.locked_positions.update(block_clump)

      def calibrate_block_positions(self):
            self.refresh_grid()
            def floodfill(matrix, j, i, block_clump):
                #"hidden" stop clause - not reinvoking for "c" or "b", only for "a".
                if matrix[j][i] != BLACK:  
                    matrix[j][i] = BLACK 
                    block_clump.append((i, j))
                    #recursively invoke flood fill on all surrounding cells:
                    if j > 0:
                        floodfill(matrix,j-1,i, block_clump)
                    if i < len(matrix[i]) - 1:
                        floodfill(matrix,j,i+1, block_clump)
                    if i > 0:
                        floodfill(matrix,j,i-1, block_clump)
                    if j < len(matrix) - 1:
                        floodfill(matrix,j+1,i, block_clump)

                return block_clump

            block_groups = []
            while self.locked_positions:
                  block_clump = []
                  block_dict = {}
                  i, j = random.choice(list(self.locked_positions.keys()))
                  detected_clump = floodfill(self.grid, j, i, block_clump)

                  for pos in detected_clump:
                        block_color = self.locked_positions.pop((pos))
                        block_dict[pos] = block_color

                  block_groups.append(block_dict)

            return block_groups

      def __str__(self):
            self.refresh_accepted_positions()
            print('\n')
            temp_grid = ''
            for j, row in enumerate(self.grid):

                  for i, col in enumerate(row):
                        temp_grid += '[0]' if (i, j) in self.accepted_position else '[ ]'

                  temp_grid += '\n'

            return temp_grid

class Render:

      def __init__(self, win_width, win_height):
            self.win_width = win_width 
            self.win_height = win_height
            self.win = pygame.display.set_mode((self.win_width, self.win_height))
            self.decrement = 0
            self.increment = 0
            self.animation_delay = 250
            self.timer = 0

      def draw_field(self, grid, cleared_row=[]):
            self.draw_screen(alpha_value=125, rect=(FIELD_X, FIELD_Y, FIELD_WIDTH, FIELD_HEIGHT), color=BLACK)
            pygame.draw.rect(self.win, TOMATO_RED, ((FIELD_X, FIELD_Y), (FIELD_WIDTH, FIELD_HEIGHT)), 9)

      def draw_text(self, text, rect, font, color=WHITE, font_size=150, transform=False, hover=False, border=False, border_radius=6):
            myfont = pygame.font.Font(font, font_size)
            label = myfont.render(text, 1, color)
            if hover:      
                  label = myfont.render(text, False, BLACK, color)
                  label.set_colorkey(BLACK)
            if transform:
                  rect = rect.inflate(-15, -15)  
                  label = pygame.transform.scale(label, (rect.width+1, rect.height))
                  text_rect = label.get_rect(x=rect.x, y=rect.y)
            if border:
                  rect.width += 8
                  rect.x -= 4
                  pygame.draw.rect(self.win, color, rect, 4, border_radius)

            self.win.blit(label, text_rect)

      def draw_block(self, grid):
            # divide the offset into multiple "sections"
            # the divided offset must reach the original offset value in the time of self.animation_delay
            for j, row in enumerate(grid):
                  for i, color in enumerate(row):
                        if color != BLACK:
                              rect = ((i * BLOCK_SIZE + FIELD_X, j * BLOCK_SIZE + FIELD_Y), (BLOCK_SIZE, BLOCK_SIZE)) 
                              pygame.draw.rect(self.win, color, rect, border_radius=6) 
                              pygame.draw.rect(self.win, WHITE, rect, 3, border_radius=6)

      def make_block_fade_white(self, block_to_fade, dt):
            self.timer += dt
            self.increment +=1.7
            for (i, j) in block_to_fade:
                  rect = pygame.Rect((i * BLOCK_SIZE + FIELD_X, j * BLOCK_SIZE + FIELD_Y), (BLOCK_SIZE, BLOCK_SIZE))
                  rect.inflate_ip(int(self.increment), int(self.increment))
                  if self.increment <= 4:
                        pygame.draw.rect(self.win, WHITE, rect, border_radius=6)
                  pygame.draw.rect(self.win, WHITE, rect, 3, border_radius=6)
            if self.timer > self.animation_delay:
                  self.increment = 0
                  self.timer = 0
                  return True

      def draw_background(self, image):
            self.decrement -= 0.5
            img_width = image.get_width()
            background_img = pygame.transform.scale(image, (img_width, self.win_height))
            # spawns 2 image of the background
            # --> one right where the screen is, the other by the 1st image's right side
            self.win.blit(background_img, (self.decrement, 0))
            self.win.blit(background_img, (img_width + self.decrement, 0))
            # if the 1st image has reached the end of the screen, 
            # spawns in the 3rd image next to the 2nd image to fill in the gap
            if self.decrement == -img_width:
                  self.win.blit(background_img, (self.win_width - self.decrement, 0))
                  self.decrement = 0

      def draw_pause_screen(self):
            self.draw_screen(alpha_value=125, rect=(0, 0, WIN_WIDTH, WIN_HEIGHT), color=BLACK)
            self.draw_screen(rect=(TETRIS_MENU_LOGO.inflate(100, 20)), color=TOMATO_RED)
            self.draw_text(text="PAUSED", rect=TETRIS_MENU_LOGO, font=RETRO_FONT, transform=True)

      def draw_screen(self, rect, color, alpha_value=255):
            x, y, width, height = rect
            smoke_screen = pygame.Surface((width, height))
            smoke_screen.set_alpha(alpha_value)
            smoke_screen.fill(color)
            self.win.blit(smoke_screen, (x, y))

      def draw_button(self, button):
            start_pos_x, start_pos_y, width, height = button.rect
            pygame.draw.rect(self.win, button.color, button.rect, 5)
            if button.image != None:
                  new_rect = button.rect.inflate(-15, -15)
                  new_x, new_y, new_width, new_height = new_rect
                  formatted_img = pygame.transform.scale(button.image, (new_width, new_height))
                  pygame.draw.rect(self.win, button.color, new_rect)
                  self.win.blit(formatted_img, (new_x, new_y))
            if button.text != None:
                  self.draw_text(text=button.text, rect=button.rect, font=button.font, color=button.color, hover=button.hover, transform=True)

class Button:


      def __init__(self, rect, function, image=None, text=None, clicked_image=None):
            self.rect = rect
            self.function = function
            self.default_image = image
            self.text = text
            self.clicked_image = clicked_image
            self.font = RETRO_FONT 
            self.color = WHITE
            self.hover = False
            self.image = self.default_image

      def handle_button(self, event, mouse_position, args=None):
            if self.rect.collidepoint(mouse_position):
                  hover_old = self.hover
                  self.hover = True
                  if event.type == pygame.MOUSEMOTION:
                        if hover_old == False and self.hover == True:
                              SOUND_CHANNEL.play(HOVER_SFX)
                  if event.type == pygame.MOUSEBUTTONDOWN:
                        self.image = self.clicked_image if self.image == self.default_image else self.default_image
                        SOUND_CHANNEL.play(CLICK_SFX)
                        self.function()
            else:
                  self.hover = False

      @staticmethod
      def toggle_sound():
            if SOUND_CHANNEL.get_volume()==0.0:
                  SOUND_CHANNEL.set_volume(SOUND_VOLUME)
            else:
                  SOUND_CHANNEL.set_volume(0)

def play_game():

      clock = pygame.time.Clock()
      rendy = Render(WIN_WIDTH, WIN_HEIGHT)
      tetris = Tetris()
      pygame.time.set_timer(GAME_SPEED, LEVEL_SYSTEM[1])
      if SOUND_CHANNEL.get_volume() != 0.0:
            pygame.mixer.music.play(-1)
      run = True
      cleared_row = []
      time_passed = 0
      delay = 0
      hard_drop = False

      while run:
            
            # refresh the grid every run to clear out the place that has been overwritten by the block piece
            # i.e the places where the block piece has travelled across &  aren't in the dicitonary of locked positions
            tetris.refresh_grid()
            tetris.update_grid()
            dt = clock.get_time()

            # MAIN GAME LOOP
            for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                        run = False
                        sys.exit()

                  if event.type == pygame.KEYDOWN:
                        hard_drop = tetris.handle_user_input(event)

                  if event.type == GAME_SPEED:
                        if not tetris.paused:
                              tetris.block.y += 1
                              if tetris.check_collisions():
                                    delay += dt
                                    tetris.block.y -= 1
                                    if tetris.check_lost():
                                          pygame.mixer.music.stop()
                                          run = False
                                    tetris.lock_old_spawn_new()
                                    cleared_row = tetris.check_clear_rows()
                                    SOUND_CHANNEL.play(BLOCK_COLLIDE_SFX) 

            # MAIN RENDERING CODE BLOCK
            rendy.draw_background(BACKGROUND)
            rendy.draw_text(text=f"SCORE: {tetris.score}", font=RETRO_FONT, rect=SCOREBOARD, transform=True, border=True, hover=True)
            rendy.draw_text(text=f"LEVEL: {tetris.level}", font=RETRO_FONT, rect=LEVEL, transform=True, border=True, hover=True)
            rendy.draw_text(text="TETRIS", font=TETRIS_LOGO_FONT, rect=TETRIS_GAME_LOGO.move(5, 5), transform=True, color=BLACK)
            rendy.draw_text(text="TETRIS", font=TETRIS_LOGO_FONT, rect=TETRIS_GAME_LOGO, transform=True)
            rendy.draw_field(tetris.grid)
            rendy.draw_block(tetris.grid)

            # CHECK FOR SPECIAL CONDITITIONS
            if hard_drop:
                  pygame.event.set_blocked([GAME_SPEED, pygame.KEYDOWN])
                  tetris.update_score_level(drop="hard_drop")
                  if rendy.make_block_fade_white(tetris.block.convert_to_positions(), dt):
                        pygame.event.set_allowed([GAME_SPEED, pygame.KEYDOWN])
                        hard_drop = False

            if cleared_row:
                  SOUND_CHANNEL.play(CLEAR_ROW_SFX)
                  # stop the game for however long the animation delay is
                  pygame.event.set_blocked([GAME_SPEED, pygame.KEYDOWN])
                  if rendy.make_block_fade_white(cleared_row, dt):
                        tetris.move_rows_down()
                        tetris.update_score_level(rows_cleared=len(cleared_row)//10)
                        pygame.event.set_allowed([GAME_SPEED, pygame.KEYDOWN])
                        cleared_row.clear()

            if tetris.paused:
                  rendy.draw_pause_screen()
                  pygame.mixer.music.pause()
            else:
                  pygame.mixer.music.unpause()

            clock.tick(FPS)
            pygame.display.update()
            
def main():

      rendy = Render(WIN_WIDTH, WIN_HEIGHT)
      clock = pygame.time.Clock()
      play_button = Button(rect=PLAY_BUTTON, text='PLAY', function=play_game)
      sound_button = Button(rect=SOUND_BUTTON, image=SOUND_BUTTON_ON, clicked_image=SOUND_BUTTON_OFF, function=Button.toggle_sound)
      SOUND_CHANNEL.set_volume(SOUND_VOLUME)
      run = True

      while run:

            for event in pygame.event.get():
                  mouse_pos = pygame.mouse.get_pos()
                  if event.type == pygame.QUIT:
                        run = False
                  play_button.handle_button(event=event, mouse_position=mouse_pos)
                  sound_button.handle_button(event=event, mouse_position=mouse_pos)

            rendy.draw_background(BACKGROUND)
            rendy.draw_text(text="TETRIS", font=TETRIS_LOGO_FONT, rect=TETRIS_MENU_LOGO.move(5,5), transform=True, color=BLACK)
            rendy.draw_text(text="TETRIS", font=TETRIS_LOGO_FONT, rect=TETRIS_MENU_LOGO, transform=True)
            rendy.draw_button(button=play_button)
            rendy.draw_button(button=sound_button)
            pygame.display.update()
            clock.tick(FPS)

if __name__ == '__main__':
      main()
