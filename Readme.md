# Lab 2: ALU Transcript Generator

An individual coding lab for *Introduction to Python Programming and
Databases*, BSE Year 1 Trimester 2.

The project reads a CSV of course assignments, validates it, calculates the
final grade and GPA, decides whether the student passed, and reports which
formative assignment may be resubmitted. A companion Bash script archives
the grade file and resets the workspace for the next batch.

## Files

| File | Purpose |
|---|---|
| `grade-evaluator.py` | The Python application: validation, GPA, pass/fail, resubmission |
| `organizer.sh` | Bash script that archives `grades.csv` and logs the operation |
| `grades.csv` | The course data the program reads |
| `Readme.md` | This file |

Running the scripts also produces `archive/` (holding timestamped copies of
past grade files) and `organizer.log`. Both are generated output rather than
source, so they are listed in `.gitignore`.

## How to run

### The Python application

~~~
python3 grade-evaluator.py
~~~

It asks for a filename. Type `grades.csv` and press Enter.

### The shell script

~~~
bash organizer.sh
~~~

Run it from the folder that holds `grades.csv`.

## How the grade is calculated

Each assignment contributes `score x weight / 100` points. Those points are
summed per category and then overall.

| Step | Rule |
|---|---|
| Score validation | Every score must be between 0 and 100 |
| Weight validation | Weights must total exactly 100, split 60 Formative and 40 Summative |
| Final grade | The sum of every assignment's contribution, out of 100 |
| GPA | `GPA = (Total Grade / 100) * 5.0` |
| Pass / Fail | The student must reach at least 50% in **both** categories |
| Resubmission | The failed formative assignment (score below 50) carrying the highest weight |

### Ties in the resubmission rule

The brief requires that when several failed formative assignments share the
same highest weight, **all** of them are reported. The supplied `grades.csv`
is exactly that case: *Group Exercise* (40) and *Functions and Debugging Lab*
(45) both fail and both carry a weight of 20, so both are listed.

`find_resubmissions()` therefore finds the highest weight first, then makes a
second pass collecting every assignment that matches it, rather than stopping
at the first one it finds.

### Why pass/fail is checked per category

A student can clear 50% overall while failing one category badly. Checking
each category separately is what the brief asks for, and the program names
the category that fell short when it reports FAILED.

## Validation and edge cases

The program never crashes on bad input. Every case below was tested.

| Situation | What happens |
|---|---|
| File does not exist | Clear message naming the file, exit code 1 |
| No filename entered | Clear message, exit code 1 |
| File is completely empty | Reported as empty, exit code 1 |
| Header row only, no data | Reported as holding no usable rows, exit code 1 |
| Wrong or missing column names | Names the missing columns and shows the expected header |
| Blank lines inside the file | Skipped silently, the rest is processed |
| A row with missing values | Reported with its line number and skipped |
| Score or weight is not a number | Reported with its line number and skipped |
| Group is neither Formative nor Summative | Reported with its line number and skipped |
| Score outside 0 to 100 | Reported; no GPA is produced from invalid data |
| Weights do not total 100, or the 60/40 split is wrong | Each problem reported separately |

Rows that cannot be used are counted, and the total is reported before the
transcript is printed. A single bad row does not abandon the whole file.

Weights are compared with a small tolerance rather than with exact equality,
because values read from a file arrive as floats and exact equality is
unreliable for them.

## What organizer.sh does

1. Checks that `grades.csv` is present, and stops with a clear message if not.
2. Creates the `archive` directory only if it does not already exist, and
   refuses to continue if something that is not a directory is in its way.
3. Captures one timestamp and moves `grades.csv` to
   `archive/grades_YYYYMMDD-HHMMSS.csv`.
4. Creates a fresh, empty `grades.csv` so the workspace is ready for the
   next batch of grades.
5. Appends the timestamp, the original filename and the archived filename to
   `organizer.log`, which accumulates one line per run.

The timestamp is captured once into a variable so that the archived filename
and the log entry can never disagree.

Note that the reset file is empty, as the brief specifies. If
`grade-evaluator.py` is then run against it, it reports that the file is
empty rather than crashing.

## Sample output

~~~
--- Processing Grades ---
Loaded 5 assignment record(s).
All scores are within 0-100 and the weighting is correct.

--- Assignment Breakdown ---
Assignment                            Group          Score   Weight   Earned
----------------------------------------------------------------------------
Quiz                                  Formative      85.00    20.00    17.00
Group Exercise                        Formative      40.00    20.00     8.00
Functions and Debugging Lab           Formative      45.00    20.00     9.00
Midterm Project - Simple Calculator   Summative      70.00    20.00    14.00
Final Project - Text-Based Game       Summative      60.00    20.00    12.00
----------------------------------------------------------------------------

Formative :  34.00 / 60.00  (56.67%)
Summative :  26.00 / 40.00  (65.00%)

Final Grade : 60.00 / 100
GPA         : 3.00 / 5.0

--- Final Decision ---
Status: PASSED

--- Resubmission ---
2 assignments are tied on the highest weight among the failed formatives, so all of them are eligible:
  - Group Exercise (score 40.00, weight 20.00)
  - Functions and Debugging Lab (score 45.00, weight 20.00)
~~~

## Requirements

- Python 3 (no external libraries; only `csv`, `sys` and `os` from the
  standard library)
- Bash
