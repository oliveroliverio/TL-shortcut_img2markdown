#!/usr/bin/env python3
"""
Script to create a basic icon for the Img2Markdown application.
This creates a simple icon with text "I2M" on it.
"""
import os
from PIL import Image, ImageDraw, ImageFont

def create_icon():
    # Create images with sizes required by macOS
    icon_sizes = [
        (16, '16x16'),
        (32, '16x16@2x'),
        (32, '32x32'),
        (64, '32x32@2x'),
        (128, '128x128'),
        (256, '128x128@2x'),
        (256, '256x256'),
        (512, '256x256@2x'),
        (512, '512x512'),
        (1024, '512x512@2x')
    ]
    
    # Create iconset directory
    iconset_path = "Img2Markdown.iconset"
    if not os.path.exists(iconset_path):
        os.makedirs(iconset_path)
    
    for size, name in icon_sizes:
        # Create a new image with a transparent background
        img = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw a filled circle as background
        margin = int(size * 0.1)
        circle_size = size - 2 * margin
        circle_pos = margin
        draw.ellipse(
            [(circle_pos, circle_pos), (circle_pos + circle_size, circle_pos + circle_size)],
            fill=(52, 152, 219, 255)  # Blue color
        )
        
        # Add text
        try:
            # Try to use a system font
            font_size = int(size * 0.4)
            try:
                font = ImageFont.truetype("Arial", font_size)
            except Exception:
                try:
                    font = ImageFont.truetype("Helvetica", font_size)
                except Exception:
                    font = ImageFont.load_default()
        except Exception:
            # Fall back to default font
            font = ImageFont.load_default()
        
        text = "I2M"
        
        # Get text size - handle different PIL versions
        # In newer PIL versions, we need to use font.getbbox() instead of textsize or getsize
        try:
            bbox = font.getbbox(text)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except AttributeError:
            # Fall back for older PIL versions
            try:
                text_width, text_height = draw.textsize(text, font=font)
            except AttributeError:
                try:
                    text_width, text_height = font.getsize(text)
                except AttributeError:
                    # Last resort fallback - just estimate based on font size
                    text_width = len(text) * font_size * 0.6
                    text_height = font_size
        
        position = ((size - text_width) // 2, (size - text_height) // 2)
        
        # Draw the text
        draw.text(position, text, fill=(255, 255, 255, 255), font=font)
        
        # Save the image
        img_path = os.path.join(iconset_path, f"icon_{name}.png")
        img.save(img_path)
    
    # Use iconutil to convert the iconset to icns (macOS only)
    os.system("iconutil -c icns Img2Markdown.iconset")
    os.system("mv Img2Markdown.icns app_icon.icns")
    
    print("Icon created successfully: app_icon.icns")

if __name__ == "__main__":
    create_icon()
