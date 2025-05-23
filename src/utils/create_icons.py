from PIL import Image, ImageDraw
import os

def create_icon(size, output_path):
    # Create a new image with a white background
    image = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw a clipboard shape
    # Main clipboard body
    draw.rectangle([size*0.2, size*0.1, size*0.8, size*0.9], 
                  fill='#2196F3', outline='#1976D2', width=2)
    
    # Clipboard clip
    draw.rectangle([size*0.35, size*0.05, size*0.65, size*0.15], 
                  fill='#1976D2', outline='#1565C0', width=2)
    
    # Lines on the clipboard
    line_spacing = size * 0.15
    for i in range(4):
        y = size * 0.25 + i * line_spacing
        draw.line([(size*0.3, y), (size*0.7, y)], 
                 fill='#FFFFFF', width=2)
    
    # Save the image
    image.save(output_path)

def main():
    # Create icons directory if it doesn't exist
    os.makedirs('assets', exist_ok=True)
    
    # Create icons for different platforms
    create_icon(256, 'assets/icon.png')  # For Linux
    create_icon(256, 'assets/icon.ico')  # For Windows
    create_icon(1024, 'assets/icon.icns')  # For macOS

if __name__ == '__main__':
    main() 