import sys
import chess
import chess.pgn

if len(sys.argv) != 3:
    print("Invalid arguments. Please give 2 args. One input, one output.")
    exit(1)

pgn_file = sys.argv[1]
output_file = sys.argv[2]

pgn = open(pgn_file)
game = chess.pgn.read_game(pgn)
board = game.board()

with open(output_file, "w") as f:
    for move_number, move in enumerate(game.mainline_moves(), start=1):
        board.push(move)
        f.write(f"{board.fen()}\n")

print(f"FEN strings have been saved to '{output_file}'.")

