"""
Pydantic models for chess game representation.
"""
from typing import List, Optional, Literal, Tuple
from pydantic import BaseModel, Field, validator

class Position(BaseModel):
    """Represents a position on the chessboard."""
    row: int = Field(..., ge=0, le=7, description="Row index (0-7)")
    col: int = Field(..., ge=0, le=7, description="Column index (0-7)")
    
    def to_tuple(self) -> Tuple[int, int]:
        """Convert to tuple representation."""
        return (self.row, self.col)
    
    def to_algebraic(self) -> str:
        """Convert to algebraic notation (e.g., 'e4')."""
        return f"{chr(self.col + ord('a'))}{8 - self.row}"
    
class Piece(BaseModel):
    """Represents a chess piece."""
    color: Literal['white', 'black']
    type: Literal['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
    
    def __str__(self) -> str:
        """Get the standard algebraic notation for the piece."""
        piece_map = {
            'pawn': 'P',
            'rook': 'R', 
            'knight': 'N',
            'bishop': 'B',
            'queen': 'Q',
            'king': 'K'
        }
        symbol = piece_map[self.type]
        return symbol.lower() if self.color == 'white' else symbol

class PieceMove(BaseModel):
    """Represents a chess piece move."""
    piece: Piece
    from_position: Position
    to_position: Position
    
    def __str__(self) -> str:
        """Get standard algebraic notation for the move."""
        piece_str = str(self.piece).upper()
        # Don't include pawn symbol for pawn moves
        if self.piece.type == 'pawn':
            piece_str = ''
        return f"{piece_str}{self.from_position.to_algebraic()}{self.to_position.to_algebraic()}"



class Chessboard(BaseModel):
    """Represents a chessboard with pieces."""
    board: List[List[Optional[Piece]]] = Field(
        ..., 
        description="8x8 grid representing the chessboard. None for empty squares."
    )
    
    def validate_board_dimensions(cls, v):
        """Ensure the board is 8x8."""
        if len(v) != 8 or any(len(row) != 8 for row in v):
            raise ValueError('Chessboard must be 8x8')
        return v
    
    def get_piece(self, position: Position) -> Optional[Piece]:
        """Get piece at a given position."""
        return self.board[position.row][position.col]
    

    
    def display(self) -> str:
        """Get a string representation of the board with column and row labels."""
        rows = []
        
        # Column labels
        rows.append('  A B C D E F G H')
        rows.append(' +-----------------+')
        
        # Board rows with numbers
        for i, row in enumerate(reversed(self.board)):  # Reverse to show row 1 at bottom
            display_row = []
            for piece in row:
                if piece is None:
                    display_row.append('.')
                else:
                    display_row.append(str(piece))
            rows.append(f'{8-i} | {' '.join(display_row)} |')
        
        rows.append(' +-----------------+')
        rows.append('  A B C D E F G H')
        
        return '\n'.join(rows)
    
    @classmethod
    def create_initial_board(cls) -> 'Chessboard':
        """Create a chessboard with the standard initial position."""
        board = [[None for _ in range(8)] for _ in range(8)]
        
        # Place black pieces
        board[0] = [
            Piece(color='black', type='rook'),
            Piece(color='black', type='knight'),
            Piece(color='black', type='bishop'),
            Piece(color='black', type='queen'),
            Piece(color='black', type='king'),
            Piece(color='black', type='bishop'),
            Piece(color='black', type='knight'),
            Piece(color='black', type='rook')
        ]
        board[1] = [Piece(color='black', type='pawn')] * 8
        
        # Place white pieces
        board[6] = [Piece(color='white', type='pawn')] * 8
        board[7] = [
            Piece(color='white', type='rook'),
            Piece(color='white', type='knight'),
            Piece(color='white', type='bishop'),
            Piece(color='white', type='queen'),
            Piece(color='white', type='king'),
            Piece(color='white', type='bishop'),
            Piece(color='white', type='knight'),
            Piece(color='white', type='rook')
        ]
        
        return cls(board=board)

# Example usage
if __name__ == "__main__":
    # Create initial board
    board = Chessboard.create_initial_board()
    print("Initial board position:")
    print(board.display())
    print()
    
