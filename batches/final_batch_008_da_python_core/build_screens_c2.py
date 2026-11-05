"""Build screens.part.c2.json for tile_python_conditionals_for_loops,
tile_python_while_loop_control, tile_python_comprehensions_iterating."""
import json

# ── helpers ──────────────────────────────────────────────────────────────────
def prose(block_id, text, role, concept_ids, fact_ids, teaching_block_ids, anchors=None):
    b = {"type": "prose", "block_id": block_id, "text": text, "role": role,
         "lineage": {"concept_ids": concept_ids, "fact_ids": fact_ids,
                     "teaching_block_ids": teaching_block_ids}}
    if anchors:
        b["lineage"]["anchors"] = anchors
    return b

def heading(block_id, text, level=2):
    return {"type": "heading", "block_id": block_id, "text": text, "level": level}

# ═══════════════════════════════════════════════════════════════════════════════
# TILE 1: tile_python_conditionals_for_loops
# ═══════════════════════════════════════════════════════════════════════════════

# ── s01 explainer: conditional_statements (tb1-tb4, f1-f4, visual=process_flow) ──
cond_s01_blocks = [
    heading("tile_python_conditionals_for_loops.s01.h1",
            "Branching on data: if, elif, else"),
    prose(
        "tile_python_conditionals_for_loops.s01.p1",
        "Not every line of code should always run — sometimes what happens next depends on the data. "
        "An if statement executes its block only when its condition is true. "
        "You can add zero or more elif parts after an if, and an optional else at the end; "
        "elif is short for 'else if' and keeps the code flat instead of deeply nested.",
        "mechanism",
        ["python.conditional_statements"],
        ["python.conditional_statements#f1", "python.conditional_statements#f2"],
        ["python.conditional_statements#tb1", "python.conditional_statements#tb2"]
    ),
    prose(
        "tile_python_conditionals_for_loops.s01.p2",
        "An if/elif/else chain selects exactly one block by evaluating conditions top to bottom "
        "until one is true; if none are true, the else block (if present) runs. "
        "Each condition ends with a colon, and the block belonging to that branch is indented beneath it:\n\n"
        "if delivery_minutes < 15:\n"
        "    category = 'fast'\n"
        "elif delivery_minutes < 45:\n"
        "    category = 'normal'\n"
        "else:\n"
        "    category = 'slow'\n\n"
        "With delivery_minutes = 30, the first condition is false and the second is true, "
        "so category becomes 'normal' and the else branch is skipped.",
        "syntax",
        ["python.conditional_statements"],
        ["python.conditional_statements#f3", "python.conditional_statements#f4"],
        ["python.conditional_statements#tb3", "python.conditional_statements#tb4"]
    ),
    # process_flow visual — decision flow for delivery_minutes = 30
    {
        "type": "process_flow",
        "block_id": "tile_python_conditionals_for_loops.s01.pf1",
        "title": "Which branch runs for delivery_minutes = 30?",
        "direction": "TB",
        "nodes": [
            {"id": "start", "label": "delivery_minutes = 30", "kind": "start"},
            {"id": "cond1", "label": "delivery_minutes < 15?", "kind": "decision"},
            {"id": "fast",  "label": "category = 'fast'",   "kind": "step",
             "detail": "skipped — condition is false"},
            {"id": "cond2", "label": "delivery_minutes < 45?", "kind": "decision"},
            {"id": "normal","label": "category = 'normal'", "kind": "step",
             "detail": "runs — condition is true"},
            {"id": "slow",  "label": "category = 'slow'",   "kind": "step",
             "detail": "skipped — earlier branch matched"},
            {"id": "end",   "label": "category = 'normal'", "kind": "end"}
        ],
        "edges": [
            {"from": "start",  "to": "cond1"},
            {"from": "cond1",  "to": "fast",   "label": "True",  "kind": "yes"},
            {"from": "cond1",  "to": "cond2",  "label": "False", "kind": "no"},
            {"from": "fast",   "to": "end",    "kind": "next"},
            {"from": "cond2",  "to": "normal", "label": "True",  "kind": "yes"},
            {"from": "cond2",  "to": "slow",   "label": "False", "kind": "no"},
            {"from": "normal", "to": "end",    "kind": "next"},
            {"from": "slow",   "to": "end",    "kind": "next"}
        ],
        "reveal": "stepwise",
        "alt_text": "Decision flow: delivery_minutes = 30 fails the first condition (< 15), passes the second (< 45), so category = 'normal' runs and the else branch is skipped.",
        "lineage": {
            "concept_ids": ["python.conditional_statements"],
            "fact_ids": ["python.conditional_statements#f3", "python.conditional_statements#f4"],
            "teaching_block_ids": ["python.conditional_statements#tb4"],
            "anchors": ["python.conditional_statements#visual"]
        }
    }
]

# ── s02 check: explain_when_if_block_runs (framing only) ──
cond_s02 = {
    "step_id": "tile_python_conditionals_for_loops.s02",
    "type": "check",
    "concept_ids": ["python.conditional_statements"],
    "eyebrow": "Quick check",
    "title": "When does an if block run?",
    "lede": "Choose the correct description of when an if statement executes its block.",
    "reward": {"gems": 5},
    "lineage": {
        "fact_ids": ["python.conditional_statements#f1"],
        "teaching_block_ids": [],
        "anchors": ["python.conditional_statements#assessment:explain_when_if_block_runs"]
    }
}

# ── s03 check: predict_branch_taken (framing only) ──
cond_s03 = {
    "step_id": "tile_python_conditionals_for_loops.s03",
    "type": "check",
    "concept_ids": ["python.conditional_statements"],
    "eyebrow": "Quick check",
    "title": "Which branch runs?",
    "lede": "Given a delivery time, predict which branch of an if/elif/else chain executes.",
    "reward": {"gems": 5},
    "lineage": {
        "fact_ids": ["python.conditional_statements#f3"],
        "teaching_block_ids": [],
        "anchors": ["python.conditional_statements#assessment:predict_branch_taken"]
    }
}

# ── s04 hands_on: write_if_elif_else_chain (framing only) ──
cond_s04 = {
    "step_id": "tile_python_conditionals_for_loops.s04",
    "type": "hands_on",
    "concept_ids": ["python.conditional_statements"],
    "eyebrow": "Practice",
    "title": "Write an if/elif/else chain",
    "lede": "Use the QuickDeliver dataset to write a chain that categorises each delivery as fast, normal, or slow.",
    "reward": {"gems": 10, "first_try_bonus": 5},
    "lineage": {
        "fact_ids": [
            "python.conditional_statements#f2",
            "python.conditional_statements#f3",
            "python.conditional_statements#f4"
        ],
        "teaching_block_ids": [],
        "anchors": [
            "python.conditional_statements#practice",
            "python.conditional_statements#assessment:write_if_elif_else_chain"
        ]
    }
}

# ── s05 explainer: for_loops (tb1-tb4, f1-f3, visual=process_flow) ──
for_s05_blocks = [
    heading("tile_python_conditionals_for_loops.s05.h1",
            "Visiting every item: the for loop"),
    prose(
        "tile_python_conditionals_for_loops.s05.p1",
        "Once delivery times are collected in a list, you'll want to do something with every single one "
        "of them, not just one at a time by hand. Python's for statement iterates over the items of any "
        "sequence — such as a list or a string — in the order they appear. "
        "Each pass binds the loop variable to the next item:\n\n"
        "for minutes in delivery_times:\n"
        "    print(minutes)\n\n"
        "This prints every delivery time in delivery_times, one per pass.",
        "mechanism",
        ["python.for_loops"],
        ["python.for_loops#f1", "python.for_loops#f2"],
        ["python.for_loops#tb1", "python.for_loops#tb2"]
    ),
    prose(
        "tile_python_conditionals_for_loops.s05.p2",
        "The header line ends with a colon, and the statements to repeat are indented beneath it. "
        "You can combine a for loop with a conditional check inside the body:\n\n"
        "for minutes in delivery_times:\n"
        "    if minutes > 45:\n"
        "        print(minutes)\n\n"
        "With delivery_times = [32, 45, 21, 60, 18], this prints only 60 — the one delivery time above 45 minutes.",
        "syntax",
        ["python.for_loops"],
        ["python.for_loops#f2", "python.for_loops#f3"],
        ["python.for_loops#tb3", "python.for_loops#tb4"]
    ),
    # process_flow visual — loop flow
    {
        "type": "process_flow",
        "block_id": "tile_python_conditionals_for_loops.s05.pf1",
        "title": "How a for loop steps through delivery_times",
        "direction": "TB",
        "nodes": [
            {"id": "start",   "label": "delivery_times = [32, 45, 21, 60, 18]", "kind": "start"},
            {"id": "check",   "label": "Next item available?", "kind": "decision"},
            {"id": "bind",    "label": "minutes = next item", "kind": "step",
             "detail": "e.g. 32, then 45, then 21 …"},
            {"id": "body",    "label": "run loop body", "kind": "step",
             "detail": "print(minutes)"},
            {"id": "end",     "label": "loop finished", "kind": "end"}
        ],
        "edges": [
            {"from": "start", "to": "check"},
            {"from": "check", "to": "bind",  "label": "Yes", "kind": "yes"},
            {"from": "check", "to": "end",   "label": "No",  "kind": "no"},
            {"from": "bind",  "to": "body",  "kind": "next"},
            {"from": "body",  "to": "check", "kind": "loop_back"}
        ],
        "reveal": "stepwise",
        "alt_text": "Loop flow: check for next item, bind minutes to it, run the body, loop back; exit when no items remain.",
        "lineage": {
            "concept_ids": ["python.for_loops"],
            "fact_ids": ["python.for_loops#f1", "python.for_loops#f2", "python.for_loops#f3"],
            "teaching_block_ids": ["python.for_loops#tb2", "python.for_loops#tb3"],
            "anchors": ["python.for_loops#visual"]
        }
    }
]

# ── s06 video: for_loops ──
for_s06_blocks = [
    {
        "type": "media_group",
        "block_id": "tile_python_conditionals_for_loops.s06.mg1",
        "group_title": "Stepping through a list with a for loop",
        "segment_ids": ["seg_python.for_loops_zmIdC0_0BgY_0_207"]
    }
]

# ── s07 check: trace_loop_variable_each_pass (framing only) ──
for_s07 = {
    "step_id": "tile_python_conditionals_for_loops.s07",
    "type": "check",
    "concept_ids": ["python.for_loops"],
    "eyebrow": "Quick check",
    "title": "Trace the loop variable",
    "lede": "What value does the loop variable hold on each pass through the list?",
    "reward": {"gems": 5},
    "lineage": {
        "fact_ids": ["python.for_loops#f2"],
        "teaching_block_ids": [],
        "anchors": ["python.for_loops#assessment:trace_loop_variable_each_pass"]
    }
}

# ── s08 hands_on: write_for_loop_over_collection (framing only) ──
for_s08 = {
    "step_id": "tile_python_conditionals_for_loops.s08",
    "type": "hands_on",
    "concept_ids": ["python.for_loops"],
    "eyebrow": "Practice",
    "title": "Write a for loop over a collection",
    "lede": "Loop over the delivery_times list and print each time that exceeds 45 minutes.",
    "reward": {"gems": 10, "first_try_bonus": 5},
    "lineage": {
        "fact_ids": [
            "python.for_loops#f1",
            "python.for_loops#f2",
            "python.for_loops#f3"
        ],
        "teaching_block_ids": [],
        "anchors": [
            "python.for_loops#practice",
            "python.for_loops#assessment:write_for_loop_over_collection"
        ]
    }
}

# ── s09 recap ──
cond_s09_blocks = [
    prose(
        "tile_python_conditionals_for_loops.s09.p1",
        "Reading top to bottom, exactly one branch of an if/elif/else chain runs for any given delivery time — "
        "the first whose condition is true, or else if none are. "
        "A for loop visits every item of a sequence such as a list once, in the order the items appear, "
        "which is what you need to process each delivery time in turn.",
        "takeaway",
        ["python.conditional_statements", "python.for_loops"],
        ["python.conditional_statements#f3", "python.for_loops#f1"],
        ["python.conditional_statements#tb5", "python.for_loops#tb5"]
    ),
    {
        "type": "up_next",
        "block_id": "tile_python_conditionals_for_loops.s09.un1",
        "title": "Up next: While Loops and Loop Control",
        "text": "Next you'll learn how to keep a loop running as long as a condition holds — and how to exit or skip iterations mid-loop."
    }
]

# ── remediation steps ──
# r01: for s02 (check: explain_when_if_block_runs, measures f1)
cond_r01_blocks = [
    heading("tile_python_conditionals_for_loops.r01.h1",
            "Reminder: when does an if block run?"),
    prose(
        "tile_python_conditionals_for_loops.r01.p1",
        "An if statement executes its block only when its condition is true — not every time the code runs. "
        "If delivery_minutes = 30 and the condition is delivery_minutes > 45, the block is skipped entirely. "
        "The block runs only when the condition evaluates to True.",
        "mechanism",
        ["python.conditional_statements"],
        ["python.conditional_statements#f1"],
        ["python.conditional_statements#tb1"]
    )
]

# r02: for s03 (check: predict_branch_taken, measures f3)
cond_r02_blocks = [
    heading("tile_python_conditionals_for_loops.r02.h1",
            "Reminder: which branch runs in a chain?"),
    prose(
        "tile_python_conditionals_for_loops.r02.p1",
        "An if/elif/else chain evaluates conditions one by one from top to bottom. "
        "The first condition that is true wins — its block runs and all others are skipped. "
        "If no condition is true, the else block (if present) runs. "
        "With delivery_minutes = 30: the first condition (< 15) is false, the second (< 45) is true, "
        "so category = 'normal' runs and the else branch is skipped.",
        "mechanism",
        ["python.conditional_statements"],
        ["python.conditional_statements#f3"],
        ["python.conditional_statements#tb3"]
    )
]

# r03: for s07 (check: trace_loop_variable_each_pass, measures f2)
for_r03_blocks = [
    heading("tile_python_conditionals_for_loops.r03.h1",
            "Reminder: what value does the loop variable hold?"),
    prose(
        "tile_python_conditionals_for_loops.r03.p1",
        "Each pass through a for loop binds the loop variable to the next item of the sequence. "
        "With delivery_times = [32, 45, 21, 60, 18], the first pass sets minutes = 32, "
        "the second sets minutes = 45, and so on. "
        "The variable takes each value in order, one per pass.",
        "mechanism",
        ["python.for_loops"],
        ["python.for_loops#f2"],
        ["python.for_loops#tb2"]
    )
]

tile_conditionals_for_loops = {
    "tile_id": "tile_python_conditionals_for_loops",
    "title": "Conditionals and For Loops",
    "steps": [
        {
            "step_id": "tile_python_conditionals_for_loops.s01",
            "type": "explainer",
            "concept_ids": ["python.conditional_statements"],
            "eyebrow": "Control flow",
            "title": "Branching on data: if, elif, else",
            "lede": "Make your code choose the right path based on each delivery's data.",
            "blocks": cond_s01_blocks,
            "reward": {"gems": 5},
            "lineage": {
                "fact_ids": [
                    "python.conditional_statements#f1",
                    "python.conditional_statements#f2",
                    "python.conditional_statements#f3",
                    "python.conditional_statements#f4"
                ],
                "teaching_block_ids": [
                    "python.conditional_statements#tb1",
                    "python.conditional_statements#tb2",
                    "python.conditional_statements#tb3",
                    "python.conditional_statements#tb4"
                ],
                "anchors": ["python.conditional_statements#visual"]
            }
        },
        cond_s02,
        cond_s03,
        cond_s04,
        {
            "step_id": "tile_python_conditionals_for_loops.s05",
            "type": "explainer",
            "concept_ids": ["python.for_loops"],
            "eyebrow": "Iteration",
            "title": "Visiting every item: the for loop",
            "lede": "Process every delivery time in a list without writing the same code over and over.",
            "blocks": for_s05_blocks,
            "reward": {"gems": 5},
            "lineage": {
                "fact_ids": [
                    "python.for_loops#f1",
                    "python.for_loops#f2",
                    "python.for_loops#f3"
                ],
                "teaching_block_ids": [
                    "python.for_loops#tb1",
                    "python.for_loops#tb2",
                    "python.for_loops#tb3",
                    "python.for_loops#tb4"
                ],
                "anchors": ["python.for_loops#visual"]
            }
        },
        {
            "step_id": "tile_python_conditionals_for_loops.s06",
            "type": "video",
            "concept_ids": ["python.for_loops"],
            "eyebrow": "Watch",
            "title": "Stepping through a list with a for loop",
            "lede": "See the loop variable take each value in turn.",
            "blocks": for_s06_blocks,
            "lineage": {
                "fact_ids": [
                    "python.for_loops#f1",
                    "python.for_loops#f2",
                    "python.for_loops#f3"
                ],
                "teaching_block_ids": [],
                "segment_ids": ["seg_python.for_loops_zmIdC0_0BgY_0_207"]
            }
        },
        for_s07,
        for_s08,
        {
            "step_id": "tile_python_conditionals_for_loops.s09",
            "type": "recap",
            "concept_ids": ["python.conditional_statements", "python.for_loops"],
            "eyebrow": "Recap",
            "title": "What you've learned",
            "lede": "One branch, every item.",
            "blocks": cond_s09_blocks,
            "reward": {"gems": 5},
            "lineage": {
                "fact_ids": [
                    "python.conditional_statements#f3",
                    "python.for_loops#f1"
                ],
                "teaching_block_ids": [
                    "python.conditional_statements#tb5",
                    "python.for_loops#tb5"
                ]
            }
        }
    ],
    "remediation_steps": [
        {
            "step_id": "tile_python_conditionals_for_loops.r01",
            "type": "remediation",
            "concept_ids": ["python.conditional_statements"],
            "title": "When does an if block run?",
            "lede": "Let's revisit the rule for when an if block executes.",
            "blocks": cond_r01_blocks,
            "lineage": {
                "fact_ids": ["python.conditional_statements#f1"],
                "teaching_block_ids": ["python.conditional_statements#tb1"],
                "anchors": ["python.conditional_statements#assessment:explain_when_if_block_runs"]
            }
        },
        {
            "step_id": "tile_python_conditionals_for_loops.r02",
            "type": "remediation",
            "concept_ids": ["python.conditional_statements"],
            "title": "Which branch runs in a chain?",
            "lede": "Let's revisit how an if/elif/else chain selects exactly one branch.",
            "blocks": cond_r02_blocks,
            "lineage": {
                "fact_ids": ["python.conditional_statements#f3"],
                "teaching_block_ids": ["python.conditional_statements#tb3"],
                "anchors": ["python.conditional_statements#assessment:predict_branch_taken"]
            }
        },
        {
            "step_id": "tile_python_conditionals_for_loops.r03",
            "type": "remediation",
            "concept_ids": ["python.for_loops"],
            "title": "What value does the loop variable hold?",
            "lede": "Let's revisit how the loop variable takes each value in turn.",
            "blocks": for_r03_blocks,
            "lineage": {
                "fact_ids": ["python.for_loops#f2"],
                "teaching_block_ids": ["python.for_loops#tb2"],
                "anchors": ["python.for_loops#assessment:trace_loop_variable_each_pass"]
            }
        }
    ]
}


# ═══════════════════════════════════════════════════════════════════════════════
# TILE 2: tile_python_while_loop_control
# ═══════════════════════════════════════════════════════════════════════════════

# ── s01 explainer: while_loops (tb1-tb3, f1-f2, visual=process_flow) ──
while_s01_blocks = [
    heading("tile_python_while_loop_control.s01.h1",
            "Repeating while a condition holds: the while loop"),
    prose(
        "tile_python_while_loop_control.s01.p1",
        "Sometimes you don't know in advance how many times you'll need to repeat something — "
        "you just want to keep going as long as some condition holds. "
        "A while loop executes its body repeatedly as long as its condition remains true; "
        "the condition can be a comparison, such as a < 10.",
        "intro",
        ["python.while_loops"],
        ["python.while_loops#f1"],
        ["python.while_loops#tb1"]
    ),
    prose(
        "tile_python_while_loop_control.s01.p2",
        "The body is indented beneath the while line, and something in the body must change what "
        "the condition checks — otherwise the loop never stops:\n\n"
        "pending = 3\n"
        "while pending > 0:\n"
        "    print('deliveries left:', pending)\n"
        "    pending = pending - 1\n\n"
        "Each pass prints the current count and decreases pending by 1, "
        "so the loop stops once pending reaches 0.",
        "mechanism",
        ["python.while_loops"],
        ["python.while_loops#f2"],
        ["python.while_loops#tb2", "python.while_loops#tb3"]
    ),
    # process_flow visual
    {
        "type": "process_flow",
        "block_id": "tile_python_while_loop_control.s01.pf1",
        "title": "How a while loop re-checks its condition each pass",
        "direction": "TB",
        "nodes": [
            {"id": "init",   "label": "pending = 3",          "kind": "start"},
            {"id": "cond",   "label": "pending > 0?",         "kind": "decision"},
            {"id": "body1",  "label": "print('deliveries left:', pending)", "kind": "step"},
            {"id": "update", "label": "pending = pending - 1", "kind": "step",
             "detail": "update must change what the condition checks"},
            {"id": "end",    "label": "loop finished (pending = 0)", "kind": "end"}
        ],
        "edges": [
            {"from": "init",   "to": "cond"},
            {"from": "cond",   "to": "body1",  "label": "True",  "kind": "yes"},
            {"from": "cond",   "to": "end",    "label": "False", "kind": "no"},
            {"from": "body1",  "to": "update", "kind": "next"},
            {"from": "update", "to": "cond",   "kind": "loop_back"}
        ],
        "reveal": "stepwise",
        "alt_text": "While loop flow: initialise pending = 3, check pending > 0, run body and decrement, loop back to check; exit when pending = 0.",
        "lineage": {
            "concept_ids": ["python.while_loops"],
            "fact_ids": ["python.while_loops#f1", "python.while_loops#f2"],
            "teaching_block_ids": ["python.while_loops#tb2", "python.while_loops#tb3"],
            "anchors": ["python.while_loops#visual"]
        }
    }
]

# ── s02 video: while_loops ──
while_s02_blocks = [
    {
        "type": "media_group",
        "block_id": "tile_python_while_loop_control.s02.mg1",
        "group_title": "A while loop as a counter",
        "segment_ids": ["seg_python.while_loops_gD8ePxAhjUM_178_421"]
    }
]

# ── s03 check: update_state_so_loop_terminates (framing only) ──
while_s03 = {
    "step_id": "tile_python_while_loop_control.s03",
    "type": "check",
    "concept_ids": ["python.while_loops"],
    "eyebrow": "Quick check",
    "title": "Making a while loop terminate",
    "lede": "Which change to the loop body ensures the loop eventually stops?",
    "reward": {"gems": 5},
    "lineage": {
        "fact_ids": ["python.while_loops#f2"],
        "teaching_block_ids": [],
        "anchors": ["python.while_loops#assessment:update_state_so_loop_terminates"]
    }
}

# ── s04 hands_on: write_while_loop_with_condition (framing only) ──
while_s04 = {
    "step_id": "tile_python_while_loop_control.s04",
    "type": "hands_on",
    "concept_ids": ["python.while_loops"],
    "eyebrow": "Practice",
    "title": "Write a while loop with a condition",
    "lede": "Write a while loop that counts down pending deliveries until none remain.",
    "reward": {"gems": 10, "first_try_bonus": 5},
    "lineage": {
        "fact_ids": ["python.while_loops#f1"],
        "teaching_block_ids": [],
        "anchors": [
            "python.while_loops#practice",
            "python.while_loops#assessment:write_while_loop_with_condition"
        ]
    }
}

# ── s05 explainer: loop_control (tb1-tb2, f1-f2, visual=process_flow) ──
ctrl_s05_blocks = [
    heading("tile_python_while_loop_control.s05.h1",
            "Steering mid-loop: break and continue"),
    prose(
        "tile_python_while_loop_control.s05.p1",
        "The break statement exits the innermost enclosing for or while loop immediately — "
        "useful for stopping a search over delivery orders as soon as the one you want is found. "
        "The continue statement skips the rest of the current iteration and moves to the next one — "
        "for example, skipping a delivery record that's missing a time without exiting the whole loop.",
        "mechanism",
        ["python.loop_control"],
        ["python.loop_control#f1", "python.loop_control#f2"],
        ["python.loop_control#tb1", "python.loop_control#tb2"]
    ),
    # process_flow visual — loop with break and continue exits
    {
        "type": "process_flow",
        "block_id": "tile_python_while_loop_control.s05.pf1",
        "title": "break exits the loop; continue skips to the next item",
        "direction": "TB",
        "nodes": [
            {"id": "start",    "label": "start loop",          "kind": "start"},
            {"id": "next_item","label": "next item available?", "kind": "decision"},
            {"id": "body",     "label": "run body",             "kind": "step"},
            {"id": "cont_dec", "label": "continue condition?",  "kind": "decision",
             "detail": "e.g. missing delivery time"},
            {"id": "brk_dec",  "label": "break condition?",     "kind": "decision",
             "detail": "e.g. target order found"},
            {"id": "end_loop", "label": "loop finished",        "kind": "end"},
            {"id": "end_break","label": "exited by break",      "kind": "end"}
        ],
        "edges": [
            {"from": "start",     "to": "next_item"},
            {"from": "next_item", "to": "body",      "label": "Yes", "kind": "yes"},
            {"from": "next_item", "to": "end_loop",  "label": "No",  "kind": "no"},
            {"from": "body",      "to": "cont_dec",  "kind": "next"},
            {"from": "cont_dec",  "to": "next_item", "label": "continue", "kind": "loop_back"},
            {"from": "cont_dec",  "to": "brk_dec",   "label": "No",       "kind": "no"},
            {"from": "brk_dec",   "to": "end_break", "label": "break",    "kind": "branch"},
            {"from": "brk_dec",   "to": "next_item", "label": "No",       "kind": "loop_back"}
        ],
        "reveal": "all",
        "alt_text": "Loop flow with two side exits: continue jumps back to the next item check, break exits the loop entirely.",
        "lineage": {
            "concept_ids": ["python.loop_control"],
            "fact_ids": ["python.loop_control#f1", "python.loop_control#f2"],
            "teaching_block_ids": ["python.loop_control#tb1", "python.loop_control#tb2"],
            "anchors": ["python.loop_control#visual"]
        }
    }
]

# ── s06 check: skip_iteration_with_continue (framing only) ──
ctrl_s06 = {
    "step_id": "tile_python_while_loop_control.s06",
    "type": "check",
    "concept_ids": ["python.loop_control"],
    "eyebrow": "Quick check",
    "title": "Skip an iteration with continue",
    "lede": "Which statement skips the rest of the current iteration and moves to the next?",
    "reward": {"gems": 5},
    "lineage": {
        "fact_ids": ["python.loop_control#f2"],
        "teaching_block_ids": [],
        "anchors": ["python.loop_control#assessment:skip_iteration_with_continue"]
    }
}

# ── s07 hands_on: exit_loop_early_with_break + skip_iteration_with_continue (framing only) ──
ctrl_s07 = {
    "step_id": "tile_python_while_loop_control.s07",
    "type": "hands_on",
    "concept_ids": ["python.loop_control"],
    "eyebrow": "Practice",
    "title": "Use break and continue in a loop",
    "lede": "Write a loop that skips orders with missing times and stops as soon as a late order is found.",
    "reward": {"gems": 10, "first_try_bonus": 5},
    "lineage": {
        "fact_ids": [
            "python.loop_control#f1",
            "python.loop_control#f2"
        ],
        "teaching_block_ids": [],
        "anchors": [
            "python.loop_control#practice",
            "python.loop_control#assessment:exit_loop_early_with_break",
            "python.loop_control#assessment:skip_iteration_with_continue"
        ]
    }
}

# ── s08 recap ──
while_s08_blocks = [
    prose(
        "tile_python_while_loop_control.s08.p1",
        "Unlike a for loop, which is bound to a known collection, a while loop keeps running purely "
        "based on its condition — so the code inside it must eventually make that condition false or "
        "the loop never stops. "
        "Use break to exit a loop early and continue to skip the rest of the current iteration.",
        "takeaway",
        ["python.while_loops", "python.loop_control"],
        ["python.while_loops#f1", "python.while_loops#f2"],
        ["python.while_loops#tb4"]
    ),
    {
        "type": "up_next",
        "block_id": "tile_python_while_loop_control.s08.un1",
        "title": "Up next: Comprehensions and Iterating Collections",
        "text": "Next you'll learn how to build lists and dictionaries in a single expression, and how to loop over any of Python's core collection types."
    }
]

# ── remediation steps ──
# r01: for s03 (check: update_state_so_loop_terminates, measures f2)
while_r01_blocks = [
    heading("tile_python_while_loop_control.r01.h1",
            "Reminder: the body must change what the condition checks"),
    prose(
        "tile_python_while_loop_control.r01.p1",
        "The body of a while loop must change what the condition checks — otherwise the condition "
        "stays true forever and the loop never stops. "
        "In the pending example, pending = pending - 1 decreases pending each pass, "
        "so pending > 0 eventually becomes false and the loop exits.",
        "mechanism",
        ["python.while_loops"],
        ["python.while_loops#f2"],
        ["python.while_loops#tb2"]
    )
]

# r02: for s06 (check: skip_iteration_with_continue, measures f2)
ctrl_r02_blocks = [
    heading("tile_python_while_loop_control.r02.h1",
            "Reminder: continue vs break"),
    prose(
        "tile_python_while_loop_control.r02.p1",
        "continue skips the rest of the current iteration and moves to the next one — "
        "the loop keeps running. "
        "break exits the innermost loop entirely — no more iterations happen. "
        "Use continue to skip a bad record; use break to stop searching once you've found what you need.",
        "mechanism",
        ["python.loop_control"],
        ["python.loop_control#f1", "python.loop_control#f2"],
        ["python.loop_control#tb1", "python.loop_control#tb2"]
    )
]

tile_while_loop_control = {
    "tile_id": "tile_python_while_loop_control",
    "title": "While Loops and Loop Control",
    "steps": [
        {
            "step_id": "tile_python_while_loop_control.s01",
            "type": "explainer",
            "concept_ids": ["python.while_loops"],
            "eyebrow": "Loops",
            "title": "Repeating while a condition holds: the while loop",
            "lede": "Keep processing deliveries as long as there are still orders to handle.",
            "blocks": while_s01_blocks,
            "reward": {"gems": 5},
            "lineage": {
                "fact_ids": [
                    "python.while_loops#f1",
                    "python.while_loops#f2"
                ],
                "teaching_block_ids": [
                    "python.while_loops#tb1",
                    "python.while_loops#tb2",
                    "python.while_loops#tb3"
                ],
                "anchors": ["python.while_loops#visual"]
            }
        },
        {
            "step_id": "tile_python_while_loop_control.s02",
            "type": "video",
            "concept_ids": ["python.while_loops"],
            "eyebrow": "Watch",
            "title": "A while loop as a counter",
            "lede": "See how the condition is re-checked each pass and what happens without an update.",
            "blocks": while_s02_blocks,
            "lineage": {
                "fact_ids": [
                    "python.while_loops#f1",
                    "python.while_loops#f2"
                ],
                "teaching_block_ids": [],
                "segment_ids": ["seg_python.while_loops_gD8ePxAhjUM_178_421"]
            }
        },
        while_s03,
        while_s04,
        {
            "step_id": "tile_python_while_loop_control.s05",
            "type": "explainer",
            "concept_ids": ["python.loop_control"],
            "eyebrow": "Loop control",
            "title": "Steering mid-loop: break and continue",
            "lede": "Exit a loop early or skip a bad record without stopping the whole loop.",
            "blocks": ctrl_s05_blocks,
            "reward": {"gems": 5},
            "lineage": {
                "fact_ids": [
                    "python.loop_control#f1",
                    "python.loop_control#f2"
                ],
                "teaching_block_ids": [
                    "python.loop_control#tb1",
                    "python.loop_control#tb2"
                ],
                "anchors": ["python.loop_control#visual"]
            }
        },
        ctrl_s06,
        ctrl_s07,
        {
            "step_id": "tile_python_while_loop_control.s08",
            "type": "recap",
            "concept_ids": ["python.while_loops", "python.loop_control"],
            "eyebrow": "Recap",
            "title": "What you've learned",
            "lede": "Condition-driven loops and mid-loop steering.",
            "blocks": while_s08_blocks,
            "reward": {"gems": 5},
            "lineage": {
                "fact_ids": [
                    "python.while_loops#f1",
                    "python.while_loops#f2"
                ],
                "teaching_block_ids": [
                    "python.while_loops#tb4"
                ]
            }
        }
    ],
    "remediation_steps": [
        {
            "step_id": "tile_python_while_loop_control.r01",
            "type": "remediation",
            "concept_ids": ["python.while_loops"],
            "title": "The body must change what the condition checks",
            "lede": "Let's revisit why the loop body must update the condition variable.",
            "blocks": while_r01_blocks,
            "lineage": {
                "fact_ids": ["python.while_loops#f2"],
                "teaching_block_ids": ["python.while_loops#tb2"],
                "anchors": ["python.while_loops#assessment:update_state_so_loop_terminates"]
            }
        },
        {
            "step_id": "tile_python_while_loop_control.r02",
            "type": "remediation",
            "concept_ids": ["python.loop_control"],
            "title": "continue vs break",
            "lede": "Let's revisit the difference between continue and break.",
            "blocks": ctrl_r02_blocks,
            "lineage": {
                "fact_ids": ["python.loop_control#f1", "python.loop_control#f2"],
                "teaching_block_ids": ["python.loop_control#tb1", "python.loop_control#tb2"],
                "anchors": ["python.loop_control#assessment:skip_iteration_with_continue"]
            }
        }
    ]
}


# ═══════════════════════════════════════════════════════════════════════════════
# TILE 3: tile_python_comprehensions_iterating
# ═══════════════════════════════════════════════════════════════════════════════

# ── s01 explainer: comprehensions (tb1-tb3, f1-f3, visual=before_after) ──
comp_s01_blocks = [
    heading("tile_python_comprehensions_iterating.s01.h1",
            "Building lists and dicts in one line: comprehensions"),
    prose(
        "tile_python_comprehensions_iterating.s01.p1",
        "Building a new list from an existing one by looping is common enough that Python has a "
        "shorthand for it. A list comprehension consists of brackets containing an expression "
        "followed by a for clause, and optionally an if clause; it produces a new list by evaluating "
        "the expression for each item — [minutes * 2 for minutes in delivery_times] doubles every value.",
        "definition",
        ["python.comprehensions"],
        ["python.comprehensions#f1"],
        ["python.comprehensions#tb1"]
    ),
    prose(
        "tile_python_comprehensions_iterating.s01.p2",
        "Add an if clause to filter the source: "
        "[minutes for minutes in delivery_times if minutes >= 45] keeps only the delivery times "
        "that satisfy that condition. "
        "Dict comprehensions work the same way with curly braces and a key: value expression — "
        "{city: len(city) for city in ('Lagos', 'Abuja', 'Kano')} maps each city name to its length.",
        "mechanism",
        ["python.comprehensions"],
        ["python.comprehensions#f2", "python.comprehensions#f3"],
        ["python.comprehensions#tb2", "python.comprehensions#tb3"]
    ),
    # before_after visual: multi-line loop vs comprehension
    {
        "type": "before_after",
        "block_id": "tile_python_comprehensions_iterating.s01.ba1",
        "before": {
            "type": "code_walkthrough",
            "block_id": "tile_python_comprehensions_iterating.s01.ba1.before",
            "language": "python",
            "code": (
                "# Multi-line loop\n"
                "doubled = []\n"
                "for minutes in delivery_times:\n"
                "    if minutes >= 45:\n"
                "        doubled.append(minutes * 2)"
            ),
            "annotations": [
                {"start_line": 2, "end_line": 2, "text": "empty list to collect results"},
                {"start_line": 3, "end_line": 3, "text": "for clause: iterate over source"},
                {"start_line": 4, "end_line": 4, "text": "if clause: filter condition"},
                {"start_line": 5, "end_line": 5, "text": "expression: double each kept value"}
            ],
            "reveal": "all"
        },
        "after": {
            "type": "code_walkthrough",
            "block_id": "tile_python_comprehensions_iterating.s01.ba1.after",
            "language": "python",
            "code": (
                "# Equivalent list comprehension\n"
                "doubled = [minutes * 2 for minutes in delivery_times if minutes >= 45]"
            ),
            "annotations": [
                {"start_line": 2, "end_line": 2, "text": "expression · for clause · if clause — all in one line"}
            ],
            "reveal": "all"
        },
        "change_summary": "Five lines collapse to one: the expression, for clause and if clause move inside brackets.",
        "lineage": {
            "concept_ids": ["python.comprehensions"],
            "fact_ids": [
                "python.comprehensions#f1",
                "python.comprehensions#f2"
            ],
            "teaching_block_ids": [
                "python.comprehensions#tb1",
                "python.comprehensions#tb2"
            ],
            "anchors": ["python.comprehensions#visual"]
        }
    }
]

# ── s02 check: write_dict_comprehension (framing only) ──
comp_s02 = {
    "step_id": "tile_python_comprehensions_iterating.s02",
    "type": "check",
    "concept_ids": ["python.comprehensions"],
    "eyebrow": "Quick check",
    "title": "Write a dict comprehension",
    "lede": "Which expression correctly builds a dictionary from a sequence using a dict comprehension?",
    "reward": {"gems": 5},
    "lineage": {
        "fact_ids": ["python.comprehensions#f3"],
        "teaching_block_ids": [],
        "anchors": ["python.comprehensions#assessment:write_dict_comprehension"]
    }
}

# ── s03 hands_on: write_list_comprehension + write_dict_comprehension (framing only) ──
comp_s03 = {
    "step_id": "tile_python_comprehensions_iterating.s03",
    "type": "hands_on",
    "concept_ids": ["python.comprehensions"],
    "eyebrow": "Practice",
    "title": "Write list and dict comprehensions",
    "lede": "Use comprehensions to filter delivery times and build a city-length dictionary.",
    "reward": {"gems": 10, "first_try_bonus": 5},
    "lineage": {
        "fact_ids": [
            "python.comprehensions#f1",
            "python.comprehensions#f2",
            "python.comprehensions#f3"
        ],
        "teaching_block_ids": [],
        "anchors": [
            "python.comprehensions#practice",
            "python.comprehensions#assessment:write_list_comprehension",
            "python.comprehensions#assessment:write_dict_comprehension"
        ]
    }
}

# ── s04 explainer: iterating_collections (tb1-tb4, f1-f4, visual=side_by_side) ──
iter_s04_blocks = [
    heading("tile_python_comprehensions_iterating.s04.h1",
            "Looping over any collection: lists, dicts, sets and tuples"),
    prose(
        "tile_python_comprehensions_iterating.s04.p1",
        "You've already looped over lists with for. The same for x in ... pattern works on other "
        "collections, but what you get back per pass differs. "
        "Looping directly over a dictionary yields its keys — "
        "for order_id in order_city: visits each order id, not each city. "
        "To get both key and value together, use .items(): "
        "for order_id, city in order_city.items(): print(order_id, city).",
        "mechanism",
        ["python.iterating_collections"],
        ["python.iterating_collections#f1", "python.iterating_collections#f2"],
        ["python.iterating_collections#tb1", "python.iterating_collections#tb2"]
    ),
    prose(
        "tile_python_comprehensions_iterating.s04.p2",
        "A set's elements may come out in a different order than expected when iterated over, "
        "because a set is unordered — looping over a set of cities won't necessarily visit them "
        "in the order they were added. "
        "Tuples are a sequence type, so a for loop visits their items in order the same way it does "
        "for a list — for value in order: visits 1042, then 'Lagos', then 32, "
        "when order = (1042, 'Lagos', 32).",
        "misconception",
        ["python.iterating_collections"],
        ["python.iterating_collections#f3", "python.iterating_collections#f4"],
        ["python.iterating_collections#tb3", "python.iterating_collections#tb4"]
    ),
    # side_by_side visual: four collection types side by side
    {
        "type": "side_by_side",
        "block_id": "tile_python_comprehensions_iterating.s04.sbs1",
        "left_label": "Collection type and loop header",
        "right_label": "What the loop variable holds each pass",
        "left": {
            "type": "code_walkthrough",
            "block_id": "tile_python_comprehensions_iterating.s04.sbs1.left",
            "language": "python",
            "code": (
                "# list\n"
                "for minutes in delivery_times: ...\n"
                "\n"
                "# dict (keys only)\n"
                "for order_id in order_city: ...\n"
                "\n"
                "# dict (key + value)\n"
                "for order_id, city in order_city.items(): ...\n"
                "\n"
                "# set\n"
                "for city in {'Lagos', 'Abuja', 'Kano'}: ...\n"
                "\n"
                "# tuple\n"
                "for value in (1042, 'Lagos', 32): ..."
            ),
            "reveal": "all"
        },
        "right": {
            "type": "code_walkthrough",
            "block_id": "tile_python_comprehensions_iterating.s04.sbs1.right",
            "language": "python",
            "code": (
                "# each integer delivery time in order\n"
                "# e.g. 32, 45, 21, 60, 18 …\n"
                "\n"
                "# each integer key in insertion order\n"
                "# e.g. 1042, 1043, 1044 …\n"
                "\n"
                "# each (key, value) pair\n"
                "# e.g. (1042, 'Lagos'), (1043, 'Abuja') …\n"
                "\n"
                "# each element — order not guaranteed\n"
                "# may be 'Kano', 'Lagos', 'Abuja' or any order\n"
                "\n"
                "# each item in sequence order\n"
                "# 1042, then 'Lagos', then 32"
            ),
            "reveal": "all"
        },
        "takeaway": "The for x in ... syntax is the same for every collection; what changes is what each pass hands you.",
        "lineage": {
            "concept_ids": ["python.iterating_collections"],
            "fact_ids": [
                "python.iterating_collections#f1",
                "python.iterating_collections#f2",
                "python.iterating_collections#f3",
                "python.iterating_collections#f4"
            ],
            "teaching_block_ids": [
                "python.iterating_collections#tb1",
                "python.iterating_collections#tb2",
                "python.iterating_collections#tb3",
                "python.iterating_collections#tb4"
            ],
            "anchors": ["python.iterating_collections#visual"]
        }
    }
]

# ── s05 check: recognize_unordered_set_iteration (framing only) ──
iter_s05 = {
    "step_id": "tile_python_comprehensions_iterating.s05",
    "type": "check",
    "concept_ids": ["python.iterating_collections"],
    "eyebrow": "Quick check",
    "title": "Set iteration order",
    "lede": "What can you rely on when iterating over a set?",
    "reward": {"gems": 5},
    "lineage": {
        "fact_ids": ["python.iterating_collections#f3"],
        "teaching_block_ids": [],
        "anchors": ["python.iterating_collections#assessment:recognize_unordered_set_iteration"]
    }
}

# ── s06 hands_on: loop_over_keys_or_sequence_items + loop_over_key_value_pairs (framing only) ──
iter_s06 = {
    "step_id": "tile_python_comprehensions_iterating.s06",
    "type": "hands_on",
    "concept_ids": ["python.iterating_collections"],
    "eyebrow": "Practice",
    "title": "Loop over keys and key-value pairs",
    "lede": "Write loops that iterate over the order_city dictionary — first keys only, then key-value pairs.",
    "reward": {"gems": 10, "first_try_bonus": 5},
    "lineage": {
        "fact_ids": [
            "python.iterating_collections#f1",
            "python.iterating_collections#f2",
            "python.iterating_collections#f4"
        ],
        "teaching_block_ids": [],
        "anchors": [
            "python.iterating_collections#practice",
            "python.iterating_collections#assessment:loop_over_keys_or_sequence_items",
            "python.iterating_collections#assessment:loop_over_key_value_pairs"
        ]
    }
}

# ── s07 recap ──
iter_s07_blocks = [
    prose(
        "tile_python_comprehensions_iterating.s07.p1",
        "A comprehension does in one line what a for loop with an if check and an empty list to "
        "append into would otherwise take several lines to build. "
        "The same for x in ... syntax works across lists, dicts, sets and tuples — "
        "what changes is what each pass hands you: an item, a key, or with .items() a key-value pair. "
        "For a set, the order isn't guaranteed.",
        "takeaway",
        ["python.comprehensions", "python.iterating_collections"],
        [
            "python.comprehensions#f1",
            "python.comprehensions#f2",
            "python.iterating_collections#f1",
            "python.iterating_collections#f2",
            "python.iterating_collections#f3",
            "python.iterating_collections#f4"
        ],
        ["python.comprehensions#tb4", "python.iterating_collections#tb5"]
    ),
    {
        "type": "up_next",
        "block_id": "tile_python_comprehensions_iterating.s07.un1",
        "title": "Up next: Functions and Scope",
        "text": "Next you'll learn how to define reusable functions, pass arguments, return values, and understand where variables are visible."
    }
]

# ── remediation steps ──
# r01: for s02 (check: write_dict_comprehension, measures f3)
comp_r01_blocks = [
    heading("tile_python_comprehensions_iterating.r01.h1",
            "Reminder: dict comprehension syntax"),
    prose(
        "tile_python_comprehensions_iterating.r01.p1",
        "Dict comprehensions use curly braces with a key: value expression before the for clause — "
        "{city: len(city) for city in ('Lagos', 'Abuja', 'Kano')} maps each city name to its length. "
        "The key and value expressions can be any valid Python expression; "
        "the result is a new dictionary, not a list.",
        "mechanism",
        ["python.comprehensions"],
        ["python.comprehensions#f3"],
        ["python.comprehensions#tb3"]
    )
]

# r02: for s05 (check: recognize_unordered_set_iteration, measures f3)
iter_r02_blocks = [
    heading("tile_python_comprehensions_iterating.r02.h1",
            "Reminder: sets are unordered"),
    prose(
        "tile_python_comprehensions_iterating.r02.p1",
        "A set's elements may come out in a different order than expected when iterated over, "
        "because a set is unordered. "
        "Looping over {'Lagos', 'Abuja', 'Kano'} won't necessarily visit them in the order they "
        "were written — the order can vary between runs. "
        "If order matters, use a list or tuple instead.",
        "misconception",
        ["python.iterating_collections"],
        ["python.iterating_collections#f3"],
        ["python.iterating_collections#tb3"]
    )
]

tile_comprehensions_iterating = {
    "tile_id": "tile_python_comprehensions_iterating",
    "title": "Comprehensions and Iterating Collections",
    "steps": [
        {
            "step_id": "tile_python_comprehensions_iterating.s01",
            "type": "explainer",
            "concept_ids": ["python.comprehensions"],
            "eyebrow": "Comprehensions",
            "title": "Building lists and dicts in one line: comprehensions",
            "lede": "Replace multi-line loops with compact, readable expressions.",
            "blocks": comp_s01_blocks,
            "reward": {"gems": 5},
            "lineage": {
                "fact_ids": [
                    "python.comprehensions#f1",
                    "python.comprehensions#f2",
                    "python.comprehensions#f3"
                ],
                "teaching_block_ids": [
                    "python.comprehensions#tb1",
                    "python.comprehensions#tb2",
                    "python.comprehensions#tb3"
                ],
                "anchors": ["python.comprehensions#visual"]
            }
        },
        comp_s02,
        comp_s03,
        {
            "step_id": "tile_python_comprehensions_iterating.s04",
            "type": "explainer",
            "concept_ids": ["python.iterating_collections"],
            "eyebrow": "Iterating collections",
            "title": "Looping over any collection: lists, dicts, sets and tuples",
            "lede": "The same for loop syntax works on every collection — what changes is what you get back.",
            "blocks": iter_s04_blocks,
            "reward": {"gems": 5},
            "lineage": {
                "fact_ids": [
                    "python.iterating_collections#f1",
                    "python.iterating_collections#f2",
                    "python.iterating_collections#f3",
                    "python.iterating_collections#f4"
                ],
                "teaching_block_ids": [
                    "python.iterating_collections#tb1",
                    "python.iterating_collections#tb2",
                    "python.iterating_collections#tb3",
                    "python.iterating_collections#tb4"
                ],
                "anchors": ["python.iterating_collections#visual"]
            }
        },
        iter_s05,
        iter_s06,
        {
            "step_id": "tile_python_comprehensions_iterating.s07",
            "type": "recap",
            "concept_ids": ["python.comprehensions", "python.iterating_collections"],
            "eyebrow": "Recap",
            "title": "What you've learned",
            "lede": "One-line builders and universal iteration.",
            "blocks": iter_s07_blocks,
            "reward": {"gems": 5},
            "lineage": {
                "fact_ids": [
                    "python.comprehensions#f1",
                    "python.comprehensions#f2",
                    "python.iterating_collections#f1",
                    "python.iterating_collections#f2",
                    "python.iterating_collections#f3",
                    "python.iterating_collections#f4"
                ],
                "teaching_block_ids": [
                    "python.comprehensions#tb4",
                    "python.iterating_collections#tb5"
                ]
            }
        }
    ],
    "remediation_steps": [
        {
            "step_id": "tile_python_comprehensions_iterating.r01",
            "type": "remediation",
            "concept_ids": ["python.comprehensions"],
            "title": "Dict comprehension syntax",
            "lede": "Let's revisit how to write a dict comprehension.",
            "blocks": comp_r01_blocks,
            "lineage": {
                "fact_ids": ["python.comprehensions#f3"],
                "teaching_block_ids": ["python.comprehensions#tb3"],
                "anchors": ["python.comprehensions#assessment:write_dict_comprehension"]
            }
        },
        {
            "step_id": "tile_python_comprehensions_iterating.r02",
            "type": "remediation",
            "concept_ids": ["python.iterating_collections"],
            "title": "Sets are unordered",
            "lede": "Let's revisit why set iteration order is not guaranteed.",
            "blocks": iter_r02_blocks,
            "lineage": {
                "fact_ids": ["python.iterating_collections#f3"],
                "teaching_block_ids": ["python.iterating_collections#tb3"],
                "anchors": ["python.iterating_collections#assessment:recognize_unordered_set_iteration"]
            }
        }
    ]
}


# ═══════════════════════════════════════════════════════════════════════════════
# ASSEMBLE OUTPUT
# ═══════════════════════════════════════════════════════════════════════════════

output = {
    "schema_version": "0.1.0",
    "kind": "screens_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_008_da_python_core",
    "tiles": [
        tile_conditionals_for_loops,
        tile_while_loop_control,
        tile_comprehensions_iterating
    ]
}

out_path = "batches/final_batch_008_da_python_core/screens.part.c2.json"
with open(out_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"Written: {out_path}")

# Count steps
for tile in output["tiles"]:
    steps = tile["steps"]
    rem = tile.get("remediation_steps", [])
    print(f"  {tile['tile_id']}: {len(steps)} steps, {len(rem)} remediation steps")
