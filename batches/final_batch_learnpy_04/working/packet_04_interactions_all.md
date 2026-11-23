# EVALUATOR PACKET — Classes and instances (learn_python.tile.066_066)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.classes_and_instances — Classes and instances

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: remediation step learn_python.tile.066_066.r02 is never referenced
  warn: learn_python.tile.066_066.s04/ix.learn_python.tile.066_066.s04: ADVISORY — syntax descriptors with no detector: ['@classmethod', '@staticmethod', 'assert', 'class Order:', 'class attribute definitions', 'def __init__', 'indented class body', 'instance attribute assignment', 'is', 'pass', 'self', 'variable assignment with =']

## SOURCE FACTS — A (python.classes_and_instances)   objective: Define classes and create ordinary instances.
A.f1: class ClassName: followed by an indented body creates a class object; pass can supply an empty body.   [sources: python_tutorial#classes.html#class-definition-syntax]
A.f2: Calling an ordinary class with ClassName() creates a new instance; two such calls create distinct instances.   [sources: python_tutorial#classes.html#class-objects]
A.f3: is tests object identity, so first is second distinguishes shared identity from two separate instances.   [sources: python_stdlib_reference#stdtypes.html#comparisons]
note: Begin with this objective: Define classes and create ordinary instances.
note: Keep the example in the Classes and instances tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.file_modes, python.instance_initialization, python.instance_methods.
PRACTICE ANCHOR (live_code): Define an empty Order class, create first and second as separate instances, and demonstrate their separate identities using is.  SUCCESS: Order has an indented pass body, first and second are created by separate Order() calls, and printing first is second produces False.
ASSESSMENT ANCHOR: define_a_simple_class_with_an_empty_body facts=['f1']
ASSESSMENT ANCHOR: distinguish_a_class_object_from_its_instances facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_separate_instances_from_shared_identity facts=['f2', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing environment variables with os.environ; Choosing explicit text-file encodings; Choosing instance, class or static method binding; Computing dates and elapsed times with datetime; Creating local modules; Defining custom exceptions; Defining useful object representations with special methods; Diagnosing module search-path problems; Extending inherited behavior with super; Guarding a program entry point; Handling file and data-format failures; Initialising instance state with __init__; Inspecting object types and attributes; Instance methods and self; Instance versus class attributes; Managing resources with with; Object composition; Organising importable packages; Parsing command-line arguments with argparse; Performing filesystem operations with pathlib; Python encapsulation conventions; Reading and writing binary files; Recording program events with logging; Selecting safe file-opening modes; Serialising and deserialising data with Python json

## LESSON, in learner order

### s01 · explainer · Classes and instances
Understand — 
(definition) An indented body after `class Order:` creates the class object Order. Use `pass` when that body is empty. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Calling an ordinary class creates a new instance. Two calls to `Order()` create two distinct instances. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Use `is` to test object identity. `first is second` asks whether the names refer to the same object; an alias shares identity, unlike two separate instances. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[DIAGRAM: Two ordinary calls create distinct instances; alias and first share one object] nodes=['Order: class object', 'First Order instance', 'Second Order instance', 'first', 'second', 'alias'] edges=[('class', 'one', 'first = Order()'), ('class', 'two', 'second = Order()'), ('first', 'one', 'refers to'), ('alias', 'one', 'alias = first'), ('second', 'two', 'refers to')] alt: Two ordinary calls create distinct instances; alias and first share one object

### s02 · video · From an empty class to separate instances
Observe — 
[VIDEO From an empty class to separate instances] bridge-before: Watch how pass supplies an empty class body and how two Employee instances differ from the class used to create them. | bridge-after: The clip demonstrates separate instances through printed object representations, but does not use is. The text teaches identity comparisons for both distinct instances and a shared alias.
  - ZDa-Z5JzLYM 98-175s facts=['f1', 'f2'] label: Define an empty class and create two distinct instances | summary: An empty class still needs an indented body; pass supplies that body without adding behavior. The Employee class acts as a blueprint, while two calls create two separate Employee instances. Printing the instances produces object representations with different memory locations, illustrating that they are distinct objects.

### s03 · check · Check: Classes and instances
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.
QUESTION [choice, intro, grading=client] Order is an ordinary class. Read this code. Which statement correctly distinguishes the identities?
```python
first = Order()
second = Order()
alias = first
```
  ✔ o1: first and alias share identity; first and second are distinct instances.
      why: This matches the stated task and the taught behavior.
  ✘ o2: All three names share identity because they use the same class.
      why: Two ordinary class calls create distinct instances, even though they use one class.
  ✘ o3: first and alias are distinct because assigning a name creates a new instance.
      why: Assignment here makes an alias; it is not another Order() call.
  feedback✔: first and alias share identity; first and second are distinct instances.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Count the class calls, then distinguish a call from an assignment.']  remediation→r01
  MEASURES: A:distinguish_separate_instances_from_shared_identity(f2,f3)   anchors=['assessment:distinguish_separate_instances_from_shared_identity']
  taught-before-tested: A.f2←s01; A.f3←s01

### s04 · hands_on · Create separate Order instances
Practice — Define an empty Order class, create first and second as separate instances, and demonstrate their separate identities using is.
QUESTION [code_exercise, stretch, grading=client] The class implementation is supplied and must remain unchanged. Create first and second by separate Order() calls before the supplied identity comparison.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['class Order:', 'indented class body', 'pass', 'Order()', 'variable assignment with =', 'is', 'print()'] blocked=13 items
  file main.py [editable]:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\ndef empty_class_probe(code):\n    tree = ast.parse(code)\n    for node in list(tree.body):\n        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == "exec" and isinstance(node.value.args[0], ast.Constant):\n            tree.body.extend(ast.parse(node.value.args[0].value).body)\n    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Order")\n    return len(cls.body) == 1 and isinstance(cls.body[0], ast.Pass)\n\n\ndef prepare_case(inputs):\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [ns["first"] is ns[inputs["reference"]], type(ns["first"]) is ns["Order"], type(ns["second"]) is ns["Order"], captured.getvalue().strip(), empty_class_probe(code)]\n')

inputs = {'reference': 'first'}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
# Supplied class/function implementation; leave unchanged.
exec('class Order:\n    pass\n')
# Create the required instance(s) here using the supplied input names.
print(first is second)
# END LEARNER

  SOLUTION main.py:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\ndef empty_class_probe(code):\n    tree = ast.parse(code)\n    for node in list(tree.body):\n        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == "exec" and isinstance(node.value.args[0], ast.Constant):\n            tree.body.extend(ast.parse(node.value.args[0].value).body)\n    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Order")\n    return len(cls.body) == 1 and isinstance(cls.body[0], ast.Pass)\n\n\ndef prepare_case(inputs):\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [ns["first"] is ns[inputs["reference"]], type(ns["first"]) is ns["Order"], type(ns["second"]) is ns["Order"], captured.getvalue().strip(), empty_class_probe(code)]\n')

inputs = {'reference': 'first'}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
# Supplied class/function implementation; leave unchanged.
exec('class Order:\n    pass\n')
first = Order()
second = Order()
print(first is second)
# END LEARNER

  test t1 (function_call, visible=True): {"function":"check_case","args":[{"reference":"first"}],"expected":[true,true,true,"False",true]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  test t2 (function_call, visible=True): {"function":"check_case","args":[{"reference":"second"}],"expected":[false,true,true,"False",true]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"c648aba1466f4e3bc5d1409f123cc241e2ec2c8f79b9117ffa2fc96a1fdda631","tests_passed":2}
  feedback✔: The completed code meets the task on the supplied fixtures, including the changed inputs.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Follow the input names rather than substituting a fixed answer.', 'Check the required operation and where its result or resource state is observed.']
  MEASURES: A:define_a_simple_class_with_an_empty_body(f1); A:distinguish_a_class_object_from_its_instances(f1,f2)   anchors=['practice', 'assessment:define_a_simple_class_with_an_empty_body', 'assessment:distinguish_a_class_object_from_its_instances']
  taught-before-tested: A.f1←s01; A.f1←s01; A.f2←s01

### s05 · recap · Keep these distinctions
Takeaways — 
(takeaway) Compare two Order calls with `alias = first`: separate creation versus another name for the same object. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Selecting safe file-opening modes: Next, begin selecting safe file-opening modes.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: Classes and instances
(definition) Calling an ordinary class creates a new instance. Two calls to `Order()` create two distinct instances. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Use `is` to test object identity. `first is second` asks whether the names refer to the same object; an alias shares identity, unlike two separate instances. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Compare two Order calls with `alias = first`: separate creation versus another name for the same object. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit: Classes and instances
(definition) An indented body after `class Order:` creates the class object Order. Use `pass` when that body is empty. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Calling an ordinary class creates a new instance. Two calls to `Order()` create two distinct instances. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) Compare two Order calls with `alias = first`: separate creation versus another name for the same object. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast

=========

# EVALUATOR PACKET — Selecting safe file-opening modes (learn_python.tile.067_067)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.file_modes — Selecting safe file-opening modes

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=3
  warn: remediation step learn_python.tile.067_067.r02 is never referenced
  warn: remediation step learn_python.tile.067_067.r03 is never referenced
  warn: learn_python.tile.067_067.s05/ix.learn_python.tile.067_067.s05: ADVISORY — syntax descriptors with no detector: ['assert statements', 'binary file modes', 'custom exception class definitions', 'string literals', 'try/except FileExistsError', 'try/finally', 'with statements']

## SOURCE FACTS — A (python.file_modes)   objective: Select Python file modes without unintended data loss.
A.f1: open(path, "r") reads an existing file; r is the default mode.   [sources: python_stdlib_reference#functions.html#open]
A.f2: open(path, "w") writes and truncates an existing file, or creates a new file.   [sources: python_stdlib_reference#functions.html#open]
A.f3: open(path, "a") appends to an existing file or creates it.   [sources: python_stdlib_reference#functions.html#open]
A.f4: open(path, "x") exclusively creates a new file and fails if it exists.   [sources: python_stdlib_reference#functions.html#open]
A.f5: Handle FileExistsError when exclusive creation finds an existing destination, rather than changing to a truncating mode unintentionally.   [sources: python_stdlib_reference#exceptions.html#FileExistsError]
note: Begin with this objective: Select Python file modes without unintended data loss.
note: Keep the example in the File modes tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.instance_initialization, python.instance_methods, python.class_and_static_methods.
note: Require linux.filesystem_navigation_and_files before this filesystem, script, module or environment unit; do not teach terminal navigation here.
PRACTICE ANCHOR (live_code): Write First to a new report.txt using exclusive creation, and handle an existing destination without replacing or extending its contents.  SUCCESS: With report.txt absent, the program creates it containing First. With report.txt already containing First, the program handles FileExistsError, reports that the destination exists, and leaves the contents unchanged.
ASSESSMENT ANCHOR: choose_read_mode_without_truncation facts=['f1', 'f2']
ASSESSMENT ANCHOR: choose_append_mode_to_preserve_existing_content facts=['f2', 'f3']
ASSESSMENT ANCHOR: choose_exclusive_creation_and_handle_existing_destination facts=['f2', 'f4', 'f5']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing environment variables with os.environ; Choosing explicit text-file encodings; Choosing instance, class or static method binding; Choosing random or secrets for randomness; Computing dates and elapsed times with datetime; Creating local modules; Defining custom exceptions; Defining useful object representations with special methods; Diagnosing module search-path problems; Extending inherited behavior with super; Guarding a program entry point; Handling file and data-format failures; Initialising instance state with __init__; Inspecting object types and attributes; Instance methods and self; Instance versus class attributes; Managing resources with with; Object composition; Organising importable packages; Parsing command-line arguments with argparse; Performing filesystem operations with pathlib; Python encapsulation conventions; Reading and writing binary files; Recording program events with logging; Serialising and deserialising data with Python json

## LESSON, in learner order

### s01 · explainer · Selecting safe file-opening modes
Understand — 
(definition) `open(path, "r")` reads an existing file. With no mode argument, `r` is the default. ⟦A.f1 A:tb2 A:tb4⟧
(definition) `w` writes: it truncates an existing file or creates a new one. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) `a` appends to an existing file, or creates it if absent. ⟦A.f3 A:tb3 A:tb4⟧
(definition) `x` exclusively creates a new file and fails if the destination already exists. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(definition) Handle `FileExistsError` when exclusive creation finds an existing report. Do not silently switch to a mode that truncates it. ⟦A.f5 A:tb3 A:tb4 A:tb5⟧
[BEFORE_AFTER] Each mode starts from the same existing report. Exclusive creation does not replace it.
  before:
[DIAGRAM: Before each independent mode choice] nodes=['report.txt contents: First'] edges=[] alt: Before each independent mode choice
  after:
[DIAGRAM: After opening and the described operation] nodes=['r: prior contents retained', 'a: retain contents, then append Second', 'w: remove prior contents before writing', 'x: retain contents; raise FileExistsError'] edges=[] alt: After opening and the described operation

### s02 · video · Write mode and the risk of replacing a report
Observe — 
[VIDEO Write mode and the risk of replacing a report] bridge-before: Watch how opening with "w" creates a file before any writing occurs. The clip calls the existing-file behavior “overwriting”; Devspace calls the immediate removal of existing contents truncation. | bridge-after: The clip mentions append but omits its create-if-missing behavior, the default read mode, exclusive creation, and collision handling. The text covers these gaps so you can protect an existing report.
  - Uh2ebFW8OYM 885-1022s facts=['f2'] label: See how write mode creates a file or truncates an existing one | summary: A file opened for reading cannot be written to. Opening test2.txt with "w" creates it even when no text is written; if the file already exists, that mode discards its existing contents. The demonstration then writes text and shows that successive write calls on the same open file place their text back to back. Append mode is briefly identified as an alternative that avoids replacing existing contents.

### s03 · check · Check: Selecting safe file-opening modes
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.
QUESTION [choice, intro, grading=client] An existing report must be read, without truncating it or writing to it. Which explicit mode matches this purpose?
  ✔ o1: r
      why: This matches the stated task and the taught behavior.
  ✘ o2: w
      why: w writes and truncates an existing file.
  ✘ o3: x
      why: x attempts exclusive creation; it is not the reading mode.
  feedback✔: r  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Match the operation to the mode, not just to whether a file exists.']  remediation→r01
  MEASURES: A:choose_read_mode_without_truncation(f1,f2)   anchors=['assessment:choose_read_mode_without_truncation']
  taught-before-tested: A.f1←s01; A.f2←s01

### s04 · check · Check: Selecting safe file-opening modes
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.
QUESTION [choice, core, grading=client] An existing report must retain its content and receive new text at the end. Which mode matches this purpose?
  ✘ o1: w
      why: w truncates the existing file, so it does not preserve the report.
  ✘ o2: x
      why: x fails when the destination already exists; it does not append.
  ✔ o3: a
      why: This matches the stated task and the taught behavior.
  feedback✔: a  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Distinguish adding content from replacing content.']
  MEASURES: A:choose_append_mode_to_preserve_existing_content(f2,f3)   anchors=['assessment:choose_append_mode_to_preserve_existing_content']
  taught-before-tested: A.f2←s01; A.f3←s01

### s05 · hands_on · Create a report without replacement
Practice — Write First to a new report.txt using exclusive creation, and handle an existing destination without replacing or extending its contents.
QUESTION [code_exercise, intro, grading=client] The exclusive-creation handler, write, and close operations are supplied. Set creation_mode to the mode that creates a new destination but refuses an existing one. Preserve the supplied try/except FileExistsError handler. An absent report must receive report_text; an existing report must remain unchanged and report "Destination exists".
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment', 'string literals', 'open(path, "r")', 'open(path)', 'open(path, "w")', 'open(path, "a")', 'open(path, "x")', 'file.read()', 'file.write(text)', 'file.close()', 'try/except FileExistsError', 'try/finally', 'print()'] blocked=8 items
  file main.py [editable]:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\n\ndef prepare_case(inputs):\n    p = pathlib.Path(inputs["path"])\n    if p.exists(): p.unlink()\n    if inputs["existing"] is not None: p.write_text(inputs["existing"])\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [pathlib.Path(inputs["path"]).read_text(), captured.getvalue().strip(), ns["file"].closed if "file" in ns else True]\n')

inputs = {'path': 'report.txt', 'report_text': 'First', 'existing': None}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
creation_mode = "r"
try:
    file = open(path, creation_mode)
    file.write(report_text)
    file.close()
except FileExistsError:
    print("Destination exists")
# END LEARNER

  SOLUTION main.py:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\n\ndef prepare_case(inputs):\n    p = pathlib.Path(inputs["path"])\n    if p.exists(): p.unlink()\n    if inputs["existing"] is not None: p.write_text(inputs["existing"])\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [pathlib.Path(inputs["path"]).read_text(), captured.getvalue().strip(), ns["file"].closed if "file" in ns else True]\n')

inputs = {'path': 'report.txt', 'report_text': 'First', 'existing': None}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
creation_mode = "x"
try:
    file = open(path, creation_mode)
    file.write(report_text)
    file.close()
except FileExistsError:
    print("Destination exists")
# END LEARNER

  test t1 (function_call, visible=True): {"function":"check_case","args":[{"path":"report.txt","report_text":"First","existing":null}],"expected":["First","",true]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  test t2 (function_call, visible=True): {"function":"check_case","args":[{"path":"report.txt","report_text":"First","existing":"First"}],"expected":["First","Destination exists",true]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  test t3 (function_call, visible=True): {"function":"check_case","args":[{"path":"report.txt","report_text":"Second","existing":null}],"expected":["Second","",true]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  test t4 (function_call, visible=True): {"function":"check_case","args":[{"path":"report.txt","report_text":"Second","existing":"Keep"}],"expected":["Keep","Destination exists",true]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"ff32492c308966b42a49e7a496099adbf87f4cb068105d68f320ff98ac01b9fd","tests_passed":4}
  feedback✔: The completed code meets the task on the supplied fixtures, including the changed inputs.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Which mode refuses to open an existing destination for writing?', 'Check the required operation and where its result or resource state is observed.']
  MEASURES: A:choose_exclusive_creation_and_handle_existing_destination(f2,f4,f5)   anchors=['practice', 'assessment:choose_exclusive_creation_and_handle_existing_destination']
  taught-before-tested: A.f2←s01; A.f4←s01; A.f5←s01

### s06 · recap · Keep these distinctions
Takeaways — 
(takeaway) For an existing report.txt, exclusive creation fails; switching to w would replace the report instead of preserving it. ⟦A.f2 A.f4 A.f5 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Initialising instance state with __init__: Next, begin initialising instance state with __init__.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: Selecting safe file-opening modes
(definition) `open(path, "r")` reads an existing file. With no mode argument, `r` is the default. ⟦A.f1 A:tb2 A:tb4⟧
(definition) `w` writes: it truncates an existing file or creates a new one. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) For an existing report.txt, exclusive creation fails; switching to w would replace the report instead of preserving it. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit: Selecting safe file-opening modes
(definition) `w` writes: it truncates an existing file or creates a new one. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) `a` appends to an existing file, or creates it if absent. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) For an existing report.txt, exclusive creation fails; switching to w would replace the report instead of preserving it. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
### r03 · Revisit: Selecting safe file-opening modes
(definition) `w` writes: it truncates an existing file or creates a new one. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) `x` exclusively creates a new file and fails if the destination already exists. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(definition) Handle `FileExistsError` when exclusive creation finds an existing report. Do not silently switch to a mode that truncates it. ⟦A.f5 A:tb3 A:tb4 A:tb5⟧
(misconception) For an existing report.txt, exclusive creation fails; switching to w would replace the report instead of preserving it. ⟦A.f2 A.f4 A.f5 A:tb3 A:tb4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: encoding= arguments to open()
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast

=========

# EVALUATOR PACKET — Initialising instance state with __init__ / Instance methods and self / Choosing instance, class or static method binding (learn_python.tile.068_070)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.instance_initialization — Initialising instance state with __init__
B = python.instance_methods — Instance methods and self
C = python.class_and_static_methods — Choosing instance, class or static method binding

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=9
  warn: remediation step learn_python.tile.068_070.r02 is never referenced
  warn: remediation step learn_python.tile.068_070.r03 is never referenced
  warn: remediation step learn_python.tile.068_070.r05 is never referenced
  warn: remediation step learn_python.tile.068_070.r06 is never referenced
  warn: remediation step learn_python.tile.068_070.r08 is never referenced
  warn: remediation step learn_python.tile.068_070.r09 is never referenced
  warn: learn_python.tile.068_070.s04/ix.learn_python.tile.068_070.s04: ADVISORY — syntax descriptors with no detector: ['@classmethod', '@property', '@staticmethod', 'additional method definitions inside Order', 'assert statements', 'class Order:', 'indented class and function bodies', 'string and integer literals']
  warn: learn_python.tile.068_070.s08/ix.learn_python.tile.068_070.s08: ADVISORY — syntax descriptors with no detector: ['+', '@classmethod', '@property', '@staticmethod', 'assert', 'attribute assignment', 'class Order:', 'indented class and method bodies', 'integer literals', 'yield']
  warn: learn_python.tile.068_070.s12/ix.learn_python.tile.068_070.s12: ADVISORY — syntax descriptors with no detector: ['@classmethod', '@property', 'assert', 'class Order:', 'indented method bodies', 'integer literals', 'string literals', 'yield']

## SOURCE FACTS — A (python.instance_initialization)   objective: Initialize per-instance state with __init__.
A.f1: If a class defines __init__, instantiation automatically invokes it on the new instance and passes the constructor arguments.   [sources: python_tutorial#classes.html#class-objects]
A.f2: Define def __init__(self, first, second): in the class and assign self.first = first and self.second = second to initialize those instance attributes.   [sources: python_tutorial#classes.html#class-objects]
A.f3: __init__ initializes the created instance rather than returning a replacement object.   [sources: python_tutorial#classes.html#class-objects]
note: Begin with this objective: Initialize per-instance state with __init__.
note: Keep the example in the Initializing objects and binding methods tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.instance_methods, python.class_and_static_methods, python.composition.
PRACTICE ANCHOR (live_code): Initialize an Order record with a label and quantity supplied as constructor arguments.  SUCCESS: Order("notebook", 3) creates an instance whose label is "notebook" and whose quantity is 3, using assignments inside __init__.
ASSESSMENT ANCHOR: initialize_attributes_from_constructor_inputs facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_initialization_from_returning_a_replacement_object facts=['f3']

## SOURCE FACTS — B (python.instance_methods)   objective: Implement instance behavior using self.
B.f1: An instance method receives the target instance as its first argument, conventionally named self.   [sources: python_tutorial#classes.html#method-objects]
B.f2: Define def method(self, argument): inside the class and use self.attribute to read or reassign that instance’s state.   [sources: python_tutorial#classes.html#method-objects]
B.f3: instance.method(value) passes instance implicitly as self and value as the next argument.   [sources: python_tutorial#classes.html#method-objects]
note: Begin with this objective: Implement instance behavior using self.
note: Keep the example in the Initializing objects and binding methods tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.class_and_static_methods, python.composition, python.encapsulation_conventions.
PRACTICE ANCHOR (live_code): Add an add(self, amount) method to Order that increases the receiving object's stored quantity by amount.  SUCCESS: Starting with order = Order(3), calling order.add(2) changes order.quantity to 5 through the method's use of self.quantity.
ASSESSMENT ANCHOR: define_instance_method_to_read_or_update_receiving_instance facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_implicit_instance_and_explicit_argument_in_method_call facts=['f1', 'f3']

## SOURCE FACTS — C (python.class_and_static_methods)   objective: Choose the method binding appropriate to an object's operation.
C.f1: An instance method receives the instance as its implicit first argument and can use that instance’s state.   [sources: python_tutorial#classes.html#method-objects]
C.f2: Put @classmethod above def method(cls, ...): to receive the class as the implicit first argument; return cls(arguments) to construct an instance in an alternative constructor.   [sources: python_stdlib_reference#functions.html#classmethod]
C.f3: Put @staticmethod above def method(...): for an operation with no implicit instance or class argument.   [sources: python_stdlib_reference#functions.html#staticmethod]
note: Begin with this objective: Choose the method binding appropriate to an object's operation.
note: Keep the example in the Initializing objects and binding methods tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.composition, python.encapsulation_conventions, python.inheritance_and_super.
PRACTICE ANCHOR (live_code): Implement Order.from_text as a class method that converts a quantity string to an integer and constructs an Order through cls.  SUCCESS: Order.from_text("3") returns an Order whose quantity is the integer 3, using @classmethod and return cls(int(text)).
ASSESSMENT ANCHOR: select_instance_binding_for_instance_state facts=['f1']
ASSESSMENT ANCHOR: select_class_binding_for_alternative_construction facts=['f2']
ASSESSMENT ANCHOR: select_static_binding_for_operations_without_implicit_state facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing environment variables with os.environ; Choosing explicit text-file encodings; Choosing instance, class or static method binding; Choosing random or secrets for randomness; Computing dates and elapsed times with datetime; Creating isolated virtual environments; Creating local modules; Defining custom exceptions; Defining useful object representations with special methods; Diagnosing module search-path problems; Extending inherited behavior with super; Guarding a program entry point; Handling file and data-format failures; Inspecting interpreter runtime information with sys; Inspecting object types and attributes; Instance methods and self; Instance versus class attributes; Managing resources with with; Matching text patterns with re; Object composition; Organising importable packages; Parsing command-line arguments with argparse; Performing filesystem operations with pathlib; Python encapsulation conventions; Reading and writing binary files; Recording program events with logging; Serialising and deserialising data with Python json

## LESSON, in learner order

### s01 · explainer · Initialising instance state with __init__
Understand — 
(definition) When a class defines `__init__`, instantiation automatically calls it on the new instance with the constructor arguments. ⟦A.f1 A:tb1 A:tb2 A:tb4⟧
(definition) Define `__init__(self, label, quantity)` inside Order. Assign `self.label = label` and `self.quantity = quantity` to store those arguments as instance attributes. ⟦A.f2 A:tb1 A:tb3 A:tb4⟧
(definition) `__init__` initializes the instance already created. It does not return a replacement object. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[CODE python]
class Order:
    def __init__(self, label, quantity):
        self.label = label
        self.quantity = quantity

order = Order("notebook", 3)
print(order.label, order.quantity)
  annotations: ['Instantiation passes the constructor arguments to the new instance’s initializer.', 'Store label on the receiving instance.', 'Store quantity on that same instance.']

### s02 · check · Check: Initialising instance state with __init__
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.
QUESTION [choice, intro, grading=client] Which initializer stores the label argument in self.label and the quantity argument in self.quantity on the new Order instance?
  ✔ o1: def __init__(self, label, quantity):
    self.label = label
    self.quantity = quantity
      why: This matches the stated task and the taught behavior.
  ✘ o2: def __init__(self, label, quantity):
    label = label
    quantity = quantity
      why: Assigning parameter names alone does not store the values as instance attributes.
  ✘ o3: def __init__(self, label, quantity):
    self.label = quantity
    self.quantity = label
      why: The attributes receive the wrong arguments: label and quantity are swapped.
  feedback✔: def __init__(self, label, quantity):
    self.label = label
    self.quantity = quantity  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Follow each constructor argument to its matching self attribute.']  remediation→r01
  MEASURES: A:initialize_attributes_from_constructor_inputs(f1,f2)   anchors=['assessment:initialize_attributes_from_constructor_inputs']
  taught-before-tested: A.f1←s01; A.f2←s01

### s03 · check · Check: Initialising instance state with __init__
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.
QUESTION [choice, core, grading=client] What is the purpose of __init__ when Order is instantiated?
  ✘ o1: Return a different object to replace the new instance.
      why: __init__ initializes the created instance rather than returning a replacement.
  ✘ o2: Create the class object each time an instance is requested.
      why: The class definition creates the class object; __init__ initializes an instance.
  ✔ o3: Initialize the already-created instance, not return a replacement object.
      why: This matches the stated task and the taught behavior.
  feedback✔: Initialize the already-created instance, not return a replacement object.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Distinguish the class, the new instance, and initializing that instance.']
  MEASURES: A:distinguish_initialization_from_returning_a_replacement_object(f3)   anchors=['assessment:distinguish_initialization_from_returning_a_replacement_object']
  taught-before-tested: A.f3←s01

### s04 · hands_on · Store constructor arguments
Practice — Initialize an Order record with a label and quantity supplied as constructor arguments.
QUESTION [code_exercise, core, grading=client] Using the unchanged supplied class, create an instance named order from the fixture’s label and quantity values before the supplied display. Do not substitute fixed values.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['class Order:', 'def __init__(self, label, quantity):', 'self.label = label', 'self.quantity = quantity', 'order = Order("notebook", 3)', 'order.label', 'order.quantity', 'print(order.label, order.quantity)', 'string and integer literals', 'indented class and function bodies'] blocked=13 items
  file main.py [editable]:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\n\ndef prepare_case(inputs):\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [ns["order"].label, ns["order"].quantity, captured.getvalue().strip()]\n')

inputs = {'label': 'notebook', 'quantity': 3}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
# Supplied class/function implementation; leave unchanged.
exec('class Order:\n    def __init__(self, label, quantity):\n        self.label = label\n        self.quantity = quantity\n')
# Create the required instance(s) here using the supplied input names.
print(order.label, order.quantity)
# END LEARNER

  SOLUTION main.py:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\n\ndef prepare_case(inputs):\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [ns["order"].label, ns["order"].quantity, captured.getvalue().strip()]\n')

inputs = {'label': 'notebook', 'quantity': 3}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
# Supplied class/function implementation; leave unchanged.
exec('class Order:\n    def __init__(self, label, quantity):\n        self.label = label\n        self.quantity = quantity\n')
order = Order(label, quantity)
print(order.label, order.quantity)
# END LEARNER

  test t1 (function_call, visible=True): {"function":"check_case","args":[{"label":"notebook","quantity":3}],"expected":["notebook",3,"notebook 3"]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  test t2 (function_call, visible=True): {"function":"check_case","args":[{"label":"blue","quantity":2}],"expected":["blue",2,"blue 2"]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"450ae2e23aa9e5b6d530632348067c3970e6de9761ef27c79ab399237492b788","tests_passed":2}
  feedback✔: The completed code meets the task on the supplied fixtures, including the changed inputs.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Follow the input names rather than substituting a fixed answer.', 'Check the required operation and where its result or resource state is observed.']
  MEASURES: A:initialize_attributes_from_constructor_inputs(f1,f2)   anchors=['practice']
  taught-before-tested: A.f1←s01; A.f2←s01

### s05 · explainer · Instance methods and self
Understand — 
(definition) An instance method receives its target instance as the first argument, conventionally called `self`. ⟦B.f1 B:tb1 B:tb2 B:tb4 B:tb5⟧
(definition) Define `add(self, amount)` inside Order. Use `self.quantity` to read or reassign the receiving instance’s state. ⟦B.f2 B:tb3 B:tb4⟧
(definition) In `order.add(2)`, order is supplied implicitly as self, and the explicit value is supplied as amount. Do not pass order again. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
[CODE python]
class Order:
    def __init__(self, quantity):
        self.quantity = quantity
    def add(self, amount):
        self.quantity = self.quantity + amount

order = Order(3)
order.add(2)
print(order.quantity)
  annotations: ['The first argument is the receiving instance, conventionally self.', 'Read and reassign the receiving instance’s quantity.', 'The target order is implicit self; the explicit argument binds amount.']

### s06 · check · Check: Instance methods and self
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.
QUESTION [choice, core, grading=client] Which method increases the receiving Order instance's quantity by amount?
  ✔ o1: def add(self, amount):
    self.quantity = self.quantity + amount
      why: This matches the stated task and the taught behavior.
  ✘ o2: def add(self, amount):
    quantity = amount
      why: A local quantity name does not reassign the receiving instance's self.quantity.
  ✘ o3: def add(self, amount):
    self.quantity = amount
      why: This replaces quantity with amount rather than increasing the current quantity.
  feedback✔: def add(self, amount):
    self.quantity = self.quantity + amount  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Check both which object is updated and whether its old state is used.']  remediation→r04
  MEASURES: B:define_instance_method_to_read_or_update_receiving_instance(f1,f2)   anchors=['assessment:define_instance_method_to_read_or_update_receiving_instance']
  taught-before-tested: B.f1←s05; B.f2←s05

### s07 · check · Check: Instance methods and self
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.
QUESTION [choice, core, grading=client] For def add(self, amount), what arguments does order.add(2) supply?
  ✘ o1: 2 as self, with no amount argument.
      why: The method receives its target instance implicitly, so 2 is the next argument.
  ✘ o2: No implicit argument; callers must write order.add(order, 2).
      why: An instance-method call supplies order implicitly; passing it again is not required.
  ✔ o3: order implicitly as self, and 2 explicitly as amount.
      why: This matches the stated task and the taught behavior.
  feedback✔: order implicitly as self, and 2 explicitly as amount.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Separate the object before the dot from the value inside the parentheses.']
  MEASURES: B:identify_implicit_instance_and_explicit_argument_in_method_call(f1,f3)   anchors=['assessment:identify_implicit_instance_and_explicit_argument_in_method_call']
  taught-before-tested: B.f1←s05; B.f3←s05

### s08 · hands_on · Update the receiving Order
Practice — Add an add(self, amount) method to Order that increases the receiving object's stored quantity by amount.
QUESTION [code_exercise, core, grading=client] The class implementation is supplied and must remain unchanged. Construct order from quantity before the supplied add(amount) call. Its quantity must reflect that method call.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['class Order:', 'def __init__(self, quantity):', 'def add(self, amount):', 'self.quantity', 'attribute assignment', 'integer literals', '+', 'order = Order(3)', 'order.add(2)', 'order.quantity', 'print(order.quantity)', 'indented class and method bodies'] blocked=11 items
  file main.py [editable]:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\n\ndef prepare_case(inputs):\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [ns["order"].quantity, captured.getvalue().strip()]\n')

inputs = {'quantity': 3, 'amount': 2}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
# Supplied class/function implementation; leave unchanged.
exec('class Order:\n    def __init__(self, quantity):\n        self.quantity = quantity\n    def add(self, amount):\n        self.quantity = self.quantity + amount\n')
# Create the required instance(s) here using the supplied input names.
order.add(amount)
print(order.quantity)
# END LEARNER

  SOLUTION main.py:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\n\ndef prepare_case(inputs):\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [ns["order"].quantity, captured.getvalue().strip()]\n')

inputs = {'quantity': 3, 'amount': 2}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
# Supplied class/function implementation; leave unchanged.
exec('class Order:\n    def __init__(self, quantity):\n        self.quantity = quantity\n    def add(self, amount):\n        self.quantity = self.quantity + amount\n')
order = Order(quantity)
order.add(amount)
print(order.quantity)
# END LEARNER

  test t1 (function_call, visible=True): {"function":"check_case","args":[{"quantity":3,"amount":2}],"expected":[5,"5"]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  test t2 (function_call, visible=True): {"function":"check_case","args":[{"quantity":2,"amount":4}],"expected":[6,"6"]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"eaf4b86e970104c4c40971e6285b9dbeb4a3eec3f71dc6e3095f77c3b8571f00","tests_passed":2}
  feedback✔: The completed code meets the task on the supplied fixtures, including the changed inputs.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Follow the input names rather than substituting a fixed answer.', 'Check the required operation and where its result or resource state is observed.']
  MEASURES: B:define_instance_method_to_read_or_update_receiving_instance(f1,f2); B:identify_implicit_instance_and_explicit_argument_in_method_call(f1,f3)   anchors=['practice']
  taught-before-tested: B.f1←s05; B.f2←s05; B.f1←s05; B.f3←s05

### s09 · explainer · Choosing instance, class or static method binding
Understand — 
(definition) An ordinary instance method receives the instance implicitly and can use that instance’s state. ⟦C.f1 C:tb1 C:tb2 C:tb4⟧
(definition) Put `@classmethod` above `def from_text(cls, text):`. The implicit argument is the class. Returning `cls(int(text))` constructs an instance through an alternative constructor. ⟦C.f2 C:tb1 C:tb3 C:tb4 C:tb5⟧
(definition) Put `@staticmethod` above the method definition for an operation such as cost that receives no implicit instance or class argument. Its arguments are explicit. ⟦C.f3 C:tb1 C:tb3 C:tb4 C:tb5⟧
[CODE python]
class Order:
    def __init__(self, quantity):
        self.quantity = quantity
    @classmethod
    def from_text(cls, text):
        return cls(int(text))
    @staticmethod
    def cost(quantity, price):
        return quantity * price

order = Order.from_text("3")
print(order.quantity)
print(Order.cost(3, 4))
  annotations: ['This decorator supplies the class as cls.', 'Construct through the received class.', 'No implicit instance or class is supplied.', 'Only quantity and price are explicit arguments.']

### s10 · check · Check: Choosing instance, class or static method binding
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.
QUESTION [choice, core, grading=client] Choose the binding pair: add updates one order's state; from_text constructs an Order through cls from a string.
  ✔ o1: add: instance method; from_text: class method.
      why: This matches the stated task and the taught behavior.
  ✘ o2: add: static method; from_text: instance method.
      why: The update needs the receiving instance; construction through cls needs an implicit class.
  ✘ o3: add: class method; from_text: static method.
      why: A class method receives a class, not that order's state; a static method receives no implicit cls.
  feedback✔: add: instance method; from_text: class method.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['For each operation, ask whether it needs an implicit instance or class.']  remediation→r07
  MEASURES: C:select_instance_binding_for_instance_state(f1); C:select_class_binding_for_alternative_construction(f2)   anchors=['assessment:select_instance_binding_for_instance_state', 'assessment:select_class_binding_for_alternative_construction']
  taught-before-tested: C.f1←s09; C.f2←s09

### s11 · check · Check: Choosing instance, class or static method binding
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.
QUESTION [choice, core, grading=client] A cost(quantity) operation needs only its explicit quantity argument, with no implicit instance or class. Which definition matches?
  ✘ o1: @classmethod above def cost(cls, quantity):
      why: A class method receives cls implicitly, contrary to the stated requirement.
  ✘ o2: An ordinary instance method def cost(self, quantity):
      why: An ordinary instance method receives self implicitly, contrary to the stated requirement.
  ✔ o3: @staticmethod above def cost(quantity):
      why: This matches the stated task and the taught behavior.
  feedback✔: @staticmethod above def cost(quantity):  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Consider which decorator removes both kinds of implicit argument.']
  MEASURES: C:select_static_binding_for_operations_without_implicit_state(f3)   anchors=['assessment:select_static_binding_for_operations_without_implicit_state']
  taught-before-tested: C.f3←s09

### s12 · hands_on · Construct through cls
Practice — Implement Order.from_text as a class method that converts a quantity string to an integer and constructs an Order through cls.
QUESTION [code_exercise, stretch, grading=client] The @classmethod implementation and alternate-constructor call are supplied. Assign constructor_text = text from the fixture before that call. Do not convert or replace the fixture text; the supplied method must produce an Order with an integer quantity.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['class Order:', 'def __init__(self, quantity):', 'self.quantity = quantity', '@classmethod', 'def from_text(cls, text):', 'return cls(int(text))', 'int(text)', 'order = Order.from_text("3")', 'order.quantity', 'print(order.quantity)', 'string literals', 'integer literals', 'indented method bodies'] blocked=8 items
  file main.py [editable]:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\n\ndef prepare_case(inputs):\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [type(ns["order"]) is ns["Order"], type(ns["order"].quantity).__name__, ns["order"].quantity, captured.getvalue().strip()]\n')

inputs = {'text': '3'}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
# Supplied class/function implementation; leave unchanged.
exec('class Order:\n    def __init__(self, quantity):\n        self.quantity = quantity\n    @classmethod\n    def from_text(cls, text):\n        return cls(int(text))\n')
constructor_text = None
# Create the required instance(s) here using the supplied input names.
order = Order.from_text(constructor_text)
print(order.quantity)
# END LEARNER

  SOLUTION main.py:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\n\ndef prepare_case(inputs):\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [type(ns["order"]) is ns["Order"], type(ns["order"].quantity).__name__, ns["order"].quantity, captured.getvalue().strip()]\n')

inputs = {'text': '3'}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
# Supplied class/function implementation; leave unchanged.
exec('class Order:\n    def __init__(self, quantity):\n        self.quantity = quantity\n    @classmethod\n    def from_text(cls, text):\n        return cls(int(text))\n')
constructor_text = None
constructor_text = text
order = Order.from_text(constructor_text)
print(order.quantity)
# END LEARNER

  test t1 (function_call, visible=True): {"function":"check_case","args":[{"text":"3"}],"expected":[true,"int",3,"3"]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  test t2 (function_call, visible=True): {"function":"check_case","args":[{"text":"12"}],"expected":[true,"int",12,"12"]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"fde2b802c517fc545958f6b0255c11ba20639ccb699887dc3615ba915d5b6a5d","tests_passed":2}
  feedback✔: The completed code meets the task on the supplied fixtures, including the changed inputs.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Follow the input names rather than substituting a fixed answer.', 'Check the required operation and where its result or resource state is observed.']
  MEASURES: C:select_class_binding_for_alternative_construction(f2)   anchors=['practice']
  taught-before-tested: C.f2←s09

### s13 · recap · Keep these distinctions
Takeaways — 
(takeaway) Storing label on self initializes the Order; returning a replacement object is a different operation. ⟦A.f2 A.f3 A:tb1 A:tb3 A:tb4 A:tb5⟧
(takeaway) In order.add(2), the receiving order is implicit; amount is explicit. ⟦B.f1 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(takeaway) Order.from_text receives cls implicitly; Order.cost receives only its explicit arguments. ⟦C.f2 C.f3 C:tb1 C:tb3 C:tb4 C:tb5⟧
[UP NEXT] Up next: Object composition: Next, begin object composition.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: Initialising instance state with __init__
(definition) When a class defines `__init__`, instantiation automatically calls it on the new instance with the constructor arguments. ⟦A.f1 A:tb1 A:tb2 A:tb4⟧
(definition) Define `__init__(self, label, quantity)` inside Order. Assign `self.label = label` and `self.quantity = quantity` to store those arguments as instance attributes. ⟦A.f2 A:tb1 A:tb3 A:tb4⟧
(misconception) Storing label on self initializes the Order; returning a replacement object is a different operation. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3 A:tb4⟧
### r02 · Revisit: Initialising instance state with __init__
(definition) `__init__` initializes the instance already created. It does not return a replacement object. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Storing label on self initializes the Order; returning a replacement object is a different operation. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
### r03 · Revisit: Initialising instance state with __init__
(definition) When a class defines `__init__`, instantiation automatically calls it on the new instance with the constructor arguments. ⟦A.f1 A:tb1 A:tb2 A:tb4⟧
(definition) Define `__init__(self, label, quantity)` inside Order. Assign `self.label = label` and `self.quantity = quantity` to store those arguments as instance attributes. ⟦A.f2 A:tb1 A:tb3 A:tb4⟧
(definition) `__init__` initializes the instance already created. It does not return a replacement object. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Storing label on self initializes the Order; returning a replacement object is a different operation. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r04 · Revisit: Instance methods and self
(definition) An instance method receives its target instance as the first argument, conventionally called `self`. ⟦B.f1 B:tb1 B:tb2 B:tb4 B:tb5⟧
(definition) Define `add(self, amount)` inside Order. Use `self.quantity` to read or reassign the receiving instance’s state. ⟦B.f2 B:tb3 B:tb4⟧
(misconception) In order.add(2), the receiving order is implicit; amount is explicit. ⟦B.f1 B.f2 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r05 · Revisit: Instance methods and self
(definition) An instance method receives its target instance as the first argument, conventionally called `self`. ⟦B.f1 B:tb1 B:tb2 B:tb4 B:tb5⟧
(definition) In `order.add(2)`, order is supplied implicitly as self, and the explicit value is supplied as amount. Do not pass order again. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) In order.add(2), the receiving order is implicit; amount is explicit. ⟦B.f1 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r06 · Revisit: Instance methods and self
(definition) An instance method receives its target instance as the first argument, conventionally called `self`. ⟦B.f1 B:tb1 B:tb2 B:tb4 B:tb5⟧
(definition) Define `add(self, amount)` inside Order. Use `self.quantity` to read or reassign the receiving instance’s state. ⟦B.f2 B:tb3 B:tb4⟧
(definition) In `order.add(2)`, order is supplied implicitly as self, and the explicit value is supplied as amount. Do not pass order again. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) In order.add(2), the receiving order is implicit; amount is explicit. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r07 · Revisit: Choosing instance, class or static method binding
(definition) An ordinary instance method receives the instance implicitly and can use that instance’s state. ⟦C.f1 C:tb1 C:tb2 C:tb4⟧
(definition) Put `@classmethod` above `def from_text(cls, text):`. The implicit argument is the class. Returning `cls(int(text))` constructs an instance through an alternative constructor. ⟦C.f2 C:tb1 C:tb3 C:tb4 C:tb5⟧
(misconception) Order.from_text receives cls implicitly; Order.cost receives only its explicit arguments. ⟦C.f1 C.f2 C:tb1 C:tb2 C:tb3 C:tb4 C:tb5⟧
### r08 · Revisit: Choosing instance, class or static method binding
(definition) Put `@staticmethod` above the method definition for an operation such as cost that receives no implicit instance or class argument. Its arguments are explicit. ⟦C.f3 C:tb1 C:tb3 C:tb4 C:tb5⟧
(misconception) Order.from_text receives cls implicitly; Order.cost receives only its explicit arguments. ⟦C.f3 C:tb1 C:tb3 C:tb4 C:tb5⟧
### r09 · Revisit: Choosing instance, class or static method binding
(definition) An ordinary instance method receives the instance implicitly and can use that instance’s state. ⟦C.f1 C:tb1 C:tb2 C:tb4⟧
(definition) Put `@classmethod` above `def from_text(cls, text):`. The implicit argument is the class. Returning `cls(int(text))` constructs an instance through an alternative constructor. ⟦C.f2 C:tb1 C:tb3 C:tb4 C:tb5⟧
(definition) Put `@staticmethod` above the method definition for an operation such as cost that receives no implicit instance or class argument. Its arguments are explicit. ⟦C.f3 C:tb1 C:tb3 C:tb4 C:tb5⟧
(misconception) Order.from_text receives cls implicitly; Order.cost receives only its explicit arguments. ⟦C.f1 C.f2 C.f3 C:tb1 C:tb2 C:tb3 C:tb4 C:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: class Subclass(Base):
· constraints.blocked_syntax: class DerivedOrder(Order):
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast

=========

# EVALUATOR PACKET — Object composition / Python encapsulation conventions / Extending inherited behavior with super (learn_python.tile.071_073)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.composition — Object composition
B = python.encapsulation_conventions — Python encapsulation conventions
C = python.inheritance_and_super — Extending inherited behavior with super

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=5
  warn: remediation step learn_python.tile.071_073.r03 is never referenced
  warn: remediation step learn_python.tile.071_073.r05 is never referenced
  warn: learn_python.tile.071_073.s03/ix.learn_python.tile.071_073.s03: ADVISORY — syntax descriptors with no detector: ['@property', '__init__', '__repr__', '__str__', 'assert', 'class definitions with base classes', 'class definitions without base classes', 'def and instance-method parameters', 'integer and string literals', 'method calls with arguments', 'multiplication', 'object construction', 'with', 'yield', 'yield from']
  warn: learn_python.tile.071_073.s06/ix.learn_python.tile.071_073.s06: ADVISORY — syntax descriptors with no detector: ['addition with +', 'assert statements', 'class Order:', 'class-level attribute assignments', 'generator expressions', 'instance attribute assignment', 'integer literals', 'return statements', 'yield expressions']
  warn: learn_python.tile.071_073.s10/ix.learn_python.tile.071_073.s10: ADVISORY — syntax descriptors with no detector: ['assert statements', 'class Order:', 'class-level attribute assignments', 'custom exception class definitions', 'generator expressions', 'instance attribute access', 'instance construction', 'instance method calls', 'string and integer literals', 'string concatenation with +', 'yield expressions']

## SOURCE FACTS — A (python.composition)   objective: Combine collaborating objects through composition.
A.f1: Instance data attributes can hold collaborator objects.   [sources: python_tutorial#classes.html#instance-objects]
A.f2: Store a collaborator as self.collaborator and invoke self.collaborator.method(arguments) from an instance method to delegate work to that object.   [sources: python_tutorial#classes.html#method-objects]
note: Begin with this objective: Combine collaborating objects through composition.
note: Keep the example in the Organizing object relationships tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.encapsulation_conventions, python.inheritance_and_super, python.custom_exceptions.
PRACTICE ANCHOR (live_code): Give a Report object a formatter collaborator, store it as instance data, and delegate formatting to it from an instance method.  SUCCESS: Report stores the formatter object and calls its method with quantity. Calling report.total(3) returns "Total: 12", with the formatting performed by the collaborator.
ASSESSMENT ANCHOR: delegate_an_operation_to_a_contained_collaborator_without_inheritance facts=['f1', 'f2']

## SOURCE FACTS — B (python.encapsulation_conventions)   objective: Apply Python conventions for non-public object state.
B.f1: A leading underscore conventionally marks a non-public implementation name; it does not enforce access protection.   [sources: python_tutorial#classes.html#private-variables]
B.f2: Python does not provide truly inaccessible private instance attributes through this naming convention.   [sources: python_tutorial#classes.html#private-variables]
B.f3: Public attributes form the interface expected to be used by clients; keep implementation details non-public with a leading underscore.   [sources: pep8_style_guide#designing-for-inheritance]
B.f4: Expose a public method that operates on the receiving instance’s supporting attributes instead of requiring callers to manage that state directly.   [sources: python_tutorial#classes.html#method-objects]
note: Begin with this objective: Apply Python conventions for non-public object state.
note: Keep the example in the Organizing object relationships tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.inheritance_and_super, python.custom_exceptions, python.instance_vs_class_attributes.
PRACTICE ANCHOR (live_code): Expose Order.add(amount) as a public operation and mark its supporting quantity attribute non-public with a leading underscore.  SUCCESS: Order stores quantity in self._quantity, and add updates and returns that state. Calling order.add(2) on Order(3) returns 5 without the caller directly managing _quantity.
ASSESSMENT ANCHOR: distinguish_non_public_naming_from_access_protection facts=['f1', 'f2']
ASSESSMENT ANCHOR: separate_public_operations_from_supporting_state facts=['f3', 'f4']

## SOURCE FACTS — C (python.inheritance_and_super)   objective: Extend inherited behavior using super().
C.f1: Define class Derived(Base): to inherit from Base; an overridden method replaces the inherited method for ordinary lookup on Derived instances.   [sources: python_tutorial#classes.html#inheritance]
C.f2: Inside an ordinary derived instance method, super().method(arguments) delegates lookup to the next class in method resolution order.   [sources: python_stdlib_reference#functions.html#super]
C.f3: In a derived __init__, call super().__init__(arguments) to run inherited initialization before adding derived initialization where required.   [sources: python_tutorial#classes.html#class-objects, python_stdlib_reference#functions.html#super]
note: Begin with this objective: Extend inherited behavior using super().
note: Keep the example in the Organizing object relationships tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.custom_exceptions, python.instance_vs_class_attributes, python.json_serialization.
PRACTICE ANCHOR (live_code): Extend an Order formatter with a FeeOrder formatter: preserve inherited quantity initialization, store fee, and extend the inherited formatted result through super().  SUCCESS: Creating FeeOrder(3, 2) preserves quantity as 3 and fee as 2. Its overridden formatting method returns the inherited quantity text followed by the fee text.
ASSESSMENT ANCHOR: override_method_and_delegate_inherited_behavior facts=['f1', 'f2']
ASSESSMENT ANCHOR: preserve_inherited_initialization facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing environment variables with os.environ; Choosing explicit text-file encodings; Choosing random or secrets for randomness; Computing dates and elapsed times with datetime; Creating isolated virtual environments; Creating local modules; Defining custom exceptions; Defining useful object representations with special methods; Diagnosing module search-path problems; Extending inherited behavior with super; Guarding a program entry point; Handling file and data-format failures; Inspecting interpreter runtime information with sys; Inspecting object types and attributes; Installing dependencies with python -m pip; Instance versus class attributes; Managing resources with with; Matching text patterns with re; Organising importable packages; Parsing command-line arguments with argparse; Performing filesystem operations with pathlib; Python encapsulation conventions; Reading and writing binary files; Recording program events with logging; Recreating dependencies from requirements files; Selecting the project environment interpreter; Serialising and deserialising data with Python json

## LESSON, in learner order

### s01 · explainer · Object composition
Understand — 
(definition) An instance attribute can hold another object as a collaborator, rather than holding the result of its work. ⟦A.f1 A:tb1 A:tb2 A:tb4 A:tb5⟧
(definition) Store the Calculator object as `self.calculator`. Within Report’s method, call `self.calculator.cost(quantity)` to delegate work through the stored object. ⟦A.f2 A:tb1 A:tb3 A:tb4 A:tb5⟧
[CODE python]
class Calculator:
    def cost(self, quantity):
        return quantity * 4

class Report:
    def __init__(self, calculator):
        self.calculator = calculator
    def total(self, quantity):
        return self.calculator.cost(quantity)

report = Report(Calculator())
print(report.total(3))
  annotations: ['Keep the collaborator object as instance data.', 'Delegate through the stored Calculator object.']

### s02 · check · Check: Object composition
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.
QUESTION [choice, intro, grading=client] Report receives a calculator collaborator. Which implementation stores that object and delegates cost(quantity) to it, without inheritance?
  ✔ o1: Store self.calculator = calculator; total returns self.calculator.cost(quantity).
      why: This matches the stated task and the taught behavior.
  ✘ o2: Store self.calculator = calculator.cost(3); total returns self.calculator.
      why: This stores one computed result, not the collaborator object, and does not delegate each operation.
  ✘ o3: Ignore calculator; total returns quantity * 4.
      why: This performs the calculation inside Report rather than delegating to its contained collaborator.
  feedback✔: Store self.calculator = calculator; total returns self.calculator.cost(quantity).  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Look for both a stored object and a method call on that object.']  remediation→r01
  MEASURES: A:delegate_an_operation_to_a_contained_collaborator_without_inheritance(f1,f2)   anchors=['assessment:delegate_an_operation_to_a_contained_collaborator_without_inheritance']
  taught-before-tested: A.f1←s01; A.f2←s01

### s03 · hands_on · Replace the collaborator
Practice — Give a Report object a formatter collaborator, store it as instance data, and delegate formatting to it from an instance method.
QUESTION [code_exercise, core, grading=client] The collaborator and Report implementations are supplied. Assign report_formatter = formatter so the supplied Report construction stores that collaborator. Preserve the delegated total(quantity) call and output. The formatter, not Report, must perform the formatting.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['class definitions without base classes', 'def and instance-method parameters', '__init__', 'self.attribute assignment and access', 'variable assignment', 'object construction', 'method calls with arguments', 'return', 'integer and string literals', 'multiplication', 'f-strings', 'print()'] blocked=12 items
  file main.py [editable]:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\n\ndef prepare_case(inputs):\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [ns["report"].formatter is ns["formatter"], ns["result"], captured.getvalue().strip()]\n')

inputs = {'quantity': 3}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
# Supplied class/function implementation; leave unchanged.
exec('class Formatter:\n    def format(self, quantity):\n        return f"Total: {quantity * 4}"\n\nclass Report:\n    def __init__(self, formatter):\n        self.formatter = formatter\n    def total(self, quantity):\n        return self.formatter.format(quantity)\n')
formatter = Formatter()
# Create the required instance(s) here using the supplied input names.
report = Report(report_formatter)
result = report.total(quantity)
print(result)
# END LEARNER

  SOLUTION main.py:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\n\ndef prepare_case(inputs):\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [ns["report"].formatter is ns["formatter"], ns["result"], captured.getvalue().strip()]\n')

inputs = {'quantity': 3}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
# Supplied class/function implementation; leave unchanged.
exec('class Formatter:\n    def format(self, quantity):\n        return f"Total: {quantity * 4}"\n\nclass Report:\n    def __init__(self, formatter):\n        self.formatter = formatter\n    def total(self, quantity):\n        return self.formatter.format(quantity)\n')
formatter = Formatter()
report_formatter = formatter
report = Report(report_formatter)
result = report.total(quantity)
print(result)
# END LEARNER

  test t1 (function_call, visible=True): {"function":"check_case","args":[{"quantity":3}],"expected":[true,"Total: 12","Total: 12"]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  test t2 (function_call, visible=True): {"function":"check_case","args":[{"quantity":2}],"expected":[true,"Total: 8","Total: 8"]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"ebb2d318ab05ac15897b860398fbd2933b044a6e2e5cf35ecc4a162b51d4ab7a","tests_passed":2}
  feedback✔: The completed code meets the task on the supplied fixtures, including the changed inputs.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Follow the input names rather than substituting a fixed answer.', 'Check the required operation and where its result or resource state is observed.']
  MEASURES: A:delegate_an_operation_to_a_contained_collaborator_without_inheritance(f1,f2)   anchors=['practice']
  taught-before-tested: A.f1←s01; A.f2←s01

### s04 · explainer · Python encapsulation conventions
Understand — 
(definition) A leading underscore marks a name as conventionally non-public. It is not an access restriction. ⟦B.f1 B:tb1 B:tb2 B:tb4 B:tb5⟧
(definition) This naming convention does not make Python instance attributes truly inaccessible. ⟦B.f2 B:tb1 B:tb3 B:tb4 B:tb5⟧
(definition) Public attributes are the interface clients are expected to use. Mark implementation details with a leading underscore. ⟦B.f3 B:tb1 B:tb3 B:tb4⟧
(definition) Expose a public method such as `add` that operates on the receiving instance’s supporting attributes. Callers need not manage `_quantity` directly. ⟦B.f4 B:tb3 B:tb4⟧
[CODE python]
class Order:
    def __init__(self, quantity):
        self._quantity = quantity
    def add(self, amount):
        self._quantity = self._quantity + amount
        return self._quantity

order = Order(3)
print(order.add(2))
  annotations: ['The underscore signals supporting state, not enforced access protection.', 'Public operation for clients.', 'The caller uses the public interface.']

### s05 · check · Check: Python encapsulation conventions
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.
QUESTION [choice, core, grading=client] What does the name order._quantity communicate in Python?
  ✘ o1: It promises callers that the attribute is the public interface.
      why: The underscore convention signals internal implementation use rather than the client interface.
  ✔ o2: It conventionally marks supporting state as non-public, but does not enforce access protection.
      why: This matches the stated task and the taught behavior.
  ✘ o3: It makes the attribute inaccessible from outside Order.
      why: A leading underscore is a convention, not an enforced access restriction.
  feedback✔: It conventionally marks supporting state as non-public, but does not enforce access protection.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Separate a naming convention from an access restriction.']  remediation→r02
  MEASURES: B:distinguish_non_public_naming_from_access_protection(f1,f2)   anchors=['assessment:distinguish_non_public_naming_from_access_protection']
  taught-before-tested: B.f1←s04; B.f2←s04

### s06 · hands_on · Expose the public operation
Practice — Expose Order.add(amount) as a public operation and mark its supporting quantity attribute non-public with a leading underscore.
QUESTION [code_exercise, core, grading=client] The class implementation is supplied and must remain unchanged. Construct order from quantity. The supplied add(amount) call must update and return its conventionally internal state.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['class Order:', 'def __init__(self, quantity):', 'def add(self, amount):', 'self.quantity', 'self._quantity', 'instance attribute assignment', 'integer literals', 'addition with +', 'return statements', 'order = Order(3)', 'order.add(2)', 'print()'] blocked=12 items
  file main.py [editable]:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\n\ndef prepare_case(inputs):\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [ns["order"]._quantity, ns["result"], "quantity" in vars(ns["order"]), captured.getvalue().strip()]\n')

inputs = {'quantity': 3, 'amount': 2}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
# Supplied class/function implementation; leave unchanged.
exec('class Order:\n    def __init__(self, quantity):\n        self._quantity = quantity\n    def add(self, amount):\n        self._quantity = self._quantity + amount\n        return self._quantity\n')
# Create the required instance(s) here using the supplied input names.
result = order.add(amount)
print(result)
# END LEARNER

  SOLUTION main.py:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\n\ndef prepare_case(inputs):\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [ns["order"]._quantity, ns["result"], "quantity" in vars(ns["order"]), captured.getvalue().strip()]\n')

inputs = {'quantity': 3, 'amount': 2}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
# Supplied class/function implementation; leave unchanged.
exec('class Order:\n    def __init__(self, quantity):\n        self._quantity = quantity\n    def add(self, amount):\n        self._quantity = self._quantity + amount\n        return self._quantity\n')
order = Order(quantity)
result = order.add(amount)
print(result)
# END LEARNER

  test t1 (function_call, visible=True): {"function":"check_case","args":[{"quantity":3,"amount":2}],"expected":[5,5,false,"5"]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  test t2 (function_call, visible=True): {"function":"check_case","args":[{"quantity":2,"amount":4}],"expected":[6,6,false,"6"]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"d1cebd73cf935cf3a51d85dc26db10cb54e630f4ff890ea8db92e6b0f51ac400","tests_passed":2}
  feedback✔: The completed code meets the task on the supplied fixtures, including the changed inputs.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Follow the input names rather than substituting a fixed answer.', 'Check the required operation and where its result or resource state is observed.']
  MEASURES: B:separate_public_operations_from_supporting_state(f3,f4)   anchors=['practice', 'assessment:separate_public_operations_from_supporting_state']
  taught-before-tested: B.f3←s04; B.f4←s04

### s07 · explainer · Extending inherited behavior with super
Understand — 
(definition) `class FeeOrder(Order):` inherits from Order. An override replaces the inherited method for ordinary lookup on FeeOrder instances. ⟦C.f1 C:tb2 C:tb4⟧
(definition) Inside an ordinary derived instance method, `super().method(arguments)` delegates lookup to the next class in method resolution order, not unconditionally to a fixed named parent. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
(definition) In the derived initializer, use `super().__init__(quantity)` to run inherited initialization before adding the derived fee state where required. ⟦C.f3 C:tb3 C:tb4⟧
[CODE python]
class Order:
    def __init__(self, quantity):
        self.quantity = quantity

    def format(self):
        return f"Quantity: {self.quantity}"

class FeeOrder(Order):
    def __init__(self, quantity, fee):
        super().__init__(quantity)
        self.fee = fee
    def format(self):
        return super().format() + f", fee: {self.fee}"

print(FeeOrder(3, 2).format())
  annotations: ['Inherited initialization precedes the added fee state.', 'Delegate lookup to the next class in method resolution order, then extend its formatting.']

### s08 · video · Preserving inherited initialization with super()
Observe — 
[VIDEO Preserving inherited initialization with super()] bridge-before: Watch how Developer delegates shared initialization before storing its additional value. The clip calls Employee the parent; Devspace describes super() more precisely as lookup delegation to the next class in method resolution order. The claim that super() is necessary for multiple inheritance is too strong: it supports cooperative delegation but is not mandatory. | bridge-after: The clip demonstrates inherited initialization, but does not teach ordinary method overriding or next-class lookup semantics. The text covers both, using FeeOrder.cost() to extend inherited behavior.
  - RSl87lqOXDE 373-610s facts=['f3'] label: Extend inherited initialization with super().__init__() | summary: A Developer needs the first name, last name and pay accepted by Employee, plus a programming language. Its own __init__ delegates the shared arguments through super().__init__ rather than duplicating Employee's initialization logic, then stores the programming language. Creating a Developer and displaying its email and programming language confirms that both inherited and derived initialization ran. In this single-base example, the delegated initialization is Employee's implementation.

### s09 · check · Check: Extending inherited behavior with super
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.
QUESTION [choice, core, grading=client] Order.__init__(quantity) stores quantity. FeeOrder.__init__(quantity, fee) must preserve that initialization before storing fee. Which sequence matches?
  ✘ o1: self.fee = fee only.
      why: Adding fee alone does not run the inherited quantity initializer.
  ✘ o2: super().format(), then self.fee = fee.
      why: Delegating formatting is not delegating initialization; use the inherited initializer.
  ✔ o3: super().__init__(quantity), then self.fee = fee.
      why: This matches the stated task and the taught behavior.
  feedback✔: super().__init__(quantity), then self.fee = fee.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Choose the inherited operation appropriate to construction, not display.']  remediation→r04
  MEASURES: C:preserve_inherited_initialization(f3)   anchors=['assessment:preserve_inherited_initialization']
  taught-before-tested: C.f3←s07

### s10 · hands_on · Extend Order behavior
Practice — Extend an Order formatter with a FeeOrder formatter: preserve inherited quantity initialization, store fee, and extend the inherited formatted result through super().
QUESTION [code_exercise, intro, grading=client] The class implementation is supplied and must remain unchanged. Create order = FeeOrder(quantity, fee). The supplied display must preserve the inherited quantity text and append the fee text.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['class Order:', 'class FeeOrder(Order):', 'def __init__(self, quantity):', 'def __init__(self, quantity, fee):', 'def format(self):', 'self.quantity = quantity', 'self.fee = fee', 'super().__init__(quantity)', 'super().format()', 'return', 'f-strings', 'string concatenation with +', 'string and integer literals', 'instance construction', 'instance attribute access', 'instance method calls', 'variable assignment', 'print()'] blocked=8 items
  file main.py [editable]:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\n\ndef prepare_case(inputs):\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [ns["order"].quantity, ns["order"].fee, ns["order"].format(), captured.getvalue().strip()]\n')

inputs = {'quantity': 3, 'fee': 2}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
# Supplied class/function implementation; leave unchanged.
exec('class Order:\n    def __init__(self, quantity):\n        self.quantity = quantity\n    def format(self):\n        return f"Quantity: {self.quantity}"\n\nclass FeeOrder(Order):\n    def __init__(self, quantity, fee):\n        super().__init__(quantity)\n        self.fee = fee\n    def format(self):\n        return super().format() + f", fee: {self.fee}"\n')
# Create the required instance(s) here using the supplied input names.
print(order.format())
# END LEARNER

  SOLUTION main.py:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\n\ndef prepare_case(inputs):\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [ns["order"].quantity, ns["order"].fee, ns["order"].format(), captured.getvalue().strip()]\n')

inputs = {'quantity': 3, 'fee': 2}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
# Supplied class/function implementation; leave unchanged.
exec('class Order:\n    def __init__(self, quantity):\n        self.quantity = quantity\n    def format(self):\n        return f"Quantity: {self.quantity}"\n\nclass FeeOrder(Order):\n    def __init__(self, quantity, fee):\n        super().__init__(quantity)\n        self.fee = fee\n    def format(self):\n        return super().format() + f", fee: {self.fee}"\n')
order = FeeOrder(quantity, fee)
print(order.format())
# END LEARNER

  test t1 (function_call, visible=True): {"function":"check_case","args":[{"quantity":3,"fee":2}],"expected":[3,2,"Quantity: 3, fee: 2","Quantity: 3, fee: 2"]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  test t2 (function_call, visible=True): {"function":"check_case","args":[{"quantity":2,"fee":4}],"expected":[2,4,"Quantity: 2, fee: 4","Quantity: 2, fee: 4"]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"86d841104ad722e21f63bade5617465c67e838aaa89fd909730124ea74b4a8ad","tests_passed":2}
  feedback✔: The completed code meets the task on the supplied fixtures, including the changed inputs.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Follow the input names rather than substituting a fixed answer.', 'Check the required operation and where its result or resource state is observed.']
  MEASURES: C:override_method_and_delegate_inherited_behavior(f1,f2); C:preserve_inherited_initialization(f3)   anchors=['practice', 'assessment:override_method_and_delegate_inherited_behavior', 'assessment:preserve_inherited_initialization']
  taught-before-tested: C.f1←s07; C.f2←s07; C.f3←s07

### s11 · recap · Keep these distinctions
Takeaways — 
(takeaway) Report stores the Calculator object and calls through it, not through a saved cost result. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Use order.add to operate on _quantity; the underscore signals internal use, not a locked attribute. ⟦B.f1 B.f2 B.f3 B.f4 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(takeaway) FeeOrder extends inherited initialization and formatting through super rather than treating super as a fixed-parent name. ⟦C.f2 C.f3 C:tb3 C:tb4 C:tb5⟧
[UP NEXT] Up next: Defining custom exceptions: Next, begin defining custom exceptions.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: Object composition
(definition) An instance attribute can hold another object as a collaborator, rather than holding the result of its work. ⟦A.f1 A:tb1 A:tb2 A:tb4 A:tb5⟧
(definition) Store the Calculator object as `self.calculator`. Within Report’s method, call `self.calculator.cost(quantity)` to delegate work through the stored object. ⟦A.f2 A:tb1 A:tb3 A:tb4 A:tb5⟧
(misconception) Report stores the Calculator object and calls through it, not through a saved cost result. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit: Python encapsulation conventions
(definition) A leading underscore marks a name as conventionally non-public. It is not an access restriction. ⟦B.f1 B:tb1 B:tb2 B:tb4 B:tb5⟧
(definition) This naming convention does not make Python instance attributes truly inaccessible. ⟦B.f2 B:tb1 B:tb3 B:tb4 B:tb5⟧
(misconception) Use order.add to operate on _quantity; the underscore signals internal use, not a locked attribute. ⟦B.f1 B.f2 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r03 · Revisit: Python encapsulation conventions
(definition) Public attributes are the interface clients are expected to use. Mark implementation details with a leading underscore. ⟦B.f3 B:tb1 B:tb3 B:tb4⟧
(definition) Expose a public method such as `add` that operates on the receiving instance’s supporting attributes. Callers need not manage `_quantity` directly. ⟦B.f4 B:tb3 B:tb4⟧
(misconception) Use order.add to operate on _quantity; the underscore signals internal use, not a locked attribute. ⟦B.f3 B.f4 B:tb1 B:tb3 B:tb4⟧
### r04 · Revisit: Extending inherited behavior with super
(definition) In the derived initializer, use `super().__init__(quantity)` to run inherited initialization before adding the derived fee state where required. ⟦C.f3 C:tb3 C:tb4⟧
(misconception) FeeOrder extends inherited initialization and formatting through super rather than treating super as a fixed-parent name. ⟦C.f3 C:tb3 C:tb4⟧
### r05 · Revisit: Extending inherited behavior with super
(definition) `class FeeOrder(Order):` inherits from Order. An override replaces the inherited method for ordinary lookup on FeeOrder instances. ⟦C.f1 C:tb2 C:tb4⟧
(definition) Inside an ordinary derived instance method, `super().method(arguments)` delegates lookup to the next class in method resolution order, not unconditionally to a fixed named parent. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
(definition) In the derived initializer, use `super().__init__(quantity)` to run inherited initialization before adding the derived fee state where required. ⟦C.f3 C:tb3 C:tb4⟧
(misconception) FeeOrder extends inherited initialization and formatting through super rather than treating super as a fixed-parent name. ⟦C.f1 C.f2 C.f3 C:tb2 C:tb3 C:tb4 C:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast

=========

# EVALUATOR PACKET — Defining custom exceptions (learn_python.tile.074_074)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.custom_exceptions — Defining custom exceptions

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: remediation step learn_python.tile.074_074.r02 is never referenced
  warn: learn_python.tile.074_074.s03/ix.learn_python.tile.074_074.s03: ADVISORY — syntax descriptors with no detector: ['assert ...', 'except InvalidRecordError:', 'generator expressions', 'if __name__ == "__main__":', 'if quantity < 0:', 'integer literals', 'pass', 'return quantity', 'string literals', 'with ... as ...:', 'yield ...']

## SOURCE FACTS — A (python.custom_exceptions)   objective: Define an application-specific exception type.
A.f1: Define an application-specific exception as a class derived from Exception, using class CustomError(Exception): with an indented pass body.   [sources: python_tutorial#errors.html#user-defined-exceptions]
A.f2: raise CustomError(message) signals that custom failure; except CustomError: handles it at a surrounding boundary.   [sources: python_tutorial#errors.html#raising-exceptions, python_tutorial#errors.html#handling-exceptions]
note: Begin with this objective: Define an application-specific exception type.
note: Keep the example in the Custom exceptions tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.instance_vs_class_attributes, python.json_serialization, python.object_introspection.
PRACTICE ANCHOR (live_code): Define InvalidRecordError as an Exception subclass and use it in check_quantity(quantity) to reject a negative quantity, handling the failure around the validator call.  SUCCESS: A nonnegative quantity is returned unchanged. A negative quantity raises InvalidRecordError with a message, and the surrounding except InvalidRecordError handler displays a rejection message.
ASSESSMENT ANCHOR: define_application_specific_exception facts=['f1']
ASSESSMENT ANCHOR: raise_and_catch_custom_exception_at_boundary facts=['f2']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing environment variables with os.environ; Choosing explicit text-file encodings; Choosing random or secrets for randomness; Computing dates and elapsed times with datetime; Creating isolated virtual environments; Creating local modules; Defining useful object representations with special methods; Development checks with the Python assert statement; Diagnosing module search-path problems; Guarding a program entry point; Handling file and data-format failures; Inspecting interpreter runtime information with sys; Inspecting object types and attributes; Installing dependencies with python -m pip; Instance versus class attributes; Managing resources with with; Matching text patterns with re; Organising importable packages; Parsing command-line arguments with argparse; Performing filesystem operations with pathlib; Reading and writing binary files; Recording program events with logging; Recreating dependencies from requirements files; Selecting the project environment interpreter; Serialising and deserialising data with Python json

## LESSON, in learner order

### s01 · explainer · Defining custom exceptions
Understand — 
(definition) Define an application-specific exception with `class InvalidRecordError(Exception):` and an indented `pass` body. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) `raise InvalidRecordError(message)` signals the custom failure. A surrounding `except InvalidRecordError:` handles that failure at the caller’s recovery boundary. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
[CODE python]
class InvalidRecordError(Exception):
    pass

def check_quantity(quantity):
    if quantity < 0:
        raise InvalidRecordError("negative quantity")
    return quantity

try:
    check_quantity(-1)
except InvalidRecordError:
    print("Order rejected")
  annotations: ['Exception subclass with an empty body.', 'Negative quantity signals the application-specific failure.', 'The surrounding boundary handles the matching custom failure.']

### s02 · check · Check: Defining custom exceptions
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.
QUESTION [choice, intro, grading=client] check_quantity raises InvalidRecordError. Which placement handles that custom failure at the caller's recovery boundary?
  ✔ o1: A try around the validator call, followed by except InvalidRecordError:.
      why: This matches the stated task and the taught behavior.
  ✘ o2: An except FileExistsError: around the validator call.
      why: The raised custom failure needs its matching handler; FileExistsError is a different failure type.
  ✘ o3: Define InvalidRecordError but call the validator without a surrounding handler.
      why: Defining the type does not itself handle a failure raised by the validator.
  feedback✔: A try around the validator call, followed by except InvalidRecordError:.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Distinguish defining, raising, and handling an exception.']  remediation→r01
  MEASURES: A:raise_and_catch_custom_exception_at_boundary(f2)   anchors=['assessment:raise_and_catch_custom_exception_at_boundary']
  taught-before-tested: A.f2←s01

### s03 · hands_on · Signal and handle an invalid record
Practice — Define InvalidRecordError as an Exception subclass and use it in check_quantity(quantity) to reject a negative quantity, handling the failure around the validator call.
QUESTION [code_exercise, stretch, grading=client] Choose the exception class for error_type so the unchanged validator’s negative-quantity failure reaches the supplied InvalidRecordError handler. Negative quantities must display ‘Order rejected’; nonnegative quantities must return unchanged. Leave the validator and handler unchanged.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['class InvalidRecordError(Exception):', 'pass', 'def check_quantity(quantity):', 'if quantity < 0:', 'raise InvalidRecordError("negative quantity")', 'return quantity', 'try:', 'except InvalidRecordError:', 'check_quantity(...)', 'print(...)', 'variable assignment', 'integer literals', 'string literals'] blocked=5 items
  file main.py [editable]:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\ndef validation_probe(ns, quantity):\n    try:\n        value = ns["check_quantity"](quantity)\n        return ["returned", value]\n    except ns["InvalidRecordError"] as error:\n        return [type(error).__name__, str(error)]\n\n\ndef prepare_case(inputs):\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [captured.getvalue().strip(), validation_probe(ns, inputs["quantity"])]\n')

inputs = {'quantity': 2}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
# Supplied class/function implementation; leave unchanged.
exec('class InvalidRecordError(Exception):\n    pass\n\ndef check_quantity(quantity):\n    if quantity < 0:\n        raise error_type("negative quantity")\n    return quantity\n')
error_type = ValueError
try:
    result = check_quantity(quantity)
    print(result)
except InvalidRecordError:
    print("Order rejected")
# END LEARNER

  SOLUTION main.py:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\ndef validation_probe(ns, quantity):\n    try:\n        value = ns["check_quantity"](quantity)\n        return ["returned", value]\n    except ns["InvalidRecordError"] as error:\n        return [type(error).__name__, str(error)]\n\n\ndef prepare_case(inputs):\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [captured.getvalue().strip(), validation_probe(ns, inputs["quantity"])]\n')

inputs = {'quantity': 2}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
# Supplied class/function implementation; leave unchanged.
exec('class InvalidRecordError(Exception):\n    pass\n\ndef check_quantity(quantity):\n    if quantity < 0:\n        raise error_type("negative quantity")\n    return quantity\n')
error_type = InvalidRecordError
try:
    result = check_quantity(quantity)
    print(result)
except InvalidRecordError:
    print("Order rejected")
# END LEARNER

  test t1 (function_call, visible=True): {"function":"check_case","args":[{"quantity":2}],"expected":["2",["returned",2]]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  test t2 (function_call, visible=True): {"function":"check_case","args":[{"quantity":0}],"expected":["0",["returned",0]]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  test t3 (function_call, visible=True): {"function":"check_case","args":[{"quantity":-1}],"expected":["Order rejected",["InvalidRecordError","negative quantity"]]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  test t4 (function_call, visible=True): {"function":"check_case","args":[{"quantity":-3}],"expected":["Order rejected",["InvalidRecordError","negative quantity"]]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"aaa3cbd3765b31d8006cfaf5e8c39d15ef12f2ceef8765952e94b6bc11ac672a","tests_passed":4}
  feedback✔: The completed code meets the task on the supplied fixtures, including the changed inputs.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Follow the input names rather than substituting a fixed answer.', 'Check the required operation and where its result or resource state is observed.']
  MEASURES: A:define_application_specific_exception(f1); A:raise_and_catch_custom_exception_at_boundary(f2)   anchors=['practice', 'assessment:define_application_specific_exception', 'assessment:raise_and_catch_custom_exception_at_boundary']
  taught-before-tested: A.f1←s01; A.f2←s01

### s04 · recap · Keep these distinctions
Takeaways — 
(takeaway) A raised InvalidRecordError reaches its matching handler; printing a failure label alone does not signal that exception. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Instance versus class attributes: Next, begin instance versus class attributes.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: Defining custom exceptions
(definition) `raise InvalidRecordError(message)` signals the custom failure. A surrounding `except InvalidRecordError:` handles that failure at the caller’s recovery boundary. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) A raised InvalidRecordError reaches its matching handler; printing a failure label alone does not signal that exception. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit: Defining custom exceptions
(definition) Define an application-specific exception with `class InvalidRecordError(Exception):` and an indented `pass` body. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) `raise InvalidRecordError(message)` signals the custom failure. A surrounding `except InvalidRecordError:` handles that failure at the caller’s recovery boundary. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) A raised InvalidRecordError reaches its matching handler; printing a failure label alone does not signal that exception. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast

=========

# EVALUATOR PACKET — Instance versus class attributes (learn_python.tile.075_075)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.instance_vs_class_attributes — Instance versus class attributes

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: remediation step learn_python.tile.075_075.r02 is never referenced
  warn: learn_python.tile.075_075.s04/ix.learn_python.tile.075_075.s04: ADVISORY — syntax descriptors with no detector: ['assert', 'class Order:', 'labels = []', 'with', 'yield']

## SOURCE FACTS — A (python.instance_vs_class_attributes)   objective: Distinguish instance state from shared class attributes.
A.f1: Class variables hold attributes shared by instances, while instance variables hold data unique to an instance.   [sources: python_tutorial#classes.html#class-and-instance-variables]
A.f2: A mutable list assigned in the class body is shared unless shadowed by an instance attribute.   [sources: python_tutorial#classes.html#class-and-instance-variables]
A.f3: Assign self.items = [] in __init__ to create a separate list for each instance rather than mutating a shared class list.   [sources: python_tutorial#classes.html#class-and-instance-variables]
note: Begin with this objective: Distinguish instance state from shared class attributes.
note: Keep the example in the Instance versus class attributes tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.json_serialization, python.object_introspection, python.pathlib_filesystem_operations.
PRACTICE ANCHOR (live_code): Move a mistakenly shared labels list from the Order class body into instance initialization as self.labels = [].  SUCCESS: After creating first and second and appending "blue" to first.labels, first.labels contains ["blue"] and second.labels remains empty.
ASSESSMENT ANCHOR: distinguish_shared_and_per_instance_attributes facts=['f1']
ASSESSMENT ANCHOR: predict_shared_list_mutation_and_instance_shadowing facts=['f2']
ASSESSMENT ANCHOR: correct_accidentally_shared_mutable_state facts=['f2', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing environment variables with os.environ; Choosing explicit text-file encodings; Choosing random or secrets for randomness; Computing dates and elapsed times with datetime; Creating isolated virtual environments; Creating local modules; Defining useful object representations with special methods; Development checks with the Python assert statement; Diagnosing module search-path problems; Guarding a program entry point; Handling file and data-format failures; Inspecting interpreter runtime information with sys; Inspecting object types and attributes; Installing dependencies with python -m pip; Iterables and iterators; Managing resources with with; Matching text patterns with re; Organising importable packages; Parsing command-line arguments with argparse; Performing filesystem operations with pathlib; Reading and writing binary files; Recording program events with logging; Recreating dependencies from requirements files; Selecting the project environment interpreter; Serialising and deserialising data with Python json

## LESSON, in learner order

### s01 · explainer · Instance versus class attributes
Understand — 
(definition) Class variables hold attributes shared by instances; instance variables hold data unique to an instance. ⟦A.f1 A:tb1 A:tb2 A:tb4⟧
(definition) A mutable list assigned in the class body is shared by instances unless an instance attribute shadows it. ⟦A.f2 A:tb1 A:tb3 A:tb4 A:tb5⟧
(definition) Assign `self.labels = []` in `__init__` for a new list on each instance. Then updating first’s list does not mutate a shared class list. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[SIDE_BY_SIDE] Move labels initialization onto self to isolate each Order’s mutable state. left_label: Shared class list | right_label: Separate instance lists
  left:
[CODE python]
class Order:
    labels = []

first = Order()
second = Order()
first.labels.append("blue")
print(first.labels)
print(second.labels)
  annotations: ['Class-body list shared unless shadowed.', 'Mutates the shared list.', "Prints ['blue'].", "Prints ['blue']."]
  right:
[CODE python]
class Order:
    def __init__(self):
        self.labels = []

first = Order()
second = Order()
first.labels.append("blue")
print(first.labels)
print(second.labels)
  annotations: ['Create a new list for each instance.', 'Only first’s instance list is changed.', "Prints ['blue'].", 'Prints [].']

### s02 · video · Shared class attributes and individual instance state
Observe — 
[VIDEO Shared class attributes and individual instance state] bridge-before: Watch how the employee example separates individual values from a shared annual raise amount. The clip uses “class variables” and “instance variables” for shared class attributes and individual instance attributes. | bridge-after: The clip establishes shared versus individual state, but does not cover mutable-list sharing or its repair. The text explains shadowing and creating a separate list during each instance’s initialization.
  - BJ-VvGyQxho 36-74s facts=['f1'] label: Distinguish shared class attributes from instance attributes | summary: Class variables store attributes shared among instances, whereas instance variables can hold individual values such as an employee’s name, email, and pay. A common annual raise amount is a candidate for a class variable because the same amount applies to all employees, even if it changes from year to year.

### s03 · check · Check: Instance versus class attributes
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.
QUESTION [choice, intro, grading=client] Order has labels = [] in its class body. Updates to first.labels also appear in second.labels. Which repair gives each instance its own list?
  ✔ o1: Move list creation into __init__ as self.labels = [].
      why: This matches the stated task and the taught behavior.
  ✘ o2: Leave labels = [] in the class body and append through first.labels.
      why: Appending through an instance still mutates the shared list unless an instance attribute shadows it.
  ✘ o3: Create the list in the class body a second time under the same name.
      why: A class-body list remains shared; redefining it there does not make per-instance lists.
  feedback✔: Move list creation into __init__ as self.labels = [].  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Consider when a fresh list must be created for each object.']  remediation→r01
  MEASURES: A:correct_accidentally_shared_mutable_state(f2,f3)   anchors=['assessment:correct_accidentally_shared_mutable_state']
  taught-before-tested: A.f2←s01; A.f3←s01

### s04 · hands_on · Give each Order its own list
Practice — Move a mistakenly shared labels list from the Order class body into instance initialization as self.labels = [].
QUESTION [code_exercise, stretch, grading=client] The class implementation is supplied and must remain unchanged. Create first and second using separate Order() calls. The supplied append(label) operation must affect only first.labels.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['class Order:', 'def __init__(self):', 'labels = []', 'self.labels = []', 'first = Order()', 'second = Order()', 'first.labels.append("blue")', 'print(first.labels)', 'print(second.labels)'] blocked=9 items
  file main.py [editable]:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\n\ndef prepare_case(inputs):\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [ns["first"].labels, ns["second"].labels, ns["first"].labels is ns["second"].labels, "labels" in ns["Order"].__dict__, captured.getvalue().strip()]\n')

inputs = {'label': 'blue'}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
# Supplied class/function implementation; leave unchanged.
exec('class Order:\n    def __init__(self):\n        self.labels = []\n')
# Create the required instance(s) here using the supplied input names.
first.labels.append(label)
print(first.labels)
print(second.labels)
# END LEARNER

  SOLUTION main.py:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\n\ndef prepare_case(inputs):\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [ns["first"].labels, ns["second"].labels, ns["first"].labels is ns["second"].labels, "labels" in ns["Order"].__dict__, captured.getvalue().strip()]\n')

inputs = {'label': 'blue'}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
# Supplied class/function implementation; leave unchanged.
exec('class Order:\n    def __init__(self):\n        self.labels = []\n')
first = Order()
second = Order()
first.labels.append(label)
print(first.labels)
print(second.labels)
# END LEARNER

  test t1 (function_call, visible=True): {"function":"check_case","args":[{"label":"blue"}],"expected":[["blue"],[],false,false,"['blue']\n[]"]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  test t2 (function_call, visible=True): {"function":"check_case","args":[{"label":"notebook"}],"expected":[["notebook"],[],false,false,"['notebook']\n[]"]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"b3c1fa02d5316e110a098d0b8c4ab08811329739e34c62a58dce8763a0218403","tests_passed":2}
  feedback✔: The completed code meets the task on the supplied fixtures, including the changed inputs.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Follow the input names rather than substituting a fixed answer.', 'Check the required operation and where its result or resource state is observed.']
  MEASURES: A:distinguish_shared_and_per_instance_attributes(f1); A:predict_shared_list_mutation_and_instance_shadowing(f2)   anchors=['practice', 'assessment:distinguish_shared_and_per_instance_attributes', 'assessment:predict_shared_list_mutation_and_instance_shadowing']
  taught-before-tested: A.f1←s01; A.f2←s01

### s05 · recap · Keep these distinctions
Takeaways — 
(takeaway) A class-body labels list is shared; assigning self.labels during initialization creates separate lists. ⟦A.f2 A.f3 A:tb1 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Serialising and deserialising data with Python json: Next, begin serialising and deserialising data with python json.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: Instance versus class attributes
(definition) A mutable list assigned in the class body is shared by instances unless an instance attribute shadows it. ⟦A.f2 A:tb1 A:tb3 A:tb4 A:tb5⟧
(definition) Assign `self.labels = []` in `__init__` for a new list on each instance. Then updating first’s list does not mutate a shared class list. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) A class-body labels list is shared; assigning self.labels during initialization creates separate lists. ⟦A.f2 A.f3 A:tb1 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit: Instance versus class attributes
(definition) Class variables hold attributes shared by instances; instance variables hold data unique to an instance. ⟦A.f1 A:tb1 A:tb2 A:tb4⟧
(definition) A mutable list assigned in the class body is shared by instances unless an instance attribute shadows it. ⟦A.f2 A:tb1 A:tb3 A:tb4 A:tb5⟧
(misconception) A class-body labels list is shared; assigning self.labels during initialization creates separate lists. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast

=========

# EVALUATOR PACKET — Serialising and deserialising data with Python json (learn_python.tile.076_076)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.json_serialization — Serialising and deserialising data with Python json

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=3
  warn: remediation step learn_python.tile.076_076.r02 is never referenced
  warn: remediation step learn_python.tile.076_076.r03 is never referenced
  warn: learn_python.tile.076_076.s05/ix.learn_python.tile.076_076.s05: ADVISORY — syntax descriptors with no detector: ['==', 'None', 'True and False', 'assert statements', 'dictionary key access', 'dictionary literals with string keys', 'generator expressions', 'integer literals', 'list indexing', 'list literals', 'string literals', 'tuple literals', 'with statements', 'yield expressions']

## SOURCE FACTS — A (python.json_serialization)   objective: Serialize and deserialize supported Python data using the json module.
A.f1: json.dumps(value) serializes supported Python values to a JSON str.   [sources: python_stdlib_reference#json.html#json.dumps]
A.f2: json.loads(text) deserializes a JSON string into Python values.   [sources: python_stdlib_reference#json.html#json.loads]
A.f3: Default conversions support dictionaries, lists, tuples, strings, numeric values, booleans and None; lists and tuples both encode as arrays, which decode as lists.   [sources: python_stdlib_reference#json.html#json.JSONEncoder, python_stdlib_reference#json.html#json.JSONDecoder]
A.f4: JSON object keys are strings, so non-string dictionary keys need not retain their original Python types on a round trip.   [sources: python_stdlib_reference#json.html#json.JSONEncoder, python_stdlib_reference#json.html#json.JSONDecoder]
note: Begin with this objective: Serialize and deserialize supported Python data using the json module.
note: Keep the example in the Python JSON serialization tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.object_introspection, python.pathlib_filesystem_operations, python.special_methods.
note: Require web.json_serialization_basics before this unit; teach the Python json API rather than the generic format foundation.
PRACTICE ANCHOR (live_code): Round-trip a nested record containing quantities and active through a JSON string using json.dumps and json.loads, then check the reconstructed values with equality comparisons.  SUCCESS: The record is serialised and deserialised successfully. The reconstructed quantities equal [[3, 2]], and active equals True, demonstrating that the nested tuple becomes a list.
ASSESSMENT ANCHOR: round_trip_supported_python_record facts=['f1', 'f2']
ASSESSMENT ANCHOR: predict_supported_value_conversions facts=['f3']
ASSESSMENT ANCHOR: predict_dictionary_key_type_changes facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing environment variables with os.environ; Choosing explicit text-file encodings; Choosing random or secrets for randomness; Computing dates and elapsed times with datetime; Creating isolated virtual environments; Creating local modules; Defining useful object representations with special methods; Development checks with the Python assert statement; Diagnosing module search-path problems; Generator functions with yield; Guarding a program entry point; Handling file and data-format failures; Inspecting interpreter runtime information with sys; Inspecting object types and attributes; Installing dependencies with python -m pip; Iterables and iterators; Managing resources with with; Matching text patterns with re; Organising importable packages; Parsing command-line arguments with argparse; Performing filesystem operations with pathlib; Reading and writing binary files; Recording program events with logging; Recreating dependencies from requirements files; Selecting the project environment interpreter

## LESSON, in learner order

### s01 · explainer · Serialising and deserialising data with Python json
Understand — 
(definition) `json.dumps(value)` serializes supported Python values to a JSON string. ⟦A.f1 A:tb2 A:tb4⟧
(definition) `json.loads(text)` deserializes JSON text into Python values. ⟦A.f2 A:tb3 A:tb4⟧
(definition) Default conversions support dictionaries, lists, tuples, strings, numbers, booleans and None. Both lists and tuples encode as arrays, which decode as lists. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(definition) JSON object keys are strings. A non-string dictionary key need not retain its original Python type after a round trip. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
[PROCESS_FLOW: A JSON round trip preserves supported values, but not every Python type] nodes=['Python record: quantities and active', 'JSON str', 'Reconstructed Python values', 'Nested tuple becomes a list', 'Boolean value retained'] edges=[('record', 'text', 'json.dumps(record)'), ('text', 'restored', 'json.loads(text)'), ('restored', 'tuple', 'arrays decode as lists'), ('restored', 'active', 'boolean conversion')] alt: A JSON round trip preserves supported values, but not every Python type
[CODE python]
import json

record = {"quantities": [(3, 2)], "active": True}
text = json.dumps(record)
restored = json.loads(text)
print(restored["quantities"])
print(restored["quantities"][0] == [3, 2])
print(restored["active"])
  annotations: []

### s02 · video · Deserialising JSON text into Python values
Observe — 
[VIDEO Deserialising JSON text into Python values] bridge-before: Watch how json.loads turns text into an accessible Python dictionary. The clip sometimes calls the result a “JSON object”; here, distinguish the JSON text from the reconstructed Python values. | bridge-after: The clip demonstrates deserialisation. The text also teaches json.dumps, the full set of supported default values, tuple-to-list conversion, and why non-string dictionary keys may change type during a round trip.
  - -51jxlQaxyA 24-132s facts=['f2'] label: Load a JSON string into Python values with json.loads | summary: A JSON string contains an object whose students entry holds an array of objects. JSON strings use double quotation marks. After importing the standard-library json module, json.loads converts the string into a Python dictionary. Dictionary key access retrieves the students collection, and indexing retrieves its first item. The result is Python data that can be accessed using familiar collection operations.

### s03 · check · Check: Serialising and deserialising data with Python json
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.
QUESTION [choice, intro, grading=client] A supported record contains a tuple nested under quantities. After json.dumps followed by json.loads, which container type does that tuple become?
  ✔ o1: A Python list.
      why: This matches the stated task and the taught behavior.
  ✘ o2: A Python tuple.
      why: Tuples encode as JSON arrays, which decode as lists, not tuples.
  ✘ o3: A string containing Python tuple syntax.
      why: The supported tuple encodes as an array rather than a Python-syntax string.
  feedback✔: A Python list.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Trace the conversion through a JSON array back into Python.']  remediation→r01
  MEASURES: A:predict_supported_value_conversions(f3)   anchors=['assessment:predict_supported_value_conversions']
  taught-before-tested: A.f3←s01

### s04 · check · Check: Serialising and deserialising data with Python json
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.
QUESTION [choice, core, grading=client] A supported Python dictionary has a non-string numeric key. Which round-trip expectation is safe?
  ✘ o1: The key must retain its numeric Python type.
      why: JSON object keys are strings, so numeric key types need not survive the round trip.
  ✘ o2: The key is dropped because JSON object keys cannot be strings.
      why: JSON object keys are strings; the stated reason for dropping it reverses that fact.
  ✔ o3: Do not assume the key retains its Python type: JSON object keys are strings.
      why: This matches the stated task and the taught behavior.
  feedback✔: Do not assume the key retains its Python type: JSON object keys are strings.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Think about the key type JSON objects represent, not the original Python key.']
  MEASURES: A:predict_dictionary_key_type_changes(f4)   anchors=['assessment:predict_dictionary_key_type_changes']
  taught-before-tested: A.f4←s01

### s05 · hands_on · Inspect a JSON round trip
Practice — Round-trip a nested record containing quantities and active through a JSON string using json.dumps and json.loads, then check the reconstructed values with equality comparisons.
QUESTION [code_exercise, stretch, grading=client] Add import json, use json.dumps(record) to assign text, and use json.loads(text) to assign restored above the supplied comparison lines. Keep those comparisons and the supplied host fixtures unchanged. For the initial record both comparisons should be True. Tests vary the supported record and inspect text and restored as well.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['import json', 'variable assignment', 'dictionary literals with string keys', 'list literals', 'tuple literals', 'string literals', 'integer literals', 'True and False', 'None', 'json.dumps(value)', 'json.loads(text)', 'dictionary key access', 'list indexing', '==', 'print()'] blocked=9 items
  file main.py [editable]:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\n\ndef prepare_case(inputs):\n    inputs = dict(inputs)\n    inputs["record"] = {"quantities": [tuple(pair) for pair in inputs["record"]["quantities"]], "active": inputs["record"]["active"]}\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [ns["text"], ns["restored"], captured.getvalue().strip()]\n')

inputs = {'record': {'quantities': [[3, 2]], 'active': True}}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
# Add import json, then assign text and restored above the supplied comparisons.
print(restored["quantities"] == [[3, 2]])
print(restored["active"] == True)
# END LEARNER

  SOLUTION main.py:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\n\ndef prepare_case(inputs):\n    inputs = dict(inputs)\n    inputs["record"] = {"quantities": [tuple(pair) for pair in inputs["record"]["quantities"]], "active": inputs["record"]["active"]}\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [ns["text"], ns["restored"], captured.getvalue().strip()]\n')

inputs = {'record': {'quantities': [[3, 2]], 'active': True}}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
import json
text = json.dumps(record)
restored = json.loads(text)
print(restored["quantities"] == [[3, 2]])
print(restored["active"] == True)
# END LEARNER

  test t1 (function_call, visible=True): {"function":"check_case","args":[{"record":{"quantities":[[3,2]],"active":true}}],"expected":["{\"quantities\": [[3, 2]], \"active\": true}",{"quantities":[[3,2]],"active":true},"True\nTrue"]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  test t2 (function_call, visible=True): {"function":"check_case","args":[{"record":{"quantities":[[2,4]],"active":false}}],"expected":["{\"quantities\": [[2, 4]], \"active\": false}",{"quantities":[[2,4]],"active":false},"False\nFalse"]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"ff445b48116ef77fe1f4c2034a588d34ab5db95bb3a0cf2f39f6e9a59e2e9d8c","tests_passed":2}
  feedback✔: The completed code meets the task on the supplied fixtures, including the changed inputs.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Follow the input names rather than substituting a fixed answer.', 'Check the required operation and where its result or resource state is observed.']
  MEASURES: A:round_trip_supported_python_record(f1,f2)   anchors=['practice', 'assessment:round_trip_supported_python_record']
  taught-before-tested: A.f1←s01; A.f2←s01

### s06 · recap · Keep these distinctions
Takeaways — 
(takeaway) A successful round trip can preserve values without preserving every Python type: tuples return as lists. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Inspecting object types and attributes: Next, begin inspecting object types and attributes.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: Serialising and deserialising data with Python json
(definition) Default conversions support dictionaries, lists, tuples, strings, numbers, booleans and None. Both lists and tuples encode as arrays, which decode as lists. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) A successful round trip can preserve values without preserving every Python type: tuples return as lists. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit: Serialising and deserialising data with Python json
(definition) JSON object keys are strings. A non-string dictionary key need not retain its original Python type after a round trip. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) A successful round trip can preserve values without preserving every Python type: tuples return as lists. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
### r03 · Revisit: Serialising and deserialising data with Python json
(definition) `json.dumps(value)` serializes supported Python values to a JSON string. ⟦A.f1 A:tb2 A:tb4⟧
(definition) `json.loads(text)` deserializes JSON text into Python values. ⟦A.f2 A:tb3 A:tb4⟧
(misconception) A successful round trip can preserve values without preserving every Python type: tuples return as lists. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4⟧

## OTHER CONTENT (fields without a dedicated renderer)
· spec.expected: {"quantities": [[3, 2]], "active": true}
· spec.expected: {"quantities": [[2, 4]], "active": false}
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast

=========

# EVALUATOR PACKET — Inspecting object types and attributes (learn_python.tile.077_077)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.object_introspection — Inspecting object types and attributes

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: remediation step learn_python.tile.077_077.r02 is never referenced
  warn: learn_python.tile.077_077.s03/ix.learn_python.tile.077_077.s03: ADVISORY — syntax descriptors with no detector: ['None', 'assert statements', 'class Order definitions', 'def and return', 'definitions of __repr__ or __str__', 'function calls', 'generator expressions', 'list comprehensions', 'string and integer literals', 'with statements', 'yield expressions']

## SOURCE FACTS — A (python.object_introspection)   objective: Inspect Python object types and attributes.
A.f1: type(object) returns the object’s type.   [sources: python_stdlib_reference#functions.html#type]
A.f2: isinstance(object, Class) checks whether the object is an instance of that class or one of its subclasses.   [sources: python_stdlib_reference#functions.html#isinstance]
A.f3: dir(object) attempts to list relevant attribute names, but is not guaranteed to be complete.   [sources: python_stdlib_reference#functions.html#dir]
A.f4: getattr(object, name) retrieves a named attribute, with an optional fallback if it is absent.   [sources: python_stdlib_reference#functions.html#getattr]
A.f5: Attribute names beginning with an underscore conventionally signal internal use rather than a public interface.   [sources: pep8_style_guide#descriptive-naming-styles]
note: Begin with this objective: Inspect Python object types and attributes.
note: Keep the example in the Inspecting objects tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.pathlib_filesystem_operations, python.special_methods, python.text_file_encodings.
PRACTICE ANCHOR (live_code): Inspect an Order instance returned by a supplied helper: determine its type, check its membership in Order, list candidate public attribute names, and retrieve quantity and an absent attribute with a fallback.  SUCCESS: The inspection identifies Order as the type, produces True for the membership check, includes quantity among names not beginning with an underscore, retrieves quantity as 3, and returns None for missing. The learner treats the filtered names as inspection candidates rather than a guaranteed complete public interface.
ASSESSMENT ANCHOR: identify_object_type facts=['f1']
ASSESSMENT ANCHOR: check_class_and_subclass_membership facts=['f2']
ASSESSMENT ANCHOR: inspect_attribute_names_with_public_interface_conventions facts=['f3', 'f5']
ASSESSMENT ANCHOR: retrieve_named_attributes_with_optional_fallback facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing environment variables with os.environ; Choosing explicit text-file encodings; Choosing random or secrets for randomness; Computing dates and elapsed times with datetime; Creating isolated virtual environments; Creating local modules; Defining useful object representations with special methods; Development checks with the Python assert statement; Diagnosing module search-path problems; Generator expressions; Generator functions with yield; Guarding a program entry point; Handling file and data-format failures; Inspecting interpreter runtime information with sys; Installing dependencies with python -m pip; Iterables and iterators; Managing resources with with; Matching text patterns with re; Organising importable packages; Parsing command-line arguments with argparse; Performing filesystem operations with pathlib; Reading and writing binary files; Recording program events with logging; Recreating dependencies from requirements files; Selecting the project environment interpreter

## LESSON, in learner order

### s01 · explainer · Inspecting object types and attributes
Understand — 
(definition) `type(order)` returns the object’s type. ⟦A.f1 A:tb2 A:tb4⟧
(definition) `isinstance(order, Order)` checks membership in Order or one of its subclasses. ⟦A.f2 A:tb3 A:tb4⟧
(definition) `dir(order)` attempts to list relevant attribute names; completeness is not guaranteed. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(definition) `getattr(order, name)` retrieves a named attribute. Supply an optional fallback for an absent attribute. ⟦A.f4 A:tb3 A:tb4⟧
(definition) Underscore-prefixed names conventionally signal internal use rather than the public interface. ⟦A.f5 A:tb3 A:tb4 A:tb5⟧
[CODE python]
class Order:
    def __init__(self):
        self.quantity = 3

def make_order():
    return Order()

order = make_order()
print(type(order))
print(isinstance(order, Order))
print(getattr(order, "quantity"))
print(getattr(order, "missing", None))
print(dir(order))
  annotations: ['Inspect the object’s type. Returns the Order class.', 'Class membership includes subclasses. Returns True.', 'Retrieve the quantity attribute by name. Returns 3.', 'Use a fallback when the named attribute is absent. Returns None.', 'Includes quantity and underscore-prefixed names such as __dict__. Candidate relevant names, not a guaranteed complete public API; underscores signal internal use.']

### s02 · check · Check: Inspecting object types and attributes
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.
QUESTION [choice, intro, grading=client] An Order has no missing attribute. Which expression retrieves it with a None fallback if it is absent?
  ✔ o1: getattr(order, "missing", None)
      why: This matches the stated task and the taught behavior.
  ✘ o2: getattr(order, "missing")
      why: Without the optional fallback, this expression does not request None for an absent attribute.
  ✘ o3: getattr(order, "quantity", None)
      why: This retrieves quantity, not the named missing attribute.
  feedback✔: getattr(order, "missing", None)  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Check both the requested attribute name and the fallback argument.']  remediation→r01
  MEASURES: A:retrieve_named_attributes_with_optional_fallback(f4)   anchors=['assessment:retrieve_named_attributes_with_optional_fallback']
  taught-before-tested: A.f4←s01

### s03 · hands_on · Inspect an Order object
Practice — Inspect an Order instance returned by a supplied helper: determine its type, check its membership in Order, list candidate public attribute names, and retrieve quantity and an absent attribute with a fallback.
QUESTION [code_exercise, stretch, grading=client] Using the supplied order, assign its actual type to object_type, its Order-or-subclass membership result to membership, its named quantity attribute to quantity, and the result of retrieving missing with a None fallback to missing. Keep public_names unchanged and treat those names as inspection candidates, not a guaranteed complete interface.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment', 'class Order definitions', 'def and return', 'def __init__(self)', 'self.quantity = 3', 'Order()', 'function calls', 'type(order)', 'isinstance(order, Order)', 'dir(order)', 'getattr(order, "quantity")', 'getattr(order, "missing", None)', 'list comprehensions', 'name.startswith("_")', 'not', 'print()', 'string and integer literals', 'None'] blocked=7 items
  file main.py [editable]:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\nclass Order:\n    def __init__(self):\n        self.quantity = 3\ndef make_order():\n    return Order()\norder = make_order()\nclass InspectionOrder(Order):\n    pass\n\ndef prepare_case(inputs):\n    order = InspectionOrder() if inputs["subclass"] else Order()\n    order.quantity = inputs["quantity"]\n    return {"order":order}\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [ns["object_type"].__name__, ns["membership"], ns["public_names"], ns["quantity"], ns["missing"]]\n')

inputs = {'quantity': 3, 'subclass': False}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
public_names = [name for name in dir(order) if not name.startswith("_")]
# Inspect the supplied order here.
# END LEARNER

  SOLUTION main.py:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\nclass Order:\n    def __init__(self):\n        self.quantity = 3\ndef make_order():\n    return Order()\norder = make_order()\nclass InspectionOrder(Order):\n    pass\n\ndef prepare_case(inputs):\n    order = InspectionOrder() if inputs["subclass"] else Order()\n    order.quantity = inputs["quantity"]\n    return {"order":order}\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [ns["object_type"].__name__, ns["membership"], ns["public_names"], ns["quantity"], ns["missing"]]\n')

inputs = {'quantity': 3, 'subclass': False}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
public_names = [name for name in dir(order) if not name.startswith("_")]
object_type = type(order)
membership = isinstance(order, Order)
quantity = getattr(order, "quantity")
missing = getattr(order, "missing", None)
# dir is not guaranteed complete; underscore names conventionally signal internal use.
# END LEARNER

  test t1 (function_call, visible=True): {"function":"check_case","args":[{"quantity":3,"subclass":false}],"expected":["Order",true,["quantity"],3,null]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  test t2 (function_call, visible=True): {"function":"check_case","args":[{"quantity":2,"subclass":true}],"expected":["InspectionOrder",true,["quantity"],2,null]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"22b96b22900a791ffcdd50fb1a1dbebafd4f8158911c37a3b2768df7c818f158","tests_passed":2}
  feedback✔: The completed code meets the task on the supplied fixtures, including the changed inputs.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Follow the input names rather than substituting a fixed answer.', 'Check the required operation and where its result or resource state is observed.']
  MEASURES: A:identify_object_type(f1); A:check_class_and_subclass_membership(f2); A:inspect_attribute_names_with_public_interface_conventions(f3,f5); A:retrieve_named_attributes_with_optional_fallback(f4)   anchors=['practice', 'assessment:identify_object_type', 'assessment:check_class_and_subclass_membership', 'assessment:inspect_attribute_names_with_public_interface_conventions', 'assessment:retrieve_named_attributes_with_optional_fallback']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01; A.f5←s01; A.f4←s01

### s04 · recap · Keep these distinctions
Takeaways — 
(takeaway) Treat dir(order) as candidate names, not a complete public-interface specification. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Performing filesystem operations with pathlib: Next, begin performing filesystem operations with pathlib.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: Inspecting object types and attributes
(definition) `getattr(order, name)` retrieves a named attribute. Supply an optional fallback for an absent attribute. ⟦A.f4 A:tb3 A:tb4⟧
(misconception) Treat dir(order) as candidate names, not a complete public-interface specification. ⟦A.f4 A:tb3 A:tb4⟧
### r02 · Revisit: Inspecting object types and attributes
(definition) `type(order)` returns the object’s type. ⟦A.f1 A:tb2 A:tb4⟧
(definition) `isinstance(order, Order)` checks membership in Order or one of its subclasses. ⟦A.f2 A:tb3 A:tb4⟧
(definition) `dir(order)` attempts to list relevant attribute names; completeness is not guaranteed. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(definition) `getattr(order, name)` retrieves a named attribute. Supply an optional fallback for an absent attribute. ⟦A.f4 A:tb3 A:tb4⟧
(definition) Underscore-prefixed names conventionally signal internal use rather than the public interface. ⟦A.f5 A:tb3 A:tb4 A:tb5⟧
(misconception) Treat dir(order) as candidate names, not a complete public-interface specification. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3 A:tb4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast

=========

# EVALUATOR PACKET — Performing filesystem operations with pathlib (learn_python.tile.078_078)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.pathlib_filesystem_operations — Performing filesystem operations with pathlib

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: remediation step learn_python.tile.078_078.r02 is never referenced
  warn: learn_python.tile.078_078.s04/ix.learn_python.tile.078_078.s04: ADVISORY — syntax descriptors with no detector: ['assert statements', 'directory / filename', 'for loops', 'generator expressions', "if __name__ == '__main__':", 'if statements', 'string literals', 'with statements', 'yield', 'yield from']

## SOURCE FACTS — A (python.pathlib_filesystem_operations)   objective: Perform filesystem operations using pathlib.
A.f1: directory.mkdir(parents=True, exist_ok=True) creates the directory and missing parents, allowing an existing directory; both options default to False.   [sources: python_stdlib_reference#pathlib.html#pathlib.Path.mkdir]
A.f2: directory.iterdir() traverses its immediate entries in arbitrary order.   [sources: python_stdlib_reference#pathlib.html#pathlib.Path.iterdir]
A.f3: source.rename(target) renames or moves the entry to target; a relative target is resolved against the current working directory, not against source’s parent.   [sources: python_stdlib_reference#pathlib.html#pathlib.Path.rename]
A.f4: rename can silently replace an existing target file on Unix when permitted, while Windows raises FileExistsError for an existing target.   [sources: python_stdlib_reference#pathlib.html#pathlib.Path.rename]
A.f5: Construct the destination as directory / filename to target the selected output directory rather than relying on a bare relative filename.   [sources: python_stdlib_reference#pathlib.html#operators]
note: Begin with this objective: Perform filesystem operations using pathlib.
note: Keep the example in the Path-based filesystem operations tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.special_methods, python.text_file_encodings, python.file_and_format_errors.
note: Require linux.filesystem_navigation_and_files before this filesystem, script, module or environment unit; do not teach terminal navigation here.
PRACTICE ANCHOR (live_code): Create the supplied output directory, including missing parents, and move the supplied generated report into it using a destination constructed from directory and filename.  SUCCESS: The output directory exists, the report is located at directory / filename, and the original source entry is no longer present. Immediate output entries can be inspected without assuming their order.
ASSESSMENT ANCHOR: create_intended_directory_with_missing_parents facts=['f1']
ASSESSMENT ANCHOR: list_immediate_directory_entries_without_order_assumptions facts=['f2']
ASSESSMENT ANCHOR: construct_destination_and_move_intended_entry facts=['f3', 'f5']
ASSESSMENT ANCHOR: recognize_platform_specific_existing_target_behavior facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing environment variables with os.environ; Choosing explicit text-file encodings; Choosing random or secrets for randomness; Computing dates and elapsed times with datetime; Creating isolated virtual environments; Creating local modules; Defining useful object representations with special methods; Development checks with the Python assert statement; Diagnosing module search-path problems; Generator expressions; Generator functions with yield; Guarding a program entry point; Handling file and data-format failures; Inspecting interpreter runtime information with sys; Installing dependencies with python -m pip; Iterables and iterators; Iterator consumption and exhaustion; Managing resources with with; Matching text patterns with re; Organising importable packages; Parsing command-line arguments with argparse; Reading and writing binary files; Recording program events with logging; Recreating dependencies from requirements files; Selecting the project environment interpreter

## LESSON, in learner order

### s01 · explainer · Performing filesystem operations with pathlib
Understand — 
(definition) `mkdir(parents=True, exist_ok=True)` creates the directory and missing parents, allowing an existing directory; both options default to False. ⟦A.f1 A:tb2⟧
(definition) `directory.iterdir()` traverses immediate entries in arbitrary order. ⟦A.f2 A:tb3⟧
(definition) `source.rename(target)` moves or renames the entry. Relative targets use the working directory, not the source’s parent. ⟦A.f3 A:tb3⟧
(definition) Rename can silently replace an existing target file on Unix when permitted; on Windows it raises `FileExistsError`. ⟦A.f4 A:tb3⟧
(definition) Build `target = directory / filename` to select the output directory, not a bare relative filename. ⟦A.f5 A:tb3⟧
[BEFORE_AFTER] target = directory / filename; source.rename(target). Inspect the target before moving.
  before:
[DIAGRAM: Before: destination absent] nodes=['incoming/report.txt', 'output/reports', 'output/reports/report.txt (absent)'] edges=[('directory', 'target', 'target = directory / filename')] alt: Before: destination absent
  after:
[DIAGRAM: After successful move] nodes=['incoming/report.txt (absent)', 'output/reports', 'output/reports/report.txt'] edges=[('directory', 'target', 'contains')] alt: After successful move

### s02 · explainer · Performing filesystem operations with pathlib
Understand — 
(example) For incoming/report.txt, build target from output/reports and filename. Create missing parents while allowing an existing directory. Move with source.rename(target), then inspect immediate entries without assuming order. A bare relative target uses the working directory, not the source’s parent. Check for an existing target before moving: Unix can replace it when permitted; Windows raises FileExistsError. The mkdir options both default to False, so specify the intended behavior. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb4 A:tb5⟧

### s03 · check · Check: Performing filesystem operations with pathlib
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.
QUESTION [choice, intro, grading=client] source.rename(target) encounters an existing target file. Which statement preserves the taught platform distinction?
  ✔ o1: Unix may silently replace it when permitted; Windows raises FileExistsError.
      why: This matches the stated task and the taught behavior.
  ✘ o2: Both platforms always raise FileExistsError.
      why: Unix can replace an existing target when permitted, so universal failure is not guaranteed.
  ✘ o3: Both platforms always append the source content to the target.
      why: rename moves or renames an entry; the stated existing-target behaviors are replacement or failure, not append.
  feedback✔: Unix may silently replace it when permitted; Windows raises FileExistsError.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Avoid a platform-independent promise for an existing target.']  remediation→r01
  MEASURES: A:recognize_platform_specific_existing_target_behavior(f4)   anchors=['assessment:recognize_platform_specific_existing_target_behavior']
  taught-before-tested: A.f4←s01

### s04 · hands_on · Move the report to its output directory
Practice — Create the supplied output directory, including missing parents, and move the supplied generated report into it using a destination constructed from directory and filename.
QUESTION [code_exercise, stretch, grading=client] Construct target from the supplied directory and filename before the unchanged directory creation, rename, and inspection operations. Preserve the source content and do not assume an inspection order.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['from pathlib import Path', 'Path(...)', 'variable assignment', 'string literals', 'directory / filename', 'directory.mkdir(parents=True, exist_ok=True)', 'source.rename(target)', 'directory.iterdir()', 'target.exists()', 'if statements', 'for loops', 'print(...)'] blocked=11 items
  file main.py [editable]:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\n\ndef prepare_case(inputs):\n    shutil.rmtree("incoming", ignore_errors=True)\n    shutil.rmtree("output", ignore_errors=True)\n    pathlib.Path("incoming").mkdir()\n    pathlib.Path("incoming/report.txt").write_text(inputs["content"])\n    return {"directory":pathlib.Path("output/reports"), "source":pathlib.Path("incoming/report.txt"), "filename":"report.txt"}\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [ns["target"].read_text(), ns["directory"].is_dir(), ns["source"].exists(), sorted(str(p) for p in ns["directory"].iterdir()), sorted(captured.getvalue().splitlines())]\n')

inputs = {'content': 'First'}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
from pathlib import Path
# Construct target from the supplied directory and filename.
directory.mkdir(parents=True, exist_ok=True)
source.rename(target)
for entry in directory.iterdir():
    print(entry)
# END LEARNER

  SOLUTION main.py:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\n\ndef prepare_case(inputs):\n    shutil.rmtree("incoming", ignore_errors=True)\n    shutil.rmtree("output", ignore_errors=True)\n    pathlib.Path("incoming").mkdir()\n    pathlib.Path("incoming/report.txt").write_text(inputs["content"])\n    return {"directory":pathlib.Path("output/reports"), "source":pathlib.Path("incoming/report.txt"), "filename":"report.txt"}\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [ns["target"].read_text(), ns["directory"].is_dir(), ns["source"].exists(), sorted(str(p) for p in ns["directory"].iterdir()), sorted(captured.getvalue().splitlines())]\n')

inputs = {'content': 'First'}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
from pathlib import Path
target = Path(directory, filename)
directory.mkdir(parents=True, exist_ok=True)
source.rename(target)
for entry in directory.iterdir():
    print(entry)
# END LEARNER

  test t1 (function_call, visible=True): {"function":"check_case","args":[{"content":"First"}],"expected":["First",true,false,["output/reports/report.txt"],["output/reports/report.txt"]]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  test t2 (function_call, visible=True): {"function":"check_case","args":[{"content":"First_updated"}],"expected":["First_updated",true,false,["output/reports/report.txt"],["output/reports/report.txt"]]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"cef7264582d39c4587ac2bcb5df500c058f4fdf29e5f04be2c321a7867f6c2e9","tests_passed":2}
  feedback✔: The completed code meets the task on the supplied fixtures, including the changed inputs.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Follow the input names rather than substituting a fixed answer.', 'Check the required operation and where its result or resource state is observed.']
  MEASURES: A:create_intended_directory_with_missing_parents(f1); A:list_immediate_directory_entries_without_order_assumptions(f2); A:construct_destination_and_move_intended_entry(f3,f5)   anchors=['practice', 'assessment:create_intended_directory_with_missing_parents', 'assessment:list_immediate_directory_entries_without_order_assumptions', 'assessment:construct_destination_and_move_intended_entry']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01; A.f5←s01

### s05 · recap · Keep these distinctions
Takeaways — 
(takeaway) Use directory / filename, not a bare relative filename whose location depends on the working directory. ⟦A.f3 A.f5 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Defining useful object representations with special methods: Next, begin defining useful object representations with special methods.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: Performing filesystem operations with pathlib
(definition) Rename can silently replace an existing target file on Unix when permitted; on Windows it raises `FileExistsError`. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Use directory / filename, not a bare relative filename whose location depends on the working directory. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit: Performing filesystem operations with pathlib
(definition) `mkdir(parents=True, exist_ok=True)` creates the directory and missing parents, allowing an existing directory; both options default to False. ⟦A.f1 A:tb2 A:tb4⟧
(definition) `directory.iterdir()` traverses immediate entries in arbitrary order. ⟦A.f2 A:tb3 A:tb4⟧
(definition) `source.rename(target)` moves or renames the entry. Relative targets use the working directory, not the source’s parent. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(definition) Build `target = directory / filename` to select the output directory, not a bare relative filename. ⟦A.f5 A:tb3 A:tb4⟧
(misconception) Use directory / filename, not a bare relative filename whose location depends on the working directory. ⟦A.f1 A.f2 A.f3 A.f5 A:tb2 A:tb3 A:tb4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: open(..., encoding=...)
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast

=========

# EVALUATOR PACKET — Defining useful object representations with special methods (learn_python.tile.079_079)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.special_methods — Defining useful object representations with special methods

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: learn_python.tile.079_079.s04/ix.learn_python.tile.079_079.s04: ADVISORY — syntax descriptors with no detector: ['assert', 'class Order:', 'generator expressions', 'if __name__ == "__main__":', 'integer literals', 'string literals', 'with', 'yield']

## SOURCE FACTS — A (python.special_methods)   objective: Define readable object representations using special methods.
A.f1: Define def __repr__(self): returning a str for an information-rich, unambiguous representation used by repr and interactive inspection.   [sources: python_language_reference#datamodel.html#object.__repr__]
A.f2: Define def __str__(self): returning a str for a convenient user-facing representation used by str and print.   [sources: python_language_reference#datamodel.html#object.__str__]
A.f3: If __str__ is not defined, the default representation uses __repr__.   [sources: python_language_reference#datamodel.html#object.__str__]
note: Begin with this objective: Define readable object representations using special methods.
note: Keep the example in the Useful special methods tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.text_file_encodings, python.file_and_format_errors, python.with_resource_management.
PRACTICE ANCHOR (live_code): Give an Order object with a quantity attribute useful inspection and user-facing representations by implementing __repr__ and __str__.  SUCCESS: For order = Order(3), repr(order) returns 'Order(quantity=3)' and str(order) returns 'Quantity: 3'; print(order) displays the user-facing string. Removing __str__ makes str(order) use the __repr__ result.
ASSESSMENT ANCHOR: implement_information_rich_repr facts=['f1']
ASSESSMENT ANCHOR: implement_user_facing_str facts=['f2']
ASSESSMENT ANCHOR: distinguish_representation_selection_and_fallback facts=['f1', 'f2', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing environment variables with os.environ; Choosing eager or lazy processing; Choosing explicit text-file encodings; Choosing random or secrets for randomness; Computing dates and elapsed times with datetime; Creating isolated virtual environments; Creating local modules; Development checks with the Python assert statement; Diagnosing module search-path problems; Generator expressions; Generator functions with yield; Guarding a program entry point; Handling file and data-format failures; Inspecting interpreter runtime information with sys; Installing dependencies with python -m pip; Iterables and iterators; Iterator consumption and exhaustion; Managing resources with with; Matching text patterns with re; Organising importable packages; Parsing command-line arguments with argparse; Reading and writing binary files; Recording program events with logging; Recreating dependencies from requirements files; Selecting the project environment interpreter

## LESSON, in learner order

### s01 · explainer · Defining useful object representations with special methods
Understand — 
(definition) Define `__repr__(self)` to return a string with an information-rich, unambiguous representation for repr and interactive inspection. ⟦A.f1 A:tb1 A:tb2 A:tb4 A:tb5⟧
(definition) Define `__str__(self)` to return a convenient user-facing string for str and print. ⟦A.f2 A:tb1 A:tb3 A:tb4 A:tb5⟧
(definition) If `__str__` is absent, the default representation uses `__repr__`. Return strings from these methods; do not replace the return with printing. ⟦A.f3 A:tb3 A:tb4⟧
[CODE python]
class Order:
    def __init__(self, quantity):
        self.quantity = quantity
    def __repr__(self):
        return f"Order(quantity={self.quantity})"
    def __str__(self):
        return f"Quantity: {self.quantity}"

order = Order(3)
print(repr(order))
print(order)
  annotations: ['Return an information-rich string for repr and inspection.', 'Return a user-facing string for str and print.', 'Use __repr__. Prints Order(quantity=3).', 'Use __str__; without it the default uses __repr__. Prints Quantity: 3.']
[CODE python]
class Order:
    def __init__(self, quantity):
        self.quantity = quantity
    def __repr__(self):
        return f"Order(quantity={self.quantity})"

order = Order(3)
print(repr(order))
print(order)
print(str(order))
  annotations: ['With __str__ removed, the default uses __repr__. Prints Order(quantity=3).', 'Prints Order(quantity=3).', 'Prints Order(quantity=3).']

### s02 · video · Separate inspection and user-facing representations
Observe — 
[VIDEO Separate inspection and user-facing representations] bridge-before: Watch how the Employee display changes as each representation method is added. The clip calls these “magic” or “dunder” methods; Devspace uses “special methods.” Focus on their distinct display purposes. | bridge-after: The clip covers both representations and the fallback when __str__ is absent. Apply the same distinction to Order: return explicit state for inspection and a convenient quantity message for users.
  - 3ohzBxoFHAY 0-350s facts=['f1', 'f2', 'f3'] label: Define __repr__ and __str__ for distinct display purposes | summary: Special methods customize built-in object behavior. Their names have double underscores on both sides, often called “dunder.” An Employee instance initially has an unhelpful default display. Defining __repr__ gives it an unambiguous, developer-oriented string containing its first name, last name, and pay in a construction-like form. When __str__ is absent, str and ordinary printing fall back to __repr__. Adding __str__ supplies a more convenient user-facing string containing the employee’s full name and email address. Both methods return strings rather than displaying messages themselves. Calling repr or str selects the corresponding representation; the demonstration also compares these calls with calling the special methods directly.

### s03 · check · Check: Defining useful object representations with special methods
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.
QUESTION [choice, intro, grading=client] Order defines __repr__ but has no __str__ implementation. What does the default str representation use?
  ✔ o1: The __repr__ result.
      why: This matches the stated task and the taught behavior.
  ✘ o2: It has no representation until __str__ is implemented.
      why: The default representation falls back to __repr__ when __str__ is absent.
  ✘ o3: It always ignores __repr__ and uses the quantity attribute alone.
      why: The fallback uses __repr__, not an automatic rendering of quantity.
  feedback✔: The __repr__ result.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Compare the missing user-facing method with the available inspection method.']  remediation→r01
  MEASURES: A:distinguish_representation_selection_and_fallback(f1,f2,f3)   anchors=['assessment:distinguish_representation_selection_and_fallback']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s04 · hands_on · Return two representations
Practice — Give an Order object with a quantity attribute useful inspection and user-facing representations by implementing __repr__ and __str__.
QUESTION [code_exercise, stretch, grading=client] The class implementation is supplied and must remain unchanged. Construct order = Order(quantity). Preserve the supplied repr and display calls; tests also inspect the fallback when __str__ is temporarily removed.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['class Order:', 'def __init__(self, quantity):', 'self.quantity = quantity', 'def __repr__(self):', 'def __str__(self):', 'return', 'f-strings', 'string literals', 'integer literals', 'order = Order(3)', 'self.quantity', 'repr(order)', 'str(order)', 'print()'] blocked=19 items
  file main.py [editable]:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\ndef representation_probe(ns, captured):\n    obj = ns["order"]\n    result = [repr(obj), str(obj), captured.getvalue().strip()]\n    method = ns["Order"].__dict__.get("__str__")\n    if method is not None:\n        delattr(ns["Order"], "__str__")\n    result.append(str(obj))\n    if method is not None:\n        setattr(ns["Order"], "__str__", method)\n    return result\n\n\ndef prepare_case(inputs):\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return representation_probe(ns, captured)\n')

inputs = {'quantity': 3}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
# Supplied class/function implementation; leave unchanged.
exec('class Order:\n    def __init__(self, quantity):\n        self.quantity = quantity\n    def __repr__(self):\n        return f"Order(quantity={self.quantity})"\n    def __str__(self):\n        return f"Quantity: {self.quantity}"\n')
# Create the required instance(s) here using the supplied input names.
print(repr(order))
print(order)
# END LEARNER

  SOLUTION main.py:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\ndef representation_probe(ns, captured):\n    obj = ns["order"]\n    result = [repr(obj), str(obj), captured.getvalue().strip()]\n    method = ns["Order"].__dict__.get("__str__")\n    if method is not None:\n        delattr(ns["Order"], "__str__")\n    result.append(str(obj))\n    if method is not None:\n        setattr(ns["Order"], "__str__", method)\n    return result\n\n\ndef prepare_case(inputs):\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return representation_probe(ns, captured)\n')

inputs = {'quantity': 3}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
# Supplied class/function implementation; leave unchanged.
exec('class Order:\n    def __init__(self, quantity):\n        self.quantity = quantity\n    def __repr__(self):\n        return f"Order(quantity={self.quantity})"\n    def __str__(self):\n        return f"Quantity: {self.quantity}"\n')
order = Order(quantity)
print(repr(order))
print(order)
# END LEARNER

  test t1 (function_call, visible=True): {"function":"check_case","args":[{"quantity":3}],"expected":["Order(quantity=3)","Quantity: 3","Order(quantity=3)\nQuantity: 3","Order(quantity=3)"]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  test t2 (function_call, visible=True): {"function":"check_case","args":[{"quantity":2}],"expected":["Order(quantity=2)","Quantity: 2","Order(quantity=2)\nQuantity: 2","Order(quantity=2)"]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"ee4ba50b2d435d4460da0368011c339e161941ce32e38fb624e8d42564565f18","tests_passed":2}
  feedback✔: The completed code meets the task on the supplied fixtures, including the changed inputs.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Follow the input names rather than substituting a fixed answer.', 'Check the required operation and where its result or resource state is observed.']
  MEASURES: A:implement_information_rich_repr(f1); A:implement_user_facing_str(f2); A:distinguish_representation_selection_and_fallback(f1,f2,f3)   anchors=['practice', 'assessment:implement_information_rich_repr', 'assessment:implement_user_facing_str', 'assessment:distinguish_representation_selection_and_fallback']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f1←s01; A.f2←s01; A.f3←s01

### s05 · recap · Keep these distinctions
Takeaways — 
(takeaway) Return a representation string from the method rather than printing it inside the method. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Choosing explicit text-file encodings: Next, begin choosing explicit text-file encodings.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: Defining useful object representations with special methods
(definition) Define `__repr__(self)` to return a string with an information-rich, unambiguous representation for repr and interactive inspection. ⟦A.f1 A:tb1 A:tb2 A:tb4 A:tb5⟧
(definition) Define `__str__(self)` to return a convenient user-facing string for str and print. ⟦A.f2 A:tb1 A:tb3 A:tb4 A:tb5⟧
(definition) If `__str__` is absent, the default representation uses `__repr__`. Return strings from these methods; do not replace the return with printing. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) Return a representation string from the method rather than printing it inside the method. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· spec.expected: Order(quantity=3)
Quantity: 3
· spec.expected: Order(quantity=2)
Quantity: 2
· remediation_steps.eyebrow: Try a clearer contrast

=========

# EVALUATOR PACKET — Choosing explicit text-file encodings / Handling file and data-format failures / Managing resources with with / Reading and writing binary files (learn_python.tile.080_083)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.text_file_encodings — Choosing explicit text-file encodings
B = python.file_and_format_errors — Handling file and data-format failures
C = python.with_resource_management — Managing resources with with
D = python.binary_files — Reading and writing binary files

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=8
  warn: remediation step learn_python.tile.080_083.r02 is never referenced
  warn: remediation step learn_python.tile.080_083.r05 is never referenced
  warn: remediation step learn_python.tile.080_083.r06 is never referenced
  warn: remediation step learn_python.tile.080_083.r08 is never referenced
  warn: learn_python.tile.080_083.s03/ix.learn_python.tile.080_083.s03: ADVISORY — syntax descriptors with no detector: ['Binary file modes "rb" and "wb"', 'Byte literals', 'String literals containing non-ASCII text', 'Variable assignment', 'assert statements', 'with statements']
  warn: learn_python.tile.080_083.s07/ix.learn_python.tile.080_083.s07: ADVISORY — syntax descriptors with no detector: ['and, or, and not', 'argparse', 'assert', 'def and return', 'dictionary indexing and membership checks', 'for row in reader', 'generator expressions', 'if __name__ == "__main__"', 'if and else', 'is None and is not None', 'itertools', 'logging', 're', 'string literals and equality comparisons', 'sys', 'unittest', 'with', 'yield']
  warn: learn_python.tile.080_083.s12/ix.learn_python.tile.080_083.s12: ADVISORY — syntax descriptors with no detector: ['assert', 'generator expressions', 'indented blocks', 'string literals', 'try/except ValueError', 'yield', 'yield from']
  warn: learn_python.tile.080_083.s16/ix.learn_python.tile.080_083.s16: ADVISORY — syntax descriptors with no detector: ['assert statements', 'generator expressions', 'if __name__ == "__main__":', 'nested indented blocks', 'yield expressions', 'yield from expressions']

## SOURCE FACTS — A (python.text_file_encodings)   objective: Specify the encoding contract for text-file access.
A.f1: Use open(path, "r", encoding="utf-8") to decode UTF-8 text and open(path, "w", encoding="utf-8") to encode written text explicitly.   [sources: python_stdlib_reference#functions.html#open]
A.f2: The encoding argument specifies the text encoding; the selected encoding must match the file’s bytes for correct decoding.   [sources: python_stdlib_reference#functions.html#open]
A.f3: A UnicodeDecodeError indicates a decoding failure, which can arise when the file’s bytes are invalid for the selected encoding.   [sources: python_stdlib_reference#exceptions.html#UnicodeDecodeError]
note: Begin with this objective: Specify the encoding contract for text-file access.
note: Keep the example in the Encoded files, failures and resource lifetimes tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.file_and_format_errors, python.with_resource_management, python.binary_files.
note: Require linux.filesystem_navigation_and_files before this filesystem, script, module or environment unit; do not teach terminal navigation here.
PRACTICE ANCHOR (live_code): Read the supplied UTF-8 label.txt containing café, then rewrite the same text to label.txt using an explicit UTF-8 encoding for both operations.  SUCCESS: The text read is café, and the rewritten file preserves that text in UTF-8. Both open calls explicitly specify encoding="utf-8", and each file is closed before the next operation.
ASSESSMENT ANCHOR: open_text_file_with_matching_explicit_encoding facts=['f1', 'f2']
ASSESSMENT ANCHOR: diagnose_text_decoding_mismatch facts=['f2', 'f3']

## SOURCE FACTS — B (python.file_and_format_errors)   objective: Handle expected file and parsing failures at a Python I/O boundary.
B.f1: FileNotFoundError indicates that the requested file or directory does not exist; handle it separately from content problems.   [sources: python_stdlib_reference#exceptions.html#FileNotFoundError]
B.f2: UnicodeDecodeError indicates failure to decode the content using the selected encoding.   [sources: python_stdlib_reference#exceptions.html#UnicodeDecodeError]
B.f3: csv.Error reports errors detected by the CSV parser; except csv.Error: can provide a parsing-failure response.   [sources: python_stdlib_reference#csv.html#csv.Error]
B.f4: DictReader fills missing fields with restval, defaulting to None, and places excess fields under restkey, defaulting to None; validate required row fields explicitly rather than assuming malformed row lengths raise csv.Error.   [sources: python_stdlib_reference#csv.html#csv.DictReader]
B.f5: Wrap the import at a boundary with specific exception handlers for missing files, decoding and parser failures, and report each according to its cause.   [sources: python_tutorial#errors.html#handling-exceptions]
note: Begin with this objective: Handle expected file and parsing failures at a Python I/O boundary.
note: Keep the example in the Encoded files, failures and resource lifetimes tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.with_resource_management, python.binary_files, python.datetime_operations.
note: Require linux.filesystem_navigation_and_files before this filesystem, script, module or environment unit; do not teach terminal navigation here.
PRACTICE ANCHOR (live_code): Add specific exception handlers and explicit row validation to a CSV import helper using the label and quantity fields.  SUCCESS: The helper reports missing files, decoding failures and parser-reported failures separately, rejects rows with missing or empty required fields or excess fields, and returns valid rows.
ASSESSMENT ANCHOR: distinguish_missing_file_decoding_and_parser_failures facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: identify_missing_and_excess_csv_row_fields facts=['f4']
ASSESSMENT ANCHOR: select_cause_specific_import_responses facts=['f1', 'f2', 'f3', 'f4', 'f5']

## SOURCE FACTS — C (python.with_resource_management)   objective: Manage resource lifetimes using with.
C.f1: Use with context_expression as resource: followed by an indented body; the context manager enters before the body and exits after it.   [sources: python_language_reference#compound_stmts.html#with]
C.f2: Once entry succeeds, the exit method runs whether the body completes normally or raises an exception; a context manager may suppress an exception.   [sources: python_language_reference#compound_stmts.html#with]
C.f3: For with open(path) as f:, leaving the body closes the file, including when the body raises.   [sources: python_tutorial#inputoutput.html#reading-and-writing-files]
note: Begin with this objective: Manage resource lifetimes using with.
note: Keep the example in the Encoded files, failures and resource lifetimes tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.binary_files, python.datetime_operations, python.local_modules.
note: Require linux.filesystem_navigation_and_files before this filesystem, script, module or environment unit; do not teach terminal navigation here.
PRACTICE ANCHOR (live_code): Use with to read label.txt and ensure that source is closed even when processing text raises a ValueError.  SUCCESS: The file is managed by with, and source.closed is True after both normal completion and a deliberately raised ValueError handled outside the with body.
ASSESSMENT ANCHOR: use_with_context_manager_and_identify_entry_exit_order facts=['f1']
ASSESSMENT ANCHOR: predict_cleanup_and_possible_exception_suppression facts=['f2']
ASSESSMENT ANCHOR: predict_file_closure_on_normal_and_exceptional_exit facts=['f3']

## SOURCE FACTS — D (python.binary_files)   objective: Read and write bytes through binary file streams.
D.f1: The b mode selects binary I/O: open(path, "rb") reads bytes and open(path, "wb") writes bytes rather than str.   [sources: python_stdlib_reference#functions.html#open]
D.f2: wb creates or truncates the destination file.   [sources: python_stdlib_reference#functions.html#open]
D.f3: Read a binary payload with source.read() and write that bytes value with destination.write(payload) to copy it without text decoding.   [sources: python_tutorial#inputoutput.html#methods-of-file-objects]
D.f4: Use managed opening with with to close both files after the copy.   [sources: python_tutorial#inputoutput.html#reading-and-writing-files]
note: Begin with this objective: Read and write bytes through binary file streams.
note: Keep the example in the Encoded files, failures and resource lifetimes tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.datetime_operations, python.local_modules, python.importable_packages.
note: Require linux.filesystem_navigation_and_files before this filesystem, script, module or environment unit; do not teach terminal navigation here.
PRACTICE ANCHOR (live_code): Copy the supplied small binary payload from source.bin to the disposable destination copy.bin without decoding it, using managed opening for both files.  SUCCESS: copy.bin contains exactly the bytes supplied in source.bin, source.bin is unchanged, and both files are closed after their managed blocks finish.
ASSESSMENT ANCHOR: select_binary_modes_and_bytes facts=['f1']
ASSESSMENT ANCHOR: recognize_destination_creation_or_truncation facts=['f2']
ASSESSMENT ANCHOR: preserve_binary_payload_without_decoding facts=['f1', 'f3']
ASSESSMENT ANCHOR: manage_both_file_lifetimes_with_with facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing environment variables with os.environ; Chaining iterables with itertools; Choosing eager or lazy processing; Choosing map or filter for iterable transformations; Choosing random or secrets for randomness; Computing dates and elapsed times with datetime; Creating isolated virtual environments; Creating local modules; Development checks with the Python assert statement; Diagnosing module search-path problems; Generator expressions; Generator functions with yield; Guarding a program entry point; Handling file and data-format failures; Inspecting interpreter runtime information with sys; Installing dependencies with python -m pip; Iterables and iterators; Iterator consumption and exhaustion; Managing resources with with; Matching text patterns with re; Organising importable packages; Parsing command-line arguments with argparse; Reading and writing binary files; Recording program events with logging; Recreating dependencies from requirements files; Running unittest and interpreting its results; Selecting the project environment interpreter; Writing Python unittest test cases

## LESSON, in learner order

### s01 · explainer · Choosing explicit text-file encodings
Understand — 
(definition) Use `open(path, "r", encoding="utf-8")` to decode UTF-8 text and `open(path, "w", encoding="utf-8")` to explicitly encode written text. ⟦A.f1 A:tb2 A:tb4⟧
(definition) The encoding argument specifies how text is encoded. Correct decoding requires the selected encoding to match the file’s bytes. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) `UnicodeDecodeError` signals a decoding failure; bytes invalid for the selected encoding can cause it. A filename does not establish its encoding. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[CODE python]
source = open("label.txt", "r", encoding="utf-8")
text = source.read()
source.close()
destination = open("label.txt", "w", encoding="utf-8")
destination.write(text)
destination.close()
print(text)
  annotations: ['Explicit UTF-8 decoding must match the source bytes.', 'Close the reader before rewriting the file.', 'Explicit UTF-8 encoding for the saved text.']

### s02 · check · Check: Choosing explicit text-file encodings
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.
QUESTION [choice, intro, grading=client] Reading an existing file with a selected text encoding raises UnicodeDecodeError. Which diagnosis is supported?
  ✔ o1: The content could not be decoded; its bytes may be invalid for the selected encoding.
      why: This matches the stated task and the taught behavior.
  ✘ o2: The failure proves the file does not exist.
      why: UnicodeDecodeError is a decoding failure, not evidence of a missing file.
  ✘ o3: The failure proves opening with w will safely preserve the original text.
      why: A decoding failure does not establish a safe rewrite; matching the bytes and encoding is required for correct decoding.
  feedback✔: The content could not be decoded; its bytes may be invalid for the selected encoding.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ["Identify the failure's cause before choosing a response."]  remediation→r01
  MEASURES: A:diagnose_text_decoding_mismatch(f2,f3)   anchors=['assessment:diagnose_text_decoding_mismatch']
  taught-before-tested: A.f2←s01; A.f3←s01

### s03 · hands_on · Preserve the UTF-8 label
Practice — Read the supplied UTF-8 label.txt containing café, then rewrite the same text to label.txt using an explicit UTF-8 encoding for both operations.
QUESTION [code_exercise, core, grading=client] Read the supplied UTF-8 label.txt into text and rewrite the same text to label.txt. Add explicit encoding="utf-8" to both open calls. Keep the read, write, close, and print sequence unchanged: close source before opening destination, and close destination afterward. Tests recreate the local text fixture with different Unicode text and inspect the preserved UTF-8 bytes.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['Variable assignment', 'String literals containing non-ASCII text', 'open("label.txt", "r", encoding="utf-8")', 'open("label.txt", "w", encoding="utf-8")', 'source.read()', 'source.close()', 'destination.write(text)', 'destination.close()', 'print(text)'] blocked=4 items
  file main.py [editable]:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\n\ndef prepare_case(inputs):\n    pathlib.Path("label.txt").write_bytes(inputs["content"].encode("utf-8"))\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [ns["text"], list(pathlib.Path("label.txt").read_bytes()), ns["source"].closed, ns["destination"].closed, ns["source"].encoding, ns["destination"].encoding, captured.getvalue().strip()]\n')

inputs = {'content': 'café'}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
source = open("label.txt", "r")
text = source.read()
source.close()
destination = open("label.txt", "w")
destination.write(text)
destination.close()
print(text)
# END LEARNER

  SOLUTION main.py:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\n\ndef prepare_case(inputs):\n    pathlib.Path("label.txt").write_bytes(inputs["content"].encode("utf-8"))\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [ns["text"], list(pathlib.Path("label.txt").read_bytes()), ns["source"].closed, ns["destination"].closed, ns["source"].encoding, ns["destination"].encoding, captured.getvalue().strip()]\n')

inputs = {'content': 'café'}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
source = open("label.txt", "r", encoding="utf-8")
text = source.read()
source.close()
destination = open("label.txt", "w", encoding="utf-8")
destination.write(text)
destination.close()
print(text)
# END LEARNER

  test t1 (function_call, visible=True): {"function":"check_case","args":[{"content":"café"}],"expected":["café",[99,97,102,195,169],true,true,"utf-8","utf-8","café"]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  test t2 (function_call, visible=True): {"function":"check_case","args":[{"content":"café notebook"}],"expected":["café notebook",[99,97,102,195,169,32,110,111,116,101,98,111,111,107],true,true,"utf-8","utf-8","café notebook"]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"e7b67e26d347ea696c43b5a637e4332832aef1fd8a25e9f91c14269ff2f40a6d","tests_passed":2}
  feedback✔: The completed code meets the task on the supplied fixtures, including the changed inputs.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Follow the input names rather than substituting a fixed answer.', 'Check the required operation and where its result or resource state is observed.']
  MEASURES: A:open_text_file_with_matching_explicit_encoding(f1,f2)   anchors=['practice', 'assessment:open_text_file_with_matching_explicit_encoding']
  taught-before-tested: A.f1←s01; A.f2←s01

### s04 · explainer · Handling file and data-format failures
Understand — 
(definition) `FileNotFoundError` means the requested file or directory does not exist. Handle it separately from content problems. ⟦B.f1 B:tb1 B:tb2⟧
(definition) `UnicodeDecodeError` indicates content could not be decoded using the selected encoding. ⟦B.f2 B:tb1 B:tb3⟧
(definition) `csv.Error` reports parser-detected errors; use a matching handler for parsing failures. ⟦B.f3 B:tb1 B:tb3⟧
(definition) DictReader fills missing fields with restval and stores excess fields under restkey; both default to None. Validate required fields explicitly, rather than assuming wrong row lengths raise `csv.Error`. ⟦B.f4 B:tb1 B:tb3⟧
(definition) At the import boundary, use specific handlers for missing files, decoding failures and parser failures. Report each according to its cause. ⟦B.f5 B:tb3⟧
[CODE python]
import csv

def import_rows(path):
    file = None
    rows = []
    try:
        file = open(path, mode="r", encoding="utf-8", newline="")
        reader = csv.DictReader(file)
        for row in reader:
            if row["label"] is None or row["label"] == "" or row["quantity"] is None or row["quantity"] == "" or None in row:
                return "Invalid row"
            rows.append(row)
        return rows
    except FileNotFoundError:
        return "Missing source"
    except UnicodeDecodeError:
        return "Decoding failure"
    except csv.Error:
        return "Parser failure"
    finally:
        if file is not None:
            file.close()

print(import_rows('valid.csv'))
print(import_rows('missing.csv'))
print(import_rows('excess.csv'))
  annotations: ['Validate required fields and excess fields independently of parser failures.', 'Missing source: not a content problem.', 'Failure to decode with the selected encoding.', 'Handle errors actually reported by the CSV parser.', 'Close an opened file at this boundary.']

### s05 · explainer · Handling file and data-format failures
Understand — 
(example) At the CSV import boundary, distinguish a missing source, a decoding failure and a parser-reported error with their specific handlers. With header label,quantity, a notebook-only row has a missing quantity filled by restval, default None. Excess fields go under restkey, also default None. These row lengths do not automatically raise csv.Error: validate required row fields as well as handling parser failures. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb4 B:tb5⟧

### s06 · check · Check: Handling file and data-format failures
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.
QUESTION [choice, core, grading=client] Choose the response plan for a CSV importer that must handle source, decoding, parser, and row-shape problems separately.
  ✘ o1: Catch FileNotFoundError only; decoding failures and invalid row shapes necessarily raise it.
      why: FileNotFoundError concerns missing sources, not decoding or row validation failures.
  ✔ o2: Use specific FileNotFoundError, UnicodeDecodeError and csv.Error handlers, plus explicit required-field and excess-field validation.
      why: This matches the stated task and the taught behavior.
  ✘ o3: Catch csv.Error only; missing fields and missing files necessarily raise it.
      why: csv.Error reports parser-detected errors; missing sources and decoding failures are separate, and row lengths need explicit validation.
  feedback✔: Use specific FileNotFoundError, UnicodeDecodeError and csv.Error handlers, plus explicit required-field and excess-field validation.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Separate failures reported by exceptions from problems visible in row fields.']  remediation→r03
  MEASURES: B:select_cause_specific_import_responses(f1,f2,f3,f4,f5)   anchors=['assessment:select_cause_specific_import_responses']
  taught-before-tested: B.f1←s04; B.f2←s04; B.f3←s04; B.f4←s04; B.f5←s04

### s07 · hands_on · Handle import causes and validate rows
Practice — Add specific exception handlers and explicit row validation to a CSV import helper using the label and quantity fields.
QUESTION [code_exercise, core, grading=client] The UTF-8 DictReader helper, row validation, and finally cleanup are supplied. Set its four message variables: invalid_row_message to "Invalid row" for missing, empty, or excess fields; missing_source_message to "Missing source" for FileNotFoundError; decoding_failed_message to "Decoding failed" for UnicodeDecodeError; and parsing_failed_message to "Parsing failed" for csv.Error. Leave the supplied reader unchanged. Tests also verify valid rows and file cleanup.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['import csv', 'def and return', 'variable assignment', 'open(path, mode="r", encoding="utf-8", newline="")', 'file.close()', 'try, except FileNotFoundError, except UnicodeDecodeError, except csv.Error, and finally', 'csv.DictReader(file)', 'for row in reader', 'if and else', 'and, or, and not', 'dictionary indexing and membership checks', 'is None and is not None', 'string literals and equality comparisons', 'list literals and list.append()'] blocked=15 items
  file main.py [editable]:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\ndef import_probe(ns, inputs):\n    original = csv.DictReader\n    opened = []\n    def tracked_open(*args, **kwargs):\n        f = builtins.open(*args, **kwargs)\n        opened.append(f)\n        return f\n    def parser_failure(file):\n        raise csv.Error("Parser-reported failure")\n    ns["open"] = tracked_open\n    try:\n        if inputs["parser_failure"]:\n            csv.DictReader = parser_failure\n        result = ns["import_rows"](inputs["path"])\n        return [result, all(f.closed for f in opened)]\n    finally:\n        csv.DictReader = original\n\n\ndef prepare_case(inputs):\n    p = pathlib.Path(inputs["path"])\n    if p.exists(): p.unlink()\n    if inputs["content"] is not None: p.write_text(inputs["content"], encoding="utf-8")\n    if inputs["invalid_bytes"]: p.write_bytes(b"label,quantity\\nnotebook,\\xff\\n")\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return import_probe(ns, inputs)\n')

inputs = {'path': 'valid.csv', 'content': 'label,quantity\nnotebook,3\nnotebook,2\n', 'parser_failure': False, 'invalid_bytes': False}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
invalid_row_message = ""
missing_source_message = ""
decoding_failed_message = ""
parsing_failed_message = ""
# Supplied validated reader and cleanup; leave unchanged.
exec('import csv\n\ndef import_rows(path):\n    file = None\n    rows = []\n    try:\n        file = open(path, mode="r", encoding="utf-8", newline="")\n        reader = csv.DictReader(file)\n        for row in reader:\n            if "label" not in row or "quantity" not in row or row["label"] is None or row["quantity"] is None or row["label"] == "" or row["quantity"] == "" or None in row:\n                return invalid_row_message\n            else:\n                rows.append(row)\n        return rows\n    except FileNotFoundError:\n        return missing_source_message\n    except UnicodeDecodeError:\n        return decoding_failed_message\n    except csv.Error:\n        return parsing_failed_message\n    finally:\n        if file is not None:\n            file.close()\n')
# END LEARNER

  SOLUTION main.py:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\ndef import_probe(ns, inputs):\n    original = csv.DictReader\n    opened = []\n    def tracked_open(*args, **kwargs):\n        f = builtins.open(*args, **kwargs)\n        opened.append(f)\n        return f\n    def parser_failure(file):\n        raise csv.Error("Parser-reported failure")\n    ns["open"] = tracked_open\n    try:\n        if inputs["parser_failure"]:\n            csv.DictReader = parser_failure\n        result = ns["import_rows"](inputs["path"])\n        return [result, all(f.closed for f in opened)]\n    finally:\n        csv.DictReader = original\n\n\ndef prepare_case(inputs):\n    p = pathlib.Path(inputs["path"])\n    if p.exists(): p.unlink()\n    if inputs["content"] is not None: p.write_text(inputs["content"], encoding="utf-8")\n    if inputs["invalid_bytes"]: p.write_bytes(b"label,quantity\\nnotebook,\\xff\\n")\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return import_probe(ns, inputs)\n')

inputs = {'path': 'valid.csv', 'content': 'label,quantity\nnotebook,3\nnotebook,2\n', 'parser_failure': False, 'invalid_bytes': False}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
invalid_row_message = "Invalid row"
missing_source_message = "Missing source"
decoding_failed_message = "Decoding failed"
parsing_failed_message = "Parsing failed"
# Supplied validated reader and cleanup; leave unchanged.
exec('import csv\n\ndef import_rows(path):\n    file = None\n    rows = []\n    try:\n        file = open(path, mode="r", encoding="utf-8", newline="")\n        reader = csv.DictReader(file)\n        for row in reader:\n            if "label" not in row or "quantity" not in row or row["label"] is None or row["quantity"] is None or row["label"] == "" or row["quantity"] == "" or None in row:\n                return invalid_row_message\n            else:\n                rows.append(row)\n        return rows\n    except FileNotFoundError:\n        return missing_source_message\n    except UnicodeDecodeError:\n        return decoding_failed_message\n    except csv.Error:\n        return parsing_failed_message\n    finally:\n        if file is not None:\n            file.close()\n')
# END LEARNER

  test t1 (function_call, visible=True): {"function":"check_case","args":[{"path":"valid.csv","content":"label,quantity\nnotebook,3\nnotebook,2\n","parser_failure":false,"invalid_bytes":false}],"expected":[[{"label":"notebook","quantity":"3"},{"label":"notebook","quantity":"2"}],true]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  test t2 (function_call, visible=True): {"function":"check_case","args":[{"path":"missing.csv","content":"label,quantity\nnotebook\n","parser_failure":false,"invalid_bytes":false}],"expected":["Invalid row",true]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  test t3 (function_call, visible=True): {"function":"check_case","args":[{"path":"empty.csv","content":"label,quantity\nnotebook,\n","parser_failure":false,"invalid_bytes":false}],"expected":["Invalid row",true]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  test t4 (function_call, visible=True): {"function":"check_case","args":[{"path":"excess.csv","content":"label,quantity\nnotebook,3,extra\n","parser_failure":false,"invalid_bytes":false}],"expected":["Invalid row",true]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  test t5 (function_call, visible=True): {"function":"check_case","args":[{"path":"nonexistent.csv","content":null,"parser_failure":false,"invalid_bytes":false}],"expected":["Missing source",true]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  test t6 (function_call, visible=True): {"function":"check_case","args":[{"path":"invalid_utf8.csv","content":null,"parser_failure":false,"invalid_bytes":true}],"expected":["Decoding failed",true]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  test t7 (function_call, visible=True): {"function":"check_case","args":[{"path":"valid.csv","content":"label,quantity\nnotebook,3\nnotebook,2\n","parser_failure":true,"invalid_bytes":false}],"expected":["Parsing failed",true]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"4e50ea1567b99676df82d70306d98559676ac7cdd0e0ca1e65229141d0a2b011","tests_passed":7}
  feedback✔: The completed code meets the task on the supplied fixtures, including the changed inputs.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Follow the input names rather than substituting a fixed answer.', 'Check the required operation and where its result or resource state is observed.']
  MEASURES: B:distinguish_missing_file_decoding_and_parser_failures(f1,f2,f3); B:identify_missing_and_excess_csv_row_fields(f4); B:select_cause_specific_import_responses(f1,f2,f3,f4,f5)   anchors=['practice', 'assessment:distinguish_missing_file_decoding_and_parser_failures', 'assessment:identify_missing_and_excess_csv_row_fields', 'assessment:select_cause_specific_import_responses']
  taught-before-tested: B.f1←s04; B.f2←s04; B.f3←s04; B.f4←s04; B.f1←s04; B.f2←s04; B.f3←s04; B.f4←s04; B.f5←s04

### s08 · explainer · Managing resources with with
Understand — 
(definition) Use `with context_expression as resource:` followed by an indented body. The context manager enters before that body and exits afterward. ⟦C.f1 C:tb1 C:tb2 C:tb4⟧
(definition) After entry succeeds, exit runs on normal completion or a raised body exception. A general context manager may suppress an exception. ⟦C.f2 C:tb1 C:tb3 C:tb4 C:tb5⟧
(definition) For `with open(path) as f:`, leaving the body closes the file even when the body raises. Keep this file-closing behavior distinct from general exception suppression. ⟦C.f3 C:tb3 C:tb4 C:tb5⟧
[PROCESS_FLOW: After entry succeeds, both body exit paths close the opened file] nodes=['Successful file entry', 'Indented read/process body', 'Normal completion', 'Body raises', 'File closes at exit'] edges=[('entry', 'body', 'enter before body'), ('body', 'normal', 'finishes'), ('body', 'raised', 'exception'), ('normal', 'closed', 'exit'), ('raised', 'closed', 'exit')] alt: After entry succeeds, both body exit paths close the opened file

### s09 · video · Automatic file cleanup with with
Observe — 
[VIDEO Automatic file cleanup with with] bridge-before: Watch for the contrast between explicit file closure and using with: the latter handles cleanup even when working with the file raises an error. | bridge-after: The clip establishes file closure, including on errors. The text supplies the complete with syntax, entry-before-body and exit-after-body ordering, and the general possibility of exception suppression.
  - -aKFBoZpiqA 0-71s facts=['f3'] label: Replace explicit file closure with with | summary: Context managers manage resource setup and cleanup. An explicit open, write, and close sequence requires remembering to close the file. Using with for the file operation removes that separate cleanup step: the file closes when the work finishes, including when an error occurs during that work.

### s10 · check · Check: Managing resources with with
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.
QUESTION [choice, core, grading=client] After a general context manager enters successfully, its body raises an exception. Which sequence and exception claim are supported?
  ✘ o1: Entry occurs after the body; exit is skipped when the body raises.
      why: Entry precedes the body, and after successful entry, exit runs even when the body raises.
  ✘ o2: Entry occurred before the body; exit always forces every exception to propagate.
      why: A general context manager may suppress an exception; propagation is not guaranteed for every manager.
  ✔ o3: Entry occurred before the body; exit runs afterward and may suppress the exception.
      why: This matches the stated task and the taught behavior.
  feedback✔: Entry occurred before the body; exit runs afterward and may suppress the exception.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Separate the entry/exit order from whether a manager suppresses an exception.']  remediation→r04
  MEASURES: C:use_with_context_manager_and_identify_entry_exit_order(f1); C:predict_cleanup_and_possible_exception_suppression(f2)   anchors=['assessment:use_with_context_manager_and_identify_entry_exit_order', 'assessment:predict_cleanup_and_possible_exception_suppression']
  taught-before-tested: C.f1←s08; C.f2←s08

### s11 · check · Check: Managing resources with with
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.
QUESTION [choice, core, grading=client] In with open(path) as source:, entry succeeds and the body raises ValueError. An outer handler catches it. What is the file's state after leaving the with body?
  ✘ o1: source closes only if the body called source.close().
      why: Managed opening supplies file closure when leaving the body; an explicit close in the body is not required.
  ✔ o2: source is closed.
      why: This matches the stated task and the taught behavior.
  ✘ o3: source stays open because the body raised.
      why: Leaving the managed file body closes the file on exceptional exit too.
  feedback✔: source is closed.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Follow the resource lifetime across the body boundary.']
  MEASURES: C:predict_file_closure_on_normal_and_exceptional_exit(f3)   anchors=['assessment:predict_file_closure_on_normal_and_exceptional_exit']
  taught-before-tested: C.f3←s08

### s12 · hands_on · Manage both file exit paths
Practice — Use with to read label.txt and ensure that source is closed even when processing text raises a ValueError.
QUESTION [code_exercise, intro, grading=client] Both normal and exceptional with-managed reads are supplied. At the marked line, print normal_closed, the closed-state value saved after the normal with block. Preserve the supplied deliberately raised ValueError and its outside handler, and the final exceptional closed-state display. Output must show True, then Processing failed, then True on separate lines.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['with open("label.txt", "r", encoding="utf-8") as source:', 'indented blocks', 'text = source.read()', 'source.closed', 'print()', 'try/except ValueError', 'raise ValueError("Processing failed")', 'variable assignment', 'string literals'] blocked=11 items
  file main.py [editable]:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\n\ndef prepare_case(inputs):\n    pathlib.Path("label.txt").write_bytes(inputs["content"].encode("utf-8"))\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [ns["text"], ns["normal_closed"], ns["exceptional_closed"], captured.getvalue().strip()]\n')

inputs = {'content': 'café'}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
with open("label.txt", "r", encoding="utf-8") as source:
    text = source.read()
normal_closed = source.closed
# Print the normal closed state here.
try:
    with open("label.txt", "r", encoding="utf-8") as source:
        text = source.read()
        raise ValueError("Processing failed")
except ValueError:
    print("Processing failed")
exceptional_closed = source.closed
print(source.closed)
# END LEARNER

  SOLUTION main.py:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\n\ndef prepare_case(inputs):\n    pathlib.Path("label.txt").write_bytes(inputs["content"].encode("utf-8"))\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [ns["text"], ns["normal_closed"], ns["exceptional_closed"], captured.getvalue().strip()]\n')

inputs = {'content': 'café'}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
with open("label.txt", "r", encoding="utf-8") as source:
    text = source.read()
normal_closed = source.closed
print(normal_closed)
try:
    with open("label.txt", "r", encoding="utf-8") as source:
        text = source.read()
        raise ValueError("Processing failed")
except ValueError:
    print("Processing failed")
exceptional_closed = source.closed
print(source.closed)
# END LEARNER

  test t1 (function_call, visible=True): {"function":"check_case","args":[{"content":"café"}],"expected":["café",true,true,"True\nProcessing failed\nTrue"]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  test t2 (function_call, visible=True): {"function":"check_case","args":[{"content":"café notebook"}],"expected":["café notebook",true,true,"True\nProcessing failed\nTrue"]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"eb2f61c4da3c124a9063f531bfb89bcd6d147cfc103dde83dcacbf7e6c8c0e53","tests_passed":2}
  feedback✔: The completed code meets the task on the supplied fixtures, including the changed inputs.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Follow the input names rather than substituting a fixed answer.', 'Check the required operation and where its result or resource state is observed.']
  MEASURES: C:use_with_context_manager_and_identify_entry_exit_order(f1); C:predict_file_closure_on_normal_and_exceptional_exit(f3)   anchors=['practice']
  taught-before-tested: C.f1←s08; C.f3←s08

### s13 · explainer · Reading and writing binary files
Understand — 
(definition) Binary mode `b` uses bytes rather than strings: `rb` reads bytes and `wb` writes bytes. ⟦D.f1 D:tb2 D:tb4 D:tb5⟧
(definition) `wb` creates or truncates the destination. Choose a destination whose replacement is intended. ⟦D.f2 D:tb3 D:tb4 D:tb5⟧
(definition) Assign `source.read()` to payload and pass that bytes value directly to `destination.write(payload)` to copy without text decoding. ⟦D.f3 D:tb3 D:tb4⟧
(definition) Manage both openings with `with` so each file closes after its managed body. ⟦D.f4 D:tb3 D:tb4⟧
[CODE python]
with open("source.bin", "rb") as source:
    with open("copy.bin", "wb") as destination:
        payload = source.read()
        destination.write(payload)
  annotations: ['Managed rb source reads bytes and closes at outer exit.', 'Managed wb destination creates or truncates; closes at inner exit.', 'Keep the read value as bytes.', 'Write those bytes unchanged, with no text decoding.']

### s14 · video · Copy binary content with managed file streams
Observe — 
[VIDEO Copy binary content with managed file streams] bridge-before: Watch how nested with statements manage the two files and how rb and wb replace text modes. The example progresses from copying text to copying image bytes in chunks. | bridge-after: The clip demonstrates binary copying but does not explain wb truncation. The text covers destination creation or truncation, explicitly explains automatic closure, and teaches a whole-payload read for a small file.
  - Uh2ebFW8OYM 1083-1440s facts=['f1', 'f3', 'f4'] label: Copy an image using binary reads and writes | summary: Nested with statements open a source for reading and a destination for writing. After copying a text file, the example attempts to copy a JPEG in text mode and encounters a decoding error. Changing the modes to rb and wb makes the operations read and write bytes instead of text. The example then copies the image in chunks: each read supplies bytes to write, and the loop reads another chunk until none remain. The copied image is opened to check the result.

### s15 · check · Check: Reading and writing binary files
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.
QUESTION [choice, core, grading=client] copy.bin already exists and is a disposable destination. What does opening it with wb do?
  ✘ o1: Appends bytes while preserving all existing contents.
      why: wb truncates an existing destination; it is not append mode.
  ✘ o2: Fails exclusively because the destination already exists.
      why: wb creates or truncates the destination; exclusive creation is a different mode.
  ✔ o3: Opens for bytes writing and truncates existing contents.
      why: This matches the stated task and the taught behavior.
  feedback✔: Opens for bytes writing and truncates existing contents.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Check the write mode before deciding whether existing contents survive.']  remediation→r07
  MEASURES: D:recognize_destination_creation_or_truncation(f2)   anchors=['assessment:recognize_destination_creation_or_truncation']
  taught-before-tested: D.f2←s13

### s16 · hands_on · Copy the binary payload
Practice — Copy the supplied small binary payload from source.bin to the disposable destination copy.bin without decoding it, using managed opening for both files.
QUESTION [code_exercise, stretch, grading=client] The nested managed copy, direct payload read/write, and cleanup are supplied. Set source_mode and destination_mode to the binary read and binary write modes respectively. Leave the nested with blocks unchanged. copy.bin must match source.bin byte-for-byte without decoding; source.bin must remain unchanged and both streams must close.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['with open("source.bin", "rb") as source:', 'with open("copy.bin", "wb") as destination:', 'nested indented blocks', 'payload = source.read()', 'destination.write(payload)'] blocked=9 items
  file main.py [editable]:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\n\ndef prepare_case(inputs):\n    pathlib.Path("source.bin").write_bytes(inputs["content"].encode("utf-8"))\n    pathlib.Path("copy.bin").write_text("Disposable destination")\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [list(pathlib.Path("source.bin").read_bytes()), list(pathlib.Path("copy.bin").read_bytes()), ns["source"].closed, ns["destination"].closed, type(ns["payload"]).__name__]\n')

inputs = {'content': '\x00\x01\x02\x03\n\rA\x7f'}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
source_mode = "r"
destination_mode = "w"
with open("source.bin", source_mode) as source:
    with open("copy.bin", destination_mode) as destination:
        payload = source.read()
        destination.write(payload)
# END LEARNER

  SOLUTION main.py:
# Supplied host fixtures: leave this immutable setup unchanged.
exec('import pathlib\n\nimport shutil\n\nimport contextlib\n\nimport io\n\nimport json\n\nimport csv\n\nimport builtins\n\nimport ast\n\n\ndef prepare_case(inputs):\n    pathlib.Path("source.bin").write_bytes(inputs["content"].encode("utf-8"))\n    pathlib.Path("copy.bin").write_text("Disposable destination")\n    return inputs\n\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return [list(pathlib.Path("source.bin").read_bytes()), list(pathlib.Path("copy.bin").read_bytes()), ns["source"].closed, ns["destination"].closed, type(ns["payload"]).__name__]\n')

inputs = {'content': '\x00\x01\x02\x03\n\rA\x7f'}
globals().update(inputs)
globals().update(prepare_case(inputs) or {})

# BEGIN LEARNER
source_mode = "rb"
destination_mode = "wb"
with open("source.bin", source_mode) as source:
    with open("copy.bin", destination_mode) as destination:
        payload = source.read()
        destination.write(payload)
# END LEARNER

  test t1 (function_call, visible=True): {"function":"check_case","args":[{"content":"\u0000\u0001\u0002\u0003\n\rA"}],"expected":[[0,1,2,3,10,13,65,127],[0,1,2,3,10,13,65,127],true,true,"bytes"]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  test t2 (function_call, visible=True): {"function":"check_case","args":[{"content":"A\r\n\u0003\u0002\u0001\u0000"}],"expected":[[127,65,13,10,3,2,1,0],[127,65,13,10,3,2,1,0],true,true,"bytes"]} | on-fail: The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"fc06f4949b8be6362a707289156a706fbce084d2f33dc418434fa6cab0cfb110","tests_passed":2}
  feedback✔: The completed code meets the task on the supplied fixtures, including the changed inputs.  feedback✘: Recheck the operation and trace which object, value, or resource each line affects.  hints: ['Follow the input names rather than substituting a fixed answer.', 'Check the required operation and where its result or resource state is observed.']
  MEASURES: D:select_binary_modes_and_bytes(f1); D:preserve_binary_payload_without_decoding(f1,f3); D:manage_both_file_lifetimes_with_with(f4)   anchors=['practice', 'assessment:select_binary_modes_and_bytes', 'assessment:preserve_binary_payload_without_decoding', 'assessment:manage_both_file_lifetimes_with_with']
  taught-before-tested: D.f1←s13; D.f1←s13; D.f3←s13; D.f4←s13

### s17 · recap · Keep these distinctions
Takeaways — 
(takeaway) Read label.txt with an encoding matching its bytes, not one guessed from its filename. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(takeaway) A missing quantity is row data to validate; it is not automatically a parser exception. ⟦B.f3 B.f4 B:tb1 B:tb3 B:tb4 B:tb5⟧
(takeaway) An opened file closes on either exit path; general managers may also suppress an exception. ⟦C.f2 C.f3 C:tb1 C:tb3 C:tb4 C:tb5⟧
(takeaway) Pass bytes directly to the destination; do not turn this copy into a text-decoding operation. ⟦D.f1 D.f3 D:tb2 D:tb3 D:tb4 D:tb5⟧
[UP NEXT] Up next: Computing dates and elapsed times with datetime: Next, begin computing dates and elapsed times with datetime.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: Choosing explicit text-file encodings
(definition) The encoding argument specifies how text is encoded. Correct decoding requires the selected encoding to match the file’s bytes. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) `UnicodeDecodeError` signals a decoding failure; bytes invalid for the selected encoding can cause it. A filename does not establish its encoding. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Read label.txt with an encoding matching its bytes, not one guessed from its filename. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit: Choosing explicit text-file encodings
(definition) Use `open(path, "r", encoding="utf-8")` to decode UTF-8 text and `open(path, "w", encoding="utf-8")` to explicitly encode written text. ⟦A.f1 A:tb2 A:tb4⟧
(definition) The encoding argument specifies how text is encoded. Correct decoding requires the selected encoding to match the file’s bytes. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) Read label.txt with an encoding matching its bytes, not one guessed from its filename. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · Revisit: Handling file and data-format failures
(definition) `FileNotFoundError` means the requested file or directory does not exist. Handle it separately from content problems. ⟦B.f1 B:tb1 B:tb2 B:tb4⟧
(definition) `UnicodeDecodeError` indicates content could not be decoded using the selected encoding. ⟦B.f2 B:tb1 B:tb3 B:tb4⟧
(definition) `csv.Error` reports parser-detected errors; use a matching handler for parsing failures. ⟦B.f3 B:tb1 B:tb3 B:tb4⟧
(definition) DictReader fills missing fields with restval and stores excess fields under restkey; both default to None. Validate required fields explicitly, rather than assuming wrong row lengths raise `csv.Error`. ⟦B.f4 B:tb1 B:tb3 B:tb4 B:tb5⟧
(definition) At the import boundary, use specific handlers for missing files, decoding failures and parser failures. Report each according to its cause. ⟦B.f5 B:tb3 B:tb4⟧
(misconception) A missing quantity is row data to validate; it is not automatically a parser exception. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r04 · Revisit: Managing resources with with
(definition) Use `with context_expression as resource:` followed by an indented body. The context manager enters before that body and exits afterward. ⟦C.f1 C:tb1 C:tb2 C:tb4⟧
(definition) After entry succeeds, exit runs on normal completion or a raised body exception. A general context manager may suppress an exception. ⟦C.f2 C:tb1 C:tb3 C:tb4 C:tb5⟧
(misconception) An opened file closes on either exit path; general managers may also suppress an exception. ⟦C.f1 C.f2 C:tb1 C:tb2 C:tb3 C:tb4 C:tb5⟧
### r05 · Revisit: Managing resources with with
(definition) For `with open(path) as f:`, leaving the body closes the file even when the body raises. Keep this file-closing behavior distinct from general exception suppression. ⟦C.f3 C:tb3 C:tb4 C:tb5⟧
(misconception) An opened file closes on either exit path; general managers may also suppress an exception. ⟦C.f3 C:tb3 C:tb4 C:tb5⟧
### r06 · Revisit: Managing resources with with
(definition) Use `with context_expression as resource:` followed by an indented body. The context manager enters before that body and exits afterward. ⟦C.f1 C:tb1 C:tb2 C:tb4⟧
(definition) After entry succeeds, exit runs on normal completion or a raised body exception. A general context manager may suppress an exception. ⟦C.f2 C:tb1 C:tb3 C:tb4 C:tb5⟧
(definition) For `with open(path) as f:`, leaving the body closes the file even when the body raises. Keep this file-closing behavior distinct from general exception suppression. ⟦C.f3 C:tb3 C:tb4 C:tb5⟧
(misconception) An opened file closes on either exit path; general managers may also suppress an exception. ⟦C.f1 C.f2 C.f3 C:tb1 C:tb2 C:tb3 C:tb4 C:tb5⟧
### r07 · Revisit: Reading and writing binary files
(definition) `wb` creates or truncates the destination. Choose a destination whose replacement is intended. ⟦D.f2 D:tb3 D:tb4 D:tb5⟧
(misconception) Pass bytes directly to the destination; do not turn this copy into a text-decoding operation. ⟦D.f2 D:tb3 D:tb4 D:tb5⟧
### r08 · Revisit: Reading and writing binary files
(definition) Binary mode `b` uses bytes rather than strings: `rb` reads bytes and `wb` writes bytes. ⟦D.f1 D:tb2 D:tb4 D:tb5⟧
(definition) Assign `source.read()` to payload and pass that bytes value directly to `destination.write(payload)` to copy without text decoding. ⟦D.f3 D:tb3 D:tb4⟧
(definition) Manage both openings with `with` so each file closes after its managed body. ⟦D.f4 D:tb3 D:tb4⟧
(misconception) Pass bytes directly to the destination; do not turn this copy into a text-decoding operation. ⟦D.f1 D.f3 D.f4 D:tb2 D:tb3 D:tb4 D:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: open(..., mode="rb")
· args.content: label,quantity
notebook,3
notebook,2

· args.content: label,quantity
notebook

· args.content: label,quantity
notebook,

· args.content: label,quantity
notebook,3,extra

· args.content: label,quantity
notebook,3
notebook,2

· constraints.blocked_syntax: open() with binary modes
· spec.expected: True
Processing failed
True
· spec.expected: True
Processing failed
True
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast