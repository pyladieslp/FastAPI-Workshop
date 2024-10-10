import os
from PIL import Image

def convert_to_webp(source):
    """Convert image to WebP format."""
    destination = os.path.splitext(source)[0] + ".webp"
    
    image = Image.open(source)
    image.save(destination, format="webp")
    
    return destination

def main():
    folder_path = "images"
    
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            source_path = os.path.join(folder_path, filename)
            
            try:
                webp_path = convert_to_webp(source_path)
                print(f"Converted {filename} to WebP: {webp_path}")
            except Exception as e:
                print(f"Error converting {filename}: {str(e)}")

if __name__ == "__main__":
    main()