"""
Setup script for building the macOS app bundle using py2app.
"""
from setuptools import setup

APP = ['img2markdown_gui.py']
DATA_FILES = [
    ('', ['dist/img2markdown']),
    ('', ['.env'])
]
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,  # Makes the app run without a dock icon (menubar only)
        'CFBundleName': 'Img2Markdown',
        'CFBundleDisplayName': 'Image to Markdown Converter',
        'CFBundleIdentifier': 'com.img2markdown.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': '© 2025',
    },
    'packages': ['PyQt5'],
    'iconfile': 'app_icon.icns',  # This will be created later
}

setup(
    name='Img2Markdown',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
