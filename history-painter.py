import tkinter as tk
from tkinter import Canvas, Button, filedialog
import json

# Define state colors
state_colors = {
    0: (22, 27, 34), 1: (14, 68, 41), 2: (0, 109, 50), 3: (38, 166, 65), 4: (57, 211, 83)
}
colors = {state: '#%02x%02x%02x' % rgb for state, rgb in state_colors.items()}

# Initialize grid and rectangle IDs
grid = [[0 for _ in range(52)] for _ in range(7)]
rect_ids = [[None for _ in range(52)] for _ in range(7)]
cell_size = 30

# Create window and canvas
root = tk.Tk()
root.title("GitHub Grid Editor")
canvas = Canvas(root, width=52 * cell_size, height=7 * cell_size)
canvas.pack()

# Draw grid
for i in range(7):
    for j in range(52):
        x0, y0 = j * cell_size, i * cell_size
        x1, y1 = x0 + cell_size, y0 + cell_size
        rect_ids[i][j] = canvas.create_rectangle(x0, y0, x1, y1, fill=colors[0], outline="gray")

# Track last updated cell
last_cell = None

# Update cell state and color
def update_cell(row, col, increment=True):
    if increment:
        grid[row][col] = min(grid[row][col] + 1, 4)
    else:
        grid[row][col] = max(grid[row][col] - 1, 0)
    canvas.itemconfig(rect_ids[row][col], fill=colors[grid[row][col]])

# Event handlers
def on_left_click(event):
    global last_cell
    col, row = event.x // cell_size, event.y // cell_size
    if 0 <= row < 7 and 0 <= col < 52:
        update_cell(row, col, True)
        last_cell = (row, col)

def on_right_click(event):
    global last_cell
    col, row = event.x // cell_size, event.y // cell_size
    if 0 <= row < 7 and 0 <= col < 52:
        update_cell(row, col, False)
        last_cell = (row, col)

def on_left_drag(event):
    global last_cell
    col, row = event.x // cell_size, event.y // cell_size
    if 0 <= row < 7 and 0 <= col < 52:
        if (row, col) != last_cell:
            update_cell(row, col, True)
            last_cell = (row, col)

def on_right_drag(event):
    global last_cell
    col, row = event.x // cell_size, event.y // cell_size
    if 0 <= row < 7 and 0 <= col < 52:
        if (row, col) != last_cell:
            update_cell(row, col, False)
            last_cell = (row, col)

# Bind events
canvas.bind("<Button-1>", on_left_click)
canvas.bind("<B1-Motion>", on_left_drag)
canvas.bind("<Button-3>", on_right_click)
canvas.bind("<B3-Motion>", on_right_drag)

# Save function
def save_grid():
    filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if filename:
        with open(filename, "w") as f:
            json.dump(grid, f)
        print(f"Grid saved to {filename}")

save_button = Button(root, text="Save Grid", command=save_grid)
save_button.pack(pady=10)

root.mainloop()