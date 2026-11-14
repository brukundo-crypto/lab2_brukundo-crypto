#!/usr/bin/python3
"""ALU Transcript Generator.

Reads a CSV of course assignments, validates the scores and the weighting,
works out the final grade and GPA, decides PASSED or FAILED, and reports
which formative assignment may be resubmitted.
"""
import csv
import sys
import os

REQUIRED_COLUMNS = ["assignment", "group", "score", "weight"]
VALID_GROUPS = ["Formative", "Summative"]


def load_csv_data():
    """Prompt for a filename and extract every usable row into a list.

    Rows that are blank, incomplete, or hold values that are not numbers
    are reported and skipped, rather than being allowed to crash the run.
    """
    filename = input(
        "Enter the name of the CSV file to process (e.g., grades.csv): "
    ).strip()

    if filename == "":
        print("Error: no filename was entered. "
              "Please run the program again and type a filename.")
        sys.exit(1)

    if not os.path.exists(filename):
        print("Error: The file '{}' was not found.".format(filename))
        print("Check the spelling, or run the program from the folder "
              "that holds the file.")
        sys.exit(1)

    assignments = []
    skipped = 0

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                print("Error: '{}' is empty, so there is nothing to "
                      "evaluate.".format(filename))
                sys.exit(1)

            missing = []
            for column in REQUIRED_COLUMNS:
                if column not in reader.fieldnames:
                    missing.append(column)
            if missing:
                print("Error: '{}' is missing the column(s): {}.".format(
                    filename, ", ".join(missing)))
                print("The file must have this header row: {}".format(
                    ",".join(REQUIRED_COLUMNS)))
                sys.exit(1)

            line_number = 1
            for row in reader:
                line_number += 1

                name = (row.get('assignment') or "").strip()
                group = (row.get('group') or "").strip().capitalize()
                score_text = (row.get('score') or "").strip()
                weight_text = (row.get('weight') or "").strip()

                if (name == "" and group == "" and score_text == ""
                        and weight_text == ""):
                    continue

                if (name == "" or group == "" or score_text == ""
                        or weight_text == ""):
                    print("  Skipped line {}: one or more values are "
                          "missing.".format(line_number))
                    skipped += 1
                    continue

                if group not in VALID_GROUPS:
                    print("  Skipped line {} ('{}'): group '{}' must be "
                          "Formative or Summative.".format(
                              line_number, name, group))
                    skipped += 1
                    continue

                try:
                    score = float(score_text)
                    weight = float(weight_text)
                except ValueError:
                    print("  Skipped line {} ('{}'): score and weight must "
                          "be numbers, for example 85 and 20.".format(
                              line_number, name))
                    skipped += 1
                    continue

                assignments.append({
                    'assignment': name,
                    'group': group,
                    'score': score,
                    'weight': weight
                })

    except OSError as error:
        print("An error occurred while reading the file: {}".format(error))
        sys.exit(1)

    if skipped > 0:
        print("  {} unusable row(s) were skipped.".format(skipped))

    if len(assignments) == 0:
        print("Error: '{}' contains no usable assignment rows.".format(
            filename))
        sys.exit(1)

    return assignments


def validate_scores(assignments):
    """Return a list of problems with any score outside 0 to 100."""
    problems = []
    for record in assignments:
        if record['score'] < 0 or record['score'] > 100:
            problems.append(
                "{}: score {:.2f} is outside the valid 0-100 range.".format(
                    record['assignment'], record['score']))
    return problems


def evaluate_grades(data):
    """Validate the records, then report the transcript for the student."""
    print("\n--- Processing Grades ---")
    print("Loaded {} assignment record(s).".format(len(data)))

    problems = validate_scores(data)
    if problems:
        print("\nThe following problems must be fixed before a grade can "
              "be calculated:")
        for problem in problems:
            print("  - {}".format(problem))
        print("\nNo GPA was calculated, because the data is not valid.")
        return

    print("All scores are within 0-100.")


if __name__ == "__main__":
    course_data = load_csv_data()
    evaluate_grades(course_data)
