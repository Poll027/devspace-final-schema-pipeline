# EVALUATOR PACKET — Exception flow and cleanup (learn_python.tile.051_053)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.exception_hierarchy — Exception hierarchy
B = python.exception_propagation — Exception propagation through calls
C = python.finally_cleanup — Guaranteed cleanup with finally

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=5
  warn: remediation step learn_python.tile.051_053.r02 is never referenced
  warn: remediation step learn_python.tile.051_053.r04 is never referenced
  warn: remediation step learn_python.tile.051_053.r06 is never referenced
  warn: learn_python.tile.051_053.s06/ix.learn_python.tile.051_053.s06: ADVISORY — syntax descriptors with no detector: ['assert', 'class', 'except Exception:', 'except*', 'finally:', 'raise', 'with', 'yield']
  warn: learn_python.tile.051_053.s10/ix.learn_python.tile.051_053.s10: ADVISORY — syntax descriptors with no detector: ['**kwargs', '*args', 'assert', 'class', 'finally:', 'function calls', 'indented blocks', 'integer literals', 'raise', 'string literals', 'with', 'yield', 'yield from']

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
QUESTION [choice, intro, grading=client] Which is the direct parent of FileNotFoundError?
  ✔ o1: OSError
      why: Correct. The stated rule applies here.
  ✘ o2: ValueError
      why: ValueError is a separate subclass of Exception, not the parent of FileNotFoundError.
  ✘ o3: BaseException
      why: BaseException is the root; FileNotFoundError is directly beneath OSError.
  feedback✔: Correct. Your answer follows the rule taught in the text.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']  remediation→r01
  MEASURES: A:identify_parent_subclass_relationships(f2)   anchors=[]
  taught-before-tested: A.f2←s01

### s03 · hands_on · Review Exception hierarchy
 — Read the supplied excerpts in this step and decide which classifications or diagnoses are correct.
QUESTION [classify, stretch, grading=client] Classify each exception class by its direct parent in the built-in hierarchy. Include the ordinary failure branch and the direct BaseException signal; do not substitute the root for a nearer parent.
  'ValueError' -> Exception
      feedback: ValueError is directly beneath Exception.
  'OSError' -> Exception
      feedback: OSError is directly beneath Exception.
  'FileNotFoundError' -> OSError
      feedback: FileNotFoundError is directly beneath OSError.
  'KeyboardInterrupt' -> BaseException
      feedback: KeyboardInterrupt is directly beneath BaseException.
  'Exception' -> BaseException
      feedback: Exception is directly beneath BaseException.
  feedback✔: Correct. ValueError and OSError are matched to Exception, FileNotFoundError to OSError, and KeyboardInterrupt to BaseException.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']
  MEASURES: A:identify_baseexception_root_and_exception_branch(f1); A:distinguish_direct_baseexception_signals_from_exception_subclasses(f3)   anchors=['practice']
  taught-before-tested: A.f1←s01; A.f3←s01

### s04 · explainer · Exception propagation through calls
(definition) When an exception is raised, the remaining operations in the current try body are skipped while Python searches for a matching handler. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(mechanism) A handler accepts its named exception class or a subclass. Python examines handlers in their written order. ⟦B.f2 B:tb3 B:tb4⟧
(mechanism) Without a matching local handler, the exception travels through callers toward an outer handler. If none matches, it remains unhandled. ⟦B.f3 B:tb3 B:tb4⟧
(mechanism) After a handler recovers, execution continues after that try/except statement. It does not restart the failed operation. ⟦B.f4 B:tb3 B:tb4 B:tb5⟧
[DIAGRAM: Exception propagation through calls] nodes=['value = quantity("three")', 'return int(text)', 'except ValueError:', 'print("Converted", value)', 'print("After recovery")'] edges=[('n1', 'n2', 'enter helper'), ('n2', 'n3', 'conversion failure propagates'), ('n3', 'n5', 'recover, then resume')] alt: Caller enters conversion; failure reaches ValueError handler. Converted-value print is skipped. Execution resumes after try/except.

### s05 · check · Check: Exception propagation through calls
 — Read the supplied evidence and choose the answer that matches the rule.
QUESTION [choice, core, grading=client] A helper has no local handler and raises ValueError. Its caller has except Exception first and except ValueError second. Which handler runs?
  ✘ o1: No handler; the failure is inside a helper.
      why: An exception without a matching local handler propagates to callers.
  ✔ o2: The caller's Exception handler.
      why: Correct. The stated rule applies here.
  ✘ o3: The caller's ValueError handler.
      why: Exception matches its subclasses; the first matching handler runs even if a later one is more specific.
  feedback✔: Correct. Your answer follows the rule taught in the text.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']  remediation→r03
  MEASURES: B:identify_first_matching_handler_in_call_chain(f2,f3)   anchors=[]
  taught-before-tested: B.f2←s04; B.f3←s04

### s06 · hands_on · Recover from a conversion failure
 — Complete the supplied helper and recovery path so execution continues after the protected conversion.
QUESTION [code_exercise, stretch, grading=client] Predict the conversion failure, skipped output and resumption point, then run the supplied demonstration unchanged. Before running the supplied conversion example, record predictions: set predicted_failure to the supplied description of the failure point, predicted_skip to the skipped statement description, and predicted_resume to the resumption description. Select from failure_site, skipped_site, and resume_site. Keep the demonstration unchanged, then run it to confirm Invalid quantity followed by After recovery, with no Converted output.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['def quantity(text):', 'return int(text)', 'quantity("three")', 'value = quantity("three")', 'try:', 'except ValueError:', 'except Exception:', 'print("Converted", value)', 'print("Invalid quantity")', 'print("After recovery")'] blocked=8 items
  file main.py [editable]:
failure_site = "int(text)"
skipped_site = "print(\"Converted\", value)"
resume_site = "after try/except"
predicted_failure = ""
predicted_skip = ""
predicted_resume = ""
# Supplied candidate implementations; inspect but do not edit this block.
if True:
    def quantity(text):
        return int(text)


try:
    value = quantity("three")
    print("Converted", value)
except ValueError:
    print("Invalid quantity")
print("After recovery")

  SOLUTION main.py:
failure_site = "int(text)"
skipped_site = "print(\"Converted\", value)"
resume_site = "after try/except"
predicted_failure = failure_site
predicted_skip = skipped_site
predicted_resume = resume_site
# Supplied candidate implementations; inspect but do not edit this block.
if True:
    def quantity(text):
        return int(text)


try:
    value = quantity("three")
    print("Converted", value)
except ValueError:
    print("Invalid quantity")
print("After recovery")

  test t1 (value_equals, visible=True): {"expr":"[predicted_failure, predicted_skip, predicted_resume]","expected":["int(text)","print(\"Converted\", value)","after try/except"]} | on-fail: Check the requested result and preserve the supplied inputs and scaffolding.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"6fe856f42181b584e8ef8d316f1c09aca8de4607ecbd19b32d649d418d5aeacc","tests_passed":1}
  feedback✔: Correct. Correctly predict and confirm that quantity("three") fails during conversion, the converted-value output is skipped, and the caller displays Invalid quantity followed by After recovery.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']
  MEASURES: B:identify_skipped_operations_and_resumption_point(f1,f4)   anchors=['practice']
  taught-before-tested: B.f1←s04; B.f4←s04

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
QUESTION [choice, core, grading=client] An aligned finally body only closes a supplied file and completes normally. What happens when try completes normally, returns a value, or raises an unhandled exception?
  ✘ o1: Cleanup runs only when an exception occurs.
      why: finally also runs on normal completion and return.
  ✘ o2: Cleanup runs in all cases and always suppresses the exception.
      why: A normally completing finally does not suppress an unhandled exception.
  ✔ o3: Cleanup runs in all three cases; the return remains a return and the unhandled exception propagates afterward.
      why: Correct. The stated rule applies here.
  feedback✔: Correct. Your answer follows the rule taught in the text.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']  remediation→r05
  MEASURES: C:predict_cleanup_on_normal_completion_exception_and_return(f1,f2); C:predict_exception_propagation_after_cleanup(f3)   anchors=[]
  taught-before-tested: C.f1←s07; C.f2←s07; C.f3←s07

### s09 · check · Check: Guaranteed cleanup with finally
 — Read the supplied evidence and choose the answer that matches the rule.
QUESTION [choice, core, grading=client] A try body has a pending return of 3, but its finally body returns 0. Which result leaves the function?
  ✘ o1: Both values are returned.
      why: The finally return replaces rather than combines with the pending return.
  ✔ o2: 0, because the finally return replaces the pending return.
      why: Correct. The stated rule applies here.
  ✘ o3: 3, because the first return always wins.
      why: A return from finally can replace a pending return.
  feedback✔: Correct. Your answer follows the rule taught in the text.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']
  MEASURES: C:identify_finally_return_overriding_pending_exit(f3)   anchors=[]
  taught-before-tested: C.f3←s07

### s10 · hands_on · Keep cleanup at the exit boundary
 — Complete the supplied finally body with the requested release action while preserving the return and exception behavior.
QUESTION [code_exercise, stretch, grading=client] Choose the cleanup action that closes the supplied file after successful or failed conversion without replacing its return or exception. Change only cleanup_action; keep the function and probes unchanged.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['def read_quantity(text):', 'try:', 'finally:', 'return', 'int(...)', 'text.read()', 'text.close()', 'function calls', 'indented blocks', 'integer literals', 'string literals'] blocked=10 items
  file main.py [editable]:
valid_number = 3
invalid_text = 'three'
release_action = "close"
no_release_action = "leave open"
cleanup_action = no_release_action
# Supplied function; keep it unchanged.
if True:
    def read_quantity(text):
        try:
            return int(text.read())
        finally:
            if cleanup_action == release_action:
                text.close()
import io
good = io.StringIO(str(valid_number))
bad = io.StringIO(invalid_text)
good_result = read_quantity(good)
try:
    read_quantity(bad)
    failure = 'no failure'
except ValueError as exc:
    failure = type(exc).__name__

  SOLUTION main.py:
valid_number = 3
invalid_text = 'three'
release_action = "close"
no_release_action = "leave open"
cleanup_action = release_action
# Supplied function; keep it unchanged.
if True:
    def read_quantity(text):
        try:
            return int(text.read())
        finally:
            if cleanup_action == release_action:
                text.close()
import io
good = io.StringIO(str(valid_number))
bad = io.StringIO(invalid_text)
good_result = read_quantity(good)
try:
    read_quantity(bad)
    failure = 'no failure'
except ValueError as exc:
    failure = type(exc).__name__

  test t1 (value_equals, visible=True): {"expr":"[good_result, good.closed, bad.closed, failure]","expected":[3,true,true,"ValueError"]} | on-fail: Check the requested result and preserve the supplied inputs and scaffolding.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"8daa1e617c4ce8b56ae9320d5c7ed04574c88295c06b4e152f7cf3fb98f2dd5d","tests_passed":1}
  feedback✔: Correct. The supplied file is closed whether conversion returns an integer or fails. Successful conversion retains its return value, and failed conversion retains its unhandled exception.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']
  MEASURES: C:predict_cleanup_on_normal_completion_exception_and_return(f1,f2); C:predict_exception_propagation_after_cleanup(f3); C:identify_finally_return_overriding_pending_exit(f3)   anchors=['practice']
  taught-before-tested: C.f1←s07; C.f2←s07; C.f3←s07; C.f3←s07

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

## OTHER CONTENT (fields without a dedicated renderer)
· ops.value: print("Converted", value)_x
· expected.value: print("Converted", value)_x

=========

# EVALUATOR PACKET — Passing and storing functions as values and Closures and enclosing scope (learn_python.tile.054_055)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.functions_as_values — Passing and storing functions as values
B = python.closures_and_enclosing_scope — Closures and enclosing scope

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=6
  warn: remediation step learn_python.tile.054_055.r02 is never referenced
  warn: remediation step learn_python.tile.054_055.r03 is never referenced
  warn: remediation step learn_python.tile.054_055.r05 is never referenced
  warn: remediation step learn_python.tile.054_055.r06 is never referenced
  warn: learn_python.tile.054_055.s04/ix.learn_python.tile.054_055.s04: ADVISORY — syntax descriptors with no detector: ['**kwargs', '*args', 'assert statements', 'bare function names', 'class statements', 'integer literals', 'lambda expressions', 'name = expression', 'nested function definitions', 'nonlocal statements', 'return expression', 'value * 2', 'yield expressions']
  warn: learn_python.tile.054_055.s09/ix.learn_python.tile.054_055.s09: ADVISORY — syntax descriptors with no detector: ['**kwargs parameters', '*args parameters', 'addition with +', 'assert statements', 'assigning returned functions to variables', 'class statements', 'def statements', 'function calls', 'indented function bodies', 'integer literals', 'lambda expressions', 'nested function definitions', 'nonlocal declarations', 'raise statements', 'return statements', 'with statements', 'yield expressions']

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
QUESTION [choice, intro, grading=client] double is a function. apply(operation, value) calls operation(value). Which call passes double itself to transform 3?
  ✔ o1: apply(double, 3)
      why: Correct. The stated rule applies here.
  ✘ o2: apply(double(3), 3)
      why: double(3) invokes double first and passes its result, not the function object.
  ✘ o3: apply("double", 3)
      why: A quoted name is text, not the function bound to the bare name double.
  feedback✔: Correct. Your answer follows the rule taught in the text.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']  remediation→r01
  MEASURES: A:pass_function_instead_of_call_result(f1,f2,f4)   anchors=[]
  taught-before-tested: A.f1←s01; A.f2←s01; A.f4←s01

### s03 · check · Check: Passing and storing functions as values
 — Read the supplied evidence and choose the answer that matches the rule.
QUESTION [choice, core, grading=client] chosen stores double. In def apply(operation, value), which return invokes the supplied callable on value?
  ✘ o1: return operation
      why: The bare parameter refers to the callable but does not invoke it.
  ✘ o2: return double(value)
      why: Calling double directly ignores the supplied operation; the receiving helper must invoke its parameter.
  ✔ o3: return operation(value)
      why: Correct. The stated rule applies here.
  feedback✔: Correct. Your answer follows the rule taught in the text.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']
  MEASURES: A:invoke_stored_callable_at_receiving_site(f3,f4)   anchors=[]
  taught-before-tested: A.f3←s01; A.f4←s01

### s04 · hands_on · Pass the calculation itself
 — Complete the helper so it receives and calls the supplied function rather than an earlier call’s result.
QUESTION [code_exercise, stretch, grading=client] Choose the helper that invokes its supplied operation, then store the transformation without calling it. Assign apply to invoke_operation or return_operation so apply calls the supplied operation on value and returns its result. Assign chosen to double without calling it. Keep all supplied implementations and input_value unchanged; the checker invokes apply with both double and increment.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['def name(parameters):', 'return expression', 'name = expression', 'bare function names', 'function(arguments)', 'parameter(value)', 'integer literals', 'value * 2', 'print(expression)'] blocked=12 items
  file main.py [editable]:
input_value = 3
# Supplied transformations; leave unchanged.
if True:
    def double(value):
        return value * 2
    
    def increment(value):
        return value + 1

# Supplied implementations: inspect, but leave this block unchanged.
if True:
    def invoke_operation(operation, value):
        return operation(value)

    def return_operation(operation, value):
        return operation

apply = return_operation

chosen = None

  SOLUTION main.py:
input_value = 3
# Supplied transformations; leave unchanged.
if True:
    def double(value):
        return value * 2
    
    def increment(value):
        return value + 1

# Supplied implementations: inspect, but leave this block unchanged.
if True:
    def invoke_operation(operation, value):
        return operation(value)

    def return_operation(operation, value):
        return operation

apply = invoke_operation

chosen = double

  test t1 (value_equals, visible=True): {"expr":"[chosen is double, apply(chosen, input_value), apply(increment, input_value)]","expected":[true,6,4]} | on-fail: Check the requested result and preserve the supplied inputs and scaffolding.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"3175fe98f218b9810cb6dc8e99a98fc7a8ec9dd6c7e04c8b65af934fe2f07966","tests_passed":1}
  feedback✔: Correct. chosen refers to double without calling it, and apply(chosen, 3) returns 6 by invoking operation(value) inside the helper.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']
  MEASURES: A:pass_function_instead_of_call_result(f1,f2,f4); A:invoke_stored_callable_at_receiving_site(f3,f4)   anchors=['practice']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f4←s01; A.f3←s01; A.f4←s01

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
[VIDEO Reading and rebinding enclosing state] bridge-before: Watch how reading an enclosing name differs from assigning to it. Compare the inner and outer values before and after the nonlocal declaration. | bridge-after: The clip demonstrates enclosing-name access and rebinding, but not independent factory calls or retained state after return. The text covers those behaviors with a counter factory.
  - 27S2qRdH2rM 0-168s facts=['f3'] label: Read an enclosing binding and update it with nonlocal | summary: An outer function binds a variable to 10 and calls an inner function that reads that enclosing value. Adding an ordinary assignment inside the inner function creates a local binding instead: the inner function reports 20, while the outer function still reports 10. Declaring the name nonlocal before assigning redirects the update to the existing enclosing binding, so both functions report 20.

### s07 · check · Check: Closures and enclosing scope
 — Read the supplied evidence and choose the answer that matches the rule.
QUESTION [choice, core, grading=client] counter and other come from separate make_counter() calls. Each factory starts count at 0; its returned advance uses nonlocal count to increment and return it. Which state description is correct?
  ✔ o1: counter retains its own count across calls; other retains a separate count.
      why: Correct. The stated rule applies here.
  ✘ o2: Both returned functions update one shared count.
      why: Each factory call has its own local bindings.
  ✘ o3: Each advance call starts count at 0 again.
      why: The returned function retains its enclosing state after the factory returns.
  feedback✔: Correct. Your answer follows the rule taught in the text.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']  remediation→r04
  MEASURES: B:predict_retained_state_across_independent_counter_calls(f1,f2,f4)   anchors=[]
  taught-before-tested: B.f1←s05; B.f2←s05; B.f4←s05

### s08 · check · Check: Closures and enclosing scope
 — Read the supplied evidence and choose the answer that matches the rule.
QUESTION [choice, core, grading=client] advance is nested inside make_counter, which already binds count. Which declaration lets advance rebind that existing enclosing count?
  ✘ o1: global count
      why: nonlocal targets an existing enclosing function binding, not a global binding.
  ✘ o2: No declaration; assigning count automatically rebinds the enclosing variable.
      why: Rebinding that existing enclosing name requires nonlocal in the nested function.
  ✔ o3: nonlocal count
      why: Correct. The stated rule applies here.
  feedback✔: Correct. Your answer follows the rule taught in the text.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']
  MEASURES: B:use_nonlocal_to_rebind_existing_enclosing_state(f3,f4)   anchors=[]
  taught-before-tested: B.f3←s05; B.f4←s05

### s09 · hands_on · Retain separate counter state
 — Complete the factory so each returned function reads and rebinds its own enclosing state.
QUESTION [code_exercise, stretch, grading=client] Choose the independently created closure so counter and other retain separate state. Change only the final counter assignment so counter uses the independent closure rather than sharing other. The checker calls counter twice and other once; their results must be 1, 2, and 1.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['def statements', 'nested function definitions', 'indented function bodies', 'variable assignment', 'integer literals', 'addition with +', 'nonlocal declarations', 'return statements', 'function calls', 'assigning returned functions to variables', 'print()'] blocked=8 items
  file main.py [editable]:
initial_count = 0
if True:

    def make_counter():
        count = initial_count

        def advance():
            nonlocal count
            count = count + 1
            return count
        return advance
independent_counter = make_counter()
other = make_counter()
counter = other

  SOLUTION main.py:
initial_count = 0
if True:

    def make_counter():
        count = initial_count

        def advance():
            nonlocal count
            count = count + 1
            return count
        return advance
independent_counter = make_counter()
other = make_counter()
counter = independent_counter

  test t1 (value_equals, visible=True): {"expr":"[counter(), counter(), other()]","expected":[1,2,1]} | on-fail: Check the requested result and preserve the supplied inputs and scaffolding.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"b730be6f4ab4687086b17a6e8606860b801e39b05be0593a1f76f9c03f708d69","tests_passed":1}
  feedback✔: Correct. Calling counter twice returns 1 then 2; calling other once returns 1. Each returned function updates only the count belonging to its creating factory call.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']
  MEASURES: B:predict_retained_state_across_independent_counter_calls(f1,f2,f4); B:use_nonlocal_to_rebind_existing_enclosing_state(f3,f4)   anchors=['practice']
  taught-before-tested: B.f1←s05; B.f2←s05; B.f4←s05; B.f3←s05; B.f4←s05

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

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: sorted(..., key=...)

=========

# EVALUATOR PACKET — Constructing and resolving pathlib paths (learn_python.tile.056_056)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.pathlib_paths — Constructing and resolving pathlib paths

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=3
  warn: remediation step learn_python.tile.056_056.r02 is never referenced
  warn: learn_python.tile.056_056.s03/ix.learn_python.tile.056_056.s03: ADVISORY — syntax descriptors with no detector: ['assert', 'class', 'raise', 'string literals', 'with', 'yield']
  warn: plan: learn_python.tile.056_056.s03 was planned to measure python.pathlib_paths#assessment:distinguish_relative_child_from_absolute_replacement but its interaction does not

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
QUESTION [choice, intro, grading=client] On this Unix platform, what location interprets Path('orders.csv'), and what does Path('/work/project') / '/tmp/orders.csv' represent?
  ✔ o1: The current working directory; /tmp/orders.csv replaces the base.
      why: Correct. Relative paths use the current working directory, and an absolute right operand replaces the base.
  ✘ o2: The script directory; /tmp/orders.csv replaces the base
      why: A relative path uses the current working directory, which need not be the script directory.
  ✘ o3: The current working directory; /work/project/tmp/orders.csv.
      why: An absolute right operand replaces the base; it is not appended beneath the base.
  feedback✔: Correct. Your answer follows the rule taught in the text.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']  remediation→r01
  MEASURES: A:explain_relative_path_resolution(f3); A:distinguish_relative_child_from_absolute_replacement(f2)   anchors=[]
  taught-before-tested: A.f3←s01; A.f2←s01

### s03 · hands_on · Construct the child path
 — Complete the path construction with a relative child beneath the supplied explicit base.
QUESTION [code_exercise, stretch, grading=client] Select the constructed child path beneath the supplied absolute base. Change only the output assignment so output represents orders.csv beneath base, rather than the directory itself. Leave the import, construction and print unchanged.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['from pathlib import Path', 'Path("...")', 'variable assignment', 'string literals', 'base / "orders.csv"', 'print(output)'] blocked=13 items
  file main.py [editable]:
from pathlib import Path
base_directory = '/work/project'
base = Path(base_directory)
orders_path = base / 'orders.csv'
output = base
print(output)

  SOLUTION main.py:
from pathlib import Path
base_directory = '/work/project'
base = Path(base_directory)
orders_path = base / 'orders.csv'
output = orders_path
print(output)

  test t1 (value_equals, visible=True): {"expr":"str(output)","expected":"/work/project/orders.csv"} | on-fail: Check the requested result and preserve the supplied inputs and scaffolding.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"6eb24a073111b4d5641ecb3aa8cf1b405af9c72c7fb69f415dd2b21849e7bc13","tests_passed":1}
  feedback✔: Correct. output represents orders.csv beneath the chosen base, using the platform's path conventions without depending on the current working directory.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']
  MEASURES: A:construct_platform_appropriate_child_path(f1,f2); A:explain_relative_path_resolution(f3)   anchors=['practice']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

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

## OTHER CONTENT (fields without a dedicated renderer)
· expected.value: /work/project_x/orders.csv

=========

# EVALUATOR PACKET — Signaling and locating a failure (learn_python.tile.057_059)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.raising_exceptions — Raising exceptions
B = python.reading_tracebacks — Reading Python tracebacks
C = python.debugger_usage — Investigating Python execution with a debugger

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=8
  warn: remediation step learn_python.tile.057_059.r02 is never referenced
  warn: remediation step learn_python.tile.057_059.r03 is never referenced
  warn: remediation step learn_python.tile.057_059.r05 is never referenced
  warn: remediation step learn_python.tile.057_059.r07 is never referenced
  warn: remediation step learn_python.tile.057_059.r08 is never referenced
  warn: learn_python.tile.057_059.s04/ix.learn_python.tile.057_059.s04: ADVISORY — syntax descriptors with no detector: ['**kwargs', '*args', '@classmethod', '@staticmethod', 'assert', 'class', 'if quantity < 0:', 'indented blocks', 'integer literals', 'return quantity * 4', 'string literals', 'with', 'yield', 'yield from']
  warn: learn_python.tile.057_059.s08/ix.learn_python.tile.057_059.s08: ADVISORY — syntax descriptors with no detector: ['**kwargs', '*args', 'assert', 'class', 'name = expression', 'return expression', 'string literals', 'with', 'yield']
  warn: learn_python.tile.057_059.s14/ix.learn_python.tile.057_059.s14: ADVISORY — syntax descriptors with no detector: ['**kwargs parameter declarations', '*args parameter declarations', 'assert statements', 'b line_number (pdb command)', 'c (pdb command)', 'def with a named parameter', 'function calls', 'generator expressions', 'if/else', 'integer literals', 'l (pdb command)', 'lambda expressions', 'n (pdb command)', 'numeric comparison operators', 'p expression (pdb command)', 's (pdb command)', 'string literals', 'with statements', 'yield', 'yield from']

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
QUESTION [choice, intro, grading=client] cost receives a numeric quantity of -1 where the contract requires a nonnegative number. Which exception best communicates the invalid value?
  ✔ o1: ValueError
      why: Correct. The stated rule applies here.
  ✘ o2: OSError
      why: The evidence concerns an inappropriate numeric value, not a file-operation failure.
  ✘ o3: FileNotFoundError
      why: No missing file is involved; this is an unsuitable argument value.
  feedback✔: Correct. Your answer follows the rule taught in the text.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']  remediation→r01
  MEASURES: A:choose_a_specific_exception_for_an_invalid_value(f2,f3)   anchors=[]
  taught-before-tested: A.f2←s01; A.f3←s01

### s03 · check · Check: Raising exceptions
 — Read the supplied evidence and choose the answer that matches the rule.
QUESTION [choice, core, grading=client] Which statement signals a failure with explanatory context instead of merely displaying text?
  ✘ o1: print("quantity must be nonnegative")
      why: Printing a message does not raise the exception.
  ✘ o2: ValueError("quantity must be nonnegative")
      why: Constructing the exception without raise does not signal it.
  ✔ o3: raise ValueError("quantity must be nonnegative")
      why: Correct. The stated rule applies here.
  feedback✔: Correct. Your answer follows the rule taught in the text.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']
  MEASURES: A:raise_an_exception_with_explanatory_context(f1)   anchors=[]
  taught-before-tested: A.f1←s01

### s04 · hands_on · Signal the value-contract failure
 — Complete the argument check with a specific exception and explanatory context.
QUESTION [code_exercise, stretch, grading=client] Choose the implementation that rejects negative quantities with a specific exception and explanatory message. Set cost to the function that raises ValueError with the nonnegative-quantity message for a negative quantity and preserves the results for zero and positive quantities. Change only the cost assignment; leave the implementations and probes unchanged.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['def cost(quantity):', 'if quantity < 0:', 'raise ValueError("quantity must be nonnegative")', 'return quantity * 4', 'cost(-1)', 'cost(0)', 'cost(2)', 'integer literals', 'string literals', 'indented blocks'] blocked=10 items
  file main.py [editable]:
negative_quantity = -1
zero_quantity = 0
positive_quantity = 2
if True:

    def guarded_cost(quantity):
        if quantity < 0:
            raise ValueError('quantity must be nonnegative')
        return quantity * 4

    def unguarded_cost(quantity):
        return quantity * 4
cost = unguarded_cost
try:
    cost(negative_quantity)
    negative_result = 'no failure'
except ValueError as exc:
    negative_result = [type(exc).__name__, str(exc)]
zero_result = cost(zero_quantity)
positive_result = cost(positive_quantity)

  SOLUTION main.py:
negative_quantity = -1
zero_quantity = 0
positive_quantity = 2
if True:

    def guarded_cost(quantity):
        if quantity < 0:
            raise ValueError('quantity must be nonnegative')
        return quantity * 4

    def unguarded_cost(quantity):
        return quantity * 4
cost = guarded_cost
try:
    cost(negative_quantity)
    negative_result = 'no failure'
except ValueError as exc:
    negative_result = [type(exc).__name__, str(exc)]
zero_result = cost(zero_quantity)
positive_result = cost(positive_quantity)

  test t1 (value_equals, visible=True): {"expr":"[negative_result, zero_result, positive_result]","expected":[["ValueError","quantity must be nonnegative"],0,8]} | on-fail: Check the requested result and preserve the supplied inputs and scaffolding.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"823870432d2ba56aba024d78b4da723a682d68a203194074d174bffa2d3f8bb6","tests_passed":1}
  feedback✔: Correct. cost(-1) raises ValueError with a message explaining that quantity must be nonnegative; cost(0) returns 0 and cost(2) returns 8.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']
  MEASURES: A:choose_a_specific_exception_for_an_invalid_value(f2,f3); A:raise_an_exception_with_explanatory_context(f1)   anchors=['practice']
  taught-before-tested: A.f2←s01; A.f3←s01; A.f1←s01

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
[VIDEO From exception report to failing statement] bridge-before: Watch how the final exception line and the source frames answer different questions. The clip calls these entries “stack frames”; Devspace uses “traceback frames” for entries in the report. | bridge-after: The clip distinguishes the immediate failure from its callers. Use the text’s conversion example to connect the exception message, failing statement and calling context without assuming the caller itself failed.
  - Qmj5UQRkL4s 25-131s facts=['f1', 'f2', 'f3'] label: Read the exception, locate the failing frame, then trace its callers | summary: Begin with the final line of the traceback: it names the exception type and gives an explanatory message, which may need careful interpretation. The frame immediately above it identifies the location of the failure through a file name, line number, function name and source statement. In this example, that location is line four of count.py, inside count_to. The preceding frames record the surrounding function calls. The deepest frame identifies where the exception occurred; frames farther outward provide calling context. The immediate failing operation is not necessarily the place that needs changing, so inspect the callers too.

### s07 · check · Check: Reading Python tracebacks
 — Read the supplied evidence and choose the answer that matches the rule.
QUESTION [choice, core, grading=client] Read this traceback excerpt:
```text
File "main.py", line 5, in outer
    return read_quantity(text)
File "main.py", line 2, in read_quantity
    return int(text)
ValueError: invalid literal for int() with base 10: 'three'
```
Which statement connects the caller to the immediate failure?
  ✔ o1: outer calls read_quantity(text); int(text) in read_quantity is the immediate failing operation.
      why: Correct. The stated rule applies here.
  ✘ o2: outer performs int(text) at line 5.
      why: The caller frame displays read_quantity(text); the innermost frame displays int(text).
  ✘ o3: The first displayed frame is necessarily the immediate failing operation.
      why: The call-chain frames lead down to the most recent failing operation; here it is in read_quantity.
  feedback✔: Correct. Your answer follows the rule taught in the text.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']  remediation→r04
  MEASURES: B:identify_relevant_calling_frame(f2,f3)   anchors=[]
  taught-before-tested: B.f2←s05; B.f3←s05

### s08 · hands_on · Locate the immediate failure
 — Inspect the supplied conversion traceback and identify the failing statement and its calling context.
QUESTION [code_exercise, stretch, grading=client] Run the supplied traceback capture and inspect the displayed two-function source. Fill the report assignments using the supplied evidence variables: record exception_type, exception_message, failing_file, failing_line, failing_function, calling_function, and calling_line. Locate return int(text) as the immediate cause in read_quantity and connect it to outer's return read_quantity(text). Use evidence variables, not hard-coded output text; keep the capture unchanged.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['def function_name(text):', 'return expression', 'function_name(argument)', 'name = expression', 'int(text)', 'string literals'] blocked=8 items
  file main.py [editable]:
# Instructor traceback capture; do not edit.
import traceback
raw_text = "three"
source_file = "quantity_example.py"
source_code = 'def read_quantity(text):\n    return int(text)\n\ndef outer(text):\n    return read_quantity(text)\n\nouter(raw_text)\n'
scope = {"raw_text": raw_text}
try:
    exec(compile(source_code, source_file, "exec"), scope)
except ValueError as exc:
    observed_type = type(exc).__name__
    observed_message = str(exc)
    frames = traceback.extract_tb(exc.__traceback__)
    inner_file = frames[-1].filename
    inner_line = frames[-1].lineno
    inner_function = frames[-1].name
    caller_function = frames[-2].name
    caller_line = frames[-2].lineno
    rendered_traceback = "".join(traceback.format_exception(exc))
print(rendered_traceback)
print(source_code)
exception_type = ""
exception_message = ""
failing_file = ""
failing_line = 0
failing_function = ""
calling_function = ""
calling_line = 0

  SOLUTION main.py:
# Instructor traceback capture; do not edit.
import traceback
raw_text = "three"
source_file = "quantity_example.py"
source_code = 'def read_quantity(text):\n    return int(text)\n\ndef outer(text):\n    return read_quantity(text)\n\nouter(raw_text)\n'
scope = {"raw_text": raw_text}
try:
    exec(compile(source_code, source_file, "exec"), scope)
except ValueError as exc:
    observed_type = type(exc).__name__
    observed_message = str(exc)
    frames = traceback.extract_tb(exc.__traceback__)
    inner_file = frames[-1].filename
    inner_line = frames[-1].lineno
    inner_function = frames[-1].name
    caller_function = frames[-2].name
    caller_line = frames[-2].lineno
    rendered_traceback = "".join(traceback.format_exception(exc))
print(rendered_traceback)
print(source_code)
exception_type = observed_type
exception_message = observed_message
failing_file = inner_file
failing_line = inner_line
failing_function = inner_function
calling_function = caller_function
calling_line = caller_line

  test t1 (value_equals, visible=True): {"expr":"[exception_type, exception_message, failing_file, failing_line, failing_function, calling_function, calling_line]","expected":["ValueError","invalid literal for int() with base 10: 'three'","quantity_example.py",2,"read_quantity","outer",5]} | on-fail: Check the requested result and preserve the supplied inputs and scaffolding.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"bc4326f2abc9d4d48d670c3af9069c7d53bbea56d78fa2a43c5f914206ec36fd","tests_passed":1}
  feedback✔: Correct. Identify the exception type and message, locate the file, line and conversion statement in the innermost frame, and connect that frame to the outer helper's call.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']
  MEASURES: B:identify_exception_type_and_message(f1); B:locate_immediate_failing_statement(f3)   anchors=['practice']
  taught-before-tested: B.f1←s05; B.f3←s05

### s09 · explainer · Investigating Python execution with a debugger
(definition) breakpoint() enters the debugger where it is called. By default, it invokes pdb.set_trace(). ⟦C.f1 C:tb2⟧
(mechanism) In pdb, p expression prints an expression’s value. Use l to list nearby source lines. ⟦C.f2 C:tb3⟧
(mechanism) Use n for the next line without entering a called function, s to step into calls, and c to continue until another breakpoint or termination. ⟦C.f3 C:tb3⟧
(mechanism) Use b line_number to set a breakpoint. When paused there, inspect the values controlling the suspect branch. ⟦C.f4 C:tb3⟧
[DIAGRAM: Investigating Python execution with a debugger] nodes=['Numbered helper source\n1: # Intended behavior: a positive quantity returns "positive".\n2: # The comparison below is deliberately wrong. Inspect it before correcting it.\n3: def quantity_branch(quantity):\n4:     breakpoint()\n5:     if quantity < 0:\n6:         return "positive"\n7:     else:\n8:         return "not positive"\n10: quantity = 3\n11: result = quantity_branch(quantity)', 'Paused before branch\nif quantity < 0:', 'Inspect values\np quantity\n3\np quantity < 0\nFalse', 'After n\nreturn "not positive"'] edges=[('n2', 'n3', 'p inspects'), ('n3', 'n4', 'n steps')] alt: Numbered source and registered paused pdb state: inspect quantity and its comparison before stepping to the defective return branch.

### s10 · explainer · Apply the distinction: Investigating Python execution with a debugger
(example) Choose n to stay outside a called function and s to enter it. These are pdb commands, not Python source statements. ⟦C.f1 C.f2 C.f3 C.f4 C:tb4 C:tb5⟧

### s11 · video · Pause execution at a breakpoint
[VIDEO Pause execution at a breakpoint] bridge-before: Watch where breakpoint() is placed inside a function. For the older debugger call, use the spelling pdb.set_trace() shown in Devspace’s text. | bridge-after: The clip explains entering the debugger, but not inspection commands, stepping, or setting a breakpoint by line number. Devspace’s text covers those commands and inspecting branch-controlling values.
  - 0LPuG825eAk 82-172s facts=['f1'] label: Place breakpoint() before a suspected problem | summary: A breakpoint marks a place where execution pauses so you can investigate the program. The presenter places one inside a function and explains the older approach of importing pdb and calling pdb.set_trace(). Python 3.7 introduced breakpoint() as a shorter built-in call that invokes the same pdb behavior by default.

### s12 · check · Check: Investigating Python execution with a debugger
 — Read the supplied evidence and choose the answer that matches the rule.
QUESTION [choice, core, grading=client] breakpoint() is immediately before a suspect if quantity < 0 branch. Execution pauses with quantity = 3. Which sequence locates the source and inspects the controlling value and condition?
  ✘ o1: Only b 5; no inspection is needed.
      why: b sets a breakpoint at a line; it does not inspect quantity or the branch condition.
  ✔ o2: l, then p quantity, then p quantity < 0
      why: Correct. The stated rule applies here.
  ✘ o3: c, then c again
      why: c continues execution rather than displaying source or the controlling expressions.
  feedback✔: Correct. Your answer follows the rule taught in the text.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']  remediation→r06
  MEASURES: C:locate_debugger_entry_point(f1); C:locate_wrong_branch_controlling_value(f2,f4)   anchors=[]
  taught-before-tested: C.f1←s09; C.f2←s09; C.f4←s09

### s13 · check · Check: Investigating Python execution with a debugger
 — Read the supplied evidence and choose the answer that matches the rule.
QUESTION [choice, core, grading=client] At a pdb pause before a helper call, you want to execute the next line without stepping into the called helper. Which command fits?
  ✔ o1: n
      why: Correct. The stated rule applies here.
  ✘ o2: s
      why: s steps into calls; the task explicitly asks not to step into the helper.
  ✘ o3: c
      why: c continues until another breakpoint or termination, not just the next line.
  feedback✔: Correct. Your answer follows the rule taught in the text.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']
  MEASURES: C:choose_execution_control_command(f3)   anchors=[]
  taught-before-tested: C.f3←s09

### s14 · hands_on · Review the paused branch
 — Read the supplied source and debugger excerpt and decide which command or diagnosis is correct.
QUESTION [code_exercise, stretch, grading=client] Inspect the supplied recorded pdb session. It pauses immediately after breakpoint(), before line 5; l lists the branch, p inspects quantity and quantity < 0, b 5 sets the branch breakpoint, n traces the wrong branch, and c resumes. Bind each command variable to the corresponding supplied command string. Then bind quantity_branch to the candidate whose comparison meets the intended behavior: positive quantities return "positive", all others "not positive". This browser task records the diagnosis from a supplied session, not interactive pdb input. Keep quantity and all supplied candidates unchanged. Also assign inspected_quantity to the supplied controlling quantity; the checker includes that inspected value in the diagnostic report.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['def with a named parameter', 'return', 'if/else', 'variable assignment', 'integer literals', 'string literals', 'numeric comparison operators', 'function calls', 'breakpoint()', 'p expression (pdb command)', 'l (pdb command)', 'n (pdb command)', 's (pdb command)', 'c (pdb command)', 'b line_number (pdb command)'] blocked=9 items
  file main.py [editable]:
# Supplied recorded pdb session (interactive stdin is unavailable).
# > /home/azureuser/roles/learn_python/final_runs/learn_python.region.03/batches/final_batch_learn_python.region.03/working/debugger_source.py(5)quantity_branch()
# -> if quantity < 0:
# (Pdb) l
#   1  	# Intended behavior: a positive quantity returns "positive".
#   2  	# The comparison below is deliberately wrong. Inspect it before correcting it.
#   3  	def quantity_branch(quantity):
#   4  	    breakpoint()
#   5  ->	    if quantity < 0:
#   6  	        return "positive"
#   7  	    else:
#   8  	        return "not positive"
#   9  	
#  10  	quantity = 3
#  11  	result = quantity_branch(quantity)
# (Pdb) p quantity
# 3
# (Pdb) p quantity < 0
# False
# (Pdb) b 5
# Breakpoint 1 at /home/azureuser/roles/learn_python/final_runs/learn_python.region.03/batches/final_batch_learn_python.region.03/working/debugger_source.py:5
# (Pdb) n
# > /home/azureuser/roles/learn_python/final_runs/learn_python.region.03/batches/final_batch_learn_python.region.03/working/debugger_source.py(8)quantity_branch()
# -> return "not positive"
# (Pdb) c

quantity = 3
# Supplied candidate implementations; inspect but do not edit this block.
if True:
    list_cmd = "l"
    value_cmd = "p quantity"
    condition_cmd = "p quantity < 0"
    branch_cmd = "b 5"
    next_cmd = "n"
    continue_cmd = "c"
    
    def greater_branch(quantity):
        if quantity > 0:
            return "positive"
        else:
            return "not positive"
    
    def lesser_branch(quantity):
        if quantity < 0:
            return "positive"
        else:
            return "not positive"

source_command = None
value_command = None
condition_command = None
break_command = None
next_command = None
continue_command = None
quantity_branch = None

inspected_quantity = None

  SOLUTION main.py:
# Supplied recorded pdb session (interactive stdin is unavailable).
# > /home/azureuser/roles/learn_python/final_runs/learn_python.region.03/batches/final_batch_learn_python.region.03/working/debugger_source.py(5)quantity_branch()
# -> if quantity < 0:
# (Pdb) l
#   1  	# Intended behavior: a positive quantity returns "positive".
#   2  	# The comparison below is deliberately wrong. Inspect it before correcting it.
#   3  	def quantity_branch(quantity):
#   4  	    breakpoint()
#   5  ->	    if quantity < 0:
#   6  	        return "positive"
#   7  	    else:
#   8  	        return "not positive"
#   9  	
#  10  	quantity = 3
#  11  	result = quantity_branch(quantity)
# (Pdb) p quantity
# 3
# (Pdb) p quantity < 0
# False
# (Pdb) b 5
# Breakpoint 1 at /home/azureuser/roles/learn_python/final_runs/learn_python.region.03/batches/final_batch_learn_python.region.03/working/debugger_source.py:5
# (Pdb) n
# > /home/azureuser/roles/learn_python/final_runs/learn_python.region.03/batches/final_batch_learn_python.region.03/working/debugger_source.py(8)quantity_branch()
# -> return "not positive"
# (Pdb) c

quantity = 3
# Supplied candidate implementations; inspect but do not edit this block.
if True:
    list_cmd = "l"
    value_cmd = "p quantity"
    condition_cmd = "p quantity < 0"
    branch_cmd = "b 5"
    next_cmd = "n"
    continue_cmd = "c"
    
    def greater_branch(quantity):
        if quantity > 0:
            return "positive"
        else:
            return "not positive"
    
    def lesser_branch(quantity):
        if quantity < 0:
            return "positive"
        else:
            return "not positive"

source_command = list_cmd
value_command = value_cmd
condition_command = condition_cmd
break_command = branch_cmd
next_command = next_cmd
continue_command = continue_cmd
quantity_branch = greater_branch

inspected_quantity = quantity

  test t1 (value_equals, visible=True): {"expr":"[source_command, value_command, condition_command, break_command, next_command, continue_command, quantity_branch(quantity), quantity_branch(-quantity), inspected_quantity]","expected":["l","p quantity","p quantity < 0","b 5","n","c","positive","not positive",3]} | on-fail: Check the requested result and preserve the supplied inputs and scaffolding.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"bd22913b83b6c29309692afa10f1bb2b2e01c1aa6cc4a0cb0c45d387e9cb11a3","tests_passed":1}
  feedback✔: Correct. The learner pauses before the suspect branch, inspects quantity and the branch condition, and identifies the incorrect comparison using the observed execution state.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']
  MEASURES: C:locate_debugger_entry_point(f1); C:locate_wrong_branch_controlling_value(f2,f4); C:choose_execution_control_command(f3)   anchors=['practice']
  taught-before-tested: C.f1←s09; C.f2←s09; C.f4←s09; C.f3←s09

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
· expected.value: invalid literal for int() with base 10: 'three_x'
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

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=3
  warn: remediation step learn_python.tile.060_060.r02 is never referenced
  warn: remediation step learn_python.tile.060_060.r03 is never referenced
  warn: learn_python.tile.060_060.s05/ix.learn_python.tile.060_060.s05: ADVISORY — syntax descriptors with no detector: ['*args and **kwargs parameter declarations', 'None', 'argument unpacking with * or **', 'assert statements', 'def with named parameters and default arguments', 'function calls with positional or keyword arguments', 'generator expressions', 'if labels is None:', 'indented function and conditional bodies', 'lambda expressions', 'list literals', 'string literals', 'with statements', 'yield']

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
[VIDEO Shared defaults and fresh per-call lists] bridge-before: Watch how calls that omit the employee list reuse its contents. Then follow the repair: a None default and an identity check move list creation into the function body. | bridge-after: The clip explains both default reuse and the None guard, but stops before executing the repair. The text demonstrates independent results and also states that this pattern works for dictionaries.
  - _JGmemuINww 43-243s facts=['f1', 'f2'] label: Replace a shared default list with a None guard | summary: An employee-list helper appends a name and displays the list. Passing an existing list updates that list as intended. However, two calls that omit the list accumulate both names in the same default list, rather than starting separately. Default values are evaluated once when the function is defined, so later calls reuse the mutable object. The repair changes the default to None and creates an empty list inside an if employee_list is None branch. The repaired function is written but not executed in this range.

### s03 · check · Check: Avoiding shared mutable default arguments
 — Read the supplied evidence and choose the answer that matches the rule.
QUESTION [choice, intro, grading=client] add_label(label, labels=[]) appends label and returns labels. Two consecutive calls omit labels. Why can the second result include the first label?
  ✔ o1: The default list is created once at function definition and retains earlier modifications.
      why: Correct. The stated rule applies here.
  ✘ o2: An omitted default list is freshly created at each call.
      why: Mutable defaults are evaluated once, not recreated for each omitted argument.
  ✘ o3: append always copies a list before changing it.
      why: Here the same default object retains modifications across calls; no per-call list is created.
  feedback✔: Correct. Your answer follows the rule taught in the text.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']  remediation→r01
  MEASURES: A:predict_mutable_default_reuse(f1)   anchors=[]
  taught-before-tested: A.f1←s01

### s04 · check · Check: Avoiding shared mutable default arguments
 — Read the supplied evidence and choose the answer that matches the rule.
QUESTION [choice, core, grading=client] Which pattern creates fresh state for omitted labels while preserving an explicitly supplied list?
  ✘ o1: Keep labels=[] in the signature.
      why: That mutable default is evaluated once and can retain modifications.
  ✘ o2: Always assign labels = [] at function entry.
      why: That would discard a caller-supplied list; the None check limits allocation to the omitted-list case.
  ✔ o3: Use labels=None; inside the function, if labels is None: assign labels = [].
      why: Correct. The stated rule applies here.
  feedback✔: Correct. Your answer follows the rule taught in the text.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']
  MEASURES: A:replace_mutable_default_with_per_call_object(f2)   anchors=[]
  taught-before-tested: A.f2←s01

### s05 · hands_on · Repair the shared default
 — Complete the helper so omitted-list calls create fresh storage while supplied lists are still used.
QUESTION [code_exercise, stretch, grading=client] Choose the default sentinel that activates fresh omitted-list storage while preserving supplied lists. Leave add_label and the probes unchanged. Consecutive omitted-list calls must return separate one-label lists, and an explicitly supplied list must still be updated and returned.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['def with named parameters and default arguments', 'None', 'if labels is None:', 'indented function and conditional bodies', 'variable assignment', 'list literals', 'string literals', 'labels.append(label)', 'return', 'function calls with positional or keyword arguments', 'print()'] blocked=10 items
  file main.py [editable]:
first_label = "blue"
second_label = "red"
default_labels = []
if True:
    def add_label(label, labels=default_labels):
        if labels is None:
            labels = []
        labels.append(label)
        return labels

# Instructor probes; do not edit.
first = add_label(first_label)
second = add_label(second_label)
supplied = []
explicit = add_label(first_label, supplied)

  SOLUTION main.py:
first_label = "blue"
second_label = "red"
default_labels = None
if True:
    def add_label(label, labels=default_labels):
        if labels is None:
            labels = []
        labels.append(label)
        return labels

# Instructor probes; do not edit.
first = add_label(first_label)
second = add_label(second_label)
supplied = []
explicit = add_label(first_label, supplied)

  test t1 (value_equals, visible=True): {"expr":"[first, second, first is second, explicit, explicit is supplied]","expected":[["blue"],["red"],false,["blue"],true]} | on-fail: Check the requested result and preserve the supplied inputs and scaffolding.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"cc0f0075b862e704e925209ee010d5cabb5f14fa2987169fea1e256caf963e46","tests_passed":1}
  feedback✔: Correct. Calling add_label("blue") and then add_label("red") returns ["blue"] and ["red"], respectively. A caller-supplied labels list is still updated and returned.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']
  MEASURES: A:predict_mutable_default_reuse(f1); A:replace_mutable_default_with_per_call_object(f2)   anchors=['practice']
  taught-before-tested: A.f1←s01; A.f2←s01

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

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: sorted(..., key=...)

=========

# EVALUATOR PACKET — Ordering iterables with a key function and Lambda expressions (learn_python.tile.061_062)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.sorting_with_key_functions — Ordering iterables with a key function
B = python.lambda_expressions — Lambda expressions

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=3
  warn: remediation step learn_python.tile.061_062.r02 is never referenced
  warn: learn_python.tile.061_062.s04/ix.learn_python.tile.061_062.s04: ADVISORY — syntax descriptors with no detector: ['*args and **kwargs parameter declarations', 'assert statements', 'def with a single parameter', 'generator expressions', 'lambda expressions', 'list and dictionary literals', 'list comprehensions', 'string and integer literals', 'yield']
  warn: learn_python.tile.061_062.s07/ix.learn_python.tile.061_062.s07: ADVISORY — syntax descriptors with no detector: ['**kwargs', '*args', 'assert statements', 'generator expressions', 'list and tuple literals', 'string and integer literals', 'tuple indexing', 'yield']

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
[VIDEO Ordering by a calculated comparison key] bridge-before: Watch how passing abs as the key changes the comparison criterion. Each number supplies a calculated comparison key, while the result still contains the original numbers. | bridge-after: The clip demonstrates comparison keys. The text also covers preserving the original list, reverse ordering, stable ordering for equal keys, and lowercase text keys.
  - D3JvDWO-BY4 323-411s facts=['f1'] label: Order numbers using an absolute-value key | summary: Ordinary numeric sorting places negative values before positive values. Passing abs as the key function changes the comparison to each number's absolute value: its distance from zero. The sorted result therefore orders the original numbers by magnitude, retaining their signs rather than replacing them with their comparison keys.

### s03 · check · Check: Ordering iterables with a key function
 — Read the supplied evidence and choose the answer that matches the rule.
QUESTION [choice, intro, grading=client] What does sorted(records, key=label_key, reverse=True) do to the original list and the result?
  ✔ o1: It returns a new list in reversed key order and leaves records unchanged.
      why: Correct. The stated rule applies here.
  ✘ o2: It sorts records in place and returns that same list.
      why: sorted does not mutate the original list.
  ✘ o3: It leaves records unchanged but ignores reverse=True.
      why: reverse=True reverses the ordering of the returned sorted result.
  feedback✔: Correct. Your answer follows the rule taught in the text.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']  remediation→r01
  MEASURES: A:distinguish_original_list_from_sorted_result_and_reverse_ordering(f2)   anchors=[]
  taught-before-tested: A.f2←s01

### s04 · hands_on · Order records by their key
 — Complete the supplied sorting task using a key function without changing the original list.
QUESTION [code_exercise, stretch, grading=client] Use the supplied named label_key function to create a new list named ordered in ascending lowercase-label order. Keep records and label_key unchanged.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment', 'list and dictionary literals', 'string and integer literals', 'dictionary access with record["label"]', 'def with a single parameter', 'return', 'str.lower()', 'sorted(records, key=function)', 'reverse=True', 'print()', 'list comprehensions'] blocked=6 items
  file main.py [editable]:
label_0 = 'blue'
quantity_0 = 3
label_1 = 'Red'
quantity_1 = 2
label_2 = 'BLUE'
quantity_2 = 3
records = [{"label": label_0, "quantity": quantity_0}, {"label": label_1, "quantity": quantity_1}, {"label": label_2, "quantity": quantity_2}]
# Supplied named key; leave unchanged.
if True:
    def label_key(record):
        return record["label"].lower()

ordered = None

  SOLUTION main.py:
label_0 = 'blue'
quantity_0 = 3
label_1 = 'Red'
quantity_1 = 2
label_2 = 'BLUE'
quantity_2 = 3
records = [{"label": label_0, "quantity": quantity_0}, {"label": label_1, "quantity": quantity_1}, {"label": label_2, "quantity": quantity_2}]
# Supplied named key; leave unchanged.
if True:
    def label_key(record):
        return record["label"].lower()

ordered = sorted(records, key=label_key)

  test t1 (value_equals, visible=True): {"expr":"[ordered, records, ordered is records]","expected":[[{"label":"blue","quantity":3},{"label":"BLUE","quantity":3},{"label":"Red","quantity":2}],[{"label":"blue","quantity":3},{"label":"Red","quantity":2},{"label":"BLUE","quantity":3}],false]} | on-fail: Check the requested result and preserve the supplied inputs and scaffolding.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"26d0ea18e6dc145472d695e4f6fd2a3bc8de3cc1fc14c68ed0719bb8df830b55","tests_passed":1}
  feedback✔: Correct. A new list contains the records in lowercase-label order; records with equal lowercase labels retain their relative order, and the original list remains unchanged.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']
  MEASURES: A:sort_records_by_a_derived_key(f1,f4); A:determine_relative_order_of_equal_key_records(f3)   anchors=['practice']
  taught-before-tested: A.f1←s01; A.f4←s01; A.f3←s01

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
QUESTION [choice, core, grading=client] Each pair is (label, quantity). Which one-parameter, single-expression lambda returns the quantity as a sorting key?
  ✘ o1: lambda: pair[1]
      why: This lambda has no parameter to receive the pair being sorted.
  ✔ o2: lambda pair: pair[1]
      why: Correct. The stated rule applies here.
  ✘ o3: lambda pair: pair[0]
      why: Index 0 is the label, not the quantity.
  feedback✔: Correct. Your answer follows the rule taught in the text.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']  remediation→r03
  MEASURES: B:express_single_expression_transformation_with_correct_parameters(f1,f2)   anchors=[]
  taught-before-tested: B.f1←s05; B.f2←s05

### s07 · hands_on · Supply a one-expression key
 — Complete the sorting key with a lambda that returns the required comparison value.
QUESTION [code_exercise, stretch, grading=client] Use the supplied one-expression quantity key to create ordered in ascending quantity order. Keep pairs and chosen_key unchanged.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment', 'list and tuple literals', 'string and integer literals', 'tuple indexing', 'sorted(pairs, key=...)', 'lambda pair: pair[1]', 'print(ordered)'] blocked=8 items
  file main.py [editable]:
label_0 = 'blue'
quantity_0 = 3
label_1 = 'red'
quantity_1 = 2
pairs = [(label_0, quantity_0), (label_1, quantity_1)]
chosen_key = lambda pair: pair[1]
ordered = None

  SOLUTION main.py:
label_0 = 'blue'
quantity_0 = 3
label_1 = 'red'
quantity_1 = 2
pairs = [(label_0, quantity_0), (label_1, quantity_1)]
chosen_key = lambda pair: pair[1]
ordered = sorted(pairs, key=chosen_key)

  test t1 (value_equals, visible=True): {"expr":"ordered","expected":[["red",2],["blue",3]]} | on-fail: Check the requested result and preserve the supplied inputs and scaffolding.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"95b53289ea66c33a3045d5ecf9ff3f0714fa63287786528e193a3f8a1ccb904b","tests_passed":1}
  feedback✔: Correct. ordered contains [("red", 2), ("blue", 3)], using a lambda that accepts one pair and returns its quantity.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']
  MEASURES: B:express_single_expression_transformation_with_correct_parameters(f1,f2)   anchors=['practice']
  taught-before-tested: B.f1←s05; B.f2←s05

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

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=4
  warn: remediation step learn_python.tile.063_064.r02 is never referenced
  warn: remediation step learn_python.tile.063_064.r04 is never referenced
  warn: learn_python.tile.063_064.s04/ix.learn_python.tile.063_064.s04: ADVISORY — syntax descriptors with no detector: ['**kwargs', '*args', 'assert statements', 'except FileNotFoundError:', 'except OSError:', 'generator expressions', 'indented blocks', 'string literals', 'try/except', 'with statements', 'yield']
  warn: learn_python.tile.063_064.s07/ix.learn_python.tile.063_064.s07: ADVISORY — syntax descriptors with no detector: ['**kwargs', '*args', 'assert', 'class', 'string literals', 'variable assignment with =', 'with', 'yield']

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
[VIDEO Keep specific recovery branches reachable] bridge-before: Watch how a broad handler reports an undefined name as a missing file. The clip uses Exception as its broader handler; our example uses OSError to focus on the relevant parent–subclass relationship. | bridge-after: The clip demonstrates specific-before-broad ordering. The text also explains subclass matching and first-match selection, and supplies the relationship absent from the clip: FileNotFoundError is a subclass of OSError.
  - NIWwJbo-9_8 33-348s facts=['f2'] label: Place FileNotFoundError before a broader handler | summary: Opening a file with an incorrect filename produces FileNotFoundError. A broad handler replaces the traceback with a missing-file message, but also gives that misleading message for an undefined name. Restricting the handler to FileNotFoundError leaves the NameError unmatched. Adding an Exception handler below it provides a separate, broader response. Putting that broader handler first would prevent the missing-file branch from running. Finally, binding the caught exception with as e allows its error message to be displayed.

### s03 · check · Check: Selecting specific exception handlers
 — Read the supplied evidence and choose the answer that matches the rule.
QUESTION [choice, intro, grading=client] A try body raises FileNotFoundError. except OSError appears before except FileNotFoundError. Which recovery action runs?
  ✔ o1: The OSError action, because it is the first matching handler.
      why: Correct. The stated rule applies here.
  ✘ o2: The FileNotFoundError action, regardless of order.
      why: FileNotFoundError is a subclass of OSError; the earlier OSError handler already matches.
  ✘ o3: Both actions run.
      why: Only the first matching handler runs.
  feedback✔: Correct. Your answer follows the rule taught in the text.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']  remediation→r01
  MEASURES: A:predict_first_matching_handler_for_subclass_exception(f1,f3)   anchors=[]
  taught-before-tested: A.f1←s01; A.f3←s01

### s04 · hands_on · Keep specific recovery reachable
 — Complete the supplied handlers with the subclass-specific recovery before its broader parent.
QUESTION [code_exercise, stretch, grading=client] Choose the handler order that keeps missing-file recovery reachable before broader file-operation recovery. Set recover to the function whose deliberately raised FileNotFoundError reaches the specific recovery and prints File missing. Change only the recover assignment; do not change either recovery action or the exception.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['try/except', 'except FileNotFoundError:', 'except OSError:', 'raise FileNotFoundError("missing-example.txt")', 'print()', 'string literals', 'indented blocks'] blocked=8 items
  file main.py [editable]:
missing_notice = 'File missing'
other_notice = 'Other file operation failure'
if True:

    def specific_first():
        try:
            raise FileNotFoundError('missing-example.txt')
        except FileNotFoundError:
            print(missing_notice)
        except OSError:
            print(other_notice)

    def broad_first():
        try:
            raise FileNotFoundError('missing-example.txt')
        except OSError:
            print(other_notice)
        except FileNotFoundError:
            print(missing_notice)
recover = broad_first
recover()

  SOLUTION main.py:
missing_notice = 'File missing'
other_notice = 'Other file operation failure'
if True:

    def specific_first():
        try:
            raise FileNotFoundError('missing-example.txt')
        except FileNotFoundError:
            print(missing_notice)
        except OSError:
            print(other_notice)

    def broad_first():
        try:
            raise FileNotFoundError('missing-example.txt')
        except OSError:
            print(other_notice)
        except FileNotFoundError:
            print(missing_notice)
recover = specific_first
recover()

  test t1 (stdout_equals, visible=True): {"expected":"File missing"} | on-fail: Select the handler order that reaches the specific recovery action.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"6df441b1807315462f9a9766ac60e4897df4dfa206aa8e1545a5a9cc0b7b5f7e","tests_passed":1}
  feedback✔: Correct. A deliberately raised FileNotFoundError reaches the specific handler and displays File missing rather than Other file operation failure.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']
  MEASURES: A:order_handlers_to_preserve_specific_recovery(f2,f3)   anchors=['practice']
  taught-before-tested: A.f2←s01; A.f3←s01

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
QUESTION [choice, core, grading=client] The input contract requires numeric text. int("three") raises ValueError. What response fits this evidence?
  ✘ o1: Treat it as proof of inadequate filesystem access rights.
      why: The report is a numeric conversion failure, not a path access failure.
  ✔ o2: Reject the unsuitable input or request corrected numeric text.
      why: Correct. The stated rule applies here.
  ✘ o3: Treat the conversion failure as proof of an implementation defect.
      why: The supplied text violates the stated input value contract; that evidence does not establish a coding defect.
  feedback✔: Correct. Your answer follows the rule taught in the text.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']  remediation→r03
  MEASURES: B:choose_input_rejection_for_value_contract_violation(f1)   anchors=[]
  taught-before-tested: B.f1←s05

### s07 · hands_on · Review the failure reports
 — Read the supplied reports and decide which diagnostic category and response fits each cause.
QUESTION [code_exercise, stretch, grading=client] Read the three supplied reports: unsuitable numeric_text fails conversion; misspelled_name causes NameError; inadequate rights for otherwise valid input_path cause PermissionError. Fill each category/response string. Use exactly these category labels: "input failure", "implementation defect", "external operational failure"; and response labels: "request corrected numeric text", "correct the misspelled name", "report access failure". Copy the causal evidence names into input_evidence, implementation_evidence, and access_evidence respectively. Do not run a filesystem operation. The checker reads each report's category, response and evidence. Use the supplied vocabulary variable names on the right side of your assignments instead of typing their text.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment with =', 'string literals'] blocked=6 items
  file main.py [editable]:
numeric_text = "three"
misspelled_name = "quanity"
input_path = "orders.csv"
input_failure = 'input failure'
implementation_defect = 'implementation defect'
external_failure = 'external operational failure'
request_correction = 'request corrected numeric text'
code_correction = 'correct the misspelled name'
access_report = 'report access failure'
# Supplied report 1: ValueError from int("three"): unsuitable numeric text.
input_category = ""
input_response = ""

# Supplied report 2: NameError caused by a misspelled local quantity name.
implementation_category = ""
implementation_response = ""

# Supplied report 3: PermissionError opening an otherwise valid input path:
# inadequate access rights. No filesystem operation needs to run here.
access_category = ""
access_response = ""

input_evidence = ""
implementation_evidence = ""
access_evidence = ""

  SOLUTION main.py:
numeric_text = "three"
misspelled_name = "quanity"
input_path = "orders.csv"
input_failure = 'input failure'
implementation_defect = 'implementation defect'
external_failure = 'external operational failure'
request_correction = 'request corrected numeric text'
code_correction = 'correct the misspelled name'
access_report = 'report access failure'
# Supplied report 1: ValueError from int("three"): unsuitable numeric text.
input_category = input_failure
input_response = request_correction

# Supplied report 2: NameError caused by a misspelled local quantity name.
implementation_category = implementation_defect
implementation_response = code_correction

# Supplied report 3: PermissionError opening an otherwise valid input path:
# inadequate access rights. No filesystem operation needs to run here.
access_category = external_failure
access_response = access_report

input_evidence = numeric_text
implementation_evidence = misspelled_name
access_evidence = input_path

  test t1 (value_equals, visible=True): {"expr":"[input_category, input_response, input_evidence]","expected":["input failure","request corrected numeric text","three"]} | on-fail: Check the requested result and preserve the supplied inputs and scaffolding.
  test t2 (value_equals, visible=True): {"expr":"[implementation_category, implementation_response, implementation_evidence]","expected":["implementation defect","correct the misspelled name","quanity"]} | on-fail: Check the requested result and preserve the supplied inputs and scaffolding.
  test t3 (value_equals, visible=True): {"expr":"[access_category, access_response, access_evidence]","expected":["external operational failure","report access failure","orders.csv"]} | on-fail: Check the requested result and preserve the supplied inputs and scaffolding.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"f5685ce81d55f8ac55a7c863b127f3752131b7e1c3faede310ce04a627801e25","tests_passed":3}
  feedback✔: Correct. The completed Python assignments classify malformed numeric input as an input failure requiring correction, the misspelled name as an implementation defect requiring code correction, and inadequate access rights as an external operational failure requiring an access-failure report.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']
  MEASURES: B:choose_implementation_correction_for_misspelled_name(f2); B:identify_access_failure_without_blaming_path_or_implementation(f3)   anchors=['practice']
  taught-before-tested: B.f2←s05; B.f3←s05

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

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=3
  warn: remediation step learn_python.tile.065_065.r02 is never referenced
  warn: remediation step learn_python.tile.065_065.r03 is never referenced
  warn: learn_python.tile.065_065.s06/ix.learn_python.tile.065_065.s06: ADVISORY — syntax descriptors with no detector: ['**kwargs in function calls', '**kwargs in function definitions', '*args in function calls', '*args in function definitions', 'assert', 'class', 'integer literals', 'keyword arguments', 'multiplication', 'positional arguments', 'with', 'yield']

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
[VIDEO Collecting arguments and expanding them at a call] bridge-before: Watch the first clip expand arguments at a call and the second collect them in a definition. “Splat” means asterisk; the second calls it an “unpacking operator,” but its demonstrated definition behavior is collection. | bridge-after: The first clip teaches call expansion; the second teaches positional collection. Neither covers keyword collection in definitions, duplicate bindings, or forwarding wrappers. The text supplies those rules and a complete forwarding example.
  - BnPO5OQ4ZZ4 50-148s facts=['f3'] label: Expand a list or dictionary into function-call arguments | summary: A function accepts x and y and prints each value. Rather than pass two list elements through separate indexing expressions, a call uses * to expand the list [21, 75] into positional arguments. The function receives x as 21 and y as 75. A second call uses ** to expand a dictionary containing x: 5 and y: 6 into keyword arguments, producing the corresponding values.
  - Vh__2V2tXUM 39-191s facts=['f1'] label: Collect variable positional arguments into a tuple with *args | summary: An addition function with two parameters rejects a third positional argument. Replacing those parameters with *args lets the function collect its positional arguments into a tuple. The function then iterates over that tuple, accumulates a total, and returns the sum, allowing calls with different numbers of arguments. The collecting parameter can have another name, such as nums; args is the conventional choice.

### s04 · check · Check: Binding variable arguments with *args and **kwargs
 — Read the supplied evidence and choose the answer that matches the rule.
QUESTION [choice, intro, grading=client] For wrapper(*args, **kwargs), what is collected by each parameter when called as wrapper(3, price=5)?
  ✔ o1: args collects positional arguments in a tuple; kwargs collects additional keywords in a dictionary.
      why: Correct. The stated rule applies here.
  ✘ o2: args collects a dictionary; kwargs collects a tuple.
      why: The collection types are reversed: positional arguments form a tuple and keyword arguments form a dictionary.
  ✘ o3: Both parameters collect lists.
      why: The documented collections are a tuple and a dictionary, not lists.
  feedback✔: Correct. Your answer follows the rule taught in the text.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']  remediation→r01
  MEASURES: A:identify_collected_positional_and_keyword_arguments(f1,f2)   anchors=[]
  taught-before-tested: A.f1←s01; A.f2←s01

### s05 · check · Check: Binding variable arguments with *args and **kwargs
 — Read the supplied evidence and choose the answer that matches the rule.
QUESTION [choice, core, grading=client] A wrapper must pass its collected positional and keyword arguments to target without adding any duplicate bindings. Which call expands both collections?
  ✘ o1: target(args, kwargs)
      why: That passes the two collections as ordinary arguments rather than expanding them.
  ✘ o2: target(*args, **kwargs, price=5)
      why: Adding price can duplicate a price already supplied through the caller's expanded arguments.
  ✔ o3: target(*args, **kwargs)
      why: Correct. The stated rule applies here.
  feedback✔: Correct. Your answer follows the rule taught in the text.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']
  MEASURES: A:expand_sequences_and_dictionaries_into_call_arguments(f3)   anchors=[]
  taught-before-tested: A.f3←s01

### s06 · hands_on · Forward the caller’s arguments
 — Complete the wrapper so it expands both collected argument groups without duplicate bindings.
QUESTION [code_exercise, stretch, grading=client] Choose the wrapper that forwards both argument groups without adding a duplicate binding. Set wrapper to the function that forwards both collected argument groups to target and returns its result without adding a duplicate price binding. Change only the wrapper assignment; leave target and both implementations unchanged.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['def', 'return', 'function parameters with default values', '*args in function definitions', '**kwargs in function definitions', '*args in function calls', '**kwargs in function calls', 'positional arguments', 'keyword arguments', 'integer literals', 'multiplication', 'variable assignment', 'print()'] blocked=4 items
  file main.py [editable]:
if True:

    def target(quantity, price=4):
        return quantity * price
if True:

    def forward_arguments(*args, **kwargs):
        return target(*args, **kwargs)

    def duplicate_price(*args, **kwargs):
        return target(*args, price=4, **kwargs)
wrapper = duplicate_price

  SOLUTION main.py:
if True:

    def target(quantity, price=4):
        return quantity * price
if True:

    def forward_arguments(*args, **kwargs):
        return target(*args, **kwargs)

    def duplicate_price(*args, **kwargs):
        return target(*args, price=4, **kwargs)
wrapper = forward_arguments

  test t1 (function_call, visible=True): {"function":"wrapper","args":[3],"kwargs":{"price":5},"expected":15} | on-fail: The function must preserve this argument-dependent behavior.
  test t2 (function_call, visible=True): {"function":"wrapper","args":[3,5],"kwargs":{},"expected":15} | on-fail: The function must preserve this argument-dependent behavior.
  test t3 (function_call, visible=True): {"function":"wrapper","args":[3],"kwargs":{},"expected":12} | on-fail: The function must preserve this argument-dependent behavior.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"47011b509c5e20b52064f992c79b340604b4f35bc4807f476fa39892f0668eb3","tests_passed":3}
  feedback✔: Correct. The wrapper returns 15 for wrapper(3, price=5), 15 for wrapper(3, 5), and 12 for wrapper(3), preserving both supplied arguments and the target's default.  feedback✘: Review the execution or relationships in the written example, then try again.  hints: ['Trace the relevant relationship or operation one step at a time.', 'Compare your result with the stated input and required behavior.']
  MEASURES: A:forward_arguments_without_duplicate_bindings(f2,f4)   anchors=['practice']
  taught-before-tested: A.f2←s01; A.f4←s01

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