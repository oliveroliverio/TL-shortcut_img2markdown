#!/usr/bin/env python3
import base64
import os
import sys
import subprocess
import tempfile
import argparse
import json
import pyperclip
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Available models with vision capabilities
VISION_MODELS = [
    "gpt-4o",
    "gpt-4-turbo",
    "gpt-4-vision-preview",
    "gpt-4"
]

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


def try_models_in_sequence(base64_image, models, prompt, max_tokens=4096):
    """Try multiple models in sequence until one succeeds."""
    last_error = None
    
    for model in models:
        try:
            print(f"Trying model: {model}...")
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
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
                max_tokens=max_tokens
            )
            print(f"Success with model: {model}")
            return response.choices[0].message.content, model
        except Exception as e:
            last_error = e
            print(f"Failed with model {model}: {e}")
            continue
    
    # If we get here, all models failed
    raise Exception(f"All models failed. Last error: {last_error}")


def image_to_markdown(base64_image, model=None, fallback=True, prompt=None):
    """Send image to OpenAI API and get markdown response."""
    if prompt is None:
        prompt = "Output the contents of the image in markdown format."
    
    try:
        if model and not fallback:
            # Use only the specified model with no fallback
            print(f"Sending image to OpenAI API (model: {model})...")
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
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
            return response.choices[0].message.content, model
        else:
            # Use fallback sequence
            models_to_try = []
            if model:
                # Start with the specified model
                models_to_try.append(model)
                # Then add the rest of the models (excluding the specified one)
                models_to_try.extend([m for m in VISION_MODELS if m != model])
            else:
                # Use all models in the predefined order
                models_to_try = VISION_MODELS
            
            return try_models_in_sequence(base64_image, models_to_try, prompt)
    
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        print("\nPossible solutions:")
        print("1. Check your OpenAI API key in the .env file")
        print("2. Ensure your OpenAI account has sufficient credits")
        print("3. Try a different model with --model parameter")
        print("   Available models with vision: " + ", ".join(VISION_MODELS))
        print("4. Check your internet connection")
        sys.exit(1)


def save_config(config_path, config):
    """Save configuration to a file."""
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"Configuration saved to {config_path}")
    except Exception as e:
        print(f"Error saving configuration: {e}")


def load_config(config_path):
    """Load configuration from a file."""
    if not os.path.exists(config_path):
        return {}
    
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return {}


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert clipboard image to markdown using OpenAI API"
    )
    parser.add_argument(
        "--model",
        type=str,
        help=f"OpenAI model to use (available: {', '.join(VISION_MODELS)})"
    )
    parser.add_argument(
        "--no-fallback",
        action="store_true",
        help="Disable fallback to other models if the specified model fails"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        help="Custom prompt to use with the image (default: convert to markdown)"
    )
    parser.add_argument(
        "--save-config",
        action="store_true",
        help="Save the current settings as default configuration"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=4096,
        help="Maximum number of tokens in the response (default: 4096)"
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List available models with vision capabilities"
    )
    return parser.parse_args()


def main():
    """Main function to process clipboard image and convert to markdown."""
    args = parse_arguments()
    
    # Handle list-models flag
    if args.list_models:
        print("Available models with vision capabilities:")
        for model in VISION_MODELS:
            print(f"- {model}")
        sys.exit(0)
    
    # Load configuration
    config_dir = os.path.join(os.path.expanduser("~"), ".config", "img2markdown")
    os.makedirs(config_dir, exist_ok=True)
    config_path = os.path.join(config_dir, "config.json")
    config = load_config(config_path)
    
    # Use command line args or fall back to config values
    model = args.model or config.get("model")
    fallback = not args.no_fallback if args.no_fallback is not None else config.get("fallback", True)
    prompt = args.prompt or config.get("prompt", "Output the contents of the image in markdown format.")
    max_tokens = args.max_tokens or config.get("max_tokens", 4096)
    
    # Save configuration if requested
    if args.save_config:
        new_config = {
            "model": model,
            "fallback": fallback,
            "prompt": prompt,
            "max_tokens": max_tokens
        }
        save_config(config_path, new_config)
    
    # Get image from clipboard
    image_bytes = get_image_from_clipboard()
    print(f"Successfully captured image ({len(image_bytes)} bytes)")
    
    # Encode image
    print("Encoding image to base64...")
    base64_image = encode_image(image_bytes)
    
    # Send to OpenAI and get markdown
    markdown_text, used_model = image_to_markdown(
        base64_image, 
        model=model, 
        fallback=fallback, 
        prompt=prompt
    )
    
    # Copy markdown to clipboard
    print("Copying markdown to clipboard...")
    pyperclip.copy(markdown_text)
    
    print(f"Done! Used model: {used_model}")
    print("Markdown content is now in your clipboard.")
    
    # Also print the first few lines of the markdown
    preview_lines = markdown_text.split('\n')[:5]
    print("\nPreview of markdown content:")
    for line in preview_lines:
        print(line)
    if len(preview_lines) < len(markdown_text.split('\n')):
        print("...")


if __name__ == "__main__":
    main()
