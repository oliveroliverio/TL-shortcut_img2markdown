#!/bin/zsh

# Wrapper script for img2markdown executable to debug Shortcuts issues
# This script will be called by Apple Shortcuts

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [ -z "$SCRIPT_DIR" ]; then
  # Fallback if BASH_SOURCE is not available
  SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
fi

# Create log directory
LOG_DIR="$HOME/.img2markdown_logs"
mkdir -p "$LOG_DIR"

# Log file
LOG_FILE="$LOG_DIR/shortcut_log.txt"

# Log function
log() {
  echo "$(date): $1" >> "$LOG_FILE"
}

# Start logging
log "=== Starting img2markdown wrapper ==="
log "Script directory: $SCRIPT_DIR"
log "Current directory: $(pwd)"
log "User: $(whoami)"

# Check if .env file exists in the script directory
if [ -f "$SCRIPT_DIR/.env" ]; then
  log ".env file found in script directory"
else
  log "WARNING: .env file not found in script directory"
fi

# Check if the executable exists
EXECUTABLE="$SCRIPT_DIR/dist/img2markdown_debug"
if [ -f "$EXECUTABLE" ]; then
  log "Executable found: $EXECUTABLE"
else
  log "ERROR: Executable not found at $EXECUTABLE"
  echo "Error: Executable not found. Please check the installation." >&2
  exit 1
fi

# Check if pngpaste is available
if command -v pngpaste &> /dev/null; then
  log "pngpaste is available: $(which pngpaste)"
else
  log "ERROR: pngpaste not found in PATH"
  echo "Error: pngpaste utility not found. Please install it with 'brew install pngpaste'." >&2
  exit 1
fi

# Log all arguments
log "Arguments: $@"

# Set working directory to script directory
cd "$SCRIPT_DIR"
log "Changed working directory to: $(pwd)"

# Run the executable with all arguments
log "Running executable with arguments: $@"
"$EXECUTABLE" "$@"
EXIT_CODE=$?

# Log the exit code
log "Executable exited with code: $EXIT_CODE"

# Return the same exit code
exit $EXIT_CODE
