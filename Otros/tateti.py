import pygame

class circle(pygame.sprite.Sprite):

    CIRCLE_SIZE = (290,290)
    CIRCLE_COLOR = (0,0,255)
    
    def __init__(self, screen, pos):
        pygame.sprite.Sprite.__init__(self)
        x = pos[0] + self.CIRCLE_SIZE[0] / 2
        y = pos[1] + self.CIRCLE_SIZE[1] / 2 
        pygame.draw.circle(screen, self.CIRCLE_COLOR, (x,y) , 100)
        
        
class cross(pygame.sprite.Sprite):

    CROSS_SIZE = (290,290)
    CROSS_COLOR = (255,0,0)
    FACE = 200
    
    def __init__(self, screen, pos):
        pygame.sprite.Sprite.__init__(self)
        x = pos[0] + self.CROSS_SIZE[0] / 2 - self.FACE / 2
        y = pos[1] + self.CROSS_SIZE[1] / 2 - self.FACE / 2
        pygame.draw.rect(screen, self.CROSS_COLOR, pygame.Rect(x,y,self.FACE,self.FACE))

class IA:
    
    def __init__(squares):
        self.square = squares
    
    def play(self, square, screen):
        mark = cross(screen, square.pos)
        square.crossed = True
        
    def 
            
class Player1:

    def play(self, square, screen):
        mark = circle(screen, square.pos)
        square.circled = True

class Player2:

    def play(self, square, screen):
        mark = cross(screen, square.pos)
        square.crossed = True
        

class square(pygame.sprite.Sprite):
    
    SQUARE_SIZE = (290,290)
    SQUARE_COLOR = (255,255,255)
    circled = False
    crossed = False
    
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.square = pygame.surface.Surface(self.SQUARE_SIZE)
        self.setColor(self.SQUARE_COLOR)
        self.setPos(pos)
        
    def setColor(self, color):
        self.square.fill(color)
        
    def setPos(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.pos = pos
        
         
class window:
    
    SIZE = (890,890)
    SQUARE_HEIGHT = 300
    SQUARE_WIDHT = 300
    turn = 1
    player1 = Player1()
    player2 = Player2()
    
    square1 = square((0,0))
    square2 = square((0,SQUARE_HEIGHT))
    square3 = square((0,SQUARE_HEIGHT * 2))
    
    square4 = square((SQUARE_WIDHT,0))
    square5 = square((SQUARE_WIDHT,SQUARE_HEIGHT))
    square6 = square((SQUARE_WIDHT,SQUARE_HEIGHT * 2))
    
    square7 = square((SQUARE_WIDHT * 2,0))
    square8 = square((SQUARE_WIDHT * 2,SQUARE_HEIGHT))
    square9 = square((SQUARE_WIDHT * 2,SQUARE_HEIGHT * 2))
    
    squares = [square1,square2,square3, \
               square4,square5,square6, \
              square7,square8,square9]
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.SIZE)
        
    def initialize(self):
        for square in self.squares:
            self.screen.blit(square.square , square.pos)
            square.circled = False
            square.crossed = False
        
    def clicked(self, pos):
        for square in self.squares:
            if square.x < pos[0] and square.x + self.SQUARE_WIDHT > pos[0] \
            and square.y < pos[1] and square.y + self.SQUARE_HEIGHT > pos[1] \
            and not square.circled and not square.crossed:
                if self.turn == 1:
                    self.player1.play(square, self.screen)
                    self.turn = 2
                else:
                    self.player2.play(square, self.screen)
                    self.turn = 1
    
    def checkWinner(self):
        if self.squares[0].circled and self.squares[1].circled and self.squares[2].circled or \
        self.squares[3].circled and self.squares[4].circled and self.squares[5].circled or \
        self.squares[6].circled and self.squares[7].circled and self.squares[8].circled or \
        self.squares[0].circled and self.squares[3].circled and self.squares[6].circled or \
        self.squares[1].circled and self.squares[4].circled and self.squares[7].circled or \
        self.squares[2].circled and self.squares[5].circled and self.squares[8].circled or \
        self.squares[0].circled and self.squares[4].circled and self.squares[8].circled or \
        self.squares[6].circled and self.squares[4].circled and self.squares[2].circled: 
            self.winner("circulo")
            return True
            
        elif self.squares[0].crossed and self.squares[1].crossed and self.squares[2].crossed or \
        self.squares[3].crossed and self.squares[4].crossed and self.squares[5].crossed or \
        self.squares[6].crossed and self.squares[7].crossed and self.squares[8].crossed or \
        self.squares[0].crossed and self.squares[3].crossed and self.squares[6].crossed or \
        self.squares[1].crossed and self.squares[4].crossed and self.squares[7].crossed or \
        self.squares[2].crossed and self.squares[5].crossed and self.squares[8].crossed or \
        self.squares[0].crossed and self.squares[4].crossed and self.squares[8].crossed or \
        self.squares[6].crossed and self.squares[4].crossed and self.squares[2].crossed: 
            self.winner("cuadrado")
            return True
        
    def winner(self, player):
        font = pygame.font.Font(None, 60)
        sup = font.render("ganador el jugador del " + player + "!!!", True, (150,20,255))
        self.screen.blit(sup, (100,100))
        
    def checkDue(self):
        for square in self.squares:
            if not square.circled and not square.crossed:
                return False
        self.due()
        return True
        
    def due(self):
        font = pygame.font.Font(None, 60)
        sup = font.render("Ha resultado un empate!", True, (150,20,255))
        self.screen.blit(sup, (180,100))
    
    def reset(self):
        back = pygame.surface.Surface(self.SIZE)
        self.screen.blit(back, (0,0))
        
        
if __name__ == "__main__":
    
    game = window()
    game.initialize()
    pygame.display.flip()
    
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.checkWinner() or game.checkDue():
                    game.reset()
                    game.initialize()
                    break
                game.clicked(pygame.mouse.get_pos())
                
        if not game.checkWinner():
            game.checkDue()
        
        pygame.display.flip()
                
