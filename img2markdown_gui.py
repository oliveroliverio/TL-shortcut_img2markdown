#!/usr/bin/env python3
import sys
import os
import subprocess
import time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
)
from PyQt5.QtCore import Qt, QTimer

class Img2MarkdownGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.timer = QTimer()
        self.timer.timeout.connect(self.reset_status)
        
    def initUI(self):
        self.setWindowTitle('Image to Markdown Converter')
        self.setFixedSize(400, 200)
        
        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)
        
        # Create convert button
        self.convert_button = QPushButton('Convert Clipboard Image to Markdown', self)
        self.convert_button.setFixedSize(300, 50)
        self.convert_button.clicked.connect(self.convert_image)
        
        # Create status label
        self.status_label = QLabel('', self)
        self.status_label.setAlignment(Qt.AlignCenter)
        
        # Add widgets to layout
        layout.addWidget(self.convert_button)
        layout.addWidget(self.status_label)
        
        # Center the window on the screen
        self.center()
        
    def center(self):
        """Center the window on the screen"""
        screen_geometry = QApplication.desktop().screenGeometry()
        window_geometry = self.geometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(x, y)
        
    def convert_image(self):
        """Run the img2markdown executable and show status"""
        try:
            # Get the absolute path to the executable
            script_dir = os.path.dirname(os.path.abspath(__file__))
            executable_path = os.path.join(script_dir, 'dist', 'img2markdown')
            
            # Run the executable
            self.status_label.setText("Converting image...")
            process = subprocess.run(
                [executable_path],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Show success message
            self.status_label.setText("Markdown copied to clipboard!")
            self.status_label.setStyleSheet("color: green;")
            
            # Reset status after 5 seconds
            self.timer.start(5000)
            
        except subprocess.CalledProcessError as e:
            # Show error message
            self.status_label.setText(f"Error: {e.stderr}")
            self.status_label.setStyleSheet("color: red;")
            # Reset status after 5 seconds
            self.timer.start(5000)
            
    def reset_status(self):
        """Reset the status label after timer expires"""
        self.status_label.setText("")
        self.status_label.setStyleSheet("")
        self.timer.stop()

def main():
    app = QApplication(sys.argv)
    window = Img2MarkdownGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
