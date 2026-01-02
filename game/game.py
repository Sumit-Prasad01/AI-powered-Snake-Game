import pygame
import random
from enum import Enum
from collections import namedtuple

from config.paths_config import *
from exception.custom_exception import CustomException
from logger.logger import get_logger

logger = get_logger(__name__)

pygame.init()
font = pygame.font.Font(FONT_PATH, 25)


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0 ,0, 0)

BLOCK_SIZE = 20
SPEED = 20


class SnakeGame:
    def __init__(self, w = 640, h = 480):
        
        self.w = w
        self.h = h

        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()

        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [  
                        self.head,
                        Point(self.head.x-BLOCK_SIZE, self.head.y),
                        Point(self.head.x-(2*BLOCK_SIZE), self.head.y)
                     ]
        
        self.score = 0
        self.food = None
        self._place_food()

    
    def _place_food(self):
        try:
            x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
            self.food = Point(x, y)

            if self.food in self.snake:
                self._place_food()
            
        
        except Exception as e:
            logger.error("Error while placing food")
            raise CustomException("Failed to place food", e)
        
    
    def play_step(self):
        try:
            # 1. Collect User Input
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.direction = Direction.LEFT

                    elif event.key == pygame.K_RIGHT:
                        self.direction = Direction.RIGHT

                    elif event.key == pygame.K_UP:
                        self.direction = Direction.UP
                    
                    elif event.key == pygame.K_DOWN:
                        self.direction = Direction.DOWN
            
            # 2. Move 

            self._move(self.direction) # update the head 
            self.snake.insert(0, self.head)

            # 3. Check if game over 
            
            game_over = False
            if self._is_collision():
                game_over = True
                return game_over, self.score
            
            # 4. Place new food or just move 

            if self.head == self.food:
                self.score += 1
                self._place_food()
            else:
                self.snake.pop()
            

            # 5. Update ui and clock

            self._update_ui()
            self.clock.tick(SPEED)

            # 6. Return game over and score 
            logger.info("GAME OVER.")
            logger.info(f"Your Final Score is : {self.score}")

            return game_over, self.score

        except Exception as e:
            logger.error("Error while implementing play steps.")
            raise CustomException("Failed to implement play steps.", e)

    def _is_collision(self):
        try:
            # hist boundary
            if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:

                return True
            
            # hits itself
            if self.head in self.snake[1:]:
                return True
            
            return False

        except Exception as e:
            logger.error("Error while detecting collisions.")
            raise CustomException("Failed to detect collisions.", e)
    
    def _update_ui(self):
        try:
            self.display.fill(BLACK)

            for pt in self.snake:
                pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

            pygame.draw.rect(self.display, RED,  pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

            text = font.render("Score: " + str(self.score), True, WHITE)
            self.display.blit(text, [0, 0])
            pygame.display.flip()

        except Exception as e:
            logger.error("Error while updating UI.")
            raise CustomException("Failed to update UI.", e)
        
    
    def _move(self, direction):
        try:
            x = self.head.x
            y = self.head.y

            if direction == Direction.RIGHT:
                x += BLOCK_SIZE

            elif direction == Direction.LEFT:
                x -= BLOCK_SIZE
            
            elif direction == Direction.DOWN:
                y += BLOCK_SIZE

            elif direction == Direction.UP:
                y -= BLOCK_SIZE

            self.head = Point(x ,y)

        except Exception as e:
            logger.error("Error while moving snake.")
            raise CustomException("Failed to move snake.", e)
        

if __name__ == "__main__":

    game = SnakeGame()

    #game loop
    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break
            
    logger.info(f"Final Score : {score}")


    pygame.quit()