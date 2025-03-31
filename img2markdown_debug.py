#!/usr/bin/env python3
"""
Image to Markdown Converter with Debug Information
"""
import os
import sys
import base64
import json
import argparse
import subprocess
import configparser
from pathlib import Path
import datetime

# Create debug log directory in user's home
debug_dir = os.path.join(os.path.expanduser("~"), ".img2markdown_debug")
os.makedirs(debug_dir, exist_ok=True)

# Set up logging to file
debug_log = os.path.join(debug_dir, "shortcut_debug.log")

def log_debug(message):
    """Write debug message to log file with timestamp"""
    timestamp = datetime.datetime.now().isoformat()
    with open(debug_log, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def log_environment():
    """Log detailed environment information"""
    env_info = {
        "timestamp": str(datetime.datetime.now()),
        "working_directory": os.getcwd(),
        "python_path": sys.executable,
        "python_version": sys.version,
        "environment_variables": {k: v for k, v in os.environ.items() if not k.startswith("SUDO_")},
        "script_path": os.path.abspath(__file__),
        "args": sys.argv,
        "platform": sys.platform,
        "executable_path": sys.executable,
    }
    
    # Check for .env file
    env_file = os.path.join(os.getcwd(), ".env")
    env_info["env_file_exists"] = os.path.exists(env_file)
    
    # Check for common dependencies
    try:
        env_info["has_openai"] = True
        import openai
        env_info["openai_version"] = openai.__version__
    except ImportError:
        env_info["has_openai"] = False
    
    try:
        env_info["has_pyperclip"] = True
        import pyperclip
    except ImportError:
        env_info["has_pyperclip"] = False
    
    try:
        env_info["has_dotenv"] = True
        import dotenv
    except ImportError:
        env_info["has_dotenv"] = False
    
    # Check if pngpaste is available
    try:
        result = subprocess.run(["which", "pngpaste"], 
                               capture_output=True, text=True, check=False)
        env_info["pngpaste_path"] = result.stdout.strip() if result.returncode == 0 else None
    except Exception as e:
        env_info["pngpaste_error"] = str(e)
    
    # Write debug info to a file
    debug_file = os.path.join(debug_dir, "environment.json")
    with open(debug_file, "w", encoding="utf-8") as f:
        json.dump(env_info, f, indent=2, default=str)
    
    log_debug(f"Environment information written to {debug_file}")

def main():
    """Main function with enhanced error handling for Shortcuts"""
    try:
        log_debug("Script started")
        log_environment()
        
        # Try to import required modules
        try:
            log_debug("Importing required modules")
            import pyperclip
            log_debug("Imported pyperclip")
            import openai
            log_debug("Imported openai")
            from dotenv import load_dotenv
            log_debug("Imported dotenv")
        except ImportError as e:
            log_debug(f"Import error: {str(e)}")
            print(f"Error importing required modules: {str(e)}")
            print("This may happen if the script is not running in the correct environment.")
            print("Try running with the full path to the executable.")
            return 1
        
        # Load environment variables
        log_debug("Loading environment variables")
        load_dotenv()
        
        # Check for OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            log_debug("No OpenAI API key found in environment")
            print("Error: OpenAI API key not found in environment variables.")
            print("Make sure you have a .env file with OPENAI_API_KEY in the same directory as the executable.")
            return 1
        
        log_debug("OpenAI API key found")
        
        # Set up OpenAI client
        client = openai.OpenAI(api_key=api_key)
        
        # Parse arguments
        parser = argparse.ArgumentParser(description="Convert image to markdown using OpenAI API")
        parser.add_argument("--file", help="Path to image file instead of using clipboard")
        parser.add_argument("--output", help="Path to save markdown output instead of copying to clipboard")
        parser.add_argument("--model", help="OpenAI model to use")
        parser.add_argument("--no-fallback", action="store_true", help="Disable model fallback")
        parser.add_argument("--prompt", help="Custom prompt to use with the API")
        parser.add_argument("--max-tokens", type=int, help="Maximum tokens for response")
        parser.add_argument("--save-config", action="store_true", help="Save current settings as default")
        parser.add_argument("--list-models", action="store_true", help="List available models and exit")
        
        args = parser.parse_args()
        log_debug(f"Arguments parsed: {args}")
        
        # List models if requested
        if args.list_models:
            log_debug("Listing models")
            print("Available models with vision capabilities:")
            for model in ["gpt-4o", "gpt-4-turbo", "gpt-4-vision-preview", "gpt-4"]:
                print(f"- {model}")
            return 0
        
        # Load config
        config_dir = os.path.expanduser("~/.config/img2markdown")
        config_file = os.path.join(config_dir, "config.json")
        config = {}
        
        if os.path.exists(config_file):
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                log_debug(f"Loaded config: {config}")
            except Exception as e:
                log_debug(f"Error loading config: {str(e)}")
        
        # Get image data
        if args.file:
            log_debug(f"Getting image from file: {args.file}")
            try:
                with open(args.file, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            except Exception as e:
                log_debug(f"Error reading image file: {str(e)}")
                print(f"Error reading image file: {str(e)}")
                return 1
        else:
            log_debug("Getting image from clipboard")
            try:
                # Create a temporary file to store the clipboard image
                temp_file = "/tmp/clipboard_image.png"
                
                # Use pngpaste to get the image from clipboard
                result = subprocess.run(["pngpaste", temp_file], 
                                       capture_output=True, text=True, check=False)
                
                if result.returncode != 0:
                    log_debug(f"pngpaste error: {result.stderr}")
                    print("Error: No image found in clipboard or pngpaste not available.")
                    print(f"pngpaste output: {result.stderr}")
                    return 1
                
                # Read the image file and encode it
                with open(temp_file, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                
                # Clean up the temporary file
                os.remove(temp_file)
                
            except Exception as e:
                log_debug(f"Error getting clipboard image: {str(e)}")
                print(f"Error getting image from clipboard: {str(e)}")
                return 1
        
        # Determine which model to use
        model = args.model or config.get("model") or "gpt-4o"
        log_debug(f"Using model: {model}")
        
        # Determine fallback setting
        fallback = not args.no_fallback and config.get("fallback", True)
        log_debug(f"Fallback enabled: {fallback}")
        
        # Determine prompt
        prompt = args.prompt or config.get("prompt") or "Convert this image to markdown format."
        log_debug(f"Using prompt: {prompt}")
        
        # Determine max tokens
        max_tokens = args.max_tokens or config.get("max_tokens") or 4096
        log_debug(f"Max tokens: {max_tokens}")
        
        # Save config if requested
        if args.save_config:
            log_debug("Saving config")
            os.makedirs(config_dir, exist_ok=True)
            
            config = {
                "model": model,
                "fallback": fallback,
                "prompt": prompt,
                "max_tokens": max_tokens
            }
            
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)
            
            print(f"Configuration saved to {config_file}")
        
        # Convert image to markdown
        log_debug("Converting image to markdown")
        try:
            # List of models to try in order of preference
            models = [model]
            if fallback and model != "gpt-4o":
                models.append("gpt-4o")
            if fallback and model != "gpt-4-turbo" and "gpt-4-turbo" not in models:
                models.append("gpt-4-turbo")
            if fallback and model != "gpt-4-vision-preview" and "gpt-4-vision-preview" not in models:
                models.append("gpt-4-vision-preview")
            if fallback and model != "gpt-4" and "gpt-4" not in models:
                models.append("gpt-4")
            
            log_debug(f"Model fallback sequence: {models}")
            
            # Try each model in sequence
            markdown_text = None
            last_error = None
            
            for m in models:
                log_debug(f"Trying model: {m}")
                try:
                    response = client.chat.completions.create(
                        model=m,
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": prompt},
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
                    
                    markdown_text = response.choices[0].message.content
                    log_debug(f"Successfully got response from model: {m}")
                    break
                    
                except Exception as e:
                    last_error = str(e)
                    log_debug(f"Error with model {m}: {last_error}")
                    continue
            
            if markdown_text is None:
                log_debug(f"All models failed. Last error: {last_error}")
                print(f"Error: Failed to convert image with all models. Last error: {last_error}")
                return 1
            
            # Output the markdown
            if args.output:
                log_debug(f"Saving markdown to file: {args.output}")
                try:
                    with open(args.output, "w", encoding="utf-8") as f:
                        f.write(markdown_text)
                    print(f"Markdown saved to {args.output}")
                except Exception as e:
                    log_debug(f"Error saving markdown to file: {str(e)}")
                    print(f"Error saving markdown to file: {str(e)}")
                    return 1
            else:
                log_debug("Copying markdown to clipboard")
                try:
                    pyperclip.copy(markdown_text)
                    print("Markdown copied to clipboard")
                except Exception as e:
                    log_debug(f"Error copying to clipboard: {str(e)}")
                    print(f"Error copying to clipboard: {str(e)}")
                    # Write to a fallback file in case clipboard fails
                    fallback_file = os.path.join(os.path.expanduser("~"), "img2markdown_output.md")
                    try:
                        with open(fallback_file, "w", encoding="utf-8") as f:
                            f.write(markdown_text)
                        print(f"Clipboard copy failed, but markdown saved to {fallback_file}")
                    except Exception as inner_e:
                        log_debug(f"Error saving to fallback file: {str(inner_e)}")
                        print(f"Error saving to fallback file: {str(inner_e)}")
                        return 1
            
            log_debug("Script completed successfully")
            return 0
            
        except Exception as e:
            log_debug(f"Unexpected error: {str(e)}")
            print(f"Unexpected error: {str(e)}")
            return 1
            
    except Exception as e:
        # Catch-all for any unexpected errors
        try:
            log_debug(f"Critical error: {str(e)}")
        except:
            pass
        print(f"Critical error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
