from PIL import Image

def map_grayscale_to_shade(value):
    if value <= 51:
        return 0  # Darkest shade (e.g., 30+ commits)
    elif value <= 102:
        return 1
    elif value <= 153:
        return 2
    elif value <= 204:
        return 3
    else:
        return 4  # Lightest shade (no commits)

def generate_grid(image_path):
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    if img.size != (52, 7):
        raise ValueError("Image must be 52x7 pixels")
    grid = [[0 for _ in range(52)] for _ in range(7)]
    for y in range(7):
        for x in range(52):
            pixel_value = img.getpixel((x, y))
            grid[y][x] = map_grayscale_to_shade(pixel_value)
    return grid

# Usage
image_path = 'bob_ross_52x7.png'  # Replace with your PNG file path
grid = generate_grid(image_path)
for row in grid:
    print(row)