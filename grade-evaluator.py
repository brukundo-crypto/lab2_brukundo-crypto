#!/usr/bin/python3
"""ALU Transcript Generator.

Reads a CSV of course assignments, validates the scores and the weighting,
works out the final grade and GPA, decides PASSED or FAILED, and reports
which formative assignment may be resubmitted.
"""
import csv
import sys
import os


def load_csv_data():
    """Prompt for a filename and read every row into a list."""
    filename = input(
        "Enter the name of the CSV file to process (e.g., grades.csv): "
    ).strip()

    if not os.path.exists(filename):
        print("Error: The file '{}' was not found.".format(filename))
        sys.exit(1)

    assignments = []

    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            assignments.append({
                'assignment': row['assignment'],
                'group': row['group'],
                'score': float(row['score']),
                'weight': float(row['weight'])
            })

    return assignments


if __name__ == "__main__":
    course_data = load_csv_data()
    print("Loaded {} assignment record(s).".format(len(course_data)))
    for record in course_data:
        print(record)
