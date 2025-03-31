# Image to Markdown Converter

A simple utility that converts clipboard images to markdown text using OpenAI's Vision API.

## Features

- Takes an image from your system clipboard or a file
- Sends it to OpenAI's GPT-4 Vision API
- Converts the image content to markdown format
- Copies the markdown back to your clipboard or saves to a file
- Supports multiple OpenAI models with automatic fallback
- Saves your preferences for future use
- Available as both a Python script and a standalone executable

## Requirements

### For Python Script
- Python 3.8+
- OpenAI API key (stored in `.env` file)
- Required packages: openai, pyperclip, python-dotenv
- macOS with pngpaste utility (install with `brew install pngpaste`)

### For Standalone Executable
- OpenAI API key (stored in `.env` file in the same directory as the executable)
- macOS with pngpaste utility (install with `brew install pngpaste`)

## Setup

### Python Script Setup

1. Make sure you have an `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

2. Install dependencies:
   ```bash
   uv init && uv venv && source .venv/bin/activate && uv add openai pyperclip python-dotenv
   ```

3. Install pngpaste utility:
   ```bash
   brew install pngpaste
   ```

4. Make the script executable:
   ```bash
   chmod +x img2markdown.py
   ```

### Standalone Executable Setup

1. The executable is already built and available in the `dist` directory
2. Make sure you have an `.env` file in the same directory as the executable with your OpenAI API key
3. Install pngpaste utility if you haven't already:
   ```bash
   brew install pngpaste
   ```

## Usage

### Basic Usage (Python Script)

1. Copy an image to your clipboard (e.g., take a screenshot)
2. Run the script:
   ```bash
   source .venv/bin/activate && ./img2markdown.py
   ```
3. The markdown content will be copied to your clipboard, ready to paste

### Basic Usage (Standalone Executable)

1. Copy an image to your clipboard (e.g., take a screenshot)
2. Run the executable:
   ```bash
   ./dist/img2markdown
   ```
3. The markdown content will be copied to your clipboard, ready to paste

### Advanced Options

The script and executable support the same command-line options:

```bash
# Use a specific model
./dist/img2markdown --model gpt-4-turbo

# Disable fallback to other models
./dist/img2markdown --model gpt-4o --no-fallback

# Use a custom prompt
./dist/img2markdown --prompt "Describe this image in detail and format as markdown"

# Save your current settings as default
./dist/img2markdown --model gpt-4-turbo --save-config

# List available models
./dist/img2markdown --list-models

# Set maximum token limit for response
./dist/img2markdown --max-tokens 2048

# Use an image file instead of clipboard
./dist/img2markdown --file path/to/image.png

# Save output to a file instead of clipboard
./dist/img2markdown --output path/to/output.md

# Combine options
./dist/img2markdown --file image.png --output result.md --model gpt-4-turbo
```

### Model Fallback

If the specified model fails (due to quota limits or other issues), the script will automatically try other models in this order:
1. Your specified model (if any)
2. gpt-4o
3. gpt-4-turbo
4. gpt-4-vision-preview
5. gpt-4

You can disable this behavior with the `--no-fallback` flag.

### Configuration

Your settings are saved in `~/.config/img2markdown/config.json` when you use the `--save-config` flag. These settings will be used as defaults for future runs.

### Apple Shortcuts Integration

#### Using the Wrapper Script (Recommended)

To fix the "exit code 1" error when running in Apple Shortcuts:

1. Open the Shortcuts app on your Mac
2. Create a new shortcut
3. Add a "Run Shell Script" action
4. Enter the full path to the wrapper script:
   ```bash
   /full/path/to/shortcut_wrapper.sh --model gpt-4-turbo
   ```
5. Set "Shell" to `/bin/zsh`
6. Set "Input" to "None"
7. Assign a keyboard shortcut to this Shortcut

The wrapper script ensures proper environment setup and provides detailed logs for troubleshooting in `~/.img2markdown_logs/shortcut_log.txt`.

#### Using the Standalone Executable Directly

If you prefer to use the executable directly (may encounter issues in Shortcuts):

1. Open the Shortcuts app on your Mac
2. Create a new shortcut
3. Add a "Run Shell Script" action
4. Enter the full path to the executable with any desired options:
   ```bash
   cd /full/path/to && ./dist/img2markdown --model gpt-4-turbo
   ```
5. Set "Shell" to `/bin/zsh`
6. Set "Input" to "None"
7. Assign a keyboard shortcut to this Shortcut

#### Using the Python Script

1. Open the Shortcuts app on your Mac
2. Create a new shortcut
3. Add a "Run Shell Script" action
4. Enter the full path to the script with virtual environment activation:
   ```bash
   cd /path/to/project && source .venv/bin/activate && ./img2markdown.py --model gpt-4-turbo
   ```
5. Set "Shell" to `/bin/zsh`
6. Set "Input" to "None"
7. Assign a keyboard shortcut to this Shortcut

Now you can:
1. Take a screenshot or copy any image
2. Press your assigned keyboard shortcut
3. Wait a moment for the API call to complete
4. Paste the markdown anywhere you need it

## Building the Executable

If you want to rebuild the executable:

1. Install PyInstaller:
   ```bash
   source .venv/bin/activate && uv pip install pyinstaller
   ```

2. Build the executable:
   ```bash
   source .venv/bin/activate && pyinstaller --onefile --name img2markdown img2markdown.py
   ```

3. The executable will be created in the `dist` directory

## Troubleshooting

If you encounter errors:

1. **API Key Issues**: Make sure your OpenAI API key is valid and has sufficient quota
2. **Model Access**: Ensure your OpenAI account has access to the model you're trying to use
3. **No Image in Clipboard**: Verify you have an image copied to your clipboard or use the `--file` option
4. **pngpaste Not Found**: Install pngpaste with `brew install pngpaste`
5. **Module Import Errors**: If using the Python script, make sure to activate the virtual environment with `source .venv/bin/activate`
6. **Executable Permissions**: If you can't run the executable, make sure it has execute permissions with `chmod +x dist/img2markdown`
7. **Exit Code 1 in Shortcuts**: If you get "exit code 1" when running in Apple Shortcuts, use the provided wrapper script instead of calling the executable directly. The wrapper script handles environment setup and provides detailed logs for troubleshooting.
8. **Check Debug Logs**: If using the wrapper script, check the logs at `~/.img2markdown_logs/shortcut_log.txt` for detailed error information.