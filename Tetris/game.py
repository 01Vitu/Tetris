import pygame
import random

# definindo constantes
BLOCK_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (BOARD_WIDTH + 6)
SCREEN_HEIGHT = BLOCK_SIZE * BOARD_HEIGHT

# definindo cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# peças possíveis
SHAPES = [
    [[1, 1],
     [1, 1]],
    [[0, 2, 0],
     [2, 2, 2]],
    [[0, 3, 3],
     [3, 3, 0]],
    [[4, 4, 0],
     [0, 4, 4]],
    [[0, 5, 0],
     [5, 5, 5]],
    [[6, 6, 6, 6]]
]

# cores das peças
COLORS = [
    WHITE,
    BLUE,
    GREEN,
    YELLOW,
    RED,
    (128, 0, 128)  # roxo
]

# classe para as peças
class Piece:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = BOARD_WIDTH // 2 - len(shape[0]) // 2
        self.y = 0

    # gira a peça
    def rotate(self):
        self.shape = [[self.shape[j][i] for j in range(len(self.shape))] for i in range(len(self.shape[0]) - 1, -1, -1)]

    # move a peça para baixo
    def move_down(self):
        self.y += 1

    # move a peça para a esquerda
    def move_left(self):
        self.x -= 1

    # move a peça para a direita
    def move_right(self):
        self.x += 1
    # move a peça pra cima
    def move_up(self):
        self.y -= 1

# classe para o jogo
class Tetris:
    def __init__(self):
        # inicializa o pygame
        pygame.init()

        # configura a janela
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")

        # inicializa o relógio
        self.clock = pygame.time.Clock()

        # inicializa o tabuleiro
        self.board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]

        # inicializa as peças
        self.piece = None
        self.next_piece = None
        self.new_piece()

        # inicializa a pontuação
        self.score = 0

    # cria uma nova peça
    def new_piece(self):
        self.piece = self.next_piece or Piece(random.choice(SHAPES), random.choice(COLORS))
        self.next_piece = Piece(random.choice(SHAPES), random.choice(COLORS))

     # verifica se uma posição é válida
    def is_valid_position(self, x, y, shape):
        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j] != 0:
                    if not (0 <= x + j < BOARD_WIDTH and 0 <= y + i < BOARD_HEIGHT and self.board[y + i][x + j] == 0):
                        return False
        return True

    # insere uma peça no tabuleiro
    def place_piece(self):
        for i in range(len(self.piece.shape)):
            for j in range(len(self.piece.shape[0])):
                if self.piece.shape[i][j] != 0:
                    self.board[self.piece.y + i][self.piece.x + j] = self.piece.color

    # remove as linhas completas
    def remove_lines(self):
        num_lines_removed = 0
        for i in range(BOARD_HEIGHT):
            if all(self.board[i]):
                num_lines_removed += 1
                del self.board[i]
                self.board.insert(0, [0] * BOARD_WIDTH)
        self.score += num_lines_removed ** 2

    # atualiza o jogo
    def update(self):
        # move a peça para baixo
        self.piece.move_down()
        if not self.is_valid_position(self.piece.x, self.piece.y, self.piece.shape):
            # se a posição não é válida, a peça não pode se mover mais
            self.piece.move_up()
            self.place_piece()
            self.remove_lines()
            self.new_piece()
            if not self.is_valid_position(self.piece.x, self.piece.y, self.piece.shape):
                # se a nova peça já ocupa uma posição inválida, o jogo acaba
                pygame.quit()
                quit()

    # desenha o tabuleiro
    def draw_board(self):
        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                pygame.draw.rect(self.screen, self.board[i][j], (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    # desenha uma peça
    def draw_piece(self, piece):
        for i in range(len(piece.shape)):
            for j in range(len(piece.shape[0])):
                if piece.shape[i][j] != 0:
                    pygame.draw.rect(self.screen, piece.color, ((piece.x + j) * BLOCK_SIZE, (piece.y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    # desenha a próxima peça
    def draw_next_piece(self, piece):
        font = pygame.font.SysFont(None, 30)
        text = font.render("Próxima peça:", True, WHITE)
        self.screen.blit(text, (SCREEN_WIDTH - BLOCK_SIZE * 6, BLOCK_SIZE))
        for i in range(len(piece.shape)):
            for j in range(len(piece.shape[0])):
                if piece.shape[i][j] != 0:
                    pygame.draw.rect(self.screen, piece.color, ((SCREEN_WIDTH - BLOCK_SIZE * 5) + j * BLOCK_SIZE, BLOCK_SIZE * (2 + i), BLOCK_SIZE, BLOCK_SIZE), 0)

    # desenha a pontuação
    def draw_score(self):
        font = pygame.font.SysFont(None, 30)
        text = font.render("Pontuação: {}".format(self.score), True, WHITE)
        self.screen.blit(text, (SCREEN_WIDTH - BLOCK_SIZE * 6, SCREEN_HEIGHT - BLOCK_SIZE))

    # executa o jogo
    def run(self):
        while True:
            # verifica os eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.piece.move_left()
                        if not self.is_valid_position(self.piece.x, self.piece.y, self.piece.shape):
                            self.piece.move_right()
                    elif event.key == pygame.K_RIGHT:
                        self.piece.move_right()
                        if not self.is_valid_position(self.piece.x, self.piece.y, self.piece.shape):
                            self.piece.move_left()
                    elif event.key == pygame.K_UP:
                        self.piece.rotate()
                        if not self.is_valid_position(self.piece.x, self.piece.y, self.piece.shape):
                            self.piece.rotate_back()
                    elif event.key == pygame.K_DOWN:
                        self.piece.move_down()
                        if not self.is_valid_position(self.piece.x, self.piece.y, self.piece.shape):
                            self.piece.move_up()
            # atualiza o jogo
            self.update()
            # desenha a tela
            self.screen.fill(BLACK)
            self.draw_board()
            self.draw_piece(self.piece)
            self.draw_next_piece(self.next_piece)
            self.draw_score()
            pygame.display.update()
            # espera um pouco antes de atualizar novamente
            pygame.time.delay(100)

if __name__ == "__main__":
    game = Tetris()
    game.run()