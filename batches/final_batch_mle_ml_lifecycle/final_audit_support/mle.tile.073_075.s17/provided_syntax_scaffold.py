import math

COST_TOLERANCE = 1e-9

def within_limit(value, limit):
    return value <= limit or math.isclose(value, limit, rel_tol=0.0, abs_tol=COST_TOLERANCE)


