# Image to Markdown Converter

A simple utility that converts clipboard images to markdown text using OpenAI's Vision API.

## Features

- Takes an image from your system clipboard
- Sends it to OpenAI's GPT-4 Vision API
- Converts the image content to markdown format
- Copies the markdown back to your clipboard for easy pasting

## Requirements

- Python 3.8+
- OpenAI API key (stored in `.env` file)
- Required packages: openai, pyperclip, pillow, python-dotenv

## Setup

1. Make sure you have an `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

2. Install dependencies:
   ```bash
   uv init && uv venv && source .venv/bin/activate && uv add openai pyperclip pillow python-dotenv
   ```

3. Make the script executable:
   ```bash
   chmod +x img2markdown.py
   ```

## Usage

### Command Line

1. Copy an image to your clipboard (e.g., take a screenshot)
2. Run the script:
   ```bash
   ./img2markdown.py
   ```
3. The markdown content will be copied to your clipboard, ready to paste

### Apple Shortcuts Integration

1. Open the Shortcuts app on your Mac
2. Create a new shortcut
3. Add a "Run Shell Script" action
4. Enter the full path to the script:
   ```bash
   /Users/your_username/path/to/img2markdown.py
   ```
5. Set "Shell" to `/bin/zsh`
6. Set "Input" to "None"
7. Assign a keyboard shortcut to this Shortcut

Now you can:
1. Take a screenshot or copy any image
2. Press your assigned keyboard shortcut
3. Wait a moment for the API call to complete
4. Paste the markdown anywhere you need it

## Notes

- The script uses the `gpt-4-vision-preview` model
- Maximum token output is set to 4096
- The script will exit with an error if no image is found in the clipboard