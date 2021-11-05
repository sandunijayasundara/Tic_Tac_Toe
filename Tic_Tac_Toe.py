import sys
import numpy as np
import pygame

BACKGROUND_COLOR = (80, 133, 199)
LINE_COLOR = (80, 160, 199)
LINE_WIDTH = 10
B_WIDTH = 600
B_HEIGHT = 600
B_ROWS = 3
B_COlS = 3
CIRCLE_RAD = 60
CIRCLE_WIDTH = 15
CIRCLE_COLOR = (239, 231, 200)
CROSS_WIDTH = 25
CROSS_COLOR = (66, 66, 66)
SPACE = 55
SQUARE_SIZE = 200
SCREEN_WIDTH = B_COlS * SQUARE_SIZE
SCREEN_HEIGHT = B_ROWS * SQUARE_SIZE



class Game:
    def __init__(self):
        # initializing pygame
        pygame.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode(size=(B_WIDTH, 100 + B_HEIGHT))
        # Change the color of the background
        pygame.display.set_caption('TIC TAC TOE')
        self.surface.fill(BACKGROUND_COLOR)
        self.draw_lines()
        self.board = np.zeros((B_ROWS, B_COlS))
        pygame.display.flip()

     # Plays continouse music
    def play_background_music(self):
        pygame.mixer.music.load("Resources/Tic Tac Toe Glow OST.mp3")
        pygame.mixer.music.play()

    # Play only once
    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"Resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        self.surface = pygame.display.set_mode(size=(B_WIDTH, B_HEIGHT))
        # Change the color of the background
        pygame.display.set_caption('TIC TAC TOE')
        self.surface.fill(BACKGROUND_COLOR)
        pygame.display.flip()

    ####### Check Board statuses #######
    def mark_square(self, row_n, col_n, player):
        self.board[row_n][col_n] = player

    def is_sqaure_available(self, row_n, col_n):
        return self.board[row_n][col_n] == 0

    def is_board_full(self):
        for row in range(B_ROWS):
            for col in range(B_COlS):
                if self.board[row][col] == 0:
                    return False
            return True

    ######### Playing Game ##########
    def play_game(self):
        win = False
        running = True
        player = 1
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and not win:
                    # rounding values to square slots
                    mouseX_colval = int(event.pos[0] // 200)
                    mouseY_rowval = int(event.pos[1] // 200)

                    if self.is_sqaure_available(mouseY_rowval, mouseX_colval):
                        self.mark_square(mouseY_rowval, mouseX_colval, player)

                        if np.count_nonzero(self.board) == 9:
                            self.show_board_full()

                        if self.check_win(player):
                            self.show_game_over(player)
                            win = True
                        player = player % 2 + 1
                        self.draw_figures(self.board)
                        pygame.display.flip()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.unpause()
                        self.reset()
                        win = False

                    if event.key == pygame.K_ESCAPE:
                        exit(0)

        # pygame.display.update()

    ########### Drawing Lines, Crosses and Circles ##########
    def draw_lines(self):
        for i in range(1, 4):
            # Horizontal Lines
            pygame.draw.line(self.surface, LINE_COLOR, (0, SQUARE_SIZE * i), (B_WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
            # Vertical Lines
            pygame.draw.line(self.surface, LINE_COLOR, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, B_HEIGHT), LINE_WIDTH)

    def draw_figures(self, board):
        for row in range(B_ROWS):
            for col in range(B_COlS):
                if board[row][col] == 1:
                    pygame.draw.circle(self.surface, CIRCLE_COLOR, (
                    int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int(row * SQUARE_SIZE + SQUARE_SIZE / 2)), CIRCLE_RAD,
                                       CIRCLE_WIDTH)
                elif board[row][col] == 2:
                    pygame.draw.line(self.surface, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
                    pygame.draw.line(self.surface, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)

    ######### Check Winning and Draw Lines #########
    def check_win(self, player):
        ver_win = self.check_vertical_win(player)
        hor_win = self.check_horizontal_win(player)
        diag_win = self.check_diagonal_win(player)
        pygame.display.flip()

        if ver_win or hor_win or diag_win:
            return True
        else:
            return False

    def check_vertical_win(self, player):
        for col in range(B_COlS):
            if self.board[0][col] == player and self.board[1][col] == player and self.board[2][col] == player:
                self.draw_vertical_winning_line(col, player)
                return True

        return False

    def check_horizontal_win(self, player):
        for row in range(B_ROWS):
            if self.board[row][0] == player and self.board[row][1] == player and self.board[row][2] == player:
                self.draw_horizontal_winning_line(row, player)
                return True

        return False

    def check_diagonal_win(self, player):
        if self.board[0][0] == player and self.board[1][1] == player and self.board[2][2] == player:
            self.draw_diagonal_winning_line(player)
            return True
        elif self.board[2][0] == player and self.board[1][1] == player and self.board[0][2] == player:
            self.draw_diagonal_winning_line(player, False)
            return True
        else:
            return False

    def draw_vertical_winning_line(self, col, player):
        posX = col * SQUARE_SIZE + SQUARE_SIZE / 2

        if player == 1:
            pygame.draw.line(self.surface, CIRCLE_COLOR, (posX, 10), (posX, SCREEN_HEIGHT - 10), CIRCLE_WIDTH)
        else:
            pygame.draw.line(self.surface, CROSS_COLOR, (posX, 10), (posX, SCREEN_HEIGHT - 10), CIRCLE_WIDTH)

    def draw_horizontal_winning_line(self, row, player):
        posY = row * SQUARE_SIZE + SQUARE_SIZE / 2

        if player == 1:
            pygame.draw.line(self.surface, CIRCLE_COLOR, (10, posY), (SCREEN_WIDTH - 10, posY), CIRCLE_WIDTH)
        else:
            pygame.draw.line(self.surface, CROSS_COLOR, (10, posY), (SCREEN_WIDTH - 10, posY), CIRCLE_WIDTH)

    def draw_diagonal_winning_line(self, player, down_diag = True):
        if down_diag:
            if player == 1:
                pygame.draw.line(self.surface, CIRCLE_COLOR, (25, 25), (SCREEN_WIDTH - 25, SCREEN_HEIGHT - 25), CROSS_WIDTH)
            else:
                pygame.draw.line(self.surface, CROSS_COLOR, (25, 25), (SCREEN_WIDTH - 25, SCREEN_HEIGHT - 25), CROSS_WIDTH)
        else:
            if player == 1:
                pygame.draw.line(self.surface, CIRCLE_COLOR, (25, SCREEN_HEIGHT - 25), (SCREEN_WIDTH - 25, 25), CROSS_WIDTH)
            else:
                pygame.draw.line(self.surface, CROSS_COLOR, (25, SCREEN_HEIGHT - 25), (SCREEN_WIDTH - 25, 25), CROSS_WIDTH)

    def reset(self):
        self.surface.fill(BACKGROUND_COLOR)
        self.draw_lines()
        self.board = np.zeros((B_ROWS, B_COlS))
        pygame.display.flip()
        self.play_game()

    def show_game_over(self, player):
        font = pygame.font.SysFont('arial', 20)
        if player==1:
            ln1 = font.render("Game is Over!, Player O won the Game ", True, (250, 250, 250))
        elif player==2:
            ln1 = font.render("Game is Over!, Player X won the Game ", True, (250, 250, 250))
        self.surface.blit(ln1, (10, 610))
        ln2 = font.render("To Play again press Enter. To exit press Esc!!!", True, (250, 250, 250))
        self.surface.blit(ln2, (10, 650))
        pygame.display.flip()
        pygame.mixer.music.pause()
        self.play_sound("game-over-sound-effect")

    def show_board_full(self):
        font = pygame.font.SysFont('arial', 20)
        ln1 = font.render("You're out of moves...", True, (250, 250, 250))
        self.surface.blit(ln1, (10, 630))
        ln2 = font.render("To Play again press Enter. To exit press Esc!!!", True, (250, 250, 250))
        self.surface.blit(ln2, (10, 650))
        pygame.display.flip()
        pygame.mixer.music.pause()
        self.play_sound("game-over-sound-effect")

if __name__ == '__main__':
    game = Game()
    game.play_game()
