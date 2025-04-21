# A function for generating a sequence with a fractional step
def frange(x, y, jump):
    while x <= y:
        yield x
        x += jump