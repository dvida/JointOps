import itertools
import string

# Board representation:
# Board is represented as an vector with N elements ranging from 0 to N-1, e.g. [4 0 3 2 1 5 7 6], where individual numbers in the vector represent queen's column

class Queens():
    def __init__(self, N):
        self.N = N
        self.alphabeth = string.uppercase[:self.N]
        self.board_list = itertools.permutations(range(self.N))

        self.solution_count = None
        self.solutions = []

    def solve(self):
        """ Find all solutions given the board size. """

        self.solution_count = 0

        for board in self.board_list:
            if self.checkQueens(board):

                self.solutions.append(board)
                self.solution_count += 1

        print 'Solutions: ', self.solution_count

    def checkQueens(self, board):
        """ Check the board if the queens don't eat each other. """
        for i, queen in enumerate(board):
            for j, other in enumerate(board):

                # Skip same queen
                if queen == other:
                    continue

                # Check diagonal
                if (abs(queen-other) == abs(i-j)):
                    return False

        return True

    def displayBoard(self, index):
        """ Display formated board. """

        if index > self.solution_count:
            print 'Board index out of range!'

        board = self.solutions[index]
        print 'Board:', self.formatBoardVector(board)

        board_display = []
        board_display.append('   ' + ' '.join(self.alphabeth))

        for i, queen in enumerate(board):
            row = ['| ']*self.N
            row[queen] = '|Q'
            row.append('|')
            row_no = str(abs(i-self.N))
            board_display.append(row_no+' '+''.join(row)+' '+row_no)

        board_display.append('   ' + ' '.join(self.alphabeth))
        board_display.append('---' + '--' * self.N + '--')

        for row in board_display:
            print row

    def formatBoardVector(self, board):
        """ Formats board vector to standard chess positions. """
        formated_board = []
        for i, queen in enumerate(board):
            row = abs(self.N - i)
            column = self.alphabeth[queen]

            formated_board.append(column+str(row))

        return ' '.join(sorted(formated_board))


    def displayAllSolutions(self):
        """ Displays all solutions. """

        for index in range(self.solution_count):
            self.displayBoard(index)


queens = Queens(8) # Initialize with number of queens and board size
queens.solve()  # Find all solutions
queens.displayAllSolutions()  # Display all solutions

#queens.displayBoard(0)  # Display first solution