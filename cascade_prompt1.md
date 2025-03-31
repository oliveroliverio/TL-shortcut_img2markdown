I'd to create a  script that will send an image from the system clipboard to the OpenAI API and return the response in markdown format.  Here's the code from the openAI docs for image input with the prompt already included ("output the contents of the image in markdown format").  This script will be bound to a keyboard shortcut in Apple Shortcuts.  The idea is, I screenshot and image, and then send the image to OpenAI to convert the contents to markdown.  The contents will then be in my system clipboard for pasting elsewhere.

```python
import base64
from openai import OpenAI

client = OpenAI()

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Path to your image
image_path = "path_to_your_image.jpg"

# Getting the Base64 string
base64_image = encode_image(image_path)


response = client.responses.create(
    model="gpt-4o",
    input=[
        {
            "role": "user",
            "content": [
                { "type": "input_text", "text": "what's in this image?" },
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                },
            ],
        }
    ],
)

print(response.output_text)
```

The only changes needed are to replace the image_path with the image from the clipboard.  I have a .env file with my OpenAI API key.

Here's a shell script that have clipboard functionality but used the Deepseek api and no image input, just text.  Might be helpful.

```bash
#!/bin/bash
# Usage: sh deepseek-chat.sh <markdown-file.md>
# Example: sh deepseek-chat.sh interstellar-summary.md

# Source environment variables from .env
. .env

# Retrieve API key, model, and endpoint from environment variables.
API_KEY=$DEEPSEEK_API_KEY
MODEL=$DEEPSEEK_MODEL
API_URL=$DEEPSEEK_API_URL

# Ensure a markdown file is provided as the argument.
if [ -z "$1" ]; then
  echo "Usage: sh deepseek-chat.sh <markdown-file.md>"
  exit 1
fi

# Check if the file exists.
if [ ! -f "$1" ]; then
  echo "Error: File '$1' not found."
  exit 1
fi

# Load and escape the prompt from the external markdown file.
ESCAPED_PROMPT=$(jq -Rs . "$1")

# Build the JSON payload using a heredoc.
# Note: Since ESCAPED_PROMPT is already a quoted JSON string,
# we do not wrap it in additional quotes.
JSON_PAYLOAD=$(cat <<EOF
{
  "model": "$MODEL",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": $ESCAPED_PROMPT}
  ],
  "stream": false
}
EOF
)

# Make the API request using curl.
RESPONSE=$(curl -s -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d "$JSON_PAYLOAD")

# Check if the API response is valid JSON.
if ! echo "$RESPONSE" | jq . >/dev/null 2>&1; then
  echo "Error: The API response is not valid JSON."
  echo "Raw response:"
  echo "$RESPONSE"
  # Copy the raw response to the clipboard for inspection.
  echo "$RESPONSE" | pbcopy
  echo "Raw API response has been copied to your clipboard."
  exit 1
fi

# Extract the markdown content from the API response.
MARKDOWN=$(echo "$RESPONSE" | jq -r '.choices[0].message.content')

# Check if markdown content was found.
if [ -z "$MARKDOWN" ] || [ "$MARKDOWN" = "null" ]; then
  echo "Error: No markdown content found in the API response."
  echo "Full API response:"
  echo "$RESPONSE"
  exit 1
fi

# remove everything before the first header line (# <header>)
MARKDOWN=$(echo "$MARKDOWN" | sed -n '/^# /,$p')

# find this string: ""},"logprobs":null,"finish_reason":"stop"}],"usage":" and remove everything after it
MARKDOWN=$(echo "$MARKDOWN" | sed -e 's/.*"logprobs":null,"finish_reason":"stop"}],"usage":"//')

# Output the markdown to the console.
echo "### Markdown Response:"
echo "----------------------"
echo "$MARKDOWN"

# Copy the markdown to the clipboard.
echo "$MARKDOWN" | pbcopy

echo "Markdown response has been copied to your clipboard."
```