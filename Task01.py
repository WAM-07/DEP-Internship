import sys

class RedBlueNim:
    def __init__(self, num_red, num_blue, version, first_player, depth):
        self.num_red = num_red
        self.num_blue = num_blue
        self.version = version
        self.first_player = first_player
        self.depth = depth if depth else float('inf')
        self.current_player = first_player

    def is_game_over(self):
        return self.num_red <= 0 or self.num_blue <= 0

    def evaluate(self):
        return self.num_red * 2 + self.num_blue * 3

    def make_move(self, color, count):
        if color == 'red':
            self.num_red -= count
        elif color == 'blue':
            self.num_blue -= count

    def undo_move(self, color, count):
        if color == 'red':
            self.num_red += count
        elif color == 'blue':
            self.num_blue += count

    def valid_moves(self):
        moves = []
        if self.num_red > 0:
            moves.append(('red', 1))
        if self.num_red > 1:
            moves.append(('red', 2))
        if self.num_blue > 0:
            moves.append(('blue', 1))
        if self.num_blue > 1:
            moves.append(('blue', 2))
        return moves

    def minmax(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_game_over():
            return self.evaluate(), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in self.valid_moves():
                self.make_move(*move)
                eval, _ = self.minmax(depth - 1, alpha, beta, False)
                self.undo_move(*move)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in self.valid_moves():
                self.make_move(*move)
                eval, _ = self.minmax(depth - 1, alpha, beta, True)
                self.undo_move(*move)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def play(self):
        while not self.is_game_over():
            print(f"Red: {self.num_red}, Blue: {self.num_blue}")
            if self.current_player == 'human':
                move = self.get_human_move()
            else:
                _, move = self.minmax(self.depth, float('-inf'), float('inf'), True)
                print(f"Computer picks {move[1]} {move[0]} marbles.")
            self.make_move(*move)
            self.current_player = 'computer' if self.current_player == 'human' else 'human'

        self.display_result()

    def get_human_move(self):
        while True:
            move = input("Enter your move (e.g., 'red 2'): ").split()
            if len(move) != 2:
                print("Invalid input. Try again.")
                continue
            color, count = move[0], int(move[1])
            if (color in ['red', 'blue']) and (count == 1 or count == 2) and ((color == 'red' and self.num_red >= count) or (color == 'blue' and self.num_blue >= count)):
                return color, count
            else:
                print("Invalid move. Try again.")

    def display_result(self):
        if (self.version == 'standard' and (self.num_red == 0 or self.num_blue == 0)) or (self.version == 'misere' and self.num_red > 0 and self.num_blue > 0):
            winner = 'human' if self.current_player == 'computer' else 'computer'
        else:
            winner = self.current_player
        print(f"{winner.capitalize()} wins!")
        print(f"Final score: Red: {self.num_red}, Blue: {self.num_blue}")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python red_blue_nim.py <num-red> <num-blue> <version> <first-player> [depth]")
        sys.exit(1)

    num_red = int(sys.argv[1])
    num_blue = int(sys.argv[2])
    version = sys.argv[3]
    first_player = sys.argv[4]
    depth = int(sys.argv[5]) if len(sys.argv) == 6 else None

    game = RedBlueNim(num_red, num_blue, version, first_player, depth)
    game.play()
