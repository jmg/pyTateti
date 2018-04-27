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

    def get_state(self, squares):

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

    def play(self, agent):

        empty_squares = self.get_empty_squares()
        if not empty_squares:
            return

        state = self.get_state(self.squares)
        square_number = agent.get_action(state, empty_squares)
        square = self.squares[square_number]

        Circle(self.screen, square)

        return square, state

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

    circled = False
    crossed = False

    def __init__(self, number, pos):

        pygame.sprite.Sprite.__init__(self)
        self.square = pygame.surface.Surface(self.SQUARE_SIZE)
        self.set_color(self.SQUARE_COLOR)
        self.set_position(pos)
        self.number = number

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

    def __init__(self):

        pygame.init()

        self.player1 = Player1()
        self.player2 = Player2()

        for i in range(3):
            for j in range(3):
                num = i*3+j
                square = Square(num, (j*self.SQUARE_HEIGHT, i*self.SQUARE_WIDHT))
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

        self.learn(agent, self.old_state, self.last_selected_square)

        if self.game_results() is None:
            self.play_ia(agent)

        if self.game_results() is not None:
            self.learn(agent, self.old_state, self.last_selected_square)

    def play_ia(self, agent):

        square, state = self.cpu.play(agent)
        self.old_state = state
        self.last_selected_square = square

    def play(self, agent, second_player_action):

        square, state = self.cpu.play(agent)
        game_result = self.game_results()

        if game_result is None:
            #play with a random action player
            self.cpu.random_play()

        self.learn(agent, state, square.number)
        return square.number

    def learn(self, agent, old_state, selected_square):

        game_result = self.game_results()
        if game_result is not None:
            #end game
            new_state = None
            reward = game_result * 10
        else:
            new_state = self.cpu.get_state(self.squares)
            reward = self.calculate_score()

        agent.learn(old_state, new_state, reward, selected_square.number, "")

    def calculate_score(self):

        two_in_a_row_count = self.posibilities_of_n_in_a_row("circled", marks_num=2)
        one_in_a_row_count = self.posibilities_of_n_in_a_row("circled", marks_num=1)

        counter_two_in_a_row_count = self.posibilities_of_n_in_a_row("crossed", marks_num=2)
        counter_one_in_a_row_count = self.posibilities_of_n_in_a_row("crossed", marks_num=1)

        score = two_in_a_row_count * 2 + one_in_a_row_count - counter_two_in_a_row_count * 2 - counter_one_in_a_row_count

        print "*" * 80
        print "The current state score is: {}".format(score)
        print "{} + {} - {} - {}".format(two_in_a_row_count * 2, one_in_a_row_count, counter_two_in_a_row_count * 2, counter_one_in_a_row_count)
        print "*" * 80

        return score

    def _get_marks_in_row(self, rows, mark, marks_num=2):

        marks_in_a_row_count = 0

        counter_marks = {
            "circled": "crossed",
            "crossed": "circled",
        }
        counter_mark = counter_marks[mark]

        for row in rows:
            marks_count = 0
            counter_marks_count = 0
            for num in row:
                if getattr(self.squares[num], mark):
                    marks_count += 1
                elif getattr(self.squares[num], counter_mark):
                    counter_marks_count += 1

            if marks_count == marks_num and counter_marks_count == 0:
                marks_in_a_row_count += 1

        return marks_in_a_row_count

    def posibilities_of_n_in_a_row(self, mark, marks_num=3):

        marks_in_a_row_count = 0

        rows = [[0,1,2],[3,4,5],[6,7,8]]
        cols = [[0,3,6],[1,4,7],[2,5,8]]
        diagonals = [[0,4,8], [2,4,6]]

        marks_in_a_row_count += self._get_marks_in_row(rows, mark, marks_num)
        marks_in_a_row_count += self._get_marks_in_row(cols, mark, marks_num)
        marks_in_a_row_count += self._get_marks_in_row(diagonals, mark, marks_num)

        return marks_in_a_row_count

    def game_results(self):

        if self.posibilities_of_n_in_a_row("circled", marks_num=3):
            self.winner("Circulo")
            return 1

        if self.posibilities_of_n_in_a_row("crossed", marks_num=3):
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

        return self.cpu.get_state(self.squares)

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

    game.play_ia(agent)
    game.calculate_score()

    pygame.display.flip()
    end = False
    game_started = True

    while not end:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True

            if event.type == pygame.MOUSEBUTTONDOWN:

                if not game_started:
                    game.play_ia(agent)
                    game.calculate_score()

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

