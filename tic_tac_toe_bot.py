import threading
import time
import tkinter as tk
from tkinter import messagebox
import pyautogui
import keyboard
from PIL import ImageGrab

# Tic Tac Toe pixel positions
CELL_POSITIONS = [
    (273, 411), (341, 408), (411, 409),
    (272, 480), (343, 481), (414, 479),
    (272, 549), (341, 549), (412, 551),
]

COLOR_X = (84, 84, 84)
COLOR_O = (242, 235, 211)
COLOR_EMPTY = (20, 189, 172)

ai_running = False

def get_pixel_color(x, y):
    image = ImageGrab.grab(bbox=(x, y, x + 1, y + 1))
    return image.getpixel((0, 0))

def read_board_state():
    board = []
    for x, y in CELL_POSITIONS:
        color = get_pixel_color(x, y)
        if color == COLOR_X:
            board.append('X')
        elif color == COLOR_O:
            board.append('O')
        else:
            board.append('?')
    return board

def is_game_over(board):
    return '?' not in board or get_winner(board) is not None

def get_winner(board):
    wins = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6],
    ]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] and board[a] != '?':
            return board[a]
    return None

def find_best_move(board, ai_letter='X', opp_letter='O'):
    for i in range(9):
        if board[i] == '?':
            temp = board[:]
            temp[i] = ai_letter
            if get_winner(temp) == ai_letter:
                return i
    for i in range(9):
        if board[i] == '?':
            temp = board[:]
            temp[i] = opp_letter
            if get_winner(temp) == opp_letter:
                return i
    if board[4] == '?':
        return 4
    for i in [0, 2, 6, 8]:
        if board[i] == '?':
            return i
    for i in range(9):
        if board[i] == '?':
            return i
    return None

def run_ai():
    global ai_running
    time.sleep(5)
    while ai_running:
        board = read_board_state()
        if is_game_over(board):
            time.sleep(1)
            continue
        move = find_best_move(board)
        if move is not None:
            x, y = CELL_POSITIONS[move]
            pyautogui.click(x, y)
        time.sleep(0.8)

def start_ai():
    global ai_running
    if ai_running:
        return
    ai_running = True
    threading.Thread(target=run_ai, daemon=True).start()

def stop_ai():
    global ai_running
    ai_running = False
    messagebox.showinfo("AI Stopped", "Tic Tac Toe AI has been stopped.")

# GUI Setup
root = tk.Tk()
root.resizable(False, False)  # Disable resizing
root.title("Tic Tac Toe AI")
root.geometry("360x200")

tk.Label(root, text="Instructions:\n1. Open Google 'Tic Tac Toe'\n2. Place it on left half of screen\n3. Works only on 1080p\n\nStart: Ctrl+Shift+S | Stop: Ctrl+Shift+Q", justify='left').pack(pady=5)

start_button = tk.Button(root, text="Start AI", command=start_ai, width=20, bg='green', fg='white')
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop AI", command=stop_ai, width=20, bg='red', fg='white')
stop_button.pack(pady=5)

# Register hotkeys
keyboard.add_hotkey('ctrl+shift+s', lambda: start_button.invoke())
keyboard.add_hotkey('ctrl+shift+q', lambda: stop_button.invoke())

root.mainloop()
