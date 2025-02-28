from PIL import Image, ImageDraw
import numpy as np

def generate_grid(image_path):
    # Open the image
    img = Image.open(image_path)
    
    # Resize to 52x7 using nearest-neighbor interpolation
    img = img.resize((52, 7), Image.NEAREST)
    
    # Convert to grayscale for consistent shading
    img = img.convert('L')
    
    # Get pixel values as a numpy array
    pixels = np.array(img)
    
    # Find unique pixel values and sort them
    unique_values = np.unique(pixels)
    unique_values.sort()
    
    # Print unique values for verification
    print("Unique pixel values after resizing:", unique_values)
    
    # Map pixel values to shades: darker (smaller values) to 0, lighter (larger values) to higher shades
    shade_mapping = {val: min(i, 4) for i, val in enumerate(unique_values)}
    
    # Warn if there are more than 5 unique values
    if len(unique_values) > 5:
        print("Warning: More than 5 unique values found. Consider re-posterizing the image.")
    
    # Create the 7x52 grid
    grid = [[0 for _ in range(52)] for _ in range(7)]
    for y in range(7):
        for x in range(52):
            pixel_value = pixels[y, x]
            grid[y][x] = shade_mapping[pixel_value]
    
    return grid

def generate_preview_image(grid, output_path='github_preview.png'):
    # Define cell size (each grid cell will be a 10x10 pixel square)
    cell_size = 10
    width = 52 * cell_size   # 520 pixels
    height = 7 * cell_size   # 70 pixels
    
    # Create a new RGB image
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Define the color mapping based on provided RGB values
    colors = {
        0: (22, 27, 34),    # No color
        1: (14, 68, 41),    # First shade
        2: (0, 109, 50),    # Second shade
        3: (38, 166, 65),   # Third shade
        4: (57, 211, 83)    # Fourth shade
    }
    
    # Draw each cell as a 10x10 square with the corresponding color
    for y in range(7):
        for x in range(52):
            shade = grid[y][x]
            color = colors[shade]
            left = x * cell_size
            top = y * cell_size
            right = left + cell_size
            bottom = top + cell_size
            draw.rectangle([left, top, right, bottom], fill=color)
    
    # Save the image
    img.save(output_path)
    print(f"Preview image saved to {output_path}")

# Main execution
if __name__ == "__main__":
    image_path = 'bob_ross_674x91.png'  # Replace with your actual image path
    grid = generate_grid(image_path)
    
    # Optional: Print the grid to terminal for reference
    for row in grid:
        print(row)
    
    # Generate the visual preview
    generate_preview_image(grid)