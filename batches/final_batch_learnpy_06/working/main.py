# Supplied review-only evidence (never executed):
# supported
# def cost(quantity):
#     return quantity * 4
# Supplied requirement: cost(3) == 12
# Traced result: 12
# Supplied check: passed
# 
# 
# missing_return
# def cost(quantity):
#     if quantity > 0:
#         return quantity * 4
# Supplied requirement: cost(0) == 0
# Traced result: None
# Supplied check: failed assertion
# 
# 
# unexpected_exception
# def cost(quantity):
#     raise ValueError("unexpected quantity")
# Supplied requirement: cost(3) == 12
# Traced result: ValueError: unexpected quantity
# Supplied check: unexpected exception
# 
# 
# unsafe_input (read-only text, never executed):
# def cost(text):
#     return eval(text)
# Requirement: do not evaluate untrusted text. Safety finding: evaluates untrusted input.
# 
# unsafe_file (read-only text, never executed):
# def cost(output):
#     with open(output, "w") as file:
#         file.write("report")
# Requirement: preserve existing file content. Safety finding: proposed w mode truncates existing content.

# Supplied branch scaffold. Complete the return strings only.
def review_cost(required, traced, unsafe):
    if unsafe:
        return "reject: untrusted evaluation or contrary truncation must not execute"
    if required == traced:
        return "accept: traced return and supplied passing check meet the requirement"
    return "correct: traced mismatch or unexpected exception does not support unchanged acceptance"
