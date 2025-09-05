import pygame
import random
import sys
pygame.init()
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700
GRID_SIZE = 20
CELL_SIZE = 20
GRID_WIDTH = GRID_SIZE * CELL_SIZE
GRID_HEIGHT = GRID_SIZE * CELL_SIZE
GRID_X = (WINDOW_WIDTH - GRID_WIDTH) // 2
GRID_Y = 150
BACKGROUND = (16, 20, 31)  
CARD_BG = (31, 41, 55)     
GRID_BORDER = (55, 65, 81) 
CELL_BORDER = (75, 85, 101) 
SNAKE_HEAD = (34, 197, 94)  
SNAKE_BODY = (22, 163, 74)  
FOOD_COLOR = (234, 179, 8)  
TEXT_GREEN = (34, 197, 94) 
TEXT_RED = (239, 68, 68)    
TEXT_WHITE = (255, 255, 255)
BUTTON_GREEN = (34, 197, 94)
BUTTON_DARK = (55, 65, 81)
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.reset_game()
        
    def reset_game(self):
        self.snake = [(10, 10)]
        self.direction = (0, -1)
        self.food = (15, 15)
        self.score = 0
        self.game_over = False
        self.game_started = False
        
    def generate_food(self):
        while True:
            food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
            if food not in self.snake:
                return food
                
    def move_snake(self):
        if self.game_over or not self.game_started:
            return
            
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        if (new_head[0] < 0 or new_head[0] >= GRID_SIZE or 
            new_head[1] < 0 or new_head[1] >= GRID_SIZE):
            self.game_over = True
            return
            
        if new_head in self.snake:
            self.game_over = True
            return
            
        self.snake.insert(0, new_head)
        
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            self.snake.pop()
            
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if not self.game_started or self.game_over:
                return
                
            if event.key == pygame.K_UP and self.direction[1] == 0:
                self.direction = (0, -1)
            elif event.key == pygame.K_DOWN and self.direction[1] == 0:
                self.direction = (0, 1)
            elif event.key == pygame.K_LEFT and self.direction[0] == 0:
                self.direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and self.direction[0] == 0:
                self.direction = (1, 0)
                
    def draw_rounded_rect(self, surface, color, rect, radius):
        pygame.draw.rect(surface, color, rect, border_radius=radius)
        
    def draw_button(self, text, x, y, width, height, color, text_color):
        button_rect = pygame.Rect(x, y, width, height)
        self.draw_rounded_rect(self.screen, color, button_rect, 8)
        
        text_surface = font_medium.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)
        
        return button_rect
        
    def draw(self):
        self.screen.fill(BACKGROUND)
        
        
        title = font_large.render("Snake Game", True, TEXT_GREEN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 50))
        self.screen.blit(title, title_rect)
        
        
        score_text = font_medium.render(f"Score: {self.score}", True, TEXT_GREEN)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, 90))
        self.screen.blit(score_text, score_rect)
        
        
        board_rect = pygame.Rect(GRID_X-10, GRID_Y-10, GRID_WIDTH+20, GRID_HEIGHT+20)
        self.draw_rounded_rect(self.screen, CARD_BG, board_rect, 12)
        
        
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                cell_x = GRID_X + x * CELL_SIZE
                cell_y = GRID_Y + y * CELL_SIZE
                cell_rect = pygame.Rect(cell_x, cell_y, CELL_SIZE, CELL_SIZE)
                
            
                pygame.draw.rect(self.screen, BACKGROUND, cell_rect)
                pygame.draw.rect(self.screen, CELL_BORDER, cell_rect, 1)
                
                
                if (x, y) == self.snake[0]:
                    self.draw_rounded_rect(self.screen, SNAKE_HEAD, cell_rect.inflate(-2, -2), 3)
                
                elif (x, y) in self.snake[1:]:
                    self.draw_rounded_rect(self.screen, SNAKE_BODY, cell_rect.inflate(-2, -2), 3)
                
                elif (x, y) == self.food:
                    food_rect = cell_rect.inflate(-4, -4)
                    pygame.draw.ellipse(self.screen, FOOD_COLOR, food_rect)
                    
        
        if not self.game_started and not self.game_over:
            self.draw_button("Start Game", WINDOW_WIDTH//2 - 80, 500, 160, 50, BUTTON_GREEN, TEXT_WHITE)
            
        elif self.game_over:
            
            game_over_text = font_large.render("Game Over!", True, TEXT_RED)
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, 450))
            self.screen.blit(game_over_text, game_over_rect)
            
            
            final_score = font_medium.render(f"Final Score: {self.score}", True, TEXT_GREEN)
            final_score_rect = final_score.get_rect(center=(WINDOW_WIDTH//2, 490))
            self.screen.blit(final_score, final_score_rect)
            
           
            self.play_again_btn = self.draw_button("Play Again", WINDOW_WIDTH//2 - 170, 530, 140, 50, BUTTON_GREEN, TEXT_WHITE)
            self.reset_btn = self.draw_button("Reset", WINDOW_WIDTH//2 + 30, 530, 140, 50, BUTTON_DARK, TEXT_WHITE)
            
        elif self.game_started and not self.game_over:
            
            instruction = font_small.render("Use arrow keys to control the snake", True, TEXT_WHITE)
            instruction_rect = instruction.get_rect(center=(WINDOW_WIDTH//2, 470))
            self.screen.blit(instruction, instruction_rect)
            
            self.reset_game_btn = self.draw_button("Reset Game", WINDOW_WIDTH//2 - 70, 500, 140, 40, BUTTON_DARK, TEXT_WHITE)
            
    def handle_mouse_click(self, pos):
        if not self.game_started and not self.game_over:
           
            if 200 <= pos[0] <= 400 and 500 <= pos[1] <= 550:
                self.game_started = True
                
        elif self.game_over:
            
            if hasattr(self, 'play_again_btn') and self.play_again_btn.collidepoint(pos):
                self.reset_game()
                self.game_started = True
            
            elif hasattr(self, 'reset_btn') and self.reset_btn.collidepoint(pos):
                self.reset_game()
                
        elif self.game_started and not self.game_over:
            
            if hasattr(self, 'reset_game_btn') and self.reset_game_btn.collidepoint(pos):
                self.reset_game()
                
    def run(self):
        running = True
        move_timer = 0
        move_delay = 150  
        
        while running:
            dt = self.clock.tick(60)
            move_timer += dt
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_input(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)
                  
             
            if move_timer >= move_delay:
                self.move_snake()
                move_timer = 0
                
            self.draw()
            pygame.display.flip()
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
