import pygame
import random


class Shape(pygame.sprite.Sprite):

    SIZE = (190,190)       


class Circle(Shape):
       
    CIRCLE_COLOR = (0,255,255)
    SUB_CIRCLE_COLOR = (0,0,255)

    def __init__(self, screen, pos):
        
        self.x = pos[0] + self.SIZE[0] / 2
        self.y = pos[1] + self.SIZE[1] / 2
        pygame.draw.circle(screen, self.CIRCLE_COLOR, (self.x,self.y) , 60)
        pygame.draw.circle(screen, self.SUB_CIRCLE_COLOR, (self.x,self.y) , 50)
    
    def mark(self, square):
        
        square.circled = True


class Cross(Shape):
    
    CROSS_COLOR = (255,0,0)
    SUB_CROSS_COLOR = (0,0,255)
    FACE = 120
    SUB_FACE = 100

    def __init__(self, screen, pos):
        
        self.x = pos[0] + self.SIZE[0] / 2 - self.FACE / 2
        self.y = pos[1] + self.SIZE[1] / 2 - self.FACE / 2
        pygame.draw.rect(screen, self.CROSS_COLOR, pygame.Rect(self.x,self.y,self.FACE,self.FACE))
        pygame.draw.rect(screen, self.SUB_CROSS_COLOR, pygame.Rect(self.x+10,self.y+10,self.SUB_FACE,self.SUB_FACE))
        
    def mark(self, square):
        
        square.crossed = True
        

class IA(object):

    def __init__(self, squares, screen):
        self.squares = squares
        self.screen = screen

    def play(self, type):
        if type == 2:
            square = self.think()
            mark = Cross(self.screen, square.pos)
            square.crossed = True
            print square.pos, "crossed"
        else:
            square = self.think()
            mark = Circle(self.screen, square.pos)
            square.circled = True
            print square.pos, "circled"

    def think(self):
        if self.tate():
            return self.tate()
        else:
            if not self.center().marked():
                return self.center()
            elif not self.twoCorners():
                return self.selectCorner()
            else:
                return self.anySide()

    def twoCorners(self):
        if self.squares[0].circled and self.squares[8].circled:
            return True
        if self.squares[2].circled and self.squares[6].circled:
            return True
        return False

    def tate(self):

        tateList = self.posibleTate()

        for places in tateList:

            if places[1] - places[0] == 1:
                if (places[1] + 1) % 3 == 0 and not self.squares[places[0]-1].marked():
                    return self.squares[places[0]-1]
                elif places[1] + 1 <= 8 and not self.squares[places[1]+1].marked():
                    return self.squares[places[1]+1]
                else:
                    continue

            if places[1] - places[0] == 3:
                if (places[1] + 3) > 8 and not self.squares[places[0]-3].marked():
                    return self.squares[places[0]-3]
                elif (places[1] + 3) <= 8 and not self.squares[places[1]+3].marked():
                    return self.squares[places[1]+3]
                else:
                    continue

            if places[1] - places[0] == 4:
                if places[1] == 4 and not self.squares[places[1]+4].marked():
                    return self.squares[places[1]+4]
                elif places[1] == 8 and not self.squares[places[0]-4].marked():
                    return self.squares[places[0]-4]
                else:
                    continue

            if places[1] - places[0] == 2:
                if places[1] == 6 and places[0] == 4 and not self.squares[places[0]-2].marked():
                    return self.squares[places[0]-2]
                elif places[1] == 4 and places[0] == 2 and not self.squares[places[1]+2].marked():
                    return self.squares[places[1]+2]
                elif (places[1] == 2 or places[1] == 5 or places[1] == 8) and not self.squares[places[1]-1].marked():
                    return self.squares[places[1]-1]
                else:
                    continue

            if places[1] - places[0] == 6 and not self.squares[places[1]-3].marked():
                return self.squares[places[1]-3]
            else:
                continue

        return False

    def posibleTate(self):
        tateList = []
        sub = [0,1,3,4]
        for i in sub:
            if i == 0 or i == 4:
                if self.squares[i].circled and self.squares[i+4].circled or \
                self.squares[i].crossed and self.squares[i+4].crossed:
                    tateList.append((i,i+4))
            if i == 1 or i == 3:
                if self.squares[i+1].circled and self.squares[i+3].circled or \
                self.squares[i+1].crossed and self.squares[i+3].crossed:
                    tateList.append((i+1,i+3))
            if self.squares[i].circled and self.squares[i+3].circled or \
            self.squares[i].crossed and self.squares[i+3].crossed:
                tateList.append((i,i+3))
            if self.squares[i].circled and self.squares[i+1].circled or \
            self.squares[i].crossed and self.squares[i+1].crossed:
                tateList.append((i,i+1))
        if self.squares[6].circled and self.squares[7].circled or \
        self.squares[6].crossed and self.squares[7].crossed:
            tateList.append((6,7))
        if self.squares[2].circled and self.squares[5].circled or \
        self.squares[2].crossed and self.squares[5].crossed:
            tateList.append((2,5))
        if self.squares[5].circled and self.squares[8].circled or \
        self.squares[5].crossed and self.squares[8].crossed:
            tateList.append((5,8))
        if self.squares[7].circled and self.squares[8].circled or \
        self.squares[7].crossed and self.squares[8].crossed:
            tateList.append((7,8))

        for i in range(3):
            if self.squares[i].circled and self.squares[i+6].circled or \
            self.squares[i].crossed and self.squares[i+6].crossed:
                tateList.append((i,i+6))
        sub = [0,3,6]
        for i in sub:
            if self.squares[i].circled and self.squares[i+2].circled or \
            self.squares[i].crossed and self.squares[i+2].crossed:
                tateList.append((i,i+2))

        return tateList

    def center(self):
        return self.squares[4]

    def corners(self):
        return [0,2,6,8]

    def selectCorner(self):
        corner = [0,2,6,8]
        if self.squares[3].marked() and self.squares[1].marked():
            corner.remove(8)
        if self.squares[3].marked() and self.squares[7].marked():
            corner.remove(2)
        if self.squares[5].marked() and self.squares[7].marked():
            corner.remove(0)
        if self.squares[1].marked() and self.squares[5].marked():
            corner.remove(6)
        for i in range(len(corner)):
            square = self.squares[corner[random.randint(0,len(corner) - 1)]]
            if not square.marked():
                return square
        return self.anySide()

    def anySide(self):
        corner = [1,3,5,7]
        for i in range(4):
            square = self.squares[corner[random.randint(0,3)]]
            if not square.marked():
                return square
        return self.any()

    def any(self):
        for square in self.squares:
            if not square.marked():
                return square


class Player(object):

    def play(self, square, screen):
        
        shape = self.shape_class(screen, square.pos)
        shape.mark(square)        


class Player1(Player):

    shape_class = Circle
        

class Player2(Player):
    
    shape_class = Cross

    
class Square(pygame.sprite.Sprite):

    SQUARE_SIZE = (190,190)
    SQUARE_COLOR = (0,0,255)
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

    def marked(self):
        return self.crossed or self.circled


class window(object):

    SIZE = (590,590)
    SQUARE_HEIGHT = 200
    SQUARE_WIDHT = 200

    square1 = Square((0,0))
    square2 = Square((0,SQUARE_HEIGHT))
    square3 = Square((0,SQUARE_HEIGHT * 2))

    square4 = Square((SQUARE_WIDHT,0))
    square5 = Square((SQUARE_WIDHT,SQUARE_HEIGHT))
    square6 = Square((SQUARE_WIDHT,SQUARE_HEIGHT * 2))

    square7 = Square((SQUARE_WIDHT * 2,0))
    square8 = Square((SQUARE_WIDHT * 2,SQUARE_HEIGHT))
    square9 = Square((SQUARE_WIDHT * 2,SQUARE_HEIGHT * 2))

    squares = [square1,square2,square3, \
               square4,square5,square6, \
              square7,square8,square9]

    turn = 1
    player1 = Player1()
    player2 = Player2()
    cpu = None

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.SIZE)
        self.cpu = IA(self.squares, self.screen)

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
                self.cpu.play(self.squares, self.screen, 1)
                if not self.checkWinner() and not self.checkDue():
                    self.cpu.play(2)

    def play(self):
        self.cpu.play(1)
        if not self.checkWinner() and not self.checkDue():
            self.cpu.play(2)

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
        font = pygame.font.Font(None, 40)
        sup = font.render("ganador el jugador del " + player + "!!!", True, (255,255,0))
        self.screen.blit(sup, (50,50))

    def checkDue(self):
        for square in self.squares:
            if not square.circled and not square.crossed:
                return False
        self.due()
        return True

    def due(self):
        font = pygame.font.Font(None, 40)
        sup = font.render("Ha resultado un empate!", True, (255,255,0))
        self.screen.blit(sup, (140,50))

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

        if game.checkWinner():
            contin = False
            while not contin:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        game.reset()
                        game.initialize()
                        contin = True

        if game.checkDue():
            game.reset()
            game.initialize()
            print "new game"

        #game.clicked(pygame.mouse.get_pos())
        game.play()

        if not game.checkWinner():
            game.checkDue()

        pygame.display.flip()

