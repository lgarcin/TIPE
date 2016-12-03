def tobin(x):
    return tobin(x // 2) + [x % 2] if x > 1 else [x]


def todec(l):
    if len(l) == 0:
        return 0
    a = l.pop()
    return 2 * todec(l) + a


def code(n):
    step = 0
    li = []
    while n > 0:
        l = tobin(n)[1:]
        li = l + li
        n = len(l)
        step += 1
    return step * [1] + [0] + li


def decode(l):
    step = 0
    while l.pop(0) == 1:
        step += 1
    if step == 0:
        return 0
    N = 1
    for _ in range(step - 1):
        li = [1]
        for _ in range(N):
            li += [l.pop(0)]
        N = todec(li)
    return N


print([decode(code(x)) for x in range(20)])
