# SOURCE: Adapted from starter code for CPSC 474 Fall 2022 Project 4

from game import Game, State

class Connect4(Game):
    def __init__(self, r=6, c=7):
        ''' Creates a Connect 4 board with the given number of
            rows and columns.
            r -- number of rows
            c -- number of columns
        '''
        self.nrows = r
        self.ncols = c
        self.cols = [[0 for _ in range(self.nrows)] for _ in range(self.ncols)]
        self.turn = 0
            
    def initial_state(self):
        ''' Creates the initial state for the board.
        '''
        return Connect4.State(self, 0)

    
    class State(State):
        def __init__(self, board, turn):
            if board is None:
                raise ValueError('board cannot be None')
            if turn != 0 and turn != 1:
                raise ValueError('invalid turn %d' % turn)
            
            self._board = board
            self._turn = turn            
            # self._compute_hash()

            
        def is_initial(self):
            ''' Determines if this state is the initial state.
            '''
            return (self._board.cols[i][0] == 0 for i in self._board.ncols)

            
        def actor(self):
            ''' Returns the index of the player who makes the next move from
                this state.  The index will be 0 or 1.
            '''
            return self._turn

        
        def is_legal(self, c):
            ''' Determines if placing a disc in the given column is a legal move.
                c -- the index of a column
            '''
            if c < 0 or c >= self._board.ncols:
                raise ValueError('Illegal column %d' % c)

            return self._board.cols[c][self._board.nrows - 1] == 0

        
        def get_actions(self):
            ''' Returns a list of legal moves from this state.
                The list of moves is given as a list of columns to place discs in.
            '''
            return [c for c in range(self._board.ncols) if self.is_legal(c)]
            
        def successor(self, c):
            ''' Returns the state that results from placing a disc in the given column
                from this state.
                c -- the column that the disc will be placed in
            '''
            if not self.is_legal(c):
                raise ValueError('Illegal move: %d' % c)

            succ = Connect4.State(self._board, 1 - self._turn)

            # Place the disk in the given column
            for i in range(succ._board.nrows):
                if succ._board.cols[c][i] == 0:
                    # player 0's discs are encoded as 1, player 1's discs are encoded as 2 (empty is encoded as 0)
                    succ._board.cols[c][i] = self._turn + 1
                    break

            # succ._compute_hash()
                
            return succ

        def _board_filled(self):
            for i in range(self._board.ncols):
                for j in range(self._board.nrows):
                    if self._board.cols[i][j] == 0:
                        return False
            return True

        # TODO: Remember previous move for quicker check?
        # Returns a boolean indicating whether the game is over as well as the winner
        # 0 for draw, 1 for player 0 win, 2 for player 1 win
        def _game_over(self):
            # Check if the board is full
            if self._board_filled():
                return True, 0

            # Check for a four-line of tokens of the same color
            for i in range(self._board.ncols):
                for j in range(self._board.nrows):
                    # Check if there is enough horizontal space 
                    if i <= self._board.ncols - 4:
                        # Check upper diagonal if valid
                        if j <= self._board.nrows - 4:
                            color = self._board.cols[i][j]
                            line = True
                            for a in range(3):
                                if self._board.cols[i + a + 1][j + a + 1] != color:
                                    line = False
                                    break
                            if line:
                                return True, color
                        
                        # Check lower diagonal if valid
                        if j >= 3:
                            color = self._board.cols[i][j]
                            line = True
                            for a in range(3):
                                if self._board.cols[i + a + 1][j - a - 1] != color:
                                    line = False
                                    break
                            if line:
                                return True, color

                        # Check horizontal
                        color = self._board.cols[i][j]
                        line = True
                        for a in range(3):
                            if self._board.cols[i + a + 1][j] != color:
                                line = False
                                break
                        if line:
                            return True, color
                
                    # Check vertical if valid
                    if j <= self._board.nrows - 4:
                        color = self._board.cols[i][j]
                        line = True
                        for a in range(3):
                            if self._board.cols[i][j + a + 1] != color:
                                line = False
                                break
                        if line:
                            return True, color

            return False, 0
        
        def is_terminal(self):
            ''' Determines if this state is terminal -- whether the game is over having
                reached this state.
            '''
            game_over, _ = self._game_over()
            return game_over

        def payoff(self):
            ''' Returns the payoff to player 0 at this state: 1 for a win, 0 for a draw, -1 for
                a loss.  The return value is None if this state is not terminal.
            '''
            game_over, winner = self._game_over()
            if game_over:
                return (winner == 1) - (winner == 2)
            else:
                return None
            
        def __str__(self):
            board_str = ""
            for i in range(self._board.nrows):
                for j in range(self._board.ncols):
                    board_str += str(self._board.cols[j][self._board.nrows - 1 - i]) + " "
                board_str += "\n"
            return board_str


        # def __repr__(self):
        #     return "" 

        
        # def _compute_hash(self):
        #     # faster hash computation; thanks to CF
        #     self.hash = hash(tuple(self._board.cols)) * 2 + self._turn

            
        def __hash__(self):
            return self.hash

        
        def __eq__(self, other):
            return isinstance(other, self.__class__) and self._seeds == other._seeds and self._turn == other._turn and self._board is other._board


if __name__ == '__main__':
    board = Connect4()
    pos = board.initial_state()
    print(pos)
    pos = pos.successor(0)
    print(pos)
    pos = pos.successor(1)
    print(pos)
    pos = pos.successor(1)
    print(pos)
    pos = pos.successor(2)
    pos = pos.successor(1)
    pos = pos.successor(3)
    pos = pos.successor(1)
    pos = pos.successor(4)
    pos = pos.successor(1)
    print(pos)
    print(pos.is_terminal())
   