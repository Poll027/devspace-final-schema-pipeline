# Intended behavior: a positive quantity returns "positive".
# The comparison below is deliberately wrong. Inspect it before correcting it.
def quantity_branch(quantity):
    breakpoint()
    if quantity < 0:
        return "positive"
    else:
        return "not positive"

quantity = 3
result = quantity_branch(quantity)
