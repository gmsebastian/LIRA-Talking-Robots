#!/bin/bash
#######################
# LIRA TALKING ROBOTS #
#######################

echo "             ⢀⣠⣄   ⢀⣀⡀"
echo "             ⢻⣿⣿⣶⣶⣶⣾⣿⣿⠇"
echo "          ⢄⣀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⢀⡀"
echo "           ⠈⠙⠻⠿⠋⠉⠉⠉⠛⢿⣿⣿⣿⣿⣿⡄"
echo "⢰⣶⡆  ⢰⣶⡆⢰⣶⣶⣶⣶⣄ ⢀⣶⣶⣆ ⠈⣿⣿⣿⣿⠉"
echo "⢸⣿⡇  ⢸⣿⡇⢸⣿⣇⣀⣿⠟ ⣼⣿⣹⣿⡄ ⠉⠛⠿⣿⡀"
echo "⢸⣿⣷⣶⣶⢸⣿⡇⢸⣿⡟⠻⣿⣧⣸⣿⠟⠛⢿⣿⡀    ⠈"
echo -e "\n\n"

# To stop the script if an error occurs 
set -e

# Directory variables
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$REPO_DIR/venv"

# Create a python virtual environment
echo "Creating new python3 virtual environment..."
python3 -m venv "$VENV_DIR"

# Install the dependencies
echo "Installing python3 dependencies"
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install faster_whisper
"$VENV_DIR/bin/pip" install piper-tts

# Define the marker to check for idempotency
echo "Adding venv packages to $BASHRC"
MARKER="### === LIRA Talking robots repo additions === ###"
BASHRC="$HOME/.bashrc"

# Add to .bashrc only if it doesn't already exist
if ! grep -q "$MARKER" "$BASHRC"; then
    echo -e "\n$MARKER" >> "$BASHRC"
    echo "export PYTHONPATH=\"$VENV_DIR/lib/python3.12/site-packages:\$PYTHONPATH\"" >> "$BASHRC"
    echo "source $REPO_DIR/ros2_ws/install/setup.bash" >> "$BASHRC"
    echo "### ========================================== ###" >> "$BASHRC"
    echo "Successfully added PYTHONPATH to $BASHRC"
else
    echo "PYTHONPATH entry already exists in $BASHRC. Skipping addition."
fi
