import chess
import random

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 100
}

def prioritize_moves(board):
    legal_moves = list(board.legal_moves)
    
    # Can we checkmate?
    for move in legal_moves:
        board.push(move)
        if board.is_checkmate():
            board.pop()
            return move
        board.pop()
    
    # Can we check by capture?
    capture_checks = []
    for move in legal_moves:
        if board.is_capture(move):  
            board.push(move)
            if board.is_check():  
                capture_checks.append(move)
            board.pop()
    if capture_checks:
        return random.choice(capture_checks)
    
    # Can we check?
    for move in legal_moves:
        board.push(move)
        if board.is_check():
            board.pop()
            return move  
        board.pop()

    # Can we capture? (highest value = priority)
    captures = []
    for move in legal_moves:
        if board.is_capture(move):
            captured_piece = board.piece_at(move.to_square)
            if captured_piece is not None:
                captures.append((move, PIECE_VALUES.get(captured_piece.piece_type, 0)))
    if captures:
        captures.sort(key=lambda x: x[1], reverse=True)
        return captures[0][0]  
    
    # Else, random move
    return random.choice(legal_moves)


# Take in input
fen_input = input()
board = chess.Board(fen_input)

print(f"Agressive bot got: {fen_input}")

# Get the best move according to our priorities
best_move = prioritize_moves(board)

print(f"I'm gonna do {best_move}")

# Apply the chosen move
board.push(best_move)
print(board.fen())  # The last print statement of the bot must be purely the FEN string of the resulting board.

