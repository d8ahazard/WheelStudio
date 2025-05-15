#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the script directory
cd "$SCRIPT_DIR"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed or not in the PATH."
    echo "Please install Python 3.6 or higher."
    exit 1
fi

# Run the Python script with all arguments passed to this shell script
python3 manage_submodules.py "$@"

if [ $? -ne 0 ]; then
    echo "An error occurred while running the script."
fi 