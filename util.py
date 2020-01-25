def add(t1, t2):
    return tuple([sum(x) for x in zip(t1, t2)])

def div(t, c):
    return tuple([x // c for x in t])
