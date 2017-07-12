class Target(object):
    D = 0
    S = 0
    L = 0

def make_target(D, S, L):
    target = Target()
    target.D = D
    target.S = S
    target.L = L
    return target