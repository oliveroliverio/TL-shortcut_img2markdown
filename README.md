# Image to Markdown Converter

A simple utility that converts clipboard images to markdown text using OpenAI's Vision API.

## Features

- Takes an image from your system clipboard
- Sends it to OpenAI's GPT-4 Vision API
- Converts the image content to markdown format
- Copies the markdown back to your clipboard for easy pasting
- Supports multiple OpenAI models with automatic fallback
- Saves your preferences for future use

## Requirements

- Python 3.8+
- OpenAI API key (stored in `.env` file)
- Required packages: openai, pyperclip, python-dotenv
- macOS with pngpaste utility (install with `brew install pngpaste`)

## Setup

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

## Usage

### Basic Usage

1. Copy an image to your clipboard (e.g., take a screenshot)
2. Run the script:
   ```bash
   ./img2markdown.py
   ```
3. The markdown content will be copied to your clipboard, ready to paste

### Advanced Options

The script supports several command-line options:

```bash
# Use a specific model
./img2markdown.py --model gpt-4-turbo

# Disable fallback to other models
./img2markdown.py --model gpt-4o --no-fallback

# Use a custom prompt
./img2markdown.py --prompt "Describe this image in detail and format as markdown"

# Save your current settings as default
./img2markdown.py --model gpt-4-turbo --save-config

# List available models
./img2markdown.py --list-models

# Set maximum token limit for response
./img2markdown.py --max-tokens 2048
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

1. Open the Shortcuts app on your Mac
2. Create a new shortcut
3. Add a "Run Shell Script" action
4. Enter the full path to the script with any desired options:
   ```bash
   /Users/your_username/path/to/img2markdown.py --model gpt-4-turbo
   ```
5. Set "Shell" to `/bin/zsh`
6. Set "Input" to "None"
7. Assign a keyboard shortcut to this Shortcut

Now you can:
1. Take a screenshot or copy any image
2. Press your assigned keyboard shortcut
3. Wait a moment for the API call to complete
4. Paste the markdown anywhere you need it

## Troubleshooting

If you encounter errors:

1. **API Key Issues**: Make sure your OpenAI API key is valid and has sufficient quota
2. **Model Access**: Ensure your OpenAI account has access to the model you're trying to use
3. **No Image in Clipboard**: Verify you have an image copied to your clipboard
4. **pngpaste Not Found**: Install pngpaste with `brew install pngpaste`