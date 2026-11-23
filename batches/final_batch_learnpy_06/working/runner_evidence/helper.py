def cost(quantity):
    if quantity < 0:
        raise ValueError("negative quantity")
    return quantity * 4
