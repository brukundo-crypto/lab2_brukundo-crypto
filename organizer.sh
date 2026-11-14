#!/bin/bash
# organizer.sh - archives the current grades.csv and resets the workspace.
#
# 1. Makes sure an "archive" directory exists.
# 2. Moves grades.csv into it, stamped with the date and time.
# 3. Creates a fresh, empty grades.csv ready for the next batch.
# 4. Appends a record of what happened to organizer.log.

SOURCE_FILE="grades.csv"
ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"

# The file we are asked to archive has to be here before we start.
if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: '$SOURCE_FILE' was not found in $(pwd)."
    echo "Run this script from the folder that holds $SOURCE_FILE."
    exit 1
fi

# Guard against a plain file called "archive" blocking the directory.
if [ -e "$ARCHIVE_DIR" ] && [ ! -d "$ARCHIVE_DIR" ]; then
    echo "Error: '$ARCHIVE_DIR' already exists but is not a directory."
    exit 1
fi

# Create the archive directory only when it is missing.
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir "$ARCHIVE_DIR"
    echo "Created the '$ARCHIVE_DIR' directory."
else
    echo "The '$ARCHIVE_DIR' directory already exists."
fi

# One timestamp, captured once, so the filename and the log always agree.
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
ARCHIVED_NAME="grades_${TIMESTAMP}.csv"
ARCHIVED_PATH="${ARCHIVE_DIR}/${ARCHIVED_NAME}"

if ! mv "$SOURCE_FILE" "$ARCHIVED_PATH"; then
    echo "Error: could not move '$SOURCE_FILE' into '$ARCHIVE_DIR'."
    exit 1
fi
echo "Archived '$SOURCE_FILE' as '$ARCHIVED_PATH'."

# Reset the workspace so the next batch of grades has somewhere to go.
touch "$SOURCE_FILE"
echo "Created a fresh, empty '$SOURCE_FILE'."

# Append to the log so entries from every run build up over time.
echo "$(date +"%Y-%m-%d %H:%M:%S") | archived: $SOURCE_FILE | saved as: $ARCHIVED_PATH" >> "$LOG_FILE"
echo "Logged the operation in '$LOG_FILE'."
