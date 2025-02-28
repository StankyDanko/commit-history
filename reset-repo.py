import subprocess
import sys

def run_command(args):
    """Run a command with arguments and handle errors."""
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result.stdout

# Check if in a Git repository
try:
    run_command(["git", "rev-parse", "--is-inside-work-tree"])
except SystemExit:
    print("Not in a Git repository. Please run this script from the repository's root directory.")
    sys.exit(1)

# Confirm with user
confirm = input("This will reset the repository history, removing all previous commits. Proceed? (y/n): ")
if confirm.lower() != 'y':
    print("Aborted.")
    sys.exit(0)

# Create an orphan branch
run_command(["git", "checkout", "--orphan", "temp"])

# Add current files and commit (or start empty)
# Note: This keeps the current files if any, but allows an empty commit if there are no files.
run_command(["git", "add", "."])
run_command(["git", "commit", "--allow-empty", "-m", "Reset commit"])

# Alternative for an empty repository (if you want to remove all files):
# run_command(["git", "rm", "-rf", "."])
# run_command(["git", "commit", "--allow-empty", "-m", "Reset commit"])

# Delete the old main branch
run_command(["git", "branch", "-D", "main"])

# Rename the temp branch to main
run_command(["git", "branch", "-m", "main"])

# Force push to GitHub
run_command(["git", "push", "-f", "origin", "main"])

print("Repository history has been reset. The old commits are removed.")