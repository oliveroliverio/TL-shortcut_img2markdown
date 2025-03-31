#!/usr/bin/env python3
import base64
import os
import sys
import subprocess
import tempfile
import argparse
import pyperclip
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY not found in environment variables.")
    print("Please make sure you have a .env file with your OpenAI API key:")
    print("OPENAI_API_KEY=your_api_key_here")
    sys.exit(1)

client = OpenAI(api_key=api_key)


def get_image_from_clipboard():
    """Get image from clipboard and convert to bytes."""
    # Create a temporary file to save the clipboard image
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
        temp_path = temp_file.name
    
    # Use macOS's pngpaste utility to get clipboard contents
    print("Getting image from clipboard using pngpaste...")
    result = subprocess.run(
        ['pngpaste', temp_path],
        capture_output=True,
        text=True,
        check=False
    )
    
    if result.returncode != 0:
        print("Error capturing clipboard content.")
        print("Make sure you have pngpaste installed: brew install pngpaste")
        print("Also ensure you have an image copied to your clipboard.")
        os.unlink(temp_path)
        sys.exit(1)
    
    # Check if the file exists and has content
    if not os.path.exists(temp_path) or os.path.getsize(temp_path) == 0:
        print("No image found in clipboard.")
        print("Please copy an image to your clipboard and try again.")
        os.unlink(temp_path)
        sys.exit(1)
    
    # Read the image file
    try:
        with open(temp_path, 'rb') as img_file:
            img_data = img_file.read()
        
        # Clean up the temporary file
        os.unlink(temp_path)
        return img_data
    except IOError as e:
        print(f"Error reading image file: {e}")
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        sys.exit(1)


def encode_image(image_bytes):
    """Encode image bytes to base64."""
    return base64.b64encode(image_bytes).decode('utf-8')


def image_to_markdown(base64_image, model="gpt-4o"):
    """Send image to OpenAI API and get markdown response."""
    try:
        print(f"Sending image to OpenAI API (model: {model})...")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Output the contents of the image in markdown format."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=4096
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        print("\nPossible solutions:")
        print("1. Check your OpenAI API key in the .env file")
        print("2. Ensure your OpenAI account has sufficient credits")
        print(f"3. Verify your OpenAI account has access to the {model} model")
        print("4. Try a different model with --model parameter")
        print("   Available models with vision: gpt-4o, gpt-4-turbo")
        print("5. Check your internet connection")
        sys.exit(1)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert clipboard image to markdown using OpenAI API"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o",
        help="OpenAI model to use (default: gpt-4o)"
    )
    return parser.parse_args()


def main():
    """Main function to process clipboard image and convert to markdown."""
    args = parse_arguments()
    
    # Get image from clipboard
    image_bytes = get_image_from_clipboard()
    print(f"Successfully captured image ({len(image_bytes)} bytes)")
    
    # Encode image
    print("Encoding image to base64...")
    base64_image = encode_image(image_bytes)
    
    # Send to OpenAI and get markdown
    markdown_text = image_to_markdown(base64_image, model=args.model)
    
    # Copy markdown to clipboard
    print("Copying markdown to clipboard...")
    pyperclip.copy(markdown_text)
    
    print("Done! Markdown content is now in your clipboard.")
    # Also print the first few lines of the markdown
    preview_lines = markdown_text.split('\n')[:5]
    print("\nPreview of markdown content:")
    for line in preview_lines:
        print(line)
    if len(preview_lines) < len(markdown_text.split('\n')):
        print("...")


if __name__ == "__main__":
    main()
