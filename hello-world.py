import datetime
import subprocess
import sys

# 5x7 font for uppercase letters (no space character needed)
font = {
    'A': ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    'B': ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    'C': ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    'D': ["11100", "10010", "10001", "10001", "10001", "10010", "11100"],
    'E': ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    'F': ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    'G': ["01110", "10001", "10000", "10011", "10001", "10001", "01110"],
    'H': ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    'I': ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    'J': ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    'K': ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    'L': ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    'M': ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    'N': ["10001", "10001", "11001", "10101", "10011", "10001", "10001"],
    'O': ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    'P': ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    'Q': ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    'R': ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    'S': ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    'T': ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    'U': ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    'V': ["10001", "10001", "10001", "10001", "01010", "01010", "00100"],
    'W': ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
    'X': ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    'Y': ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    'Z': ["11111", "00001", "00010", "00100", "01000", "10000", "11111"]
}

def get_word_bitmap(word):
    """Generate a 7xM bitmap for a single word."""
    bitmaps = [font[c] for c in word if c in font]
    if not bitmaps:
        return []
    letter_width = 5
    total_width = letter_width * len(bitmaps)
    bitmap = [["0"] * total_width for _ in range(7)]
    for k, char_bitmap in enumerate(bitmaps):
        start_col = k * letter_width
        for i in range(7):
            for j in range(letter_width):
                bitmap[i][start_col + j] = char_bitmap[i][j]
    return bitmap

def get_message_bitmap(message, word_space=1):
    """Generate a 7xM bitmap for the entire message with specified space between words."""
    words = message.split()
    word_bitmaps = [get_word_bitmap(word) for word in words]
    if not word_bitmaps:
        return []
    total_width = sum(len(wb[0]) for wb in word_bitmaps) + word_space * (len(word_bitmaps) - 1)
    bitmap = [["0"] * total_width for _ in range(7)]
    current_col = 0
    for wb in word_bitmaps:
        word_width = len(wb[0])
        for i in range(7):
            for j in range(word_width):
                bitmap[i][current_col + j] = wb[i][j]
        current_col += word_width + word_space
    return bitmap

def calculate_start_date():
    """Calculate the start date (51 weeks ago from the current Sunday)."""
    today = datetime.date.today()
    days_since_sunday = (today.weekday() + 1) % 7
    current_sunday = today - datetime.timedelta(days=days_since_sunday)
    start_date = current_sunday - datetime.timedelta(days=51 * 7)
    return start_date

def make_commits(bitmap, start_date):
    """Create commits for each '1' in the bitmap."""
    total_width = len(bitmap[0]) if bitmap else 0
    if total_width > 52:
        print(f"Error: Message too long ({total_width} > 52 columns). Truncate or shorten it.")
        sys.exit(1)
    commit_dates = []
    for j in range(total_width):
        week_start = start_date + datetime.timedelta(days=j * 7)
        for i in range(7):
            if bitmap[i][j] == "1":
                commit_date = week_start + datetime.timedelta(days=i)
                commit_dates.append(commit_date)
    for date in sorted(commit_dates):
        date_str = f"{date.isoformat()} 12:00:00"
        subprocess.run([
            "git", "commit", "--allow-empty",
            "--date", date_str,
            "-m", "Commit for message display"
        ])

def main():
    message = "HELLO WORLD".upper()
    bitmap = get_message_bitmap(message, word_space=1)
    if not bitmap:
        print("Error: Message contains unsupported characters.")
        print("Supported characters:", " ".join(sorted(font.keys())))
        sys.exit(1)
    try:
        subprocess.check_call(["git", "rev-parse", "--is-inside-work-tree"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("Error: Run this script inside a Git repository.")
        sys.exit(1)
    num_commits = sum(sum(1 for cell in row if cell == "1") for row in bitmap)
    print(f"Will create {num_commits} commits to display '{message}'.")
    confirm = input("Proceed? (y/n): ")
    if confirm.lower() != "y":
        print("Aborted.")
        sys.exit(0)
    start_date = calculate_start_date()
    make_commits(bitmap, start_date)
    print("Commits created successfully!")
    print("Run 'git push' to upload them to GitHub.")

if __name__ == "__main__":
    main()