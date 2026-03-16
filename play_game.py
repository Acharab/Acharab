import os
import re
import random
import sys

# Get the issue title from GitHub Actions environment
issue_title = os.environ.get("ISSUE_TITLE")
if not issue_title or not issue_title.startswith("ttt|"):
    print("Not a Tic-Tac-Toe move.")
    sys.exit(0)

# Extract the user's move (0-8)
try:
    user_move = int(issue_title.split("|")[1])
except ValueError:
    sys.exit(0)

# Read the current README
with open("README.md", "r", encoding="utf-8") as file:
    readme = file.read()

# Find the board using our hidden markers
board_match = re.search(r"(.*?)", readme, re.DOTALL)
if not board_match:
    print("Could not find the board in README.md")
    sys.exit(1)

board_html = board_match.group(1)

# Extract the current state of the 9 squares (⬜, ❌, or ⭕)
squares = re.findall(r">(⬜|❌|⭕)</a>", board_html)

# If the game is already over or someone messed with the board, reset it
if len(squares) != 9 or "❌" not in squares and "⭕" not in squares and user_move == -1:
    squares = ["⬜"] * 9

# Check if the user's move is valid
if squares[user_move] == "⬜":
    squares[user_move] = "❌" # User is X
else:
    print("Invalid move. Square already taken.")
    sys.exit(0)

# Bot's Turn (Random AI)
available_moves = [i for i, square in enumerate(squares) if square == "⬜"]
if available_moves:
    bot_move = random.choice(available_moves)
    squares[bot_move] = "⭕" # Bot is O

# Rebuild the HTML board
new_board_html = '\n<div align="center">\n  <h2>\n'
for i in range(9):
    if squares[i] == "⬜":
        link = f'https://github.com/Acharab/Acharab/issues/new?title=ttt%7C{i}&body=Just+click+%27Submit+new+issue%27.'
    else:
        # If square is taken, link does nothing
        link = '#'
    
    new_board_html += f'    <a href="{link}">{squares[i]}</a>\n'
    if i in [2, 5]: # Line breaks for the grid
        new_board_html += '    <br>\n'

new_board_html += '  </h2>\n</div>\n'

# Check if the game is over (simple check to see if board is full, resets if true)
if "⬜" not in squares:
    new_board_html += "<p align='center'><b>Game Over! It's a draw! Click <a href='https://github.com/Acharab/Acharab/issues/new?title=ttt%7Creset&body=Submit+to+reset'>here</a> to reset.</b></p>\n"

# If user clicked reset
if "reset" in issue_title.lower():
    new_board_html = board_match.group(1).replace("❌", "⬜").replace("⭕", "⬜") # Reset all to white

# Replace the old board with the new board in the README text
new_readme = readme.replace(board_match.group(0), f"{new_board_html}")

# Write the updated README
with open("README.md", "w", encoding="utf-8") as file:
    file.write(new_readme)

print("Move processed successfully!")
