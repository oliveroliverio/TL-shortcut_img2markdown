#!/bin/bash
# Setup script for installing the Img2Markdown launcher as a macOS launch agent

# Get the absolute path to the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create logs directory if it doesn't exist
mkdir -p ~/.img2markdown_logs

# Update the plist file with the correct paths
sed -i '' "s|REPLACE_WITH_FULL_PATH|$PROJECT_DIR|g" "$PROJECT_DIR/com.img2markdown.launcher.plist"

# Create the LaunchAgents directory if it doesn't exist
mkdir -p ~/Library/LaunchAgents

# Copy the plist file to the LaunchAgents directory
cp "$PROJECT_DIR/com.img2markdown.launcher.plist" ~/Library/LaunchAgents/

# Load the launch agent
launchctl load ~/Library/LaunchAgents/com.img2markdown.launcher.plist

echo "Img2Markdown launcher has been installed and will start automatically at login."
echo "The application is also starting now."

# Start the application immediately
python3 "$PROJECT_DIR/img2markdown_gui.py" &

echo "Setup complete!"
