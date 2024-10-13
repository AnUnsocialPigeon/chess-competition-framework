import subprocess
import sys
import os
from datetime import datetime
import chess
import chess.pgn

# Get bot locations
if len(sys.argv) != 3:
    print("Invalid arguments. Please give 2 args of the local files to the bots")
    exit(1)

bot1_location = sys.argv[1]
bot2_location = sys.argv[2]

failureString = "Lost"
chess_state = chess.Board()
move_log = []
fen_log = [chess_state.fen()]

if not (os.path.isfile(bot1_location) and os.path.isfile(bot2_location)):
    print("Invalid bot location.")
    exit(1)


def playGame():
    """Play a game between 2 bots. Returns 1 for bot 1 win, 2 for bot 2 win, or 0 for draw"""

    while True:
        winner = playTurn(chess_state, bot1_location)
        if winner != 0:
            return winner % 3
        
        winner = playTurn(chess_state, bot2_location)
        if winner != 0:
            return winner % 3


def playTurn(chess_state: chess.Board, bot_location: str):
    """Play a single turn of chess. Returns 0 for continue, 1 for white won, 2 for black won, 3 for draw"""
    outcome = runBot(chess_state.fen(), bot_location).strip().split('\n')[-1]   # Take just the last output

    if outcome == failureString:
        print("Failed.")
        return 2
    
    move = checkMoveValidity(chess_state.fen(), outcome)
    if move == "": 
        print("Invalid move.")
        return 2
    
    # Play the move - must be logged
    move_log.append(move.uci())
    chess_state.push(move)
    fen_log.append(chess_state.fen())


    return gameState(chess_state)


def gameState(chess_state: chess.Board):
    """Returns the game state. 0 for continue, 1 for white won, 2 for black won, 3 for draw"""
    if chess_state.is_checkmate():
        if chess_state.turn == chess.WHITE:
            print("Black won")
            return 2
        else:
            print("White won")
            return 1
    elif chess_state.is_stalemate():
        print("Draw (Stalemate)")
        return 3
    elif chess_state.is_insufficient_material():
        print("Draw (Insufficient Material)")
        return 3
    elif chess_state.is_fifty_moves():
        print("Draw (50-move rule)")
        return 3
    elif chess_state.is_fivefold_repetition():
        print("Draw (Fivefold Repetition)")
        return 3
    elif chess_state.is_variant_draw():
        print("Draw (Variant)")
        return 3
    elif chess_state.is_game_over():
        print("Draw")
        return 3
    else:
        #print("Game continues")
        return 0


def runBot(game_state: str, bot_file: str):
    """Runs a single round between 2 bots"""
    bot_file = bot_file.split('/')[-1]
    print(f"Running {bot_file} with {game_state}")

    bot = subprocess.Popen(
        ["python3", bot_file],
        stdin=subprocess.PIPE,                
        stdout=subprocess.PIPE,               
        stderr=subprocess.PIPE,               
        text=True,                 
        cwd="./bots"
    )
    
    try:
        stdout, stderr = bot.communicate(game_state, timeout=5)  # Change this to edit timeout.
        if stderr:
            return failureString
        return stdout

    except subprocess.TimeoutExpired:
        print(f"{bot_file} did not finish in time, terminating...")
        bot.kill()
        bot.wait()
        print(f"{bot_file} terminated.")
    return failureString


def checkMoveValidity(initial_fen: str, next_fen: str):
    """Checks the validity between 2 fen states"""
    hypothetical_chess = chess.Board(initial_fen)
    legal_moves = list(hypothetical_chess.legal_moves)

    # Sanitise
    next_fen = next_fen.strip()

    for move in legal_moves:
        future_board = hypothetical_chess.copy()
        future_board.push(move)

        if future_board.fen().strip() == next_fen:
            return move
    
    return ""


def saveGame(round: int):
    """Save the game log to a PGN file"""
    game = chess.pgn.Game()


    # Set relevant PGN headers
    game.headers["Event"] = "Warwick AI chess competition"
    game.headers["Site"] = "Online"
    game.headers["Date"] = datetime.now().strftime("%Y.%m.%d")
    game.headers["Round"] = str(round)
    game.headers["White"] = bot1_location   
    game.headers["Black"] = bot2_location

    node = game

    for move in move_log:
        uci_move = chess.Move.from_uci(move)
        node = node.add_main_variation(uci_move)
    
    file_location = f"logs/{bot1_location.split('/')[-1].split('\\')[-1]} vs {bot2_location.split('/')[-1].split('\\')[-1]} round {round}"

    # Export the game to a PGN file
    with open(f"{file_location}.pgn", "w") as pgn_file:
        print(game, file=pgn_file)

    # Export fen to a log file
    with open(f"{file_location}.log", "w") as log_file:
        for fen in fen_log:
            print(fen, file=log_file)

    print(f"Game saved to \"{file_location}\"")


if __name__ == "__main__":
    winner = playGame()
    saveGame(1)

