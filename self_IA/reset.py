import os
try:
    os.remove("policy.pickle")
except:
    pass

try:
    os.remove("log.txt")
except:
    pass