import pygame
import random
import time
from agent import QLearningAgent


class Shape(pygame.sprite.Sprite):

    SIZE = (190,190)


class Circle(Shape):

    CIRCLE_COLOR = (0,255,255)
    SUB_CIRCLE_COLOR = (0,0,255)

    def __init__(self, screen, square):

        self.x = square.pos[0] + self.SIZE[0] / 2
        self.y = square.pos[1] + self.SIZE[1] / 2
        pygame.draw.circle(screen, self.CIRCLE_COLOR, (self.x,self.y) , 60)
        pygame.draw.circle(screen, self.SUB_CIRCLE_COLOR, (self.x,self.y) , 50)

        square.circled = True


class Cross(Shape):

    CROSS_COLOR = (255,0,0)
    SUB_CROSS_COLOR = (0,0,255)
    FACE = 120
    SUB_FACE = 100

    def __init__(self, screen, square):

        self.x = square.pos[0] + self.SIZE[0] / 2 - self.FACE / 2
        self.y = square.pos[1] + self.SIZE[1] / 2 - self.FACE / 2
        pygame.draw.rect(screen, self.CROSS_COLOR, pygame.Rect(self.x,self.y,self.FACE,self.FACE))
        pygame.draw.rect(screen, self.SUB_CROSS_COLOR, pygame.Rect(self.x+10,self.y+10,self.SUB_FACE,self.SUB_FACE))

        square.crossed = True


class IA(object):

    def __init__(self, game, squares, screen):

        self.game = game
        self.squares = squares
        self.screen = screen

    def _get_state(self, squares):

        state = []
        for square in squares:
            if square.crossed:
                state.append("X")
            elif square.circled:
                state.append("O")
            else:
                state.append("-")

        return tuple(state)

    def get_empty_squares(self):

        return [s for s in self.squares if not s.marked()]

    def _play(self, agent):

        empty_squares = self.get_empty_squares()
        if not empty_squares:
            return

        state = self._get_state(self.squares)
        square_number = agent.get_action(state, empty_squares)
        square = self.squares[square_number]

        Circle(self.screen, square)

        return square, state

    def play_ia(self, agent):

        self._play(agent)

    def play(self, agent):

        square, state = self._play(agent)
        game_result = self.game.game_results()

        if game_result is None:
            #play with a random action player
            self.random_play()
            game_result = self.game.game_results()

        if game_result is not None:
            #end game
            new_state = None
            reward = game_result * 20
        else:
            new_state = self._get_state(self.squares)
            two_in_a_row_count = self.marks_in_a_row("circled")
            reward = square.score + two_in_a_row_count

        agent.learn(state, new_state, reward, square.number, "")

        return square.number

    def marks_in_a_row(self, mark, marks_num=2):

        marks_in_a_row_count = 0

        #check rows
        for i in range(3):
            marks_count = 0
            for j in range(3):
                num = i*3+j
                if getattr(self.squares[num], mark):
                    marks_count += 1
            if marks_count == marks_num:
                marks_in_a_row_count += 1

        #check columns
        for i in range(3):
            marks_count = 0
            for j in range(3):
                num = i+j*3
                if getattr(self.squares[num], mark):
                    marks_count += 1
            if marks_count == marks_num:
                marks_in_a_row_count += 1

        #check diagonals
        diagonals = [[0,4,8], [2,4,6]]
        for diagonal in diagonals:
            marks_count = 0
            for i in diagonal:
                if getattr(self.squares[i], mark):
                    marks_count += 1
            if marks_count == marks_num:
                marks_in_a_row_count += 1

        return marks_in_a_row_count

    def random_play(self):

        empty_squares = self.get_empty_squares()
        if not empty_squares:
            return

        square = random.choice(empty_squares)
        Cross(self.screen, square)


class Player(object):

    def play(self, square, screen):

        shape = self.shape_class(screen, square)


class Player1(Player):

    shape_class = Circle


class Player2(Player):

    shape_class = Cross


class Square(pygame.sprite.Sprite):

    SQUARE_SIZE = (190,190)
    SQUARE_COLOR = (0,0,255)

    def __init__(self, number, score, pos):

        pygame.sprite.Sprite.__init__(self)
        self.square = pygame.surface.Surface(self.SQUARE_SIZE)
        self.set_color(self.SQUARE_COLOR)
        self.set_position(pos)
        self.number = number
        self.score = score

        self.circled = False
        self.crossed = False

    def set_color(self, color):

        self.square.fill(color)

    def set_position(self, pos):

        self.x = pos[0]
        self.y = pos[1]
        self.pos = pos

    def marked(self):

        return self.crossed or self.circled

    def clicked(self, pos):

        return self.x < pos[0] and self.x + Game.SQUARE_WIDHT > pos[0] and self.y < pos[1] and self.y + Game.SQUARE_HEIGHT > pos[1]


class Game(object):

    SIZE = (590,590)
    SQUARE_HEIGHT = 200
    SQUARE_WIDHT = 200
    squares = []

    squares_scores = [0.5, 0.2, 0.5,
                      0.2, 10, 0.2,
                      0.5, 0.2, 0.5]

    def __init__(self):

        pygame.init()

        self.player1 = Player1()
        self.player2 = Player2()

        for i in range(3):
            for j in range(3):
                num = i*3+j
                square = Square(num, self.squares_scores[num], (i*self.SQUARE_WIDHT, j*self.SQUARE_HEIGHT))
                self.squares.append(square)

        self.screen = pygame.display.set_mode(self.SIZE)
        self.cpu = IA(self, self.squares, self.screen)

    def initialize(self):

        for square in self.squares:
            self.screen.blit(square.square , square.pos)
            square.circled = False
            square.crossed = False

    def human_play(self, pos, agent):

        valid_click = False
        for square in self.squares:
            if square.clicked(pos) and not square.marked():
                valid_click = True
                self.player2.play(square, self.screen)

        if not valid_click:
            return

        if self.game_results() is None:
            self.cpu.play_ia(agent)

    def play(self, agent):

        return self.cpu.play(agent)

    def game_results(self):

        if self.cpu.marks_in_a_row("circled", marks_num=3):
            self.winner("Circulo")
            return 1

        if self.cpu.marks_in_a_row("crossed", marks_num=3):
            self.winner("Cuadrado")
            return -1

        if not self.cpu.get_empty_squares():
            self.due()
            return 0

        return None

    def winner(self, player):

        font = pygame.font.Font(None, 40)
        msg = "ganador el jugador del {}!!!".format(player)
        sup = font.render(msg, True, (255,255,0))
        self.screen.blit(sup, (50,50))

    def due(self):

        font = pygame.font.Font(None, 40)
        sup = font.render("Ha resultado un empate!", True, (255,255,0))
        self.screen.blit(sup, (140,50))

    def reset(self):

        back = pygame.surface.Surface(self.SIZE)
        self.screen.blit(back, (0,0))

    def get_state(self):

        return self.cpu._get_state(self.squares)

    def train(self, total_games=500):

        fixed_epsilon = None
        alpha = 0.5
        gamma = 0.9
        epsilon = 1

        agent = QLearningAgent(epsilon=epsilon, fixed_epsilon=fixed_epsilon, alpha=alpha, gamma=gamma, total_games=total_games)
        for game_number in range(total_games):

            last_action = None

            while True:
                game_result = game.game_results()
                if game_result is not None:
                    pygame.display.flip()
                    game.reset()
                    game.initialize()
                    break

                last_action = game.play(agent)

                pygame.display.flip()

        agent.save_policy()
        return agent


if __name__ == "__main__":

    game = Game()
    game.initialize()
    pygame.display.flip()

    agent = game.train(total_games=0)
    #do not explorate more
    agent.use_epsilon = False

    game.cpu.play_ia(agent)
    pygame.display.flip()
    end = False
    game_started = True

    while not end:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True

            if event.type == pygame.MOUSEBUTTONDOWN:

                if not game_started:
                    game.cpu.play_ia(agent)
                    pygame.display.flip()
                    game_started = True
                else:
                    game.human_play(pygame.mouse.get_pos(), agent)

                    game_result = game.game_results()
                    if game_result is not None:
                        pygame.display.flip()
                        game.reset()
                        game.initialize()
                        game_started = False

                        break

                    pygame.display.flip()

    pygame.display.quit()

