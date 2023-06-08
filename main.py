import pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH = 600
HEIGHT = 600
GWHITE = (210, 255, 255)
GBLACK = (0, 45, 45)
YELLOW = (255, 255, 210)
ORANGE = (255,105,25)
BLUE = (0, 0, 255)
RED = (255, 55, 55)
BLOCK_S = 75
CLOCK = pygame.time.Clock()
FPS = 60

IMG_BS = pygame.transform.scale(pygame.image.load("res/bs.png"), (44, 44))
IMG_WS = pygame.transform.scale(pygame.image.load("res/ws.png"), (44, 44))
IMG_BR = pygame.transform.scale(pygame.image.load("res/br.png"), (44, 54))
IMG_WR = pygame.transform.scale(pygame.image.load("res/wr.png"), (44, 54))
IMG_BB = pygame.transform.scale(pygame.image.load("res/bb.png"), (54, 54))
IMG_WB = pygame.transform.scale(pygame.image.load("res/wb.png"), (54, 54))
IMG_BQ = pygame.transform.scale(pygame.image.load("res/bq.png"), (54, 54))
IMG_WQ = pygame.transform.scale(pygame.image.load("res/wq.png"), (54, 54))
IMG_BK = pygame.transform.scale(pygame.image.load("res/bk.png"), (54, 54))
IMG_WK = pygame.transform.scale(pygame.image.load("res/wk.png"), (54, 54))
IMG_BH = pygame.transform.scale(pygame.image.load("res/bh.png"), (54, 54))
IMG_WH = pygame.transform.scale(pygame.image.load("res/wh.png"), (54, 54))
SOUND_PIECE = pygame.mixer.Sound("res/piece.wav")
SOUND_CHECK = pygame.mixer.Sound("res/check.wav")
SOUND_CHECKMATE = pygame.mixer.Sound("res/checkmate.wav")
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
FONT = pygame.font.SysFont("monospace", 84)


class Piece:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def draw(self):
        WIN.blit(self.img, (self.col*BLOCK_S+BLOCK_S//2-self.img.get_width() //
                 2, self.row*BLOCK_S+BLOCK_S//2-self.img.get_height()//2))

    @staticmethod
    def get_striaght_moves(piece):
        ind = []
        for i in range(piece.col+1, 8):
            if (piece.row, i) in game.locked_pos:
                if game.locked_pos[(piece.row, i)].kind == piece.kind:
                    break
                ind.append((piece.row, i))
                break
            ind.append((piece.row, i))
        for i in range(piece.col-1, -1, -1):
            if (piece.row, i) in game.locked_pos:
                if game.locked_pos[(piece.row, i)].kind == piece.kind:
                    break
                ind.append((piece.row, i))
                break
            ind.append((piece.row, i))
        for i in range(piece.row+1, 8):
            if (i, piece.col) in game.locked_pos:
                if game.locked_pos[(i, piece.col)].kind == piece.kind:
                    break
                ind.append((i, piece.col))
                break
            ind.append((i, piece.col))
        for i in range(piece.row-1, -1, -1):
            if (i, piece.col) in game.locked_pos:
                if game.locked_pos[(i, piece.col)].kind == piece.kind:
                    break
                ind.append((i, piece.col))
                break
            ind.append((i, piece.col))
        return ind

    @staticmethod
    def get_diagonal_moves(piece):
        ind = []
        c = 1
        while 1:
            if piece.row-c < 0 or piece.col-c < 0:
                break
            if (piece.row-c, piece.col-c) in game.locked_pos:
                if game.locked_pos[(piece.row-c, piece.col-c)].kind == piece.kind:
                    break
                ind.append((piece.row-c, piece.col-c))
                break
            ind.append((piece.row-c, piece.col-c))
            c += 1
        c = 1
        while 1:
            if piece.row-c < 0 or piece.col+c > 7:
                break
            if (piece.row-c, piece.col+c) in game.locked_pos:
                if game.locked_pos[(piece.row-c, piece.col+c)].kind == piece.kind:
                    break
                ind.append((piece.row-c, piece.col+c))
                break
            ind.append((piece.row-c, piece.col+c))
            c += 1
        c = 1
        while 1:
            if piece.row+c > 7 or piece.col-c < 0:
                break
            if (piece.row+c, piece.col-c) in game.locked_pos:
                if game.locked_pos[(piece.row+c, piece.col-c)].kind == piece.kind:
                    break
                ind.append((piece.row+c, piece.col-c))
                break
            ind.append((piece.row+c, piece.col-c))
            c += 1
        c = 1
        while 1:
            if piece.row+c > 7 or piece.col+c > 7:
                break
            if (piece.row+c, piece.col+c) in game.locked_pos:
                if game.locked_pos[(piece.row+c, piece.col+c)].kind == piece.kind:
                    break
                ind.append((piece.row+c, piece.col+c))
                break
            ind.append((piece.row+c, piece.col+c))
            c += 1
        return ind


class Rook(Piece):

    def __init__(self, row, col, kind):
        super().__init__(row, col)
        self.kind = kind
        if kind == 1:
            self.img = IMG_WR
        else:
            self.img = IMG_BR

    def get_moves(self):
        return Piece.get_striaght_moves(self)


class Soldier(Piece):

    def __init__(self, row, col, kind):
        super().__init__(row, col)
        self.kind = kind
        if kind == 1:
            self.img = IMG_WS
        else:
            self.img = IMG_BS

    def update_cross_moves(self):
        if game.current_turn == self.kind:
            self.cross_moves = [(self.row-1, self.col+1), (self.row-1, self.col-1)]
        else:
            self.cross_moves = [(self.row+1, self.col-1), (self.row+1, self.col+1)]

    def get_moves(self):
        self.update_cross_moves()
        ind = []
        if (self.row-1, self.col) not in game.locked_pos and self.row > 0:
            ind.append((self.row-1, self.col))
            if self.row >= 6:
                if (self.row-2, self.col) not in game.locked_pos:
                    ind.append((self.row-2, self.col))
        for pos in self.cross_moves:
            if pos in game.locked_pos:
                if game.locked_pos[pos].kind != self.kind:
                    ind.append(pos)
        return ind


class Bishop(Piece):

    def __init__(self, row, col, kind):
        super().__init__(row, col)
        self.kind = kind
        if kind == 1:
            self.img = IMG_WB
        else:
            self.img = IMG_BB

    def get_moves(self):
        return Piece.get_diagonal_moves(self)


class Queen(Piece):

    def __init__(self, row, col, kind):
        super().__init__(row, col)
        self.kind = kind
        if kind == 1:
            self.img = IMG_WQ
        else:
            self.img = IMG_BQ

    def get_moves(self):
        return Piece.get_striaght_moves(self) + Piece.get_diagonal_moves(self)


class King(Piece):

    def __init__(self, row, col, kind):
        super().__init__(row, col)
        self.kind = kind
        if kind == 1:
            self.img = IMG_WK
        else:
            self.img = IMG_BK

    def clean_get_moves(self, ind):
        """Removes the moves which leads to check"""
        if self.kind == 1:
            enemy = game.black
        else:
            enemy = game.white
        for p in enemy:
            for move in p.get_moves():
                if move in ind:
                    ind.remove(move)

    def update_moves(self):
        self.moves = [(self.row+1, self.col+1), (self.row+1, self.col),
                      (self.row+1, self.col-1), (self.row-1, self.col+1),
                      (self.row-1, self.col-1), (self.row-1, self.col),
                      (self.row, self.col+1), (self.row, self.col-1)]

    def get_moves(self):
        self.update_moves()
        ind = []
        for move in self.moves:
            if move in game.locked_pos:
                if game.locked_pos[move].kind != self.kind:
                    ind.append(move)
            else:
                if move[0] >= 0 and move[0] <= 7 and move[1] >= 0 and move[1] <= 7:
                    ind.append(move)
        if self.kind == game.current_turn:
            self.clean_get_moves(ind)

        return ind


class Horse(Piece):

    def __init__(self, row, col, kind):
        super().__init__(row, col)
        self.kind = kind
        if kind == 1:
            self.img = IMG_WH
        else:
            self.img = IMG_BH

    def update_moves(self):
        self.moves = [(self.row-2, self.col+1), (self.row-2, self.col-1),
                      (self.row-1, self.col+2), (self.row-1, self.col-2),
                      (self.row+2, self.col+1), (self.row+2, self.col-1),
                      (self.row+1, self.col+2), (self.row+1, self.col-2)]

    def get_moves(self):
        self.update_moves()
        ind = []
        for move in self.moves:
            if move in game.locked_pos:
                if game.locked_pos[move].kind != self.kind:
                    ind.append(move)
            else:
                if move[0] >= 0 and move[0] <= 7 and move[1] >= 0 and move[1] <= 7:
                    ind.append(move)
        return ind


class Game:

    def __init__(self):
        self.reset_attributes()

    def start(self):
        while self.run:
            self.mouse_pos = pygame.mouse.get_pos()
            self.mouse_pressed = pygame.mouse.get_pressed()
            self.grid_pos = self.get_grid_pos()
            self.draw()
            CLOCK.tick(FPS)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.MOUSEBUTTONUP and self.mouse_pressed[0]:
                    if self.selected_piece:
                        self.move_piece()
                    else:
                        self.select_piece()

    def reset_attributes(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_pressed = pygame.mouse.get_pressed()
        self.run = True
        self.locked_pos = {}
        self.white = [King(7, 3, 1), Rook(7, 0, 1), Rook(7, 7, 1), Soldier(6, 0, 1),
                      Soldier(6, 2, 1), Soldier(6, 3, 1), Soldier(6, 4, 1),
                      Soldier(6, 5, 1), Soldier(6, 6, 1), Soldier(6, 7, 1),
                      Bishop(7, 2, 1), Bishop(7, 5, 1), Queen(
                          7, 4, 1), Soldier(6, 1, 1),
                      Horse(7, 1, 1), Horse(7, 6, 1)]

        self.black = [King(0, 3, 0), Rook(0, 0, 0), Rook(0, 7, 0), Soldier(1, 0, 0),
                      Soldier(1, 2, 0), Soldier(1, 3, 0), Soldier(
                          1, 4, 0), Soldier(1, 5, 0),
                      Soldier(1, 6, 0), Soldier(1, 7, 0), Bishop(
            0, 2, 0), Bishop(0, 5, 0),
            Queen(0, 4, 0), Soldier(1, 1, 0), Horse(0, 1, 0), Horse(0, 6, 0)]

        self.current_turn = 1
        self.selected_piece = None
        self.movable_places = None
        self.grid_pos = None
        self.ischeck = False

        for piece in self.white:
            self.locked_pos[(piece.row, piece.col)] = piece
        for piece in self.black:
            self.locked_pos[(piece.row, piece.col)] = piece

    def move_piece(self):
        if self.grid_pos in self.movable_places:
            self.move_animation(self.selected_piece,self.grid_pos)
            SOUND_PIECE.play()
            if self.grid_pos in self.locked_pos:

                if self.locked_pos[self.grid_pos].kind == 1:
                    self.white.remove(self.locked_pos[self.grid_pos])
                else:
                    self.black.remove(self.locked_pos[self.grid_pos])
                del self.locked_pos[self.grid_pos]
            del self.locked_pos[(self.selected_piece.row,
                                 self.selected_piece.col)]
            self.selected_piece.row = self.grid_pos[0]
            self.selected_piece.col = self.grid_pos[1]
            self.locked_pos[self.grid_pos] = self.selected_piece
            self.selected_piece = None
            self.movable_places = None          
            self.draw()
            pygame.display.update()
            pygame.time.delay(300)
            self.swap_current_turn()
            self.swap_side()
            if self.check():
                self.ischeck = True
                if self.checkmate() == False:
                    SOUND_CHECK.play()
            else:
                self.ischeck = False
                if not self.ensure_moves():
                    self.ischeck = True
                    self.game_over()

        elif self.grid_pos in self.locked_pos:
            self.select_piece()

        else:
            self.selected_piece = None
      
    
    def move_animation(self,piece,pos):
        if piece.row == pos[0]:
            if piece.col > pos[1]:
                pass
            else:
                pass
        elif piece.col == pos[1]:
            if piece.col > pos[1]:
                pass
            else:
                pass
    
    def check(self):
        if self.current_turn == 1:
            enemy = self.black
        else:
            enemy = self.white
        for piece in enemy:
            for move in piece.get_moves():
                if move in self.locked_pos:
                    if isinstance(self.locked_pos[move], King):
                        return True

        return False

    def checkmate(self):
        if self.current_turn == 1:
            pieces = self.white
        else:
            pieces = self.black

        for piece in pieces:
            for move in piece.get_moves():
                if not self.check_when_move(piece, move):
                    return False
        self.game_over()

    def show_winner(self, winner):
        c = 255
        while c > 0:
            text = FONT.render(winner, 1, (c, c, c))
            WIN.fill((0, 0, 0))
            WIN.blit(text, (WIDTH//2-text.get_width()//2,
                            HEIGHT//2-text.get_height()//2))
            c -= 2
            CLOCK.tick(FPS)
            pygame.display.update()

    def game_over(self):
        SOUND_CHECKMATE.play()
        winner = "WHITE WINS" if self.current_turn == 0 else "BLACK WINS"
        self.show_winner(winner)
        self.draw()
        pygame.display.update()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    run = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    run = False
                    break
            CLOCK.tick(FPS)

        self.reset_attributes()

    def ensure_moves(self):
        if self.current_turn == 1:
            pieces = self.white
        else:
            pieces = self.black
        for piece in pieces:
            if piece.get_moves():
                return True
        return False

    def check_when_move(self, piece, pos):
        ischeck = False
        enemy_piece = None
        piece_pos = (piece.row, piece.col)
        if pos in self.locked_pos:
            if self.current_turn == 1:
                enemy = self.black
            else:
                enemy = self.white
            enemy_piece = self.locked_pos[pos]
            enemy.remove(enemy_piece)

        del self.locked_pos[piece_pos]
        piece.row = pos[0]
        piece.col = pos[1]
        self.locked_pos[pos] = piece
        if self.check():
            ischeck = True
        piece.row = piece_pos[0]
        piece.col = piece_pos[1]
        self.locked_pos[piece_pos] = piece
        del self.locked_pos[pos]
        if enemy_piece:
            enemy.append(enemy_piece)
            self.locked_pos[pos] = enemy_piece

        return ischeck

    def draw(self):
        self.draw_window()
        self.draw_check()
        self.show_cursor()
        self.show_selected_piece()
        self.show_movable_places()
        self.draw_pieces()

    def draw_window(self):
        WIN.fill(GBLACK)
        for i in range(8):
            for j in range(8):
                if (i+j) % 2 == 0:
                    pygame.draw.rect(
                        WIN, GWHITE, (j*BLOCK_S, i*BLOCK_S, BLOCK_S, BLOCK_S))

    def draw_pieces(self):
        for piece in self.white:
            piece.draw()
        for piece in self.black:
            piece.draw()

    def draw_check(self):
        if self.ischeck:
            if self.current_turn == 1:
                king = self.white[0]
            else:
                king = self.black[0]
            pygame.draw.rect(WIN, RED, (king.col*BLOCK_S,
                             king.row*BLOCK_S, BLOCK_S, BLOCK_S))

    def get_grid_pos(self):
        return self.mouse_pos[1]//BLOCK_S, self.mouse_pos[0]//BLOCK_S

    def show_movable_places(self):
        if self.selected_piece:
            if self.grid_pos in self.movable_places:
                if (self.grid_pos[0]+self.grid_pos[1]) % 2 == 0:
                    color = GWHITE
                else:
                    color = GBLACK
                pygame.draw.rect(WIN, color, (self.grid_pos[1]*BLOCK_S,
                                              self.grid_pos[0]*BLOCK_S, BLOCK_S, BLOCK_S), 7)

    def show_selected_piece(self):
        if self.selected_piece:
            pygame.draw.rect(WIN, ORANGE, (BLOCK_S*self.selected_piece.col,
                                           BLOCK_S*self.selected_piece.row,
                                           BLOCK_S, BLOCK_S), 5)

    def show_cursor(self):
        if self.grid_pos in self.locked_pos:
            if self.locked_pos[self.grid_pos].kind == self.current_turn:
                pygame.draw.rect(WIN, BLUE, (BLOCK_S*self.grid_pos[1],
                                             BLOCK_S*self.grid_pos[0],
                                             BLOCK_S, BLOCK_S), 5)

    def select_piece(self):
        if self.grid_pos in self.locked_pos:
            if self.locked_pos[self.grid_pos].kind == self.current_turn:
                self.selected_piece = self.locked_pos[self.grid_pos]
                movable_places = self.selected_piece.get_moves()
                new_movable_places = []
                for move in movable_places:
                    if not self.check_when_move(self.selected_piece, move):
                        new_movable_places.append(move)
                self.movable_places = new_movable_places
            else:
                self.selected_piece = None

    def swap_current_turn(self):
        if self.current_turn == 1:
            self.current_turn = 0
        else:
            self.current_turn = 1

    def swap_side(self):
        dup = self.locked_pos.copy()
        self.locked_pos.clear()
        for i, j in dup:
            self.locked_pos[(7-i, 7-j)] = dup[(i, j)]
        for piece in self.black:
            piece.row = 7-piece.row
            piece.col = 7-piece.col
        for piece in self.white:
            piece.row = 7-piece.row
            piece.col = 7-piece.col


if __name__ == "__main__":
    game = Game()
    game.start() 
    pygame.quit()
