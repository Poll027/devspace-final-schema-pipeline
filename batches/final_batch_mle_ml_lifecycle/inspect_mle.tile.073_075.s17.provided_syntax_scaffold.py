def fatal_acceptance(args):
    return acceptance(cases[args[-2]], cases[contract['accepted_reference']], contract, args[-1])
