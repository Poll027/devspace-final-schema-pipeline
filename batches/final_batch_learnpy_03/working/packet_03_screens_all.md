# EVALUATOR PACKET — Exception flow and cleanup (learn_python.tile.051_053)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.exception_hierarchy — Exception hierarchy
B = python.exception_propagation — Exception propagation through calls
C = python.finally_cleanup — Guaranteed cleanup with finally

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.exception_hierarchy)   objective: Classify Python exception types by their position in the exception hierarchy.
A.f1: BaseException is the root of the built-in exception hierarchy, and Exception is its subclass for ordinary application failures.   [sources: python_stdlib_reference#exceptions.html#exception-hierarchy]
A.f2: ValueError and OSError are subclasses of Exception, and FileNotFoundError is a subclass of OSError.   [sources: python_stdlib_reference#exceptions.html#exception-hierarchy]
A.f3: KeyboardInterrupt, SystemExit and GeneratorExit are directly under BaseException rather than under Exception.   [sources: python_stdlib_reference#exceptions.html#exception-hierarchy]
note: Begin with this objective: Classify Python exception types by their position in the exception hierarchy.
note: Keep the example in the Exception flow and cleanup tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.exception_propagation, python.finally_cleanup, python.functions_as_values.
PRACTICE ANCHOR (matching): Match ValueError, OSError, FileNotFoundError and KeyboardInterrupt to their direct parents in the documented exception hierarchy.  SUCCESS: ValueError and OSError are matched to Exception, FileNotFoundError to OSError, and KeyboardInterrupt to BaseException.
ASSESSMENT ANCHOR: identify_baseexception_root_and_exception_branch facts=['f1']
ASSESSMENT ANCHOR: identify_parent_subclass_relationships facts=['f2']
ASSESSMENT ANCHOR: distinguish_direct_baseexception_signals_from_exception_subclasses facts=['f3']

## SOURCE FACTS — B (python.exception_propagation)   objective: Trace exception propagation through function calls.
B.f1: A raised exception skips the remaining operations in its current try body and searches for a matching handler.   [sources: python_tutorial#errors.html#handling-exceptions]
B.f2: Handler matching accepts an exception of the named class or a subclass; handlers are examined in their written order.   [sources: python_tutorial#errors.html#handling-exceptions]
B.f3: If no local handler matches, the exception propagates through the callers to an outer handler, or becomes unhandled if none matches.   [sources: python_tutorial#errors.html#handling-exceptions]
B.f4: When a handler recovers, execution continues after its try/except statement, not at the failed operation.   [sources: python_tutorial#errors.html#handling-exceptions]
note: Begin with this objective: Trace exception propagation through function calls.
note: Keep the example in the Exception flow and cleanup tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.finally_cleanup, python.functions_as_values, python.closures_and_enclosing_scope.
PRACTICE ANCHOR (live_code): Trace a conversion failure in quantity(text) to its caller's ValueError handler, identifying the skipped operation and where execution resumes.  SUCCESS: Correctly predict and confirm that quantity("three") fails during conversion, the converted-value output is skipped, and the caller displays Invalid quantity followed by After recovery.
ASSESSMENT ANCHOR: identify_first_matching_handler_in_call_chain facts=['f2', 'f3']
ASSESSMENT ANCHOR: identify_skipped_operations_and_resumption_point facts=['f1', 'f4']

## SOURCE FACTS — C (python.finally_cleanup)   objective: Guarantee cleanup with finally.
C.f1: Place release operations in an aligned finally: body following try: to run them when leaving the protected operation.   [sources: python_tutorial#errors.html#defining-clean-up-actions]
C.f2: finally executes on normal completion, on an exception and on a return from the try body.   [sources: python_tutorial#errors.html#defining-clean-up-actions]
C.f3: An unhandled exception is re-raised after finally completes normally; a return from finally can replace a pending return or suppress a pending exception.   [sources: python_tutorial#errors.html#defining-clean-up-actions]
note: Begin with this objective: Guarantee cleanup with finally.
note: Keep the example in the Exception flow and cleanup tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.functions_as_values, python.closures_and_enclosing_scope, python.pathlib_paths.
PRACTICE ANCHOR (live_code): Complete read_quantity(text), where text is a manually opened file supplied to the function, so that text.close() runs in finally after attempting to read and convert its contents.  SUCCESS: The supplied file is closed whether conversion returns an integer or fails. Successful conversion retains its return value, and failed conversion retains its unhandled exception.
ASSESSMENT ANCHOR: predict_cleanup_on_normal_completion_exception_and_return facts=['f1', 'f2']
ASSESSMENT ANCHOR: predict_exception_propagation_after_cleanup facts=['f3']
ASSESSMENT ANCHOR: identify_finally_return_overriding_pending_exit facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Avoiding shared mutable default arguments; Binding variable arguments with *args and **kwargs; Choosing instance, class or static method binding; Classes and instances; Closures and enclosing scope; Constructing and resolving pathlib paths; Defining custom exceptions; Distinguishing input failures from programming defects; Exception propagation through calls; Extending inherited behavior with super; Guaranteed cleanup with finally; Initialising instance state with __init__; Inspecting object types and attributes; Instance methods and self; Instance versus class attributes; Investigating Python execution with a debugger; Lambda expressions; Object composition; Ordering iterables with a key function; Passing and storing functions as values; Performing filesystem operations with pathlib; Python encapsulation conventions; Raising exceptions; Reading Python tracebacks; Selecting safe file-opening modes; Selecting specific exception handlers; Serialising and deserialising data with Python json

## LESSON, in learner order

### s01 · explainer · Exception hierarchy
(definition) BaseException is the root of Python’s built-in exception hierarchy. Its Exception subclass covers ordinary application failures. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) ValueError and OSError sit under Exception. FileNotFoundError sits under OSError. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) KeyboardInterrupt, SystemExit and GeneratorExit sit directly under BaseException, not under Exception. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[DIAGRAM: Exception hierarchy] nodes=['BaseException', 'Exception', 'ValueError', 'OSError', 'FileNotFoundError', 'KeyboardInterrupt', 'SystemExit', 'GeneratorExit'] edges=[('n1', 'n2', 'subclass'), ('n2', 'n3', 'subclass'), ('n2', 'n4', 'subclass'), ('n4', 'n5', 'subclass'), ('n1', 'n6', 'subclass'), ('n1', 'n7', 'subclass'), ('n1', 'n8', 'subclass')] alt: Built-in exception branches: BaseException → Exception; Exception → ValueError; Exception → OSError; OSError → FileNotFoundError; BaseException → KeyboardInterrupt; BaseException → SystemExit; BaseException → GeneratorExit

### s02 · check · Check: Exception hierarchy
 — Read the supplied evidence and choose the answer that matches the rule.

### s03 · hands_on · Review Exception hierarchy
 — Read the supplied excerpts in this step and decide which classifications or diagnoses are correct.

### s04 · explainer · Exception propagation through calls
(definition) When an exception is raised, the remaining operations in the current try body are skipped while Python searches for a matching handler. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(mechanism) A handler accepts its named exception class or a subclass. Python examines handlers in their written order. ⟦B.f2 B:tb3 B:tb4⟧
(mechanism) Without a matching local handler, the exception travels through callers toward an outer handler. If none matches, it remains unhandled. ⟦B.f3 B:tb3 B:tb4⟧
(mechanism) After a handler recovers, execution continues after that try/except statement. It does not restart the failed operation. ⟦B.f4 B:tb3 B:tb4 B:tb5⟧
[DIAGRAM: Exception propagation through calls] nodes=['value = quantity("three")', 'return int(text)', 'except ValueError:', 'print("Converted", value)', 'print("After recovery")'] edges=[('n1', 'n2', 'enter helper'), ('n2', 'n3', 'conversion failure propagates'), ('n3', 'n5', 'recover, then resume')] alt: Caller enters conversion; failure reaches ValueError handler. Converted-value print is skipped. Execution resumes after try/except.

### s05 · check · Check: Exception propagation through calls
 — Read the supplied evidence and choose the answer that matches the rule.

### s06 · hands_on · Recover from a conversion failure
 — Complete the supplied helper and recovery path so execution continues after the protected conversion.

### s07 · explainer · Guaranteed cleanup with finally
(definition) Put release operations in a finally: body aligned with the preceding try:. They run when execution leaves the protected operation. ⟦C.f1 C:tb2 C:tb4⟧
(mechanism) The finally body runs after normal completion, an exception, or a return from the try body. ⟦C.f2 C:tb3 C:tb4⟧
(mechanism) If finally completes normally, an unhandled exception is re-raised afterward. A return inside finally can replace a pending return or suppress a pending exception. ⟦C.f3 C:tb3 C:tb4 C:tb5⟧
[CODE python]
def read_quantity(text):
    try:
        return int(text)
    finally:
        print("Leaving conversion")

print(read_quantity("3"))
  annotations: ['Protected calculation; a pending return leaves through cleanup.', 'Aligned exit action: normal completion, return, or exception.', 'Cleanup completes before a pending return or unhandled exception proceeds.']

### s08 · check · Check: Guaranteed cleanup with finally
 — Read the supplied evidence and choose the answer that matches the rule.

### s09 · check · Check: Guaranteed cleanup with finally
 — Read the supplied evidence and choose the answer that matches the rule.

### s10 · hands_on · Keep cleanup at the exit boundary
 — Complete the supplied finally body with the requested release action while preserving the return and exception behavior.

### s11 · recap · Keep these distinctions
(takeaway) BaseException is the root; ordinary failures belong to its Exception branch. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Find the matching handler, then resume after its try/except—not at the failed operation. ⟦B.f1 B.f2 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧
(takeaway) finally runs on exit; a return there can replace a pending return or suppress an exception. ⟦C.f1 C.f2 C.f3 C:tb2 C:tb3 C:tb4 C:tb5⟧
[UP NEXT] Passing and storing functions as values: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: Exception hierarchy
(mechanism) ValueError and OSError sit under Exception. FileNotFoundError sits under OSError. ⟦A.f2 A:tb3 A:tb4⟧
(example) Contrast the ordinary Exception branch with the three signals directly under BaseException; these are not all children of Exception. ⟦A.f2 A:tb3 A:tb4⟧
### r02 · Review: Exception hierarchy
(definition) BaseException is the root of Python’s built-in exception hierarchy. Its Exception subclass covers ordinary application failures. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) KeyboardInterrupt, SystemExit and GeneratorExit sit directly under BaseException, not under Exception. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) Contrast the ordinary Exception branch with the three signals directly under BaseException; these are not all children of Exception. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · Review: Exception propagation through calls
(mechanism) A handler accepts its named exception class or a subclass. Python examines handlers in their written order. ⟦B.f2 B:tb3 B:tb4⟧
(mechanism) Without a matching local handler, the exception travels through callers toward an outer handler. If none matches, it remains unhandled. ⟦B.f3 B:tb3 B:tb4⟧
(example) In quantity("three"), recovery follows the caller’s try/except; it does not retry int(text) or the skipped converted-value print. ⟦B.f2 B.f3 B:tb3 B:tb4⟧
### r04 · Review: Exception propagation through calls
(definition) When an exception is raised, the remaining operations in the current try body are skipped while Python searches for a matching handler. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(mechanism) After a handler recovers, execution continues after that try/except statement. It does not restart the failed operation. ⟦B.f4 B:tb3 B:tb4 B:tb5⟧
(example) In quantity("three"), recovery follows the caller’s try/except; it does not retry int(text) or the skipped converted-value print. ⟦B.f1 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r05 · Review: Guaranteed cleanup with finally
(definition) Put release operations in a finally: body aligned with the preceding try:. They run when execution leaves the protected operation. ⟦C.f1 C:tb2 C:tb4⟧
(mechanism) The finally body runs after normal completion, an exception, or a return from the try body. ⟦C.f2 C:tb3 C:tb4⟧
(mechanism) If finally completes normally, an unhandled exception is re-raised afterward. A return inside finally can replace a pending return or suppress a pending exception. ⟦C.f3 C:tb3 C:tb4 C:tb5⟧
(example) In read_quantity, cleanup belongs to finally, not to a replacement return. Keep the exit action separate from the calculation’s result. ⟦C.f1 C.f2 C.f3 C:tb2 C:tb3 C:tb4 C:tb5⟧
### r06 · Review: Guaranteed cleanup with finally
(mechanism) If finally completes normally, an unhandled exception is re-raised afterward. A return inside finally can replace a pending return or suppress a pending exception. ⟦C.f3 C:tb3 C:tb4 C:tb5⟧
(example) In read_quantity, cleanup belongs to finally, not to a replacement return. Keep the exit action separate from the calculation’s result. ⟦C.f3 C:tb3 C:tb4 C:tb5⟧

=========

# EVALUATOR PACKET — Passing and storing functions as values and Closures and enclosing scope (learn_python.tile.054_055)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.functions_as_values — Passing and storing functions as values
B = python.closures_and_enclosing_scope — Closures and enclosing scope

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.functions_as_values)   objective: Pass functions as callback values.
A.f1: A function definition creates a function object bound to its name; the bare name refers to the function and name(arguments) calls it.   [sources: python_tutorial#controlflow.html#defining-functions]
A.f2: Functions can be passed where a function object is required.   [sources: python_tutorial#controlflow.html#lambda-expressions]
A.f3: A callable can be stored and invoked later.   [sources: python_tutorial#classes.html#method-objects]
A.f4: A receiving helper can call a supplied function parameter using parameter(value), rather than passing the result of an earlier call.   [sources: python_language_reference#expressions.html#calls]
note: Begin with this objective: Pass functions as callback values.
note: Keep the example in the Functions as values and closures tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.closures_and_enclosing_scope, python.pathlib_paths, python.raising_exceptions.
PRACTICE ANCHOR (live_code): Write apply(operation, value) so it applies a supplied transformation, then store double in chosen and pass chosen to the helper.  SUCCESS: chosen refers to double without calling it, and apply(chosen, 3) returns 6 by invoking operation(value) inside the helper.
ASSESSMENT ANCHOR: pass_function_instead_of_call_result facts=['f1', 'f2', 'f4']
ASSESSMENT ANCHOR: invoke_stored_callable_at_receiving_site facts=['f3', 'f4']

## SOURCE FACTS — B (python.closures_and_enclosing_scope)   objective: Capture enclosing function state in a closure.
B.f1: A nested function can resolve a free name in an enclosing function scope; each call has its own local bindings.   [sources: python_language_reference#executionmodel.html#resolution-of-names]
B.f2: A returned nested function can use enclosing values after its creating call has finished.   [sources: python_tutorial#controlflow.html#lambda-expressions]
B.f3: Declare nonlocal name in a nested function to rebind an existing name in the nearest enclosing function scope.   [sources: python_language_reference#simple_stmts.html#nonlocal]
B.f4: A stateful factory can bind state in its body and return a nested function that reads and rebinds that state with nonlocal.   [sources: python_language_reference#simple_stmts.html#nonlocal]
note: Begin with this objective: Capture enclosing function state in a closure.
note: Keep the example in the Functions as values and closures tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.pathlib_paths, python.raising_exceptions, python.reading_tracebacks.
PRACTICE ANCHOR (live_code): Write make_counter so it returns an advance function that retains and increments its own enclosing count. Create counter and other from separate factory calls.  SUCCESS: Calling counter twice returns 1 then 2; calling other once returns 1. Each returned function updates only the count belonging to its creating factory call.
ASSESSMENT ANCHOR: predict_retained_state_across_independent_counter_calls facts=['f1', 'f2', 'f4']
ASSESSMENT ANCHOR: use_nonlocal_to_rebind_existing_enclosing_state facts=['f3', 'f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Avoiding shared mutable default arguments; Binding variable arguments with *args and **kwargs; Choosing explicit text-file encodings; Choosing instance, class or static method binding; Classes and instances; Closures and enclosing scope; Constructing and resolving pathlib paths; Defining custom exceptions; Defining useful object representations with special methods; Distinguishing input failures from programming defects; Extending inherited behavior with super; Initialising instance state with __init__; Inspecting object types and attributes; Instance methods and self; Instance versus class attributes; Investigating Python execution with a debugger; Lambda expressions; Object composition; Ordering iterables with a key function; Performing filesystem operations with pathlib; Python encapsulation conventions; Raising exceptions; Reading Python tracebacks; Selecting safe file-opening modes; Selecting specific exception handlers; Serialising and deserialising data with Python json

## LESSON, in learner order

### s01 · explainer · Passing and storing functions as values
(definition) Defining a function creates a function object bound to its name. The bare name refers to that function; name(arguments) calls it. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Pass a function itself when the receiving helper requires a function object. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) You can store a callable and invoke it later. ⟦A.f3 A:tb3 A:tb4⟧
(mechanism) A helper can call its supplied function parameter with parameter(value). Passing an earlier call’s result is different from supplying the function. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
[CODE python]
def double(value):
    return value * 2

def apply(operation, value):
    return operation(value)

chosen = double
print(apply(chosen, 3))
  annotations: ['Definition binds the function object.', 'Store the callable, rather than the result of a call.', 'Invoke the supplied function through the parameter.', 'Pass the stored function and the value to the receiving helper.']

### s02 · check · Check: Passing and storing functions as values
 — Read the supplied evidence and choose the answer that matches the rule.

### s03 · check · Check: Passing and storing functions as values
 — Read the supplied evidence and choose the answer that matches the rule.

### s04 · hands_on · Pass the calculation itself
 — Complete the helper so it receives and calls the supplied function rather than an earlier call’s result.

### s05 · explainer · Closures and enclosing scope
(definition) A nested function can resolve a free name in an enclosing function scope. Each call has its own local bindings. ⟦B.f1 B:tb1 B:tb2 B:tb4 B:tb5⟧
(mechanism) A returned nested function can still use enclosing values after the call that created it has finished. ⟦B.f2 B:tb1 B:tb3 B:tb4⟧
(mechanism) Use nonlocal name to rebind an existing name in the nearest enclosing function scope. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(mechanism) A stateful factory can bind state and return a nested function that reads it and uses nonlocal to rebind it. ⟦B.f4 B:tb3 B:tb4⟧
[CODE python]
def make_counter():
    count = 0
    def advance():
        nonlocal count
        count = count + 1
        return count
    return advance

counter = make_counter()
print(counter())
print(counter())
other = make_counter()
print(other())
  annotations: ['State belongs to this factory call.', 'Rebind the existing enclosing count.', 'The returned function retains access to enclosing state.', 'First factory call: retain its own binding.', 'Separate factory call: distinct local state.', 'First counter call returns 1.', 'Second counter call returns 2.', 'The separate other counter starts at 1.']

### s06 · video · Reading and rebinding enclosing state
[VIDEO ] bridge-before:  | bridge-after: 

### s07 · check · Check: Closures and enclosing scope
 — Read the supplied evidence and choose the answer that matches the rule.

### s08 · check · Check: Closures and enclosing scope
 — Read the supplied evidence and choose the answer that matches the rule.

### s09 · hands_on · Retain separate counter state
 — Complete the factory so each returned function reads and rebinds its own enclosing state.

### s10 · recap · Keep these distinctions
(takeaway) Pass the function itself when a helper needs to call it later. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Use nonlocal for an existing enclosing binding; separate factory calls have separate local state. ⟦B.f1 B.f2 B.f3 B.f4 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Constructing and resolving pathlib paths: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: Passing and storing functions as values
(definition) Defining a function creates a function object bound to its name. The bare name refers to that function; name(arguments) calls it. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Pass a function itself when the receiving helper requires a function object. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) A helper can call its supplied function parameter with parameter(value). Passing an earlier call’s result is different from supplying the function. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(example) chosen = double stores the function. double(3) calls it now; it does not supply the function for apply to call later. ⟦A.f1 A.f2 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Review: Passing and storing functions as values
(mechanism) You can store a callable and invoke it later. ⟦A.f3 A:tb3 A:tb4⟧
(mechanism) A helper can call its supplied function parameter with parameter(value). Passing an earlier call’s result is different from supplying the function. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(example) chosen = double stores the function. double(3) calls it now; it does not supply the function for apply to call later. ⟦A.f3 A.f4 A:tb3 A:tb4 A:tb5⟧
### r03 · Review: Passing and storing functions as values
(definition) Defining a function creates a function object bound to its name. The bare name refers to that function; name(arguments) calls it. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Pass a function itself when the receiving helper requires a function object. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) You can store a callable and invoke it later. ⟦A.f3 A:tb3 A:tb4⟧
(mechanism) A helper can call its supplied function parameter with parameter(value). Passing an earlier call’s result is different from supplying the function. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(example) chosen = double stores the function. double(3) calls it now; it does not supply the function for apply to call later. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r04 · Review: Closures and enclosing scope
(definition) A nested function can resolve a free name in an enclosing function scope. Each call has its own local bindings. ⟦B.f1 B:tb1 B:tb2 B:tb4 B:tb5⟧
(mechanism) A returned nested function can still use enclosing values after the call that created it has finished. ⟦B.f2 B:tb1 B:tb3 B:tb4⟧
(mechanism) A stateful factory can bind state and return a nested function that reads it and uses nonlocal to rebind it. ⟦B.f4 B:tb3 B:tb4⟧
(example) counter and other come from separate make_counter calls. Updating counter’s enclosing count does not continue other’s state. ⟦B.f1 B.f2 B.f4 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r05 · Review: Closures and enclosing scope
(mechanism) Use nonlocal name to rebind an existing name in the nearest enclosing function scope. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(mechanism) A stateful factory can bind state and return a nested function that reads it and uses nonlocal to rebind it. ⟦B.f4 B:tb3 B:tb4⟧
(example) counter and other come from separate make_counter calls. Updating counter’s enclosing count does not continue other’s state. ⟦B.f3 B.f4 B:tb3 B:tb4 B:tb5⟧
### r06 · Review: Closures and enclosing scope
(definition) A nested function can resolve a free name in an enclosing function scope. Each call has its own local bindings. ⟦B.f1 B:tb1 B:tb2 B:tb4 B:tb5⟧
(mechanism) A returned nested function can still use enclosing values after the call that created it has finished. ⟦B.f2 B:tb1 B:tb3 B:tb4⟧
(mechanism) Use nonlocal name to rebind an existing name in the nearest enclosing function scope. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(mechanism) A stateful factory can bind state and return a nested function that reads it and uses nonlocal to rebind it. ⟦B.f4 B:tb3 B:tb4⟧
(example) counter and other come from separate make_counter calls. Updating counter’s enclosing count does not continue other’s state. ⟦B.f1 B.f2 B.f3 B.f4 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧

=========

# EVALUATOR PACKET — Constructing and resolving pathlib paths (learn_python.tile.056_056)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.pathlib_paths — Constructing and resolving pathlib paths

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.pathlib_paths)   objective: Construct and resolve filesystem paths using pathlib.
A.f1: from pathlib import Path provides concrete paths using the platform’s path conventions.   [sources: python_stdlib_reference#pathlib.html#pathlib.Path]
A.f2: base / "child" constructs a child path; an absolute right operand replaces the previous path rather than remaining underneath it.   [sources: python_stdlib_reference#pathlib.html#operators]
A.f3: Relative paths are interpreted against the current working directory; choosing an explicit base directory avoids relying on an unintended working directory.   [sources: python_stdlib_reference#pathlib.html#pathlib.Path.absolute]
note: Begin with this objective: Construct and resolve filesystem paths using pathlib.
note: Keep the example in the Working with paths tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.raising_exceptions, python.reading_tracebacks, python.debugger_usage.
note: Require linux.filesystem_navigation_and_files before this filesystem, script, module or environment unit; do not teach terminal navigation here.
PRACTICE ANCHOR (live_code): Construct output for orders.csv under a chosen absolute project directory using Path and a relative child name.  SUCCESS: output represents orders.csv beneath the chosen base, using the platform's path conventions without depending on the current working directory.
ASSESSMENT ANCHOR: construct_platform_appropriate_child_path facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_relative_child_from_absolute_replacement facts=['f2']
ASSESSMENT ANCHOR: explain_relative_path_resolution facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Avoiding shared mutable default arguments; Binding variable arguments with *args and **kwargs; Choosing explicit text-file encodings; Choosing instance, class or static method binding; Classes and instances; Defining custom exceptions; Defining useful object representations with special methods; Distinguishing input failures from programming defects; Extending inherited behavior with super; Handling file and data-format failures; Initialising instance state with __init__; Inspecting object types and attributes; Instance methods and self; Instance versus class attributes; Investigating Python execution with a debugger; Lambda expressions; Object composition; Ordering iterables with a key function; Performing filesystem operations with pathlib; Python encapsulation conventions; Raising exceptions; Reading Python tracebacks; Selecting safe file-opening modes; Selecting specific exception handlers; Serialising and deserialising data with Python json

## LESSON, in learner order

### s01 · explainer · Constructing and resolving pathlib paths
(definition) Import Path with from pathlib import Path. It provides concrete paths using the platform’s path conventions. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) base / "child" builds a child path. An absolute right operand instead replaces the previous path; it does not stay beneath that base. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Relative paths are interpreted against the current working directory. Choose an explicit base directory to avoid depending on an unintended working directory. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[DIAGRAM: Constructing and resolving pathlib paths] nodes=['Path("/work/project")', 'output = base / "orders.csv"', 'Path("/work/project") / "/tmp/orders.csv"', 'base = Path("project")', 'Current working directory'] edges=[('n1', 'n2', 'relative child appended'), ('n1', 'n3', 'absolute right operand replaces base'), ('n5', 'n4', 'relative base interpreted here')] alt: Relative child stays beneath an absolute project base. Absolute right operand replaces it. Relative project base is interpreted against the current working directory.

### s02 · check · Check: Constructing and resolving pathlib paths
 — Read the supplied evidence and choose the answer that matches the rule.

### s03 · hands_on · Construct the child path
 — Complete the path construction with a relative child beneath the supplied explicit base.

### s04 · recap · Keep these distinctions
(takeaway) Distinguish relative children, absolute replacements, and working-directory-dependent paths. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Raising exceptions: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: Constructing and resolving pathlib paths
(mechanism) Relative paths are interpreted against the current working directory. Choose an explicit base directory to avoid depending on an unintended working directory. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) A relative orders.csv is a child of base. An absolute right operand replaces base instead of staying beneath it. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Review: Constructing and resolving pathlib paths
(definition) Import Path with from pathlib import Path. It provides concrete paths using the platform’s path conventions. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) base / "child" builds a child path. An absolute right operand instead replaces the previous path; it does not stay beneath that base. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Relative paths are interpreted against the current working directory. Choose an explicit base directory to avoid depending on an unintended working directory. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) A relative orders.csv is a child of base. An absolute right operand replaces base instead of staying beneath it. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Signaling and locating a failure (learn_python.tile.057_059)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.raising_exceptions — Raising exceptions
B = python.reading_tracebacks — Reading Python tracebacks
C = python.debugger_usage — Investigating Python execution with a debugger

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.raising_exceptions)   objective: Raise a meaningful exception for an invalid operation.
A.f1: Use raise ExceptionType(message) to signal a particular failure with explanatory context.   [sources: python_tutorial#errors.html#raising-exceptions]
A.f2: ValueError indicates an argument of an appropriate type but an inappropriate value, apart from cases with a more precise exception.   [sources: python_stdlib_reference#exceptions.html#ValueError]
A.f3: Use specific exceptions to permit precise handling.   [sources: pep8_style_guide#programming-recommendations]
note: Begin with this objective: Raise a meaningful exception for an invalid operation.
note: Keep the example in the Raising and investigating failures tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.reading_tracebacks, python.debugger_usage, python.safe_mutable_defaults.
PRACTICE ANCHOR (live_code): Update cost(quantity) to reject a negative numeric quantity with ValueError and a useful message while preserving the result for nonnegative quantities.  SUCCESS: cost(-1) raises ValueError with a message explaining that quantity must be nonnegative; cost(0) returns 0 and cost(2) returns 8.
ASSESSMENT ANCHOR: choose_a_specific_exception_for_an_invalid_value facts=['f2', 'f3']
ASSESSMENT ANCHOR: raise_an_exception_with_explanatory_context facts=['f1']

## SOURCE FACTS — B (python.reading_tracebacks)   objective: Locate Python failures from tracebacks.
B.f1: The final line of an exception report gives the exception type and message.   [sources: python_tutorial#errors.html#exceptions]
B.f2: The traceback’s preceding frames give source locations and the calling context where the exception occurred.   [sources: python_tutorial#errors.html#exceptions]
B.f3: Traceback frames in a call chain lead down to the most recent failing operation; use its displayed file, line and statement to locate the immediate cause.   [sources: python_tutorial#errors.html#exceptions]
note: Begin with this objective: Locate Python failures from tracebacks.
note: Keep the example in the Raising and investigating failures tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.debugger_usage, python.safe_mutable_defaults, python.sorting_with_key_functions.
PRACTICE ANCHOR (live_code): Trace a failed conversion through two functions: an outer helper calls read_quantity(text), whose return int(text) fails for "three".  SUCCESS: Identify the exception type and message, locate the file, line and conversion statement in the innermost frame, and connect that frame to the outer helper's call.
ASSESSMENT ANCHOR: identify_exception_type_and_message facts=['f1']
ASSESSMENT ANCHOR: locate_immediate_failing_statement facts=['f3']
ASSESSMENT ANCHOR: identify_relevant_calling_frame facts=['f2', 'f3']

## SOURCE FACTS — C (python.debugger_usage)   objective: Inspect Python execution using breakpoints and stepping.
C.f1: breakpoint() enters the debugger at the call site; by default it invokes pdb.set_trace().   [sources: python_stdlib_reference#functions.html#breakpoint]
C.f2: In pdb, p expression prints an expression’s value, and l lists nearby source lines.   [sources: python_stdlib_reference#pdb.html#debugger-commands]
C.f3: n executes the next line without stepping into a called function, s steps into calls, and c continues until another breakpoint or termination.   [sources: python_stdlib_reference#pdb.html#debugger-commands]
C.f4: Use b line_number to set a breakpoint and inspect the values controlling a suspect branch when execution pauses there.   [sources: python_stdlib_reference#pdb.html#debugger-commands]
note: Begin with this objective: Inspect Python execution using breakpoints and stepping.
note: Keep the example in the Raising and investigating failures tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.safe_mutable_defaults, python.sorting_with_key_functions, python.lambda_expressions.
PRACTICE ANCHOR (live_code): Use pdb to isolate an incorrect branch in a helper by pausing execution, inspecting quantity and its comparison, and tracing which branch executes.  SUCCESS: The learner pauses before the suspect branch, inspects quantity and the branch condition, and identifies the incorrect comparison using the observed execution state.
ASSESSMENT ANCHOR: locate_debugger_entry_point facts=['f1']
ASSESSMENT ANCHOR: locate_wrong_branch_controlling_value facts=['f2', 'f4']
ASSESSMENT ANCHOR: choose_execution_control_command facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Avoiding shared mutable default arguments; Binding variable arguments with *args and **kwargs; Choosing explicit text-file encodings; Choosing instance, class or static method binding; Classes and instances; Computing dates and elapsed times with datetime; Defining custom exceptions; Defining useful object representations with special methods; Distinguishing input failures from programming defects; Extending inherited behavior with super; Handling file and data-format failures; Initialising instance state with __init__; Inspecting object types and attributes; Instance methods and self; Instance versus class attributes; Investigating Python execution with a debugger; Lambda expressions; Managing resources with with; Object composition; Ordering iterables with a key function; Performing filesystem operations with pathlib; Python encapsulation conventions; Reading Python tracebacks; Reading and writing binary files; Selecting safe file-opening modes; Selecting specific exception handlers; Serialising and deserialising data with Python json

## LESSON, in learner order

### s01 · explainer · Raising exceptions
(definition) Use raise ExceptionType(message) to signal a particular failure and give explanatory context. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) ValueError indicates an argument with an appropriate type but an inappropriate value, except where a more precise exception applies. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) Choose a specific exception so callers can handle the failure precisely. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[CODE python]
def cost(quantity):
    if quantity < 0:
        raise ValueError("quantity must be nonnegative")
    return quantity * 4

try:
    cost(-1)
except ValueError:
    print("Quantity rejected")
  annotations: ['Check the stated value requirement.', 'The negative-quantity path signals failure and does not reach the return.', 'An accepted quantity reaches the calculation.', 'Specific handling of the signaled value failure.']

### s02 · check · Check: Raising exceptions
 — Read the supplied evidence and choose the answer that matches the rule.

### s03 · check · Check: Raising exceptions
 — Read the supplied evidence and choose the answer that matches the rule.

### s04 · hands_on · Signal the value-contract failure
 — Complete the argument check with a specific exception and explanatory context.

### s05 · explainer · Reading Python tracebacks
(definition) The final line of an exception report names the exception type and gives its message. ⟦B.f1 B:tb2 B:tb4⟧
(mechanism) The preceding traceback frames show source locations and the calling context in which the exception occurred. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(mechanism) Follow the call-chain frames down to the most recent failing operation. Its displayed file, line and statement locate the immediate cause. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
[CODE python]
def read_quantity(text):
    return int(text)

def outer(text):
    return read_quantity(text)

outer("three")
  annotations: ['Immediate failing operation for the supplied numeric text; find this frame’s file and line.', 'The outer helper’s calling frame provides context, not the immediate conversion failure.', 'Follow the report down the call chain; its final line supplies the exception type and message.']
(info) ```text
Traceback (most recent call last):
  File "main.py", line 7, in <module>
    outer("three")
  File "main.py", line 5, in outer
    return read_quantity(text)
  File "main.py", line 2, in read_quantity
    return int(text)
ValueError: invalid literal for int() with base 10: 'three'
```

The final line gives ValueError and its message. The main.py line 2 frame identifies the immediate failing conversion; line 5 shows the outer helper’s call. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧

### s06 · video · From exception report to failing statement
[VIDEO ] bridge-before:  | bridge-after: 

### s07 · check · Check: Reading Python tracebacks
 — Read the supplied evidence and choose the answer that matches the rule.

### s08 · hands_on · Locate the immediate failure
 — Inspect the supplied conversion traceback and identify the failing statement and its calling context.

### s09 · explainer · Investigating Python execution with a debugger
(definition) breakpoint() enters the debugger where it is called. By default, it invokes pdb.set_trace(). ⟦C.f1 C:tb2⟧
(mechanism) In pdb, p expression prints an expression’s value. Use l to list nearby source lines. ⟦C.f2 C:tb3⟧
(mechanism) Use n for the next line without entering a called function, s to step into calls, and c to continue until another breakpoint or termination. ⟦C.f3 C:tb3⟧
(mechanism) Use b line_number to set a breakpoint. When paused there, inspect the values controlling the suspect branch. ⟦C.f4 C:tb3⟧
[DIAGRAM: Investigating Python execution with a debugger] nodes=['Numbered helper source\n1: # Intended behavior: a positive quantity returns "positive".\n2: # The comparison below is deliberately wrong. Inspect it before correcting it.\n3: def quantity_branch(quantity):\n4:     breakpoint()\n5:     if quantity < 0:\n6:         return "positive"\n7:     else:\n8:         return "not positive"\n10: quantity = 3\n11: result = quantity_branch(quantity)', 'Paused before branch\nif quantity < 0:', 'Inspect values\np quantity\n3\np quantity < 0\nFalse', 'After n\nreturn "not positive"'] edges=[('n2', 'n3', 'p inspects'), ('n3', 'n4', 'n steps')] alt: Numbered source and registered paused pdb state: inspect quantity and its comparison before stepping to the defective return branch.

### s10 · explainer · Apply the distinction: Investigating Python execution with a debugger
(example) Choose n to stay outside a called function and s to enter it. These are pdb commands, not Python source statements. ⟦C.f1 C.f2 C.f3 C.f4 C:tb4 C:tb5⟧

### s11 · video · Pause execution at a breakpoint
[VIDEO ] bridge-before:  | bridge-after: 

### s12 · check · Check: Investigating Python execution with a debugger
 — Read the supplied evidence and choose the answer that matches the rule.

### s13 · check · Check: Investigating Python execution with a debugger
 — Read the supplied evidence and choose the answer that matches the rule.

### s14 · hands_on · Review the paused branch
 — Read the supplied source and debugger excerpt and decide which command or diagnosis is correct.

### s15 · recap · Keep these distinctions
(takeaway) Signal a value-contract failure with context and a specific exception. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Read the final exception line, then locate the immediate failure in the most recent frame. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
(takeaway) Inspect paused values and choose whether to step into a call. ⟦C.f1 C.f2 C.f3 C.f4 C:tb2 C:tb3 C:tb4 C:tb5⟧
[UP NEXT] Avoiding shared mutable default arguments: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: Raising exceptions
(mechanism) ValueError indicates an argument with an appropriate type but an inappropriate value, except where a more precise exception applies. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) Choose a specific exception so callers can handle the failure precisely. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) In cost, a negative quantity violates the stated value requirement. raise signals that failure; merely displaying a message is different. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Review: Raising exceptions
(definition) Use raise ExceptionType(message) to signal a particular failure and give explanatory context. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(example) In cost, a negative quantity violates the stated value requirement. raise signals that failure; merely displaying a message is different. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
### r03 · Review: Raising exceptions
(definition) Use raise ExceptionType(message) to signal a particular failure and give explanatory context. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) ValueError indicates an argument with an appropriate type but an inappropriate value, except where a more precise exception applies. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) Choose a specific exception so callers can handle the failure precisely. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) In cost, a negative quantity violates the stated value requirement. raise signals that failure; merely displaying a message is different. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r04 · Review: Reading Python tracebacks
(mechanism) The preceding traceback frames show source locations and the calling context in which the exception occurred. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(mechanism) Follow the call-chain frames down to the most recent failing operation. Its displayed file, line and statement locate the immediate cause. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(example) The outer helper’s frame shows who requested the conversion. The int(text) frame identifies the operation that immediately failed. ⟦B.f2 B.f3 B:tb3 B:tb4 B:tb5⟧
### r05 · Review: Reading Python tracebacks
(definition) The final line of an exception report names the exception type and gives its message. ⟦B.f1 B:tb2 B:tb4⟧
(mechanism) Follow the call-chain frames down to the most recent failing operation. Its displayed file, line and statement locate the immediate cause. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(example) The outer helper’s frame shows who requested the conversion. The int(text) frame identifies the operation that immediately failed. ⟦B.f1 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r06 · Review: Investigating Python execution with a debugger
(definition) breakpoint() enters the debugger where it is called. By default, it invokes pdb.set_trace(). ⟦C.f1 C:tb2 C:tb4⟧
(mechanism) In pdb, p expression prints an expression’s value. Use l to list nearby source lines. ⟦C.f2 C:tb3 C:tb4⟧
(mechanism) Use b line_number to set a breakpoint. When paused there, inspect the values controlling the suspect branch. ⟦C.f4 C:tb3 C:tb4⟧
(example) Choose n to stay outside a called function and s to enter it. These are pdb commands, not Python source statements. ⟦C.f1 C.f2 C.f4 C:tb2 C:tb3 C:tb4⟧
### r07 · Review: Investigating Python execution with a debugger
(mechanism) Use n for the next line without entering a called function, s to step into calls, and c to continue until another breakpoint or termination. ⟦C.f3 C:tb3 C:tb4 C:tb5⟧
(example) Choose n to stay outside a called function and s to enter it. These are pdb commands, not Python source statements. ⟦C.f3 C:tb3 C:tb4 C:tb5⟧
### r08 · Review: Investigating Python execution with a debugger
(definition) breakpoint() enters the debugger where it is called. By default, it invokes pdb.set_trace(). ⟦C.f1 C:tb2 C:tb4⟧
(mechanism) In pdb, p expression prints an expression’s value. Use l to list nearby source lines. ⟦C.f2 C:tb3 C:tb4⟧
(mechanism) Use n for the next line without entering a called function, s to step into calls, and c to continue until another breakpoint or termination. ⟦C.f3 C:tb3 C:tb4 C:tb5⟧
(mechanism) Use b line_number to set a breakpoint. When paused there, inspect the values controlling the suspect branch. ⟦C.f4 C:tb3 C:tb4⟧
(example) Choose n to stay outside a called function and s to enter it. These are pdb commands, not Python source statements. ⟦C.f1 C.f2 C.f3 C.f4 C:tb2 C:tb3 C:tb4 C:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· nodes.label: Numbered helper source
1: # Intended behavior: a positive quantity returns "positive".
2: # The comparison below is deliberately wrong. Inspect it before correcting it.
3: def quantity_branch(quantity):
4:     breakpoint()
5:     if quantity < 0:
6:         return "positive"
7:     else:
8:         return "not positive"
10: quantity = 3
11: result = quantity_branch(quantity)
· nodes.label: Paused before branch
if quantity < 0:
· nodes.label: Inspect values
p quantity
3
p quantity < 0
False
· nodes.label: After n
return "not positive"

=========

# EVALUATOR PACKET — Avoiding shared mutable default arguments (learn_python.tile.060_060)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.safe_mutable_defaults — Avoiding shared mutable default arguments

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.safe_mutable_defaults)   objective: Avoid shared mutable function defaults.
A.f1: Default argument values are evaluated once at definition time, so a mutable default can retain modifications across calls.   [sources: python_tutorial#controlflow.html#default-argument-values]
A.f2: Use a None default and an if parameter is None: branch that creates a new list or dictionary in the function body to obtain fresh per-call state.   [sources: python_tutorial#controlflow.html#default-argument-values]
note: Begin with this objective: Avoid shared mutable function defaults.
note: Keep the example in the Safe mutable defaults tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.sorting_with_key_functions, python.lambda_expressions, python.specific_exception_handlers.
PRACTICE ANCHOR (live_code): Repair add_label so calls that omit labels create separate lists instead of accumulating earlier labels.  SUCCESS: Calling add_label("blue") and then add_label("red") returns ["blue"] and ["red"], respectively. A caller-supplied labels list is still updated and returned.
ASSESSMENT ANCHOR: predict_mutable_default_reuse facts=['f1']
ASSESSMENT ANCHOR: replace_mutable_default_with_per_call_object facts=['f2']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Binding variable arguments with *args and **kwargs; Choosing explicit text-file encodings; Choosing instance, class or static method binding; Classes and instances; Computing dates and elapsed times with datetime; Creating local modules; Defining custom exceptions; Defining useful object representations with special methods; Distinguishing input failures from programming defects; Extending inherited behavior with super; Handling file and data-format failures; Initialising instance state with __init__; Inspecting object types and attributes; Instance methods and self; Instance versus class attributes; Lambda expressions; Managing resources with with; Object composition; Ordering iterables with a key function; Performing filesystem operations with pathlib; Python encapsulation conventions; Reading and writing binary files; Selecting safe file-opening modes; Selecting specific exception handlers; Serialising and deserialising data with Python json

## LESSON, in learner order

### s01 · explainer · Avoiding shared mutable default arguments
(definition) Default values are evaluated once, when the function is defined. A mutable default can therefore retain modifications across calls. ⟦A.f1 A:tb1 A:tb2 A:tb4 A:tb5⟧
(mechanism) For fresh per-call state, use a None default and create a new list or dictionary inside an if parameter is None: branch in the function body. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
[SIDE_BY_SIDE] Create omitted-list storage during the call, not as a mutable default. left_label: Shared mutable default | right_label: Fresh omitted-list state
  left:
[CODE python]
def add_label(label, labels=[]):
    labels.append(label)
    return labels

print(add_label("blue"))
print(add_label("red"))
  annotations: ['Default list is evaluated once at definition time.', "First call prints ['blue'].", "Second call prints ['blue', 'red']."]
  right:
[CODE python]
def add_label(label, labels=None):
    if labels is None:
        labels = []
    labels.append(label)
    return labels

print(add_label("blue"))
print(add_label("red"))
  annotations: ['Distinguish an omitted list from supplied storage.', 'Create fresh storage in the function body.', "First call prints ['blue'].", "Second call prints ['red']."]

### s02 · video · Shared defaults and fresh per-call lists
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Check: Avoiding shared mutable default arguments
 — Read the supplied evidence and choose the answer that matches the rule.

### s04 · check · Check: Avoiding shared mutable default arguments
 — Read the supplied evidence and choose the answer that matches the rule.

### s05 · hands_on · Repair the shared default
 — Complete the helper so omitted-list calls create fresh storage while supplied lists are still used.

### s06 · recap · Keep these distinctions
(takeaway) Defaults are evaluated once; a None guard can create fresh per-call storage. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Ordering iterables with a key function: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: Avoiding shared mutable default arguments
(definition) Default values are evaluated once, when the function is defined. A mutable default can therefore retain modifications across calls. ⟦A.f1 A:tb1 A:tb2 A:tb4 A:tb5⟧
(example) labels=[] is evaluated at definition time. labels=None with the None guard creates fresh storage during an omitted-list call. ⟦A.f1 A:tb1 A:tb2 A:tb4 A:tb5⟧
### r02 · Review: Avoiding shared mutable default arguments
(mechanism) For fresh per-call state, use a None default and create a new list or dictionary inside an if parameter is None: branch in the function body. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(example) labels=[] is evaluated at definition time. labels=None with the None guard creates fresh storage during an omitted-list call. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
### r03 · Review: Avoiding shared mutable default arguments
(definition) Default values are evaluated once, when the function is defined. A mutable default can therefore retain modifications across calls. ⟦A.f1 A:tb1 A:tb2 A:tb4 A:tb5⟧
(mechanism) For fresh per-call state, use a None default and create a new list or dictionary inside an if parameter is None: branch in the function body. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(example) labels=[] is evaluated at definition time. labels=None with the None guard creates fresh storage during an omitted-list call. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Ordering iterables with a key function and Lambda expressions (learn_python.tile.061_062)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.sorting_with_key_functions — Ordering iterables with a key function
B = python.lambda_expressions — Lambda expressions

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.sorting_with_key_functions)   objective: Order iterable values using a key function.
A.f1: sorted(records, key=function) returns a new sorted list and uses function(record) as each record’s comparison key.   [sources: python_stdlib_reference#functions.html#sorted]
A.f2: sorted does not mutate the original list; reverse=True reverses the ordering.   [sources: python_stdlib_reference#functions.html#sorted]
A.f3: Sorting is stable: items with equal keys retain their original relative order.   [sources: python_stdlib_reference#functions.html#sorted]
A.f4: str.lower can provide a lowercase text key for case-normalized ordering.   [sources: python_stdlib_reference#stdtypes.html#str.lower]
note: Begin with this objective: Order iterable values using a key function.
note: Keep the example in the Sorting callbacks and lambdas tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.lambda_expressions, python.specific_exception_handlers, python.validation_vs_programming_errors.
PRACTICE ANCHOR (live_code): Sort order records by their lowercase label using a named key function, without changing the original list.  SUCCESS: A new list contains the records in lowercase-label order; records with equal lowercase labels retain their relative order, and the original list remains unchanged.
ASSESSMENT ANCHOR: sort_records_by_a_derived_key facts=['f1', 'f4']
ASSESSMENT ANCHOR: determine_relative_order_of_equal_key_records facts=['f3']
ASSESSMENT ANCHOR: distinguish_original_list_from_sorted_result_and_reverse_ordering facts=['f2']

## SOURCE FACTS — B (python.lambda_expressions)   objective: Write a small anonymous callable using lambda.
B.f1: lambda parameters: expression creates an anonymous function whose result is the single expression’s value.   [sources: python_tutorial#controlflow.html#lambda-expressions]
B.f2: A lambda is restricted to one expression and can be passed as key=lambda item: expression to sorting.   [sources: python_tutorial#controlflow.html#lambda-expressions]
note: Begin with this objective: Write a small anonymous callable using lambda.
note: Keep the example in the Sorting callbacks and lambdas tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.specific_exception_handlers, python.validation_vs_programming_errors, python.variadic_arguments_and_unpacking.
PRACTICE ANCHOR (live_code): Provide a lambda as the sorting key to order pairs by their quantity.  SUCCESS: ordered contains [("red", 2), ("blue", 3)], using a lambda that accepts one pair and returns its quantity.
ASSESSMENT ANCHOR: express_single_expression_transformation_with_correct_parameters facts=['f1', 'f2']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Binding variable arguments with *args and **kwargs; Choosing explicit text-file encodings; Choosing instance, class or static method binding; Classes and instances; Computing dates and elapsed times with datetime; Creating local modules; Defining custom exceptions; Defining useful object representations with special methods; Distinguishing input failures from programming defects; Extending inherited behavior with super; Handling file and data-format failures; Initialising instance state with __init__; Inspecting object types and attributes; Instance methods and self; Instance versus class attributes; Lambda expressions; Managing resources with with; Object composition; Organising importable packages; Performing filesystem operations with pathlib; Python encapsulation conventions; Reading and writing binary files; Recording program events with logging; Selecting safe file-opening modes; Selecting specific exception handlers; Serialising and deserialising data with Python json

## LESSON, in learner order

### s01 · explainer · Ordering iterables with a key function
(definition) sorted(records, key=function) creates a new sorted list. Each function(record) result supplies that record’s comparison key. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) sorted leaves the original list unchanged. Use reverse=True to reverse the ordering. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Sorting is stable: records with equal keys keep their original relative order. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(mechanism) For case-normalized text ordering, str.lower can supply a lowercase comparison key. ⟦A.f4 A:tb3 A:tb4⟧
[CODE python]
records = [{"label": "blue", "quantity": 3}, {"label": "Red", "quantity": 2}, {"label": "BLUE", "quantity": 3}]

def label_key(record):
    return record["label"].lower()

ordered = sorted(records, key=label_key)
print([record["label"] for record in ordered])
print([record["label"] for record in records])
  annotations: ["The comparison keys are 'blue', 'red', and 'blue'.", 'Create a new list; blue and BLUE have equal keys and retain their original relative order.', "The sorted labels are ['blue', 'BLUE', 'Red'].", "The original labels remain ['blue', 'Red', 'BLUE']."]

### s02 · video · Ordering by a calculated comparison key
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Check: Ordering iterables with a key function
 — Read the supplied evidence and choose the answer that matches the rule.

### s04 · hands_on · Order records by their key
 — Complete the supplied sorting task using a key function without changing the original list.

### s05 · explainer · Lambda expressions
(definition) lambda parameters: expression creates an anonymous function. Its result is the value of that single expression. ⟦B.f1 B:tb1 B:tb2 B:tb4⟧
(mechanism) A lambda contains just one expression. You can pass it to sorting as key=lambda item: expression. ⟦B.f2 B:tb1 B:tb3 B:tb4 B:tb5⟧
[CODE python]
pairs = [("blue", 3), ("red", 2)]
ordered = sorted(pairs, key=lambda pair: pair[1])
print(ordered)
  annotations: ['The anonymous key function returns the second item’s value; its body is one expression.']

### s06 · check · Check: Lambda expressions
 — Read the supplied evidence and choose the answer that matches the rule.

### s07 · hands_on · Supply a one-expression key
 — Complete the sorting key with a lambda that returns the required comparison value.

### s08 · recap · Keep these distinctions
(takeaway) sorted creates a new list using comparison keys; equal keys retain relative order. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) A lambda is an anonymous function with one expression. ⟦B.f1 B.f2 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Selecting specific exception handlers: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: Ordering iterables with a key function
(mechanism) sorted leaves the original list unchanged. Use reverse=True to reverse the ordering. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(example) The quantity key is a comparison value, not a rearranged record. Equal-key blue and green retain their relative order. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
### r02 · Review: Ordering iterables with a key function
(definition) sorted(records, key=function) creates a new sorted list. Each function(record) result supplies that record’s comparison key. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Sorting is stable: records with equal keys keep their original relative order. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(mechanism) For case-normalized text ordering, str.lower can supply a lowercase comparison key. ⟦A.f4 A:tb3 A:tb4⟧
(example) The quantity key is a comparison value, not a rearranged record. Equal-key blue and green retain their relative order. ⟦A.f1 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · Review: Lambda expressions
(definition) lambda parameters: expression creates an anonymous function. Its result is the value of that single expression. ⟦B.f1 B:tb1 B:tb2 B:tb4⟧
(mechanism) A lambda contains just one expression. You can pass it to sorting as key=lambda item: expression. ⟦B.f2 B:tb1 B:tb3 B:tb4 B:tb5⟧
(example) lambda pair: pair[1] supplies a pair’s comparison key. It is one expression, not a loop or statement body. ⟦B.f1 B.f2 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧

=========

# EVALUATOR PACKET — Selecting specific exception handlers and Distinguishing input failures from programming defects (learn_python.tile.063_064)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.specific_exception_handlers — Selecting specific exception handlers
B = python.validation_vs_programming_errors — Distinguishing input failures from programming defects

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.specific_exception_handlers)   objective: Select and order specific Python exception handlers.
A.f1: An except handler matches its named exception class and subclasses; the first matching handler runs.   [sources: python_tutorial#errors.html#handling-exceptions]
A.f2: Order subclass-specific handlers before broader parent handlers so the specific recovery remains reachable.   [sources: python_tutorial#errors.html#handling-exceptions]
A.f3: FileNotFoundError is a subclass of OSError, so except FileNotFoundError: must precede except OSError: when their recovery actions differ.   [sources: python_stdlib_reference#exceptions.html#exception-hierarchy]
note: Begin with this objective: Select and order specific Python exception handlers.
note: Keep the example in the Specific handling and validation boundaries tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.validation_vs_programming_errors, python.variadic_arguments_and_unpacking, python.classes_and_instances.
PRACTICE ANCHOR (live_code): Repair handler ordering so FileNotFoundError is handled before the broader OSError branch without changing either recovery action.  SUCCESS: A deliberately raised FileNotFoundError reaches the specific handler and displays File missing rather than Other file operation failure.
ASSESSMENT ANCHOR: predict_first_matching_handler_for_subclass_exception facts=['f1', 'f3']
ASSESSMENT ANCHOR: order_handlers_to_preserve_specific_recovery facts=['f2', 'f3']

## SOURCE FACTS — B (python.validation_vs_programming_errors)   objective: Diagnose whether a Python failure comes from invalid input, an implementation defect or an external operational problem.
B.f1: ValueError can identify an unsuitable value such as malformed numeric input; reject or request correction of an input that violates the stated value contract.   [sources: python_stdlib_reference#exceptions.html#ValueError]
B.f2: NameError means a local or global name cannot be found; a misspelled implementation name calls for code correction rather than rejection of the supplied input.   [sources: python_stdlib_reference#exceptions.html#NameError]
B.f3: PermissionError reports inadequate access rights for a filesystem operation; report the access failure rather than assuming the supplied path or implementation is inherently wrong.   [sources: python_stdlib_reference#exceptions.html#PermissionError]
note: Begin with this objective: Diagnose whether a Python failure comes from invalid input, an implementation defect or an external operational problem.
note: Keep the example in the Specific handling and validation boundaries tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.variadic_arguments_and_unpacking, python.classes_and_instances, python.file_modes.
PRACTICE ANCHOR (live_code): Assign diagnostic categories and appropriate responses to three supplied failure reports: malformed numeric input, a NameError caused by a misspelled local quantity name, and a PermissionError opening an otherwise valid input path.  SUCCESS: The completed Python assignments classify malformed numeric input as an input failure requiring correction, the misspelled name as an implementation defect requiring code correction, and inadequate access rights as an external operational failure requiring an access-failure report.
ASSESSMENT ANCHOR: choose_input_rejection_for_value_contract_violation facts=['f1']
ASSESSMENT ANCHOR: choose_implementation_correction_for_misspelled_name facts=['f2']
ASSESSMENT ANCHOR: identify_access_failure_without_blaming_path_or_implementation facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Binding variable arguments with *args and **kwargs; Choosing explicit text-file encodings; Choosing instance, class or static method binding; Classes and instances; Computing dates and elapsed times with datetime; Creating local modules; Defining custom exceptions; Defining useful object representations with special methods; Distinguishing input failures from programming defects; Extending inherited behavior with super; Guarding a program entry point; Handling file and data-format failures; Initialising instance state with __init__; Inspecting object types and attributes; Instance methods and self; Instance versus class attributes; Managing resources with with; Object composition; Organising importable packages; Parsing command-line arguments with argparse; Performing filesystem operations with pathlib; Python encapsulation conventions; Reading and writing binary files; Recording program events with logging; Selecting safe file-opening modes; Serialising and deserialising data with Python json

## LESSON, in learner order

### s01 · explainer · Selecting specific exception handlers
(definition) An except handler matches its named exception class and subclasses. The first matching handler runs. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Put subclass-specific handlers before broader parent handlers so the specific recovery remains reachable. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) FileNotFoundError is an OSError subclass. When recovery actions differ, except FileNotFoundError: must come before except OSError:. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[CODE python]
try:
    with open("missing-example.txt", "r") as source:
        print(source.read())
except FileNotFoundError:
    print("File missing")
except OSError:
    print("Other file operation failure")
  annotations: ['Specific subclass recovery comes first.', 'Broader parent recovery comes later; first match wins.']

### s02 · video · Keep specific recovery branches reachable
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Check: Selecting specific exception handlers
 — Read the supplied evidence and choose the answer that matches the rule.

### s04 · hands_on · Keep specific recovery reachable
 — Complete the supplied handlers with the subclass-specific recovery before its broader parent.

### s05 · explainer · Distinguishing input failures from programming defects
(definition) ValueError can identify unsuitable input, such as malformed numeric text. Reject or request correction of input that violates the stated value contract. ⟦B.f1 B:tb2 B:tb4⟧
(mechanism) NameError means a local or global name cannot be found. Correct a misspelled implementation name rather than rejecting the supplied input. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(mechanism) PermissionError reports inadequate access rights for a filesystem operation. Report the access failure; do not assume the path or implementation is inherently wrong. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
[SIDE_BY_SIDE] Choose the response from the reported cause, not an assumption that every failure is bad input. left_label: Input value failure | right_label: Implementation or access failure
  left:
[DIAGRAM: Distinguishing input failures from programming defects] nodes=['ValueError from int("three")', 'Request corrected numeric input'] edges=[('n1', 'n2', 'unsuitable value')] alt: ValueError from int("three") → Request corrected numeric input
  right:
[DIAGRAM: Distinguishing input failures from programming defects] nodes=['NameError: misspelled quantity name', 'Correct implementation name', 'PermissionError: inadequate access rights', 'Report access failure'] edges=[('n1', 'n2', 'missing implementation name'), ('n3', 'n4', 'access problem')] alt: Two independent diagnostic mappings: NameError caused by a misspelled quantity name → correct the implementation name; PermissionError caused by inadequate access rights → report the access failure.

### s06 · check · Check: Distinguishing input failures from programming defects
 — Read the supplied evidence and choose the answer that matches the rule.

### s07 · hands_on · Review the failure reports
 — Read the supplied reports and decide which diagnostic category and response fits each cause.

### s08 · recap · Keep these distinctions
(takeaway) The first matching handler runs; place a specific subclass before its broader parent. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Separate input correction, implementation correction, and access-failure reporting. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Binding variable arguments with *args and **kwargs: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: Selecting specific exception handlers
(definition) An except handler matches its named exception class and subclasses. The first matching handler runs. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) FileNotFoundError is an OSError subclass. When recovery actions differ, except FileNotFoundError: must come before except OSError:. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) For a missing file, an earlier OSError handler matches before FileNotFoundError. Put the specific handler first when recoveries differ. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Review: Selecting specific exception handlers
(mechanism) Put subclass-specific handlers before broader parent handlers so the specific recovery remains reachable. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) FileNotFoundError is an OSError subclass. When recovery actions differ, except FileNotFoundError: must come before except OSError:. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(example) For a missing file, an earlier OSError handler matches before FileNotFoundError. Put the specific handler first when recoveries differ. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
### r03 · Review: Distinguishing input failures from programming defects
(definition) ValueError can identify unsuitable input, such as malformed numeric text. Reject or request correction of input that violates the stated value contract. ⟦B.f1 B:tb2 B:tb4⟧
(example) Malformed numeric text calls for input correction; a misspelled quantity name calls for code correction. Inadequate access rights need an access-failure report. ⟦B.f1 B:tb2 B:tb4⟧
### r04 · Review: Distinguishing input failures from programming defects
(mechanism) NameError means a local or global name cannot be found. Correct a misspelled implementation name rather than rejecting the supplied input. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(mechanism) PermissionError reports inadequate access rights for a filesystem operation. Report the access failure; do not assume the path or implementation is inherently wrong. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(example) Malformed numeric text calls for input correction; a misspelled quantity name calls for code correction. Inadequate access rights need an access-failure report. ⟦B.f2 B.f3 B:tb3 B:tb4 B:tb5⟧

=========

# EVALUATOR PACKET — Binding variable arguments with *args and **kwargs (learn_python.tile.065_065)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.variadic_arguments_and_unpacking — Binding variable arguments with *args and **kwargs

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.variadic_arguments_and_unpacking)   objective: Bind variable arguments using *args and **kwargs.
A.f1: In a function definition, *args collects remaining positional arguments into a tuple.   [sources: python_tutorial#controlflow.html#arbitrary-argument-lists]
A.f2: In a function definition, **kwargs collects additional keyword arguments into a dictionary; a parameter may not receive two values in a call.   [sources: python_tutorial#controlflow.html#keyword-arguments]
A.f3: In a call, *args expands a sequence into positional arguments and **kwargs expands a dictionary into keyword arguments.   [sources: python_tutorial#controlflow.html#unpacking-argument-lists]
A.f4: A forwarding wrapper can define def wrapper(*args, **kwargs): and return target(*args, **kwargs), avoiding additional arguments that duplicate a supplied binding.   [sources: python_tutorial#controlflow.html#unpacking-argument-lists]
note: Begin with this objective: Bind variable arguments using *args and **kwargs.
note: Keep the example in the Variable arguments and unpacking tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.classes_and_instances, python.file_modes, python.instance_initialization.
PRACTICE ANCHOR (live_code): Write wrapper(*args, **kwargs) to forward the caller's arguments to target and return its result without adding duplicate bindings.  SUCCESS: The wrapper returns 15 for wrapper(3, price=5), 15 for wrapper(3, 5), and 12 for wrapper(3), preserving both supplied arguments and the target's default.
ASSESSMENT ANCHOR: identify_collected_positional_and_keyword_arguments facts=['f1', 'f2']
ASSESSMENT ANCHOR: expand_sequences_and_dictionaries_into_call_arguments facts=['f3']
ASSESSMENT ANCHOR: forward_arguments_without_duplicate_bindings facts=['f2', 'f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Choosing explicit text-file encodings; Choosing instance, class or static method binding; Classes and instances; Computing dates and elapsed times with datetime; Creating local modules; Defining custom exceptions; Defining useful object representations with special methods; Diagnosing module search-path problems; Extending inherited behavior with super; Guarding a program entry point; Handling file and data-format failures; Initialising instance state with __init__; Inspecting object types and attributes; Instance methods and self; Instance versus class attributes; Managing resources with with; Object composition; Organising importable packages; Parsing command-line arguments with argparse; Performing filesystem operations with pathlib; Python encapsulation conventions; Reading and writing binary files; Recording program events with logging; Selecting safe file-opening modes; Serialising and deserialising data with Python json

## LESSON, in learner order

### s01 · explainer · Binding variable arguments with *args and **kwargs
(definition) In a definition, *args collects remaining positional arguments into a tuple. ⟦A.f1 A:tb2⟧
(mechanism) In a definition, **kwargs collects additional keyword arguments into a dictionary. A call cannot give one parameter two values. ⟦A.f2 A:tb3⟧
(mechanism) In a call, *args expands a sequence into positional arguments; **kwargs expands a dictionary into keyword arguments. ⟦A.f3 A:tb3⟧
(mechanism) A forwarding wrapper can define wrapper(*args, **kwargs) and return target(*args, **kwargs). Do not add arguments that duplicate a supplied binding. ⟦A.f4 A:tb3⟧
[CODE python]
def target(quantity, price=4):
    return quantity * price

def wrapper(*args, **kwargs):
    return target(*args, **kwargs)

print(wrapper(3, price=5))
  annotations: ['Collect positional arguments and additional keyword arguments.', 'Expand both collections at the target call; do not duplicate a parameter.', 'The supplied positional quantity and keyword price reach the target.']

### s02 · explainer · Apply the distinction: Binding variable arguments with *args and **kwargs
(example) For wrapper(3, price=5), args is (3,) and kwargs is {'price': 5}. target(*args, **kwargs) binds quantity to 3 and price to 5. Adding price=4 to that target call would supply price twice. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · video · Collecting arguments and expanding them at a call
[VIDEO ] bridge-before:  | bridge-after: 

### s04 · check · Check: Binding variable arguments with *args and **kwargs
 — Read the supplied evidence and choose the answer that matches the rule.

### s05 · check · Check: Binding variable arguments with *args and **kwargs
 — Read the supplied evidence and choose the answer that matches the rule.

### s06 · hands_on · Forward the caller’s arguments
 — Complete the wrapper so it expands both collected argument groups without duplicate bindings.

### s07 · recap · Keep these distinctions
(takeaway) Collect arguments in definitions, expand them in calls, and avoid duplicate bindings. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Classes and instances: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review: Binding variable arguments with *args and **kwargs
(definition) In a definition, *args collects remaining positional arguments into a tuple. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) In a definition, **kwargs collects additional keyword arguments into a dictionary. A call cannot give one parameter two values. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(example) The wrapper collects arguments in its definition and expands them at the target call. Adding another price can duplicate the caller’s binding. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Review: Binding variable arguments with *args and **kwargs
(mechanism) In a call, *args expands a sequence into positional arguments; **kwargs expands a dictionary into keyword arguments. ⟦A.f3 A:tb3 A:tb4⟧
(example) The wrapper collects arguments in its definition and expands them at the target call. Adding another price can duplicate the caller’s binding. ⟦A.f3 A:tb3 A:tb4⟧
### r03 · Review: Binding variable arguments with *args and **kwargs
(mechanism) In a definition, **kwargs collects additional keyword arguments into a dictionary. A call cannot give one parameter two values. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) A forwarding wrapper can define wrapper(*args, **kwargs) and return target(*args, **kwargs). Do not add arguments that duplicate a supplied binding. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(example) The wrapper collects arguments in its definition and expands them at the target call. Adding another price can duplicate the caller’s binding. ⟦A.f2 A.f4 A:tb3 A:tb4 A:tb5⟧