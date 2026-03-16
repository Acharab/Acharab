import os
import re
import random
import sys

issue_title = os.environ.get("ISSUE_TITLE", "")
if not issue_title.startswith("ttt|"):
    print("Not a Tic-Tac-Toe move.")
    sys.exit(0)

try:
    move_str = issue_title.split("|")[1]
    user_move = -1 if "reset" in move_str.lower() else int(move_str)
except (IndexError, ValueError):
    sys.exit(0)

with open("README.md", "r", encoding="utf-8") as file:
    readme = file.read()

# ✅ FIX: These were both empty strings before — that's why the board kept prepending
start_marker = "<!-- TIC-TAC-TOE-START -->"
end_marker = "<!-- TIC-TAC-TOE-END -->"

start_idx = readme.find(start_marker)
end_idx = readme.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("CRITICAL: Markers missing. Aborting to protect README.")
    sys.exit(1)

# Extract current board state
board_html = readme[start_idx : end_idx + len(end_marker)]
squares = re.findall(r">(⬜|❌|⭕)</a>", board_html)

def check_winner(s):
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a, b, c in wins:
        if s[a] == s[b] == s[c] and s[a] != "⬜":
            return s[a]
    return None

# Reset if requested, board is corrupted, or no moves exist yet
if user_move == -1 or len(squares) != 9:
    squares = ["⬜"] * 9
else:
    # ✅ FIX: Check if game was already over before this move
    if check_winner(squares) or "⬜" not in squares:
        print("Game already over. Submit a reset issue.")
        sys.exit(0)

    # Apply user move
    if 0 <= user_move <= 8 and squares[user_move] == "⬜":
        squares[user_move] = "❌"
    else:
        print("Invalid move.")
        sys.exit(0)

    # Bot move (only if game not over after user move)
    if not check_winner(squares):
        available = [i for i, s in enumerate(squares) if s == "⬜"]
        if available:
            squares[random.choice(available)] = "⭕"

winner = check_winner(squares)
game_over = winner is not None or "⬜" not in squares

# Build new board HTML
new_board = '\n<div align="center">\n  <h2>\n'
for i in range(9):
    if squares[i] == "⬜" and not game_over:
        link = f'https://github.com/Acharab/Acharab/issues/new?title=ttt%7C{i}&body=Just+click+%27Submit+new+issue%27.'
    else:
        link = '#'
    new_board += f'    <a href="{link}">{squares[i]}</a>\n'
    if i in [2, 5]:
        new_board += '    <br>\n'
new_board += '  </h2>\n</div>\n'

if game_over:
    if winner:
        msg = f"**{winner} wins!**"
    else:
        msg = "**It's a draw!**"
    reset_url = "https://github.com/Acharab/Acharab/issues/new?title=ttt%7Creset&body=Submit+to+reset"
    new_board += f"<p align='center'>{msg} Click <a href='{reset_url}'>here</a> to play again.</p>\n"

# ✅ Stitch README back together using the markers as anchors
new_readme = (
    readme[:start_idx]
    + start_marker
    + new_board
    + end_marker
    + readme[end_idx + len(end_marker):]
)

with open("README.md", "w", encoding="utf-8") as file:
    file.write(new_readme)

print("Board updated successfully!")
