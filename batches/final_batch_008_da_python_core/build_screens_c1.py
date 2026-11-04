"""Build screens.part.c1.json for tile_python_operators_conversion,
tile_python_lists_dicts_tuples, tile_python_sets_strings."""
import json, pathlib

OUT = pathlib.Path("batches/final_batch_008_da_python_core/screens.part.c1.json")

# ── helpers ──────────────────────────────────────────────────────────────────

def prose(bid, role, text, concept_ids, fact_ids, tb_ids, anchors=None):
    return {
        "type": "prose",
        "block_id": bid,
        "role": role,
        "text": text,
        "lineage": {
            "concept_ids": concept_ids,
            "fact_ids": fact_ids,
            "teaching_block_ids": tb_ids,
            "anchors": anchors or []
        }
    }

def code_walk(bid, language, code, annotations, reveal="all"):
    return {
        "type": "code_walkthrough",
        "block_id": bid,
        "language": language,
        "code": code,
        "annotations": annotations,
        "reveal": reveal
    }

def side_by_side(bid, left, right, left_label, right_label, takeaway, concept_ids, fact_ids, tb_ids, anchors=None):
    return {
        "type": "side_by_side",
        "block_id": bid,
        "left": left,
        "right": right,
        "left_label": left_label,
        "right_label": right_label,
        "takeaway": takeaway,
        "lineage": {
            "concept_ids": concept_ids,
            "fact_ids": fact_ids,
            "teaching_block_ids": tb_ids,
            "anchors": anchors or []
        }
    }

def before_after(bid, before, after, change_summary, concept_ids, fact_ids, tb_ids, anchors=None):
    return {
        "type": "before_after",
        "block_id": bid,
        "before": before,
        "after": after,
        "change_summary": change_summary,
        "lineage": {
            "concept_ids": concept_ids,
            "fact_ids": fact_ids,
            "teaching_block_ids": tb_ids,
            "anchors": anchors or []
        }
    }

def diagram(bid, diagram_kind, title, nodes, edges, alt_text, concept_ids, fact_ids, tb_ids, anchors=None):
    d = {
        "type": "diagram",
        "block_id": bid,
        "diagram_kind": diagram_kind,
        "title": title,
        "nodes": nodes,
        "alt_text": alt_text,
        "lineage": {
            "concept_ids": concept_ids,
            "fact_ids": fact_ids,
            "teaching_block_ids": tb_ids,
            "anchors": anchors or []
        }
    }
    if edges:
        d["edges"] = edges
    return d

def media_group(bid, segment_ids):
    return {
        "type": "media_group",
        "block_id": bid,
        "segment_ids": segment_ids
    }

def up_next(bid, title, text):
    return {
        "type": "up_next",
        "block_id": bid,
        "title": title,
        "text": text
    }

def step(step_id, stype, concept_ids, eyebrow, title, lede, blocks, lineage, reward=None):
    s = {
        "step_id": step_id,
        "type": stype,
        "concept_ids": concept_ids,
        "eyebrow": eyebrow,
        "title": title,
        "lede": lede,
        "blocks": blocks,
        "lineage": lineage
    }
    if reward:
        s["reward"] = reward
    return s

def check_step(step_id, concept_ids, eyebrow, title, lede, lineage, reward=None):
    s = {
        "step_id": step_id,
        "type": "check",
        "concept_ids": concept_ids,
        "eyebrow": eyebrow,
        "title": title,
        "lede": lede,
        "lineage": lineage
    }
    if reward:
        s["reward"] = reward
    return s

def hands_on_step(step_id, concept_ids, eyebrow, title, lede, lineage, reward=None):
    s = {
        "step_id": step_id,
        "type": "hands_on",
        "concept_ids": concept_ids,
        "eyebrow": eyebrow,
        "title": title,
        "lede": lede,
        "lineage": lineage
    }
    if reward:
        s["reward"] = reward
    return s

def lineage(concept_ids, fact_ids, tb_ids, anchors=None, segment_ids=None):
    d = {
        "concept_ids": concept_ids,
        "fact_ids": fact_ids,
        "teaching_block_ids": tb_ids,
        "anchors": anchors or []
    }
    if segment_ids:
        d["segment_ids"] = segment_ids
    return d

# ═══════════════════════════════════════════════════════════════════════════════
# TILE 1: tile_python_operators_conversion
# ═══════════════════════════════════════════════════════════════════════════════

T1 = "tile_python_operators_conversion"
C_ARITH = "python.arithmetic_operators"
C_COMP  = "python.comparison_operators"
C_LOG   = "python.logical_operators"
C_CONV  = "python.type_conversion"

def t1_s01():
    """explainer: arithmetic operators, side_by_side visual"""
    p = f"{T1}.s01"
    # prose: ~60 words
    p1 = prose(
        f"{p}.b01", "definition",
        "Python provides seven arithmetic operators for numeric work. "
        "The familiar four — + (addition), - (subtraction), * (multiplication) and / (division) — "
        "work as expected, but / always returns a float even when both operands are whole numbers: "
        "8 / 2 gives 4.0, not 4. "
        "The ** operator raises a number to a power: 5 ** 2 is 25.",
        [C_ARITH],
        [f"{C_ARITH}#f1", f"{C_ARITH}#f3"],
        [f"{C_ARITH}#tb1"]
    )
    # side_by_side: floor division and remainder
    left_code = code_walk(
        f"{p}.b02.left", "python",
        "17 // 5   # floor division\n17 % 5    # remainder",
        [
            {"start_line": 1, "end_line": 1, "text": "Result: 3 (fractional part discarded)"},
            {"start_line": 2, "end_line": 2, "text": "Result: 2 (what's left over)"}
        ]
    )
    right_code = code_walk(
        f"{p}.b02.right", "python",
        "(32 + 8) * 2    # parentheses group first\n4 * 3.75 - 1    # int promoted to float",
        [
            {"start_line": 1, "end_line": 1, "text": "Result: 80 — addition runs before multiplication"},
            {"start_line": 2, "end_line": 2, "text": "Result: 14.0 — mixed int/float gives float"}
        ]
    )
    ss = side_by_side(
        f"{p}.b02",
        left_code, right_code,
        "// and %", "Grouping and mixed types",
        "17 // 5 is 3 and 17 % 5 is 2; parentheses control evaluation order; mixing int and float promotes the result to float.",
        [C_ARITH],
        [f"{C_ARITH}#f2", f"{C_ARITH}#f4", f"{C_ARITH}#f5"],
        [f"{C_ARITH}#tb1", f"{C_ARITH}#tb2"],
        [f"{C_ARITH}#visual"]
    )
    return step(
        f"{p}", "explainer", [C_ARITH],
        "Arithmetic operators",
        "Seven operators for numeric work",
        "Python gives you seven arithmetic operators — including two you may not have seen before.",
        [p1, ss],
        lineage([C_ARITH],
                [f"{C_ARITH}#f1", f"{C_ARITH}#f2", f"{C_ARITH}#f3", f"{C_ARITH}#f4", f"{C_ARITH}#f5"],
                [f"{C_ARITH}#tb1", f"{C_ARITH}#tb2"],
                [f"{C_ARITH}#visual"]),
        {"gems": 5}
    )

def t1_s02():
    """check: arithmetic operators"""
    return check_step(
        f"{T1}.s02", [C_ARITH],
        "Quick check",
        "Predict the result of a grouped, mixed-type expression",
        "Can you work out what Python evaluates when parentheses and a float are involved?",
        lineage([C_ARITH],
                [f"{C_ARITH}#f4", f"{C_ARITH}#f5"],
                [],
                [f"{C_ARITH}#assessment:predict_grouped_and_mixed_type_result"]),
        {"gems": 10, "first_try_bonus": 5}
    )

def t1_s03():
    """hands_on: arithmetic operators"""
    return hands_on_step(
        f"{T1}.s03", [C_ARITH],
        "Practice",
        "Use arithmetic operators on delivery data",
        "Apply +, -, *, /, //, % and ** to compute delivery metrics.",
        lineage([C_ARITH],
                [f"{C_ARITH}#f1", f"{C_ARITH}#f2", f"{C_ARITH}#f3"],
                [],
                [f"{C_ARITH}#practice",
                 f"{C_ARITH}#assessment:choose_arithmetic_operator",
                 f"{C_ARITH}#assessment:use_floor_division_and_remainder",
                 f"{C_ARITH}#assessment:use_power_operator"]),
        {"gems": 15}
    )

def t1_s04():
    """explainer: comparison operators, side_by_side visual"""
    p = f"{T1}.s04"
    p1 = prose(
        f"{p}.b01", "definition",
        "Comparing two values is how a question like 'is this delivery late?' becomes something Python can act on. "
        "The six comparison operators are < (less than), <= (less than or equal), > (greater than), "
        ">= (greater than or equal), == (equal) and != (not equal). "
        "Every comparison evaluates to exactly one of the two boolean values: True or False.",
        [C_COMP],
        [f"{C_COMP}#f1", f"{C_COMP}#f2"],
        [f"{C_COMP}#tb1", f"{C_COMP}#tb2"]
    )
    left_code = code_walk(
        f"{p}.b02.left", "python",
        "delivery_minutes > 60\ndelivery_minutes >= 60\ndelivery_minutes == 60",
        [
            {"start_line": 1, "end_line": 1, "text": "True if over 60 minutes"},
            {"start_line": 2, "end_line": 2, "text": "True if 60 or more"},
            {"start_line": 3, "end_line": 3, "text": "True only if exactly 60"}
        ]
    )
    right_code = code_walk(
        f"{p}.b02.right", "python",
        "delivery_minutes < 60\ndelivery_minutes <= 60\ncity != 'Lagos'",
        [
            {"start_line": 1, "end_line": 1, "text": "True if under 60 minutes"},
            {"start_line": 2, "end_line": 2, "text": "True if 60 or fewer"},
            {"start_line": 3, "end_line": 3, "text": "True for any city other than Lagos"}
        ]
    )
    ss = side_by_side(
        f"{p}.b02",
        left_code, right_code,
        "Greater-than family", "Less-than family and !=",
        "Each operator returns True or False; delivery_minutes > 60 is True for a 72-minute order and False for a 32-minute one.",
        [C_COMP],
        [f"{C_COMP}#f1", f"{C_COMP}#f2"],
        [f"{C_COMP}#tb2", f"{C_COMP}#tb3"],
        [f"{C_COMP}#visual"]
    )
    return step(
        f"{p}", "explainer", [C_COMP],
        "Comparison operators",
        "Six operators that return True or False",
        "Comparisons turn a question about data into a boolean value Python can branch on.",
        [p1, ss],
        lineage([C_COMP],
                [f"{C_COMP}#f1", f"{C_COMP}#f2"],
                [f"{C_COMP}#tb1", f"{C_COMP}#tb2", f"{C_COMP}#tb3"],
                [f"{C_COMP}#visual"]),
        {"gems": 5}
    )

def t1_s05():
    return check_step(
        f"{T1}.s05", [C_COMP],
        "Quick check",
        "Choose the right comparison operator",
        "Pick the operator that expresses the condition described.",
        lineage([C_COMP],
                [f"{C_COMP}#f1", f"{C_COMP}#f2"],
                [],
                [f"{C_COMP}#assessment:write_comparison_expression"]),
        {"gems": 10, "first_try_bonus": 5}
    )

def t1_s06():
    return check_step(
        f"{T1}.s06", [C_COMP],
        "Quick check",
        "Predict the boolean result of a comparison",
        "Given a value and an operator, what does the expression evaluate to?",
        lineage([C_COMP],
                [f"{C_COMP}#f2"],
                [],
                [f"{C_COMP}#assessment:predict_boolean_result_of_comparison"]),
        {"gems": 10, "first_try_bonus": 5}
    )

def t1_s07():
    return hands_on_step(
        f"{T1}.s07", [C_COMP],
        "Practice",
        "Write comparison expressions for delivery data",
        "Use the six comparison operators to filter and flag orders.",
        lineage([C_COMP],
                [],
                [],
                [f"{C_COMP}#practice"]),
        {"gems": 15}
    )

def t1_s08():
    """explainer: logical operators, side_by_side visual — tb1..tb4, f1..f3"""
    p = f"{T1}.s08"
    p1 = prose(
        f"{p}.b01", "intro",
        "A single comparison asks one question at a time. "
        "To combine conditions — 'is this delivery both late and far from the depot?' — "
        "Python provides three logical operators: or, and and not. "
        "In ascending priority order they are: or (lowest), and, not (highest among the three). "
        "When there are no parentheses, and binds more tightly than or, "
        "so is_late or is_far and is_first_week groups as is_late or (is_far and is_first_week).",
        [C_LOG],
        [f"{C_LOG}#f1"],
        [f"{C_LOG}#tb1", f"{C_LOG}#tb2"]
    )
    p2 = prose(
        f"{p}.b02", "mechanism",
        "x or y returns x if x is true, otherwise y. "
        "It is short-circuit: if is_late is True, Python never evaluates is_far. "
        "x and y returns x if x is false, otherwise y. "
        "It is also short-circuit: if is_late is False, Python skips is_far entirely.",
        [C_LOG],
        [f"{C_LOG}#f2", f"{C_LOG}#f3"],
        [f"{C_LOG}#tb3", f"{C_LOG}#tb4"]
    )
    left_code = code_walk(
        f"{p}.b03.left", "python",
        "is_late or is_far\nTrue or False\nFalse or True\nFalse or False",
        [
            {"start_line": 1, "end_line": 1, "text": "True if either condition holds"},
            {"start_line": 2, "end_line": 2, "text": "True — first operand is true"},
            {"start_line": 3, "end_line": 3, "text": "True — second operand is true"},
            {"start_line": 4, "end_line": 4, "text": "False — neither is true"}
        ]
    )
    right_code = code_walk(
        f"{p}.b03.right", "python",
        "is_late and is_far\nTrue and True\nTrue and False\nFalse and True",
        [
            {"start_line": 1, "end_line": 1, "text": "True only if both conditions hold"},
            {"start_line": 2, "end_line": 2, "text": "True — both are true"},
            {"start_line": 3, "end_line": 3, "text": "False — second is false"},
            {"start_line": 4, "end_line": 4, "text": "False — first is false, short-circuits"}
        ]
    )
    ss = side_by_side(
        f"{p}.b03",
        left_code, right_code,
        "or — true if either", "and — true only if both",
        "or is true when at least one operand is true; and is true only when both are; both short-circuit to skip the second operand when the result is already determined.",
        [C_LOG],
        [f"{C_LOG}#f1", f"{C_LOG}#f2", f"{C_LOG}#f3"],
        [f"{C_LOG}#tb2", f"{C_LOG}#tb3", f"{C_LOG}#tb4"],
        [f"{C_LOG}#visual"]
    )
    return step(
        f"{p}", "explainer", [C_LOG],
        "Logical operators",
        "Combining conditions with and, or and not",
        "Build compound conditions from simpler comparisons using Python's three logical operators.",
        [p1, p2, ss],
        lineage([C_LOG],
                [f"{C_LOG}#f1", f"{C_LOG}#f2", f"{C_LOG}#f3"],
                [f"{C_LOG}#tb1", f"{C_LOG}#tb2", f"{C_LOG}#tb3", f"{C_LOG}#tb4"],
                [f"{C_LOG}#visual"]),
        {"gems": 5}
    )

def t1_s09():
    """explainer: logical operators continued — tb5..tb6, f2..f4"""
    p = f"{T1}.s09"
    p1 = prose(
        f"{p}.b01", "mechanism",
        "not x flips the boolean: not is_late is True when is_late is False, and False when is_late is True. "
        "not has lower priority than the comparison operators, "
        "so not delivery_minutes == 0 is read as not (delivery_minutes == 0), not as (not delivery_minutes) == 0.",
        [C_LOG],
        [f"{C_LOG}#f4"],
        [f"{C_LOG}#tb5"]
    )
    p2 = prose(
        f"{p}.b02", "example",
        "A rule like 'flag this delivery if it is late or unusually far' reads directly as is_late or is_far. "
        "A stricter rule — 'flag it only if it is late and it is the driver's first week' — reads as is_late and is_first_week. "
        "and, or and not let you build one compound condition out of several simpler comparisons.",
        [C_LOG],
        [f"{C_LOG}#f2", f"{C_LOG}#f3"],
        [f"{C_LOG}#tb6"]
    )
    return step(
        f"{p}", "explainer", [C_LOG],
        "Logical operators",
        "not, priority and real-world compound conditions",
        "not flips a boolean; priority rules determine how mixed expressions group without parentheses.",
        [p1, p2],
        lineage([C_LOG],
                [f"{C_LOG}#f2", f"{C_LOG}#f3", f"{C_LOG}#f4"],
                [f"{C_LOG}#tb5", f"{C_LOG}#tb6"]),
        {"gems": 5}
    )

def t1_s10():
    return check_step(
        f"{T1}.s10", [C_LOG],
        "Quick check",
        "Predict operator priority in a mixed expression",
        "How does Python group an expression that mixes and and or without parentheses?",
        lineage([C_LOG],
                [f"{C_LOG}#f1", f"{C_LOG}#f4"],
                [],
                [f"{C_LOG}#assessment:predict_operator_priority"]),
        {"gems": 10, "first_try_bonus": 5}
    )

def t1_s11():
    return check_step(
        f"{T1}.s11", [C_LOG],
        "Quick check",
        "Predict the result of a short-circuit expression",
        "Which operand does Python evaluate when the first one already decides the outcome?",
        lineage([C_LOG],
                [f"{C_LOG}#f2", f"{C_LOG}#f3"],
                [],
                [f"{C_LOG}#assessment:predict_short_circuit_result"]),
        {"gems": 10, "first_try_bonus": 5}
    )

def t1_s12():
    return hands_on_step(
        f"{T1}.s12", [C_LOG],
        "Practice",
        "Write compound boolean expressions",
        "Combine comparisons with and, or and not to express multi-condition rules.",
        lineage([C_LOG],
                [f"{C_LOG}#f1", f"{C_LOG}#f2", f"{C_LOG}#f3", f"{C_LOG}#f4"],
                [],
                [f"{C_LOG}#practice",
                 f"{C_LOG}#assessment:write_compound_boolean_expression"]),
        {"gems": 15}
    )

def t1_s13():
    """explainer: type conversion, before_after visual"""
    p = f"{T1}.s13"
    p1 = prose(
        f"{p}.b01", "intro",
        "Data often arrives as the wrong type. A delivery time typed into a form as the text '32' "
        "cannot be used in arithmetic until it is converted to a number. "
        "Python provides three constructors for explicit conversion: "
        "int() and float() produce a number from a string or another numeric type, "
        "and str() turns any value into its string representation.",
        [C_CONV],
        [f"{C_CONV}#f1", f"{C_CONV}#f4"],
        [f"{C_CONV}#tb1", f"{C_CONV}#tb4"]
    )
    p2 = prose(
        f"{p}.b02", "mechanism",
        "int('123') returns the integer 123. "
        "float('+1.23') returns the float 1.23. "
        "str(32) turns the integer 32 into the string '32'. "
        "These conversions work in both directions between numbers and their string representations.",
        [C_CONV],
        [f"{C_CONV}#f2", f"{C_CONV}#f3", f"{C_CONV}#f4"],
        [f"{C_CONV}#tb2", f"{C_CONV}#tb3", f"{C_CONV}#tb4"]
    )
    p3 = prose(
        f"{p}.b03", "misconception",
        "Not every string can be converted. float() requires the string to match a numeric format — "
        "an optional sign, digits, and optionally a decimal point or exponent — after stripping surrounding whitespace. "
        "int() requires an integer string. "
        "A string that does not match raises a ValueError: int('3.5') fails because '3.5' is not an integer string.",
        [C_CONV],
        [f"{C_CONV}#f5", f"{C_CONV}#f6"],
        [f"{C_CONV}#tb5"]
    )
    before_code = code_walk(
        f"{p}.b04.before", "python",
        "delivery_time = '32'\ndelivery_time + 10",
        [
            {"start_line": 1, "end_line": 1, "text": "String '32' — cannot add a number to it"},
            {"start_line": 2, "end_line": 2, "text": "TypeError: can only concatenate str to str"}
        ]
    )
    after_code = code_walk(
        f"{p}.b04.after", "python",
        "delivery_time = int('32')\ndelivery_time + 10",
        [
            {"start_line": 1, "end_line": 1, "text": "int('32') returns the integer 32"},
            {"start_line": 2, "end_line": 2, "text": "Result: 42 — arithmetic now works"}
        ]
    )
    ba = before_after(
        f"{p}.b04",
        before_code, after_code,
        "Converting '32' from string to int with int() makes arithmetic possible; without conversion, adding a number raises a TypeError.",
        [C_CONV],
        [f"{C_CONV}#f1", f"{C_CONV}#f2"],
        [f"{C_CONV}#tb1", f"{C_CONV}#tb2"],
        [f"{C_CONV}#visual"]
    )
    return step(
        f"{p}", "explainer", [C_CONV],
        "Type conversion",
        "Converting between strings and numbers",
        "int(), float() and str() let you move values between types — but only when the format matches.",
        [p1, p2, p3, ba],
        lineage([C_CONV],
                [f"{C_CONV}#f1", f"{C_CONV}#f2", f"{C_CONV}#f3",
                 f"{C_CONV}#f4", f"{C_CONV}#f5", f"{C_CONV}#f6"],
                [f"{C_CONV}#tb1", f"{C_CONV}#tb2", f"{C_CONV}#tb3",
                 f"{C_CONV}#tb4", f"{C_CONV}#tb5"],
                [f"{C_CONV}#visual"]),
        {"gems": 5}
    )

def t1_s14():
    return check_step(
        f"{T1}.s14", [C_CONV],
        "Quick check",
        "Convert a value to the target type",
        "Which constructor and argument produces the value described?",
        lineage([C_CONV],
                [f"{C_CONV}#f1", f"{C_CONV}#f2", f"{C_CONV}#f3", f"{C_CONV}#f4"],
                [],
                [f"{C_CONV}#assessment:convert_value_to_target_type"]),
        {"gems": 10, "first_try_bonus": 5}
    )

def t1_s15():
    return check_step(
        f"{T1}.s15", [C_CONV],
        "Quick check",
        "Recognise an invalid conversion",
        "Which string cannot be converted by the given constructor?",
        lineage([C_CONV],
                [f"{C_CONV}#f5", f"{C_CONV}#f6"],
                [],
                [f"{C_CONV}#assessment:recognize_invalid_conversion"]),
        {"gems": 10, "first_try_bonus": 5}
    )

def t1_s16():
    return hands_on_step(
        f"{T1}.s16", [C_CONV],
        "Practice",
        "Convert delivery data between types",
        "Use int(), float() and str() to fix type mismatches in order records.",
        lineage([C_CONV],
                [],
                [],
                [f"{C_CONV}#practice"]),
        {"gems": 15}
    )

def t1_s17():
    """recap with up_next"""
    p = f"{T1}.s17"
    p1 = prose(
        f"{p}.b01", "takeaway",
        "Comparison operators (<, <=, >, >=, ==, !=) each return True or False. "
        "and, or and not combine those booleans into compound conditions; and has higher priority than or. "
        "Converting a string to a number only works when the string matches the format the target type accepts — "
        "otherwise the conversion raises a ValueError.",
        [C_ARITH, C_COMP, C_LOG, C_CONV],
        [f"{C_COMP}#f2", f"{C_LOG}#f1", f"{C_CONV}#f5", f"{C_CONV}#f6"],
        [f"{C_COMP}#tb4", f"{C_LOG}#tb7", f"{C_CONV}#tb6"]
    )
    un = up_next(
        f"{p}.b02",
        "Up next: Lists, Dictionaries, and Tuples",
        "In the next tile you will store ordered sequences of delivery times in lists, "
        "map order IDs to cities in dictionaries, and group fixed records in tuples."
    )
    return step(
        f"{p}", "recap",
        [C_ARITH, C_COMP, C_LOG, C_CONV],
        "Recap",
        "What you learned",
        "Key ideas from this tile.",
        [p1, un],
        lineage([C_ARITH, C_COMP, C_LOG, C_CONV],
                [f"{C_COMP}#f2", f"{C_LOG}#f1", f"{C_CONV}#f5", f"{C_CONV}#f6"],
                [f"{C_COMP}#tb4", f"{C_LOG}#tb7", f"{C_CONV}#tb6"]),
        {"gems": 5}
    )

# Remediation steps for tile 1
def t1_r01():
    """remediation for s02 (check: f4, f5 — grouping and mixed types)"""
    p = f"{T1}.r01"
    p1 = prose(
        f"{p}.b01", "mechanism",
        "Parentheses control evaluation order: (32 + 8) * 2 adds first, giving 80. "
        "Without parentheses, * runs before +. "
        "When you mix an int and a float in one operation, Python promotes the int to float: "
        "4 * 3.75 - 1 gives 14.0, not 14.",
        [C_ARITH],
        [f"{C_ARITH}#f4", f"{C_ARITH}#f5"],
        [f"{C_ARITH}#tb2"]
    )
    before_code = code_walk(
        f"{p}.b02.before", "python",
        "32 + 8 * 2",
        [{"start_line": 1, "end_line": 1, "text": "Result: 48 — * runs before +"}]
    )
    after_code = code_walk(
        f"{p}.b02.after", "python",
        "(32 + 8) * 2",
        [{"start_line": 1, "end_line": 1, "text": "Result: 80 — parentheses force addition first"}]
    )
    ba = before_after(
        f"{p}.b02",
        before_code, after_code,
        "Adding parentheses changes the evaluation order and the result.",
        [C_ARITH],
        [f"{C_ARITH}#f4"],
        [f"{C_ARITH}#tb2"]
    )
    return {
        "step_id": f"{p}",
        "type": "remediation",
        "concept_ids": [C_ARITH],
        "eyebrow": "Let's revisit",
        "title": "Grouping with parentheses and mixed int/float",
        "lede": "A clear contrast showing how parentheses change the result, and why mixing int and float gives a float.",
        "blocks": [p1, ba],
        "lineage": lineage([C_ARITH],
                           [f"{C_ARITH}#f4", f"{C_ARITH}#f5"],
                           [f"{C_ARITH}#tb2"])
    }

def t1_r02():
    """remediation for s05/s06 (check: comparison operators, f1, f2)"""
    p = f"{T1}.r02"
    p1 = prose(
        f"{p}.b01", "definition",
        "The six comparison operators are < (less than), <= (less than or equal), "
        "> (greater than), >= (greater than or equal), == (equal) and != (not equal). "
        "Every comparison returns exactly True or False — never a number.",
        [C_COMP],
        [f"{C_COMP}#f1", f"{C_COMP}#f2"],
        [f"{C_COMP}#tb1", f"{C_COMP}#tb2"]
    )
    left_code = code_walk(
        f"{p}.b02.left", "python",
        "delivery_minutes = 32\ndelivery_minutes > 60",
        [
            {"start_line": 1, "end_line": 1, "text": "32 minutes"},
            {"start_line": 2, "end_line": 2, "text": "False — 32 is not greater than 60"}
        ]
    )
    right_code = code_walk(
        f"{p}.b02.right", "python",
        "delivery_minutes = 72\ndelivery_minutes > 60",
        [
            {"start_line": 1, "end_line": 1, "text": "72 minutes"},
            {"start_line": 2, "end_line": 2, "text": "True — 72 is greater than 60"}
        ]
    )
    ss = side_by_side(
        f"{p}.b02",
        left_code, right_code,
        "32 minutes (not late)", "72 minutes (late)",
        "The same expression delivery_minutes > 60 gives False for 32 and True for 72.",
        [C_COMP],
        [f"{C_COMP}#f1", f"{C_COMP}#f2"],
        [f"{C_COMP}#tb2", f"{C_COMP}#tb3"]
    )
    return {
        "step_id": f"{p}",
        "type": "remediation",
        "concept_ids": [C_COMP],
        "eyebrow": "Let's revisit",
        "title": "Comparison operators and boolean results",
        "lede": "A side-by-side contrast showing the same expression returning different booleans for different values.",
        "blocks": [p1, ss],
        "lineage": lineage([C_COMP],
                           [f"{C_COMP}#f1", f"{C_COMP}#f2"],
                           [f"{C_COMP}#tb1", f"{C_COMP}#tb2", f"{C_COMP}#tb3"])
    }

def t1_r03():
    """remediation for s10 (check: f1, f4 — priority)"""
    p = f"{T1}.r03"
    p1 = prose(
        f"{p}.b01", "mechanism",
        "In ascending priority order the logical operators are: or (lowest), and, not. "
        "and binds more tightly than or, so is_late or is_far and is_first_week "
        "groups as is_late or (is_far and is_first_week). "
        "not has lower priority than comparison operators: not delivery_minutes == 0 "
        "means not (delivery_minutes == 0).",
        [C_LOG],
        [f"{C_LOG}#f1", f"{C_LOG}#f4"],
        [f"{C_LOG}#tb2", f"{C_LOG}#tb5"]
    )
    before_code = code_walk(
        f"{p}.b02.before", "python",
        "is_late or is_far and is_first_week",
        [{"start_line": 1, "end_line": 1, "text": "Groups as: is_late or (is_far and is_first_week)"}]
    )
    after_code = code_walk(
        f"{p}.b02.after", "python",
        "(is_late or is_far) and is_first_week",
        [{"start_line": 1, "end_line": 1, "text": "Parentheses override priority — both sides must be true"}]
    )
    ba = before_after(
        f"{p}.b02",
        before_code, after_code,
        "Without parentheses, and groups first; adding parentheses changes which conditions must both be true.",
        [C_LOG],
        [f"{C_LOG}#f1"],
        [f"{C_LOG}#tb2"]
    )
    return {
        "step_id": f"{p}",
        "type": "remediation",
        "concept_ids": [C_LOG],
        "eyebrow": "Let's revisit",
        "title": "Operator priority: and before or",
        "lede": "A contrast showing how and and or group when there are no parentheses.",
        "blocks": [p1, ba],
        "lineage": lineage([C_LOG],
                           [f"{C_LOG}#f1", f"{C_LOG}#f4"],
                           [f"{C_LOG}#tb2", f"{C_LOG}#tb5"])
    }

def t1_r04():
    """remediation for s11 (check: f2, f3 — short-circuit)"""
    p = f"{T1}.r04"
    p1 = prose(
        f"{p}.b01", "mechanism",
        "or short-circuits: if the first operand is True, Python returns it immediately without evaluating the second. "
        "and short-circuits: if the first operand is False, Python returns it immediately without evaluating the second. "
        "This means is_late or is_far only checks is_far when is_late is False, "
        "and is_late and is_far only checks is_far when is_late is True.",
        [C_LOG],
        [f"{C_LOG}#f2", f"{C_LOG}#f3"],
        [f"{C_LOG}#tb3", f"{C_LOG}#tb4"]
    )
    left_code = code_walk(
        f"{p}.b02.left", "python",
        "is_late = True\nis_late or is_far",
        [
            {"start_line": 1, "end_line": 1, "text": "is_late is True"},
            {"start_line": 2, "end_line": 2, "text": "Returns True — is_far never evaluated"}
        ]
    )
    right_code = code_walk(
        f"{p}.b02.right", "python",
        "is_late = False\nis_late and is_far",
        [
            {"start_line": 1, "end_line": 1, "text": "is_late is False"},
            {"start_line": 2, "end_line": 2, "text": "Returns False — is_far never evaluated"}
        ]
    )
    ss = side_by_side(
        f"{p}.b02",
        left_code, right_code,
        "or short-circuits on True", "and short-circuits on False",
        "Both operators skip the second operand when the first operand already determines the result.",
        [C_LOG],
        [f"{C_LOG}#f2", f"{C_LOG}#f3"],
        [f"{C_LOG}#tb3", f"{C_LOG}#tb4"]
    )
    return {
        "step_id": f"{p}",
        "type": "remediation",
        "concept_ids": [C_LOG],
        "eyebrow": "Let's revisit",
        "title": "Short-circuit evaluation in or and and",
        "lede": "A side-by-side contrast showing when each operator stops evaluating early.",
        "blocks": [p1, ss],
        "lineage": lineage([C_LOG],
                           [f"{C_LOG}#f2", f"{C_LOG}#f3"],
                           [f"{C_LOG}#tb3", f"{C_LOG}#tb4"])
    }

def t1_r05():
    """remediation for s14 (check: f1..f4 — valid conversions)"""
    p = f"{T1}.r05"
    p1 = prose(
        f"{p}.b01", "mechanism",
        "int('123') returns 123. float('+1.23') returns 1.23. str(32) returns '32'. "
        "These constructors convert between compatible types: "
        "a string of digits to int, a numeric-format string to float, any value to its string form.",
        [C_CONV],
        [f"{C_CONV}#f1", f"{C_CONV}#f2", f"{C_CONV}#f3", f"{C_CONV}#f4"],
        [f"{C_CONV}#tb2", f"{C_CONV}#tb3", f"{C_CONV}#tb4"]
    )
    before_code = code_walk(
        f"{p}.b02.before", "python",
        "delivery_time = '32'\nresult = delivery_time + 10",
        [
            {"start_line": 1, "end_line": 1, "text": "String — cannot add to int"},
            {"start_line": 2, "end_line": 2, "text": "TypeError raised"}
        ]
    )
    after_code = code_walk(
        f"{p}.b02.after", "python",
        "delivery_time = int('32')\nresult = delivery_time + 10",
        [
            {"start_line": 1, "end_line": 1, "text": "int('32') gives 32"},
            {"start_line": 2, "end_line": 2, "text": "Result: 42"}
        ]
    )
    ba = before_after(
        f"{p}.b02",
        before_code, after_code,
        "Wrapping '32' in int() converts it to the integer 32, making arithmetic possible.",
        [C_CONV],
        [f"{C_CONV}#f1", f"{C_CONV}#f2"],
        [f"{C_CONV}#tb1", f"{C_CONV}#tb2"]
    )
    return {
        "step_id": f"{p}",
        "type": "remediation",
        "concept_ids": [C_CONV],
        "eyebrow": "Let's revisit",
        "title": "Converting between strings and numbers",
        "lede": "A before/after showing what happens with and without int().",
        "blocks": [p1, ba],
        "lineage": lineage([C_CONV],
                           [f"{C_CONV}#f1", f"{C_CONV}#f2", f"{C_CONV}#f3", f"{C_CONV}#f4"],
                           [f"{C_CONV}#tb2", f"{C_CONV}#tb3", f"{C_CONV}#tb4"])
    }

def t1_r06():
    """remediation for s15 (check: f5, f6 — invalid conversions)"""
    p = f"{T1}.r06"
    p1 = prose(
        f"{p}.b01", "misconception",
        "float() requires the string to match a numeric format: an optional sign, digits, "
        "and optionally a decimal point or exponent, after stripping surrounding whitespace. "
        "int() requires an integer string — no decimal point. "
        "A string that does not match raises a ValueError: int('3.5') fails because '3.5' contains a decimal point.",
        [C_CONV],
        [f"{C_CONV}#f5", f"{C_CONV}#f6"],
        [f"{C_CONV}#tb5"]
    )
    left_code = code_walk(
        f"{p}.b02.left", "python",
        "int('3.5')",
        [{"start_line": 1, "end_line": 1, "text": "ValueError — '3.5' is not an integer string"}]
    )
    right_code = code_walk(
        f"{p}.b02.right", "python",
        "int(float('3.5'))",
        [{"start_line": 1, "end_line": 1, "text": "Result: 3 — convert to float first, then truncate"}]
    )
    ss = side_by_side(
        f"{p}.b02",
        left_code, right_code,
        "int('3.5') — ValueError", "int(float('3.5')) — works",
        "int() cannot parse a decimal string directly; convert to float first if you need to truncate.",
        [C_CONV],
        [f"{C_CONV}#f5", f"{C_CONV}#f6"],
        [f"{C_CONV}#tb5"]
    )
    return {
        "step_id": f"{p}",
        "type": "remediation",
        "concept_ids": [C_CONV],
        "eyebrow": "Let's revisit",
        "title": "When type conversion raises ValueError",
        "lede": "A contrast between a failing conversion and a working alternative.",
        "blocks": [p1, ss],
        "lineage": lineage([C_CONV],
                           [f"{C_CONV}#f5", f"{C_CONV}#f6"],
                           [f"{C_CONV}#tb5"])
    }

tile1 = {
    "tile_id": T1,
    "title": "Comparison and Logical Operators",
    "summary": "Learn Python's arithmetic, comparison and logical operators, understand short-circuit evaluation and operator priority, and convert values between int, float and str.",
    "steps": [
        t1_s01(), t1_s02(), t1_s03(),
        t1_s04(), t1_s05(), t1_s06(), t1_s07(),
        t1_s08(), t1_s09(), t1_s10(), t1_s11(), t1_s12(),
        t1_s13(), t1_s14(), t1_s15(), t1_s16(),
        t1_s17()
    ],
    "remediation_steps": [
        t1_r01(), t1_r02(), t1_r03(), t1_r04(), t1_r05(), t1_r06()
    ]
}

# ═══════════════════════════════════════════════════════════════════════════════
# TILE 2: tile_python_lists_dicts_tuples
# ═══════════════════════════════════════════════════════════════════════════════

T2 = "tile_python_lists_dicts_tuples"
C_LISTS = "python.lists"
C_DICTS = "python.dictionaries"
C_TUPLES = "python.tuples"

def t2_s01():
    """explainer: lists, diagram visual"""
    p = f"{T2}.s01"
    p1 = prose(
        f"{p}.b01", "intro",
        "Keeping five separate variables for five delivery times gets unwieldy fast. "
        "A list stores an ordered sequence of values in a single name: "
        "delivery_times = [32, 45, 21, 60, 18]. "
        "Items are indexed from 0 at the left and from -1 at the right, "
        "so delivery_times[0] is 32 and delivery_times[-1] is 18.",
        [C_LISTS],
        [f"{C_LISTS}#f1", f"{C_LISTS}#f2"],
        [f"{C_LISTS}#tb1", f"{C_LISTS}#tb2"]
    )
    p2 = prose(
        f"{p}.b02", "mechanism",
        "A slice extracts a sub-list: delivery_times[1:3] returns [45, 21]. "
        "The start index is included; the end index is excluded. "
        "delivery_times[-3:] returns the last three items. "
        "Lists are mutable: delivery_times[3] = 64 replaces the item at index 3 in place.",
        [C_LISTS],
        [f"{C_LISTS}#f3", f"{C_LISTS}#f5"],
        [f"{C_LISTS}#tb3"]
    )
    # diagram: array showing indexes
    d = diagram(
        f"{p}.b03", "array",
        "delivery_times — positive and negative indexes",
        [
            {"id": "i0", "label": "32", "kind": "item", "group": "positive", "fields": ["index 0", "index -5"]},
            {"id": "i1", "label": "45", "kind": "item", "group": "positive", "fields": ["index 1", "index -4"]},
            {"id": "i2", "label": "21", "kind": "item", "group": "positive", "fields": ["index 2", "index -3"]},
            {"id": "i3", "label": "60", "kind": "item", "group": "positive", "fields": ["index 3", "index -2"]},
            {"id": "i4", "label": "18", "kind": "item", "group": "positive", "fields": ["index 4", "index -1"]},
            {"id": "slice_start", "label": "slice [1:3] starts here (included)", "kind": "annotation"},
            {"id": "slice_end", "label": "slice [1:3] ends here (excluded)", "kind": "annotation"}
        ],
        [
            {"from": "slice_start", "to": "i1", "directed": True},
            {"from": "slice_end", "to": "i3", "directed": True}
        ],
        "Array of five delivery times with positive indexes 0–4 above and negative indexes -5 to -1 below; a bracket marks slice [1:3] from index 1 (included) to index 3 (excluded), yielding [45, 21].",
        [C_LISTS],
        [f"{C_LISTS}#f1", f"{C_LISTS}#f2", f"{C_LISTS}#f3", f"{C_LISTS}#f5"],
        [f"{C_LISTS}#tb2", f"{C_LISTS}#tb3"],
        [f"{C_LISTS}#visual"]
    )
    return step(
        f"{p}", "explainer", [C_LISTS],
        "Lists",
        "Ordered, mutable sequences",
        "A list stores an ordered sequence of values you can index, slice and modify.",
        [p1, p2, d],
        lineage([C_LISTS],
                [f"{C_LISTS}#f1", f"{C_LISTS}#f2", f"{C_LISTS}#f3", f"{C_LISTS}#f5"],
                [f"{C_LISTS}#tb1", f"{C_LISTS}#tb2", f"{C_LISTS}#tb3", f"{C_LISTS}#tb4"],
                [f"{C_LISTS}#visual"]),
        {"gems": 5}
    )

def t2_s02():
    """video: lists"""
    p = f"{T2}.s02"
    mg = media_group(
        f"{p}.b01",
        ["seg_python.lists_ajrtAuDg3yw_0_177", "seg_python.lists_SfX8IIxoJwQ_19_208"]
    )
    return step(
        f"{p}", "video", [C_LISTS],
        "Watch",
        "Lists in action",
        "See list creation, indexing and slicing demonstrated.",
        [mg],
        lineage([C_LISTS],
                [f"{C_LISTS}#f1", f"{C_LISTS}#f2", f"{C_LISTS}#f3", f"{C_LISTS}#f5"],
                [],
                [],
                ["seg_python.lists_ajrtAuDg3yw_0_177", "seg_python.lists_SfX8IIxoJwQ_19_208"])
    )

def t2_s03():
    """explainer: lists append — tb5, f4"""
    p = f"{T2}.s03"
    p1 = prose(
        f"{p}.b01", "mechanism",
        "To add a new item to the end of a list, call the append() method: "
        "delivery_times.append(27) adds 27 as the last element.",
        [C_LISTS],
        [f"{C_LISTS}#f4"],
        [f"{C_LISTS}#tb5"]
    )
    return step(
        f"{p}", "explainer", [C_LISTS],
        "Lists",
        "Adding items with append()",
        "append() grows a list by one item at the end.",
        [p1],
        lineage([C_LISTS],
                [f"{C_LISTS}#f4"],
                [f"{C_LISTS}#tb5"]),
        {"gems": 5}
    )

def t2_s04():
    return check_step(
        f"{T2}.s04", [C_LISTS],
        "Quick check",
        "Modify and extend a list",
        "Can you predict what a list looks like after an assignment and an append?",
        lineage([C_LISTS],
                [f"{C_LISTS}#f3", f"{C_LISTS}#f4"],
                [],
                [f"{C_LISTS}#assessment:modify_and_extend_a_list"]),
        {"gems": 10, "first_try_bonus": 5}
    )

def t2_s05():
    return hands_on_step(
        f"{T2}.s05", [C_LISTS],
        "Practice",
        "Build and work with a list of delivery times",
        "Create a list, index into it, slice it and append a new item.",
        lineage([C_LISTS],
                [f"{C_LISTS}#f1", f"{C_LISTS}#f2", f"{C_LISTS}#f3",
                 f"{C_LISTS}#f4", f"{C_LISTS}#f5"],
                [],
                [f"{C_LISTS}#practice",
                 f"{C_LISTS}#assessment:create_a_list",
                 f"{C_LISTS}#assessment:index_and_slice_a_list",
                 f"{C_LISTS}#assessment:modify_and_extend_a_list"]),
        {"gems": 15}
    )

def t2_s06():
    """explainer: dictionaries, diagram visual"""
    p = f"{T2}.s06"
    p1 = prose(
        f"{p}.b01", "intro",
        "Sometimes you need to look up a value by a meaningful key rather than by position. "
        "A dictionary is a collection of key: value pairs written inside braces, "
        "where keys must be unique: order_city = {1042: 'Lagos', 1043: 'Abuja', 1044: 'Kano'}. "
        "Retrieve a value by subscripting with its key: order_city[1042] returns 'Lagos'.",
        [C_DICTS],
        [f"{C_DICTS}#f1", f"{C_DICTS}#f2"],
        [f"{C_DICTS}#tb1", f"{C_DICTS}#tb2"]
    )
    p2 = prose(
        f"{p}.b02", "mechanism",
        "Store or update a value by assigning to a key: order_city[1044] = 'Kano' adds a new entry; "
        "assigning to an existing key replaces its value. "
        "The get() method returns None (or a specified default) instead of raising an error "
        "when a key is absent: order_city.get(9999) returns None rather than crashing.",
        [C_DICTS],
        [f"{C_DICTS}#f2", f"{C_DICTS}#f4"],
        [f"{C_DICTS}#tb2", f"{C_DICTS}#tb4"]
    )
    p3 = prose(
        f"{p}.b03", "misconception",
        "Subscripting a key that is not in the dictionary raises a KeyError: "
        "order_city[9999] fails if no order 9999 was ever added. "
        "Use get() when you are not certain the key exists.",
        [C_DICTS],
        [f"{C_DICTS}#f3"],
        [f"{C_DICTS}#tb3"]
    )
    # diagram: mapping from keys to values
    d = diagram(
        f"{p}.b04", "mapping",
        "order_city — key-to-value lookup",
        [
            {"id": "k1042", "label": "1042", "kind": "key"},
            {"id": "k1043", "label": "1043", "kind": "key"},
            {"id": "k1044", "label": "1044", "kind": "key"},
            {"id": "k9999", "label": "9999 (missing)", "kind": "key"},
            {"id": "v_lagos", "label": "'Lagos'", "kind": "value"},
            {"id": "v_abuja", "label": "'Abuja'", "kind": "value"},
            {"id": "v_kano", "label": "'Kano'", "kind": "value"},
            {"id": "v_error", "label": "KeyError", "kind": "error"}
        ],
        [
            {"from": "k1042", "to": "v_lagos", "directed": True, "label": "lookup"},
            {"from": "k1043", "to": "v_abuja", "directed": True, "label": "lookup"},
            {"from": "k1044", "to": "v_kano", "directed": True, "label": "lookup"},
            {"from": "k9999", "to": "v_error", "directed": True, "label": "KeyError"}
        ],
        "Mapping diagram: keys 1042, 1043, 1044 each point to their city values; key 9999 points to a KeyError node showing what happens when a missing key is subscripted.",
        [C_DICTS],
        [f"{C_DICTS}#f1", f"{C_DICTS}#f2", f"{C_DICTS}#f3", f"{C_DICTS}#f4"],
        [f"{C_DICTS}#tb1", f"{C_DICTS}#tb2", f"{C_DICTS}#tb3", f"{C_DICTS}#tb4"],
        [f"{C_DICTS}#visual"]
    )
    return step(
        f"{p}", "explainer", [C_DICTS],
        "Dictionaries",
        "Key-to-value lookup",
        "A dictionary maps unique keys to values — look up a city by order ID, not by position.",
        [p1, p2, p3, d],
        lineage([C_DICTS],
                [f"{C_DICTS}#f1", f"{C_DICTS}#f2", f"{C_DICTS}#f3", f"{C_DICTS}#f4"],
                [f"{C_DICTS}#tb1", f"{C_DICTS}#tb2", f"{C_DICTS}#tb3", f"{C_DICTS}#tb4"],
                [f"{C_DICTS}#visual"]),
        {"gems": 5}
    )

def t2_s07():
    """video: dictionaries"""
    p = f"{T2}.s07"
    mg = media_group(
        f"{p}.b01",
        ["seg_python.dictionaries_daefaLgNkw0_0_300"]
    )
    return step(
        f"{p}", "video", [C_DICTS],
        "Watch",
        "Dictionaries in action",
        "See dictionary creation, lookup and the KeyError demonstrated.",
        [mg],
        lineage([C_DICTS],
                [f"{C_DICTS}#f1", f"{C_DICTS}#f2", f"{C_DICTS}#f3", f"{C_DICTS}#f4"],
                [],
                [],
                ["seg_python.dictionaries_daefaLgNkw0_0_300"])
    )

def t2_s08():
    """explainer: dictionaries — in keyword, tb5, f5"""
    p = f"{T2}.s08"
    p1 = prose(
        f"{p}.b01", "mechanism",
        "The in keyword checks whether a key is present in a dictionary: "
        "1042 in order_city is True.",
        [C_DICTS],
        [f"{C_DICTS}#f5"],
        [f"{C_DICTS}#tb5"]
    )
    return step(
        f"{p}", "explainer", [C_DICTS],
        "Dictionaries",
        "Testing key membership with in",
        "Use in to check whether a key exists before accessing it.",
        [p1],
        lineage([C_DICTS],
                [f"{C_DICTS}#f5"],
                [f"{C_DICTS}#tb5"]),
        {"gems": 5}
    )

def t2_s09():
    return check_step(
        f"{T2}.s09", [C_DICTS],
        "Quick check",
        "Predict what happens with a missing key",
        "What does Python do when you subscript a key that is not in the dictionary?",
        lineage([C_DICTS],
                [f"{C_DICTS}#f3"],
                [],
                [f"{C_DICTS}#assessment:predict_missing_key_error"]),
        {"gems": 10, "first_try_bonus": 5}
    )

def t2_s10():
    return hands_on_step(
        f"{T2}.s10", [C_DICTS],
        "Practice",
        "Build and query an order-city dictionary",
        "Create a dictionary, add entries, look up values and use get() for safe access.",
        lineage([C_DICTS],
                [f"{C_DICTS}#f1", f"{C_DICTS}#f2"],
                [],
                [f"{C_DICTS}#practice",
                 f"{C_DICTS}#assessment:build_and_update_dictionary",
                 f"{C_DICTS}#assessment:look_up_value_by_key"]),
        {"gems": 15}
    )

def t2_s11():
    """explainer: tuples, before_after visual"""
    p = f"{T2}.s11"
    p1 = prose(
        f"{p}.b01", "intro",
        "A tuple groups a small, fixed set of values together. "
        "It is written as comma-separated values, with or without surrounding parentheses: "
        "order = 1042, 'Lagos', 32 or order = (1042, 'Lagos', 32). "
        "Python shows tuples enclosed in parentheses on output.",
        [C_TUPLES],
        [f"{C_TUPLES}#f1"],
        [f"{C_TUPLES}#tb1"]
    )
    p2 = prose(
        f"{p}.b02", "misconception",
        "Tuples are immutable: once created, an item cannot be reassigned. "
        "order[0] = 1099 raises a TypeError. "
        "Also, enclosing a single value in parentheses does not make it a tuple — "
        "singleton = ('Lagos') is still just the string 'Lagos'. "
        "A one-item tuple needs a trailing comma: singleton = 'Lagos',",
        [C_TUPLES],
        [f"{C_TUPLES}#f2", f"{C_TUPLES}#m1"],
        [f"{C_TUPLES}#tb2", f"{C_TUPLES}#tb4"]
    )
    before_code = code_walk(
        f"{p}.b03.before", "python",
        "order = (1042, 'Lagos', 32)",
        [{"start_line": 1, "end_line": 1, "text": "Three values packed into one tuple"}]
    )
    after_code = code_walk(
        f"{p}.b03.after", "python",
        "order_id, city, minutes = order",
        [
            {"start_line": 1, "end_line": 1, "text": "Unpacking: order_id=1042, city='Lagos', minutes=32"}
        ]
    )
    ba = before_after(
        f"{p}.b03",
        before_code, after_code,
        "Unpacking hands each element of the tuple back to its own name — order_id, city and minutes are now separate variables.",
        [C_TUPLES],
        [f"{C_TUPLES}#f1", f"{C_TUPLES}#f3"],
        [f"{C_TUPLES}#tb1", f"{C_TUPLES}#tb3"],
        [f"{C_TUPLES}#visual"]
    )
    return step(
        f"{p}", "explainer", [C_TUPLES],
        "Tuples",
        "Immutable sequences and unpacking",
        "A tuple groups a fixed set of values; unpacking hands each piece back to its own name.",
        [p1, p2, ba],
        lineage([C_TUPLES],
                [f"{C_TUPLES}#f1", f"{C_TUPLES}#f2", f"{C_TUPLES}#f3", f"{C_TUPLES}#m1"],
                [f"{C_TUPLES}#tb1", f"{C_TUPLES}#tb2", f"{C_TUPLES}#tb3", f"{C_TUPLES}#tb4"],
                [f"{C_TUPLES}#visual"]),
        {"gems": 5}
    )

def t2_s12():
    return check_step(
        f"{T2}.s12", [C_TUPLES],
        "Quick check",
        "Recognise when a one-item tuple needs a trailing comma",
        "Which expression actually creates a tuple with one element?",
        lineage([C_TUPLES],
                [f"{C_TUPLES}#m1"],
                [],
                [f"{C_TUPLES}#assessment:recognize_single_item_tuple_needs_comma"]),
        {"gems": 10, "first_try_bonus": 5}
    )

def t2_s13():
    return hands_on_step(
        f"{T2}.s13", [C_TUPLES],
        "Practice",
        "Create, inspect and unpack a tuple",
        "Build a tuple for an order record, confirm it is immutable, and unpack it into named variables.",
        lineage([C_TUPLES],
                [f"{C_TUPLES}#f1", f"{C_TUPLES}#f2", f"{C_TUPLES}#f3"],
                [],
                [f"{C_TUPLES}#practice",
                 f"{C_TUPLES}#assessment:create_a_tuple",
                 f"{C_TUPLES}#assessment:recognize_tuple_immutability",
                 f"{C_TUPLES}#assessment:unpack_tuple_into_variables"]),
        {"gems": 15}
    )

def t2_s14():
    """recap with up_next"""
    p = f"{T2}.s14"
    p1 = prose(
        f"{p}.b01", "takeaway",
        "A list is an ordered, mutable sequence indexed from 0; slices use start-included, end-excluded bounds. "
        "A dictionary maps unique keys to values; subscripting a missing key raises a KeyError — use get() to avoid it. "
        "A tuple groups a fixed set of values that cannot be reassigned; unpacking distributes each element to its own name.",
        [C_LISTS, C_DICTS, C_TUPLES],
        [f"{C_LISTS}#f1", f"{C_LISTS}#f2", f"{C_LISTS}#f5",
         f"{C_DICTS}#f1", f"{C_DICTS}#f3",
         f"{C_TUPLES}#f1", f"{C_TUPLES}#f3"],
        [f"{C_LISTS}#tb6", f"{C_DICTS}#tb6", f"{C_TUPLES}#tb5"]
    )
    un = up_next(
        f"{p}.b02",
        "Up next: Sets and Strings",
        "In the next tile you will use sets to collect unique delivery cities with no duplicates, "
        "and f-strings to build readable messages that embed variable values."
    )
    return step(
        f"{p}", "recap",
        [C_LISTS, C_DICTS, C_TUPLES],
        "Recap",
        "What you learned",
        "Key ideas from this tile.",
        [p1, un],
        lineage([C_LISTS, C_DICTS, C_TUPLES],
                [f"{C_LISTS}#f1", f"{C_LISTS}#f2", f"{C_LISTS}#f5",
                 f"{C_DICTS}#f1", f"{C_DICTS}#f3",
                 f"{C_TUPLES}#f1", f"{C_TUPLES}#f3"],
                [f"{C_LISTS}#tb6", f"{C_DICTS}#tb6", f"{C_TUPLES}#tb5"]),
        {"gems": 5}
    )

# Remediation steps for tile 2
def t2_r01():
    """remediation for s04 (check: f3, f4 — mutability and append)"""
    p = f"{T2}.r01"
    p1 = prose(
        f"{p}.b01", "mechanism",
        "Lists are mutable: you can replace any item by assigning to its index. "
        "delivery_times[3] = 64 changes the value at index 3 in place. "
        "append() adds a new item to the end: delivery_times.append(27) grows the list by one.",
        [C_LISTS],
        [f"{C_LISTS}#f3", f"{C_LISTS}#f4"],
        [f"{C_LISTS}#tb3", f"{C_LISTS}#tb5"]
    )
    before_code = code_walk(
        f"{p}.b02.before", "python",
        "delivery_times = [32, 45, 21, 60, 18]",
        [{"start_line": 1, "end_line": 1, "text": "Original list"}]
    )
    after_code = code_walk(
        f"{p}.b02.after", "python",
        "delivery_times[3] = 64\ndelivery_times.append(27)",
        [
            {"start_line": 1, "end_line": 1, "text": "60 replaced by 64 at index 3"},
            {"start_line": 2, "end_line": 2, "text": "27 added at the end"}
        ]
    )
    ba = before_after(
        f"{p}.b02",
        before_code, after_code,
        "Index assignment replaces an item in place; append() adds a new item at the end.",
        [C_LISTS],
        [f"{C_LISTS}#f3", f"{C_LISTS}#f4"],
        [f"{C_LISTS}#tb3", f"{C_LISTS}#tb5"]
    )
    return {
        "step_id": f"{p}",
        "type": "remediation",
        "concept_ids": [C_LISTS],
        "eyebrow": "Let's revisit",
        "title": "Modifying a list and adding items",
        "lede": "A before/after showing index assignment and append() on the same list.",
        "blocks": [p1, ba],
        "lineage": lineage([C_LISTS],
                           [f"{C_LISTS}#f3", f"{C_LISTS}#f4"],
                           [f"{C_LISTS}#tb3", f"{C_LISTS}#tb5"])
    }

def t2_r02():
    """remediation for s09 (check: f3 — KeyError)"""
    p = f"{T2}.r02"
    p1 = prose(
        f"{p}.b01", "misconception",
        "Subscripting a key that is not in the dictionary raises a KeyError. "
        "order_city[9999] fails if 9999 was never added. "
        "Use get() to avoid the error: order_city.get(9999) returns None instead of crashing.",
        [C_DICTS],
        [f"{C_DICTS}#f3"],
        [f"{C_DICTS}#tb3", f"{C_DICTS}#tb4"]
    )
    left_code = code_walk(
        f"{p}.b02.left", "python",
        "order_city = {1042: 'Lagos', 1043: 'Abuja'}\norder_city[9999]",
        [
            {"start_line": 1, "end_line": 1, "text": "Dictionary with two entries"},
            {"start_line": 2, "end_line": 2, "text": "KeyError — 9999 is not a key"}
        ]
    )
    right_code = code_walk(
        f"{p}.b02.right", "python",
        "order_city = {1042: 'Lagos', 1043: 'Abuja'}\norder_city.get(9999)",
        [
            {"start_line": 1, "end_line": 1, "text": "Same dictionary"},
            {"start_line": 2, "end_line": 2, "text": "Returns None — no error raised"}
        ]
    )
    ss = side_by_side(
        f"{p}.b02",
        left_code, right_code,
        "Subscript — raises KeyError", "get() — returns None",
        "Use get() when you are not certain the key exists; it returns None (or a default) instead of raising an error.",
        [C_DICTS],
        [f"{C_DICTS}#f3"],
        [f"{C_DICTS}#tb3", f"{C_DICTS}#tb4"]
    )
    return {
        "step_id": f"{p}",
        "type": "remediation",
        "concept_ids": [C_DICTS],
        "eyebrow": "Let's revisit",
        "title": "KeyError vs get() for missing keys",
        "lede": "A side-by-side contrast between subscripting a missing key and using get().",
        "blocks": [p1, ss],
        "lineage": lineage([C_DICTS],
                           [f"{C_DICTS}#f3"],
                           [f"{C_DICTS}#tb3", f"{C_DICTS}#tb4"])
    }

def t2_r03():
    """remediation for s12 (check: m1 — one-item tuple)"""
    p = f"{T2}.r03"
    p1 = prose(
        f"{p}.b01", "misconception",
        "Enclosing a single value in parentheses does not make it a tuple — "
        "singleton = ('Lagos') is still just the string 'Lagos'. "
        "A one-item tuple requires a trailing comma: singleton = 'Lagos', "
        "or equivalently singleton = ('Lagos',).",
        [C_TUPLES],
        [f"{C_TUPLES}#m1"],
        [f"{C_TUPLES}#tb4"]
    )
    left_code = code_walk(
        f"{p}.b02.left", "python",
        "singleton = ('Lagos')\ntype(singleton)",
        [
            {"start_line": 1, "end_line": 1, "text": "Just parentheses — still a str"},
            {"start_line": 2, "end_line": 2, "text": "<class 'str'>"}
        ]
    )
    right_code = code_walk(
        f"{p}.b02.right", "python",
        "singleton = ('Lagos',)\ntype(singleton)",
        [
            {"start_line": 1, "end_line": 1, "text": "Trailing comma — this is a tuple"},
            {"start_line": 2, "end_line": 2, "text": "<class 'tuple'>"}
        ]
    )
    ss = side_by_side(
        f"{p}.b02",
        left_code, right_code,
        "('Lagos') — str, not tuple", "('Lagos',) — one-item tuple",
        "The trailing comma, not the parentheses, is what makes a one-item tuple.",
        [C_TUPLES],
        [f"{C_TUPLES}#m1"],
        [f"{C_TUPLES}#tb4"]
    )
    return {
        "step_id": f"{p}",
        "type": "remediation",
        "concept_ids": [C_TUPLES],
        "eyebrow": "Let's revisit",
        "title": "One-item tuples need a trailing comma",
        "lede": "A side-by-side contrast showing that parentheses alone do not create a tuple.",
        "blocks": [p1, ss],
        "lineage": lineage([C_TUPLES],
                           [f"{C_TUPLES}#m1"],
                           [f"{C_TUPLES}#tb4"])
    }

tile2 = {
    "tile_id": T2,
    "title": "Lists, Dictionaries, and Tuples",
    "summary": "Store ordered sequences in lists, map keys to values in dictionaries, and group fixed records in immutable tuples.",
    "steps": [
        t2_s01(), t2_s02(), t2_s03(), t2_s04(), t2_s05(),
        t2_s06(), t2_s07(), t2_s08(), t2_s09(), t2_s10(),
        t2_s11(), t2_s12(), t2_s13(),
        t2_s14()
    ],
    "remediation_steps": [
        t2_r01(), t2_r02(), t2_r03()
    ]
}

# ═══════════════════════════════════════════════════════════════════════════════
# TILE 3: tile_python_sets_strings
# ═══════════════════════════════════════════════════════════════════════════════

T3 = "tile_python_sets_strings"
C_SETS = "python.sets"
C_STR  = "python.string_basics_formatting"

def t3_s01():
    """explainer: sets, before_after visual"""
    p = f"{T3}.s01"
    p1 = prose(
        f"{p}.b01", "intro",
        "Sometimes you only care about which distinct values appear — "
        "which cities orders were delivered to, with no duplicates. "
        "A set is an unordered collection with no duplicate elements, "
        "used for membership testing and eliminating duplicate entries.",
        [C_SETS],
        [f"{C_SETS}#f1"],
        [f"{C_SETS}#tb1"]
    )
    p2 = prose(
        f"{p}.b02", "mechanism",
        "Curly braces or the set() function create a set. "
        "set() must be used for an empty set, because {} creates an empty dictionary instead. "
        "set() can also build a set from another collection: "
        "cities = set(['Lagos', 'Abuja', 'Lagos', 'Kano']) produces {'Lagos', 'Abuja', 'Kano'} — "
        "the duplicate 'Lagos' is collapsed to one entry.",
        [C_SETS],
        [f"{C_SETS}#f2", f"{C_SETS}#f3"],
        [f"{C_SETS}#tb2", f"{C_SETS}#tb3"]
    )
    before_code = code_walk(
        f"{p}.b03.before", "python",
        "cities_list = ['Lagos', 'Abuja', 'Lagos', 'Kano']",
        [{"start_line": 1, "end_line": 1, "text": "List with a repeated city"}]
    )
    after_code = code_walk(
        f"{p}.b03.after", "python",
        "cities = set(['Lagos', 'Abuja', 'Lagos', 'Kano'])",
        [{"start_line": 1, "end_line": 1, "text": "{'Lagos', 'Abuja', 'Kano'} — duplicate removed"}]
    )
    ba = before_after(
        f"{p}.b03",
        before_code, after_code,
        "Passing the list through set() collapses the repeated 'Lagos' to a single entry, leaving only unique cities.",
        [C_SETS],
        [f"{C_SETS}#f1", f"{C_SETS}#f2", f"{C_SETS}#f3"],
        [f"{C_SETS}#tb1", f"{C_SETS}#tb2", f"{C_SETS}#tb3"],
        [f"{C_SETS}#visual"]
    )
    return step(
        f"{p}", "explainer", [C_SETS],
        "Sets",
        "Unique, unordered collections",
        "A set stores only distinct values — duplicates are automatically removed.",
        [p1, p2, ba],
        lineage([C_SETS],
                [f"{C_SETS}#f1", f"{C_SETS}#f2", f"{C_SETS}#f3", f"{C_SETS}#f4"],
                [f"{C_SETS}#tb1", f"{C_SETS}#tb2", f"{C_SETS}#tb3", f"{C_SETS}#tb4"],
                [f"{C_SETS}#visual"]),
        {"gems": 5}
    )

def t3_s02():
    """video: sets"""
    p = f"{T3}.s02"
    mg = media_group(
        f"{p}.b01",
        ["seg_python.sets_r3R3h5ly_8g_26_158", "seg_python.sets_t9j8lCUGZXo_2_243"]
    )
    return step(
        f"{p}", "video", [C_SETS],
        "Watch",
        "Sets in action",
        "See set creation, membership testing and set operations demonstrated.",
        [mg],
        lineage([C_SETS],
                [f"{C_SETS}#f1", f"{C_SETS}#f2", f"{C_SETS}#f3",
                 f"{C_SETS}#f4", f"{C_SETS}#f5"],
                [],
                [],
                ["seg_python.sets_r3R3h5ly_8g_26_158", "seg_python.sets_t9j8lCUGZXo_2_243"])
    )

def t3_s03():
    """explainer: sets — set operations, tb5, f5"""
    p = f"{T3}.s03"
    p1 = prose(
        f"{p}.b01", "mechanism",
        "Set objects support mathematical operations. "
        "Union (a | b) gives all elements from both sets. "
        "Intersection (a & b) gives only the elements present in both. "
        "If week1_cities and week2_cities are two sets of cities, "
        "week1_cities & week2_cities gives the cities that appeared in both weeks.",
        [C_SETS],
        [f"{C_SETS}#f5"],
        [f"{C_SETS}#tb5"]
    )
    return step(
        f"{p}", "explainer", [C_SETS],
        "Sets",
        "Union and intersection",
        "| combines two sets; & finds what they share.",
        [p1],
        lineage([C_SETS],
                [f"{C_SETS}#f5"],
                [f"{C_SETS}#tb5"]),
        {"gems": 5}
    )

def t3_s04():
    return check_step(
        f"{T3}.s04", [C_SETS],
        "Quick check",
        "Create a set of unique values",
        "Which expression produces a set with no duplicates from a list of cities?",
        lineage([C_SETS],
                [f"{C_SETS}#f1", f"{C_SETS}#f2", f"{C_SETS}#f3"],
                [],
                [f"{C_SETS}#assessment:create_set_of_unique_values"]),
        {"gems": 10, "first_try_bonus": 5}
    )

def t3_s05():
    return check_step(
        f"{T3}.s05", [C_SETS],
        "Quick check",
        "Combine sets with union and intersection",
        "Which operator gives elements present in both sets, and which gives all elements from either?",
        lineage([C_SETS],
                [f"{C_SETS}#f5"],
                [],
                [f"{C_SETS}#assessment:combine_sets_with_union_and_intersection"]),
        {"gems": 10, "first_try_bonus": 5}
    )

def t3_s06():
    return hands_on_step(
        f"{T3}.s06", [C_SETS],
        "Practice",
        "Test membership in a set of cities",
        "Build a set of delivery cities and use in to check whether a given city is present.",
        lineage([C_SETS],
                [f"{C_SETS}#f4"],
                [],
                [f"{C_SETS}#practice",
                 f"{C_SETS}#assessment:test_set_membership"]),
        {"gems": 15}
    )

def t3_s07():
    """explainer: string basics and f-strings, before_after visual"""
    p = f"{T3}.s07"
    p1 = prose(
        f"{p}.b01", "mechanism",
        "A quote character can be embedded in a string without escaping it by using the other kind of quote. "
        "Writing \"This delivery wasn't late\" inside double quotes needs no escaping; "
        "the same text inside single quotes would need the apostrophe escaped as \\'.",
        [C_STR],
        [f"{C_STR}#f1"],
        [f"{C_STR}#tb1"]
    )
    p2 = prose(
        f"{p}.b02", "definition",
        "An f-string is a string literal prefixed with f or F that embeds the value of a Python expression "
        "inside the string by writing the expression in curly brackets: "
        "f\"Delivery to {city} took {delivery_minutes} minutes\" substitutes in the current values of city and delivery_minutes.",
        [C_STR],
        [f"{C_STR}#f2"],
        [f"{C_STR}#tb2"]
    )
    p3 = prose(
        f"{p}.b03", "mechanism",
        "An optional format specifier follows the expression after a colon, controlling how the value is displayed. "
        "f\"Average: {avg_minutes:.2f} minutes\" produces 'Average: 32.67 minutes' when avg_minutes is 32.666 — "
        "the .2f specifier rounds to two decimal places.",
        [C_STR],
        [f"{C_STR}#f3"],
        [f"{C_STR}#tb3"]
    )
    before_code = code_walk(
        f"{p}.b04.before", "python",
        "avg_minutes = 32.666\nf\"Average: {avg_minutes} minutes\"",
        [
            {"start_line": 1, "end_line": 1, "text": "avg_minutes holds 32.666"},
            {"start_line": 2, "end_line": 2, "text": "Produces: 'Average: 32.666 minutes'"}
        ]
    )
    after_code = code_walk(
        f"{p}.b04.after", "python",
        "avg_minutes = 32.666\nf\"Average: {avg_minutes:.2f} minutes\"",
        [
            {"start_line": 1, "end_line": 1, "text": "Same value"},
            {"start_line": 2, "end_line": 2, "text": "Produces: 'Average: 32.67 minutes'"}
        ]
    )
    ba = before_after(
        f"{p}.b04",
        before_code, after_code,
        "Adding :.2f after the expression rounds the output to two decimal places — the {value:.2f} part and its rounded result.",
        [C_STR],
        [f"{C_STR}#f2", f"{C_STR}#f3"],
        [f"{C_STR}#tb2", f"{C_STR}#tb3"],
        [f"{C_STR}#visual"]
    )
    return step(
        f"{p}", "explainer", [C_STR],
        "Strings and f-strings",
        "Embedding values and formatting numbers",
        "f-strings embed variable values directly in a string; a format specifier controls how numbers are displayed.",
        [p1, p2, p3, ba],
        lineage([C_STR],
                [f"{C_STR}#f1", f"{C_STR}#f2", f"{C_STR}#f3"],
                [f"{C_STR}#tb1", f"{C_STR}#tb2", f"{C_STR}#tb3"],
                [f"{C_STR}#visual"]),
        {"gems": 5}
    )

def t3_s08():
    return check_step(
        f"{T3}.s08", [C_STR],
        "Quick check",
        "Embed a quote without escaping",
        "Which string literal correctly embeds an apostrophe without a backslash escape?",
        lineage([C_STR],
                [f"{C_STR}#f1"],
                [],
                [f"{C_STR}#assessment:embed_quote_without_escaping"]),
        {"gems": 10, "first_try_bonus": 5}
    )

def t3_s09():
    return hands_on_step(
        f"{T3}.s09", [C_STR],
        "Practice",
        "Write a formatted f-string",
        "Build an f-string that reports a computed total formatted to two decimal places.",
        lineage([C_STR],
                [f"{C_STR}#f2", f"{C_STR}#f3"],
                [],
                [f"{C_STR}#practice",
                 f"{C_STR}#assessment:write_formatted_fstring"]),
        {"gems": 15}
    )

def t3_s10():
    """recap with up_next"""
    p = f"{T3}.s10"
    p1 = prose(
        f"{p}.b01", "takeaway",
        "A set stores only distinct values — pass a list through set() to remove duplicates. "
        "The in operator tests membership; | and & compute union and intersection. "
        "f-strings embed variable values with {expression}; a format specifier like :.2f controls decimal places.",
        [C_SETS, C_STR],
        [f"{C_SETS}#f1", f"{C_SETS}#f4", f"{C_STR}#f2", f"{C_STR}#f3"],
        [f"{C_SETS}#tb6", f"{C_STR}#tb4"]
    )
    un = up_next(
        f"{p}.b02",
        "Up next: Conditionals and For Loops",
        "In the next tile you will write if/elif/else chains to branch on conditions "
        "and for loops to iterate over lists and other sequences."
    )
    return step(
        f"{p}", "recap",
        [C_SETS, C_STR],
        "Recap",
        "What you learned",
        "Key ideas from this tile.",
        [p1, un],
        lineage([C_SETS, C_STR],
                [f"{C_SETS}#f1", f"{C_SETS}#f4", f"{C_STR}#f2", f"{C_STR}#f3"],
                [f"{C_SETS}#tb6", f"{C_STR}#tb4"]),
        {"gems": 5}
    )

# Remediation steps for tile 3
def t3_r01():
    """remediation for s04 (check: f1, f2, f3 — creating sets)"""
    p = f"{T3}.r01"
    p1 = prose(
        f"{p}.b01", "mechanism",
        "A set is an unordered collection with no duplicate elements. "
        "Use set() to create one from a list: set(['Lagos', 'Abuja', 'Lagos', 'Kano']) "
        "gives {'Lagos', 'Abuja', 'Kano'}. "
        "Use {} for a non-empty set literal: {'Lagos', 'Abuja'}. "
        "For an empty set, you must use set() — {} creates an empty dictionary.",
        [C_SETS],
        [f"{C_SETS}#f1", f"{C_SETS}#f2", f"{C_SETS}#f3"],
        [f"{C_SETS}#tb1", f"{C_SETS}#tb2", f"{C_SETS}#tb3"]
    )
    before_code = code_walk(
        f"{p}.b02.before", "python",
        "cities = ['Lagos', 'Abuja', 'Lagos', 'Kano']\nlen(cities)",
        [
            {"start_line": 1, "end_line": 1, "text": "List — 4 items, with a duplicate"},
            {"start_line": 2, "end_line": 2, "text": "4"}
        ]
    )
    after_code = code_walk(
        f"{p}.b02.after", "python",
        "cities = set(['Lagos', 'Abuja', 'Lagos', 'Kano'])\nlen(cities)",
        [
            {"start_line": 1, "end_line": 1, "text": "Set — duplicate removed"},
            {"start_line": 2, "end_line": 2, "text": "3"}
        ]
    )
    ba = before_after(
        f"{p}.b02",
        before_code, after_code,
        "Converting the list to a set removes the duplicate 'Lagos', reducing the count from 4 to 3.",
        [C_SETS],
        [f"{C_SETS}#f1", f"{C_SETS}#f2", f"{C_SETS}#f3"],
        [f"{C_SETS}#tb1", f"{C_SETS}#tb2", f"{C_SETS}#tb3"]
    )
    return {
        "step_id": f"{p}",
        "type": "remediation",
        "concept_ids": [C_SETS],
        "eyebrow": "Let's revisit",
        "title": "Creating a set and removing duplicates",
        "lede": "A before/after showing how set() collapses duplicates from a list.",
        "blocks": [p1, ba],
        "lineage": lineage([C_SETS],
                           [f"{C_SETS}#f1", f"{C_SETS}#f2", f"{C_SETS}#f3"],
                           [f"{C_SETS}#tb1", f"{C_SETS}#tb2", f"{C_SETS}#tb3"])
    }

def t3_r02():
    """remediation for s05 (check: f5 — union and intersection)"""
    p = f"{T3}.r02"
    p1 = prose(
        f"{p}.b01", "mechanism",
        "| (union) gives all elements from either set — no duplicates. "
        "& (intersection) gives only the elements present in both sets. "
        "If week1_cities = {'Lagos', 'Abuja'} and week2_cities = {'Abuja', 'Kano'}, "
        "then week1_cities | week2_cities is {'Lagos', 'Abuja', 'Kano'} "
        "and week1_cities & week2_cities is {'Abuja'}.",
        [C_SETS],
        [f"{C_SETS}#f5"],
        [f"{C_SETS}#tb5"]
    )
    left_code = code_walk(
        f"{p}.b02.left", "python",
        "week1 = {'Lagos', 'Abuja'}\nweek2 = {'Abuja', 'Kano'}\nweek1 | week2",
        [
            {"start_line": 1, "end_line": 1, "text": "Week 1 cities"},
            {"start_line": 2, "end_line": 2, "text": "Week 2 cities"},
            {"start_line": 3, "end_line": 3, "text": "{'Lagos', 'Abuja', 'Kano'} — all cities"}
        ]
    )
    right_code = code_walk(
        f"{p}.b02.right", "python",
        "week1 = {'Lagos', 'Abuja'}\nweek2 = {'Abuja', 'Kano'}\nweek1 & week2",
        [
            {"start_line": 1, "end_line": 1, "text": "Week 1 cities"},
            {"start_line": 2, "end_line": 2, "text": "Week 2 cities"},
            {"start_line": 3, "end_line": 3, "text": "{'Abuja'} — only the shared city"}
        ]
    )
    ss = side_by_side(
        f"{p}.b02",
        left_code, right_code,
        "| union — all cities from either", "& intersection — only shared cities",
        "| combines both sets; & keeps only what they have in common.",
        [C_SETS],
        [f"{C_SETS}#f5"],
        [f"{C_SETS}#tb5"]
    )
    return {
        "step_id": f"{p}",
        "type": "remediation",
        "concept_ids": [C_SETS],
        "eyebrow": "Let's revisit",
        "title": "Union and intersection on sets",
        "lede": "A side-by-side contrast showing | and & on the same two sets.",
        "blocks": [p1, ss],
        "lineage": lineage([C_SETS],
                           [f"{C_SETS}#f5"],
                           [f"{C_SETS}#tb5"])
    }

def t3_r03():
    """remediation for s08 (check: f1 — quote embedding)"""
    p = f"{T3}.r03"
    p1 = prose(
        f"{p}.b01", "mechanism",
        "A quote character can be embedded in a string without escaping it by enclosing the string "
        "in the other kind of quote. "
        "\"This delivery wasn't late\" uses double quotes, so the apostrophe in wasn't needs no backslash. "
        "Inside single quotes the same apostrophe would need escaping: 'This delivery wasn\\'t late'.",
        [C_STR],
        [f"{C_STR}#f1"],
        [f"{C_STR}#tb1"]
    )
    left_code = code_walk(
        f"{p}.b02.left", "python",
        "'This delivery wasn\\'t late'",
        [{"start_line": 1, "end_line": 1, "text": "Backslash needed inside single quotes"}]
    )
    right_code = code_walk(
        f"{p}.b02.right", "python",
        "\"This delivery wasn't late\"",
        [{"start_line": 1, "end_line": 1, "text": "No backslash needed — double quotes wrap the string"}]
    )
    ss = side_by_side(
        f"{p}.b02",
        left_code, right_code,
        "Single quotes — escape needed", "Double quotes — no escape needed",
        "Switching to the other kind of quote avoids the need to escape the embedded quote character.",
        [C_STR],
        [f"{C_STR}#f1"],
        [f"{C_STR}#tb1"]
    )
    return {
        "step_id": f"{p}",
        "type": "remediation",
        "concept_ids": [C_STR],
        "eyebrow": "Let's revisit",
        "title": "Embedding a quote without escaping",
        "lede": "A side-by-side contrast showing the same string with and without an escape.",
        "blocks": [p1, ss],
        "lineage": lineage([C_STR],
                           [f"{C_STR}#f1"],
                           [f"{C_STR}#tb1"])
    }

tile3 = {
    "tile_id": T3,
    "title": "Sets and Strings",
    "summary": "Use sets to collect unique values and test membership, combine sets with union and intersection, and build readable messages with f-strings and format specifiers.",
    "steps": [
        t3_s01(), t3_s02(), t3_s03(),
        t3_s04(), t3_s05(), t3_s06(),
        t3_s07(), t3_s08(), t3_s09(),
        t3_s10()
    ],
    "remediation_steps": [
        t3_r01(), t3_r02(), t3_r03()
    ]
}

# ═══════════════════════════════════════════════════════════════════════════════
# Assemble and write
# ═══════════════════════════════════════════════════════════════════════════════

output = {
    "schema_version": "0.1.0",
    "kind": "screens_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_008_da_python_core",
    "tiles": [tile1, tile2, tile3]
}

OUT.write_text(json.dumps(output, indent=2, ensure_ascii=False))
print(f"Written: {OUT}")

# Print step counts
for tile in output["tiles"]:
    steps = tile["steps"]
    rem = tile.get("remediation_steps", [])
    print(f"  {tile['tile_id']}: {len(steps)} steps, {len(rem)} remediation steps")
    for s in steps:
        print(f"    {s['step_id']} ({s['type']})")
