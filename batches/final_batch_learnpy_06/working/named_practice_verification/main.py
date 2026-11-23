text = "3"
quantity = None
# Rejected, non-executable proposal: quantity = eval(text)
# Requirement: a nonnegative integer; malformed/negative text leaves quantity None.


try:
    quantity = int(text)
    if quantity < 0:
        quantity = None
except ValueError:
    quantity = None
