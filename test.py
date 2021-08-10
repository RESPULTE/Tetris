      def make_block_fade_white(self, cleared_row, dt):
            self.timer += dt
            for (i, j) in cleared_row:
                  rect = ((i * BLOCK_SIZE + FIELD_X, j * BLOCK_SIZE + FIELD_Y), (BLOCK_SIZE, BLOCK_SIZE)) 
                  pygame.draw.rect(self.win, WHITE, rect)
                  if self.timer > self.animation_delay:
                        self.timer = 0
                        return True