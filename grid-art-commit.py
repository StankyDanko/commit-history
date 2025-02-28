import datetime
import subprocess
import sys
import json

# Mapping of grid states to number of commits
commit_counts = {0: 0, 1: 1, 2: 10, 3: 20, 4: 30}

def calculate_start_date():
    """Calculate the start date (51 weeks ago from the current Sunday)."""
    today = datetime.date.today()
    days_since_sunday = (today.weekday() + 1) % 7
    current_sunday = today - datetime.timedelta(days=days_since_sunday)
    start_date = current_sunday - datetime.timedelta(days=51 * 7)
    return start_date

def validate_grid(grid):
    """Validate that the grid is 7x52 with integers 0-4."""
    if len(grid) != 7:
        return False
    for row in grid:
        if len(row) != 52:
            return False
        for value in row:
            if not isinstance(value, int) or value < 0 or value > 4:
                return False
    return True

def make_commits(grid, start_date):
    """Create commits based on the grid states."""
    for j in range(52):  # Columns (weeks)
        week_start = start_date + datetime.timedelta(days=j * 7)
        for i in range(7):  # Rows (days)
            day_date = week_start + datetime.timedelta(days=i)
            state = grid[i][j]
            num_commits = commit_counts[state]
            date_str = f"{day_date.isoformat()} 12:00:00"
            for _ in range(num_commits):
                subprocess.run([
                    "git", "commit", "--allow-empty",
                    "--date", date_str,
                    "-m", "Grid art commit"
                ])

def main():
    json_file = input("Enter the JSON grid file name: ")
    try:
        with open(json_file, 'r') as f:
            grid = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{json_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: File '{json_file}' is not a valid JSON file.")
        sys.exit(1)
    
    if not validate_grid(grid):
        print("Error: Invalid grid. Must be 7x52 with integers 0-4.")
        sys.exit(1)
    
    total_commits = sum(commit_counts[value] for row in grid for value in row)
    print(f"Will create {total_commits} commits based on the grid in '{json_file}'.")
    confirm = input("Proceed? (y/n): ")
    if confirm.lower() != "y":
        print("Aborted.")
        sys.exit(0)
    
    try:
        subprocess.check_call(["git", "rev-parse", "--is-inside-work-tree"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("Error: Run this script inside a Git repository.")
        sys.exit(1)
    
    start_date = calculate_start_date()
    make_commits(grid, start_date)
    print("Commits created successfully!")
    print("Run 'git push' to upload them to GitHub.")

if __name__ == "__main__":
    main()