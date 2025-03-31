```markdown
# For terminal command

```sh
# Navigate to DevSetup/Tools
cd DevSetup/Tools

# Source and execute the script with Debug mode ON
source ./build/imagebuild.sh && generate.py -d -g get-picture
```

**Issue 1:**
- Error retrieving images from clipboard using Python script...
  Make sure you have ImgPaste installed.
  For accurate clipboard content extraction before initial run, ensure you have an image copied to your clipboard.

```sh
# List Clipboard Content
pbpaste | grep 'image'
```

**Issue 2:**
- The script is returning an error when encountering an issue with capturing the clipboard content. This could be because either:
  1. The imagecopy utility is not installed.
  2. There is no image in your clipboard.
  3. There might be an issue with how pbpaste is being called or ImageGrab library is installed.

```sh
# To install imagecopy
sudo apt-get install imagecopy
```

```sh
# Debug Clipboard Output
/usr/bin/xclip -selection clipboard
```

**Adjustment:**
- Modify the Python utility installed on your system. Let’s modify the script to detect errors in image or clipboard errors better. This is to generate a more accurate user-friendly way to handle this situation.

**Addition:**
- A feature to optionally use a file as input instead of relying solely on handling clipboard.

```sh
# Add the following functionality to the script
if [[ "$1" == "-f" ]]; then
  script=./imagebuilder.sh ./imgpaste.py -f ${2}
else
  script=./imagebuilder.sh ./imgpaste.py
fi
```

# For terminal command

```sh
# Navigate to DevSetup/Utilities
cd DevSetup/Utilities

# Execute with file input option
./generate.py --imgbuilder -f ./image.png
```

# Updates Version Results  

```sh
# Add new capabilities and commit the updated script
git add .
git commit -m "Enhanced capture capabilities."
```

# For terminal command
```sh
# Commit the changes with detailed commit message
cd ..
git add .
git commit -m "Added File Input functionality and updated documentation."
git push origin main
```

**Summary of Improvements:**
1. **File Input Support:** You can now use the `-file` option to process an image file directly instead of relying on the clipboard.
2. **Clipboard Support:** You can use the `imgpaste` output as a file instead of the clipboard, avoiding errors when the clipboard is empty.
3. **Improved Error Handling:** The script now gracefully handles image clipboard mistakes and provides clearer error messages.
4. **Better Encoding Support:** Added UTF-8 encoding for file operations to ensure proper character handling, check/improvements made.
5. **Updates:** New options, better documentation, and optimized patch notes.
```