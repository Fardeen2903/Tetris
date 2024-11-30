import pygame
import random
from config import *
from piece import Piece
from board import Board
from utils import check_collision, clear_full_lines
from menu import show_start_screen, show_game_over_screen

class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.current_piece = Piece()
        self.game_over = False
        self.score = 0
        self.level = 1
        self.high_score = self.load_high_score()  # Load the high score
        self.fall_speed = 1000  # Initial speed (in milliseconds)
        self.last_fall_time = pygame.time.get_ticks()  # Time of the last fall

    def toggle_fullscreen(self):
        current_mode = pygame.display.get_surface().get_size()
        if current_mode == (SCREEN_WIDTH, SCREEN_HEIGHT):
            pygame.display.set_mode((SCREEN_WIDTH_FULLSCREEN, SCREEN_HEIGHT_FULLSCREEN), pygame.FULLSCREEN)
        else:
            pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def load_high_score(self):
        try:
            with open("highscore.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0  # If the file doesn't exist, start with 0

    def save_high_score(self):
        if self.score > self.high_score:
            with open("highscore.txt", "w") as file:
                file.write(str(self.score))
            self.high_score = self.score  # Update in memory

    def draw(self):
        # Draw the board
        self.board.draw(self.screen)
        # Draw the falling piece
        for x, y in self.current_piece.get_positions():
            pygame.draw.rect(self.screen, self.current_piece.color,
                             (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Draw the scorecard and high score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        high_score_text = font.render(f"High Score: {self.high_score}", True, (255, 255, 255))
        self.screen.blit(score_text, (SCREEN_WIDTH + 10, 50))
        self.screen.blit(high_score_text, (SCREEN_WIDTH + 10, 100))

    def game_loop(self):
        while not self.game_over:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_fall_time > self.fall_speed:  # Automatically fall
                self.current_piece.y += 1
                if check_collision(self.current_piece, self.board):
                    self.current_piece.y -= 1
                    self.board.add_piece(self.current_piece)
                    lines_cleared = clear_full_lines(self.board)
                    self.score += lines_cleared * 100
                    if lines_cleared > 0:
                        self.level += 1
                        self.fall_speed = max(100, self.fall_speed - 50)  # Speed up the fall
                    self.current_piece = Piece()
                    if check_collision(self.current_piece, self.board):
                        self.game_over = True
                self.last_fall_time = current_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.current_piece.x -= 1
                        if check_collision(self.current_piece, self.board):
                            self.current_piece.x += 1
                    elif event.key == pygame.K_RIGHT:
                        self.current_piece.x += 1
                        if check_collision(self.current_piece, self.board):
                            self.current_piece.x -= 1
                    elif event.key == pygame.K_DOWN:
                        self.current_piece.y += 1
                        if check_collision(self.current_piece, self.board):
                            self.current_piece.y -= 1
                            self.board.add_piece(self.current_piece)
                            lines_cleared = clear_full_lines(self.board)
                            self.score += lines_cleared * 100
                            self.current_piece = Piece()
                            if check_collision(self.current_piece, self.board):
                                self.game_over = True
                    elif event.key == pygame.K_SPACE:  # Rotate piece on Space key press
                        self.current_piece.rotate()
                        if check_collision(self.current_piece, self.board):
                            self.current_piece.rotate()  # Undo rotation if collision
                            self.current_piece.rotate()
                            self.current_piece.rotate()  # Undo rotation if collision
                    elif event.key == pygame.K_f:  # Toggle fullscreen with F key
                        self.toggle_fullscreen()

            self.screen.fill((0, 0, 0))  # Clear screen with black background
            self.draw()  # Draw the board and current piece
            pygame.display.flip()
            self.clock.tick(FPS)

        self.save_high_score()  # Save high score when game is over
        show_game_over_screen(self.screen, self.score)

if __name__ == "__main__":
    game = Tetris()
    game.game_loop()  # Corrected to call the proper game loop
    pygame.quit()
