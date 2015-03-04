def combinations(num, *args):
    if len(args) < num:
        raise ValueError("not enough args")
    if len(args) == num:
        return args
