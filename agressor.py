import chess
import random

# Piece values for determining which piece to capture, based on standard chess piece values.
# The higher the value, the more desirable to capture
PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 100  # You can't really capture the king, but it's there for reference.
}

# Function to prioritize moves based on checkmate, checks, and captures
def prioritize_moves(board):
    legal_moves = list(board.legal_moves)
    
    # First, check if we can deliver checkmate
    for move in legal_moves:
        board.push(move)
        if board.is_checkmate():
            board.pop()
            return move  # Immediate checkmate is the highest priority
        board.pop()
    
    # Second, look for checks by capturing a piece
    capture_checks = []
    for move in legal_moves:
        if board.is_capture(move):  # Check if it's a capture
            board.push(move)
            if board.is_check():  # Check if it also delivers check
                capture_checks.append(move)
            board.pop()
    if capture_checks:
        # If there are any capture checks, return one at random (could improve by choosing highest-value capture)
        return random.choice(capture_checks)

    # Third, prioritize moves that capture the highest value piece
    captures = []
    for move in legal_moves:
        if board.is_capture(move):
            captured_piece = board.piece_at(move.to_square)
            if captured_piece is not None:
                captures.append((move, PIECE_VALUES.get(captured_piece.piece_type, 0)))
    
    if captures:
        # Sort captures by piece value and return the highest one
        captures.sort(key=lambda x: x[1], reverse=True)
        return captures[0][0]  # Return the move that captures the most valuable piece

    # Fourth, prioritize checks (without capturing)
    for move in legal_moves:
        board.push(move)
        if board.is_check():
            board.pop()
            return move  # Deliver check if possible
        board.pop()

    # Finally, if none of the above, just return a random move
    return random.choice(legal_moves)

# Get FEN string
fen_input = input()
board = chess.Board(fen_input)

print(f"Improved bot got: {fen_input}")

# Get the best move according to our priorities
best_move = prioritize_moves(board)

print(f"I'm gonna do {best_move}")

# Apply the chosen move
board.push(best_move)
print(board.fen())  # The last print statement of the bot must be purely the FEN string of the resulting board.
