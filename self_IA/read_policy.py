import pickle
import operator

try:
    with open("policy.pickle", "r") as f:
        data = pickle.loads(f.read())
except:
    print "Can't open policy file"
    exit()


for state, actions in data.items():

    #actions = [action for action, q in actions.items() if q == max_q]
    actions_q = sorted([(key, value) for key, value in actions.items() if value != 0], key=operator.itemgetter(1), reverse=True)

    print state, "->", [(action, q) for action, q in actions.items()]
