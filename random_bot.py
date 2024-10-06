import chess
import random

# Get FEN string
fen_input = input()
board = chess.Board(fen_input)

print(f"Random bot got: {fen_input}")

# Get all legal moves and pick one at random
legal_moves = list(board.legal_moves)
random_move = random.choice(legal_moves)

print(f"I'm gonna do {random_move}")

# Apply the random move
board.push(random_move)
print(board.fen())

