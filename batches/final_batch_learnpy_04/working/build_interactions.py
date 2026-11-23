import json, pathlib, tempfile, os, contextlib, io, copy, ast
B=pathlib.Path('batches/final_batch_learn_python.region.04')
plans=json.load(open(B/'tile_plans.json')); screens=json.load(open(B/'screens.json'))
bundles={b['context']['concept_id']:b for b in json.load(open(B/'inputs/path_glossary_bundle.json'))['bundles']}
assets={a['asset_id']:a for a in json.load(open(B/'scenario_asset_registry.json'))['assets']}
pin=json.load(open('00_FINAL_PIPELINE_CORE/registry/runtimes.json'))['runtimes']['python']['version']
# Each choice tuple: question, correct option, two misconceptions, and fact-grounded explanations.
Q={}
def q(tile,step,prompt,correct,w1,w2,e1,e2,hint): Q[f'learn_python.tile.{tile}.s{step:02}']=(prompt,correct,w1,w2,e1,e2,hint)
q('066_066',3,'Order is an ordinary class. Read this code. Which statement correctly distinguishes the identities?\n```python\nfirst = Order()\nsecond = Order()\nalias = first\n```','first and alias share identity; first and second are distinct instances.','All three names share identity because they use the same class.','first and alias are distinct because assigning a name creates a new instance.','Two ordinary class calls create distinct instances, even though they use one class.','Assignment here makes an alias; it is not another Order() call.','Count the class calls, then distinguish a call from an assignment.')
q('067_067',3,'An existing report must be read, without truncating it or writing to it. Which explicit mode matches this purpose?','r','w','x','w writes and truncates an existing file.','x attempts exclusive creation; it is not the reading mode.','Match the operation to the mode, not just to whether a file exists.')
q('067_067',4,'An existing report must retain its content and receive new text at the end. Which mode matches this purpose?','a','w','x','w truncates the existing file, so it does not preserve the report.','x fails when the destination already exists; it does not append.','Distinguish adding content from replacing content.')
q('068_070',2,'Which initializer stores both constructor arguments on the new Order instance?','def __init__(self, label, quantity):\n    self.label = label\n    self.quantity = quantity','def __init__(self, label, quantity):\n    label = label\n    quantity = quantity','def __init__(self, label, quantity):\n    self.label = quantity\n    self.quantity = label','Assigning parameter names alone does not store the values as instance attributes.','The attributes receive the wrong arguments: label and quantity are swapped.','Follow each constructor argument to its matching self attribute.')
q('068_070',3,'What is the purpose of __init__ when Order is instantiated?','Initialize the already-created instance, not return a replacement object.','Return a different object to replace the new instance.','Create the class object each time an instance is requested.','__init__ initializes the created instance rather than returning a replacement.','The class definition creates the class object; __init__ initializes an instance.','Distinguish the class, the new instance, and initializing that instance.')
q('068_070',6,'Which method increases the receiving Order instance\'s quantity by amount?','def add(self, amount):\n    self.quantity = self.quantity + amount','def add(self, amount):\n    quantity = amount','def add(self, amount):\n    self.quantity = amount','A local quantity name does not reassign the receiving instance\'s self.quantity.','This replaces quantity with amount rather than increasing the current quantity.','Check both which object is updated and whether its old state is used.')
q('068_070',7,'For def add(self, amount), what arguments does order.add(2) supply?','order implicitly as self, and 2 explicitly as amount.','2 as self, with no amount argument.','No implicit argument; callers must write order.add(order, 2).','The method receives its target instance implicitly, so 2 is the next argument.','An instance-method call supplies order implicitly; passing it again is not required.','Separate the object before the dot from the value inside the parentheses.')
q('068_070',10,'Choose the binding pair: add updates one order\'s state; from_text constructs an Order through cls from a string.','add: instance method; from_text: class method.','add: static method; from_text: instance method.','add: class method; from_text: static method.','The update needs the receiving instance; construction through cls needs an implicit class.','A class method receives a class, not that order\'s state; a static method receives no implicit cls.','For each operation, ask whether it needs an implicit instance or class.')
q('068_070',11,'A cost(quantity) operation needs only its explicit quantity argument, with no implicit instance or class. Which definition matches?','@staticmethod above def cost(quantity):','@classmethod above def cost(cls, quantity):','An ordinary instance method def cost(self, quantity):','A class method receives cls implicitly, contrary to the stated requirement.','An ordinary instance method receives self implicitly, contrary to the stated requirement.','Consider which decorator removes both kinds of implicit argument.')
q('071_073',2,'Report receives a calculator collaborator. Which implementation stores that object and delegates cost(quantity) to it, without inheritance?','Store self.calculator = calculator; total returns self.calculator.cost(quantity).','Store self.calculator = calculator.cost(3); total returns self.calculator.','Ignore calculator; total returns quantity * 4.','This stores one computed result, not the collaborator object, and does not delegate each operation.','This performs the calculation inside Report rather than delegating to its contained collaborator.','Look for both a stored object and a method call on that object.')
q('071_073',5,'What does the name order._quantity communicate in Python?','It conventionally marks supporting state as non-public, but does not enforce access protection.','It makes the attribute inaccessible from outside Order.','It promises callers that the attribute is the public interface.','A leading underscore is a convention, not an enforced access restriction.','The underscore convention signals internal implementation use rather than the client interface.','Separate a naming convention from an access restriction.')
q('071_073',9,'Order.__init__(quantity) stores quantity. FeeOrder.__init__(quantity, fee) must preserve that initialization before storing fee. Which sequence matches?','super().__init__(quantity), then self.fee = fee.','self.fee = fee only.','super().format(), then self.fee = fee.','Adding fee alone does not run the inherited quantity initializer.','Delegating formatting is not delegating initialization; use the inherited initializer.','Choose the inherited operation appropriate to construction, not display.')
q('074_074',2,'check_quantity raises InvalidRecordError. Which placement handles that custom failure at the caller\'s recovery boundary?','A try around the validator call, followed by except InvalidRecordError:.','An except FileExistsError: around the validator call.','Define InvalidRecordError but call the validator without a surrounding handler.','The raised custom failure needs its matching handler; FileExistsError is a different failure type.','Defining the type does not itself handle a failure raised by the validator.','Distinguish defining, raising, and handling an exception.')
q('075_075',3,'Order has labels = [] in its class body. Updates to first.labels also appear in second.labels. Which repair gives each instance its own list?','Move list creation into __init__ as self.labels = [].','Leave labels = [] in the class body and append through first.labels.','Create the list in the class body a second time under the same name.','Appending through an instance still mutates the shared list unless an instance attribute shadows it.','A class-body list remains shared; redefining it there does not make per-instance lists.','Consider when a fresh list must be created for each object.')
q('076_076',3,'A supported record contains a tuple nested under quantities. After json.dumps followed by json.loads, which container type does that tuple become?','A Python list.','A Python tuple.','A string containing Python tuple syntax.','Tuples encode as JSON arrays, which decode as lists, not tuples.','The supported tuple encodes as an array rather than a Python-syntax string.','Trace the conversion through a JSON array back into Python.')
q('076_076',4,'A supported Python dictionary has a non-string numeric key. Which round-trip expectation is safe?','Do not assume the key retains its Python type: JSON object keys are strings.','The key must retain its numeric Python type.','The key is dropped because JSON object keys cannot be strings.','JSON object keys are strings, so numeric key types need not survive the round trip.','JSON object keys are strings; the stated reason for dropping it reverses that fact.','Think about the key type JSON objects represent, not the original Python key.')
q('077_077',2,'An Order has no missing attribute. Which expression retrieves it with a None fallback if it is absent?','getattr(order, "missing", None)','getattr(order, "missing")','getattr(order, "quantity", None)','Without the optional fallback, this expression does not request None for an absent attribute.','This retrieves quantity, not the named missing attribute.','Check both the requested attribute name and the fallback argument.')
q('078_078',3,'source.rename(target) encounters an existing target file. Which statement preserves the taught platform distinction?','Unix may silently replace it when permitted; Windows raises FileExistsError.','Both platforms always raise FileExistsError.','Both platforms always append the source content to the target.','Unix can replace an existing target when permitted, so universal failure is not guaranteed.','rename moves or renames an entry; the stated existing-target behaviors are replacement or failure, not append.','Avoid a platform-independent promise for an existing target.')
q('079_079',3,'Order defines __repr__ but has no __str__ implementation. What does the default str representation use?','The __repr__ result.','It has no representation until __str__ is implemented.','It always ignores __repr__ and uses the quantity attribute alone.','The default representation falls back to __repr__ when __str__ is absent.','The fallback uses __repr__, not an automatic rendering of quantity.','Compare the missing user-facing method with the available inspection method.')
q('080_083',2,'Reading an existing file with a selected text encoding raises UnicodeDecodeError. Which diagnosis is supported?','The content could not be decoded; its bytes may be invalid for the selected encoding.','The failure proves the file does not exist.','The failure proves opening with w will safely preserve the original text.','UnicodeDecodeError is a decoding failure, not evidence of a missing file.','A decoding failure does not establish a safe rewrite; matching the bytes and encoding is required for correct decoding.','Identify the failure\'s cause before choosing a response.')
q('080_083',6,'Choose the response plan for a CSV importer that must handle source, decoding, parser, and row-shape problems separately.','Use specific FileNotFoundError, UnicodeDecodeError and csv.Error handlers, plus explicit required-field and excess-field validation.','Catch csv.Error only; missing fields and missing files necessarily raise it.','Catch FileNotFoundError only; decoding failures and invalid row shapes necessarily raise it.','csv.Error reports parser-detected errors; missing sources and decoding failures are separate, and row lengths need explicit validation.','FileNotFoundError concerns missing sources, not decoding or row validation failures.','Separate failures reported by exceptions from problems visible in row fields.')
q('080_083',10,'After a general context manager enters successfully, its body raises an exception. Which sequence and exception claim are supported?','Entry occurred before the body; exit runs afterward and may suppress the exception.','Entry occurs after the body; exit is skipped when the body raises.','Entry occurred before the body; exit always forces every exception to propagate.','Entry precedes the body, and after successful entry, exit runs even when the body raises.','A general context manager may suppress an exception; propagation is not guaranteed for every manager.','Separate the entry/exit order from whether a manager suppresses an exception.')
q('080_083',11,'In with open(path) as source:, entry succeeds and the body raises ValueError. An outer handler catches it. What is the file\'s state after leaving the with body?','source is closed.','source stays open because the body raised.','source closes only if the body called source.close().','Leaving the managed file body closes the file on exceptional exit too.','Managed opening supplies file closure when leaving the body; an explicit close in the body is not required.','Follow the resource lifetime across the body boundary.')
q('080_083',15,'copy.bin already exists and is a disposable destination. What does opening it with wb do?','Opens for bytes writing and truncates existing contents.','Appends bytes while preserving all existing contents.','Fails exclusively because the destination already exists.','wb truncates an existing destination; it is not append mode.','wb creates or truncates the destination; exclusive creation is a different mode.','Check the write mode before deciding whether existing contents survive.')

# Runnable host fixtures are unchanged scaffolding. They recreate local registered fixtures for each test,
# run just the learner region, and inspect its real objects/files/output with different inputs.
EX={}
def ex(cid,prompt,starter,solution,defaults,cases,probe,setup=''):
 EX['python.'+cid]=dict(prompt=prompt,starter=starter,solution=solution,defaults=defaults,cases=cases,probe=probe,setup=setup)
ex('classes_and_instances','Define an empty Order class with an indented pass body. Assign first and second through separate Order() calls, then print(first is second). Keep the supplied test scaffolding unchanged; it probes identity against each of those two names.', '# Define Order, first and second, then print their identity comparison.\n', 'class Order:\n    pass\nfirst = Order()\nsecond = Order()\nprint(first is second)\n', {'reference':'first'}, [{'reference':'first'},{'reference':'second'}], '[ns["first"] is ns[inputs["reference"]], type(ns["first"]) is ns["Order"], type(ns["second"]) is ns["Order"], captured.getvalue().strip(), empty_class_probe(code)]')
ex('file_modes','Use the supplied path and report_text to exclusively create report.txt, write report_text, and close the file. Catch FileExistsError, print exactly "Destination exists", and leave an existing report unchanged. Do not fall back to any other writing mode. Tests recreate absent and existing destinations with different content.', '# Complete exclusive creation and its matching handler.\n', 'try:\n    file = open(path, "x")\n    file.write(report_text)\n    file.close()\nexcept FileExistsError:\n    print("Destination exists")\n', {'path':'report.txt','report_text':'First','existing':None}, [{'path':'report.txt','report_text':'First','existing':None},{'path':'report.txt','report_text':'First','existing':'First'},{'path':'report.txt','report_text':'Second','existing':None},{'path':'report.txt','report_text':'Second','existing':'Keep'}], '[pathlib.Path(inputs["path"]).read_text(), captured.getvalue().strip(), ns["file"].closed if "file" in ns else True]', 'p = pathlib.Path(inputs["path"])\n    if p.exists(): p.unlink()\n    if inputs["existing"] is not None: p.write_text(inputs["existing"])')
ex('instance_initialization','Complete Order.__init__(self, label, quantity) by storing both supplied values in self.label and self.quantity. Keep the scaffold construction and display: order = Order(label, quantity) and print(order.label, order.quantity). The initial inputs are notebook and 3; tests also use different inputs.', 'class Order:\n    def __init__(self, label, quantity):\n        pass\norder = Order(label, quantity)\nprint(order.label, order.quantity)\n', 'class Order:\n    def __init__(self, label, quantity):\n        self.label = label\n        self.quantity = quantity\norder = Order(label, quantity)\nprint(order.label, order.quantity)\n', {'label':'notebook','quantity':3}, [{'label':'notebook','quantity':3},{'label':'blue','quantity':2}], '[ns["order"].label, ns["order"].quantity, captured.getvalue().strip()]')
ex('instance_methods','Add add(self, amount) to Order. Increase the receiving instance\'s self.quantity by amount and assign it back. Preserve the supplied initializer and calls. With quantity 3 and amount 2 the final order.quantity must be 5; tests vary both inputs.', 'class Order:\n    def __init__(self, quantity):\n        self.quantity = quantity\n    # Add the instance method here.\norder = Order(quantity)\norder.add(amount)\nprint(order.quantity)\n', 'class Order:\n    def __init__(self, quantity):\n        self.quantity = quantity\n    def add(self, amount):\n        self.quantity = self.quantity + amount\norder = Order(quantity)\norder.add(amount)\nprint(order.quantity)\n', {'quantity':3,'amount':2}, [{'quantity':3,'amount':2},{'quantity':2,'amount':4}], '[ns["order"].quantity, captured.getvalue().strip()]')
ex('class_and_static_methods','Implement Order.from_text with @classmethod above def from_text(cls, text): and return cls(int(text)). Preserve the initializer and scaffold call. The supplied text is "3"; order.quantity must be the integer conversion of text, not a constant. Tests use two text values.', 'class Order:\n    def __init__(self, quantity):\n        self.quantity = quantity\n    # Add the alternative constructor.\norder = Order.from_text(text)\nprint(order.quantity)\n', 'class Order:\n    def __init__(self, quantity):\n        self.quantity = quantity\n    @classmethod\n    def from_text(cls, text):\n        return cls(int(text))\norder = Order.from_text(text)\nprint(order.quantity)\n', {'text':'3'}, [{'text':'3'},{'text':'12'}], '[type(ns["order"]) is ns["Order"], type(ns["order"].quantity).__name__, ns["order"].quantity, captured.getvalue().strip()]')
formatter='class Formatter:\n    def format(self, quantity):\n        return f"Total: {quantity * 4}"\n'
ex('composition','Complete Report so its initializer stores the supplied formatter as self.formatter, and total(quantity) returns self.formatter.format(quantity). Keep Formatter\'s calculation unchanged; Report must only delegate. With the supplied quantity 3, report.total(quantity) must return "Total: 12". Tests inspect the stored collaborator and vary quantity.',formatter+'class Report:\n    def __init__(self, formatter):\n        pass\n    def total(self, quantity):\n        pass\nformatter = Formatter()\nreport = Report(formatter)\nresult = report.total(quantity)\nprint(result)\n',formatter+'class Report:\n    def __init__(self, formatter):\n        self.formatter = formatter\n    def total(self, quantity):\n        return self.formatter.format(quantity)\nformatter = Formatter()\nreport = Report(formatter)\nresult = report.total(quantity)\nprint(result)\n', {'quantity':3}, [{'quantity':3},{'quantity':2}], '[ns["report"].formatter is ns["formatter"], ns["result"], captured.getvalue().strip()]')
ex('encapsulation_conventions','Rename supporting state consistently to self._quantity. Complete public add(self, amount) to increase and return that state. The caller must use order.add(amount), without managing _quantity directly. Preserve the scaffold call and display; inputs 3 and 2 must return 5.', 'class Order:\n    def __init__(self, quantity):\n        self.quantity = quantity\n    def add(self, amount):\n        pass\norder = Order(quantity)\nresult = order.add(amount)\nprint(result)\n', 'class Order:\n    def __init__(self, quantity):\n        self._quantity = quantity\n    def add(self, amount):\n        self._quantity = self._quantity + amount\n        return self._quantity\norder = Order(quantity)\nresult = order.add(amount)\nprint(result)\n', {'quantity':3,'amount':2}, [{'quantity':3,'amount':2},{'quantity':2,'amount':4}], '[ns["order"]._quantity, ns["result"], "quantity" in vars(ns["order"]), captured.getvalue().strip()]')
base='class Order:\n    def __init__(self, quantity):\n        self.quantity = quantity\n    def format(self):\n        return f"Quantity: {self.quantity}"\n'
ex('inheritance_and_super','Keep Order unchanged. Define FeeOrder(Order). Its __init__(self, quantity, fee) must call super().__init__(quantity) before storing self.fee. Override format(self) to extend super().format() with f", fee: {self.fee}". Preserve construction and display. For quantity 3 and fee 2 the output is "Quantity: 3, fee: 2"; tests vary both fields.',base+'# Add FeeOrder here.\norder = FeeOrder(quantity, fee)\nprint(order.format())\n',base+'class FeeOrder(Order):\n    def __init__(self, quantity, fee):\n        super().__init__(quantity)\n        self.fee = fee\n    def format(self):\n        return super().format() + f", fee: {self.fee}"\norder = FeeOrder(quantity, fee)\nprint(order.format())\n',{'quantity':3,'fee':2},[{'quantity':3,'fee':2},{'quantity':2,'fee':4}], '[ns["order"].quantity, ns["order"].fee, ns["order"].format(), captured.getvalue().strip()]')
ex('custom_exceptions','Define InvalidRecordError(Exception) with pass. Complete check_quantity(quantity): return nonnegative quantity unchanged; raise InvalidRecordError("negative quantity") for a negative value. Complete the supplied caller boundary: catch InvalidRecordError and print exactly "Order rejected". On success print the returned quantity. Tests exercise nonnegative and negative inputs.', '# Define the custom exception.\ndef check_quantity(quantity):\n    pass\n# Add the caller boundary.\n', 'class InvalidRecordError(Exception):\n    pass\ndef check_quantity(quantity):\n    if quantity < 0:\n        raise InvalidRecordError("negative quantity")\n    return quantity\ntry:\n    result = check_quantity(quantity)\n    print(result)\nexcept InvalidRecordError:\n    print("Order rejected")\n', {'quantity':2}, [{'quantity':2},{'quantity':0},{'quantity':-1},{'quantity':-3}], '[captured.getvalue().strip(), validation_probe(ns, inputs["quantity"])]')
ex('instance_vs_class_attributes','Repair the shared list: remove labels = [] from the class body and create self.labels = [] in __init__(self). Keep the supplied constructions, append call, and two print calls unchanged. After appending the supplied label (initially "blue"), first.labels must contain only that label, while second.labels remains empty. Tests vary the appended label.', 'class Order:\n    labels = []\nfirst = Order()\nsecond = Order()\nfirst.labels.append(label)\nprint(first.labels)\nprint(second.labels)\n', 'class Order:\n    def __init__(self):\n        self.labels = []\nfirst = Order()\nsecond = Order()\nfirst.labels.append(label)\nprint(first.labels)\nprint(second.labels)\n', {'label':'blue'}, [{'label':'blue'},{'label':'notebook'}], '[ns["first"].labels, ns["second"].labels, ns["first"].labels is ns["second"].labels, "labels" in ns["Order"].__dict__, captured.getvalue().strip()]')
ex('json_serialization','Use json.dumps(record) to assign text and json.loads(text) to assign restored. Print restored["quantities"] == [[3, 2]] and restored["active"] == True. For the initial record both comparisons should be True. Do not hard-code the reconstructed values: tests vary the supported record and inspect text and restored as well.', '# Assign text and restored, then print the two comparisons.\n', 'text = json.dumps(record)\nrestored = json.loads(text)\nprint(restored["quantities"] == [[3, 2]])\nprint(restored["active"] == True)\n', {'record':{'quantities':[[3,2]],'active':True}}, [{'record':{'quantities':[[3,2]],'active':True}},{'record':{'quantities':[[2,4]],'active':False}}], '[ns["text"], ns["restored"], captured.getvalue().strip()]', 'inputs = dict(inputs)\n    inputs["record"] = {"quantities": [tuple(pair) for pair in inputs["record"]["quantities"]], "active": inputs["record"]["active"]}\n    return inputs')
intro='class Order:\n    def __init__(self):\n        self.quantity = 3\ndef make_order():\n    return Order()\norder = make_order()\n'
ex('object_introspection','Keep the supplied Order and make_order definitions and the order binding. Assign object_type = type(order), membership = isinstance(order, Order), public_names = [name for name in dir(order) if not name.startswith("_")], quantity = getattr(order, "quantity"), and missing = getattr(order, "missing", None). Add a comment that dir is not guaranteed complete and underscore names conventionally signal internal use. Tests also inspect a fixture subclass; treat filtered names as candidates, not a guaranteed complete public interface.', '# Add the inspection assignments and a comment about discovery limits.\n', 'object_type = type(order)\nmembership = isinstance(order, Order)\npublic_names = [name for name in dir(order) if not name.startswith("_")]\nquantity = getattr(order, "quantity")\nmissing = getattr(order, "missing", None)\n# dir is not guaranteed complete; underscore names conventionally signal internal use.\n', {'quantity':3,'subclass':False}, [{'quantity':3,'subclass':False},{'quantity':2,'subclass':True}], '[ns["object_type"].__name__, ns["membership"], ns["public_names"], ns["quantity"], ns["missing"]]', 'order = InspectionOrder() if inputs["subclass"] else Order()\n    order.quantity = inputs["quantity"]\n    return {"order":order}')
ex('pathlib_filesystem_operations','Use the supplied directory, source and filename. Create directory and missing parents with parents=True, exist_ok=True; assign target = directory / filename and move source with source.rename(target). Inspect immediate entries with a for loop over directory.iterdir(), printing each entry, with no ordering assumption. Fixtures guarantee the destination is absent and supply the source report; do not generate its content.', '# Create directory, construct target, move source, then inspect immediate entries.\n', 'directory.mkdir(parents=True, exist_ok=True)\ntarget = directory / filename\nsource.rename(target)\nfor entry in directory.iterdir():\n    print(entry)\n', {'content':assets['ws.pathlib_filesystem_operations']['files'][1]['content']}, [{'content':assets['ws.pathlib_filesystem_operations']['files'][1]['content']},{'content':assets['ws.pathlib_filesystem_operations']['files'][1]['content']+'_updated'}], '[ns["target"].read_text(), ns["directory"].is_dir(), ns["source"].exists(), sorted(str(p) for p in ns["directory"].iterdir()), sorted(captured.getvalue().splitlines())]', 'shutil.rmtree("incoming", ignore_errors=True)\n    shutil.rmtree("output", ignore_errors=True)\n    pathlib.Path("incoming").mkdir()\n    pathlib.Path("incoming/report.txt").write_text(inputs["content"])\n    return {"directory":pathlib.Path("output/reports"), "source":pathlib.Path("incoming/report.txt"), "filename":"report.txt"}')
base_special='class Order:\n    def __init__(self, quantity):\n        self.quantity = quantity\n'
ex('special_methods','Implement __repr__ returning f"Order(quantity={self.quantity})" and __str__ returning f"Quantity: {self.quantity}". Preserve the supplied order construction and both display calls. Tests inspect repr, str and printed output for two quantities and use host scaffolding to remove __str__ temporarily to verify the __repr__ fallback.',base_special+'    # Add both representation methods.\norder = Order(quantity)\nprint(repr(order))\nprint(order)\n',base_special+'    def __repr__(self):\n        return f"Order(quantity={self.quantity})"\n    def __str__(self):\n        return f"Quantity: {self.quantity}"\norder = Order(quantity)\nprint(repr(order))\nprint(order)\n', {'quantity':3}, [{'quantity':3},{'quantity':2}], 'representation_probe(ns, captured)')
label=next(f['content'] for f in assets['ws.text_file_encodings']['files'] if f['path']=='label.txt')
ex('text_file_encodings','Read the supplied UTF-8 label.txt into text and rewrite the same text to label.txt. Add explicit encoding="utf-8" to both open calls. Keep the read, write, close, and print sequence unchanged: close source before opening destination, and close destination afterward. Tests recreate the local text fixture with different Unicode text and inspect the preserved UTF-8 bytes.', 'source = open("label.txt", "r")\ntext = source.read()\nsource.close()\ndestination = open("label.txt", "w")\ndestination.write(text)\ndestination.close()\nprint(text)\n', 'source = open("label.txt", "r", encoding="utf-8")\ntext = source.read()\nsource.close()\ndestination = open("label.txt", "w", encoding="utf-8")\ndestination.write(text)\ndestination.close()\nprint(text)\n', {'content':label}, [{'content':label},{'content':label+' notebook'}], '[ns["text"], list(pathlib.Path("label.txt").read_bytes()), ns["source"].closed, ns["destination"].closed, ns["source"].encoding, ns["destination"].encoding, captured.getvalue().strip()]', 'pathlib.Path("label.txt").write_bytes(inputs["content"].encode("utf-8"))')
file_starter=assets['ws.file_and_format_errors']['files'][0]['content']
file_solution='''import csv

def import_rows(path):
    file = None
    rows = []
    try:
        file = open(path, mode="r", encoding="utf-8", newline="")
        reader = csv.DictReader(file)
        for row in reader:
            if "label" not in row or "quantity" not in row or row["label"] is None or row["quantity"] is None or row["label"] == "" or row["quantity"] == "" or None in row:
                return "Invalid row"
            else:
                rows.append(row)
        return rows
    except FileNotFoundError:
        return "Missing source"
    except UnicodeDecodeError:
        return "Decoding failed"
    except csv.Error:
        return "Parsing failed"
    finally:
        if file is not None:
            file.close()
'''
fixture_files={f['path']:f['content'] for f in assets['ws.file_and_format_errors']['files'] if f['path'].endswith('.csv')}
file_cases=[{'path':n,'content':v,'parser_failure':False,'invalid_bytes':False} for n,v in fixture_files.items()]
file_cases += [{'path':'nonexistent.csv','content':None,'parser_failure':False,'invalid_bytes':False},{'path':'invalid_utf8.csv','content':None,'parser_failure':False,'invalid_bytes':True},{'path':'valid.csv','content':fixture_files['valid.csv'],'parser_failure':True,'invalid_bytes':False}]
ex('file_and_format_errors','Complete import_rows(path) using its existing UTF-8 DictReader scaffold and finally cleanup. Return valid rows as a list of dictionaries. Reject any row with a missing or empty label or quantity, or any excess fields under the None key: return exactly "Invalid row". Return exactly "Missing source", "Decoding failed", or "Parsing failed" from the matching FileNotFoundError, UnicodeDecodeError, or csv.Error handler. Tests supply valid, missing-field, empty-field and excess-field CSVs, a missing source, invalid UTF-8 bytes, and a host-injected parser-reported csv.Error. Wrong row widths alone are not a parser-exception test.', file_starter,file_solution,file_cases[0],file_cases,'import_probe(ns, inputs)', 'p = pathlib.Path(inputs["path"])\n    if p.exists(): p.unlink()\n    if inputs["content"] is not None: p.write_text(inputs["content"], encoding="utf-8")\n    if inputs["invalid_bytes"]: p.write_bytes(b"label,quantity\\nnotebook,\\xff\\n")')
with_solution='''with open("label.txt", "r", encoding="utf-8") as source:
    text = source.read()
normal_closed = source.closed
print(source.closed)
try:
    with open("label.txt", "r", encoding="utf-8") as source:
        text = source.read()
        raise ValueError("Processing failed")
except ValueError:
    print("Processing failed")
exceptional_closed = source.closed
print(source.closed)
'''
ex('with_resource_management','Implement two managed reads of the supplied UTF-8 label.txt. First, assign source.read() to text inside with open("label.txt", "r", encoding="utf-8") as source:, then assign normal_closed = source.closed and print(source.closed) after the block. Second, inside a try, use the same managed read and deliberately raise ValueError("Processing failed") in its body. Catch ValueError outside the with body and print "Processing failed". After the handler assign exceptional_closed = source.closed and print(source.closed). Keep both reads managed; do not call close explicitly. Tests inspect text and both closure states.', '# Complete the normal and exceptional managed reads.\n', with_solution, {'content':label}, [{'content':label},{'content':label+' notebook'}], '[ns["text"], ns["normal_closed"], ns["exceptional_closed"], captured.getvalue().strip()]', 'pathlib.Path("label.txt").write_bytes(inputs["content"].encode("utf-8"))')
payload=next(f['content'] for f in assets['ws.binary_files']['files'] if f['path']=='source.bin')
ex('binary_files','Copy the supplied source.bin into the disposable copy.bin. Use nested with open("source.bin", "rb") as source: and with open("copy.bin", "wb") as destination:. Assign payload = source.read() and pass payload directly to destination.write(payload), without decoding. Both managed streams must be closed afterward and source.bin unchanged. Tests recreate different source bytes and an existing disposable destination.', '# Copy the binary payload with nested managed blocks.\n', 'with open("source.bin", "rb") as source:\n    with open("copy.bin", "wb") as destination:\n        payload = source.read()\n        destination.write(payload)\n', {'content':payload}, [{'content':payload},{'content':payload[::-1]}], '[list(pathlib.Path("source.bin").read_bytes()), list(pathlib.Path("copy.bin").read_bytes()), ns["source"].closed, ns["destination"].closed, type(ns["payload"]).__name__]', 'pathlib.Path("source.bin").write_bytes(inputs["content"].encode("utf-8"))\n    pathlib.Path("copy.bin").write_text("Disposable destination")')

# Shared authored host fixture functions. These unchanged top-level statements are not learner syntax.
HOST='''import pathlib
import shutil
import contextlib
import io
import json
import csv
import builtins
import ast

def empty_class_probe(code):
    tree = ast.parse(code)
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Order")
    return len(cls.body) == 1 and isinstance(cls.body[0], ast.Pass)

def validation_probe(ns, quantity):
    try:
        value = ns["check_quantity"](quantity)
        return ["returned", value]
    except ns["InvalidRecordError"] as error:
        return [type(error).__name__, str(error)]

def representation_probe(ns, captured):
    obj = ns["order"]
    result = [repr(obj), str(obj), captured.getvalue().strip()]
    method = ns["Order"].__dict__.get("__str__")
    if method is not None:
        delattr(ns["Order"], "__str__")
    result.append(str(obj))
    if method is not None:
        setattr(ns["Order"], "__str__", method)
    return result

def import_probe(ns, inputs):
    original = csv.DictReader
    opened = []
    def tracked_open(*args, **kwargs):
        f = builtins.open(*args, **kwargs)
        opened.append(f)
        return f
    def parser_failure(file):
        raise csv.Error("Parser-reported failure")
    ns["open"] = tracked_open
    try:
        if inputs["parser_failure"]:
            csv.DictReader = parser_failure
        result = ns["import_rows"](inputs["path"])
        return [result, all(f.closed for f in opened)]
    finally:
        csv.DictReader = original
'''
INTRO_HOST=intro+'class InspectionOrder(Order):\n    pass\n'

def build_code(e,cid):
 setup=e['setup'] or 'return inputs'
 if 'return ' not in setup:setup+='\n    return inputs'
 # Setup and probes are supplied host-side fixtures, present verbatim in starter and solution.
 host_tree=ast.parse(HOST)
 wanted={'python.classes_and_instances':'empty_class_probe', 'python.custom_exceptions':'validation_probe', 'python.special_methods':'representation_probe', 'python.file_and_format_errors':'import_probe'}.get(cid)
 host=''.join(ast.get_source_segment(HOST,n)+'\n\n' for n in host_tree.body if isinstance(n,(ast.Import,ast.ImportFrom)) or isinstance(n,ast.FunctionDef) and n.name==wanted)
 head=host+(INTRO_HOST if cid=='python.object_introspection' else '')+'\ndef prepare_case(inputs):\n    '+setup+'\n'
 head+='\ndef check_case(inputs):\n    prepared = prepare_case(inputs)\n    ns = dict(globals())\n    ns.update(inputs)\n    ns.update(prepared or {})\n    source_code = pathlib.Path("main.py").read_text(encoding="utf-8")\n    code = source_code.split("# BEGIN " + "LEARNER\\n", 1)[1].split("# END " + "LEARNER", 1)[0]\n    captured = io.StringIO()\n    with contextlib.redirect_stdout(captured):\n        exec(code, ns)\n    return '+e['probe']+'\n'
 # Host fixture definitions are immutable scaffold data executed before the learner region.
 head='# Supplied host fixtures: leave this immutable setup unchanged.\nexec('+repr(head)+')\n'
 # Inputs supplied outside the editable region. Literal data are copied from assets or authored scenario inputs.
 head+='\ninputs = '+repr(e['defaults'])+'\nglobals().update(inputs)\nglobals().update(prepare_case(inputs) or {})\n'
 return head+'\n# BEGIN LEARNER\n'+e['starter']+'# END LEARNER\n', head+'\n# BEGIN LEARNER\n'+e['solution']+'# END LEARNER\n'

out={k:plans[k] for k in ['schema_version','path_id','batch_id']};out['kind']='interactions_part';out['tiles']=[]
for t,sc in zip(plans['tiles'],screens['tiles']):
 its=[];seen=set();steps=[s for s in t['steps'] if s['type'] in ['check','hands_on']]
 for pos,s in enumerate(steps):
  cid=s['concept_ids'][0];b=bundles[cid]
  measures=[]
  for anchor in s['anchors']:
   if '#assessment:' in anchor:
    cap=anchor.split('#assessment:')[1];a=next(a for a in b['assessment_anchors'] if a['capability']==cap)
    measures.append({'concept_id':cid,'capability':cap,'fact_ids':a['fact_ids']})
  if not measures:
   chosen={'python.instance_initialization':[0], 'python.instance_methods':[0,1], 'python.class_and_static_methods':[1], 'python.composition':[0], 'python.with_resource_management':[0,2]}[cid]
   measures=[{'concept_id':cid,'capability':b['assessment_anchors'][j]['capability'],'fact_ids':b['assessment_anchors'][j]['fact_ids']} for j in chosen]
  feedback={'correct':{'message':'Correct. Your response matches the stated operation and the taught behavior.'},'incorrect':{'message':'Recheck the operation and trace which object, value, or resource each line affects.'},'hints':['Trace the supplied inputs through the operation before choosing or editing.']}
  if cid not in seen:
   rem=next((r for r in sc.get('remediation_steps',[]) if cid in r['concept_ids']),None)
   if rem:feedback['remediation_step_id']=rem['step_id']
  seen.add(cid)
  ix={'type':s['planned_interaction_type'],'interaction_id':'ix.'+s['step_id'],'difficulty': 'intro' if pos==0 else ('stretch' if pos==len(steps)-1 else 'core'),'grading_mode':'client','standalone':True,'measures':measures,'anchors':s['anchors'],'feedback':feedback}
  if ix['type']=='choice':
   prompt,correct,w1,w2,e1,e2,hint=Q[s['step_id']]
   # Keys come from the authored correct-role option; positions rotate deterministically.
   opts=[{'text':correct,'correct':True,'why':'This matches the stated task and the taught behavior.'},{'text':w1,'correct':False,'why':e1},{'text':w2,'correct':False,'why':e2}]
   rot=pos%3;opts=opts[rot:]+opts[:rot]
   options=[{'option_id':f'o{j+1}','text':o['text']} for j,o in enumerate(opts)]
   ix['public']={'prompt':prompt,'options':options,'selection':'single','shuffle':True}
   ix['grading']={'correct_option_ids':[options[j]['option_id'] for j,o in enumerate(opts) if o['correct']], 'option_feedback':{options[j]['option_id']:{'message':o['why']} for j,o in enumerate(opts)}}
   feedback['hints']=[hint];feedback['correct']['message']=correct
  else:
   e=EX[cid];starter,solution=build_code(e,cid)
   ix['standalone']=False
   ix['public']={'prompt':e['prompt'],'runtime':{'kind':'python','version':pin,'packages':[]},'workspace':{'entry':'main.py','files':[{'path':'main.py','role':'editable','language':'python','content':starter}],'asset_mounts':[]},'constraints':{k:b['practice_anchor']['live_code'][k] for k in ['allowed_syntax','blocked_syntax']}}
   # Execute, including fixture recreation, to derive all JSON expected values. Never type output keys.
   tests=[]
   with tempfile.TemporaryDirectory(dir=B/'working') as temp:
    old=os.getcwd();os.chdir(temp)
    try:
     pathlib.Path('main.py').write_text(solution)
     ns={}
     with contextlib.redirect_stdout(io.StringIO()): exec(solution,ns)
     for j,case in enumerate(e['cases']):
      result=ns['check_case'](copy.deepcopy(case))
      # Normalize Python tuples through JSON exactly as the player runner does.
      expected=json.loads(json.dumps(result,ensure_ascii=False))
      tests.append({'test_id':f't{j+1}','kind':'function_call','spec':{'function':'check_case','args':[case],'expected':expected},'visible':True,'message_on_fail':'The result does not match this fixture. Trace the supplied inputs and the required state, output, and cleanup.'})
    finally:os.chdir(old)
   ix['grading']={'solution_files':[{'path':'main.py','content':solution}],'tests':tests}
   feedback['correct']['message']='The completed code meets the task on the supplied fixtures, including the changed inputs.'
   feedback['hints']=['Follow the input names rather than substituting a fixed answer.','Check the required operation and where its result or resource state is observed.']
  its.append({'step_id':s['step_id'],'interaction':ix})
 out['tiles'].append({'tile_id':t['tile_id'],'interactions':its})
(B/'interactions.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('Wrote',len(out['tiles']),'tiles',sum(len(t['interactions']) for t in out['tiles']),'interactions')
