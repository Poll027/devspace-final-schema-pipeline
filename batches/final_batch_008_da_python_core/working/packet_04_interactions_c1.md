# EVALUATOR PACKET — Lists, Dictionaries, and Tuples (tile_python_lists_dicts_tuples)
Tile summary: Store ordered sequences in lists, map keys to values in dictionaries, and group fixed records in immutable tuples.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.lists — Core data structure: lists
B = python.dictionaries — Core data structure: dictionaries
C = python.tuples — Core data structure: tuples

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (python.lists)   objective: Create a list, then index into it, slice it, and append a new item to build and read an ordered, mutable collection.
A.f1: A list is written as a comma-separated sequence of values inside square brackets, e.g. squares = [1, 4, 9, 16, 25].   [sources: python_docs_tutorial_introduction#lists]
A.f2: Like strings, lists can be indexed (squares[0] returns the first item, squares[-1] returns the last) and sliced (squares[-3:] returns a new list of the last three items).   [sources: python_docs_tutorial_introduction#lists]
A.f3: Lists are mutable: an item can be replaced in place, e.g. cubes[3] = 64 changes the value stored at that index.   [sources: python_docs_tutorial_introduction#lists]
A.f4: New items can be added to the end of a list with the list.append() method.   [sources: python_docs_tutorial_introduction#lists, python_docs_tutorial_datastructures#more-on-lists]
A.f5: In a slice such as word[0:2], the start index is included and the end index is excluded; lists support the same indexing and slicing operations as strings, e.g. squares[1:3] returns [4, 9], the items from index 1 up to but not including index 3.   [sources: python_docs_tutorial_introduction#text, python_docs_tutorial_introduction#lists]
note: Keep delivery_times = [32, 45, 21, 60, 18] as the one running list for every operation in this entry.
PRACTICE ANCHOR (live_code): Build a list of delivery times, append one more item, and retrieve a slice of it.  SUCCESS: The list holds the original items plus the appended one, and the printed slice is exactly the expected items.
ASSESSMENT ANCHOR: create_a_list facts=['f1']
ASSESSMENT ANCHOR: index_and_slice_a_list facts=['f2', 'f5']
ASSESSMENT ANCHOR: modify_and_extend_a_list facts=['f3', 'f4']

## SOURCE FACTS — B (python.dictionaries)   objective: Build a dictionary mapping keys to values, and look up, add, or update a value by its key.
B.f1: A dictionary is a collection of key: value pairs, written inside braces, where the keys must be unique within the dictionary.   [sources: python_docs_tutorial_datastructures#dictionaries]
B.f2: A value is stored or updated by assigning to a key, e.g. tel['guido'] = 4127, and retrieved by subscripting with the key, e.g. tel['jack'].   [sources: python_docs_tutorial_datastructures#dictionaries]
B.f3: Extracting a value for a key that is not in the dictionary by subscripting raises a KeyError.   [sources: python_docs_tutorial_datastructures#dictionaries]
B.f4: The get() method returns None or a specified default instead of raising an error when a key is not in the dictionary.   [sources: python_docs_tutorial_datastructures#dictionaries]
B.f5: The in keyword checks whether a key is present in a dictionary.   [sources: python_docs_tutorial_datastructures#dictionaries]
note: Keep order_city as the one running dictionary across all blocks.
PRACTICE ANCHOR (live_code): Build a dictionary mapping product names to prices and look up one price by its key.  SUCCESS: The dictionary has the product names as keys; looking up one name prints that product's price.
ASSESSMENT ANCHOR: build_and_update_dictionary facts=['f1', 'f2']
ASSESSMENT ANCHOR: look_up_value_by_key facts=['f2']
ASSESSMENT ANCHOR: predict_missing_key_error facts=['f3']

## SOURCE FACTS — C (python.tuples)   objective: Create a tuple to group a fixed set of values together, and unpack it into separate variables.
C.f1: A tuple consists of a number of values separated by commas; a tuple's items are shown enclosed in parentheses on output, and a tuple may be written with or without surrounding parentheses as input, e.g. t = 12345, 54321, 'hello!'.   [sources: python_docs_tutorial_datastructures#tuples-and-sequences]
C.f2: Tuples are immutable: once created, an item inside a tuple cannot be reassigned (t[0] = 88888 raises a TypeError).   [sources: python_docs_tutorial_datastructures#tuples-and-sequences]
C.f3: A tuple can be unpacked into several variables at once, e.g. x, y, z = t, provided there are as many variables as there are elements in the tuple.   [sources: python_docs_tutorial_datastructures#tuples-and-sequences]
C.m1 (misconception): Enclosing a single value in parentheses does not make it a tuple; a one-item tuple requires a trailing comma, e.g. singleton = 'hello',.   [sources: python_docs_tutorial_datastructures#tuples-and-sequences]
note: TOC conflict: this concept's practice_objective returns a tuple from a function, but functions aren't taught until python.defining_calling_functions, much later in this region -- this entry teaches tuple creation, immutability and unpacking without using any function.
PRACTICE ANCHOR (live_code): Create a tuple holding a smallest and a largest delivery time, then unpack it into two variables and print them.  SUCCESS: The tuple has two values; unpacking gives each value its own name, and printing both shows the correct numbers.
ASSESSMENT ANCHOR: create_a_tuple facts=['f1']
ASSESSMENT ANCHOR: recognize_tuple_immutability facts=['f2']
ASSESSMENT ANCHOR: unpack_tuple_into_variables facts=['f3']
ASSESSMENT ANCHOR: recognize_single_item_tuple_needs_comma facts=['m1']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Basic error handling (try/except); Basic file I/O (reading/writing text and CSV files); Comparing correlation strength across multiple variable pairs; Control flow: if/elif/else; Core data structure: dictionaries; Core data structure: sets; Core data structure: tuples; Correlation between two variables; Correlation-vs-causation caveat in business interpretation; Default and keyword arguments; Defining calling functions; Distribution shape (skewness, symmetry, outliers); For loops; Identifying and reasoning about outliers; Idiomatic style conventions for readable Python; Iterating over data structures; List and dict comprehensions; Loop control statements (break, continue); Measures of central tendency (mean, median, mode); Measures of spread (range, variance, standard deviation); Modules and imports; Parameters arguments; Reading a frequency distribution/histogram in statistical terms; Return values; String basics and f-string formatting; Variable scope (local vs global); While loops

## LESSON, in learner order

### s01 · explainer · Ordered, mutable sequences  [reward 5]
Lists — A list stores an ordered sequence of values you can index, slice and modify.
(intro) Keeping five separate variables for five delivery times gets unwieldy fast. A list stores an ordered sequence of values in a single name: delivery_times = [32, 45, 21, 60, 18]. Items are indexed from 0 at the left and from -1 at the right, so delivery_times[0] is 32 and delivery_times[-1] is 18. ⟦A.f1 A.f2 A:tb1 A:tb2⟧
(mechanism) A slice extracts a sub-list: delivery_times[1:3] returns [45, 21]. The start index is included; the end index is excluded. delivery_times[-3:] returns the last three items. Lists are mutable: delivery_times[3] = 64 replaces the item at index 3 in place. ⟦A.f3 A.f5 A:tb3⟧
[DIAGRAM: delivery_times — positive and negative indexes] nodes=['32 {index 0; index -5}', '45 {index 1; index -4}', '21 {index 2; index -3}', '60 {index 3; index -2}', '18 {index 4; index -1}', 'slice [1:3] starts here (included)', 'slice [1:3] ends here (excluded)'] edges=[('slice_start', 'i1', None), ('slice_end', 'i3', None)] alt: Array of five delivery times with positive indexes 0–4 above and negative indexes -5 to -1 below; a bracket marks slice [1:3] from index 1 (included) to index 3 (excluded), yielding [45, 21].

### s02 · video · Lists in action
Watch — See list creation, indexing and slicing demonstrated.
[VIDEO Indexing and slicing a list, and changing it in place] bridge-before: Watch the slice end index: the clip says it is not included, so 0 to 5 stops at 4. Caveat: the second clip says a list 'is no longer a variable'; in fact a list is a value stored in a variable. | bridge-after: Neither clip shows append(); the text covers adding to the end. The first clip stops at reading values, and the second shows replacing one.
  - ajrtAuDg3yw 0-177s facts=['f2', 'f5'] label: Index into a list with positive and negative positions, and see why a slice's end index is excluded | summary: Takes a list holding the numbers 0 to 9 and reads single items by position, from the front (index 0 is the first value) and from the back (-1 is the last value, -10 the first). Then extracts a range by writing a start index and an end index separated by a colon, stressing that the end index is not included: 0 to 5 returns 0 through 4, ending at 6 is needed to get 5, and 3 to 8 returns 3 through 7. A step value is mentioned but not used in this range.
  - SfX8IIxoJwQ 19-208s facts=['f1', 'f3'] label: Building a list with square brackets, indexing elements by position, and replacing an element in place | summary: Introduces a list as a way to store several items under one name, using a food example: the items go inside square brackets, each item is an element, and elements are read by index starting at 0. Asking for an index past the end fails with an out-of-range error until a fifth element exists. It ends by replacing the element at index 0 and showing that reading index 0 now gives the new value. Only positions counted from the front are shown, with no negative indexes or slicing.

### s03 · explainer · Adding items with append()  [reward 5]
Lists — append() grows a list by one item at the end.
(mechanism) To add a new item to the end of a list, call the append() method: delivery_times.append(27) adds 27 as the last element. ⟦A.f4 A:tb5⟧

### s04 · check · Modify and extend a list  [reward 10]
Quick check — Can you predict what a list looks like after an assignment and an append?
QUESTION [choice, intro, grading=client] After running:

```python
delivery_times = [32, 45, 21]
delivery_times[1] = 50
delivery_times.append(18)
```

What is the value of `delivery_times`?
  ✔ opt_a: `[32, 50, 21, 18]`
      why: Correct. `delivery_times[1] = 50` replaces the item at index 1 (which was `45`) with `50`, and `.append(18)` adds `18` at the end.
  ✘ opt_b: `[32, 45, 21, 18]`
      why: The assignment `delivery_times[1] = 50` replaces the item at index 1. Index 1 holds `45`, so after the assignment it becomes `50`, not `45`.
  ✘ opt_c: `[50, 45, 21, 18]`
      why: Index 1 is the second item (`45`), not the first (`32`). `delivery_times[1] = 50` replaces `45` with `50`, leaving `32` unchanged.
  ✘ opt_d: `[32, 50, 21]`
      why: `.append(18)` adds `18` to the end of the list. The list should have four items after both operations.
  feedback✔: Right — `delivery_times[1] = 50` replaces the item at index 1 (was `45`, now `50`), and `.append(18)` adds `18` at the end: `[32, 50, 21, 18]`.  feedback✘: Index 1 is the second item. `delivery_times[1] = 50` replaces `45` with `50`. Then `.append(18)` adds `18` at the end.  hints: ['List indexes start at 0. What item is at index 1 in `[32, 45, 21]`?', '`.append(value)` always adds to the end. How many items does the list have after both operations?']  remediation→r01
  MEASURES: A:modify_and_extend_a_list(f3,f4)   anchors=['assessment:modify_and_extend_a_list']
  taught-before-tested: A.f3←s01; A.f4←s03

### s05 · hands_on · Build and work with a list of delivery times  [reward 15]
Practice — Create a list, index into it, slice it and append a new item.
QUESTION [code_exercise, core, grading=client] QuickDeliver stores delivery times in a list. `delivery_times` is assigned below from scalar time variables.

Add lines that:
1. Assign `first` — the item at index `0`
2. Assign `last` — the item at index `-1`
3. Assign `sliced` — items from index `1` up to (but not including) index `3`
4. Reassign `delivery_times` to `delivery_times + [new_time]` (adds `new_time` to the end)

Then print `first`, `last`, `sliced`, and `delivery_times` each on its own line.

Expected output:
```
32
18
[45, 21]
[32, 45, 21, 60, 18, 27]
```
  runtime={'kind': 'python', 'version': '0.29.5'} constraints.allowed=['name = value assignment', 'using assigned names in an expression, as in the width * height example', 'int, float, str and bool literals', 'single- or double-quoted strings', 'True / False', 'print()', 'type()', '+ - * / // % **', 'parentheses for grouping', '< <= > >= == !=', 'and', 'or', 'not', 'int()', 'float()', 'str()', '[...] list literal', 'list[i] and list[-1] indexing', 'list[a:b] slicing', 'list[i] = value', 'list.append()', 'len()'] blocked=55 items
  file solution.py [editable]:
t0 = 32
t1 = 45
t2 = 21
t3 = 60
t4 = 18
new_time = 27
delivery_times = [t0, t1, t2, t3, t4]
# Assign first, last, sliced; extend delivery_times with new_time; then print all four

  SOLUTION solution.py:
t0 = 32
t1 = 45
t2 = 21
t3 = 60
t4 = 18
new_time = 27
delivery_times = [t0, t1, t2, t3, t4]
first = delivery_times[0]
last = delivery_times[-1]
sliced = delivery_times[1:3]
delivery_times = delivery_times + [new_time]
print(first)
print(last)
print(sliced)
print(delivery_times)

  test t1_stdout (stdout_equals, visible=True): {"expected":"32\n18\n[45, 21]\n[32, 45, 21, 60, 18, 27]"} | on-fail: Output does not match. Print `first`, `last`, `sliced`, `delivery_times` each on its own line in that order.
  test t2_sliced (value_equals, visible=True): {"expr":"sliced","expected":[45,21]} | on-fail: `sliced` should be `[45, 21]`. Use `delivery_times[1:3]` — the end index is excluded.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"466f7d8e8be6a968e94e9601007ba9dc14c361023a550767395521a199406703","tests_passed":2}
  feedback✔: All correct — `delivery_times[0]` gives `first`, `delivery_times[-1]` gives `last`, `delivery_times[1:3]` gives `sliced`, and `delivery_times + [new_time]` extends the list.  feedback✘: Use `delivery_times[0]` for the first item, `delivery_times[-1]` for the last, `delivery_times[1:3]` for the slice, and `delivery_times = delivery_times + [new_time]` to extend.  hints: ['Index `0` gives the first item; index `-1` gives the last. Slicing `[1:3]` gives items at positions 1 and 2.', 'To add `new_time` to the end: `delivery_times = delivery_times + [new_time]`. This creates a new list with `new_time` appended.']  remediation→r01
  MEASURES: A:create_a_list(f1); A:index_and_slice_a_list(f2,f5); A:modify_and_extend_a_list(f3,f4)   anchors=['practice', 'assessment:create_a_list', 'assessment:index_and_slice_a_list', 'assessment:modify_and_extend_a_list']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f5←s01; A.f3←s01; A.f4←s03

### s06 · explainer · Key-to-value lookup  [reward 5]
Dictionaries — A dictionary maps unique keys to values — look up a city by order ID, not by position.
(intro) Sometimes you need to look up a value by a meaningful key rather than by position. A dictionary is a collection of key: value pairs written inside braces, where keys must be unique: order_city = {1042: 'Lagos', 1043: 'Abuja', 1044: 'Kano'}. Retrieve a value by subscripting with its key: order_city[1042] returns 'Lagos'. ⟦B.f1 B.f2 B:tb1 B:tb2⟧
(mechanism) Store or update a value by assigning to a key: order_city[1044] = 'Kano' adds a new entry; assigning to an existing key replaces its value. The get() method returns None (or a specified default) instead of raising an error when a key is absent: order_city.get(9999) returns None rather than crashing. ⟦B.f2 B.f4 B:tb2 B:tb4⟧
(misconception) Subscripting a key that is not in the dictionary raises a KeyError: order_city[9999] fails if no order 9999 was ever added. Use get() when you are not certain the key exists. ⟦B.f3 B:tb3⟧
[DIAGRAM: order_city — key-to-value lookup] nodes=['1042', '1043', '1044', '9999 (missing)', "'Lagos'", "'Abuja'", "'Kano'", 'KeyError'] edges=[('k1042', 'v_lagos', 'lookup'), ('k1043', 'v_abuja', 'lookup'), ('k1044', 'v_kano', 'lookup'), ('k9999', 'v_error', 'KeyError')] alt: Mapping diagram: keys 1042, 1043, 1044 each point to their city values; key 9999 points to a KeyError node showing what happens when a missing key is subscripted.

### s07 · video · Dictionaries in action
Watch — See dictionary creation, lookup and the KeyError demonstrated.
[VIDEO Building, reading and updating a dictionary] bridge-before: Watch what happens with a missing key: square brackets fail with an error, while get() returns a fallback. The clip's example keys are text like 'name'; Devspace's example keys are order ids. | bridge-after: The text adds the in test for whether a key is present, which the clip does not show, and applies the same lookups to order ids and cities.
  - daefaLgNkw0 0-300s facts=['f1', 'f2', 'f3', 'f4'] label: Live demo: creating a dictionary, reading by key, KeyError, get() with a default, and adding or updating an entry | summary: Explains a dictionary as linked key and value pairs, where the key is a unique identifier used to find the data, like looking up a word in a physical dictionary. Builds one for a student with curly braces, a colon between each key and value and commas between pairs, then reads values by putting a key in square brackets. Asking for a key that is not there (phone) fails with a key error, while get() returns None, or a default such as 'Not Found' when one is passed. Finishes by assigning to a new key to add an entry and assigning to an existing key to update it.

### s08 · explainer · Testing key membership with in  [reward 5]
Dictionaries — Use in to check whether a key exists before accessing it.
(mechanism) The in keyword checks whether a key is present in a dictionary: 1042 in order_city is True. ⟦B.f5 B:tb5⟧

### s09 · check · Predict what happens with a missing key  [reward 10]
Quick check — What does Python do when you subscript a key that is not in the dictionary?
QUESTION [choice, core, grading=client] After running:

```python
order_city = {1042: 'Lagos', 1043: 'Abuja'}
print(order_city[1099])
```

What happens?
  ✔ opt_a: Raises a `KeyError` — key `1099` is not in the dictionary
      why: Correct. Subscripting a dictionary with a key that does not exist raises `KeyError`. Use `.get()` if you want `None` instead of an error.
  ✘ opt_b: Prints `None` — Python returns `None` for missing keys
      why: Subscripting with `[]` raises `KeyError` for a missing key. To get `None` for a missing key, use `order_city.get(1099)` instead.
  ✘ opt_c: Prints an empty string — Python returns `''` for missing keys
      why: Python does not return an empty string for missing keys. Subscripting with `[]` raises `KeyError`; use `.get()` to get a default value.
  ✘ opt_d: Raises a `ValueError` — the key type does not match
      why: The error is `KeyError`, not `ValueError`. Python raises `KeyError` when the key is not present, regardless of the key's type.
  feedback✔: Right — `order_city[1099]` raises `KeyError` because `1099` is not a key in the dictionary. Use `.get(1099)` to get `None` instead of an error.  feedback✘: Subscripting a dictionary with a missing key raises `KeyError`. To avoid the error, use `.get(key)` which returns `None` (or a default) when the key is absent.  hints: ['What does Python do when you use `d[key]` and `key` is not in `d`?', 'Which method returns `None` instead of raising an error for a missing key?']  remediation→r02
  MEASURES: B:predict_missing_key_error(f3)   anchors=['assessment:predict_missing_key_error']
  taught-before-tested: B.f3←s06

### s10 · hands_on · Build and query an order-city dictionary  [reward 15]
Practice — Create a dictionary, add entries, look up values and use get() for safe access.
QUESTION [code_exercise, core, grading=client] QuickDeliver maps order IDs to cities. `order_city` is assigned below using scalar city variables.

Add lines that:
1. Add a new entry: key `1045`, value `new_city`
2. Assign `city` — the value for key `1042`
3. Print `city` and `order_city[1045]` each on its own line

Expected output:
```
Lagos
Ibadan
```
  runtime={'kind': 'python', 'version': '0.29.5'} constraints.allowed=['name = value assignment', 'using assigned names in an expression, as in the width * height example', 'int, float, str and bool literals', 'single- or double-quoted strings', 'True / False', 'print()', 'type()', '+ - * / // % **', 'parentheses for grouping', '< <= > >= == !=', 'and', 'or', 'not', 'int()', 'float()', 'str()', '[...] list literal', 'list[i] and list[-1] indexing', 'list[a:b] slicing', 'list[i] = value', 'list.append()', 'len()', '{key: value} dictionary literal', 'd[key] lookup and assignment', 'd.get()', 'key in d'] blocked=51 items
  file solution.py [editable]:
city_a = 'Lagos'
city_b = 'Abuja'
city_c = 'Kano'
new_city = 'Ibadan'
order_city = {1042: city_a, 1043: city_b, 1044: city_c}
# Add key 1045 -> new_city, look up key 1042, then print city and order_city[1045]

  SOLUTION solution.py:
city_a = 'Lagos'
city_b = 'Abuja'
city_c = 'Kano'
new_city = 'Ibadan'
order_city = {1042: city_a, 1043: city_b, 1044: city_c}
order_city[1045] = new_city
city = order_city[1042]
print(city)
print(order_city[1045])

  test t1_stdout (stdout_equals, visible=True): {"expected":"Lagos\nIbadan"} | on-fail: Output does not match. Print `city` then `order_city[1045]`, each on its own line.
  test t2_city (value_equals, visible=True): {"expr":"city","expected":"Lagos"} | on-fail: `city` should be `'Lagos'`. Use `city = order_city[1042]` to look up the value for key `1042`.
  test t3_new_entry (value_equals, visible=True): {"expr":"order_city[1045]","expected":"Ibadan"} | on-fail: `order_city[1045]` should be `'Ibadan'`. Use `order_city[1045] = new_city` to add the entry.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"5b84c6838b63d663d4c2d8dac33b9816e340caf5d1313386040a7e36d5e00080","tests_passed":3}
  feedback✔: All correct — `order_city[1045] = new_city` adds the entry, `order_city[1042]` returns `city_a` (`'Lagos'`), and `order_city[1045]` returns `new_city` (`'Ibadan'`).  feedback✘: Use `d[key] = value` to add/update, and `d[key]` to look up. Make sure you assign `city = order_city[1042]` and print both `city` and `order_city[1045]`.  hints: ['To add a new key-value pair: `order_city[1045] = new_city`. To look up: `city = order_city[1042]`.', 'Print each result on its own line: `print(city)` then `print(order_city[1045])`.']  remediation→r02
  MEASURES: B:build_and_update_dictionary(f1,f2,f3); B:look_up_value_by_key(f2)   anchors=['practice', 'assessment:build_and_update_dictionary', 'assessment:look_up_value_by_key']
  taught-before-tested: B.f1←s06; B.f2←s06; B.f3←s06; B.f2←s06

### s11 · explainer · Immutable sequences and unpacking  [reward 5]
Tuples — A tuple groups a fixed set of values; unpacking hands each piece back to its own name.
(intro) A tuple groups a small, fixed set of values together. It is written as comma-separated values, with or without surrounding parentheses: order = 1042, 'Lagos', 32 or order = (1042, 'Lagos', 32). Python shows tuples enclosed in parentheses on output. ⟦C.f1 C:tb1⟧
(misconception) Tuples are immutable: once created, an item cannot be reassigned. order[0] = 1099 raises a TypeError. Also, enclosing a single value in parentheses does not make it a tuple — singleton = ('Lagos') is still just the string 'Lagos'. A one-item tuple needs a trailing comma: singleton = 'Lagos', ⟦C.f3⟧ ⟦C.f2 C.m1 C.f3 C:tb2 C:tb4 C:tb3⟧
[BEFORE_AFTER] Unpacking hands each element of the tuple back to its own name — order_id, city and minutes are now separate variables. ⟦C.f3⟧
  before:
[CODE python]
order = (1042, 'Lagos', 32)
  annotations: ['Three values packed into one tuple']
  after:
[CODE python]
order_id, city, minutes = order
  annotations: ["Unpacking: order_id=1042, city='Lagos', minutes=32"]

### s12 · check · Recognise when a one-item tuple needs a trailing comma  [reward 10]
Quick check — Which expression actually creates a tuple with one element?
QUESTION [choice, core, grading=client] Which of the following creates a **tuple** containing the single value `'Lagos'`?
  ✔ opt_a: `singleton = 'Lagos',`
      why: Correct. A trailing comma after the value creates a one-item tuple: `'Lagos',` is a tuple. The parentheses are optional.
  ✘ opt_b: `singleton = ('Lagos')`
      why: `('Lagos')` is just `'Lagos'` in parentheses — the parentheses are grouping, not a tuple. Without a trailing comma, Python sees a plain string.
  ✘ opt_c: `singleton = ['Lagos']`
      why: `['Lagos']` creates a **list** with one item, not a tuple. Lists use square brackets; tuples use commas (with optional parentheses).
  ✘ opt_d: `singleton = {'Lagos'}`
      why: `{'Lagos'}` creates a **set** with one item, not a tuple. Sets use curly braces; tuples use commas.
  feedback✔: Right — a one-item tuple requires a trailing comma: `'Lagos',` or `('Lagos',)`. Without the comma, `('Lagos')` is just a string in parentheses.  feedback✘: A one-item tuple needs a trailing comma: `singleton = 'Lagos',`. Without the comma, parentheses alone do not create a tuple.  hints: ['What makes a tuple a tuple — the parentheses, or the commas?', "Try `type(('Lagos'))` versus `type(('Lagos',))` — what does each return?"]  remediation→r03
  MEASURES: C:recognize_single_item_tuple_needs_comma(m1)   anchors=['assessment:recognize_single_item_tuple_needs_comma']
  taught-before-tested: C.m1←s11

### s13 · hands_on · Create, inspect and unpack a tuple  [reward 15]
Practice — Build a tuple for an order record, confirm it is immutable, and unpack it into named variables.
QUESTION [code_exercise, core, grading=client] QuickDeliver records the minimum and maximum delivery times as a fixed pair.

`min_val`, `max_val`, and `order_stats` are already assigned below.

Add lines that:
1. Unpack `order_stats` into two variables: `min_time` and `max_time`
2. Print `min_time` and `max_time` each on its own line

Expected output:
```
32
45
```
  runtime={'kind': 'python', 'version': '0.29.5'} constraints.allowed=['name = value assignment', 'using assigned names in an expression, as in the width * height example', 'int, float, str and bool literals', 'single- or double-quoted strings', 'True / False', 'print()', 'type()', '+ - * / // % **', 'parentheses for grouping', '< <= > >= == !=', 'and', 'or', 'not', 'int()', 'float()', 'str()', '[...] list literal', 'list[i] and list[-1] indexing', 'list[a:b] slicing', 'list[i] = value', 'list.append()', 'len()', '{key: value} dictionary literal', 'd[key] lookup and assignment', 'd.get()', 'key in d', 'tuple literal with commas or parentheses', 'unpacking a, b = t', 'one-item tuple with trailing comma'] blocked=49 items
  file solution.py [editable]:
min_val = 32
max_val = 45
order_stats = (min_val, max_val)
# Unpack order_stats into min_time and max_time, then print each

  SOLUTION solution.py:
min_val = 32
max_val = 45
order_stats = (min_val, max_val)
min_time, max_time = order_stats
print(min_time)
print(max_time)

  test t1_stdout (stdout_equals, visible=True): {"expected":"32\n45"} | on-fail: Output does not match. Print `min_time` then `max_time`, each on its own line.
  test t2_min_time (value_equals, visible=True): {"expr":"min_time","expected":32} | on-fail: `min_time` should be `32`. Unpack with `min_time, max_time = order_stats`.
  test t3_max_time (value_equals, visible=True): {"expr":"max_time","expected":45} | on-fail: `max_time` should be `45`. Unpack with `min_time, max_time = order_stats`.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"9f9743b612514d4492f9b79a544b8f40f0ec3359e4512bf00c403bcf623e61fd","tests_passed":3}
  feedback✔: Correct — `min_time, max_time = order_stats` unpacks the tuple into two names, giving `min_time=32` and `max_time=45`.  feedback✘: Use tuple unpacking: `min_time, max_time = order_stats`. The number of variables on the left must match the number of items in the tuple.  hints: ['Tuple unpacking looks like: `a, b = some_tuple`. How many items are in `order_stats`?', 'After unpacking, `min_time` holds the first item and `max_time` holds the second.']  remediation→r03
  MEASURES: C:create_a_tuple(f1,m1); C:recognize_tuple_immutability(f2); C:unpack_tuple_into_variables(f3)   anchors=['practice', 'assessment:create_a_tuple', 'assessment:recognize_tuple_immutability', 'assessment:unpack_tuple_into_variables']
  taught-before-tested: C.f1←s11; C.m1←s11; C.f2←s11; C.f3←s11

### s14 · recap · What you learned  [reward 5]
Recap — Key ideas from this tile.
(takeaway) A list is an ordered, mutable sequence indexed from 0; slices use start-included, end-excluded bounds; index assignment replaces an item in place and append() adds one at the end. A dictionary maps unique keys to values; subscripting a missing key raises a KeyError — use get() to avoid it. A tuple groups a fixed set of values that cannot be reassigned; unpacking distributes each element to its own name. ⟦A.f1 A.f3 A.f4 B.f1 B.f2 C.f2 C.f3 A:tb7 B:tb6 C:tb5⟧
[UP NEXT] Up next: Sets and Strings: In the next tile you will use sets to collect unique delivery cities with no duplicates, and f-strings to build readable messages that embed variable values.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Modifying a list and adding items — A before/after showing index assignment and append() on the same list.
(mechanism) Lists are mutable: you can replace any item by assigning to its index. delivery_times[3] = 64 changes the value at index 3 in place. append() adds a new item to the end: delivery_times.append(27) grows the list by one. ⟦A.f3 A.f4 A:tb3 A:tb5⟧
[BEFORE_AFTER] Index assignment replaces an item in place; append() adds a new item at the end.
  before:
[CODE python]
delivery_times = [32, 45, 21, 60, 18]
  annotations: ['Original list']
  after:
[CODE python]
delivery_times[3] = 64
delivery_times.append(27)
  annotations: ['60 replaced by 64 at index 3', '27 added at the end']
### r02 · KeyError vs get() for missing keys — A side-by-side contrast between subscripting a missing key and using get().
(misconception) Subscripting a key that is not in the dictionary raises a KeyError. order_city[9999] fails if 9999 was never added. Use get() to avoid the error: order_city.get(9999) returns None instead of crashing. ⟦B.f3 B:tb3 B:tb4⟧
[SIDE_BY_SIDE] Use get() when you are not certain the key exists; it returns None (or a default) instead of raising an error. left_label: Subscript — raises KeyError | right_label: get() — returns None
  left:
[CODE python]
order_city = {1042: 'Lagos', 1043: 'Abuja'}
order_city[9999]
  annotations: ['Dictionary with two entries', 'KeyError — 9999 is not a key']
  right:
[CODE python]
order_city = {1042: 'Lagos', 1043: 'Abuja'}
order_city.get(9999)
  annotations: ['Same dictionary', 'Returns None — no error raised']
### r03 · One-item tuples need a trailing comma — A side-by-side contrast showing that parentheses alone do not create a tuple.
(misconception) Enclosing a single value in parentheses does not make it a tuple — singleton = ('Lagos') is still just the string 'Lagos'. A one-item tuple requires a trailing comma: singleton = 'Lagos', or equivalently singleton = ('Lagos',). ⟦C.m1 C:tb4⟧
[SIDE_BY_SIDE] The trailing comma, not the parentheses, is what makes a one-item tuple. left_label: ('Lagos') — str, not tuple | right_label: ('Lagos',) — one-item tuple
  left:
[CODE python]
singleton = ('Lagos')
type(singleton)
  annotations: ['Just parentheses — still a str', "<class 'str'>"]
  right:
[CODE python]
singleton = ('Lagos',)
type(singleton)
  annotations: ['Trailing comma — this is a tuple', "<class 'tuple'>"]

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: quote mixing to embed a quote
· constraints.blocked_syntax: f-strings f"...{expr}..."
· constraints.blocked_syntax: format specifier such as {value:.2f}
· constraints.blocked_syntax: colon and indented block
· constraints.blocked_syntax: for item in sequence:
· constraints.blocked_syntax: [expr for x in seq if cond]
· constraints.blocked_syntax: for k, v in d.items():
· constraints.blocked_syntax: positional arguments in a call
· constraints.blocked_syntax: def f(a, b=default):
· constraints.blocked_syntax: keyword arguments f(name=value)
· constraints.blocked_syntax: from module import name
· constraints.blocked_syntax: with open(...) as f:
· constraints.blocked_syntax: += and other augmented assignment
· expected.value: 39
18
[45, 21]
[39, 45, 21, 60, 18, 27]
· expected.value: 32
18
[52, 21]
[32, 52, 21, 60, 18, 27]
· constraints.blocked_syntax: quote mixing to embed a quote
· constraints.blocked_syntax: f-strings f"...{expr}..."
· constraints.blocked_syntax: format specifier such as {value:.2f}
· constraints.blocked_syntax: colon and indented block
· constraints.blocked_syntax: for item in sequence:
· constraints.blocked_syntax: [expr for x in seq if cond]
· constraints.blocked_syntax: for k, v in d.items():
· constraints.blocked_syntax: positional arguments in a call
· constraints.blocked_syntax: def f(a, b=default):
· constraints.blocked_syntax: keyword arguments f(name=value)
· constraints.blocked_syntax: from module import name
· constraints.blocked_syntax: with open(...) as f:
· constraints.blocked_syntax: += and other augmented assignment
· constraints.blocked_syntax: def / return (functions come later)
· constraints.blocked_syntax: quote mixing to embed a quote
· constraints.blocked_syntax: f-strings f"...{expr}..."
· constraints.blocked_syntax: format specifier such as {value:.2f}
· constraints.blocked_syntax: colon and indented block
· constraints.blocked_syntax: for item in sequence:
· constraints.blocked_syntax: [expr for x in seq if cond]
· constraints.blocked_syntax: for k, v in d.items():
· constraints.blocked_syntax: positional arguments in a call
· constraints.blocked_syntax: def f(a, b=default):
· constraints.blocked_syntax: keyword arguments f(name=value)
· constraints.blocked_syntax: from module import name
· constraints.blocked_syntax: with open(...) as f:
· constraints.blocked_syntax: += and other augmented assignment

=========

# EVALUATOR PACKET — Comparison and Logical Operators (tile_python_operators_conversion)
Tile summary: Learn Python's arithmetic, comparison and logical operators, understand short-circuit evaluation and operator priority, and convert values between int, float and str.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.arithmetic_operators — Arithmetic operators
B = python.comparison_operators — Comparison operators
C = python.logical_operators — Logical operators
D = python.type_conversion — Type conversion/casting

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=10
  warn: tile_python_operators_conversion.s03: remediation tile_python_operators_conversion.r01 re-teaches ['python.arithmetic_operators#f4', 'python.arithmetic_operators#f5'] but the check measures ['python.arithmetic_operators#f1', 'python.arithmetic_operators#f2', 'python.arithmetic_operators#f3'] — a learner who fails it is sent to an unrelated fact
  warn: remediation step tile_python_operators_conversion.r04 is never referenced
  warn: tile_python_operators_conversion.s01: 155 words vs budget 101
  warn: tile_python_operators_conversion.s04: text contains the name of blocked future concept python.comparison_operators ('comparison operators') — check it is not needed to understand
  warn: tile_python_operators_conversion.s08: text contains the name of blocked future concept python.logical_operators ('logical operators') — check it is not needed to understand
  warn: tile_python_operators_conversion.s09: text contains the name of blocked future concept python.comparison_operators ('comparison operators') — check it is not needed to understand
  warn: tile_python_operators_conversion.s17: text contains the name of blocked future concept python.comparison_operators ('comparison operators') — check it is not needed to understand
  warn: tile_python_operators_conversion.r02: text contains the name of blocked future concept python.comparison_operators ('comparison operators') — check it is not needed to understand
  warn: tile_python_operators_conversion.r03: text contains the name of blocked future concept python.comparison_operators ('comparison operators') — check it is not needed to understand
  warn: tile_python_operators_conversion.r03: text contains the name of blocked future concept python.logical_operators ('logical operators') — check it is not needed to understand

## SOURCE FACTS — A (python.arithmetic_operators)   objective: Apply Python's arithmetic operators (+, -, *, /, //, %, **) to combine numeric values into a derived result.
A.f1: The operators +, -, * and / perform addition, subtraction, multiplication and division; division (/) always returns a float.   [sources: python_docs_tutorial_introduction#numbers]
A.f2: The // operator performs floor division, discarding the fractional part, and the % operator returns the remainder of the division.   [sources: python_docs_tutorial_introduction#numbers]
A.f3: The ** operator calculates a power, e.g. 5 ** 2 is 5 squared.   [sources: python_docs_tutorial_introduction#numbers]
A.f4: Parentheses can be used to group an expression and control how it is evaluated.   [sources: python_docs_tutorial_introduction#numbers]
A.f5: Operators with mixed int/float operands convert the integer operand to floating point, e.g. 4 * 3.75 - 1 evaluates to 14.0.   [sources: python_docs_tutorial_introduction#numbers]
note: Keep this tight -- reference tier, one line per operator group.
PRACTICE ANCHOR (live_code): Compute derived values from numeric inputs using the arithmetic operators, for example a total, an average-style quotient and a remainder.  SUCCESS: Each derived value prints the correct number, with / giving a float and // and % giving the quotient and remainder.
ASSESSMENT ANCHOR: choose_arithmetic_operator facts=['f1']
ASSESSMENT ANCHOR: use_floor_division_and_remainder facts=['f2']
ASSESSMENT ANCHOR: use_power_operator facts=['f3']
ASSESSMENT ANCHOR: predict_grouped_and_mixed_type_result facts=['f4', 'f5']

## SOURCE FACTS — B (python.comparison_operators)   objective: Write comparisons between Python values using <, <=, >, >=, == and != so each evaluates to the boolean result a task requires.
B.f1: The standard comparison operators are <, <=, >, >=, == and !=.   [sources: python_docs_tutorial_introduction#first-steps-towards-programming]
B.f2: A comparison evaluates to a boolean value: True or False, e.g. 3 < 5 is True.   [sources: python_official_docs#reference/expressions.html#comparisons]
note: Skip chained comparisons (optional f3) unless there's room -- it's enrichment, not required.
PRACTICE ANCHOR (live_code): Write simple threshold checks that compare a number to a limit and print the True or False result.  SUCCESS: Each check prints True or False correctly for values below, at and above the threshold.
ASSESSMENT ANCHOR: write_comparison_expression facts=['f1', 'f2']
ASSESSMENT ANCHOR: predict_boolean_result_of_comparison facts=['f2']

## SOURCE FACTS — C (python.logical_operators)   objective: Combine comparisons and boolean conditions using and, or, and not to express compound rules.
C.f1: The Boolean operations, in ascending priority, are or, and, and not.   [sources: python_docs_stdtypes#boolean-operations-and-or-not]
C.f2: x or y evaluates to x if x is true, otherwise to y, and is a short-circuit operator that only evaluates y if x is false.   [sources: python_docs_stdtypes#boolean-operations-and-or-not]
C.f3: x and y evaluates to x if x is false, otherwise to y, and is a short-circuit operator that only evaluates y if x is true.   [sources: python_docs_stdtypes#boolean-operations-and-or-not]
C.f4: not x evaluates to True if x is false, else False; not has a lower priority than the comparison operators, so not a == b is interpreted as not (a == b).   [sources: python_docs_stdtypes#boolean-operations-and-or-not]
note: Keep is_late/is_far as the running example throughout -- don't introduce a third condition.
note: No video was approved for this concept (every candidate clip was rejected), so the text carries all four facts alone.
PRACTICE ANCHOR (live_code): Write a rule that combines comparisons with and, or and not and print whether a sample delivery meets it, using is_late and is_far as the condition variables.  SUCCESS: The compound expression prints the expected True or False for sample values of is_late and is_far, including a case where the priority of and over or matters.
ASSESSMENT ANCHOR: predict_operator_priority facts=['f1', 'f4']
ASSESSMENT ANCHOR: predict_short_circuit_result facts=['f2', 'f3']
ASSESSMENT ANCHOR: write_compound_boolean_expression facts=['f1', 'f2', 'f3', 'f4']

## SOURCE FACTS — D (python.type_conversion)   objective: Convert a value from one core type to another using int(), float(), or str(), and recognize when a conversion is invalid.
D.f1: The constructors int() and float() can be used to produce a number of a specific type from another value.   [sources: python_docs_stdtypes#numeric-types-int-float-complex]
D.f2: int(string) returns an integer object constructed from a string, e.g. int('123') returns 123.   [sources: python_docs_library_functions#int]
D.f3: float(string) returns a floating-point number constructed from a string, e.g. float('+1.23') returns 1.23.   [sources: python_docs_library_functions#float]
D.f4: Strings may also be created from other objects using the str constructor.   [sources: python_docs_stdtypes#text-sequence-type-str]
D.f5: float(string) requires the string to conform to a specific numeric format (an optional sign and digits, optionally with a decimal point or exponent, after surrounding whitespace is removed); not every string can be converted this way.   [sources: python_docs_library_functions#float]
D.f6: A string that isn't in the format the target type accepts (for int(), an integer string) raises a ValueError, e.g. int('3.5').   [sources: python_docs_library_functions#int, python_docs_tutorial_errors#handling-exceptions]
note: TOC conflict: the assessment_target mentions 'handling conversion errors', but try/except is taught later in python.error_handling. The assessment anchors cover recognizing when a conversion raises a ValueError, not handling it.
PRACTICE ANCHOR (live_code): Take a numeric string, convert it to a float and use it in a calculation.  SUCCESS: The string is converted with float() and the calculation prints a numeric result.
ASSESSMENT ANCHOR: convert_value_to_target_type facts=['f1', 'f2', 'f3', 'f4']
ASSESSMENT ANCHOR: recognize_invalid_conversion facts=['f5', 'f6']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Basic error handling (try/except); Basic file I/O (reading/writing text and CSV files); Comparison operators; Control flow: if/elif/else; Core data structure: dictionaries; Core data structure: lists; Core data structure: sets; Core data structure: tuples; Default and keyword arguments; Defining calling functions; Distribution shape (skewness, symmetry, outliers); For loops; Identifying and reasoning about outliers; Idiomatic style conventions for readable Python; Iterating over data structures; List and dict comprehensions; Logical operators; Loop control statements (break, continue); Measures of central tendency (mean, median, mode); Measures of spread (range, variance, standard deviation); Modules and imports; Parameters arguments; Reading a frequency distribution/histogram in statistical terms; Return values; String basics and f-string formatting; Type conversion/casting; Variable scope (local vs global); While loops

## LESSON, in learner order

### s01 · explainer · Seven operators for numeric work  [reward 5]
Arithmetic operators — Python gives you seven arithmetic operators — including two you may not have seen before.
(definition) Python provides seven arithmetic operators for numeric work. The familiar four — + (addition), - (subtraction), * (multiplication) and / (division) — work as expected, but / always returns a float even when both operands are whole numbers: 8 / 2 gives 4.0, not 4. The ** operator raises a number to a power: 5 ** 2 is 25. ⟦A.f1 A.f3 A:tb1⟧
(definition) The // operator performs floor division: it divides and discards the fractional part, so 17 // 5 is 3. The % operator returns the remainder of the division, so 17 % 5 is 2. Together they let you split a quantity into whole units and a leftover — for example, 17 minutes is 3 complete five-minute slots with 2 minutes remaining. ⟦A.f2 A:tb1⟧
(example) Parentheses group an expression and control the order of evaluation: (32 + 8) * 2 adds first, then multiplies, giving 80. When an expression mixes an int and a float, Python converts the integer to floating point before computing — so 4 * 3.75 - 1 evaluates to 14.0, not 14. ⟦A.f4 A.f5 A:tb2⟧
[SIDE_BY_SIDE] 17 // 5 is 3 and 17 % 5 is 2; parentheses control evaluation order; mixing int and float promotes the result to float. left_label: // and % | right_label: Grouping and mixed types
  left:
[CODE python]
17 // 5   # floor division
17 % 5    # remainder
  annotations: ['Result: 3 (fractional part discarded)', "Result: 2 (what's left over)"]
  right:
[CODE python]
(32 + 8) * 2    # parentheses group first
4 * 3.75 - 1    # int promoted to float
  annotations: ['Result: 80 — parentheses force addition before multiplication', 'Result: 14.0 — mixed int/float gives float']

### s02 · check · Predict the result of a grouped, mixed-type expression  [reward 10]
Quick check — Can you work out what Python evaluates when parentheses and a float are involved?
QUESTION [choice, intro, grading=client] What does Python evaluate `4 * 3.75 - 1` to?

*(Hint: mixed int/float operands convert the integer to float.)*
  ✔ opt_a: `14.0` — a float, because one operand is a float
      why: Correct. `4 * 3.75` is `15.0` (float), then `15.0 - 1` is `14.0`. When an int and a float are combined, the int is converted to float first.
  ✘ opt_b: `14` — an int, because the result is a whole number
      why: The result is a float, not an int. When any operand is a float, Python converts the int operand to float, so the result is `14.0`, not `14`.
  ✘ opt_c: `13.0` — subtraction happens before multiplication
      why: Multiplication and division have higher precedence than subtraction, so `4 * 3.75` is evaluated first, giving `15.0`, then `15.0 - 1 = 14.0`.
  ✘ opt_d: `15.0` — Python rounds up when mixing types
      why: Python does not round when mixing types. It converts the int to float and computes exactly: `4 * 3.75 = 15.0`, then `15.0 - 1 = 14.0`.
  feedback✔: Right — `4 * 3.75 - 1` evaluates to `14.0`. Multiplication runs first (higher precedence), and the int `4` is converted to float because `3.75` is a float.  feedback✘: Remember: `*` has higher precedence than `-`, so `4 * 3.75 = 15.0` first. Then `15.0 - 1 = 14.0`. Any int mixed with a float gives a float result.  hints: ['Which operator has higher precedence: `*` or `-`? Apply that one first.', 'When one operand is a float (like `3.75`), what type does Python use for the result?']  remediation→r01
  MEASURES: A:predict_grouped_and_mixed_type_result(f4,f5)   anchors=['assessment:predict_grouped_and_mixed_type_result']
  taught-before-tested: A.f4←s01; A.f5←s01

### s03 · hands_on · Use arithmetic operators on delivery data  [reward 15]
Practice — Apply +, -, *, /, //, % and ** to compute delivery metrics.
QUESTION [code_exercise, core, grading=client] QuickDeliver's analytics team needs five derived values from two base numbers.

`orders_per_driver` and `days_worked` are already assigned below.

Add five lines that compute and print:
1. `total` — `orders_per_driver` multiplied by `days_worked`
2. `avg` — `total` divided by `days_worked` (use `/`; the result must be a float)
3. `quotient` — `total` floor-divided by `3` (use `//`)
4. `remainder` — `total` modulo `3` (use `%`)
5. `squared` — `orders_per_driver` raised to the power `2` (use `**`)

Print each variable on its own line in the order above.

Expected output:
```
100
20.0
33
1
400
```
  runtime={'kind': 'python', 'version': '0.29.5'} constraints.allowed=['name = value assignment', 'using assigned names in an expression, as in the width * height example', 'int, float, str and bool literals', 'single- or double-quoted strings', 'True / False', 'print()', 'type()', '+ - * / // % **', 'parentheses for grouping'] blocked=68 items
  file solution.py [editable]:
orders_per_driver = 20
days_worked = 5
# Compute total, avg, quotient, remainder and print each

  SOLUTION solution.py:
orders_per_driver = 20
days_worked = 5
total = orders_per_driver * days_worked
avg = total / days_worked
quotient = total // 3
remainder = total % 3
squared = orders_per_driver ** 2
print(total)
print(avg)
print(quotient)
print(remainder)
print(squared)

  test t1_stdout (stdout_equals, visible=True): {"expected":"100\n20.0\n33\n1\n400"} | on-fail: Output does not match. Print `total`, `avg`, `quotient`, `remainder`, `squared` each on its own line, in that order.
  test t2_avg_float (value_equals, visible=True): {"expr":"avg","expected":20.0} | on-fail: `avg` should be `20.0` (a float). Use `/` for division, not `//`.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"809852bcff6abf9ff7171c37275790fad5c9760e302b230713ac1d28727570bd","tests_passed":2}
  feedback✔: All five values correct — `total=100`, `avg=20.0` (float from `/`), `quotient=33` and `remainder=1` from `//` and `%`, and `squared=400` from `**`.  feedback✘: Check each operator: `*` for total, `/` for avg (must give a float), `//` for floor quotient, `%` for remainder, `**` for power. Print them in order.  hints: ['For `avg`, use `/` (not `//`) — regular division always returns a float in Python 3.', 'For `quotient` and `remainder`, use `//` and `%` on `total` divided by `3`.', 'For `squared`, use `orders_per_driver ** 2` — `**` is the power operator.']  remediation→r01
  MEASURES: A:choose_arithmetic_operator(f1); A:use_floor_division_and_remainder(f2); A:use_power_operator(f3)   anchors=['practice', 'assessment:choose_arithmetic_operator', 'assessment:use_floor_division_and_remainder', 'assessment:use_power_operator']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s04 · explainer · Six operators that return True or False  [reward 5]
Comparison operators — Comparisons turn a question about data into a boolean value Python can branch on.
(definition) Comparing two values is how a question like 'is this delivery late?' becomes something Python can act on. The six comparison operators are < (less than), <= (less than or equal), > (greater than), >= (greater than or equal), == (equal) and != (not equal). Every comparison evaluates to exactly one of the two boolean values: True or False. ⟦B.f1 B.f2 B:tb1 B:tb2⟧
[SIDE_BY_SIDE] Each operator returns True or False; delivery_minutes > 60 is True for a 72-minute order and False for a 32-minute one. left_label: Greater-than family | right_label: Less-than family and !=
  left:
[CODE python]
delivery_minutes > 60
delivery_minutes >= 60
delivery_minutes == 60
  annotations: ['True if over 60 minutes', 'True if 60 or more', 'True only if exactly 60']
  right:
[CODE python]
delivery_minutes < 60
delivery_minutes <= 60
city != 'Lagos'
  annotations: ['True if under 60 minutes', 'True if 60 or fewer', 'True for any city other than Lagos']

### s05 · check · Choose the right comparison operator  [reward 10]
Quick check — Pick the operator that expresses the condition described.
QUESTION [choice, intro, grading=client] A QuickDeliver order has `delivery_minutes = 60` and the SLA threshold is `45` minutes.

Which expression correctly checks whether the delivery exceeded the SLA?
  ✔ opt_a: `delivery_minutes > 45`
      why: Correct. `delivery_minutes > 45` evaluates to `True` when `delivery_minutes` is `60`, meaning the delivery exceeded the SLA.
  ✘ opt_b: `delivery_minutes = 45`
      why: `=` is the assignment operator, not a comparison. To compare two values, use `>`, `<`, `==`, `!=`, `>=`, or `<=`.
  ✘ opt_c: `delivery_minutes => 45`
      why: Python does not have a `=>` operator. The greater-than-or-equal operator is `>=` (the `>` comes first).
  ✘ opt_d: `delivery_minutes <> 45`
      why: `<>` is not valid Python syntax. To check inequality, use `!=`.
  feedback✔: Right — `delivery_minutes > 45` is `True` when `delivery_minutes` is `60`. The six comparison operators are `<`, `<=`, `>`, `>=`, `==`, and `!=`.  feedback✘: Use one of the six comparison operators: `<`, `<=`, `>`, `>=`, `==`, `!=`. Remember that `=` is assignment, not comparison.  hints: ['To check if one value is greater than another, which operator do you use?', "Python's comparison operators are `<`, `<=`, `>`, `>=`, `==`, `!=`. Which one means 'greater than'?"]  remediation→r02
  MEASURES: B:write_comparison_expression(f1,f2)   anchors=['assessment:write_comparison_expression']
  taught-before-tested: B.f1←s04; B.f2←s04

### s06 · check · Predict the boolean result of a comparison  [reward 10]
Quick check — Given a value and an operator, what does the expression evaluate to?
QUESTION [choice, core, grading=client] After running:

```python
delivery_minutes = 45
sla = 45
print(delivery_minutes == sla)
print(delivery_minutes > sla)
```

What is printed?
  ✔ opt_a: `True` then `False`
      why: Correct. `45 == 45` is `True` (equal values), and `45 > 45` is `False` (not strictly greater).
  ✘ opt_b: `True` then `True`
      why: `45 > 45` is `False`, not `True`. The `>` operator requires the left side to be strictly greater than the right.
  ✘ opt_c: `False` then `True`
      why: `45 == 45` is `True`, not `False`. Two equal values satisfy `==`.
  ✘ opt_d: `False` then `False`
      why: `45 == 45` is `True` because both sides are equal. Only `45 > 45` is `False`.
  feedback✔: Correct — `45 == 45` is `True` (equal), and `45 > 45` is `False` (not strictly greater). Comparisons always return a boolean.  feedback✘: `==` checks equality (both sides equal → `True`), while `>` checks strict greater-than (`45 > 45` is `False` because they are equal, not greater).  hints: ['Does `==` return `True` when both sides are the same value?', 'Does `>` return `True` when both sides are equal, or only when the left is strictly larger?']
  MEASURES: B:predict_boolean_result_of_comparison(f2)   anchors=['assessment:predict_boolean_result_of_comparison']
  taught-before-tested: B.f2←s04

### s07 · hands_on · Write comparison expressions for delivery data  [reward 15]
Practice — Use the six comparison operators to filter and flag orders.
QUESTION [code_exercise, core, grading=client] QuickDeliver's SLA is 45 minutes. Three delivery times are assigned below: one below, one at, and one above the threshold.

Add three `print()` calls that each output a boolean:
1. Whether `dm_below` is **less than** `sla`
2. Whether `dm_at` is **equal to** `sla`
3. Whether `dm_above` is **greater than** `sla`

Expected output:
```
True
True
True
```
  runtime={'kind': 'python', 'version': '0.29.5'} constraints.allowed=['name = value assignment', 'using assigned names in an expression, as in the width * height example', 'int, float, str and bool literals', 'single- or double-quoted strings', 'True / False', 'print()', 'type()', '+ - * / // % **', 'parentheses for grouping', '< <= > >= == !='] blocked=67 items
  file solution.py [editable]:
dm_below = 32
dm_at = 45
dm_above = 60
sla = 45
# Print three boolean results: dm_below < sla, dm_at == sla, dm_above > sla

  SOLUTION solution.py:
dm_below = 32
dm_at = 45
dm_above = 60
sla = 45
print(dm_below < sla)
print(dm_at == sla)
print(dm_above > sla)

  test t1_stdout (stdout_equals, visible=True): {"expected":"True\nTrue\nTrue"} | on-fail: Output does not match. Print `dm_below < sla`, `dm_at == sla`, `dm_above > sla` each on its own line.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"a8099e4fdad10a9dc06ca443f20089e2446f119210e2bb8e8e6ee89cd69f0b74","tests_passed":1}
  feedback✔: All three comparisons correct — `32 < 45` is `True`, `45 == 45` is `True`, and `60 > 45` is `True`.  feedback✘: Check each comparison: use `<` for 'less than', `==` for 'equal to', and `>` for 'greater than'. Each `print()` should wrap one comparison expression.  hints: ['Each `print()` call should look like `print(variable operator sla)`. Which operator goes with each check?', 'Remember: `==` (two equals signs) tests equality; `=` (one equals sign) is assignment.']  remediation→r02
  MEASURES: B:write_comparison_expression(f1,f2); B:predict_boolean_result_of_comparison(f2)   anchors=['practice']
  taught-before-tested: B.f1←s04; B.f2←s04; B.f2←s04

### s08 · explainer · Combining conditions with and, or and not  [reward 5]
Logical operators — Build compound conditions from simpler comparisons using Python's three logical operators.
(intro) A single comparison asks one question at a time. To combine conditions — 'is this delivery both late and far from the depot?' — Python provides three logical operators: or, and and not. In ascending priority order they are: or (lowest), and, not (highest among the three). When there are no parentheses, and binds more tightly than or. ⟦C.f1 C:tb1 C:tb2⟧
(mechanism) x or y returns x if x is true, otherwise y. It is short-circuit: if is_late is True, Python never evaluates is_far. x and y returns x if x is false, otherwise y. It is also short-circuit: if is_late is False, Python skips is_far entirely. ⟦C.f2 C.f3 C:tb3 C:tb4⟧
[SIDE_BY_SIDE] or is true when at least one operand is true; and is true only when both are; both short-circuit to skip the second operand when the result is already determined. left_label: or — true if either | right_label: and — true only if both
  left:
[CODE python]
is_late or is_far
True or False
False or True
False or False
  annotations: ['True if either condition holds', 'True — first operand is true', 'True — second operand is true', 'False — neither is true']
  right:
[CODE python]
is_late and is_far
True and True
True and False
False and True
  annotations: ['True only if both conditions hold', 'True — both are true', 'False — second is false', 'False — first is false, short-circuits']

### s09 · explainer · not, priority and real-world compound conditions  [reward 5]
Logical operators — not flips a boolean; priority rules determine how mixed expressions group without parentheses.
(mechanism) not x flips the boolean: not is_late is True when is_late is False, and False when is_late is True. not has lower priority than the comparison operators, so not delivery_minutes == 0 is read as not (delivery_minutes == 0), not as (not delivery_minutes) == 0. ⟦C.f4 C:tb5⟧
(example) A rule like 'flag this delivery if it is late or unusually far' reads directly as is_late or is_far. A stricter rule — 'flag it only if it is late and it is the driver's first week' — reads as is_late and is_first_week. and, or and not let you build one compound condition out of several simpler comparisons. ⟦C.f2 C.f3 C:tb6⟧

### s10 · check · Predict operator priority in a mixed expression  [reward 10]
Quick check — How does Python group an expression that mixes and and or without parentheses?
QUESTION [choice, core, grading=client] What does Python evaluate `not is_late == False` to when `is_late = True`?

*(Hint: `not` has lower priority than comparison operators.)*
  ✔ opt_a: `True` — `not` applies to the result of `is_late == False`
      why: Correct. `not` has lower priority than `==`, so Python reads `not (is_late == False)`. `is_late == False` is `True == False` which is `False`, then `not False` is `True`.
  ✘ opt_b: `False` — `not is_late` is evaluated first, then compared to `False`
      why: This would be correct if `not` had higher priority than `==`, but it does not. `not` is evaluated last, so `is_late == False` is computed first.
  ✘ opt_c: `False` — `not` cancels out the comparison, making the whole expression `False`
      why: `not` does not cancel the comparison. It has lower priority than `==`, so Python evaluates `is_late == False` first (`True == False` → `False`), then `not False` → `True`.
  ✘ opt_d: A `SyntaxError` — `not` cannot appear before a comparison
      why: `not` is a valid operator and can appear before a comparison expression. Python evaluates the comparison first, then applies `not`.
  feedback✔: Right — `not` has lower priority than `==`, so Python evaluates `is_late == False` first (`True == False` = `False`), then `not False` = `True`.  feedback✘: Remember: `not` has lower priority than comparison operators. Python evaluates `is_late == False` first, then applies `not` to the result.  hints: ['The priority order (ascending) is: `or`, `and`, `not`, then comparison operators. Which is evaluated first: `==` or `not`?', 'Rewrite the expression with explicit parentheses to show which part Python evaluates first.']  remediation→r03
  MEASURES: C:predict_operator_priority(f1,f4)   anchors=['assessment:predict_operator_priority']
  taught-before-tested: C.f1←s08; C.f4←s09

### s11 · check · Predict the result of a short-circuit expression  [reward 10]
Quick check — Which operand does Python evaluate when the first one already decides the outcome?
QUESTION [choice, core, grading=client] Given `is_late = False` and `is_far = True`, what does `is_late and is_far` evaluate to?
  ✔ opt_a: `False` — `and` short-circuits: if the left side is false, it returns the left side without evaluating the right
      why: Correct. `x and y` returns `x` if `x` is false (short-circuit), so `False and is_far` returns `False` without evaluating `is_far`.
  ✘ opt_b: `True` — `and` returns `True` if either operand is `True`
      why: That describes `or`, not `and`. `and` requires both sides to be true; if the left side is false, it short-circuits and returns the left side.
  ✘ opt_c: `True` — `and` returns `True` when at least one operand is `True`
      why: `and` requires both operands to be true to return a truthy value. Since `is_late` is `False`, `False and is_far` returns `False`, not `True`.
  ✘ opt_d: `True` — `and` evaluates both sides and returns the last one
      why: That describes `or` when the left side is true. For `and`, if the left side is false, Python returns it immediately without evaluating the right side.
  feedback✔: Correct — `and` short-circuits: `False and is_far` returns `False` immediately, without evaluating `is_far`.  feedback✘: `x and y` returns `x` if `x` is false (short-circuit). Since `is_late` is `False`, Python returns `False` without checking `is_far`.  hints: ['For `x and y`: if `x` is false, what does Python return — and does it even look at `y`?', 'Short-circuit means Python stops as soon as the result is determined. Can `True and False` change the result of `False and ...`?']
  MEASURES: C:predict_short_circuit_result(f2,f3)   anchors=['assessment:predict_short_circuit_result']
  taught-before-tested: C.f2←s08; C.f3←s08

### s12 · hands_on · Write compound boolean expressions  [reward 15]
Practice — Combine comparisons with and, or and not to express multi-condition rules.
QUESTION [code_exercise, stretch, grading=client] QuickDeliver flags an order for review if it is late **or** it is far **and** not late (far-but-on-time is a different concern).

The rule is: `is_late or is_far and not is_late`

`delivery_minutes`, `sla`, `distance_km`, and `max_km` are assigned below.

Add lines that:
1. Assign `is_late` — `True` if `delivery_minutes > sla`, else `False`
2. Assign `is_far` — `True` if `distance_km > max_km`, else `False`
3. Print `is_late or is_far and not is_late`

Expected output:
```
True
```

*(Hint: `and` has higher priority than `or`, so `is_far and not is_late` is evaluated first.)*
  runtime={'kind': 'python', 'version': '0.29.5'} constraints.allowed=['name = value assignment', 'using assigned names in an expression, as in the width * height example', 'int, float, str and bool literals', 'single- or double-quoted strings', 'True / False', 'print()', 'type()', '+ - * / // % **', 'parentheses for grouping', '< <= > >= == !=', 'and', 'or', 'not'] blocked=64 items
  file solution.py [editable]:
delivery_minutes = 50
sla = 45
distance_km = 5
max_km = 10
# Derive is_late and is_far, then print the compound expression

  SOLUTION solution.py:
delivery_minutes = 50
sla = 45
distance_km = 5
max_km = 10
is_late = delivery_minutes > sla
is_far = distance_km > max_km
print(is_late or is_far and not is_late)

  test t1_stdout (stdout_equals, visible=True): {"expected":"True"} | on-fail: Output does not match. Derive `is_late = delivery_minutes > sla` and `is_far = distance_km > max_km`, then print `is_late or is_far and not is_late`.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"9bffe4c275a6e515f76ffe4d4ac8fdc8b854e07b605085b182d0a27c5d049ecf","tests_passed":1}
  feedback✔: Correct — `and` has higher priority than `or`, so Python evaluates `is_far and not is_late` first (`False and False = False`), then `is_late or False = True`.  feedback✘: Derive `is_late = delivery_minutes > sla` and `is_far = distance_km > max_km`, then print `is_late or is_far and not is_late`. Remember: `and` binds tighter than `or`.  hints: ['Use `>` to derive `is_late` and `is_far` from the numeric inputs.', 'For `is_late=True, is_far=False`: `is_far and not is_late` = `False and False` = `False`, then `True or False` = `True`.']  remediation→r03
  MEASURES: C:write_compound_boolean_expression(f1,f2,f3,f4); C:predict_operator_priority(f1,f4); C:predict_short_circuit_result(f2,f3)   anchors=['practice', 'assessment:write_compound_boolean_expression']
  taught-before-tested: C.f1←s08; C.f2←s08; C.f3←s08; C.f4←s09; C.f1←s08; C.f4←s09; C.f2←s08; C.f3←s08

### s13 · explainer · Converting between strings and numbers  [reward 5]
Type conversion — int(), float() and str() let you move values between types — but only when the format matches.
(intro) Data often arrives as the wrong type. A delivery time typed into a form as the text '32' cannot be used in arithmetic until it is converted to a number. Python provides three constructors for explicit conversion: int() and float() produce a number from a string or another numeric type, and str() turns any value into its string representation. ⟦D.f1 D.f4 D:tb1 D:tb4⟧
(mechanism) int('123') returns the integer 123. float('+1.23') returns the float 1.23. str(32) turns the integer 32 into the string '32'. These conversions work in both directions between numbers and their string representations. ⟦D.f2 D.f3 D.f4 D:tb2 D:tb3 D:tb4⟧
(misconception) Not every string can be converted. float() requires the string to match a numeric format — an optional sign, digits, and optionally a decimal point or exponent — after stripping surrounding whitespace. int() requires an integer string. A string that does not match raises a ValueError: int('3.5') fails because '3.5' is not an integer string. ⟦D.f5 D.f6 D:tb5⟧
[BEFORE_AFTER] Converting '32' from string to int with int() makes arithmetic possible; without conversion, adding a number raises a TypeError.
  before:
[CODE python]
delivery_time = '32'
delivery_time + 10
  annotations: ["String '32' — cannot add a number to it", 'TypeError: can only concatenate str to str']
  after:
[CODE python]
delivery_time = int('32')
delivery_time + 10
  annotations: ["int('32') returns the integer 32", 'Result: 42 — arithmetic now works']

### s14 · check · Convert a value to the target type  [reward 10]
Quick check — Which constructor and argument produces the value described?
QUESTION [choice, intro, grading=client] A CSV file stores delivery times as strings. The value `'45'` needs to be used in arithmetic.

Which expression converts the string `'45'` to an integer?
  ✔ opt_a: `int('45')`
      why: Correct. `int('45')` returns the integer `45`, constructed from the string `'45'`.
  ✘ opt_b: `float('45')`
      why: `float('45')` returns `45.0`, a floating-point number — not an integer. Use `int()` when you need a whole number.
  ✘ opt_c: `str(45)`
      why: `str(45)` converts the integer `45` to the string `'45'` — the opposite direction. You need `int()` to go from string to integer.
  ✘ opt_d: `bool('45')`
      why: `bool('45')` returns `True` (any non-empty string is truthy), not an integer. Use `int()` to convert a numeric string to an integer.
  feedback✔: Right — `int('45')` constructs the integer `45` from the string `'45'`. This is the standard way to convert a numeric string to an integer.  feedback✘: To convert a string to an integer, use `int(string)`. `float()` gives a decimal, `str()` goes the other direction, and `bool()` gives `True`/`False`.  hints: ['Which constructor produces an integer object: `int()`, `float()`, `str()`, or `bool()`?', 'The function name matches the type you want: `int()` → integer, `float()` → float, `str()` → string.']  remediation→r05
  MEASURES: D:convert_value_to_target_type(f1,f2,f3,f4)   anchors=['assessment:convert_value_to_target_type']
  taught-before-tested: D.f1←s13; D.f2←s13; D.f3←s13; D.f4←s13

### s15 · check · Recognise an invalid conversion  [reward 10]
Quick check — Which string cannot be converted by the given constructor?
QUESTION [choice, core, grading=client] What happens when Python executes `int('3.5')`?
  ✔ opt_a: Raises a `ValueError` — `int()` requires an integer-format string, not a decimal string
      why: Correct. `int()` requires a string in integer format (digits only, with optional sign and whitespace). `'3.5'` contains a decimal point, so Python raises `ValueError`.
  ✘ opt_b: Returns `3` — `int()` truncates the decimal part
      why: `int()` does not truncate decimal strings. To truncate, first convert to float: `int(float('3.5'))` gives `3`. Passing `'3.5'` directly to `int()` raises `ValueError`.
  ✘ opt_c: Returns `4` — `int()` rounds to the nearest integer
      why: `int()` does not round. It raises `ValueError` for any string that is not in integer format. To round, use `round(float('3.5'))`.
  ✘ opt_d: Returns `3.5` — `int()` passes the value through unchanged
      why: `int()` cannot pass a string through unchanged — it must parse it as an integer. `'3.5'` is not a valid integer string, so it raises `ValueError`.
  feedback✔: Correct — `int('3.5')` raises `ValueError` because `'3.5'` is not in integer format. To convert a decimal string, use `int(float('3.5'))` instead.  feedback✘: `int()` requires the string to be in integer format (whole number only). `'3.5'` has a decimal point, so Python raises `ValueError`.  hints: ['What format does `int()` require its string argument to be in?', "If you need to convert `'3.5'` to an integer, what two-step conversion would work?"]  remediation→r06
  MEASURES: D:recognize_invalid_conversion(f5,f6)   anchors=['assessment:recognize_invalid_conversion']
  taught-before-tested: D.f5←s13; D.f6←s13

### s16 · hands_on · Convert delivery data between types  [reward 15]
Practice — Use int(), float() and str() to fix type mismatches in order records.
QUESTION [code_exercise, core, grading=client] A delivery record stores the time as an integer. Convert it to different types and print each result.

`delivery_minutes` is assigned below as an integer.

Add four lines that:
1. Assign `dm_str` — `delivery_minutes` converted to a **string** using `str()`
2. Assign `dm_float` — `dm_str` converted to a **float** using `float()`
3. Assign `dm_int` — `dm_str` converted to an **integer** using `int()`
4. Print `dm_str`, `dm_float`, and `dm_int` each on its own line.

Expected output:
```
32
32.0
32
```
  runtime={'kind': 'python', 'version': '0.29.5'} constraints.allowed=['name = value assignment', 'using assigned names in an expression, as in the width * height example', 'int, float, str and bool literals', 'single- or double-quoted strings', 'True / False', 'print()', 'type()', '+ - * / // % **', 'parentheses for grouping', '< <= > >= == !=', 'and', 'or', 'not', 'int()', 'float()', 'str()'] blocked=61 items
  file solution.py [editable]:
delivery_minutes = 32
# Convert to str, float, and int; then print each

  SOLUTION solution.py:
delivery_minutes = 32
dm_str = str(delivery_minutes)
dm_float = float(dm_str)
dm_int = int(dm_str)
print(dm_str)
print(dm_float)
print(dm_int)

  test t1_dm_str (value_equals, visible=True): {"expr":"type(dm_str).__name__ + ':' + dm_str","expected":"str:32"} | on-fail: `dm_str` should be a string. Use `str(delivery_minutes)` to convert.
  test t2_dm_float (value_equals, visible=True): {"expr":"type(dm_float).__name__ + ':' + str(dm_float)","expected":"float:32.0"} | on-fail: `dm_float` should be a float. Use `float(dm_str)` to convert.
  test t3_dm_int (value_equals, visible=True): {"expr":"type(dm_int).__name__ + ':' + str(dm_int)","expected":"int:32"} | on-fail: `dm_int` should be an integer. Use `int(dm_str)` to convert.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"77d30ac3e69d57698306f7f935f9e8f8166458b4b4c5e5cf6c93f1f6b9a34a31","tests_passed":3}
  feedback✔: All three conversions correct — `str(32)` gives `'32'`, `float('32')` gives `32.0`, and `int('32')` gives `32`.  feedback✘: Use `str()`, `float()`, and `int()` to convert between types. First convert `delivery_minutes` to a string with `str()`, then convert that string to float and int.  hints: ['Step 1: `dm_str = str(delivery_minutes)` converts the integer to a string.', 'Step 2: `dm_float = float(dm_str)` and `dm_int = int(dm_str)` convert the string to float and int.']  remediation→r05
  MEASURES: D:convert_value_to_target_type(f1,f2,f3,f4)   anchors=['practice']
  taught-before-tested: D.f1←s13; D.f2←s13; D.f3←s13; D.f4←s13

### s17 · recap · What you learned  [reward 5]
Recap — Key ideas from this tile.
(takeaway) Comparison operators (<, <=, >, >=, ==, !=) each return True or False. and, or and not combine those booleans into compound conditions; and has higher priority than or. Converting a string to a number only works when the string matches the format the target type accepts — otherwise the conversion raises a ValueError. ⟦B.f2 C.f1 D.f5 D.f6 B:tb4 C:tb7 D:tb6⟧
[UP NEXT] Up next: Lists, Dictionaries, and Tuples: In the next tile you will store ordered sequences of delivery times in lists, map order IDs to cities in dictionaries, and group fixed records in tuples.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Grouping with parentheses and mixed int/float — A clear contrast showing how parentheses change the result, and why mixing int and float gives a float.
(mechanism) Parentheses control evaluation order: (32 + 8) * 2 adds first, giving 80. Without parentheses, * runs before +. When you mix an int and a float in one operation, Python promotes the int to float: 4 * 3.75 - 1 gives 14.0, not 14. ⟦A.f4 A.f5 A:tb2⟧
[BEFORE_AFTER] Adding parentheses changes the evaluation order and the result.
  before:
[CODE python]
32 + 8 * 2
  annotations: ['Result: 48 — * runs before +']
  after:
[CODE python]
(32 + 8) * 2
  annotations: ['Result: 80 — parentheses force addition first']
### r02 · Comparison operators and boolean results — A side-by-side contrast showing the same expression returning different booleans for different values.
(definition) The six comparison operators are < (less than), <= (less than or equal), > (greater than), >= (greater than or equal), == (equal) and != (not equal). Every comparison returns exactly True or False — never a number. ⟦B.f1 B.f2 B:tb1 B:tb2⟧
[SIDE_BY_SIDE] The same expression delivery_minutes > 60 gives False for 32 and True for 72. left_label: 32 minutes (not late) | right_label: 72 minutes (late)
  left:
[CODE python]
delivery_minutes = 32
delivery_minutes > 60
  annotations: ['32 minutes', 'False — 32 is not greater than 60']
  right:
[CODE python]
delivery_minutes = 72
delivery_minutes > 60
  annotations: ['72 minutes', 'True — 72 is greater than 60']
### r03 · Operator priority: and before or — A contrast showing how and and or group when there are no parentheses.
(mechanism) In ascending priority order the logical operators are: or (lowest), and, not. and binds more tightly than or, so is_late or is_far and is_first_week groups as is_late or (is_far and is_first_week). not has lower priority than comparison operators: not delivery_minutes == 0 means not (delivery_minutes == 0). ⟦C.f1 C.f4 C:tb2 C:tb5⟧
[BEFORE_AFTER] Without parentheses, and groups first; adding parentheses changes which conditions must both be true.
  before:
[CODE python]
is_late or is_far and is_first_week
  annotations: ['Groups as: is_late or (is_far and is_first_week)']
  after:
[CODE python]
(is_late or is_far) and is_first_week
  annotations: ['Parentheses override priority — both sides must be true']
### r04 · Short-circuit evaluation in or and and — A side-by-side contrast showing when each operator stops evaluating early.
(mechanism) or short-circuits: if the first operand is True, Python returns it immediately without evaluating the second. and short-circuits: if the first operand is False, Python returns it immediately without evaluating the second. This means is_late or is_far only checks is_far when is_late is False, and is_late and is_far only checks is_far when is_late is True. ⟦C.f2 C.f3 C:tb3 C:tb4⟧
[SIDE_BY_SIDE] Both operators skip the second operand when the first operand already determines the result. left_label: or short-circuits on True | right_label: and short-circuits on False
  left:
[CODE python]
is_late = True
is_late or is_far
  annotations: ['is_late is True', 'Returns True — is_far never evaluated']
  right:
[CODE python]
is_late = False
is_late and is_far
  annotations: ['is_late is False', 'Returns False — is_far never evaluated']
### r05 · Converting between strings and numbers — A before/after showing what happens with and without int().
(mechanism) int('123') returns 123. float('+1.23') returns 1.23. str(32) returns '32'. These constructors convert between compatible types: a string of digits to int, a numeric-format string to float, any value to its string form. ⟦D.f1 D.f2 D.f3 D.f4 D:tb2 D:tb3 D:tb4⟧
[BEFORE_AFTER] Wrapping '32' in int() converts it to the integer 32, making arithmetic possible.
  before:
[CODE python]
delivery_time = '32'
result = delivery_time + 10
  annotations: ['String — cannot add to int', 'TypeError raised']
  after:
[CODE python]
delivery_time = int('32')
result = delivery_time + 10
  annotations: ["int('32') gives 32", 'Result: 42']
### r06 · When type conversion raises ValueError — A contrast between a failing conversion and a working alternative.
(misconception) float() requires the string to match a numeric format: an optional sign, digits, and optionally a decimal point or exponent, after stripping surrounding whitespace. int() requires an integer string — no decimal point. A string that does not match raises a ValueError: int('3.5') fails because '3.5' contains a decimal point. ⟦D.f5 D.f6 D:tb5⟧
[SIDE_BY_SIDE] int() cannot parse a decimal string — it raises ValueError. float() accepts decimal strings; use float() when the string contains a decimal point. left_label: int('3.5') — ValueError | right_label: float('3.5') — succeeds
  left:
[CODE python]
int('3.5')
  annotations: ["ValueError — '3.5' is not an integer string"]
  right:
[CODE python]
float('3.5')
  annotations: ['Result: 3.5 — decimal strings are valid for float()']

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: list[i] and list[-1] indexing
· constraints.blocked_syntax: {key: value} dictionary literal
· constraints.blocked_syntax: d[key] lookup and assignment
· constraints.blocked_syntax: tuple literal with commas or parentheses
· constraints.blocked_syntax: one-item tuple with trailing comma
· constraints.blocked_syntax: quote mixing to embed a quote
· constraints.blocked_syntax: f-strings f"...{expr}..."
· constraints.blocked_syntax: format specifier such as {value:.2f}
· constraints.blocked_syntax: colon and indented block
· constraints.blocked_syntax: for item in sequence:
· constraints.blocked_syntax: [expr for x in seq if cond]
· constraints.blocked_syntax: for k, v in d.items():
· constraints.blocked_syntax: positional arguments in a call
· constraints.blocked_syntax: def f(a, b=default):
· constraints.blocked_syntax: keyword arguments f(name=value)
· constraints.blocked_syntax: from module import name
· constraints.blocked_syntax: with open(...) as f:
· constraints.blocked_syntax: += and other augmented assignment
· constraints.blocked_syntax: list[i] and list[-1] indexing
· constraints.blocked_syntax: {key: value} dictionary literal
· constraints.blocked_syntax: d[key] lookup and assignment
· constraints.blocked_syntax: tuple literal with commas or parentheses
· constraints.blocked_syntax: one-item tuple with trailing comma
· constraints.blocked_syntax: quote mixing to embed a quote
· constraints.blocked_syntax: f-strings f"...{expr}..."
· constraints.blocked_syntax: format specifier such as {value:.2f}
· constraints.blocked_syntax: colon and indented block
· constraints.blocked_syntax: for item in sequence:
· constraints.blocked_syntax: [expr for x in seq if cond]
· constraints.blocked_syntax: for k, v in d.items():
· constraints.blocked_syntax: positional arguments in a call
· constraints.blocked_syntax: def f(a, b=default):
· constraints.blocked_syntax: keyword arguments f(name=value)
· constraints.blocked_syntax: from module import name
· constraints.blocked_syntax: with open(...) as f:
· constraints.blocked_syntax: += and other augmented assignment
· constraints.blocked_syntax: list[i] and list[-1] indexing
· constraints.blocked_syntax: {key: value} dictionary literal
· constraints.blocked_syntax: d[key] lookup and assignment
· constraints.blocked_syntax: tuple literal with commas or parentheses
· constraints.blocked_syntax: one-item tuple with trailing comma
· constraints.blocked_syntax: quote mixing to embed a quote
· constraints.blocked_syntax: f-strings f"...{expr}..."
· constraints.blocked_syntax: format specifier such as {value:.2f}
· constraints.blocked_syntax: colon and indented block
· constraints.blocked_syntax: for item in sequence:
· constraints.blocked_syntax: [expr for x in seq if cond]
· constraints.blocked_syntax: for k, v in d.items():
· constraints.blocked_syntax: positional arguments in a call
· constraints.blocked_syntax: def f(a, b=default):
· constraints.blocked_syntax: keyword arguments f(name=value)
· constraints.blocked_syntax: from module import name
· constraints.blocked_syntax: with open(...) as f:
· constraints.blocked_syntax: += and other augmented assignment
· constraints.blocked_syntax: list[i] and list[-1] indexing
· constraints.blocked_syntax: {key: value} dictionary literal
· constraints.blocked_syntax: d[key] lookup and assignment
· constraints.blocked_syntax: tuple literal with commas or parentheses
· constraints.blocked_syntax: one-item tuple with trailing comma
· constraints.blocked_syntax: quote mixing to embed a quote
· constraints.blocked_syntax: f-strings f"...{expr}..."
· constraints.blocked_syntax: format specifier such as {value:.2f}
· constraints.blocked_syntax: colon and indented block
· constraints.blocked_syntax: for item in sequence:
· constraints.blocked_syntax: [expr for x in seq if cond]
· constraints.blocked_syntax: for k, v in d.items():
· constraints.blocked_syntax: positional arguments in a call
· constraints.blocked_syntax: def f(a, b=default):
· constraints.blocked_syntax: keyword arguments f(name=value)
· constraints.blocked_syntax: from module import name
· constraints.blocked_syntax: with open(...) as f:
· constraints.blocked_syntax: += and other augmented assignment

=========

# EVALUATOR PACKET — Sets and Strings (tile_python_sets_strings)
Tile summary: Use sets to collect unique values and test membership, combine sets with union and intersection, and build readable messages with f-strings and format specifiers.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.sets — Core data structure: sets
B = python.string_basics_formatting — String basics and f-string formatting

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: remediation step tile_python_sets_strings.r02 is never referenced

## SOURCE FACTS — A (python.sets)   objective: Create a set to store unique values, test membership in it, and combine two sets with union and intersection.
A.f1: A set is an unordered collection with no duplicate elements, used for membership testing and eliminating duplicate entries.   [sources: python_docs_tutorial_datastructures#sets]
A.f2: Curly braces or the set() function create a set; set() must be used for an empty set, because {} creates an empty dictionary instead.   [sources: python_docs_tutorial_datastructures#sets]
A.f3: set() can also build a set from the items of another collection, e.g. set('abracadabra') produces the set of unique letters in that string.   [sources: python_docs_tutorial_datastructures#sets]
A.f4: The in operator tests membership in a set, e.g. 'orange' in basket.   [sources: python_docs_tutorial_datastructures#sets]
A.f5: Set objects support mathematical operations such as union (a | b) and intersection (a & b).   [sources: python_docs_tutorial_datastructures#sets]
note: Keep the cities-from-orders framing throughout so 'unique values' stays concrete.
PRACTICE ANCHOR (live_code): Remove duplicates from a list of cities by converting it to a set, then test whether a given city is in the set.  SUCCESS: The set holds each city once; the membership test prints True for a city in the list and False for one that is not.
ASSESSMENT ANCHOR: create_set_of_unique_values facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: test_set_membership facts=['f4']
ASSESSMENT ANCHOR: combine_sets_with_union_and_intersection facts=['f5']

## SOURCE FACTS — B (python.string_basics_formatting)   objective: Write string literals and use f-strings to build a readable message that embeds variable values, including numbers formatted to a chosen number of decimal places.
B.f1: A quote character can be embedded in a string without escaping it by enclosing the string in the other kind of quote instead, e.g. "doesn't" instead of 'doesn\'t'.   [sources: python_docs_tutorial_introduction#text]
B.f2: An f-string is a string literal prefixed with f or F that embeds the value of a Python expression inside the string by writing the expression in curly brackets {expression}.   [sources: python_docs_tutorial_inputoutput#formatted-string-literals]
B.f3: An optional format specifier can follow the expression after a colon, giving greater control over how the value is formatted, such as rounding a number to a chosen number of places after the decimal (e.g. {value:.3f}).   [sources: python_docs_tutorial_inputoutput#formatted-string-literals]
PRACTICE ANCHOR (live_code): Write an f-string that reports a computed total inside a sentence, formatted to two decimal places.  SUCCESS: The printed sentence contains the computed total rounded to two decimal places.
ASSESSMENT ANCHOR: embed_quote_without_escaping facts=['f1']
ASSESSMENT ANCHOR: write_formatted_fstring facts=['f2', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Basic error handling (try/except); Basic file I/O (reading/writing text and CSV files); Comparing correlation strength across multiple variable pairs; Control flow: if/elif/else; Correlation between two variables; Correlation-vs-causation caveat in business interpretation; Default and keyword arguments; Defining calling functions; Distribution shape (skewness, symmetry, outliers); For loops; Identifying and reasoning about outliers; Idiomatic style conventions for readable Python; Iterating over data structures; List and dict comprehensions; Loop control statements (break, continue); Measures of central tendency (mean, median, mode); Measures of spread (range, variance, standard deviation); Modules and imports; Parameters arguments; Reading a frequency distribution/histogram in statistical terms; Reading data (read_csv, read_excel); Return values; Series and DataFrame data structures; String basics and f-string formatting; Variable scope (local vs global); While loops

## LESSON, in learner order

### s01 · explainer · Unique, unordered collections  [reward 5]
Sets — A set stores only distinct values — duplicates are automatically removed.
(intro) Sometimes you only care about which distinct values appear — which cities orders were delivered to, with no duplicates. A set is an unordered collection with no duplicate elements, used for membership testing and eliminating duplicate entries. ⟦A.f1 A:tb1⟧
(mechanism) Curly braces or the set() function create a set. set() must be used for an empty set, because {} creates an empty dictionary instead. set() can also build a set from another collection: cities = set(['Lagos', 'Abuja', 'Lagos', 'Kano']) produces {'Lagos', 'Abuja', 'Kano'} — the duplicate 'Lagos' is collapsed to one entry. ⟦A.f2 A.f3 A:tb2 A:tb3⟧
[BEFORE_AFTER] Passing the list through set() collapses the repeated 'Lagos' to a single entry, leaving only unique cities.
  before:
[CODE python]
cities_list = ['Lagos', 'Abuja', 'Lagos', 'Kano']
  annotations: ['List with a repeated city']
  after:
[CODE python]
cities = set(['Lagos', 'Abuja', 'Lagos', 'Kano'])
  annotations: ["{'Lagos', 'Abuja', 'Kano'} — duplicate removed"]
(mechanism) Test whether a value is in the set with the `in` operator: `'Lagos' in cities` returns `True` if `'Lagos'` is in the set, and `False` otherwise. This membership test is the primary reason to use a set rather than a list when you only need to check presence. ⟦A.f4 A:tb4⟧ ⟦A.f4 A:tb4⟧

### s02 · video · Sets in action
Watch — See set creation, membership testing and set operations demonstrated.
[VIDEO Creating sets, dropping duplicates, and combining sets] bridge-before: Watch the duplicates disappear in both clips, then the | and & results on two small sets. The membership check near the end uses an if-statement the course hasn't covered yet — focus on the expression 1 in first, which is the membership test. | bridge-after: Only the first clip gives the empty-set caveat (set() instead of {}). The text ties creation, membership and the two operations to one delivery-cities example.
  - r3R3h5ly_8g 26-158s facts=['f1', 'f2', 'f3'] label: What a set is, two ways to create one, and how duplicates are dropped | summary: Describes a set as like a list that removes duplicate values; intersection and difference are only named as extra tools here. Creates one by passing a list of the numbers 1 to 5 to set(), prints it with curly brackets, then shows the same result by writing the values directly inside curly braces. Warns that empty curly braces make an empty dictionary, so an empty set needs set() with no arguments. Adding repeated values to the end leaves the printed set unchanged.
  - t9j8lCUGZXo 2-243s facts=['f1', 'f3', 'f4', 'f5'] label: Sets in Python: unordered unique collections, set() constructor, membership testing, and union/intersection operations | summary: Starts from a list of numbers with duplicates and converts it with set() so only unique items remain, then shows curly braces defining a set and quickly adds, removes and counts items. The main part runs union with the vertical bar, intersection with &, difference with a minus sign and symmetric difference with a caret on two small sets, then notes that sets are unordered so indexing into one raises an error. Ends with a membership check, 1 in first, and a recap.

### s03 · explainer · Union and intersection  [reward 5]
Sets — | combines two sets; & finds what they share.
(mechanism) Set objects support mathematical operations. Union (a | b) gives all elements from both sets. Intersection (a & b) gives only elements present in both: week1_cities & week2_cities gives cities that appeared in both weeks. ⟦A.f5 A:tb5⟧

### s04 · check · Create a set of unique values  [reward 10]
Quick check — Which expression produces a set with no duplicates from a list of cities?
QUESTION [choice, intro, grading=client] Which expression creates a set of unique cities from the list `['Lagos', 'Abuja', 'Lagos', 'Kano']`?
  ✔ opt_a: `set(['Lagos', 'Abuja', 'Lagos', 'Kano'])`
      why: Correct. `set(iterable)` builds a set from any iterable, removing duplicates. `set(['Lagos', 'Abuja', 'Lagos', 'Kano'])` gives `{'Lagos', 'Abuja', 'Kano'}`.
  ✘ opt_b: `{}`
      why: `{}` creates an **empty dictionary**, not an empty set. To create an empty set, use `set()`. To create a non-empty set, use `set(iterable)` or `{val1, val2, ...}`.
  ✘ opt_c: `['Lagos', 'Abuja', 'Kano']`
      why: `['Lagos', 'Abuja', 'Kano']` is a list, not a set. Lists preserve order and allow duplicates; sets do not.
  ✘ opt_d: `{'Lagos': True, 'Abuja': True, 'Kano': True}`
      why: That creates a dictionary with string keys and `True` values — not a set. Use `set(iterable)` or `{val1, val2, ...}` to create a set.
  feedback✔: `set(iterable)` builds a set of unique values from any iterable. Note: `{}` alone creates an empty dictionary — use `set()` for an empty set.  feedback✘: Use `set(iterable)` to build a set from a list, removing duplicates. `{}` creates an empty dictionary, not a set.  hints: ['Which function builds a set from an existing collection, removing duplicates?', 'What does `{}` create — a set or a dictionary? How do you create an empty set?']  remediation→r01
  MEASURES: A:create_set_of_unique_values(f1,f2,f3)   anchors=['assessment:create_set_of_unique_values']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s05 · check · Combine sets with union and intersection  [reward 10]
Quick check — Which operator gives elements present in both sets, and which gives all elements from either?
QUESTION [choice, core, grading=client] Given:

```python
morning = {'Lagos', 'Abuja', 'Kano'}
evening = {'Kano', 'Ibadan', 'Lagos'}
```

What does `morning & evening` return?
  ✔ opt_a: A set containing `'Lagos'` and `'Kano'` — cities that appear in both sets
      why: Correct. `&` is the intersection operator — it returns only the elements that appear in **both** sets. `'Lagos'` and `'Kano'` are in both `morning` and `evening`.
  ✘ opt_b: A set containing all four cities — all cities from both sets
      why: That is the **union** (`|`), which returns all elements from both sets. The intersection (`&`) returns only elements present in both.
  ✘ opt_c: A set containing `'Abuja'` and `'Ibadan'` — cities that appear in only one set
      why: That is the **symmetric difference** (`^`), which returns elements in one set but not the other. The intersection (`&`) returns elements in both.
  ✘ opt_d: A set containing `'Lagos'`, `'Kano'`, and `'Ibadan'` — cities from the evening set
      why: That is the `evening` set itself. The intersection (`&`) returns only elements that appear in both sets.
  feedback✔: Right — `&` is intersection: elements in both sets. `morning & evening` gives `{'Lagos', 'Kano'}`. Use `|` for union (all elements from both).  feedback✘: `&` is intersection — only elements present in **both** sets. `|` is union — all elements from either set.  hints: ["In set mathematics, intersection means 'in both'. Which cities appear in both `morning` and `evening`?", 'Remember: `|` is union (all elements), `&` is intersection (shared elements only).']
  MEASURES: A:combine_sets_with_union_and_intersection(f5)   anchors=['assessment:combine_sets_with_union_and_intersection']
  taught-before-tested: A.f5←s03

### s06 · hands_on · Test membership in a set of cities  [reward 15]
Practice — Build a set of delivery cities and use in to check whether a given city is present.
QUESTION [code_exercise, core, grading=client] QuickDeliver wants to know which unique cities appear in a batch of orders.

`city_a`, `city_b`, `city_c`, `city_d`, and `cities_list` are assigned below (the list contains duplicates).

Add lines that:
1. Assign `unique_cities` — a set built from `cities_list` using `set()`
2. Print whether `'Lagos'` is in `unique_cities`
3. Print whether `'Enugu'` is in `unique_cities`

Expected output:
```
True
False
```
  runtime={'kind': 'python', 'version': '0.29.5'} constraints.allowed=['name = value assignment', 'using assigned names in an expression, as in the width * height example', 'int, float, str and bool literals', 'single- or double-quoted strings', 'True / False', 'print()', 'type()', '+ - * / // % **', 'parentheses for grouping', '< <= > >= == !=', 'and', 'or', 'not', 'int()', 'float()', 'str()', '[...] list literal', 'list[i] and list[-1] indexing', 'list[a:b] slicing', 'list[i] = value', 'list.append()', 'len()', '{key: value} dictionary literal', 'd[key] lookup and assignment', 'd.get()', 'key in d', 'tuple literal with commas or parentheses', 'unpacking a, b = t', 'one-item tuple with trailing comma', 'set()', '{...} set literal', 'x in a_set', '| and & on sets'] blocked=45 items
  file solution.py [editable]:
city_a = 'Lagos'
city_b = 'Abuja'
city_c = 'Kano'
city_d = 'Ibadan'
cities_list = [city_a, city_b, city_c, city_a, city_d, city_b]
# Build unique_cities set, then print membership for 'Lagos' and 'Enugu'

  SOLUTION solution.py:
city_a = 'Lagos'
city_b = 'Abuja'
city_c = 'Kano'
city_d = 'Ibadan'
cities_list = [city_a, city_b, city_c, city_a, city_d, city_b]
unique_cities = set(cities_list)
print('Lagos' in unique_cities)
print('Enugu' in unique_cities)

  test t1_stdout (stdout_equals, visible=True): {"expected":"True\nFalse"} | on-fail: Output does not match. Print `'Lagos' in unique_cities` then `'Enugu' in unique_cities`, each on its own line.
  test t2_lagos_present (value_equals, visible=True): {"expr":"'Lagos' in unique_cities","expected":true} | on-fail: `'Lagos'` should be in `unique_cities`. Use `unique_cities = set(cities_list)` — `city_a` is `'Lagos'` and appears in `cities_list`.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"9b09fe7ed4f260e6576679a3f6ae5cda6c4f4ddde956743fbae38c3213d21c1c","tests_passed":2}
  feedback✔: Correct — `set(cities_list)` removes duplicates, and `'Lagos' in unique_cities` is `True` while `'Enugu' in unique_cities` is `False`.  feedback✘: Use `set(cities_list)` to build the set, then `print('Lagos' in unique_cities)` and `print('Enugu' in unique_cities)`.  hints: ['To build a set from a list: `unique_cities = set(cities_list)`. Sets automatically remove duplicates.', "The `in` operator tests membership: `'Lagos' in unique_cities` returns `True` if `'Lagos'` is in the set."]  remediation→r01
  MEASURES: A:create_set_of_unique_values(f1,f2,f3); A:test_set_membership(f4)   anchors=['practice', 'assessment:test_set_membership']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01; A.f4←s01

### s07 · explainer · Embedding values and formatting numbers  [reward 5]
Strings and f-strings — f-strings embed variable values directly in a string; a format specifier controls how numbers are displayed.
(mechanism) A quote character can be embedded in a string without escaping it by using the other kind of quote. Writing "This delivery wasn't late" inside double quotes needs no escaping; the same text inside single quotes would need the apostrophe escaped as \'. ⟦B.f1 B:tb1⟧
(definition) An f-string is a string literal prefixed with f or F that embeds the value of a Python expression inside the string by writing the expression in curly brackets: f"Delivery to {city} took {delivery_minutes} minutes" substitutes in the current values of city and delivery_minutes. ⟦B.f2 B:tb2⟧
(mechanism) An optional format specifier follows the expression after a colon, controlling how the value is displayed. f"Average: {avg_minutes:.2f} minutes" produces 'Average: 32.67 minutes' when avg_minutes is 32.666 — the .2f specifier rounds to two decimal places. ⟦B.f3 B:tb3⟧
[BEFORE_AFTER] Adding :.2f after the expression rounds the output to two decimal places — the {value:.2f} part and its rounded result.
  before:
[CODE python]
avg_minutes = 32.666
f"Average: {avg_minutes} minutes"
  annotations: ['avg_minutes holds 32.666', "Produces: 'Average: 32.666 minutes'"]
  after:
[CODE python]
avg_minutes = 32.666
f"Average: {avg_minutes:.2f} minutes"
  annotations: ['Same value', "Produces: 'Average: 32.67 minutes'"]

### s08 · check · Embed a quote without escaping  [reward 10]
Quick check — Which string literal correctly embeds an apostrophe without a backslash escape?
QUESTION [choice, intro, grading=client] Which string literal correctly stores the text: `The driver's route`?
  ✔ opt_a: `"The driver's route"`
      why: Correct. Enclosing the string in double quotes lets you include a single quote (`'`) inside without escaping it.
  ✘ opt_b: `'The driver's route'`
      why: The single quote in `driver's` ends the string early, causing a `SyntaxError`. Use double quotes to enclose a string that contains a single quote.
  ✘ opt_c: `"The driver"s route"`
      why: The double quote after `driver` ends the string, and `s route"` is invalid syntax. The string must be enclosed consistently.
  ✘ opt_d: `The driver's route`
      why: A string literal must be enclosed in quotes. Without quotes, Python treats `The` as a name and raises a `NameError`.
  feedback✔: Right — enclosing in double quotes lets you include a single quote inside: `"The driver's route"`. No escaping needed.  feedback✘: To include a single quote in a string, enclose the whole string in double quotes: `"The driver's route"`. The outer quote type must differ from the embedded one.  hints: ["If the string contains a `'`, which type of outer quotes avoids a conflict?", 'Python lets you mix quote types: use `"..."` when the string contains `\'`, and `\'...\'` when it contains `"`.']  remediation→r03
  MEASURES: B:embed_quote_without_escaping(f1)   anchors=['assessment:embed_quote_without_escaping']
  taught-before-tested: B.f1←s07

### s09 · hands_on · Write a formatted f-string  [reward 15]
Practice — Build an f-string that reports a computed total formatted to two decimal places.
QUESTION [code_exercise, core, grading=client] QuickDeliver wants a summary sentence showing the average delivery time.

`delivery_a` and `delivery_b` are assigned below.

Add lines that:
1. Assign `total` — the sum of `delivery_a` and `delivery_b`
2. Assign `avg` — `total` divided by `2`
3. Print the sentence using an f-string with `avg` rounded to **two decimal places**

Expected output:
```
Average delivery time: 38.50 minutes
```
  runtime={'kind': 'python', 'version': '0.29.5'} constraints.allowed=['name = value assignment', 'using assigned names in an expression, as in the width * height example', 'int, float, str and bool literals', 'single- or double-quoted strings', 'True / False', 'print()', 'type()', '+ - * / // % **', 'parentheses for grouping', '< <= > >= == !=', 'and', 'or', 'not', 'int()', 'float()', 'str()', '[...] list literal', 'list[i] and list[-1] indexing', 'list[a:b] slicing', 'list[i] = value', 'list.append()', 'len()', '{key: value} dictionary literal', 'd[key] lookup and assignment', 'd.get()', 'key in d', 'tuple literal with commas or parentheses', 'unpacking a, b = t', 'one-item tuple with trailing comma', 'set()', '{...} set literal', 'x in a_set', '| and & on sets', 'quote mixing to embed a quote', 'f-strings f"...{expr}..."', 'format specifier such as {value:.2f}'] blocked=41 items
  file solution.py [editable]:
delivery_a = 32
delivery_b = 45
# Compute total and avg, then print the formatted sentence

  SOLUTION solution.py:
delivery_a = 32
delivery_b = 45
total = delivery_a + delivery_b
avg = total / 2
print(f"Average delivery time: {avg:.2f} minutes")

  test t1_stdout (stdout_equals, visible=True): {"expected":"Average delivery time: 38.50 minutes"} | on-fail: Output does not match. Use an f-string with `{avg:.2f}` to round to two decimal places.
  test t2_avg (value_equals, visible=True): {"expr":"avg","expected":38.5} | on-fail: `avg` should be `38.5`. Compute `total = delivery_a + delivery_b`, then `avg = total / 2`.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"bc6786b6a665f7fd8f8987935c9ef7bf0c0a58bcefb49874b5cb16055ba36450","tests_passed":2}
  feedback✔: Correct — `{avg:.2f}` in the f-string formats `38.5` as `38.50`, giving the sentence `Average delivery time: 38.50 minutes`.  feedback✘: Use an f-string: `f"Average delivery time: {avg:.2f} minutes"`. The `:.2f` format specifier rounds to two decimal places.  hints: ['An f-string starts with `f` before the opening quote: `f"..."`.', 'To embed a value rounded to two decimal places, write `{avg:.2f}` inside the f-string.']  remediation→r03
  MEASURES: B:write_formatted_fstring(f1,f2,f3)   anchors=['practice', 'assessment:write_formatted_fstring']
  taught-before-tested: B.f1←s07; B.f2←s07; B.f3←s07

### s10 · recap · What you learned  [reward 5]
Recap — Key ideas from this tile.
(takeaway) A set stores only distinct values — pass a list through set() to remove duplicates. The in operator tests membership; | and & compute union and intersection. f-strings embed variable values with {expression}; a format specifier like :.2f controls decimal places. ⟦A.f1 A.f4 B.f2 B.f3 A:tb6 B:tb4⟧
[UP NEXT] Up next: Conditionals and For Loops: In the next tile you will write if/elif/else chains to branch on conditions and for loops to iterate over lists and other sequences.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Creating a set and removing duplicates — A before/after showing how set() collapses duplicates from a list.
(mechanism) A set is an unordered collection with no duplicate elements. Use set() to create one from a list: set(['Lagos', 'Abuja', 'Lagos', 'Kano']) gives {'Lagos', 'Abuja', 'Kano'}. Use {} for a non-empty set literal: {'Lagos', 'Abuja'}. For an empty set, you must use set() — {} creates an empty dictionary. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3⟧
[BEFORE_AFTER] Converting the list to a set removes the duplicate 'Lagos', reducing the count from 4 to 3.
  before:
[CODE python]
cities = ['Lagos', 'Abuja', 'Lagos', 'Kano']
len(cities)
  annotations: ['List — 4 items, with a duplicate', '4']
  after:
[CODE python]
cities = set(['Lagos', 'Abuja', 'Lagos', 'Kano'])
len(cities)
  annotations: ['Set — duplicate removed', '3']
### r02 · Union and intersection on sets — A side-by-side contrast showing | and & on the same two sets.
(mechanism) | (union) gives all elements from either set — no duplicates. & (intersection) gives only the elements present in both sets. If week1_cities = {'Lagos', 'Abuja'} and week2_cities = {'Abuja', 'Kano'}, then week1_cities | week2_cities is {'Lagos', 'Abuja', 'Kano'} and week1_cities & week2_cities is {'Abuja'}. ⟦A.f5 A:tb5⟧
[SIDE_BY_SIDE] | combines both sets; & keeps only what they have in common. left_label: | union — all cities from either | right_label: & intersection — only shared cities
  left:
[CODE python]
week1 = {'Lagos', 'Abuja'}
week2 = {'Abuja', 'Kano'}
week1 | week2
  annotations: ['Week 1 cities', 'Week 2 cities', "{'Lagos', 'Abuja', 'Kano'} — all cities"]
  right:
[CODE python]
week1 = {'Lagos', 'Abuja'}
week2 = {'Abuja', 'Kano'}
week1 & week2
  annotations: ['Week 1 cities', 'Week 2 cities', "{'Abuja'} — only the shared city"]
### r03 · Embedding a quote without escaping — A side-by-side contrast showing the same string with and without an escape.
(mechanism) A quote character can be embedded in a string without escaping it by enclosing the string in the other kind of quote. "This delivery wasn't late" uses double quotes, so the apostrophe in wasn't needs no backslash. Inside single quotes the same apostrophe would need escaping: 'This delivery wasn\'t late'. ⟦B.f1 B:tb1⟧
[SIDE_BY_SIDE] Switching to the other kind of quote avoids the need to escape the embedded quote character. left_label: Single quotes — escape needed | right_label: Double quotes — no escape needed
  left:
[CODE python]
'This delivery wasn\'t late'
  annotations: ['Backslash needed inside single quotes']
  right:
[CODE python]
"This delivery wasn't late"
  annotations: ['No backslash needed — double quotes wrap the string']

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: if statements around the membership test
· constraints.blocked_syntax: colon and indented block
· constraints.blocked_syntax: for item in sequence:
· constraints.blocked_syntax: [expr for x in seq if cond]
· constraints.blocked_syntax: for k, v in d.items():
· constraints.blocked_syntax: positional arguments in a call
· constraints.blocked_syntax: def f(a, b=default):
· constraints.blocked_syntax: keyword arguments f(name=value)
· constraints.blocked_syntax: from module import name
· constraints.blocked_syntax: with open(...) as f:
· constraints.blocked_syntax: += and other augmented assignment
· feedback.hints: Python lets you mix quote types: use `"..."` when the string contains `'`, and `'...'` when it contains `"`.
· constraints.blocked_syntax: colon and indented block
· constraints.blocked_syntax: for item in sequence:
· constraints.blocked_syntax: [expr for x in seq if cond]
· constraints.blocked_syntax: for k, v in d.items():
· constraints.blocked_syntax: positional arguments in a call
· constraints.blocked_syntax: def f(a, b=default):
· constraints.blocked_syntax: keyword arguments f(name=value)
· constraints.blocked_syntax: from module import name
· constraints.blocked_syntax: with open(...) as f:
· constraints.blocked_syntax: += and other augmented assignment
· expected.value: Average delivery time: 42.00 minutes
· expected.value: Average delivery time: 42.00 minutes