def fatal_behavior(args):
    case = execution[args[-1]]
    return test_behavior(FittedPackage(case['regression']), cases[case['fixture_id']], contract)
