"""
Build screens.part.c1.json for tile ids:
  tile_viz_line_scatter_box
  tile_viz_bar_histograms
  tile_viz_labeling_chart_selection
  tile_viz_custom_multi_panel
  tile_viz_seaborn_stats_themes
"""
import json

# ── helpers ──────────────────────────────────────────────────────────────────

def prose(block_id, role, text, concept_ids, tb_ids, fact_ids, anchors=None):
    lin = {"concept_ids": concept_ids, "teaching_block_ids": tb_ids, "fact_ids": fact_ids}
    if anchors:
        lin["anchors"] = anchors
    return {"type": "prose", "block_id": block_id, "role": role, "text": text, "lineage": lin}

def heading(block_id, text, level=3):
    return {"type": "heading", "block_id": block_id, "text": text, "level": level}

def media_group(block_id, segment_ids):
    return {"type": "media_group", "block_id": block_id, "segment_ids": segment_ids}

def chart(block_id, chart_kind, asset_id, title, alt_text, encoding,
          concept_ids, tb_ids, fact_ids, anchors=None, variant_id=None, columns=None):
    lin = {"concept_ids": concept_ids, "teaching_block_ids": tb_ids, "fact_ids": fact_ids}
    if anchors:
        lin["anchors"] = anchors
    asset_ref = {"asset_id": asset_id}
    if variant_id:
        asset_ref["variant_id"] = variant_id
    if columns:
        asset_ref["columns"] = columns
    blk = {"type": "chart", "block_id": block_id, "chart_kind": chart_kind,
           "asset_ref": asset_ref, "title": title, "alt_text": alt_text,
           "encoding": encoding, "lineage": lin}
    return blk

def code_walk(block_id, code, annotations, concept_ids, tb_ids, fact_ids, anchors=None):
    lin = {"concept_ids": concept_ids, "teaching_block_ids": tb_ids, "fact_ids": fact_ids}
    if anchors:
        lin["anchors"] = anchors
    return {"type": "code_walkthrough", "block_id": block_id, "language": "python",
            "code": code, "annotations": annotations, "reveal": "line_by_line", "lineage": lin}

def before_after(block_id, before_blk, after_blk, change_summary,
                 concept_ids, tb_ids, fact_ids, anchors=None):
    lin = {"concept_ids": concept_ids, "teaching_block_ids": tb_ids, "fact_ids": fact_ids}
    if anchors:
        lin["anchors"] = anchors
    return {"type": "before_after", "block_id": block_id,
            "before": before_blk, "after": after_blk,
            "change_summary": change_summary, "lineage": lin}

def diagram(block_id, diagram_kind, nodes, alt_text, title=None, edges=None,
            concept_ids=None, tb_ids=None, fact_ids=None, anchors=None):
    lin = {"concept_ids": concept_ids or [], "teaching_block_ids": tb_ids or [],
           "fact_ids": fact_ids or []}
    if anchors:
        lin["anchors"] = anchors
    blk = {"type": "diagram", "block_id": block_id, "diagram_kind": diagram_kind,
           "nodes": nodes, "alt_text": alt_text, "layout": "auto", "lineage": lin}
    if title:
        blk["title"] = title
    if edges:
        blk["edges"] = edges
    return blk

def annotated_image(block_id, asset_id, alt_text, hotspots,
                    concept_ids, tb_ids, fact_ids, anchors=None):
    lin = {"concept_ids": concept_ids, "teaching_block_ids": tb_ids, "fact_ids": fact_ids}
    if anchors:
        lin["anchors"] = anchors
    return {"type": "annotated_image", "block_id": block_id, "asset_id": asset_id,
            "alt_text": alt_text, "hotspots": hotspots, "lineage": lin}

def side_by_side(block_id, left_blk, right_blk, left_label, right_label, takeaway,
                 concept_ids, tb_ids, fact_ids, anchors=None):
    lin = {"concept_ids": concept_ids, "teaching_block_ids": tb_ids, "fact_ids": fact_ids}
    if anchors:
        lin["anchors"] = anchors
    return {"type": "side_by_side", "block_id": block_id,
            "left": left_blk, "right": right_blk,
            "left_label": left_label, "right_label": right_label,
            "takeaway": takeaway, "lineage": lin}

def up_next(block_id, title, text):
    return {"type": "up_next", "block_id": block_id, "title": title, "text": text}

def step_explainer(step_id, concept_ids, eyebrow, title, lede, blocks,
                   tb_ids, fact_ids, anchors=None, gems=5):
    lin = {"concept_ids": concept_ids, "teaching_block_ids": tb_ids, "fact_ids": fact_ids}
    if anchors:
        lin["anchors"] = anchors
    return {"step_id": step_id, "type": "explainer", "concept_ids": concept_ids,
            "eyebrow": eyebrow, "title": title, "lede": lede,
            "blocks": blocks, "reward": {"gems": gems}, "lineage": lin}

def step_video(step_id, concept_ids, eyebrow, title, segment_ids, fact_ids):
    lin = {"concept_ids": concept_ids, "teaching_block_ids": [],
           "fact_ids": fact_ids, "segment_ids": segment_ids}
    return {"step_id": step_id, "type": "video", "concept_ids": concept_ids,
            "eyebrow": eyebrow, "title": title,
            "blocks": [media_group(step_id + ".b01", segment_ids)],
            "reward": {"gems": 5}, "lineage": lin}

def step_check(step_id, concept_ids, eyebrow, title, lede, fact_ids, anchors, gems=10):
    lin = {"concept_ids": concept_ids, "teaching_block_ids": [],
           "fact_ids": fact_ids, "anchors": anchors}
    return {"step_id": step_id, "type": "check", "concept_ids": concept_ids,
            "eyebrow": eyebrow, "title": title, "lede": lede,
            "reward": {"gems": gems, "first_try_bonus": 5}, "lineage": lin}

def step_hands_on(step_id, concept_ids, eyebrow, title, lede, fact_ids, anchors, gems=15):
    lin = {"concept_ids": concept_ids, "teaching_block_ids": [],
           "fact_ids": fact_ids, "anchors": anchors}
    return {"step_id": step_id, "type": "hands_on", "concept_ids": concept_ids,
            "eyebrow": eyebrow, "title": title, "lede": lede,
            "reward": {"gems": gems}, "lineage": lin}

def step_recap(step_id, concept_ids, title, lede, blocks, tb_ids, fact_ids, gems=10):
    lin = {"concept_ids": concept_ids, "teaching_block_ids": tb_ids, "fact_ids": fact_ids}
    return {"step_id": step_id, "type": "recap", "concept_ids": concept_ids,
            "eyebrow": "recap", "title": title, "lede": lede,
            "blocks": blocks, "reward": {"gems": gems}, "lineage": lin}

def step_remediation(step_id, concept_ids, title, lede, blocks, tb_ids, fact_ids):
    lin = {"concept_ids": concept_ids, "teaching_block_ids": tb_ids, "fact_ids": fact_ids}
    return {"step_id": step_id, "type": "remediation", "concept_ids": concept_ids,
            "eyebrow": "try again", "title": title, "lede": lede,
            "blocks": blocks, "lineage": lin}


# ═══════════════════════════════════════════════════════════════════════════════
# TILE 1: tile_viz_bar_histograms
# ═══════════════════════════════════════════════════════════════════════════════

T_BAR = "tile_viz_bar_histograms"
C_BAR = "viz.bar_charts"
C_HIST = "viz.histograms"

# s01 explainer – bar charts intro + syntax (before_after visual)
# before: code without groupby; after: code with groupby + plt.bar
bar_before_code = code_walk(
    T_BAR + ".s01.b01.before",
    "# Delivery times as a raw list — hard to compare cities\nprint(orders['delivery_time_minutes'].tolist())",
    [{"start_line": 2, "end_line": 2, "text": "A flat list gives no per-city comparison"}],
    [C_BAR], ["viz.bar_charts#tb1"], ["viz.bar_charts#f2"]
)
bar_after_code = code_walk(
    T_BAR + ".s01.b01.after",
    "city_avg = orders.groupby('city')['delivery_time_minutes'].mean()\nplt.bar(city_avg.index, city_avg)",
    [
        {"start_line": 1, "end_line": 1, "text": "groupby + mean produces one average per city"},
        {"start_line": 2, "end_line": 2, "text": "plt.bar(city_avg.index, city_avg) passes city names as x and averages as heights"}
    ],
    [C_BAR], ["viz.bar_charts#tb2"], ["viz.bar_charts#f1", "viz.bar_charts#f4"]
)

s01_bar = step_explainer(
    T_BAR + ".s01", [C_BAR], "bar charts",
    "Comparing Cities with a Bar Chart",
    "When you want to compare a number across discrete categories, a bar chart aligns every bar to a shared baseline so the eye can judge lengths at a glance.",
    [
        prose(T_BAR + ".s01.b02", "intro",
              "Suppose you want to compare average delivery time across Lagos, Abuja, and Kano. "
              "A bar chart is a common chart type for graphing categorical data or data sorted into groups — "
              "which fits this comparison exactly.",
              [C_BAR], ["viz.bar_charts#tb1"], ["viz.bar_charts#f2"]),
        prose(T_BAR + ".s01.b03", "syntax",
              "`plt.bar(x, height)` (or `ax.bar(x, height)`) makes a bar plot with bars positioned at the "
              "given x coordinates and given heights, with the baseline defaulting to 0. "
              "Categorical names can be passed directly as the x argument: "
              "`plt.bar(city_avg.index, city_avg)` plots the three city names as bar positions "
              "and each city's average delivery time as the bar height.",
              [C_BAR], ["viz.bar_charts#tb2"], ["viz.bar_charts#f1", "viz.bar_charts#f4"]),
        before_after(
            T_BAR + ".s01.b04",
            bar_before_code, bar_after_code,
            "Adding groupby + plt.bar turns a flat list into a per-city comparison chart.",
            [C_BAR], ["viz.bar_charts#tb1", "viz.bar_charts#tb2"],
            ["viz.bar_charts#f1", "viz.bar_charts#f2", "viz.bar_charts#f4"],
            anchors=["viz.bar_charts#visual"]
        )
    ],
    tb_ids=["viz.bar_charts#tb1", "viz.bar_charts#tb2"],
    fact_ids=["viz.bar_charts#f1", "viz.bar_charts#f2", "viz.bar_charts#f4"],
    anchors=["viz.bar_charts#visual"]
)

# s02 video
s02_bar = step_video(
    T_BAR + ".s02", [C_BAR], "watch",
    "Bar Charts: Live Code and the Zero-Baseline Rule",
    ["seg_viz.bar_charts_k7UJg2E-TyU_0_144", "seg_viz.bar_charts_dNVjFpHjbDs_70_134"],
    ["viz.bar_charts#f1", "viz.bar_charts#f2", "viz.bar_charts#f3", "viz.bar_charts#f4"]
)

# s03 explainer – baseline mental model + misconception
s03_bar = step_explainer(
    T_BAR + ".s03", [C_BAR], "bar charts",
    "Why the Baseline Must Start at Zero",
    "The bar chart's power comes from comparing lengths — and that only works when every bar starts at the same point.",
    [
        prose(T_BAR + ".s03.b01", "mental_model",
              "Bar charts are easy to interpret because the eye is good at comparing lengths when the objects "
              "being compared are aligned to a common baseline. Every bar starts at 0, so a taller bar "
              "genuinely represents a larger value — Kano's bar looks taller than Lagos's because its "
              "average delivery time is higher.",
              [C_BAR], ["viz.bar_charts#tb3"], ["viz.bar_charts#f3"]),
        prose(T_BAR + ".s03.b02", "misconception",
              "Starting bars at a value other than 0 — say 20 minutes — distorts the comparison. "
              "If Kano averages 30 minutes and Lagos 25, bars starting at 20 are 10 and 5 units tall: "
              "Kano's bar looks twice as long even though its average is only 5 minutes higher. "
              "Keep the baseline at 0.",
              [C_BAR], ["viz.bar_charts#tb4"], ["viz.bar_charts#f3", "viz.bar_charts#m1"])
    ],
    tb_ids=["viz.bar_charts#tb3", "viz.bar_charts#tb4"],
    fact_ids=["viz.bar_charts#f3", "viz.bar_charts#m1"]
)

# s04 check – f2 (categorical use case)
s04_bar = step_check(
    T_BAR + ".s04", [C_BAR], "quick check",
    "When to Use a Bar Chart",
    "Which kind of data is a bar chart designed to compare?",
    ["viz.bar_charts#f2"],
    ["viz.bar_charts#assessment:identify_bar_chart_as_categorical_comparison_tool"]
)

# s05 check – f3 + m1 (baseline)
s05_bar = step_check(
    T_BAR + ".s05", [C_BAR], "quick check",
    "The Zero-Baseline Rule",
    "Why must a bar chart's baseline start at zero?",
    ["viz.bar_charts#f3", "viz.bar_charts#m1"],
    ["viz.bar_charts#assessment:explain_why_zero_baseline_is_required_for_valid_length_comparison"]
)

# s06 hands_on – f1 + f4
s06_bar = step_hands_on(
    T_BAR + ".s06", [C_BAR], "hands-on",
    "Plot City Averages with plt.bar()",
    "Use groupby to compute per-city averages, then pass the city names and averages to plt.bar().",
    ["viz.bar_charts#f1", "viz.bar_charts#f4"],
    ["viz.bar_charts#practice",
     "viz.bar_charts#assessment:construct_bar_chart_with_plt_bar_using_categorical_x"]
)

# s07 explainer – histograms (before_after visual)
hist_before_code = code_walk(
    T_BAR + ".s07.b01.before",
    "# Delivery times as a sorted list — shape is not visible\nprint(sorted(orders['delivery_time_minutes'].tolist()))",
    [{"start_line": 2, "end_line": 2, "text": "A sorted list shows individual values but not the distribution shape"}],
    [C_HIST], ["viz.histograms#tb1"], ["viz.histograms#f1"]
)
hist_after_code = code_walk(
    T_BAR + ".s07.b01.after",
    "plt.hist(orders['delivery_time_minutes'], bins=10)",
    [{"start_line": 1, "end_line": 1, "text": "plt.hist bins the values and draws one bar per bin, revealing the distribution shape"}],
    [C_HIST], ["viz.histograms#tb2"], ["viz.histograms#f1"]
)

s07_hist = step_explainer(
    T_BAR + ".s07", [C_HIST], "histograms",
    "Seeing the Distribution with a Histogram",
    "A histogram bins a numeric variable and draws one bar per bin — revealing the shape of the distribution rather than individual values.",
    [
        prose(T_BAR + ".s07.b02", "intro",
              "A bar chart compares categories, but delivery times are a numeric variable. "
              "You might instead want to see how those times are distributed — how many deliveries were fast, "
              "how many were slow, and whether most cluster in the middle. "
              "A histogram answers that question.",
              [C_HIST], ["viz.histograms#tb1"], ["viz.histograms#f1"]),
        prose(T_BAR + ".s07.b03", "mechanism",
              "`plt.hist(x, bins=...)` uses `numpy.histogram` to bin the data in x, count the number of "
              "values in each bin, and draw the result as bars. "
              "`plt.hist(orders['delivery_time_minutes'])` bins every delivery time and shows how many "
              "orders fall into each time range.",
              [C_HIST], ["viz.histograms#tb2"], ["viz.histograms#f1"]),
        prose(T_BAR + ".s07.b04", "syntax",
              "The `bins` parameter defaults to `rcParams['hist.bins']`, which defaults to 10. "
              "Passing an integer sets that many equal-width bins; passing a sequence sets explicit bin edges; "
              "passing a string such as `'auto'` selects a binning strategy automatically.",
              [C_HIST], ["viz.histograms#tb3"], ["viz.histograms#f2"]),
        before_after(
            T_BAR + ".s07.b05",
            hist_before_code, hist_after_code,
            "plt.hist() replaces a sorted list with a binned bar chart that reveals the distribution shape.",
            [C_HIST], ["viz.histograms#tb1", "viz.histograms#tb2"],
            ["viz.histograms#f1", "viz.histograms#f2"],
            anchors=["viz.histograms#visual"]
        )
    ],
    tb_ids=["viz.histograms#tb1", "viz.histograms#tb2", "viz.histograms#tb3"],
    fact_ids=["viz.histograms#f1", "viz.histograms#f2"],
    anchors=["viz.histograms#visual"]
)

# s08 video
s08_hist = step_video(
    T_BAR + ".s08", [C_HIST], "watch",
    "Histograms: Binning and Distribution Shape",
    ["seg_viz.histograms_XDv6T4a0RNc_126_408"],
    ["viz.histograms#f1", "viz.histograms#f2"]
)

# s09 check – f1 (binning mechanism)
s09_hist = step_check(
    T_BAR + ".s09", [C_HIST], "quick check",
    "How plt.hist() Works",
    "What does plt.hist() do with the values you pass it?",
    ["viz.histograms#f1"],
    ["viz.histograms#assessment:call_plt_hist_and_explain_binning_mechanism"]
)

# s10 check – f2 (bins parameter)
s10_hist = step_check(
    T_BAR + ".s10", [C_HIST], "quick check",
    "Controlling Bin Count",
    "What does passing an integer to the bins parameter do?",
    ["viz.histograms#f2"],
    ["viz.histograms#assessment:configure_bins_parameter_with_integer_sequence_or_string"]
)

# s11 hands_on – histograms practice
s11_hist = step_hands_on(
    T_BAR + ".s11", [C_HIST], "hands-on",
    "Plot a Delivery-Time Histogram",
    "Call plt.hist() on the delivery_time_minutes column and experiment with the bins parameter.",
    [],
    ["viz.histograms#practice",
     "viz.histograms#assessment:call_plt_hist_and_explain_binning_mechanism",
     "viz.histograms#assessment:configure_bins_parameter_with_integer_sequence_or_string"]
)

# s12 recap
s12_recap_bar = step_recap(
    T_BAR + ".s12", [C_BAR, C_HIST],
    "Bar Charts and Histograms: What You Learned",
    "Two chart types, two different questions — categories versus distribution.",
    [
        prose(T_BAR + ".s12.b01", "takeaway",
              "Use `plt.bar(x, height)` to compare a numeric value across discrete categories, "
              "keeping the baseline at 0 so bar lengths stay honest. "
              "Use `plt.hist(x, bins=...)` to reveal how a numeric variable is distributed — "
              "it bins the values and draws one bar per bin.",
              [C_BAR, C_HIST], [], []),
        up_next(T_BAR + ".s12.b02",
                "Up next: Line Plots, Scatter Plots, and Box Plots",
                "Next you'll plot trends over time with plt.plot(), relationships between two numeric "
                "variables with plt.scatter(), and per-city spread with plt.boxplot().")
    ],
    tb_ids=[], fact_ids=[]
)

# remediation steps
rem_bar_s04 = step_remediation(
    T_BAR + ".r01", [C_BAR],
    "Bar Charts Are for Categories",
    "A bar chart compares a numeric value across discrete groups — not distributions or trends.",
    [
        prose(T_BAR + ".r01.b01", "definition",
              "A bar chart is a common chart type for graphing categorical data or data sorted into groups. "
              "The three cities Lagos, Abuja, and Kano are discrete categories, so a bar chart comparing "
              "their average delivery times is the right fit. "
              "A histogram would show the spread of times, not a city-by-city comparison.",
              [C_BAR], ["viz.bar_charts#tb1"], ["viz.bar_charts#f2"])
    ],
    tb_ids=["viz.bar_charts#tb1"], fact_ids=["viz.bar_charts#f2"]
)

rem_bar_s05 = step_remediation(
    T_BAR + ".r02", [C_BAR],
    "The Baseline Must Be Zero",
    "Shifting the baseline away from zero makes bars misleading because the eye compares lengths.",
    [
        prose(T_BAR + ".r02.b01", "misconception",
              "Bar charts are easy to interpret because the eye compares lengths from a common baseline. "
              "If Kano averages 30 minutes and Lagos 25, bars starting at 20 are 10 and 5 units tall — "
              "Kano's bar looks twice as long even though its average is only 5 minutes higher. "
              "Keep the baseline at 0 so lengths stay proportional to values.",
              [C_BAR], ["viz.bar_charts#tb3", "viz.bar_charts#tb4"],
              ["viz.bar_charts#f3", "viz.bar_charts#m1"])
    ],
    tb_ids=["viz.bar_charts#tb3", "viz.bar_charts#tb4"],
    fact_ids=["viz.bar_charts#f3", "viz.bar_charts#m1"]
)

rem_hist_s09 = step_remediation(
    T_BAR + ".r03", [C_HIST],
    "How plt.hist() Bins Your Data",
    "plt.hist() doesn't just count values — it groups them into bins first.",
    [
        prose(T_BAR + ".r03.b01", "mechanism",
              "`plt.hist(x, bins=...)` uses `numpy.histogram` to bin the data in x, count the number of "
              "values in each bin, and draw the result as bars. "
              "Each bar represents a range of values, not a single value — that's what makes a histogram "
              "different from a bar chart.",
              [C_HIST], ["viz.histograms#tb2"], ["viz.histograms#f1"])
    ],
    tb_ids=["viz.histograms#tb2"], fact_ids=["viz.histograms#f1"]
)

rem_hist_s10 = step_remediation(
    T_BAR + ".r04", [C_HIST],
    "Controlling Bins in plt.hist()",
    "The bins parameter accepts an integer, a sequence, or a strategy string.",
    [
        prose(T_BAR + ".r04.b01", "syntax",
              "The `bins` parameter defaults to `rcParams['hist.bins']`, which defaults to 10. "
              "Passing an integer sets that many equal-width bins. "
              "Passing a sequence sets explicit bin edges. "
              "Passing a string such as `'auto'` selects a binning strategy automatically.",
              [C_HIST], ["viz.histograms#tb3"], ["viz.histograms#f2"])
    ],
    tb_ids=["viz.histograms#tb3"], fact_ids=["viz.histograms#f2"]
)

tile_bar_histograms = {
    "tile_id": T_BAR,
    "title": "Bar Charts and Histograms",
    "summary": "Learn to compare categories with plt.bar() and reveal distributions with plt.hist(), understanding the zero-baseline rule and the bins parameter.",
    "steps": [s01_bar, s02_bar, s03_bar, s04_bar, s05_bar, s06_bar,
              s07_hist, s08_hist, s09_hist, s10_hist, s11_hist, s12_recap_bar],
    "remediation_steps": [rem_bar_s04, rem_bar_s05, rem_hist_s09, rem_hist_s10]
}


# ═══════════════════════════════════════════════════════════════════════════════
# TILE 2: tile_viz_line_scatter_box
# ═══════════════════════════════════════════════════════════════════════════════

T_LSB = "tile_viz_line_scatter_box"
C_LINE = "viz.line_plots"
C_SCAT = "viz.scatter_plots"
C_BOX = "viz.box_plots"

# s01 explainer – line plots (chart visual)
s01_lsb = step_explainer(
    T_LSB + ".s01", [C_LINE], "line plots",
    "Tracking Trends Over Time with a Line Plot",
    "A line plot connects measured points in order — making rises and falls in the data immediately visible.",
    [
        prose(T_LSB + ".s01.b01", "intro",
              "Suppose you have this week's average Lagos delivery time for each of 5 days and want to see "
              "whether it is getting better or worse. "
              "Line graphs are best when you want to show how the value of something changes over time, "
              "or compare how several things change over time relative to each other.",
              [C_LINE], ["viz.line_plots#tb1"], ["viz.line_plots#f1"]),
        prose(T_LSB + ".s01.b02", "mechanism",
              "A line graph plots the measured points and then draws a line that connects those points, "
              "making it easier to see how the values rose, fell, or stayed the same over time.",
              [C_LINE], ["viz.line_plots#tb2"], ["viz.line_plots#f3"]),
        prose(T_LSB + ".s01.b03", "syntax",
              "`plt.plot(x, y)` plots the y-values against the given x-values. "
              "`plt.plot([1, 2, 3, 4, 5], [21, 23, 19, 25, 20])` plots 5 days of average Lagos delivery "
              "times, with the connecting line making the day-to-day rise and fall immediately readable.",
              [C_LINE], ["viz.line_plots#tb3"], ["viz.line_plots#f2"]),
        chart(
            T_LSB + ".s01.b04", "line", "ds.daily_averages",
            "Average Lagos Delivery Time — Days 1–5",
            "A line chart of 5 days of Lagos average delivery times (21, 23, 19, 25, 20 minutes). "
            "The connected line makes the day-to-day rise and fall immediately readable.",
            {"x": {"field": "day", "type": "ordinal", "title": "Day"},
             "y": {"field": "lagos_avg", "type": "quantitative", "title": "Avg delivery time (min)"}},
            [C_LINE], ["viz.line_plots#tb1", "viz.line_plots#tb2", "viz.line_plots#tb3"],
            ["viz.line_plots#f1", "viz.line_plots#f2", "viz.line_plots#f3"],
            anchors=["viz.line_plots#visual"]
        )
    ],
    tb_ids=["viz.line_plots#tb1", "viz.line_plots#tb2", "viz.line_plots#tb3"],
    fact_ids=["viz.line_plots#f1", "viz.line_plots#f2", "viz.line_plots#f3"],
    anchors=["viz.line_plots#visual"]
)

# s02 video
s02_lsb = step_video(
    T_LSB + ".s02", [C_LINE], "watch",
    "Line Plots: Connecting Points to Reveal Trends",
    ["seg_viz.line_plots_Xhqj3gzn0gg_0_122", "seg_viz.line_plots_UO98lJQ3QGI_226_383"],
    ["viz.line_plots#f1", "viz.line_plots#f2", "viz.line_plots#f3"]
)

# s03 check – f3 (connecting line reveals trend)
s03_lsb = step_check(
    T_LSB + ".s03", [C_LINE], "quick check",
    "What the Connecting Line Adds",
    "Why does a line graph draw a line through the measured points?",
    ["viz.line_plots#f3"],
    ["viz.line_plots#assessment:explain_how_connecting_line_reveals_trend"]
)

# s04 hands_on – line plots
s04_lsb = step_hands_on(
    T_LSB + ".s04", [C_LINE], "hands-on",
    "Plot Lagos Delivery Trends with plt.plot()",
    "Call plt.plot() with a list of days and a list of average delivery times to draw a line chart.",
    ["viz.line_plots#f1", "viz.line_plots#f2", "viz.line_plots#f3"],
    ["viz.line_plots#practice",
     "viz.line_plots#assessment:identify_line_plot_appropriate_use_case",
     "viz.line_plots#assessment:call_plt_plot_with_x_and_y_arguments",
     "viz.line_plots#assessment:build_line_plot_for_time_ordered_numeric_data"]
)

# s05 explainer – scatter plots (chart visual)
s05_lsb = step_explainer(
    T_LSB + ".s05", [C_SCAT], "scatter plots",
    "Exploring Relationships with a Scatter Plot",
    "A scatter plot places one point per (x, y) pair — making the relationship between two numeric variables visible at a glance.",
    [
        prose(T_LSB + ".s05.b01", "intro",
              "Suppose you want to see whether delivery distance and delivery time move together across "
              "your orders. A scatterplot shows the relationship between two numerical variables plotted "
              "simultaneously along the horizontal and vertical axis, and is useful for focusing on the "
              "relationship between two series.",
              [C_SCAT], ["viz.scatter_plots#tb1"], ["viz.scatter_plots#f2"]),
        prose(T_LSB + ".s05.b02", "syntax",
              "`plt.scatter(x, y)` (or `ax.scatter(x, y)`) makes a scatter plot of the y-values against "
              "the x-values, one point per (x, y) pair. "
              "`plt.scatter(orders['distance_km'], orders['delivery_time_minutes'])` plots one point per "
              "order, with distance on the x-axis and delivery time on the y-axis.",
              [C_SCAT], ["viz.scatter_plots#tb2"], ["viz.scatter_plots#f1"]),
        chart(
            T_LSB + ".s05.b03", "scatter", "ds.orders",
            "Distance vs Delivery Time — QuickDeliver Orders",
            "A scatter plot of distance_km on the x-axis versus delivery_time_minutes on the y-axis, "
            "one point per order. Points trend upward, showing that longer distances tend to take more time.",
            {"x": {"field": "distance_km", "type": "quantitative", "title": "Distance (km)"},
             "y": {"field": "delivery_time_minutes", "type": "quantitative", "title": "Delivery time (min)"}},
            [C_SCAT], ["viz.scatter_plots#tb1", "viz.scatter_plots#tb2"],
            ["viz.scatter_plots#f1", "viz.scatter_plots#f2"],
            anchors=["viz.scatter_plots#visual"],
            columns=["distance_km", "delivery_time_minutes"]
        )
    ],
    tb_ids=["viz.scatter_plots#tb1", "viz.scatter_plots#tb2"],
    fact_ids=["viz.scatter_plots#f1", "viz.scatter_plots#f2"],
    anchors=["viz.scatter_plots#visual"]
)

# s06 video
s06_lsb = step_video(
    T_LSB + ".s06", [C_SCAT], "watch",
    "Scatter Plots: One Point per Pair",
    ["seg_viz.scatter_plots_zZZ_RCwp49g_120_180"],
    ["viz.scatter_plots#f1", "viz.scatter_plots#f2"]
)

# s07 check – f1 + f2
s07_lsb = step_check(
    T_LSB + ".s07", [C_SCAT], "quick check",
    "Scatter Plot Basics",
    "What does each point in a scatter plot represent?",
    ["viz.scatter_plots#f1", "viz.scatter_plots#f2"],
    ["viz.scatter_plots#assessment:build_scatter_plot_from_two_numeric_columns"]
)

# s08 hands_on – scatter
s08_lsb = step_hands_on(
    T_LSB + ".s08", [C_SCAT], "hands-on",
    "Plot Distance vs Delivery Time",
    "Use plt.scatter() to plot distance_km against delivery_time_minutes from the orders dataset.",
    ["viz.scatter_plots#f1", "viz.scatter_plots#f2"],
    ["viz.scatter_plots#practice",
     "viz.scatter_plots#assessment:build_scatter_plot_from_two_numeric_columns"]
)

# s09 explainer – box plots intro (annotated_image visual)
# The annotated_image references a rendered box plot image asset
s09_lsb = step_explainer(
    T_LSB + ".s09", [C_BOX], "box plots",
    "Reading a Box Plot",
    "Every part of a box plot has a name — learn to read the box, whiskers, and flier points.",
    [
        prose(T_LSB + ".s09.b01", "intro",
              "Boxplots offer a condensed display for comparing the distributions of multiple datasets "
              "side by side — showing spread, median, and outliers in a single compact shape.",
              [C_BOX], ["viz.box_plots#tb1"], ["viz.box_plots#f3"]),
        annotated_image(
            T_LSB + ".s09.b02",
            "img.boxplot_anatomy",
            "A box plot with labelled parts: Q1 at the bottom of the box, median as a line inside the box, "
            "Q3 at the top of the box, IQR as the box height, upper and lower whiskers extending to the "
            "farthest in-range points, and a flier point above the upper whisker.",
            [
                {"x": 0.5, "y": 0.25, "w": 0.15, "h": 0.05, "label": "Q1 (first quartile)",
                 "detail": "Bottom edge of the box"},
                {"x": 0.5, "y": 0.5, "w": 0.15, "h": 0.05, "label": "Median",
                 "detail": "Line inside the box"},
                {"x": 0.5, "y": 0.75, "w": 0.15, "h": 0.05, "label": "Q3 (third quartile)",
                 "detail": "Top edge of the box"},
                {"x": 0.5, "y": 0.12, "w": 0.12, "h": 0.04, "label": "Lower whisker",
                 "detail": "Farthest point within 1.5×IQR below Q1"},
                {"x": 0.5, "y": 0.88, "w": 0.12, "h": 0.04, "label": "Upper whisker",
                 "detail": "Farthest point within 1.5×IQR above Q3"},
                {"x": 0.5, "y": 0.97, "w": 0.08, "h": 0.03, "label": "Flier point (outlier)",
                 "detail": "Point beyond the whisker end"}
            ],
            [C_BOX], ["viz.box_plots#tb1"], ["viz.box_plots#f3"],
            anchors=["viz.box_plots#visual"]
        )
    ],
    tb_ids=["viz.box_plots#tb1"],
    fact_ids=["viz.box_plots#f3"],
    anchors=["viz.box_plots#visual"]
)

# s10 explainer – box plot mechanism (f1, f2)
s10_lsb = step_explainer(
    T_LSB + ".s10", [C_BOX], "box plots",
    "The Box, Whiskers, and Flier Points",
    "The box spans Q1 to Q3; whiskers reach 1.5×IQR beyond the box; anything further is a flier.",
    [
        prose(T_LSB + ".s10.b01", "mechanism",
              "`plt.boxplot(x)` (or `ax.boxplot(x)`) draws a box plot from the data in x; it accepts "
              "array-like data and can draw one or more boxes. "
              "The box extends from Q1 to Q3, with a line at the median. "
              "The whiskers extend to the farthest data point lying within 1.5× the IQR from the box; "
              "points past the whisker ends are flier points (outliers).",
              [C_BOX], ["viz.box_plots#tb2"], ["viz.box_plots#f1", "viz.box_plots#f2"]),
        prose(T_LSB + ".s10.b02", "example",
              "If Lagos's box runs from Q1 = 20 to Q3 = 30 minutes, the IQR is 10 minutes. "
              "The whiskers can reach at most 1.5 × 10 = 15 minutes beyond the box — no lower than "
              "5 minutes and no higher than 45 minutes — so a 50-minute Lagos delivery would be drawn "
              "as a separate flier point.",
              [C_BOX], ["viz.box_plots#tb2"], ["viz.box_plots#f2"])
    ],
    tb_ids=["viz.box_plots#tb2"],
    fact_ids=["viz.box_plots#f1", "viz.box_plots#f2"]
)

# s11 video
s11_lsb = step_video(
    T_LSB + ".s11", [C_BOX], "watch",
    "Box Plots: Distribution and Outliers",
    ["seg_viz.box_plots_XFZRVnP-MTU_402_503"],
    ["viz.box_plots#f2", "viz.box_plots#f3"]
)

# s12 explainer – multi-box syntax (f4)
s12_lsb = step_explainer(
    T_LSB + ".s12", [C_BOX], "box plots",
    "Comparing Multiple Cities Side by Side",
    "Pass a sequence of arrays to draw one box per group, and use tick_labels to name each box.",
    [
        prose(T_LSB + ".s12.b01", "syntax",
              "Passing a sequence of 1D arrays as x draws one box for each array in the sequence; "
              "`tick_labels=[...]` labels each boxplot's tick accordingly instead of leaving it as a "
              "numeric value. "
              "`plt.boxplot([lagos_times, abuja_times, kano_times], tick_labels=['Lagos', 'Abuja', 'Kano'])` "
              "draws three boxes side by side, each labeled with its city name.",
              [C_BOX], ["viz.box_plots#tb3"], ["viz.box_plots#f4"])
    ],
    tb_ids=["viz.box_plots#tb3"],
    fact_ids=["viz.box_plots#f4"]
)

# s13 check – f2 (box anatomy)
s13_lsb = step_check(
    T_LSB + ".s13", [C_BOX], "quick check",
    "Box Plot Anatomy",
    "What do the edges of the box represent?",
    ["viz.box_plots#f2"],
    ["viz.box_plots#assessment:identify_boxplot_quartile_and_whisker_positions"]
)

# s14 check – f3 (condensed display)
s14_lsb = step_check(
    T_LSB + ".s14", [C_BOX], "quick check",
    "When to Use a Box Plot",
    "What is a box plot's main advantage over a bar chart for delivery-time data?",
    ["viz.box_plots#f3"],
    ["viz.box_plots#assessment:identify_boxplot_use_case"]
)

# s15 hands_on – box plots
s15_lsb = step_hands_on(
    T_LSB + ".s15", [C_BOX], "hands-on",
    "Compare City Delivery Spreads with plt.boxplot()",
    "Filter the orders dataset by city, then pass the three arrays to plt.boxplot() with tick_labels.",
    ["viz.box_plots#f1", "viz.box_plots#f2", "viz.box_plots#f4"],
    ["viz.box_plots#practice",
     "viz.box_plots#assessment:draw_multi_group_boxplot_with_tick_labels"]
)

# s16 recap
s16_recap_lsb = step_recap(
    T_LSB + ".s16", [C_LINE, C_SCAT, C_BOX],
    "Line, Scatter, and Box Plots: What You Learned",
    "Three chart types for three different questions about numeric data.",
    [
        prose(T_LSB + ".s16.b01", "takeaway",
              "Use `plt.plot(x, y)` to show how a value changes over time. "
              "Use `plt.scatter(x, y)` to explore the relationship between two numeric variables. "
              "Use `plt.boxplot(x)` to compare the full spread — median, quartiles, and outliers — "
              "across multiple groups.",
              [C_LINE, C_SCAT, C_BOX], [], []),
        up_next(T_LSB + ".s16.b02",
                "Up next: Labeling Charts and Choosing Chart Types",
                "Next you'll add titles, axis labels, and legends to make charts self-explanatory, "
                "then learn a decision framework for choosing the right chart type for any question.")
    ],
    tb_ids=[], fact_ids=[]
)

# remediation steps
rem_lsb_s03 = step_remediation(
    T_LSB + ".r01", [C_LINE],
    "The Connecting Line Reveals the Trend",
    "Without the line, you see points; with it, you see the direction of change.",
    [
        prose(T_LSB + ".r01.b01", "mechanism",
              "A line graph plots the measured points and then draws a line that connects those points, "
              "making it easier to see how the values rose, fell, or stayed the same over time. "
              "The line between day 2 (23 min) and day 3 (19 min) slopes downward — showing improvement — "
              "in a way that a list of numbers does not.",
              [C_LINE], ["viz.line_plots#tb2"], ["viz.line_plots#f3"])
    ],
    tb_ids=["viz.line_plots#tb2"], fact_ids=["viz.line_plots#f3"]
)

rem_lsb_s07 = step_remediation(
    T_LSB + ".r02", [C_SCAT],
    "Scatter Plots Show Relationships Between Two Variables",
    "Each point encodes one (x, y) pair — the pattern of points reveals whether the two variables move together.",
    [
        prose(T_LSB + ".r02.b01", "definition",
              "A scatterplot shows the relationship between two numerical variables plotted simultaneously "
              "along the horizontal and vertical axis. "
              "`plt.scatter(orders['distance_km'], orders['delivery_time_minutes'])` places one point per "
              "order — if longer distances consistently produce longer times, the points will trend upward "
              "from left to right.",
              [C_SCAT], ["viz.scatter_plots#tb1", "viz.scatter_plots#tb2"],
              ["viz.scatter_plots#f1", "viz.scatter_plots#f2"])
    ],
    tb_ids=["viz.scatter_plots#tb1", "viz.scatter_plots#tb2"],
    fact_ids=["viz.scatter_plots#f1", "viz.scatter_plots#f2"]
)

rem_lsb_s13 = step_remediation(
    T_LSB + ".r03", [C_BOX],
    "The Box Spans Q1 to Q3",
    "The box edges mark the first and third quartiles; the line inside marks the median.",
    [
        prose(T_LSB + ".r03.b01", "mechanism",
              "The box extends from the first quartile (Q1) to the third quartile (Q3) of the data, "
              "with a line at the median. "
              "The whiskers extend to the farthest data point lying within 1.5× the IQR from the box; "
              "points past the whisker ends are flier points (outliers).",
              [C_BOX], ["viz.box_plots#tb2"], ["viz.box_plots#f2"])
    ],
    tb_ids=["viz.box_plots#tb2"], fact_ids=["viz.box_plots#f2"]
)

rem_lsb_s14 = step_remediation(
    T_LSB + ".r04", [C_BOX],
    "Box Plots Compare Distributions, Not Just Averages",
    "A box plot shows spread, median, and outliers — a bar chart shows only a single summary value per group.",
    [
        prose(T_LSB + ".r04.b01", "definition",
              "Boxplots offer a condensed display for comparing the distributions of multiple datasets "
              "side by side. Unlike a bar chart that shows only the average per city, a box plot shows "
              "how spread out the delivery times are, where the middle half falls, and whether any "
              "deliveries are unusually slow.",
              [C_BOX], ["viz.box_plots#tb1"], ["viz.box_plots#f3"])
    ],
    tb_ids=["viz.box_plots#tb1"], fact_ids=["viz.box_plots#f3"]
)

tile_line_scatter_box = {
    "tile_id": T_LSB,
    "title": "Line Plots, Scatter Plots, and Box Plots",
    "summary": "Plot trends over time with plt.plot(), relationships between two numeric variables with plt.scatter(), and per-group distributions with plt.boxplot().",
    "steps": [s01_lsb, s02_lsb, s03_lsb, s04_lsb, s05_lsb, s06_lsb, s07_lsb, s08_lsb,
              s09_lsb, s10_lsb, s11_lsb, s12_lsb, s13_lsb, s14_lsb, s15_lsb, s16_recap_lsb],
    "remediation_steps": [rem_lsb_s03, rem_lsb_s07, rem_lsb_s13, rem_lsb_s14]
}


# ═══════════════════════════════════════════════════════════════════════════════
# TILE 3: tile_viz_labeling_chart_selection
# ═══════════════════════════════════════════════════════════════════════════════

T_LCS = "tile_viz_labeling_chart_selection"
C_LAB = "viz.labeling_annotation"
C_SEL = "viz.chart_type_selection"

# s01 explainer – labeling (before_after visual)
label_before_code = code_walk(
    T_LCS + ".s01.b01.before",
    "fig, ax = plt.subplots()\nax.plot(days, lagos_avg)",
    [{"start_line": 2, "end_line": 2, "text": "No labels — the reader cannot tell what the axes or line represent"}],
    [C_LAB], ["viz.labeling_annotation#tb1"], ["viz.labeling_annotation#f1"]
)
label_after_code = code_walk(
    T_LCS + ".s01.b01.after",
    "fig, ax = plt.subplots()\nax.plot(days, lagos_avg, label='Lagos')\nax.set_xlabel('Day')\nax.set_ylabel('Average delivery time (minutes)')\nax.set_title('Average delivery time by day')\nax.legend()",
    [
        {"start_line": 2, "end_line": 2, "text": "label='Lagos' names this series for the legend"},
        {"start_line": 3, "end_line": 3, "text": "ax.set_xlabel() labels the x-axis"},
        {"start_line": 4, "end_line": 4, "text": "ax.set_ylabel() labels the y-axis"},
        {"start_line": 5, "end_line": 5, "text": "ax.set_title() sets the Axes title"},
        {"start_line": 6, "end_line": 6, "text": "ax.legend() displays the legend for all labeled series"}
    ],
    [C_LAB], ["viz.labeling_annotation#tb2", "viz.labeling_annotation#tb3"],
    ["viz.labeling_annotation#f1", "viz.labeling_annotation#f2"]
)

s01_lcs = step_explainer(
    T_LCS + ".s01", [C_LAB], "chart labeling",
    "Titles, Axis Labels, and Legends",
    "A chart without labels forces the reader to guess — three method calls make it self-explanatory.",
    [
        prose(T_LCS + ".s01.b02", "intro",
              "Titles, axis labels, and legends are the text that tells a reader what a plot shows. "
              "Matplotlib gives two parallel ways to add them, depending on whether you are working with "
              "an Axes object or the pyplot interface directly.",
              [C_LAB], ["viz.labeling_annotation#tb1"], []),
        prose(T_LCS + ".s01.b03", "syntax",
              "`ax.set_xlabel('...')` and `ax.set_ylabel('...')` set the x-axis and y-axis labels, "
              "and `ax.set_title('...')` sets the Axes title. "
              "`ax.set_xlabel('Day')`, `ax.set_ylabel('Average delivery time (minutes)')`, and "
              "`ax.set_title('Average delivery time by day')` label the Lagos trend line.",
              [C_LAB], ["viz.labeling_annotation#tb2"], ["viz.labeling_annotation#f1"]),
        prose(T_LCS + ".s01.b04", "syntax",
              "Passing `label='...'` to a plotting call and then calling `ax.legend()` displays a legend "
              "identifying each labeled series. "
              "`ax.plot(days, lagos_avg, label='Lagos')` followed by `ax.legend()` shows a legend "
              "identifying the Lagos line — which matters once a second city's line is added.",
              [C_LAB], ["viz.labeling_annotation#tb3"], ["viz.labeling_annotation#f2"]),
        before_after(
            T_LCS + ".s01.b05",
            label_before_code, label_after_code,
            "Adding set_xlabel, set_ylabel, set_title, and legend turns an unlabeled plot into a self-explanatory chart.",
            [C_LAB], ["viz.labeling_annotation#tb1", "viz.labeling_annotation#tb2", "viz.labeling_annotation#tb3"],
            ["viz.labeling_annotation#f1", "viz.labeling_annotation#f2"],
            anchors=["viz.labeling_annotation#visual"]
        )
    ],
    tb_ids=["viz.labeling_annotation#tb1", "viz.labeling_annotation#tb2", "viz.labeling_annotation#tb3"],
    fact_ids=["viz.labeling_annotation#f1", "viz.labeling_annotation#f2"],
    anchors=["viz.labeling_annotation#visual"]
)

# s02 explainer – pyplot interface (f3)
s02_lcs = step_explainer(
    T_LCS + ".s02", [C_LAB], "chart labeling",
    "The pyplot Shorthand",
    "plt.xlabel(), plt.ylabel(), and plt.title() do the same job as the Axes methods.",
    [
        prose(T_LCS + ".s02.b01", "syntax",
              "In the pyplot interface, `plt.xlabel()`, `plt.ylabel()`, and `plt.title()` set the same "
              "label/title elements on the current Axes — the pyplot equivalents of `ax.set_xlabel()`, "
              "`ax.set_ylabel()`, and `ax.set_title()`.",
              [C_LAB], ["viz.labeling_annotation#tb4"], ["viz.labeling_annotation#f3"])
    ],
    tb_ids=["viz.labeling_annotation#tb4"],
    fact_ids=["viz.labeling_annotation#f3"]
)

# s03 check – f1 (axes labeling methods)
s03_lcs = step_check(
    T_LCS + ".s03", [C_LAB], "quick check",
    "Axes Labeling Methods",
    "Which three method calls add a title and both axis labels to an Axes object?",
    ["viz.labeling_annotation#f1"],
    ["viz.labeling_annotation#assessment:apply_axes_object_labeling_methods"]
)

# s04 check – f3 (pyplot interface)
s04_lcs = step_check(
    T_LCS + ".s04", [C_LAB], "quick check",
    "pyplot vs Axes Interface",
    "What is the pyplot equivalent of ax.set_title()?",
    ["viz.labeling_annotation#f3"],
    ["viz.labeling_annotation#assessment:apply_pyplot_interface_labeling_functions"]
)

# s05 hands_on – labeling
s05_lcs = step_hands_on(
    T_LCS + ".s05", [C_LAB], "hands-on",
    "Label a Two-Series Line Chart",
    "Add a title, both axis labels, and a legend that distinguishes the Lagos and Abuja lines.",
    ["viz.labeling_annotation#f1", "viz.labeling_annotation#f2", "viz.labeling_annotation#f3"],
    ["viz.labeling_annotation#practice",
     "viz.labeling_annotation#assessment:add_title_axis_labels_and_legend_to_unlabeled_plot",
     "viz.labeling_annotation#assessment:attach_legend_via_label_kwarg_and_legend_call"]
)

# s06 explainer – chart type selection (side_by_side visual)
# side_by_side: left = scatter chart, right = bar chart
sel_left_chart = chart(
    T_LCS + ".s06.b01.left", "scatter", "ds.chart_selection_mini",
    "Scatter: distance vs delivery time",
    "A scatter plot of distance_km vs delivery_minutes showing a positive relationship between the two variables.",
    {"x": {"field": "distance_km", "type": "quantitative", "title": "Distance (km)"},
     "y": {"field": "delivery_minutes", "type": "quantitative", "title": "Delivery time (min)"}},
    [C_SEL], ["viz.chart_type_selection#tb1"],
    ["viz.chart_type_selection#f4"]
)
sel_right_chart = chart(
    T_LCS + ".s06.b01.right", "bar", "ds.orders",
    "Bar: average delivery time by city",
    "A bar chart showing average delivery_time_minutes for Lagos, Abuja, and Kano side by side.",
    {"x": {"field": "city", "type": "nominal", "title": "City"},
     "y": {"field": "delivery_time_minutes", "type": "quantitative", "aggregate": "mean",
           "title": "Avg delivery time (min)"}},
    [C_SEL], ["viz.chart_type_selection#tb1"],
    ["viz.chart_type_selection#f1"]
)

s06_lcs = step_explainer(
    T_LCS + ".s06", [C_SEL], "chart selection",
    "Choosing the Right Chart for Your Question",
    "The chart type follows from the analytical question — name what you're asking before you plot.",
    [
        prose(T_LCS + ".s06.b02", "definition",
              "Use a bar chart to compare a numeric value across discrete categories. "
              "Use a histogram to see how a numeric variable is distributed. "
              "Use a line graph to show how a value changes over time. "
              "Use a scatter plot to explore the relationship between two numeric variables.",
              [C_SEL], ["viz.chart_type_selection#tb1"],
              ["viz.chart_type_selection#f1", "viz.chart_type_selection#f2",
               "viz.chart_type_selection#f3", "viz.chart_type_selection#f4"]),
        prose(T_LCS + ".s06.b03", "definition",
              "Use a box plot to compare the full spread — median, quartiles, and outliers — "
              "of a numeric variable across several groups side by side.",
              [C_SEL], ["viz.chart_type_selection#tb2"],
              ["viz.chart_type_selection#f5"]),
        side_by_side(
            T_LCS + ".s06.b04",
            sel_left_chart, sel_right_chart,
            "Scatter: relationship between two numeric variables",
            "Bar: numeric value compared across categories",
            "The same delivery dataset rendered two ways — the question you ask determines which chart fits.",
            [C_SEL], ["viz.chart_type_selection#tb1", "viz.chart_type_selection#tb2"],
            ["viz.chart_type_selection#f1", "viz.chart_type_selection#f2",
             "viz.chart_type_selection#f3", "viz.chart_type_selection#f4",
             "viz.chart_type_selection#f5"],
            anchors=["viz.chart_type_selection#visual"]
        )
    ],
    tb_ids=["viz.chart_type_selection#tb1", "viz.chart_type_selection#tb2"],
    fact_ids=["viz.chart_type_selection#f1", "viz.chart_type_selection#f2",
              "viz.chart_type_selection#f3", "viz.chart_type_selection#f4",
              "viz.chart_type_selection#f5"],
    anchors=["viz.chart_type_selection#visual"]
)

# s07 video
s07_lcs = step_video(
    T_LCS + ".s07", [C_SEL], "watch",
    "Chart Selection: Boxplot Fitness and Histogram Construction",
    ["seg_viz.chart_type_selection_Z77c53eYtHc_149_201",
     "seg_viz.chart_type_selection_ZyTO4SwhSeE_503_649"],
    ["viz.chart_type_selection#f2", "viz.chart_type_selection#f5"]
)

# s08 check – all five facts
s08_lcs = step_check(
    T_LCS + ".s08", [C_SEL], "quick check",
    "Match the Question to the Chart",
    "For each analytical question, choose the chart type that fits best.",
    ["viz.chart_type_selection#f1", "viz.chart_type_selection#f2",
     "viz.chart_type_selection#f3", "viz.chart_type_selection#f4",
     "viz.chart_type_selection#f5"],
    ["viz.chart_type_selection#assessment:select_chart_type_for_analytical_question"]
)

# s09 check – f3 + f5 (line and boxplot)
s09_lcs = step_check(
    T_LCS + ".s09", [C_SEL], "quick check",
    "Line Graph or Box Plot?",
    "Which chart type shows how a value changes over time, and which compares spread across groups?",
    ["viz.chart_type_selection#f3", "viz.chart_type_selection#f5"],
    ["viz.chart_type_selection#assessment:identify_line_graph_use_case",
     "viz.chart_type_selection#assessment:identify_boxplot_use_case"]
)

# s10 hands_on – chart selection
s10_lcs = step_hands_on(
    T_LCS + ".s10", [C_SEL], "hands-on",
    "Choose and Build the Right Chart",
    "Given a question about whether longer distances lead to longer delivery times, choose the right chart type and build it.",
    ["viz.chart_type_selection#f1", "viz.chart_type_selection#f4"],
    ["viz.chart_type_selection#practice",
     "viz.chart_type_selection#assessment:select_chart_type_for_analytical_question",
     "viz.chart_type_selection#assessment:identify_scatter_plot_use_case"]
)

# s11 recap
s11_recap_lcs = step_recap(
    T_LCS + ".s11", [C_LAB, C_SEL],
    "Labeling and Chart Selection: What You Learned",
    "Labels make charts readable; the right chart type makes the answer visible.",
    [
        prose(T_LCS + ".s11.b01", "takeaway",
              "Add `ax.set_xlabel()`, `ax.set_ylabel()`, and `ax.set_title()` to label every chart. "
              "Use `label='...'` plus `ax.legend()` when a chart has more than one series. "
              "Choose the chart type by naming the question: category comparison → bar; "
              "distribution → histogram; trend over time → line; "
              "relationship between two variables → scatter; spread across groups → box plot.",
              [C_LAB, C_SEL], ["viz.chart_type_selection#tb3"],
              ["viz.chart_type_selection#f1", "viz.chart_type_selection#f2",
               "viz.chart_type_selection#f3", "viz.chart_type_selection#f4",
               "viz.chart_type_selection#f5"]),
        up_next(T_LCS + ".s11.b02",
                "Up next: Seaborn — DataFrame Plotting, Stats, and Themes",
                "Next you'll use seaborn's dataframe-aware plotting functions, add automatic statistical "
                "estimates with sns.regplot(), and apply themes and palettes with sns.set_theme().")
    ],
    tb_ids=["viz.chart_type_selection#tb3"],
    fact_ids=["viz.chart_type_selection#f1", "viz.chart_type_selection#f2",
              "viz.chart_type_selection#f3", "viz.chart_type_selection#f4",
              "viz.chart_type_selection#f5"]
)

# remediation steps
rem_lcs_s03 = step_remediation(
    T_LCS + ".r01", [C_LAB],
    "Three Calls to Label an Axes",
    "ax.set_xlabel(), ax.set_ylabel(), and ax.set_title() are the three Axes labeling methods.",
    [
        prose(T_LCS + ".r01.b01", "syntax",
              "`ax.set_xlabel('...')` and `ax.set_ylabel('...')` set the x-axis and y-axis labels, "
              "and `ax.set_title('...')` sets the Axes title. "
              "All three take a string argument — for example `ax.set_xlabel('Day')` labels the x-axis "
              "with the word 'Day'.",
              [C_LAB], ["viz.labeling_annotation#tb2"], ["viz.labeling_annotation#f1"])
    ],
    tb_ids=["viz.labeling_annotation#tb2"], fact_ids=["viz.labeling_annotation#f1"]
)

rem_lcs_s04 = step_remediation(
    T_LCS + ".r02", [C_LAB],
    "pyplot Labeling Functions",
    "plt.xlabel(), plt.ylabel(), and plt.title() are the pyplot equivalents of the Axes methods.",
    [
        prose(T_LCS + ".r02.b01", "syntax",
              "In the pyplot interface, `plt.xlabel()`, `plt.ylabel()`, and `plt.title()` set the same "
              "label/title elements on the current Axes — the pyplot equivalents of `ax.set_xlabel()`, "
              "`ax.set_ylabel()`, and `ax.set_title()`.",
              [C_LAB], ["viz.labeling_annotation#tb4"], ["viz.labeling_annotation#f3"])
    ],
    tb_ids=["viz.labeling_annotation#tb4"], fact_ids=["viz.labeling_annotation#f3"]
)

rem_lcs_s08 = step_remediation(
    T_LCS + ".r03", [C_SEL],
    "Five Chart Types, Five Questions",
    "Each chart type answers a different analytical question — match the question to the chart.",
    [
        prose(T_LCS + ".r03.b01", "definition",
              "Bar chart: compare a numeric value across discrete categories. "
              "Histogram: see how a numeric variable is distributed. "
              "Line graph: show how a value changes over time. "
              "Scatter plot: explore the relationship between two numeric variables. "
              "Box plot: compare the full spread across several groups.",
              [C_SEL], ["viz.chart_type_selection#tb1", "viz.chart_type_selection#tb2"],
              ["viz.chart_type_selection#f1", "viz.chart_type_selection#f2",
               "viz.chart_type_selection#f3", "viz.chart_type_selection#f4",
               "viz.chart_type_selection#f5"])
    ],
    tb_ids=["viz.chart_type_selection#tb1", "viz.chart_type_selection#tb2"],
    fact_ids=["viz.chart_type_selection#f1", "viz.chart_type_selection#f2",
              "viz.chart_type_selection#f3", "viz.chart_type_selection#f4",
              "viz.chart_type_selection#f5"]
)

rem_lcs_s09 = step_remediation(
    T_LCS + ".r04", [C_SEL],
    "Line Graph vs Box Plot",
    "A line graph tracks change over time; a box plot compares spread across groups.",
    [
        prose(T_LCS + ".r04.b01", "definition",
              "A line graph is best when you want to show how the value of something changes over time. "
              "A box plot offers a condensed display for comparing the distributions of multiple datasets "
              "side by side — showing spread, median, and outliers per group, not a trend over time.",
              [C_SEL], ["viz.chart_type_selection#tb1"],
              ["viz.chart_type_selection#f3", "viz.chart_type_selection#f5"])
    ],
    tb_ids=["viz.chart_type_selection#tb1"],
    fact_ids=["viz.chart_type_selection#f3", "viz.chart_type_selection#f5"]
)

tile_labeling_chart_selection = {
    "tile_id": T_LCS,
    "title": "Labeling Charts and Selecting Chart Types",
    "summary": "Add titles, axis labels, and legends with ax.set_xlabel/ylabel/title and ax.legend(), then choose the right chart type by matching it to the analytical question.",
    "steps": [s01_lcs, s02_lcs, s03_lcs, s04_lcs, s05_lcs,
              s06_lcs, s07_lcs, s08_lcs, s09_lcs, s10_lcs, s11_recap_lcs],
    "remediation_steps": [rem_lcs_s03, rem_lcs_s04, rem_lcs_s08, rem_lcs_s09]
}


# ═══════════════════════════════════════════════════════════════════════════════
# TILE 4: tile_viz_seaborn_stats_themes
# ═══════════════════════════════════════════════════════════════════════════════

T_SST = "tile_viz_seaborn_stats_themes"
C_SNS_DF = "viz.seaborn_dataframe_plotting"
C_SNS_STAT = "viz.seaborn_statistical_functions"
C_SNS_THEME = "viz.seaborn_themes_palettes"

# s01 explainer – seaborn dataframe plotting (chart visual)
s01_sst = step_explainer(
    T_SST + ".s01", [C_SNS_DF], "seaborn",
    "Plotting Directly from a DataFrame with Seaborn",
    "Seaborn's functions take column names instead of extracted arrays — less code, same chart.",
    [
        prose(T_SST + ".s01.b01", "intro",
              "Most matplotlib calls so far have needed you to pull a column out of `orders` yourself "
              "before plotting it. Seaborn's plotting functions operate on dataframes and arrays containing "
              "whole datasets, taking only the names of the variables and their roles in the plot "
              "(for example `data=`, `x=`, `y=`) rather than requiring the caller to extract each array.",
              [C_SNS_DF], ["viz.seaborn_dataframe_plotting#tb1"],
              ["viz.seaborn_dataframe_plotting#f1"]),
        prose(T_SST + ".s01.b02", "syntax",
              "`seaborn.barplot(data=..., x=..., y=...)` visualizes an aggregate statistical estimate "
              "for each category as a bar; its default estimator is the mean, and it draws an error bar "
              "(uncertainty indicator) around each bar by default. "
              "`sns.barplot(data=orders, x='city', y='delivery_time_minutes')` produces a per-city "
              "mean bar chart without a groupby call.",
              [C_SNS_DF], ["viz.seaborn_dataframe_plotting#tb2"],
              ["viz.seaborn_dataframe_plotting#f2"]),
        chart(
            T_SST + ".s01.b03", "bar", "ds.orders",
            "Average Delivery Time by City — seaborn barplot",
            "A seaborn barplot showing the mean delivery_time_minutes for Lagos, Abuja, and Kano, "
            "with error bars indicating uncertainty around each mean.",
            {"x": {"field": "city", "type": "nominal", "title": "City"},
             "y": {"field": "delivery_time_minutes", "type": "quantitative", "aggregate": "mean",
                   "title": "Avg delivery time (min)"}},
            [C_SNS_DF],
            ["viz.seaborn_dataframe_plotting#tb1", "viz.seaborn_dataframe_plotting#tb2"],
            ["viz.seaborn_dataframe_plotting#f1", "viz.seaborn_dataframe_plotting#f2"],
            anchors=["viz.seaborn_dataframe_plotting#visual"],
            columns=["city", "delivery_time_minutes"]
        )
    ],
    tb_ids=["viz.seaborn_dataframe_plotting#tb1", "viz.seaborn_dataframe_plotting#tb2"],
    fact_ids=["viz.seaborn_dataframe_plotting#f1", "viz.seaborn_dataframe_plotting#f2"],
    anchors=["viz.seaborn_dataframe_plotting#visual"]
)

# s02 check – f1 + f2
s02_sst = step_check(
    T_SST + ".s02", [C_SNS_DF], "quick check",
    "Seaborn's DataFrame Interface",
    "How does sns.barplot() differ from plt.bar() in how it receives data?",
    ["viz.seaborn_dataframe_plotting#f1", "viz.seaborn_dataframe_plotting#f2"],
    ["viz.seaborn_dataframe_plotting#assessment:build_seaborn_barplot_from_dataframe_using_column_names"]
)

# s03 hands_on – seaborn barplot
s03_sst = step_hands_on(
    T_SST + ".s03", [C_SNS_DF], "hands-on",
    "Build a Seaborn Bar Chart from a DataFrame",
    "Call sns.barplot() with data=orders and column names for x and y — no groupby needed.",
    ["viz.seaborn_dataframe_plotting#f1", "viz.seaborn_dataframe_plotting#f2"],
    ["viz.seaborn_dataframe_plotting#practice",
     "viz.seaborn_dataframe_plotting#assessment:build_seaborn_barplot_from_dataframe_using_column_names"]
)

# s04 explainer – seaborn statistical functions (before_after visual)
stat_before_chart = chart(
    T_SST + ".s04.b01.before", "scatter", "ds.orders",
    "Scatter: distance vs delivery time (no trend line)",
    "A plain scatter plot of distance_km vs delivery_time_minutes with no regression line.",
    {"x": {"field": "distance_km", "type": "quantitative", "title": "Distance (km)"},
     "y": {"field": "delivery_time_minutes", "type": "quantitative", "title": "Delivery time (min)"}},
    [C_SNS_STAT], ["viz.seaborn_statistical_functions#tb1"],
    ["viz.seaborn_statistical_functions#f1"],
    columns=["distance_km", "delivery_time_minutes"]
)
stat_after_chart = chart(
    T_SST + ".s04.b01.after", "scatter", "ds.orders",
    "regplot: scatter + fitted regression line",
    "The same scatter plot of distance_km vs delivery_time_minutes with a fitted linear regression line added by sns.regplot().",
    {"x": {"field": "distance_km", "type": "quantitative", "title": "Distance (km)"},
     "y": {"field": "delivery_time_minutes", "type": "quantitative", "title": "Delivery time (min)"}},
    [C_SNS_STAT], ["viz.seaborn_statistical_functions#tb2"],
    ["viz.seaborn_statistical_functions#f2"],
    columns=["distance_km", "delivery_time_minutes"]
)

s04_sst = step_explainer(
    T_SST + ".s04", [C_SNS_STAT], "seaborn",
    "Automatic Statistical Estimates with Seaborn",
    "Many seaborn functions compute a statistical estimate for you — sns.regplot() adds a fitted regression line to a scatter plot.",
    [
        prose(T_SST + ".s04.b02", "definition",
              "Many seaborn functions will automatically perform the statistical estimation necessary to "
              "answer questions such as the average value of one variable as a function of other variables. "
              "`sns.barplot()` already does this — it computes the mean per category without a groupby call.",
              [C_SNS_STAT], ["viz.seaborn_statistical_functions#tb1"],
              ["viz.seaborn_statistical_functions#f1"]),
        prose(T_SST + ".s04.b03", "syntax",
              "`seaborn.regplot(data=..., x=..., y=...)` plots a scatterplot of the observations together "
              "with a fitted linear regression line. "
              "`sns.regplot(data=orders, x='distance_km', y='delivery_time_minutes')` draws each order "
              "as a point and overlays the best-fit line through those points.",
              [C_SNS_STAT], ["viz.seaborn_statistical_functions#tb2"],
              ["viz.seaborn_statistical_functions#f2"]),
        before_after(
            T_SST + ".s04.b04",
            stat_before_chart, stat_after_chart,
            "sns.regplot() adds a fitted regression line to the scatter plot, making the statistical relationship visible.",
            [C_SNS_STAT],
            ["viz.seaborn_statistical_functions#tb1", "viz.seaborn_statistical_functions#tb2"],
            ["viz.seaborn_statistical_functions#f1", "viz.seaborn_statistical_functions#f2"],
            anchors=["viz.seaborn_statistical_functions#visual"]
        )
    ],
    tb_ids=["viz.seaborn_statistical_functions#tb1", "viz.seaborn_statistical_functions#tb2"],
    fact_ids=["viz.seaborn_statistical_functions#f1", "viz.seaborn_statistical_functions#f2"],
    anchors=["viz.seaborn_statistical_functions#visual"]
)

# s05 check – f1 (automatic estimation)
s05_sst = step_check(
    T_SST + ".s05", [C_SNS_STAT], "quick check",
    "Seaborn's Automatic Estimation",
    "What does seaborn do automatically that you would otherwise have to compute yourself?",
    ["viz.seaborn_statistical_functions#f1"],
    ["viz.seaborn_statistical_functions#assessment:identify_seaborn_automatic_statistical_estimation"]
)

# s06 check – f1 + f2 (select correct function)
s06_sst = step_check(
    T_SST + ".s06", [C_SNS_STAT], "quick check",
    "Choosing the Right Seaborn Function",
    "Which seaborn function adds a fitted regression line to a scatter plot?",
    ["viz.seaborn_statistical_functions#f1", "viz.seaborn_statistical_functions#f2"],
    ["viz.seaborn_statistical_functions#assessment:select_correct_seaborn_statistical_function_for_given_question"]
)

# s07 hands_on – regplot
s07_sst = step_hands_on(
    T_SST + ".s07", [C_SNS_STAT], "hands-on",
    "Add a Regression Line with sns.regplot()",
    "Call sns.regplot() with data=orders and column names to produce a scatter plot with a fitted trend line.",
    ["viz.seaborn_statistical_functions#f2"],
    ["viz.seaborn_statistical_functions#practice",
     "viz.seaborn_statistical_functions#assessment:apply_regplot_to_visualize_relationship_with_fitted_trend"]
)

# s08 explainer – seaborn themes (before_after visual)
theme_before_chart = chart(
    T_SST + ".s08.b01.before", "bar", "ds.theming_demo",
    "Default matplotlib styling",
    "A seaborn barplot of category vs value rendered with default matplotlib styling — grey background, no gridlines.",
    {"x": {"field": "category", "type": "nominal", "title": "City"},
     "y": {"field": "value", "type": "quantitative", "title": "Avg delivery time (min)"}},
    [C_SNS_THEME], ["viz.seaborn_themes_palettes#tb1"],
    ["viz.seaborn_themes_palettes#f2"]
)
theme_after_chart = chart(
    T_SST + ".s08.b01.after", "bar", "ds.theming_demo",
    "After sns.set_theme(style='whitegrid', palette='deep')",
    "The same seaborn barplot after calling sns.set_theme(style='whitegrid', palette='deep') — white background with gridlines and the 'deep' color palette.",
    {"x": {"field": "category", "type": "nominal", "title": "City"},
     "y": {"field": "value", "type": "quantitative", "title": "Avg delivery time (min)"}},
    [C_SNS_THEME], ["viz.seaborn_themes_palettes#tb1", "viz.seaborn_themes_palettes#tb2"],
    ["viz.seaborn_themes_palettes#f1", "viz.seaborn_themes_palettes#f2"]
)

s08_sst = step_explainer(
    T_SST + ".s08", [C_SNS_THEME], "seaborn themes",
    "Applying Themes and Palettes with sns.set_theme()",
    "One call before your plot changes the background, gridlines, and colors for every chart that follows.",
    [
        prose(T_SST + ".s08.b02", "syntax",
              "`seaborn.set_theme()` accepts a `style` parameter (default `'darkgrid'`) and a `palette` "
              "parameter (default `'deep'`) among its arguments, which set the plot's background/gridline "
              "style and its color palette respectively. "
              "`sns.set_theme(style='whitegrid', palette='deep')` switches to a white background with "
              "gridlines.",
              [C_SNS_THEME], ["viz.seaborn_themes_palettes#tb1"],
              ["viz.seaborn_themes_palettes#f2"]),
        prose(T_SST + ".s08.b03", "mechanism",
              "`sns.set_theme(style=..., palette=...)` changes the global defaults for all plots using "
              "the matplotlib rcParams system, so it affects matplotlib plots too, even ones not made "
              "with seaborn. Calling `sns.set_theme()` changes how plots drawn after that call look — "
              "it does not restyle a figure you already drew and displayed.",
              [C_SNS_THEME], ["viz.seaborn_themes_palettes#tb2"],
              ["viz.seaborn_themes_palettes#f1"]),
        before_after(
            T_SST + ".s08.b04",
            theme_before_chart, theme_after_chart,
            "sns.set_theme(style='whitegrid', palette='deep') changes the background, gridlines, and colors for all subsequent plots.",
            [C_SNS_THEME],
            ["viz.seaborn_themes_palettes#tb1", "viz.seaborn_themes_palettes#tb2"],
            ["viz.seaborn_themes_palettes#f1", "viz.seaborn_themes_palettes#f2"],
            anchors=["viz.seaborn_themes_palettes#visual"]
        )
    ],
    tb_ids=["viz.seaborn_themes_palettes#tb1", "viz.seaborn_themes_palettes#tb2"],
    fact_ids=["viz.seaborn_themes_palettes#f1", "viz.seaborn_themes_palettes#f2"],
    anchors=["viz.seaborn_themes_palettes#visual"]
)

# s09 check – f1 (global rcParams effect)
s09_sst = step_check(
    T_SST + ".s09", [C_SNS_THEME], "quick check",
    "Global Effect of sns.set_theme()",
    "Why does sns.set_theme() affect matplotlib plots that were not made with seaborn?",
    ["viz.seaborn_themes_palettes#f1"],
    ["viz.seaborn_themes_palettes#assessment:explain_global_rcparams_effect_on_subsequent_plots"]
)

# s10 hands_on – themes
s10_sst = step_hands_on(
    T_SST + ".s10", [C_SNS_THEME], "hands-on",
    "Apply a Theme and Palette with sns.set_theme()",
    "Call sns.set_theme() with a named style and palette before drawing a seaborn plot.",
    ["viz.seaborn_themes_palettes#f1", "viz.seaborn_themes_palettes#f2"],
    ["viz.seaborn_themes_palettes#practice",
     "viz.seaborn_themes_palettes#assessment:apply_seaborn_theme_and_palette_to_produce_polished_plot",
     "viz.seaborn_themes_palettes#assessment:identify_style_and_palette_parameters_and_their_defaults"]
)

# s11 recap
s11_recap_sst = step_recap(
    T_SST + ".s11", [C_SNS_DF, C_SNS_STAT, C_SNS_THEME],
    "Seaborn: What You Learned",
    "Seaborn plots from DataFrames, computes statistics automatically, and applies themes globally.",
    [
        prose(T_SST + ".s11.b01", "takeaway",
              "Use `sns.barplot(data=..., x=..., y=...)` to plot directly from a DataFrame without "
              "extracting columns. Use `sns.regplot(data=..., x=..., y=...)` to add a fitted regression "
              "line to a scatter plot. Call `sns.set_theme(style=..., palette=...)` before plotting to "
              "apply a consistent visual style to all subsequent charts.",
              [C_SNS_DF, C_SNS_STAT, C_SNS_THEME], [], []),
        up_next(T_SST + ".s11.b02",
                "Up next: Custom Styling and Multi-Panel Figures",
                "Next you'll apply matplotlib style sheets and rcParams for custom branding, "
                "and use plt.subplots(nrows, ncols) to arrange multiple charts in a single figure.")
    ],
    tb_ids=[], fact_ids=[]
)

# remediation steps
rem_sst_s02 = step_remediation(
    T_SST + ".r01", [C_SNS_DF],
    "Seaborn Takes Column Names, Not Arrays",
    "Pass the DataFrame and column names — seaborn extracts the data for you.",
    [
        prose(T_SST + ".r01.b01", "definition",
              "Seaborn's plotting functions operate on dataframes and arrays containing whole datasets, "
              "taking only the names of the variables and their roles in the plot (`data=`, `x=`, `y=`) "
              "rather than requiring the caller to extract each array. "
              "`sns.barplot(data=orders, x='city', y='delivery_time_minutes')` produces a per-city "
              "mean bar chart without a groupby call.",
              [C_SNS_DF],
              ["viz.seaborn_dataframe_plotting#tb1", "viz.seaborn_dataframe_plotting#tb2"],
              ["viz.seaborn_dataframe_plotting#f1", "viz.seaborn_dataframe_plotting#f2"])
    ],
    tb_ids=["viz.seaborn_dataframe_plotting#tb1", "viz.seaborn_dataframe_plotting#tb2"],
    fact_ids=["viz.seaborn_dataframe_plotting#f1", "viz.seaborn_dataframe_plotting#f2"]
)

rem_sst_s05 = step_remediation(
    T_SST + ".r02", [C_SNS_STAT],
    "Seaborn Computes Statistics Automatically",
    "You don't need to compute the mean or fit a regression line yourself — seaborn does it.",
    [
        prose(T_SST + ".r02.b01", "definition",
              "Many seaborn functions will automatically perform the statistical estimation necessary to "
              "answer questions such as the average value of one variable as a function of other variables. "
              "`sns.barplot()` computes the mean per category; `sns.regplot()` fits a linear regression "
              "line through the scatter points — both without any manual calculation.",
              [C_SNS_STAT],
              ["viz.seaborn_statistical_functions#tb1"],
              ["viz.seaborn_statistical_functions#f1"])
    ],
    tb_ids=["viz.seaborn_statistical_functions#tb1"],
    fact_ids=["viz.seaborn_statistical_functions#f1"]
)

rem_sst_s09 = step_remediation(
    T_SST + ".r03", [C_SNS_THEME],
    "sns.set_theme() Changes Global rcParams",
    "It works by changing matplotlib's global defaults — so it affects every plot drawn after the call.",
    [
        prose(T_SST + ".r03.b01", "mechanism",
              "`sns.set_theme(style=..., palette=...)` changes the global defaults for all plots using "
              "the matplotlib rcParams system, so it affects matplotlib plots too, even ones not made "
              "with seaborn. Because it works by changing global defaults, calling `sns.set_theme()` "
              "changes how plots drawn after that call look — it does not go back and restyle a figure "
              "you already drew and displayed earlier.",
              [C_SNS_THEME], ["viz.seaborn_themes_palettes#tb2"],
              ["viz.seaborn_themes_palettes#f1"])
    ],
    tb_ids=["viz.seaborn_themes_palettes#tb2"],
    fact_ids=["viz.seaborn_themes_palettes#f1"]
)

tile_seaborn_stats_themes = {
    "tile_id": T_SST,
    "title": "Seaborn: DataFrame Plotting, Statistical Functions, and Themes",
    "summary": "Use seaborn's dataframe-aware plotting functions, add automatic statistical estimates with sns.regplot(), and apply themes and palettes with sns.set_theme().",
    "steps": [s01_sst, s02_sst, s03_sst, s04_sst, s05_sst, s06_sst,
              s07_sst, s08_sst, s09_sst, s10_sst, s11_recap_sst],
    "remediation_steps": [rem_sst_s02, rem_sst_s05, rem_sst_s09]
}


# ═══════════════════════════════════════════════════════════════════════════════
# TILE 5: tile_viz_custom_multi_panel
# ═══════════════════════════════════════════════════════════════════════════════

T_CMP = "tile_viz_custom_multi_panel"
C_STYLE = "viz.custom_styling_theming"
C_MULTI = "viz.multi_panel_figures"

# s01 explainer – custom styling (before_after visual)
style_before_code = code_walk(
    T_CMP + ".s01.b01.before",
    "import matplotlib.pyplot as plt\nfig, ax = plt.subplots()\nax.plot(days, lagos_avg)",
    [{"start_line": 3, "end_line": 3, "text": "Default matplotlib style — grey background, thin lines"}],
    [C_STYLE], ["viz.custom_styling_theming#tb1"], ["viz.custom_styling_theming#f1"]
)
style_after_code = code_walk(
    T_CMP + ".s01.b01.after",
    "import matplotlib.pyplot as plt\nimport matplotlib as mpl\nplt.style.use('ggplot')\nmpl.rcParams['lines.linewidth'] = 2\nfig, ax = plt.subplots()\nax.plot(days, lagos_avg)",
    [
        {"start_line": 3, "end_line": 3, "text": "plt.style.use('ggplot') applies the ggplot style sheet"},
        {"start_line": 4, "end_line": 4, "text": "mpl.rcParams['lines.linewidth'] = 2 sets the default line width globally"}
    ],
    [C_STYLE], ["viz.custom_styling_theming#tb1", "viz.custom_styling_theming#tb2"],
    ["viz.custom_styling_theming#f1", "viz.custom_styling_theming#f2"]
)

s01_cmp = step_explainer(
    T_CMP + ".s01", [C_STYLE], "custom styling",
    "Style Sheets, rcParams, and Seaborn Palettes",
    "Three tools let you control the visual appearance of every chart: style sheets, rcParams, and seaborn palettes.",
    [
        prose(T_CMP + ".s01.b02", "syntax",
              "`plt.style.use('style-name')` applies one of matplotlib's predefined style sheets — "
              "for example `'ggplot'` or `'dark_background'`. "
              "The available styles can be listed with `plt.style.available`.",
              [C_STYLE], ["viz.custom_styling_theming#tb1"], ["viz.custom_styling_theming#f1"]),
        prose(T_CMP + ".s01.b03", "mechanism",
              "A custom style file can set specific properties such as `'axes.titlesize'`, "
              "`'lines.linewidth'`, or tick label sizes, and rcParams can be set directly to change "
              "defaults globally. After `import matplotlib as mpl`, "
              "`mpl.rcParams['lines.linewidth'] = 2` sets the default line width for every plot "
              "drawn after that call.",
              [C_STYLE], ["viz.custom_styling_theming#tb2"], ["viz.custom_styling_theming#f2"]),
        prose(T_CMP + ".s01.b04", "syntax",
              "`seaborn.set_palette(palette, ...)` sets the matplotlib color cycle from a seaborn palette, "
              "applying that color scheme to subsequent plots. "
              "`sns.set_palette('pastel')` switches later plots to seaborn's pastel color scheme.",
              [C_STYLE], ["viz.custom_styling_theming#tb3"], ["viz.custom_styling_theming#f3"]),
        before_after(
            T_CMP + ".s01.b05",
            style_before_code, style_after_code,
            "plt.style.use('ggplot') and mpl.rcParams['lines.linewidth'] = 2 change the chart's appearance globally.",
            [C_STYLE],
            ["viz.custom_styling_theming#tb1", "viz.custom_styling_theming#tb2",
             "viz.custom_styling_theming#tb3"],
            ["viz.custom_styling_theming#f1", "viz.custom_styling_theming#f2",
             "viz.custom_styling_theming#f3"],
            anchors=["viz.custom_styling_theming#visual"]
        )
    ],
    tb_ids=["viz.custom_styling_theming#tb1", "viz.custom_styling_theming#tb2",
            "viz.custom_styling_theming#tb3"],
    fact_ids=["viz.custom_styling_theming#f1", "viz.custom_styling_theming#f2",
              "viz.custom_styling_theming#f3"],
    anchors=["viz.custom_styling_theming#visual"]
)

# s02 check – f1 (style sheets)
s02_cmp = step_check(
    T_CMP + ".s02", [C_STYLE], "quick check",
    "Applying a Style Sheet",
    "Which call applies a predefined matplotlib style sheet?",
    ["viz.custom_styling_theming#f1"],
    ["viz.custom_styling_theming#assessment:apply_matplotlib_style_sheet"]
)

# s03 check – f1 + f2 + f3 (all three methods)
s03_cmp = step_check(
    T_CMP + ".s03", [C_STYLE], "quick check",
    "Three Ways to Style a Chart",
    "Match each styling tool to what it controls.",
    ["viz.custom_styling_theming#f1", "viz.custom_styling_theming#f2",
     "viz.custom_styling_theming#f3"],
    ["viz.custom_styling_theming#assessment:select_appropriate_styling_method_for_branding_requirement"]
)

# s04 hands_on – custom styling
s04_cmp = step_hands_on(
    T_CMP + ".s04", [C_STYLE], "hands-on",
    "Apply rcParams and a Seaborn Palette",
    "Set a line width with mpl.rcParams and apply a seaborn palette with sns.set_palette().",
    ["viz.custom_styling_theming#f2", "viz.custom_styling_theming#f3"],
    ["viz.custom_styling_theming#practice",
     "viz.custom_styling_theming#assessment:set_rcparams_globally",
     "viz.custom_styling_theming#assessment:apply_seaborn_custom_palette"]
)

# s05 explainer – multi-panel figures (diagram visual)
s05_cmp = step_explainer(
    T_CMP + ".s05", [C_MULTI], "multi-panel figures",
    "Arranging Multiple Charts in One Figure",
    "plt.subplots(nrows, ncols) creates a grid of Axes — each panel is independent.",
    [
        prose(T_CMP + ".s05.b01", "intro",
              "Suppose you want to show the delivery-time histogram and the distance/delivery-time "
              "scatter plot together, side by side, instead of as two separate figures.",
              [C_MULTI], ["viz.multi_panel_figures#tb1"], []),
        prose(T_CMP + ".s05.b02", "syntax",
              "`fig, axs = plt.subplots(nrows, ncols)` creates a Figure containing a grid of Axes with "
              "the given number of rows and columns. "
              "`fig, axs = plt.subplots(2, 2)` creates one Figure holding four Axes arranged in two "
              "rows and two columns.",
              [C_MULTI], ["viz.multi_panel_figures#tb2"], ["viz.multi_panel_figures#f1"]),
        prose(T_CMP + ".s05.b03", "mechanism",
              "Each Axes in the returned grid is indexed separately (for example `axs[0, 0]`) and "
              "plotting/labeling calls made on one Axes only affect that panel. "
              "`axs[0, 0].hist(orders['delivery_time_minutes'])` draws the histogram into the top-left "
              "panel, and `axs[0, 1].scatter(orders['distance_km'], orders['delivery_time_minutes'])` "
              "draws the scatter into the top-right panel without disturbing the first.",
              [C_MULTI], ["viz.multi_panel_figures#tb3"], ["viz.multi_panel_figures#f2"]),
        diagram(
            T_CMP + ".s05.b04", "container",
            [
                {"id": "fig_node", "label": "Figure", "kind": "outer"},
                {"id": "ax00", "label": "axs[0,0]\nhistogram", "kind": "panel"},
                {"id": "ax01", "label": "axs[0,1]\nscatter", "kind": "panel"},
                {"id": "ax10", "label": "axs[1,0]\nbar chart", "kind": "panel"},
                {"id": "ax11", "label": "axs[1,1]\nbox plot", "kind": "panel"}
            ],
            "A 2×2 grid of panels inside one Figure. Each panel is labelled with its Axes index "
            "(axs[0,0] through axs[1,1]) and a chart type. Plotting on one panel does not affect the others.",
            title="plt.subplots(2, 2) — four independent Axes in one Figure",
            edges=[
                {"from": "fig_node", "to": "ax00", "label": "contains"},
                {"from": "fig_node", "to": "ax01", "label": "contains"},
                {"from": "fig_node", "to": "ax10", "label": "contains"},
                {"from": "fig_node", "to": "ax11", "label": "contains"}
            ],
            concept_ids=[C_MULTI],
            tb_ids=["viz.multi_panel_figures#tb2", "viz.multi_panel_figures#tb3"],
            fact_ids=["viz.multi_panel_figures#f1", "viz.multi_panel_figures#f2"],
            anchors=["viz.multi_panel_figures#visual"]
        )
    ],
    tb_ids=["viz.multi_panel_figures#tb1", "viz.multi_panel_figures#tb2",
            "viz.multi_panel_figures#tb3"],
    fact_ids=["viz.multi_panel_figures#f1", "viz.multi_panel_figures#f2"],
    anchors=["viz.multi_panel_figures#visual"]
)

# s06 video
s06_cmp = step_video(
    T_CMP + ".s06", [C_MULTI], "watch",
    "Multi-Panel Figures: Indexing and Independent Axes",
    ["seg_viz.multi_panel_figures_XFZRVnP-MTU_503_804"],
    ["viz.multi_panel_figures#f1", "viz.multi_panel_figures#f2"]
)

# s07 check – f2 (indexing axes)
s07_cmp = step_check(
    T_CMP + ".s07", [C_MULTI], "quick check",
    "Indexing into the Axes Grid",
    "How do you plot on the top-right panel of a 2×2 subplot grid?",
    ["viz.multi_panel_figures#f2"],
    ["viz.multi_panel_figures#assessment:index_and_plot_on_individual_axes_independently"]
)

# s08 hands_on – multi-panel
s08_cmp = step_hands_on(
    T_CMP + ".s08", [C_MULTI], "hands-on",
    "Build a Two-Panel Figure",
    "Use plt.subplots(1, 2) to create two side-by-side panels, then plot a histogram and a scatter plot.",
    ["viz.multi_panel_figures#f1"],
    ["viz.multi_panel_figures#practice",
     "viz.multi_panel_figures#assessment:create_subplot_grid_with_subplots"]
)

# s09 recap
s09_recap_cmp = step_recap(
    T_CMP + ".s09", [C_STYLE, C_MULTI],
    "Custom Styling and Multi-Panel Figures: What You Learned",
    "Style sheets and rcParams control appearance; plt.subplots(nrows, ncols) arranges multiple charts.",
    [
        prose(T_CMP + ".s09.b01", "takeaway",
              "Use `plt.style.use('style-name')` to apply a predefined style sheet, "
              "`mpl.rcParams['property'] = value` to set individual defaults globally, and "
              "`sns.set_palette('palette-name')` to change the color cycle. "
              "Use `fig, axs = plt.subplots(nrows, ncols)` to create a grid of independent panels "
              "and index each one with `axs[row, col]`.",
              [C_STYLE, C_MULTI], [], []),
        up_next(T_CMP + ".s09.b02",
                "Up next: A/B Tests and Statistical Significance",
                "Next you'll learn how to structure an A/B test, interpret lift, and decide whether "
                "an observed difference is statistically significant.")
    ],
    tb_ids=[], fact_ids=[]
)

# remediation steps
rem_cmp_s02 = step_remediation(
    T_CMP + ".r01", [C_STYLE],
    "plt.style.use() Applies a Style Sheet",
    "Pass a style name as a string — the style is applied to all plots drawn after the call.",
    [
        prose(T_CMP + ".r01.b01", "syntax",
              "`plt.style.use('style-name')` applies one of matplotlib's predefined style sheets — "
              "for example `'ggplot'` or `'dark_background'`. "
              "The available styles can be listed with `plt.style.available`.",
              [C_STYLE], ["viz.custom_styling_theming#tb1"], ["viz.custom_styling_theming#f1"])
    ],
    tb_ids=["viz.custom_styling_theming#tb1"], fact_ids=["viz.custom_styling_theming#f1"]
)

rem_cmp_s03 = step_remediation(
    T_CMP + ".r02", [C_STYLE],
    "Three Styling Tools and What They Control",
    "Style sheets set a bundle of defaults; rcParams set individual properties; set_palette sets colors.",
    [
        prose(T_CMP + ".r02.b01", "definition",
              "`plt.style.use('style-name')` applies a predefined bundle of style settings. "
              "`mpl.rcParams['lines.linewidth'] = 2` sets a single default property globally. "
              "`sns.set_palette('pastel')` sets the matplotlib color cycle from a seaborn palette, "
              "applying that color scheme to subsequent plots.",
              [C_STYLE],
              ["viz.custom_styling_theming#tb1", "viz.custom_styling_theming#tb2",
               "viz.custom_styling_theming#tb3"],
              ["viz.custom_styling_theming#f1", "viz.custom_styling_theming#f2",
               "viz.custom_styling_theming#f3"])
    ],
    tb_ids=["viz.custom_styling_theming#tb1", "viz.custom_styling_theming#tb2",
            "viz.custom_styling_theming#tb3"],
    fact_ids=["viz.custom_styling_theming#f1", "viz.custom_styling_theming#f2",
              "viz.custom_styling_theming#f3"]
)

rem_cmp_s07 = step_remediation(
    T_CMP + ".r03", [C_MULTI],
    "Each Panel Has Its Own Index",
    "axs[row, col] selects one panel — calls on that Axes only affect that panel.",
    [
        prose(T_CMP + ".r03.b01", "mechanism",
              "Each Axes in the returned grid is indexed separately (for example `axs[0, 0]`) and "
              "plotting/labeling calls made on one Axes only affect that panel. "
              "`axs[0, 1].scatter(orders['distance_km'], orders['delivery_time_minutes'])` draws the "
              "scatter into the top-right panel without disturbing the histogram in `axs[0, 0]`.",
              [C_MULTI], ["viz.multi_panel_figures#tb3"], ["viz.multi_panel_figures#f2"])
    ],
    tb_ids=["viz.multi_panel_figures#tb3"], fact_ids=["viz.multi_panel_figures#f2"]
)

tile_custom_multi_panel = {
    "tile_id": T_CMP,
    "title": "Custom Styling and Multi-Panel Figures",
    "summary": "Apply matplotlib style sheets and rcParams for custom branding, use sns.set_palette() for color schemes, and arrange multiple charts with plt.subplots(nrows, ncols).",
    "steps": [s01_cmp, s02_cmp, s03_cmp, s04_cmp, s05_cmp, s06_cmp,
              s07_cmp, s08_cmp, s09_recap_cmp],
    "remediation_steps": [rem_cmp_s02, rem_cmp_s03, rem_cmp_s07]
}


# ═══════════════════════════════════════════════════════════════════════════════
# ASSEMBLE OUTPUT
# ═══════════════════════════════════════════════════════════════════════════════

output = {
    "schema_version": "0.1.0",
    "kind": "screens_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_012_da_viz",
    "tiles": [
        tile_bar_histograms,
        tile_line_scatter_box,
        tile_labeling_chart_selection,
        tile_seaborn_stats_themes,
        tile_custom_multi_panel
    ]
}

out_path = "batches/final_batch_012_da_viz/screens.part.c1.json"
with open(out_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"Written: {out_path}")
# Count steps
for tile in output["tiles"]:
    steps = tile["steps"]
    rem = tile.get("remediation_steps", [])
    print(f"  {tile['tile_id']}: {len(steps)} steps, {len(rem)} remediation steps")
