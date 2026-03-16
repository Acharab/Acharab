import os
import re
import random
import sys

issue_title = os.environ.get("ISSUE_TITLE", "")
if not issue_title.startswith("ttt|"):
    print("Not a Tic-Tac-Toe move.")
    sys.exit(0)

# Check if it's a reset command or a move
try:
    move_str = issue_title.split("|")[1]
    user_move = -1 if "reset" in move_str.lower() else int(move_str)
except (IndexError, ValueError):
    sys.exit(0)

with open("README.md", "r", encoding="utf-8") as file:
    readme = file.read()

# Exact markers
start_marker = ""
end_marker = ""

start_idx = readme.find(start_marker)
end_idx = readme.find(end_marker)

# Failsafe: If markers are missing, do not touch the file!
if start_idx == -1 or end_idx == -1:
    print("CRITICAL: Markers missing. Aborting to protect README.")
    sys.exit(1)

# Extract the current board
board_html = readme[start_idx : end_idx + len(end_marker)]
squares = re.findall(r">(⬜|❌|⭕)</a>", board_html)

# Reset game if board is corrupted, already full, or user clicked reset
if len(squares) != 9 or ("❌" not in squares and "⭕" not in squares and user_move == -1) or user_move == -1:
    squares = ["⬜"] * 9
else:
    # Apply user move
    if 0 <= user_move <= 8 and squares[user_move] == "⬜":
        squares[user_move] = "❌"
    else:
        print("Invalid move.")
        sys.exit(0)
    
    # Apply bot move
    available = [i for i, s in enumerate(squares) if s == "⬜"]
    if available:
        squares[random.choice(available)] = "⭕"

# Build the new board HTML safely
new_board = '\n<div align="center">\n  <h2>\n'
for i in range(9):
    if squares[i] == "⬜":
        link = f'https://github.com/Acharab/Acharab/issues/new?title=ttt%7C{i}&body=Just+click+%27Submit+new+issue%27.'
    else:
        link = '#'
    new_board += f'    <a href="{link}">{squares[i]}</a>\n'
    if i in [2, 5]:
        new_board += '    <br>\n'
new_board += '  </h2>\n</div>\n'

# Add reset button if game is over
if "⬜" not in squares:
    new_board += "<p align='center'><b>Game Over! Click <a href='https://github.com/Acharab/Acharab/issues/new?title=ttt%7Creset&body=Submit+to+reset'>here</a> to reset.</b></p>\n"

# Safely stitch the README back together
new_readme = readme[:start_idx] + start_marker + new_board + end_marker + readme[end_idx + len(end_marker):]

with open("README.md", "w", encoding="utf-8") as file:
    file.write(new_readme)

print("Board updated successfully without touching the rest of the README!")
