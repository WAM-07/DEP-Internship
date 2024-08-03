import sys
import random
import tkinter as tk
from tkinter import messagebox
from enum import Enum

class GameVersion(Enum):
    STANDARD = "standard"
    MISERE = "misere"

class Player(Enum):
    HUMAN = "human"
    COMPUTER = "computer"

class NimGame:
    def __init__(self, num_red, num_blue, version, first_player, depth):
        self.num_red = num_red
        self.num_blue = num_blue
        self.version = GameVersion(version)
        self.current_player = Player(first_player)
        self.depth = depth if depth else 3  # Default search depth

    def switch_player(self):
        self.current_player = Player.HUMAN if self.current_player == Player.COMPUTER else Player.COMPUTER

    def is_game_over(self):
        return self.num_red == 0 or self.num_blue == 0

    def calculate_score(self):
        return (self.num_red * 2) + (self.num_blue * 3)

    def human_move(self, red, blue):
        if red <= self.num_red and blue <= self.num_blue and (red > 0 or blue > 0):
            self.num_red -= red
            self.num_blue -= blue
            return True
        return False

    def computer_move(self):
        if self.num_red > 0:
            red = random.randint(0, min(2, self.num_red))
        else:
            red = 0
        if self.num_blue > 0:
            blue = random.randint(0, min(2, self.num_blue))
        else:
            blue = 0
        if red == 0 and blue == 0:
            red = 1 if self.num_red > 0 else 0
            blue = 1 if self.num_blue > 0 else 0
        self.num_red -= red
        self.num_blue -= blue
        return red, blue

def play_game(num_red, num_blue, version, first_player, depth):
    game = NimGame(num_red, num_blue, version, first_player, depth)

    def update_display():
        red_label.config(text=f"Red Marbles: {game.num_red}")
        blue_label.config(text=f"Blue Marbles: {game.num_blue}")
        player_label.config(text=f"Current Player: {game.current_player.value.capitalize()}")

    def human_move():
        try:
            red = int(red_entry.get())
            blue = int(blue_entry.get())
            if game.human_move(red, blue):
                update_display()
                check_game_over()
                game.switch_player()
                if game.current_player == Player.COMPUTER:
                    computer_move()
            else:
                messagebox.showerror("Invalid Move", "Invalid move, try again.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers.")

    def computer_move():
        red, blue = game.computer_move()
        update_display()
        check_game_over()
        game.switch_player()

    def check_game_over():
        if game.is_game_over():
            if game.version == GameVersion.STANDARD:
                result = "You lose!" if game.current_player == Player.HUMAN else "You win!"
            else:
                result = "You win!" if game.current_player == Player.HUMAN else "You lose!"
            messagebox.showinfo("Game Over", f"{result}\nFinal Score: {game.calculate_score()}")
            root.quit()

    root = tk.Tk()
    root.title("Red-Blue Nim Game")

    tk.Label(root, text="Red Marbles:").grid(row=0, column=0, padx=10, pady=10)
    red_label = tk.Label(root, text=f"Red Marbles: {game.num_red}")
    red_label.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Blue Marbles:").grid(row=1, column=0, padx=10, pady=10)
    blue_label = tk.Label(root, text=f"Blue Marbles: {game.num_blue}")
    blue_label.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(root, text="Current Player:").grid(row=2, column=0, padx=10, pady=10)
    player_label = tk.Label(root, text=f"Current Player: {game.current_player.value.capitalize()}")
    player_label.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(root, text="Pick Red:").grid(row=3, column=0, padx=10, pady=10)
    red_entry = tk.Entry(root)
    red_entry.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(root, text="Pick Blue:").grid(row=4, column=0, padx=10, pady=10)
    blue_entry = tk.Entry(root)
    blue_entry.grid(row=4, column=1, padx=10, pady=10)

    tk.Button(root, text="Make Move", command=human_move).grid(row=5, column=0, columnspan=2, pady=20)

    update_display()
    root.mainloop()

def show_config_window():
    def start_game():
        num_red = int(num_red_var.get())
        num_blue = int(num_blue_var.get())
        version = version_var.get()
        first_player = first_player_var.get()
        depth = int(depth_var.get()) if depth_var.get() else None
        root.destroy()
        play_game(num_red, num_blue, version, first_player, depth)

    root = tk.Tk()
    root.title("Red-Blue Nim Game Configuration")

    tk.Label(root, text="Number of Red Marbles:").grid(row=0, column=0, padx=10, pady=10)
    num_red_var = tk.StringVar(value="5")
    tk.Entry(root, textvariable=num_red_var).grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Number of Blue Marbles:").grid(row=1, column=0, padx=10, pady=10)
    num_blue_var = tk.StringVar(value="3")
    tk.Entry(root, textvariable=num_blue_var).grid(row=1, column=1, padx=10, pady=10)

    tk.Label(root, text="Game Version:").grid(row=2, column=0, padx=10, pady=10)
    version_var = tk.StringVar(value="standard")
    tk.OptionMenu(root, version_var, "standard", "misere").grid(row=2, column=1, padx=10, pady=10)

    tk.Label(root, text="First Player:").grid(row=3, column=0, padx=10, pady=10)
    first_player_var = tk.StringVar(value="human")
    tk.OptionMenu(root, first_player_var, "human", "computer").grid(row=3, column=1, padx=10, pady=10)

    tk.Label(root, text="AI Depth (optional):").grid(row=4, column=0, padx=10, pady=10)
    depth_var = tk.StringVar()
    tk.Entry(root, textvariable=depth_var).grid(row=4, column=1, padx=10, pady=10)

    tk.Button(root, text="Start Game", command=start_game).grid(row=5, column=0, columnspan=2, pady=20)

    root.mainloop()

def parse_arguments(args):
    if len(args) < 5:
        print("Usage: python red_blue_nim.py <num-red> <num-blue> <version> <first-player> [depth]")
        sys.exit(1)
    try:
        num_red = int(args[1])
        num_blue = int(args[2])
        version = args[3]
        first_player = args[4]
        depth = int(args[5]) if len(args) > 5 else None
        if version not in [v.value for v in GameVersion]:
            raise ValueError
        if first_player not in [p.value for p in Player]:
            raise ValueError
        return num_red, num_blue, version, first_player, depth
    except ValueError:
        print("Invalid arguments. Usage: python red_blue_nim.py <num-red> <num-blue> <version> <first-player> [depth]")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        num_red, num_blue, version, first_player, depth = parse_arguments(sys.argv)
        play_game(num_red, num_blue, version, first_player, depth)
    else:
        show_config_window()
