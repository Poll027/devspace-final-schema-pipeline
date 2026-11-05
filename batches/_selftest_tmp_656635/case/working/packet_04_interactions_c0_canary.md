# EVALUATOR PACKET — Measures of Center and Spread (tile_stats_center_spread)
Tile summary: Introduces the three measures of central tendency (mean, median, mode) and three measures of spread (range, variance, standard deviation) using a seven-order QuickRide delivery dataset. Emphasises when the median is more representative than the mean, and why standard deviation is more interpretable than variance.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = stats.descriptive_measures_of_center — Measures of central tendency (mean, median, mode)
B = stats.measures_of_spread — Measures of spread (range, variance, standard deviation)

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (stats.descriptive_measures_of_center)   objective: Compute the mean, median, and mode of a dataset and choose which one best represents its typical (central) value, especially when the data is skewed.
A.f1: The sample mean is computed as the sum of the observed values divided by the number of observations.   [sources: openintro_statistics_textbook#2.1.2]
A.f2: The median is the middle value when the data are ordered from smallest to largest; if there is an even number of observations, the median is the average of the two middle values.   [sources: openintro_statistics_textbook#2.1.5]
A.f3: The mode is the value that occurs most often in the data; there can be more than one mode.   [sources: nist_eda_handbook#1.3.5.1]
A.f4: The mean is more strongly affected by extreme observations (such as those in the tail of a skewed distribution) than the median, which is more robust to them; for this reason the median can better represent a typical value in a skewed dataset.   [sources: openintro_statistics_textbook#2.1.6]
note: The dataset (18, 20, 22, 22, 26, 28, 80 minutes) is reused across measures of center and spread for continuity -- keep the sum (216), mean (~30.9), median (22), and mode (22) consistent everywhere they reappear.
note: TOC conflict: the concept's own assessment/practice ask the learner to reason about a 'skewed dataset', but formal skew (stats.distribution_shape) isn't taught until later and isn't in this concept's allowed knowledge. The word 'skewed' above is used only in the informal sense the brief's own fact (f4) already uses it in, not as a defined term.
note: Practice anchor says 'one unusually large value' instead of the TOC's 'skewed dataset': formal skew (stats.distribution_shape) comes later and is not allowed knowledge here.
PRACTICE ANCHOR (formula): Given seven delivery times with one unusually large value, compute the mean, median and mode, then say which best represents a typical delivery time and why.  SUCCESS: The learner sums and divides for the mean, finds the middle value of the sorted list for the median, names the most frequent value as the mode, and picks the median because the large value pulls the mean up.
ASSESSMENT ANCHOR: compute_sample_mean facts=['f1']
ASSESSMENT ANCHOR: compute_median_and_mode facts=['f2', 'f3']
ASSESSMENT ANCHOR: choose_representative_center facts=['f1', 'f2', 'f4']

## SOURCE FACTS — B (stats.measures_of_spread)   objective: Compute the range, variance, and standard deviation of a dataset and interpret what each says about how spread out the data are.
B.f1: The range of a data set is the largest value minus the smallest value.   [sources: nist_eda_handbook#1.3.5.6]
B.f2: The variance is computed by taking each observation's deviation from the mean, squaring it, summing the squared deviations, and dividing by n - 1 (one less than the number of observations); it is roughly the average squared distance of the observations from the mean.   [sources: openintro_statistics_textbook#2.1.4, nist_eda_handbook#1.3.5.6]
B.f3: The standard deviation is the square root of the variance, and it describes the typical distance of an observation from the mean.   [sources: openintro_statistics_textbook#2.1.4]
B.f4: The standard deviation is expressed in the same units as the original data, while the variance is expressed in squared units; the range is based only on the two most extreme values and ignores how the rest of the data are spread.   [sources: nist_eda_handbook#1.3.5.6]
note: Reuses the same seven-value delivery-time dataset and mean (~30.9) from measures of center -- keep the variance (~481.1) and standard deviation (~21.9) consistent if this dataset resurfaces later.
note: Don't introduce a rule-of-thumb interpretation (e.g. 68-95-99.7) for standard deviation -- that's not in the source facts.
PRACTICE ANCHOR (formula): Given a small numeric column and its mean, compute the range, the variance (dividing by n - 1) and the standard deviation, then say what the standard deviation means in the column's own units.  SUCCESS: The learner reports max minus min, sums the squared deviations and divides by n - 1, takes the square root, and states the result as a typical distance from the mean in the original units.
ASSESSMENT ANCHOR: compute_range facts=['f1']
ASSESSMENT ANCHOR: compute_sample_variance facts=['f2']
ASSESSMENT ANCHOR: interpret_standard_deviation_in_units facts=['f3', 'f4']
ASSESSMENT ANCHOR: explain_range_limitation facts=['f4']

## DATA ASSETS USED
ds_seven_delivery_times: Seven-Order Delivery Batch (Teaching Example) — columns: order_id(identifier), delivery_time(numerical)
   ["ORD-001",18]
   ["ORD-002",20]
   ["ORD-003",22]
   ["ORD-004",22]
   ["ORD-005",26]
   ["ORD-006",28]
   ["ORD-007",80]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply transform; Boolean/conditional filtering; Comparing correlation strength across multiple variable pairs; Computing descriptive statistics with pandas (describe, mean, median, std); Concat stacking; Correlation between two variables; Correlation-vs-causation caveat in business interpretation; Creating DataFrames from dicts/lists/files; Distribution shape (skewness, symmetry, outliers); Grouping and aggregation (groupby); Handling missing data (isna, dropna, fillna); Identifying and reasoning about outliers; Inspecting data (head, info, describe, shape, dtypes); Map substitution; Measures of spread (range, variance, standard deviation); Merge join; Reading a frequency distribution/histogram in statistical terms; Reading data (read_csv, read_excel); Removing duplicate rows; Renaming columns and index labels; Selecting rows/columns with loc/iloc; Series and DataFrame data structures; Sorting values; String cleaning with the .str accessor; Type conversion and dtype management (astype); Working with datetime data (to_datetime, date components)

## LESSON, in learner order

### s01 · explainer · What's a typical delivery time?  [reward 2]
Measures of Center — Seven QuickRide orders came in at 18, 20, 22, 22, 26, 28, and 80 minutes. Before you can say anything useful, you need one number that answers "what's typical here?" — and there are three ways to find it.
[TABLE ds_seven_delivery_times cols=['order_id', 'delivery_time'] highlights=[["row",null,"outlier pulls mean up"],["row",null,"median (4th of 7)"],["row",null,"mode (22 appears twice)"]]] caption: Seven delivery times sorted smallest to largest. Mean ≈ 30.9 min (pulled up by ORD-007), median = 22 min (middle value), mode = 22 min (appears twice).
(definition) The **sample mean** is the sum of all values divided by the count. For these seven orders: 18 + 20 + 22 + 22 + 26 + 28 + 80 = 216, and 216 ÷ 7 ≈ **30.9 minutes**. ⟦A.f1 A:tb2⟧
(definition) The **median** is the middle value of the sorted list. With seven orders, the fourth value is the middle one — that's **22 minutes**. If there were an even number of orders, you'd average the two middle values. ⟦A.f2 A:tb3⟧

### s02 · explainer · Mode and when the mean misleads  [reward 2]
Measures of Center — The mean and median both describe center, but they react very differently when one value is far from the rest.
(definition) The **mode** is the value that appears most often. In this batch, 22 minutes appears twice while every other time appears once — so **22 minutes** is the mode. A dataset can have more than one mode. ⟦A.f3 A:tb4⟧
(misconception) Notice the gap: mean ≈ 30.9 min, but median = mode = 22 min. The mean is more strongly affected by extreme observations than the median, which is more robust to them. That single 80-minute delivery pulls the mean almost 9 minutes above where six of the seven orders actually sit. When a dataset has one unusually large value, the median is usually the better "typical" number to report. ⟦A.f4 A:tb5⟧

### s03 · check · Choose the right center  [reward 3]
Quick Check — Pick the measure that best represents a typical delivery time for this batch.
QUESTION [choice, core, grading=client] Seven QuickRide delivery times are 18, 20, 22, 22, 26, 28, and 80 minutes. The mean is about 30.9 min and the median is 22 min. Which measure best represents a typical delivery time for this batch, and why?
  ✔ opt_median: The median (22 min), because the single 80-min delivery pulls the mean well above where six of the seven orders actually sit.
      why: Correct. The mean is more strongly affected by extreme observations than the median. The 80-min outlier pulls the mean to 30.9 — nearly 9 min above where six of the seven orders sit — so the median (22 min) is the more representative typical value.
  ✘ opt_mean: The mean (30.9 min), because it uses every value in the calculation and is therefore the most complete measure.
      why: The mean does use every value, but that is exactly why it is misleading here. The single 80-min delivery pulls the mean to 30.9 min, well above the six orders that completed in 18–28 min. Using every value is not always an advantage when one value is extreme.
  ✘ opt_mode: The mode (22 min), because it is the most common value and therefore the most representative.
      why: The mode names the most frequent value, but frequency alone does not make a value representative of the whole distribution. Here the mode and median happen to be the same (22 min), but the reason to prefer 22 min is that the median is robust to the extreme 80-min value — not that 22 appears twice.
  ✘ opt_none: None of the above — you need to know the range before choosing a center measure.
      why: The range measures spread, not center. Knowing the range does not help you choose between mean, median, and mode. The choice depends on whether extreme values are present — and here the 80-min outlier makes the median the better center measure.
  feedback✔: Exactly right. When one value is unusually large, the median is more robust than the mean and gives a better picture of what is typical.  feedback✘: Think about what happens to the mean when one value is much larger than the rest. Does 30.9 min feel like a typical delivery time when six of the seven orders finished in 18–28 min?  hints: ['Compare the mean (30.9 min) with the six orders that completed in 18–28 min. Does 30.9 feel like a typical delivery time for this batch?', 'The mean is computed by summing all values — including the 80-min outlier. The median is the middle value of the sorted list, so it is not pulled by extreme values.']  remediation→r01
  MEASURES: A:choose_representative_center(f1,f2,f4)   anchors=['assessment:choose_representative_center']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f4←s02

### s04 · hands_on · Compute mean, median, and mode  [reward 5]
Hands-On — Use the seven QuickRide delivery times to compute all three measures of center, then decide which one best represents a typical delivery.
QUESTION [code_exercise, core, grading=client] The file `delivery_times.csv` contains seven delivery times in the column `delivery_time`. Compute three measures of center and assign them to the named variables:
- `mean_val`: the sample mean (use `.mean()`)
- `median_val`: the median (use `.median()`)
- `mode_val`: the mode (use `.mode()[0]`)

The starter already loads the data and prints the three values; replace each `None` with the correct pandas expression.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['pandas']} constraints.allowed=['import pandas as pd', "df['col'].mean()", "df['col'].median()", "df['col'].mode()", 'list[i] and list[-1] indexing', 'int, float, str and bool literals'] blocked=0 items
  file solution.py [editable]:
import pandas as pd

df = pd.read_csv('delivery_times.csv')

# Compute the sample mean (sum / count)
mean_val = None  # replace None with your calculation

# Compute the median (middle value of the sorted list)
median_val = None  # replace None with your calculation

# Compute the mode (most frequent value)
mode_val = None  # replace None with your calculation

print(mean_val)
print(median_val)
print(mode_val)

  SOLUTION solution.py:
import pandas as pd

df = pd.read_csv('delivery_times.csv')

mean_val = df['delivery_time'].mean()
median_val = df['delivery_time'].median()
mode_val = df['delivery_time'].mode()[0]

print(mean_val)
print(median_val)
print(mode_val)

  test t_mean (value_equals, visible=True): {"expr":"mean_val","expected":30.857142857142858,"tolerance":1e-06} | on-fail: mean_val is not correct. The sample mean is the sum of all delivery times divided by the count. Use df['delivery_time'].mean().
  test t_median (value_equals, visible=True): {"expr":"median_val","expected":22.0,"tolerance":1e-09} | on-fail: median_val is not correct. The median is the middle value of the sorted list. Use df['delivery_time'].median().
  test t_output (stdout_equals, visible=True): {"expected":"30.857142857142858\n22.0\n22"} | on-fail: The printed output does not match. Check that mean_val, median_val, and mode_val are all computed correctly and printed in order.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"7b2d1293f290182f96cb1f469b3eb0663ecbc66f36dbac45f3c931a4f37cee14","tests_passed":3}
  feedback✔: Well done. Mean ≈ 30.9 min, median = 22 min, mode = 22 min. Notice that the mean sits well above the median — the 80-min outlier is pulling it up.  feedback✘: Check each variable. Use .mean() for the mean, .median() for the median, and .mode()[0] for the mode — all on df['delivery_time'].  hints: ["All three methods are called on df['delivery_time']: .mean(), .median(), and .mode()[0].", 'The mode() method returns a Series; add [0] to get the first (most frequent) value.']  remediation→r02
  MEASURES: A:compute_sample_mean(f1); A:compute_median_and_mode(f2,f3)   anchors=['practice', 'assessment:compute_sample_mean', 'assessment:compute_median_and_mode']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s02

### s05 · explainer · How spread out are the delivery times?  [reward 2]
Measures of Spread — Knowing the median is 22 minutes doesn't say whether all orders are close to that or wildly scattered. Spread measures fill that gap.
(intro) Most of the seven delivery times (18, 20, 22, 22, 26, 28, 80 minutes) cluster fairly close together — but one sits far away. The **range** is the simplest spread measure: largest minus smallest. Here that's 80 − 18 = **62 minutes**. ⟦B.f1 B:tb1 B:tb2⟧
(mechanism) The **variance** measures the average squared distance from the mean. With a mean of about 30.9 minutes, the seven squared deviations sum to about 2 886.9. Dividing by n − 1 = 6 gives a variance of about **481.1 minutes²**. ⟦B.f2 B:tb3⟧
[PROCESS_FLOW: From raw values to standard deviation] nodes=['Each value − mean — deviation (minutes)', 'Square each deviation — squared deviation (minutes²)', 'Sum the squared deviations — ≈ 2 886.9 minutes²', 'Divide by n − 1 — variance ≈ 481.1 minutes²', 'Take the square root — standard deviation ≈ 21.9 minutes'] edges=[('n1', 'n2', None), ('n2', 'n3', None), ('n3', 'n4', None), ('n4', 'n5', None)] alt: Five-step flowchart: subtract mean → square → sum → divide by n-1 (variance, minutes²) → square root (standard deviation, minutes).

### s06 · explainer · Standard deviation and the range's blind spot  [reward 2]
Measures of Spread — The variance is useful for calculation, but its units are squared. The standard deviation brings the number back to the original units — and the range has a hidden weakness.
(mechanism) The **standard deviation** is the square root of the variance: √481.1 ≈ **21.9 minutes** — roughly how far a typical delivery time sits from the 30.9-minute mean. It's in the same units as the data, making it easier to interpret than the variance (minutes²). ⟦B.f3 B:tb4⟧
(misconception) The **range** (62 minutes) uses only the two most extreme values and ignores how the rest of the data are spread. Variance and standard deviation use every observation's distance from the mean, so they capture whether the middle values are bunched or scattered. ⟦B.f4 B:tb5⟧

### s07 · video · Variance and standard deviation, worked by hand  [reward 1]
Watch — Watch the squared-deviation method in action, then see why dividing by n − 1 gives a better estimate for a sample.
[VIDEO Variance and standard deviation, worked by hand] bridge-before: Watch squaring make the units squared and the square root bring them back. The clip first divides by n for a full population, then by n - 1 for a sample; Devspace's variance is the n - 1 version. | bridge-after: The clip never covers the range. Devspace adds it: the range uses only the two extreme values, so it can't say whether the rest of the data is bunched or scattered.
  - SzZ6GpcfoQY 236-612s facts=['f2', 'f3', 'f4'] label: Variance and standard deviation worked from squared deviations, for a whole population and then for a sample | summary: Works through variance and standard deviation on a small set of measurements. For a full population, each value's difference from the mean is squared, the squares are added, and the total is divided by the number of values, giving 100. Squaring makes the units squared, so the square root is taken to get a standard deviation of 10 in the original units, drawn as the mean plus and minus that distance. The clip then explains that real data is usually a sample, so the sample mean is used and the total is divided by one less than the number of values, because dividing by the full count would consistently underestimate the spread. That gives a variance of 101.8 and a standard deviation of 10.1. The range is never mentioned.

### s08 · check · Why the range can mislead  [reward 3]
Quick Check — Choose the statement that best explains the range's main limitation as a spread measure.
QUESTION [choice, core, grading=client] The seven delivery times are 18, 20, 22, 22, 26, 28, and 80 minutes. The range is 62 minutes. Which statement best explains the range's main limitation as a measure of spread?
  ✔ opt_extremes: The range uses only the two most extreme values and ignores how the remaining observations are distributed.
      why: Correct. The range is max minus min, so it depends entirely on the two most extreme values. If all six non-outlier deliveries were exactly 22 min, the range would still be 62 min — even though the data would be far less scattered.
  ✘ opt_units: The range is expressed in squared units, making it hard to interpret directly.
      why: Squared units are a limitation of variance, not the range. The range is expressed in the same units as the data (minutes here). The real problem is that it only looks at the two extremes and ignores everything in between.
  ✘ opt_mean: The range does not use the mean, so it cannot describe how far observations sit from the center.
      why: Variance and standard deviation are the measures that use each observation's distance from the mean — not the range. The range's limitation is different: it ignores all observations except the largest and smallest.
  ✘ opt_size: The range grows with sample size, so it is not comparable across datasets of different lengths.
      why: The range can grow with sample size, but that is not its main limitation. The core problem is that it is based only on the two most extreme values and tells you nothing about how the rest of the data are spread.
  feedback✔: Right. The range is max minus min — it only looks at the two extremes and ignores everything in between.  feedback✘: Think about what the range formula actually uses: max minus min. How many of the seven delivery times does that formula actually look at?  hints: ['The range formula is: largest value minus smallest value. How many of the seven delivery times does that formula actually use?', 'Imagine replacing the five middle values (20, 22, 22, 26, 28) with a single value of 22. Would the range change?']  remediation→r03
  MEASURES: B:explain_range_limitation(f4)   anchors=['assessment:explain_range_limitation']
  taught-before-tested: B.f4←s06

### s09 · hands_on · Compute range, variance, and standard deviation  [reward 5]
Hands-On — Using the same seven delivery times, compute the range, the sample variance (dividing by n − 1), and the standard deviation. Then state what the standard deviation means in minutes.
QUESTION [code_exercise, stretch, grading=client] The file `delivery_times.csv` contains seven delivery times in the column `delivery_time`. Compute three measures of spread and assign them to the named variables:
- `range_val`: the range (use `.max() - .min()`)
- `variance_val`: the sample variance (use `.var()`, which divides by n − 1 by default)
- `std_val`: the standard deviation (use `.std()`)

The starter already loads the data and prints the three values; replace each `None` with the correct pandas expression.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['pandas']} constraints.allowed=['import pandas as pd', "df['col'].max()", "df['col'].min()", "df['col'].var()", "df['col'].std()", 'arithmetic operators (-, /, *)'] blocked=0 items
  file solution.py [editable]:
import pandas as pd

df = pd.read_csv('delivery_times.csv')

# Compute the range (largest minus smallest)
range_val = None  # replace None with your calculation

# Compute the sample variance (divides by n - 1 by default)
variance_val = None  # replace None with your calculation

# Compute the standard deviation (square root of variance)
std_val = None  # replace None with your calculation

print(range_val)
print(variance_val)
print(std_val)

  SOLUTION solution.py:
import pandas as pd

df = pd.read_csv('delivery_times.csv')

range_val = df['delivery_time'].max() - df['delivery_time'].min()
variance_val = df['delivery_time'].var()
std_val = df['delivery_time'].std()

print(range_val)
print(variance_val)
print(std_val)

  test t_range (value_equals, visible=True): {"expr":"range_val","expected":62,"tolerance":1e-09} | on-fail: range_val is not correct. The range is the largest value minus the smallest. Use df['delivery_time'].max() - df['delivery_time'].min().
  test t_variance (value_equals, visible=True): {"expr":"variance_val","expected":481.1428571428571,"tolerance":0.0001} | on-fail: variance_val is not correct. Use df['delivery_time'].var() — pandas divides by n − 1 by default, giving the sample variance.
  test t_std (value_equals, visible=True): {"expr":"std_val","expected":21.93496882019341,"tolerance":0.0001} | on-fail: std_val is not correct. Use df['delivery_time'].std() — it returns the square root of the sample variance.
  test t_output (stdout_equals, visible=True): {"expected":"62\n481.1428571428571\n21.93496882019341"} | on-fail: The printed output does not match. Check that range_val, variance_val, and std_val are all computed correctly and printed in order.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"ab6046fe18e0e01d2ffc1a63cb1ae7d38a77ab289fb6a9173173078f76196a30","tests_passed":4}
  feedback✔: Well done. Range = 62 min, variance ≈ 481.1 min², std dev ≈ 21.9 min. The standard deviation tells you that a typical delivery time sits about 21.9 minutes from the mean — expressed in the original units, making it directly interpretable.  feedback✘: Check each variable. Use .max() - .min() for the range, .var() for the sample variance (n − 1), and .std() for the standard deviation — all on df['delivery_time'].  hints: ["All three methods are called on df['delivery_time']: .max() - .min() for range, .var() for variance, .std() for standard deviation.", 'pandas .var() and .std() use ddof=1 by default, which means they divide by n − 1 — that is the sample variance and sample standard deviation.']  remediation→r04
  MEASURES: B:compute_range(f1); B:compute_sample_variance(f2); B:interpret_standard_deviation_in_units(f3,f4); B:explain_range_limitation(f4)   anchors=['practice', 'assessment:compute_range', 'assessment:compute_sample_variance', 'assessment:interpret_standard_deviation_in_units', 'assessment:explain_range_limitation']
  taught-before-tested: B.f1←s05; B.f2←s05; B.f3←s06; B.f4←s06; B.f4←s06

### s10 · recap · Center and spread: what you've learned  [reward 2]
Recap — Three measures of center, three measures of spread — and a clear rule for which to use.
(takeaway) Mean, median, and mode all answer "what's typical," but the mean is pulled by extreme values while the median is not — so check for unusually large values before reporting a single center number. ⟦A.f1 A.f2 A.f3 A.f4 A:tb6⟧
(takeaway) Range, variance, and standard deviation all quantify spread. The range uses only the two extremes; variance and standard deviation use every observation's distance from the mean. Standard deviation is in the original units, making it the most directly interpretable. ⟦B.f1 B.f2 B.f3 B.f4 B:tb6⟧
[UP NEXT] Up next: Distribution Shape and Outliers: You've seen how a single extreme value pulls the mean away from the median. Next, you'll learn to describe the overall shape of a distribution — whether it's symmetric or lopsided — and develop a principled approach to identifying and reasoning about outliers.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Mean vs median: which one to trust — The check asked which measure best represents a typical delivery time. Here's the contrast that makes it clear.
(definition) The **mean** sums all values and divides by the count: 216 ÷ 7 ≈ 30.9 minutes. The **median** is the middle value of the sorted list: the fourth of seven sorted values is 22 minutes. ⟦A.f1 A.f2 A:tb2 A:tb3⟧
(misconception) The mean is more strongly affected by extreme observations than the median. The single 80-minute delivery pulls the mean to 30.9 — nearly 9 minutes above where six of the seven orders actually sit. When one value is unusually large, the median (22 minutes here) is the more representative "typical" delivery time. ⟦A.f4 A:tb5⟧
### r02 · Computing mean, median, and mode step by step — The hands-on asked you to compute all three measures. Here's each calculation laid out clearly.
(definition) **Mean:** add all seven values (18 + 20 + 22 + 22 + 26 + 28 + 80 = 216) and divide by 7 → ≈ **30.9 minutes**. **Median:** sort the values; the fourth (middle) value is **22 minutes**. **Mode:** 22 minutes appears twice, every other value once → mode = **22 minutes**. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4⟧
### r03 · Why the range misses the full picture — The check asked about the range's main limitation. Here's the contrast that makes it concrete.
(misconception) The range (62 minutes) is based only on the two most extreme values — 80 and 18 — and ignores how the rest of the data are spread. Imagine all six non-outlier deliveries were exactly 22 minutes: the range would still be 62, even though the data is far less scattered. Variance and standard deviation use every observation's distance from the mean, so they capture that difference. ⟦B.f4 B:tb5⟧
### r04 · Range, variance, and standard deviation step by step — The hands-on asked you to compute all three spread measures. Here's each calculation laid out clearly.
(definition) **Range:** 80 − 18 = **62 minutes** (largest minus smallest). **Variance:** sum the squared deviations from the mean (≈ 30.9) and divide by n − 1 = 6 → ≈ **481.1 minutes²**. **Standard deviation:** √481.1 ≈ **21.9 minutes** — the typical distance of a delivery time from the mean, in the original units. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4⟧
(misconception) The range only looks at the two extremes; variance and standard deviation take every observation into account. Standard deviation is expressed in the same units as the data (minutes), while variance is in squared units (minutes²) — making standard deviation the easier one to interpret directly. ⟦B.f4 B:tb5 B:tb6⟧

## OTHER CONTENT (fields without a dedicated renderer)
· spec.expected: 30.857142857142858
22.0
22
· expected.value: 22.666666666666668
22.0
22
· spec.expected: 62
481.1428571428571
21.93496882019341
· expected.value: 60
538.8
23.212065827926647
· expected.value: 62
714.2857142857143
26.72612419124244
· expected.value: 10
13.866666666666665
3.723797345005051
· expected.value: 60.0
538.8
23.212065827926647