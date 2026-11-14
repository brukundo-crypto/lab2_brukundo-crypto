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


def load_csv_data():
    """Prompt for a filename and read every row into a list."""
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

            for row in reader:
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })

    except OSError as error:
        print("An error occurred while reading the file: {}".format(error))
        sys.exit(1)

    return assignments


if __name__ == "__main__":
    course_data = load_csv_data()
    print("Loaded {} assignment record(s).".format(len(course_data)))
    for record in course_data:
        print(record)
