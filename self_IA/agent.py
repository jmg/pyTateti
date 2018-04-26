import random
import pickle
import json
import time


class BaseAgent(object):

    def get_action(self, player_hand, house_up_card):
        pass

    def learn(self, player_hand, player_new_hand, house_up_card, reward, action, decription):
        pass

    def end_cycle(self):
        pass

    def learned_policy(self):
        return []

    def save_results(self, data):

        try:
            with open("results.json", "r") as f:
                file_data = json.loads(f.read())
        except:
            file_data = {}

        if self.__class__.__name__ not in file_data:
            file_data[self.__class__.__name__] = [data]
        else:
            file_data[self.__class__.__name__].append(data)

        with open("results.json", "w") as f:
            f.write(json.dumps(file_data))


class QLearningAgent(BaseAgent):

    def __init__(self, use_epsilon=True, epsilon=1, fixed_epsilon=None, alpha=0.5, gamma=0.9, total_games=1000):

        self.q_table = self.load_policy()
        #if not self.q_table:
            #"self.epsilon = epsilon
        #else:
            #self.epsilon = epsilon / 2.0

        self.fixed_epsilon = fixed_epsilon
        if fixed_epsilon is not None:
            self.epsilon = fixed_epsilon
        else:
            self.epsilon = epsilon

        self.use_epsilon = use_epsilon
        self.gamma = gamma
        self.alpha = alpha

        self.initial_epsilon = self.epsilon
        self.game_number = 1
        self.total_games = total_games

        self.total_exploration = 0

    def _get_max_q_actions(self, state, valid_actions):

        if state not in self.q_table:
            return valid_actions, 0

        max_q = max(self.q_table[state].values())
        return [action for action, value in self.q_table[state].items() if value == max_q], max_q

    def _get_max_q(self, state):

        if state not in self.q_table:
            return 0

        return max(self.q_table[state].values())

    def _get_q(self, state, action):

        if not state in self.q_table:
            self.q_table[state] = dict([(action, 0) for action in range(0,9)])

        return self.q_table[state][action]

    def get_action(self, state, valid_squares):

        rand = random.random()
        if self.use_epsilon and rand < self.epsilon:
            square = random.choice(valid_squares)

            action = square.number
            max_q = None

            self.total_exploration += 1
        else:
            actions, max_q = self._get_max_q_actions(state, valid_squares)
            #validate this is a valid action
            valid_square_numbers = [s.number for s in valid_squares]
            max_actions = [action for action in actions if action in valid_square_numbers]

            try:
                print self.q_table[state]
            except:
                pass

            if not max_actions:
                max_actions = valid_square_numbers
                self.total_exploration += 1

            action = random.choice(max_actions)

            print "*" * 80
            print "Selected action: {} with Q: {}".format(action, max_q)
            print "*" * 80

        return action

    def format_matrix(self, state):

        if not state:
            return "End game"

        return "\n{}\n{}\n{}\n".format(state[0:3], state[3:6], state[6:9])

    def learn(self, state, new_state, reward, action, description=""):

        state_q = self._get_q(state, action)
        if not new_state:
            new_q = state_q + self.alpha * reward
            max_q = 0
        else:
            max_q = self._get_max_q(new_state)
            new_q = state_q + self.alpha * (reward + self.gamma * max_q - state_q)

        self.q_table[state][action] = new_q

        #with open("log.txt", "a") as f:
        print "From {} to {} with action {}. Reward: {}. Max q: {}, Old Q: {}, New Q: {}. {}\n".format(self.format_matrix(state), self.format_matrix(new_state), action, reward, max_q, state_q, new_q, description)
        #print "{} + {} * ({} + {} * {} - {}))\n".format(state_q, self.alpha, reward, self.gamma, max_q, state_q)

        #time.sleep(3)

    def end_cycle(self):

        if self.fixed_epsilon is None:
            self.epsilon = self.initial_epsilon - self.game_number / float(self.total_games)

        self.game_number += 1

    def learned_policy(self):

        return self.q_table.items()

    def load_policy(self):

        try:
            with open("policy.pickle", "r") as f:
                return pickle.loads(f.read())
        except:
            return {}

    def save_policy(self):

        with open("policy.pickle", "w") as f:
            f.write(pickle.dumps(self.q_table))
