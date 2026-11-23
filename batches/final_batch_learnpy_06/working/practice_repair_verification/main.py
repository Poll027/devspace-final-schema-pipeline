text = "3"
quantity = None
# Rejected, non-executable proposal: quantity = eval(text)
# Requirement: a nonnegative integer; malformed/negative text leaves quantity None.


# TODO: Implement the quantity parser for text without executing the supplied text. Valid nonnegative integer text must produce the integer in quantity. Malformed text and negative integers must leave quantity as None without an uncaught conversion error. Write the conversion-error handler and explicit nonnegative validation yourself. Keep the rejected eval proposal commented and never use eval, exec or shell invocation. Keep the supplied input unchanged.
