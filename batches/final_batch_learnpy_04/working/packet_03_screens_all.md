# EVALUATOR PACKET — Classes and instances (learn_python.tile.066_066)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.classes_and_instances — Classes and instances

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Check: Classes and instances
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.

### s04 · hands_on · Create separate Order instances
Practice — Define an empty Order class, create first and second as separate instances, and demonstrate their separate identities using is.

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Check: Selecting safe file-opening modes
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.

### s04 · check · Check: Selecting safe file-opening modes
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.

### s05 · hands_on · Create a report without replacement
Practice — Write First to a new report.txt using exclusive creation, and handle an existing destination without replacing or extending its contents.

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · check · Check: Initialising instance state with __init__
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.

### s04 · hands_on · Store constructor arguments
Practice — Initialize an Order record with a label and quantity supplied as constructor arguments.

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

### s07 · check · Check: Instance methods and self
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.

### s08 · hands_on · Update the receiving Order
Practice — Add an add(self, amount) method to Order that increases the receiving object's stored quantity by amount.

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

### s11 · check · Check: Choosing instance, class or static method binding
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.

### s12 · hands_on · Construct through cls
Practice — Implement Order.from_text as a class method that converts a quantity string to an integer and constructs an Order through cls.

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · hands_on · Replace the collaborator
Practice — Give a Report object a formatter collaborator, store it as instance data, and delegate formatting to it from an instance method.

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

### s06 · hands_on · Expose the public operation
Practice — Expose Order.add(amount) as a public operation and mark its supporting quantity attribute non-public with a leading underscore.

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
[VIDEO ] bridge-before:  | bridge-after: 

### s09 · check · Check: Extending inherited behavior with super
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.

### s10 · hands_on · Extend Order behavior
Practice — Extend an Order formatter with a FeeOrder formatter: preserve inherited quantity initialization, store fee, and extend the inherited formatted result through super().

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · hands_on · Signal and handle an invalid record
Practice — Define InvalidRecordError as an Exception subclass and use it in check_quantity(quantity) to reject a negative quantity, handling the failure around the validator call.

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
  annotations: ['Class-body list shared unless shadowed.', 'Mutates the shared list.']
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
  annotations: ['Create a new list for each instance.', 'Only first’s instance list is changed.']

### s02 · video · Shared class attributes and individual instance state
Observe — 
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Check: Instance versus class attributes
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.

### s04 · hands_on · Give each Order its own list
Practice — Move a mistakenly shared labels list from the Order class body into instance initialization as self.labels = [].

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
print(type(restored["quantities"][0]))
print(restored["active"])
  annotations: []

### s02 · video · Deserialising JSON text into Python values
Observe — 
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Check: Serialising and deserialising data with Python json
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.

### s04 · check · Check: Serialising and deserialising data with Python json
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.

### s05 · hands_on · Inspect a JSON round trip
Practice — Round-trip a nested record containing quantities and active through a JSON string using json.dumps and json.loads, then check the reconstructed values with equality comparisons.

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
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast

=========

# EVALUATOR PACKET — Inspecting object types and attributes (learn_python.tile.077_077)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.object_introspection — Inspecting object types and attributes

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
  annotations: ['Inspect the object’s type.', 'Class membership includes subclasses.', 'Retrieve the quantity attribute by name.', 'Use a fallback when the named attribute is absent.', 'Candidate relevant names, not a guaranteed complete public API; underscores signal internal use.']

### s02 · check · Check: Inspecting object types and attributes
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.

### s03 · hands_on · Inspect an Order object
Practice — Inspect an Order instance returned by a supplied helper: determine its type, check its membership in Order, list candidate public attribute names, and retrieve quantity and an absent attribute with a fallback.

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s04 · hands_on · Move the report to its output directory
Practice — Create the supplied output directory, including missing parents, and move the supplied generated report into it using a destination constructed from directory and filename.

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
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast

=========

# EVALUATOR PACKET — Defining useful object representations with special methods (learn_python.tile.079_079)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.special_methods — Defining useful object representations with special methods

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
  annotations: ['Return an information-rich string for repr and inspection.', 'Return a user-facing string for str and print.', 'Use __repr__.', 'Use __str__; without it the default uses __repr__.']
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
  annotations: ['With __str__ removed, the default uses __repr__.']

### s02 · video · Separate inspection and user-facing representations
Observe — 
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Check: Defining useful object representations with special methods
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.

### s04 · hands_on · Return two representations
Practice — Give an Order object with a quantity attribute useful inspection and user-facing representations by implementing __repr__ and __str__.

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
· remediation_steps.eyebrow: Try a clearer contrast

=========

# EVALUATOR PACKET — Choosing explicit text-file encodings / Handling file and data-format failures / Managing resources with with / Reading and writing binary files (learn_python.tile.080_083)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.text_file_encodings — Choosing explicit text-file encodings
B = python.file_and_format_errors — Handling file and data-format failures
C = python.with_resource_management — Managing resources with with
D = python.binary_files — Reading and writing binary files

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · hands_on · Preserve the UTF-8 label
Practice — Read the supplied UTF-8 label.txt containing café, then rewrite the same text to label.txt using an explicit UTF-8 encoding for both operations.

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

### s07 · hands_on · Handle import causes and validate rows
Practice — Add specific exception handlers and explicit row validation to a CSV import helper using the label and quantity fields.

### s08 · explainer · Managing resources with with
Understand — 
(definition) Use `with context_expression as resource:` followed by an indented body. The context manager enters before that body and exits afterward. ⟦C.f1 C:tb1 C:tb2 C:tb4⟧
(definition) After entry succeeds, exit runs on normal completion or a raised body exception. A general context manager may suppress an exception. ⟦C.f2 C:tb1 C:tb3 C:tb4 C:tb5⟧
(definition) For `with open(path) as f:`, leaving the body closes the file even when the body raises. Keep this file-closing behavior distinct from general exception suppression. ⟦C.f3 C:tb3 C:tb4 C:tb5⟧
[PROCESS_FLOW: After entry succeeds, both body exit paths close the opened file] nodes=['Successful file entry', 'Indented read/process body', 'Normal completion', 'Body raises', 'File closes at exit'] edges=[('entry', 'body', 'enter before body'), ('body', 'normal', 'finishes'), ('body', 'raised', 'exception'), ('normal', 'closed', 'exit'), ('raised', 'closed', 'exit')] alt: After entry succeeds, both body exit paths close the opened file

### s09 · video · Automatic file cleanup with with
Observe — 
[VIDEO ] bridge-before:  | bridge-after: 

### s10 · check · Check: Managing resources with with
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.

### s11 · check · Check: Managing resources with with
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.

### s12 · hands_on · Manage both file exit paths
Practice — Use with to read label.txt and ensure that source is closed even when processing text raises a ValueError.

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
[VIDEO ] bridge-before:  | bridge-after: 

### s15 · check · Check: Reading and writing binary files
Check your understanding — Read the supplied question and choose the answer that follows the rules you have learned.

### s16 · hands_on · Copy the binary payload
Practice — Copy the supplied small binary payload from source.bin to the disposable destination copy.bin without decoding it, using managed opening for both files.

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
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast
· remediation_steps.eyebrow: Try a clearer contrast