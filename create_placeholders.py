from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder(filename, size=(300, 300), color=(200, 200, 200), text=None):
    # Create a new image with the given color
    image = Image.new('RGB', size, color)
    
    if text:
        # Add text to the image
        draw = ImageDraw.Draw(image)
        text_size = min(size) // 5  # Smaller text for better visibility
        try:
            font = ImageFont.truetype("arial.ttf", text_size)
        except:
            font = ImageFont.load_default()
            
        # Get text size
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Calculate text position
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        
        # Draw text
        draw.text((x, y), text, fill=(255, 255, 255), font=font)  # White text for better visibility
    
    # Save the image
    image.save(filename)

# Create avatar placeholder (smaller size for phone screen)
create_placeholder("avatar_placeholder.png", (160, 160), (50, 50, 50), "A")

# Create photo placeholders (smaller size for phone screen)
colors = [
    (70, 130, 180),  # Steel Blue
    (205, 92, 92),   # Indian Red
    (46, 139, 87),   # Sea Green
    (218, 112, 214), # Orchid
    (255, 140, 0),   # Dark Orange
    (75, 0, 130),    # Indigo
]

for i, color in enumerate(colors, 1):
    create_placeholder(f"photo{i}.png", (280, 280), color, f"{i}")

print("Placeholder images created successfully!") 