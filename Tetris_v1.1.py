from utils import *
# TO-DO LIST: 
# 1: find a way to state the arguements that a function takes with a pop-up
# 2: make a 'You Lost' screen with fading text
# 3: make a scoreboard 
# 6: maybe make a lil logo for the game

# PS: clean-up the damn scoring system function -> it's all over the place
# PS clean-up the flood fill algorithm
# MAIN GOAL: make the row of blocks fades to turn white when its cleared
# ---> try to use the frame rate of the game to regulate the speed of the animation



class Block():

      def __init__(self, x, y):
            self.x = x
            self.y = y
            self.rotation = 0
            self.shape = I
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
            self.level = 1
            self.score = 0

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
                              self.add_score(drop="hard_drop")

      def update_grid(self):
            self.block_positions = self.block.convert_to_positions()
            for pos in self.block_positions:
                  i, j = pos
                  if pos[1] > -1:
                        self.grid[j][i] = self.block.color

      def refresh_grid(self):
            self.grid = [[self.locked_positions[(i, j)] if (i, j) in self.locked_positions else BLACK for i in range(COLUMN)] for j in range(ROW)]

      def refresh_accepted_positions(self):
            self.accepted_position = [(i, j) for j in range(ROW) for i in range(COLUMN) if (i, j) not in self.locked_positions]

      def check_lost(self):
            self.block_positions = self.block.convert_to_positions()
            for pos in self.block_positions:
                  if pos[1] < 0:
                        return True

      def check_collisions(self):
            self.accepted_position = [(i, j) for j in range(ROW) for i in range(COLUMN) if (i, j) not in self.locked_positions]
            # Needs to call this function twice so that the positions being used is the latest
            self.block_positions = self.block.convert_to_positions()
            if not set(self.block_positions).issubset(self.accepted_position):
                  if min(self.block_positions, key=lambda x: x[1])[1] > -1:
                        return True

      def lock_old_spawn_new(self):
            self.block_positions = self.block.convert_to_positions()
            for (i, j) in self.block_positions:
                  self.locked_positions[(i, j)] = self.block.color
            self.block = Block(COLUMN//2, 0)

      def hard_drop(self):
            while set(self.block_positions).issubset(self.accepted_position):
                  self.block.y +=1
                  self.block_positions = self.block.convert_to_positions()

      def add_score(self, rows_cleared=0, drop=None):

            if rows_cleared:
                  score_gained = SCORE_SYSTEM[rows_cleared]
            if drop:
                  score_gained = SCORE_SYSTEM[drop]

            self.score += (score_gained) * self.level

      def check_clear_rows(self):
            rows_cleared = []
            for j in range(ROW-1, -1, -1):
                  if BLACK not in self.grid[j]:
                        for i in range(COLUMN):
                              rows_cleared.append((i, j))
                              del self.locked_positions[(i, j)]
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
            self.accepted_position = [(i, j) for j in range(ROW) for i in range(COLUMN) if (i, j) not in self.locked_positions]
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
            self.animation_delay = 300
            self.timer = 0

      def draw_field(self, grid, cleared_row=[]):
            if DRAW_GRID_LINES:

                  for i in range(ROW+1):
                        pygame.draw.line(self.win, GREY, (FIELD_X, i * BLOCK_SIZE + FIELD_Y), (FIELD_WIDTH + FIELD_X, i * BLOCK_SIZE + FIELD_Y))
                  for j in range(COLUMN+1):
                        pygame.draw.line(self.win, GREY, (j * BLOCK_SIZE + FIELD_X, FIELD_Y), (j * BLOCK_SIZE + FIELD_X, FIELD_HEIGHT + FIELD_Y))
            # This thing below draws the border fro the playing field
            # have put it at the end here so that the block doesn overlap it when spawning
            pygame.draw.rect(self.win, TOMATO_RED, ((FIELD_X, FIELD_Y), (FIELD_WIDTH, FIELD_HEIGHT)), 4)

      def draw_text(self, text, rect, font, color=WHITE, font_size=150, placement=False, transform=False, hover=False):
            myfont = pygame.font.Font(font, font_size)
            label = myfont.render(text, 1, color)
            # Offset the values a lil bit to create that nice, bordered-up look
            start_pos_x, start_pos_y, width, height = rect.inflate(-15, -15)   
            # MUST be in this order, or else the label used to alter the text will not be the right one and everything fuck up
            if hover:      
                  label = myfont.render(text, False, BLACK, color)
                  label.set_colorkey(BLACK)
            if transform:
                  label = pygame.transform.scale(label, (width, height))
            if placement:
                  if placement == 'middle':
                        rect = label.get_rect(center=(rect.center)) 
            self.win.blit(label, rect)

      def draw_block(self, grid):
            # divide the offset into multiple "sections"
            # the divided offset must reach the original offset value in the time of self.animation_delay
            for j, row in enumerate(grid):
                  for i, color in enumerate(row):
                        if color != BLACK:
                              rect = ((i * BLOCK_SIZE + FIELD_X, j * BLOCK_SIZE + FIELD_Y), (BLOCK_SIZE, BLOCK_SIZE)) 
                              pygame.draw.rect(self.win, color, rect) 
                              pygame.draw.rect(self.win, WHITE, rect, 3)

      def make_block_fade_white(self, cleared_row, dt):
            self.timer += dt
            for (i, j) in cleared_row:
                  rect = ((i * BLOCK_SIZE + FIELD_X, j * BLOCK_SIZE + FIELD_Y), (BLOCK_SIZE, BLOCK_SIZE)) 
                  pygame.draw.rect(self.win, WHITE, rect)
                  if self.timer > self.animation_delay:
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
            if self.decrement <= -img_width:
                  self.win.blit(background_img, (self.win_width - self.decrement, 0))
                  self.decrement = 0

      def draw_pause_screen(self):
            self.draw_screen(alpha_value=125, rect=(0, 0, WIN_WIDTH, WIN_HEIGHT), color=BLACK)
            self.draw_screen(rect=(TETRIS_MENU_LOGO.inflate(100, 20)), color=TOMATO_RED)
            self.draw_text(text="PAUSED", rect=TETRIS_MENU_LOGO, font=RETRO_FONT, transform=True, placement="middle")

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
                  self.draw_text(text=button.text, rect=button.rect, font=button.font, color=button.color, hover=button.hover, placement='middle', transform=True)

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
                  SOUND_CHANNEL.set_volume(1)
            else:
                  SOUND_CHANNEL.set_volume(0)

class particle:

      def __init__(self):
            self.x = x
            self.y = y

def play_game():

      clock = pygame.time.Clock()
      rendy = Render(WIN_WIDTH, WIN_HEIGHT)
      tetris = Tetris()
      if SOUND_CHANNEL.get_volume() != 0.0:
            pygame.mixer.music.play(-1)
      run = True
      cleared_row = []
      time_passed = 0

      while run:
            
            # refresh the grid every run to clear out the place that has been overwritten by the block piece
            # i.e the places where the block piece has travelled across &  aren't in the dicitonary of locked positions
            tetris.refresh_grid()
            dt = clock.get_time()

            for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                        run = False
                        sys.exit()

                  if event.type == pygame.KEYDOWN:
                        tetris.handle_user_input(event)

                  if event.type == GAME_SPEED:
                        if not tetris.paused:
                              tetris.block.y += 1
                              if tetris.check_collisions():
                                    tetris.block.y -= 1
                                    SOUND_CHANNEL.play(BLOCK_COLLIDE_SFX)
                                    if tetris.check_lost():
                                          run = False
                                    # [tetris.lock_old_spawn_new()] MUST be put inside this code block
                                    # --> This Function is responsible for updating the grid
                                    # ----> should only occur once the block has hit the ground
                                    # ----> or else the clear_row function will be triggered while the block is still in mid-air
                                    tetris.lock_old_spawn_new()
                              # [tetris.check_clear_rows()] MUST be put outside of the above 'if' code block
                              # --> This function depends on the grid that's being refreshed constantly
                              # if it's put in the above 'if' code block, it'll only run once a collision occurs
                              # -->since the grid hasn't been refreshed yet, it'll use the 'old' grid, 
                              #    not triggering the function until the next collision occurs
                              cleared_row = tetris.check_clear_rows()

            tetris.update_grid()
            rendy.draw_background(BACKGROUND)
            rendy.draw_screen(alpha_value=125, rect=(FIELD_X, FIELD_Y, FIELD_WIDTH, FIELD_HEIGHT), color=BLACK)
            rendy.draw_field(tetris.grid)
            rendy.draw_block(tetris.grid)
            rendy.draw_text(text="TETRIS", font=TETRIS_LOGO_FONT, rect=TETRIS_GAME_LOGO.move(5, 5), transform=True, color=BLACK)
            rendy.draw_text(text="TETRIS", font=TETRIS_LOGO_FONT, rect=TETRIS_GAME_LOGO, transform=True)

            if cleared_row:
                  SOUND_CHANNEL.play(CLEAR_ROW_SFX)
                  pygame.event.set_blocked([GAME_SPEED, pygame.KEYDOWN])
                  if rendy.make_block_fade_white(cleared_row, dt):
                        tetris.move_rows_down()
                        pygame.event.set_allowed([GAME_SPEED, pygame.KEYDOWN])
                        cleared_row.clear()
            if tetris.paused:
                  rendy.draw_pause_screen()
            clock.tick(FPS)
            pygame.display.update()
            
def main():

      rendy = Render(WIN_WIDTH, WIN_HEIGHT)
      clock = pygame.time.Clock()
      play_button = Button(rect=PLAY_BUTTON, text='PLAY', function=play_game)
      sound_button = Button(rect=SOUND_BUTTON, image=SOUND_BUTTON_ON, clicked_image=SOUND_BUTTON_OFF, function=Button.toggle_sound)
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
